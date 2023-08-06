import os

import setuptools

NAME = "sagemaker-studio-analytics-extension"
AUTHOR = "Amazon Web Services"
DESCRIPTION = "SageMaker Studio Analytics Extension"
LICENSE = "Apache 2.0"
URL = "https://aws.amazon.com/sagemaker"
README = "README.md"
VERSION = "0.0.9"
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

INSTALL_REQUIRES = [
    "boto3>=1.10.44, < 2.0",
    "sparkmagic>=0.19.0",
    "sagemaker_studio_sparkmagic_lib>=0.1.1",
    "filelock>=3.0.12",
]
ENTRY_POINTS = {
    "console_scripts": [
        "sm_analytics_runtime_check=sagemaker_studio_analytics_extension.utils.runtime_check:main"
    ]
}

HERE = os.path.dirname(__file__)


def read(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.read()


LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        version=VERSION,
        package_dir={"": "src"},
        packages=[
            "sagemaker_studio_analytics_extension",
            "sagemaker_studio_analytics_extension/utils",
            "sagemaker_studio_analytics_extension/magics",
            "sagemaker_studio_analytics_extension/resource/",
            "sagemaker_studio_analytics_extension/resource/emr/",
        ],
        author=AUTHOR,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        include_package_data=True,
    )
