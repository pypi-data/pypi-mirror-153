"""
Type annotations for resourcegroupstaggingapi service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/type_defs/)

Usage::

    ```python
    from mypy_boto3_resourcegroupstaggingapi.type_defs import ComplianceDetailsTypeDef

    data: ComplianceDetailsTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import ErrorCodeType, GroupByAttributeType, TargetIdTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ComplianceDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "FailureInfoTypeDef",
    "PaginatorConfigTypeDef",
    "GetComplianceSummaryInputRequestTypeDef",
    "SummaryTypeDef",
    "TagFilterTypeDef",
    "GetTagKeysInputRequestTypeDef",
    "GetTagValuesInputRequestTypeDef",
    "TagTypeDef",
    "StartReportCreationInputRequestTypeDef",
    "TagResourcesInputRequestTypeDef",
    "UntagResourcesInputRequestTypeDef",
    "DescribeReportCreationOutputTypeDef",
    "GetTagKeysOutputTypeDef",
    "GetTagValuesOutputTypeDef",
    "TagResourcesOutputTypeDef",
    "UntagResourcesOutputTypeDef",
    "GetComplianceSummaryInputGetComplianceSummaryPaginateTypeDef",
    "GetTagKeysInputGetTagKeysPaginateTypeDef",
    "GetTagValuesInputGetTagValuesPaginateTypeDef",
    "GetComplianceSummaryOutputTypeDef",
    "GetResourcesInputGetResourcesPaginateTypeDef",
    "GetResourcesInputRequestTypeDef",
    "ResourceTagMappingTypeDef",
    "GetResourcesOutputTypeDef",
)

ComplianceDetailsTypeDef = TypedDict(
    "ComplianceDetailsTypeDef",
    {
        "NoncompliantKeys": List[str],
        "KeysWithNoncompliantValues": List[str],
        "ComplianceStatus": bool,
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

FailureInfoTypeDef = TypedDict(
    "FailureInfoTypeDef",
    {
        "StatusCode": int,
        "ErrorCode": ErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
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

GetComplianceSummaryInputRequestTypeDef = TypedDict(
    "GetComplianceSummaryInputRequestTypeDef",
    {
        "TargetIdFilters": Sequence[str],
        "RegionFilters": Sequence[str],
        "ResourceTypeFilters": Sequence[str],
        "TagKeyFilters": Sequence[str],
        "GroupBy": Sequence[GroupByAttributeType],
        "MaxResults": int,
        "PaginationToken": str,
    },
    total=False,
)

SummaryTypeDef = TypedDict(
    "SummaryTypeDef",
    {
        "LastUpdated": str,
        "TargetId": str,
        "TargetIdType": TargetIdTypeType,
        "Region": str,
        "ResourceType": str,
        "NonCompliantResources": int,
    },
    total=False,
)

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
    total=False,
)

GetTagKeysInputRequestTypeDef = TypedDict(
    "GetTagKeysInputRequestTypeDef",
    {
        "PaginationToken": str,
    },
    total=False,
)

_RequiredGetTagValuesInputRequestTypeDef = TypedDict(
    "_RequiredGetTagValuesInputRequestTypeDef",
    {
        "Key": str,
    },
)
_OptionalGetTagValuesInputRequestTypeDef = TypedDict(
    "_OptionalGetTagValuesInputRequestTypeDef",
    {
        "PaginationToken": str,
    },
    total=False,
)

class GetTagValuesInputRequestTypeDef(
    _RequiredGetTagValuesInputRequestTypeDef, _OptionalGetTagValuesInputRequestTypeDef
):
    pass

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

StartReportCreationInputRequestTypeDef = TypedDict(
    "StartReportCreationInputRequestTypeDef",
    {
        "S3Bucket": str,
    },
)

TagResourcesInputRequestTypeDef = TypedDict(
    "TagResourcesInputRequestTypeDef",
    {
        "ResourceARNList": Sequence[str],
        "Tags": Mapping[str, str],
    },
)

UntagResourcesInputRequestTypeDef = TypedDict(
    "UntagResourcesInputRequestTypeDef",
    {
        "ResourceARNList": Sequence[str],
        "TagKeys": Sequence[str],
    },
)

DescribeReportCreationOutputTypeDef = TypedDict(
    "DescribeReportCreationOutputTypeDef",
    {
        "Status": str,
        "S3Location": str,
        "ErrorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTagKeysOutputTypeDef = TypedDict(
    "GetTagKeysOutputTypeDef",
    {
        "PaginationToken": str,
        "TagKeys": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTagValuesOutputTypeDef = TypedDict(
    "GetTagValuesOutputTypeDef",
    {
        "PaginationToken": str,
        "TagValues": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourcesOutputTypeDef = TypedDict(
    "TagResourcesOutputTypeDef",
    {
        "FailedResourcesMap": Dict[str, FailureInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourcesOutputTypeDef = TypedDict(
    "UntagResourcesOutputTypeDef",
    {
        "FailedResourcesMap": Dict[str, FailureInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComplianceSummaryInputGetComplianceSummaryPaginateTypeDef = TypedDict(
    "GetComplianceSummaryInputGetComplianceSummaryPaginateTypeDef",
    {
        "TargetIdFilters": Sequence[str],
        "RegionFilters": Sequence[str],
        "ResourceTypeFilters": Sequence[str],
        "TagKeyFilters": Sequence[str],
        "GroupBy": Sequence[GroupByAttributeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetTagKeysInputGetTagKeysPaginateTypeDef = TypedDict(
    "GetTagKeysInputGetTagKeysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetTagValuesInputGetTagValuesPaginateTypeDef = TypedDict(
    "_RequiredGetTagValuesInputGetTagValuesPaginateTypeDef",
    {
        "Key": str,
    },
)
_OptionalGetTagValuesInputGetTagValuesPaginateTypeDef = TypedDict(
    "_OptionalGetTagValuesInputGetTagValuesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetTagValuesInputGetTagValuesPaginateTypeDef(
    _RequiredGetTagValuesInputGetTagValuesPaginateTypeDef,
    _OptionalGetTagValuesInputGetTagValuesPaginateTypeDef,
):
    pass

GetComplianceSummaryOutputTypeDef = TypedDict(
    "GetComplianceSummaryOutputTypeDef",
    {
        "SummaryList": List[SummaryTypeDef],
        "PaginationToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcesInputGetResourcesPaginateTypeDef = TypedDict(
    "GetResourcesInputGetResourcesPaginateTypeDef",
    {
        "TagFilters": Sequence[TagFilterTypeDef],
        "TagsPerPage": int,
        "ResourceTypeFilters": Sequence[str],
        "IncludeComplianceDetails": bool,
        "ExcludeCompliantResources": bool,
        "ResourceARNList": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetResourcesInputRequestTypeDef = TypedDict(
    "GetResourcesInputRequestTypeDef",
    {
        "PaginationToken": str,
        "TagFilters": Sequence[TagFilterTypeDef],
        "ResourcesPerPage": int,
        "TagsPerPage": int,
        "ResourceTypeFilters": Sequence[str],
        "IncludeComplianceDetails": bool,
        "ExcludeCompliantResources": bool,
        "ResourceARNList": Sequence[str],
    },
    total=False,
)

ResourceTagMappingTypeDef = TypedDict(
    "ResourceTagMappingTypeDef",
    {
        "ResourceARN": str,
        "Tags": List[TagTypeDef],
        "ComplianceDetails": ComplianceDetailsTypeDef,
    },
    total=False,
)

GetResourcesOutputTypeDef = TypedDict(
    "GetResourcesOutputTypeDef",
    {
        "PaginationToken": str,
        "ResourceTagMappingList": List[ResourceTagMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
