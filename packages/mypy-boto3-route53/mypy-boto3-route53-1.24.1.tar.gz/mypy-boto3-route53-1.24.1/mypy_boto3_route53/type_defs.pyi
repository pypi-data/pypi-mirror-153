"""
Type annotations for route53 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53.type_defs import AccountLimitTypeDef

    data: AccountLimitTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AccountLimitTypeType,
    ChangeActionType,
    ChangeStatusType,
    CidrCollectionChangeActionType,
    CloudWatchRegionType,
    ComparisonOperatorType,
    HealthCheckRegionType,
    HealthCheckTypeType,
    HostedZoneLimitTypeType,
    InsufficientDataHealthStatusType,
    ResettableElementNameType,
    ResourceRecordSetFailoverType,
    ResourceRecordSetRegionType,
    RRTypeType,
    StatisticType,
    TagResourceTypeType,
    VPCRegionType,
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
    "AccountLimitTypeDef",
    "ActivateKeySigningKeyRequestRequestTypeDef",
    "ChangeInfoTypeDef",
    "ResponseMetadataTypeDef",
    "AlarmIdentifierTypeDef",
    "AliasTargetTypeDef",
    "VPCTypeDef",
    "CidrCollectionChangeTypeDef",
    "TagTypeDef",
    "CidrBlockSummaryTypeDef",
    "CidrCollectionTypeDef",
    "CidrRoutingConfigTypeDef",
    "DimensionTypeDef",
    "CollectionSummaryTypeDef",
    "CreateCidrCollectionRequestRequestTypeDef",
    "HostedZoneConfigTypeDef",
    "DelegationSetTypeDef",
    "CreateKeySigningKeyRequestRequestTypeDef",
    "KeySigningKeyTypeDef",
    "CreateQueryLoggingConfigRequestRequestTypeDef",
    "QueryLoggingConfigTypeDef",
    "CreateReusableDelegationSetRequestRequestTypeDef",
    "CreateTrafficPolicyInstanceRequestRequestTypeDef",
    "TrafficPolicyInstanceTypeDef",
    "CreateTrafficPolicyRequestRequestTypeDef",
    "TrafficPolicyTypeDef",
    "CreateTrafficPolicyVersionRequestRequestTypeDef",
    "DNSSECStatusTypeDef",
    "DeactivateKeySigningKeyRequestRequestTypeDef",
    "DeleteCidrCollectionRequestRequestTypeDef",
    "DeleteHealthCheckRequestRequestTypeDef",
    "DeleteHostedZoneRequestRequestTypeDef",
    "DeleteKeySigningKeyRequestRequestTypeDef",
    "DeleteQueryLoggingConfigRequestRequestTypeDef",
    "DeleteReusableDelegationSetRequestRequestTypeDef",
    "DeleteTrafficPolicyInstanceRequestRequestTypeDef",
    "DeleteTrafficPolicyRequestRequestTypeDef",
    "DisableHostedZoneDNSSECRequestRequestTypeDef",
    "EnableHostedZoneDNSSECRequestRequestTypeDef",
    "GeoLocationDetailsTypeDef",
    "GeoLocationTypeDef",
    "GetAccountLimitRequestRequestTypeDef",
    "GetChangeRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetDNSSECRequestRequestTypeDef",
    "GetGeoLocationRequestRequestTypeDef",
    "GetHealthCheckLastFailureReasonRequestRequestTypeDef",
    "GetHealthCheckRequestRequestTypeDef",
    "GetHealthCheckStatusRequestRequestTypeDef",
    "GetHostedZoneLimitRequestRequestTypeDef",
    "HostedZoneLimitTypeDef",
    "GetHostedZoneRequestRequestTypeDef",
    "GetQueryLoggingConfigRequestRequestTypeDef",
    "GetReusableDelegationSetLimitRequestRequestTypeDef",
    "ReusableDelegationSetLimitTypeDef",
    "GetReusableDelegationSetRequestRequestTypeDef",
    "GetTrafficPolicyInstanceRequestRequestTypeDef",
    "GetTrafficPolicyRequestRequestTypeDef",
    "StatusReportTypeDef",
    "LinkedServiceTypeDef",
    "HostedZoneOwnerTypeDef",
    "PaginatorConfigTypeDef",
    "ListCidrBlocksRequestRequestTypeDef",
    "ListCidrCollectionsRequestRequestTypeDef",
    "ListCidrLocationsRequestRequestTypeDef",
    "LocationSummaryTypeDef",
    "ListGeoLocationsRequestRequestTypeDef",
    "ListHealthChecksRequestRequestTypeDef",
    "ListHostedZonesByNameRequestRequestTypeDef",
    "ListHostedZonesByVPCRequestRequestTypeDef",
    "ListHostedZonesRequestRequestTypeDef",
    "ListQueryLoggingConfigsRequestRequestTypeDef",
    "ListResourceRecordSetsRequestRequestTypeDef",
    "ListReusableDelegationSetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourcesRequestRequestTypeDef",
    "ListTrafficPoliciesRequestRequestTypeDef",
    "TrafficPolicySummaryTypeDef",
    "ListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef",
    "ListTrafficPolicyInstancesByPolicyRequestRequestTypeDef",
    "ListTrafficPolicyInstancesRequestRequestTypeDef",
    "ListTrafficPolicyVersionsRequestRequestTypeDef",
    "ListVPCAssociationAuthorizationsRequestRequestTypeDef",
    "ResourceRecordTypeDef",
    "TestDNSAnswerRequestRequestTypeDef",
    "UpdateHostedZoneCommentRequestRequestTypeDef",
    "UpdateTrafficPolicyCommentRequestRequestTypeDef",
    "UpdateTrafficPolicyInstanceRequestRequestTypeDef",
    "ActivateKeySigningKeyResponseTypeDef",
    "AssociateVPCWithHostedZoneResponseTypeDef",
    "ChangeCidrCollectionResponseTypeDef",
    "ChangeResourceRecordSetsResponseTypeDef",
    "DeactivateKeySigningKeyResponseTypeDef",
    "DeleteHostedZoneResponseTypeDef",
    "DeleteKeySigningKeyResponseTypeDef",
    "DisableHostedZoneDNSSECResponseTypeDef",
    "DisassociateVPCFromHostedZoneResponseTypeDef",
    "EnableHostedZoneDNSSECResponseTypeDef",
    "GetAccountLimitResponseTypeDef",
    "GetChangeResponseTypeDef",
    "GetCheckerIpRangesResponseTypeDef",
    "GetHealthCheckCountResponseTypeDef",
    "GetHostedZoneCountResponseTypeDef",
    "GetTrafficPolicyInstanceCountResponseTypeDef",
    "TestDNSAnswerResponseTypeDef",
    "HealthCheckConfigTypeDef",
    "UpdateHealthCheckRequestRequestTypeDef",
    "AssociateVPCWithHostedZoneRequestRequestTypeDef",
    "CreateVPCAssociationAuthorizationRequestRequestTypeDef",
    "CreateVPCAssociationAuthorizationResponseTypeDef",
    "DeleteVPCAssociationAuthorizationRequestRequestTypeDef",
    "DisassociateVPCFromHostedZoneRequestRequestTypeDef",
    "ListVPCAssociationAuthorizationsResponseTypeDef",
    "ChangeCidrCollectionRequestRequestTypeDef",
    "ChangeTagsForResourceRequestRequestTypeDef",
    "ResourceTagSetTypeDef",
    "ListCidrBlocksResponseTypeDef",
    "CreateCidrCollectionResponseTypeDef",
    "CloudWatchAlarmConfigurationTypeDef",
    "ListCidrCollectionsResponseTypeDef",
    "CreateHostedZoneRequestRequestTypeDef",
    "CreateReusableDelegationSetResponseTypeDef",
    "GetReusableDelegationSetResponseTypeDef",
    "ListReusableDelegationSetsResponseTypeDef",
    "CreateKeySigningKeyResponseTypeDef",
    "CreateQueryLoggingConfigResponseTypeDef",
    "GetQueryLoggingConfigResponseTypeDef",
    "ListQueryLoggingConfigsResponseTypeDef",
    "CreateTrafficPolicyInstanceResponseTypeDef",
    "GetTrafficPolicyInstanceResponseTypeDef",
    "ListTrafficPolicyInstancesByHostedZoneResponseTypeDef",
    "ListTrafficPolicyInstancesByPolicyResponseTypeDef",
    "ListTrafficPolicyInstancesResponseTypeDef",
    "UpdateTrafficPolicyInstanceResponseTypeDef",
    "CreateTrafficPolicyResponseTypeDef",
    "CreateTrafficPolicyVersionResponseTypeDef",
    "GetTrafficPolicyResponseTypeDef",
    "ListTrafficPolicyVersionsResponseTypeDef",
    "UpdateTrafficPolicyCommentResponseTypeDef",
    "GetDNSSECResponseTypeDef",
    "GetGeoLocationResponseTypeDef",
    "ListGeoLocationsResponseTypeDef",
    "GetChangeRequestResourceRecordSetsChangedWaitTypeDef",
    "GetHostedZoneLimitResponseTypeDef",
    "GetReusableDelegationSetLimitResponseTypeDef",
    "HealthCheckObservationTypeDef",
    "HostedZoneTypeDef",
    "HostedZoneSummaryTypeDef",
    "ListCidrBlocksRequestListCidrBlocksPaginateTypeDef",
    "ListCidrCollectionsRequestListCidrCollectionsPaginateTypeDef",
    "ListCidrLocationsRequestListCidrLocationsPaginateTypeDef",
    "ListHealthChecksRequestListHealthChecksPaginateTypeDef",
    "ListHostedZonesRequestListHostedZonesPaginateTypeDef",
    "ListQueryLoggingConfigsRequestListQueryLoggingConfigsPaginateTypeDef",
    "ListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef",
    "ListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef",
    "ListCidrLocationsResponseTypeDef",
    "ListTrafficPoliciesResponseTypeDef",
    "ResourceRecordSetTypeDef",
    "CreateHealthCheckRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTagsForResourcesResponseTypeDef",
    "HealthCheckTypeDef",
    "GetHealthCheckLastFailureReasonResponseTypeDef",
    "GetHealthCheckStatusResponseTypeDef",
    "CreateHostedZoneResponseTypeDef",
    "GetHostedZoneResponseTypeDef",
    "ListHostedZonesByNameResponseTypeDef",
    "ListHostedZonesResponseTypeDef",
    "UpdateHostedZoneCommentResponseTypeDef",
    "ListHostedZonesByVPCResponseTypeDef",
    "ChangeTypeDef",
    "ListResourceRecordSetsResponseTypeDef",
    "CreateHealthCheckResponseTypeDef",
    "GetHealthCheckResponseTypeDef",
    "ListHealthChecksResponseTypeDef",
    "UpdateHealthCheckResponseTypeDef",
    "ChangeBatchTypeDef",
    "ChangeResourceRecordSetsRequestRequestTypeDef",
)

AccountLimitTypeDef = TypedDict(
    "AccountLimitTypeDef",
    {
        "Type": AccountLimitTypeType,
        "Value": int,
    },
)

ActivateKeySigningKeyRequestRequestTypeDef = TypedDict(
    "ActivateKeySigningKeyRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "Name": str,
    },
)

_RequiredChangeInfoTypeDef = TypedDict(
    "_RequiredChangeInfoTypeDef",
    {
        "Id": str,
        "Status": ChangeStatusType,
        "SubmittedAt": datetime,
    },
)
_OptionalChangeInfoTypeDef = TypedDict(
    "_OptionalChangeInfoTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class ChangeInfoTypeDef(_RequiredChangeInfoTypeDef, _OptionalChangeInfoTypeDef):
    pass

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

AlarmIdentifierTypeDef = TypedDict(
    "AlarmIdentifierTypeDef",
    {
        "Region": CloudWatchRegionType,
        "Name": str,
    },
)

AliasTargetTypeDef = TypedDict(
    "AliasTargetTypeDef",
    {
        "HostedZoneId": str,
        "DNSName": str,
        "EvaluateTargetHealth": bool,
    },
)

VPCTypeDef = TypedDict(
    "VPCTypeDef",
    {
        "VPCRegion": VPCRegionType,
        "VPCId": str,
    },
    total=False,
)

CidrCollectionChangeTypeDef = TypedDict(
    "CidrCollectionChangeTypeDef",
    {
        "LocationName": str,
        "Action": CidrCollectionChangeActionType,
        "CidrList": Sequence[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

CidrBlockSummaryTypeDef = TypedDict(
    "CidrBlockSummaryTypeDef",
    {
        "CidrBlock": str,
        "LocationName": str,
    },
    total=False,
)

CidrCollectionTypeDef = TypedDict(
    "CidrCollectionTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Version": int,
    },
    total=False,
)

CidrRoutingConfigTypeDef = TypedDict(
    "CidrRoutingConfigTypeDef",
    {
        "CollectionId": str,
        "LocationName": str,
    },
)

DimensionTypeDef = TypedDict(
    "DimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

CollectionSummaryTypeDef = TypedDict(
    "CollectionSummaryTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Version": int,
    },
    total=False,
)

CreateCidrCollectionRequestRequestTypeDef = TypedDict(
    "CreateCidrCollectionRequestRequestTypeDef",
    {
        "Name": str,
        "CallerReference": str,
    },
)

HostedZoneConfigTypeDef = TypedDict(
    "HostedZoneConfigTypeDef",
    {
        "Comment": str,
        "PrivateZone": bool,
    },
    total=False,
)

_RequiredDelegationSetTypeDef = TypedDict(
    "_RequiredDelegationSetTypeDef",
    {
        "NameServers": List[str],
    },
)
_OptionalDelegationSetTypeDef = TypedDict(
    "_OptionalDelegationSetTypeDef",
    {
        "Id": str,
        "CallerReference": str,
    },
    total=False,
)

class DelegationSetTypeDef(_RequiredDelegationSetTypeDef, _OptionalDelegationSetTypeDef):
    pass

CreateKeySigningKeyRequestRequestTypeDef = TypedDict(
    "CreateKeySigningKeyRequestRequestTypeDef",
    {
        "CallerReference": str,
        "HostedZoneId": str,
        "KeyManagementServiceArn": str,
        "Name": str,
        "Status": str,
    },
)

KeySigningKeyTypeDef = TypedDict(
    "KeySigningKeyTypeDef",
    {
        "Name": str,
        "KmsArn": str,
        "Flag": int,
        "SigningAlgorithmMnemonic": str,
        "SigningAlgorithmType": int,
        "DigestAlgorithmMnemonic": str,
        "DigestAlgorithmType": int,
        "KeyTag": int,
        "DigestValue": str,
        "PublicKey": str,
        "DSRecord": str,
        "DNSKEYRecord": str,
        "Status": str,
        "StatusMessage": str,
        "CreatedDate": datetime,
        "LastModifiedDate": datetime,
    },
    total=False,
)

CreateQueryLoggingConfigRequestRequestTypeDef = TypedDict(
    "CreateQueryLoggingConfigRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "CloudWatchLogsLogGroupArn": str,
    },
)

QueryLoggingConfigTypeDef = TypedDict(
    "QueryLoggingConfigTypeDef",
    {
        "Id": str,
        "HostedZoneId": str,
        "CloudWatchLogsLogGroupArn": str,
    },
)

_RequiredCreateReusableDelegationSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReusableDelegationSetRequestRequestTypeDef",
    {
        "CallerReference": str,
    },
)
_OptionalCreateReusableDelegationSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReusableDelegationSetRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
    total=False,
)

class CreateReusableDelegationSetRequestRequestTypeDef(
    _RequiredCreateReusableDelegationSetRequestRequestTypeDef,
    _OptionalCreateReusableDelegationSetRequestRequestTypeDef,
):
    pass

CreateTrafficPolicyInstanceRequestRequestTypeDef = TypedDict(
    "CreateTrafficPolicyInstanceRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "Name": str,
        "TTL": int,
        "TrafficPolicyId": str,
        "TrafficPolicyVersion": int,
    },
)

TrafficPolicyInstanceTypeDef = TypedDict(
    "TrafficPolicyInstanceTypeDef",
    {
        "Id": str,
        "HostedZoneId": str,
        "Name": str,
        "TTL": int,
        "State": str,
        "Message": str,
        "TrafficPolicyId": str,
        "TrafficPolicyVersion": int,
        "TrafficPolicyType": RRTypeType,
    },
)

_RequiredCreateTrafficPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrafficPolicyRequestRequestTypeDef",
    {
        "Name": str,
        "Document": str,
    },
)
_OptionalCreateTrafficPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrafficPolicyRequestRequestTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class CreateTrafficPolicyRequestRequestTypeDef(
    _RequiredCreateTrafficPolicyRequestRequestTypeDef,
    _OptionalCreateTrafficPolicyRequestRequestTypeDef,
):
    pass

_RequiredTrafficPolicyTypeDef = TypedDict(
    "_RequiredTrafficPolicyTypeDef",
    {
        "Id": str,
        "Version": int,
        "Name": str,
        "Type": RRTypeType,
        "Document": str,
    },
)
_OptionalTrafficPolicyTypeDef = TypedDict(
    "_OptionalTrafficPolicyTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class TrafficPolicyTypeDef(_RequiredTrafficPolicyTypeDef, _OptionalTrafficPolicyTypeDef):
    pass

_RequiredCreateTrafficPolicyVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrafficPolicyVersionRequestRequestTypeDef",
    {
        "Id": str,
        "Document": str,
    },
)
_OptionalCreateTrafficPolicyVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrafficPolicyVersionRequestRequestTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class CreateTrafficPolicyVersionRequestRequestTypeDef(
    _RequiredCreateTrafficPolicyVersionRequestRequestTypeDef,
    _OptionalCreateTrafficPolicyVersionRequestRequestTypeDef,
):
    pass

DNSSECStatusTypeDef = TypedDict(
    "DNSSECStatusTypeDef",
    {
        "ServeSignature": str,
        "StatusMessage": str,
    },
    total=False,
)

DeactivateKeySigningKeyRequestRequestTypeDef = TypedDict(
    "DeactivateKeySigningKeyRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "Name": str,
    },
)

DeleteCidrCollectionRequestRequestTypeDef = TypedDict(
    "DeleteCidrCollectionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteHealthCheckRequestRequestTypeDef = TypedDict(
    "DeleteHealthCheckRequestRequestTypeDef",
    {
        "HealthCheckId": str,
    },
)

DeleteHostedZoneRequestRequestTypeDef = TypedDict(
    "DeleteHostedZoneRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteKeySigningKeyRequestRequestTypeDef = TypedDict(
    "DeleteKeySigningKeyRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "Name": str,
    },
)

DeleteQueryLoggingConfigRequestRequestTypeDef = TypedDict(
    "DeleteQueryLoggingConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteReusableDelegationSetRequestRequestTypeDef = TypedDict(
    "DeleteReusableDelegationSetRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteTrafficPolicyInstanceRequestRequestTypeDef = TypedDict(
    "DeleteTrafficPolicyInstanceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteTrafficPolicyRequestRequestTypeDef = TypedDict(
    "DeleteTrafficPolicyRequestRequestTypeDef",
    {
        "Id": str,
        "Version": int,
    },
)

DisableHostedZoneDNSSECRequestRequestTypeDef = TypedDict(
    "DisableHostedZoneDNSSECRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
)

EnableHostedZoneDNSSECRequestRequestTypeDef = TypedDict(
    "EnableHostedZoneDNSSECRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
)

GeoLocationDetailsTypeDef = TypedDict(
    "GeoLocationDetailsTypeDef",
    {
        "ContinentCode": str,
        "ContinentName": str,
        "CountryCode": str,
        "CountryName": str,
        "SubdivisionCode": str,
        "SubdivisionName": str,
    },
    total=False,
)

GeoLocationTypeDef = TypedDict(
    "GeoLocationTypeDef",
    {
        "ContinentCode": str,
        "CountryCode": str,
        "SubdivisionCode": str,
    },
    total=False,
)

GetAccountLimitRequestRequestTypeDef = TypedDict(
    "GetAccountLimitRequestRequestTypeDef",
    {
        "Type": AccountLimitTypeType,
    },
)

GetChangeRequestRequestTypeDef = TypedDict(
    "GetChangeRequestRequestTypeDef",
    {
        "Id": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

GetDNSSECRequestRequestTypeDef = TypedDict(
    "GetDNSSECRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
)

GetGeoLocationRequestRequestTypeDef = TypedDict(
    "GetGeoLocationRequestRequestTypeDef",
    {
        "ContinentCode": str,
        "CountryCode": str,
        "SubdivisionCode": str,
    },
    total=False,
)

GetHealthCheckLastFailureReasonRequestRequestTypeDef = TypedDict(
    "GetHealthCheckLastFailureReasonRequestRequestTypeDef",
    {
        "HealthCheckId": str,
    },
)

GetHealthCheckRequestRequestTypeDef = TypedDict(
    "GetHealthCheckRequestRequestTypeDef",
    {
        "HealthCheckId": str,
    },
)

GetHealthCheckStatusRequestRequestTypeDef = TypedDict(
    "GetHealthCheckStatusRequestRequestTypeDef",
    {
        "HealthCheckId": str,
    },
)

GetHostedZoneLimitRequestRequestTypeDef = TypedDict(
    "GetHostedZoneLimitRequestRequestTypeDef",
    {
        "Type": HostedZoneLimitTypeType,
        "HostedZoneId": str,
    },
)

HostedZoneLimitTypeDef = TypedDict(
    "HostedZoneLimitTypeDef",
    {
        "Type": HostedZoneLimitTypeType,
        "Value": int,
    },
)

GetHostedZoneRequestRequestTypeDef = TypedDict(
    "GetHostedZoneRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetQueryLoggingConfigRequestRequestTypeDef = TypedDict(
    "GetQueryLoggingConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetReusableDelegationSetLimitRequestRequestTypeDef = TypedDict(
    "GetReusableDelegationSetLimitRequestRequestTypeDef",
    {
        "Type": Literal["MAX_ZONES_BY_REUSABLE_DELEGATION_SET"],
        "DelegationSetId": str,
    },
)

ReusableDelegationSetLimitTypeDef = TypedDict(
    "ReusableDelegationSetLimitTypeDef",
    {
        "Type": Literal["MAX_ZONES_BY_REUSABLE_DELEGATION_SET"],
        "Value": int,
    },
)

GetReusableDelegationSetRequestRequestTypeDef = TypedDict(
    "GetReusableDelegationSetRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetTrafficPolicyInstanceRequestRequestTypeDef = TypedDict(
    "GetTrafficPolicyInstanceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetTrafficPolicyRequestRequestTypeDef = TypedDict(
    "GetTrafficPolicyRequestRequestTypeDef",
    {
        "Id": str,
        "Version": int,
    },
)

StatusReportTypeDef = TypedDict(
    "StatusReportTypeDef",
    {
        "Status": str,
        "CheckedTime": datetime,
    },
    total=False,
)

LinkedServiceTypeDef = TypedDict(
    "LinkedServiceTypeDef",
    {
        "ServicePrincipal": str,
        "Description": str,
    },
    total=False,
)

HostedZoneOwnerTypeDef = TypedDict(
    "HostedZoneOwnerTypeDef",
    {
        "OwningAccount": str,
        "OwningService": str,
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

_RequiredListCidrBlocksRequestRequestTypeDef = TypedDict(
    "_RequiredListCidrBlocksRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListCidrBlocksRequestRequestTypeDef = TypedDict(
    "_OptionalListCidrBlocksRequestRequestTypeDef",
    {
        "LocationName": str,
        "NextToken": str,
        "MaxResults": str,
    },
    total=False,
)

class ListCidrBlocksRequestRequestTypeDef(
    _RequiredListCidrBlocksRequestRequestTypeDef, _OptionalListCidrBlocksRequestRequestTypeDef
):
    pass

ListCidrCollectionsRequestRequestTypeDef = TypedDict(
    "ListCidrCollectionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": str,
    },
    total=False,
)

_RequiredListCidrLocationsRequestRequestTypeDef = TypedDict(
    "_RequiredListCidrLocationsRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListCidrLocationsRequestRequestTypeDef = TypedDict(
    "_OptionalListCidrLocationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": str,
    },
    total=False,
)

class ListCidrLocationsRequestRequestTypeDef(
    _RequiredListCidrLocationsRequestRequestTypeDef, _OptionalListCidrLocationsRequestRequestTypeDef
):
    pass

LocationSummaryTypeDef = TypedDict(
    "LocationSummaryTypeDef",
    {
        "LocationName": str,
    },
    total=False,
)

ListGeoLocationsRequestRequestTypeDef = TypedDict(
    "ListGeoLocationsRequestRequestTypeDef",
    {
        "StartContinentCode": str,
        "StartCountryCode": str,
        "StartSubdivisionCode": str,
        "MaxItems": str,
    },
    total=False,
)

ListHealthChecksRequestRequestTypeDef = TypedDict(
    "ListHealthChecksRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListHostedZonesByNameRequestRequestTypeDef = TypedDict(
    "ListHostedZonesByNameRequestRequestTypeDef",
    {
        "DNSName": str,
        "HostedZoneId": str,
        "MaxItems": str,
    },
    total=False,
)

_RequiredListHostedZonesByVPCRequestRequestTypeDef = TypedDict(
    "_RequiredListHostedZonesByVPCRequestRequestTypeDef",
    {
        "VPCId": str,
        "VPCRegion": VPCRegionType,
    },
)
_OptionalListHostedZonesByVPCRequestRequestTypeDef = TypedDict(
    "_OptionalListHostedZonesByVPCRequestRequestTypeDef",
    {
        "MaxItems": str,
        "NextToken": str,
    },
    total=False,
)

class ListHostedZonesByVPCRequestRequestTypeDef(
    _RequiredListHostedZonesByVPCRequestRequestTypeDef,
    _OptionalListHostedZonesByVPCRequestRequestTypeDef,
):
    pass

ListHostedZonesRequestRequestTypeDef = TypedDict(
    "ListHostedZonesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
        "DelegationSetId": str,
    },
    total=False,
)

ListQueryLoggingConfigsRequestRequestTypeDef = TypedDict(
    "ListQueryLoggingConfigsRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "NextToken": str,
        "MaxResults": str,
    },
    total=False,
)

_RequiredListResourceRecordSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListResourceRecordSetsRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
)
_OptionalListResourceRecordSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListResourceRecordSetsRequestRequestTypeDef",
    {
        "StartRecordName": str,
        "StartRecordType": RRTypeType,
        "StartRecordIdentifier": str,
        "MaxItems": str,
    },
    total=False,
)

class ListResourceRecordSetsRequestRequestTypeDef(
    _RequiredListResourceRecordSetsRequestRequestTypeDef,
    _OptionalListResourceRecordSetsRequestRequestTypeDef,
):
    pass

ListReusableDelegationSetsRequestRequestTypeDef = TypedDict(
    "ListReusableDelegationSetsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceType": TagResourceTypeType,
        "ResourceId": str,
    },
)

ListTagsForResourcesRequestRequestTypeDef = TypedDict(
    "ListTagsForResourcesRequestRequestTypeDef",
    {
        "ResourceType": TagResourceTypeType,
        "ResourceIds": Sequence[str],
    },
)

ListTrafficPoliciesRequestRequestTypeDef = TypedDict(
    "ListTrafficPoliciesRequestRequestTypeDef",
    {
        "TrafficPolicyIdMarker": str,
        "MaxItems": str,
    },
    total=False,
)

TrafficPolicySummaryTypeDef = TypedDict(
    "TrafficPolicySummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Type": RRTypeType,
        "LatestVersion": int,
        "TrafficPolicyCount": int,
    },
)

_RequiredListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef = TypedDict(
    "_RequiredListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
)
_OptionalListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef = TypedDict(
    "_OptionalListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef",
    {
        "TrafficPolicyInstanceNameMarker": str,
        "TrafficPolicyInstanceTypeMarker": RRTypeType,
        "MaxItems": str,
    },
    total=False,
)

class ListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef(
    _RequiredListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef,
    _OptionalListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef,
):
    pass

_RequiredListTrafficPolicyInstancesByPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredListTrafficPolicyInstancesByPolicyRequestRequestTypeDef",
    {
        "TrafficPolicyId": str,
        "TrafficPolicyVersion": int,
    },
)
_OptionalListTrafficPolicyInstancesByPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalListTrafficPolicyInstancesByPolicyRequestRequestTypeDef",
    {
        "HostedZoneIdMarker": str,
        "TrafficPolicyInstanceNameMarker": str,
        "TrafficPolicyInstanceTypeMarker": RRTypeType,
        "MaxItems": str,
    },
    total=False,
)

class ListTrafficPolicyInstancesByPolicyRequestRequestTypeDef(
    _RequiredListTrafficPolicyInstancesByPolicyRequestRequestTypeDef,
    _OptionalListTrafficPolicyInstancesByPolicyRequestRequestTypeDef,
):
    pass

ListTrafficPolicyInstancesRequestRequestTypeDef = TypedDict(
    "ListTrafficPolicyInstancesRequestRequestTypeDef",
    {
        "HostedZoneIdMarker": str,
        "TrafficPolicyInstanceNameMarker": str,
        "TrafficPolicyInstanceTypeMarker": RRTypeType,
        "MaxItems": str,
    },
    total=False,
)

_RequiredListTrafficPolicyVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTrafficPolicyVersionsRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalListTrafficPolicyVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTrafficPolicyVersionsRequestRequestTypeDef",
    {
        "TrafficPolicyVersionMarker": str,
        "MaxItems": str,
    },
    total=False,
)

class ListTrafficPolicyVersionsRequestRequestTypeDef(
    _RequiredListTrafficPolicyVersionsRequestRequestTypeDef,
    _OptionalListTrafficPolicyVersionsRequestRequestTypeDef,
):
    pass

_RequiredListVPCAssociationAuthorizationsRequestRequestTypeDef = TypedDict(
    "_RequiredListVPCAssociationAuthorizationsRequestRequestTypeDef",
    {
        "HostedZoneId": str,
    },
)
_OptionalListVPCAssociationAuthorizationsRequestRequestTypeDef = TypedDict(
    "_OptionalListVPCAssociationAuthorizationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": str,
    },
    total=False,
)

class ListVPCAssociationAuthorizationsRequestRequestTypeDef(
    _RequiredListVPCAssociationAuthorizationsRequestRequestTypeDef,
    _OptionalListVPCAssociationAuthorizationsRequestRequestTypeDef,
):
    pass

ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "Value": str,
    },
)

_RequiredTestDNSAnswerRequestRequestTypeDef = TypedDict(
    "_RequiredTestDNSAnswerRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "RecordName": str,
        "RecordType": RRTypeType,
    },
)
_OptionalTestDNSAnswerRequestRequestTypeDef = TypedDict(
    "_OptionalTestDNSAnswerRequestRequestTypeDef",
    {
        "ResolverIP": str,
        "EDNS0ClientSubnetIP": str,
        "EDNS0ClientSubnetMask": str,
    },
    total=False,
)

class TestDNSAnswerRequestRequestTypeDef(
    _RequiredTestDNSAnswerRequestRequestTypeDef, _OptionalTestDNSAnswerRequestRequestTypeDef
):
    pass

_RequiredUpdateHostedZoneCommentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateHostedZoneCommentRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateHostedZoneCommentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateHostedZoneCommentRequestRequestTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class UpdateHostedZoneCommentRequestRequestTypeDef(
    _RequiredUpdateHostedZoneCommentRequestRequestTypeDef,
    _OptionalUpdateHostedZoneCommentRequestRequestTypeDef,
):
    pass

UpdateTrafficPolicyCommentRequestRequestTypeDef = TypedDict(
    "UpdateTrafficPolicyCommentRequestRequestTypeDef",
    {
        "Id": str,
        "Version": int,
        "Comment": str,
    },
)

UpdateTrafficPolicyInstanceRequestRequestTypeDef = TypedDict(
    "UpdateTrafficPolicyInstanceRequestRequestTypeDef",
    {
        "Id": str,
        "TTL": int,
        "TrafficPolicyId": str,
        "TrafficPolicyVersion": int,
    },
)

ActivateKeySigningKeyResponseTypeDef = TypedDict(
    "ActivateKeySigningKeyResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateVPCWithHostedZoneResponseTypeDef = TypedDict(
    "AssociateVPCWithHostedZoneResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ChangeCidrCollectionResponseTypeDef = TypedDict(
    "ChangeCidrCollectionResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ChangeResourceRecordSetsResponseTypeDef = TypedDict(
    "ChangeResourceRecordSetsResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeactivateKeySigningKeyResponseTypeDef = TypedDict(
    "DeactivateKeySigningKeyResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteHostedZoneResponseTypeDef = TypedDict(
    "DeleteHostedZoneResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteKeySigningKeyResponseTypeDef = TypedDict(
    "DeleteKeySigningKeyResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisableHostedZoneDNSSECResponseTypeDef = TypedDict(
    "DisableHostedZoneDNSSECResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateVPCFromHostedZoneResponseTypeDef = TypedDict(
    "DisassociateVPCFromHostedZoneResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableHostedZoneDNSSECResponseTypeDef = TypedDict(
    "EnableHostedZoneDNSSECResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountLimitResponseTypeDef = TypedDict(
    "GetAccountLimitResponseTypeDef",
    {
        "Limit": AccountLimitTypeDef,
        "Count": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChangeResponseTypeDef = TypedDict(
    "GetChangeResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCheckerIpRangesResponseTypeDef = TypedDict(
    "GetCheckerIpRangesResponseTypeDef",
    {
        "CheckerIpRanges": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHealthCheckCountResponseTypeDef = TypedDict(
    "GetHealthCheckCountResponseTypeDef",
    {
        "HealthCheckCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHostedZoneCountResponseTypeDef = TypedDict(
    "GetHostedZoneCountResponseTypeDef",
    {
        "HostedZoneCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrafficPolicyInstanceCountResponseTypeDef = TypedDict(
    "GetTrafficPolicyInstanceCountResponseTypeDef",
    {
        "TrafficPolicyInstanceCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestDNSAnswerResponseTypeDef = TypedDict(
    "TestDNSAnswerResponseTypeDef",
    {
        "Nameserver": str,
        "RecordName": str,
        "RecordType": RRTypeType,
        "RecordData": List[str],
        "ResponseCode": str,
        "Protocol": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
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
        "IPAddress": str,
        "Port": int,
        "ResourcePath": str,
        "FullyQualifiedDomainName": str,
        "SearchString": str,
        "RequestInterval": int,
        "FailureThreshold": int,
        "MeasureLatency": bool,
        "Inverted": bool,
        "Disabled": bool,
        "HealthThreshold": int,
        "ChildHealthChecks": Sequence[str],
        "EnableSNI": bool,
        "Regions": Sequence[HealthCheckRegionType],
        "AlarmIdentifier": AlarmIdentifierTypeDef,
        "InsufficientDataHealthStatus": InsufficientDataHealthStatusType,
        "RoutingControlArn": str,
    },
    total=False,
)

class HealthCheckConfigTypeDef(
    _RequiredHealthCheckConfigTypeDef, _OptionalHealthCheckConfigTypeDef
):
    pass

_RequiredUpdateHealthCheckRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateHealthCheckRequestRequestTypeDef",
    {
        "HealthCheckId": str,
    },
)
_OptionalUpdateHealthCheckRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateHealthCheckRequestRequestTypeDef",
    {
        "HealthCheckVersion": int,
        "IPAddress": str,
        "Port": int,
        "ResourcePath": str,
        "FullyQualifiedDomainName": str,
        "SearchString": str,
        "FailureThreshold": int,
        "Inverted": bool,
        "Disabled": bool,
        "HealthThreshold": int,
        "ChildHealthChecks": Sequence[str],
        "EnableSNI": bool,
        "Regions": Sequence[HealthCheckRegionType],
        "AlarmIdentifier": AlarmIdentifierTypeDef,
        "InsufficientDataHealthStatus": InsufficientDataHealthStatusType,
        "ResetElements": Sequence[ResettableElementNameType],
    },
    total=False,
)

class UpdateHealthCheckRequestRequestTypeDef(
    _RequiredUpdateHealthCheckRequestRequestTypeDef, _OptionalUpdateHealthCheckRequestRequestTypeDef
):
    pass

_RequiredAssociateVPCWithHostedZoneRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateVPCWithHostedZoneRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "VPC": VPCTypeDef,
    },
)
_OptionalAssociateVPCWithHostedZoneRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateVPCWithHostedZoneRequestRequestTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class AssociateVPCWithHostedZoneRequestRequestTypeDef(
    _RequiredAssociateVPCWithHostedZoneRequestRequestTypeDef,
    _OptionalAssociateVPCWithHostedZoneRequestRequestTypeDef,
):
    pass

CreateVPCAssociationAuthorizationRequestRequestTypeDef = TypedDict(
    "CreateVPCAssociationAuthorizationRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "VPC": VPCTypeDef,
    },
)

CreateVPCAssociationAuthorizationResponseTypeDef = TypedDict(
    "CreateVPCAssociationAuthorizationResponseTypeDef",
    {
        "HostedZoneId": str,
        "VPC": VPCTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVPCAssociationAuthorizationRequestRequestTypeDef = TypedDict(
    "DeleteVPCAssociationAuthorizationRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "VPC": VPCTypeDef,
    },
)

_RequiredDisassociateVPCFromHostedZoneRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateVPCFromHostedZoneRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "VPC": VPCTypeDef,
    },
)
_OptionalDisassociateVPCFromHostedZoneRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateVPCFromHostedZoneRequestRequestTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class DisassociateVPCFromHostedZoneRequestRequestTypeDef(
    _RequiredDisassociateVPCFromHostedZoneRequestRequestTypeDef,
    _OptionalDisassociateVPCFromHostedZoneRequestRequestTypeDef,
):
    pass

ListVPCAssociationAuthorizationsResponseTypeDef = TypedDict(
    "ListVPCAssociationAuthorizationsResponseTypeDef",
    {
        "HostedZoneId": str,
        "NextToken": str,
        "VPCs": List[VPCTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredChangeCidrCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredChangeCidrCollectionRequestRequestTypeDef",
    {
        "Id": str,
        "Changes": Sequence[CidrCollectionChangeTypeDef],
    },
)
_OptionalChangeCidrCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalChangeCidrCollectionRequestRequestTypeDef",
    {
        "CollectionVersion": int,
    },
    total=False,
)

class ChangeCidrCollectionRequestRequestTypeDef(
    _RequiredChangeCidrCollectionRequestRequestTypeDef,
    _OptionalChangeCidrCollectionRequestRequestTypeDef,
):
    pass

_RequiredChangeTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredChangeTagsForResourceRequestRequestTypeDef",
    {
        "ResourceType": TagResourceTypeType,
        "ResourceId": str,
    },
)
_OptionalChangeTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalChangeTagsForResourceRequestRequestTypeDef",
    {
        "AddTags": Sequence[TagTypeDef],
        "RemoveTagKeys": Sequence[str],
    },
    total=False,
)

class ChangeTagsForResourceRequestRequestTypeDef(
    _RequiredChangeTagsForResourceRequestRequestTypeDef,
    _OptionalChangeTagsForResourceRequestRequestTypeDef,
):
    pass

ResourceTagSetTypeDef = TypedDict(
    "ResourceTagSetTypeDef",
    {
        "ResourceType": TagResourceTypeType,
        "ResourceId": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

ListCidrBlocksResponseTypeDef = TypedDict(
    "ListCidrBlocksResponseTypeDef",
    {
        "NextToken": str,
        "CidrBlocks": List[CidrBlockSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCidrCollectionResponseTypeDef = TypedDict(
    "CreateCidrCollectionResponseTypeDef",
    {
        "Collection": CidrCollectionTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCloudWatchAlarmConfigurationTypeDef = TypedDict(
    "_RequiredCloudWatchAlarmConfigurationTypeDef",
    {
        "EvaluationPeriods": int,
        "Threshold": float,
        "ComparisonOperator": ComparisonOperatorType,
        "Period": int,
        "MetricName": str,
        "Namespace": str,
        "Statistic": StatisticType,
    },
)
_OptionalCloudWatchAlarmConfigurationTypeDef = TypedDict(
    "_OptionalCloudWatchAlarmConfigurationTypeDef",
    {
        "Dimensions": List[DimensionTypeDef],
    },
    total=False,
)

class CloudWatchAlarmConfigurationTypeDef(
    _RequiredCloudWatchAlarmConfigurationTypeDef, _OptionalCloudWatchAlarmConfigurationTypeDef
):
    pass

ListCidrCollectionsResponseTypeDef = TypedDict(
    "ListCidrCollectionsResponseTypeDef",
    {
        "NextToken": str,
        "CidrCollections": List[CollectionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateHostedZoneRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHostedZoneRequestRequestTypeDef",
    {
        "Name": str,
        "CallerReference": str,
    },
)
_OptionalCreateHostedZoneRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHostedZoneRequestRequestTypeDef",
    {
        "VPC": VPCTypeDef,
        "HostedZoneConfig": HostedZoneConfigTypeDef,
        "DelegationSetId": str,
    },
    total=False,
)

class CreateHostedZoneRequestRequestTypeDef(
    _RequiredCreateHostedZoneRequestRequestTypeDef, _OptionalCreateHostedZoneRequestRequestTypeDef
):
    pass

CreateReusableDelegationSetResponseTypeDef = TypedDict(
    "CreateReusableDelegationSetResponseTypeDef",
    {
        "DelegationSet": DelegationSetTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReusableDelegationSetResponseTypeDef = TypedDict(
    "GetReusableDelegationSetResponseTypeDef",
    {
        "DelegationSet": DelegationSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReusableDelegationSetsResponseTypeDef = TypedDict(
    "ListReusableDelegationSetsResponseTypeDef",
    {
        "DelegationSets": List[DelegationSetTypeDef],
        "Marker": str,
        "IsTruncated": bool,
        "NextMarker": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKeySigningKeyResponseTypeDef = TypedDict(
    "CreateKeySigningKeyResponseTypeDef",
    {
        "ChangeInfo": ChangeInfoTypeDef,
        "KeySigningKey": KeySigningKeyTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateQueryLoggingConfigResponseTypeDef = TypedDict(
    "CreateQueryLoggingConfigResponseTypeDef",
    {
        "QueryLoggingConfig": QueryLoggingConfigTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueryLoggingConfigResponseTypeDef = TypedDict(
    "GetQueryLoggingConfigResponseTypeDef",
    {
        "QueryLoggingConfig": QueryLoggingConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueryLoggingConfigsResponseTypeDef = TypedDict(
    "ListQueryLoggingConfigsResponseTypeDef",
    {
        "QueryLoggingConfigs": List[QueryLoggingConfigTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrafficPolicyInstanceResponseTypeDef = TypedDict(
    "CreateTrafficPolicyInstanceResponseTypeDef",
    {
        "TrafficPolicyInstance": TrafficPolicyInstanceTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrafficPolicyInstanceResponseTypeDef = TypedDict(
    "GetTrafficPolicyInstanceResponseTypeDef",
    {
        "TrafficPolicyInstance": TrafficPolicyInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrafficPolicyInstancesByHostedZoneResponseTypeDef = TypedDict(
    "ListTrafficPolicyInstancesByHostedZoneResponseTypeDef",
    {
        "TrafficPolicyInstances": List[TrafficPolicyInstanceTypeDef],
        "TrafficPolicyInstanceNameMarker": str,
        "TrafficPolicyInstanceTypeMarker": RRTypeType,
        "IsTruncated": bool,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrafficPolicyInstancesByPolicyResponseTypeDef = TypedDict(
    "ListTrafficPolicyInstancesByPolicyResponseTypeDef",
    {
        "TrafficPolicyInstances": List[TrafficPolicyInstanceTypeDef],
        "HostedZoneIdMarker": str,
        "TrafficPolicyInstanceNameMarker": str,
        "TrafficPolicyInstanceTypeMarker": RRTypeType,
        "IsTruncated": bool,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrafficPolicyInstancesResponseTypeDef = TypedDict(
    "ListTrafficPolicyInstancesResponseTypeDef",
    {
        "TrafficPolicyInstances": List[TrafficPolicyInstanceTypeDef],
        "HostedZoneIdMarker": str,
        "TrafficPolicyInstanceNameMarker": str,
        "TrafficPolicyInstanceTypeMarker": RRTypeType,
        "IsTruncated": bool,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTrafficPolicyInstanceResponseTypeDef = TypedDict(
    "UpdateTrafficPolicyInstanceResponseTypeDef",
    {
        "TrafficPolicyInstance": TrafficPolicyInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrafficPolicyResponseTypeDef = TypedDict(
    "CreateTrafficPolicyResponseTypeDef",
    {
        "TrafficPolicy": TrafficPolicyTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrafficPolicyVersionResponseTypeDef = TypedDict(
    "CreateTrafficPolicyVersionResponseTypeDef",
    {
        "TrafficPolicy": TrafficPolicyTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrafficPolicyResponseTypeDef = TypedDict(
    "GetTrafficPolicyResponseTypeDef",
    {
        "TrafficPolicy": TrafficPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrafficPolicyVersionsResponseTypeDef = TypedDict(
    "ListTrafficPolicyVersionsResponseTypeDef",
    {
        "TrafficPolicies": List[TrafficPolicyTypeDef],
        "IsTruncated": bool,
        "TrafficPolicyVersionMarker": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTrafficPolicyCommentResponseTypeDef = TypedDict(
    "UpdateTrafficPolicyCommentResponseTypeDef",
    {
        "TrafficPolicy": TrafficPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDNSSECResponseTypeDef = TypedDict(
    "GetDNSSECResponseTypeDef",
    {
        "Status": DNSSECStatusTypeDef,
        "KeySigningKeys": List[KeySigningKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGeoLocationResponseTypeDef = TypedDict(
    "GetGeoLocationResponseTypeDef",
    {
        "GeoLocationDetails": GeoLocationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGeoLocationsResponseTypeDef = TypedDict(
    "ListGeoLocationsResponseTypeDef",
    {
        "GeoLocationDetailsList": List[GeoLocationDetailsTypeDef],
        "IsTruncated": bool,
        "NextContinentCode": str,
        "NextCountryCode": str,
        "NextSubdivisionCode": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetChangeRequestResourceRecordSetsChangedWaitTypeDef = TypedDict(
    "_RequiredGetChangeRequestResourceRecordSetsChangedWaitTypeDef",
    {
        "Id": str,
    },
)
_OptionalGetChangeRequestResourceRecordSetsChangedWaitTypeDef = TypedDict(
    "_OptionalGetChangeRequestResourceRecordSetsChangedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetChangeRequestResourceRecordSetsChangedWaitTypeDef(
    _RequiredGetChangeRequestResourceRecordSetsChangedWaitTypeDef,
    _OptionalGetChangeRequestResourceRecordSetsChangedWaitTypeDef,
):
    pass

GetHostedZoneLimitResponseTypeDef = TypedDict(
    "GetHostedZoneLimitResponseTypeDef",
    {
        "Limit": HostedZoneLimitTypeDef,
        "Count": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReusableDelegationSetLimitResponseTypeDef = TypedDict(
    "GetReusableDelegationSetLimitResponseTypeDef",
    {
        "Limit": ReusableDelegationSetLimitTypeDef,
        "Count": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HealthCheckObservationTypeDef = TypedDict(
    "HealthCheckObservationTypeDef",
    {
        "Region": HealthCheckRegionType,
        "IPAddress": str,
        "StatusReport": StatusReportTypeDef,
    },
    total=False,
)

_RequiredHostedZoneTypeDef = TypedDict(
    "_RequiredHostedZoneTypeDef",
    {
        "Id": str,
        "Name": str,
        "CallerReference": str,
    },
)
_OptionalHostedZoneTypeDef = TypedDict(
    "_OptionalHostedZoneTypeDef",
    {
        "Config": HostedZoneConfigTypeDef,
        "ResourceRecordSetCount": int,
        "LinkedService": LinkedServiceTypeDef,
    },
    total=False,
)

class HostedZoneTypeDef(_RequiredHostedZoneTypeDef, _OptionalHostedZoneTypeDef):
    pass

HostedZoneSummaryTypeDef = TypedDict(
    "HostedZoneSummaryTypeDef",
    {
        "HostedZoneId": str,
        "Name": str,
        "Owner": HostedZoneOwnerTypeDef,
    },
)

_RequiredListCidrBlocksRequestListCidrBlocksPaginateTypeDef = TypedDict(
    "_RequiredListCidrBlocksRequestListCidrBlocksPaginateTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListCidrBlocksRequestListCidrBlocksPaginateTypeDef = TypedDict(
    "_OptionalListCidrBlocksRequestListCidrBlocksPaginateTypeDef",
    {
        "LocationName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListCidrBlocksRequestListCidrBlocksPaginateTypeDef(
    _RequiredListCidrBlocksRequestListCidrBlocksPaginateTypeDef,
    _OptionalListCidrBlocksRequestListCidrBlocksPaginateTypeDef,
):
    pass

ListCidrCollectionsRequestListCidrCollectionsPaginateTypeDef = TypedDict(
    "ListCidrCollectionsRequestListCidrCollectionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListCidrLocationsRequestListCidrLocationsPaginateTypeDef = TypedDict(
    "_RequiredListCidrLocationsRequestListCidrLocationsPaginateTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListCidrLocationsRequestListCidrLocationsPaginateTypeDef = TypedDict(
    "_OptionalListCidrLocationsRequestListCidrLocationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListCidrLocationsRequestListCidrLocationsPaginateTypeDef(
    _RequiredListCidrLocationsRequestListCidrLocationsPaginateTypeDef,
    _OptionalListCidrLocationsRequestListCidrLocationsPaginateTypeDef,
):
    pass

ListHealthChecksRequestListHealthChecksPaginateTypeDef = TypedDict(
    "ListHealthChecksRequestListHealthChecksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListHostedZonesRequestListHostedZonesPaginateTypeDef = TypedDict(
    "ListHostedZonesRequestListHostedZonesPaginateTypeDef",
    {
        "DelegationSetId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListQueryLoggingConfigsRequestListQueryLoggingConfigsPaginateTypeDef = TypedDict(
    "ListQueryLoggingConfigsRequestListQueryLoggingConfigsPaginateTypeDef",
    {
        "HostedZoneId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef = TypedDict(
    "_RequiredListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef",
    {
        "HostedZoneId": str,
    },
)
_OptionalListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef = TypedDict(
    "_OptionalListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef(
    _RequiredListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef,
    _OptionalListResourceRecordSetsRequestListResourceRecordSetsPaginateTypeDef,
):
    pass

_RequiredListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef = TypedDict(
    "_RequiredListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef",
    {
        "HostedZoneId": str,
    },
)
_OptionalListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef = TypedDict(
    "_OptionalListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef",
    {
        "MaxResults": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef(
    _RequiredListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef,
    _OptionalListVPCAssociationAuthorizationsRequestListVPCAssociationAuthorizationsPaginateTypeDef,
):
    pass

ListCidrLocationsResponseTypeDef = TypedDict(
    "ListCidrLocationsResponseTypeDef",
    {
        "NextToken": str,
        "CidrLocations": List[LocationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrafficPoliciesResponseTypeDef = TypedDict(
    "ListTrafficPoliciesResponseTypeDef",
    {
        "TrafficPolicySummaries": List[TrafficPolicySummaryTypeDef],
        "IsTruncated": bool,
        "TrafficPolicyIdMarker": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredResourceRecordSetTypeDef = TypedDict(
    "_RequiredResourceRecordSetTypeDef",
    {
        "Name": str,
        "Type": RRTypeType,
    },
)
_OptionalResourceRecordSetTypeDef = TypedDict(
    "_OptionalResourceRecordSetTypeDef",
    {
        "SetIdentifier": str,
        "Weight": int,
        "Region": ResourceRecordSetRegionType,
        "GeoLocation": GeoLocationTypeDef,
        "Failover": ResourceRecordSetFailoverType,
        "MultiValueAnswer": bool,
        "TTL": int,
        "ResourceRecords": Sequence[ResourceRecordTypeDef],
        "AliasTarget": AliasTargetTypeDef,
        "HealthCheckId": str,
        "TrafficPolicyInstanceId": str,
        "CidrRoutingConfig": CidrRoutingConfigTypeDef,
    },
    total=False,
)

class ResourceRecordSetTypeDef(
    _RequiredResourceRecordSetTypeDef, _OptionalResourceRecordSetTypeDef
):
    pass

CreateHealthCheckRequestRequestTypeDef = TypedDict(
    "CreateHealthCheckRequestRequestTypeDef",
    {
        "CallerReference": str,
        "HealthCheckConfig": HealthCheckConfigTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceTagSet": ResourceTagSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourcesResponseTypeDef = TypedDict(
    "ListTagsForResourcesResponseTypeDef",
    {
        "ResourceTagSets": List[ResourceTagSetTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredHealthCheckTypeDef = TypedDict(
    "_RequiredHealthCheckTypeDef",
    {
        "Id": str,
        "CallerReference": str,
        "HealthCheckConfig": HealthCheckConfigTypeDef,
        "HealthCheckVersion": int,
    },
)
_OptionalHealthCheckTypeDef = TypedDict(
    "_OptionalHealthCheckTypeDef",
    {
        "LinkedService": LinkedServiceTypeDef,
        "CloudWatchAlarmConfiguration": CloudWatchAlarmConfigurationTypeDef,
    },
    total=False,
)

class HealthCheckTypeDef(_RequiredHealthCheckTypeDef, _OptionalHealthCheckTypeDef):
    pass

GetHealthCheckLastFailureReasonResponseTypeDef = TypedDict(
    "GetHealthCheckLastFailureReasonResponseTypeDef",
    {
        "HealthCheckObservations": List[HealthCheckObservationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHealthCheckStatusResponseTypeDef = TypedDict(
    "GetHealthCheckStatusResponseTypeDef",
    {
        "HealthCheckObservations": List[HealthCheckObservationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHostedZoneResponseTypeDef = TypedDict(
    "CreateHostedZoneResponseTypeDef",
    {
        "HostedZone": HostedZoneTypeDef,
        "ChangeInfo": ChangeInfoTypeDef,
        "DelegationSet": DelegationSetTypeDef,
        "VPC": VPCTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHostedZoneResponseTypeDef = TypedDict(
    "GetHostedZoneResponseTypeDef",
    {
        "HostedZone": HostedZoneTypeDef,
        "DelegationSet": DelegationSetTypeDef,
        "VPCs": List[VPCTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHostedZonesByNameResponseTypeDef = TypedDict(
    "ListHostedZonesByNameResponseTypeDef",
    {
        "HostedZones": List[HostedZoneTypeDef],
        "DNSName": str,
        "HostedZoneId": str,
        "IsTruncated": bool,
        "NextDNSName": str,
        "NextHostedZoneId": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHostedZonesResponseTypeDef = TypedDict(
    "ListHostedZonesResponseTypeDef",
    {
        "HostedZones": List[HostedZoneTypeDef],
        "Marker": str,
        "IsTruncated": bool,
        "NextMarker": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateHostedZoneCommentResponseTypeDef = TypedDict(
    "UpdateHostedZoneCommentResponseTypeDef",
    {
        "HostedZone": HostedZoneTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHostedZonesByVPCResponseTypeDef = TypedDict(
    "ListHostedZonesByVPCResponseTypeDef",
    {
        "HostedZoneSummaries": List[HostedZoneSummaryTypeDef],
        "MaxItems": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ChangeTypeDef = TypedDict(
    "ChangeTypeDef",
    {
        "Action": ChangeActionType,
        "ResourceRecordSet": ResourceRecordSetTypeDef,
    },
)

ListResourceRecordSetsResponseTypeDef = TypedDict(
    "ListResourceRecordSetsResponseTypeDef",
    {
        "ResourceRecordSets": List[ResourceRecordSetTypeDef],
        "IsTruncated": bool,
        "NextRecordName": str,
        "NextRecordType": RRTypeType,
        "NextRecordIdentifier": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHealthCheckResponseTypeDef = TypedDict(
    "CreateHealthCheckResponseTypeDef",
    {
        "HealthCheck": HealthCheckTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHealthCheckResponseTypeDef = TypedDict(
    "GetHealthCheckResponseTypeDef",
    {
        "HealthCheck": HealthCheckTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHealthChecksResponseTypeDef = TypedDict(
    "ListHealthChecksResponseTypeDef",
    {
        "HealthChecks": List[HealthCheckTypeDef],
        "Marker": str,
        "IsTruncated": bool,
        "NextMarker": str,
        "MaxItems": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateHealthCheckResponseTypeDef = TypedDict(
    "UpdateHealthCheckResponseTypeDef",
    {
        "HealthCheck": HealthCheckTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredChangeBatchTypeDef = TypedDict(
    "_RequiredChangeBatchTypeDef",
    {
        "Changes": Sequence[ChangeTypeDef],
    },
)
_OptionalChangeBatchTypeDef = TypedDict(
    "_OptionalChangeBatchTypeDef",
    {
        "Comment": str,
    },
    total=False,
)

class ChangeBatchTypeDef(_RequiredChangeBatchTypeDef, _OptionalChangeBatchTypeDef):
    pass

ChangeResourceRecordSetsRequestRequestTypeDef = TypedDict(
    "ChangeResourceRecordSetsRequestRequestTypeDef",
    {
        "HostedZoneId": str,
        "ChangeBatch": ChangeBatchTypeDef,
    },
)
