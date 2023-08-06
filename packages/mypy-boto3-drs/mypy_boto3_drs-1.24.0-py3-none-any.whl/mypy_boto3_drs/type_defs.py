"""
Type annotations for drs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_drs/type_defs/)

Usage::

    ```python
    from mypy_boto3_drs.type_defs import AccountTypeDef

    data: AccountTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    EC2InstanceStateType,
    ExtensionStatusType,
    FailbackReplicationErrorType,
    FailbackStateType,
    InitiatedByType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LastLaunchResultType,
    LastLaunchTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    PITPolicyRuleUnitsType,
    RecoveryInstanceDataReplicationInitiationStepNameType,
    RecoveryInstanceDataReplicationInitiationStepStatusType,
    RecoveryInstanceDataReplicationStateType,
    RecoverySnapshotsOrderType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    TargetInstanceTypeRightSizingMethodType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountTypeDef",
    "CPUTypeDef",
    "ConversionPropertiesTypeDef",
    "CreateExtendedSourceServerRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "PITPolicyRuleTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteRecoveryInstanceRequestRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    "DeleteSourceServerRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeJobLogItemsRequestRequestTypeDef",
    "DescribeJobsRequestFiltersTypeDef",
    "DescribeRecoveryInstancesRequestFiltersTypeDef",
    "DescribeRecoverySnapshotsRequestFiltersTypeDef",
    "RecoverySnapshotTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DisconnectRecoveryInstanceRequestRequestTypeDef",
    "DisconnectSourceServerRequestRequestTypeDef",
    "DiskTypeDef",
    "GetFailbackReplicationConfigurationRequestRequestTypeDef",
    "GetLaunchConfigurationRequestRequestTypeDef",
    "GetReplicationConfigurationRequestRequestTypeDef",
    "IdentificationHintsTypeDef",
    "ParticipatingServerTypeDef",
    "LicensingTypeDef",
    "LifeCycleLastLaunchInitiatedTypeDef",
    "ListExtensibleSourceServersRequestRequestTypeDef",
    "StagingSourceServerTypeDef",
    "ListStagingAccountsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "RecoveryInstanceDataReplicationErrorTypeDef",
    "RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef",
    "RecoveryInstanceDataReplicationInitiationStepTypeDef",
    "RecoveryInstanceDiskTypeDef",
    "RecoveryInstanceFailbackTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "RetryDataReplicationRequestRequestTypeDef",
    "StagingAreaTypeDef",
    "StartFailbackLaunchRequestRequestTypeDef",
    "StartRecoveryRequestSourceServerTypeDef",
    "StopFailbackRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TerminateRecoveryInstancesRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFailbackReplicationConfigurationRequestRequestTypeDef",
    "JobLogEventDataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetFailbackReplicationConfigurationResponseTypeDef",
    "ListStagingAccountsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateReplicationConfigurationTemplateRequestRequestTypeDef",
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "UpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    "DataReplicationInitiationTypeDef",
    "DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    "ListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef",
    "ListStagingAccountsRequestListStagingAccountsPaginateTypeDef",
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    "DescribeJobsRequestRequestTypeDef",
    "DescribeRecoveryInstancesRequestDescribeRecoveryInstancesPaginateTypeDef",
    "DescribeRecoveryInstancesRequestRequestTypeDef",
    "DescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef",
    "DescribeRecoverySnapshotsRequestRequestTypeDef",
    "DescribeRecoverySnapshotsResponseTypeDef",
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    "DescribeSourceServersRequestRequestTypeDef",
    "JobTypeDef",
    "LaunchConfigurationTypeDef",
    "UpdateLaunchConfigurationRequestRequestTypeDef",
    "LifeCycleLastLaunchTypeDef",
    "ListExtensibleSourceServersResponseTypeDef",
    "SourcePropertiesTypeDef",
    "RecoveryInstanceDataReplicationInitiationTypeDef",
    "RecoveryInstancePropertiesTypeDef",
    "ReplicationConfigurationTypeDef",
    "UpdateReplicationConfigurationRequestRequestTypeDef",
    "StartRecoveryRequestRequestTypeDef",
    "JobLogTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DataReplicationInfoTypeDef",
    "DescribeJobsResponseTypeDef",
    "StartFailbackLaunchResponseTypeDef",
    "StartRecoveryResponseTypeDef",
    "TerminateRecoveryInstancesResponseTypeDef",
    "LifeCycleTypeDef",
    "RecoveryInstanceDataReplicationInfoTypeDef",
    "DescribeJobLogItemsResponseTypeDef",
    "SourceServerResponseMetadataTypeDef",
    "SourceServerTypeDef",
    "RecoveryInstanceTypeDef",
    "CreateExtendedSourceServerResponseTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "DescribeRecoveryInstancesResponseTypeDef",
)

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "accountID": str,
    },
    total=False,
)

CPUTypeDef = TypedDict(
    "CPUTypeDef",
    {
        "cores": int,
        "modelName": str,
    },
    total=False,
)

ConversionPropertiesTypeDef = TypedDict(
    "ConversionPropertiesTypeDef",
    {
        "dataTimestamp": str,
        "forceUefi": bool,
        "rootVolumeName": str,
        "volumeToConversionMap": Dict[str, Dict[str, str]],
        "volumeToVolumeSize": Dict[str, int],
    },
    total=False,
)

_RequiredCreateExtendedSourceServerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExtendedSourceServerRequestRequestTypeDef",
    {
        "sourceServerArn": str,
    },
)
_OptionalCreateExtendedSourceServerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExtendedSourceServerRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateExtendedSourceServerRequestRequestTypeDef(
    _RequiredCreateExtendedSourceServerRequestRequestTypeDef,
    _OptionalCreateExtendedSourceServerRequestRequestTypeDef,
):
    pass


ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredPITPolicyRuleTypeDef = TypedDict(
    "_RequiredPITPolicyRuleTypeDef",
    {
        "interval": int,
        "retentionDuration": int,
        "units": PITPolicyRuleUnitsType,
    },
)
_OptionalPITPolicyRuleTypeDef = TypedDict(
    "_OptionalPITPolicyRuleTypeDef",
    {
        "enabled": bool,
        "ruleID": int,
    },
    total=False,
)


class PITPolicyRuleTypeDef(_RequiredPITPolicyRuleTypeDef, _OptionalPITPolicyRuleTypeDef):
    pass


DataReplicationErrorTypeDef = TypedDict(
    "DataReplicationErrorTypeDef",
    {
        "error": DataReplicationErrorStringType,
        "rawError": str,
    },
    total=False,
)

DataReplicationInfoReplicatedDiskTypeDef = TypedDict(
    "DataReplicationInfoReplicatedDiskTypeDef",
    {
        "backloggedStorageBytes": int,
        "deviceName": str,
        "replicatedStorageBytes": int,
        "rescannedStorageBytes": int,
        "totalStorageBytes": int,
    },
    total=False,
)

DataReplicationInitiationStepTypeDef = TypedDict(
    "DataReplicationInitiationStepTypeDef",
    {
        "name": DataReplicationInitiationStepNameType,
        "status": DataReplicationInitiationStepStatusType,
    },
    total=False,
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "jobID": str,
    },
)

DeleteRecoveryInstanceRequestRequestTypeDef = TypedDict(
    "DeleteRecoveryInstanceRequestRequestTypeDef",
    {
        "recoveryInstanceID": str,
    },
)

DeleteReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)

DeleteSourceServerRequestRequestTypeDef = TypedDict(
    "DeleteSourceServerRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestRequestTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class DescribeJobLogItemsRequestRequestTypeDef(
    _RequiredDescribeJobLogItemsRequestRequestTypeDef,
    _OptionalDescribeJobLogItemsRequestRequestTypeDef,
):
    pass


DescribeJobsRequestFiltersTypeDef = TypedDict(
    "DescribeJobsRequestFiltersTypeDef",
    {
        "fromDate": str,
        "jobIDs": Sequence[str],
        "toDate": str,
    },
    total=False,
)

DescribeRecoveryInstancesRequestFiltersTypeDef = TypedDict(
    "DescribeRecoveryInstancesRequestFiltersTypeDef",
    {
        "recoveryInstanceIDs": Sequence[str],
        "sourceServerIDs": Sequence[str],
    },
    total=False,
)

DescribeRecoverySnapshotsRequestFiltersTypeDef = TypedDict(
    "DescribeRecoverySnapshotsRequestFiltersTypeDef",
    {
        "fromDateTime": str,
        "toDateTime": str,
    },
    total=False,
)

_RequiredRecoverySnapshotTypeDef = TypedDict(
    "_RequiredRecoverySnapshotTypeDef",
    {
        "expectedTimestamp": str,
        "snapshotID": str,
        "sourceServerID": str,
    },
)
_OptionalRecoverySnapshotTypeDef = TypedDict(
    "_OptionalRecoverySnapshotTypeDef",
    {
        "ebsSnapshots": List[str],
        "timestamp": str,
    },
    total=False,
)


class RecoverySnapshotTypeDef(_RequiredRecoverySnapshotTypeDef, _OptionalRecoverySnapshotTypeDef):
    pass


DescribeReplicationConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "replicationConfigurationTemplateIDs": Sequence[str],
    },
    total=False,
)

DescribeSourceServersRequestFiltersTypeDef = TypedDict(
    "DescribeSourceServersRequestFiltersTypeDef",
    {
        "hardwareId": str,
        "sourceServerIDs": Sequence[str],
        "stagingAccountIDs": Sequence[str],
    },
    total=False,
)

DisconnectRecoveryInstanceRequestRequestTypeDef = TypedDict(
    "DisconnectRecoveryInstanceRequestRequestTypeDef",
    {
        "recoveryInstanceID": str,
    },
)

DisconnectSourceServerRequestRequestTypeDef = TypedDict(
    "DisconnectSourceServerRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "bytes": int,
        "deviceName": str,
    },
    total=False,
)

GetFailbackReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "GetFailbackReplicationConfigurationRequestRequestTypeDef",
    {
        "recoveryInstanceID": str,
    },
)

GetLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "GetLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

GetReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "GetReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

IdentificationHintsTypeDef = TypedDict(
    "IdentificationHintsTypeDef",
    {
        "awsInstanceID": str,
        "fqdn": str,
        "hostname": str,
        "vmWareUuid": str,
    },
    total=False,
)

ParticipatingServerTypeDef = TypedDict(
    "ParticipatingServerTypeDef",
    {
        "launchStatus": LaunchStatusType,
        "recoveryInstanceID": str,
        "sourceServerID": str,
    },
    total=False,
)

LicensingTypeDef = TypedDict(
    "LicensingTypeDef",
    {
        "osByol": bool,
    },
    total=False,
)

LifeCycleLastLaunchInitiatedTypeDef = TypedDict(
    "LifeCycleLastLaunchInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
        "type": LastLaunchTypeType,
    },
    total=False,
)

_RequiredListExtensibleSourceServersRequestRequestTypeDef = TypedDict(
    "_RequiredListExtensibleSourceServersRequestRequestTypeDef",
    {
        "stagingAccountID": str,
    },
)
_OptionalListExtensibleSourceServersRequestRequestTypeDef = TypedDict(
    "_OptionalListExtensibleSourceServersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListExtensibleSourceServersRequestRequestTypeDef(
    _RequiredListExtensibleSourceServersRequestRequestTypeDef,
    _OptionalListExtensibleSourceServersRequestRequestTypeDef,
):
    pass


StagingSourceServerTypeDef = TypedDict(
    "StagingSourceServerTypeDef",
    {
        "arn": str,
        "hostname": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ListStagingAccountsRequestRequestTypeDef = TypedDict(
    "ListStagingAccountsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "ips": List[str],
        "isPrimary": bool,
        "macAddress": str,
    },
    total=False,
)

OSTypeDef = TypedDict(
    "OSTypeDef",
    {
        "fullString": str,
    },
    total=False,
)

RecoveryInstanceDataReplicationErrorTypeDef = TypedDict(
    "RecoveryInstanceDataReplicationErrorTypeDef",
    {
        "error": FailbackReplicationErrorType,
        "rawError": str,
    },
    total=False,
)

RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef = TypedDict(
    "RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef",
    {
        "backloggedStorageBytes": int,
        "deviceName": str,
        "replicatedStorageBytes": int,
        "rescannedStorageBytes": int,
        "totalStorageBytes": int,
    },
    total=False,
)

RecoveryInstanceDataReplicationInitiationStepTypeDef = TypedDict(
    "RecoveryInstanceDataReplicationInitiationStepTypeDef",
    {
        "name": RecoveryInstanceDataReplicationInitiationStepNameType,
        "status": RecoveryInstanceDataReplicationInitiationStepStatusType,
    },
    total=False,
)

RecoveryInstanceDiskTypeDef = TypedDict(
    "RecoveryInstanceDiskTypeDef",
    {
        "bytes": int,
        "ebsVolumeID": str,
        "internalDeviceName": str,
    },
    total=False,
)

RecoveryInstanceFailbackTypeDef = TypedDict(
    "RecoveryInstanceFailbackTypeDef",
    {
        "agentLastSeenByServiceDateTime": str,
        "elapsedReplicationDuration": str,
        "failbackClientID": str,
        "failbackClientLastSeenByServiceDateTime": str,
        "failbackInitiationTime": str,
        "failbackJobID": str,
        "failbackToOriginalServer": bool,
        "firstByteDateTime": str,
        "state": FailbackStateType,
    },
    total=False,
)

ReplicationConfigurationReplicatedDiskTypeDef = TypedDict(
    "ReplicationConfigurationReplicatedDiskTypeDef",
    {
        "deviceName": str,
        "iops": int,
        "isBootDisk": bool,
        "stagingDiskType": ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
        "throughput": int,
    },
    total=False,
)

RetryDataReplicationRequestRequestTypeDef = TypedDict(
    "RetryDataReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

StagingAreaTypeDef = TypedDict(
    "StagingAreaTypeDef",
    {
        "errorMessage": str,
        "stagingAccountID": str,
        "stagingSourceServerArn": str,
        "status": ExtensionStatusType,
    },
    total=False,
)

_RequiredStartFailbackLaunchRequestRequestTypeDef = TypedDict(
    "_RequiredStartFailbackLaunchRequestRequestTypeDef",
    {
        "recoveryInstanceIDs": Sequence[str],
    },
)
_OptionalStartFailbackLaunchRequestRequestTypeDef = TypedDict(
    "_OptionalStartFailbackLaunchRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartFailbackLaunchRequestRequestTypeDef(
    _RequiredStartFailbackLaunchRequestRequestTypeDef,
    _OptionalStartFailbackLaunchRequestRequestTypeDef,
):
    pass


_RequiredStartRecoveryRequestSourceServerTypeDef = TypedDict(
    "_RequiredStartRecoveryRequestSourceServerTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalStartRecoveryRequestSourceServerTypeDef = TypedDict(
    "_OptionalStartRecoveryRequestSourceServerTypeDef",
    {
        "recoverySnapshotID": str,
    },
    total=False,
)


class StartRecoveryRequestSourceServerTypeDef(
    _RequiredStartRecoveryRequestSourceServerTypeDef,
    _OptionalStartRecoveryRequestSourceServerTypeDef,
):
    pass


StopFailbackRequestRequestTypeDef = TypedDict(
    "StopFailbackRequestRequestTypeDef",
    {
        "recoveryInstanceID": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

TerminateRecoveryInstancesRequestRequestTypeDef = TypedDict(
    "TerminateRecoveryInstancesRequestRequestTypeDef",
    {
        "recoveryInstanceIDs": Sequence[str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateFailbackReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFailbackReplicationConfigurationRequestRequestTypeDef",
    {
        "recoveryInstanceID": str,
    },
)
_OptionalUpdateFailbackReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFailbackReplicationConfigurationRequestRequestTypeDef",
    {
        "bandwidthThrottling": int,
        "name": str,
        "usePrivateIP": bool,
    },
    total=False,
)


class UpdateFailbackReplicationConfigurationRequestRequestTypeDef(
    _RequiredUpdateFailbackReplicationConfigurationRequestRequestTypeDef,
    _OptionalUpdateFailbackReplicationConfigurationRequestRequestTypeDef,
):
    pass


JobLogEventDataTypeDef = TypedDict(
    "JobLogEventDataTypeDef",
    {
        "conversionProperties": ConversionPropertiesTypeDef,
        "conversionServerID": str,
        "rawError": str,
        "sourceServerID": str,
        "targetInstanceID": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFailbackReplicationConfigurationResponseTypeDef = TypedDict(
    "GetFailbackReplicationConfigurationResponseTypeDef",
    {
        "bandwidthThrottling": int,
        "name": str,
        "recoveryInstanceID": str,
        "usePrivateIP": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStagingAccountsResponseTypeDef = TypedDict(
    "ListStagingAccountsResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "pitPolicy": Sequence[PITPolicyRuleTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
)
_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "ebsEncryptionKeyArn": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass


ReplicationConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "pitPolicy": List[PITPolicyRuleTypeDef],
        "replicationConfigurationTemplateID": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredReplicationConfigurationTemplateTypeDef = TypedDict(
    "_RequiredReplicationConfigurationTemplateTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalReplicationConfigurationTemplateTypeDef = TypedDict(
    "_OptionalReplicationConfigurationTemplateTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "pitPolicy": List[PITPolicyRuleTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)


class ReplicationConfigurationTemplateTypeDef(
    _RequiredReplicationConfigurationTemplateTypeDef,
    _OptionalReplicationConfigurationTemplateTypeDef,
):
    pass


_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "pitPolicy": Sequence[PITPolicyRuleTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)


class UpdateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass


DataReplicationInitiationTypeDef = TypedDict(
    "DataReplicationInitiationTypeDef",
    {
        "nextAttemptDateTime": str,
        "startDateTime": str,
        "steps": List[DataReplicationInitiationStepTypeDef],
    },
    total=False,
)

_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef(
    _RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
    _OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
):
    pass


DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    {
        "replicationConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef = TypedDict(
    "_RequiredListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef",
    {
        "stagingAccountID": str,
    },
)
_OptionalListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef = TypedDict(
    "_OptionalListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef(
    _RequiredListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef,
    _OptionalListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef,
):
    pass


ListStagingAccountsRequestListStagingAccountsPaginateTypeDef = TypedDict(
    "ListStagingAccountsRequestListStagingAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobsRequestDescribeJobsPaginateTypeDef = TypedDict(
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    {
        "filters": DescribeJobsRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobsRequestRequestTypeDef = TypedDict(
    "DescribeJobsRequestRequestTypeDef",
    {
        "filters": DescribeJobsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeRecoveryInstancesRequestDescribeRecoveryInstancesPaginateTypeDef = TypedDict(
    "DescribeRecoveryInstancesRequestDescribeRecoveryInstancesPaginateTypeDef",
    {
        "filters": DescribeRecoveryInstancesRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeRecoveryInstancesRequestRequestTypeDef = TypedDict(
    "DescribeRecoveryInstancesRequestRequestTypeDef",
    {
        "filters": DescribeRecoveryInstancesRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredDescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef = TypedDict(
    "_RequiredDescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalDescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef = TypedDict(
    "_OptionalDescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef",
    {
        "filters": DescribeRecoverySnapshotsRequestFiltersTypeDef,
        "order": RecoverySnapshotsOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef(
    _RequiredDescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef,
    _OptionalDescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef,
):
    pass


_RequiredDescribeRecoverySnapshotsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRecoverySnapshotsRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalDescribeRecoverySnapshotsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRecoverySnapshotsRequestRequestTypeDef",
    {
        "filters": DescribeRecoverySnapshotsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
        "order": RecoverySnapshotsOrderType,
    },
    total=False,
)


class DescribeRecoverySnapshotsRequestRequestTypeDef(
    _RequiredDescribeRecoverySnapshotsRequestRequestTypeDef,
    _OptionalDescribeRecoverySnapshotsRequestRequestTypeDef,
):
    pass


DescribeRecoverySnapshotsResponseTypeDef = TypedDict(
    "DescribeRecoverySnapshotsResponseTypeDef",
    {
        "items": List[RecoverySnapshotTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef = TypedDict(
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    {
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSourceServersRequestRequestTypeDef = TypedDict(
    "DescribeSourceServersRequestRequestTypeDef",
    {
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredJobTypeDef = TypedDict(
    "_RequiredJobTypeDef",
    {
        "jobID": str,
    },
)
_OptionalJobTypeDef = TypedDict(
    "_OptionalJobTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "endDateTime": str,
        "initiatedBy": InitiatedByType,
        "participatingServers": List[ParticipatingServerTypeDef],
        "status": JobStatusType,
        "tags": Dict[str, str],
        "type": JobTypeType,
    },
    total=False,
)


class JobTypeDef(_RequiredJobTypeDef, _OptionalJobTypeDef):
    pass


LaunchConfigurationTypeDef = TypedDict(
    "LaunchConfigurationTypeDef",
    {
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "name": str,
        "sourceServerID": str,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "copyPrivateIp": bool,
        "copyTags": bool,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "name": str,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class UpdateLaunchConfigurationRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationRequestRequestTypeDef,
):
    pass


LifeCycleLastLaunchTypeDef = TypedDict(
    "LifeCycleLastLaunchTypeDef",
    {
        "initiated": LifeCycleLastLaunchInitiatedTypeDef,
    },
    total=False,
)

ListExtensibleSourceServersResponseTypeDef = TypedDict(
    "ListExtensibleSourceServersResponseTypeDef",
    {
        "items": List[StagingSourceServerTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourcePropertiesTypeDef = TypedDict(
    "SourcePropertiesTypeDef",
    {
        "cpus": List[CPUTypeDef],
        "disks": List[DiskTypeDef],
        "identificationHints": IdentificationHintsTypeDef,
        "lastUpdatedDateTime": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "os": OSTypeDef,
        "ramBytes": int,
        "recommendedInstanceType": str,
    },
    total=False,
)

RecoveryInstanceDataReplicationInitiationTypeDef = TypedDict(
    "RecoveryInstanceDataReplicationInitiationTypeDef",
    {
        "startDateTime": str,
        "steps": List[RecoveryInstanceDataReplicationInitiationStepTypeDef],
    },
    total=False,
)

RecoveryInstancePropertiesTypeDef = TypedDict(
    "RecoveryInstancePropertiesTypeDef",
    {
        "cpus": List[CPUTypeDef],
        "disks": List[RecoveryInstanceDiskTypeDef],
        "identificationHints": IdentificationHintsTypeDef,
        "lastUpdatedDateTime": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "os": OSTypeDef,
        "ramBytes": int,
    },
    total=False,
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "pitPolicy": List[PITPolicyRuleTypeDef],
        "replicatedDisks": List[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "sourceServerID": str,
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "pitPolicy": Sequence[PITPolicyRuleTypeDef],
        "replicatedDisks": Sequence[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)


class UpdateReplicationConfigurationRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationRequestRequestTypeDef,
):
    pass


_RequiredStartRecoveryRequestRequestTypeDef = TypedDict(
    "_RequiredStartRecoveryRequestRequestTypeDef",
    {
        "sourceServers": Sequence[StartRecoveryRequestSourceServerTypeDef],
    },
)
_OptionalStartRecoveryRequestRequestTypeDef = TypedDict(
    "_OptionalStartRecoveryRequestRequestTypeDef",
    {
        "isDrill": bool,
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartRecoveryRequestRequestTypeDef(
    _RequiredStartRecoveryRequestRequestTypeDef, _OptionalStartRecoveryRequestRequestTypeDef
):
    pass


JobLogTypeDef = TypedDict(
    "JobLogTypeDef",
    {
        "event": JobLogEventType,
        "eventData": JobLogEventDataTypeDef,
        "logDateTime": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    {
        "items": List[ReplicationConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataReplicationInfoTypeDef = TypedDict(
    "DataReplicationInfoTypeDef",
    {
        "dataReplicationError": DataReplicationErrorTypeDef,
        "dataReplicationInitiation": DataReplicationInitiationTypeDef,
        "dataReplicationState": DataReplicationStateType,
        "etaDateTime": str,
        "lagDuration": str,
        "replicatedDisks": List[DataReplicationInfoReplicatedDiskTypeDef],
    },
    total=False,
)

DescribeJobsResponseTypeDef = TypedDict(
    "DescribeJobsResponseTypeDef",
    {
        "items": List[JobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFailbackLaunchResponseTypeDef = TypedDict(
    "StartFailbackLaunchResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartRecoveryResponseTypeDef = TypedDict(
    "StartRecoveryResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TerminateRecoveryInstancesResponseTypeDef = TypedDict(
    "TerminateRecoveryInstancesResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifeCycleTypeDef = TypedDict(
    "LifeCycleTypeDef",
    {
        "addedToServiceDateTime": str,
        "elapsedReplicationDuration": str,
        "firstByteDateTime": str,
        "lastLaunch": LifeCycleLastLaunchTypeDef,
        "lastSeenByServiceDateTime": str,
    },
    total=False,
)

RecoveryInstanceDataReplicationInfoTypeDef = TypedDict(
    "RecoveryInstanceDataReplicationInfoTypeDef",
    {
        "dataReplicationError": RecoveryInstanceDataReplicationErrorTypeDef,
        "dataReplicationInitiation": RecoveryInstanceDataReplicationInitiationTypeDef,
        "dataReplicationState": RecoveryInstanceDataReplicationStateType,
        "etaDateTime": str,
        "lagDuration": str,
        "replicatedDisks": List[RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef],
    },
    total=False,
)

DescribeJobLogItemsResponseTypeDef = TypedDict(
    "DescribeJobLogItemsResponseTypeDef",
    {
        "items": List[JobLogTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceServerResponseMetadataTypeDef = TypedDict(
    "SourceServerResponseMetadataTypeDef",
    {
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "lastLaunchResult": LastLaunchResultType,
        "lifeCycle": LifeCycleTypeDef,
        "recoveryInstanceId": str,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "stagingArea": StagingAreaTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceServerTypeDef = TypedDict(
    "SourceServerTypeDef",
    {
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "lastLaunchResult": LastLaunchResultType,
        "lifeCycle": LifeCycleTypeDef,
        "recoveryInstanceId": str,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "stagingArea": StagingAreaTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

RecoveryInstanceTypeDef = TypedDict(
    "RecoveryInstanceTypeDef",
    {
        "arn": str,
        "dataReplicationInfo": RecoveryInstanceDataReplicationInfoTypeDef,
        "ec2InstanceID": str,
        "ec2InstanceState": EC2InstanceStateType,
        "failback": RecoveryInstanceFailbackTypeDef,
        "isDrill": bool,
        "jobID": str,
        "pointInTimeSnapshotDateTime": str,
        "recoveryInstanceID": str,
        "recoveryInstanceProperties": RecoveryInstancePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
    },
    total=False,
)

CreateExtendedSourceServerResponseTypeDef = TypedDict(
    "CreateExtendedSourceServerResponseTypeDef",
    {
        "sourceServer": SourceServerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSourceServersResponseTypeDef = TypedDict(
    "DescribeSourceServersResponseTypeDef",
    {
        "items": List[SourceServerTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRecoveryInstancesResponseTypeDef = TypedDict(
    "DescribeRecoveryInstancesResponseTypeDef",
    {
        "items": List[RecoveryInstanceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
