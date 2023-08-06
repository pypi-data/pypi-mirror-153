"""
Type annotations for appmesh service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/type_defs/)

Usage::

    ```python
    from mypy_boto3_appmesh.type_defs import FileAccessLogTypeDef

    data: FileAccessLogTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    DefaultGatewayRouteRewriteType,
    DnsResponseTypeType,
    DurationUnitType,
    EgressFilterTypeType,
    GatewayRouteStatusCodeType,
    GrpcRetryPolicyEventType,
    HttpMethodType,
    HttpSchemeType,
    IpPreferenceType,
    ListenerTlsModeType,
    MeshStatusCodeType,
    PortProtocolType,
    RouteStatusCodeType,
    VirtualGatewayListenerTlsModeType,
    VirtualGatewayPortProtocolType,
    VirtualGatewayStatusCodeType,
    VirtualNodeStatusCodeType,
    VirtualRouterStatusCodeType,
    VirtualServiceStatusCodeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "FileAccessLogTypeDef",
    "AwsCloudMapInstanceAttributeTypeDef",
    "ListenerTlsFileCertificateTypeDef",
    "ListenerTlsSdsCertificateTypeDef",
    "TagRefTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteGatewayRouteInputRequestTypeDef",
    "DeleteMeshInputRequestTypeDef",
    "DeleteRouteInputRequestTypeDef",
    "DeleteVirtualGatewayInputRequestTypeDef",
    "DeleteVirtualNodeInputRequestTypeDef",
    "DeleteVirtualRouterInputRequestTypeDef",
    "DeleteVirtualServiceInputRequestTypeDef",
    "DescribeGatewayRouteInputRequestTypeDef",
    "DescribeMeshInputRequestTypeDef",
    "DescribeRouteInputRequestTypeDef",
    "DescribeVirtualGatewayInputRequestTypeDef",
    "DescribeVirtualNodeInputRequestTypeDef",
    "DescribeVirtualRouterInputRequestTypeDef",
    "DescribeVirtualServiceInputRequestTypeDef",
    "DnsServiceDiscoveryTypeDef",
    "DurationTypeDef",
    "EgressFilterTypeDef",
    "GatewayRouteStatusTypeDef",
    "ResourceMetadataTypeDef",
    "GatewayRouteHostnameMatchTypeDef",
    "GatewayRouteHostnameRewriteTypeDef",
    "GatewayRouteRefTypeDef",
    "GatewayRouteVirtualServiceTypeDef",
    "MatchRangeTypeDef",
    "WeightedTargetTypeDef",
    "HealthCheckPolicyTypeDef",
    "HttpPathMatchTypeDef",
    "HttpGatewayRoutePathRewriteTypeDef",
    "HttpGatewayRoutePrefixRewriteTypeDef",
    "QueryParameterMatchTypeDef",
    "PaginatorConfigTypeDef",
    "ListGatewayRoutesInputRequestTypeDef",
    "ListMeshesInputRequestTypeDef",
    "MeshRefTypeDef",
    "ListRoutesInputRequestTypeDef",
    "RouteRefTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListVirtualGatewaysInputRequestTypeDef",
    "VirtualGatewayRefTypeDef",
    "ListVirtualNodesInputRequestTypeDef",
    "VirtualNodeRefTypeDef",
    "ListVirtualRoutersInputRequestTypeDef",
    "VirtualRouterRefTypeDef",
    "ListVirtualServicesInputRequestTypeDef",
    "VirtualServiceRefTypeDef",
    "ListenerTlsAcmCertificateTypeDef",
    "TlsValidationContextFileTrustTypeDef",
    "TlsValidationContextSdsTrustTypeDef",
    "PortMappingTypeDef",
    "MeshStatusTypeDef",
    "MeshServiceDiscoveryTypeDef",
    "RouteStatusTypeDef",
    "SubjectAlternativeNameMatchersTypeDef",
    "TlsValidationContextAcmTrustTypeDef",
    "UntagResourceInputRequestTypeDef",
    "VirtualGatewayFileAccessLogTypeDef",
    "VirtualGatewayListenerTlsFileCertificateTypeDef",
    "VirtualGatewayListenerTlsSdsCertificateTypeDef",
    "VirtualGatewayGrpcConnectionPoolTypeDef",
    "VirtualGatewayHttp2ConnectionPoolTypeDef",
    "VirtualGatewayHttpConnectionPoolTypeDef",
    "VirtualGatewayStatusTypeDef",
    "VirtualGatewayHealthCheckPolicyTypeDef",
    "VirtualGatewayListenerTlsAcmCertificateTypeDef",
    "VirtualGatewayTlsValidationContextFileTrustTypeDef",
    "VirtualGatewayTlsValidationContextSdsTrustTypeDef",
    "VirtualGatewayPortMappingTypeDef",
    "VirtualGatewayTlsValidationContextAcmTrustTypeDef",
    "VirtualNodeGrpcConnectionPoolTypeDef",
    "VirtualNodeHttp2ConnectionPoolTypeDef",
    "VirtualNodeHttpConnectionPoolTypeDef",
    "VirtualNodeTcpConnectionPoolTypeDef",
    "VirtualNodeStatusTypeDef",
    "VirtualNodeServiceProviderTypeDef",
    "VirtualRouterStatusTypeDef",
    "VirtualRouterServiceProviderTypeDef",
    "VirtualServiceStatusTypeDef",
    "AccessLogTypeDef",
    "AwsCloudMapServiceDiscoveryTypeDef",
    "ClientTlsCertificateTypeDef",
    "TagResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "GrpcRetryPolicyTypeDef",
    "GrpcTimeoutTypeDef",
    "HttpRetryPolicyTypeDef",
    "HttpTimeoutTypeDef",
    "OutlierDetectionTypeDef",
    "TcpTimeoutTypeDef",
    "GrpcGatewayRouteRewriteTypeDef",
    "ListGatewayRoutesOutputTypeDef",
    "GatewayRouteTargetTypeDef",
    "GrpcMetadataMatchMethodTypeDef",
    "GrpcRouteMetadataMatchMethodTypeDef",
    "HeaderMatchMethodTypeDef",
    "GrpcRouteActionTypeDef",
    "HttpRouteActionTypeDef",
    "TcpRouteActionTypeDef",
    "HttpGatewayRouteRewriteTypeDef",
    "HttpQueryParameterTypeDef",
    "ListGatewayRoutesInputListGatewayRoutesPaginateTypeDef",
    "ListMeshesInputListMeshesPaginateTypeDef",
    "ListRoutesInputListRoutesPaginateTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef",
    "ListVirtualNodesInputListVirtualNodesPaginateTypeDef",
    "ListVirtualRoutersInputListVirtualRoutersPaginateTypeDef",
    "ListVirtualServicesInputListVirtualServicesPaginateTypeDef",
    "ListMeshesOutputTypeDef",
    "ListRoutesOutputTypeDef",
    "ListVirtualGatewaysOutputTypeDef",
    "ListVirtualNodesOutputTypeDef",
    "ListVirtualRoutersOutputTypeDef",
    "ListVirtualServicesOutputTypeDef",
    "ListenerTlsCertificateTypeDef",
    "ListenerTlsValidationContextTrustTypeDef",
    "VirtualRouterListenerTypeDef",
    "MeshSpecTypeDef",
    "SubjectAlternativeNamesTypeDef",
    "TlsValidationContextTrustTypeDef",
    "VirtualGatewayAccessLogTypeDef",
    "VirtualGatewayClientTlsCertificateTypeDef",
    "VirtualGatewayConnectionPoolTypeDef",
    "VirtualGatewayListenerTlsCertificateTypeDef",
    "VirtualGatewayListenerTlsValidationContextTrustTypeDef",
    "VirtualGatewayTlsValidationContextTrustTypeDef",
    "VirtualNodeConnectionPoolTypeDef",
    "VirtualServiceProviderTypeDef",
    "LoggingTypeDef",
    "ServiceDiscoveryTypeDef",
    "ListenerTimeoutTypeDef",
    "GrpcGatewayRouteActionTypeDef",
    "GrpcGatewayRouteMetadataTypeDef",
    "GrpcRouteMetadataTypeDef",
    "HttpGatewayRouteHeaderTypeDef",
    "HttpRouteHeaderTypeDef",
    "TcpRouteTypeDef",
    "HttpGatewayRouteActionTypeDef",
    "VirtualRouterSpecTypeDef",
    "CreateMeshInputRequestTypeDef",
    "MeshDataTypeDef",
    "UpdateMeshInputRequestTypeDef",
    "ListenerTlsValidationContextTypeDef",
    "TlsValidationContextTypeDef",
    "VirtualGatewayLoggingTypeDef",
    "VirtualGatewayListenerTlsValidationContextTypeDef",
    "VirtualGatewayTlsValidationContextTypeDef",
    "VirtualServiceSpecTypeDef",
    "GrpcGatewayRouteMatchTypeDef",
    "GrpcRouteMatchTypeDef",
    "HttpGatewayRouteMatchTypeDef",
    "HttpRouteMatchTypeDef",
    "CreateVirtualRouterInputRequestTypeDef",
    "UpdateVirtualRouterInputRequestTypeDef",
    "VirtualRouterDataTypeDef",
    "CreateMeshOutputTypeDef",
    "DeleteMeshOutputTypeDef",
    "DescribeMeshOutputTypeDef",
    "UpdateMeshOutputTypeDef",
    "ListenerTlsTypeDef",
    "ClientPolicyTlsTypeDef",
    "VirtualGatewayListenerTlsTypeDef",
    "VirtualGatewayClientPolicyTlsTypeDef",
    "CreateVirtualServiceInputRequestTypeDef",
    "UpdateVirtualServiceInputRequestTypeDef",
    "VirtualServiceDataTypeDef",
    "GrpcGatewayRouteTypeDef",
    "GrpcRouteTypeDef",
    "HttpGatewayRouteTypeDef",
    "HttpRouteTypeDef",
    "CreateVirtualRouterOutputTypeDef",
    "DeleteVirtualRouterOutputTypeDef",
    "DescribeVirtualRouterOutputTypeDef",
    "UpdateVirtualRouterOutputTypeDef",
    "ListenerTypeDef",
    "ClientPolicyTypeDef",
    "VirtualGatewayListenerTypeDef",
    "VirtualGatewayClientPolicyTypeDef",
    "CreateVirtualServiceOutputTypeDef",
    "DeleteVirtualServiceOutputTypeDef",
    "DescribeVirtualServiceOutputTypeDef",
    "UpdateVirtualServiceOutputTypeDef",
    "GatewayRouteSpecTypeDef",
    "RouteSpecTypeDef",
    "BackendDefaultsTypeDef",
    "VirtualServiceBackendTypeDef",
    "VirtualGatewayBackendDefaultsTypeDef",
    "CreateGatewayRouteInputRequestTypeDef",
    "GatewayRouteDataTypeDef",
    "UpdateGatewayRouteInputRequestTypeDef",
    "CreateRouteInputRequestTypeDef",
    "RouteDataTypeDef",
    "UpdateRouteInputRequestTypeDef",
    "BackendTypeDef",
    "VirtualGatewaySpecTypeDef",
    "CreateGatewayRouteOutputTypeDef",
    "DeleteGatewayRouteOutputTypeDef",
    "DescribeGatewayRouteOutputTypeDef",
    "UpdateGatewayRouteOutputTypeDef",
    "CreateRouteOutputTypeDef",
    "DeleteRouteOutputTypeDef",
    "DescribeRouteOutputTypeDef",
    "UpdateRouteOutputTypeDef",
    "VirtualNodeSpecTypeDef",
    "CreateVirtualGatewayInputRequestTypeDef",
    "UpdateVirtualGatewayInputRequestTypeDef",
    "VirtualGatewayDataTypeDef",
    "CreateVirtualNodeInputRequestTypeDef",
    "UpdateVirtualNodeInputRequestTypeDef",
    "VirtualNodeDataTypeDef",
    "CreateVirtualGatewayOutputTypeDef",
    "DeleteVirtualGatewayOutputTypeDef",
    "DescribeVirtualGatewayOutputTypeDef",
    "UpdateVirtualGatewayOutputTypeDef",
    "CreateVirtualNodeOutputTypeDef",
    "DeleteVirtualNodeOutputTypeDef",
    "DescribeVirtualNodeOutputTypeDef",
    "UpdateVirtualNodeOutputTypeDef",
)

FileAccessLogTypeDef = TypedDict(
    "FileAccessLogTypeDef",
    {
        "path": str,
    },
)

AwsCloudMapInstanceAttributeTypeDef = TypedDict(
    "AwsCloudMapInstanceAttributeTypeDef",
    {
        "key": str,
        "value": str,
    },
)

ListenerTlsFileCertificateTypeDef = TypedDict(
    "ListenerTlsFileCertificateTypeDef",
    {
        "certificateChain": str,
        "privateKey": str,
    },
)

ListenerTlsSdsCertificateTypeDef = TypedDict(
    "ListenerTlsSdsCertificateTypeDef",
    {
        "secretName": str,
    },
)

TagRefTypeDef = TypedDict(
    "TagRefTypeDef",
    {
        "key": str,
        "value": str,
    },
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

_RequiredDeleteGatewayRouteInputRequestTypeDef = TypedDict(
    "_RequiredDeleteGatewayRouteInputRequestTypeDef",
    {
        "gatewayRouteName": str,
        "meshName": str,
        "virtualGatewayName": str,
    },
)
_OptionalDeleteGatewayRouteInputRequestTypeDef = TypedDict(
    "_OptionalDeleteGatewayRouteInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DeleteGatewayRouteInputRequestTypeDef(
    _RequiredDeleteGatewayRouteInputRequestTypeDef, _OptionalDeleteGatewayRouteInputRequestTypeDef
):
    pass


DeleteMeshInputRequestTypeDef = TypedDict(
    "DeleteMeshInputRequestTypeDef",
    {
        "meshName": str,
    },
)

_RequiredDeleteRouteInputRequestTypeDef = TypedDict(
    "_RequiredDeleteRouteInputRequestTypeDef",
    {
        "meshName": str,
        "routeName": str,
        "virtualRouterName": str,
    },
)
_OptionalDeleteRouteInputRequestTypeDef = TypedDict(
    "_OptionalDeleteRouteInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DeleteRouteInputRequestTypeDef(
    _RequiredDeleteRouteInputRequestTypeDef, _OptionalDeleteRouteInputRequestTypeDef
):
    pass


_RequiredDeleteVirtualGatewayInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVirtualGatewayInputRequestTypeDef",
    {
        "meshName": str,
        "virtualGatewayName": str,
    },
)
_OptionalDeleteVirtualGatewayInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVirtualGatewayInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DeleteVirtualGatewayInputRequestTypeDef(
    _RequiredDeleteVirtualGatewayInputRequestTypeDef,
    _OptionalDeleteVirtualGatewayInputRequestTypeDef,
):
    pass


_RequiredDeleteVirtualNodeInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVirtualNodeInputRequestTypeDef",
    {
        "meshName": str,
        "virtualNodeName": str,
    },
)
_OptionalDeleteVirtualNodeInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVirtualNodeInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DeleteVirtualNodeInputRequestTypeDef(
    _RequiredDeleteVirtualNodeInputRequestTypeDef, _OptionalDeleteVirtualNodeInputRequestTypeDef
):
    pass


_RequiredDeleteVirtualRouterInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVirtualRouterInputRequestTypeDef",
    {
        "meshName": str,
        "virtualRouterName": str,
    },
)
_OptionalDeleteVirtualRouterInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVirtualRouterInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DeleteVirtualRouterInputRequestTypeDef(
    _RequiredDeleteVirtualRouterInputRequestTypeDef, _OptionalDeleteVirtualRouterInputRequestTypeDef
):
    pass


_RequiredDeleteVirtualServiceInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVirtualServiceInputRequestTypeDef",
    {
        "meshName": str,
        "virtualServiceName": str,
    },
)
_OptionalDeleteVirtualServiceInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVirtualServiceInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DeleteVirtualServiceInputRequestTypeDef(
    _RequiredDeleteVirtualServiceInputRequestTypeDef,
    _OptionalDeleteVirtualServiceInputRequestTypeDef,
):
    pass


_RequiredDescribeGatewayRouteInputRequestTypeDef = TypedDict(
    "_RequiredDescribeGatewayRouteInputRequestTypeDef",
    {
        "gatewayRouteName": str,
        "meshName": str,
        "virtualGatewayName": str,
    },
)
_OptionalDescribeGatewayRouteInputRequestTypeDef = TypedDict(
    "_OptionalDescribeGatewayRouteInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeGatewayRouteInputRequestTypeDef(
    _RequiredDescribeGatewayRouteInputRequestTypeDef,
    _OptionalDescribeGatewayRouteInputRequestTypeDef,
):
    pass


_RequiredDescribeMeshInputRequestTypeDef = TypedDict(
    "_RequiredDescribeMeshInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalDescribeMeshInputRequestTypeDef = TypedDict(
    "_OptionalDescribeMeshInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeMeshInputRequestTypeDef(
    _RequiredDescribeMeshInputRequestTypeDef, _OptionalDescribeMeshInputRequestTypeDef
):
    pass


_RequiredDescribeRouteInputRequestTypeDef = TypedDict(
    "_RequiredDescribeRouteInputRequestTypeDef",
    {
        "meshName": str,
        "routeName": str,
        "virtualRouterName": str,
    },
)
_OptionalDescribeRouteInputRequestTypeDef = TypedDict(
    "_OptionalDescribeRouteInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeRouteInputRequestTypeDef(
    _RequiredDescribeRouteInputRequestTypeDef, _OptionalDescribeRouteInputRequestTypeDef
):
    pass


_RequiredDescribeVirtualGatewayInputRequestTypeDef = TypedDict(
    "_RequiredDescribeVirtualGatewayInputRequestTypeDef",
    {
        "meshName": str,
        "virtualGatewayName": str,
    },
)
_OptionalDescribeVirtualGatewayInputRequestTypeDef = TypedDict(
    "_OptionalDescribeVirtualGatewayInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeVirtualGatewayInputRequestTypeDef(
    _RequiredDescribeVirtualGatewayInputRequestTypeDef,
    _OptionalDescribeVirtualGatewayInputRequestTypeDef,
):
    pass


_RequiredDescribeVirtualNodeInputRequestTypeDef = TypedDict(
    "_RequiredDescribeVirtualNodeInputRequestTypeDef",
    {
        "meshName": str,
        "virtualNodeName": str,
    },
)
_OptionalDescribeVirtualNodeInputRequestTypeDef = TypedDict(
    "_OptionalDescribeVirtualNodeInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeVirtualNodeInputRequestTypeDef(
    _RequiredDescribeVirtualNodeInputRequestTypeDef, _OptionalDescribeVirtualNodeInputRequestTypeDef
):
    pass


_RequiredDescribeVirtualRouterInputRequestTypeDef = TypedDict(
    "_RequiredDescribeVirtualRouterInputRequestTypeDef",
    {
        "meshName": str,
        "virtualRouterName": str,
    },
)
_OptionalDescribeVirtualRouterInputRequestTypeDef = TypedDict(
    "_OptionalDescribeVirtualRouterInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeVirtualRouterInputRequestTypeDef(
    _RequiredDescribeVirtualRouterInputRequestTypeDef,
    _OptionalDescribeVirtualRouterInputRequestTypeDef,
):
    pass


_RequiredDescribeVirtualServiceInputRequestTypeDef = TypedDict(
    "_RequiredDescribeVirtualServiceInputRequestTypeDef",
    {
        "meshName": str,
        "virtualServiceName": str,
    },
)
_OptionalDescribeVirtualServiceInputRequestTypeDef = TypedDict(
    "_OptionalDescribeVirtualServiceInputRequestTypeDef",
    {
        "meshOwner": str,
    },
    total=False,
)


class DescribeVirtualServiceInputRequestTypeDef(
    _RequiredDescribeVirtualServiceInputRequestTypeDef,
    _OptionalDescribeVirtualServiceInputRequestTypeDef,
):
    pass


_RequiredDnsServiceDiscoveryTypeDef = TypedDict(
    "_RequiredDnsServiceDiscoveryTypeDef",
    {
        "hostname": str,
    },
)
_OptionalDnsServiceDiscoveryTypeDef = TypedDict(
    "_OptionalDnsServiceDiscoveryTypeDef",
    {
        "ipPreference": IpPreferenceType,
        "responseType": DnsResponseTypeType,
    },
    total=False,
)


class DnsServiceDiscoveryTypeDef(
    _RequiredDnsServiceDiscoveryTypeDef, _OptionalDnsServiceDiscoveryTypeDef
):
    pass


DurationTypeDef = TypedDict(
    "DurationTypeDef",
    {
        "unit": DurationUnitType,
        "value": int,
    },
    total=False,
)

EgressFilterTypeDef = TypedDict(
    "EgressFilterTypeDef",
    {
        "type": EgressFilterTypeType,
    },
)

GatewayRouteStatusTypeDef = TypedDict(
    "GatewayRouteStatusTypeDef",
    {
        "status": GatewayRouteStatusCodeType,
    },
)

ResourceMetadataTypeDef = TypedDict(
    "ResourceMetadataTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshOwner": str,
        "resourceOwner": str,
        "uid": str,
        "version": int,
    },
)

GatewayRouteHostnameMatchTypeDef = TypedDict(
    "GatewayRouteHostnameMatchTypeDef",
    {
        "exact": str,
        "suffix": str,
    },
    total=False,
)

GatewayRouteHostnameRewriteTypeDef = TypedDict(
    "GatewayRouteHostnameRewriteTypeDef",
    {
        "defaultTargetHostname": DefaultGatewayRouteRewriteType,
    },
    total=False,
)

GatewayRouteRefTypeDef = TypedDict(
    "GatewayRouteRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "gatewayRouteName": str,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualGatewayName": str,
    },
)

GatewayRouteVirtualServiceTypeDef = TypedDict(
    "GatewayRouteVirtualServiceTypeDef",
    {
        "virtualServiceName": str,
    },
)

MatchRangeTypeDef = TypedDict(
    "MatchRangeTypeDef",
    {
        "end": int,
        "start": int,
    },
)

WeightedTargetTypeDef = TypedDict(
    "WeightedTargetTypeDef",
    {
        "virtualNode": str,
        "weight": int,
    },
)

_RequiredHealthCheckPolicyTypeDef = TypedDict(
    "_RequiredHealthCheckPolicyTypeDef",
    {
        "healthyThreshold": int,
        "intervalMillis": int,
        "protocol": PortProtocolType,
        "timeoutMillis": int,
        "unhealthyThreshold": int,
    },
)
_OptionalHealthCheckPolicyTypeDef = TypedDict(
    "_OptionalHealthCheckPolicyTypeDef",
    {
        "path": str,
        "port": int,
    },
    total=False,
)


class HealthCheckPolicyTypeDef(
    _RequiredHealthCheckPolicyTypeDef, _OptionalHealthCheckPolicyTypeDef
):
    pass


HttpPathMatchTypeDef = TypedDict(
    "HttpPathMatchTypeDef",
    {
        "exact": str,
        "regex": str,
    },
    total=False,
)

HttpGatewayRoutePathRewriteTypeDef = TypedDict(
    "HttpGatewayRoutePathRewriteTypeDef",
    {
        "exact": str,
    },
    total=False,
)

HttpGatewayRoutePrefixRewriteTypeDef = TypedDict(
    "HttpGatewayRoutePrefixRewriteTypeDef",
    {
        "defaultPrefix": DefaultGatewayRouteRewriteType,
        "value": str,
    },
    total=False,
)

QueryParameterMatchTypeDef = TypedDict(
    "QueryParameterMatchTypeDef",
    {
        "exact": str,
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

_RequiredListGatewayRoutesInputRequestTypeDef = TypedDict(
    "_RequiredListGatewayRoutesInputRequestTypeDef",
    {
        "meshName": str,
        "virtualGatewayName": str,
    },
)
_OptionalListGatewayRoutesInputRequestTypeDef = TypedDict(
    "_OptionalListGatewayRoutesInputRequestTypeDef",
    {
        "limit": int,
        "meshOwner": str,
        "nextToken": str,
    },
    total=False,
)


class ListGatewayRoutesInputRequestTypeDef(
    _RequiredListGatewayRoutesInputRequestTypeDef, _OptionalListGatewayRoutesInputRequestTypeDef
):
    pass


ListMeshesInputRequestTypeDef = TypedDict(
    "ListMeshesInputRequestTypeDef",
    {
        "limit": int,
        "nextToken": str,
    },
    total=False,
)

MeshRefTypeDef = TypedDict(
    "MeshRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
    },
)

_RequiredListRoutesInputRequestTypeDef = TypedDict(
    "_RequiredListRoutesInputRequestTypeDef",
    {
        "meshName": str,
        "virtualRouterName": str,
    },
)
_OptionalListRoutesInputRequestTypeDef = TypedDict(
    "_OptionalListRoutesInputRequestTypeDef",
    {
        "limit": int,
        "meshOwner": str,
        "nextToken": str,
    },
    total=False,
)


class ListRoutesInputRequestTypeDef(
    _RequiredListRoutesInputRequestTypeDef, _OptionalListRoutesInputRequestTypeDef
):
    pass


RouteRefTypeDef = TypedDict(
    "RouteRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "routeName": str,
        "version": int,
        "virtualRouterName": str,
    },
)

_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "limit": int,
        "nextToken": str,
    },
    total=False,
)


class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass


_RequiredListVirtualGatewaysInputRequestTypeDef = TypedDict(
    "_RequiredListVirtualGatewaysInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualGatewaysInputRequestTypeDef = TypedDict(
    "_OptionalListVirtualGatewaysInputRequestTypeDef",
    {
        "limit": int,
        "meshOwner": str,
        "nextToken": str,
    },
    total=False,
)


class ListVirtualGatewaysInputRequestTypeDef(
    _RequiredListVirtualGatewaysInputRequestTypeDef, _OptionalListVirtualGatewaysInputRequestTypeDef
):
    pass


VirtualGatewayRefTypeDef = TypedDict(
    "VirtualGatewayRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualGatewayName": str,
    },
)

_RequiredListVirtualNodesInputRequestTypeDef = TypedDict(
    "_RequiredListVirtualNodesInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualNodesInputRequestTypeDef = TypedDict(
    "_OptionalListVirtualNodesInputRequestTypeDef",
    {
        "limit": int,
        "meshOwner": str,
        "nextToken": str,
    },
    total=False,
)


class ListVirtualNodesInputRequestTypeDef(
    _RequiredListVirtualNodesInputRequestTypeDef, _OptionalListVirtualNodesInputRequestTypeDef
):
    pass


VirtualNodeRefTypeDef = TypedDict(
    "VirtualNodeRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualNodeName": str,
    },
)

_RequiredListVirtualRoutersInputRequestTypeDef = TypedDict(
    "_RequiredListVirtualRoutersInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualRoutersInputRequestTypeDef = TypedDict(
    "_OptionalListVirtualRoutersInputRequestTypeDef",
    {
        "limit": int,
        "meshOwner": str,
        "nextToken": str,
    },
    total=False,
)


class ListVirtualRoutersInputRequestTypeDef(
    _RequiredListVirtualRoutersInputRequestTypeDef, _OptionalListVirtualRoutersInputRequestTypeDef
):
    pass


VirtualRouterRefTypeDef = TypedDict(
    "VirtualRouterRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualRouterName": str,
    },
)

_RequiredListVirtualServicesInputRequestTypeDef = TypedDict(
    "_RequiredListVirtualServicesInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualServicesInputRequestTypeDef = TypedDict(
    "_OptionalListVirtualServicesInputRequestTypeDef",
    {
        "limit": int,
        "meshOwner": str,
        "nextToken": str,
    },
    total=False,
)


class ListVirtualServicesInputRequestTypeDef(
    _RequiredListVirtualServicesInputRequestTypeDef, _OptionalListVirtualServicesInputRequestTypeDef
):
    pass


VirtualServiceRefTypeDef = TypedDict(
    "VirtualServiceRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualServiceName": str,
    },
)

ListenerTlsAcmCertificateTypeDef = TypedDict(
    "ListenerTlsAcmCertificateTypeDef",
    {
        "certificateArn": str,
    },
)

TlsValidationContextFileTrustTypeDef = TypedDict(
    "TlsValidationContextFileTrustTypeDef",
    {
        "certificateChain": str,
    },
)

TlsValidationContextSdsTrustTypeDef = TypedDict(
    "TlsValidationContextSdsTrustTypeDef",
    {
        "secretName": str,
    },
)

PortMappingTypeDef = TypedDict(
    "PortMappingTypeDef",
    {
        "port": int,
        "protocol": PortProtocolType,
    },
)

MeshStatusTypeDef = TypedDict(
    "MeshStatusTypeDef",
    {
        "status": MeshStatusCodeType,
    },
    total=False,
)

MeshServiceDiscoveryTypeDef = TypedDict(
    "MeshServiceDiscoveryTypeDef",
    {
        "ipPreference": IpPreferenceType,
    },
    total=False,
)

RouteStatusTypeDef = TypedDict(
    "RouteStatusTypeDef",
    {
        "status": RouteStatusCodeType,
    },
)

SubjectAlternativeNameMatchersTypeDef = TypedDict(
    "SubjectAlternativeNameMatchersTypeDef",
    {
        "exact": Sequence[str],
    },
)

TlsValidationContextAcmTrustTypeDef = TypedDict(
    "TlsValidationContextAcmTrustTypeDef",
    {
        "certificateAuthorityArns": Sequence[str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

VirtualGatewayFileAccessLogTypeDef = TypedDict(
    "VirtualGatewayFileAccessLogTypeDef",
    {
        "path": str,
    },
)

VirtualGatewayListenerTlsFileCertificateTypeDef = TypedDict(
    "VirtualGatewayListenerTlsFileCertificateTypeDef",
    {
        "certificateChain": str,
        "privateKey": str,
    },
)

VirtualGatewayListenerTlsSdsCertificateTypeDef = TypedDict(
    "VirtualGatewayListenerTlsSdsCertificateTypeDef",
    {
        "secretName": str,
    },
)

VirtualGatewayGrpcConnectionPoolTypeDef = TypedDict(
    "VirtualGatewayGrpcConnectionPoolTypeDef",
    {
        "maxRequests": int,
    },
)

VirtualGatewayHttp2ConnectionPoolTypeDef = TypedDict(
    "VirtualGatewayHttp2ConnectionPoolTypeDef",
    {
        "maxRequests": int,
    },
)

_RequiredVirtualGatewayHttpConnectionPoolTypeDef = TypedDict(
    "_RequiredVirtualGatewayHttpConnectionPoolTypeDef",
    {
        "maxConnections": int,
    },
)
_OptionalVirtualGatewayHttpConnectionPoolTypeDef = TypedDict(
    "_OptionalVirtualGatewayHttpConnectionPoolTypeDef",
    {
        "maxPendingRequests": int,
    },
    total=False,
)


class VirtualGatewayHttpConnectionPoolTypeDef(
    _RequiredVirtualGatewayHttpConnectionPoolTypeDef,
    _OptionalVirtualGatewayHttpConnectionPoolTypeDef,
):
    pass


VirtualGatewayStatusTypeDef = TypedDict(
    "VirtualGatewayStatusTypeDef",
    {
        "status": VirtualGatewayStatusCodeType,
    },
)

_RequiredVirtualGatewayHealthCheckPolicyTypeDef = TypedDict(
    "_RequiredVirtualGatewayHealthCheckPolicyTypeDef",
    {
        "healthyThreshold": int,
        "intervalMillis": int,
        "protocol": VirtualGatewayPortProtocolType,
        "timeoutMillis": int,
        "unhealthyThreshold": int,
    },
)
_OptionalVirtualGatewayHealthCheckPolicyTypeDef = TypedDict(
    "_OptionalVirtualGatewayHealthCheckPolicyTypeDef",
    {
        "path": str,
        "port": int,
    },
    total=False,
)


class VirtualGatewayHealthCheckPolicyTypeDef(
    _RequiredVirtualGatewayHealthCheckPolicyTypeDef, _OptionalVirtualGatewayHealthCheckPolicyTypeDef
):
    pass


VirtualGatewayListenerTlsAcmCertificateTypeDef = TypedDict(
    "VirtualGatewayListenerTlsAcmCertificateTypeDef",
    {
        "certificateArn": str,
    },
)

VirtualGatewayTlsValidationContextFileTrustTypeDef = TypedDict(
    "VirtualGatewayTlsValidationContextFileTrustTypeDef",
    {
        "certificateChain": str,
    },
)

VirtualGatewayTlsValidationContextSdsTrustTypeDef = TypedDict(
    "VirtualGatewayTlsValidationContextSdsTrustTypeDef",
    {
        "secretName": str,
    },
)

VirtualGatewayPortMappingTypeDef = TypedDict(
    "VirtualGatewayPortMappingTypeDef",
    {
        "port": int,
        "protocol": VirtualGatewayPortProtocolType,
    },
)

VirtualGatewayTlsValidationContextAcmTrustTypeDef = TypedDict(
    "VirtualGatewayTlsValidationContextAcmTrustTypeDef",
    {
        "certificateAuthorityArns": Sequence[str],
    },
)

VirtualNodeGrpcConnectionPoolTypeDef = TypedDict(
    "VirtualNodeGrpcConnectionPoolTypeDef",
    {
        "maxRequests": int,
    },
)

VirtualNodeHttp2ConnectionPoolTypeDef = TypedDict(
    "VirtualNodeHttp2ConnectionPoolTypeDef",
    {
        "maxRequests": int,
    },
)

_RequiredVirtualNodeHttpConnectionPoolTypeDef = TypedDict(
    "_RequiredVirtualNodeHttpConnectionPoolTypeDef",
    {
        "maxConnections": int,
    },
)
_OptionalVirtualNodeHttpConnectionPoolTypeDef = TypedDict(
    "_OptionalVirtualNodeHttpConnectionPoolTypeDef",
    {
        "maxPendingRequests": int,
    },
    total=False,
)


class VirtualNodeHttpConnectionPoolTypeDef(
    _RequiredVirtualNodeHttpConnectionPoolTypeDef, _OptionalVirtualNodeHttpConnectionPoolTypeDef
):
    pass


VirtualNodeTcpConnectionPoolTypeDef = TypedDict(
    "VirtualNodeTcpConnectionPoolTypeDef",
    {
        "maxConnections": int,
    },
)

VirtualNodeStatusTypeDef = TypedDict(
    "VirtualNodeStatusTypeDef",
    {
        "status": VirtualNodeStatusCodeType,
    },
)

VirtualNodeServiceProviderTypeDef = TypedDict(
    "VirtualNodeServiceProviderTypeDef",
    {
        "virtualNodeName": str,
    },
)

VirtualRouterStatusTypeDef = TypedDict(
    "VirtualRouterStatusTypeDef",
    {
        "status": VirtualRouterStatusCodeType,
    },
)

VirtualRouterServiceProviderTypeDef = TypedDict(
    "VirtualRouterServiceProviderTypeDef",
    {
        "virtualRouterName": str,
    },
)

VirtualServiceStatusTypeDef = TypedDict(
    "VirtualServiceStatusTypeDef",
    {
        "status": VirtualServiceStatusCodeType,
    },
)

AccessLogTypeDef = TypedDict(
    "AccessLogTypeDef",
    {
        "file": FileAccessLogTypeDef,
    },
    total=False,
)

_RequiredAwsCloudMapServiceDiscoveryTypeDef = TypedDict(
    "_RequiredAwsCloudMapServiceDiscoveryTypeDef",
    {
        "namespaceName": str,
        "serviceName": str,
    },
)
_OptionalAwsCloudMapServiceDiscoveryTypeDef = TypedDict(
    "_OptionalAwsCloudMapServiceDiscoveryTypeDef",
    {
        "attributes": Sequence[AwsCloudMapInstanceAttributeTypeDef],
        "ipPreference": IpPreferenceType,
    },
    total=False,
)


class AwsCloudMapServiceDiscoveryTypeDef(
    _RequiredAwsCloudMapServiceDiscoveryTypeDef, _OptionalAwsCloudMapServiceDiscoveryTypeDef
):
    pass


ClientTlsCertificateTypeDef = TypedDict(
    "ClientTlsCertificateTypeDef",
    {
        "file": ListenerTlsFileCertificateTypeDef,
        "sds": ListenerTlsSdsCertificateTypeDef,
    },
    total=False,
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagRefTypeDef],
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "nextToken": str,
        "tags": List[TagRefTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGrpcRetryPolicyTypeDef = TypedDict(
    "_RequiredGrpcRetryPolicyTypeDef",
    {
        "maxRetries": int,
        "perRetryTimeout": DurationTypeDef,
    },
)
_OptionalGrpcRetryPolicyTypeDef = TypedDict(
    "_OptionalGrpcRetryPolicyTypeDef",
    {
        "grpcRetryEvents": Sequence[GrpcRetryPolicyEventType],
        "httpRetryEvents": Sequence[str],
        "tcpRetryEvents": Sequence[Literal["connection-error"]],
    },
    total=False,
)


class GrpcRetryPolicyTypeDef(_RequiredGrpcRetryPolicyTypeDef, _OptionalGrpcRetryPolicyTypeDef):
    pass


GrpcTimeoutTypeDef = TypedDict(
    "GrpcTimeoutTypeDef",
    {
        "idle": DurationTypeDef,
        "perRequest": DurationTypeDef,
    },
    total=False,
)

_RequiredHttpRetryPolicyTypeDef = TypedDict(
    "_RequiredHttpRetryPolicyTypeDef",
    {
        "maxRetries": int,
        "perRetryTimeout": DurationTypeDef,
    },
)
_OptionalHttpRetryPolicyTypeDef = TypedDict(
    "_OptionalHttpRetryPolicyTypeDef",
    {
        "httpRetryEvents": Sequence[str],
        "tcpRetryEvents": Sequence[Literal["connection-error"]],
    },
    total=False,
)


class HttpRetryPolicyTypeDef(_RequiredHttpRetryPolicyTypeDef, _OptionalHttpRetryPolicyTypeDef):
    pass


HttpTimeoutTypeDef = TypedDict(
    "HttpTimeoutTypeDef",
    {
        "idle": DurationTypeDef,
        "perRequest": DurationTypeDef,
    },
    total=False,
)

OutlierDetectionTypeDef = TypedDict(
    "OutlierDetectionTypeDef",
    {
        "baseEjectionDuration": DurationTypeDef,
        "interval": DurationTypeDef,
        "maxEjectionPercent": int,
        "maxServerErrors": int,
    },
)

TcpTimeoutTypeDef = TypedDict(
    "TcpTimeoutTypeDef",
    {
        "idle": DurationTypeDef,
    },
    total=False,
)

GrpcGatewayRouteRewriteTypeDef = TypedDict(
    "GrpcGatewayRouteRewriteTypeDef",
    {
        "hostname": GatewayRouteHostnameRewriteTypeDef,
    },
    total=False,
)

ListGatewayRoutesOutputTypeDef = TypedDict(
    "ListGatewayRoutesOutputTypeDef",
    {
        "gatewayRoutes": List[GatewayRouteRefTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GatewayRouteTargetTypeDef = TypedDict(
    "GatewayRouteTargetTypeDef",
    {
        "virtualService": GatewayRouteVirtualServiceTypeDef,
    },
)

GrpcMetadataMatchMethodTypeDef = TypedDict(
    "GrpcMetadataMatchMethodTypeDef",
    {
        "exact": str,
        "prefix": str,
        "range": MatchRangeTypeDef,
        "regex": str,
        "suffix": str,
    },
    total=False,
)

GrpcRouteMetadataMatchMethodTypeDef = TypedDict(
    "GrpcRouteMetadataMatchMethodTypeDef",
    {
        "exact": str,
        "prefix": str,
        "range": MatchRangeTypeDef,
        "regex": str,
        "suffix": str,
    },
    total=False,
)

HeaderMatchMethodTypeDef = TypedDict(
    "HeaderMatchMethodTypeDef",
    {
        "exact": str,
        "prefix": str,
        "range": MatchRangeTypeDef,
        "regex": str,
        "suffix": str,
    },
    total=False,
)

GrpcRouteActionTypeDef = TypedDict(
    "GrpcRouteActionTypeDef",
    {
        "weightedTargets": Sequence[WeightedTargetTypeDef],
    },
)

HttpRouteActionTypeDef = TypedDict(
    "HttpRouteActionTypeDef",
    {
        "weightedTargets": Sequence[WeightedTargetTypeDef],
    },
)

TcpRouteActionTypeDef = TypedDict(
    "TcpRouteActionTypeDef",
    {
        "weightedTargets": Sequence[WeightedTargetTypeDef],
    },
)

HttpGatewayRouteRewriteTypeDef = TypedDict(
    "HttpGatewayRouteRewriteTypeDef",
    {
        "hostname": GatewayRouteHostnameRewriteTypeDef,
        "path": HttpGatewayRoutePathRewriteTypeDef,
        "prefix": HttpGatewayRoutePrefixRewriteTypeDef,
    },
    total=False,
)

_RequiredHttpQueryParameterTypeDef = TypedDict(
    "_RequiredHttpQueryParameterTypeDef",
    {
        "name": str,
    },
)
_OptionalHttpQueryParameterTypeDef = TypedDict(
    "_OptionalHttpQueryParameterTypeDef",
    {
        "match": QueryParameterMatchTypeDef,
    },
    total=False,
)


class HttpQueryParameterTypeDef(
    _RequiredHttpQueryParameterTypeDef, _OptionalHttpQueryParameterTypeDef
):
    pass


_RequiredListGatewayRoutesInputListGatewayRoutesPaginateTypeDef = TypedDict(
    "_RequiredListGatewayRoutesInputListGatewayRoutesPaginateTypeDef",
    {
        "meshName": str,
        "virtualGatewayName": str,
    },
)
_OptionalListGatewayRoutesInputListGatewayRoutesPaginateTypeDef = TypedDict(
    "_OptionalListGatewayRoutesInputListGatewayRoutesPaginateTypeDef",
    {
        "meshOwner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGatewayRoutesInputListGatewayRoutesPaginateTypeDef(
    _RequiredListGatewayRoutesInputListGatewayRoutesPaginateTypeDef,
    _OptionalListGatewayRoutesInputListGatewayRoutesPaginateTypeDef,
):
    pass


ListMeshesInputListMeshesPaginateTypeDef = TypedDict(
    "ListMeshesInputListMeshesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRoutesInputListRoutesPaginateTypeDef = TypedDict(
    "_RequiredListRoutesInputListRoutesPaginateTypeDef",
    {
        "meshName": str,
        "virtualRouterName": str,
    },
)
_OptionalListRoutesInputListRoutesPaginateTypeDef = TypedDict(
    "_OptionalListRoutesInputListRoutesPaginateTypeDef",
    {
        "meshOwner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRoutesInputListRoutesPaginateTypeDef(
    _RequiredListRoutesInputListRoutesPaginateTypeDef,
    _OptionalListRoutesInputListRoutesPaginateTypeDef,
):
    pass


_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef = TypedDict(
    "_RequiredListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef = TypedDict(
    "_OptionalListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef",
    {
        "meshOwner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef(
    _RequiredListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef,
    _OptionalListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef,
):
    pass


_RequiredListVirtualNodesInputListVirtualNodesPaginateTypeDef = TypedDict(
    "_RequiredListVirtualNodesInputListVirtualNodesPaginateTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualNodesInputListVirtualNodesPaginateTypeDef = TypedDict(
    "_OptionalListVirtualNodesInputListVirtualNodesPaginateTypeDef",
    {
        "meshOwner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListVirtualNodesInputListVirtualNodesPaginateTypeDef(
    _RequiredListVirtualNodesInputListVirtualNodesPaginateTypeDef,
    _OptionalListVirtualNodesInputListVirtualNodesPaginateTypeDef,
):
    pass


_RequiredListVirtualRoutersInputListVirtualRoutersPaginateTypeDef = TypedDict(
    "_RequiredListVirtualRoutersInputListVirtualRoutersPaginateTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualRoutersInputListVirtualRoutersPaginateTypeDef = TypedDict(
    "_OptionalListVirtualRoutersInputListVirtualRoutersPaginateTypeDef",
    {
        "meshOwner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListVirtualRoutersInputListVirtualRoutersPaginateTypeDef(
    _RequiredListVirtualRoutersInputListVirtualRoutersPaginateTypeDef,
    _OptionalListVirtualRoutersInputListVirtualRoutersPaginateTypeDef,
):
    pass


_RequiredListVirtualServicesInputListVirtualServicesPaginateTypeDef = TypedDict(
    "_RequiredListVirtualServicesInputListVirtualServicesPaginateTypeDef",
    {
        "meshName": str,
    },
)
_OptionalListVirtualServicesInputListVirtualServicesPaginateTypeDef = TypedDict(
    "_OptionalListVirtualServicesInputListVirtualServicesPaginateTypeDef",
    {
        "meshOwner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListVirtualServicesInputListVirtualServicesPaginateTypeDef(
    _RequiredListVirtualServicesInputListVirtualServicesPaginateTypeDef,
    _OptionalListVirtualServicesInputListVirtualServicesPaginateTypeDef,
):
    pass


ListMeshesOutputTypeDef = TypedDict(
    "ListMeshesOutputTypeDef",
    {
        "meshes": List[MeshRefTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoutesOutputTypeDef = TypedDict(
    "ListRoutesOutputTypeDef",
    {
        "nextToken": str,
        "routes": List[RouteRefTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualGatewaysOutputTypeDef = TypedDict(
    "ListVirtualGatewaysOutputTypeDef",
    {
        "nextToken": str,
        "virtualGateways": List[VirtualGatewayRefTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualNodesOutputTypeDef = TypedDict(
    "ListVirtualNodesOutputTypeDef",
    {
        "nextToken": str,
        "virtualNodes": List[VirtualNodeRefTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualRoutersOutputTypeDef = TypedDict(
    "ListVirtualRoutersOutputTypeDef",
    {
        "nextToken": str,
        "virtualRouters": List[VirtualRouterRefTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualServicesOutputTypeDef = TypedDict(
    "ListVirtualServicesOutputTypeDef",
    {
        "nextToken": str,
        "virtualServices": List[VirtualServiceRefTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListenerTlsCertificateTypeDef = TypedDict(
    "ListenerTlsCertificateTypeDef",
    {
        "acm": ListenerTlsAcmCertificateTypeDef,
        "file": ListenerTlsFileCertificateTypeDef,
        "sds": ListenerTlsSdsCertificateTypeDef,
    },
    total=False,
)

ListenerTlsValidationContextTrustTypeDef = TypedDict(
    "ListenerTlsValidationContextTrustTypeDef",
    {
        "file": TlsValidationContextFileTrustTypeDef,
        "sds": TlsValidationContextSdsTrustTypeDef,
    },
    total=False,
)

VirtualRouterListenerTypeDef = TypedDict(
    "VirtualRouterListenerTypeDef",
    {
        "portMapping": PortMappingTypeDef,
    },
)

MeshSpecTypeDef = TypedDict(
    "MeshSpecTypeDef",
    {
        "egressFilter": EgressFilterTypeDef,
        "serviceDiscovery": MeshServiceDiscoveryTypeDef,
    },
    total=False,
)

SubjectAlternativeNamesTypeDef = TypedDict(
    "SubjectAlternativeNamesTypeDef",
    {
        "match": SubjectAlternativeNameMatchersTypeDef,
    },
)

TlsValidationContextTrustTypeDef = TypedDict(
    "TlsValidationContextTrustTypeDef",
    {
        "acm": TlsValidationContextAcmTrustTypeDef,
        "file": TlsValidationContextFileTrustTypeDef,
        "sds": TlsValidationContextSdsTrustTypeDef,
    },
    total=False,
)

VirtualGatewayAccessLogTypeDef = TypedDict(
    "VirtualGatewayAccessLogTypeDef",
    {
        "file": VirtualGatewayFileAccessLogTypeDef,
    },
    total=False,
)

VirtualGatewayClientTlsCertificateTypeDef = TypedDict(
    "VirtualGatewayClientTlsCertificateTypeDef",
    {
        "file": VirtualGatewayListenerTlsFileCertificateTypeDef,
        "sds": VirtualGatewayListenerTlsSdsCertificateTypeDef,
    },
    total=False,
)

VirtualGatewayConnectionPoolTypeDef = TypedDict(
    "VirtualGatewayConnectionPoolTypeDef",
    {
        "grpc": VirtualGatewayGrpcConnectionPoolTypeDef,
        "http": VirtualGatewayHttpConnectionPoolTypeDef,
        "http2": VirtualGatewayHttp2ConnectionPoolTypeDef,
    },
    total=False,
)

VirtualGatewayListenerTlsCertificateTypeDef = TypedDict(
    "VirtualGatewayListenerTlsCertificateTypeDef",
    {
        "acm": VirtualGatewayListenerTlsAcmCertificateTypeDef,
        "file": VirtualGatewayListenerTlsFileCertificateTypeDef,
        "sds": VirtualGatewayListenerTlsSdsCertificateTypeDef,
    },
    total=False,
)

VirtualGatewayListenerTlsValidationContextTrustTypeDef = TypedDict(
    "VirtualGatewayListenerTlsValidationContextTrustTypeDef",
    {
        "file": VirtualGatewayTlsValidationContextFileTrustTypeDef,
        "sds": VirtualGatewayTlsValidationContextSdsTrustTypeDef,
    },
    total=False,
)

VirtualGatewayTlsValidationContextTrustTypeDef = TypedDict(
    "VirtualGatewayTlsValidationContextTrustTypeDef",
    {
        "acm": VirtualGatewayTlsValidationContextAcmTrustTypeDef,
        "file": VirtualGatewayTlsValidationContextFileTrustTypeDef,
        "sds": VirtualGatewayTlsValidationContextSdsTrustTypeDef,
    },
    total=False,
)

VirtualNodeConnectionPoolTypeDef = TypedDict(
    "VirtualNodeConnectionPoolTypeDef",
    {
        "grpc": VirtualNodeGrpcConnectionPoolTypeDef,
        "http": VirtualNodeHttpConnectionPoolTypeDef,
        "http2": VirtualNodeHttp2ConnectionPoolTypeDef,
        "tcp": VirtualNodeTcpConnectionPoolTypeDef,
    },
    total=False,
)

VirtualServiceProviderTypeDef = TypedDict(
    "VirtualServiceProviderTypeDef",
    {
        "virtualNode": VirtualNodeServiceProviderTypeDef,
        "virtualRouter": VirtualRouterServiceProviderTypeDef,
    },
    total=False,
)

LoggingTypeDef = TypedDict(
    "LoggingTypeDef",
    {
        "accessLog": AccessLogTypeDef,
    },
    total=False,
)

ServiceDiscoveryTypeDef = TypedDict(
    "ServiceDiscoveryTypeDef",
    {
        "awsCloudMap": AwsCloudMapServiceDiscoveryTypeDef,
        "dns": DnsServiceDiscoveryTypeDef,
    },
    total=False,
)

ListenerTimeoutTypeDef = TypedDict(
    "ListenerTimeoutTypeDef",
    {
        "grpc": GrpcTimeoutTypeDef,
        "http": HttpTimeoutTypeDef,
        "http2": HttpTimeoutTypeDef,
        "tcp": TcpTimeoutTypeDef,
    },
    total=False,
)

_RequiredGrpcGatewayRouteActionTypeDef = TypedDict(
    "_RequiredGrpcGatewayRouteActionTypeDef",
    {
        "target": GatewayRouteTargetTypeDef,
    },
)
_OptionalGrpcGatewayRouteActionTypeDef = TypedDict(
    "_OptionalGrpcGatewayRouteActionTypeDef",
    {
        "rewrite": GrpcGatewayRouteRewriteTypeDef,
    },
    total=False,
)


class GrpcGatewayRouteActionTypeDef(
    _RequiredGrpcGatewayRouteActionTypeDef, _OptionalGrpcGatewayRouteActionTypeDef
):
    pass


_RequiredGrpcGatewayRouteMetadataTypeDef = TypedDict(
    "_RequiredGrpcGatewayRouteMetadataTypeDef",
    {
        "name": str,
    },
)
_OptionalGrpcGatewayRouteMetadataTypeDef = TypedDict(
    "_OptionalGrpcGatewayRouteMetadataTypeDef",
    {
        "invert": bool,
        "match": GrpcMetadataMatchMethodTypeDef,
    },
    total=False,
)


class GrpcGatewayRouteMetadataTypeDef(
    _RequiredGrpcGatewayRouteMetadataTypeDef, _OptionalGrpcGatewayRouteMetadataTypeDef
):
    pass


_RequiredGrpcRouteMetadataTypeDef = TypedDict(
    "_RequiredGrpcRouteMetadataTypeDef",
    {
        "name": str,
    },
)
_OptionalGrpcRouteMetadataTypeDef = TypedDict(
    "_OptionalGrpcRouteMetadataTypeDef",
    {
        "invert": bool,
        "match": GrpcRouteMetadataMatchMethodTypeDef,
    },
    total=False,
)


class GrpcRouteMetadataTypeDef(
    _RequiredGrpcRouteMetadataTypeDef, _OptionalGrpcRouteMetadataTypeDef
):
    pass


_RequiredHttpGatewayRouteHeaderTypeDef = TypedDict(
    "_RequiredHttpGatewayRouteHeaderTypeDef",
    {
        "name": str,
    },
)
_OptionalHttpGatewayRouteHeaderTypeDef = TypedDict(
    "_OptionalHttpGatewayRouteHeaderTypeDef",
    {
        "invert": bool,
        "match": HeaderMatchMethodTypeDef,
    },
    total=False,
)


class HttpGatewayRouteHeaderTypeDef(
    _RequiredHttpGatewayRouteHeaderTypeDef, _OptionalHttpGatewayRouteHeaderTypeDef
):
    pass


_RequiredHttpRouteHeaderTypeDef = TypedDict(
    "_RequiredHttpRouteHeaderTypeDef",
    {
        "name": str,
    },
)
_OptionalHttpRouteHeaderTypeDef = TypedDict(
    "_OptionalHttpRouteHeaderTypeDef",
    {
        "invert": bool,
        "match": HeaderMatchMethodTypeDef,
    },
    total=False,
)


class HttpRouteHeaderTypeDef(_RequiredHttpRouteHeaderTypeDef, _OptionalHttpRouteHeaderTypeDef):
    pass


_RequiredTcpRouteTypeDef = TypedDict(
    "_RequiredTcpRouteTypeDef",
    {
        "action": TcpRouteActionTypeDef,
    },
)
_OptionalTcpRouteTypeDef = TypedDict(
    "_OptionalTcpRouteTypeDef",
    {
        "timeout": TcpTimeoutTypeDef,
    },
    total=False,
)


class TcpRouteTypeDef(_RequiredTcpRouteTypeDef, _OptionalTcpRouteTypeDef):
    pass


_RequiredHttpGatewayRouteActionTypeDef = TypedDict(
    "_RequiredHttpGatewayRouteActionTypeDef",
    {
        "target": GatewayRouteTargetTypeDef,
    },
)
_OptionalHttpGatewayRouteActionTypeDef = TypedDict(
    "_OptionalHttpGatewayRouteActionTypeDef",
    {
        "rewrite": HttpGatewayRouteRewriteTypeDef,
    },
    total=False,
)


class HttpGatewayRouteActionTypeDef(
    _RequiredHttpGatewayRouteActionTypeDef, _OptionalHttpGatewayRouteActionTypeDef
):
    pass


VirtualRouterSpecTypeDef = TypedDict(
    "VirtualRouterSpecTypeDef",
    {
        "listeners": Sequence[VirtualRouterListenerTypeDef],
    },
    total=False,
)

_RequiredCreateMeshInputRequestTypeDef = TypedDict(
    "_RequiredCreateMeshInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalCreateMeshInputRequestTypeDef = TypedDict(
    "_OptionalCreateMeshInputRequestTypeDef",
    {
        "clientToken": str,
        "spec": MeshSpecTypeDef,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateMeshInputRequestTypeDef(
    _RequiredCreateMeshInputRequestTypeDef, _OptionalCreateMeshInputRequestTypeDef
):
    pass


MeshDataTypeDef = TypedDict(
    "MeshDataTypeDef",
    {
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "spec": MeshSpecTypeDef,
        "status": MeshStatusTypeDef,
    },
)

_RequiredUpdateMeshInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMeshInputRequestTypeDef",
    {
        "meshName": str,
    },
)
_OptionalUpdateMeshInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMeshInputRequestTypeDef",
    {
        "clientToken": str,
        "spec": MeshSpecTypeDef,
    },
    total=False,
)


class UpdateMeshInputRequestTypeDef(
    _RequiredUpdateMeshInputRequestTypeDef, _OptionalUpdateMeshInputRequestTypeDef
):
    pass


_RequiredListenerTlsValidationContextTypeDef = TypedDict(
    "_RequiredListenerTlsValidationContextTypeDef",
    {
        "trust": ListenerTlsValidationContextTrustTypeDef,
    },
)
_OptionalListenerTlsValidationContextTypeDef = TypedDict(
    "_OptionalListenerTlsValidationContextTypeDef",
    {
        "subjectAlternativeNames": SubjectAlternativeNamesTypeDef,
    },
    total=False,
)


class ListenerTlsValidationContextTypeDef(
    _RequiredListenerTlsValidationContextTypeDef, _OptionalListenerTlsValidationContextTypeDef
):
    pass


_RequiredTlsValidationContextTypeDef = TypedDict(
    "_RequiredTlsValidationContextTypeDef",
    {
        "trust": TlsValidationContextTrustTypeDef,
    },
)
_OptionalTlsValidationContextTypeDef = TypedDict(
    "_OptionalTlsValidationContextTypeDef",
    {
        "subjectAlternativeNames": SubjectAlternativeNamesTypeDef,
    },
    total=False,
)


class TlsValidationContextTypeDef(
    _RequiredTlsValidationContextTypeDef, _OptionalTlsValidationContextTypeDef
):
    pass


VirtualGatewayLoggingTypeDef = TypedDict(
    "VirtualGatewayLoggingTypeDef",
    {
        "accessLog": VirtualGatewayAccessLogTypeDef,
    },
    total=False,
)

_RequiredVirtualGatewayListenerTlsValidationContextTypeDef = TypedDict(
    "_RequiredVirtualGatewayListenerTlsValidationContextTypeDef",
    {
        "trust": VirtualGatewayListenerTlsValidationContextTrustTypeDef,
    },
)
_OptionalVirtualGatewayListenerTlsValidationContextTypeDef = TypedDict(
    "_OptionalVirtualGatewayListenerTlsValidationContextTypeDef",
    {
        "subjectAlternativeNames": SubjectAlternativeNamesTypeDef,
    },
    total=False,
)


class VirtualGatewayListenerTlsValidationContextTypeDef(
    _RequiredVirtualGatewayListenerTlsValidationContextTypeDef,
    _OptionalVirtualGatewayListenerTlsValidationContextTypeDef,
):
    pass


_RequiredVirtualGatewayTlsValidationContextTypeDef = TypedDict(
    "_RequiredVirtualGatewayTlsValidationContextTypeDef",
    {
        "trust": VirtualGatewayTlsValidationContextTrustTypeDef,
    },
)
_OptionalVirtualGatewayTlsValidationContextTypeDef = TypedDict(
    "_OptionalVirtualGatewayTlsValidationContextTypeDef",
    {
        "subjectAlternativeNames": SubjectAlternativeNamesTypeDef,
    },
    total=False,
)


class VirtualGatewayTlsValidationContextTypeDef(
    _RequiredVirtualGatewayTlsValidationContextTypeDef,
    _OptionalVirtualGatewayTlsValidationContextTypeDef,
):
    pass


VirtualServiceSpecTypeDef = TypedDict(
    "VirtualServiceSpecTypeDef",
    {
        "provider": VirtualServiceProviderTypeDef,
    },
    total=False,
)

GrpcGatewayRouteMatchTypeDef = TypedDict(
    "GrpcGatewayRouteMatchTypeDef",
    {
        "hostname": GatewayRouteHostnameMatchTypeDef,
        "metadata": Sequence[GrpcGatewayRouteMetadataTypeDef],
        "serviceName": str,
    },
    total=False,
)

GrpcRouteMatchTypeDef = TypedDict(
    "GrpcRouteMatchTypeDef",
    {
        "metadata": Sequence[GrpcRouteMetadataTypeDef],
        "methodName": str,
        "serviceName": str,
    },
    total=False,
)

HttpGatewayRouteMatchTypeDef = TypedDict(
    "HttpGatewayRouteMatchTypeDef",
    {
        "headers": Sequence[HttpGatewayRouteHeaderTypeDef],
        "hostname": GatewayRouteHostnameMatchTypeDef,
        "method": HttpMethodType,
        "path": HttpPathMatchTypeDef,
        "prefix": str,
        "queryParameters": Sequence[HttpQueryParameterTypeDef],
    },
    total=False,
)

HttpRouteMatchTypeDef = TypedDict(
    "HttpRouteMatchTypeDef",
    {
        "headers": Sequence[HttpRouteHeaderTypeDef],
        "method": HttpMethodType,
        "path": HttpPathMatchTypeDef,
        "prefix": str,
        "queryParameters": Sequence[HttpQueryParameterTypeDef],
        "scheme": HttpSchemeType,
    },
    total=False,
)

_RequiredCreateVirtualRouterInputRequestTypeDef = TypedDict(
    "_RequiredCreateVirtualRouterInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualRouterSpecTypeDef,
        "virtualRouterName": str,
    },
)
_OptionalCreateVirtualRouterInputRequestTypeDef = TypedDict(
    "_OptionalCreateVirtualRouterInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateVirtualRouterInputRequestTypeDef(
    _RequiredCreateVirtualRouterInputRequestTypeDef, _OptionalCreateVirtualRouterInputRequestTypeDef
):
    pass


_RequiredUpdateVirtualRouterInputRequestTypeDef = TypedDict(
    "_RequiredUpdateVirtualRouterInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualRouterSpecTypeDef,
        "virtualRouterName": str,
    },
)
_OptionalUpdateVirtualRouterInputRequestTypeDef = TypedDict(
    "_OptionalUpdateVirtualRouterInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
    },
    total=False,
)


class UpdateVirtualRouterInputRequestTypeDef(
    _RequiredUpdateVirtualRouterInputRequestTypeDef, _OptionalUpdateVirtualRouterInputRequestTypeDef
):
    pass


VirtualRouterDataTypeDef = TypedDict(
    "VirtualRouterDataTypeDef",
    {
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "spec": VirtualRouterSpecTypeDef,
        "status": VirtualRouterStatusTypeDef,
        "virtualRouterName": str,
    },
)

CreateMeshOutputTypeDef = TypedDict(
    "CreateMeshOutputTypeDef",
    {
        "mesh": MeshDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMeshOutputTypeDef = TypedDict(
    "DeleteMeshOutputTypeDef",
    {
        "mesh": MeshDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMeshOutputTypeDef = TypedDict(
    "DescribeMeshOutputTypeDef",
    {
        "mesh": MeshDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMeshOutputTypeDef = TypedDict(
    "UpdateMeshOutputTypeDef",
    {
        "mesh": MeshDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListenerTlsTypeDef = TypedDict(
    "_RequiredListenerTlsTypeDef",
    {
        "certificate": ListenerTlsCertificateTypeDef,
        "mode": ListenerTlsModeType,
    },
)
_OptionalListenerTlsTypeDef = TypedDict(
    "_OptionalListenerTlsTypeDef",
    {
        "validation": ListenerTlsValidationContextTypeDef,
    },
    total=False,
)


class ListenerTlsTypeDef(_RequiredListenerTlsTypeDef, _OptionalListenerTlsTypeDef):
    pass


_RequiredClientPolicyTlsTypeDef = TypedDict(
    "_RequiredClientPolicyTlsTypeDef",
    {
        "validation": TlsValidationContextTypeDef,
    },
)
_OptionalClientPolicyTlsTypeDef = TypedDict(
    "_OptionalClientPolicyTlsTypeDef",
    {
        "certificate": ClientTlsCertificateTypeDef,
        "enforce": bool,
        "ports": Sequence[int],
    },
    total=False,
)


class ClientPolicyTlsTypeDef(_RequiredClientPolicyTlsTypeDef, _OptionalClientPolicyTlsTypeDef):
    pass


_RequiredVirtualGatewayListenerTlsTypeDef = TypedDict(
    "_RequiredVirtualGatewayListenerTlsTypeDef",
    {
        "certificate": VirtualGatewayListenerTlsCertificateTypeDef,
        "mode": VirtualGatewayListenerTlsModeType,
    },
)
_OptionalVirtualGatewayListenerTlsTypeDef = TypedDict(
    "_OptionalVirtualGatewayListenerTlsTypeDef",
    {
        "validation": VirtualGatewayListenerTlsValidationContextTypeDef,
    },
    total=False,
)


class VirtualGatewayListenerTlsTypeDef(
    _RequiredVirtualGatewayListenerTlsTypeDef, _OptionalVirtualGatewayListenerTlsTypeDef
):
    pass


_RequiredVirtualGatewayClientPolicyTlsTypeDef = TypedDict(
    "_RequiredVirtualGatewayClientPolicyTlsTypeDef",
    {
        "validation": VirtualGatewayTlsValidationContextTypeDef,
    },
)
_OptionalVirtualGatewayClientPolicyTlsTypeDef = TypedDict(
    "_OptionalVirtualGatewayClientPolicyTlsTypeDef",
    {
        "certificate": VirtualGatewayClientTlsCertificateTypeDef,
        "enforce": bool,
        "ports": Sequence[int],
    },
    total=False,
)


class VirtualGatewayClientPolicyTlsTypeDef(
    _RequiredVirtualGatewayClientPolicyTlsTypeDef, _OptionalVirtualGatewayClientPolicyTlsTypeDef
):
    pass


_RequiredCreateVirtualServiceInputRequestTypeDef = TypedDict(
    "_RequiredCreateVirtualServiceInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualServiceSpecTypeDef,
        "virtualServiceName": str,
    },
)
_OptionalCreateVirtualServiceInputRequestTypeDef = TypedDict(
    "_OptionalCreateVirtualServiceInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateVirtualServiceInputRequestTypeDef(
    _RequiredCreateVirtualServiceInputRequestTypeDef,
    _OptionalCreateVirtualServiceInputRequestTypeDef,
):
    pass


_RequiredUpdateVirtualServiceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateVirtualServiceInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualServiceSpecTypeDef,
        "virtualServiceName": str,
    },
)
_OptionalUpdateVirtualServiceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateVirtualServiceInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
    },
    total=False,
)


class UpdateVirtualServiceInputRequestTypeDef(
    _RequiredUpdateVirtualServiceInputRequestTypeDef,
    _OptionalUpdateVirtualServiceInputRequestTypeDef,
):
    pass


VirtualServiceDataTypeDef = TypedDict(
    "VirtualServiceDataTypeDef",
    {
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "spec": VirtualServiceSpecTypeDef,
        "status": VirtualServiceStatusTypeDef,
        "virtualServiceName": str,
    },
)

GrpcGatewayRouteTypeDef = TypedDict(
    "GrpcGatewayRouteTypeDef",
    {
        "action": GrpcGatewayRouteActionTypeDef,
        "match": GrpcGatewayRouteMatchTypeDef,
    },
)

_RequiredGrpcRouteTypeDef = TypedDict(
    "_RequiredGrpcRouteTypeDef",
    {
        "action": GrpcRouteActionTypeDef,
        "match": GrpcRouteMatchTypeDef,
    },
)
_OptionalGrpcRouteTypeDef = TypedDict(
    "_OptionalGrpcRouteTypeDef",
    {
        "retryPolicy": GrpcRetryPolicyTypeDef,
        "timeout": GrpcTimeoutTypeDef,
    },
    total=False,
)


class GrpcRouteTypeDef(_RequiredGrpcRouteTypeDef, _OptionalGrpcRouteTypeDef):
    pass


HttpGatewayRouteTypeDef = TypedDict(
    "HttpGatewayRouteTypeDef",
    {
        "action": HttpGatewayRouteActionTypeDef,
        "match": HttpGatewayRouteMatchTypeDef,
    },
)

_RequiredHttpRouteTypeDef = TypedDict(
    "_RequiredHttpRouteTypeDef",
    {
        "action": HttpRouteActionTypeDef,
        "match": HttpRouteMatchTypeDef,
    },
)
_OptionalHttpRouteTypeDef = TypedDict(
    "_OptionalHttpRouteTypeDef",
    {
        "retryPolicy": HttpRetryPolicyTypeDef,
        "timeout": HttpTimeoutTypeDef,
    },
    total=False,
)


class HttpRouteTypeDef(_RequiredHttpRouteTypeDef, _OptionalHttpRouteTypeDef):
    pass


CreateVirtualRouterOutputTypeDef = TypedDict(
    "CreateVirtualRouterOutputTypeDef",
    {
        "virtualRouter": VirtualRouterDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVirtualRouterOutputTypeDef = TypedDict(
    "DeleteVirtualRouterOutputTypeDef",
    {
        "virtualRouter": VirtualRouterDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVirtualRouterOutputTypeDef = TypedDict(
    "DescribeVirtualRouterOutputTypeDef",
    {
        "virtualRouter": VirtualRouterDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVirtualRouterOutputTypeDef = TypedDict(
    "UpdateVirtualRouterOutputTypeDef",
    {
        "virtualRouter": VirtualRouterDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListenerTypeDef = TypedDict(
    "_RequiredListenerTypeDef",
    {
        "portMapping": PortMappingTypeDef,
    },
)
_OptionalListenerTypeDef = TypedDict(
    "_OptionalListenerTypeDef",
    {
        "connectionPool": VirtualNodeConnectionPoolTypeDef,
        "healthCheck": HealthCheckPolicyTypeDef,
        "outlierDetection": OutlierDetectionTypeDef,
        "timeout": ListenerTimeoutTypeDef,
        "tls": ListenerTlsTypeDef,
    },
    total=False,
)


class ListenerTypeDef(_RequiredListenerTypeDef, _OptionalListenerTypeDef):
    pass


ClientPolicyTypeDef = TypedDict(
    "ClientPolicyTypeDef",
    {
        "tls": ClientPolicyTlsTypeDef,
    },
    total=False,
)

_RequiredVirtualGatewayListenerTypeDef = TypedDict(
    "_RequiredVirtualGatewayListenerTypeDef",
    {
        "portMapping": VirtualGatewayPortMappingTypeDef,
    },
)
_OptionalVirtualGatewayListenerTypeDef = TypedDict(
    "_OptionalVirtualGatewayListenerTypeDef",
    {
        "connectionPool": VirtualGatewayConnectionPoolTypeDef,
        "healthCheck": VirtualGatewayHealthCheckPolicyTypeDef,
        "tls": VirtualGatewayListenerTlsTypeDef,
    },
    total=False,
)


class VirtualGatewayListenerTypeDef(
    _RequiredVirtualGatewayListenerTypeDef, _OptionalVirtualGatewayListenerTypeDef
):
    pass


VirtualGatewayClientPolicyTypeDef = TypedDict(
    "VirtualGatewayClientPolicyTypeDef",
    {
        "tls": VirtualGatewayClientPolicyTlsTypeDef,
    },
    total=False,
)

CreateVirtualServiceOutputTypeDef = TypedDict(
    "CreateVirtualServiceOutputTypeDef",
    {
        "virtualService": VirtualServiceDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVirtualServiceOutputTypeDef = TypedDict(
    "DeleteVirtualServiceOutputTypeDef",
    {
        "virtualService": VirtualServiceDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVirtualServiceOutputTypeDef = TypedDict(
    "DescribeVirtualServiceOutputTypeDef",
    {
        "virtualService": VirtualServiceDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVirtualServiceOutputTypeDef = TypedDict(
    "UpdateVirtualServiceOutputTypeDef",
    {
        "virtualService": VirtualServiceDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GatewayRouteSpecTypeDef = TypedDict(
    "GatewayRouteSpecTypeDef",
    {
        "grpcRoute": GrpcGatewayRouteTypeDef,
        "http2Route": HttpGatewayRouteTypeDef,
        "httpRoute": HttpGatewayRouteTypeDef,
        "priority": int,
    },
    total=False,
)

RouteSpecTypeDef = TypedDict(
    "RouteSpecTypeDef",
    {
        "grpcRoute": GrpcRouteTypeDef,
        "http2Route": HttpRouteTypeDef,
        "httpRoute": HttpRouteTypeDef,
        "priority": int,
        "tcpRoute": TcpRouteTypeDef,
    },
    total=False,
)

BackendDefaultsTypeDef = TypedDict(
    "BackendDefaultsTypeDef",
    {
        "clientPolicy": ClientPolicyTypeDef,
    },
    total=False,
)

_RequiredVirtualServiceBackendTypeDef = TypedDict(
    "_RequiredVirtualServiceBackendTypeDef",
    {
        "virtualServiceName": str,
    },
)
_OptionalVirtualServiceBackendTypeDef = TypedDict(
    "_OptionalVirtualServiceBackendTypeDef",
    {
        "clientPolicy": ClientPolicyTypeDef,
    },
    total=False,
)


class VirtualServiceBackendTypeDef(
    _RequiredVirtualServiceBackendTypeDef, _OptionalVirtualServiceBackendTypeDef
):
    pass


VirtualGatewayBackendDefaultsTypeDef = TypedDict(
    "VirtualGatewayBackendDefaultsTypeDef",
    {
        "clientPolicy": VirtualGatewayClientPolicyTypeDef,
    },
    total=False,
)

_RequiredCreateGatewayRouteInputRequestTypeDef = TypedDict(
    "_RequiredCreateGatewayRouteInputRequestTypeDef",
    {
        "gatewayRouteName": str,
        "meshName": str,
        "spec": GatewayRouteSpecTypeDef,
        "virtualGatewayName": str,
    },
)
_OptionalCreateGatewayRouteInputRequestTypeDef = TypedDict(
    "_OptionalCreateGatewayRouteInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateGatewayRouteInputRequestTypeDef(
    _RequiredCreateGatewayRouteInputRequestTypeDef, _OptionalCreateGatewayRouteInputRequestTypeDef
):
    pass


GatewayRouteDataTypeDef = TypedDict(
    "GatewayRouteDataTypeDef",
    {
        "gatewayRouteName": str,
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "spec": GatewayRouteSpecTypeDef,
        "status": GatewayRouteStatusTypeDef,
        "virtualGatewayName": str,
    },
)

_RequiredUpdateGatewayRouteInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayRouteInputRequestTypeDef",
    {
        "gatewayRouteName": str,
        "meshName": str,
        "spec": GatewayRouteSpecTypeDef,
        "virtualGatewayName": str,
    },
)
_OptionalUpdateGatewayRouteInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayRouteInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
    },
    total=False,
)


class UpdateGatewayRouteInputRequestTypeDef(
    _RequiredUpdateGatewayRouteInputRequestTypeDef, _OptionalUpdateGatewayRouteInputRequestTypeDef
):
    pass


_RequiredCreateRouteInputRequestTypeDef = TypedDict(
    "_RequiredCreateRouteInputRequestTypeDef",
    {
        "meshName": str,
        "routeName": str,
        "spec": RouteSpecTypeDef,
        "virtualRouterName": str,
    },
)
_OptionalCreateRouteInputRequestTypeDef = TypedDict(
    "_OptionalCreateRouteInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateRouteInputRequestTypeDef(
    _RequiredCreateRouteInputRequestTypeDef, _OptionalCreateRouteInputRequestTypeDef
):
    pass


RouteDataTypeDef = TypedDict(
    "RouteDataTypeDef",
    {
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "routeName": str,
        "spec": RouteSpecTypeDef,
        "status": RouteStatusTypeDef,
        "virtualRouterName": str,
    },
)

_RequiredUpdateRouteInputRequestTypeDef = TypedDict(
    "_RequiredUpdateRouteInputRequestTypeDef",
    {
        "meshName": str,
        "routeName": str,
        "spec": RouteSpecTypeDef,
        "virtualRouterName": str,
    },
)
_OptionalUpdateRouteInputRequestTypeDef = TypedDict(
    "_OptionalUpdateRouteInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
    },
    total=False,
)


class UpdateRouteInputRequestTypeDef(
    _RequiredUpdateRouteInputRequestTypeDef, _OptionalUpdateRouteInputRequestTypeDef
):
    pass


BackendTypeDef = TypedDict(
    "BackendTypeDef",
    {
        "virtualService": VirtualServiceBackendTypeDef,
    },
    total=False,
)

_RequiredVirtualGatewaySpecTypeDef = TypedDict(
    "_RequiredVirtualGatewaySpecTypeDef",
    {
        "listeners": Sequence[VirtualGatewayListenerTypeDef],
    },
)
_OptionalVirtualGatewaySpecTypeDef = TypedDict(
    "_OptionalVirtualGatewaySpecTypeDef",
    {
        "backendDefaults": VirtualGatewayBackendDefaultsTypeDef,
        "logging": VirtualGatewayLoggingTypeDef,
    },
    total=False,
)


class VirtualGatewaySpecTypeDef(
    _RequiredVirtualGatewaySpecTypeDef, _OptionalVirtualGatewaySpecTypeDef
):
    pass


CreateGatewayRouteOutputTypeDef = TypedDict(
    "CreateGatewayRouteOutputTypeDef",
    {
        "gatewayRoute": GatewayRouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGatewayRouteOutputTypeDef = TypedDict(
    "DeleteGatewayRouteOutputTypeDef",
    {
        "gatewayRoute": GatewayRouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGatewayRouteOutputTypeDef = TypedDict(
    "DescribeGatewayRouteOutputTypeDef",
    {
        "gatewayRoute": GatewayRouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewayRouteOutputTypeDef = TypedDict(
    "UpdateGatewayRouteOutputTypeDef",
    {
        "gatewayRoute": GatewayRouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRouteOutputTypeDef = TypedDict(
    "CreateRouteOutputTypeDef",
    {
        "route": RouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRouteOutputTypeDef = TypedDict(
    "DeleteRouteOutputTypeDef",
    {
        "route": RouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRouteOutputTypeDef = TypedDict(
    "DescribeRouteOutputTypeDef",
    {
        "route": RouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRouteOutputTypeDef = TypedDict(
    "UpdateRouteOutputTypeDef",
    {
        "route": RouteDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VirtualNodeSpecTypeDef = TypedDict(
    "VirtualNodeSpecTypeDef",
    {
        "backendDefaults": BackendDefaultsTypeDef,
        "backends": Sequence[BackendTypeDef],
        "listeners": Sequence[ListenerTypeDef],
        "logging": LoggingTypeDef,
        "serviceDiscovery": ServiceDiscoveryTypeDef,
    },
    total=False,
)

_RequiredCreateVirtualGatewayInputRequestTypeDef = TypedDict(
    "_RequiredCreateVirtualGatewayInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualGatewaySpecTypeDef,
        "virtualGatewayName": str,
    },
)
_OptionalCreateVirtualGatewayInputRequestTypeDef = TypedDict(
    "_OptionalCreateVirtualGatewayInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateVirtualGatewayInputRequestTypeDef(
    _RequiredCreateVirtualGatewayInputRequestTypeDef,
    _OptionalCreateVirtualGatewayInputRequestTypeDef,
):
    pass


_RequiredUpdateVirtualGatewayInputRequestTypeDef = TypedDict(
    "_RequiredUpdateVirtualGatewayInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualGatewaySpecTypeDef,
        "virtualGatewayName": str,
    },
)
_OptionalUpdateVirtualGatewayInputRequestTypeDef = TypedDict(
    "_OptionalUpdateVirtualGatewayInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
    },
    total=False,
)


class UpdateVirtualGatewayInputRequestTypeDef(
    _RequiredUpdateVirtualGatewayInputRequestTypeDef,
    _OptionalUpdateVirtualGatewayInputRequestTypeDef,
):
    pass


VirtualGatewayDataTypeDef = TypedDict(
    "VirtualGatewayDataTypeDef",
    {
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "spec": VirtualGatewaySpecTypeDef,
        "status": VirtualGatewayStatusTypeDef,
        "virtualGatewayName": str,
    },
)

_RequiredCreateVirtualNodeInputRequestTypeDef = TypedDict(
    "_RequiredCreateVirtualNodeInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualNodeSpecTypeDef,
        "virtualNodeName": str,
    },
)
_OptionalCreateVirtualNodeInputRequestTypeDef = TypedDict(
    "_OptionalCreateVirtualNodeInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
        "tags": Sequence[TagRefTypeDef],
    },
    total=False,
)


class CreateVirtualNodeInputRequestTypeDef(
    _RequiredCreateVirtualNodeInputRequestTypeDef, _OptionalCreateVirtualNodeInputRequestTypeDef
):
    pass


_RequiredUpdateVirtualNodeInputRequestTypeDef = TypedDict(
    "_RequiredUpdateVirtualNodeInputRequestTypeDef",
    {
        "meshName": str,
        "spec": VirtualNodeSpecTypeDef,
        "virtualNodeName": str,
    },
)
_OptionalUpdateVirtualNodeInputRequestTypeDef = TypedDict(
    "_OptionalUpdateVirtualNodeInputRequestTypeDef",
    {
        "clientToken": str,
        "meshOwner": str,
    },
    total=False,
)


class UpdateVirtualNodeInputRequestTypeDef(
    _RequiredUpdateVirtualNodeInputRequestTypeDef, _OptionalUpdateVirtualNodeInputRequestTypeDef
):
    pass


VirtualNodeDataTypeDef = TypedDict(
    "VirtualNodeDataTypeDef",
    {
        "meshName": str,
        "metadata": ResourceMetadataTypeDef,
        "spec": VirtualNodeSpecTypeDef,
        "status": VirtualNodeStatusTypeDef,
        "virtualNodeName": str,
    },
)

CreateVirtualGatewayOutputTypeDef = TypedDict(
    "CreateVirtualGatewayOutputTypeDef",
    {
        "virtualGateway": VirtualGatewayDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVirtualGatewayOutputTypeDef = TypedDict(
    "DeleteVirtualGatewayOutputTypeDef",
    {
        "virtualGateway": VirtualGatewayDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVirtualGatewayOutputTypeDef = TypedDict(
    "DescribeVirtualGatewayOutputTypeDef",
    {
        "virtualGateway": VirtualGatewayDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVirtualGatewayOutputTypeDef = TypedDict(
    "UpdateVirtualGatewayOutputTypeDef",
    {
        "virtualGateway": VirtualGatewayDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVirtualNodeOutputTypeDef = TypedDict(
    "CreateVirtualNodeOutputTypeDef",
    {
        "virtualNode": VirtualNodeDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVirtualNodeOutputTypeDef = TypedDict(
    "DeleteVirtualNodeOutputTypeDef",
    {
        "virtualNode": VirtualNodeDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVirtualNodeOutputTypeDef = TypedDict(
    "DescribeVirtualNodeOutputTypeDef",
    {
        "virtualNode": VirtualNodeDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVirtualNodeOutputTypeDef = TypedDict(
    "UpdateVirtualNodeOutputTypeDef",
    {
        "virtualNode": VirtualNodeDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
