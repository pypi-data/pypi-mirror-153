"""
Type annotations for docdb service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_docdb.client import DocDBClient

    session = Session()
    client: DocDBClient = session.client("docdb")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import SourceTypeType
from .paginator import (
    DescribeCertificatesPaginator,
    DescribeDBClusterParameterGroupsPaginator,
    DescribeDBClusterParametersPaginator,
    DescribeDBClusterSnapshotsPaginator,
    DescribeDBClustersPaginator,
    DescribeDBEngineVersionsPaginator,
    DescribeDBInstancesPaginator,
    DescribeDBSubnetGroupsPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeGlobalClustersPaginator,
    DescribeOrderableDBInstanceOptionsPaginator,
    DescribePendingMaintenanceActionsPaginator,
)
from .type_defs import (
    AddSourceIdentifierToSubscriptionResultTypeDef,
    ApplyPendingMaintenanceActionResultTypeDef,
    CertificateMessageTypeDef,
    CloudwatchLogsExportConfigurationTypeDef,
    CopyDBClusterParameterGroupResultTypeDef,
    CopyDBClusterSnapshotResultTypeDef,
    CreateDBClusterParameterGroupResultTypeDef,
    CreateDBClusterResultTypeDef,
    CreateDBClusterSnapshotResultTypeDef,
    CreateDBInstanceResultTypeDef,
    CreateDBSubnetGroupResultTypeDef,
    CreateEventSubscriptionResultTypeDef,
    CreateGlobalClusterResultTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupNameMessageTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DeleteDBClusterResultTypeDef,
    DeleteDBClusterSnapshotResultTypeDef,
    DeleteDBInstanceResultTypeDef,
    DeleteEventSubscriptionResultTypeDef,
    DeleteGlobalClusterResultTypeDef,
    DescribeDBClusterSnapshotAttributesResultTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EventCategoriesMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FailoverDBClusterResultTypeDef,
    FilterTypeDef,
    GlobalClustersMessageTypeDef,
    ModifyDBClusterResultTypeDef,
    ModifyDBClusterSnapshotAttributeResultTypeDef,
    ModifyDBInstanceResultTypeDef,
    ModifyDBSubnetGroupResultTypeDef,
    ModifyEventSubscriptionResultTypeDef,
    ModifyGlobalClusterResultTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    ParameterTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    RebootDBInstanceResultTypeDef,
    RemoveFromGlobalClusterResultTypeDef,
    RemoveSourceIdentifierFromSubscriptionResultTypeDef,
    RestoreDBClusterFromSnapshotResultTypeDef,
    RestoreDBClusterToPointInTimeResultTypeDef,
    StartDBClusterResultTypeDef,
    StopDBClusterResultTypeDef,
    TagListMessageTypeDef,
    TagTypeDef,
)
from .waiter import DBInstanceAvailableWaiter, DBInstanceDeletedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DocDBClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    CertificateNotFoundFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DBClusterAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterNotFoundFault: Type[BotocoreClientError]
    DBClusterParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBClusterQuotaExceededFault: Type[BotocoreClientError]
    DBClusterSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterSnapshotNotFoundFault: Type[BotocoreClientError]
    DBInstanceAlreadyExistsFault: Type[BotocoreClientError]
    DBInstanceNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSecurityGroupNotFoundFault: Type[BotocoreClientError]
    DBSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBSnapshotNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBSubnetGroupDoesNotCoverEnoughAZs: Type[BotocoreClientError]
    DBSubnetGroupNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSubnetQuotaExceededFault: Type[BotocoreClientError]
    DBUpgradeDependencyFailureFault: Type[BotocoreClientError]
    EventSubscriptionQuotaExceededFault: Type[BotocoreClientError]
    GlobalClusterAlreadyExistsFault: Type[BotocoreClientError]
    GlobalClusterNotFoundFault: Type[BotocoreClientError]
    GlobalClusterQuotaExceededFault: Type[BotocoreClientError]
    InstanceQuotaExceededFault: Type[BotocoreClientError]
    InsufficientDBClusterCapacityFault: Type[BotocoreClientError]
    InsufficientDBInstanceCapacityFault: Type[BotocoreClientError]
    InsufficientStorageClusterCapacityFault: Type[BotocoreClientError]
    InvalidDBClusterSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBClusterStateFault: Type[BotocoreClientError]
    InvalidDBInstanceStateFault: Type[BotocoreClientError]
    InvalidDBParameterGroupStateFault: Type[BotocoreClientError]
    InvalidDBSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidDBSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBSubnetGroupStateFault: Type[BotocoreClientError]
    InvalidDBSubnetStateFault: Type[BotocoreClientError]
    InvalidEventSubscriptionStateFault: Type[BotocoreClientError]
    InvalidGlobalClusterStateFault: Type[BotocoreClientError]
    InvalidRestoreFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    KMSKeyNotAccessibleFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    SNSTopicArnNotFoundFault: Type[BotocoreClientError]
    SharedSnapshotQuotaExceededFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SourceNotFoundFault: Type[BotocoreClientError]
    StorageQuotaExceededFault: Type[BotocoreClientError]
    StorageTypeNotSupportedFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    SubscriptionAlreadyExistFault: Type[BotocoreClientError]
    SubscriptionCategoryNotFoundFault: Type[BotocoreClientError]
    SubscriptionNotFoundFault: Type[BotocoreClientError]


class DocDBClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DocDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#exceptions)
        """

    def add_source_identifier_to_subscription(
        self, *, SubscriptionName: str, SourceIdentifier: str
    ) -> AddSourceIdentifierToSubscriptionResultTypeDef:
        """
        Adds a source identifier to an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.add_source_identifier_to_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#add_source_identifier_to_subscription)
        """

    def add_tags_to_resource(
        self, *, ResourceName: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds metadata tags to an Amazon DocumentDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.add_tags_to_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#add_tags_to_resource)
        """

    def apply_pending_maintenance_action(
        self, *, ResourceIdentifier: str, ApplyAction: str, OptInType: str
    ) -> ApplyPendingMaintenanceActionResultTypeDef:
        """
        Applies a pending maintenance action to a resource (for example, to an Amazon
        DocumentDB instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.apply_pending_maintenance_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#apply_pending_maintenance_action)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#can_paginate)
        """

    def copy_db_cluster_parameter_group(
        self,
        *,
        SourceDBClusterParameterGroupIdentifier: str,
        TargetDBClusterParameterGroupIdentifier: str,
        TargetDBClusterParameterGroupDescription: str,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CopyDBClusterParameterGroupResultTypeDef:
        """
        Copies the specified cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.copy_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#copy_db_cluster_parameter_group)
        """

    def copy_db_cluster_snapshot(
        self,
        *,
        SourceDBClusterSnapshotIdentifier: str,
        TargetDBClusterSnapshotIdentifier: str,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        CopyTags: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SourceRegion: str = ...
    ) -> CopyDBClusterSnapshotResultTypeDef:
        """
        Copies a snapshot of a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.copy_db_cluster_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#copy_db_cluster_snapshot)
        """

    def create_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        Engine: str,
        AvailabilityZones: Sequence[str] = ...,
        BackupRetentionPeriod: int = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        DBSubnetGroupName: str = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        MasterUsername: str = ...,
        MasterUserPassword: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DeletionProtection: bool = ...,
        GlobalClusterIdentifier: str = ...,
        SourceRegion: str = ...
    ) -> CreateDBClusterResultTypeDef:
        """
        Creates a new Amazon DocumentDB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_db_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_db_cluster)
        """

    def create_db_cluster_parameter_group(
        self,
        *,
        DBClusterParameterGroupName: str,
        DBParameterGroupFamily: str,
        Description: str,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateDBClusterParameterGroupResultTypeDef:
        """
        Creates a new cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_db_cluster_parameter_group)
        """

    def create_db_cluster_snapshot(
        self,
        *,
        DBClusterSnapshotIdentifier: str,
        DBClusterIdentifier: str,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateDBClusterSnapshotResultTypeDef:
        """
        Creates a snapshot of a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_db_cluster_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_db_cluster_snapshot)
        """

    def create_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        DBInstanceClass: str,
        Engine: str,
        DBClusterIdentifier: str,
        AvailabilityZone: str = ...,
        PreferredMaintenanceWindow: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        PromotionTier: int = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...
    ) -> CreateDBInstanceResultTypeDef:
        """
        Creates a new instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_db_instance)
        """

    def create_db_subnet_group(
        self,
        *,
        DBSubnetGroupName: str,
        DBSubnetGroupDescription: str,
        SubnetIds: Sequence[str],
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateDBSubnetGroupResultTypeDef:
        """
        Creates a new subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_db_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_db_subnet_group)
        """

    def create_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        SourceIds: Sequence[str] = ...,
        Enabled: bool = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateEventSubscriptionResultTypeDef:
        """
        Creates an Amazon DocumentDB event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_event_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_event_subscription)
        """

    def create_global_cluster(
        self,
        *,
        GlobalClusterIdentifier: str,
        SourceDBClusterIdentifier: str = ...,
        Engine: str = ...,
        EngineVersion: str = ...,
        DeletionProtection: bool = ...,
        DatabaseName: str = ...,
        StorageEncrypted: bool = ...
    ) -> CreateGlobalClusterResultTypeDef:
        """
        Creates an Amazon DocumentDB global cluster that can span multiple multiple
        Amazon Web Services Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.create_global_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#create_global_cluster)
        """

    def delete_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        SkipFinalSnapshot: bool = ...,
        FinalDBSnapshotIdentifier: str = ...
    ) -> DeleteDBClusterResultTypeDef:
        """
        Deletes a previously provisioned cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_db_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_db_cluster)
        """

    def delete_db_cluster_parameter_group(
        self, *, DBClusterParameterGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_db_cluster_parameter_group)
        """

    def delete_db_cluster_snapshot(
        self, *, DBClusterSnapshotIdentifier: str
    ) -> DeleteDBClusterSnapshotResultTypeDef:
        """
        Deletes a cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_db_cluster_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_db_cluster_snapshot)
        """

    def delete_db_instance(self, *, DBInstanceIdentifier: str) -> DeleteDBInstanceResultTypeDef:
        """
        Deletes a previously provisioned instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_db_instance)
        """

    def delete_db_subnet_group(self, *, DBSubnetGroupName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_db_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_db_subnet_group)
        """

    def delete_event_subscription(
        self, *, SubscriptionName: str
    ) -> DeleteEventSubscriptionResultTypeDef:
        """
        Deletes an Amazon DocumentDB event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_event_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_event_subscription)
        """

    def delete_global_cluster(
        self, *, GlobalClusterIdentifier: str
    ) -> DeleteGlobalClusterResultTypeDef:
        """
        Deletes a global cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.delete_global_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#delete_global_cluster)
        """

    def describe_certificates(
        self,
        *,
        CertificateIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> CertificateMessageTypeDef:
        """
        Returns a list of certificate authority (CA) certificates provided by Amazon
        DocumentDB for this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_certificates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_certificates)
        """

    def describe_db_cluster_parameter_groups(
        self,
        *,
        DBClusterParameterGroupName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterParameterGroupsMessageTypeDef:
        """
        Returns a list of `DBClusterParameterGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_cluster_parameter_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_cluster_parameter_groups)
        """

    def describe_db_cluster_parameters(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_cluster_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_cluster_parameters)
        """

    def describe_db_cluster_snapshot_attributes(
        self, *, DBClusterSnapshotIdentifier: str
    ) -> DescribeDBClusterSnapshotAttributesResultTypeDef:
        """
        Returns a list of cluster snapshot attribute names and values for a manual DB
        cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_cluster_snapshot_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_cluster_snapshot_attributes)
        """

    def describe_db_cluster_snapshots(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...
    ) -> DBClusterSnapshotMessageTypeDef:
        """
        Returns information about cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_cluster_snapshots)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_cluster_snapshots)
        """

    def describe_db_clusters(
        self,
        *,
        DBClusterIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterMessageTypeDef:
        """
        Returns information about provisioned Amazon DocumentDB clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_clusters)
        """

    def describe_db_engine_versions(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        DBParameterGroupFamily: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        DefaultOnly: bool = ...,
        ListSupportedCharacterSets: bool = ...,
        ListSupportedTimezones: bool = ...
    ) -> DBEngineVersionMessageTypeDef:
        """
        Returns a list of the available engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_engine_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_engine_versions)
        """

    def describe_db_instances(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBInstanceMessageTypeDef:
        """
        Returns information about provisioned Amazon DocumentDB instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_instances)
        """

    def describe_db_subnet_groups(
        self,
        *,
        DBSubnetGroupName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBSubnetGroupMessageTypeDef:
        """
        Returns a list of `DBSubnetGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_subnet_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_db_subnet_groups)
        """

    def describe_engine_default_cluster_parameters(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEngineDefaultClusterParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the cluster
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_engine_default_cluster_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_engine_default_cluster_parameters)
        """

    def describe_event_categories(
        self, *, SourceType: str = ..., Filters: Sequence[FilterTypeDef] = ...
    ) -> EventCategoriesMessageTypeDef:
        """
        Displays a list of categories for all event source types, or, if specified, for
        a specified source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_event_categories)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_event_categories)
        """

    def describe_event_subscriptions(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> EventSubscriptionsMessageTypeDef:
        """
        Lists all the subscription descriptions for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_event_subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_event_subscriptions)
        """

    def describe_events(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> EventsMessageTypeDef:
        """
        Returns events related to instances, security groups, snapshots, and DB
        parameter groups for the past 14 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_events)
        """

    def describe_global_clusters(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> GlobalClustersMessageTypeDef:
        """
        Returns information about Amazon DocumentDB global clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_global_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_global_clusters)
        """

    def describe_orderable_db_instance_options(
        self,
        *,
        Engine: str,
        EngineVersion: str = ...,
        DBInstanceClass: str = ...,
        LicenseModel: str = ...,
        Vpc: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> OrderableDBInstanceOptionsMessageTypeDef:
        """
        Returns a list of orderable instance options for the specified engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_orderable_db_instance_options)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_orderable_db_instance_options)
        """

    def describe_pending_maintenance_actions(
        self,
        *,
        ResourceIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> PendingMaintenanceActionsMessageTypeDef:
        """
        Returns a list of resources (for example, instances) that have at least one
        pending maintenance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_pending_maintenance_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#describe_pending_maintenance_actions)
        """

    def failover_db_cluster(
        self, *, DBClusterIdentifier: str = ..., TargetDBInstanceIdentifier: str = ...
    ) -> FailoverDBClusterResultTypeDef:
        """
        Forces a failover for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.failover_db_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#failover_db_cluster)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#generate_presigned_url)
        """

    def list_tags_for_resource(
        self, *, ResourceName: str, Filters: Sequence[FilterTypeDef] = ...
    ) -> TagListMessageTypeDef:
        """
        Lists all tags on an Amazon DocumentDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#list_tags_for_resource)
        """

    def modify_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        NewDBClusterIdentifier: str = ...,
        ApplyImmediately: bool = ...,
        BackupRetentionPeriod: int = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Port: int = ...,
        MasterUserPassword: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        CloudwatchLogsExportConfiguration: CloudwatchLogsExportConfigurationTypeDef = ...,
        EngineVersion: str = ...,
        DeletionProtection: bool = ...
    ) -> ModifyDBClusterResultTypeDef:
        """
        Modifies a setting for an Amazon DocumentDB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_db_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_db_cluster)
        """

    def modify_db_cluster_parameter_group(
        self, *, DBClusterParameterGroupName: str, Parameters: Sequence[ParameterTypeDef]
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_db_cluster_parameter_group)
        """

    def modify_db_cluster_snapshot_attribute(
        self,
        *,
        DBClusterSnapshotIdentifier: str,
        AttributeName: str,
        ValuesToAdd: Sequence[str] = ...,
        ValuesToRemove: Sequence[str] = ...
    ) -> ModifyDBClusterSnapshotAttributeResultTypeDef:
        """
        Adds an attribute and values to, or removes an attribute and values from, a
        manual cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_db_cluster_snapshot_attribute)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_db_cluster_snapshot_attribute)
        """

    def modify_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        DBInstanceClass: str = ...,
        ApplyImmediately: bool = ...,
        PreferredMaintenanceWindow: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        NewDBInstanceIdentifier: str = ...,
        CACertificateIdentifier: str = ...,
        PromotionTier: int = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...
    ) -> ModifyDBInstanceResultTypeDef:
        """
        Modifies settings for an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_db_instance)
        """

    def modify_db_subnet_group(
        self,
        *,
        DBSubnetGroupName: str,
        SubnetIds: Sequence[str],
        DBSubnetGroupDescription: str = ...
    ) -> ModifyDBSubnetGroupResultTypeDef:
        """
        Modifies an existing subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_db_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_db_subnet_group)
        """

    def modify_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str = ...,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        Enabled: bool = ...
    ) -> ModifyEventSubscriptionResultTypeDef:
        """
        Modifies an existing Amazon DocumentDB event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_event_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_event_subscription)
        """

    def modify_global_cluster(
        self,
        *,
        GlobalClusterIdentifier: str,
        NewGlobalClusterIdentifier: str = ...,
        DeletionProtection: bool = ...
    ) -> ModifyGlobalClusterResultTypeDef:
        """
        Modify a setting for an Amazon DocumentDB global cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.modify_global_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#modify_global_cluster)
        """

    def reboot_db_instance(
        self, *, DBInstanceIdentifier: str, ForceFailover: bool = ...
    ) -> RebootDBInstanceResultTypeDef:
        """
        You might need to reboot your instance, usually for maintenance reasons.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.reboot_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#reboot_db_instance)
        """

    def remove_from_global_cluster(
        self, *, GlobalClusterIdentifier: str, DbClusterIdentifier: str
    ) -> RemoveFromGlobalClusterResultTypeDef:
        """
        Detaches an Amazon DocumentDB secondary cluster from a global cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.remove_from_global_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#remove_from_global_cluster)
        """

    def remove_source_identifier_from_subscription(
        self, *, SubscriptionName: str, SourceIdentifier: str
    ) -> RemoveSourceIdentifierFromSubscriptionResultTypeDef:
        """
        Removes a source identifier from an existing Amazon DocumentDB event
        notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.remove_source_identifier_from_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#remove_source_identifier_from_subscription)
        """

    def remove_tags_from_resource(
        self, *, ResourceName: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes metadata tags from an Amazon DocumentDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.remove_tags_from_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#remove_tags_from_resource)
        """

    def reset_db_cluster_parameter_group(
        self,
        *,
        DBClusterParameterGroupName: str,
        ResetAllParameters: bool = ...,
        Parameters: Sequence[ParameterTypeDef] = ...
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a cluster parameter group to the default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.reset_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#reset_db_cluster_parameter_group)
        """

    def restore_db_cluster_from_snapshot(
        self,
        *,
        DBClusterIdentifier: str,
        SnapshotIdentifier: str,
        Engine: str,
        AvailabilityZones: Sequence[str] = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        DBSubnetGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        KmsKeyId: str = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DeletionProtection: bool = ...
    ) -> RestoreDBClusterFromSnapshotResultTypeDef:
        """
        Creates a new cluster from a snapshot or cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.restore_db_cluster_from_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#restore_db_cluster_from_snapshot)
        """

    def restore_db_cluster_to_point_in_time(
        self,
        *,
        DBClusterIdentifier: str,
        SourceDBClusterIdentifier: str,
        RestoreToTime: Union[datetime, str] = ...,
        UseLatestRestorableTime: bool = ...,
        Port: int = ...,
        DBSubnetGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        KmsKeyId: str = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DeletionProtection: bool = ...
    ) -> RestoreDBClusterToPointInTimeResultTypeDef:
        """
        Restores a cluster to an arbitrary point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.restore_db_cluster_to_point_in_time)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#restore_db_cluster_to_point_in_time)
        """

    def start_db_cluster(self, *, DBClusterIdentifier: str) -> StartDBClusterResultTypeDef:
        """
        Restarts the stopped cluster that is specified by `DBClusterIdentifier`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.start_db_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#start_db_cluster)
        """

    def stop_db_cluster(self, *, DBClusterIdentifier: str) -> StopDBClusterResultTypeDef:
        """
        Stops the running cluster that is specified by `DBClusterIdentifier`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.stop_db_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#stop_db_cluster)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_certificates"]
    ) -> DescribeCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameter_groups"]
    ) -> DescribeDBClusterParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameters"]
    ) -> DescribeDBClusterParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_snapshots"]
    ) -> DescribeDBClusterSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_clusters"]
    ) -> DescribeDBClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_engine_versions"]
    ) -> DescribeDBEngineVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_instances"]
    ) -> DescribeDBInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_subnet_groups"]
    ) -> DescribeDBSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_global_clusters"]
    ) -> DescribeGlobalClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_db_instance_options"]
    ) -> DescribeOrderableDBInstanceOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pending_maintenance_actions"]
    ) -> DescribePendingMaintenanceActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_instance_available"]
    ) -> DBInstanceAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["db_instance_deleted"]) -> DBInstanceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/client/#get_waiter)
        """
