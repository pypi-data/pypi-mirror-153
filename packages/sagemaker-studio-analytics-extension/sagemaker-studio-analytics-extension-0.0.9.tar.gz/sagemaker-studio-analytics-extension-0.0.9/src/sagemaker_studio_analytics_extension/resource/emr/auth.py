# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from collections import namedtuple

CREDENTIAL_TYPE_USERNAME_PASSWORD = "usernamePassword"

ClusterSessionCredentials = namedtuple("ClusterSessionCredentials", "username password")


class ClusterSessionCredentialsProvider:
    def get_cluster_session_credentials(
        self, emr_client, cluster_id, emr_execution_role_arn
    ):
        """
        This method is to retrieve the credentials by calling GetClusterSessionCredentials API.
        :param emr_client: EMR client used to communicate with EMR endpoint.
        :param emr_execution_role_arn: The role passed to EMR and used to set up job security context.
        :return: ClusterSessionCredentials
        """
        response = emr_client.get_cluster_session_credentials(
            ClusterId=cluster_id,
            ExecutionRoleArn=emr_execution_role_arn,
            CredentialType=CREDENTIAL_TYPE_USERNAME_PASSWORD,
        )
        credentials = response["Credentials"]["UsernamePassword"]
        return ClusterSessionCredentials(
            credentials["Username"], credentials["Password"]
        )
