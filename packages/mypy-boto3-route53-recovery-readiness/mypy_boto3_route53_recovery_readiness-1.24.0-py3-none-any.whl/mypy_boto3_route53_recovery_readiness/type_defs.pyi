"""
Type annotations for route53-recovery-readiness service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53_recovery_readiness.type_defs import CellOutputTypeDef

    data: CellOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import ReadinessType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CellOutputTypeDef",
    "CreateCellRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateCrossAccountAuthorizationRequestRequestTypeDef",
    "CreateReadinessCheckRequestRequestTypeDef",
    "CreateRecoveryGroupRequestRequestTypeDef",
    "DeleteCellRequestRequestTypeDef",
    "DeleteCrossAccountAuthorizationRequestRequestTypeDef",
    "DeleteReadinessCheckRequestRequestTypeDef",
    "DeleteRecoveryGroupRequestRequestTypeDef",
    "DeleteResourceSetRequestRequestTypeDef",
    "GetArchitectureRecommendationsRequestRequestTypeDef",
    "RecommendationTypeDef",
    "PaginatorConfigTypeDef",
    "GetCellReadinessSummaryRequestRequestTypeDef",
    "ReadinessCheckSummaryTypeDef",
    "GetCellRequestRequestTypeDef",
    "GetReadinessCheckRequestRequestTypeDef",
    "GetReadinessCheckResourceStatusRequestRequestTypeDef",
    "GetReadinessCheckStatusRequestRequestTypeDef",
    "MessageTypeDef",
    "ResourceResultTypeDef",
    "GetRecoveryGroupReadinessSummaryRequestRequestTypeDef",
    "GetRecoveryGroupRequestRequestTypeDef",
    "GetResourceSetRequestRequestTypeDef",
    "ListCellsRequestRequestTypeDef",
    "ListCrossAccountAuthorizationsRequestRequestTypeDef",
    "ListReadinessChecksRequestRequestTypeDef",
    "ReadinessCheckOutputTypeDef",
    "ListRecoveryGroupsRequestRequestTypeDef",
    "RecoveryGroupOutputTypeDef",
    "ListResourceSetsRequestRequestTypeDef",
    "ListRulesOutputTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListTagsForResourcesRequestRequestTypeDef",
    "NLBResourceTypeDef",
    "R53ResourceRecordTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCellRequestRequestTypeDef",
    "UpdateReadinessCheckRequestRequestTypeDef",
    "UpdateRecoveryGroupRequestRequestTypeDef",
    "CreateCellResponseTypeDef",
    "CreateCrossAccountAuthorizationResponseTypeDef",
    "CreateReadinessCheckResponseTypeDef",
    "CreateRecoveryGroupResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCellResponseTypeDef",
    "GetReadinessCheckResponseTypeDef",
    "GetRecoveryGroupResponseTypeDef",
    "ListCellsResponseTypeDef",
    "ListCrossAccountAuthorizationsResponseTypeDef",
    "ListTagsForResourcesResponseTypeDef",
    "UpdateCellResponseTypeDef",
    "UpdateReadinessCheckResponseTypeDef",
    "UpdateRecoveryGroupResponseTypeDef",
    "GetArchitectureRecommendationsResponseTypeDef",
    "GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef",
    "GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef",
    "GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef",
    "GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef",
    "ListCellsRequestListCellsPaginateTypeDef",
    "ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef",
    "ListReadinessChecksRequestListReadinessChecksPaginateTypeDef",
    "ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef",
    "ListResourceSetsRequestListResourceSetsPaginateTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "GetCellReadinessSummaryResponseTypeDef",
    "GetRecoveryGroupReadinessSummaryResponseTypeDef",
    "RuleResultTypeDef",
    "GetReadinessCheckStatusResponseTypeDef",
    "ListReadinessChecksResponseTypeDef",
    "ListRecoveryGroupsResponseTypeDef",
    "ListRulesResponseTypeDef",
    "TargetResourceTypeDef",
    "GetReadinessCheckResourceStatusResponseTypeDef",
    "DNSTargetResourceTypeDef",
    "ResourceTypeDef",
    "CreateResourceSetRequestRequestTypeDef",
    "CreateResourceSetResponseTypeDef",
    "GetResourceSetResponseTypeDef",
    "ResourceSetOutputTypeDef",
    "UpdateResourceSetRequestRequestTypeDef",
    "UpdateResourceSetResponseTypeDef",
    "ListResourceSetsResponseTypeDef",
)

_RequiredCellOutputTypeDef = TypedDict(
    "_RequiredCellOutputTypeDef",
    {
        "CellArn": str,
        "CellName": str,
        "Cells": List[str],
        "ParentReadinessScopes": List[str],
    },
)
_OptionalCellOutputTypeDef = TypedDict(
    "_OptionalCellOutputTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class CellOutputTypeDef(_RequiredCellOutputTypeDef, _OptionalCellOutputTypeDef):
    pass

_RequiredCreateCellRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCellRequestRequestTypeDef",
    {
        "CellName": str,
    },
)
_OptionalCreateCellRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCellRequestRequestTypeDef",
    {
        "Cells": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateCellRequestRequestTypeDef(
    _RequiredCreateCellRequestRequestTypeDef, _OptionalCreateCellRequestRequestTypeDef
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

CreateCrossAccountAuthorizationRequestRequestTypeDef = TypedDict(
    "CreateCrossAccountAuthorizationRequestRequestTypeDef",
    {
        "CrossAccountAuthorization": str,
    },
)

_RequiredCreateReadinessCheckRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReadinessCheckRequestRequestTypeDef",
    {
        "ReadinessCheckName": str,
        "ResourceSetName": str,
    },
)
_OptionalCreateReadinessCheckRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReadinessCheckRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateReadinessCheckRequestRequestTypeDef(
    _RequiredCreateReadinessCheckRequestRequestTypeDef,
    _OptionalCreateReadinessCheckRequestRequestTypeDef,
):
    pass

_RequiredCreateRecoveryGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRecoveryGroupRequestRequestTypeDef",
    {
        "RecoveryGroupName": str,
    },
)
_OptionalCreateRecoveryGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRecoveryGroupRequestRequestTypeDef",
    {
        "Cells": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateRecoveryGroupRequestRequestTypeDef(
    _RequiredCreateRecoveryGroupRequestRequestTypeDef,
    _OptionalCreateRecoveryGroupRequestRequestTypeDef,
):
    pass

DeleteCellRequestRequestTypeDef = TypedDict(
    "DeleteCellRequestRequestTypeDef",
    {
        "CellName": str,
    },
)

DeleteCrossAccountAuthorizationRequestRequestTypeDef = TypedDict(
    "DeleteCrossAccountAuthorizationRequestRequestTypeDef",
    {
        "CrossAccountAuthorization": str,
    },
)

DeleteReadinessCheckRequestRequestTypeDef = TypedDict(
    "DeleteReadinessCheckRequestRequestTypeDef",
    {
        "ReadinessCheckName": str,
    },
)

DeleteRecoveryGroupRequestRequestTypeDef = TypedDict(
    "DeleteRecoveryGroupRequestRequestTypeDef",
    {
        "RecoveryGroupName": str,
    },
)

DeleteResourceSetRequestRequestTypeDef = TypedDict(
    "DeleteResourceSetRequestRequestTypeDef",
    {
        "ResourceSetName": str,
    },
)

_RequiredGetArchitectureRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredGetArchitectureRecommendationsRequestRequestTypeDef",
    {
        "RecoveryGroupName": str,
    },
)
_OptionalGetArchitectureRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalGetArchitectureRecommendationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetArchitectureRecommendationsRequestRequestTypeDef(
    _RequiredGetArchitectureRecommendationsRequestRequestTypeDef,
    _OptionalGetArchitectureRecommendationsRequestRequestTypeDef,
):
    pass

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "RecommendationText": str,
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

_RequiredGetCellReadinessSummaryRequestRequestTypeDef = TypedDict(
    "_RequiredGetCellReadinessSummaryRequestRequestTypeDef",
    {
        "CellName": str,
    },
)
_OptionalGetCellReadinessSummaryRequestRequestTypeDef = TypedDict(
    "_OptionalGetCellReadinessSummaryRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetCellReadinessSummaryRequestRequestTypeDef(
    _RequiredGetCellReadinessSummaryRequestRequestTypeDef,
    _OptionalGetCellReadinessSummaryRequestRequestTypeDef,
):
    pass

ReadinessCheckSummaryTypeDef = TypedDict(
    "ReadinessCheckSummaryTypeDef",
    {
        "Readiness": ReadinessType,
        "ReadinessCheckName": str,
    },
    total=False,
)

GetCellRequestRequestTypeDef = TypedDict(
    "GetCellRequestRequestTypeDef",
    {
        "CellName": str,
    },
)

GetReadinessCheckRequestRequestTypeDef = TypedDict(
    "GetReadinessCheckRequestRequestTypeDef",
    {
        "ReadinessCheckName": str,
    },
)

_RequiredGetReadinessCheckResourceStatusRequestRequestTypeDef = TypedDict(
    "_RequiredGetReadinessCheckResourceStatusRequestRequestTypeDef",
    {
        "ReadinessCheckName": str,
        "ResourceIdentifier": str,
    },
)
_OptionalGetReadinessCheckResourceStatusRequestRequestTypeDef = TypedDict(
    "_OptionalGetReadinessCheckResourceStatusRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetReadinessCheckResourceStatusRequestRequestTypeDef(
    _RequiredGetReadinessCheckResourceStatusRequestRequestTypeDef,
    _OptionalGetReadinessCheckResourceStatusRequestRequestTypeDef,
):
    pass

_RequiredGetReadinessCheckStatusRequestRequestTypeDef = TypedDict(
    "_RequiredGetReadinessCheckStatusRequestRequestTypeDef",
    {
        "ReadinessCheckName": str,
    },
)
_OptionalGetReadinessCheckStatusRequestRequestTypeDef = TypedDict(
    "_OptionalGetReadinessCheckStatusRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetReadinessCheckStatusRequestRequestTypeDef(
    _RequiredGetReadinessCheckStatusRequestRequestTypeDef,
    _OptionalGetReadinessCheckStatusRequestRequestTypeDef,
):
    pass

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "MessageText": str,
    },
    total=False,
)

_RequiredResourceResultTypeDef = TypedDict(
    "_RequiredResourceResultTypeDef",
    {
        "LastCheckedTimestamp": datetime,
        "Readiness": ReadinessType,
    },
)
_OptionalResourceResultTypeDef = TypedDict(
    "_OptionalResourceResultTypeDef",
    {
        "ComponentId": str,
        "ResourceArn": str,
    },
    total=False,
)

class ResourceResultTypeDef(_RequiredResourceResultTypeDef, _OptionalResourceResultTypeDef):
    pass

_RequiredGetRecoveryGroupReadinessSummaryRequestRequestTypeDef = TypedDict(
    "_RequiredGetRecoveryGroupReadinessSummaryRequestRequestTypeDef",
    {
        "RecoveryGroupName": str,
    },
)
_OptionalGetRecoveryGroupReadinessSummaryRequestRequestTypeDef = TypedDict(
    "_OptionalGetRecoveryGroupReadinessSummaryRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetRecoveryGroupReadinessSummaryRequestRequestTypeDef(
    _RequiredGetRecoveryGroupReadinessSummaryRequestRequestTypeDef,
    _OptionalGetRecoveryGroupReadinessSummaryRequestRequestTypeDef,
):
    pass

GetRecoveryGroupRequestRequestTypeDef = TypedDict(
    "GetRecoveryGroupRequestRequestTypeDef",
    {
        "RecoveryGroupName": str,
    },
)

GetResourceSetRequestRequestTypeDef = TypedDict(
    "GetResourceSetRequestRequestTypeDef",
    {
        "ResourceSetName": str,
    },
)

ListCellsRequestRequestTypeDef = TypedDict(
    "ListCellsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListCrossAccountAuthorizationsRequestRequestTypeDef = TypedDict(
    "ListCrossAccountAuthorizationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListReadinessChecksRequestRequestTypeDef = TypedDict(
    "ListReadinessChecksRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredReadinessCheckOutputTypeDef = TypedDict(
    "_RequiredReadinessCheckOutputTypeDef",
    {
        "ReadinessCheckArn": str,
        "ResourceSet": str,
    },
)
_OptionalReadinessCheckOutputTypeDef = TypedDict(
    "_OptionalReadinessCheckOutputTypeDef",
    {
        "ReadinessCheckName": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

class ReadinessCheckOutputTypeDef(
    _RequiredReadinessCheckOutputTypeDef, _OptionalReadinessCheckOutputTypeDef
):
    pass

ListRecoveryGroupsRequestRequestTypeDef = TypedDict(
    "ListRecoveryGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredRecoveryGroupOutputTypeDef = TypedDict(
    "_RequiredRecoveryGroupOutputTypeDef",
    {
        "Cells": List[str],
        "RecoveryGroupArn": str,
        "RecoveryGroupName": str,
    },
)
_OptionalRecoveryGroupOutputTypeDef = TypedDict(
    "_OptionalRecoveryGroupOutputTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class RecoveryGroupOutputTypeDef(
    _RequiredRecoveryGroupOutputTypeDef, _OptionalRecoveryGroupOutputTypeDef
):
    pass

ListResourceSetsRequestRequestTypeDef = TypedDict(
    "ListResourceSetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListRulesOutputTypeDef = TypedDict(
    "ListRulesOutputTypeDef",
    {
        "ResourceType": str,
        "RuleDescription": str,
        "RuleId": str,
    },
)

ListRulesRequestRequestTypeDef = TypedDict(
    "ListRulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "ResourceType": str,
    },
    total=False,
)

ListTagsForResourcesRequestRequestTypeDef = TypedDict(
    "ListTagsForResourcesRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

NLBResourceTypeDef = TypedDict(
    "NLBResourceTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

R53ResourceRecordTypeDef = TypedDict(
    "R53ResourceRecordTypeDef",
    {
        "DomainName": str,
        "RecordSetId": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateCellRequestRequestTypeDef = TypedDict(
    "UpdateCellRequestRequestTypeDef",
    {
        "CellName": str,
        "Cells": Sequence[str],
    },
)

UpdateReadinessCheckRequestRequestTypeDef = TypedDict(
    "UpdateReadinessCheckRequestRequestTypeDef",
    {
        "ReadinessCheckName": str,
        "ResourceSetName": str,
    },
)

UpdateRecoveryGroupRequestRequestTypeDef = TypedDict(
    "UpdateRecoveryGroupRequestRequestTypeDef",
    {
        "Cells": Sequence[str],
        "RecoveryGroupName": str,
    },
)

CreateCellResponseTypeDef = TypedDict(
    "CreateCellResponseTypeDef",
    {
        "CellArn": str,
        "CellName": str,
        "Cells": List[str],
        "ParentReadinessScopes": List[str],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCrossAccountAuthorizationResponseTypeDef = TypedDict(
    "CreateCrossAccountAuthorizationResponseTypeDef",
    {
        "CrossAccountAuthorization": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateReadinessCheckResponseTypeDef = TypedDict(
    "CreateReadinessCheckResponseTypeDef",
    {
        "ReadinessCheckArn": str,
        "ReadinessCheckName": str,
        "ResourceSet": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecoveryGroupResponseTypeDef = TypedDict(
    "CreateRecoveryGroupResponseTypeDef",
    {
        "Cells": List[str],
        "RecoveryGroupArn": str,
        "RecoveryGroupName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCellResponseTypeDef = TypedDict(
    "GetCellResponseTypeDef",
    {
        "CellArn": str,
        "CellName": str,
        "Cells": List[str],
        "ParentReadinessScopes": List[str],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReadinessCheckResponseTypeDef = TypedDict(
    "GetReadinessCheckResponseTypeDef",
    {
        "ReadinessCheckArn": str,
        "ReadinessCheckName": str,
        "ResourceSet": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecoveryGroupResponseTypeDef = TypedDict(
    "GetRecoveryGroupResponseTypeDef",
    {
        "Cells": List[str],
        "RecoveryGroupArn": str,
        "RecoveryGroupName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCellsResponseTypeDef = TypedDict(
    "ListCellsResponseTypeDef",
    {
        "Cells": List[CellOutputTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCrossAccountAuthorizationsResponseTypeDef = TypedDict(
    "ListCrossAccountAuthorizationsResponseTypeDef",
    {
        "CrossAccountAuthorizations": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourcesResponseTypeDef = TypedDict(
    "ListTagsForResourcesResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCellResponseTypeDef = TypedDict(
    "UpdateCellResponseTypeDef",
    {
        "CellArn": str,
        "CellName": str,
        "Cells": List[str],
        "ParentReadinessScopes": List[str],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateReadinessCheckResponseTypeDef = TypedDict(
    "UpdateReadinessCheckResponseTypeDef",
    {
        "ReadinessCheckArn": str,
        "ReadinessCheckName": str,
        "ResourceSet": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRecoveryGroupResponseTypeDef = TypedDict(
    "UpdateRecoveryGroupResponseTypeDef",
    {
        "Cells": List[str],
        "RecoveryGroupArn": str,
        "RecoveryGroupName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetArchitectureRecommendationsResponseTypeDef = TypedDict(
    "GetArchitectureRecommendationsResponseTypeDef",
    {
        "LastAuditTimestamp": datetime,
        "NextToken": str,
        "Recommendations": List[RecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef = TypedDict(
    "_RequiredGetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef",
    {
        "CellName": str,
    },
)
_OptionalGetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef = TypedDict(
    "_OptionalGetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef(
    _RequiredGetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef,
    _OptionalGetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef,
):
    pass

_RequiredGetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef = TypedDict(
    "_RequiredGetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef",
    {
        "ReadinessCheckName": str,
        "ResourceIdentifier": str,
    },
)
_OptionalGetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef = TypedDict(
    "_OptionalGetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef(
    _RequiredGetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef,
    _OptionalGetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef,
):
    pass

_RequiredGetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef = TypedDict(
    "_RequiredGetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef",
    {
        "ReadinessCheckName": str,
    },
)
_OptionalGetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef = TypedDict(
    "_OptionalGetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef(
    _RequiredGetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef,
    _OptionalGetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef,
):
    pass

_RequiredGetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef = TypedDict(
    "_RequiredGetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef",
    {
        "RecoveryGroupName": str,
    },
)
_OptionalGetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef = TypedDict(
    "_OptionalGetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef(
    _RequiredGetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef,
    _OptionalGetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef,
):
    pass

ListCellsRequestListCellsPaginateTypeDef = TypedDict(
    "ListCellsRequestListCellsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef = TypedDict(
    "ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListReadinessChecksRequestListReadinessChecksPaginateTypeDef = TypedDict(
    "ListReadinessChecksRequestListReadinessChecksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef = TypedDict(
    "ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResourceSetsRequestListResourceSetsPaginateTypeDef = TypedDict(
    "ListResourceSetsRequestListResourceSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "ListRulesRequestListRulesPaginateTypeDef",
    {
        "ResourceType": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetCellReadinessSummaryResponseTypeDef = TypedDict(
    "GetCellReadinessSummaryResponseTypeDef",
    {
        "NextToken": str,
        "Readiness": ReadinessType,
        "ReadinessChecks": List[ReadinessCheckSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecoveryGroupReadinessSummaryResponseTypeDef = TypedDict(
    "GetRecoveryGroupReadinessSummaryResponseTypeDef",
    {
        "NextToken": str,
        "Readiness": ReadinessType,
        "ReadinessChecks": List[ReadinessCheckSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleResultTypeDef = TypedDict(
    "RuleResultTypeDef",
    {
        "LastCheckedTimestamp": datetime,
        "Messages": List[MessageTypeDef],
        "Readiness": ReadinessType,
        "RuleId": str,
    },
)

GetReadinessCheckStatusResponseTypeDef = TypedDict(
    "GetReadinessCheckStatusResponseTypeDef",
    {
        "Messages": List[MessageTypeDef],
        "NextToken": str,
        "Readiness": ReadinessType,
        "Resources": List[ResourceResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReadinessChecksResponseTypeDef = TypedDict(
    "ListReadinessChecksResponseTypeDef",
    {
        "NextToken": str,
        "ReadinessChecks": List[ReadinessCheckOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecoveryGroupsResponseTypeDef = TypedDict(
    "ListRecoveryGroupsResponseTypeDef",
    {
        "NextToken": str,
        "RecoveryGroups": List[RecoveryGroupOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef",
    {
        "NextToken": str,
        "Rules": List[ListRulesOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TargetResourceTypeDef = TypedDict(
    "TargetResourceTypeDef",
    {
        "NLBResource": NLBResourceTypeDef,
        "R53Resource": R53ResourceRecordTypeDef,
    },
    total=False,
)

GetReadinessCheckResourceStatusResponseTypeDef = TypedDict(
    "GetReadinessCheckResourceStatusResponseTypeDef",
    {
        "NextToken": str,
        "Readiness": ReadinessType,
        "Rules": List[RuleResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DNSTargetResourceTypeDef = TypedDict(
    "DNSTargetResourceTypeDef",
    {
        "DomainName": str,
        "HostedZoneArn": str,
        "RecordSetId": str,
        "RecordType": str,
        "TargetResource": TargetResourceTypeDef,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "ComponentId": str,
        "DnsTargetResource": DNSTargetResourceTypeDef,
        "ReadinessScopes": Sequence[str],
        "ResourceArn": str,
    },
    total=False,
)

_RequiredCreateResourceSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResourceSetRequestRequestTypeDef",
    {
        "ResourceSetName": str,
        "ResourceSetType": str,
        "Resources": Sequence[ResourceTypeDef],
    },
)
_OptionalCreateResourceSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResourceSetRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateResourceSetRequestRequestTypeDef(
    _RequiredCreateResourceSetRequestRequestTypeDef, _OptionalCreateResourceSetRequestRequestTypeDef
):
    pass

CreateResourceSetResponseTypeDef = TypedDict(
    "CreateResourceSetResponseTypeDef",
    {
        "ResourceSetArn": str,
        "ResourceSetName": str,
        "ResourceSetType": str,
        "Resources": List[ResourceTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceSetResponseTypeDef = TypedDict(
    "GetResourceSetResponseTypeDef",
    {
        "ResourceSetArn": str,
        "ResourceSetName": str,
        "ResourceSetType": str,
        "Resources": List[ResourceTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredResourceSetOutputTypeDef = TypedDict(
    "_RequiredResourceSetOutputTypeDef",
    {
        "ResourceSetArn": str,
        "ResourceSetName": str,
        "ResourceSetType": str,
        "Resources": List[ResourceTypeDef],
    },
)
_OptionalResourceSetOutputTypeDef = TypedDict(
    "_OptionalResourceSetOutputTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class ResourceSetOutputTypeDef(
    _RequiredResourceSetOutputTypeDef, _OptionalResourceSetOutputTypeDef
):
    pass

UpdateResourceSetRequestRequestTypeDef = TypedDict(
    "UpdateResourceSetRequestRequestTypeDef",
    {
        "ResourceSetName": str,
        "ResourceSetType": str,
        "Resources": Sequence[ResourceTypeDef],
    },
)

UpdateResourceSetResponseTypeDef = TypedDict(
    "UpdateResourceSetResponseTypeDef",
    {
        "ResourceSetArn": str,
        "ResourceSetName": str,
        "ResourceSetType": str,
        "Resources": List[ResourceTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourceSetsResponseTypeDef = TypedDict(
    "ListResourceSetsResponseTypeDef",
    {
        "NextToken": str,
        "ResourceSets": List[ResourceSetOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
