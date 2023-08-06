"""
Type annotations for servicediscovery service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_servicediscovery.client import ServiceDiscoveryClient

    session = Session()
    client: ServiceDiscoveryClient = session.client("servicediscovery")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import CustomHealthStatusType, HealthStatusFilterType
from .paginator import (
    ListInstancesPaginator,
    ListNamespacesPaginator,
    ListOperationsPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    CreateHttpNamespaceResponseTypeDef,
    CreatePrivateDnsNamespaceResponseTypeDef,
    CreatePublicDnsNamespaceResponseTypeDef,
    CreateServiceResponseTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeregisterInstanceResponseTypeDef,
    DiscoverInstancesResponseTypeDef,
    DnsConfigTypeDef,
    EmptyResponseMetadataTypeDef,
    GetInstanceResponseTypeDef,
    GetInstancesHealthStatusResponseTypeDef,
    GetNamespaceResponseTypeDef,
    GetOperationResponseTypeDef,
    GetServiceResponseTypeDef,
    HealthCheckConfigTypeDef,
    HealthCheckCustomConfigTypeDef,
    HttpNamespaceChangeTypeDef,
    ListInstancesResponseTypeDef,
    ListNamespacesResponseTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NamespaceFilterTypeDef,
    OperationFilterTypeDef,
    PrivateDnsNamespaceChangeTypeDef,
    PrivateDnsNamespacePropertiesTypeDef,
    PublicDnsNamespaceChangeTypeDef,
    PublicDnsNamespacePropertiesTypeDef,
    RegisterInstanceResponseTypeDef,
    ServiceChangeTypeDef,
    ServiceFilterTypeDef,
    TagTypeDef,
    UpdateHttpNamespaceResponseTypeDef,
    UpdatePrivateDnsNamespaceResponseTypeDef,
    UpdatePublicDnsNamespaceResponseTypeDef,
    UpdateServiceResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ServiceDiscoveryClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CustomHealthNotFound: Type[BotocoreClientError]
    DuplicateRequest: Type[BotocoreClientError]
    InstanceNotFound: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    NamespaceAlreadyExists: Type[BotocoreClientError]
    NamespaceNotFound: Type[BotocoreClientError]
    OperationNotFound: Type[BotocoreClientError]
    RequestLimitExceeded: Type[BotocoreClientError]
    ResourceInUse: Type[BotocoreClientError]
    ResourceLimitExceeded: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceAlreadyExists: Type[BotocoreClientError]
    ServiceNotFound: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ServiceDiscoveryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServiceDiscoveryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#can_paginate)
        """

    def create_http_namespace(
        self,
        *,
        Name: str,
        CreatorRequestId: str = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateHttpNamespaceResponseTypeDef:
        """
        Creates an HTTP namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_http_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_http_namespace)
        """

    def create_private_dns_namespace(
        self,
        *,
        Name: str,
        Vpc: str,
        CreatorRequestId: str = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        Properties: PrivateDnsNamespacePropertiesTypeDef = ...
    ) -> CreatePrivateDnsNamespaceResponseTypeDef:
        """
        Creates a private namespace based on DNS, which is visible only inside a
        specified Amazon VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_private_dns_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_private_dns_namespace)
        """

    def create_public_dns_namespace(
        self,
        *,
        Name: str,
        CreatorRequestId: str = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        Properties: PublicDnsNamespacePropertiesTypeDef = ...
    ) -> CreatePublicDnsNamespaceResponseTypeDef:
        """
        Creates a public namespace based on DNS, which is visible on the internet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_public_dns_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_public_dns_namespace)
        """

    def create_service(
        self,
        *,
        Name: str,
        NamespaceId: str = ...,
        CreatorRequestId: str = ...,
        Description: str = ...,
        DnsConfig: DnsConfigTypeDef = ...,
        HealthCheckConfig: HealthCheckConfigTypeDef = ...,
        HealthCheckCustomConfig: HealthCheckCustomConfigTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        Type: Literal["HTTP"] = ...
    ) -> CreateServiceResponseTypeDef:
        """
        Creates a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#create_service)
        """

    def delete_namespace(self, *, Id: str) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes a namespace from the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.delete_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#delete_namespace)
        """

    def delete_service(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.delete_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#delete_service)
        """

    def deregister_instance(
        self, *, ServiceId: str, InstanceId: str
    ) -> DeregisterInstanceResponseTypeDef:
        """
        Deletes the Amazon Route 53 DNS records and health check, if any, that Cloud Map
        created for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.deregister_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#deregister_instance)
        """

    def discover_instances(
        self,
        *,
        NamespaceName: str,
        ServiceName: str,
        MaxResults: int = ...,
        QueryParameters: Mapping[str, str] = ...,
        OptionalParameters: Mapping[str, str] = ...,
        HealthStatus: HealthStatusFilterType = ...
    ) -> DiscoverInstancesResponseTypeDef:
        """
        Discovers registered instances for a specified namespace and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.discover_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#discover_instances)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#generate_presigned_url)
        """

    def get_instance(self, *, ServiceId: str, InstanceId: str) -> GetInstanceResponseTypeDef:
        """
        Gets information about a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_instance)
        """

    def get_instances_health_status(
        self,
        *,
        ServiceId: str,
        Instances: Sequence[str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> GetInstancesHealthStatusResponseTypeDef:
        """
        Gets the current health status (`Healthy` , `Unhealthy` , or `Unknown` ) of one
        or more instances that are associated with a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_instances_health_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_instances_health_status)
        """

    def get_namespace(self, *, Id: str) -> GetNamespaceResponseTypeDef:
        """
        Gets information about a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_namespace)
        """

    def get_operation(self, *, OperationId: str) -> GetOperationResponseTypeDef:
        """
        Gets information about any operation that returns an operation ID in the
        response, such as a `CreateService` request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_operation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_operation)
        """

    def get_service(self, *, Id: str) -> GetServiceResponseTypeDef:
        """
        Gets the settings for a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_service)
        """

    def list_instances(
        self, *, ServiceId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListInstancesResponseTypeDef:
        """
        Lists summary information about the instances that you registered by using a
        specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_instances)
        """

    def list_namespaces(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[NamespaceFilterTypeDef] = ...
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists summary information about the namespaces that were created by the current
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_namespaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_namespaces)
        """

    def list_operations(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[OperationFilterTypeDef] = ...
    ) -> ListOperationsResponseTypeDef:
        """
        Lists operations that match the criteria that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_operations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_operations)
        """

    def list_services(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[ServiceFilterTypeDef] = ...
    ) -> ListServicesResponseTypeDef:
        """
        Lists summary information for all the services that are associated with one or
        more specified namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_services)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_services)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#list_tags_for_resource)
        """

    def register_instance(
        self,
        *,
        ServiceId: str,
        InstanceId: str,
        Attributes: Mapping[str, str],
        CreatorRequestId: str = ...
    ) -> RegisterInstanceResponseTypeDef:
        """
        Creates or updates one or more records and, optionally, creates a health check
        based on the settings in a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.register_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#register_instance)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#untag_resource)
        """

    def update_http_namespace(
        self, *, Id: str, Namespace: HttpNamespaceChangeTypeDef, UpdaterRequestId: str = ...
    ) -> UpdateHttpNamespaceResponseTypeDef:
        """
        Updates an HTTP namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_http_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_http_namespace)
        """

    def update_instance_custom_health_status(
        self, *, ServiceId: str, InstanceId: str, Status: CustomHealthStatusType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Submits a request to change the health status of a custom health check to
        healthy or unhealthy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_instance_custom_health_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_instance_custom_health_status)
        """

    def update_private_dns_namespace(
        self, *, Id: str, Namespace: PrivateDnsNamespaceChangeTypeDef, UpdaterRequestId: str = ...
    ) -> UpdatePrivateDnsNamespaceResponseTypeDef:
        """
        Updates a private DNS namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_private_dns_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_private_dns_namespace)
        """

    def update_public_dns_namespace(
        self, *, Id: str, Namespace: PublicDnsNamespaceChangeTypeDef, UpdaterRequestId: str = ...
    ) -> UpdatePublicDnsNamespaceResponseTypeDef:
        """
        Updates a public DNS namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_public_dns_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_public_dns_namespace)
        """

    def update_service(
        self, *, Id: str, Service: ServiceChangeTypeDef
    ) -> UpdateServiceResponseTypeDef:
        """
        Submits a request to perform the following operations * Update the TTL setting
        for existing `DnsRecords` configurations * Add, update, or delete
        `HealthCheckConfig` for a specified service .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_service)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#update_service)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_namespaces"]) -> ListNamespacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_operations"]) -> ListOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/client/#get_paginator)
        """
