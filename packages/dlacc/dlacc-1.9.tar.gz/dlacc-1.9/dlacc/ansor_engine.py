import tvm
from tvm import auto_scheduler
import tvm.relay as relay
from tvm.contrib import graph_executor
import numpy as np
import timeit
import onnxruntime as ort
import pandas as pd
from pathlib import Path

from .metadata import output_prefix, input_prefix
from .base_class import BaseClass

class AnsorEngine(BaseClass):
    def __init__(
        self, network_name, traced_model, target, input_shape, input_dtype, out_json
    ) -> None:
        self.network_name = network_name.replace("/", "_")
        mod, params = relay.frontend.from_onnx(
            traced_model, shape=input_shape, dtype=input_dtype
        )
        self.mod = mod
        self.params = params
        self.out_json = out_json
        self.target = target
        self.input_shape = input_shape
        self.input_dtype = input_dtype
        self.onnx_model = traced_model

    def ansor_run_tuning(self, num_measure_trials=500, verbose=0):
        self._print("Run tuning for network=%s" % self.network_name)

        self.log_file = output_prefix + (
            "/tuninglog_network_name=%s--target=%s.json"
            % (self.network_name, str(self.target))
        )

        self._print("Extract tasks...")
        tasks, task_weights = auto_scheduler.extract_tasks(
            self.mod["main"], self.params, self.target
        )

        self._print("Begin tuning...")
        tuner = auto_scheduler.TaskScheduler(tasks, task_weights)
        tune_option = auto_scheduler.TuningOptions(
            num_measure_trials=num_measure_trials,  # change this to 20000 to achieve the best performance
            runner=auto_scheduler.LocalRunner(
                repeat=10, enable_cpu_cache_flush=True, timeout=40
            ),
            early_stopping=300,
            measure_callbacks=[auto_scheduler.RecordToFile(self.log_file)],
            verbose=verbose,
        )
        use_sparse = False
        if use_sparse:
            from tvm.topi.sparse.utils import sparse_sketch_rules

            search_policy = [
                auto_scheduler.SketchPolicy(
                    task,
                    program_cost_model=auto_scheduler.XGBModel(),
                    init_search_callbacks=sparse_sketch_rules(),
                )
                for task in tasks
            ]

            tuner.tune(tune_option, search_policy=search_policy)
        else:
            tuner.tune(tune_option)
        # mark log as finished
        p = Path(self.log_file)
        name_without_extension = p.stem
        ext = p.suffix
        new_file_name = f"{name_without_extension}_finished"
        p.rename(Path(p.parent, new_file_name + ext))
        self.log_file = str(p.parent) + "/" + new_file_name + ext
        self._print("Tuning Success, configuration file saved at %s" % self.log_file)
        self.out_json["status"] = 2
        self.ansor_compile(self.log_file)
        return self

    def ansor_compile(self, log_file=None):
        output_path = output_prefix + "/optimized_model"
        if log_file:
            self.log_file = log_file
        self._print("Compile from %s" % self.log_file)
        with auto_scheduler.ApplyHistoryBest(self.log_file):
            with tvm.transform.PassContext(
                opt_level=3, config={"relay.backend.use_auto_scheduler": True}
            ):
                graph, lib, graph_params = relay.build(
                    self.mod, target=self.target, params=self.params
                )
        Path(output_path).mkdir(parents=True, exist_ok=True)
        self._save(output_path, lib, graph, graph_params)
        self.device = tvm.device(str(self.target), 0)
        self.module = graph_executor.create(graph, lib, self.device)
        self._print("Compile success.")
        self.out_json["status"] = 3
        return self

    def _save(self, output_path, lib, graph, params):
        lib.export_library(output_path + "/deploy_lib.tar")
        with open(output_path + "/deploy_graph.json", "w") as fo:
            fo.write(graph)
        with open(output_path + "/deploy_param.params", "wb") as fo:
            fo.write(relay.save_param_dict(params))

    def evaluate(self):
        self._print("Evaluate inference time cost...")
        timing_results = self.module.benchmark(
            self.device, repeat=5, number=10, end_to_end=True
        )
        dummy_input = dict(
            [
                (k, np.random.rand(*v).astype(self.input_dtype[k]))
                for k, v in self.input_shape.items()
            ]
        )
        ort_sess = ort.InferenceSession(input_prefix + "/model.onnx")
        to_comp = (
            np.array(
                timeit.Timer(lambda: ort_sess.run(None, dummy_input)).repeat(
                    repeat=5, number=10
                )
            )
            / 10
        )
        prof_res = np.array(timing_results.results) * 1000
        to_comp_res = to_comp * 1000
        df_optimized = pd.DataFrame(prof_res).describe()
        df_original = pd.DataFrame(to_comp_res).describe()
        result_df = pd.concat([df_optimized, df_original], axis=1)
        result_df.columns = ["optimized", "original"]
        result_df.to_csv(output_prefix + "/inference_time.csv")
