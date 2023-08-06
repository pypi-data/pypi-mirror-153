# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from enum import Enum

LIBRARY_NAME = "sagemaker-analytics"
EXTENSION_NAME = "sagemaker_studio_analytics_extension"


class SERVICE(str, Enum):
    EMR = "emr"

    @staticmethod
    def list():
        return list(map(lambda s: s.value, SERVICE))


class OPERATION(str, Enum):
    CONNECT = "connect"

    @staticmethod
    def list():
        return list(map(lambda s: s.value, OPERATION))


## Logging
SAGEMAKER_ANALYTICS_LOG_BASE_DIRECTORY = "/var/log/studio/sagemaker_analytics"
