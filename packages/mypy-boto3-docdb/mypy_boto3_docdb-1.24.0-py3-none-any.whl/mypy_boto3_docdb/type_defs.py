"""
Type annotations for docdb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/type_defs/)

Usage::

    ```python
    from mypy_boto3_docdb.type_defs import AddSourceIdentifierToSubscriptionMessageRequestTypeDef

    data: AddSourceIdentifierToSubscriptionMessageRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import ApplyMethodType, SourceTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    "EventSubscriptionTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "AvailabilityZoneTypeDef",
    "CertificateTypeDef",
    "CloudwatchLogsExportConfigurationTypeDef",
    "DBClusterParameterGroupTypeDef",
    "DBClusterSnapshotTypeDef",
    "CreateGlobalClusterMessageRequestTypeDef",
    "DBClusterMemberTypeDef",
    "ParameterTypeDef",
    "DBClusterRoleTypeDef",
    "DBClusterSnapshotAttributeTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "UpgradeTargetTypeDef",
    "DBInstanceStatusInfoTypeDef",
    "EndpointTypeDef",
    "DeleteDBClusterMessageRequestTypeDef",
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    "DeleteDBInstanceMessageRequestTypeDef",
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteGlobalClusterMessageRequestTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    "WaiterConfigTypeDef",
    "EventCategoriesMapTypeDef",
    "EventTypeDef",
    "FailoverDBClusterMessageRequestTypeDef",
    "GlobalClusterMemberTypeDef",
    "ModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    "ModifyDBInstanceMessageRequestTypeDef",
    "ModifyDBSubnetGroupMessageRequestTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifyGlobalClusterMessageRequestTypeDef",
    "PendingCloudwatchLogsExportsTypeDef",
    "PendingMaintenanceActionTypeDef",
    "RebootDBInstanceMessageRequestTypeDef",
    "RemoveFromGlobalClusterMessageRequestTypeDef",
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "StartDBClusterMessageRequestTypeDef",
    "StopDBClusterMessageRequestTypeDef",
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    "CreateEventSubscriptionResultTypeDef",
    "DBClusterParameterGroupNameMessageTypeDef",
    "DeleteEventSubscriptionResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventSubscriptionsMessageTypeDef",
    "ModifyEventSubscriptionResultTypeDef",
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "CopyDBClusterParameterGroupMessageRequestTypeDef",
    "CopyDBClusterSnapshotMessageRequestTypeDef",
    "CreateDBClusterMessageRequestTypeDef",
    "CreateDBClusterParameterGroupMessageRequestTypeDef",
    "CreateDBClusterSnapshotMessageRequestTypeDef",
    "CreateDBInstanceMessageRequestTypeDef",
    "CreateDBSubnetGroupMessageRequestTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "RestoreDBClusterFromSnapshotMessageRequestTypeDef",
    "RestoreDBClusterToPointInTimeMessageRequestTypeDef",
    "TagListMessageTypeDef",
    "OrderableDBInstanceOptionTypeDef",
    "SubnetTypeDef",
    "CertificateMessageTypeDef",
    "ModifyDBClusterMessageRequestTypeDef",
    "CopyDBClusterParameterGroupResultTypeDef",
    "CreateDBClusterParameterGroupResultTypeDef",
    "DBClusterParameterGroupsMessageTypeDef",
    "CopyDBClusterSnapshotResultTypeDef",
    "CreateDBClusterSnapshotResultTypeDef",
    "DBClusterSnapshotMessageTypeDef",
    "DeleteDBClusterSnapshotResultTypeDef",
    "DBClusterParameterGroupDetailsTypeDef",
    "EngineDefaultsTypeDef",
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    "ResetDBClusterParameterGroupMessageRequestTypeDef",
    "DBClusterSnapshotAttributesResultTypeDef",
    "DBClusterTypeDef",
    "DBEngineVersionTypeDef",
    "DescribeCertificatesMessageRequestTypeDef",
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    "DescribeDBClusterParametersMessageRequestTypeDef",
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    "DescribeDBClustersMessageRequestTypeDef",
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    "DescribeDBInstancesMessageRequestTypeDef",
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    "DescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeGlobalClustersMessageRequestTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    "DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    "EventCategoriesMessageTypeDef",
    "EventsMessageTypeDef",
    "GlobalClusterTypeDef",
    "PendingModifiedValuesTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "OrderableDBInstanceOptionsMessageTypeDef",
    "DBSubnetGroupTypeDef",
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    "CreateDBClusterResultTypeDef",
    "DBClusterMessageTypeDef",
    "DeleteDBClusterResultTypeDef",
    "FailoverDBClusterResultTypeDef",
    "ModifyDBClusterResultTypeDef",
    "RestoreDBClusterFromSnapshotResultTypeDef",
    "RestoreDBClusterToPointInTimeResultTypeDef",
    "StartDBClusterResultTypeDef",
    "StopDBClusterResultTypeDef",
    "DBEngineVersionMessageTypeDef",
    "CreateGlobalClusterResultTypeDef",
    "DeleteGlobalClusterResultTypeDef",
    "GlobalClustersMessageTypeDef",
    "ModifyGlobalClusterResultTypeDef",
    "RemoveFromGlobalClusterResultTypeDef",
    "ApplyPendingMaintenanceActionResultTypeDef",
    "PendingMaintenanceActionsMessageTypeDef",
    "CreateDBSubnetGroupResultTypeDef",
    "DBInstanceTypeDef",
    "DBSubnetGroupMessageTypeDef",
    "ModifyDBSubnetGroupResultTypeDef",
    "CreateDBInstanceResultTypeDef",
    "DBInstanceMessageTypeDef",
    "DeleteDBInstanceResultTypeDef",
    "ModifyDBInstanceResultTypeDef",
    "RebootDBInstanceResultTypeDef",
)

AddSourceIdentifierToSubscriptionMessageRequestTypeDef = TypedDict(
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SourceIdentifier": str,
    },
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": str,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Enabled": bool,
        "EventSubscriptionArn": str,
    },
    total=False,
)

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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ApplyPendingMaintenanceActionMessageRequestTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "ApplyAction": str,
        "OptInType": str,
    },
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateIdentifier": str,
        "CertificateType": str,
        "Thumbprint": str,
        "ValidFrom": datetime,
        "ValidTill": datetime,
        "CertificateArn": str,
    },
    total=False,
)

CloudwatchLogsExportConfigurationTypeDef = TypedDict(
    "CloudwatchLogsExportConfigurationTypeDef",
    {
        "EnableLogTypes": Sequence[str],
        "DisableLogTypes": Sequence[str],
    },
    total=False,
)

DBClusterParameterGroupTypeDef = TypedDict(
    "DBClusterParameterGroupTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
        "DBClusterParameterGroupArn": str,
    },
    total=False,
)

DBClusterSnapshotTypeDef = TypedDict(
    "DBClusterSnapshotTypeDef",
    {
        "AvailabilityZones": List[str],
        "DBClusterSnapshotIdentifier": str,
        "DBClusterIdentifier": str,
        "SnapshotCreateTime": datetime,
        "Engine": str,
        "Status": str,
        "Port": int,
        "VpcId": str,
        "ClusterCreateTime": datetime,
        "MasterUsername": str,
        "EngineVersion": str,
        "SnapshotType": str,
        "PercentProgress": int,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DBClusterSnapshotArn": str,
        "SourceDBClusterSnapshotArn": str,
    },
    total=False,
)

_RequiredCreateGlobalClusterMessageRequestTypeDef = TypedDict(
    "_RequiredCreateGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
    },
)
_OptionalCreateGlobalClusterMessageRequestTypeDef = TypedDict(
    "_OptionalCreateGlobalClusterMessageRequestTypeDef",
    {
        "SourceDBClusterIdentifier": str,
        "Engine": str,
        "EngineVersion": str,
        "DeletionProtection": bool,
        "DatabaseName": str,
        "StorageEncrypted": bool,
    },
    total=False,
)


class CreateGlobalClusterMessageRequestTypeDef(
    _RequiredCreateGlobalClusterMessageRequestTypeDef,
    _OptionalCreateGlobalClusterMessageRequestTypeDef,
):
    pass


DBClusterMemberTypeDef = TypedDict(
    "DBClusterMemberTypeDef",
    {
        "DBInstanceIdentifier": str,
        "IsClusterWriter": bool,
        "DBClusterParameterGroupStatus": str,
        "PromotionTier": int,
    },
    total=False,
)

ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
        "Description": str,
        "Source": str,
        "ApplyType": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "MinimumEngineVersion": str,
        "ApplyMethod": ApplyMethodType,
    },
    total=False,
)

DBClusterRoleTypeDef = TypedDict(
    "DBClusterRoleTypeDef",
    {
        "RoleArn": str,
        "Status": str,
    },
    total=False,
)

DBClusterSnapshotAttributeTypeDef = TypedDict(
    "DBClusterSnapshotAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": List[str],
    },
    total=False,
)

VpcSecurityGroupMembershipTypeDef = TypedDict(
    "VpcSecurityGroupMembershipTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

UpgradeTargetTypeDef = TypedDict(
    "UpgradeTargetTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "Description": str,
        "AutoUpgrade": bool,
        "IsMajorVersionUpgrade": bool,
    },
    total=False,
)

DBInstanceStatusInfoTypeDef = TypedDict(
    "DBInstanceStatusInfoTypeDef",
    {
        "StatusType": str,
        "Normal": bool,
        "Status": str,
        "Message": str,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "HostedZoneId": str,
    },
    total=False,
)

_RequiredDeleteDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalDeleteDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteDBClusterMessageRequestTypeDef",
    {
        "SkipFinalSnapshot": bool,
        "FinalDBSnapshotIdentifier": str,
    },
    total=False,
)


class DeleteDBClusterMessageRequestTypeDef(
    _RequiredDeleteDBClusterMessageRequestTypeDef, _OptionalDeleteDBClusterMessageRequestTypeDef
):
    pass


DeleteDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)

DeleteDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
    },
)

DeleteDBInstanceMessageRequestTypeDef = TypedDict(
    "DeleteDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)

DeleteDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
    },
)

DeleteEventSubscriptionMessageRequestTypeDef = TypedDict(
    "DeleteEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)

DeleteGlobalClusterMessageRequestTypeDef = TypedDict(
    "DeleteGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
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

DescribeDBClusterSnapshotAttributesMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

EventCategoriesMapTypeDef = TypedDict(
    "EventCategoriesMapTypeDef",
    {
        "SourceType": str,
        "EventCategories": List[str],
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "Message": str,
        "EventCategories": List[str],
        "Date": datetime,
        "SourceArn": str,
    },
    total=False,
)

FailoverDBClusterMessageRequestTypeDef = TypedDict(
    "FailoverDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "TargetDBInstanceIdentifier": str,
    },
    total=False,
)

GlobalClusterMemberTypeDef = TypedDict(
    "GlobalClusterMemberTypeDef",
    {
        "DBClusterArn": str,
        "Readers": List[str],
        "IsWriter": bool,
    },
    total=False,
)

_RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "AttributeName": str,
    },
)
_OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    {
        "ValuesToAdd": Sequence[str],
        "ValuesToRemove": Sequence[str],
    },
    total=False,
)


class ModifyDBClusterSnapshotAttributeMessageRequestTypeDef(
    _RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
    _OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
):
    pass


_RequiredModifyDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalModifyDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceClass": str,
        "ApplyImmediately": bool,
        "PreferredMaintenanceWindow": str,
        "AutoMinorVersionUpgrade": bool,
        "NewDBInstanceIdentifier": str,
        "CACertificateIdentifier": str,
        "PromotionTier": int,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
    },
    total=False,
)


class ModifyDBInstanceMessageRequestTypeDef(
    _RequiredModifyDBInstanceMessageRequestTypeDef, _OptionalModifyDBInstanceMessageRequestTypeDef
):
    pass


_RequiredModifyDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalModifyDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupDescription": str,
    },
    total=False,
)


class ModifyDBSubnetGroupMessageRequestTypeDef(
    _RequiredModifyDBSubnetGroupMessageRequestTypeDef,
    _OptionalModifyDBSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)
_OptionalModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SnsTopicArn": str,
        "SourceType": str,
        "EventCategories": Sequence[str],
        "Enabled": bool,
    },
    total=False,
)


class ModifyEventSubscriptionMessageRequestTypeDef(
    _RequiredModifyEventSubscriptionMessageRequestTypeDef,
    _OptionalModifyEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredModifyGlobalClusterMessageRequestTypeDef = TypedDict(
    "_RequiredModifyGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
    },
)
_OptionalModifyGlobalClusterMessageRequestTypeDef = TypedDict(
    "_OptionalModifyGlobalClusterMessageRequestTypeDef",
    {
        "NewGlobalClusterIdentifier": str,
        "DeletionProtection": bool,
    },
    total=False,
)


class ModifyGlobalClusterMessageRequestTypeDef(
    _RequiredModifyGlobalClusterMessageRequestTypeDef,
    _OptionalModifyGlobalClusterMessageRequestTypeDef,
):
    pass


PendingCloudwatchLogsExportsTypeDef = TypedDict(
    "PendingCloudwatchLogsExportsTypeDef",
    {
        "LogTypesToEnable": List[str],
        "LogTypesToDisable": List[str],
    },
    total=False,
)

PendingMaintenanceActionTypeDef = TypedDict(
    "PendingMaintenanceActionTypeDef",
    {
        "Action": str,
        "AutoAppliedAfterDate": datetime,
        "ForcedApplyDate": datetime,
        "OptInStatus": str,
        "CurrentApplyDate": datetime,
        "Description": str,
    },
    total=False,
)

_RequiredRebootDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredRebootDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalRebootDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalRebootDBInstanceMessageRequestTypeDef",
    {
        "ForceFailover": bool,
    },
    total=False,
)


class RebootDBInstanceMessageRequestTypeDef(
    _RequiredRebootDBInstanceMessageRequestTypeDef, _OptionalRebootDBInstanceMessageRequestTypeDef
):
    pass


RemoveFromGlobalClusterMessageRequestTypeDef = TypedDict(
    "RemoveFromGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "DbClusterIdentifier": str,
    },
)

RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef = TypedDict(
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SourceIdentifier": str,
    },
)

RemoveTagsFromResourceMessageRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
        "TagKeys": Sequence[str],
    },
)

StartDBClusterMessageRequestTypeDef = TypedDict(
    "StartDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

StopDBClusterMessageRequestTypeDef = TypedDict(
    "StopDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

AddSourceIdentifierToSubscriptionResultTypeDef = TypedDict(
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEventSubscriptionResultTypeDef = TypedDict(
    "CreateEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupNameMessageTypeDef = TypedDict(
    "DBClusterParameterGroupNameMessageTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEventSubscriptionResultTypeDef = TypedDict(
    "DeleteEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventSubscriptionsMessageTypeDef = TypedDict(
    "EventSubscriptionsMessageTypeDef",
    {
        "Marker": str,
        "EventSubscriptionsList": List[EventSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyEventSubscriptionResultTypeDef = TypedDict(
    "ModifyEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveSourceIdentifierFromSubscriptionResultTypeDef = TypedDict(
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsToResourceMessageRequestTypeDef = TypedDict(
    "AddTagsToResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCopyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "SourceDBClusterParameterGroupIdentifier": str,
        "TargetDBClusterParameterGroupIdentifier": str,
        "TargetDBClusterParameterGroupDescription": str,
    },
)
_OptionalCopyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredCopyDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalCopyDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCopyDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBClusterSnapshotMessageRequestTypeDef",
    {
        "SourceDBClusterSnapshotIdentifier": str,
        "TargetDBClusterSnapshotIdentifier": str,
    },
)
_OptionalCopyDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBClusterSnapshotMessageRequestTypeDef",
    {
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "CopyTags": bool,
        "Tags": Sequence[TagTypeDef],
        "SourceRegion": str,
    },
    total=False,
)


class CopyDBClusterSnapshotMessageRequestTypeDef(
    _RequiredCopyDBClusterSnapshotMessageRequestTypeDef,
    _OptionalCopyDBClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Engine": str,
    },
)
_OptionalCreateDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterMessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "BackupRetentionPeriod": int,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "DBSubnetGroupName": str,
        "EngineVersion": str,
        "Port": int,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "Tags": Sequence[TagTypeDef],
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DeletionProtection": bool,
        "GlobalClusterIdentifier": str,
        "SourceRegion": str,
    },
    total=False,
)


class CreateDBClusterMessageRequestTypeDef(
    _RequiredCreateDBClusterMessageRequestTypeDef, _OptionalCreateDBClusterMessageRequestTypeDef
):
    pass


_RequiredCreateDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
    },
)
_OptionalCreateDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredCreateDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalCreateDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterSnapshotMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "DBClusterIdentifier": str,
    },
)
_OptionalCreateDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterSnapshotMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterSnapshotMessageRequestTypeDef(
    _RequiredCreateDBClusterSnapshotMessageRequestTypeDef,
    _OptionalCreateDBClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCreateDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
        "DBClusterIdentifier": str,
    },
)
_OptionalCreateDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBInstanceMessageRequestTypeDef",
    {
        "AvailabilityZone": str,
        "PreferredMaintenanceWindow": str,
        "AutoMinorVersionUpgrade": bool,
        "Tags": Sequence[TagTypeDef],
        "PromotionTier": int,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
    },
    total=False,
)


class CreateDBInstanceMessageRequestTypeDef(
    _RequiredCreateDBInstanceMessageRequestTypeDef, _OptionalCreateDBInstanceMessageRequestTypeDef
):
    pass


_RequiredCreateDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "DBSubnetGroupDescription": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBSubnetGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBSubnetGroupMessageRequestTypeDef(
    _RequiredCreateDBSubnetGroupMessageRequestTypeDef,
    _OptionalCreateDBSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SnsTopicArn": str,
    },
)
_OptionalCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SourceType": str,
        "EventCategories": Sequence[str],
        "SourceIds": Sequence[str],
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEventSubscriptionMessageRequestTypeDef(
    _RequiredCreateEventSubscriptionMessageRequestTypeDef,
    _OptionalCreateEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "Engine": str,
    },
)
_OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "EngineVersion": str,
        "Port": int,
        "DBSubnetGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DeletionProtection": bool,
    },
    total=False,
)


class RestoreDBClusterFromSnapshotMessageRequestTypeDef(
    _RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef,
    _OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef,
):
    pass


_RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "SourceDBClusterIdentifier": str,
    },
)
_OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef",
    {
        "RestoreToTime": Union[datetime, str],
        "UseLatestRestorableTime": bool,
        "Port": int,
        "DBSubnetGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DeletionProtection": bool,
    },
    total=False,
)


class RestoreDBClusterToPointInTimeMessageRequestTypeDef(
    _RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef,
    _OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef,
):
    pass


TagListMessageTypeDef = TypedDict(
    "TagListMessageTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OrderableDBInstanceOptionTypeDef = TypedDict(
    "OrderableDBInstanceOptionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "Vpc": bool,
    },
    total=False,
)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AvailabilityZoneTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

CertificateMessageTypeDef = TypedDict(
    "CertificateMessageTypeDef",
    {
        "Certificates": List[CertificateTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredModifyDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalModifyDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterMessageRequestTypeDef",
    {
        "NewDBClusterIdentifier": str,
        "ApplyImmediately": bool,
        "BackupRetentionPeriod": int,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Port": int,
        "MasterUserPassword": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "CloudwatchLogsExportConfiguration": CloudwatchLogsExportConfigurationTypeDef,
        "EngineVersion": str,
        "DeletionProtection": bool,
    },
    total=False,
)


class ModifyDBClusterMessageRequestTypeDef(
    _RequiredModifyDBClusterMessageRequestTypeDef, _OptionalModifyDBClusterMessageRequestTypeDef
):
    pass


CopyDBClusterParameterGroupResultTypeDef = TypedDict(
    "CopyDBClusterParameterGroupResultTypeDef",
    {
        "DBClusterParameterGroup": DBClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterParameterGroupResultTypeDef = TypedDict(
    "CreateDBClusterParameterGroupResultTypeDef",
    {
        "DBClusterParameterGroup": DBClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupsMessageTypeDef = TypedDict(
    "DBClusterParameterGroupsMessageTypeDef",
    {
        "Marker": str,
        "DBClusterParameterGroups": List[DBClusterParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyDBClusterSnapshotResultTypeDef = TypedDict(
    "CopyDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterSnapshotResultTypeDef = TypedDict(
    "CreateDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterSnapshotMessageTypeDef = TypedDict(
    "DBClusterSnapshotMessageTypeDef",
    {
        "Marker": str,
        "DBClusterSnapshots": List[DBClusterSnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterSnapshotResultTypeDef = TypedDict(
    "DeleteDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupDetailsTypeDef = TypedDict(
    "DBClusterParameterGroupDetailsTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EngineDefaultsTypeDef = TypedDict(
    "EngineDefaultsTypeDef",
    {
        "DBParameterGroupFamily": str,
        "Marker": str,
        "Parameters": List[ParameterTypeDef],
    },
    total=False,
)

ModifyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Parameters": Sequence[ParameterTypeDef],
    },
)

_RequiredResetDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredResetDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalResetDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalResetDBClusterParameterGroupMessageRequestTypeDef",
    {
        "ResetAllParameters": bool,
        "Parameters": Sequence[ParameterTypeDef],
    },
    total=False,
)


class ResetDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredResetDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalResetDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


DBClusterSnapshotAttributesResultTypeDef = TypedDict(
    "DBClusterSnapshotAttributesResultTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "DBClusterSnapshotAttributes": List[DBClusterSnapshotAttributeTypeDef],
    },
    total=False,
)

DBClusterTypeDef = TypedDict(
    "DBClusterTypeDef",
    {
        "AvailabilityZones": List[str],
        "BackupRetentionPeriod": int,
        "DBClusterIdentifier": str,
        "DBClusterParameterGroup": str,
        "DBSubnetGroup": str,
        "Status": str,
        "PercentProgress": str,
        "EarliestRestorableTime": datetime,
        "Endpoint": str,
        "ReaderEndpoint": str,
        "MultiAZ": bool,
        "Engine": str,
        "EngineVersion": str,
        "LatestRestorableTime": datetime,
        "Port": int,
        "MasterUsername": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReplicationSourceIdentifier": str,
        "ReadReplicaIdentifiers": List[str],
        "DBClusterMembers": List[DBClusterMemberTypeDef],
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "HostedZoneId": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterResourceId": str,
        "DBClusterArn": str,
        "AssociatedRoles": List[DBClusterRoleTypeDef],
        "ClusterCreateTime": datetime,
        "EnabledCloudwatchLogsExports": List[str],
        "DeletionProtection": bool,
    },
    total=False,
)

DBEngineVersionTypeDef = TypedDict(
    "DBEngineVersionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "DBEngineDescription": str,
        "DBEngineVersionDescription": str,
        "ValidUpgradeTarget": List[UpgradeTargetTypeDef],
        "ExportableLogTypes": List[str],
        "SupportsLogExportsToCloudwatchLogs": bool,
    },
    total=False,
)

DescribeCertificatesMessageRequestTypeDef = TypedDict(
    "DescribeCertificatesMessageRequestTypeDef",
    {
        "CertificateIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBClusterParameterGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBClusterParametersMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalDescribeDBClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBClusterParametersMessageRequestTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBClusterParametersMessageRequestTypeDef(
    _RequiredDescribeDBClusterParametersMessageRequestTypeDef,
    _OptionalDescribeDBClusterParametersMessageRequestTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
    },
    total=False,
)

DescribeDBClustersMessageRequestTypeDef = TypedDict(
    "DescribeDBClustersMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBEngineVersionsMessageRequestTypeDef = TypedDict(
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "DefaultOnly": bool,
        "ListSupportedCharacterSets": bool,
        "ListSupportedTimezones": bool,
    },
    total=False,
)

DescribeDBInstancesMessageRequestTypeDef = TypedDict(
    "DescribeDBInstancesMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBSubnetGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeEngineDefaultClusterParametersMessageRequestTypeDef(
    _RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef,
    _OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef,
):
    pass


DescribeEventCategoriesMessageRequestTypeDef = TypedDict(
    "DescribeEventCategoriesMessageRequestTypeDef",
    {
        "SourceType": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

DescribeEventSubscriptionsMessageRequestTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventsMessageRequestTypeDef = TypedDict(
    "DescribeEventsMessageRequestTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeGlobalClustersMessageRequestTypeDef = TypedDict(
    "DescribeGlobalClustersMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    {
        "Engine": str,
    },
)
_OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    {
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "Vpc": bool,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeOrderableDBInstanceOptionsMessageRequestTypeDef(
    _RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
    _OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
):
    pass


DescribePendingMaintenanceActionsMessageRequestTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

_RequiredListTagsForResourceMessageRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
    },
)
_OptionalListTagsForResourceMessageRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class ListTagsForResourceMessageRequestTypeDef(
    _RequiredListTagsForResourceMessageRequestTypeDef,
    _OptionalListTagsForResourceMessageRequestTypeDef,
):
    pass


DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef = TypedDict(
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    {
        "CertificateIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef(
    _RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
    _OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "IncludeShared": bool,
        "IncludePublic": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef = TypedDict(
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef = TypedDict(
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "Filters": Sequence[FilterTypeDef],
        "DefaultOnly": bool,
        "ListSupportedCharacterSets": bool,
        "ListSupportedTimezones": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef = TypedDict(
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    {
        "DBSubnetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventsMessageDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef = TypedDict(
    "DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    {
        "Engine": str,
    },
)
_OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    {
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "Vpc": bool,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef(
    _RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
    _OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
):
    pass


DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef = (
    TypedDict(
        "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
        {
            "ResourceIdentifier": str,
            "Filters": Sequence[FilterTypeDef],
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef = TypedDict(
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef = TypedDict(
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

EventCategoriesMessageTypeDef = TypedDict(
    "EventCategoriesMessageTypeDef",
    {
        "EventCategoriesMapList": List[EventCategoriesMapTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventsMessageTypeDef = TypedDict(
    "EventsMessageTypeDef",
    {
        "Marker": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GlobalClusterTypeDef = TypedDict(
    "GlobalClusterTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "GlobalClusterResourceId": str,
        "GlobalClusterArn": str,
        "Status": str,
        "Engine": str,
        "EngineVersion": str,
        "DatabaseName": str,
        "StorageEncrypted": bool,
        "DeletionProtection": bool,
        "GlobalClusterMembers": List[GlobalClusterMemberTypeDef],
    },
    total=False,
)

PendingModifiedValuesTypeDef = TypedDict(
    "PendingModifiedValuesTypeDef",
    {
        "DBInstanceClass": str,
        "AllocatedStorage": int,
        "MasterUserPassword": str,
        "Port": int,
        "BackupRetentionPeriod": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "DBInstanceIdentifier": str,
        "StorageType": str,
        "CACertificateIdentifier": str,
        "DBSubnetGroupName": str,
        "PendingCloudwatchLogsExports": PendingCloudwatchLogsExportsTypeDef,
    },
    total=False,
)

ResourcePendingMaintenanceActionsTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionsTypeDef",
    {
        "ResourceIdentifier": str,
        "PendingMaintenanceActionDetails": List[PendingMaintenanceActionTypeDef],
    },
    total=False,
)

OrderableDBInstanceOptionsMessageTypeDef = TypedDict(
    "OrderableDBInstanceOptionsMessageTypeDef",
    {
        "OrderableDBInstanceOptions": List[OrderableDBInstanceOptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBSubnetGroupTypeDef = TypedDict(
    "DBSubnetGroupTypeDef",
    {
        "DBSubnetGroupName": str,
        "DBSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetTypeDef],
        "DBSubnetGroupArn": str,
    },
    total=False,
)

DescribeEngineDefaultClusterParametersResultTypeDef = TypedDict(
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    {
        "EngineDefaults": EngineDefaultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBClusterSnapshotAttributesResultTypeDef = TypedDict(
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    {
        "DBClusterSnapshotAttributesResult": DBClusterSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBClusterSnapshotAttributeResultTypeDef = TypedDict(
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    {
        "DBClusterSnapshotAttributesResult": DBClusterSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterResultTypeDef = TypedDict(
    "CreateDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterMessageTypeDef = TypedDict(
    "DBClusterMessageTypeDef",
    {
        "Marker": str,
        "DBClusters": List[DBClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterResultTypeDef = TypedDict(
    "DeleteDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FailoverDBClusterResultTypeDef = TypedDict(
    "FailoverDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBClusterResultTypeDef = TypedDict(
    "ModifyDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterFromSnapshotResultTypeDef = TypedDict(
    "RestoreDBClusterFromSnapshotResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterToPointInTimeResultTypeDef = TypedDict(
    "RestoreDBClusterToPointInTimeResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDBClusterResultTypeDef = TypedDict(
    "StartDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDBClusterResultTypeDef = TypedDict(
    "StopDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBEngineVersionMessageTypeDef = TypedDict(
    "DBEngineVersionMessageTypeDef",
    {
        "Marker": str,
        "DBEngineVersions": List[DBEngineVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGlobalClusterResultTypeDef = TypedDict(
    "CreateGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGlobalClusterResultTypeDef = TypedDict(
    "DeleteGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GlobalClustersMessageTypeDef = TypedDict(
    "GlobalClustersMessageTypeDef",
    {
        "Marker": str,
        "GlobalClusters": List[GlobalClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyGlobalClusterResultTypeDef = TypedDict(
    "ModifyGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveFromGlobalClusterResultTypeDef = TypedDict(
    "RemoveFromGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ApplyPendingMaintenanceActionResultTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionResultTypeDef",
    {
        "ResourcePendingMaintenanceActions": ResourcePendingMaintenanceActionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PendingMaintenanceActionsMessageTypeDef = TypedDict(
    "PendingMaintenanceActionsMessageTypeDef",
    {
        "PendingMaintenanceActions": List[ResourcePendingMaintenanceActionsTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBSubnetGroupResultTypeDef = TypedDict(
    "CreateDBSubnetGroupResultTypeDef",
    {
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceTypeDef = TypedDict(
    "DBInstanceTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
        "DBInstanceStatus": str,
        "Endpoint": EndpointTypeDef,
        "InstanceCreateTime": datetime,
        "PreferredBackupWindow": str,
        "BackupRetentionPeriod": int,
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "AvailabilityZone": str,
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": PendingModifiedValuesTypeDef,
        "LatestRestorableTime": datetime,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "PubliclyAccessible": bool,
        "StatusInfos": List[DBInstanceStatusInfoTypeDef],
        "DBClusterIdentifier": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbiResourceId": str,
        "CACertificateIdentifier": str,
        "PromotionTier": int,
        "DBInstanceArn": str,
        "EnabledCloudwatchLogsExports": List[str],
    },
    total=False,
)

DBSubnetGroupMessageTypeDef = TypedDict(
    "DBSubnetGroupMessageTypeDef",
    {
        "Marker": str,
        "DBSubnetGroups": List[DBSubnetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBSubnetGroupResultTypeDef = TypedDict(
    "ModifyDBSubnetGroupResultTypeDef",
    {
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBInstanceResultTypeDef = TypedDict(
    "CreateDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceMessageTypeDef = TypedDict(
    "DBInstanceMessageTypeDef",
    {
        "Marker": str,
        "DBInstances": List[DBInstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBInstanceResultTypeDef = TypedDict(
    "DeleteDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBInstanceResultTypeDef = TypedDict(
    "ModifyDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootDBInstanceResultTypeDef = TypedDict(
    "RebootDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
