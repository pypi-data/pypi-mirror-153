import io
from setuptools import find_packages
from setuptools import setup

setup(
    name="dlacc",
    version=1.3,
    url="https://gitlab.gnomondigital.com/fzyuan/dl_acceleration",
    project_urls={},
    license="Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)",
    author="gnomondigital",
    author_email="contact@gnomondigital.com",
    description="A simple framework for accelerating deep learning inference runtime.",
    long_description="readme.md",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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