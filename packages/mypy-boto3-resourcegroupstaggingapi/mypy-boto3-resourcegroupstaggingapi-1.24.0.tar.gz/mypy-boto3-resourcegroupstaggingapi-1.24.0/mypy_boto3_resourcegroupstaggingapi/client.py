"""
Type annotations for resourcegroupstaggingapi service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient

    session = Session()
    client: ResourceGroupsTaggingAPIClient = session.client("resourcegroupstaggingapi")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import GroupByAttributeType
from .paginator import (
    GetComplianceSummaryPaginator,
    GetResourcesPaginator,
    GetTagKeysPaginator,
    GetTagValuesPaginator,
)
from .type_defs import (
    DescribeReportCreationOutputTypeDef,
    GetComplianceSummaryOutputTypeDef,
    GetResourcesOutputTypeDef,
    GetTagKeysOutputTypeDef,
    GetTagValuesOutputTypeDef,
    TagFilterTypeDef,
    TagResourcesOutputTypeDef,
    UntagResourcesOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ResourceGroupsTaggingAPIClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConstraintViolationException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    PaginationTokenExpiredException: Type[BotocoreClientError]
    ThrottledException: Type[BotocoreClientError]


class ResourceGroupsTaggingAPIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResourceGroupsTaggingAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#can_paginate)
        """

    def describe_report_creation(self) -> DescribeReportCreationOutputTypeDef:
        """
        Describes the status of the `StartReportCreation` operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.describe_report_creation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#describe_report_creation)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#generate_presigned_url)
        """

    def get_compliance_summary(
        self,
        *,
        TargetIdFilters: Sequence[str] = ...,
        RegionFilters: Sequence[str] = ...,
        ResourceTypeFilters: Sequence[str] = ...,
        TagKeyFilters: Sequence[str] = ...,
        GroupBy: Sequence[GroupByAttributeType] = ...,
        MaxResults: int = ...,
        PaginationToken: str = ...
    ) -> GetComplianceSummaryOutputTypeDef:
        """
        Returns a table that shows counts of resources that are noncompliant with their
        tag policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_compliance_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_compliance_summary)
        """

    def get_resources(
        self,
        *,
        PaginationToken: str = ...,
        TagFilters: Sequence[TagFilterTypeDef] = ...,
        ResourcesPerPage: int = ...,
        TagsPerPage: int = ...,
        ResourceTypeFilters: Sequence[str] = ...,
        IncludeComplianceDetails: bool = ...,
        ExcludeCompliantResources: bool = ...,
        ResourceARNList: Sequence[str] = ...
    ) -> GetResourcesOutputTypeDef:
        """
        Returns all the tagged or previously tagged resources that are located in the
        specified Amazon Web Services Region for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_resources)
        """

    def get_tag_keys(self, *, PaginationToken: str = ...) -> GetTagKeysOutputTypeDef:
        """
        Returns all tag keys currently in use in the specified Amazon Web Services
        Region for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_tag_keys)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_tag_keys)
        """

    def get_tag_values(self, *, Key: str, PaginationToken: str = ...) -> GetTagValuesOutputTypeDef:
        """
        Returns all tag values for the specified key that are used in the specified
        Amazon Web Services Region for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_tag_values)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_tag_values)
        """

    def start_report_creation(self, *, S3Bucket: str) -> Dict[str, Any]:
        """
        Generates a report that lists all tagged resources in the accounts across your
        organization and tells whether each resource is compliant with the effective tag
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.start_report_creation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#start_report_creation)
        """

    def tag_resources(
        self, *, ResourceARNList: Sequence[str], Tags: Mapping[str, str]
    ) -> TagResourcesOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.tag_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#tag_resources)
        """

    def untag_resources(
        self, *, ResourceARNList: Sequence[str], TagKeys: Sequence[str]
    ) -> UntagResourcesOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.untag_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#untag_resources)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_compliance_summary"]
    ) -> GetComplianceSummaryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_resources"]) -> GetResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tag_keys"]) -> GetTagKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tag_values"]) -> GetTagValuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """
