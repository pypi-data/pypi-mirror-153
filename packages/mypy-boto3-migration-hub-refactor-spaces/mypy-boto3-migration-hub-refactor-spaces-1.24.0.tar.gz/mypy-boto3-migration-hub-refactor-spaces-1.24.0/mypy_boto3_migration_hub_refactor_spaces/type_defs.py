"""
Type annotations for migration-hub-refactor-spaces service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/type_defs/)

Usage::

    ```python
    from mypy_boto3_migration_hub_refactor_spaces.type_defs import ApiGatewayProxyConfigTypeDef

    data: ApiGatewayProxyConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ApiGatewayEndpointTypeType,
    ApplicationStateType,
    EnvironmentStateType,
    ErrorCodeType,
    ErrorResourceTypeType,
    HttpMethodType,
    RouteStateType,
    RouteTypeType,
    ServiceEndpointTypeType,
    ServiceStateType,
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
    "ApiGatewayProxyConfigTypeDef",
    "ApiGatewayProxyInputTypeDef",
    "ApiGatewayProxySummaryTypeDef",
    "ErrorResponseTypeDef",
    "ResponseMetadataTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "UriPathRouteInputTypeDef",
    "LambdaEndpointInputTypeDef",
    "UrlEndpointInputTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRouteRequestRequestTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "EnvironmentVpcTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetRouteRequestRequestTypeDef",
    "GetServiceRequestRequestTypeDef",
    "LambdaEndpointConfigTypeDef",
    "UrlEndpointConfigTypeDef",
    "LambdaEndpointSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListEnvironmentVpcsRequestRequestTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListRoutesRequestRequestTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "UrlEndpointSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ApplicationSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "RouteSummaryTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "DeleteApplicationResponseTypeDef",
    "DeleteEnvironmentResponseTypeDef",
    "DeleteRouteResponseTypeDef",
    "DeleteServiceResponseTypeDef",
    "GetApplicationResponseTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetRouteResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateRouteRequestRequestTypeDef",
    "CreateRouteResponseTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "ListEnvironmentVpcsResponseTypeDef",
    "GetServiceResponseTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef",
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    "ListRoutesRequestListRoutesPaginateTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ServiceSummaryTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListRoutesResponseTypeDef",
    "ListServicesResponseTypeDef",
)

ApiGatewayProxyConfigTypeDef = TypedDict(
    "ApiGatewayProxyConfigTypeDef",
    {
        "ApiGatewayId": str,
        "EndpointType": ApiGatewayEndpointTypeType,
        "NlbArn": str,
        "NlbName": str,
        "ProxyUrl": str,
        "StageName": str,
        "VpcLinkId": str,
    },
    total=False,
)

ApiGatewayProxyInputTypeDef = TypedDict(
    "ApiGatewayProxyInputTypeDef",
    {
        "EndpointType": ApiGatewayEndpointTypeType,
        "StageName": str,
    },
    total=False,
)

ApiGatewayProxySummaryTypeDef = TypedDict(
    "ApiGatewayProxySummaryTypeDef",
    {
        "ApiGatewayId": str,
        "EndpointType": ApiGatewayEndpointTypeType,
        "NlbArn": str,
        "NlbName": str,
        "ProxyUrl": str,
        "StageName": str,
        "VpcLinkId": str,
    },
    total=False,
)

ErrorResponseTypeDef = TypedDict(
    "ErrorResponseTypeDef",
    {
        "AccountId": str,
        "AdditionalDetails": Dict[str, str],
        "Code": ErrorCodeType,
        "Message": str,
        "ResourceIdentifier": str,
        "ResourceType": ErrorResourceTypeType,
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

_RequiredCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentRequestRequestTypeDef",
    {
        "Name": str,
        "NetworkFabricType": Literal["TRANSIT_GATEWAY"],
    },
)
_OptionalCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateEnvironmentRequestRequestTypeDef(
    _RequiredCreateEnvironmentRequestRequestTypeDef, _OptionalCreateEnvironmentRequestRequestTypeDef
):
    pass


_RequiredUriPathRouteInputTypeDef = TypedDict(
    "_RequiredUriPathRouteInputTypeDef",
    {
        "ActivationState": Literal["ACTIVE"],
        "SourcePath": str,
    },
)
_OptionalUriPathRouteInputTypeDef = TypedDict(
    "_OptionalUriPathRouteInputTypeDef",
    {
        "IncludeChildPaths": bool,
        "Methods": Sequence[HttpMethodType],
    },
    total=False,
)


class UriPathRouteInputTypeDef(
    _RequiredUriPathRouteInputTypeDef, _OptionalUriPathRouteInputTypeDef
):
    pass


LambdaEndpointInputTypeDef = TypedDict(
    "LambdaEndpointInputTypeDef",
    {
        "Arn": str,
    },
)

_RequiredUrlEndpointInputTypeDef = TypedDict(
    "_RequiredUrlEndpointInputTypeDef",
    {
        "Url": str,
    },
)
_OptionalUrlEndpointInputTypeDef = TypedDict(
    "_OptionalUrlEndpointInputTypeDef",
    {
        "HealthUrl": str,
    },
    total=False,
)


class UrlEndpointInputTypeDef(_RequiredUrlEndpointInputTypeDef, _OptionalUrlEndpointInputTypeDef):
    pass


DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "EnvironmentIdentifier": str,
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

DeleteRouteRequestRequestTypeDef = TypedDict(
    "DeleteRouteRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
        "RouteIdentifier": str,
    },
)

DeleteServiceRequestRequestTypeDef = TypedDict(
    "DeleteServiceRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
        "ServiceIdentifier": str,
    },
)

EnvironmentVpcTypeDef = TypedDict(
    "EnvironmentVpcTypeDef",
    {
        "AccountId": str,
        "CidrBlocks": List[str],
        "CreatedTime": datetime,
        "EnvironmentId": str,
        "LastUpdatedTime": datetime,
        "VpcId": str,
        "VpcName": str,
    },
    total=False,
)

GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "EnvironmentIdentifier": str,
    },
)

GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetRouteRequestRequestTypeDef = TypedDict(
    "GetRouteRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
        "RouteIdentifier": str,
    },
)

GetServiceRequestRequestTypeDef = TypedDict(
    "GetServiceRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
        "ServiceIdentifier": str,
    },
)

LambdaEndpointConfigTypeDef = TypedDict(
    "LambdaEndpointConfigTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

UrlEndpointConfigTypeDef = TypedDict(
    "UrlEndpointConfigTypeDef",
    {
        "HealthUrl": str,
        "Url": str,
    },
    total=False,
)

LambdaEndpointSummaryTypeDef = TypedDict(
    "LambdaEndpointSummaryTypeDef",
    {
        "Arn": str,
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

_RequiredListApplicationsRequestRequestTypeDef = TypedDict(
    "_RequiredListApplicationsRequestRequestTypeDef",
    {
        "EnvironmentIdentifier": str,
    },
)
_OptionalListApplicationsRequestRequestTypeDef = TypedDict(
    "_OptionalListApplicationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListApplicationsRequestRequestTypeDef(
    _RequiredListApplicationsRequestRequestTypeDef, _OptionalListApplicationsRequestRequestTypeDef
):
    pass


_RequiredListEnvironmentVpcsRequestRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentVpcsRequestRequestTypeDef",
    {
        "EnvironmentIdentifier": str,
    },
)
_OptionalListEnvironmentVpcsRequestRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentVpcsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListEnvironmentVpcsRequestRequestTypeDef(
    _RequiredListEnvironmentVpcsRequestRequestTypeDef,
    _OptionalListEnvironmentVpcsRequestRequestTypeDef,
):
    pass


ListEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListEnvironmentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListRoutesRequestRequestTypeDef = TypedDict(
    "_RequiredListRoutesRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)
_OptionalListRoutesRequestRequestTypeDef = TypedDict(
    "_OptionalListRoutesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListRoutesRequestRequestTypeDef(
    _RequiredListRoutesRequestRequestTypeDef, _OptionalListRoutesRequestRequestTypeDef
):
    pass


_RequiredListServicesRequestRequestTypeDef = TypedDict(
    "_RequiredListServicesRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)
_OptionalListServicesRequestRequestTypeDef = TypedDict(
    "_OptionalListServicesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListServicesRequestRequestTypeDef(
    _RequiredListServicesRequestRequestTypeDef, _OptionalListServicesRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "Policy": str,
        "ResourceArn": str,
    },
)

UrlEndpointSummaryTypeDef = TypedDict(
    "UrlEndpointSummaryTypeDef",
    {
        "HealthUrl": str,
        "Url": str,
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

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "EnvironmentIdentifier": str,
        "Name": str,
        "ProxyType": Literal["API_GATEWAY"],
        "VpcId": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "ApiGatewayProxy": ApiGatewayProxyInputTypeDef,
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "ApiGatewayProxy": ApiGatewayProxySummaryTypeDef,
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "OwnerAccountId": str,
        "ProxyType": Literal["API_GATEWAY"],
        "State": ApplicationStateType,
        "Tags": Dict[str, str],
        "VpcId": str,
    },
    total=False,
)

EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "Description": str,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "NetworkFabricType": Literal["TRANSIT_GATEWAY"],
        "OwnerAccountId": str,
        "State": EnvironmentStateType,
        "Tags": Dict[str, str],
        "TransitGatewayId": str,
    },
    total=False,
)

RouteSummaryTypeDef = TypedDict(
    "RouteSummaryTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "IncludeChildPaths": bool,
        "LastUpdatedTime": datetime,
        "Methods": List[HttpMethodType],
        "OwnerAccountId": str,
        "PathResourceToId": Dict[str, str],
        "RouteId": str,
        "RouteType": RouteTypeType,
        "ServiceId": str,
        "SourcePath": str,
        "State": RouteStateType,
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "ApiGatewayProxy": ApiGatewayProxyInputTypeDef,
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "EnvironmentId": str,
        "LastUpdatedTime": datetime,
        "Name": str,
        "OwnerAccountId": str,
        "ProxyType": Literal["API_GATEWAY"],
        "State": ApplicationStateType,
        "Tags": Dict[str, str],
        "VpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentResponseTypeDef = TypedDict(
    "CreateEnvironmentResponseTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "Description": str,
        "EnvironmentId": str,
        "LastUpdatedTime": datetime,
        "Name": str,
        "NetworkFabricType": Literal["TRANSIT_GATEWAY"],
        "OwnerAccountId": str,
        "State": EnvironmentStateType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApplicationResponseTypeDef = TypedDict(
    "DeleteApplicationResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "EnvironmentId": str,
        "LastUpdatedTime": datetime,
        "Name": str,
        "State": ApplicationStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEnvironmentResponseTypeDef = TypedDict(
    "DeleteEnvironmentResponseTypeDef",
    {
        "Arn": str,
        "EnvironmentId": str,
        "LastUpdatedTime": datetime,
        "Name": str,
        "State": EnvironmentStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRouteResponseTypeDef = TypedDict(
    "DeleteRouteResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "LastUpdatedTime": datetime,
        "RouteId": str,
        "ServiceId": str,
        "State": RouteStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceResponseTypeDef = TypedDict(
    "DeleteServiceResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "EnvironmentId": str,
        "LastUpdatedTime": datetime,
        "Name": str,
        "ServiceId": str,
        "State": ServiceStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "ApiGatewayProxy": ApiGatewayProxyConfigTypeDef,
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "OwnerAccountId": str,
        "ProxyType": Literal["API_GATEWAY"],
        "State": ApplicationStateType,
        "Tags": Dict[str, str],
        "VpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnvironmentResponseTypeDef = TypedDict(
    "GetEnvironmentResponseTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "Description": str,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "NetworkFabricType": Literal["TRANSIT_GATEWAY"],
        "OwnerAccountId": str,
        "State": EnvironmentStateType,
        "Tags": Dict[str, str],
        "TransitGatewayId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRouteResponseTypeDef = TypedDict(
    "GetRouteResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "IncludeChildPaths": bool,
        "LastUpdatedTime": datetime,
        "Methods": List[HttpMethodType],
        "OwnerAccountId": str,
        "PathResourceToId": Dict[str, str],
        "RouteId": str,
        "RouteType": RouteTypeType,
        "ServiceId": str,
        "SourcePath": str,
        "State": RouteStateType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateRouteRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRouteRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
        "RouteType": RouteTypeType,
        "ServiceIdentifier": str,
    },
)
_OptionalCreateRouteRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRouteRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
        "UriPathRoute": UriPathRouteInputTypeDef,
    },
    total=False,
)


class CreateRouteRequestRequestTypeDef(
    _RequiredCreateRouteRequestRequestTypeDef, _OptionalCreateRouteRequestRequestTypeDef
):
    pass


CreateRouteResponseTypeDef = TypedDict(
    "CreateRouteResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "OwnerAccountId": str,
        "RouteId": str,
        "RouteType": RouteTypeType,
        "ServiceId": str,
        "State": RouteStateType,
        "Tags": Dict[str, str],
        "UriPathRoute": UriPathRouteInputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateServiceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EndpointType": ServiceEndpointTypeType,
        "EnvironmentIdentifier": str,
        "Name": str,
    },
)
_OptionalCreateServiceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "LambdaEndpoint": LambdaEndpointInputTypeDef,
        "Tags": Mapping[str, str],
        "UrlEndpoint": UrlEndpointInputTypeDef,
        "VpcId": str,
    },
    total=False,
)


class CreateServiceRequestRequestTypeDef(
    _RequiredCreateServiceRequestRequestTypeDef, _OptionalCreateServiceRequestRequestTypeDef
):
    pass


CreateServiceResponseTypeDef = TypedDict(
    "CreateServiceResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "Description": str,
        "EndpointType": ServiceEndpointTypeType,
        "EnvironmentId": str,
        "LambdaEndpoint": LambdaEndpointInputTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "OwnerAccountId": str,
        "ServiceId": str,
        "State": ServiceStateType,
        "Tags": Dict[str, str],
        "UrlEndpoint": UrlEndpointInputTypeDef,
        "VpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentVpcsResponseTypeDef = TypedDict(
    "ListEnvironmentVpcsResponseTypeDef",
    {
        "EnvironmentVpcList": List[EnvironmentVpcTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceResponseTypeDef = TypedDict(
    "GetServiceResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "Description": str,
        "EndpointType": ServiceEndpointTypeType,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "LambdaEndpoint": LambdaEndpointConfigTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "OwnerAccountId": str,
        "ServiceId": str,
        "State": ServiceStateType,
        "Tags": Dict[str, str],
        "UrlEndpoint": UrlEndpointConfigTypeDef,
        "VpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "_RequiredListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "EnvironmentIdentifier": str,
    },
)
_OptionalListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "_OptionalListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListApplicationsRequestListApplicationsPaginateTypeDef(
    _RequiredListApplicationsRequestListApplicationsPaginateTypeDef,
    _OptionalListApplicationsRequestListApplicationsPaginateTypeDef,
):
    pass


_RequiredListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef",
    {
        "EnvironmentIdentifier": str,
    },
)
_OptionalListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef(
    _RequiredListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef,
    _OptionalListEnvironmentVpcsRequestListEnvironmentVpcsPaginateTypeDef,
):
    pass


ListEnvironmentsRequestListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRoutesRequestListRoutesPaginateTypeDef = TypedDict(
    "_RequiredListRoutesRequestListRoutesPaginateTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)
_OptionalListRoutesRequestListRoutesPaginateTypeDef = TypedDict(
    "_OptionalListRoutesRequestListRoutesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRoutesRequestListRoutesPaginateTypeDef(
    _RequiredListRoutesRequestListRoutesPaginateTypeDef,
    _OptionalListRoutesRequestListRoutesPaginateTypeDef,
):
    pass


_RequiredListServicesRequestListServicesPaginateTypeDef = TypedDict(
    "_RequiredListServicesRequestListServicesPaginateTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)
_OptionalListServicesRequestListServicesPaginateTypeDef = TypedDict(
    "_OptionalListServicesRequestListServicesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListServicesRequestListServicesPaginateTypeDef(
    _RequiredListServicesRequestListServicesPaginateTypeDef,
    _OptionalListServicesRequestListServicesPaginateTypeDef,
):
    pass


ServiceSummaryTypeDef = TypedDict(
    "ServiceSummaryTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreatedByAccountId": str,
        "CreatedTime": datetime,
        "Description": str,
        "EndpointType": ServiceEndpointTypeType,
        "EnvironmentId": str,
        "Error": ErrorResponseTypeDef,
        "LambdaEndpoint": LambdaEndpointSummaryTypeDef,
        "LastUpdatedTime": datetime,
        "Name": str,
        "OwnerAccountId": str,
        "ServiceId": str,
        "State": ServiceStateType,
        "Tags": Dict[str, str],
        "UrlEndpoint": UrlEndpointSummaryTypeDef,
        "VpcId": str,
    },
    total=False,
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "ApplicationSummaryList": List[ApplicationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsResponseTypeDef = TypedDict(
    "ListEnvironmentsResponseTypeDef",
    {
        "EnvironmentSummaryList": List[EnvironmentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoutesResponseTypeDef = TypedDict(
    "ListRoutesResponseTypeDef",
    {
        "NextToken": str,
        "RouteSummaryList": List[RouteSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicesResponseTypeDef = TypedDict(
    "ListServicesResponseTypeDef",
    {
        "NextToken": str,
        "ServiceSummaryList": List[ServiceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
