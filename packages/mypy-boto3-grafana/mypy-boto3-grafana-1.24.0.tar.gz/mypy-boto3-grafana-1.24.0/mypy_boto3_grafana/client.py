"""
Type annotations for grafana service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_grafana.client import ManagedGrafanaClient

    session = Session()
    client: ManagedGrafanaClient = session.client("grafana")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AccountAccessTypeType,
    AuthenticationProviderTypesType,
    DataSourceTypeType,
    LicenseTypeType,
    PermissionTypeType,
    UserTypeType,
)
from .paginator import ListPermissionsPaginator, ListWorkspacesPaginator
from .type_defs import (
    AssociateLicenseResponseTypeDef,
    CreateWorkspaceApiKeyResponseTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteWorkspaceApiKeyResponseTypeDef,
    DeleteWorkspaceResponseTypeDef,
    DescribeWorkspaceAuthenticationResponseTypeDef,
    DescribeWorkspaceResponseTypeDef,
    DisassociateLicenseResponseTypeDef,
    ListPermissionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesResponseTypeDef,
    SamlConfigurationTypeDef,
    UpdateInstructionTypeDef,
    UpdatePermissionsResponseTypeDef,
    UpdateWorkspaceAuthenticationResponseTypeDef,
    UpdateWorkspaceResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ManagedGrafanaClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ManagedGrafanaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedGrafanaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#exceptions)
        """

    def associate_license(
        self, *, licenseType: LicenseTypeType, workspaceId: str
    ) -> AssociateLicenseResponseTypeDef:
        """
        Assigns a Grafana Enterprise license to a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.associate_license)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#associate_license)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#can_paginate)
        """

    def create_workspace(
        self,
        *,
        accountAccessType: AccountAccessTypeType,
        authenticationProviders: Sequence[AuthenticationProviderTypesType],
        permissionType: PermissionTypeType,
        clientToken: str = ...,
        organizationRoleName: str = ...,
        stackSetName: str = ...,
        tags: Mapping[str, str] = ...,
        workspaceDataSources: Sequence[DataSourceTypeType] = ...,
        workspaceDescription: str = ...,
        workspaceName: str = ...,
        workspaceNotificationDestinations: Sequence[Literal["SNS"]] = ...,
        workspaceOrganizationalUnits: Sequence[str] = ...,
        workspaceRoleArn: str = ...
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a *workspace*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.create_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#create_workspace)
        """

    def create_workspace_api_key(
        self, *, keyName: str, keyRole: str, secondsToLive: int, workspaceId: str
    ) -> CreateWorkspaceApiKeyResponseTypeDef:
        """
        Creates an API key for the workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.create_workspace_api_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#create_workspace_api_key)
        """

    def delete_workspace(self, *, workspaceId: str) -> DeleteWorkspaceResponseTypeDef:
        """
        Deletes an Amazon Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.delete_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#delete_workspace)
        """

    def delete_workspace_api_key(
        self, *, keyName: str, workspaceId: str
    ) -> DeleteWorkspaceApiKeyResponseTypeDef:
        """
        Deletes an API key for a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.delete_workspace_api_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#delete_workspace_api_key)
        """

    def describe_workspace(self, *, workspaceId: str) -> DescribeWorkspaceResponseTypeDef:
        """
        Displays information about one Amazon Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.describe_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#describe_workspace)
        """

    def describe_workspace_authentication(
        self, *, workspaceId: str
    ) -> DescribeWorkspaceAuthenticationResponseTypeDef:
        """
        Displays information about the authentication methods used in one Amazon Managed
        Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.describe_workspace_authentication)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#describe_workspace_authentication)
        """

    def disassociate_license(
        self, *, licenseType: LicenseTypeType, workspaceId: str
    ) -> DisassociateLicenseResponseTypeDef:
        """
        Removes the Grafana Enterprise license from a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.disassociate_license)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#disassociate_license)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#generate_presigned_url)
        """

    def list_permissions(
        self,
        *,
        workspaceId: str,
        groupId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        userId: str = ...,
        userType: UserTypeType = ...
    ) -> ListPermissionsResponseTypeDef:
        """
        Lists the users and groups who have the Grafana `Admin` and `Editor` roles in
        this workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.list_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#list_permissions)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        The `ListTagsForResource` operation returns the tags that are associated with
        the Amazon Managed Service for Grafana resource specified by the `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#list_tags_for_resource)
        """

    def list_workspaces(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkspacesResponseTypeDef:
        """
        Returns a list of Amazon Managed Grafana workspaces in the account, with some
        information about each workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.list_workspaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#list_workspaces)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        The `TagResource` operation associates tags with an Amazon Managed Grafana
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        The `UntagResource` operation removes the association of the tag with the Amazon
        Managed Grafana resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#untag_resource)
        """

    def update_permissions(
        self, *, updateInstructionBatch: Sequence[UpdateInstructionTypeDef], workspaceId: str
    ) -> UpdatePermissionsResponseTypeDef:
        """
        Updates which users in a workspace have the Grafana `Admin` or `Editor` roles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.update_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#update_permissions)
        """

    def update_workspace(
        self,
        *,
        workspaceId: str,
        accountAccessType: AccountAccessTypeType = ...,
        organizationRoleName: str = ...,
        permissionType: PermissionTypeType = ...,
        stackSetName: str = ...,
        workspaceDataSources: Sequence[DataSourceTypeType] = ...,
        workspaceDescription: str = ...,
        workspaceName: str = ...,
        workspaceNotificationDestinations: Sequence[Literal["SNS"]] = ...,
        workspaceOrganizationalUnits: Sequence[str] = ...,
        workspaceRoleArn: str = ...
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Modifies an existing Amazon Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.update_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#update_workspace)
        """

    def update_workspace_authentication(
        self,
        *,
        authenticationProviders: Sequence[AuthenticationProviderTypesType],
        workspaceId: str,
        samlConfiguration: SamlConfigurationTypeDef = ...
    ) -> UpdateWorkspaceAuthenticationResponseTypeDef:
        """
        Use this operation to define the identity provider (IdP) that this workspace
        authenticates users from, using SAML.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.update_workspace_authentication)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#update_workspace_authentication)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permissions"]
    ) -> ListPermissionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workspaces"]) -> ListWorkspacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/client/#get_paginator)
        """
