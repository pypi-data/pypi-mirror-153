"""
Type annotations for docdb service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_docdb.client import DocDBClient
    from mypy_boto3_docdb.paginator import (
        DescribeCertificatesPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeGlobalClustersPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
    )

    session = Session()
    client: DocDBClient = session.client("docdb")

    describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
    describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
    describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
    describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
    describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
    describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
    describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
    describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
    describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
    describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
    describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import SourceTypeType
from .type_defs import (
    CertificateMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FilterTypeDef,
    GlobalClustersMessageTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PaginatorConfigTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
)

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeCertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describecertificatespaginator)
    """

    def paginate(
        self,
        *,
        CertificateIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeCertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describecertificatespaginator)
        """


class DescribeDBClusterParameterGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameterGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterParameterGroupName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparametergroupspaginator)
        """


class DescribeDBClusterParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterparameterspaginator)
        """


class DescribeDBClusterSnapshotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterSnapshots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclustersnapshotspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclustersnapshotspaginator)
        """


class DescribeDBClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbclusterspaginator)
        """


class DescribeDBEngineVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBEngineVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbengineversionspaginator)
    """

    def paginate(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        DBParameterGroupFamily: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        DefaultOnly: bool = ...,
        ListSupportedCharacterSets: bool = ...,
        ListSupportedTimezones: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBEngineVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbengineversionspaginator)
        """


class DescribeDBInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbinstancespaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbinstancespaginator)
        """


class DescribeDBSubnetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBSubnetGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbsubnetgroupspaginator)
    """

    def paginate(
        self,
        *,
        DBSubnetGroupName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBSubnetGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describedbsubnetgroupspaginator)
        """


class DescribeEventSubscriptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEventSubscriptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventsubscriptionspaginator)
    """

    def paginate(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEventSubscriptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventsubscriptionspaginator)
        """


class DescribeEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventspaginator)
    """

    def paginate(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeeventspaginator)
        """


class DescribeGlobalClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeGlobalClusters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeglobalclusterspaginator)
    """

    def paginate(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeGlobalClusters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeglobalclusterspaginator)
        """


class DescribeOrderableDBInstanceOptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
    """

    def paginate(
        self,
        *,
        Engine: str,
        EngineVersion: str = ...,
        DBInstanceClass: str = ...,
        LicenseModel: str = ...,
        Vpc: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
        """


class DescribePendingMaintenanceActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribePendingMaintenanceActions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describependingmaintenanceactionspaginator)
    """

    def paginate(
        self,
        *,
        ResourceIdentifier: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb/paginators/#describependingmaintenanceactionspaginator)
        """
