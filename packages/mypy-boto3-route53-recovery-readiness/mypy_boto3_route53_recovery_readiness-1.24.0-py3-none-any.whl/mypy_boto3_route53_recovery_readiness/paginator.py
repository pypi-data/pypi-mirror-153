"""
Type annotations for route53-recovery-readiness service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53_recovery_readiness.client import Route53RecoveryReadinessClient
    from mypy_boto3_route53_recovery_readiness.paginator import (
        GetCellReadinessSummaryPaginator,
        GetReadinessCheckResourceStatusPaginator,
        GetReadinessCheckStatusPaginator,
        GetRecoveryGroupReadinessSummaryPaginator,
        ListCellsPaginator,
        ListCrossAccountAuthorizationsPaginator,
        ListReadinessChecksPaginator,
        ListRecoveryGroupsPaginator,
        ListResourceSetsPaginator,
        ListRulesPaginator,
    )

    session = Session()
    client: Route53RecoveryReadinessClient = session.client("route53-recovery-readiness")

    get_cell_readiness_summary_paginator: GetCellReadinessSummaryPaginator = client.get_paginator("get_cell_readiness_summary")
    get_readiness_check_resource_status_paginator: GetReadinessCheckResourceStatusPaginator = client.get_paginator("get_readiness_check_resource_status")
    get_readiness_check_status_paginator: GetReadinessCheckStatusPaginator = client.get_paginator("get_readiness_check_status")
    get_recovery_group_readiness_summary_paginator: GetRecoveryGroupReadinessSummaryPaginator = client.get_paginator("get_recovery_group_readiness_summary")
    list_cells_paginator: ListCellsPaginator = client.get_paginator("list_cells")
    list_cross_account_authorizations_paginator: ListCrossAccountAuthorizationsPaginator = client.get_paginator("list_cross_account_authorizations")
    list_readiness_checks_paginator: ListReadinessChecksPaginator = client.get_paginator("list_readiness_checks")
    list_recovery_groups_paginator: ListRecoveryGroupsPaginator = client.get_paginator("list_recovery_groups")
    list_resource_sets_paginator: ListResourceSetsPaginator = client.get_paginator("list_resource_sets")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GetCellReadinessSummaryResponseTypeDef,
    GetReadinessCheckResourceStatusResponseTypeDef,
    GetReadinessCheckStatusResponseTypeDef,
    GetRecoveryGroupReadinessSummaryResponseTypeDef,
    ListCellsResponseTypeDef,
    ListCrossAccountAuthorizationsResponseTypeDef,
    ListReadinessChecksResponseTypeDef,
    ListRecoveryGroupsResponseTypeDef,
    ListResourceSetsResponseTypeDef,
    ListRulesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetCellReadinessSummaryPaginator",
    "GetReadinessCheckResourceStatusPaginator",
    "GetReadinessCheckStatusPaginator",
    "GetRecoveryGroupReadinessSummaryPaginator",
    "ListCellsPaginator",
    "ListCrossAccountAuthorizationsPaginator",
    "ListReadinessChecksPaginator",
    "ListRecoveryGroupsPaginator",
    "ListResourceSetsPaginator",
    "ListRulesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetCellReadinessSummaryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getcellreadinesssummarypaginator)
    """

    def paginate(
        self, *, CellName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetCellReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getcellreadinesssummarypaginator)
        """


class GetReadinessCheckResourceStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckresourcestatuspaginator)
    """

    def paginate(
        self,
        *,
        ReadinessCheckName: str,
        ResourceIdentifier: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetReadinessCheckResourceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckresourcestatuspaginator)
        """


class GetReadinessCheckStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckstatuspaginator)
    """

    def paginate(
        self, *, ReadinessCheckName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetReadinessCheckStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckstatuspaginator)
        """


class GetRecoveryGroupReadinessSummaryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getrecoverygroupreadinesssummarypaginator)
    """

    def paginate(
        self, *, RecoveryGroupName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRecoveryGroupReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getrecoverygroupreadinesssummarypaginator)
        """


class ListCellsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCells)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcellspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCellsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCells.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcellspaginator)
        """


class ListCrossAccountAuthorizationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcrossaccountauthorizationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCrossAccountAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcrossaccountauthorizationspaginator)
        """


class ListReadinessChecksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listreadinesscheckspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListReadinessChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listreadinesscheckspaginator)
        """


class ListRecoveryGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrecoverygroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecoveryGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrecoverygroupspaginator)
        """


class ListResourceSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListResourceSets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listresourcesetspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListResourceSets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listresourcesetspaginator)
        """


class ListRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrulespaginator)
    """

    def paginate(
        self, *, ResourceType: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrulespaginator)
        """
