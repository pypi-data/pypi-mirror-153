"""
Type annotations for alexaforbusiness service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/type_defs/)

Usage::

    ```python
    from mypy_boto3_alexaforbusiness.type_defs import AddressBookDataTypeDef

    data: AddressBookDataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BusinessReportFailureCodeType,
    BusinessReportFormatType,
    BusinessReportIntervalType,
    BusinessReportStatusType,
    CommsProtocolType,
    ConferenceProviderTypeType,
    ConnectionStatusType,
    DeviceEventTypeType,
    DeviceStatusDetailCodeType,
    DeviceStatusType,
    DistanceUnitType,
    EnablementTypeFilterType,
    EnablementTypeType,
    EndOfMeetingReminderTypeType,
    EnrollmentStatusType,
    FeatureType,
    NetworkSecurityTypeType,
    PhoneNumberTypeType,
    RequirePinType,
    SkillTypeFilterType,
    SkillTypeType,
    SortValueType,
    TemperatureUnitType,
    WakeWordType,
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
    "AddressBookDataTypeDef",
    "AddressBookTypeDef",
    "ApproveSkillRequestRequestTypeDef",
    "AssociateContactWithAddressBookRequestRequestTypeDef",
    "AssociateDeviceWithNetworkProfileRequestRequestTypeDef",
    "AssociateDeviceWithRoomRequestRequestTypeDef",
    "AssociateSkillGroupWithRoomRequestRequestTypeDef",
    "AssociateSkillWithSkillGroupRequestRequestTypeDef",
    "AssociateSkillWithUsersRequestRequestTypeDef",
    "AudioTypeDef",
    "BusinessReportContentRangeTypeDef",
    "BusinessReportRecurrenceTypeDef",
    "BusinessReportS3LocationTypeDef",
    "CategoryTypeDef",
    "ConferencePreferenceTypeDef",
    "IPDialInTypeDef",
    "MeetingSettingTypeDef",
    "PSTNDialInTypeDef",
    "PhoneNumberTypeDef",
    "SipAddressTypeDef",
    "SsmlTypeDef",
    "TextTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "CreateEndOfMeetingReminderTypeDef",
    "CreateInstantBookingTypeDef",
    "CreateRequireCheckInTypeDef",
    "DeleteAddressBookRequestRequestTypeDef",
    "DeleteBusinessReportScheduleRequestRequestTypeDef",
    "DeleteConferenceProviderRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DeleteDeviceRequestRequestTypeDef",
    "DeleteDeviceUsageDataRequestRequestTypeDef",
    "DeleteGatewayGroupRequestRequestTypeDef",
    "DeleteNetworkProfileRequestRequestTypeDef",
    "DeleteProfileRequestRequestTypeDef",
    "DeleteRoomRequestRequestTypeDef",
    "DeleteRoomSkillParameterRequestRequestTypeDef",
    "DeleteSkillAuthorizationRequestRequestTypeDef",
    "DeleteSkillGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeveloperInfoTypeDef",
    "DeviceEventTypeDef",
    "DeviceNetworkProfileInfoTypeDef",
    "DeviceStatusDetailTypeDef",
    "DisassociateContactFromAddressBookRequestRequestTypeDef",
    "DisassociateDeviceFromRoomRequestRequestTypeDef",
    "DisassociateSkillFromSkillGroupRequestRequestTypeDef",
    "DisassociateSkillFromUsersRequestRequestTypeDef",
    "DisassociateSkillGroupFromRoomRequestRequestTypeDef",
    "EndOfMeetingReminderTypeDef",
    "FilterTypeDef",
    "ForgetSmartHomeAppliancesRequestRequestTypeDef",
    "GatewayGroupSummaryTypeDef",
    "GatewayGroupTypeDef",
    "GatewaySummaryTypeDef",
    "GatewayTypeDef",
    "GetAddressBookRequestRequestTypeDef",
    "GetConferenceProviderRequestRequestTypeDef",
    "GetContactRequestRequestTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetGatewayGroupRequestRequestTypeDef",
    "GetGatewayRequestRequestTypeDef",
    "GetNetworkProfileRequestRequestTypeDef",
    "NetworkProfileTypeDef",
    "GetProfileRequestRequestTypeDef",
    "GetRoomRequestRequestTypeDef",
    "RoomTypeDef",
    "GetRoomSkillParameterRequestRequestTypeDef",
    "RoomSkillParameterTypeDef",
    "GetSkillGroupRequestRequestTypeDef",
    "SkillGroupTypeDef",
    "InstantBookingTypeDef",
    "PaginatorConfigTypeDef",
    "ListBusinessReportSchedulesRequestRequestTypeDef",
    "ListConferenceProvidersRequestRequestTypeDef",
    "ListDeviceEventsRequestRequestTypeDef",
    "ListGatewayGroupsRequestRequestTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListSkillsRequestRequestTypeDef",
    "SkillSummaryTypeDef",
    "ListSkillsStoreCategoriesRequestRequestTypeDef",
    "ListSkillsStoreSkillsByCategoryRequestRequestTypeDef",
    "ListSmartHomeAppliancesRequestRequestTypeDef",
    "SmartHomeApplianceTypeDef",
    "ListTagsRequestRequestTypeDef",
    "RequireCheckInTypeDef",
    "NetworkProfileDataTypeDef",
    "ProfileDataTypeDef",
    "PutInvitationConfigurationRequestRequestTypeDef",
    "PutSkillAuthorizationRequestRequestTypeDef",
    "RejectSkillRequestRequestTypeDef",
    "ResolveRoomRequestRequestTypeDef",
    "RevokeInvitationRequestRequestTypeDef",
    "RoomDataTypeDef",
    "SortTypeDef",
    "SkillGroupDataTypeDef",
    "UserDataTypeDef",
    "SendInvitationRequestRequestTypeDef",
    "StartDeviceSyncRequestRequestTypeDef",
    "StartSmartHomeApplianceDiscoveryRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAddressBookRequestRequestTypeDef",
    "UpdateDeviceRequestRequestTypeDef",
    "UpdateEndOfMeetingReminderTypeDef",
    "UpdateGatewayGroupRequestRequestTypeDef",
    "UpdateGatewayRequestRequestTypeDef",
    "UpdateInstantBookingTypeDef",
    "UpdateRequireCheckInTypeDef",
    "UpdateNetworkProfileRequestRequestTypeDef",
    "UpdateRoomRequestRequestTypeDef",
    "UpdateSkillGroupRequestRequestTypeDef",
    "UpdateBusinessReportScheduleRequestRequestTypeDef",
    "BusinessReportTypeDef",
    "PutConferencePreferenceRequestRequestTypeDef",
    "ConferenceProviderTypeDef",
    "UpdateConferenceProviderRequestRequestTypeDef",
    "ContactDataTypeDef",
    "ContactTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "ContentTypeDef",
    "CreateAddressBookRequestRequestTypeDef",
    "CreateBusinessReportScheduleRequestRequestTypeDef",
    "CreateConferenceProviderRequestRequestTypeDef",
    "CreateContactRequestRequestTypeDef",
    "CreateGatewayGroupRequestRequestTypeDef",
    "CreateNetworkProfileRequestRequestTypeDef",
    "CreateRoomRequestRequestTypeDef",
    "CreateSkillGroupRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "RegisterAVSDeviceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAddressBookResponseTypeDef",
    "CreateBusinessReportScheduleResponseTypeDef",
    "CreateConferenceProviderResponseTypeDef",
    "CreateContactResponseTypeDef",
    "CreateGatewayGroupResponseTypeDef",
    "CreateNetworkProfileResponseTypeDef",
    "CreateProfileResponseTypeDef",
    "CreateRoomResponseTypeDef",
    "CreateSkillGroupResponseTypeDef",
    "CreateUserResponseTypeDef",
    "GetAddressBookResponseTypeDef",
    "GetConferencePreferenceResponseTypeDef",
    "GetInvitationConfigurationResponseTypeDef",
    "ListSkillsStoreCategoriesResponseTypeDef",
    "ListTagsResponseTypeDef",
    "RegisterAVSDeviceResponseTypeDef",
    "SearchAddressBooksResponseTypeDef",
    "SendAnnouncementResponseTypeDef",
    "CreateMeetingRoomConfigurationTypeDef",
    "SkillDetailsTypeDef",
    "ListDeviceEventsResponseTypeDef",
    "DeviceStatusInfoTypeDef",
    "ListGatewayGroupsResponseTypeDef",
    "GetGatewayGroupResponseTypeDef",
    "ListGatewaysResponseTypeDef",
    "GetGatewayResponseTypeDef",
    "GetNetworkProfileResponseTypeDef",
    "GetRoomResponseTypeDef",
    "GetRoomSkillParameterResponseTypeDef",
    "PutRoomSkillParameterRequestRequestTypeDef",
    "ResolveRoomResponseTypeDef",
    "GetSkillGroupResponseTypeDef",
    "ListBusinessReportSchedulesRequestListBusinessReportSchedulesPaginateTypeDef",
    "ListConferenceProvidersRequestListConferenceProvidersPaginateTypeDef",
    "ListDeviceEventsRequestListDeviceEventsPaginateTypeDef",
    "ListSkillsRequestListSkillsPaginateTypeDef",
    "ListSkillsStoreCategoriesRequestListSkillsStoreCategoriesPaginateTypeDef",
    "ListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef",
    "ListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef",
    "ListTagsRequestListTagsPaginateTypeDef",
    "ListSkillsResponseTypeDef",
    "ListSmartHomeAppliancesResponseTypeDef",
    "MeetingRoomConfigurationTypeDef",
    "SearchNetworkProfilesResponseTypeDef",
    "SearchProfilesResponseTypeDef",
    "SearchRoomsResponseTypeDef",
    "SearchAddressBooksRequestRequestTypeDef",
    "SearchContactsRequestRequestTypeDef",
    "SearchDevicesRequestRequestTypeDef",
    "SearchDevicesRequestSearchDevicesPaginateTypeDef",
    "SearchNetworkProfilesRequestRequestTypeDef",
    "SearchProfilesRequestRequestTypeDef",
    "SearchProfilesRequestSearchProfilesPaginateTypeDef",
    "SearchRoomsRequestRequestTypeDef",
    "SearchRoomsRequestSearchRoomsPaginateTypeDef",
    "SearchSkillGroupsRequestRequestTypeDef",
    "SearchSkillGroupsRequestSearchSkillGroupsPaginateTypeDef",
    "SearchUsersRequestRequestTypeDef",
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    "SearchSkillGroupsResponseTypeDef",
    "SearchUsersResponseTypeDef",
    "UpdateMeetingRoomConfigurationTypeDef",
    "BusinessReportScheduleTypeDef",
    "GetConferenceProviderResponseTypeDef",
    "ListConferenceProvidersResponseTypeDef",
    "SearchContactsResponseTypeDef",
    "GetContactResponseTypeDef",
    "SendAnnouncementRequestRequestTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "SkillsStoreSkillTypeDef",
    "DeviceDataTypeDef",
    "DeviceTypeDef",
    "ProfileTypeDef",
    "UpdateProfileRequestRequestTypeDef",
    "ListBusinessReportSchedulesResponseTypeDef",
    "ListSkillsStoreSkillsByCategoryResponseTypeDef",
    "SearchDevicesResponseTypeDef",
    "GetDeviceResponseTypeDef",
    "GetProfileResponseTypeDef",
)

AddressBookDataTypeDef = TypedDict(
    "AddressBookDataTypeDef",
    {
        "AddressBookArn": str,
        "Name": str,
        "Description": str,
    },
    total=False,
)

AddressBookTypeDef = TypedDict(
    "AddressBookTypeDef",
    {
        "AddressBookArn": str,
        "Name": str,
        "Description": str,
    },
    total=False,
)

ApproveSkillRequestRequestTypeDef = TypedDict(
    "ApproveSkillRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)

AssociateContactWithAddressBookRequestRequestTypeDef = TypedDict(
    "AssociateContactWithAddressBookRequestRequestTypeDef",
    {
        "ContactArn": str,
        "AddressBookArn": str,
    },
)

AssociateDeviceWithNetworkProfileRequestRequestTypeDef = TypedDict(
    "AssociateDeviceWithNetworkProfileRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "NetworkProfileArn": str,
    },
)

AssociateDeviceWithRoomRequestRequestTypeDef = TypedDict(
    "AssociateDeviceWithRoomRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "RoomArn": str,
    },
    total=False,
)

AssociateSkillGroupWithRoomRequestRequestTypeDef = TypedDict(
    "AssociateSkillGroupWithRoomRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
        "RoomArn": str,
    },
    total=False,
)

_RequiredAssociateSkillWithSkillGroupRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateSkillWithSkillGroupRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
_OptionalAssociateSkillWithSkillGroupRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateSkillWithSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
    },
    total=False,
)


class AssociateSkillWithSkillGroupRequestRequestTypeDef(
    _RequiredAssociateSkillWithSkillGroupRequestRequestTypeDef,
    _OptionalAssociateSkillWithSkillGroupRequestRequestTypeDef,
):
    pass


AssociateSkillWithUsersRequestRequestTypeDef = TypedDict(
    "AssociateSkillWithUsersRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)

AudioTypeDef = TypedDict(
    "AudioTypeDef",
    {
        "Locale": Literal["en-US"],
        "Location": str,
    },
)

BusinessReportContentRangeTypeDef = TypedDict(
    "BusinessReportContentRangeTypeDef",
    {
        "Interval": BusinessReportIntervalType,
    },
)

BusinessReportRecurrenceTypeDef = TypedDict(
    "BusinessReportRecurrenceTypeDef",
    {
        "StartDate": str,
    },
    total=False,
)

BusinessReportS3LocationTypeDef = TypedDict(
    "BusinessReportS3LocationTypeDef",
    {
        "Path": str,
        "BucketName": str,
    },
    total=False,
)

CategoryTypeDef = TypedDict(
    "CategoryTypeDef",
    {
        "CategoryId": int,
        "CategoryName": str,
    },
    total=False,
)

ConferencePreferenceTypeDef = TypedDict(
    "ConferencePreferenceTypeDef",
    {
        "DefaultConferenceProviderArn": str,
    },
    total=False,
)

IPDialInTypeDef = TypedDict(
    "IPDialInTypeDef",
    {
        "Endpoint": str,
        "CommsProtocol": CommsProtocolType,
    },
)

MeetingSettingTypeDef = TypedDict(
    "MeetingSettingTypeDef",
    {
        "RequirePin": RequirePinType,
    },
)

PSTNDialInTypeDef = TypedDict(
    "PSTNDialInTypeDef",
    {
        "CountryCode": str,
        "PhoneNumber": str,
        "OneClickIdDelay": str,
        "OneClickPinDelay": str,
    },
)

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "Number": str,
        "Type": PhoneNumberTypeType,
    },
)

SipAddressTypeDef = TypedDict(
    "SipAddressTypeDef",
    {
        "Uri": str,
        "Type": Literal["WORK"],
    },
)

SsmlTypeDef = TypedDict(
    "SsmlTypeDef",
    {
        "Locale": Literal["en-US"],
        "Value": str,
    },
)

TextTypeDef = TypedDict(
    "TextTypeDef",
    {
        "Locale": Literal["en-US"],
        "Value": str,
    },
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

CreateEndOfMeetingReminderTypeDef = TypedDict(
    "CreateEndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": Sequence[int],
        "ReminderType": EndOfMeetingReminderTypeType,
        "Enabled": bool,
    },
)

CreateInstantBookingTypeDef = TypedDict(
    "CreateInstantBookingTypeDef",
    {
        "DurationInMinutes": int,
        "Enabled": bool,
    },
)

CreateRequireCheckInTypeDef = TypedDict(
    "CreateRequireCheckInTypeDef",
    {
        "ReleaseAfterMinutes": int,
        "Enabled": bool,
    },
)

DeleteAddressBookRequestRequestTypeDef = TypedDict(
    "DeleteAddressBookRequestRequestTypeDef",
    {
        "AddressBookArn": str,
    },
)

DeleteBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "DeleteBusinessReportScheduleRequestRequestTypeDef",
    {
        "ScheduleArn": str,
    },
)

DeleteConferenceProviderRequestRequestTypeDef = TypedDict(
    "DeleteConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderArn": str,
    },
)

DeleteContactRequestRequestTypeDef = TypedDict(
    "DeleteContactRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)

DeleteDeviceRequestRequestTypeDef = TypedDict(
    "DeleteDeviceRequestRequestTypeDef",
    {
        "DeviceArn": str,
    },
)

DeleteDeviceUsageDataRequestRequestTypeDef = TypedDict(
    "DeleteDeviceUsageDataRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "DeviceUsageType": Literal["VOICE"],
    },
)

DeleteGatewayGroupRequestRequestTypeDef = TypedDict(
    "DeleteGatewayGroupRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
    },
)

DeleteNetworkProfileRequestRequestTypeDef = TypedDict(
    "DeleteNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileArn": str,
    },
)

DeleteProfileRequestRequestTypeDef = TypedDict(
    "DeleteProfileRequestRequestTypeDef",
    {
        "ProfileArn": str,
    },
    total=False,
)

DeleteRoomRequestRequestTypeDef = TypedDict(
    "DeleteRoomRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)

_RequiredDeleteRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRoomSkillParameterRequestRequestTypeDef",
    {
        "SkillId": str,
        "ParameterKey": str,
    },
)
_OptionalDeleteRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRoomSkillParameterRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)


class DeleteRoomSkillParameterRequestRequestTypeDef(
    _RequiredDeleteRoomSkillParameterRequestRequestTypeDef,
    _OptionalDeleteRoomSkillParameterRequestRequestTypeDef,
):
    pass


_RequiredDeleteSkillAuthorizationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSkillAuthorizationRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
_OptionalDeleteSkillAuthorizationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSkillAuthorizationRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)


class DeleteSkillAuthorizationRequestRequestTypeDef(
    _RequiredDeleteSkillAuthorizationRequestRequestTypeDef,
    _OptionalDeleteSkillAuthorizationRequestRequestTypeDef,
):
    pass


DeleteSkillGroupRequestRequestTypeDef = TypedDict(
    "DeleteSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
    },
    total=False,
)

_RequiredDeleteUserRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteUserRequestRequestTypeDef",
    {
        "EnrollmentId": str,
    },
)
_OptionalDeleteUserRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteUserRequestRequestTypeDef",
    {
        "UserArn": str,
    },
    total=False,
)


class DeleteUserRequestRequestTypeDef(
    _RequiredDeleteUserRequestRequestTypeDef, _OptionalDeleteUserRequestRequestTypeDef
):
    pass


DeveloperInfoTypeDef = TypedDict(
    "DeveloperInfoTypeDef",
    {
        "DeveloperName": str,
        "PrivacyPolicy": str,
        "Email": str,
        "Url": str,
    },
    total=False,
)

DeviceEventTypeDef = TypedDict(
    "DeviceEventTypeDef",
    {
        "Type": DeviceEventTypeType,
        "Value": str,
        "Timestamp": datetime,
    },
    total=False,
)

DeviceNetworkProfileInfoTypeDef = TypedDict(
    "DeviceNetworkProfileInfoTypeDef",
    {
        "NetworkProfileArn": str,
        "CertificateArn": str,
        "CertificateExpirationTime": datetime,
    },
    total=False,
)

DeviceStatusDetailTypeDef = TypedDict(
    "DeviceStatusDetailTypeDef",
    {
        "Feature": FeatureType,
        "Code": DeviceStatusDetailCodeType,
    },
    total=False,
)

DisassociateContactFromAddressBookRequestRequestTypeDef = TypedDict(
    "DisassociateContactFromAddressBookRequestRequestTypeDef",
    {
        "ContactArn": str,
        "AddressBookArn": str,
    },
)

DisassociateDeviceFromRoomRequestRequestTypeDef = TypedDict(
    "DisassociateDeviceFromRoomRequestRequestTypeDef",
    {
        "DeviceArn": str,
    },
    total=False,
)

_RequiredDisassociateSkillFromSkillGroupRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateSkillFromSkillGroupRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
_OptionalDisassociateSkillFromSkillGroupRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateSkillFromSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
    },
    total=False,
)


class DisassociateSkillFromSkillGroupRequestRequestTypeDef(
    _RequiredDisassociateSkillFromSkillGroupRequestRequestTypeDef,
    _OptionalDisassociateSkillFromSkillGroupRequestRequestTypeDef,
):
    pass


DisassociateSkillFromUsersRequestRequestTypeDef = TypedDict(
    "DisassociateSkillFromUsersRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)

DisassociateSkillGroupFromRoomRequestRequestTypeDef = TypedDict(
    "DisassociateSkillGroupFromRoomRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
        "RoomArn": str,
    },
    total=False,
)

EndOfMeetingReminderTypeDef = TypedDict(
    "EndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": List[int],
        "ReminderType": EndOfMeetingReminderTypeType,
        "Enabled": bool,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
)

ForgetSmartHomeAppliancesRequestRequestTypeDef = TypedDict(
    "ForgetSmartHomeAppliancesRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
)

GatewayGroupSummaryTypeDef = TypedDict(
    "GatewayGroupSummaryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
    },
    total=False,
)

GatewayGroupTypeDef = TypedDict(
    "GatewayGroupTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
    },
    total=False,
)

GatewaySummaryTypeDef = TypedDict(
    "GatewaySummaryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
        "GatewayGroupArn": str,
        "SoftwareVersion": str,
    },
    total=False,
)

GatewayTypeDef = TypedDict(
    "GatewayTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
        "GatewayGroupArn": str,
        "SoftwareVersion": str,
    },
    total=False,
)

GetAddressBookRequestRequestTypeDef = TypedDict(
    "GetAddressBookRequestRequestTypeDef",
    {
        "AddressBookArn": str,
    },
)

GetConferenceProviderRequestRequestTypeDef = TypedDict(
    "GetConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderArn": str,
    },
)

GetContactRequestRequestTypeDef = TypedDict(
    "GetContactRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)

GetDeviceRequestRequestTypeDef = TypedDict(
    "GetDeviceRequestRequestTypeDef",
    {
        "DeviceArn": str,
    },
    total=False,
)

GetGatewayGroupRequestRequestTypeDef = TypedDict(
    "GetGatewayGroupRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
    },
)

GetGatewayRequestRequestTypeDef = TypedDict(
    "GetGatewayRequestRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

GetNetworkProfileRequestRequestTypeDef = TypedDict(
    "GetNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileArn": str,
    },
)

NetworkProfileTypeDef = TypedDict(
    "NetworkProfileTypeDef",
    {
        "NetworkProfileArn": str,
        "NetworkProfileName": str,
        "Description": str,
        "Ssid": str,
        "SecurityType": NetworkSecurityTypeType,
        "EapMethod": Literal["EAP_TLS"],
        "CurrentPassword": str,
        "NextPassword": str,
        "CertificateAuthorityArn": str,
        "TrustAnchors": List[str],
    },
    total=False,
)

GetProfileRequestRequestTypeDef = TypedDict(
    "GetProfileRequestRequestTypeDef",
    {
        "ProfileArn": str,
    },
    total=False,
)

GetRoomRequestRequestTypeDef = TypedDict(
    "GetRoomRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)

RoomTypeDef = TypedDict(
    "RoomTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "Description": str,
        "ProviderCalendarId": str,
        "ProfileArn": str,
    },
    total=False,
)

_RequiredGetRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "_RequiredGetRoomSkillParameterRequestRequestTypeDef",
    {
        "SkillId": str,
        "ParameterKey": str,
    },
)
_OptionalGetRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "_OptionalGetRoomSkillParameterRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)


class GetRoomSkillParameterRequestRequestTypeDef(
    _RequiredGetRoomSkillParameterRequestRequestTypeDef,
    _OptionalGetRoomSkillParameterRequestRequestTypeDef,
):
    pass


RoomSkillParameterTypeDef = TypedDict(
    "RoomSkillParameterTypeDef",
    {
        "ParameterKey": str,
        "ParameterValue": str,
    },
)

GetSkillGroupRequestRequestTypeDef = TypedDict(
    "GetSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
    },
    total=False,
)

SkillGroupTypeDef = TypedDict(
    "SkillGroupTypeDef",
    {
        "SkillGroupArn": str,
        "SkillGroupName": str,
        "Description": str,
    },
    total=False,
)

InstantBookingTypeDef = TypedDict(
    "InstantBookingTypeDef",
    {
        "DurationInMinutes": int,
        "Enabled": bool,
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

ListBusinessReportSchedulesRequestRequestTypeDef = TypedDict(
    "ListBusinessReportSchedulesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListConferenceProvidersRequestRequestTypeDef = TypedDict(
    "ListConferenceProvidersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListDeviceEventsRequestRequestTypeDef = TypedDict(
    "_RequiredListDeviceEventsRequestRequestTypeDef",
    {
        "DeviceArn": str,
    },
)
_OptionalListDeviceEventsRequestRequestTypeDef = TypedDict(
    "_OptionalListDeviceEventsRequestRequestTypeDef",
    {
        "EventType": DeviceEventTypeType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDeviceEventsRequestRequestTypeDef(
    _RequiredListDeviceEventsRequestRequestTypeDef, _OptionalListDeviceEventsRequestRequestTypeDef
):
    pass


ListGatewayGroupsRequestRequestTypeDef = TypedDict(
    "ListGatewayGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListGatewaysRequestRequestTypeDef = TypedDict(
    "ListGatewaysRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListSkillsRequestRequestTypeDef = TypedDict(
    "ListSkillsRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
        "EnablementType": EnablementTypeFilterType,
        "SkillType": SkillTypeFilterType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SkillSummaryTypeDef = TypedDict(
    "SkillSummaryTypeDef",
    {
        "SkillId": str,
        "SkillName": str,
        "SupportsLinking": bool,
        "EnablementType": EnablementTypeType,
        "SkillType": SkillTypeType,
    },
    total=False,
)

ListSkillsStoreCategoriesRequestRequestTypeDef = TypedDict(
    "ListSkillsStoreCategoriesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListSkillsStoreSkillsByCategoryRequestRequestTypeDef = TypedDict(
    "_RequiredListSkillsStoreSkillsByCategoryRequestRequestTypeDef",
    {
        "CategoryId": int,
    },
)
_OptionalListSkillsStoreSkillsByCategoryRequestRequestTypeDef = TypedDict(
    "_OptionalListSkillsStoreSkillsByCategoryRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListSkillsStoreSkillsByCategoryRequestRequestTypeDef(
    _RequiredListSkillsStoreSkillsByCategoryRequestRequestTypeDef,
    _OptionalListSkillsStoreSkillsByCategoryRequestRequestTypeDef,
):
    pass


_RequiredListSmartHomeAppliancesRequestRequestTypeDef = TypedDict(
    "_RequiredListSmartHomeAppliancesRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
)
_OptionalListSmartHomeAppliancesRequestRequestTypeDef = TypedDict(
    "_OptionalListSmartHomeAppliancesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListSmartHomeAppliancesRequestRequestTypeDef(
    _RequiredListSmartHomeAppliancesRequestRequestTypeDef,
    _OptionalListSmartHomeAppliancesRequestRequestTypeDef,
):
    pass


SmartHomeApplianceTypeDef = TypedDict(
    "SmartHomeApplianceTypeDef",
    {
        "FriendlyName": str,
        "Description": str,
        "ManufacturerName": str,
    },
    total=False,
)

_RequiredListTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsRequestRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalListTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTagsRequestRequestTypeDef(
    _RequiredListTagsRequestRequestTypeDef, _OptionalListTagsRequestRequestTypeDef
):
    pass


RequireCheckInTypeDef = TypedDict(
    "RequireCheckInTypeDef",
    {
        "ReleaseAfterMinutes": int,
        "Enabled": bool,
    },
    total=False,
)

NetworkProfileDataTypeDef = TypedDict(
    "NetworkProfileDataTypeDef",
    {
        "NetworkProfileArn": str,
        "NetworkProfileName": str,
        "Description": str,
        "Ssid": str,
        "SecurityType": NetworkSecurityTypeType,
        "EapMethod": Literal["EAP_TLS"],
        "CertificateAuthorityArn": str,
    },
    total=False,
)

ProfileDataTypeDef = TypedDict(
    "ProfileDataTypeDef",
    {
        "ProfileArn": str,
        "ProfileName": str,
        "IsDefault": bool,
        "Address": str,
        "Timezone": str,
        "DistanceUnit": DistanceUnitType,
        "TemperatureUnit": TemperatureUnitType,
        "WakeWord": WakeWordType,
        "Locale": str,
    },
    total=False,
)

_RequiredPutInvitationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutInvitationConfigurationRequestRequestTypeDef",
    {
        "OrganizationName": str,
    },
)
_OptionalPutInvitationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutInvitationConfigurationRequestRequestTypeDef",
    {
        "ContactEmail": str,
        "PrivateSkillIds": Sequence[str],
    },
    total=False,
)


class PutInvitationConfigurationRequestRequestTypeDef(
    _RequiredPutInvitationConfigurationRequestRequestTypeDef,
    _OptionalPutInvitationConfigurationRequestRequestTypeDef,
):
    pass


_RequiredPutSkillAuthorizationRequestRequestTypeDef = TypedDict(
    "_RequiredPutSkillAuthorizationRequestRequestTypeDef",
    {
        "AuthorizationResult": Mapping[str, str],
        "SkillId": str,
    },
)
_OptionalPutSkillAuthorizationRequestRequestTypeDef = TypedDict(
    "_OptionalPutSkillAuthorizationRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)


class PutSkillAuthorizationRequestRequestTypeDef(
    _RequiredPutSkillAuthorizationRequestRequestTypeDef,
    _OptionalPutSkillAuthorizationRequestRequestTypeDef,
):
    pass


RejectSkillRequestRequestTypeDef = TypedDict(
    "RejectSkillRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)

ResolveRoomRequestRequestTypeDef = TypedDict(
    "ResolveRoomRequestRequestTypeDef",
    {
        "UserId": str,
        "SkillId": str,
    },
)

RevokeInvitationRequestRequestTypeDef = TypedDict(
    "RevokeInvitationRequestRequestTypeDef",
    {
        "UserArn": str,
        "EnrollmentId": str,
    },
    total=False,
)

RoomDataTypeDef = TypedDict(
    "RoomDataTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "Description": str,
        "ProviderCalendarId": str,
        "ProfileArn": str,
        "ProfileName": str,
    },
    total=False,
)

SortTypeDef = TypedDict(
    "SortTypeDef",
    {
        "Key": str,
        "Value": SortValueType,
    },
)

SkillGroupDataTypeDef = TypedDict(
    "SkillGroupDataTypeDef",
    {
        "SkillGroupArn": str,
        "SkillGroupName": str,
        "Description": str,
    },
    total=False,
)

UserDataTypeDef = TypedDict(
    "UserDataTypeDef",
    {
        "UserArn": str,
        "FirstName": str,
        "LastName": str,
        "Email": str,
        "EnrollmentStatus": EnrollmentStatusType,
        "EnrollmentId": str,
    },
    total=False,
)

SendInvitationRequestRequestTypeDef = TypedDict(
    "SendInvitationRequestRequestTypeDef",
    {
        "UserArn": str,
    },
    total=False,
)

_RequiredStartDeviceSyncRequestRequestTypeDef = TypedDict(
    "_RequiredStartDeviceSyncRequestRequestTypeDef",
    {
        "Features": Sequence[FeatureType],
    },
)
_OptionalStartDeviceSyncRequestRequestTypeDef = TypedDict(
    "_OptionalStartDeviceSyncRequestRequestTypeDef",
    {
        "RoomArn": str,
        "DeviceArn": str,
    },
    total=False,
)


class StartDeviceSyncRequestRequestTypeDef(
    _RequiredStartDeviceSyncRequestRequestTypeDef, _OptionalStartDeviceSyncRequestRequestTypeDef
):
    pass


StartSmartHomeApplianceDiscoveryRequestRequestTypeDef = TypedDict(
    "StartSmartHomeApplianceDiscoveryRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAddressBookRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAddressBookRequestRequestTypeDef",
    {
        "AddressBookArn": str,
    },
)
_OptionalUpdateAddressBookRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAddressBookRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)


class UpdateAddressBookRequestRequestTypeDef(
    _RequiredUpdateAddressBookRequestRequestTypeDef, _OptionalUpdateAddressBookRequestRequestTypeDef
):
    pass


UpdateDeviceRequestRequestTypeDef = TypedDict(
    "UpdateDeviceRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "DeviceName": str,
    },
    total=False,
)

UpdateEndOfMeetingReminderTypeDef = TypedDict(
    "UpdateEndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": Sequence[int],
        "ReminderType": EndOfMeetingReminderTypeType,
        "Enabled": bool,
    },
    total=False,
)

_RequiredUpdateGatewayGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayGroupRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
    },
)
_OptionalUpdateGatewayGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)


class UpdateGatewayGroupRequestRequestTypeDef(
    _RequiredUpdateGatewayGroupRequestRequestTypeDef,
    _OptionalUpdateGatewayGroupRequestRequestTypeDef,
):
    pass


_RequiredUpdateGatewayRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayRequestRequestTypeDef",
    {
        "GatewayArn": str,
    },
)
_OptionalUpdateGatewayRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "SoftwareVersion": str,
    },
    total=False,
)


class UpdateGatewayRequestRequestTypeDef(
    _RequiredUpdateGatewayRequestRequestTypeDef, _OptionalUpdateGatewayRequestRequestTypeDef
):
    pass


UpdateInstantBookingTypeDef = TypedDict(
    "UpdateInstantBookingTypeDef",
    {
        "DurationInMinutes": int,
        "Enabled": bool,
    },
    total=False,
)

UpdateRequireCheckInTypeDef = TypedDict(
    "UpdateRequireCheckInTypeDef",
    {
        "ReleaseAfterMinutes": int,
        "Enabled": bool,
    },
    total=False,
)

_RequiredUpdateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileArn": str,
    },
)
_OptionalUpdateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileName": str,
        "Description": str,
        "CurrentPassword": str,
        "NextPassword": str,
        "CertificateAuthorityArn": str,
        "TrustAnchors": Sequence[str],
    },
    total=False,
)


class UpdateNetworkProfileRequestRequestTypeDef(
    _RequiredUpdateNetworkProfileRequestRequestTypeDef,
    _OptionalUpdateNetworkProfileRequestRequestTypeDef,
):
    pass


UpdateRoomRequestRequestTypeDef = TypedDict(
    "UpdateRoomRequestRequestTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "Description": str,
        "ProviderCalendarId": str,
        "ProfileArn": str,
    },
    total=False,
)

UpdateSkillGroupRequestRequestTypeDef = TypedDict(
    "UpdateSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": str,
        "SkillGroupName": str,
        "Description": str,
    },
    total=False,
)

_RequiredUpdateBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBusinessReportScheduleRequestRequestTypeDef",
    {
        "ScheduleArn": str,
    },
)
_OptionalUpdateBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBusinessReportScheduleRequestRequestTypeDef",
    {
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "Format": BusinessReportFormatType,
        "ScheduleName": str,
        "Recurrence": BusinessReportRecurrenceTypeDef,
    },
    total=False,
)


class UpdateBusinessReportScheduleRequestRequestTypeDef(
    _RequiredUpdateBusinessReportScheduleRequestRequestTypeDef,
    _OptionalUpdateBusinessReportScheduleRequestRequestTypeDef,
):
    pass


BusinessReportTypeDef = TypedDict(
    "BusinessReportTypeDef",
    {
        "Status": BusinessReportStatusType,
        "FailureCode": BusinessReportFailureCodeType,
        "S3Location": BusinessReportS3LocationTypeDef,
        "DeliveryTime": datetime,
        "DownloadUrl": str,
    },
    total=False,
)

PutConferencePreferenceRequestRequestTypeDef = TypedDict(
    "PutConferencePreferenceRequestRequestTypeDef",
    {
        "ConferencePreference": ConferencePreferenceTypeDef,
    },
)

ConferenceProviderTypeDef = TypedDict(
    "ConferenceProviderTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": ConferenceProviderTypeType,
        "IPDialIn": IPDialInTypeDef,
        "PSTNDialIn": PSTNDialInTypeDef,
        "MeetingSetting": MeetingSettingTypeDef,
    },
    total=False,
)

_RequiredUpdateConferenceProviderRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderArn": str,
        "ConferenceProviderType": ConferenceProviderTypeType,
        "MeetingSetting": MeetingSettingTypeDef,
    },
)
_OptionalUpdateConferenceProviderRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConferenceProviderRequestRequestTypeDef",
    {
        "IPDialIn": IPDialInTypeDef,
        "PSTNDialIn": PSTNDialInTypeDef,
    },
    total=False,
)


class UpdateConferenceProviderRequestRequestTypeDef(
    _RequiredUpdateConferenceProviderRequestRequestTypeDef,
    _OptionalUpdateConferenceProviderRequestRequestTypeDef,
):
    pass


ContactDataTypeDef = TypedDict(
    "ContactDataTypeDef",
    {
        "ContactArn": str,
        "DisplayName": str,
        "FirstName": str,
        "LastName": str,
        "PhoneNumber": str,
        "PhoneNumbers": List[PhoneNumberTypeDef],
        "SipAddresses": List[SipAddressTypeDef],
    },
    total=False,
)

ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "ContactArn": str,
        "DisplayName": str,
        "FirstName": str,
        "LastName": str,
        "PhoneNumber": str,
        "PhoneNumbers": List[PhoneNumberTypeDef],
        "SipAddresses": List[SipAddressTypeDef],
    },
    total=False,
)

_RequiredUpdateContactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)
_OptionalUpdateContactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactRequestRequestTypeDef",
    {
        "DisplayName": str,
        "FirstName": str,
        "LastName": str,
        "PhoneNumber": str,
        "PhoneNumbers": Sequence[PhoneNumberTypeDef],
        "SipAddresses": Sequence[SipAddressTypeDef],
    },
    total=False,
)


class UpdateContactRequestRequestTypeDef(
    _RequiredUpdateContactRequestRequestTypeDef, _OptionalUpdateContactRequestRequestTypeDef
):
    pass


ContentTypeDef = TypedDict(
    "ContentTypeDef",
    {
        "TextList": Sequence[TextTypeDef],
        "SsmlList": Sequence[SsmlTypeDef],
        "AudioList": Sequence[AudioTypeDef],
    },
    total=False,
)

_RequiredCreateAddressBookRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAddressBookRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateAddressBookRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAddressBookRequestRequestTypeDef",
    {
        "Description": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAddressBookRequestRequestTypeDef(
    _RequiredCreateAddressBookRequestRequestTypeDef, _OptionalCreateAddressBookRequestRequestTypeDef
):
    pass


_RequiredCreateBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBusinessReportScheduleRequestRequestTypeDef",
    {
        "Format": BusinessReportFormatType,
        "ContentRange": BusinessReportContentRangeTypeDef,
    },
)
_OptionalCreateBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBusinessReportScheduleRequestRequestTypeDef",
    {
        "ScheduleName": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "Recurrence": BusinessReportRecurrenceTypeDef,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateBusinessReportScheduleRequestRequestTypeDef(
    _RequiredCreateBusinessReportScheduleRequestRequestTypeDef,
    _OptionalCreateBusinessReportScheduleRequestRequestTypeDef,
):
    pass


_RequiredCreateConferenceProviderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderName": str,
        "ConferenceProviderType": ConferenceProviderTypeType,
        "MeetingSetting": MeetingSettingTypeDef,
    },
)
_OptionalCreateConferenceProviderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConferenceProviderRequestRequestTypeDef",
    {
        "IPDialIn": IPDialInTypeDef,
        "PSTNDialIn": PSTNDialInTypeDef,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateConferenceProviderRequestRequestTypeDef(
    _RequiredCreateConferenceProviderRequestRequestTypeDef,
    _OptionalCreateConferenceProviderRequestRequestTypeDef,
):
    pass


_RequiredCreateContactRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactRequestRequestTypeDef",
    {
        "FirstName": str,
    },
)
_OptionalCreateContactRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactRequestRequestTypeDef",
    {
        "DisplayName": str,
        "LastName": str,
        "PhoneNumber": str,
        "PhoneNumbers": Sequence[PhoneNumberTypeDef],
        "SipAddresses": Sequence[SipAddressTypeDef],
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateContactRequestRequestTypeDef(
    _RequiredCreateContactRequestRequestTypeDef, _OptionalCreateContactRequestRequestTypeDef
):
    pass


_RequiredCreateGatewayGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGatewayGroupRequestRequestTypeDef",
    {
        "Name": str,
        "ClientRequestToken": str,
    },
)
_OptionalCreateGatewayGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGatewayGroupRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGatewayGroupRequestRequestTypeDef(
    _RequiredCreateGatewayGroupRequestRequestTypeDef,
    _OptionalCreateGatewayGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileName": str,
        "Ssid": str,
        "SecurityType": NetworkSecurityTypeType,
        "ClientRequestToken": str,
    },
)
_OptionalCreateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkProfileRequestRequestTypeDef",
    {
        "Description": str,
        "EapMethod": Literal["EAP_TLS"],
        "CurrentPassword": str,
        "NextPassword": str,
        "CertificateAuthorityArn": str,
        "TrustAnchors": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateNetworkProfileRequestRequestTypeDef(
    _RequiredCreateNetworkProfileRequestRequestTypeDef,
    _OptionalCreateNetworkProfileRequestRequestTypeDef,
):
    pass


_RequiredCreateRoomRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRoomRequestRequestTypeDef",
    {
        "RoomName": str,
    },
)
_OptionalCreateRoomRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRoomRequestRequestTypeDef",
    {
        "Description": str,
        "ProfileArn": str,
        "ProviderCalendarId": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRoomRequestRequestTypeDef(
    _RequiredCreateRoomRequestRequestTypeDef, _OptionalCreateRoomRequestRequestTypeDef
):
    pass


_RequiredCreateSkillGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupName": str,
    },
)
_OptionalCreateSkillGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSkillGroupRequestRequestTypeDef",
    {
        "Description": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSkillGroupRequestRequestTypeDef(
    _RequiredCreateSkillGroupRequestRequestTypeDef, _OptionalCreateSkillGroupRequestRequestTypeDef
):
    pass


_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "UserId": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "FirstName": str,
        "LastName": str,
        "Email": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass


_RequiredRegisterAVSDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterAVSDeviceRequestRequestTypeDef",
    {
        "ClientId": str,
        "UserCode": str,
        "ProductId": str,
        "AmazonId": str,
    },
)
_OptionalRegisterAVSDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterAVSDeviceRequestRequestTypeDef",
    {
        "DeviceSerialNumber": str,
        "RoomArn": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class RegisterAVSDeviceRequestRequestTypeDef(
    _RequiredRegisterAVSDeviceRequestRequestTypeDef, _OptionalRegisterAVSDeviceRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateAddressBookResponseTypeDef = TypedDict(
    "CreateAddressBookResponseTypeDef",
    {
        "AddressBookArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBusinessReportScheduleResponseTypeDef = TypedDict(
    "CreateBusinessReportScheduleResponseTypeDef",
    {
        "ScheduleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConferenceProviderResponseTypeDef = TypedDict(
    "CreateConferenceProviderResponseTypeDef",
    {
        "ConferenceProviderArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateContactResponseTypeDef = TypedDict(
    "CreateContactResponseTypeDef",
    {
        "ContactArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGatewayGroupResponseTypeDef = TypedDict(
    "CreateGatewayGroupResponseTypeDef",
    {
        "GatewayGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNetworkProfileResponseTypeDef = TypedDict(
    "CreateNetworkProfileResponseTypeDef",
    {
        "NetworkProfileArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProfileResponseTypeDef = TypedDict(
    "CreateProfileResponseTypeDef",
    {
        "ProfileArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRoomResponseTypeDef = TypedDict(
    "CreateRoomResponseTypeDef",
    {
        "RoomArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSkillGroupResponseTypeDef = TypedDict(
    "CreateSkillGroupResponseTypeDef",
    {
        "SkillGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "UserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAddressBookResponseTypeDef = TypedDict(
    "GetAddressBookResponseTypeDef",
    {
        "AddressBook": AddressBookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConferencePreferenceResponseTypeDef = TypedDict(
    "GetConferencePreferenceResponseTypeDef",
    {
        "Preference": ConferencePreferenceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInvitationConfigurationResponseTypeDef = TypedDict(
    "GetInvitationConfigurationResponseTypeDef",
    {
        "OrganizationName": str,
        "ContactEmail": str,
        "PrivateSkillIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSkillsStoreCategoriesResponseTypeDef = TypedDict(
    "ListSkillsStoreCategoriesResponseTypeDef",
    {
        "CategoryList": List[CategoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterAVSDeviceResponseTypeDef = TypedDict(
    "RegisterAVSDeviceResponseTypeDef",
    {
        "DeviceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAddressBooksResponseTypeDef = TypedDict(
    "SearchAddressBooksResponseTypeDef",
    {
        "AddressBooks": List[AddressBookDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendAnnouncementResponseTypeDef = TypedDict(
    "SendAnnouncementResponseTypeDef",
    {
        "AnnouncementArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMeetingRoomConfigurationTypeDef = TypedDict(
    "CreateMeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": bool,
        "EndOfMeetingReminder": CreateEndOfMeetingReminderTypeDef,
        "InstantBooking": CreateInstantBookingTypeDef,
        "RequireCheckIn": CreateRequireCheckInTypeDef,
    },
    total=False,
)

SkillDetailsTypeDef = TypedDict(
    "SkillDetailsTypeDef",
    {
        "ProductDescription": str,
        "InvocationPhrase": str,
        "ReleaseDate": str,
        "EndUserLicenseAgreement": str,
        "GenericKeywords": List[str],
        "BulletPoints": List[str],
        "NewInThisVersionBulletPoints": List[str],
        "SkillTypes": List[str],
        "Reviews": Dict[str, str],
        "DeveloperInfo": DeveloperInfoTypeDef,
    },
    total=False,
)

ListDeviceEventsResponseTypeDef = TypedDict(
    "ListDeviceEventsResponseTypeDef",
    {
        "DeviceEvents": List[DeviceEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeviceStatusInfoTypeDef = TypedDict(
    "DeviceStatusInfoTypeDef",
    {
        "DeviceStatusDetails": List[DeviceStatusDetailTypeDef],
        "ConnectionStatus": ConnectionStatusType,
        "ConnectionStatusUpdatedTime": datetime,
    },
    total=False,
)

ListGatewayGroupsResponseTypeDef = TypedDict(
    "ListGatewayGroupsResponseTypeDef",
    {
        "GatewayGroups": List[GatewayGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGatewayGroupResponseTypeDef = TypedDict(
    "GetGatewayGroupResponseTypeDef",
    {
        "GatewayGroup": GatewayGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {
        "Gateways": List[GatewaySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGatewayResponseTypeDef = TypedDict(
    "GetGatewayResponseTypeDef",
    {
        "Gateway": GatewayTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNetworkProfileResponseTypeDef = TypedDict(
    "GetNetworkProfileResponseTypeDef",
    {
        "NetworkProfile": NetworkProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRoomResponseTypeDef = TypedDict(
    "GetRoomResponseTypeDef",
    {
        "Room": RoomTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRoomSkillParameterResponseTypeDef = TypedDict(
    "GetRoomSkillParameterResponseTypeDef",
    {
        "RoomSkillParameter": RoomSkillParameterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "_RequiredPutRoomSkillParameterRequestRequestTypeDef",
    {
        "SkillId": str,
        "RoomSkillParameter": RoomSkillParameterTypeDef,
    },
)
_OptionalPutRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "_OptionalPutRoomSkillParameterRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
    total=False,
)


class PutRoomSkillParameterRequestRequestTypeDef(
    _RequiredPutRoomSkillParameterRequestRequestTypeDef,
    _OptionalPutRoomSkillParameterRequestRequestTypeDef,
):
    pass


ResolveRoomResponseTypeDef = TypedDict(
    "ResolveRoomResponseTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "RoomSkillParameters": List[RoomSkillParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSkillGroupResponseTypeDef = TypedDict(
    "GetSkillGroupResponseTypeDef",
    {
        "SkillGroup": SkillGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBusinessReportSchedulesRequestListBusinessReportSchedulesPaginateTypeDef = TypedDict(
    "ListBusinessReportSchedulesRequestListBusinessReportSchedulesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListConferenceProvidersRequestListConferenceProvidersPaginateTypeDef = TypedDict(
    "ListConferenceProvidersRequestListConferenceProvidersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDeviceEventsRequestListDeviceEventsPaginateTypeDef = TypedDict(
    "_RequiredListDeviceEventsRequestListDeviceEventsPaginateTypeDef",
    {
        "DeviceArn": str,
    },
)
_OptionalListDeviceEventsRequestListDeviceEventsPaginateTypeDef = TypedDict(
    "_OptionalListDeviceEventsRequestListDeviceEventsPaginateTypeDef",
    {
        "EventType": DeviceEventTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDeviceEventsRequestListDeviceEventsPaginateTypeDef(
    _RequiredListDeviceEventsRequestListDeviceEventsPaginateTypeDef,
    _OptionalListDeviceEventsRequestListDeviceEventsPaginateTypeDef,
):
    pass


ListSkillsRequestListSkillsPaginateTypeDef = TypedDict(
    "ListSkillsRequestListSkillsPaginateTypeDef",
    {
        "SkillGroupArn": str,
        "EnablementType": EnablementTypeFilterType,
        "SkillType": SkillTypeFilterType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSkillsStoreCategoriesRequestListSkillsStoreCategoriesPaginateTypeDef = TypedDict(
    "ListSkillsStoreCategoriesRequestListSkillsStoreCategoriesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef = TypedDict(
    "_RequiredListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef",
    {
        "CategoryId": int,
    },
)
_OptionalListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef = TypedDict(
    "_OptionalListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef(
    _RequiredListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef,
    _OptionalListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef,
):
    pass


_RequiredListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef = TypedDict(
    "_RequiredListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef",
    {
        "RoomArn": str,
    },
)
_OptionalListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef = TypedDict(
    "_OptionalListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef(
    _RequiredListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef,
    _OptionalListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef,
):
    pass


_RequiredListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_RequiredListTagsRequestListTagsPaginateTypeDef",
    {
        "Arn": str,
    },
)
_OptionalListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_OptionalListTagsRequestListTagsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsRequestListTagsPaginateTypeDef(
    _RequiredListTagsRequestListTagsPaginateTypeDef, _OptionalListTagsRequestListTagsPaginateTypeDef
):
    pass


ListSkillsResponseTypeDef = TypedDict(
    "ListSkillsResponseTypeDef",
    {
        "SkillSummaries": List[SkillSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSmartHomeAppliancesResponseTypeDef = TypedDict(
    "ListSmartHomeAppliancesResponseTypeDef",
    {
        "SmartHomeAppliances": List[SmartHomeApplianceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MeetingRoomConfigurationTypeDef = TypedDict(
    "MeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": bool,
        "EndOfMeetingReminder": EndOfMeetingReminderTypeDef,
        "InstantBooking": InstantBookingTypeDef,
        "RequireCheckIn": RequireCheckInTypeDef,
    },
    total=False,
)

SearchNetworkProfilesResponseTypeDef = TypedDict(
    "SearchNetworkProfilesResponseTypeDef",
    {
        "NetworkProfiles": List[NetworkProfileDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchProfilesResponseTypeDef = TypedDict(
    "SearchProfilesResponseTypeDef",
    {
        "Profiles": List[ProfileDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchRoomsResponseTypeDef = TypedDict(
    "SearchRoomsResponseTypeDef",
    {
        "Rooms": List[RoomDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAddressBooksRequestRequestTypeDef = TypedDict(
    "SearchAddressBooksRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SearchContactsRequestRequestTypeDef = TypedDict(
    "SearchContactsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SearchDevicesRequestRequestTypeDef = TypedDict(
    "SearchDevicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
    },
    total=False,
)

SearchDevicesRequestSearchDevicesPaginateTypeDef = TypedDict(
    "SearchDevicesRequestSearchDevicesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SearchNetworkProfilesRequestRequestTypeDef = TypedDict(
    "SearchNetworkProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
    },
    total=False,
)

SearchProfilesRequestRequestTypeDef = TypedDict(
    "SearchProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
    },
    total=False,
)

SearchProfilesRequestSearchProfilesPaginateTypeDef = TypedDict(
    "SearchProfilesRequestSearchProfilesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SearchRoomsRequestRequestTypeDef = TypedDict(
    "SearchRoomsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
    },
    total=False,
)

SearchRoomsRequestSearchRoomsPaginateTypeDef = TypedDict(
    "SearchRoomsRequestSearchRoomsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SearchSkillGroupsRequestRequestTypeDef = TypedDict(
    "SearchSkillGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
    },
    total=False,
)

SearchSkillGroupsRequestSearchSkillGroupsPaginateTypeDef = TypedDict(
    "SearchSkillGroupsRequestSearchSkillGroupsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SearchUsersRequestRequestTypeDef = TypedDict(
    "SearchUsersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
    },
    total=False,
)

SearchUsersRequestSearchUsersPaginateTypeDef = TypedDict(
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortCriteria": Sequence[SortTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SearchSkillGroupsResponseTypeDef = TypedDict(
    "SearchSkillGroupsResponseTypeDef",
    {
        "SkillGroups": List[SkillGroupDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchUsersResponseTypeDef = TypedDict(
    "SearchUsersResponseTypeDef",
    {
        "Users": List[UserDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMeetingRoomConfigurationTypeDef = TypedDict(
    "UpdateMeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": bool,
        "EndOfMeetingReminder": UpdateEndOfMeetingReminderTypeDef,
        "InstantBooking": UpdateInstantBookingTypeDef,
        "RequireCheckIn": UpdateRequireCheckInTypeDef,
    },
    total=False,
)

BusinessReportScheduleTypeDef = TypedDict(
    "BusinessReportScheduleTypeDef",
    {
        "ScheduleArn": str,
        "ScheduleName": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "Format": BusinessReportFormatType,
        "ContentRange": BusinessReportContentRangeTypeDef,
        "Recurrence": BusinessReportRecurrenceTypeDef,
        "LastBusinessReport": BusinessReportTypeDef,
    },
    total=False,
)

GetConferenceProviderResponseTypeDef = TypedDict(
    "GetConferenceProviderResponseTypeDef",
    {
        "ConferenceProvider": ConferenceProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConferenceProvidersResponseTypeDef = TypedDict(
    "ListConferenceProvidersResponseTypeDef",
    {
        "ConferenceProviders": List[ConferenceProviderTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchContactsResponseTypeDef = TypedDict(
    "SearchContactsResponseTypeDef",
    {
        "Contacts": List[ContactDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactResponseTypeDef = TypedDict(
    "GetContactResponseTypeDef",
    {
        "Contact": ContactTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSendAnnouncementRequestRequestTypeDef = TypedDict(
    "_RequiredSendAnnouncementRequestRequestTypeDef",
    {
        "RoomFilters": Sequence[FilterTypeDef],
        "Content": ContentTypeDef,
        "ClientRequestToken": str,
    },
)
_OptionalSendAnnouncementRequestRequestTypeDef = TypedDict(
    "_OptionalSendAnnouncementRequestRequestTypeDef",
    {
        "TimeToLiveInSeconds": int,
    },
    total=False,
)


class SendAnnouncementRequestRequestTypeDef(
    _RequiredSendAnnouncementRequestRequestTypeDef, _OptionalSendAnnouncementRequestRequestTypeDef
):
    pass


_RequiredCreateProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProfileRequestRequestTypeDef",
    {
        "ProfileName": str,
        "Timezone": str,
        "Address": str,
        "DistanceUnit": DistanceUnitType,
        "TemperatureUnit": TemperatureUnitType,
        "WakeWord": WakeWordType,
    },
)
_OptionalCreateProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProfileRequestRequestTypeDef",
    {
        "Locale": str,
        "ClientRequestToken": str,
        "SetupModeDisabled": bool,
        "MaxVolumeLimit": int,
        "PSTNEnabled": bool,
        "DataRetentionOptIn": bool,
        "MeetingRoomConfiguration": CreateMeetingRoomConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateProfileRequestRequestTypeDef(
    _RequiredCreateProfileRequestRequestTypeDef, _OptionalCreateProfileRequestRequestTypeDef
):
    pass


SkillsStoreSkillTypeDef = TypedDict(
    "SkillsStoreSkillTypeDef",
    {
        "SkillId": str,
        "SkillName": str,
        "ShortDescription": str,
        "IconUrl": str,
        "SampleUtterances": List[str],
        "SkillDetails": SkillDetailsTypeDef,
        "SupportsLinking": bool,
    },
    total=False,
)

DeviceDataTypeDef = TypedDict(
    "DeviceDataTypeDef",
    {
        "DeviceArn": str,
        "DeviceSerialNumber": str,
        "DeviceType": str,
        "DeviceName": str,
        "SoftwareVersion": str,
        "MacAddress": str,
        "DeviceStatus": DeviceStatusType,
        "NetworkProfileArn": str,
        "NetworkProfileName": str,
        "RoomArn": str,
        "RoomName": str,
        "DeviceStatusInfo": DeviceStatusInfoTypeDef,
        "CreatedTime": datetime,
    },
    total=False,
)

DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "DeviceArn": str,
        "DeviceSerialNumber": str,
        "DeviceType": str,
        "DeviceName": str,
        "SoftwareVersion": str,
        "MacAddress": str,
        "RoomArn": str,
        "DeviceStatus": DeviceStatusType,
        "DeviceStatusInfo": DeviceStatusInfoTypeDef,
        "NetworkProfileInfo": DeviceNetworkProfileInfoTypeDef,
    },
    total=False,
)

ProfileTypeDef = TypedDict(
    "ProfileTypeDef",
    {
        "ProfileArn": str,
        "ProfileName": str,
        "IsDefault": bool,
        "Address": str,
        "Timezone": str,
        "DistanceUnit": DistanceUnitType,
        "TemperatureUnit": TemperatureUnitType,
        "WakeWord": WakeWordType,
        "Locale": str,
        "SetupModeDisabled": bool,
        "MaxVolumeLimit": int,
        "PSTNEnabled": bool,
        "DataRetentionOptIn": bool,
        "AddressBookArn": str,
        "MeetingRoomConfiguration": MeetingRoomConfigurationTypeDef,
    },
    total=False,
)

UpdateProfileRequestRequestTypeDef = TypedDict(
    "UpdateProfileRequestRequestTypeDef",
    {
        "ProfileArn": str,
        "ProfileName": str,
        "IsDefault": bool,
        "Timezone": str,
        "Address": str,
        "DistanceUnit": DistanceUnitType,
        "TemperatureUnit": TemperatureUnitType,
        "WakeWord": WakeWordType,
        "Locale": str,
        "SetupModeDisabled": bool,
        "MaxVolumeLimit": int,
        "PSTNEnabled": bool,
        "DataRetentionOptIn": bool,
        "MeetingRoomConfiguration": UpdateMeetingRoomConfigurationTypeDef,
    },
    total=False,
)

ListBusinessReportSchedulesResponseTypeDef = TypedDict(
    "ListBusinessReportSchedulesResponseTypeDef",
    {
        "BusinessReportSchedules": List[BusinessReportScheduleTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSkillsStoreSkillsByCategoryResponseTypeDef = TypedDict(
    "ListSkillsStoreSkillsByCategoryResponseTypeDef",
    {
        "SkillsStoreSkills": List[SkillsStoreSkillTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchDevicesResponseTypeDef = TypedDict(
    "SearchDevicesResponseTypeDef",
    {
        "Devices": List[DeviceDataTypeDef],
        "NextToken": str,
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeviceResponseTypeDef = TypedDict(
    "GetDeviceResponseTypeDef",
    {
        "Device": DeviceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProfileResponseTypeDef = TypedDict(
    "GetProfileResponseTypeDef",
    {
        "Profile": ProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
