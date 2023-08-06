"""
Type annotations for iotwireless service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotwireless.type_defs import SessionKeysAbpV1_0_xTypeDef

    data: SessionKeysAbpV1_0_xTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    BatteryLevelType,
    ConnectionStatusType,
    DeviceStateType,
    DlClassType,
    EventNotificationResourceTypeType,
    EventNotificationTopicStatusType,
    EventType,
    ExpressionTypeType,
    FuotaDeviceStatusType,
    FuotaTaskStatusType,
    IdentifierTypeType,
    LogLevelType,
    MessageTypeType,
    SigningAlgType,
    SupportedRfRegionType,
    WirelessDeviceEventType,
    WirelessDeviceFrameInfoType,
    WirelessDeviceIdTypeType,
    WirelessDeviceTypeType,
    WirelessGatewayEventType,
    WirelessGatewayIdTypeType,
    WirelessGatewayServiceTypeType,
    WirelessGatewayTaskStatusType,
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
    "SessionKeysAbpV1_0_xTypeDef",
    "SessionKeysAbpV1_1TypeDef",
    "SidewalkAccountInfoTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef",
    "AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef",
    "AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    "AssociateWirelessDeviceWithThingRequestRequestTypeDef",
    "AssociateWirelessGatewayWithCertificateRequestRequestTypeDef",
    "AssociateWirelessGatewayWithThingRequestRequestTypeDef",
    "CancelMulticastGroupSessionRequestRequestTypeDef",
    "CertificateListTypeDef",
    "LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef",
    "LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef",
    "LoRaWANDeviceProfileTypeDef",
    "LoRaWANFuotaTaskTypeDef",
    "LoRaWANMulticastTypeDef",
    "TraceContentTypeDef",
    "LoRaWANServiceProfileTypeDef",
    "LoRaWANGatewayTypeDef",
    "CreateWirelessGatewayTaskRequestRequestTypeDef",
    "DeleteDestinationRequestRequestTypeDef",
    "DeleteDeviceProfileRequestRequestTypeDef",
    "DeleteFuotaTaskRequestRequestTypeDef",
    "DeleteMulticastGroupRequestRequestTypeDef",
    "DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "DeleteQueuedMessagesRequestRequestTypeDef",
    "DeleteServiceProfileRequestRequestTypeDef",
    "DeleteWirelessDeviceRequestRequestTypeDef",
    "DeleteWirelessGatewayRequestRequestTypeDef",
    "DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    "DeleteWirelessGatewayTaskRequestRequestTypeDef",
    "DestinationsTypeDef",
    "DeviceProfileTypeDef",
    "SidewalkEventNotificationConfigurationsTypeDef",
    "SidewalkResourceTypeEventConfigurationTypeDef",
    "DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef",
    "DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef",
    "DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef",
    "DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    "DisassociateWirelessDeviceFromThingRequestRequestTypeDef",
    "DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef",
    "DisassociateWirelessGatewayFromThingRequestRequestTypeDef",
    "LoRaWANSendDataToDeviceTypeDef",
    "FPortsTypeDef",
    "FuotaTaskTypeDef",
    "GetDestinationRequestRequestTypeDef",
    "GetDeviceProfileRequestRequestTypeDef",
    "GetFuotaTaskRequestRequestTypeDef",
    "LoRaWANFuotaTaskGetInfoTypeDef",
    "GetMulticastGroupRequestRequestTypeDef",
    "LoRaWANMulticastGetTypeDef",
    "GetMulticastGroupSessionRequestRequestTypeDef",
    "LoRaWANMulticastSessionTypeDef",
    "GetNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "GetPartnerAccountRequestRequestTypeDef",
    "SidewalkAccountInfoWithFingerprintTypeDef",
    "GetResourceEventConfigurationRequestRequestTypeDef",
    "GetResourceLogLevelRequestRequestTypeDef",
    "GetServiceEndpointRequestRequestTypeDef",
    "GetServiceProfileRequestRequestTypeDef",
    "LoRaWANGetServiceProfileInfoTypeDef",
    "GetWirelessDeviceRequestRequestTypeDef",
    "GetWirelessDeviceStatisticsRequestRequestTypeDef",
    "SidewalkDeviceMetadataTypeDef",
    "GetWirelessGatewayCertificateRequestRequestTypeDef",
    "GetWirelessGatewayFirmwareInformationRequestRequestTypeDef",
    "GetWirelessGatewayRequestRequestTypeDef",
    "GetWirelessGatewayStatisticsRequestRequestTypeDef",
    "GetWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    "GetWirelessGatewayTaskRequestRequestTypeDef",
    "LoRaWANJoinEventNotificationConfigurationsTypeDef",
    "LoRaWANJoinResourceTypeEventConfigurationTypeDef",
    "ListDestinationsRequestRequestTypeDef",
    "ListDeviceProfilesRequestRequestTypeDef",
    "ListEventConfigurationsRequestRequestTypeDef",
    "ListFuotaTasksRequestRequestTypeDef",
    "ListMulticastGroupsByFuotaTaskRequestRequestTypeDef",
    "MulticastGroupByFuotaTaskTypeDef",
    "ListMulticastGroupsRequestRequestTypeDef",
    "MulticastGroupTypeDef",
    "ListNetworkAnalyzerConfigurationsRequestRequestTypeDef",
    "NetworkAnalyzerConfigurationsTypeDef",
    "ListPartnerAccountsRequestRequestTypeDef",
    "ListQueuedMessagesRequestRequestTypeDef",
    "ListServiceProfilesRequestRequestTypeDef",
    "ServiceProfileTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWirelessDevicesRequestRequestTypeDef",
    "ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef",
    "ListWirelessGatewaysRequestRequestTypeDef",
    "LoRaWANGatewayMetadataTypeDef",
    "OtaaV1_0_xTypeDef",
    "OtaaV1_1TypeDef",
    "LoRaWANGatewayVersionTypeDef",
    "LoRaWANListDeviceTypeDef",
    "LoRaWANMulticastMetadataTypeDef",
    "LoRaWANStartFuotaTaskTypeDef",
    "UpdateAbpV1_0_xTypeDef",
    "UpdateAbpV1_1TypeDef",
    "PutResourceLogLevelRequestRequestTypeDef",
    "ResetResourceLogLevelRequestRequestTypeDef",
    "SidewalkSendDataToDeviceTypeDef",
    "SidewalkUpdateAccountTypeDef",
    "TestWirelessDeviceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDestinationRequestRequestTypeDef",
    "UpdateWirelessGatewayRequestRequestTypeDef",
    "WirelessDeviceEventLogOptionTypeDef",
    "WirelessGatewayEventLogOptionTypeDef",
    "AbpV1_0_xTypeDef",
    "AbpV1_1TypeDef",
    "AssociateAwsAccountWithPartnerAccountRequestRequestTypeDef",
    "CreateDestinationRequestRequestTypeDef",
    "StartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    "StartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "AssociateAwsAccountWithPartnerAccountResponseTypeDef",
    "AssociateWirelessGatewayWithCertificateResponseTypeDef",
    "CreateDestinationResponseTypeDef",
    "CreateDeviceProfileResponseTypeDef",
    "CreateFuotaTaskResponseTypeDef",
    "CreateMulticastGroupResponseTypeDef",
    "CreateNetworkAnalyzerConfigurationResponseTypeDef",
    "CreateServiceProfileResponseTypeDef",
    "CreateWirelessDeviceResponseTypeDef",
    "CreateWirelessGatewayResponseTypeDef",
    "CreateWirelessGatewayTaskDefinitionResponseTypeDef",
    "CreateWirelessGatewayTaskResponseTypeDef",
    "GetDestinationResponseTypeDef",
    "GetResourceLogLevelResponseTypeDef",
    "GetServiceEndpointResponseTypeDef",
    "GetWirelessGatewayCertificateResponseTypeDef",
    "GetWirelessGatewayStatisticsResponseTypeDef",
    "GetWirelessGatewayTaskResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SendDataToMulticastGroupResponseTypeDef",
    "SendDataToWirelessDeviceResponseTypeDef",
    "TestWirelessDeviceResponseTypeDef",
    "SidewalkDeviceTypeDef",
    "SidewalkListDeviceTypeDef",
    "ConnectionStatusEventConfigurationTypeDef",
    "ConnectionStatusResourceTypeEventConfigurationTypeDef",
    "CreateDeviceProfileRequestRequestTypeDef",
    "GetDeviceProfileResponseTypeDef",
    "CreateFuotaTaskRequestRequestTypeDef",
    "UpdateFuotaTaskRequestRequestTypeDef",
    "CreateMulticastGroupRequestRequestTypeDef",
    "UpdateMulticastGroupRequestRequestTypeDef",
    "CreateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "GetNetworkAnalyzerConfigurationResponseTypeDef",
    "UpdateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "CreateServiceProfileRequestRequestTypeDef",
    "CreateWirelessGatewayRequestRequestTypeDef",
    "GetWirelessGatewayResponseTypeDef",
    "WirelessGatewayStatisticsTypeDef",
    "ListDestinationsResponseTypeDef",
    "ListDeviceProfilesResponseTypeDef",
    "DeviceRegistrationStateEventConfigurationTypeDef",
    "ProximityEventConfigurationTypeDef",
    "DeviceRegistrationStateResourceTypeEventConfigurationTypeDef",
    "ProximityResourceTypeEventConfigurationTypeDef",
    "DownlinkQueueMessageTypeDef",
    "ListFuotaTasksResponseTypeDef",
    "GetFuotaTaskResponseTypeDef",
    "GetMulticastGroupResponseTypeDef",
    "GetMulticastGroupSessionResponseTypeDef",
    "StartMulticastGroupSessionRequestRequestTypeDef",
    "GetPartnerAccountResponseTypeDef",
    "ListPartnerAccountsResponseTypeDef",
    "GetServiceProfileResponseTypeDef",
    "JoinEventConfigurationTypeDef",
    "JoinResourceTypeEventConfigurationTypeDef",
    "ListMulticastGroupsByFuotaTaskResponseTypeDef",
    "ListMulticastGroupsResponseTypeDef",
    "ListNetworkAnalyzerConfigurationsResponseTypeDef",
    "ListServiceProfilesResponseTypeDef",
    "LoRaWANDeviceMetadataTypeDef",
    "LoRaWANGatewayCurrentVersionTypeDef",
    "LoRaWANUpdateGatewayTaskCreateTypeDef",
    "LoRaWANUpdateGatewayTaskEntryTypeDef",
    "MulticastWirelessMetadataTypeDef",
    "StartFuotaTaskRequestRequestTypeDef",
    "LoRaWANUpdateDeviceTypeDef",
    "WirelessMetadataTypeDef",
    "UpdatePartnerAccountRequestRequestTypeDef",
    "WirelessDeviceLogOptionTypeDef",
    "WirelessGatewayLogOptionTypeDef",
    "LoRaWANDeviceTypeDef",
    "WirelessDeviceStatisticsTypeDef",
    "ListWirelessGatewaysResponseTypeDef",
    "ListQueuedMessagesResponseTypeDef",
    "EventNotificationItemConfigurationsTypeDef",
    "GetResourceEventConfigurationResponseTypeDef",
    "UpdateResourceEventConfigurationRequestRequestTypeDef",
    "GetEventConfigurationByResourceTypesResponseTypeDef",
    "UpdateEventConfigurationByResourceTypesRequestRequestTypeDef",
    "GetWirelessDeviceStatisticsResponseTypeDef",
    "GetWirelessGatewayFirmwareInformationResponseTypeDef",
    "UpdateWirelessGatewayTaskCreateTypeDef",
    "UpdateWirelessGatewayTaskEntryTypeDef",
    "SendDataToMulticastGroupRequestRequestTypeDef",
    "UpdateWirelessDeviceRequestRequestTypeDef",
    "SendDataToWirelessDeviceRequestRequestTypeDef",
    "GetLogLevelsByResourceTypesResponseTypeDef",
    "UpdateLogLevelsByResourceTypesRequestRequestTypeDef",
    "CreateWirelessDeviceRequestRequestTypeDef",
    "GetWirelessDeviceResponseTypeDef",
    "ListWirelessDevicesResponseTypeDef",
    "EventConfigurationItemTypeDef",
    "CreateWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    "GetWirelessGatewayTaskDefinitionResponseTypeDef",
    "ListWirelessGatewayTaskDefinitionsResponseTypeDef",
    "ListEventConfigurationsResponseTypeDef",
)

SessionKeysAbpV1_0_xTypeDef = TypedDict(
    "SessionKeysAbpV1_0_xTypeDef",
    {
        "NwkSKey": str,
        "AppSKey": str,
    },
    total=False,
)

SessionKeysAbpV1_1TypeDef = TypedDict(
    "SessionKeysAbpV1_1TypeDef",
    {
        "FNwkSIntKey": str,
        "SNwkSIntKey": str,
        "NwkSEncKey": str,
        "AppSKey": str,
    },
    total=False,
)

SidewalkAccountInfoTypeDef = TypedDict(
    "SidewalkAccountInfoTypeDef",
    {
        "AmazonId": str,
        "AppServerPrivateKey": str,
    },
    total=False,
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

AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef = TypedDict(
    "AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
        "MulticastGroupId": str,
    },
)

AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef = TypedDict(
    "AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
        "WirelessDeviceId": str,
    },
)

AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef = TypedDict(
    "AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
        "WirelessDeviceId": str,
    },
)

AssociateWirelessDeviceWithThingRequestRequestTypeDef = TypedDict(
    "AssociateWirelessDeviceWithThingRequestRequestTypeDef",
    {
        "Id": str,
        "ThingArn": str,
    },
)

AssociateWirelessGatewayWithCertificateRequestRequestTypeDef = TypedDict(
    "AssociateWirelessGatewayWithCertificateRequestRequestTypeDef",
    {
        "Id": str,
        "IotCertificateId": str,
    },
)

AssociateWirelessGatewayWithThingRequestRequestTypeDef = TypedDict(
    "AssociateWirelessGatewayWithThingRequestRequestTypeDef",
    {
        "Id": str,
        "ThingArn": str,
    },
)

CancelMulticastGroupSessionRequestRequestTypeDef = TypedDict(
    "CancelMulticastGroupSessionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

CertificateListTypeDef = TypedDict(
    "CertificateListTypeDef",
    {
        "SigningAlg": SigningAlgType,
        "Value": str,
    },
)

LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef = TypedDict(
    "LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef",
    {
        "GatewayEuiEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef = TypedDict(
    "LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef",
    {
        "WirelessGatewayEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

LoRaWANDeviceProfileTypeDef = TypedDict(
    "LoRaWANDeviceProfileTypeDef",
    {
        "SupportsClassB": bool,
        "ClassBTimeout": int,
        "PingSlotPeriod": int,
        "PingSlotDr": int,
        "PingSlotFreq": int,
        "SupportsClassC": bool,
        "ClassCTimeout": int,
        "MacVersion": str,
        "RegParamsRevision": str,
        "RxDelay1": int,
        "RxDrOffset1": int,
        "RxDataRate2": int,
        "RxFreq2": int,
        "FactoryPresetFreqsList": Sequence[int],
        "MaxEirp": int,
        "MaxDutyCycle": int,
        "RfRegion": str,
        "SupportsJoin": bool,
        "Supports32BitFCnt": bool,
    },
    total=False,
)

LoRaWANFuotaTaskTypeDef = TypedDict(
    "LoRaWANFuotaTaskTypeDef",
    {
        "RfRegion": SupportedRfRegionType,
    },
    total=False,
)

LoRaWANMulticastTypeDef = TypedDict(
    "LoRaWANMulticastTypeDef",
    {
        "RfRegion": SupportedRfRegionType,
        "DlClass": DlClassType,
    },
    total=False,
)

TraceContentTypeDef = TypedDict(
    "TraceContentTypeDef",
    {
        "WirelessDeviceFrameInfo": WirelessDeviceFrameInfoType,
        "LogLevel": LogLevelType,
    },
    total=False,
)

LoRaWANServiceProfileTypeDef = TypedDict(
    "LoRaWANServiceProfileTypeDef",
    {
        "AddGwMetadata": bool,
    },
    total=False,
)

LoRaWANGatewayTypeDef = TypedDict(
    "LoRaWANGatewayTypeDef",
    {
        "GatewayEui": str,
        "RfRegion": str,
        "JoinEuiFilters": Sequence[Sequence[str]],
        "NetIdFilters": Sequence[str],
        "SubBands": Sequence[int],
    },
    total=False,
)

CreateWirelessGatewayTaskRequestRequestTypeDef = TypedDict(
    "CreateWirelessGatewayTaskRequestRequestTypeDef",
    {
        "Id": str,
        "WirelessGatewayTaskDefinitionId": str,
    },
)

DeleteDestinationRequestRequestTypeDef = TypedDict(
    "DeleteDestinationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteDeviceProfileRequestRequestTypeDef = TypedDict(
    "DeleteDeviceProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteFuotaTaskRequestRequestTypeDef = TypedDict(
    "DeleteFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteMulticastGroupRequestRequestTypeDef = TypedDict(
    "DeleteMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef",
    {
        "ConfigurationName": str,
    },
)

_RequiredDeleteQueuedMessagesRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteQueuedMessagesRequestRequestTypeDef",
    {
        "Id": str,
        "MessageId": str,
    },
)
_OptionalDeleteQueuedMessagesRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteQueuedMessagesRequestRequestTypeDef",
    {
        "WirelessDeviceType": WirelessDeviceTypeType,
    },
    total=False,
)


class DeleteQueuedMessagesRequestRequestTypeDef(
    _RequiredDeleteQueuedMessagesRequestRequestTypeDef,
    _OptionalDeleteQueuedMessagesRequestRequestTypeDef,
):
    pass


DeleteServiceProfileRequestRequestTypeDef = TypedDict(
    "DeleteServiceProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteWirelessDeviceRequestRequestTypeDef = TypedDict(
    "DeleteWirelessDeviceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteWirelessGatewayRequestRequestTypeDef = TypedDict(
    "DeleteWirelessGatewayRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeleteWirelessGatewayTaskRequestRequestTypeDef = TypedDict(
    "DeleteWirelessGatewayTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DestinationsTypeDef = TypedDict(
    "DestinationsTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ExpressionType": ExpressionTypeType,
        "Expression": str,
        "Description": str,
        "RoleArn": str,
    },
    total=False,
)

DeviceProfileTypeDef = TypedDict(
    "DeviceProfileTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Id": str,
    },
    total=False,
)

SidewalkEventNotificationConfigurationsTypeDef = TypedDict(
    "SidewalkEventNotificationConfigurationsTypeDef",
    {
        "AmazonIdEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

SidewalkResourceTypeEventConfigurationTypeDef = TypedDict(
    "SidewalkResourceTypeEventConfigurationTypeDef",
    {
        "WirelessDeviceEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef = TypedDict(
    "DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef",
    {
        "PartnerAccountId": str,
        "PartnerType": Literal["Sidewalk"],
    },
)

DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef = TypedDict(
    "DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
        "MulticastGroupId": str,
    },
)

DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef = TypedDict(
    "DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
        "WirelessDeviceId": str,
    },
)

DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef = TypedDict(
    "DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
        "WirelessDeviceId": str,
    },
)

DisassociateWirelessDeviceFromThingRequestRequestTypeDef = TypedDict(
    "DisassociateWirelessDeviceFromThingRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef = TypedDict(
    "DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DisassociateWirelessGatewayFromThingRequestRequestTypeDef = TypedDict(
    "DisassociateWirelessGatewayFromThingRequestRequestTypeDef",
    {
        "Id": str,
    },
)

LoRaWANSendDataToDeviceTypeDef = TypedDict(
    "LoRaWANSendDataToDeviceTypeDef",
    {
        "FPort": int,
    },
    total=False,
)

FPortsTypeDef = TypedDict(
    "FPortsTypeDef",
    {
        "Fuota": int,
        "Multicast": int,
        "ClockSync": int,
    },
    total=False,
)

FuotaTaskTypeDef = TypedDict(
    "FuotaTaskTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

GetDestinationRequestRequestTypeDef = TypedDict(
    "GetDestinationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetDeviceProfileRequestRequestTypeDef = TypedDict(
    "GetDeviceProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetFuotaTaskRequestRequestTypeDef = TypedDict(
    "GetFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)

LoRaWANFuotaTaskGetInfoTypeDef = TypedDict(
    "LoRaWANFuotaTaskGetInfoTypeDef",
    {
        "RfRegion": str,
        "StartTime": datetime,
    },
    total=False,
)

GetMulticastGroupRequestRequestTypeDef = TypedDict(
    "GetMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)

LoRaWANMulticastGetTypeDef = TypedDict(
    "LoRaWANMulticastGetTypeDef",
    {
        "RfRegion": SupportedRfRegionType,
        "DlClass": DlClassType,
        "NumberOfDevicesRequested": int,
        "NumberOfDevicesInGroup": int,
    },
    total=False,
)

GetMulticastGroupSessionRequestRequestTypeDef = TypedDict(
    "GetMulticastGroupSessionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

LoRaWANMulticastSessionTypeDef = TypedDict(
    "LoRaWANMulticastSessionTypeDef",
    {
        "DlDr": int,
        "DlFreq": int,
        "SessionStartTime": datetime,
        "SessionTimeout": int,
    },
    total=False,
)

GetNetworkAnalyzerConfigurationRequestRequestTypeDef = TypedDict(
    "GetNetworkAnalyzerConfigurationRequestRequestTypeDef",
    {
        "ConfigurationName": str,
    },
)

GetPartnerAccountRequestRequestTypeDef = TypedDict(
    "GetPartnerAccountRequestRequestTypeDef",
    {
        "PartnerAccountId": str,
        "PartnerType": Literal["Sidewalk"],
    },
)

SidewalkAccountInfoWithFingerprintTypeDef = TypedDict(
    "SidewalkAccountInfoWithFingerprintTypeDef",
    {
        "AmazonId": str,
        "Fingerprint": str,
        "Arn": str,
    },
    total=False,
)

_RequiredGetResourceEventConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceEventConfigurationRequestRequestTypeDef",
    {
        "Identifier": str,
        "IdentifierType": IdentifierTypeType,
    },
)
_OptionalGetResourceEventConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceEventConfigurationRequestRequestTypeDef",
    {
        "PartnerType": Literal["Sidewalk"],
    },
    total=False,
)


class GetResourceEventConfigurationRequestRequestTypeDef(
    _RequiredGetResourceEventConfigurationRequestRequestTypeDef,
    _OptionalGetResourceEventConfigurationRequestRequestTypeDef,
):
    pass


GetResourceLogLevelRequestRequestTypeDef = TypedDict(
    "GetResourceLogLevelRequestRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "ResourceType": str,
    },
)

GetServiceEndpointRequestRequestTypeDef = TypedDict(
    "GetServiceEndpointRequestRequestTypeDef",
    {
        "ServiceType": WirelessGatewayServiceTypeType,
    },
    total=False,
)

GetServiceProfileRequestRequestTypeDef = TypedDict(
    "GetServiceProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)

LoRaWANGetServiceProfileInfoTypeDef = TypedDict(
    "LoRaWANGetServiceProfileInfoTypeDef",
    {
        "UlRate": int,
        "UlBucketSize": int,
        "UlRatePolicy": str,
        "DlRate": int,
        "DlBucketSize": int,
        "DlRatePolicy": str,
        "AddGwMetadata": bool,
        "DevStatusReqFreq": int,
        "ReportDevStatusBattery": bool,
        "ReportDevStatusMargin": bool,
        "DrMin": int,
        "DrMax": int,
        "ChannelMask": str,
        "PrAllowed": bool,
        "HrAllowed": bool,
        "RaAllowed": bool,
        "NwkGeoLoc": bool,
        "TargetPer": int,
        "MinGwDiversity": int,
    },
    total=False,
)

GetWirelessDeviceRequestRequestTypeDef = TypedDict(
    "GetWirelessDeviceRequestRequestTypeDef",
    {
        "Identifier": str,
        "IdentifierType": WirelessDeviceIdTypeType,
    },
)

GetWirelessDeviceStatisticsRequestRequestTypeDef = TypedDict(
    "GetWirelessDeviceStatisticsRequestRequestTypeDef",
    {
        "WirelessDeviceId": str,
    },
)

SidewalkDeviceMetadataTypeDef = TypedDict(
    "SidewalkDeviceMetadataTypeDef",
    {
        "Rssi": int,
        "BatteryLevel": BatteryLevelType,
        "Event": EventType,
        "DeviceState": DeviceStateType,
    },
    total=False,
)

GetWirelessGatewayCertificateRequestRequestTypeDef = TypedDict(
    "GetWirelessGatewayCertificateRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetWirelessGatewayFirmwareInformationRequestRequestTypeDef = TypedDict(
    "GetWirelessGatewayFirmwareInformationRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetWirelessGatewayRequestRequestTypeDef = TypedDict(
    "GetWirelessGatewayRequestRequestTypeDef",
    {
        "Identifier": str,
        "IdentifierType": WirelessGatewayIdTypeType,
    },
)

GetWirelessGatewayStatisticsRequestRequestTypeDef = TypedDict(
    "GetWirelessGatewayStatisticsRequestRequestTypeDef",
    {
        "WirelessGatewayId": str,
    },
)

GetWirelessGatewayTaskDefinitionRequestRequestTypeDef = TypedDict(
    "GetWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetWirelessGatewayTaskRequestRequestTypeDef = TypedDict(
    "GetWirelessGatewayTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)

LoRaWANJoinEventNotificationConfigurationsTypeDef = TypedDict(
    "LoRaWANJoinEventNotificationConfigurationsTypeDef",
    {
        "DevEuiEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

LoRaWANJoinResourceTypeEventConfigurationTypeDef = TypedDict(
    "LoRaWANJoinResourceTypeEventConfigurationTypeDef",
    {
        "WirelessDeviceEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

ListDestinationsRequestRequestTypeDef = TypedDict(
    "ListDestinationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListDeviceProfilesRequestRequestTypeDef = TypedDict(
    "ListDeviceProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListEventConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListEventConfigurationsRequestRequestTypeDef",
    {
        "ResourceType": EventNotificationResourceTypeType,
    },
)
_OptionalListEventConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListEventConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListEventConfigurationsRequestRequestTypeDef(
    _RequiredListEventConfigurationsRequestRequestTypeDef,
    _OptionalListEventConfigurationsRequestRequestTypeDef,
):
    pass


ListFuotaTasksRequestRequestTypeDef = TypedDict(
    "ListFuotaTasksRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListMulticastGroupsByFuotaTaskRequestRequestTypeDef = TypedDict(
    "_RequiredListMulticastGroupsByFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalListMulticastGroupsByFuotaTaskRequestRequestTypeDef = TypedDict(
    "_OptionalListMulticastGroupsByFuotaTaskRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListMulticastGroupsByFuotaTaskRequestRequestTypeDef(
    _RequiredListMulticastGroupsByFuotaTaskRequestRequestTypeDef,
    _OptionalListMulticastGroupsByFuotaTaskRequestRequestTypeDef,
):
    pass


MulticastGroupByFuotaTaskTypeDef = TypedDict(
    "MulticastGroupByFuotaTaskTypeDef",
    {
        "Id": str,
    },
    total=False,
)

ListMulticastGroupsRequestRequestTypeDef = TypedDict(
    "ListMulticastGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MulticastGroupTypeDef = TypedDict(
    "MulticastGroupTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

ListNetworkAnalyzerConfigurationsRequestRequestTypeDef = TypedDict(
    "ListNetworkAnalyzerConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

NetworkAnalyzerConfigurationsTypeDef = TypedDict(
    "NetworkAnalyzerConfigurationsTypeDef",
    {
        "Arn": str,
        "Name": str,
    },
    total=False,
)

ListPartnerAccountsRequestRequestTypeDef = TypedDict(
    "ListPartnerAccountsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListQueuedMessagesRequestRequestTypeDef = TypedDict(
    "_RequiredListQueuedMessagesRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalListQueuedMessagesRequestRequestTypeDef = TypedDict(
    "_OptionalListQueuedMessagesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "WirelessDeviceType": WirelessDeviceTypeType,
    },
    total=False,
)


class ListQueuedMessagesRequestRequestTypeDef(
    _RequiredListQueuedMessagesRequestRequestTypeDef,
    _OptionalListQueuedMessagesRequestRequestTypeDef,
):
    pass


ListServiceProfilesRequestRequestTypeDef = TypedDict(
    "ListServiceProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ServiceProfileTypeDef = TypedDict(
    "ServiceProfileTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Id": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListWirelessDevicesRequestRequestTypeDef = TypedDict(
    "ListWirelessDevicesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "DestinationName": str,
        "DeviceProfileId": str,
        "ServiceProfileId": str,
        "WirelessDeviceType": WirelessDeviceTypeType,
        "FuotaTaskId": str,
        "MulticastGroupId": str,
    },
    total=False,
)

ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef = TypedDict(
    "ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "TaskDefinitionType": Literal["UPDATE"],
    },
    total=False,
)

ListWirelessGatewaysRequestRequestTypeDef = TypedDict(
    "ListWirelessGatewaysRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

LoRaWANGatewayMetadataTypeDef = TypedDict(
    "LoRaWANGatewayMetadataTypeDef",
    {
        "GatewayEui": str,
        "Snr": float,
        "Rssi": float,
    },
    total=False,
)

OtaaV1_0_xTypeDef = TypedDict(
    "OtaaV1_0_xTypeDef",
    {
        "AppKey": str,
        "AppEui": str,
        "GenAppKey": str,
    },
    total=False,
)

OtaaV1_1TypeDef = TypedDict(
    "OtaaV1_1TypeDef",
    {
        "AppKey": str,
        "NwkKey": str,
        "JoinEui": str,
    },
    total=False,
)

LoRaWANGatewayVersionTypeDef = TypedDict(
    "LoRaWANGatewayVersionTypeDef",
    {
        "PackageVersion": str,
        "Model": str,
        "Station": str,
    },
    total=False,
)

LoRaWANListDeviceTypeDef = TypedDict(
    "LoRaWANListDeviceTypeDef",
    {
        "DevEui": str,
    },
    total=False,
)

LoRaWANMulticastMetadataTypeDef = TypedDict(
    "LoRaWANMulticastMetadataTypeDef",
    {
        "FPort": int,
    },
    total=False,
)

LoRaWANStartFuotaTaskTypeDef = TypedDict(
    "LoRaWANStartFuotaTaskTypeDef",
    {
        "StartTime": Union[datetime, str],
    },
    total=False,
)

UpdateAbpV1_0_xTypeDef = TypedDict(
    "UpdateAbpV1_0_xTypeDef",
    {
        "FCntStart": int,
    },
    total=False,
)

UpdateAbpV1_1TypeDef = TypedDict(
    "UpdateAbpV1_1TypeDef",
    {
        "FCntStart": int,
    },
    total=False,
)

PutResourceLogLevelRequestRequestTypeDef = TypedDict(
    "PutResourceLogLevelRequestRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "ResourceType": str,
        "LogLevel": LogLevelType,
    },
)

ResetResourceLogLevelRequestRequestTypeDef = TypedDict(
    "ResetResourceLogLevelRequestRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "ResourceType": str,
    },
)

SidewalkSendDataToDeviceTypeDef = TypedDict(
    "SidewalkSendDataToDeviceTypeDef",
    {
        "Seq": int,
        "MessageType": MessageTypeType,
    },
    total=False,
)

SidewalkUpdateAccountTypeDef = TypedDict(
    "SidewalkUpdateAccountTypeDef",
    {
        "AppServerPrivateKey": str,
    },
    total=False,
)

TestWirelessDeviceRequestRequestTypeDef = TypedDict(
    "TestWirelessDeviceRequestRequestTypeDef",
    {
        "Id": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDestinationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDestinationRequestRequestTypeDef",
    {
        "ExpressionType": ExpressionTypeType,
        "Expression": str,
        "Description": str,
        "RoleArn": str,
    },
    total=False,
)


class UpdateDestinationRequestRequestTypeDef(
    _RequiredUpdateDestinationRequestRequestTypeDef, _OptionalUpdateDestinationRequestRequestTypeDef
):
    pass


_RequiredUpdateWirelessGatewayRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWirelessGatewayRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateWirelessGatewayRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWirelessGatewayRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "JoinEuiFilters": Sequence[Sequence[str]],
        "NetIdFilters": Sequence[str],
    },
    total=False,
)


class UpdateWirelessGatewayRequestRequestTypeDef(
    _RequiredUpdateWirelessGatewayRequestRequestTypeDef,
    _OptionalUpdateWirelessGatewayRequestRequestTypeDef,
):
    pass


WirelessDeviceEventLogOptionTypeDef = TypedDict(
    "WirelessDeviceEventLogOptionTypeDef",
    {
        "Event": WirelessDeviceEventType,
        "LogLevel": LogLevelType,
    },
)

WirelessGatewayEventLogOptionTypeDef = TypedDict(
    "WirelessGatewayEventLogOptionTypeDef",
    {
        "Event": WirelessGatewayEventType,
        "LogLevel": LogLevelType,
    },
)

AbpV1_0_xTypeDef = TypedDict(
    "AbpV1_0_xTypeDef",
    {
        "DevAddr": str,
        "SessionKeys": SessionKeysAbpV1_0_xTypeDef,
        "FCntStart": int,
    },
    total=False,
)

AbpV1_1TypeDef = TypedDict(
    "AbpV1_1TypeDef",
    {
        "DevAddr": str,
        "SessionKeys": SessionKeysAbpV1_1TypeDef,
        "FCntStart": int,
    },
    total=False,
)

_RequiredAssociateAwsAccountWithPartnerAccountRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateAwsAccountWithPartnerAccountRequestRequestTypeDef",
    {
        "Sidewalk": SidewalkAccountInfoTypeDef,
    },
)
_OptionalAssociateAwsAccountWithPartnerAccountRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateAwsAccountWithPartnerAccountRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class AssociateAwsAccountWithPartnerAccountRequestRequestTypeDef(
    _RequiredAssociateAwsAccountWithPartnerAccountRequestRequestTypeDef,
    _OptionalAssociateAwsAccountWithPartnerAccountRequestRequestTypeDef,
):
    pass


_RequiredCreateDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDestinationRequestRequestTypeDef",
    {
        "Name": str,
        "ExpressionType": ExpressionTypeType,
        "Expression": str,
        "RoleArn": str,
    },
)
_OptionalCreateDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDestinationRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)


class CreateDestinationRequestRequestTypeDef(
    _RequiredCreateDestinationRequestRequestTypeDef, _OptionalCreateDestinationRequestRequestTypeDef
):
    pass


_RequiredStartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef = TypedDict(
    "_RequiredStartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalStartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef = TypedDict(
    "_OptionalStartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    {
        "QueryString": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class StartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef(
    _RequiredStartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef,
    _OptionalStartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef,
):
    pass


_RequiredStartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef = TypedDict(
    "_RequiredStartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalStartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef = TypedDict(
    "_OptionalStartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    {
        "QueryString": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class StartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef(
    _RequiredStartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef,
    _OptionalStartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

AssociateAwsAccountWithPartnerAccountResponseTypeDef = TypedDict(
    "AssociateAwsAccountWithPartnerAccountResponseTypeDef",
    {
        "Sidewalk": SidewalkAccountInfoTypeDef,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateWirelessGatewayWithCertificateResponseTypeDef = TypedDict(
    "AssociateWirelessGatewayWithCertificateResponseTypeDef",
    {
        "IotCertificateId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDestinationResponseTypeDef = TypedDict(
    "CreateDestinationResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeviceProfileResponseTypeDef = TypedDict(
    "CreateDeviceProfileResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFuotaTaskResponseTypeDef = TypedDict(
    "CreateFuotaTaskResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMulticastGroupResponseTypeDef = TypedDict(
    "CreateMulticastGroupResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNetworkAnalyzerConfigurationResponseTypeDef = TypedDict(
    "CreateNetworkAnalyzerConfigurationResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceProfileResponseTypeDef = TypedDict(
    "CreateServiceProfileResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWirelessDeviceResponseTypeDef = TypedDict(
    "CreateWirelessDeviceResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWirelessGatewayResponseTypeDef = TypedDict(
    "CreateWirelessGatewayResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWirelessGatewayTaskDefinitionResponseTypeDef = TypedDict(
    "CreateWirelessGatewayTaskDefinitionResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWirelessGatewayTaskResponseTypeDef = TypedDict(
    "CreateWirelessGatewayTaskResponseTypeDef",
    {
        "WirelessGatewayTaskDefinitionId": str,
        "Status": WirelessGatewayTaskStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDestinationResponseTypeDef = TypedDict(
    "GetDestinationResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Expression": str,
        "ExpressionType": ExpressionTypeType,
        "Description": str,
        "RoleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceLogLevelResponseTypeDef = TypedDict(
    "GetResourceLogLevelResponseTypeDef",
    {
        "LogLevel": LogLevelType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceEndpointResponseTypeDef = TypedDict(
    "GetServiceEndpointResponseTypeDef",
    {
        "ServiceType": WirelessGatewayServiceTypeType,
        "ServiceEndpoint": str,
        "ServerTrust": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWirelessGatewayCertificateResponseTypeDef = TypedDict(
    "GetWirelessGatewayCertificateResponseTypeDef",
    {
        "IotCertificateId": str,
        "LoRaWANNetworkServerCertificateId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWirelessGatewayStatisticsResponseTypeDef = TypedDict(
    "GetWirelessGatewayStatisticsResponseTypeDef",
    {
        "WirelessGatewayId": str,
        "LastUplinkReceivedAt": str,
        "ConnectionStatus": ConnectionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWirelessGatewayTaskResponseTypeDef = TypedDict(
    "GetWirelessGatewayTaskResponseTypeDef",
    {
        "WirelessGatewayId": str,
        "WirelessGatewayTaskDefinitionId": str,
        "LastUplinkReceivedAt": str,
        "TaskCreatedAt": str,
        "Status": WirelessGatewayTaskStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendDataToMulticastGroupResponseTypeDef = TypedDict(
    "SendDataToMulticastGroupResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendDataToWirelessDeviceResponseTypeDef = TypedDict(
    "SendDataToWirelessDeviceResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestWirelessDeviceResponseTypeDef = TypedDict(
    "TestWirelessDeviceResponseTypeDef",
    {
        "Result": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SidewalkDeviceTypeDef = TypedDict(
    "SidewalkDeviceTypeDef",
    {
        "AmazonId": str,
        "SidewalkId": str,
        "SidewalkManufacturingSn": str,
        "DeviceCertificates": List[CertificateListTypeDef],
    },
    total=False,
)

SidewalkListDeviceTypeDef = TypedDict(
    "SidewalkListDeviceTypeDef",
    {
        "AmazonId": str,
        "SidewalkId": str,
        "SidewalkManufacturingSn": str,
        "DeviceCertificates": List[CertificateListTypeDef],
    },
    total=False,
)

ConnectionStatusEventConfigurationTypeDef = TypedDict(
    "ConnectionStatusEventConfigurationTypeDef",
    {
        "LoRaWAN": LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef,
        "WirelessGatewayIdEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

ConnectionStatusResourceTypeEventConfigurationTypeDef = TypedDict(
    "ConnectionStatusResourceTypeEventConfigurationTypeDef",
    {
        "LoRaWAN": LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef,
    },
    total=False,
)

CreateDeviceProfileRequestRequestTypeDef = TypedDict(
    "CreateDeviceProfileRequestRequestTypeDef",
    {
        "Name": str,
        "LoRaWAN": LoRaWANDeviceProfileTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)

GetDeviceProfileResponseTypeDef = TypedDict(
    "GetDeviceProfileResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Id": str,
        "LoRaWAN": LoRaWANDeviceProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateFuotaTaskRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFuotaTaskRequestRequestTypeDef",
    {
        "FirmwareUpdateImage": str,
        "FirmwareUpdateRole": str,
    },
)
_OptionalCreateFuotaTaskRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFuotaTaskRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "ClientRequestToken": str,
        "LoRaWAN": LoRaWANFuotaTaskTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFuotaTaskRequestRequestTypeDef(
    _RequiredCreateFuotaTaskRequestRequestTypeDef, _OptionalCreateFuotaTaskRequestRequestTypeDef
):
    pass


_RequiredUpdateFuotaTaskRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateFuotaTaskRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFuotaTaskRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "LoRaWAN": LoRaWANFuotaTaskTypeDef,
        "FirmwareUpdateImage": str,
        "FirmwareUpdateRole": str,
    },
    total=False,
)


class UpdateFuotaTaskRequestRequestTypeDef(
    _RequiredUpdateFuotaTaskRequestRequestTypeDef, _OptionalUpdateFuotaTaskRequestRequestTypeDef
):
    pass


_RequiredCreateMulticastGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMulticastGroupRequestRequestTypeDef",
    {
        "LoRaWAN": LoRaWANMulticastTypeDef,
    },
)
_OptionalCreateMulticastGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMulticastGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMulticastGroupRequestRequestTypeDef(
    _RequiredCreateMulticastGroupRequestRequestTypeDef,
    _OptionalCreateMulticastGroupRequestRequestTypeDef,
):
    pass


_RequiredUpdateMulticastGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateMulticastGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMulticastGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "LoRaWAN": LoRaWANMulticastTypeDef,
    },
    total=False,
)


class UpdateMulticastGroupRequestRequestTypeDef(
    _RequiredUpdateMulticastGroupRequestRequestTypeDef,
    _OptionalUpdateMulticastGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateNetworkAnalyzerConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateNetworkAnalyzerConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    {
        "TraceContent": TraceContentTypeDef,
        "WirelessDevices": Sequence[str],
        "WirelessGateways": Sequence[str],
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)


class CreateNetworkAnalyzerConfigurationRequestRequestTypeDef(
    _RequiredCreateNetworkAnalyzerConfigurationRequestRequestTypeDef,
    _OptionalCreateNetworkAnalyzerConfigurationRequestRequestTypeDef,
):
    pass


GetNetworkAnalyzerConfigurationResponseTypeDef = TypedDict(
    "GetNetworkAnalyzerConfigurationResponseTypeDef",
    {
        "TraceContent": TraceContentTypeDef,
        "WirelessDevices": List[str],
        "WirelessGateways": List[str],
        "Description": str,
        "Arn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateNetworkAnalyzerConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    {
        "ConfigurationName": str,
    },
)
_OptionalUpdateNetworkAnalyzerConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    {
        "TraceContent": TraceContentTypeDef,
        "WirelessDevicesToAdd": Sequence[str],
        "WirelessDevicesToRemove": Sequence[str],
        "WirelessGatewaysToAdd": Sequence[str],
        "WirelessGatewaysToRemove": Sequence[str],
        "Description": str,
    },
    total=False,
)


class UpdateNetworkAnalyzerConfigurationRequestRequestTypeDef(
    _RequiredUpdateNetworkAnalyzerConfigurationRequestRequestTypeDef,
    _OptionalUpdateNetworkAnalyzerConfigurationRequestRequestTypeDef,
):
    pass


CreateServiceProfileRequestRequestTypeDef = TypedDict(
    "CreateServiceProfileRequestRequestTypeDef",
    {
        "Name": str,
        "LoRaWAN": LoRaWANServiceProfileTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)

_RequiredCreateWirelessGatewayRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWirelessGatewayRequestRequestTypeDef",
    {
        "LoRaWAN": LoRaWANGatewayTypeDef,
    },
)
_OptionalCreateWirelessGatewayRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWirelessGatewayRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)


class CreateWirelessGatewayRequestRequestTypeDef(
    _RequiredCreateWirelessGatewayRequestRequestTypeDef,
    _OptionalCreateWirelessGatewayRequestRequestTypeDef,
):
    pass


GetWirelessGatewayResponseTypeDef = TypedDict(
    "GetWirelessGatewayResponseTypeDef",
    {
        "Name": str,
        "Id": str,
        "Description": str,
        "LoRaWAN": LoRaWANGatewayTypeDef,
        "Arn": str,
        "ThingName": str,
        "ThingArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WirelessGatewayStatisticsTypeDef = TypedDict(
    "WirelessGatewayStatisticsTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "LoRaWAN": LoRaWANGatewayTypeDef,
        "LastUplinkReceivedAt": str,
    },
    total=False,
)

ListDestinationsResponseTypeDef = TypedDict(
    "ListDestinationsResponseTypeDef",
    {
        "NextToken": str,
        "DestinationList": List[DestinationsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeviceProfilesResponseTypeDef = TypedDict(
    "ListDeviceProfilesResponseTypeDef",
    {
        "NextToken": str,
        "DeviceProfileList": List[DeviceProfileTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeviceRegistrationStateEventConfigurationTypeDef = TypedDict(
    "DeviceRegistrationStateEventConfigurationTypeDef",
    {
        "Sidewalk": SidewalkEventNotificationConfigurationsTypeDef,
        "WirelessDeviceIdEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

ProximityEventConfigurationTypeDef = TypedDict(
    "ProximityEventConfigurationTypeDef",
    {
        "Sidewalk": SidewalkEventNotificationConfigurationsTypeDef,
        "WirelessDeviceIdEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

DeviceRegistrationStateResourceTypeEventConfigurationTypeDef = TypedDict(
    "DeviceRegistrationStateResourceTypeEventConfigurationTypeDef",
    {
        "Sidewalk": SidewalkResourceTypeEventConfigurationTypeDef,
    },
    total=False,
)

ProximityResourceTypeEventConfigurationTypeDef = TypedDict(
    "ProximityResourceTypeEventConfigurationTypeDef",
    {
        "Sidewalk": SidewalkResourceTypeEventConfigurationTypeDef,
    },
    total=False,
)

DownlinkQueueMessageTypeDef = TypedDict(
    "DownlinkQueueMessageTypeDef",
    {
        "MessageId": str,
        "TransmitMode": int,
        "ReceivedAt": str,
        "LoRaWAN": LoRaWANSendDataToDeviceTypeDef,
    },
    total=False,
)

ListFuotaTasksResponseTypeDef = TypedDict(
    "ListFuotaTasksResponseTypeDef",
    {
        "NextToken": str,
        "FuotaTaskList": List[FuotaTaskTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFuotaTaskResponseTypeDef = TypedDict(
    "GetFuotaTaskResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Status": FuotaTaskStatusType,
        "Name": str,
        "Description": str,
        "LoRaWAN": LoRaWANFuotaTaskGetInfoTypeDef,
        "FirmwareUpdateImage": str,
        "FirmwareUpdateRole": str,
        "CreatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMulticastGroupResponseTypeDef = TypedDict(
    "GetMulticastGroupResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "Status": str,
        "LoRaWAN": LoRaWANMulticastGetTypeDef,
        "CreatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMulticastGroupSessionResponseTypeDef = TypedDict(
    "GetMulticastGroupSessionResponseTypeDef",
    {
        "LoRaWAN": LoRaWANMulticastSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMulticastGroupSessionRequestRequestTypeDef = TypedDict(
    "StartMulticastGroupSessionRequestRequestTypeDef",
    {
        "Id": str,
        "LoRaWAN": LoRaWANMulticastSessionTypeDef,
    },
)

GetPartnerAccountResponseTypeDef = TypedDict(
    "GetPartnerAccountResponseTypeDef",
    {
        "Sidewalk": SidewalkAccountInfoWithFingerprintTypeDef,
        "AccountLinked": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPartnerAccountsResponseTypeDef = TypedDict(
    "ListPartnerAccountsResponseTypeDef",
    {
        "NextToken": str,
        "Sidewalk": List[SidewalkAccountInfoWithFingerprintTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceProfileResponseTypeDef = TypedDict(
    "GetServiceProfileResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Id": str,
        "LoRaWAN": LoRaWANGetServiceProfileInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JoinEventConfigurationTypeDef = TypedDict(
    "JoinEventConfigurationTypeDef",
    {
        "LoRaWAN": LoRaWANJoinEventNotificationConfigurationsTypeDef,
        "WirelessDeviceIdEventTopic": EventNotificationTopicStatusType,
    },
    total=False,
)

JoinResourceTypeEventConfigurationTypeDef = TypedDict(
    "JoinResourceTypeEventConfigurationTypeDef",
    {
        "LoRaWAN": LoRaWANJoinResourceTypeEventConfigurationTypeDef,
    },
    total=False,
)

ListMulticastGroupsByFuotaTaskResponseTypeDef = TypedDict(
    "ListMulticastGroupsByFuotaTaskResponseTypeDef",
    {
        "NextToken": str,
        "MulticastGroupList": List[MulticastGroupByFuotaTaskTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMulticastGroupsResponseTypeDef = TypedDict(
    "ListMulticastGroupsResponseTypeDef",
    {
        "NextToken": str,
        "MulticastGroupList": List[MulticastGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNetworkAnalyzerConfigurationsResponseTypeDef = TypedDict(
    "ListNetworkAnalyzerConfigurationsResponseTypeDef",
    {
        "NextToken": str,
        "NetworkAnalyzerConfigurationList": List[NetworkAnalyzerConfigurationsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceProfilesResponseTypeDef = TypedDict(
    "ListServiceProfilesResponseTypeDef",
    {
        "NextToken": str,
        "ServiceProfileList": List[ServiceProfileTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoRaWANDeviceMetadataTypeDef = TypedDict(
    "LoRaWANDeviceMetadataTypeDef",
    {
        "DevEui": str,
        "FPort": int,
        "DataRate": int,
        "Frequency": int,
        "Timestamp": str,
        "Gateways": List[LoRaWANGatewayMetadataTypeDef],
    },
    total=False,
)

LoRaWANGatewayCurrentVersionTypeDef = TypedDict(
    "LoRaWANGatewayCurrentVersionTypeDef",
    {
        "CurrentVersion": LoRaWANGatewayVersionTypeDef,
    },
    total=False,
)

LoRaWANUpdateGatewayTaskCreateTypeDef = TypedDict(
    "LoRaWANUpdateGatewayTaskCreateTypeDef",
    {
        "UpdateSignature": str,
        "SigKeyCrc": int,
        "CurrentVersion": LoRaWANGatewayVersionTypeDef,
        "UpdateVersion": LoRaWANGatewayVersionTypeDef,
    },
    total=False,
)

LoRaWANUpdateGatewayTaskEntryTypeDef = TypedDict(
    "LoRaWANUpdateGatewayTaskEntryTypeDef",
    {
        "CurrentVersion": LoRaWANGatewayVersionTypeDef,
        "UpdateVersion": LoRaWANGatewayVersionTypeDef,
    },
    total=False,
)

MulticastWirelessMetadataTypeDef = TypedDict(
    "MulticastWirelessMetadataTypeDef",
    {
        "LoRaWAN": LoRaWANMulticastMetadataTypeDef,
    },
    total=False,
)

_RequiredStartFuotaTaskRequestRequestTypeDef = TypedDict(
    "_RequiredStartFuotaTaskRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalStartFuotaTaskRequestRequestTypeDef = TypedDict(
    "_OptionalStartFuotaTaskRequestRequestTypeDef",
    {
        "LoRaWAN": LoRaWANStartFuotaTaskTypeDef,
    },
    total=False,
)


class StartFuotaTaskRequestRequestTypeDef(
    _RequiredStartFuotaTaskRequestRequestTypeDef, _OptionalStartFuotaTaskRequestRequestTypeDef
):
    pass


LoRaWANUpdateDeviceTypeDef = TypedDict(
    "LoRaWANUpdateDeviceTypeDef",
    {
        "DeviceProfileId": str,
        "ServiceProfileId": str,
        "AbpV1_1": UpdateAbpV1_1TypeDef,
        "AbpV1_0_x": UpdateAbpV1_0_xTypeDef,
    },
    total=False,
)

WirelessMetadataTypeDef = TypedDict(
    "WirelessMetadataTypeDef",
    {
        "LoRaWAN": LoRaWANSendDataToDeviceTypeDef,
        "Sidewalk": SidewalkSendDataToDeviceTypeDef,
    },
    total=False,
)

UpdatePartnerAccountRequestRequestTypeDef = TypedDict(
    "UpdatePartnerAccountRequestRequestTypeDef",
    {
        "Sidewalk": SidewalkUpdateAccountTypeDef,
        "PartnerAccountId": str,
        "PartnerType": Literal["Sidewalk"],
    },
)

_RequiredWirelessDeviceLogOptionTypeDef = TypedDict(
    "_RequiredWirelessDeviceLogOptionTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "LogLevel": LogLevelType,
    },
)
_OptionalWirelessDeviceLogOptionTypeDef = TypedDict(
    "_OptionalWirelessDeviceLogOptionTypeDef",
    {
        "Events": List[WirelessDeviceEventLogOptionTypeDef],
    },
    total=False,
)


class WirelessDeviceLogOptionTypeDef(
    _RequiredWirelessDeviceLogOptionTypeDef, _OptionalWirelessDeviceLogOptionTypeDef
):
    pass


_RequiredWirelessGatewayLogOptionTypeDef = TypedDict(
    "_RequiredWirelessGatewayLogOptionTypeDef",
    {
        "Type": Literal["LoRaWAN"],
        "LogLevel": LogLevelType,
    },
)
_OptionalWirelessGatewayLogOptionTypeDef = TypedDict(
    "_OptionalWirelessGatewayLogOptionTypeDef",
    {
        "Events": List[WirelessGatewayEventLogOptionTypeDef],
    },
    total=False,
)


class WirelessGatewayLogOptionTypeDef(
    _RequiredWirelessGatewayLogOptionTypeDef, _OptionalWirelessGatewayLogOptionTypeDef
):
    pass


LoRaWANDeviceTypeDef = TypedDict(
    "LoRaWANDeviceTypeDef",
    {
        "DevEui": str,
        "DeviceProfileId": str,
        "ServiceProfileId": str,
        "OtaaV1_1": OtaaV1_1TypeDef,
        "OtaaV1_0_x": OtaaV1_0_xTypeDef,
        "AbpV1_1": AbpV1_1TypeDef,
        "AbpV1_0_x": AbpV1_0_xTypeDef,
        "FPorts": FPortsTypeDef,
    },
    total=False,
)

WirelessDeviceStatisticsTypeDef = TypedDict(
    "WirelessDeviceStatisticsTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Type": WirelessDeviceTypeType,
        "Name": str,
        "DestinationName": str,
        "LastUplinkReceivedAt": str,
        "LoRaWAN": LoRaWANListDeviceTypeDef,
        "Sidewalk": SidewalkListDeviceTypeDef,
        "FuotaDeviceStatus": FuotaDeviceStatusType,
        "MulticastDeviceStatus": str,
        "McGroupId": int,
    },
    total=False,
)

ListWirelessGatewaysResponseTypeDef = TypedDict(
    "ListWirelessGatewaysResponseTypeDef",
    {
        "NextToken": str,
        "WirelessGatewayList": List[WirelessGatewayStatisticsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueuedMessagesResponseTypeDef = TypedDict(
    "ListQueuedMessagesResponseTypeDef",
    {
        "NextToken": str,
        "DownlinkQueueMessagesList": List[DownlinkQueueMessageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventNotificationItemConfigurationsTypeDef = TypedDict(
    "EventNotificationItemConfigurationsTypeDef",
    {
        "DeviceRegistrationState": DeviceRegistrationStateEventConfigurationTypeDef,
        "Proximity": ProximityEventConfigurationTypeDef,
        "Join": JoinEventConfigurationTypeDef,
        "ConnectionStatus": ConnectionStatusEventConfigurationTypeDef,
    },
    total=False,
)

GetResourceEventConfigurationResponseTypeDef = TypedDict(
    "GetResourceEventConfigurationResponseTypeDef",
    {
        "DeviceRegistrationState": DeviceRegistrationStateEventConfigurationTypeDef,
        "Proximity": ProximityEventConfigurationTypeDef,
        "Join": JoinEventConfigurationTypeDef,
        "ConnectionStatus": ConnectionStatusEventConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateResourceEventConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResourceEventConfigurationRequestRequestTypeDef",
    {
        "Identifier": str,
        "IdentifierType": IdentifierTypeType,
    },
)
_OptionalUpdateResourceEventConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResourceEventConfigurationRequestRequestTypeDef",
    {
        "PartnerType": Literal["Sidewalk"],
        "DeviceRegistrationState": DeviceRegistrationStateEventConfigurationTypeDef,
        "Proximity": ProximityEventConfigurationTypeDef,
        "Join": JoinEventConfigurationTypeDef,
        "ConnectionStatus": ConnectionStatusEventConfigurationTypeDef,
    },
    total=False,
)


class UpdateResourceEventConfigurationRequestRequestTypeDef(
    _RequiredUpdateResourceEventConfigurationRequestRequestTypeDef,
    _OptionalUpdateResourceEventConfigurationRequestRequestTypeDef,
):
    pass


GetEventConfigurationByResourceTypesResponseTypeDef = TypedDict(
    "GetEventConfigurationByResourceTypesResponseTypeDef",
    {
        "DeviceRegistrationState": DeviceRegistrationStateResourceTypeEventConfigurationTypeDef,
        "Proximity": ProximityResourceTypeEventConfigurationTypeDef,
        "Join": JoinResourceTypeEventConfigurationTypeDef,
        "ConnectionStatus": ConnectionStatusResourceTypeEventConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEventConfigurationByResourceTypesRequestRequestTypeDef = TypedDict(
    "UpdateEventConfigurationByResourceTypesRequestRequestTypeDef",
    {
        "DeviceRegistrationState": DeviceRegistrationStateResourceTypeEventConfigurationTypeDef,
        "Proximity": ProximityResourceTypeEventConfigurationTypeDef,
        "Join": JoinResourceTypeEventConfigurationTypeDef,
        "ConnectionStatus": ConnectionStatusResourceTypeEventConfigurationTypeDef,
    },
    total=False,
)

GetWirelessDeviceStatisticsResponseTypeDef = TypedDict(
    "GetWirelessDeviceStatisticsResponseTypeDef",
    {
        "WirelessDeviceId": str,
        "LastUplinkReceivedAt": str,
        "LoRaWAN": LoRaWANDeviceMetadataTypeDef,
        "Sidewalk": SidewalkDeviceMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWirelessGatewayFirmwareInformationResponseTypeDef = TypedDict(
    "GetWirelessGatewayFirmwareInformationResponseTypeDef",
    {
        "LoRaWAN": LoRaWANGatewayCurrentVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWirelessGatewayTaskCreateTypeDef = TypedDict(
    "UpdateWirelessGatewayTaskCreateTypeDef",
    {
        "UpdateDataSource": str,
        "UpdateDataRole": str,
        "LoRaWAN": LoRaWANUpdateGatewayTaskCreateTypeDef,
    },
    total=False,
)

UpdateWirelessGatewayTaskEntryTypeDef = TypedDict(
    "UpdateWirelessGatewayTaskEntryTypeDef",
    {
        "Id": str,
        "LoRaWAN": LoRaWANUpdateGatewayTaskEntryTypeDef,
        "Arn": str,
    },
    total=False,
)

SendDataToMulticastGroupRequestRequestTypeDef = TypedDict(
    "SendDataToMulticastGroupRequestRequestTypeDef",
    {
        "Id": str,
        "PayloadData": str,
        "WirelessMetadata": MulticastWirelessMetadataTypeDef,
    },
)

_RequiredUpdateWirelessDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWirelessDeviceRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateWirelessDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWirelessDeviceRequestRequestTypeDef",
    {
        "DestinationName": str,
        "Name": str,
        "Description": str,
        "LoRaWAN": LoRaWANUpdateDeviceTypeDef,
    },
    total=False,
)


class UpdateWirelessDeviceRequestRequestTypeDef(
    _RequiredUpdateWirelessDeviceRequestRequestTypeDef,
    _OptionalUpdateWirelessDeviceRequestRequestTypeDef,
):
    pass


_RequiredSendDataToWirelessDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredSendDataToWirelessDeviceRequestRequestTypeDef",
    {
        "Id": str,
        "TransmitMode": int,
        "PayloadData": str,
    },
)
_OptionalSendDataToWirelessDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalSendDataToWirelessDeviceRequestRequestTypeDef",
    {
        "WirelessMetadata": WirelessMetadataTypeDef,
    },
    total=False,
)


class SendDataToWirelessDeviceRequestRequestTypeDef(
    _RequiredSendDataToWirelessDeviceRequestRequestTypeDef,
    _OptionalSendDataToWirelessDeviceRequestRequestTypeDef,
):
    pass


GetLogLevelsByResourceTypesResponseTypeDef = TypedDict(
    "GetLogLevelsByResourceTypesResponseTypeDef",
    {
        "DefaultLogLevel": LogLevelType,
        "WirelessGatewayLogOptions": List[WirelessGatewayLogOptionTypeDef],
        "WirelessDeviceLogOptions": List[WirelessDeviceLogOptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLogLevelsByResourceTypesRequestRequestTypeDef = TypedDict(
    "UpdateLogLevelsByResourceTypesRequestRequestTypeDef",
    {
        "DefaultLogLevel": LogLevelType,
        "WirelessDeviceLogOptions": Sequence[WirelessDeviceLogOptionTypeDef],
        "WirelessGatewayLogOptions": Sequence[WirelessGatewayLogOptionTypeDef],
    },
    total=False,
)

_RequiredCreateWirelessDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWirelessDeviceRequestRequestTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "DestinationName": str,
    },
)
_OptionalCreateWirelessDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWirelessDeviceRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "ClientRequestToken": str,
        "LoRaWAN": LoRaWANDeviceTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWirelessDeviceRequestRequestTypeDef(
    _RequiredCreateWirelessDeviceRequestRequestTypeDef,
    _OptionalCreateWirelessDeviceRequestRequestTypeDef,
):
    pass


GetWirelessDeviceResponseTypeDef = TypedDict(
    "GetWirelessDeviceResponseTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "Name": str,
        "Description": str,
        "DestinationName": str,
        "Id": str,
        "Arn": str,
        "ThingName": str,
        "ThingArn": str,
        "LoRaWAN": LoRaWANDeviceTypeDef,
        "Sidewalk": SidewalkDeviceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWirelessDevicesResponseTypeDef = TypedDict(
    "ListWirelessDevicesResponseTypeDef",
    {
        "NextToken": str,
        "WirelessDeviceList": List[WirelessDeviceStatisticsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventConfigurationItemTypeDef = TypedDict(
    "EventConfigurationItemTypeDef",
    {
        "Identifier": str,
        "IdentifierType": IdentifierTypeType,
        "PartnerType": Literal["Sidewalk"],
        "Events": EventNotificationItemConfigurationsTypeDef,
    },
    total=False,
)

_RequiredCreateWirelessGatewayTaskDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    {
        "AutoCreateTasks": bool,
    },
)
_OptionalCreateWirelessGatewayTaskDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    {
        "Name": str,
        "Update": UpdateWirelessGatewayTaskCreateTypeDef,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWirelessGatewayTaskDefinitionRequestRequestTypeDef(
    _RequiredCreateWirelessGatewayTaskDefinitionRequestRequestTypeDef,
    _OptionalCreateWirelessGatewayTaskDefinitionRequestRequestTypeDef,
):
    pass


GetWirelessGatewayTaskDefinitionResponseTypeDef = TypedDict(
    "GetWirelessGatewayTaskDefinitionResponseTypeDef",
    {
        "AutoCreateTasks": bool,
        "Name": str,
        "Update": UpdateWirelessGatewayTaskCreateTypeDef,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWirelessGatewayTaskDefinitionsResponseTypeDef = TypedDict(
    "ListWirelessGatewayTaskDefinitionsResponseTypeDef",
    {
        "NextToken": str,
        "TaskDefinitions": List[UpdateWirelessGatewayTaskEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEventConfigurationsResponseTypeDef = TypedDict(
    "ListEventConfigurationsResponseTypeDef",
    {
        "NextToken": str,
        "EventConfigurationsList": List[EventConfigurationItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
