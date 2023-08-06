"""
Type annotations for mobile service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/type_defs/)

Usage::

    ```python
    from mypy_boto3_mobile.type_defs import BundleDetailsTypeDef

    data: BundleDetailsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Union

from botocore.response import StreamingBody

from .literals import PlatformType, ProjectStateType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BundleDetailsTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "ResourceTypeDef",
    "DescribeBundleRequestRequestTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "ExportBundleRequestRequestTypeDef",
    "ExportProjectRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListBundlesRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "DescribeBundleResultTypeDef",
    "ExportBundleResultTypeDef",
    "ExportProjectResultTypeDef",
    "ListBundlesResultTypeDef",
    "DeleteProjectResultTypeDef",
    "ProjectDetailsTypeDef",
    "ListBundlesRequestListBundlesPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsResultTypeDef",
    "CreateProjectResultTypeDef",
    "DescribeProjectResultTypeDef",
    "UpdateProjectResultTypeDef",
)

BundleDetailsTypeDef = TypedDict(
    "BundleDetailsTypeDef",
    {
        "bundleId": str,
        "title": str,
        "version": str,
        "description": str,
        "iconUrl": str,
        "availablePlatforms": List[PlatformType],
    },
    total=False,
)

CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "name": str,
        "region": str,
        "contents": Union[str, bytes, IO[Any], StreamingBody],
        "snapshotId": str,
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

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "type": str,
        "name": str,
        "arn": str,
        "feature": str,
        "attributes": Dict[str, str],
    },
    total=False,
)

DescribeBundleRequestRequestTypeDef = TypedDict(
    "DescribeBundleRequestRequestTypeDef",
    {
        "bundleId": str,
    },
)

_RequiredDescribeProjectRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalDescribeProjectRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeProjectRequestRequestTypeDef",
    {
        "syncFromResources": bool,
    },
    total=False,
)

class DescribeProjectRequestRequestTypeDef(
    _RequiredDescribeProjectRequestRequestTypeDef, _OptionalDescribeProjectRequestRequestTypeDef
):
    pass

_RequiredExportBundleRequestRequestTypeDef = TypedDict(
    "_RequiredExportBundleRequestRequestTypeDef",
    {
        "bundleId": str,
    },
)
_OptionalExportBundleRequestRequestTypeDef = TypedDict(
    "_OptionalExportBundleRequestRequestTypeDef",
    {
        "projectId": str,
        "platform": PlatformType,
    },
    total=False,
)

class ExportBundleRequestRequestTypeDef(
    _RequiredExportBundleRequestRequestTypeDef, _OptionalExportBundleRequestRequestTypeDef
):
    pass

ExportProjectRequestRequestTypeDef = TypedDict(
    "ExportProjectRequestRequestTypeDef",
    {
        "projectId": str,
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

ListBundlesRequestRequestTypeDef = TypedDict(
    "ListBundlesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "name": str,
        "projectId": str,
    },
    total=False,
)

_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "contents": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)

class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass

DescribeBundleResultTypeDef = TypedDict(
    "DescribeBundleResultTypeDef",
    {
        "details": BundleDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportBundleResultTypeDef = TypedDict(
    "ExportBundleResultTypeDef",
    {
        "downloadUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportProjectResultTypeDef = TypedDict(
    "ExportProjectResultTypeDef",
    {
        "downloadUrl": str,
        "shareUrl": str,
        "snapshotId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBundlesResultTypeDef = TypedDict(
    "ListBundlesResultTypeDef",
    {
        "bundleList": List[BundleDetailsTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectResultTypeDef = TypedDict(
    "DeleteProjectResultTypeDef",
    {
        "deletedResources": List[ResourceTypeDef],
        "orphanedResources": List[ResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProjectDetailsTypeDef = TypedDict(
    "ProjectDetailsTypeDef",
    {
        "name": str,
        "projectId": str,
        "region": str,
        "state": ProjectStateType,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "consoleUrl": str,
        "resources": List[ResourceTypeDef],
    },
    total=False,
)

ListBundlesRequestListBundlesPaginateTypeDef = TypedDict(
    "ListBundlesRequestListBundlesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProjectsResultTypeDef = TypedDict(
    "ListProjectsResultTypeDef",
    {
        "projects": List[ProjectSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResultTypeDef = TypedDict(
    "CreateProjectResultTypeDef",
    {
        "details": ProjectDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProjectResultTypeDef = TypedDict(
    "DescribeProjectResultTypeDef",
    {
        "details": ProjectDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProjectResultTypeDef = TypedDict(
    "UpdateProjectResultTypeDef",
    {
        "details": ProjectDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
