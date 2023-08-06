# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import print_function

import contextlib
import io
import json
import logging
import os
import subprocess
import sys
from time import sleep
from uuid import uuid4

import IPython
import botocore
import filelock
from IPython import get_ipython
from IPython.core.display import display
from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
)
from IPython.core.magic_arguments import magic_arguments, argument, parse_argstring
import sparkmagic.utils.configuration as conf
from ..resource.emr.auth import ClusterSessionCredentialsProvider
from ..utils.boto_client_utils import get_boto3_session
from ..utils.constants import (
    LIBRARY_NAME,
    SERVICE,
    OPERATION,
    SAGEMAKER_ANALYTICS_LOG_BASE_DIRECTORY,
)
from ..utils.service_metrics import (
    records_service_metrics,
)
from ..utils.logging_utils import ServiceFileLogger

from ..utils.emr_constants import (
    IPYTHON_KERNEL,
    MAGIC_KERNELS,
    LANGUAGES_SUPPORTED,
    AUTH_TYPE_SET,
    KRB_FILE_PATH,
    SPARK_SESSION_NAME_PREFIX,
    INSTANCE_COLLECTION_TYPE_GROUP,
    LIVY_DEFAULT_PORT,
    AUTH_TYPE_NONE,
    AUTH_TYPE_KERBEROS,
    AUTH_TYPE_BASIC_ACCESS,
    EMR_CONNECTION_LOG_FILE,
)
from ..utils.resource_check import check_host_and_port, is_ssl_enabled
from ..utils.arn_util import RoleArnValidator

# The class MUST call this class decorator at creation time
# https://ipython.readthedocs.io/en/stable/config/custommagics.html
from ipywidgets import widgets
from requests_kerberos import REQUIRED
from sagemaker_studio_sparkmagic_lib.emr import EMRCluster
from sagemaker_studio_sparkmagic_lib.kerberos import write_krb_conf

# This logger emits logs to sys.stdout, which is visible in customer's notebook in Studio
sys_out_logger = logging.getLogger(__name__)
sys_out_logger.setLevel(logging.INFO)
sys_out_logger.addHandler(logging.StreamHandler(sys.stdout))

sagemaker_analytics_service_logger = None


def _magic_kernel_connect_to_emr(
    emr_client, args, emr_cluster, username, password, kernel_name
):
    """
    Handles connectivity to EMR clusters from PySpark and SparkScala kernels
    """
    print("Initiating EMR connection..")
    ipy = get_ipython()
    _run_preset_cell_magics(ipy)

    endpoint_magic_line = _get_endpoint_magic_line(
        emr_client, args, emr_cluster, username, password, kernel_name
    )

    _handle_kerberos_endpoint_override(emr_cluster=emr_cluster)

    # Pass the livy endpoint to connect to, through the internal cell magic without spark.conf
    change_endpoint_magic = ipy.find_line_magic("_do_not_call_change_endpoint")
    change_endpoint_magic(endpoint_magic_line)

    # Start spark session
    start_session_magic = ipy.find_cell_magic("_do_not_call_start_session")
    error_message = None
    session_started = start_session_magic("")
    if not session_started:
        error_message = "Failed to start spark session."

    _echo_response_to_iopub_web_socket(
        _build_response(
            cluster_id=args.cluster_id,
            error_message=error_message,
            success=session_started,
            service="emr",
            operation="connect",
        )
    )


def _get_endpoint_magic_line(
    emr_client, args, emr_cluster, username, password, kernel_name
):
    livy_host = emr_cluster.primary_node_private_dns_name()
    livy_port = _get_livy_port(
        args=args, emr_client=emr_client, emr_cluster=emr_cluster
    )

    livy_endpoint = _prepare_livy_endpoint(livy_host, int(livy_port))
    if kernel_name in MAGIC_KERNELS:
        return _get_magic_kernel_endpoint_magic_line(
            args=args,
            livy_endpoint=livy_endpoint,
            username=username,
            password=password,
        )

    return _get_ipython_kernel_endpoint_magic_line(
        args=args,
        livy_endpoint=livy_endpoint,
        username=username,
        password=password,
    )


def _prepare_livy_endpoint(livy_host, livy_port):
    # fast fail by check livy port availability. If fail, do not proceed to compose the endpoint.
    if not check_host_and_port(livy_host, livy_port):
        raise RuntimeError(f"Cannot connect to livy service: {livy_host}:{livy_port}")

    protocol = "http"
    if is_ssl_enabled(livy_host, livy_port):
        protocol = "https"
        _enable_ignore_ssl_errors()

    livy_endpoint = "{0}://{1}:{2}".format(protocol, livy_host, livy_port)
    return livy_endpoint


def _get_livy_port(args, emr_client, emr_cluster):
    livy_port = LIVY_DEFAULT_PORT

    livy_port_from_cluster_configuration = _get_livy_port_from_cluster_configuration(
        emr_cluster=emr_cluster,
    )
    if livy_port_from_cluster_configuration:
        livy_port = livy_port_from_cluster_configuration
    # Given the logic cannot support EMR with INSTANCE_FLEET enabled. To avoid unexpected failure, check
    # InstanceCollectionType before calling logic to get livy port from instance group. This help unblock customer who
    # is using INSTANCE_FLEET but has no requirement to have custom livy port configured on instance fleet level.
    # Next step, we will add full support for livy port configured on instance fleet level.
    elif (
        _get_emr_instance_collection_type(emr_cluster) == INSTANCE_COLLECTION_TYPE_GROUP
    ):
        livy_port_from_instance_group = _get_livy_port_from_instance_group(
            emr_client=emr_client,
            args=args,
        )
        if livy_port_from_instance_group:
            livy_port = livy_port_from_instance_group
    return livy_port


def _get_emr_instance_collection_type(emr_cluster):
    """
    Get EMR instance collection type.
    The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.
    The EMR version 5.9.0 starts to support livy which is a pre-condition to work with Studio. So we can safely assume
    the InstanceCollectionType is available.
    :param emr_cluster: EMR cluster
    :return: InstanceCollectionType with valid Values: INSTANCE_FLEET | INSTANCE_GROUP
    """
    return emr_cluster.__dict__.get("_cluster").get("InstanceCollectionType")


def _run_preset_cell_magics(ipy):
    # To allow retry on user errors without kernel restart
    allow_retry_fatal = ipy.find_cell_magic("_do_not_call_allow_retry_fatal")
    allow_retry_fatal("")
    # To delete existing sessions before creating a new one for eac astra connect
    # This is to prevent any race conditions that may arise because of session reuse
    delete_session_magic = ipy.find_cell_magic("_do_not_call_delete_session")
    delete_session_magic("")


def _get_lock():
    """
    Handle cases when same studio user tries to connect to multiple kerberos clusters across notebooks.
    Because the krb5.conf location is same, this lock prevents async modifications to the file till one
    connection either succeeds or fails For same EMR cluster across notebooks, spark magic will hold off
    one initiating a session till the parallel session from another notebook is initiated or fails
    """
    lock = filelock.FileLock("{0}.lock".format(KRB_FILE_PATH))
    if lock.is_locked:
        sys_out_logger.debug("Lock is already acquired, waiting for 15s to check again")
        # Try to handle an unexpected kernel crash case
        sleep(15)
        # Check if lock is still locked
        if lock.is_locked:
            # Force release the lock as the kernel might have died silently
            sys_out_logger.debug(
                "Lock is still acquired after wait, trying to force release lock before attempting "
                "to acquire for processing"
            )
            lock.release(force=True)
    return lock


# IpythonWidgetBasedAuthProvider class must reside in this root file.
class IpythonWidgetBasedAuthProvider:
    """
    Class responsible for retrieving credentials needed to connect to EMR cluster.
    """

    def get_credentials_and_connect_to_cluster(
        self, emr_client, args, emr_cluster, kernel_name
    ):
        username = widgets.Text(
            value="", placeholder="", description="Username:", disabled=False
        )
        password = widgets.Password(
            value="",
            placeholder="Enter password",
            description="Password:",
            disabled=False,
        )
        display(username, password)
        button = widgets.Button(
            description="Connect",
            disabled=False,
            button_style="",
            tooltip="Connect to EMR",
            icon="",
        )
        output = widgets.Output()
        display(button, output)

        # Do not remove the unused param otherwise the button will become unresponsive
        def _on_button_clicked(b):
            with output:
                _connect_to_cluster(
                    emr_client=emr_client,
                    args=args,
                    emr_cluster=emr_cluster,
                    kernel_name=kernel_name,
                    username=username.value,
                    password=password.value,
                )

        button.on_click(_on_button_clicked)


def _connect_to_cluster(emr_client, args, emr_cluster, kernel_name, username, password):
    if args.auth_type == AUTH_TYPE_BASIC_ACCESS:
        _initiate_connect_based_on_kernel(
            emr_client=emr_client,
            args=args,
            emr_cluster=emr_cluster,
            username=username,
            password=password,
            kernel_name=kernel_name,
        )
    else:
        # At this point lock should be available to acquire if another process has not already taken it
        # Go ahead and try to use the "with" context directly
        with _get_lock().acquire(
            # Try for 15 seconds to acquire the lock, otherwise fail with lock acquire failure
            timeout=15
        ):
            completed_process = _generate_kerberos_token(
                emr_cluster=emr_cluster, username=username, password=password
            )
            if completed_process.returncode == 0:
                _initiate_connect_based_on_kernel(
                    emr_client=emr_client,
                    args=args,
                    emr_cluster=emr_cluster,
                    username=None,
                    password=None,
                    kernel_name=kernel_name,
                )
            else:
                _handle_kerberos_connectivity_failure(
                    args=args, completed_process=completed_process
                )


def _generate_kerberos_token(emr_cluster, username, password):
    # noinspection PyTypeChecker
    write_krb_conf(emr_cluster, KRB_FILE_PATH)
    cmd = ["kinit", username.encode()]
    completed_process = subprocess.run(
        cmd,
        input=password.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed_process


def _handle_kerberos_connectivity_failure(args, completed_process):
    error_message = None
    if completed_process.stderr:
        error_message = str(completed_process.stderr, "UTF-8")

    _echo_response_to_iopub_web_socket(
        _build_response(
            cluster_id=args.cluster_id,
            error_message=error_message,
            success=False,
            service="emr",
            operation="connect",
        )
    )

    if error_message:
        raise Exception(
            "Failed to generate kerberos token using provided credentials. \n{} \n{}".format(
                error_message, str(completed_process.stdout, "UTF-8")
            )
        )


def _get_magic_kernel_endpoint_magic_line(args, livy_endpoint, username, password):
    if args.auth_type == AUTH_TYPE_BASIC_ACCESS:
        return "-s {0} -t {1} -u {2} -p {3}".format(
            livy_endpoint, args.auth_type, username, password
        )
    else:
        return "-s {0} -t {1}".format(livy_endpoint, args.auth_type)


def _get_ipython_kernel_endpoint_magic_line(args, livy_endpoint, username, password):
    # Choice of uuid generator based on: https://docs.python.org/3/library/uuid.html
    # Maintain same session name for sparkmagic session and livy session
    session_name = conf.session_configs()["name"]

    if args.auth_type == AUTH_TYPE_BASIC_ACCESS:
        return "add -s {0} -l {1} -t {2} -u {3} -a {4} -p {5}".format(
            session_name,
            args.language,
            args.auth_type,
            livy_endpoint,
            username,
            password,
        )
    else:
        return "add -s {0} -l {1} -t {2} -u {3}".format(
            session_name, args.language, args.auth_type, livy_endpoint
        )


def _get_livy_port_from_instance_group(emr_client, args):
    """
    Check if livy port is overridden as an EMR instance group override This case will happen when the describe
    cluster response does not have livy port as cluster conf but in individual instance group configuration
    """
    emr_instance_group_list = _list_instance_groups(emr_client, args.cluster_id)
    for instance_group in emr_instance_group_list:
        # TODO: Test with multi-name-node configuration to see if livy server port is set to all master nodes or not
        if instance_group["InstanceGroupType"] == "MASTER":
            instance_group_configuration_list = instance_group.get("Configurations")
            for configuration in instance_group_configuration_list:
                livy_port_override = _get_livy_port_override(configuration)
                if livy_port_override:
                    return livy_port_override


def _get_livy_port_override(configuration):
    if (
        "Classification" in configuration
        and configuration["Classification"] == "livy-conf"
        and "Properties" in configuration
    ):
        """
        There are two cases when livy port is overridden post start and on-create
        In both cases the livy port appears in different places in the describe-cluster response
        It can either be in cluster config or instance group config
        """
        livy_properties = configuration["Properties"]
        if "livy.server.port" in livy_properties:
            livy_overridden_port = livy_properties["livy.server.port"]
            return livy_overridden_port


def _ipython_kernel_connect_to_emr(
    emr_client, args, emr_cluster, username, password, kernel_name
):
    print("Initiating EMR connection..")

    ipy = get_ipython()
    # Depth should be 2 if run_line_magic is being called from within a magic
    ipy.run_line_magic("load_ext", "sparkmagic.magics", 2)
    endpoint_magic_line = _get_endpoint_magic_line(
        emr_client, args, emr_cluster, username, password, kernel_name
    )

    _handle_kerberos_endpoint_override(emr_cluster=emr_cluster)

    ipy.run_line_magic("spark", "cleanup")
    ipy.run_line_magic("spark", endpoint_magic_line)

    # Check if session is created. Return true if sagemaker session name prefix is in '%spark info' response.
    # Sagemaker session name prefix is under control and can be used as stable contract.
    spark_info_output = io.StringIO()
    with contextlib.redirect_stdout(spark_info_output):
        ipy.run_line_magic("spark", "info")

    session_started = SPARK_SESSION_NAME_PREFIX in spark_info_output.getvalue()
    error_message = None
    if not session_started:
        error_message = "Failed to start spark session."

    _echo_response_to_iopub_web_socket(
        _build_response(
            cluster_id=args.cluster_id,
            error_message=error_message,
            success=session_started,
            service="emr",
            operation="connect",
        )
    )


# External KDC use cases require the kerberos endpoint to be overridden
def _handle_kerberos_endpoint_override(emr_cluster):
    if emr_cluster.krb_hostname_override():
        # Kerberos endpoint is overridden
        overridden_kerberos_auth_config = {
            "mutual_authentication": REQUIRED,
            "hostname_override": emr_cluster.krb_hostname_override(),
        }

        # Override kerberos auth config with new KDC endpoint
        conf.override(
            conf.kerberos_auth_configuration.__name__, overridden_kerberos_auth_config
        )


def _enable_ignore_ssl_errors():
    """
    Set ignore_ssl_errors as true so the self-signed certificate can be accepted.
    """
    conf.override(conf.ignore_ssl_errors.__name__, True)


def _get_livy_port_from_cluster_configuration(emr_cluster):
    emr_configuration_list = emr_cluster.__dict__.get("_cluster").get("Configurations")
    # For cluster configuration
    for configuration in emr_configuration_list:
        livy_port_override = _get_livy_port_override(configuration)
        if livy_port_override:
            return livy_port_override


def _validate_emr_args(args, usage, kernel_name):
    if args.cluster_id is None:
        raise ValueError(
            "Missing required argument '{}'. {}".format("--cluster-id", usage)
        )
    elif args.auth_type is None:
        raise ValueError(
            "Missing required argument '{}'. {}".format("--auth-type", usage)
        )
    elif args.auth_type not in AUTH_TYPE_SET:
        raise Exception(
            "Invalid auth type, supported auth types are '{}'. {}".format(
                AUTH_TYPE_SET, usage
            )
        )

    if args.assumable_role_arn:
        RoleArnValidator.validate(args.assumable_role_arn)

    if args.emr_execution_role_arn:
        RoleArnValidator.validate(args.emr_execution_role_arn)

    # Only IPython kernel needs language option support
    if kernel_name == IPYTHON_KERNEL:
        if args.language is None:
            raise ValueError(
                "Missing required argument '{}' for IPython kernel. {}".format(
                    "--language", usage
                )
            )
        elif args.language not in LANGUAGES_SUPPORTED:
            raise Exception(
                "Invalid language, supported languages are '{}'. {}".format(
                    LANGUAGES_SUPPORTED, usage
                )
            )


def _initiate_emr_connect(args, boto_session, kernel_name):
    # Needs EMR list instance group permissions
    emr_client = boto_session.client("emr")

    """
    Even if assumable role arn is None, we can pass it to the EMRCluster constructor and will be handled by
    get_boto3_session method call gracefully. So no need to do a explicit None check here.
    """
    cluster = EMRCluster(
        cluster_id=args.cluster_id, role_arn=args.assumable_role_arn, emr=emr_client
    )
    _validate_cluster_auth_with_auth_type_provided(
        auth_type=args.auth_type, emr_cluster=cluster
    )

    # If emr execution role is passed, the EMR IAM passthrough should be used and the token API is invoked
    # to get user and password which are later used for basic auth.
    if args.auth_type == AUTH_TYPE_BASIC_ACCESS and args.emr_execution_role_arn:
        # Before EMR IAM Passthrough is GA, use emr-iam-passthrough-beta as service.
        beta_emr_client = boto_session.client("emr-iam-passthrough-beta")

        credentials = (
            ClusterSessionCredentialsProvider().get_cluster_session_credentials(
                beta_emr_client, args.cluster_id, args.emr_execution_role_arn
            )
        )
        # wait for 3s for EMR token propagation
        sleep(3)

        _initiate_connect_based_on_kernel(
            emr_client=emr_client,
            args=args,
            emr_cluster=cluster,
            username=credentials.username,
            password=credentials.password,
            kernel_name=kernel_name,
        )
    elif cluster.is_krb_cluster or args.auth_type == AUTH_TYPE_BASIC_ACCESS:
        authProvider = IpythonWidgetBasedAuthProvider()
        authProvider.get_credentials_and_connect_to_cluster(
            emr_client=emr_client,
            args=args,
            emr_cluster=cluster,
            kernel_name=kernel_name,
        )
    else:
        _initiate_connect_based_on_kernel(
            emr_client=emr_client,
            args=args,
            emr_cluster=cluster,
            username=None,
            password=None,
            kernel_name=kernel_name,
        )


def _initiate_connect_based_on_kernel(
    emr_client, args, emr_cluster, username, password, kernel_name
):

    # Define livy session name. session_configs are passed to livy api.
    session_name = f"{SPARK_SESSION_NAME_PREFIX}_{uuid4().hex}"
    conf.override(conf.session_configs.__name__, {"name": session_name})

    _set_logging_config()

    if kernel_name in MAGIC_KERNELS:
        _magic_kernel_connect_to_emr(
            emr_client=emr_client,
            args=args,
            emr_cluster=emr_cluster,
            username=username,
            password=password,
            kernel_name=kernel_name,
        )

    elif kernel_name == IPYTHON_KERNEL:
        _ipython_kernel_connect_to_emr(
            emr_client=emr_client,
            args=args,
            emr_cluster=emr_cluster,
            username=username,
            password=password,
            kernel_name=kernel_name,
        )


def _set_logging_config() -> None:
    """
    Sets `disable_existing_loggers` key on the dictconfig config used by sparkmagic to create loggers.
    By default, loading a logger via `logging.config.dictConfig` disables all existing loggers, including our loggers.
    python doc: https://docs.python.org/3/library/logging.config.html
    sparkmagic ref: https://github.com/jupyter-incubator/sparkmagic/blob/master/hdijupyterutils/hdijupyterutils/log.py#L13
    :return: None
    """
    logging_config = conf.logging_config()
    logging_config["disable_existing_loggers"] = False
    conf.override(conf.logging_config.__name__, logging_config)


def _validate_cluster_auth_with_auth_type_provided(auth_type, emr_cluster):
    is_cluster_kerberos_authenticated = emr_cluster.is_krb_cluster
    is_cluster_ldap_authenticated = _is_cluster_ldap(emr_cluster)
    is_cluster_no_auth = (
        not is_cluster_ldap_authenticated and not is_cluster_kerberos_authenticated
    )

    if (
        (auth_type == AUTH_TYPE_NONE and is_cluster_kerberos_authenticated)
        or (auth_type == AUTH_TYPE_NONE and is_cluster_ldap_authenticated)
        or (auth_type == AUTH_TYPE_KERBEROS and is_cluster_ldap_authenticated)
        or (auth_type == AUTH_TYPE_KERBEROS and is_cluster_no_auth)
    ):
        raise Exception(
            "Cluster auth type does not match provided auth {}".format(auth_type)
        )


def _check_required_args(args, usage):
    if args is None or args.command is None or len(args.command) != 2:
        raise Exception(
            "Please provide service name and operation to perform. {}".format(usage)
        )


def _is_cluster_ldap(cluster):
    emr_configuration_list = cluster.__dict__.get("_cluster").get("Configurations")
    if emr_configuration_list is None or not emr_configuration_list:
        return False

    # For cluster configuration
    for configuration in emr_configuration_list:
        if (
            "Classification" in configuration
            and configuration["Classification"] == "livy-conf"
            and "Properties" in configuration
        ):
            livy_properties = configuration["Properties"]
            if "livy.server.auth.type" in livy_properties:
                livy_server_auth_type = livy_properties["livy.server.auth.type"]
                if livy_server_auth_type == "ldap":
                    return True
    return False


@magics_class
class SagemakerAnalytics(Magics):
    @line_magic
    @magic_arguments()
    @argument(
        "command",
        type=str,
        default=[""],
        nargs="*",
        help="Command to execute. The command consists of a service name followed by a ' ' followed by an operation. "
        "Supported services are {0} and supported operations are {1}. For example a valid command is '{2}'.".format(
            SERVICE.list(), OPERATION.list(), "emr connect"
        ),
    )
    @argument(
        "--auth-type",
        type=str,
        default=None,
        help="The authentication type to be used. Supported authentication types are {0}.".format(
            AUTH_TYPE_SET
        ),
    )
    @argument(
        "--cluster-id",
        type=str,
        default=None,
        help="The cluster id to connect to.",
    )
    @argument(
        "--language",
        type=str,
        default=None,
        help="Language to use. The supported languages for IPython kernel(s) are {0}. This is a required "
        "argument for IPython kernels, but not for magic kernels such as PySpark or SparkScala.".format(
            LANGUAGES_SUPPORTED
        ),
    )
    @argument(
        "--assumable-role-arn",
        type=str,
        default=None,
        help="The IAM role to assume when connecting to a cluster in a different AWS account. This argument is not "
        "required when connecting to a cluster in the same AWS account.",
    )
    @argument(
        "--emr-execution-role-arn",
        type=str,
        default=None,
        help="The IAM role passed to EMR to set up EMR job security context. This argument is optional and "
        "used when IAM Passthrough feature is enabled for EMR.",
    )
    def sm_analytics(self, line):
        usage = "Please look at usage of %sm_analytics by executing `%sm_analytics?`."
        user_input = line
        args = parse_argstring(self.sm_analytics, user_input)

        _check_required_args(args, usage)

        service = args.command[0].lower()
        operation = args.command[1].lower()

        global sagemaker_analytics_service_logger
        kernel_name = None

        # emr
        if service == SERVICE.EMR:
            if operation == OPERATION.CONNECT:
                sagemaker_analytics_service_logger = ServiceFileLogger(
                    EMR_CONNECTION_LOG_FILE,
                    SAGEMAKER_ANALYTICS_LOG_BASE_DIRECTORY,
                    sys_out_logger,
                )
                try:
                    kernel_name = type(IPython.Application.instance().kernel).__name__
                except Exception as e:
                    _echo_response_to_iopub_web_socket(
                        _build_response(
                            cluster_id=args.cluster_id,
                            error_message=str(e),
                            success=False,
                            service=service,
                            operation=operation,
                        )
                    )
                    raise e
                _connect_to_emr(
                    service=service,
                    operation=operation,
                    args=args,
                    usage=usage,
                    kernel_name=kernel_name,
                    service_logger=sagemaker_analytics_service_logger,
                )
            else:
                raise Exception("Operation '{}' not found. {}".format(operation, usage))
        else:
            raise Exception("Service '{}' not found. {}".format(service, usage))


@records_service_metrics
def _connect_to_emr(service, operation, args, usage, kernel_name, service_logger):
    try:
        _validate_emr_args(args=args, usage=usage, kernel_name=kernel_name)
        # Only create boto session if absolutely needed
        boto_session = get_boto3_session(args.assumable_role_arn)
        _initiate_emr_connect(
            args=args, boto_session=boto_session, kernel_name=kernel_name
        )
    except Exception as e:
        _echo_response_to_iopub_web_socket(
            _build_response(
                cluster_id=args.cluster_id,
                error_message=str(e),
                success=False,
                service=service,
                operation=operation,
            )
        )
        raise e


# In order to actually use these magics, you must register them with a
# running IPython.
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    auto-loaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(SagemakerAnalytics)


def _list_instance_groups(emr_client, cluster_id):
    try:
        emr_instance_group_list = []
        paginator = emr_client.get_paginator("list_instance_groups")
        operation_parameters = {"ClusterId": cluster_id}
        page_iterator = paginator.paginate(**operation_parameters)
        for page in page_iterator:
            emr_instance_group_list.extend(page["InstanceGroups"])

    except botocore.exceptions.ClientError as ce:
        sys_out_logger.error(
            "Failed to list instance groups for EMR cluster({0}). {1}".format(
                cluster_id, ce.response
            )
        )
        raise ValueError(
            "Unable to list instance groups for EMR cluster(Id: {0}) using ListInstanceGroups API. Error: {1}".format(
                cluster_id, ce.response["Error"]
            )
        ) from None
    return emr_instance_group_list


def _echo_response_to_iopub_web_socket(response):
    print(json.dumps(response))


def _build_response(cluster_id, error_message, success, service, operation):
    return {
        "namespace": LIBRARY_NAME,
        "cluster_id": cluster_id,
        "error_message": error_message,
        "success": success,
        "service": service,
        "operation": operation,
    }
