"""
Type annotations for elbv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_elbv2.type_defs import AuthenticateCognitoActionConfigTypeDef

    data: AuthenticateCognitoActionConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ActionTypeEnumType,
    AuthenticateCognitoActionConditionalBehaviorEnumType,
    AuthenticateOidcActionConditionalBehaviorEnumType,
    IpAddressTypeType,
    LoadBalancerSchemeEnumType,
    LoadBalancerStateEnumType,
    LoadBalancerTypeEnumType,
    ProtocolEnumType,
    RedirectActionStatusCodeEnumType,
    TargetGroupIpAddressTypeEnumType,
    TargetHealthReasonEnumType,
    TargetHealthStateEnumType,
    TargetTypeEnumType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AuthenticateCognitoActionConfigTypeDef",
    "AuthenticateOidcActionConfigTypeDef",
    "FixedResponseActionConfigTypeDef",
    "RedirectActionConfigTypeDef",
    "CertificateTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "LoadBalancerAddressTypeDef",
    "CipherTypeDef",
    "SubnetMappingTypeDef",
    "MatcherTypeDef",
    "DeleteListenerInputRequestTypeDef",
    "DeleteLoadBalancerInputRequestTypeDef",
    "DeleteRuleInputRequestTypeDef",
    "DeleteTargetGroupInputRequestTypeDef",
    "TargetDescriptionTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAccountLimitsInputRequestTypeDef",
    "LimitTypeDef",
    "DescribeListenerCertificatesInputRequestTypeDef",
    "DescribeListenersInputRequestTypeDef",
    "DescribeLoadBalancerAttributesInputRequestTypeDef",
    "LoadBalancerAttributeTypeDef",
    "WaiterConfigTypeDef",
    "DescribeLoadBalancersInputRequestTypeDef",
    "DescribeRulesInputRequestTypeDef",
    "DescribeSSLPoliciesInputRequestTypeDef",
    "DescribeTagsInputRequestTypeDef",
    "DescribeTargetGroupAttributesInputRequestTypeDef",
    "TargetGroupAttributeTypeDef",
    "DescribeTargetGroupsInputRequestTypeDef",
    "TargetGroupStickinessConfigTypeDef",
    "TargetGroupTupleTypeDef",
    "HostHeaderConditionConfigTypeDef",
    "HttpHeaderConditionConfigTypeDef",
    "HttpRequestMethodConditionConfigTypeDef",
    "LoadBalancerStateTypeDef",
    "PathPatternConditionConfigTypeDef",
    "QueryStringKeyValuePairTypeDef",
    "RemoveTagsInputRequestTypeDef",
    "SourceIpConditionConfigTypeDef",
    "RulePriorityPairTypeDef",
    "SetIpAddressTypeInputRequestTypeDef",
    "SetSecurityGroupsInputRequestTypeDef",
    "TargetHealthTypeDef",
    "AddListenerCertificatesInputRequestTypeDef",
    "RemoveListenerCertificatesInputRequestTypeDef",
    "AddListenerCertificatesOutputTypeDef",
    "DescribeListenerCertificatesOutputTypeDef",
    "SetIpAddressTypeOutputTypeDef",
    "SetSecurityGroupsOutputTypeDef",
    "AddTagsInputRequestTypeDef",
    "TagDescriptionTypeDef",
    "AvailabilityZoneTypeDef",
    "SslPolicyTypeDef",
    "CreateLoadBalancerInputRequestTypeDef",
    "SetSubnetsInputRequestTypeDef",
    "CreateTargetGroupInputRequestTypeDef",
    "ModifyTargetGroupInputRequestTypeDef",
    "TargetGroupTypeDef",
    "DeregisterTargetsInputRequestTypeDef",
    "DescribeTargetHealthInputRequestTypeDef",
    "RegisterTargetsInputRequestTypeDef",
    "DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef",
    "DescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef",
    "DescribeListenersInputDescribeListenersPaginateTypeDef",
    "DescribeLoadBalancersInputDescribeLoadBalancersPaginateTypeDef",
    "DescribeRulesInputDescribeRulesPaginateTypeDef",
    "DescribeSSLPoliciesInputDescribeSSLPoliciesPaginateTypeDef",
    "DescribeTargetGroupsInputDescribeTargetGroupsPaginateTypeDef",
    "DescribeAccountLimitsOutputTypeDef",
    "DescribeLoadBalancerAttributesOutputTypeDef",
    "ModifyLoadBalancerAttributesInputRequestTypeDef",
    "ModifyLoadBalancerAttributesOutputTypeDef",
    "DescribeLoadBalancersInputLoadBalancerAvailableWaitTypeDef",
    "DescribeLoadBalancersInputLoadBalancerExistsWaitTypeDef",
    "DescribeLoadBalancersInputLoadBalancersDeletedWaitTypeDef",
    "DescribeTargetHealthInputTargetDeregisteredWaitTypeDef",
    "DescribeTargetHealthInputTargetInServiceWaitTypeDef",
    "DescribeTargetGroupAttributesOutputTypeDef",
    "ModifyTargetGroupAttributesInputRequestTypeDef",
    "ModifyTargetGroupAttributesOutputTypeDef",
    "ForwardActionConfigTypeDef",
    "QueryStringConditionConfigTypeDef",
    "SetRulePrioritiesInputRequestTypeDef",
    "TargetHealthDescriptionTypeDef",
    "DescribeTagsOutputTypeDef",
    "LoadBalancerTypeDef",
    "SetSubnetsOutputTypeDef",
    "DescribeSSLPoliciesOutputTypeDef",
    "CreateTargetGroupOutputTypeDef",
    "DescribeTargetGroupsOutputTypeDef",
    "ModifyTargetGroupOutputTypeDef",
    "ActionTypeDef",
    "RuleConditionTypeDef",
    "DescribeTargetHealthOutputTypeDef",
    "CreateLoadBalancerOutputTypeDef",
    "DescribeLoadBalancersOutputTypeDef",
    "CreateListenerInputRequestTypeDef",
    "ListenerTypeDef",
    "ModifyListenerInputRequestTypeDef",
    "CreateRuleInputRequestTypeDef",
    "ModifyRuleInputRequestTypeDef",
    "RuleTypeDef",
    "CreateListenerOutputTypeDef",
    "DescribeListenersOutputTypeDef",
    "ModifyListenerOutputTypeDef",
    "CreateRuleOutputTypeDef",
    "DescribeRulesOutputTypeDef",
    "ModifyRuleOutputTypeDef",
    "SetRulePrioritiesOutputTypeDef",
)

_RequiredAuthenticateCognitoActionConfigTypeDef = TypedDict(
    "_RequiredAuthenticateCognitoActionConfigTypeDef",
    {
        "UserPoolArn": str,
        "UserPoolClientId": str,
        "UserPoolDomain": str,
    },
)
_OptionalAuthenticateCognitoActionConfigTypeDef = TypedDict(
    "_OptionalAuthenticateCognitoActionConfigTypeDef",
    {
        "SessionCookieName": str,
        "Scope": str,
        "SessionTimeout": int,
        "AuthenticationRequestExtraParams": Mapping[str, str],
        "OnUnauthenticatedRequest": AuthenticateCognitoActionConditionalBehaviorEnumType,
    },
    total=False,
)


class AuthenticateCognitoActionConfigTypeDef(
    _RequiredAuthenticateCognitoActionConfigTypeDef, _OptionalAuthenticateCognitoActionConfigTypeDef
):
    pass


_RequiredAuthenticateOidcActionConfigTypeDef = TypedDict(
    "_RequiredAuthenticateOidcActionConfigTypeDef",
    {
        "Issuer": str,
        "AuthorizationEndpoint": str,
        "TokenEndpoint": str,
        "UserInfoEndpoint": str,
        "ClientId": str,
    },
)
_OptionalAuthenticateOidcActionConfigTypeDef = TypedDict(
    "_OptionalAuthenticateOidcActionConfigTypeDef",
    {
        "ClientSecret": str,
        "SessionCookieName": str,
        "Scope": str,
        "SessionTimeout": int,
        "AuthenticationRequestExtraParams": Mapping[str, str],
        "OnUnauthenticatedRequest": AuthenticateOidcActionConditionalBehaviorEnumType,
        "UseExistingClientSecret": bool,
    },
    total=False,
)


class AuthenticateOidcActionConfigTypeDef(
    _RequiredAuthenticateOidcActionConfigTypeDef, _OptionalAuthenticateOidcActionConfigTypeDef
):
    pass


_RequiredFixedResponseActionConfigTypeDef = TypedDict(
    "_RequiredFixedResponseActionConfigTypeDef",
    {
        "StatusCode": str,
    },
)
_OptionalFixedResponseActionConfigTypeDef = TypedDict(
    "_OptionalFixedResponseActionConfigTypeDef",
    {
        "MessageBody": str,
        "ContentType": str,
    },
    total=False,
)


class FixedResponseActionConfigTypeDef(
    _RequiredFixedResponseActionConfigTypeDef, _OptionalFixedResponseActionConfigTypeDef
):
    pass


_RequiredRedirectActionConfigTypeDef = TypedDict(
    "_RequiredRedirectActionConfigTypeDef",
    {
        "StatusCode": RedirectActionStatusCodeEnumType,
    },
)
_OptionalRedirectActionConfigTypeDef = TypedDict(
    "_OptionalRedirectActionConfigTypeDef",
    {
        "Protocol": str,
        "Port": str,
        "Host": str,
        "Path": str,
        "Query": str,
    },
    total=False,
)


class RedirectActionConfigTypeDef(
    _RequiredRedirectActionConfigTypeDef, _OptionalRedirectActionConfigTypeDef
):
    pass


CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateArn": str,
        "IsDefault": bool,
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

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


LoadBalancerAddressTypeDef = TypedDict(
    "LoadBalancerAddressTypeDef",
    {
        "IpAddress": str,
        "AllocationId": str,
        "PrivateIPv4Address": str,
        "IPv6Address": str,
    },
    total=False,
)

CipherTypeDef = TypedDict(
    "CipherTypeDef",
    {
        "Name": str,
        "Priority": int,
    },
    total=False,
)

SubnetMappingTypeDef = TypedDict(
    "SubnetMappingTypeDef",
    {
        "SubnetId": str,
        "AllocationId": str,
        "PrivateIPv4Address": str,
        "IPv6Address": str,
    },
    total=False,
)

MatcherTypeDef = TypedDict(
    "MatcherTypeDef",
    {
        "HttpCode": str,
        "GrpcCode": str,
    },
    total=False,
)

DeleteListenerInputRequestTypeDef = TypedDict(
    "DeleteListenerInputRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

DeleteLoadBalancerInputRequestTypeDef = TypedDict(
    "DeleteLoadBalancerInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
    },
)

DeleteRuleInputRequestTypeDef = TypedDict(
    "DeleteRuleInputRequestTypeDef",
    {
        "RuleArn": str,
    },
)

DeleteTargetGroupInputRequestTypeDef = TypedDict(
    "DeleteTargetGroupInputRequestTypeDef",
    {
        "TargetGroupArn": str,
    },
)

_RequiredTargetDescriptionTypeDef = TypedDict(
    "_RequiredTargetDescriptionTypeDef",
    {
        "Id": str,
    },
)
_OptionalTargetDescriptionTypeDef = TypedDict(
    "_OptionalTargetDescriptionTypeDef",
    {
        "Port": int,
        "AvailabilityZone": str,
    },
    total=False,
)


class TargetDescriptionTypeDef(
    _RequiredTargetDescriptionTypeDef, _OptionalTargetDescriptionTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

DescribeAccountLimitsInputRequestTypeDef = TypedDict(
    "DescribeAccountLimitsInputRequestTypeDef",
    {
        "Marker": str,
        "PageSize": int,
    },
    total=False,
)

LimitTypeDef = TypedDict(
    "LimitTypeDef",
    {
        "Name": str,
        "Max": str,
    },
    total=False,
)

_RequiredDescribeListenerCertificatesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeListenerCertificatesInputRequestTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalDescribeListenerCertificatesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeListenerCertificatesInputRequestTypeDef",
    {
        "Marker": str,
        "PageSize": int,
    },
    total=False,
)


class DescribeListenerCertificatesInputRequestTypeDef(
    _RequiredDescribeListenerCertificatesInputRequestTypeDef,
    _OptionalDescribeListenerCertificatesInputRequestTypeDef,
):
    pass


DescribeListenersInputRequestTypeDef = TypedDict(
    "DescribeListenersInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
        "ListenerArns": Sequence[str],
        "Marker": str,
        "PageSize": int,
    },
    total=False,
)

DescribeLoadBalancerAttributesInputRequestTypeDef = TypedDict(
    "DescribeLoadBalancerAttributesInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
    },
)

LoadBalancerAttributeTypeDef = TypedDict(
    "LoadBalancerAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeLoadBalancersInputRequestTypeDef = TypedDict(
    "DescribeLoadBalancersInputRequestTypeDef",
    {
        "LoadBalancerArns": Sequence[str],
        "Names": Sequence[str],
        "Marker": str,
        "PageSize": int,
    },
    total=False,
)

DescribeRulesInputRequestTypeDef = TypedDict(
    "DescribeRulesInputRequestTypeDef",
    {
        "ListenerArn": str,
        "RuleArns": Sequence[str],
        "Marker": str,
        "PageSize": int,
    },
    total=False,
)

DescribeSSLPoliciesInputRequestTypeDef = TypedDict(
    "DescribeSSLPoliciesInputRequestTypeDef",
    {
        "Names": Sequence[str],
        "Marker": str,
        "PageSize": int,
        "LoadBalancerType": LoadBalancerTypeEnumType,
    },
    total=False,
)

DescribeTagsInputRequestTypeDef = TypedDict(
    "DescribeTagsInputRequestTypeDef",
    {
        "ResourceArns": Sequence[str],
    },
)

DescribeTargetGroupAttributesInputRequestTypeDef = TypedDict(
    "DescribeTargetGroupAttributesInputRequestTypeDef",
    {
        "TargetGroupArn": str,
    },
)

TargetGroupAttributeTypeDef = TypedDict(
    "TargetGroupAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

DescribeTargetGroupsInputRequestTypeDef = TypedDict(
    "DescribeTargetGroupsInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
        "TargetGroupArns": Sequence[str],
        "Names": Sequence[str],
        "Marker": str,
        "PageSize": int,
    },
    total=False,
)

TargetGroupStickinessConfigTypeDef = TypedDict(
    "TargetGroupStickinessConfigTypeDef",
    {
        "Enabled": bool,
        "DurationSeconds": int,
    },
    total=False,
)

TargetGroupTupleTypeDef = TypedDict(
    "TargetGroupTupleTypeDef",
    {
        "TargetGroupArn": str,
        "Weight": int,
    },
    total=False,
)

HostHeaderConditionConfigTypeDef = TypedDict(
    "HostHeaderConditionConfigTypeDef",
    {
        "Values": Sequence[str],
    },
    total=False,
)

HttpHeaderConditionConfigTypeDef = TypedDict(
    "HttpHeaderConditionConfigTypeDef",
    {
        "HttpHeaderName": str,
        "Values": Sequence[str],
    },
    total=False,
)

HttpRequestMethodConditionConfigTypeDef = TypedDict(
    "HttpRequestMethodConditionConfigTypeDef",
    {
        "Values": Sequence[str],
    },
    total=False,
)

LoadBalancerStateTypeDef = TypedDict(
    "LoadBalancerStateTypeDef",
    {
        "Code": LoadBalancerStateEnumType,
        "Reason": str,
    },
    total=False,
)

PathPatternConditionConfigTypeDef = TypedDict(
    "PathPatternConditionConfigTypeDef",
    {
        "Values": Sequence[str],
    },
    total=False,
)

QueryStringKeyValuePairTypeDef = TypedDict(
    "QueryStringKeyValuePairTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

RemoveTagsInputRequestTypeDef = TypedDict(
    "RemoveTagsInputRequestTypeDef",
    {
        "ResourceArns": Sequence[str],
        "TagKeys": Sequence[str],
    },
)

SourceIpConditionConfigTypeDef = TypedDict(
    "SourceIpConditionConfigTypeDef",
    {
        "Values": Sequence[str],
    },
    total=False,
)

RulePriorityPairTypeDef = TypedDict(
    "RulePriorityPairTypeDef",
    {
        "RuleArn": str,
        "Priority": int,
    },
    total=False,
)

SetIpAddressTypeInputRequestTypeDef = TypedDict(
    "SetIpAddressTypeInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
        "IpAddressType": IpAddressTypeType,
    },
)

SetSecurityGroupsInputRequestTypeDef = TypedDict(
    "SetSecurityGroupsInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
        "SecurityGroups": Sequence[str],
    },
)

TargetHealthTypeDef = TypedDict(
    "TargetHealthTypeDef",
    {
        "State": TargetHealthStateEnumType,
        "Reason": TargetHealthReasonEnumType,
        "Description": str,
    },
    total=False,
)

AddListenerCertificatesInputRequestTypeDef = TypedDict(
    "AddListenerCertificatesInputRequestTypeDef",
    {
        "ListenerArn": str,
        "Certificates": Sequence[CertificateTypeDef],
    },
)

RemoveListenerCertificatesInputRequestTypeDef = TypedDict(
    "RemoveListenerCertificatesInputRequestTypeDef",
    {
        "ListenerArn": str,
        "Certificates": Sequence[CertificateTypeDef],
    },
)

AddListenerCertificatesOutputTypeDef = TypedDict(
    "AddListenerCertificatesOutputTypeDef",
    {
        "Certificates": List[CertificateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeListenerCertificatesOutputTypeDef = TypedDict(
    "DescribeListenerCertificatesOutputTypeDef",
    {
        "Certificates": List[CertificateTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetIpAddressTypeOutputTypeDef = TypedDict(
    "SetIpAddressTypeOutputTypeDef",
    {
        "IpAddressType": IpAddressTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetSecurityGroupsOutputTypeDef = TypedDict(
    "SetSecurityGroupsOutputTypeDef",
    {
        "SecurityGroupIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsInputRequestTypeDef = TypedDict(
    "AddTagsInputRequestTypeDef",
    {
        "ResourceArns": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
)

TagDescriptionTypeDef = TypedDict(
    "TagDescriptionTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "ZoneName": str,
        "SubnetId": str,
        "OutpostId": str,
        "LoadBalancerAddresses": List[LoadBalancerAddressTypeDef],
    },
    total=False,
)

SslPolicyTypeDef = TypedDict(
    "SslPolicyTypeDef",
    {
        "SslProtocols": List[str],
        "Ciphers": List[CipherTypeDef],
        "Name": str,
        "SupportedLoadBalancerTypes": List[str],
    },
    total=False,
)

_RequiredCreateLoadBalancerInputRequestTypeDef = TypedDict(
    "_RequiredCreateLoadBalancerInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateLoadBalancerInputRequestTypeDef = TypedDict(
    "_OptionalCreateLoadBalancerInputRequestTypeDef",
    {
        "Subnets": Sequence[str],
        "SubnetMappings": Sequence[SubnetMappingTypeDef],
        "SecurityGroups": Sequence[str],
        "Scheme": LoadBalancerSchemeEnumType,
        "Tags": Sequence[TagTypeDef],
        "Type": LoadBalancerTypeEnumType,
        "IpAddressType": IpAddressTypeType,
        "CustomerOwnedIpv4Pool": str,
    },
    total=False,
)


class CreateLoadBalancerInputRequestTypeDef(
    _RequiredCreateLoadBalancerInputRequestTypeDef, _OptionalCreateLoadBalancerInputRequestTypeDef
):
    pass


_RequiredSetSubnetsInputRequestTypeDef = TypedDict(
    "_RequiredSetSubnetsInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
    },
)
_OptionalSetSubnetsInputRequestTypeDef = TypedDict(
    "_OptionalSetSubnetsInputRequestTypeDef",
    {
        "Subnets": Sequence[str],
        "SubnetMappings": Sequence[SubnetMappingTypeDef],
        "IpAddressType": IpAddressTypeType,
    },
    total=False,
)


class SetSubnetsInputRequestTypeDef(
    _RequiredSetSubnetsInputRequestTypeDef, _OptionalSetSubnetsInputRequestTypeDef
):
    pass


_RequiredCreateTargetGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateTargetGroupInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateTargetGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateTargetGroupInputRequestTypeDef",
    {
        "Protocol": ProtocolEnumType,
        "ProtocolVersion": str,
        "Port": int,
        "VpcId": str,
        "HealthCheckProtocol": ProtocolEnumType,
        "HealthCheckPort": str,
        "HealthCheckEnabled": bool,
        "HealthCheckPath": str,
        "HealthCheckIntervalSeconds": int,
        "HealthCheckTimeoutSeconds": int,
        "HealthyThresholdCount": int,
        "UnhealthyThresholdCount": int,
        "Matcher": MatcherTypeDef,
        "TargetType": TargetTypeEnumType,
        "Tags": Sequence[TagTypeDef],
        "IpAddressType": TargetGroupIpAddressTypeEnumType,
    },
    total=False,
)


class CreateTargetGroupInputRequestTypeDef(
    _RequiredCreateTargetGroupInputRequestTypeDef, _OptionalCreateTargetGroupInputRequestTypeDef
):
    pass


_RequiredModifyTargetGroupInputRequestTypeDef = TypedDict(
    "_RequiredModifyTargetGroupInputRequestTypeDef",
    {
        "TargetGroupArn": str,
    },
)
_OptionalModifyTargetGroupInputRequestTypeDef = TypedDict(
    "_OptionalModifyTargetGroupInputRequestTypeDef",
    {
        "HealthCheckProtocol": ProtocolEnumType,
        "HealthCheckPort": str,
        "HealthCheckPath": str,
        "HealthCheckEnabled": bool,
        "HealthCheckIntervalSeconds": int,
        "HealthCheckTimeoutSeconds": int,
        "HealthyThresholdCount": int,
        "UnhealthyThresholdCount": int,
        "Matcher": MatcherTypeDef,
    },
    total=False,
)


class ModifyTargetGroupInputRequestTypeDef(
    _RequiredModifyTargetGroupInputRequestTypeDef, _OptionalModifyTargetGroupInputRequestTypeDef
):
    pass


TargetGroupTypeDef = TypedDict(
    "TargetGroupTypeDef",
    {
        "TargetGroupArn": str,
        "TargetGroupName": str,
        "Protocol": ProtocolEnumType,
        "Port": int,
        "VpcId": str,
        "HealthCheckProtocol": ProtocolEnumType,
        "HealthCheckPort": str,
        "HealthCheckEnabled": bool,
        "HealthCheckIntervalSeconds": int,
        "HealthCheckTimeoutSeconds": int,
        "HealthyThresholdCount": int,
        "UnhealthyThresholdCount": int,
        "HealthCheckPath": str,
        "Matcher": MatcherTypeDef,
        "LoadBalancerArns": List[str],
        "TargetType": TargetTypeEnumType,
        "ProtocolVersion": str,
        "IpAddressType": TargetGroupIpAddressTypeEnumType,
    },
    total=False,
)

DeregisterTargetsInputRequestTypeDef = TypedDict(
    "DeregisterTargetsInputRequestTypeDef",
    {
        "TargetGroupArn": str,
        "Targets": Sequence[TargetDescriptionTypeDef],
    },
)

_RequiredDescribeTargetHealthInputRequestTypeDef = TypedDict(
    "_RequiredDescribeTargetHealthInputRequestTypeDef",
    {
        "TargetGroupArn": str,
    },
)
_OptionalDescribeTargetHealthInputRequestTypeDef = TypedDict(
    "_OptionalDescribeTargetHealthInputRequestTypeDef",
    {
        "Targets": Sequence[TargetDescriptionTypeDef],
    },
    total=False,
)


class DescribeTargetHealthInputRequestTypeDef(
    _RequiredDescribeTargetHealthInputRequestTypeDef,
    _OptionalDescribeTargetHealthInputRequestTypeDef,
):
    pass


RegisterTargetsInputRequestTypeDef = TypedDict(
    "RegisterTargetsInputRequestTypeDef",
    {
        "TargetGroupArn": str,
        "Targets": Sequence[TargetDescriptionTypeDef],
    },
)

DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef = TypedDict(
    "DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef = TypedDict(
    "_RequiredDescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalDescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef = TypedDict(
    "_OptionalDescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef(
    _RequiredDescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef,
    _OptionalDescribeListenerCertificatesInputDescribeListenerCertificatesPaginateTypeDef,
):
    pass


DescribeListenersInputDescribeListenersPaginateTypeDef = TypedDict(
    "DescribeListenersInputDescribeListenersPaginateTypeDef",
    {
        "LoadBalancerArn": str,
        "ListenerArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeLoadBalancersInputDescribeLoadBalancersPaginateTypeDef = TypedDict(
    "DescribeLoadBalancersInputDescribeLoadBalancersPaginateTypeDef",
    {
        "LoadBalancerArns": Sequence[str],
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeRulesInputDescribeRulesPaginateTypeDef = TypedDict(
    "DescribeRulesInputDescribeRulesPaginateTypeDef",
    {
        "ListenerArn": str,
        "RuleArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSSLPoliciesInputDescribeSSLPoliciesPaginateTypeDef = TypedDict(
    "DescribeSSLPoliciesInputDescribeSSLPoliciesPaginateTypeDef",
    {
        "Names": Sequence[str],
        "LoadBalancerType": LoadBalancerTypeEnumType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeTargetGroupsInputDescribeTargetGroupsPaginateTypeDef = TypedDict(
    "DescribeTargetGroupsInputDescribeTargetGroupsPaginateTypeDef",
    {
        "LoadBalancerArn": str,
        "TargetGroupArns": Sequence[str],
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAccountLimitsOutputTypeDef = TypedDict(
    "DescribeAccountLimitsOutputTypeDef",
    {
        "Limits": List[LimitTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancerAttributesOutputTypeDef = TypedDict(
    "DescribeLoadBalancerAttributesOutputTypeDef",
    {
        "Attributes": List[LoadBalancerAttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyLoadBalancerAttributesInputRequestTypeDef = TypedDict(
    "ModifyLoadBalancerAttributesInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
        "Attributes": Sequence[LoadBalancerAttributeTypeDef],
    },
)

ModifyLoadBalancerAttributesOutputTypeDef = TypedDict(
    "ModifyLoadBalancerAttributesOutputTypeDef",
    {
        "Attributes": List[LoadBalancerAttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancersInputLoadBalancerAvailableWaitTypeDef = TypedDict(
    "DescribeLoadBalancersInputLoadBalancerAvailableWaitTypeDef",
    {
        "LoadBalancerArns": Sequence[str],
        "Names": Sequence[str],
        "Marker": str,
        "PageSize": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeLoadBalancersInputLoadBalancerExistsWaitTypeDef = TypedDict(
    "DescribeLoadBalancersInputLoadBalancerExistsWaitTypeDef",
    {
        "LoadBalancerArns": Sequence[str],
        "Names": Sequence[str],
        "Marker": str,
        "PageSize": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeLoadBalancersInputLoadBalancersDeletedWaitTypeDef = TypedDict(
    "DescribeLoadBalancersInputLoadBalancersDeletedWaitTypeDef",
    {
        "LoadBalancerArns": Sequence[str],
        "Names": Sequence[str],
        "Marker": str,
        "PageSize": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeTargetHealthInputTargetDeregisteredWaitTypeDef = TypedDict(
    "_RequiredDescribeTargetHealthInputTargetDeregisteredWaitTypeDef",
    {
        "TargetGroupArn": str,
    },
)
_OptionalDescribeTargetHealthInputTargetDeregisteredWaitTypeDef = TypedDict(
    "_OptionalDescribeTargetHealthInputTargetDeregisteredWaitTypeDef",
    {
        "Targets": Sequence[TargetDescriptionTypeDef],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeTargetHealthInputTargetDeregisteredWaitTypeDef(
    _RequiredDescribeTargetHealthInputTargetDeregisteredWaitTypeDef,
    _OptionalDescribeTargetHealthInputTargetDeregisteredWaitTypeDef,
):
    pass


_RequiredDescribeTargetHealthInputTargetInServiceWaitTypeDef = TypedDict(
    "_RequiredDescribeTargetHealthInputTargetInServiceWaitTypeDef",
    {
        "TargetGroupArn": str,
    },
)
_OptionalDescribeTargetHealthInputTargetInServiceWaitTypeDef = TypedDict(
    "_OptionalDescribeTargetHealthInputTargetInServiceWaitTypeDef",
    {
        "Targets": Sequence[TargetDescriptionTypeDef],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeTargetHealthInputTargetInServiceWaitTypeDef(
    _RequiredDescribeTargetHealthInputTargetInServiceWaitTypeDef,
    _OptionalDescribeTargetHealthInputTargetInServiceWaitTypeDef,
):
    pass


DescribeTargetGroupAttributesOutputTypeDef = TypedDict(
    "DescribeTargetGroupAttributesOutputTypeDef",
    {
        "Attributes": List[TargetGroupAttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyTargetGroupAttributesInputRequestTypeDef = TypedDict(
    "ModifyTargetGroupAttributesInputRequestTypeDef",
    {
        "TargetGroupArn": str,
        "Attributes": Sequence[TargetGroupAttributeTypeDef],
    },
)

ModifyTargetGroupAttributesOutputTypeDef = TypedDict(
    "ModifyTargetGroupAttributesOutputTypeDef",
    {
        "Attributes": List[TargetGroupAttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ForwardActionConfigTypeDef = TypedDict(
    "ForwardActionConfigTypeDef",
    {
        "TargetGroups": Sequence[TargetGroupTupleTypeDef],
        "TargetGroupStickinessConfig": TargetGroupStickinessConfigTypeDef,
    },
    total=False,
)

QueryStringConditionConfigTypeDef = TypedDict(
    "QueryStringConditionConfigTypeDef",
    {
        "Values": Sequence[QueryStringKeyValuePairTypeDef],
    },
    total=False,
)

SetRulePrioritiesInputRequestTypeDef = TypedDict(
    "SetRulePrioritiesInputRequestTypeDef",
    {
        "RulePriorities": Sequence[RulePriorityPairTypeDef],
    },
)

TargetHealthDescriptionTypeDef = TypedDict(
    "TargetHealthDescriptionTypeDef",
    {
        "Target": TargetDescriptionTypeDef,
        "HealthCheckPort": str,
        "TargetHealth": TargetHealthTypeDef,
    },
    total=False,
)

DescribeTagsOutputTypeDef = TypedDict(
    "DescribeTagsOutputTypeDef",
    {
        "TagDescriptions": List[TagDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoadBalancerTypeDef = TypedDict(
    "LoadBalancerTypeDef",
    {
        "LoadBalancerArn": str,
        "DNSName": str,
        "CanonicalHostedZoneId": str,
        "CreatedTime": datetime,
        "LoadBalancerName": str,
        "Scheme": LoadBalancerSchemeEnumType,
        "VpcId": str,
        "State": LoadBalancerStateTypeDef,
        "Type": LoadBalancerTypeEnumType,
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "SecurityGroups": List[str],
        "IpAddressType": IpAddressTypeType,
        "CustomerOwnedIpv4Pool": str,
    },
    total=False,
)

SetSubnetsOutputTypeDef = TypedDict(
    "SetSubnetsOutputTypeDef",
    {
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "IpAddressType": IpAddressTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSSLPoliciesOutputTypeDef = TypedDict(
    "DescribeSSLPoliciesOutputTypeDef",
    {
        "SslPolicies": List[SslPolicyTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTargetGroupOutputTypeDef = TypedDict(
    "CreateTargetGroupOutputTypeDef",
    {
        "TargetGroups": List[TargetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTargetGroupsOutputTypeDef = TypedDict(
    "DescribeTargetGroupsOutputTypeDef",
    {
        "TargetGroups": List[TargetGroupTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyTargetGroupOutputTypeDef = TypedDict(
    "ModifyTargetGroupOutputTypeDef",
    {
        "TargetGroups": List[TargetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredActionTypeDef = TypedDict(
    "_RequiredActionTypeDef",
    {
        "Type": ActionTypeEnumType,
    },
)
_OptionalActionTypeDef = TypedDict(
    "_OptionalActionTypeDef",
    {
        "TargetGroupArn": str,
        "AuthenticateOidcConfig": AuthenticateOidcActionConfigTypeDef,
        "AuthenticateCognitoConfig": AuthenticateCognitoActionConfigTypeDef,
        "Order": int,
        "RedirectConfig": RedirectActionConfigTypeDef,
        "FixedResponseConfig": FixedResponseActionConfigTypeDef,
        "ForwardConfig": ForwardActionConfigTypeDef,
    },
    total=False,
)


class ActionTypeDef(_RequiredActionTypeDef, _OptionalActionTypeDef):
    pass


RuleConditionTypeDef = TypedDict(
    "RuleConditionTypeDef",
    {
        "Field": str,
        "Values": Sequence[str],
        "HostHeaderConfig": HostHeaderConditionConfigTypeDef,
        "PathPatternConfig": PathPatternConditionConfigTypeDef,
        "HttpHeaderConfig": HttpHeaderConditionConfigTypeDef,
        "QueryStringConfig": QueryStringConditionConfigTypeDef,
        "HttpRequestMethodConfig": HttpRequestMethodConditionConfigTypeDef,
        "SourceIpConfig": SourceIpConditionConfigTypeDef,
    },
    total=False,
)

DescribeTargetHealthOutputTypeDef = TypedDict(
    "DescribeTargetHealthOutputTypeDef",
    {
        "TargetHealthDescriptions": List[TargetHealthDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLoadBalancerOutputTypeDef = TypedDict(
    "CreateLoadBalancerOutputTypeDef",
    {
        "LoadBalancers": List[LoadBalancerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancersOutputTypeDef = TypedDict(
    "DescribeLoadBalancersOutputTypeDef",
    {
        "LoadBalancers": List[LoadBalancerTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateListenerInputRequestTypeDef = TypedDict(
    "_RequiredCreateListenerInputRequestTypeDef",
    {
        "LoadBalancerArn": str,
        "DefaultActions": Sequence[ActionTypeDef],
    },
)
_OptionalCreateListenerInputRequestTypeDef = TypedDict(
    "_OptionalCreateListenerInputRequestTypeDef",
    {
        "Protocol": ProtocolEnumType,
        "Port": int,
        "SslPolicy": str,
        "Certificates": Sequence[CertificateTypeDef],
        "AlpnPolicy": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateListenerInputRequestTypeDef(
    _RequiredCreateListenerInputRequestTypeDef, _OptionalCreateListenerInputRequestTypeDef
):
    pass


ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "ListenerArn": str,
        "LoadBalancerArn": str,
        "Port": int,
        "Protocol": ProtocolEnumType,
        "Certificates": List[CertificateTypeDef],
        "SslPolicy": str,
        "DefaultActions": List[ActionTypeDef],
        "AlpnPolicy": List[str],
    },
    total=False,
)

_RequiredModifyListenerInputRequestTypeDef = TypedDict(
    "_RequiredModifyListenerInputRequestTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalModifyListenerInputRequestTypeDef = TypedDict(
    "_OptionalModifyListenerInputRequestTypeDef",
    {
        "Port": int,
        "Protocol": ProtocolEnumType,
        "SslPolicy": str,
        "Certificates": Sequence[CertificateTypeDef],
        "DefaultActions": Sequence[ActionTypeDef],
        "AlpnPolicy": Sequence[str],
    },
    total=False,
)


class ModifyListenerInputRequestTypeDef(
    _RequiredModifyListenerInputRequestTypeDef, _OptionalModifyListenerInputRequestTypeDef
):
    pass


_RequiredCreateRuleInputRequestTypeDef = TypedDict(
    "_RequiredCreateRuleInputRequestTypeDef",
    {
        "ListenerArn": str,
        "Conditions": Sequence[RuleConditionTypeDef],
        "Priority": int,
        "Actions": Sequence[ActionTypeDef],
    },
)
_OptionalCreateRuleInputRequestTypeDef = TypedDict(
    "_OptionalCreateRuleInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRuleInputRequestTypeDef(
    _RequiredCreateRuleInputRequestTypeDef, _OptionalCreateRuleInputRequestTypeDef
):
    pass


_RequiredModifyRuleInputRequestTypeDef = TypedDict(
    "_RequiredModifyRuleInputRequestTypeDef",
    {
        "RuleArn": str,
    },
)
_OptionalModifyRuleInputRequestTypeDef = TypedDict(
    "_OptionalModifyRuleInputRequestTypeDef",
    {
        "Conditions": Sequence[RuleConditionTypeDef],
        "Actions": Sequence[ActionTypeDef],
    },
    total=False,
)


class ModifyRuleInputRequestTypeDef(
    _RequiredModifyRuleInputRequestTypeDef, _OptionalModifyRuleInputRequestTypeDef
):
    pass


RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "RuleArn": str,
        "Priority": str,
        "Conditions": List[RuleConditionTypeDef],
        "Actions": List[ActionTypeDef],
        "IsDefault": bool,
    },
    total=False,
)

CreateListenerOutputTypeDef = TypedDict(
    "CreateListenerOutputTypeDef",
    {
        "Listeners": List[ListenerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeListenersOutputTypeDef = TypedDict(
    "DescribeListenersOutputTypeDef",
    {
        "Listeners": List[ListenerTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyListenerOutputTypeDef = TypedDict(
    "ModifyListenerOutputTypeDef",
    {
        "Listeners": List[ListenerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleOutputTypeDef = TypedDict(
    "CreateRuleOutputTypeDef",
    {
        "Rules": List[RuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRulesOutputTypeDef = TypedDict(
    "DescribeRulesOutputTypeDef",
    {
        "Rules": List[RuleTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyRuleOutputTypeDef = TypedDict(
    "ModifyRuleOutputTypeDef",
    {
        "Rules": List[RuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetRulePrioritiesOutputTypeDef = TypedDict(
    "SetRulePrioritiesOutputTypeDef",
    {
        "Rules": List[RuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
