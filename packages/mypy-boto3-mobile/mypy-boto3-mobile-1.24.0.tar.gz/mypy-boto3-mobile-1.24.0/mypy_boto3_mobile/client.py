"""
Type annotations for mobile service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mobile.client import MobileClient

    session = Session()
    client: MobileClient = session.client("mobile")
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Type, Union, overload

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .literals import PlatformType
from .paginator import ListBundlesPaginator, ListProjectsPaginator
from .type_defs import (
    CreateProjectResultTypeDef,
    DeleteProjectResultTypeDef,
    DescribeBundleResultTypeDef,
    DescribeProjectResultTypeDef,
    ExportBundleResultTypeDef,
    ExportProjectResultTypeDef,
    ListBundlesResultTypeDef,
    ListProjectsResultTypeDef,
    UpdateProjectResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MobileClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccountActionRequiredException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class MobileClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MobileClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#can_paginate)
        """

    def create_project(
        self,
        *,
        name: str = ...,
        region: str = ...,
        contents: Union[str, bytes, IO[Any], StreamingBody] = ...,
        snapshotId: str = ...
    ) -> CreateProjectResultTypeDef:
        """
        Creates an AWS Mobile Hub project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.create_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#create_project)
        """

    def delete_project(self, *, projectId: str) -> DeleteProjectResultTypeDef:
        """
        Delets a project in AWS Mobile Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.delete_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#delete_project)
        """

    def describe_bundle(self, *, bundleId: str) -> DescribeBundleResultTypeDef:
        """
        Get the bundle details for the requested bundle id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.describe_bundle)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#describe_bundle)
        """

    def describe_project(
        self, *, projectId: str, syncFromResources: bool = ...
    ) -> DescribeProjectResultTypeDef:
        """
        Gets details about a project in AWS Mobile Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.describe_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#describe_project)
        """

    def export_bundle(
        self, *, bundleId: str, projectId: str = ..., platform: PlatformType = ...
    ) -> ExportBundleResultTypeDef:
        """
        Generates customized software development kit (SDK) and or tool packages used to
        integrate mobile web or mobile app clients with backend AWS resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.export_bundle)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#export_bundle)
        """

    def export_project(self, *, projectId: str) -> ExportProjectResultTypeDef:
        """
        Exports project configuration to a snapshot which can be downloaded and shared.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.export_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#export_project)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#generate_presigned_url)
        """

    def list_bundles(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListBundlesResultTypeDef:
        """
        List all available bundles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.list_bundles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#list_bundles)
        """

    def list_projects(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListProjectsResultTypeDef:
        """
        Lists projects in AWS Mobile Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.list_projects)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#list_projects)
        """

    def update_project(
        self, *, projectId: str, contents: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> UpdateProjectResultTypeDef:
        """
        Update an existing project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.update_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#update_project)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_bundles"]) -> ListBundlesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/client/#get_paginator)
        """
