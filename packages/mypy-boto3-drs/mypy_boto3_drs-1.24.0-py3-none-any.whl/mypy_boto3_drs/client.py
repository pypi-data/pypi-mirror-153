"""
Type annotations for drs service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_drs.client import drsClient

    session = Session()
    client: drsClient = session.client("drs")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    LaunchDispositionType,
    RecoverySnapshotsOrderType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    TargetInstanceTypeRightSizingMethodType,
)
from .paginator import (
    DescribeJobLogItemsPaginator,
    DescribeJobsPaginator,
    DescribeRecoveryInstancesPaginator,
    DescribeRecoverySnapshotsPaginator,
    DescribeReplicationConfigurationTemplatesPaginator,
    DescribeSourceServersPaginator,
    ListExtensibleSourceServersPaginator,
    ListStagingAccountsPaginator,
)
from .type_defs import (
    CreateExtendedSourceServerResponseTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestFiltersTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeRecoveryInstancesRequestFiltersTypeDef,
    DescribeRecoveryInstancesResponseTypeDef,
    DescribeRecoverySnapshotsRequestFiltersTypeDef,
    DescribeRecoverySnapshotsResponseTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestFiltersTypeDef,
    DescribeSourceServersResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetFailbackReplicationConfigurationResponseTypeDef,
    LaunchConfigurationTypeDef,
    LicensingTypeDef,
    ListExtensibleSourceServersResponseTypeDef,
    ListStagingAccountsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PITPolicyRuleTypeDef,
    ReplicationConfigurationReplicatedDiskTypeDef,
    ReplicationConfigurationTemplateResponseMetadataTypeDef,
    ReplicationConfigurationTypeDef,
    SourceServerResponseMetadataTypeDef,
    StartFailbackLaunchResponseTypeDef,
    StartRecoveryRequestSourceServerTypeDef,
    StartRecoveryResponseTypeDef,
    TerminateRecoveryInstancesResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("drsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UninitializedAccountException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class drsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        drsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#can_paginate)
        """

    def create_extended_source_server(
        self, *, sourceServerArn: str, tags: Mapping[str, str] = ...
    ) -> CreateExtendedSourceServerResponseTypeDef:
        """
        Create an extended source server in the target Account based on the source
        server in staging account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.create_extended_source_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#create_extended_source_server)
        """

    def create_replication_configuration_template(
        self,
        *,
        associateDefaultSecurityGroup: bool,
        bandwidthThrottling: int,
        createPublicIP: bool,
        dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType,
        defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        ebsEncryption: ReplicationConfigurationEbsEncryptionType,
        pitPolicy: Sequence[PITPolicyRuleTypeDef],
        replicationServerInstanceType: str,
        replicationServersSecurityGroupsIDs: Sequence[str],
        stagingAreaSubnetId: str,
        stagingAreaTags: Mapping[str, str],
        useDedicatedReplicationServer: bool,
        ebsEncryptionKeyArn: str = ...,
        tags: Mapping[str, str] = ...
    ) -> ReplicationConfigurationTemplateResponseMetadataTypeDef:
        """
        Creates a new ReplicationConfigurationTemplate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.create_replication_configuration_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#create_replication_configuration_template)
        """

    def delete_job(self, *, jobID: str) -> Dict[str, Any]:
        """
        Deletes a single Job by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.delete_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#delete_job)
        """

    def delete_recovery_instance(self, *, recoveryInstanceID: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a single Recovery Instance by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.delete_recovery_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#delete_recovery_instance)
        """

    def delete_replication_configuration_template(
        self, *, replicationConfigurationTemplateID: str
    ) -> Dict[str, Any]:
        """
        Deletes a single Replication Configuration Template by ID See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/drs-2020-02-26/DeleteReplicationConfigurationTemplate).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.delete_replication_configuration_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#delete_replication_configuration_template)
        """

    def delete_source_server(self, *, sourceServerID: str) -> Dict[str, Any]:
        """
        Deletes a single Source Server by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.delete_source_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#delete_source_server)
        """

    def describe_job_log_items(
        self, *, jobID: str, maxResults: int = ..., nextToken: str = ...
    ) -> DescribeJobLogItemsResponseTypeDef:
        """
        Retrieves a detailed Job log with pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.describe_job_log_items)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#describe_job_log_items)
        """

    def describe_jobs(
        self,
        *,
        filters: DescribeJobsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeJobsResponseTypeDef:
        """
        Returns a list of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.describe_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#describe_jobs)
        """

    def describe_recovery_instances(
        self,
        *,
        filters: DescribeRecoveryInstancesRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeRecoveryInstancesResponseTypeDef:
        """
        Lists all Recovery Instances or multiple Recovery Instances by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.describe_recovery_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#describe_recovery_instances)
        """

    def describe_recovery_snapshots(
        self,
        *,
        sourceServerID: str,
        filters: DescribeRecoverySnapshotsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        order: RecoverySnapshotsOrderType = ...
    ) -> DescribeRecoverySnapshotsResponseTypeDef:
        """
        Lists all Recovery Snapshots for a single Source Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.describe_recovery_snapshots)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#describe_recovery_snapshots)
        """

    def describe_replication_configuration_templates(
        self,
        *,
        maxResults: int = ...,
        nextToken: str = ...,
        replicationConfigurationTemplateIDs: Sequence[str] = ...
    ) -> DescribeReplicationConfigurationTemplatesResponseTypeDef:
        """
        Lists all ReplicationConfigurationTemplates, filtered by Source Server IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.describe_replication_configuration_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#describe_replication_configuration_templates)
        """

    def describe_source_servers(
        self,
        *,
        filters: DescribeSourceServersRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeSourceServersResponseTypeDef:
        """
        Lists all Source Servers or multiple Source Servers filtered by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.describe_source_servers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#describe_source_servers)
        """

    def disconnect_recovery_instance(
        self, *, recoveryInstanceID: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disconnect a Recovery Instance from Elastic Disaster Recovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.disconnect_recovery_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#disconnect_recovery_instance)
        """

    def disconnect_source_server(
        self, *, sourceServerID: str
    ) -> SourceServerResponseMetadataTypeDef:
        """
        Disconnects a specific Source Server from Elastic Disaster Recovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.disconnect_source_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#disconnect_source_server)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#generate_presigned_url)
        """

    def get_failback_replication_configuration(
        self, *, recoveryInstanceID: str
    ) -> GetFailbackReplicationConfigurationResponseTypeDef:
        """
        Lists all Failback ReplicationConfigurations, filtered by Recovery Instance ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_failback_replication_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_failback_replication_configuration)
        """

    def get_launch_configuration(self, *, sourceServerID: str) -> LaunchConfigurationTypeDef:
        """
        Gets a LaunchConfiguration, filtered by Source Server IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_launch_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_launch_configuration)
        """

    def get_replication_configuration(
        self, *, sourceServerID: str
    ) -> ReplicationConfigurationTypeDef:
        """
        Gets a ReplicationConfiguration, filtered by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_replication_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_replication_configuration)
        """

    def initialize_service(self) -> Dict[str, Any]:
        """
        Initialize Elastic Disaster Recovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.initialize_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#initialize_service)
        """

    def list_extensible_source_servers(
        self, *, stagingAccountID: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListExtensibleSourceServersResponseTypeDef:
        """
        Returns a list of source servers on a staging account that are extensible, which
        means that: a.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.list_extensible_source_servers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#list_extensible_source_servers)
        """

    def list_staging_accounts(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListStagingAccountsResponseTypeDef:
        """
        Returns an array of staging accounts for existing extended source servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.list_staging_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#list_staging_accounts)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags for your Elastic Disaster Recovery resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#list_tags_for_resource)
        """

    def retry_data_replication(self, *, sourceServerID: str) -> SourceServerResponseMetadataTypeDef:
        """
        Causes the data replication initiation sequence to begin immediately upon next
        Handshake for the specified Source Server ID, regardless of when the previous
        initiation started.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.retry_data_replication)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#retry_data_replication)
        """

    def start_failback_launch(
        self, *, recoveryInstanceIDs: Sequence[str], tags: Mapping[str, str] = ...
    ) -> StartFailbackLaunchResponseTypeDef:
        """
        Initiates a Job for launching the machine that is being failed back to from the
        specified Recovery Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.start_failback_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#start_failback_launch)
        """

    def start_recovery(
        self,
        *,
        sourceServers: Sequence[StartRecoveryRequestSourceServerTypeDef],
        isDrill: bool = ...,
        tags: Mapping[str, str] = ...
    ) -> StartRecoveryResponseTypeDef:
        """
        Launches Recovery Instances for the specified Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.start_recovery)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#start_recovery)
        """

    def stop_failback(self, *, recoveryInstanceID: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops the failback process for a specified Recovery Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.stop_failback)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#stop_failback)
        """

    def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or overwrites only the specified tags for the specified Elastic Disaster
        Recovery resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#tag_resource)
        """

    def terminate_recovery_instances(
        self, *, recoveryInstanceIDs: Sequence[str]
    ) -> TerminateRecoveryInstancesResponseTypeDef:
        """
        Initiates a Job for terminating the EC2 resources associated with the specified
        Recovery Instances, and then will delete the Recovery Instances from the Elastic
        Disaster Recovery service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.terminate_recovery_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#terminate_recovery_instances)
        """

    def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified set of tags from the specified set of Elastic Disaster
        Recovery resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#untag_resource)
        """

    def update_failback_replication_configuration(
        self,
        *,
        recoveryInstanceID: str,
        bandwidthThrottling: int = ...,
        name: str = ...,
        usePrivateIP: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Allows you to update the failback replication configuration of a Recovery
        Instance by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.update_failback_replication_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#update_failback_replication_configuration)
        """

    def update_launch_configuration(
        self,
        *,
        sourceServerID: str,
        copyPrivateIp: bool = ...,
        copyTags: bool = ...,
        launchDisposition: LaunchDispositionType = ...,
        licensing: LicensingTypeDef = ...,
        name: str = ...,
        targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType = ...
    ) -> LaunchConfigurationTypeDef:
        """
        Updates a LaunchConfiguration by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.update_launch_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#update_launch_configuration)
        """

    def update_replication_configuration(
        self,
        *,
        sourceServerID: str,
        associateDefaultSecurityGroup: bool = ...,
        bandwidthThrottling: int = ...,
        createPublicIP: bool = ...,
        dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType = ...,
        defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType = ...,
        ebsEncryption: ReplicationConfigurationEbsEncryptionType = ...,
        ebsEncryptionKeyArn: str = ...,
        name: str = ...,
        pitPolicy: Sequence[PITPolicyRuleTypeDef] = ...,
        replicatedDisks: Sequence[ReplicationConfigurationReplicatedDiskTypeDef] = ...,
        replicationServerInstanceType: str = ...,
        replicationServersSecurityGroupsIDs: Sequence[str] = ...,
        stagingAreaSubnetId: str = ...,
        stagingAreaTags: Mapping[str, str] = ...,
        useDedicatedReplicationServer: bool = ...
    ) -> ReplicationConfigurationTypeDef:
        """
        Allows you to update a ReplicationConfiguration by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.update_replication_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#update_replication_configuration)
        """

    def update_replication_configuration_template(
        self,
        *,
        replicationConfigurationTemplateID: str,
        arn: str = ...,
        associateDefaultSecurityGroup: bool = ...,
        bandwidthThrottling: int = ...,
        createPublicIP: bool = ...,
        dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType = ...,
        defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType = ...,
        ebsEncryption: ReplicationConfigurationEbsEncryptionType = ...,
        ebsEncryptionKeyArn: str = ...,
        pitPolicy: Sequence[PITPolicyRuleTypeDef] = ...,
        replicationServerInstanceType: str = ...,
        replicationServersSecurityGroupsIDs: Sequence[str] = ...,
        stagingAreaSubnetId: str = ...,
        stagingAreaTags: Mapping[str, str] = ...,
        useDedicatedReplicationServer: bool = ...
    ) -> ReplicationConfigurationTemplateResponseMetadataTypeDef:
        """
        Updates a ReplicationConfigurationTemplate by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.update_replication_configuration_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#update_replication_configuration_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_log_items"]
    ) -> DescribeJobLogItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_jobs"]) -> DescribeJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_recovery_instances"]
    ) -> DescribeRecoveryInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_recovery_snapshots"]
    ) -> DescribeRecoverySnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_configuration_templates"]
    ) -> DescribeReplicationConfigurationTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_source_servers"]
    ) -> DescribeSourceServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_extensible_source_servers"]
    ) -> ListExtensibleSourceServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_staging_accounts"]
    ) -> ListStagingAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs.html#drs.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/client/#get_paginator)
        """
