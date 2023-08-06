"""
Type annotations for elb service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elb.client import ElasticLoadBalancingClient
    from mypy_boto3_elb.waiter import (
        AnyInstanceInServiceWaiter,
        InstanceDeregisteredWaiter,
        InstanceInServiceWaiter,
    )

    session = Session()
    client: ElasticLoadBalancingClient = session.client("elb")

    any_instance_in_service_waiter: AnyInstanceInServiceWaiter = client.get_waiter("any_instance_in_service")
    instance_deregistered_waiter: InstanceDeregisteredWaiter = client.get_waiter("instance_deregistered")
    instance_in_service_waiter: InstanceInServiceWaiter = client.get_waiter("instance_in_service")
    ```
"""
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import InstanceTypeDef, WaiterConfigTypeDef

__all__ = ("AnyInstanceInServiceWaiter", "InstanceDeregisteredWaiter", "InstanceInServiceWaiter")


class AnyInstanceInServiceWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.AnyInstanceInService)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/#anyinstanceinservicewaiter)
    """

    def wait(
        self,
        *,
        LoadBalancerName: str,
        Instances: Sequence[InstanceTypeDef] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.AnyInstanceInService.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/#anyinstanceinservicewaiter)
        """


class InstanceDeregisteredWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceDeregistered)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/#instancederegisteredwaiter)
    """

    def wait(
        self,
        *,
        LoadBalancerName: str,
        Instances: Sequence[InstanceTypeDef] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceDeregistered.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/#instancederegisteredwaiter)
        """


class InstanceInServiceWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceInService)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/#instanceinservicewaiter)
    """

    def wait(
        self,
        *,
        LoadBalancerName: str,
        Instances: Sequence[InstanceTypeDef] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceInService.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters/#instanceinservicewaiter)
        """
