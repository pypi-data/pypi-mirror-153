import boto3
import pkg_resources

from ..utils.constants import EXTENSION_NAME


class ResourceMetadata:
    DOMAIN = "amazonaws.com"
    # China regions use different domain: https://docs.amazonaws.cn/en_us/aws/latest/userguide/endpoints-Ningxia.html
    CHINA_DOMAIN = "amazonaws.com.cn"
    CHINA_REGION_PREFIX = "cn-"

    def __init__(self):
        try:
            self.library_version = pkg_resources.require(EXTENSION_NAME)[0].version
        except Exception as e:
            self.library_version = "UNKNOWN"

        try:
            self.__boto_session = boto3.session.Session()
            self.__region_name = self.__boto_session.region_name
            if self.__region_name.startswith(ResourceMetadata.CHINA_REGION_PREFIX):
                regional_sts_endpoint = (
                    f"https://sts.{self.__region_name}.{ResourceMetadata.CHINA_DOMAIN}"
                )
            else:
                regional_sts_endpoint = (
                    f"https://sts.{self.__region_name}.{ResourceMetadata.DOMAIN}"
                )
            self.__regional_sts_client = boto3.client(
                "sts",
                endpoint_url=regional_sts_endpoint,
                region_name=self.__region_name,
            )
            self.account_id = self.__regional_sts_client.get_caller_identity().get(
                "Account"
            )
        except Exception as e:
            # Fallback on global endpoint
            self.account_id = boto3.client("sts").get_caller_identity().get("Account")
