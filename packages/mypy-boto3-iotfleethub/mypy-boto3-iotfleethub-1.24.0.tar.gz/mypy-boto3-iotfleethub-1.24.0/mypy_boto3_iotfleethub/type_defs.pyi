"""
Type annotations for iotfleethub service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotfleethub/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotfleethub.type_defs import ApplicationSummaryTypeDef

    data: ApplicationSummaryTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import ApplicationStateType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DescribeApplicationRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "DescribeApplicationResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
)

_RequiredApplicationSummaryTypeDef = TypedDict(
    "_RequiredApplicationSummaryTypeDef",
    {
        "applicationId": str,
        "applicationName": str,
        "applicationUrl": str,
    },
)
_OptionalApplicationSummaryTypeDef = TypedDict(
    "_OptionalApplicationSummaryTypeDef",
    {
        "applicationDescription": str,
        "applicationCreationDate": int,
        "applicationLastUpdateDate": int,
        "applicationState": ApplicationStateType,
    },
    total=False,
)

class ApplicationSummaryTypeDef(
    _RequiredApplicationSummaryTypeDef, _OptionalApplicationSummaryTypeDef
):
    pass

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "applicationName": str,
        "roleArn": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "applicationDescription": str,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
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

_RequiredDeleteApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalDeleteApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteApplicationRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class DeleteApplicationRequestRequestTypeDef(
    _RequiredDeleteApplicationRequestRequestTypeDef, _OptionalDeleteApplicationRequestRequestTypeDef
):
    pass

DescribeApplicationRequestRequestTypeDef = TypedDict(
    "DescribeApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
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

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
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

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "applicationName": str,
        "applicationDescription": str,
        "clientToken": str,
    },
    total=False,
)

class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "applicationId": str,
        "applicationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef",
    {
        "applicationId": str,
        "applicationArn": str,
        "applicationName": str,
        "applicationDescription": str,
        "applicationUrl": str,
        "applicationState": ApplicationStateType,
        "applicationCreationDate": int,
        "applicationLastUpdateDate": int,
        "roleArn": str,
        "ssoClientId": str,
        "errorMessage": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "applicationSummaries": List[ApplicationSummaryTypeDef],
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

ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)
