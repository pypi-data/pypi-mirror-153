"""
Type annotations for elb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/type_defs/)

Usage::

    ```python
    from mypy_boto3_elb.type_defs import AccessLogTypeDef

    data: AccessLogTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessLogTypeDef",
    "AddAvailabilityZonesInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "AdditionalAttributeTypeDef",
    "AppCookieStickinessPolicyTypeDef",
    "ApplySecurityGroupsToLoadBalancerInputRequestTypeDef",
    "AttachLoadBalancerToSubnetsInputRequestTypeDef",
    "BackendServerDescriptionTypeDef",
    "HealthCheckTypeDef",
    "ConnectionDrainingTypeDef",
    "ConnectionSettingsTypeDef",
    "ListenerTypeDef",
    "CreateAppCookieStickinessPolicyInputRequestTypeDef",
    "CreateLBCookieStickinessPolicyInputRequestTypeDef",
    "PolicyAttributeTypeDef",
    "CrossZoneLoadBalancingTypeDef",
    "DeleteAccessPointInputRequestTypeDef",
    "DeleteLoadBalancerListenerInputRequestTypeDef",
    "DeleteLoadBalancerPolicyInputRequestTypeDef",
    "InstanceTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAccessPointsInputRequestTypeDef",
    "DescribeAccountLimitsInputRequestTypeDef",
    "LimitTypeDef",
    "WaiterConfigTypeDef",
    "InstanceStateTypeDef",
    "DescribeLoadBalancerAttributesInputRequestTypeDef",
    "DescribeLoadBalancerPoliciesInputRequestTypeDef",
    "DescribeLoadBalancerPolicyTypesInputRequestTypeDef",
    "DescribeTagsInputRequestTypeDef",
    "DetachLoadBalancerFromSubnetsInputRequestTypeDef",
    "LBCookieStickinessPolicyTypeDef",
    "SourceSecurityGroupTypeDef",
    "PolicyAttributeDescriptionTypeDef",
    "PolicyAttributeTypeDescriptionTypeDef",
    "RemoveAvailabilityZonesInputRequestTypeDef",
    "TagKeyOnlyTypeDef",
    "SetLoadBalancerListenerSSLCertificateInputRequestTypeDef",
    "SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef",
    "SetLoadBalancerPoliciesOfListenerInputRequestTypeDef",
    "AddAvailabilityZonesOutputTypeDef",
    "ApplySecurityGroupsToLoadBalancerOutputTypeDef",
    "AttachLoadBalancerToSubnetsOutputTypeDef",
    "CreateAccessPointOutputTypeDef",
    "DetachLoadBalancerFromSubnetsOutputTypeDef",
    "RemoveAvailabilityZonesOutputTypeDef",
    "AddTagsInputRequestTypeDef",
    "TagDescriptionTypeDef",
    "ConfigureHealthCheckInputRequestTypeDef",
    "ConfigureHealthCheckOutputTypeDef",
    "CreateAccessPointInputRequestTypeDef",
    "CreateLoadBalancerListenerInputRequestTypeDef",
    "ListenerDescriptionTypeDef",
    "CreateLoadBalancerPolicyInputRequestTypeDef",
    "LoadBalancerAttributesTypeDef",
    "DeregisterEndPointsInputRequestTypeDef",
    "DeregisterEndPointsOutputTypeDef",
    "DescribeEndPointStateInputRequestTypeDef",
    "RegisterEndPointsInputRequestTypeDef",
    "RegisterEndPointsOutputTypeDef",
    "DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef",
    "DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef",
    "DescribeAccountLimitsOutputTypeDef",
    "DescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef",
    "DescribeEndPointStateInputInstanceDeregisteredWaitTypeDef",
    "DescribeEndPointStateInputInstanceInServiceWaitTypeDef",
    "DescribeEndPointStateOutputTypeDef",
    "PoliciesTypeDef",
    "PolicyDescriptionTypeDef",
    "PolicyTypeDescriptionTypeDef",
    "RemoveTagsInputRequestTypeDef",
    "DescribeTagsOutputTypeDef",
    "DescribeLoadBalancerAttributesOutputTypeDef",
    "ModifyLoadBalancerAttributesInputRequestTypeDef",
    "ModifyLoadBalancerAttributesOutputTypeDef",
    "LoadBalancerDescriptionTypeDef",
    "DescribeLoadBalancerPoliciesOutputTypeDef",
    "DescribeLoadBalancerPolicyTypesOutputTypeDef",
    "DescribeAccessPointsOutputTypeDef",
)

_RequiredAccessLogTypeDef = TypedDict(
    "_RequiredAccessLogTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalAccessLogTypeDef = TypedDict(
    "_OptionalAccessLogTypeDef",
    {
        "S3BucketName": str,
        "EmitInterval": int,
        "S3BucketPrefix": str,
    },
    total=False,
)


class AccessLogTypeDef(_RequiredAccessLogTypeDef, _OptionalAccessLogTypeDef):
    pass


AddAvailabilityZonesInputRequestTypeDef = TypedDict(
    "AddAvailabilityZonesInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "AvailabilityZones": Sequence[str],
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


AdditionalAttributeTypeDef = TypedDict(
    "AdditionalAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AppCookieStickinessPolicyTypeDef = TypedDict(
    "AppCookieStickinessPolicyTypeDef",
    {
        "PolicyName": str,
        "CookieName": str,
    },
    total=False,
)

ApplySecurityGroupsToLoadBalancerInputRequestTypeDef = TypedDict(
    "ApplySecurityGroupsToLoadBalancerInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "SecurityGroups": Sequence[str],
    },
)

AttachLoadBalancerToSubnetsInputRequestTypeDef = TypedDict(
    "AttachLoadBalancerToSubnetsInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "Subnets": Sequence[str],
    },
)

BackendServerDescriptionTypeDef = TypedDict(
    "BackendServerDescriptionTypeDef",
    {
        "InstancePort": int,
        "PolicyNames": List[str],
    },
    total=False,
)

HealthCheckTypeDef = TypedDict(
    "HealthCheckTypeDef",
    {
        "Target": str,
        "Interval": int,
        "Timeout": int,
        "UnhealthyThreshold": int,
        "HealthyThreshold": int,
    },
)

_RequiredConnectionDrainingTypeDef = TypedDict(
    "_RequiredConnectionDrainingTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalConnectionDrainingTypeDef = TypedDict(
    "_OptionalConnectionDrainingTypeDef",
    {
        "Timeout": int,
    },
    total=False,
)


class ConnectionDrainingTypeDef(
    _RequiredConnectionDrainingTypeDef, _OptionalConnectionDrainingTypeDef
):
    pass


ConnectionSettingsTypeDef = TypedDict(
    "ConnectionSettingsTypeDef",
    {
        "IdleTimeout": int,
    },
)

_RequiredListenerTypeDef = TypedDict(
    "_RequiredListenerTypeDef",
    {
        "Protocol": str,
        "LoadBalancerPort": int,
        "InstancePort": int,
    },
)
_OptionalListenerTypeDef = TypedDict(
    "_OptionalListenerTypeDef",
    {
        "InstanceProtocol": str,
        "SSLCertificateId": str,
    },
    total=False,
)


class ListenerTypeDef(_RequiredListenerTypeDef, _OptionalListenerTypeDef):
    pass


CreateAppCookieStickinessPolicyInputRequestTypeDef = TypedDict(
    "CreateAppCookieStickinessPolicyInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "PolicyName": str,
        "CookieName": str,
    },
)

_RequiredCreateLBCookieStickinessPolicyInputRequestTypeDef = TypedDict(
    "_RequiredCreateLBCookieStickinessPolicyInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "PolicyName": str,
    },
)
_OptionalCreateLBCookieStickinessPolicyInputRequestTypeDef = TypedDict(
    "_OptionalCreateLBCookieStickinessPolicyInputRequestTypeDef",
    {
        "CookieExpirationPeriod": int,
    },
    total=False,
)


class CreateLBCookieStickinessPolicyInputRequestTypeDef(
    _RequiredCreateLBCookieStickinessPolicyInputRequestTypeDef,
    _OptionalCreateLBCookieStickinessPolicyInputRequestTypeDef,
):
    pass


PolicyAttributeTypeDef = TypedDict(
    "PolicyAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValue": str,
    },
    total=False,
)

CrossZoneLoadBalancingTypeDef = TypedDict(
    "CrossZoneLoadBalancingTypeDef",
    {
        "Enabled": bool,
    },
)

DeleteAccessPointInputRequestTypeDef = TypedDict(
    "DeleteAccessPointInputRequestTypeDef",
    {
        "LoadBalancerName": str,
    },
)

DeleteLoadBalancerListenerInputRequestTypeDef = TypedDict(
    "DeleteLoadBalancerListenerInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "LoadBalancerPorts": Sequence[int],
    },
)

DeleteLoadBalancerPolicyInputRequestTypeDef = TypedDict(
    "DeleteLoadBalancerPolicyInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "PolicyName": str,
    },
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "InstanceId": str,
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

DescribeAccessPointsInputRequestTypeDef = TypedDict(
    "DescribeAccessPointsInputRequestTypeDef",
    {
        "LoadBalancerNames": Sequence[str],
        "Marker": str,
        "PageSize": int,
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

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

InstanceStateTypeDef = TypedDict(
    "InstanceStateTypeDef",
    {
        "InstanceId": str,
        "State": str,
        "ReasonCode": str,
        "Description": str,
    },
    total=False,
)

DescribeLoadBalancerAttributesInputRequestTypeDef = TypedDict(
    "DescribeLoadBalancerAttributesInputRequestTypeDef",
    {
        "LoadBalancerName": str,
    },
)

DescribeLoadBalancerPoliciesInputRequestTypeDef = TypedDict(
    "DescribeLoadBalancerPoliciesInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "PolicyNames": Sequence[str],
    },
    total=False,
)

DescribeLoadBalancerPolicyTypesInputRequestTypeDef = TypedDict(
    "DescribeLoadBalancerPolicyTypesInputRequestTypeDef",
    {
        "PolicyTypeNames": Sequence[str],
    },
    total=False,
)

DescribeTagsInputRequestTypeDef = TypedDict(
    "DescribeTagsInputRequestTypeDef",
    {
        "LoadBalancerNames": Sequence[str],
    },
)

DetachLoadBalancerFromSubnetsInputRequestTypeDef = TypedDict(
    "DetachLoadBalancerFromSubnetsInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "Subnets": Sequence[str],
    },
)

LBCookieStickinessPolicyTypeDef = TypedDict(
    "LBCookieStickinessPolicyTypeDef",
    {
        "PolicyName": str,
        "CookieExpirationPeriod": int,
    },
    total=False,
)

SourceSecurityGroupTypeDef = TypedDict(
    "SourceSecurityGroupTypeDef",
    {
        "OwnerAlias": str,
        "GroupName": str,
    },
    total=False,
)

PolicyAttributeDescriptionTypeDef = TypedDict(
    "PolicyAttributeDescriptionTypeDef",
    {
        "AttributeName": str,
        "AttributeValue": str,
    },
    total=False,
)

PolicyAttributeTypeDescriptionTypeDef = TypedDict(
    "PolicyAttributeTypeDescriptionTypeDef",
    {
        "AttributeName": str,
        "AttributeType": str,
        "Description": str,
        "DefaultValue": str,
        "Cardinality": str,
    },
    total=False,
)

RemoveAvailabilityZonesInputRequestTypeDef = TypedDict(
    "RemoveAvailabilityZonesInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "AvailabilityZones": Sequence[str],
    },
)

TagKeyOnlyTypeDef = TypedDict(
    "TagKeyOnlyTypeDef",
    {
        "Key": str,
    },
    total=False,
)

SetLoadBalancerListenerSSLCertificateInputRequestTypeDef = TypedDict(
    "SetLoadBalancerListenerSSLCertificateInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "LoadBalancerPort": int,
        "SSLCertificateId": str,
    },
)

SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef = TypedDict(
    "SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "InstancePort": int,
        "PolicyNames": Sequence[str],
    },
)

SetLoadBalancerPoliciesOfListenerInputRequestTypeDef = TypedDict(
    "SetLoadBalancerPoliciesOfListenerInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "LoadBalancerPort": int,
        "PolicyNames": Sequence[str],
    },
)

AddAvailabilityZonesOutputTypeDef = TypedDict(
    "AddAvailabilityZonesOutputTypeDef",
    {
        "AvailabilityZones": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ApplySecurityGroupsToLoadBalancerOutputTypeDef = TypedDict(
    "ApplySecurityGroupsToLoadBalancerOutputTypeDef",
    {
        "SecurityGroups": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AttachLoadBalancerToSubnetsOutputTypeDef = TypedDict(
    "AttachLoadBalancerToSubnetsOutputTypeDef",
    {
        "Subnets": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPointOutputTypeDef = TypedDict(
    "CreateAccessPointOutputTypeDef",
    {
        "DNSName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetachLoadBalancerFromSubnetsOutputTypeDef = TypedDict(
    "DetachLoadBalancerFromSubnetsOutputTypeDef",
    {
        "Subnets": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveAvailabilityZonesOutputTypeDef = TypedDict(
    "RemoveAvailabilityZonesOutputTypeDef",
    {
        "AvailabilityZones": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsInputRequestTypeDef = TypedDict(
    "AddTagsInputRequestTypeDef",
    {
        "LoadBalancerNames": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
)

TagDescriptionTypeDef = TypedDict(
    "TagDescriptionTypeDef",
    {
        "LoadBalancerName": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

ConfigureHealthCheckInputRequestTypeDef = TypedDict(
    "ConfigureHealthCheckInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "HealthCheck": HealthCheckTypeDef,
    },
)

ConfigureHealthCheckOutputTypeDef = TypedDict(
    "ConfigureHealthCheckOutputTypeDef",
    {
        "HealthCheck": HealthCheckTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAccessPointInputRequestTypeDef = TypedDict(
    "_RequiredCreateAccessPointInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "Listeners": Sequence[ListenerTypeDef],
    },
)
_OptionalCreateAccessPointInputRequestTypeDef = TypedDict(
    "_OptionalCreateAccessPointInputRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "Subnets": Sequence[str],
        "SecurityGroups": Sequence[str],
        "Scheme": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAccessPointInputRequestTypeDef(
    _RequiredCreateAccessPointInputRequestTypeDef, _OptionalCreateAccessPointInputRequestTypeDef
):
    pass


CreateLoadBalancerListenerInputRequestTypeDef = TypedDict(
    "CreateLoadBalancerListenerInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "Listeners": Sequence[ListenerTypeDef],
    },
)

ListenerDescriptionTypeDef = TypedDict(
    "ListenerDescriptionTypeDef",
    {
        "Listener": ListenerTypeDef,
        "PolicyNames": List[str],
    },
    total=False,
)

_RequiredCreateLoadBalancerPolicyInputRequestTypeDef = TypedDict(
    "_RequiredCreateLoadBalancerPolicyInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "PolicyName": str,
        "PolicyTypeName": str,
    },
)
_OptionalCreateLoadBalancerPolicyInputRequestTypeDef = TypedDict(
    "_OptionalCreateLoadBalancerPolicyInputRequestTypeDef",
    {
        "PolicyAttributes": Sequence[PolicyAttributeTypeDef],
    },
    total=False,
)


class CreateLoadBalancerPolicyInputRequestTypeDef(
    _RequiredCreateLoadBalancerPolicyInputRequestTypeDef,
    _OptionalCreateLoadBalancerPolicyInputRequestTypeDef,
):
    pass


LoadBalancerAttributesTypeDef = TypedDict(
    "LoadBalancerAttributesTypeDef",
    {
        "CrossZoneLoadBalancing": CrossZoneLoadBalancingTypeDef,
        "AccessLog": AccessLogTypeDef,
        "ConnectionDraining": ConnectionDrainingTypeDef,
        "ConnectionSettings": ConnectionSettingsTypeDef,
        "AdditionalAttributes": List[AdditionalAttributeTypeDef],
    },
    total=False,
)

DeregisterEndPointsInputRequestTypeDef = TypedDict(
    "DeregisterEndPointsInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "Instances": Sequence[InstanceTypeDef],
    },
)

DeregisterEndPointsOutputTypeDef = TypedDict(
    "DeregisterEndPointsOutputTypeDef",
    {
        "Instances": List[InstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeEndPointStateInputRequestTypeDef = TypedDict(
    "_RequiredDescribeEndPointStateInputRequestTypeDef",
    {
        "LoadBalancerName": str,
    },
)
_OptionalDescribeEndPointStateInputRequestTypeDef = TypedDict(
    "_OptionalDescribeEndPointStateInputRequestTypeDef",
    {
        "Instances": Sequence[InstanceTypeDef],
    },
    total=False,
)


class DescribeEndPointStateInputRequestTypeDef(
    _RequiredDescribeEndPointStateInputRequestTypeDef,
    _OptionalDescribeEndPointStateInputRequestTypeDef,
):
    pass


RegisterEndPointsInputRequestTypeDef = TypedDict(
    "RegisterEndPointsInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "Instances": Sequence[InstanceTypeDef],
    },
)

RegisterEndPointsOutputTypeDef = TypedDict(
    "RegisterEndPointsOutputTypeDef",
    {
        "Instances": List[InstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef = TypedDict(
    "DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef",
    {
        "LoadBalancerNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef = TypedDict(
    "DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef",
    {
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

_RequiredDescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef = TypedDict(
    "_RequiredDescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef",
    {
        "LoadBalancerName": str,
    },
)
_OptionalDescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef = TypedDict(
    "_OptionalDescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef",
    {
        "Instances": Sequence[InstanceTypeDef],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef(
    _RequiredDescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef,
    _OptionalDescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef,
):
    pass


_RequiredDescribeEndPointStateInputInstanceDeregisteredWaitTypeDef = TypedDict(
    "_RequiredDescribeEndPointStateInputInstanceDeregisteredWaitTypeDef",
    {
        "LoadBalancerName": str,
    },
)
_OptionalDescribeEndPointStateInputInstanceDeregisteredWaitTypeDef = TypedDict(
    "_OptionalDescribeEndPointStateInputInstanceDeregisteredWaitTypeDef",
    {
        "Instances": Sequence[InstanceTypeDef],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeEndPointStateInputInstanceDeregisteredWaitTypeDef(
    _RequiredDescribeEndPointStateInputInstanceDeregisteredWaitTypeDef,
    _OptionalDescribeEndPointStateInputInstanceDeregisteredWaitTypeDef,
):
    pass


_RequiredDescribeEndPointStateInputInstanceInServiceWaitTypeDef = TypedDict(
    "_RequiredDescribeEndPointStateInputInstanceInServiceWaitTypeDef",
    {
        "LoadBalancerName": str,
    },
)
_OptionalDescribeEndPointStateInputInstanceInServiceWaitTypeDef = TypedDict(
    "_OptionalDescribeEndPointStateInputInstanceInServiceWaitTypeDef",
    {
        "Instances": Sequence[InstanceTypeDef],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeEndPointStateInputInstanceInServiceWaitTypeDef(
    _RequiredDescribeEndPointStateInputInstanceInServiceWaitTypeDef,
    _OptionalDescribeEndPointStateInputInstanceInServiceWaitTypeDef,
):
    pass


DescribeEndPointStateOutputTypeDef = TypedDict(
    "DescribeEndPointStateOutputTypeDef",
    {
        "InstanceStates": List[InstanceStateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PoliciesTypeDef = TypedDict(
    "PoliciesTypeDef",
    {
        "AppCookieStickinessPolicies": List[AppCookieStickinessPolicyTypeDef],
        "LBCookieStickinessPolicies": List[LBCookieStickinessPolicyTypeDef],
        "OtherPolicies": List[str],
    },
    total=False,
)

PolicyDescriptionTypeDef = TypedDict(
    "PolicyDescriptionTypeDef",
    {
        "PolicyName": str,
        "PolicyTypeName": str,
        "PolicyAttributeDescriptions": List[PolicyAttributeDescriptionTypeDef],
    },
    total=False,
)

PolicyTypeDescriptionTypeDef = TypedDict(
    "PolicyTypeDescriptionTypeDef",
    {
        "PolicyTypeName": str,
        "Description": str,
        "PolicyAttributeTypeDescriptions": List[PolicyAttributeTypeDescriptionTypeDef],
    },
    total=False,
)

RemoveTagsInputRequestTypeDef = TypedDict(
    "RemoveTagsInputRequestTypeDef",
    {
        "LoadBalancerNames": Sequence[str],
        "Tags": Sequence[TagKeyOnlyTypeDef],
    },
)

DescribeTagsOutputTypeDef = TypedDict(
    "DescribeTagsOutputTypeDef",
    {
        "TagDescriptions": List[TagDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancerAttributesOutputTypeDef = TypedDict(
    "DescribeLoadBalancerAttributesOutputTypeDef",
    {
        "LoadBalancerAttributes": LoadBalancerAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyLoadBalancerAttributesInputRequestTypeDef = TypedDict(
    "ModifyLoadBalancerAttributesInputRequestTypeDef",
    {
        "LoadBalancerName": str,
        "LoadBalancerAttributes": LoadBalancerAttributesTypeDef,
    },
)

ModifyLoadBalancerAttributesOutputTypeDef = TypedDict(
    "ModifyLoadBalancerAttributesOutputTypeDef",
    {
        "LoadBalancerName": str,
        "LoadBalancerAttributes": LoadBalancerAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoadBalancerDescriptionTypeDef = TypedDict(
    "LoadBalancerDescriptionTypeDef",
    {
        "LoadBalancerName": str,
        "DNSName": str,
        "CanonicalHostedZoneName": str,
        "CanonicalHostedZoneNameID": str,
        "ListenerDescriptions": List[ListenerDescriptionTypeDef],
        "Policies": PoliciesTypeDef,
        "BackendServerDescriptions": List[BackendServerDescriptionTypeDef],
        "AvailabilityZones": List[str],
        "Subnets": List[str],
        "VPCId": str,
        "Instances": List[InstanceTypeDef],
        "HealthCheck": HealthCheckTypeDef,
        "SourceSecurityGroup": SourceSecurityGroupTypeDef,
        "SecurityGroups": List[str],
        "CreatedTime": datetime,
        "Scheme": str,
    },
    total=False,
)

DescribeLoadBalancerPoliciesOutputTypeDef = TypedDict(
    "DescribeLoadBalancerPoliciesOutputTypeDef",
    {
        "PolicyDescriptions": List[PolicyDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancerPolicyTypesOutputTypeDef = TypedDict(
    "DescribeLoadBalancerPolicyTypesOutputTypeDef",
    {
        "PolicyTypeDescriptions": List[PolicyTypeDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccessPointsOutputTypeDef = TypedDict(
    "DescribeAccessPointsOutputTypeDef",
    {
        "LoadBalancerDescriptions": List[LoadBalancerDescriptionTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
