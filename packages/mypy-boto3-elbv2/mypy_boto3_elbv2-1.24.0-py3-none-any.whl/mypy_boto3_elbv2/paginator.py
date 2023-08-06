"""
Type annotations for elbv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elbv2.client import ElasticLoadBalancingv2Client
    from mypy_boto3_elbv2.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeListenerCertificatesPaginator,
        DescribeListenersPaginator,
        DescribeLoadBalancersPaginator,
        DescribeRulesPaginator,
        DescribeSSLPoliciesPaginator,
        DescribeTargetGroupsPaginator,
    )

    session = Session()
    client: ElasticLoadBalancingv2Client = session.client("elbv2")

    describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
    describe_listener_certificates_paginator: DescribeListenerCertificatesPaginator = client.get_paginator("describe_listener_certificates")
    describe_listeners_paginator: DescribeListenersPaginator = client.get_paginator("describe_listeners")
    describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
    describe_rules_paginator: DescribeRulesPaginator = client.get_paginator("describe_rules")
    describe_ssl_policies_paginator: DescribeSSLPoliciesPaginator = client.get_paginator("describe_ssl_policies")
    describe_target_groups_paginator: DescribeTargetGroupsPaginator = client.get_paginator("describe_target_groups")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import LoadBalancerTypeEnumType
from .type_defs import (
    DescribeAccountLimitsOutputTypeDef,
    DescribeListenerCertificatesOutputTypeDef,
    DescribeListenersOutputTypeDef,
    DescribeLoadBalancersOutputTypeDef,
    DescribeRulesOutputTypeDef,
    DescribeSSLPoliciesOutputTypeDef,
    DescribeTargetGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeAccountLimitsPaginator",
    "DescribeListenerCertificatesPaginator",
    "DescribeListenersPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeRulesPaginator",
    "DescribeSSLPoliciesPaginator",
    "DescribeTargetGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAccountLimitsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeAccountLimits)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describeaccountlimitspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeAccountLimits.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describeaccountlimitspaginator)
        """


class DescribeListenerCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListenerCertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describelistenercertificatespaginator)
    """

    def paginate(
        self, *, ListenerArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeListenerCertificatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListenerCertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describelistenercertificatespaginator)
        """


class DescribeListenersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListeners)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describelistenerspaginator)
    """

    def paginate(
        self,
        *,
        LoadBalancerArn: str = ...,
        ListenerArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeListenersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListeners.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describelistenerspaginator)
        """


class DescribeLoadBalancersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeLoadBalancers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describeloadbalancerspaginator)
    """

    def paginate(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeLoadBalancersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeLoadBalancers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describeloadbalancerspaginator)
        """


class DescribeRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describerulespaginator)
    """

    def paginate(
        self,
        *,
        ListenerArn: str = ...,
        RuleArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describerulespaginator)
        """


class DescribeSSLPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeSSLPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describesslpoliciespaginator)
    """

    def paginate(
        self,
        *,
        Names: Sequence[str] = ...,
        LoadBalancerType: LoadBalancerTypeEnumType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSSLPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeSSLPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describesslpoliciespaginator)
        """


class DescribeTargetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeTargetGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describetargetgroupspaginator)
    """

    def paginate(
        self,
        *,
        LoadBalancerArn: str = ...,
        TargetGroupArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTargetGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeTargetGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/paginators/#describetargetgroupspaginator)
        """
