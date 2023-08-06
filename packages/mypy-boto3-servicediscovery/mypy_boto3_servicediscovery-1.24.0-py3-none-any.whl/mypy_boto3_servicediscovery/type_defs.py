"""
Type annotations for servicediscovery service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/type_defs/)

Usage::

    ```python
    from mypy_boto3_servicediscovery.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    CustomHealthStatusType,
    FilterConditionType,
    HealthCheckTypeType,
    HealthStatusFilterType,
    HealthStatusType,
    NamespaceTypeType,
    OperationFilterNameType,
    OperationStatusType,
    OperationTargetTypeType,
    OperationTypeType,
    RecordTypeType,
    RoutingPolicyType,
    ServiceTypeType,
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
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "HealthCheckConfigTypeDef",
    "HealthCheckCustomConfigTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeregisterInstanceRequestRequestTypeDef",
    "DiscoverInstancesRequestRequestTypeDef",
    "HttpInstanceSummaryTypeDef",
    "DnsRecordTypeDef",
    "SOATypeDef",
    "GetInstanceRequestRequestTypeDef",
    "InstanceTypeDef",
    "GetInstancesHealthStatusRequestRequestTypeDef",
    "GetNamespaceRequestRequestTypeDef",
    "GetOperationRequestRequestTypeDef",
    "OperationTypeDef",
    "GetServiceRequestRequestTypeDef",
    "HttpNamespaceChangeTypeDef",
    "HttpPropertiesTypeDef",
    "InstanceSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "NamespaceFilterTypeDef",
    "OperationFilterTypeDef",
    "OperationSummaryTypeDef",
    "ServiceFilterTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "SOAChangeTypeDef",
    "RegisterInstanceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateInstanceCustomHealthStatusRequestRequestTypeDef",
    "CreateHttpNamespaceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateHttpNamespaceResponseTypeDef",
    "CreatePrivateDnsNamespaceResponseTypeDef",
    "CreatePublicDnsNamespaceResponseTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeregisterInstanceResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetInstancesHealthStatusResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RegisterInstanceResponseTypeDef",
    "UpdateHttpNamespaceResponseTypeDef",
    "UpdatePrivateDnsNamespaceResponseTypeDef",
    "UpdatePublicDnsNamespaceResponseTypeDef",
    "UpdateServiceResponseTypeDef",
    "DiscoverInstancesResponseTypeDef",
    "DnsConfigChangeTypeDef",
    "DnsConfigTypeDef",
    "DnsPropertiesTypeDef",
    "PrivateDnsPropertiesMutableTypeDef",
    "PublicDnsPropertiesMutableTypeDef",
    "GetInstanceResponseTypeDef",
    "GetOperationResponseTypeDef",
    "UpdateHttpNamespaceRequestRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListOperationsRequestListOperationsPaginateTypeDef",
    "ListOperationsRequestRequestTypeDef",
    "ListOperationsResponseTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListServicesRequestRequestTypeDef",
    "PrivateDnsPropertiesMutableChangeTypeDef",
    "PublicDnsPropertiesMutableChangeTypeDef",
    "ServiceChangeTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceTypeDef",
    "NamespacePropertiesTypeDef",
    "PrivateDnsNamespacePropertiesTypeDef",
    "PublicDnsNamespacePropertiesTypeDef",
    "PrivateDnsNamespacePropertiesChangeTypeDef",
    "PublicDnsNamespacePropertiesChangeTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "CreateServiceResponseTypeDef",
    "GetServiceResponseTypeDef",
    "NamespaceSummaryTypeDef",
    "NamespaceTypeDef",
    "CreatePrivateDnsNamespaceRequestRequestTypeDef",
    "CreatePublicDnsNamespaceRequestRequestTypeDef",
    "PrivateDnsNamespaceChangeTypeDef",
    "PublicDnsNamespaceChangeTypeDef",
    "ListNamespacesResponseTypeDef",
    "GetNamespaceResponseTypeDef",
    "UpdatePrivateDnsNamespaceRequestRequestTypeDef",
    "UpdatePublicDnsNamespaceRequestRequestTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

_RequiredHealthCheckConfigTypeDef = TypedDict(
    "_RequiredHealthCheckConfigTypeDef",
    {
        "Type": HealthCheckTypeType,
    },
)
_OptionalHealthCheckConfigTypeDef = TypedDict(
    "_OptionalHealthCheckConfigTypeDef",
    {
        "ResourcePath": str,
        "FailureThreshold": int,
    },
    total=False,
)


class HealthCheckConfigTypeDef(
    _RequiredHealthCheckConfigTypeDef, _OptionalHealthCheckConfigTypeDef
):
    pass


HealthCheckCustomConfigTypeDef = TypedDict(
    "HealthCheckCustomConfigTypeDef",
    {
        "FailureThreshold": int,
    },
    total=False,
)

DeleteNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteNamespaceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteServiceRequestRequestTypeDef = TypedDict(
    "DeleteServiceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeregisterInstanceRequestRequestTypeDef = TypedDict(
    "DeregisterInstanceRequestRequestTypeDef",
    {
        "ServiceId": str,
        "InstanceId": str,
    },
)

_RequiredDiscoverInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredDiscoverInstancesRequestRequestTypeDef",
    {
        "NamespaceName": str,
        "ServiceName": str,
    },
)
_OptionalDiscoverInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalDiscoverInstancesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "QueryParameters": Mapping[str, str],
        "OptionalParameters": Mapping[str, str],
        "HealthStatus": HealthStatusFilterType,
    },
    total=False,
)


class DiscoverInstancesRequestRequestTypeDef(
    _RequiredDiscoverInstancesRequestRequestTypeDef, _OptionalDiscoverInstancesRequestRequestTypeDef
):
    pass


HttpInstanceSummaryTypeDef = TypedDict(
    "HttpInstanceSummaryTypeDef",
    {
        "InstanceId": str,
        "NamespaceName": str,
        "ServiceName": str,
        "HealthStatus": HealthStatusType,
        "Attributes": Dict[str, str],
    },
    total=False,
)

DnsRecordTypeDef = TypedDict(
    "DnsRecordTypeDef",
    {
        "Type": RecordTypeType,
        "TTL": int,
    },
)

SOATypeDef = TypedDict(
    "SOATypeDef",
    {
        "TTL": int,
    },
)

GetInstanceRequestRequestTypeDef = TypedDict(
    "GetInstanceRequestRequestTypeDef",
    {
        "ServiceId": str,
        "InstanceId": str,
    },
)

_RequiredInstanceTypeDef = TypedDict(
    "_RequiredInstanceTypeDef",
    {
        "Id": str,
    },
)
_OptionalInstanceTypeDef = TypedDict(
    "_OptionalInstanceTypeDef",
    {
        "CreatorRequestId": str,
        "Attributes": Dict[str, str],
    },
    total=False,
)


class InstanceTypeDef(_RequiredInstanceTypeDef, _OptionalInstanceTypeDef):
    pass


_RequiredGetInstancesHealthStatusRequestRequestTypeDef = TypedDict(
    "_RequiredGetInstancesHealthStatusRequestRequestTypeDef",
    {
        "ServiceId": str,
    },
)
_OptionalGetInstancesHealthStatusRequestRequestTypeDef = TypedDict(
    "_OptionalGetInstancesHealthStatusRequestRequestTypeDef",
    {
        "Instances": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetInstancesHealthStatusRequestRequestTypeDef(
    _RequiredGetInstancesHealthStatusRequestRequestTypeDef,
    _OptionalGetInstancesHealthStatusRequestRequestTypeDef,
):
    pass


GetNamespaceRequestRequestTypeDef = TypedDict(
    "GetNamespaceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetOperationRequestRequestTypeDef = TypedDict(
    "GetOperationRequestRequestTypeDef",
    {
        "OperationId": str,
    },
)

OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "Id": str,
        "Type": OperationTypeType,
        "Status": OperationStatusType,
        "ErrorMessage": str,
        "ErrorCode": str,
        "CreateDate": datetime,
        "UpdateDate": datetime,
        "Targets": Dict[OperationTargetTypeType, str],
    },
    total=False,
)

GetServiceRequestRequestTypeDef = TypedDict(
    "GetServiceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

HttpNamespaceChangeTypeDef = TypedDict(
    "HttpNamespaceChangeTypeDef",
    {
        "Description": str,
    },
)

HttpPropertiesTypeDef = TypedDict(
    "HttpPropertiesTypeDef",
    {
        "HttpName": str,
    },
    total=False,
)

InstanceSummaryTypeDef = TypedDict(
    "InstanceSummaryTypeDef",
    {
        "Id": str,
        "Attributes": Dict[str, str],
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

_RequiredListInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredListInstancesRequestRequestTypeDef",
    {
        "ServiceId": str,
    },
)
_OptionalListInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalListInstancesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListInstancesRequestRequestTypeDef(
    _RequiredListInstancesRequestRequestTypeDef, _OptionalListInstancesRequestRequestTypeDef
):
    pass


_RequiredNamespaceFilterTypeDef = TypedDict(
    "_RequiredNamespaceFilterTypeDef",
    {
        "Name": Literal["TYPE"],
        "Values": Sequence[str],
    },
)
_OptionalNamespaceFilterTypeDef = TypedDict(
    "_OptionalNamespaceFilterTypeDef",
    {
        "Condition": FilterConditionType,
    },
    total=False,
)


class NamespaceFilterTypeDef(_RequiredNamespaceFilterTypeDef, _OptionalNamespaceFilterTypeDef):
    pass


_RequiredOperationFilterTypeDef = TypedDict(
    "_RequiredOperationFilterTypeDef",
    {
        "Name": OperationFilterNameType,
        "Values": Sequence[str],
    },
)
_OptionalOperationFilterTypeDef = TypedDict(
    "_OptionalOperationFilterTypeDef",
    {
        "Condition": FilterConditionType,
    },
    total=False,
)


class OperationFilterTypeDef(_RequiredOperationFilterTypeDef, _OptionalOperationFilterTypeDef):
    pass


OperationSummaryTypeDef = TypedDict(
    "OperationSummaryTypeDef",
    {
        "Id": str,
        "Status": OperationStatusType,
    },
    total=False,
)

_RequiredServiceFilterTypeDef = TypedDict(
    "_RequiredServiceFilterTypeDef",
    {
        "Name": Literal["NAMESPACE_ID"],
        "Values": Sequence[str],
    },
)
_OptionalServiceFilterTypeDef = TypedDict(
    "_OptionalServiceFilterTypeDef",
    {
        "Condition": FilterConditionType,
    },
    total=False,
)


class ServiceFilterTypeDef(_RequiredServiceFilterTypeDef, _OptionalServiceFilterTypeDef):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

SOAChangeTypeDef = TypedDict(
    "SOAChangeTypeDef",
    {
        "TTL": int,
    },
)

_RequiredRegisterInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterInstanceRequestRequestTypeDef",
    {
        "ServiceId": str,
        "InstanceId": str,
        "Attributes": Mapping[str, str],
    },
)
_OptionalRegisterInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterInstanceRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
    },
    total=False,
)


class RegisterInstanceRequestRequestTypeDef(
    _RequiredRegisterInstanceRequestRequestTypeDef, _OptionalRegisterInstanceRequestRequestTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateInstanceCustomHealthStatusRequestRequestTypeDef = TypedDict(
    "UpdateInstanceCustomHealthStatusRequestRequestTypeDef",
    {
        "ServiceId": str,
        "InstanceId": str,
        "Status": CustomHealthStatusType,
    },
)

_RequiredCreateHttpNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHttpNamespaceRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateHttpNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHttpNamespaceRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateHttpNamespaceRequestRequestTypeDef(
    _RequiredCreateHttpNamespaceRequestRequestTypeDef,
    _OptionalCreateHttpNamespaceRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateHttpNamespaceResponseTypeDef = TypedDict(
    "CreateHttpNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePrivateDnsNamespaceResponseTypeDef = TypedDict(
    "CreatePrivateDnsNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePublicDnsNamespaceResponseTypeDef = TypedDict(
    "CreatePublicDnsNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteNamespaceResponseTypeDef = TypedDict(
    "DeleteNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterInstanceResponseTypeDef = TypedDict(
    "DeregisterInstanceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInstancesHealthStatusResponseTypeDef = TypedDict(
    "GetInstancesHealthStatusResponseTypeDef",
    {
        "Status": Dict[str, HealthStatusType],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterInstanceResponseTypeDef = TypedDict(
    "RegisterInstanceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateHttpNamespaceResponseTypeDef = TypedDict(
    "UpdateHttpNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePrivateDnsNamespaceResponseTypeDef = TypedDict(
    "UpdatePrivateDnsNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePublicDnsNamespaceResponseTypeDef = TypedDict(
    "UpdatePublicDnsNamespaceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceResponseTypeDef = TypedDict(
    "UpdateServiceResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DiscoverInstancesResponseTypeDef = TypedDict(
    "DiscoverInstancesResponseTypeDef",
    {
        "Instances": List[HttpInstanceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DnsConfigChangeTypeDef = TypedDict(
    "DnsConfigChangeTypeDef",
    {
        "DnsRecords": Sequence[DnsRecordTypeDef],
    },
)

_RequiredDnsConfigTypeDef = TypedDict(
    "_RequiredDnsConfigTypeDef",
    {
        "DnsRecords": Sequence[DnsRecordTypeDef],
    },
)
_OptionalDnsConfigTypeDef = TypedDict(
    "_OptionalDnsConfigTypeDef",
    {
        "NamespaceId": str,
        "RoutingPolicy": RoutingPolicyType,
    },
    total=False,
)


class DnsConfigTypeDef(_RequiredDnsConfigTypeDef, _OptionalDnsConfigTypeDef):
    pass


DnsPropertiesTypeDef = TypedDict(
    "DnsPropertiesTypeDef",
    {
        "HostedZoneId": str,
        "SOA": SOATypeDef,
    },
    total=False,
)

PrivateDnsPropertiesMutableTypeDef = TypedDict(
    "PrivateDnsPropertiesMutableTypeDef",
    {
        "SOA": SOATypeDef,
    },
)

PublicDnsPropertiesMutableTypeDef = TypedDict(
    "PublicDnsPropertiesMutableTypeDef",
    {
        "SOA": SOATypeDef,
    },
)

GetInstanceResponseTypeDef = TypedDict(
    "GetInstanceResponseTypeDef",
    {
        "Instance": InstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOperationResponseTypeDef = TypedDict(
    "GetOperationResponseTypeDef",
    {
        "Operation": OperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateHttpNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateHttpNamespaceRequestRequestTypeDef",
    {
        "Id": str,
        "Namespace": HttpNamespaceChangeTypeDef,
    },
)
_OptionalUpdateHttpNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateHttpNamespaceRequestRequestTypeDef",
    {
        "UpdaterRequestId": str,
    },
    total=False,
)


class UpdateHttpNamespaceRequestRequestTypeDef(
    _RequiredUpdateHttpNamespaceRequestRequestTypeDef,
    _OptionalUpdateHttpNamespaceRequestRequestTypeDef,
):
    pass


ListInstancesResponseTypeDef = TypedDict(
    "ListInstancesResponseTypeDef",
    {
        "Instances": List[InstanceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListInstancesRequestListInstancesPaginateTypeDef = TypedDict(
    "_RequiredListInstancesRequestListInstancesPaginateTypeDef",
    {
        "ServiceId": str,
    },
)
_OptionalListInstancesRequestListInstancesPaginateTypeDef = TypedDict(
    "_OptionalListInstancesRequestListInstancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListInstancesRequestListInstancesPaginateTypeDef(
    _RequiredListInstancesRequestListInstancesPaginateTypeDef,
    _OptionalListInstancesRequestListInstancesPaginateTypeDef,
):
    pass


ListNamespacesRequestListNamespacesPaginateTypeDef = TypedDict(
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    {
        "Filters": Sequence[NamespaceFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListNamespacesRequestRequestTypeDef = TypedDict(
    "ListNamespacesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[NamespaceFilterTypeDef],
    },
    total=False,
)

ListOperationsRequestListOperationsPaginateTypeDef = TypedDict(
    "ListOperationsRequestListOperationsPaginateTypeDef",
    {
        "Filters": Sequence[OperationFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOperationsRequestRequestTypeDef = TypedDict(
    "ListOperationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[OperationFilterTypeDef],
    },
    total=False,
)

ListOperationsResponseTypeDef = TypedDict(
    "ListOperationsResponseTypeDef",
    {
        "Operations": List[OperationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicesRequestListServicesPaginateTypeDef = TypedDict(
    "ListServicesRequestListServicesPaginateTypeDef",
    {
        "Filters": Sequence[ServiceFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServicesRequestRequestTypeDef = TypedDict(
    "ListServicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[ServiceFilterTypeDef],
    },
    total=False,
)

PrivateDnsPropertiesMutableChangeTypeDef = TypedDict(
    "PrivateDnsPropertiesMutableChangeTypeDef",
    {
        "SOA": SOAChangeTypeDef,
    },
)

PublicDnsPropertiesMutableChangeTypeDef = TypedDict(
    "PublicDnsPropertiesMutableChangeTypeDef",
    {
        "SOA": SOAChangeTypeDef,
    },
)

ServiceChangeTypeDef = TypedDict(
    "ServiceChangeTypeDef",
    {
        "Description": str,
        "DnsConfig": DnsConfigChangeTypeDef,
        "HealthCheckConfig": HealthCheckConfigTypeDef,
    },
    total=False,
)

_RequiredCreateServiceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateServiceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceRequestRequestTypeDef",
    {
        "NamespaceId": str,
        "CreatorRequestId": str,
        "Description": str,
        "DnsConfig": DnsConfigTypeDef,
        "HealthCheckConfig": HealthCheckConfigTypeDef,
        "HealthCheckCustomConfig": HealthCheckCustomConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "Type": Literal["HTTP"],
    },
    total=False,
)


class CreateServiceRequestRequestTypeDef(
    _RequiredCreateServiceRequestRequestTypeDef, _OptionalCreateServiceRequestRequestTypeDef
):
    pass


ServiceSummaryTypeDef = TypedDict(
    "ServiceSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Type": ServiceTypeType,
        "Description": str,
        "InstanceCount": int,
        "DnsConfig": DnsConfigTypeDef,
        "HealthCheckConfig": HealthCheckConfigTypeDef,
        "HealthCheckCustomConfig": HealthCheckCustomConfigTypeDef,
        "CreateDate": datetime,
    },
    total=False,
)

ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "NamespaceId": str,
        "Description": str,
        "InstanceCount": int,
        "DnsConfig": DnsConfigTypeDef,
        "Type": ServiceTypeType,
        "HealthCheckConfig": HealthCheckConfigTypeDef,
        "HealthCheckCustomConfig": HealthCheckCustomConfigTypeDef,
        "CreateDate": datetime,
        "CreatorRequestId": str,
    },
    total=False,
)

NamespacePropertiesTypeDef = TypedDict(
    "NamespacePropertiesTypeDef",
    {
        "DnsProperties": DnsPropertiesTypeDef,
        "HttpProperties": HttpPropertiesTypeDef,
    },
    total=False,
)

PrivateDnsNamespacePropertiesTypeDef = TypedDict(
    "PrivateDnsNamespacePropertiesTypeDef",
    {
        "DnsProperties": PrivateDnsPropertiesMutableTypeDef,
    },
)

PublicDnsNamespacePropertiesTypeDef = TypedDict(
    "PublicDnsNamespacePropertiesTypeDef",
    {
        "DnsProperties": PublicDnsPropertiesMutableTypeDef,
    },
)

PrivateDnsNamespacePropertiesChangeTypeDef = TypedDict(
    "PrivateDnsNamespacePropertiesChangeTypeDef",
    {
        "DnsProperties": PrivateDnsPropertiesMutableChangeTypeDef,
    },
)

PublicDnsNamespacePropertiesChangeTypeDef = TypedDict(
    "PublicDnsNamespacePropertiesChangeTypeDef",
    {
        "DnsProperties": PublicDnsPropertiesMutableChangeTypeDef,
    },
)

UpdateServiceRequestRequestTypeDef = TypedDict(
    "UpdateServiceRequestRequestTypeDef",
    {
        "Id": str,
        "Service": ServiceChangeTypeDef,
    },
)

ListServicesResponseTypeDef = TypedDict(
    "ListServicesResponseTypeDef",
    {
        "Services": List[ServiceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceResponseTypeDef = TypedDict(
    "CreateServiceResponseTypeDef",
    {
        "Service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceResponseTypeDef = TypedDict(
    "GetServiceResponseTypeDef",
    {
        "Service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NamespaceSummaryTypeDef = TypedDict(
    "NamespaceSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Type": NamespaceTypeType,
        "Description": str,
        "ServiceCount": int,
        "Properties": NamespacePropertiesTypeDef,
        "CreateDate": datetime,
    },
    total=False,
)

NamespaceTypeDef = TypedDict(
    "NamespaceTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Type": NamespaceTypeType,
        "Description": str,
        "ServiceCount": int,
        "Properties": NamespacePropertiesTypeDef,
        "CreateDate": datetime,
        "CreatorRequestId": str,
    },
    total=False,
)

_RequiredCreatePrivateDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePrivateDnsNamespaceRequestRequestTypeDef",
    {
        "Name": str,
        "Vpc": str,
    },
)
_OptionalCreatePrivateDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePrivateDnsNamespaceRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "Properties": PrivateDnsNamespacePropertiesTypeDef,
    },
    total=False,
)


class CreatePrivateDnsNamespaceRequestRequestTypeDef(
    _RequiredCreatePrivateDnsNamespaceRequestRequestTypeDef,
    _OptionalCreatePrivateDnsNamespaceRequestRequestTypeDef,
):
    pass


_RequiredCreatePublicDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePublicDnsNamespaceRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreatePublicDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePublicDnsNamespaceRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "Properties": PublicDnsNamespacePropertiesTypeDef,
    },
    total=False,
)


class CreatePublicDnsNamespaceRequestRequestTypeDef(
    _RequiredCreatePublicDnsNamespaceRequestRequestTypeDef,
    _OptionalCreatePublicDnsNamespaceRequestRequestTypeDef,
):
    pass


PrivateDnsNamespaceChangeTypeDef = TypedDict(
    "PrivateDnsNamespaceChangeTypeDef",
    {
        "Description": str,
        "Properties": PrivateDnsNamespacePropertiesChangeTypeDef,
    },
    total=False,
)

PublicDnsNamespaceChangeTypeDef = TypedDict(
    "PublicDnsNamespaceChangeTypeDef",
    {
        "Description": str,
        "Properties": PublicDnsNamespacePropertiesChangeTypeDef,
    },
    total=False,
)

ListNamespacesResponseTypeDef = TypedDict(
    "ListNamespacesResponseTypeDef",
    {
        "Namespaces": List[NamespaceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNamespaceResponseTypeDef = TypedDict(
    "GetNamespaceResponseTypeDef",
    {
        "Namespace": NamespaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdatePrivateDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePrivateDnsNamespaceRequestRequestTypeDef",
    {
        "Id": str,
        "Namespace": PrivateDnsNamespaceChangeTypeDef,
    },
)
_OptionalUpdatePrivateDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePrivateDnsNamespaceRequestRequestTypeDef",
    {
        "UpdaterRequestId": str,
    },
    total=False,
)


class UpdatePrivateDnsNamespaceRequestRequestTypeDef(
    _RequiredUpdatePrivateDnsNamespaceRequestRequestTypeDef,
    _OptionalUpdatePrivateDnsNamespaceRequestRequestTypeDef,
):
    pass


_RequiredUpdatePublicDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePublicDnsNamespaceRequestRequestTypeDef",
    {
        "Id": str,
        "Namespace": PublicDnsNamespaceChangeTypeDef,
    },
)
_OptionalUpdatePublicDnsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePublicDnsNamespaceRequestRequestTypeDef",
    {
        "UpdaterRequestId": str,
    },
    total=False,
)


class UpdatePublicDnsNamespaceRequestRequestTypeDef(
    _RequiredUpdatePublicDnsNamespaceRequestRequestTypeDef,
    _OptionalUpdatePublicDnsNamespaceRequestRequestTypeDef,
):
    pass
