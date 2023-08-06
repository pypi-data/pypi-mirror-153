"""
Type annotations for ds service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds/type_defs/)

Usage::

    ```python
    from mypy_boto3_ds.type_defs import AcceptSharedDirectoryRequestRequestTypeDef

    data: AcceptSharedDirectoryRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    CertificateStateType,
    CertificateTypeType,
    ClientAuthenticationStatusType,
    DirectoryEditionType,
    DirectorySizeType,
    DirectoryStageType,
    DirectoryTypeType,
    DomainControllerStatusType,
    IpRouteStatusMsgType,
    LDAPSStatusType,
    RadiusAuthenticationProtocolType,
    RadiusStatusType,
    RegionTypeType,
    SchemaExtensionStatusType,
    SelectiveAuthType,
    ShareMethodType,
    ShareStatusType,
    SnapshotStatusType,
    SnapshotTypeType,
    TopicStatusType,
    TrustDirectionType,
    TrustStateType,
    TrustTypeType,
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
    "AcceptSharedDirectoryRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SharedDirectoryTypeDef",
    "IpRouteTypeDef",
    "DirectoryVpcSettingsTypeDef",
    "TagTypeDef",
    "AttributeTypeDef",
    "CancelSchemaExtensionRequestRequestTypeDef",
    "CertificateInfoTypeDef",
    "ClientCertAuthSettingsTypeDef",
    "ClientAuthenticationSettingInfoTypeDef",
    "ConditionalForwarderTypeDef",
    "DirectoryConnectSettingsTypeDef",
    "CreateAliasRequestRequestTypeDef",
    "CreateConditionalForwarderRequestRequestTypeDef",
    "CreateLogSubscriptionRequestRequestTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateTrustRequestRequestTypeDef",
    "DeleteConditionalForwarderRequestRequestTypeDef",
    "DeleteDirectoryRequestRequestTypeDef",
    "DeleteLogSubscriptionRequestRequestTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteTrustRequestRequestTypeDef",
    "DeregisterCertificateRequestRequestTypeDef",
    "DeregisterEventTopicRequestRequestTypeDef",
    "DescribeCertificateRequestRequestTypeDef",
    "DescribeClientAuthenticationSettingsRequestRequestTypeDef",
    "DescribeConditionalForwardersRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDirectoriesRequestRequestTypeDef",
    "DescribeDomainControllersRequestRequestTypeDef",
    "DomainControllerTypeDef",
    "DescribeEventTopicsRequestRequestTypeDef",
    "EventTopicTypeDef",
    "DescribeLDAPSSettingsRequestRequestTypeDef",
    "LDAPSSettingInfoTypeDef",
    "DescribeRegionsRequestRequestTypeDef",
    "DescribeSharedDirectoriesRequestRequestTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "SnapshotTypeDef",
    "DescribeTrustsRequestRequestTypeDef",
    "TrustTypeDef",
    "DirectoryConnectSettingsDescriptionTypeDef",
    "DirectoryVpcSettingsDescriptionTypeDef",
    "RadiusSettingsTypeDef",
    "RegionsInfoTypeDef",
    "DirectoryLimitsTypeDef",
    "DisableClientAuthenticationRequestRequestTypeDef",
    "DisableLDAPSRequestRequestTypeDef",
    "DisableRadiusRequestRequestTypeDef",
    "DisableSsoRequestRequestTypeDef",
    "EnableClientAuthenticationRequestRequestTypeDef",
    "EnableLDAPSRequestRequestTypeDef",
    "EnableSsoRequestRequestTypeDef",
    "GetSnapshotLimitsRequestRequestTypeDef",
    "SnapshotLimitsTypeDef",
    "IpRouteInfoTypeDef",
    "ListCertificatesRequestRequestTypeDef",
    "ListIpRoutesRequestRequestTypeDef",
    "ListLogSubscriptionsRequestRequestTypeDef",
    "LogSubscriptionTypeDef",
    "ListSchemaExtensionsRequestRequestTypeDef",
    "SchemaExtensionInfoTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RegisterEventTopicRequestRequestTypeDef",
    "RejectSharedDirectoryRequestRequestTypeDef",
    "RemoveIpRoutesRequestRequestTypeDef",
    "RemoveRegionRequestRequestTypeDef",
    "RemoveTagsFromResourceRequestRequestTypeDef",
    "ResetUserPasswordRequestRequestTypeDef",
    "RestoreFromSnapshotRequestRequestTypeDef",
    "ShareTargetTypeDef",
    "StartSchemaExtensionRequestRequestTypeDef",
    "UnshareTargetTypeDef",
    "UpdateConditionalForwarderRequestRequestTypeDef",
    "UpdateNumberOfDomainControllersRequestRequestTypeDef",
    "UpdateTrustRequestRequestTypeDef",
    "VerifyTrustRequestRequestTypeDef",
    "ConnectDirectoryResultTypeDef",
    "CreateAliasResultTypeDef",
    "CreateDirectoryResultTypeDef",
    "CreateMicrosoftADResultTypeDef",
    "CreateSnapshotResultTypeDef",
    "CreateTrustResultTypeDef",
    "DeleteDirectoryResultTypeDef",
    "DeleteSnapshotResultTypeDef",
    "DeleteTrustResultTypeDef",
    "RegisterCertificateResultTypeDef",
    "RejectSharedDirectoryResultTypeDef",
    "ShareDirectoryResultTypeDef",
    "StartSchemaExtensionResultTypeDef",
    "UnshareDirectoryResultTypeDef",
    "UpdateTrustResultTypeDef",
    "VerifyTrustResultTypeDef",
    "AcceptSharedDirectoryResultTypeDef",
    "DescribeSharedDirectoriesResultTypeDef",
    "AddIpRoutesRequestRequestTypeDef",
    "AddRegionRequestRequestTypeDef",
    "RegionDescriptionTypeDef",
    "AddTagsToResourceRequestRequestTypeDef",
    "CreateDirectoryRequestRequestTypeDef",
    "CreateMicrosoftADRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "ComputerTypeDef",
    "CreateComputerRequestRequestTypeDef",
    "ListCertificatesResultTypeDef",
    "CertificateTypeDef",
    "RegisterCertificateRequestRequestTypeDef",
    "DescribeClientAuthenticationSettingsResultTypeDef",
    "DescribeConditionalForwardersResultTypeDef",
    "ConnectDirectoryRequestRequestTypeDef",
    "DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef",
    "DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef",
    "DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef",
    "DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef",
    "DescribeTrustsRequestDescribeTrustsPaginateTypeDef",
    "ListIpRoutesRequestListIpRoutesPaginateTypeDef",
    "ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef",
    "ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "DescribeDomainControllersResultTypeDef",
    "DescribeEventTopicsResultTypeDef",
    "DescribeLDAPSSettingsResultTypeDef",
    "DescribeSnapshotsResultTypeDef",
    "DescribeTrustsResultTypeDef",
    "EnableRadiusRequestRequestTypeDef",
    "OwnerDirectoryDescriptionTypeDef",
    "UpdateRadiusRequestRequestTypeDef",
    "GetDirectoryLimitsResultTypeDef",
    "GetSnapshotLimitsResultTypeDef",
    "ListIpRoutesResultTypeDef",
    "ListLogSubscriptionsResultTypeDef",
    "ListSchemaExtensionsResultTypeDef",
    "ShareDirectoryRequestRequestTypeDef",
    "UnshareDirectoryRequestRequestTypeDef",
    "DescribeRegionsResultTypeDef",
    "CreateComputerResultTypeDef",
    "DescribeCertificateResultTypeDef",
    "DirectoryDescriptionTypeDef",
    "DescribeDirectoriesResultTypeDef",
)

AcceptSharedDirectoryRequestRequestTypeDef = TypedDict(
    "AcceptSharedDirectoryRequestRequestTypeDef",
    {
        "SharedDirectoryId": str,
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

SharedDirectoryTypeDef = TypedDict(
    "SharedDirectoryTypeDef",
    {
        "OwnerAccountId": str,
        "OwnerDirectoryId": str,
        "ShareMethod": ShareMethodType,
        "SharedAccountId": str,
        "SharedDirectoryId": str,
        "ShareStatus": ShareStatusType,
        "ShareNotes": str,
        "CreatedDateTime": datetime,
        "LastUpdatedDateTime": datetime,
    },
    total=False,
)

IpRouteTypeDef = TypedDict(
    "IpRouteTypeDef",
    {
        "CidrIp": str,
        "Description": str,
    },
    total=False,
)

DirectoryVpcSettingsTypeDef = TypedDict(
    "DirectoryVpcSettingsTypeDef",
    {
        "VpcId": str,
        "SubnetIds": Sequence[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

CancelSchemaExtensionRequestRequestTypeDef = TypedDict(
    "CancelSchemaExtensionRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "SchemaExtensionId": str,
    },
)

CertificateInfoTypeDef = TypedDict(
    "CertificateInfoTypeDef",
    {
        "CertificateId": str,
        "CommonName": str,
        "State": CertificateStateType,
        "ExpiryDateTime": datetime,
        "Type": CertificateTypeType,
    },
    total=False,
)

ClientCertAuthSettingsTypeDef = TypedDict(
    "ClientCertAuthSettingsTypeDef",
    {
        "OCSPUrl": str,
    },
    total=False,
)

ClientAuthenticationSettingInfoTypeDef = TypedDict(
    "ClientAuthenticationSettingInfoTypeDef",
    {
        "Type": Literal["SmartCard"],
        "Status": ClientAuthenticationStatusType,
        "LastUpdatedDateTime": datetime,
    },
    total=False,
)

ConditionalForwarderTypeDef = TypedDict(
    "ConditionalForwarderTypeDef",
    {
        "RemoteDomainName": str,
        "DnsIpAddrs": List[str],
        "ReplicationScope": Literal["Domain"],
    },
    total=False,
)

DirectoryConnectSettingsTypeDef = TypedDict(
    "DirectoryConnectSettingsTypeDef",
    {
        "VpcId": str,
        "SubnetIds": Sequence[str],
        "CustomerDnsIps": Sequence[str],
        "CustomerUserName": str,
    },
)

CreateAliasRequestRequestTypeDef = TypedDict(
    "CreateAliasRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Alias": str,
    },
)

CreateConditionalForwarderRequestRequestTypeDef = TypedDict(
    "CreateConditionalForwarderRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RemoteDomainName": str,
        "DnsIpAddrs": Sequence[str],
    },
)

CreateLogSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateLogSubscriptionRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "LogGroupName": str,
    },
)

_RequiredCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class CreateSnapshotRequestRequestTypeDef(
    _RequiredCreateSnapshotRequestRequestTypeDef, _OptionalCreateSnapshotRequestRequestTypeDef
):
    pass


_RequiredCreateTrustRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrustRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RemoteDomainName": str,
        "TrustPassword": str,
        "TrustDirection": TrustDirectionType,
    },
)
_OptionalCreateTrustRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrustRequestRequestTypeDef",
    {
        "TrustType": TrustTypeType,
        "ConditionalForwarderIpAddrs": Sequence[str],
        "SelectiveAuth": SelectiveAuthType,
    },
    total=False,
)


class CreateTrustRequestRequestTypeDef(
    _RequiredCreateTrustRequestRequestTypeDef, _OptionalCreateTrustRequestRequestTypeDef
):
    pass


DeleteConditionalForwarderRequestRequestTypeDef = TypedDict(
    "DeleteConditionalForwarderRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RemoteDomainName": str,
    },
)

DeleteDirectoryRequestRequestTypeDef = TypedDict(
    "DeleteDirectoryRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)

DeleteLogSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteLogSubscriptionRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)

DeleteSnapshotRequestRequestTypeDef = TypedDict(
    "DeleteSnapshotRequestRequestTypeDef",
    {
        "SnapshotId": str,
    },
)

_RequiredDeleteTrustRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTrustRequestRequestTypeDef",
    {
        "TrustId": str,
    },
)
_OptionalDeleteTrustRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTrustRequestRequestTypeDef",
    {
        "DeleteAssociatedConditionalForwarder": bool,
    },
    total=False,
)


class DeleteTrustRequestRequestTypeDef(
    _RequiredDeleteTrustRequestRequestTypeDef, _OptionalDeleteTrustRequestRequestTypeDef
):
    pass


DeregisterCertificateRequestRequestTypeDef = TypedDict(
    "DeregisterCertificateRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "CertificateId": str,
    },
)

DeregisterEventTopicRequestRequestTypeDef = TypedDict(
    "DeregisterEventTopicRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "TopicName": str,
    },
)

DescribeCertificateRequestRequestTypeDef = TypedDict(
    "DescribeCertificateRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "CertificateId": str,
    },
)

_RequiredDescribeClientAuthenticationSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeClientAuthenticationSettingsRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDescribeClientAuthenticationSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeClientAuthenticationSettingsRequestRequestTypeDef",
    {
        "Type": Literal["SmartCard"],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class DescribeClientAuthenticationSettingsRequestRequestTypeDef(
    _RequiredDescribeClientAuthenticationSettingsRequestRequestTypeDef,
    _OptionalDescribeClientAuthenticationSettingsRequestRequestTypeDef,
):
    pass


_RequiredDescribeConditionalForwardersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeConditionalForwardersRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDescribeConditionalForwardersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeConditionalForwardersRequestRequestTypeDef",
    {
        "RemoteDomainNames": Sequence[str],
    },
    total=False,
)


class DescribeConditionalForwardersRequestRequestTypeDef(
    _RequiredDescribeConditionalForwardersRequestRequestTypeDef,
    _OptionalDescribeConditionalForwardersRequestRequestTypeDef,
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

DescribeDirectoriesRequestRequestTypeDef = TypedDict(
    "DescribeDirectoriesRequestRequestTypeDef",
    {
        "DirectoryIds": Sequence[str],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

_RequiredDescribeDomainControllersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDomainControllersRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDescribeDomainControllersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDomainControllersRequestRequestTypeDef",
    {
        "DomainControllerIds": Sequence[str],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class DescribeDomainControllersRequestRequestTypeDef(
    _RequiredDescribeDomainControllersRequestRequestTypeDef,
    _OptionalDescribeDomainControllersRequestRequestTypeDef,
):
    pass


DomainControllerTypeDef = TypedDict(
    "DomainControllerTypeDef",
    {
        "DirectoryId": str,
        "DomainControllerId": str,
        "DnsIpAddr": str,
        "VpcId": str,
        "SubnetId": str,
        "AvailabilityZone": str,
        "Status": DomainControllerStatusType,
        "StatusReason": str,
        "LaunchTime": datetime,
        "StatusLastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeEventTopicsRequestRequestTypeDef = TypedDict(
    "DescribeEventTopicsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "TopicNames": Sequence[str],
    },
    total=False,
)

EventTopicTypeDef = TypedDict(
    "EventTopicTypeDef",
    {
        "DirectoryId": str,
        "TopicName": str,
        "TopicArn": str,
        "CreatedDateTime": datetime,
        "Status": TopicStatusType,
    },
    total=False,
)

_RequiredDescribeLDAPSSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeLDAPSSettingsRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDescribeLDAPSSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeLDAPSSettingsRequestRequestTypeDef",
    {
        "Type": Literal["Client"],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class DescribeLDAPSSettingsRequestRequestTypeDef(
    _RequiredDescribeLDAPSSettingsRequestRequestTypeDef,
    _OptionalDescribeLDAPSSettingsRequestRequestTypeDef,
):
    pass


LDAPSSettingInfoTypeDef = TypedDict(
    "LDAPSSettingInfoTypeDef",
    {
        "LDAPSStatus": LDAPSStatusType,
        "LDAPSStatusReason": str,
        "LastUpdatedDateTime": datetime,
    },
    total=False,
)

_RequiredDescribeRegionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRegionsRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDescribeRegionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRegionsRequestRequestTypeDef",
    {
        "RegionName": str,
        "NextToken": str,
    },
    total=False,
)


class DescribeRegionsRequestRequestTypeDef(
    _RequiredDescribeRegionsRequestRequestTypeDef, _OptionalDescribeRegionsRequestRequestTypeDef
):
    pass


_RequiredDescribeSharedDirectoriesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSharedDirectoriesRequestRequestTypeDef",
    {
        "OwnerDirectoryId": str,
    },
)
_OptionalDescribeSharedDirectoriesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSharedDirectoriesRequestRequestTypeDef",
    {
        "SharedDirectoryIds": Sequence[str],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class DescribeSharedDirectoriesRequestRequestTypeDef(
    _RequiredDescribeSharedDirectoriesRequestRequestTypeDef,
    _OptionalDescribeSharedDirectoriesRequestRequestTypeDef,
):
    pass


DescribeSnapshotsRequestRequestTypeDef = TypedDict(
    "DescribeSnapshotsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "SnapshotIds": Sequence[str],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "DirectoryId": str,
        "SnapshotId": str,
        "Type": SnapshotTypeType,
        "Name": str,
        "Status": SnapshotStatusType,
        "StartTime": datetime,
    },
    total=False,
)

DescribeTrustsRequestRequestTypeDef = TypedDict(
    "DescribeTrustsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "TrustIds": Sequence[str],
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

TrustTypeDef = TypedDict(
    "TrustTypeDef",
    {
        "DirectoryId": str,
        "TrustId": str,
        "RemoteDomainName": str,
        "TrustType": TrustTypeType,
        "TrustDirection": TrustDirectionType,
        "TrustState": TrustStateType,
        "CreatedDateTime": datetime,
        "LastUpdatedDateTime": datetime,
        "StateLastUpdatedDateTime": datetime,
        "TrustStateReason": str,
        "SelectiveAuth": SelectiveAuthType,
    },
    total=False,
)

DirectoryConnectSettingsDescriptionTypeDef = TypedDict(
    "DirectoryConnectSettingsDescriptionTypeDef",
    {
        "VpcId": str,
        "SubnetIds": List[str],
        "CustomerUserName": str,
        "SecurityGroupId": str,
        "AvailabilityZones": List[str],
        "ConnectIps": List[str],
    },
    total=False,
)

DirectoryVpcSettingsDescriptionTypeDef = TypedDict(
    "DirectoryVpcSettingsDescriptionTypeDef",
    {
        "VpcId": str,
        "SubnetIds": List[str],
        "SecurityGroupId": str,
        "AvailabilityZones": List[str],
    },
    total=False,
)

RadiusSettingsTypeDef = TypedDict(
    "RadiusSettingsTypeDef",
    {
        "RadiusServers": List[str],
        "RadiusPort": int,
        "RadiusTimeout": int,
        "RadiusRetries": int,
        "SharedSecret": str,
        "AuthenticationProtocol": RadiusAuthenticationProtocolType,
        "DisplayLabel": str,
        "UseSameUsername": bool,
    },
    total=False,
)

RegionsInfoTypeDef = TypedDict(
    "RegionsInfoTypeDef",
    {
        "PrimaryRegion": str,
        "AdditionalRegions": List[str],
    },
    total=False,
)

DirectoryLimitsTypeDef = TypedDict(
    "DirectoryLimitsTypeDef",
    {
        "CloudOnlyDirectoriesLimit": int,
        "CloudOnlyDirectoriesCurrentCount": int,
        "CloudOnlyDirectoriesLimitReached": bool,
        "CloudOnlyMicrosoftADLimit": int,
        "CloudOnlyMicrosoftADCurrentCount": int,
        "CloudOnlyMicrosoftADLimitReached": bool,
        "ConnectedDirectoriesLimit": int,
        "ConnectedDirectoriesCurrentCount": int,
        "ConnectedDirectoriesLimitReached": bool,
    },
    total=False,
)

DisableClientAuthenticationRequestRequestTypeDef = TypedDict(
    "DisableClientAuthenticationRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": Literal["SmartCard"],
    },
)

DisableLDAPSRequestRequestTypeDef = TypedDict(
    "DisableLDAPSRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": Literal["Client"],
    },
)

DisableRadiusRequestRequestTypeDef = TypedDict(
    "DisableRadiusRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)

_RequiredDisableSsoRequestRequestTypeDef = TypedDict(
    "_RequiredDisableSsoRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDisableSsoRequestRequestTypeDef = TypedDict(
    "_OptionalDisableSsoRequestRequestTypeDef",
    {
        "UserName": str,
        "Password": str,
    },
    total=False,
)


class DisableSsoRequestRequestTypeDef(
    _RequiredDisableSsoRequestRequestTypeDef, _OptionalDisableSsoRequestRequestTypeDef
):
    pass


EnableClientAuthenticationRequestRequestTypeDef = TypedDict(
    "EnableClientAuthenticationRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": Literal["SmartCard"],
    },
)

EnableLDAPSRequestRequestTypeDef = TypedDict(
    "EnableLDAPSRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "Type": Literal["Client"],
    },
)

_RequiredEnableSsoRequestRequestTypeDef = TypedDict(
    "_RequiredEnableSsoRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalEnableSsoRequestRequestTypeDef = TypedDict(
    "_OptionalEnableSsoRequestRequestTypeDef",
    {
        "UserName": str,
        "Password": str,
    },
    total=False,
)


class EnableSsoRequestRequestTypeDef(
    _RequiredEnableSsoRequestRequestTypeDef, _OptionalEnableSsoRequestRequestTypeDef
):
    pass


GetSnapshotLimitsRequestRequestTypeDef = TypedDict(
    "GetSnapshotLimitsRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)

SnapshotLimitsTypeDef = TypedDict(
    "SnapshotLimitsTypeDef",
    {
        "ManualSnapshotsLimit": int,
        "ManualSnapshotsCurrentCount": int,
        "ManualSnapshotsLimitReached": bool,
    },
    total=False,
)

IpRouteInfoTypeDef = TypedDict(
    "IpRouteInfoTypeDef",
    {
        "DirectoryId": str,
        "CidrIp": str,
        "IpRouteStatusMsg": IpRouteStatusMsgType,
        "AddedDateTime": datetime,
        "IpRouteStatusReason": str,
        "Description": str,
    },
    total=False,
)

_RequiredListCertificatesRequestRequestTypeDef = TypedDict(
    "_RequiredListCertificatesRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalListCertificatesRequestRequestTypeDef = TypedDict(
    "_OptionalListCertificatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class ListCertificatesRequestRequestTypeDef(
    _RequiredListCertificatesRequestRequestTypeDef, _OptionalListCertificatesRequestRequestTypeDef
):
    pass


_RequiredListIpRoutesRequestRequestTypeDef = TypedDict(
    "_RequiredListIpRoutesRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalListIpRoutesRequestRequestTypeDef = TypedDict(
    "_OptionalListIpRoutesRequestRequestTypeDef",
    {
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class ListIpRoutesRequestRequestTypeDef(
    _RequiredListIpRoutesRequestRequestTypeDef, _OptionalListIpRoutesRequestRequestTypeDef
):
    pass


ListLogSubscriptionsRequestRequestTypeDef = TypedDict(
    "ListLogSubscriptionsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

LogSubscriptionTypeDef = TypedDict(
    "LogSubscriptionTypeDef",
    {
        "DirectoryId": str,
        "LogGroupName": str,
        "SubscriptionCreatedDateTime": datetime,
    },
    total=False,
)

_RequiredListSchemaExtensionsRequestRequestTypeDef = TypedDict(
    "_RequiredListSchemaExtensionsRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalListSchemaExtensionsRequestRequestTypeDef = TypedDict(
    "_OptionalListSchemaExtensionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class ListSchemaExtensionsRequestRequestTypeDef(
    _RequiredListSchemaExtensionsRequestRequestTypeDef,
    _OptionalListSchemaExtensionsRequestRequestTypeDef,
):
    pass


SchemaExtensionInfoTypeDef = TypedDict(
    "SchemaExtensionInfoTypeDef",
    {
        "DirectoryId": str,
        "SchemaExtensionId": str,
        "Description": str,
        "SchemaExtensionStatus": SchemaExtensionStatusType,
        "SchemaExtensionStatusReason": str,
        "StartDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


RegisterEventTopicRequestRequestTypeDef = TypedDict(
    "RegisterEventTopicRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "TopicName": str,
    },
)

RejectSharedDirectoryRequestRequestTypeDef = TypedDict(
    "RejectSharedDirectoryRequestRequestTypeDef",
    {
        "SharedDirectoryId": str,
    },
)

RemoveIpRoutesRequestRequestTypeDef = TypedDict(
    "RemoveIpRoutesRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "CidrIps": Sequence[str],
    },
)

RemoveRegionRequestRequestTypeDef = TypedDict(
    "RemoveRegionRequestRequestTypeDef",
    {
        "DirectoryId": str,
    },
)

RemoveTagsFromResourceRequestRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagKeys": Sequence[str],
    },
)

ResetUserPasswordRequestRequestTypeDef = TypedDict(
    "ResetUserPasswordRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "UserName": str,
        "NewPassword": str,
    },
)

RestoreFromSnapshotRequestRequestTypeDef = TypedDict(
    "RestoreFromSnapshotRequestRequestTypeDef",
    {
        "SnapshotId": str,
    },
)

ShareTargetTypeDef = TypedDict(
    "ShareTargetTypeDef",
    {
        "Id": str,
        "Type": Literal["ACCOUNT"],
    },
)

StartSchemaExtensionRequestRequestTypeDef = TypedDict(
    "StartSchemaExtensionRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "CreateSnapshotBeforeSchemaExtension": bool,
        "LdifContent": str,
        "Description": str,
    },
)

UnshareTargetTypeDef = TypedDict(
    "UnshareTargetTypeDef",
    {
        "Id": str,
        "Type": Literal["ACCOUNT"],
    },
)

UpdateConditionalForwarderRequestRequestTypeDef = TypedDict(
    "UpdateConditionalForwarderRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RemoteDomainName": str,
        "DnsIpAddrs": Sequence[str],
    },
)

UpdateNumberOfDomainControllersRequestRequestTypeDef = TypedDict(
    "UpdateNumberOfDomainControllersRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "DesiredNumber": int,
    },
)

_RequiredUpdateTrustRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrustRequestRequestTypeDef",
    {
        "TrustId": str,
    },
)
_OptionalUpdateTrustRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrustRequestRequestTypeDef",
    {
        "SelectiveAuth": SelectiveAuthType,
    },
    total=False,
)


class UpdateTrustRequestRequestTypeDef(
    _RequiredUpdateTrustRequestRequestTypeDef, _OptionalUpdateTrustRequestRequestTypeDef
):
    pass


VerifyTrustRequestRequestTypeDef = TypedDict(
    "VerifyTrustRequestRequestTypeDef",
    {
        "TrustId": str,
    },
)

ConnectDirectoryResultTypeDef = TypedDict(
    "ConnectDirectoryResultTypeDef",
    {
        "DirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAliasResultTypeDef = TypedDict(
    "CreateAliasResultTypeDef",
    {
        "DirectoryId": str,
        "Alias": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDirectoryResultTypeDef = TypedDict(
    "CreateDirectoryResultTypeDef",
    {
        "DirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMicrosoftADResultTypeDef = TypedDict(
    "CreateMicrosoftADResultTypeDef",
    {
        "DirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSnapshotResultTypeDef = TypedDict(
    "CreateSnapshotResultTypeDef",
    {
        "SnapshotId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrustResultTypeDef = TypedDict(
    "CreateTrustResultTypeDef",
    {
        "TrustId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDirectoryResultTypeDef = TypedDict(
    "DeleteDirectoryResultTypeDef",
    {
        "DirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSnapshotResultTypeDef = TypedDict(
    "DeleteSnapshotResultTypeDef",
    {
        "SnapshotId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTrustResultTypeDef = TypedDict(
    "DeleteTrustResultTypeDef",
    {
        "TrustId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterCertificateResultTypeDef = TypedDict(
    "RegisterCertificateResultTypeDef",
    {
        "CertificateId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RejectSharedDirectoryResultTypeDef = TypedDict(
    "RejectSharedDirectoryResultTypeDef",
    {
        "SharedDirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ShareDirectoryResultTypeDef = TypedDict(
    "ShareDirectoryResultTypeDef",
    {
        "SharedDirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSchemaExtensionResultTypeDef = TypedDict(
    "StartSchemaExtensionResultTypeDef",
    {
        "SchemaExtensionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UnshareDirectoryResultTypeDef = TypedDict(
    "UnshareDirectoryResultTypeDef",
    {
        "SharedDirectoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTrustResultTypeDef = TypedDict(
    "UpdateTrustResultTypeDef",
    {
        "RequestId": str,
        "TrustId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyTrustResultTypeDef = TypedDict(
    "VerifyTrustResultTypeDef",
    {
        "TrustId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AcceptSharedDirectoryResultTypeDef = TypedDict(
    "AcceptSharedDirectoryResultTypeDef",
    {
        "SharedDirectory": SharedDirectoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSharedDirectoriesResultTypeDef = TypedDict(
    "DescribeSharedDirectoriesResultTypeDef",
    {
        "SharedDirectories": List[SharedDirectoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAddIpRoutesRequestRequestTypeDef = TypedDict(
    "_RequiredAddIpRoutesRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "IpRoutes": Sequence[IpRouteTypeDef],
    },
)
_OptionalAddIpRoutesRequestRequestTypeDef = TypedDict(
    "_OptionalAddIpRoutesRequestRequestTypeDef",
    {
        "UpdateSecurityGroupForDirectoryControllers": bool,
    },
    total=False,
)


class AddIpRoutesRequestRequestTypeDef(
    _RequiredAddIpRoutesRequestRequestTypeDef, _OptionalAddIpRoutesRequestRequestTypeDef
):
    pass


AddRegionRequestRequestTypeDef = TypedDict(
    "AddRegionRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RegionName": str,
        "VPCSettings": DirectoryVpcSettingsTypeDef,
    },
)

RegionDescriptionTypeDef = TypedDict(
    "RegionDescriptionTypeDef",
    {
        "DirectoryId": str,
        "RegionName": str,
        "RegionType": RegionTypeType,
        "Status": DirectoryStageType,
        "VpcSettings": DirectoryVpcSettingsTypeDef,
        "DesiredNumberOfDomainControllers": int,
        "LaunchTime": datetime,
        "StatusLastUpdatedDateTime": datetime,
        "LastUpdatedDateTime": datetime,
    },
    total=False,
)

AddTagsToResourceRequestRequestTypeDef = TypedDict(
    "AddTagsToResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateDirectoryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDirectoryRequestRequestTypeDef",
    {
        "Name": str,
        "Password": str,
        "Size": DirectorySizeType,
    },
)
_OptionalCreateDirectoryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDirectoryRequestRequestTypeDef",
    {
        "ShortName": str,
        "Description": str,
        "VpcSettings": DirectoryVpcSettingsTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDirectoryRequestRequestTypeDef(
    _RequiredCreateDirectoryRequestRequestTypeDef, _OptionalCreateDirectoryRequestRequestTypeDef
):
    pass


_RequiredCreateMicrosoftADRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMicrosoftADRequestRequestTypeDef",
    {
        "Name": str,
        "Password": str,
        "VpcSettings": DirectoryVpcSettingsTypeDef,
    },
)
_OptionalCreateMicrosoftADRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMicrosoftADRequestRequestTypeDef",
    {
        "ShortName": str,
        "Description": str,
        "Edition": DirectoryEditionType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMicrosoftADRequestRequestTypeDef(
    _RequiredCreateMicrosoftADRequestRequestTypeDef, _OptionalCreateMicrosoftADRequestRequestTypeDef
):
    pass


ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ComputerTypeDef = TypedDict(
    "ComputerTypeDef",
    {
        "ComputerId": str,
        "ComputerName": str,
        "ComputerAttributes": List[AttributeTypeDef],
    },
    total=False,
)

_RequiredCreateComputerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateComputerRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "ComputerName": str,
        "Password": str,
    },
)
_OptionalCreateComputerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateComputerRequestRequestTypeDef",
    {
        "OrganizationalUnitDistinguishedName": str,
        "ComputerAttributes": Sequence[AttributeTypeDef],
    },
    total=False,
)


class CreateComputerRequestRequestTypeDef(
    _RequiredCreateComputerRequestRequestTypeDef, _OptionalCreateComputerRequestRequestTypeDef
):
    pass


ListCertificatesResultTypeDef = TypedDict(
    "ListCertificatesResultTypeDef",
    {
        "NextToken": str,
        "CertificatesInfo": List[CertificateInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateId": str,
        "State": CertificateStateType,
        "StateReason": str,
        "CommonName": str,
        "RegisteredDateTime": datetime,
        "ExpiryDateTime": datetime,
        "Type": CertificateTypeType,
        "ClientCertAuthSettings": ClientCertAuthSettingsTypeDef,
    },
    total=False,
)

_RequiredRegisterCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterCertificateRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "CertificateData": str,
    },
)
_OptionalRegisterCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterCertificateRequestRequestTypeDef",
    {
        "Type": CertificateTypeType,
        "ClientCertAuthSettings": ClientCertAuthSettingsTypeDef,
    },
    total=False,
)


class RegisterCertificateRequestRequestTypeDef(
    _RequiredRegisterCertificateRequestRequestTypeDef,
    _OptionalRegisterCertificateRequestRequestTypeDef,
):
    pass


DescribeClientAuthenticationSettingsResultTypeDef = TypedDict(
    "DescribeClientAuthenticationSettingsResultTypeDef",
    {
        "ClientAuthenticationSettingsInfo": List[ClientAuthenticationSettingInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConditionalForwardersResultTypeDef = TypedDict(
    "DescribeConditionalForwardersResultTypeDef",
    {
        "ConditionalForwarders": List[ConditionalForwarderTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredConnectDirectoryRequestRequestTypeDef = TypedDict(
    "_RequiredConnectDirectoryRequestRequestTypeDef",
    {
        "Name": str,
        "Password": str,
        "Size": DirectorySizeType,
        "ConnectSettings": DirectoryConnectSettingsTypeDef,
    },
)
_OptionalConnectDirectoryRequestRequestTypeDef = TypedDict(
    "_OptionalConnectDirectoryRequestRequestTypeDef",
    {
        "ShortName": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class ConnectDirectoryRequestRequestTypeDef(
    _RequiredConnectDirectoryRequestRequestTypeDef, _OptionalConnectDirectoryRequestRequestTypeDef
):
    pass


DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef = TypedDict(
    "DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef",
    {
        "DirectoryIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalDescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef",
    {
        "DomainControllerIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef(
    _RequiredDescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef,
    _OptionalDescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef,
):
    pass


_RequiredDescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef = TypedDict(
    "_RequiredDescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef",
    {
        "OwnerDirectoryId": str,
    },
)
_OptionalDescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef = TypedDict(
    "_OptionalDescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef",
    {
        "SharedDirectoryIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef(
    _RequiredDescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef,
    _OptionalDescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef,
):
    pass


DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef = TypedDict(
    "DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef",
    {
        "DirectoryId": str,
        "SnapshotIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeTrustsRequestDescribeTrustsPaginateTypeDef = TypedDict(
    "DescribeTrustsRequestDescribeTrustsPaginateTypeDef",
    {
        "DirectoryId": str,
        "TrustIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListIpRoutesRequestListIpRoutesPaginateTypeDef = TypedDict(
    "_RequiredListIpRoutesRequestListIpRoutesPaginateTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalListIpRoutesRequestListIpRoutesPaginateTypeDef = TypedDict(
    "_OptionalListIpRoutesRequestListIpRoutesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListIpRoutesRequestListIpRoutesPaginateTypeDef(
    _RequiredListIpRoutesRequestListIpRoutesPaginateTypeDef,
    _OptionalListIpRoutesRequestListIpRoutesPaginateTypeDef,
):
    pass


ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef = TypedDict(
    "ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef",
    {
        "DirectoryId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef = TypedDict(
    "_RequiredListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef",
    {
        "DirectoryId": str,
    },
)
_OptionalListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef = TypedDict(
    "_OptionalListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef(
    _RequiredListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef,
    _OptionalListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef,
):
    pass


_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


DescribeDomainControllersResultTypeDef = TypedDict(
    "DescribeDomainControllersResultTypeDef",
    {
        "DomainControllers": List[DomainControllerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventTopicsResultTypeDef = TypedDict(
    "DescribeEventTopicsResultTypeDef",
    {
        "EventTopics": List[EventTopicTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLDAPSSettingsResultTypeDef = TypedDict(
    "DescribeLDAPSSettingsResultTypeDef",
    {
        "LDAPSSettingsInfo": List[LDAPSSettingInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSnapshotsResultTypeDef = TypedDict(
    "DescribeSnapshotsResultTypeDef",
    {
        "Snapshots": List[SnapshotTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTrustsResultTypeDef = TypedDict(
    "DescribeTrustsResultTypeDef",
    {
        "Trusts": List[TrustTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableRadiusRequestRequestTypeDef = TypedDict(
    "EnableRadiusRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RadiusSettings": RadiusSettingsTypeDef,
    },
)

OwnerDirectoryDescriptionTypeDef = TypedDict(
    "OwnerDirectoryDescriptionTypeDef",
    {
        "DirectoryId": str,
        "AccountId": str,
        "DnsIpAddrs": List[str],
        "VpcSettings": DirectoryVpcSettingsDescriptionTypeDef,
        "RadiusSettings": RadiusSettingsTypeDef,
        "RadiusStatus": RadiusStatusType,
    },
    total=False,
)

UpdateRadiusRequestRequestTypeDef = TypedDict(
    "UpdateRadiusRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "RadiusSettings": RadiusSettingsTypeDef,
    },
)

GetDirectoryLimitsResultTypeDef = TypedDict(
    "GetDirectoryLimitsResultTypeDef",
    {
        "DirectoryLimits": DirectoryLimitsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSnapshotLimitsResultTypeDef = TypedDict(
    "GetSnapshotLimitsResultTypeDef",
    {
        "SnapshotLimits": SnapshotLimitsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIpRoutesResultTypeDef = TypedDict(
    "ListIpRoutesResultTypeDef",
    {
        "IpRoutesInfo": List[IpRouteInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLogSubscriptionsResultTypeDef = TypedDict(
    "ListLogSubscriptionsResultTypeDef",
    {
        "LogSubscriptions": List[LogSubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemaExtensionsResultTypeDef = TypedDict(
    "ListSchemaExtensionsResultTypeDef",
    {
        "SchemaExtensionsInfo": List[SchemaExtensionInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredShareDirectoryRequestRequestTypeDef = TypedDict(
    "_RequiredShareDirectoryRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "ShareTarget": ShareTargetTypeDef,
        "ShareMethod": ShareMethodType,
    },
)
_OptionalShareDirectoryRequestRequestTypeDef = TypedDict(
    "_OptionalShareDirectoryRequestRequestTypeDef",
    {
        "ShareNotes": str,
    },
    total=False,
)


class ShareDirectoryRequestRequestTypeDef(
    _RequiredShareDirectoryRequestRequestTypeDef, _OptionalShareDirectoryRequestRequestTypeDef
):
    pass


UnshareDirectoryRequestRequestTypeDef = TypedDict(
    "UnshareDirectoryRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "UnshareTarget": UnshareTargetTypeDef,
    },
)

DescribeRegionsResultTypeDef = TypedDict(
    "DescribeRegionsResultTypeDef",
    {
        "RegionsDescription": List[RegionDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateComputerResultTypeDef = TypedDict(
    "CreateComputerResultTypeDef",
    {
        "Computer": ComputerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCertificateResultTypeDef = TypedDict(
    "DescribeCertificateResultTypeDef",
    {
        "Certificate": CertificateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DirectoryDescriptionTypeDef = TypedDict(
    "DirectoryDescriptionTypeDef",
    {
        "DirectoryId": str,
        "Name": str,
        "ShortName": str,
        "Size": DirectorySizeType,
        "Edition": DirectoryEditionType,
        "Alias": str,
        "AccessUrl": str,
        "Description": str,
        "DnsIpAddrs": List[str],
        "Stage": DirectoryStageType,
        "ShareStatus": ShareStatusType,
        "ShareMethod": ShareMethodType,
        "ShareNotes": str,
        "LaunchTime": datetime,
        "StageLastUpdatedDateTime": datetime,
        "Type": DirectoryTypeType,
        "VpcSettings": DirectoryVpcSettingsDescriptionTypeDef,
        "ConnectSettings": DirectoryConnectSettingsDescriptionTypeDef,
        "RadiusSettings": RadiusSettingsTypeDef,
        "RadiusStatus": RadiusStatusType,
        "StageReason": str,
        "SsoEnabled": bool,
        "DesiredNumberOfDomainControllers": int,
        "OwnerDirectoryDescription": OwnerDirectoryDescriptionTypeDef,
        "RegionsInfo": RegionsInfoTypeDef,
    },
    total=False,
)

DescribeDirectoriesResultTypeDef = TypedDict(
    "DescribeDirectoriesResultTypeDef",
    {
        "DirectoryDescriptions": List[DirectoryDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
