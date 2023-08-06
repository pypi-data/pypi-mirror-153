"""
Type annotations for migration-hub-refactor-spaces service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient

    session = Session()
    client: MigrationHubRefactorSpacesClient = session.client("migration-hub-refactor-spaces")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import RouteTypeType, ServiceEndpointTypeType
from .paginator import (
    ListApplicationsPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentVpcsPaginator,
    ListRoutesPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    ApiGatewayProxyInputTypeDef,
    CreateApplicationResponseTypeDef,
    CreateEnvironmentResponseTypeDef,
    CreateRouteResponseTypeDef,
    CreateServiceResponseTypeDef,
    DeleteApplicationResponseTypeDef,
    DeleteEnvironmentResponseTypeDef,
    DeleteRouteResponseTypeDef,
    DeleteServiceResponseTypeDef,
    GetApplicationResponseTypeDef,
    GetEnvironmentResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetRouteResponseTypeDef,
    GetServiceResponseTypeDef,
    LambdaEndpointInputTypeDef,
    ListApplicationsResponseTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListEnvironmentVpcsResponseTypeDef,
    ListRoutesResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    UriPathRouteInputTypeDef,
    UrlEndpointInputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MigrationHubRefactorSpacesClient",)


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
    InvalidResourcePolicyException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MigrationHubRefactorSpacesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubRefactorSpacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#can_paginate)
        """

    def create_application(
        self,
        *,
        EnvironmentIdentifier: str,
        Name: str,
        ProxyType: Literal["API_GATEWAY"],
        VpcId: str,
        ApiGatewayProxy: ApiGatewayProxyInputTypeDef = ...,
        ClientToken: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#create_application)
        """

    def create_environment(
        self,
        *,
        Name: str,
        NetworkFabricType: Literal["TRANSIT_GATEWAY"],
        ClientToken: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#create_environment)
        """

    def create_route(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        RouteType: RouteTypeType,
        ServiceIdentifier: str,
        ClientToken: str = ...,
        Tags: Mapping[str, str] = ...,
        UriPathRoute: UriPathRouteInputTypeDef = ...
    ) -> CreateRouteResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#create_route)
        """

    def create_service(
        self,
        *,
        ApplicationIdentifier: str,
        EndpointType: ServiceEndpointTypeType,
        EnvironmentIdentifier: str,
        Name: str,
        ClientToken: str = ...,
        Description: str = ...,
        LambdaEndpoint: LambdaEndpointInputTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        UrlEndpoint: UrlEndpointInputTypeDef = ...,
        VpcId: str = ...
    ) -> CreateServiceResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#create_service)
        """

    def delete_application(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str
    ) -> DeleteApplicationResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#delete_application)
        """

    def delete_environment(self, *, EnvironmentIdentifier: str) -> DeleteEnvironmentResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#delete_environment)
        """

    def delete_resource_policy(self, *, Identifier: str) -> Dict[str, Any]:
        """
        Deletes the resource policy set for the environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#delete_resource_policy)
        """

    def delete_route(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, RouteIdentifier: str
    ) -> DeleteRouteResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#delete_route)
        """

    def delete_service(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, ServiceIdentifier: str
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#delete_service)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#generate_presigned_url)
        """

    def get_application(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str
    ) -> GetApplicationResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_application)
        """

    def get_environment(self, *, EnvironmentIdentifier: str) -> GetEnvironmentResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_environment)
        """

    def get_resource_policy(self, *, Identifier: str) -> GetResourcePolicyResponseTypeDef:
        """
        Gets the resource-based permission policy that is set for the given environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_resource_policy)
        """

    def get_route(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, RouteIdentifier: str
    ) -> GetRouteResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_route)
        """

    def get_service(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, ServiceIdentifier: str
    ) -> GetServiceResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_service)
        """

    def list_applications(
        self, *, EnvironmentIdentifier: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists all the Amazon Web Services Migration Hub Refactor Spaces applications
        within an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#list_applications)
        """

    def list_environment_vpcs(
        self, *, EnvironmentIdentifier: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEnvironmentVpcsResponseTypeDef:
        """
        Lists all Amazon Web Services Migration Hub Refactor Spaces service virtual
        private clouds (VPCs) that are part of the environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_environment_vpcs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#list_environment_vpcs)
        """

    def list_environments(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEnvironmentsResponseTypeDef:
        """
        Lists Amazon Web Services Migration Hub Refactor Spaces environments owned by a
        caller account or shared with the caller account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#list_environments)
        """

    def list_routes(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListRoutesResponseTypeDef:
        """
        Lists all the Amazon Web Services Migration Hub Refactor Spaces routes within an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_routes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#list_routes)
        """

    def list_services(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListServicesResponseTypeDef:
        """
        Lists all the Amazon Web Services Migration Hub Refactor Spaces services within
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_services)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#list_services)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#list_tags_for_resource)
        """

    def put_resource_policy(self, *, Policy: str, ResourceArn: str) -> Dict[str, Any]:
        """
        Attaches a resource-based permission policy to the Amazon Web Services Migration
        Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.put_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#put_resource_policy)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Removes the tags of a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_vpcs"]
    ) -> ListEnvironmentVpcsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_routes"]) -> ListRoutesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/client/#get_paginator)
        """
