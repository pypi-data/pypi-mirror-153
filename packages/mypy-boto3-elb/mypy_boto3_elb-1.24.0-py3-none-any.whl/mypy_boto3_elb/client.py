"""
Type annotations for elb service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elb.client import ElasticLoadBalancingClient

    session = Session()
    client: ElasticLoadBalancingClient = session.client("elb")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeAccountLimitsPaginator, DescribeLoadBalancersPaginator
from .type_defs import (
    AddAvailabilityZonesOutputTypeDef,
    ApplySecurityGroupsToLoadBalancerOutputTypeDef,
    AttachLoadBalancerToSubnetsOutputTypeDef,
    ConfigureHealthCheckOutputTypeDef,
    CreateAccessPointOutputTypeDef,
    DeregisterEndPointsOutputTypeDef,
    DescribeAccessPointsOutputTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeEndPointStateOutputTypeDef,
    DescribeLoadBalancerAttributesOutputTypeDef,
    DescribeLoadBalancerPoliciesOutputTypeDef,
    DescribeLoadBalancerPolicyTypesOutputTypeDef,
    DescribeTagsOutputTypeDef,
    DetachLoadBalancerFromSubnetsOutputTypeDef,
    HealthCheckTypeDef,
    InstanceTypeDef,
    ListenerTypeDef,
    LoadBalancerAttributesTypeDef,
    ModifyLoadBalancerAttributesOutputTypeDef,
    PolicyAttributeTypeDef,
    RegisterEndPointsOutputTypeDef,
    RemoveAvailabilityZonesOutputTypeDef,
    TagKeyOnlyTypeDef,
    TagTypeDef,
)
from .waiter import AnyInstanceInServiceWaiter, InstanceDeregisteredWaiter, InstanceInServiceWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ElasticLoadBalancingClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessPointNotFoundException: Type[BotocoreClientError]
    CertificateNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependencyThrottleException: Type[BotocoreClientError]
    DuplicateAccessPointNameException: Type[BotocoreClientError]
    DuplicateListenerException: Type[BotocoreClientError]
    DuplicatePolicyNameException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    InvalidConfigurationRequestException: Type[BotocoreClientError]
    InvalidEndPointException: Type[BotocoreClientError]
    InvalidSchemeException: Type[BotocoreClientError]
    InvalidSecurityGroupException: Type[BotocoreClientError]
    InvalidSubnetException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    LoadBalancerAttributeNotFoundException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    PolicyTypeNotFoundException: Type[BotocoreClientError]
    SubnetNotFoundException: Type[BotocoreClientError]
    TooManyAccessPointsException: Type[BotocoreClientError]
    TooManyPoliciesException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedProtocolException: Type[BotocoreClientError]


class ElasticLoadBalancingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticLoadBalancingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#exceptions)
        """

    def add_tags(
        self, *, LoadBalancerNames: Sequence[str], Tags: Sequence[TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.add_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#add_tags)
        """

    def apply_security_groups_to_load_balancer(
        self, *, LoadBalancerName: str, SecurityGroups: Sequence[str]
    ) -> ApplySecurityGroupsToLoadBalancerOutputTypeDef:
        """
        Associates one or more security groups with your load balancer in a virtual
        private cloud (VPC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.apply_security_groups_to_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#apply_security_groups_to_load_balancer)
        """

    def attach_load_balancer_to_subnets(
        self, *, LoadBalancerName: str, Subnets: Sequence[str]
    ) -> AttachLoadBalancerToSubnetsOutputTypeDef:
        """
        Adds one or more subnets to the set of configured subnets for the specified load
        balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.attach_load_balancer_to_subnets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#attach_load_balancer_to_subnets)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#can_paginate)
        """

    def configure_health_check(
        self, *, LoadBalancerName: str, HealthCheck: HealthCheckTypeDef
    ) -> ConfigureHealthCheckOutputTypeDef:
        """
        Specifies the health check settings to use when evaluating the health state of
        your EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.configure_health_check)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#configure_health_check)
        """

    def create_app_cookie_stickiness_policy(
        self, *, LoadBalancerName: str, PolicyName: str, CookieName: str
    ) -> Dict[str, Any]:
        """
        Generates a stickiness policy with sticky session lifetimes that follow that of
        an application-generated cookie.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.create_app_cookie_stickiness_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#create_app_cookie_stickiness_policy)
        """

    def create_lb_cookie_stickiness_policy(
        self, *, LoadBalancerName: str, PolicyName: str, CookieExpirationPeriod: int = ...
    ) -> Dict[str, Any]:
        """
        Generates a stickiness policy with sticky session lifetimes controlled by the
        lifetime of the browser (user-agent) or a specified expiration period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.create_lb_cookie_stickiness_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#create_lb_cookie_stickiness_policy)
        """

    def create_load_balancer(
        self,
        *,
        LoadBalancerName: str,
        Listeners: Sequence[ListenerTypeDef],
        AvailabilityZones: Sequence[str] = ...,
        Subnets: Sequence[str] = ...,
        SecurityGroups: Sequence[str] = ...,
        Scheme: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateAccessPointOutputTypeDef:
        """
        Creates a Classic Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#create_load_balancer)
        """

    def create_load_balancer_listeners(
        self, *, LoadBalancerName: str, Listeners: Sequence[ListenerTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates one or more listeners for the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer_listeners)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#create_load_balancer_listeners)
        """

    def create_load_balancer_policy(
        self,
        *,
        LoadBalancerName: str,
        PolicyName: str,
        PolicyTypeName: str,
        PolicyAttributes: Sequence[PolicyAttributeTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Creates a policy with the specified attributes for the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#create_load_balancer_policy)
        """

    def delete_load_balancer(self, *, LoadBalancerName: str) -> Dict[str, Any]:
        """
        Deletes the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.delete_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#delete_load_balancer)
        """

    def delete_load_balancer_listeners(
        self, *, LoadBalancerName: str, LoadBalancerPorts: Sequence[int]
    ) -> Dict[str, Any]:
        """
        Deletes the specified listeners from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.delete_load_balancer_listeners)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#delete_load_balancer_listeners)
        """

    def delete_load_balancer_policy(
        self, *, LoadBalancerName: str, PolicyName: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.delete_load_balancer_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#delete_load_balancer_policy)
        """

    def deregister_instances_from_load_balancer(
        self, *, LoadBalancerName: str, Instances: Sequence[InstanceTypeDef]
    ) -> DeregisterEndPointsOutputTypeDef:
        """
        Deregisters the specified instances from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.deregister_instances_from_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#deregister_instances_from_load_balancer)
        """

    def describe_account_limits(
        self, *, Marker: str = ..., PageSize: int = ...
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        Describes the current Elastic Load Balancing resource limits for your AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_account_limits)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_account_limits)
        """

    def describe_instance_health(
        self, *, LoadBalancerName: str, Instances: Sequence[InstanceTypeDef] = ...
    ) -> DescribeEndPointStateOutputTypeDef:
        """
        Describes the state of the specified instances with respect to the specified
        load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_instance_health)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_instance_health)
        """

    def describe_load_balancer_attributes(
        self, *, LoadBalancerName: str
    ) -> DescribeLoadBalancerAttributesOutputTypeDef:
        """
        Describes the attributes for the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancer_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_load_balancer_attributes)
        """

    def describe_load_balancer_policies(
        self, *, LoadBalancerName: str = ..., PolicyNames: Sequence[str] = ...
    ) -> DescribeLoadBalancerPoliciesOutputTypeDef:
        """
        Describes the specified policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancer_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_load_balancer_policies)
        """

    def describe_load_balancer_policy_types(
        self, *, PolicyTypeNames: Sequence[str] = ...
    ) -> DescribeLoadBalancerPolicyTypesOutputTypeDef:
        """
        Describes the specified load balancer policy types or all load balancer policy
        types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancer_policy_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_load_balancer_policy_types)
        """

    def describe_load_balancers(
        self, *, LoadBalancerNames: Sequence[str] = ..., Marker: str = ..., PageSize: int = ...
    ) -> DescribeAccessPointsOutputTypeDef:
        """
        Describes the specified the load balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_load_balancers)
        """

    def describe_tags(self, *, LoadBalancerNames: Sequence[str]) -> DescribeTagsOutputTypeDef:
        """
        Describes the tags associated with the specified load balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#describe_tags)
        """

    def detach_load_balancer_from_subnets(
        self, *, LoadBalancerName: str, Subnets: Sequence[str]
    ) -> DetachLoadBalancerFromSubnetsOutputTypeDef:
        """
        Removes the specified subnets from the set of configured subnets for the load
        balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.detach_load_balancer_from_subnets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#detach_load_balancer_from_subnets)
        """

    def disable_availability_zones_for_load_balancer(
        self, *, LoadBalancerName: str, AvailabilityZones: Sequence[str]
    ) -> RemoveAvailabilityZonesOutputTypeDef:
        """
        Removes the specified Availability Zones from the set of Availability Zones for
        the specified load balancer in EC2-Classic or a default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.disable_availability_zones_for_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#disable_availability_zones_for_load_balancer)
        """

    def enable_availability_zones_for_load_balancer(
        self, *, LoadBalancerName: str, AvailabilityZones: Sequence[str]
    ) -> AddAvailabilityZonesOutputTypeDef:
        """
        Adds the specified Availability Zones to the set of Availability Zones for the
        specified load balancer in EC2-Classic or a default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.enable_availability_zones_for_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#enable_availability_zones_for_load_balancer)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#generate_presigned_url)
        """

    def modify_load_balancer_attributes(
        self, *, LoadBalancerName: str, LoadBalancerAttributes: LoadBalancerAttributesTypeDef
    ) -> ModifyLoadBalancerAttributesOutputTypeDef:
        """
        Modifies the attributes of the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.modify_load_balancer_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#modify_load_balancer_attributes)
        """

    def register_instances_with_load_balancer(
        self, *, LoadBalancerName: str, Instances: Sequence[InstanceTypeDef]
    ) -> RegisterEndPointsOutputTypeDef:
        """
        Adds the specified instances to the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.register_instances_with_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#register_instances_with_load_balancer)
        """

    def remove_tags(
        self, *, LoadBalancerNames: Sequence[str], Tags: Sequence[TagKeyOnlyTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.remove_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#remove_tags)
        """

    def set_load_balancer_listener_ssl_certificate(
        self, *, LoadBalancerName: str, LoadBalancerPort: int, SSLCertificateId: str
    ) -> Dict[str, Any]:
        """
        Sets the certificate that terminates the specified listener's SSL connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.set_load_balancer_listener_ssl_certificate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#set_load_balancer_listener_ssl_certificate)
        """

    def set_load_balancer_policies_for_backend_server(
        self, *, LoadBalancerName: str, InstancePort: int, PolicyNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Replaces the set of policies associated with the specified port on which the EC2
        instance is listening with a new set of policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.set_load_balancer_policies_for_backend_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#set_load_balancer_policies_for_backend_server)
        """

    def set_load_balancer_policies_of_listener(
        self, *, LoadBalancerName: str, LoadBalancerPort: int, PolicyNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Replaces the current set of policies for the specified load balancer port with
        the specified set of policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.set_load_balancer_policies_of_listener)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#set_load_balancer_policies_of_listener)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["any_instance_in_service"]
    ) -> AnyInstanceInServiceWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["instance_deregistered"]
    ) -> InstanceDeregisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_in_service"]) -> InstanceInServiceWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/client/#get_waiter)
        """
