import io
from setuptools import find_packages
import os
from setuptools import setup

def read(fname):
    return open(fname).read()

setup(
    name="dlacc",
    version=1.5,
    url="https://gitlab.gnomondigital.com/fzyuan/dl_acceleration",
    project_urls={},
    license="Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)",
    author="gnomondigital",
    author_email="contact@gnomondigital.com",
    description="A simple framework for accelerating deep learning inference runtime.",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "onnx",
        "onnxruntime",
        "pandas",
        "google-cloud-storage",
        "tvm"
    ],
)