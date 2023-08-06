"""
Type annotations for appmesh service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appmesh.client import AppMeshClient

    session = Session()
    client: AppMeshClient = session.client("appmesh")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListGatewayRoutesPaginator,
    ListMeshesPaginator,
    ListRoutesPaginator,
    ListTagsForResourcePaginator,
    ListVirtualGatewaysPaginator,
    ListVirtualNodesPaginator,
    ListVirtualRoutersPaginator,
    ListVirtualServicesPaginator,
)
from .type_defs import (
    CreateGatewayRouteOutputTypeDef,
    CreateMeshOutputTypeDef,
    CreateRouteOutputTypeDef,
    CreateVirtualGatewayOutputTypeDef,
    CreateVirtualNodeOutputTypeDef,
    CreateVirtualRouterOutputTypeDef,
    CreateVirtualServiceOutputTypeDef,
    DeleteGatewayRouteOutputTypeDef,
    DeleteMeshOutputTypeDef,
    DeleteRouteOutputTypeDef,
    DeleteVirtualGatewayOutputTypeDef,
    DeleteVirtualNodeOutputTypeDef,
    DeleteVirtualRouterOutputTypeDef,
    DeleteVirtualServiceOutputTypeDef,
    DescribeGatewayRouteOutputTypeDef,
    DescribeMeshOutputTypeDef,
    DescribeRouteOutputTypeDef,
    DescribeVirtualGatewayOutputTypeDef,
    DescribeVirtualNodeOutputTypeDef,
    DescribeVirtualRouterOutputTypeDef,
    DescribeVirtualServiceOutputTypeDef,
    GatewayRouteSpecTypeDef,
    ListGatewayRoutesOutputTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualGatewaysOutputTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesOutputTypeDef,
    MeshSpecTypeDef,
    RouteSpecTypeDef,
    TagRefTypeDef,
    UpdateGatewayRouteOutputTypeDef,
    UpdateMeshOutputTypeDef,
    UpdateRouteOutputTypeDef,
    UpdateVirtualGatewayOutputTypeDef,
    UpdateVirtualNodeOutputTypeDef,
    UpdateVirtualRouterOutputTypeDef,
    UpdateVirtualServiceOutputTypeDef,
    VirtualGatewaySpecTypeDef,
    VirtualNodeSpecTypeDef,
    VirtualRouterSpecTypeDef,
    VirtualServiceSpecTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppMeshClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class AppMeshClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppMeshClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#can_paginate)
        """

    def create_gateway_route(
        self,
        *,
        gatewayRouteName: str,
        meshName: str,
        spec: GatewayRouteSpecTypeDef,
        virtualGatewayName: str,
        clientToken: str = ...,
        meshOwner: str = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateGatewayRouteOutputTypeDef:
        """
        Creates a gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_gateway_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_gateway_route)
        """

    def create_mesh(
        self,
        *,
        meshName: str,
        clientToken: str = ...,
        spec: MeshSpecTypeDef = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateMeshOutputTypeDef:
        """
        Creates a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_mesh)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_mesh)
        """

    def create_route(
        self,
        *,
        meshName: str,
        routeName: str,
        spec: RouteSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = ...,
        meshOwner: str = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateRouteOutputTypeDef:
        """
        Creates a route that is associated with a virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_route)
        """

    def create_virtual_gateway(
        self,
        *,
        meshName: str,
        spec: VirtualGatewaySpecTypeDef,
        virtualGatewayName: str,
        clientToken: str = ...,
        meshOwner: str = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateVirtualGatewayOutputTypeDef:
        """
        Creates a virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_virtual_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_gateway)
        """

    def create_virtual_node(
        self,
        *,
        meshName: str,
        spec: VirtualNodeSpecTypeDef,
        virtualNodeName: str,
        clientToken: str = ...,
        meshOwner: str = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateVirtualNodeOutputTypeDef:
        """
        Creates a virtual node within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_virtual_node)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_node)
        """

    def create_virtual_router(
        self,
        *,
        meshName: str,
        spec: VirtualRouterSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = ...,
        meshOwner: str = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateVirtualRouterOutputTypeDef:
        """
        Creates a virtual router within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_virtual_router)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_router)
        """

    def create_virtual_service(
        self,
        *,
        meshName: str,
        spec: VirtualServiceSpecTypeDef,
        virtualServiceName: str,
        clientToken: str = ...,
        meshOwner: str = ...,
        tags: Sequence[TagRefTypeDef] = ...
    ) -> CreateVirtualServiceOutputTypeDef:
        """
        Creates a virtual service within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.create_virtual_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#create_virtual_service)
        """

    def delete_gateway_route(
        self, *, gatewayRouteName: str, meshName: str, virtualGatewayName: str, meshOwner: str = ...
    ) -> DeleteGatewayRouteOutputTypeDef:
        """
        Deletes an existing gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_gateway_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_gateway_route)
        """

    def delete_mesh(self, *, meshName: str) -> DeleteMeshOutputTypeDef:
        """
        Deletes an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_mesh)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_mesh)
        """

    def delete_route(
        self, *, meshName: str, routeName: str, virtualRouterName: str, meshOwner: str = ...
    ) -> DeleteRouteOutputTypeDef:
        """
        Deletes an existing route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_route)
        """

    def delete_virtual_gateway(
        self, *, meshName: str, virtualGatewayName: str, meshOwner: str = ...
    ) -> DeleteVirtualGatewayOutputTypeDef:
        """
        Deletes an existing virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_virtual_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_gateway)
        """

    def delete_virtual_node(
        self, *, meshName: str, virtualNodeName: str, meshOwner: str = ...
    ) -> DeleteVirtualNodeOutputTypeDef:
        """
        Deletes an existing virtual node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_virtual_node)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_node)
        """

    def delete_virtual_router(
        self, *, meshName: str, virtualRouterName: str, meshOwner: str = ...
    ) -> DeleteVirtualRouterOutputTypeDef:
        """
        Deletes an existing virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_virtual_router)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_router)
        """

    def delete_virtual_service(
        self, *, meshName: str, virtualServiceName: str, meshOwner: str = ...
    ) -> DeleteVirtualServiceOutputTypeDef:
        """
        Deletes an existing virtual service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.delete_virtual_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#delete_virtual_service)
        """

    def describe_gateway_route(
        self, *, gatewayRouteName: str, meshName: str, virtualGatewayName: str, meshOwner: str = ...
    ) -> DescribeGatewayRouteOutputTypeDef:
        """
        Describes an existing gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_gateway_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_gateway_route)
        """

    def describe_mesh(self, *, meshName: str, meshOwner: str = ...) -> DescribeMeshOutputTypeDef:
        """
        Describes an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_mesh)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_mesh)
        """

    def describe_route(
        self, *, meshName: str, routeName: str, virtualRouterName: str, meshOwner: str = ...
    ) -> DescribeRouteOutputTypeDef:
        """
        Describes an existing route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_route)
        """

    def describe_virtual_gateway(
        self, *, meshName: str, virtualGatewayName: str, meshOwner: str = ...
    ) -> DescribeVirtualGatewayOutputTypeDef:
        """
        Describes an existing virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_virtual_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_gateway)
        """

    def describe_virtual_node(
        self, *, meshName: str, virtualNodeName: str, meshOwner: str = ...
    ) -> DescribeVirtualNodeOutputTypeDef:
        """
        Describes an existing virtual node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_virtual_node)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_node)
        """

    def describe_virtual_router(
        self, *, meshName: str, virtualRouterName: str, meshOwner: str = ...
    ) -> DescribeVirtualRouterOutputTypeDef:
        """
        Describes an existing virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_virtual_router)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_router)
        """

    def describe_virtual_service(
        self, *, meshName: str, virtualServiceName: str, meshOwner: str = ...
    ) -> DescribeVirtualServiceOutputTypeDef:
        """
        Describes an existing virtual service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.describe_virtual_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#describe_virtual_service)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#generate_presigned_url)
        """

    def list_gateway_routes(
        self,
        *,
        meshName: str,
        virtualGatewayName: str,
        limit: int = ...,
        meshOwner: str = ...,
        nextToken: str = ...
    ) -> ListGatewayRoutesOutputTypeDef:
        """
        Returns a list of existing gateway routes that are associated to a virtual
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_gateway_routes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_gateway_routes)
        """

    def list_meshes(self, *, limit: int = ..., nextToken: str = ...) -> ListMeshesOutputTypeDef:
        """
        Returns a list of existing service meshes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_meshes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_meshes)
        """

    def list_routes(
        self,
        *,
        meshName: str,
        virtualRouterName: str,
        limit: int = ...,
        meshOwner: str = ...,
        nextToken: str = ...
    ) -> ListRoutesOutputTypeDef:
        """
        Returns a list of existing routes in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_routes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_routes)
        """

    def list_tags_for_resource(
        self, *, resourceArn: str, limit: int = ..., nextToken: str = ...
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List the tags for an App Mesh resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_tags_for_resource)
        """

    def list_virtual_gateways(
        self, *, meshName: str, limit: int = ..., meshOwner: str = ..., nextToken: str = ...
    ) -> ListVirtualGatewaysOutputTypeDef:
        """
        Returns a list of existing virtual gateways in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_virtual_gateways)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_gateways)
        """

    def list_virtual_nodes(
        self, *, meshName: str, limit: int = ..., meshOwner: str = ..., nextToken: str = ...
    ) -> ListVirtualNodesOutputTypeDef:
        """
        Returns a list of existing virtual nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_virtual_nodes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_nodes)
        """

    def list_virtual_routers(
        self, *, meshName: str, limit: int = ..., meshOwner: str = ..., nextToken: str = ...
    ) -> ListVirtualRoutersOutputTypeDef:
        """
        Returns a list of existing virtual routers in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_virtual_routers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_routers)
        """

    def list_virtual_services(
        self, *, meshName: str, limit: int = ..., meshOwner: str = ..., nextToken: str = ...
    ) -> ListVirtualServicesOutputTypeDef:
        """
        Returns a list of existing virtual services in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.list_virtual_services)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#list_virtual_services)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence[TagRefTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#untag_resource)
        """

    def update_gateway_route(
        self,
        *,
        gatewayRouteName: str,
        meshName: str,
        spec: GatewayRouteSpecTypeDef,
        virtualGatewayName: str,
        clientToken: str = ...,
        meshOwner: str = ...
    ) -> UpdateGatewayRouteOutputTypeDef:
        """
        Updates an existing gateway route that is associated to a specified virtual
        gateway in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_gateway_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_gateway_route)
        """

    def update_mesh(
        self, *, meshName: str, clientToken: str = ..., spec: MeshSpecTypeDef = ...
    ) -> UpdateMeshOutputTypeDef:
        """
        Updates an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_mesh)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_mesh)
        """

    def update_route(
        self,
        *,
        meshName: str,
        routeName: str,
        spec: RouteSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = ...,
        meshOwner: str = ...
    ) -> UpdateRouteOutputTypeDef:
        """
        Updates an existing route for a specified service mesh and virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_route)
        """

    def update_virtual_gateway(
        self,
        *,
        meshName: str,
        spec: VirtualGatewaySpecTypeDef,
        virtualGatewayName: str,
        clientToken: str = ...,
        meshOwner: str = ...
    ) -> UpdateVirtualGatewayOutputTypeDef:
        """
        Updates an existing virtual gateway in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_virtual_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_gateway)
        """

    def update_virtual_node(
        self,
        *,
        meshName: str,
        spec: VirtualNodeSpecTypeDef,
        virtualNodeName: str,
        clientToken: str = ...,
        meshOwner: str = ...
    ) -> UpdateVirtualNodeOutputTypeDef:
        """
        Updates an existing virtual node in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_virtual_node)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_node)
        """

    def update_virtual_router(
        self,
        *,
        meshName: str,
        spec: VirtualRouterSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = ...,
        meshOwner: str = ...
    ) -> UpdateVirtualRouterOutputTypeDef:
        """
        Updates an existing virtual router in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_virtual_router)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_router)
        """

    def update_virtual_service(
        self,
        *,
        meshName: str,
        spec: VirtualServiceSpecTypeDef,
        virtualServiceName: str,
        clientToken: str = ...,
        meshOwner: str = ...
    ) -> UpdateVirtualServiceOutputTypeDef:
        """
        Updates an existing virtual service in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.update_virtual_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#update_virtual_service)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_gateway_routes"]
    ) -> ListGatewayRoutesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_meshes"]) -> ListMeshesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_routes"]) -> ListRoutesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_gateways"]
    ) -> ListVirtualGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_nodes"]
    ) -> ListVirtualNodesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_routers"]
    ) -> ListVirtualRoutersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_services"]
    ) -> ListVirtualServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/client/#get_paginator)
        """
