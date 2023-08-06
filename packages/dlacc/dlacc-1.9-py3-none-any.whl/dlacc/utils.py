from google.cloud import storage
from pathlib import Path
import os
import json
import re
import glob
import numpy as np
import onnx

from .base_class import BaseClass
from .metadata import ModelType, platformType, input_prefix, output_prefix

def get_traced_model(
    origin_model, example_inputs, save_path=None, model_name="default_network_name"
):
    import torch

    print("Generate jit traced model...")
    example_inputs = tuple(example_inputs.values())
    model_name = networkname_to_path(model_name)
    traced_model = torch.jit.trace(origin_model, example_inputs=example_inputs).eval()
    if save_path:
        path = save_path + "jit_traced_%s.pt" % (model_name)
        torch.jit.save(traced_model, path)
        print("%s saved." % path)
    print("Jit traced model generation success.")
    return traced_model


def get_input_info_hf(traced_model):
    shape_list = [
        (i.debugName().split(".")[0], i.type().sizes())
        for i in list(traced_model.graph.inputs())[1:]
    ]
    batch_size = shape_list[0][1][0]
    return batch_size, shape_list


def from_hf_pretrained(network_name):
    from transformers import AutoTokenizer, AutoModel

    tokenizer = AutoTokenizer.from_pretrained(
        network_name, TOKENIZERS_PARALLELISM=False
    )  # uggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks
    model = AutoModel.from_pretrained(network_name, return_dict=False)
    return tokenizer, model


def infer_platform_type(model_path: str):
    if model_path.startswith("gs://"):
        return platformType.GOOGLESTORAGE
    else:
        return platformType.LOCAL


def networkname_to_path(network_name):
    return network_name.replace("/", "_")


def get_bucket_object_name(url: str):
    matches = re.match("gs://(.*?)/(.*)", url)
    if matches:
        bucket, object_name = matches.groups()
    else:
        raise Exception("invalid url pattern")
    return bucket, object_name


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # source_blob_name = "storage-object-name"
    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)
    print(
        f"{destination_blob_name} with contents {contents} has been uploaded to {bucket_name}."
    )


def upload_blobs_from_directory(
    directory_path: str, dest_bucket_name: str, dest_blob_name: str
):
    storage_client = storage.Client()
    rel_paths = glob.glob(directory_path + "/**", recursive=True)
    bucket = storage_client.bucket(dest_bucket_name)
    for local_file in rel_paths:
        remote_path = f'{dest_blob_name}/{"/".join(local_file.split(os.sep)[2:])}'
        if os.path.isfile(local_file):
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)

    print(
        f"Folder: {directory_path} has been uploaded to {dest_bucket_name}/{dest_blob_name}."
    )


def download_file_from_gcp(url, dst_folder, dst_name: str):
    output_dir = Path(dst_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    bucket_name, blob_name = get_bucket_object_name(url)
    destination_file_name = f"{dst_folder}/{dst_name}"
    download_blob(bucket_name, blob_name, destination_file_name)

    return destination_file_name


def upload_outputs(bucket_name, blob_name, platform_type):
    if platform_type == platformType.GOOGLESTORAGE:
        upload_blobs_from_directory(output_prefix, bucket_name, blob_name)
        upload_blob_from_memory(bucket_name, "OK", f"{blob_name}/success")
    else:
        raise NotImplementedError


def contruct_dummy_input(input_shape, input_dtype, tensor_type, device="cuda"):
    import numpy as np

    if tensor_type == "pt":
        import torch

        dummy_input = tuple(
            [
                torch.randn(*v).type(
                    {
                        "int32": torch.int32,
                        "int64": torch.int64,
                        "float32": torch.float32,
                        "float64": torch.float64,
                    }[input_dtype[k]]
                )
                for k, v in input_shape.items()
            ]
        )
    elif tensor_type == "tf":
        import tensorflow as tf

        dummy_input = [
            tf.TensorSpec(
                v,
                {
                    "int32": tf.int32,
                    "int64": tf.int64,
                    "float32": tf.float32,
                    "float64": tf.float64,
                }[input_dtype[k]],
                name="x",
            )
            for k, v in input_shape.items()
        ]
    else:
        dummy_input = dict(
            [
                (k, np.random.rand(*v).astype(input_dtype[k]))
                for k, v in input_shape.items()
            ]
        )
    return dummy_input


def convert2onnx(platform_type, model_path, model_type, input_shape, input_dtype):
    file_path = None
    if platform_type == int(platformType.LOCAL):
        file_path = model_path
    elif platform_type == int(platformType.GOOGLESTORAGE):
        file_path = download_file_from_gcp(
            model_path, input_prefix, model_path.split("/")[-1]
        )
    else:
        raise NotImplementedError
    if file_path:
        model = None
        onnx_model = None
        if model_type == int(ModelType.PT):
            raise NotImplementedError
            # import torch
            # import sys
            # sys.path.insert(0, '/home/mac_yuan/repo/RecSys_PyTorch/saves/')
            # print(file_path)
            # model = torch.load(file_path)
            # model.eval()
            # dummy_input = contruct_dummy_input(input_shape, input_dtype, "pt")
            # torch.onnx.export(model, dummy_input, onnx_path, verbose=True)
        elif model_type == int(ModelType.TF):
            # import tensorflow as tf
            # tf.saved_model.load(file_path, tags='serve')
            # os.system("python3.9 -m tf2onnx.convert --saved-model %s --output %s" % (file_path, './inputs/model.onnx'))
            raise NotImplementedError
        elif model_type == int(ModelType.ONNX):
            pass
    if not onnx_model:
        onnx_model = onnx.load(file_path)
        os.system("cp %s inputs/model.onnx" % file_path)
    return onnx_model


class JSONConfig(BaseClass):
    def __init__(self, json_path, platform_type) -> None:
        self.load(json_path, platform_type)

    def load(self, json_path, platform_type):
        path = input_prefix + "/" + json_path
        if platform_type == platformType.GOOGLESTORAGE:
            path = download_file_from_gcp(json_path, input_prefix, "config.json")
        elif platform_type == platformType.AWSSTORAGE:
            raise NotImplementedError
        with open(path) as json_file:
            self.meta = json.load(json_file)

    def __getitem__(self, key):
        return self.meta[key]


class JSONOutput(BaseClass):
    def __init__(self, json_config: JSONConfig):
        self.meta = json_config.meta

    def save(self, file_path):
        with open(file_path, "w") as outfile:
            json.dump(self.meta, outfile)

    def __getitem__(self, key):
        return self.meta[key]

    def __setitem__(self, key, value):
        self.meta[key] = value
        self.save(output_prefix + "/output_json.json")
