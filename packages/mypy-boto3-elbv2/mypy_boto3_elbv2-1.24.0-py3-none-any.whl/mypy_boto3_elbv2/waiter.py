"""
Type annotations for elbv2 service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elbv2.client import ElasticLoadBalancingv2Client
    from mypy_boto3_elbv2.waiter import (
        LoadBalancerAvailableWaiter,
        LoadBalancerExistsWaiter,
        LoadBalancersDeletedWaiter,
        TargetDeregisteredWaiter,
        TargetInServiceWaiter,
    )

    session = Session()
    client: ElasticLoadBalancingv2Client = session.client("elbv2")

    load_balancer_available_waiter: LoadBalancerAvailableWaiter = client.get_waiter("load_balancer_available")
    load_balancer_exists_waiter: LoadBalancerExistsWaiter = client.get_waiter("load_balancer_exists")
    load_balancers_deleted_waiter: LoadBalancersDeletedWaiter = client.get_waiter("load_balancers_deleted")
    target_deregistered_waiter: TargetDeregisteredWaiter = client.get_waiter("target_deregistered")
    target_in_service_waiter: TargetInServiceWaiter = client.get_waiter("target_in_service")
    ```
"""
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import TargetDescriptionTypeDef, WaiterConfigTypeDef

__all__ = (
    "LoadBalancerAvailableWaiter",
    "LoadBalancerExistsWaiter",
    "LoadBalancersDeletedWaiter",
    "TargetDeregisteredWaiter",
    "TargetInServiceWaiter",
)


class LoadBalancerAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerAvailable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#loadbalanceravailablewaiter)
    """

    def wait(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerAvailable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#loadbalanceravailablewaiter)
        """


class LoadBalancerExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerExists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#loadbalancerexistswaiter)
    """

    def wait(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerExists.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#loadbalancerexistswaiter)
        """


class LoadBalancersDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancersDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#loadbalancersdeletedwaiter)
    """

    def wait(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancersDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#loadbalancersdeletedwaiter)
        """


class TargetDeregisteredWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetDeregistered)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#targetderegisteredwaiter)
    """

    def wait(
        self,
        *,
        TargetGroupArn: str,
        Targets: Sequence[TargetDescriptionTypeDef] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetDeregistered.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#targetderegisteredwaiter)
        """


class TargetInServiceWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetInService)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#targetinservicewaiter)
    """

    def wait(
        self,
        *,
        TargetGroupArn: str,
        Targets: Sequence[TargetDescriptionTypeDef] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetInService.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/waiters/#targetinservicewaiter)
        """
