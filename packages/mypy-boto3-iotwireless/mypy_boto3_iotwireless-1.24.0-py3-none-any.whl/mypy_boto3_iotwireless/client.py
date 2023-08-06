"""
Type annotations for iotwireless service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotwireless.client import IoTWirelessClient

    session = Session()
    client: IoTWirelessClient = session.client("iotwireless")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    EventNotificationResourceTypeType,
    ExpressionTypeType,
    IdentifierTypeType,
    LogLevelType,
    WirelessDeviceIdTypeType,
    WirelessDeviceTypeType,
    WirelessGatewayIdTypeType,
    WirelessGatewayServiceTypeType,
)
from .type_defs import (
    AssociateAwsAccountWithPartnerAccountResponseTypeDef,
    AssociateWirelessGatewayWithCertificateResponseTypeDef,
    ConnectionStatusEventConfigurationTypeDef,
    ConnectionStatusResourceTypeEventConfigurationTypeDef,
    CreateDestinationResponseTypeDef,
    CreateDeviceProfileResponseTypeDef,
    CreateFuotaTaskResponseTypeDef,
    CreateMulticastGroupResponseTypeDef,
    CreateNetworkAnalyzerConfigurationResponseTypeDef,
    CreateServiceProfileResponseTypeDef,
    CreateWirelessDeviceResponseTypeDef,
    CreateWirelessGatewayResponseTypeDef,
    CreateWirelessGatewayTaskDefinitionResponseTypeDef,
    CreateWirelessGatewayTaskResponseTypeDef,
    DeviceRegistrationStateEventConfigurationTypeDef,
    DeviceRegistrationStateResourceTypeEventConfigurationTypeDef,
    GetDestinationResponseTypeDef,
    GetDeviceProfileResponseTypeDef,
    GetEventConfigurationByResourceTypesResponseTypeDef,
    GetFuotaTaskResponseTypeDef,
    GetLogLevelsByResourceTypesResponseTypeDef,
    GetMulticastGroupResponseTypeDef,
    GetMulticastGroupSessionResponseTypeDef,
    GetNetworkAnalyzerConfigurationResponseTypeDef,
    GetPartnerAccountResponseTypeDef,
    GetResourceEventConfigurationResponseTypeDef,
    GetResourceLogLevelResponseTypeDef,
    GetServiceEndpointResponseTypeDef,
    GetServiceProfileResponseTypeDef,
    GetWirelessDeviceResponseTypeDef,
    GetWirelessDeviceStatisticsResponseTypeDef,
    GetWirelessGatewayCertificateResponseTypeDef,
    GetWirelessGatewayFirmwareInformationResponseTypeDef,
    GetWirelessGatewayResponseTypeDef,
    GetWirelessGatewayStatisticsResponseTypeDef,
    GetWirelessGatewayTaskDefinitionResponseTypeDef,
    GetWirelessGatewayTaskResponseTypeDef,
    JoinEventConfigurationTypeDef,
    JoinResourceTypeEventConfigurationTypeDef,
    ListDestinationsResponseTypeDef,
    ListDeviceProfilesResponseTypeDef,
    ListEventConfigurationsResponseTypeDef,
    ListFuotaTasksResponseTypeDef,
    ListMulticastGroupsByFuotaTaskResponseTypeDef,
    ListMulticastGroupsResponseTypeDef,
    ListNetworkAnalyzerConfigurationsResponseTypeDef,
    ListPartnerAccountsResponseTypeDef,
    ListQueuedMessagesResponseTypeDef,
    ListServiceProfilesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWirelessDevicesResponseTypeDef,
    ListWirelessGatewaysResponseTypeDef,
    ListWirelessGatewayTaskDefinitionsResponseTypeDef,
    LoRaWANDeviceProfileTypeDef,
    LoRaWANDeviceTypeDef,
    LoRaWANFuotaTaskTypeDef,
    LoRaWANGatewayTypeDef,
    LoRaWANMulticastSessionTypeDef,
    LoRaWANMulticastTypeDef,
    LoRaWANServiceProfileTypeDef,
    LoRaWANStartFuotaTaskTypeDef,
    LoRaWANUpdateDeviceTypeDef,
    MulticastWirelessMetadataTypeDef,
    ProximityEventConfigurationTypeDef,
    ProximityResourceTypeEventConfigurationTypeDef,
    SendDataToMulticastGroupResponseTypeDef,
    SendDataToWirelessDeviceResponseTypeDef,
    SidewalkAccountInfoTypeDef,
    SidewalkUpdateAccountTypeDef,
    TagTypeDef,
    TestWirelessDeviceResponseTypeDef,
    TraceContentTypeDef,
    UpdateWirelessGatewayTaskCreateTypeDef,
    WirelessDeviceLogOptionTypeDef,
    WirelessGatewayLogOptionTypeDef,
    WirelessMetadataTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTWirelessClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IoTWirelessClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTWirelessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#exceptions)
        """

    def associate_aws_account_with_partner_account(
        self,
        *,
        Sidewalk: SidewalkAccountInfoTypeDef,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> AssociateAwsAccountWithPartnerAccountResponseTypeDef:
        """
        Associates a partner account with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_aws_account_with_partner_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_aws_account_with_partner_account)
        """

    def associate_multicast_group_with_fuota_task(
        self, *, Id: str, MulticastGroupId: str
    ) -> Dict[str, Any]:
        """
        Associate a multicast group with a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_multicast_group_with_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_multicast_group_with_fuota_task)
        """

    def associate_wireless_device_with_fuota_task(
        self, *, Id: str, WirelessDeviceId: str
    ) -> Dict[str, Any]:
        """
        Associate a wireless device with a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_wireless_device_with_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_wireless_device_with_fuota_task)
        """

    def associate_wireless_device_with_multicast_group(
        self, *, Id: str, WirelessDeviceId: str
    ) -> Dict[str, Any]:
        """
        Associates a wireless device with a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_wireless_device_with_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_wireless_device_with_multicast_group)
        """

    def associate_wireless_device_with_thing(self, *, Id: str, ThingArn: str) -> Dict[str, Any]:
        """
        Associates a wireless device with a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_wireless_device_with_thing)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_wireless_device_with_thing)
        """

    def associate_wireless_gateway_with_certificate(
        self, *, Id: str, IotCertificateId: str
    ) -> AssociateWirelessGatewayWithCertificateResponseTypeDef:
        """
        Associates a wireless gateway with a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_wireless_gateway_with_certificate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_wireless_gateway_with_certificate)
        """

    def associate_wireless_gateway_with_thing(self, *, Id: str, ThingArn: str) -> Dict[str, Any]:
        """
        Associates a wireless gateway with a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.associate_wireless_gateway_with_thing)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#associate_wireless_gateway_with_thing)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#can_paginate)
        """

    def cancel_multicast_group_session(self, *, Id: str) -> Dict[str, Any]:
        """
        Cancels an existing multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.cancel_multicast_group_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#cancel_multicast_group_session)
        """

    def create_destination(
        self,
        *,
        Name: str,
        ExpressionType: ExpressionTypeType,
        Expression: str,
        RoleArn: str,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateDestinationResponseTypeDef:
        """
        Creates a new destination that maps a device message to an AWS IoT rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_destination)
        """

    def create_device_profile(
        self,
        *,
        Name: str = ...,
        LoRaWAN: LoRaWANDeviceProfileTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateDeviceProfileResponseTypeDef:
        """
        Creates a new device profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_device_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_device_profile)
        """

    def create_fuota_task(
        self,
        *,
        FirmwareUpdateImage: str,
        FirmwareUpdateRole: str,
        Name: str = ...,
        Description: str = ...,
        ClientRequestToken: str = ...,
        LoRaWAN: LoRaWANFuotaTaskTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateFuotaTaskResponseTypeDef:
        """
        Creates a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_fuota_task)
        """

    def create_multicast_group(
        self,
        *,
        LoRaWAN: LoRaWANMulticastTypeDef,
        Name: str = ...,
        Description: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateMulticastGroupResponseTypeDef:
        """
        Creates a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_multicast_group)
        """

    def create_network_analyzer_configuration(
        self,
        *,
        Name: str,
        TraceContent: TraceContentTypeDef = ...,
        WirelessDevices: Sequence[str] = ...,
        WirelessGateways: Sequence[str] = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateNetworkAnalyzerConfigurationResponseTypeDef:
        """
        Creates a new network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_network_analyzer_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_network_analyzer_configuration)
        """

    def create_service_profile(
        self,
        *,
        Name: str = ...,
        LoRaWAN: LoRaWANServiceProfileTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateServiceProfileResponseTypeDef:
        """
        Creates a new service profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_service_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_service_profile)
        """

    def create_wireless_device(
        self,
        *,
        Type: WirelessDeviceTypeType,
        DestinationName: str,
        Name: str = ...,
        Description: str = ...,
        ClientRequestToken: str = ...,
        LoRaWAN: LoRaWANDeviceTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateWirelessDeviceResponseTypeDef:
        """
        Provisions a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_wireless_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_wireless_device)
        """

    def create_wireless_gateway(
        self,
        *,
        LoRaWAN: LoRaWANGatewayTypeDef,
        Name: str = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateWirelessGatewayResponseTypeDef:
        """
        Provisions a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_wireless_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_wireless_gateway)
        """

    def create_wireless_gateway_task(
        self, *, Id: str, WirelessGatewayTaskDefinitionId: str
    ) -> CreateWirelessGatewayTaskResponseTypeDef:
        """
        Creates a task for a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_wireless_gateway_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_wireless_gateway_task)
        """

    def create_wireless_gateway_task_definition(
        self,
        *,
        AutoCreateTasks: bool,
        Name: str = ...,
        Update: UpdateWirelessGatewayTaskCreateTypeDef = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateWirelessGatewayTaskDefinitionResponseTypeDef:
        """
        Creates a gateway task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.create_wireless_gateway_task_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#create_wireless_gateway_task_definition)
        """

    def delete_destination(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_destination)
        """

    def delete_device_profile(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a device profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_device_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_device_profile)
        """

    def delete_fuota_task(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_fuota_task)
        """

    def delete_multicast_group(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a multicast group if it is not in use by a fuota task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_multicast_group)
        """

    def delete_network_analyzer_configuration(self, *, ConfigurationName: str) -> Dict[str, Any]:
        """
        Deletes a network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_network_analyzer_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_network_analyzer_configuration)
        """

    def delete_queued_messages(
        self, *, Id: str, MessageId: str, WirelessDeviceType: WirelessDeviceTypeType = ...
    ) -> Dict[str, Any]:
        """
        Remove queued messages from the downlink queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_queued_messages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_queued_messages)
        """

    def delete_service_profile(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a service profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_service_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_service_profile)
        """

    def delete_wireless_device(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_wireless_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_wireless_device)
        """

    def delete_wireless_gateway(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_wireless_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_wireless_gateway)
        """

    def delete_wireless_gateway_task(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a wireless gateway task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_wireless_gateway_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_wireless_gateway_task)
        """

    def delete_wireless_gateway_task_definition(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a wireless gateway task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.delete_wireless_gateway_task_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#delete_wireless_gateway_task_definition)
        """

    def disassociate_aws_account_from_partner_account(
        self, *, PartnerAccountId: str, PartnerType: Literal["Sidewalk"]
    ) -> Dict[str, Any]:
        """
        Disassociates your AWS account from a partner account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_aws_account_from_partner_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_aws_account_from_partner_account)
        """

    def disassociate_multicast_group_from_fuota_task(
        self, *, Id: str, MulticastGroupId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a multicast group from a fuota task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_multicast_group_from_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_multicast_group_from_fuota_task)
        """

    def disassociate_wireless_device_from_fuota_task(
        self, *, Id: str, WirelessDeviceId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless device from a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_wireless_device_from_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_wireless_device_from_fuota_task)
        """

    def disassociate_wireless_device_from_multicast_group(
        self, *, Id: str, WirelessDeviceId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless device from a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_wireless_device_from_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_wireless_device_from_multicast_group)
        """

    def disassociate_wireless_device_from_thing(self, *, Id: str) -> Dict[str, Any]:
        """
        Disassociates a wireless device from its currently associated thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_wireless_device_from_thing)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_wireless_device_from_thing)
        """

    def disassociate_wireless_gateway_from_certificate(self, *, Id: str) -> Dict[str, Any]:
        """
        Disassociates a wireless gateway from its currently associated certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_wireless_gateway_from_certificate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_wireless_gateway_from_certificate)
        """

    def disassociate_wireless_gateway_from_thing(self, *, Id: str) -> Dict[str, Any]:
        """
        Disassociates a wireless gateway from its currently associated thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.disassociate_wireless_gateway_from_thing)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#disassociate_wireless_gateway_from_thing)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#generate_presigned_url)
        """

    def get_destination(self, *, Name: str) -> GetDestinationResponseTypeDef:
        """
        Gets information about a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_destination)
        """

    def get_device_profile(self, *, Id: str) -> GetDeviceProfileResponseTypeDef:
        """
        Gets information about a device profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_device_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_device_profile)
        """

    def get_event_configuration_by_resource_types(
        self,
    ) -> GetEventConfigurationByResourceTypesResponseTypeDef:
        """
        Get the event configuration by resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_event_configuration_by_resource_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_event_configuration_by_resource_types)
        """

    def get_fuota_task(self, *, Id: str) -> GetFuotaTaskResponseTypeDef:
        """
        Gets information about a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_fuota_task)
        """

    def get_log_levels_by_resource_types(self) -> GetLogLevelsByResourceTypesResponseTypeDef:
        """
        Returns current default log levels or log levels by resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_log_levels_by_resource_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_log_levels_by_resource_types)
        """

    def get_multicast_group(self, *, Id: str) -> GetMulticastGroupResponseTypeDef:
        """
        Gets information about a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_multicast_group)
        """

    def get_multicast_group_session(self, *, Id: str) -> GetMulticastGroupSessionResponseTypeDef:
        """
        Gets information about a multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_multicast_group_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_multicast_group_session)
        """

    def get_network_analyzer_configuration(
        self, *, ConfigurationName: str
    ) -> GetNetworkAnalyzerConfigurationResponseTypeDef:
        """
        Get network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_network_analyzer_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_network_analyzer_configuration)
        """

    def get_partner_account(
        self, *, PartnerAccountId: str, PartnerType: Literal["Sidewalk"]
    ) -> GetPartnerAccountResponseTypeDef:
        """
        Gets information about a partner account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_partner_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_partner_account)
        """

    def get_resource_event_configuration(
        self,
        *,
        Identifier: str,
        IdentifierType: IdentifierTypeType,
        PartnerType: Literal["Sidewalk"] = ...
    ) -> GetResourceEventConfigurationResponseTypeDef:
        """
        Get the event configuration for a particular resource identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_resource_event_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_resource_event_configuration)
        """

    def get_resource_log_level(
        self, *, ResourceIdentifier: str, ResourceType: str
    ) -> GetResourceLogLevelResponseTypeDef:
        """
        Fetches the log-level override, if any, for a given resource-ID and resource-
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_resource_log_level)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_resource_log_level)
        """

    def get_service_endpoint(
        self, *, ServiceType: WirelessGatewayServiceTypeType = ...
    ) -> GetServiceEndpointResponseTypeDef:
        """
        Gets the account-specific endpoint for Configuration and Update Server (CUPS)
        protocol or LoRaWAN Network Server (LNS) connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_service_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_service_endpoint)
        """

    def get_service_profile(self, *, Id: str) -> GetServiceProfileResponseTypeDef:
        """
        Gets information about a service profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_service_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_service_profile)
        """

    def get_wireless_device(
        self, *, Identifier: str, IdentifierType: WirelessDeviceIdTypeType
    ) -> GetWirelessDeviceResponseTypeDef:
        """
        Gets information about a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_device)
        """

    def get_wireless_device_statistics(
        self, *, WirelessDeviceId: str
    ) -> GetWirelessDeviceStatisticsResponseTypeDef:
        """
        Gets operating information about a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_device_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_device_statistics)
        """

    def get_wireless_gateway(
        self, *, Identifier: str, IdentifierType: WirelessGatewayIdTypeType
    ) -> GetWirelessGatewayResponseTypeDef:
        """
        Gets information about a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_gateway)
        """

    def get_wireless_gateway_certificate(
        self, *, Id: str
    ) -> GetWirelessGatewayCertificateResponseTypeDef:
        """
        Gets the ID of the certificate that is currently associated with a wireless
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_gateway_certificate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_gateway_certificate)
        """

    def get_wireless_gateway_firmware_information(
        self, *, Id: str
    ) -> GetWirelessGatewayFirmwareInformationResponseTypeDef:
        """
        Gets the firmware version and other information about a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_gateway_firmware_information)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_gateway_firmware_information)
        """

    def get_wireless_gateway_statistics(
        self, *, WirelessGatewayId: str
    ) -> GetWirelessGatewayStatisticsResponseTypeDef:
        """
        Gets operating information about a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_gateway_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_gateway_statistics)
        """

    def get_wireless_gateway_task(self, *, Id: str) -> GetWirelessGatewayTaskResponseTypeDef:
        """
        Gets information about a wireless gateway task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_gateway_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_gateway_task)
        """

    def get_wireless_gateway_task_definition(
        self, *, Id: str
    ) -> GetWirelessGatewayTaskDefinitionResponseTypeDef:
        """
        Gets information about a wireless gateway task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.get_wireless_gateway_task_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#get_wireless_gateway_task_definition)
        """

    def list_destinations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDestinationsResponseTypeDef:
        """
        Lists the destinations registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_destinations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_destinations)
        """

    def list_device_profiles(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDeviceProfilesResponseTypeDef:
        """
        Lists the device profiles registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_device_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_device_profiles)
        """

    def list_event_configurations(
        self,
        *,
        ResourceType: EventNotificationResourceTypeType,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListEventConfigurationsResponseTypeDef:
        """
        List event configurations where at least one event topic has been enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_event_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_event_configurations)
        """

    def list_fuota_tasks(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFuotaTasksResponseTypeDef:
        """
        Lists the FUOTA tasks registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_fuota_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_fuota_tasks)
        """

    def list_multicast_groups(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMulticastGroupsResponseTypeDef:
        """
        Lists the multicast groups registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_multicast_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_multicast_groups)
        """

    def list_multicast_groups_by_fuota_task(
        self, *, Id: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMulticastGroupsByFuotaTaskResponseTypeDef:
        """
        List all multicast groups associated with a fuota task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_multicast_groups_by_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_multicast_groups_by_fuota_task)
        """

    def list_network_analyzer_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListNetworkAnalyzerConfigurationsResponseTypeDef:
        """
        Lists the network analyzer configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_network_analyzer_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_network_analyzer_configurations)
        """

    def list_partner_accounts(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPartnerAccountsResponseTypeDef:
        """
        Lists the partner accounts associated with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_partner_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_partner_accounts)
        """

    def list_queued_messages(
        self,
        *,
        Id: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        WirelessDeviceType: WirelessDeviceTypeType = ...
    ) -> ListQueuedMessagesResponseTypeDef:
        """
        List queued messages in the downlink queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_queued_messages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_queued_messages)
        """

    def list_service_profiles(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListServiceProfilesResponseTypeDef:
        """
        Lists the service profiles registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_service_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_service_profiles)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_tags_for_resource)
        """

    def list_wireless_devices(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        DestinationName: str = ...,
        DeviceProfileId: str = ...,
        ServiceProfileId: str = ...,
        WirelessDeviceType: WirelessDeviceTypeType = ...,
        FuotaTaskId: str = ...,
        MulticastGroupId: str = ...
    ) -> ListWirelessDevicesResponseTypeDef:
        """
        Lists the wireless devices registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_wireless_devices)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_wireless_devices)
        """

    def list_wireless_gateway_task_definitions(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        TaskDefinitionType: Literal["UPDATE"] = ...
    ) -> ListWirelessGatewayTaskDefinitionsResponseTypeDef:
        """
        List the wireless gateway tasks definitions registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_wireless_gateway_task_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_wireless_gateway_task_definitions)
        """

    def list_wireless_gateways(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWirelessGatewaysResponseTypeDef:
        """
        Lists the wireless gateways registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.list_wireless_gateways)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#list_wireless_gateways)
        """

    def put_resource_log_level(
        self, *, ResourceIdentifier: str, ResourceType: str, LogLevel: LogLevelType
    ) -> Dict[str, Any]:
        """
        Sets the log-level override for a resource-ID and resource-type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.put_resource_log_level)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#put_resource_log_level)
        """

    def reset_all_resource_log_levels(self) -> Dict[str, Any]:
        """
        Removes the log-level overrides for all resources; both wireless devices and
        wireless gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.reset_all_resource_log_levels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#reset_all_resource_log_levels)
        """

    def reset_resource_log_level(
        self, *, ResourceIdentifier: str, ResourceType: str
    ) -> Dict[str, Any]:
        """
        Removes the log-level override, if any, for a specific resource-ID and resource-
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.reset_resource_log_level)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#reset_resource_log_level)
        """

    def send_data_to_multicast_group(
        self, *, Id: str, PayloadData: str, WirelessMetadata: MulticastWirelessMetadataTypeDef
    ) -> SendDataToMulticastGroupResponseTypeDef:
        """
        Sends the specified data to a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.send_data_to_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#send_data_to_multicast_group)
        """

    def send_data_to_wireless_device(
        self,
        *,
        Id: str,
        TransmitMode: int,
        PayloadData: str,
        WirelessMetadata: WirelessMetadataTypeDef = ...
    ) -> SendDataToWirelessDeviceResponseTypeDef:
        """
        Sends a decrypted application data frame to a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.send_data_to_wireless_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#send_data_to_wireless_device)
        """

    def start_bulk_associate_wireless_device_with_multicast_group(
        self, *, Id: str, QueryString: str = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Starts a bulk association of all qualifying wireless devices with a multicast
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.start_bulk_associate_wireless_device_with_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#start_bulk_associate_wireless_device_with_multicast_group)
        """

    def start_bulk_disassociate_wireless_device_from_multicast_group(
        self, *, Id: str, QueryString: str = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Starts a bulk disassociatin of all qualifying wireless devices from a multicast
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.start_bulk_disassociate_wireless_device_from_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#start_bulk_disassociate_wireless_device_from_multicast_group)
        """

    def start_fuota_task(
        self, *, Id: str, LoRaWAN: LoRaWANStartFuotaTaskTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Starts a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.start_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#start_fuota_task)
        """

    def start_multicast_group_session(
        self, *, Id: str, LoRaWAN: LoRaWANMulticastSessionTypeDef
    ) -> Dict[str, Any]:
        """
        Starts a multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.start_multicast_group_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#start_multicast_group_session)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#tag_resource)
        """

    def test_wireless_device(self, *, Id: str) -> TestWirelessDeviceResponseTypeDef:
        """
        Simulates a provisioned device by sending an uplink data payload of `Hello` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.test_wireless_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#test_wireless_device)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#untag_resource)
        """

    def update_destination(
        self,
        *,
        Name: str,
        ExpressionType: ExpressionTypeType = ...,
        Expression: str = ...,
        Description: str = ...,
        RoleArn: str = ...
    ) -> Dict[str, Any]:
        """
        Updates properties of a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_destination)
        """

    def update_event_configuration_by_resource_types(
        self,
        *,
        DeviceRegistrationState: DeviceRegistrationStateResourceTypeEventConfigurationTypeDef = ...,
        Proximity: ProximityResourceTypeEventConfigurationTypeDef = ...,
        Join: JoinResourceTypeEventConfigurationTypeDef = ...,
        ConnectionStatus: ConnectionStatusResourceTypeEventConfigurationTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Update the event configuration by resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_event_configuration_by_resource_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_event_configuration_by_resource_types)
        """

    def update_fuota_task(
        self,
        *,
        Id: str,
        Name: str = ...,
        Description: str = ...,
        LoRaWAN: LoRaWANFuotaTaskTypeDef = ...,
        FirmwareUpdateImage: str = ...,
        FirmwareUpdateRole: str = ...
    ) -> Dict[str, Any]:
        """
        Updates properties of a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_fuota_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_fuota_task)
        """

    def update_log_levels_by_resource_types(
        self,
        *,
        DefaultLogLevel: LogLevelType = ...,
        WirelessDeviceLogOptions: Sequence[WirelessDeviceLogOptionTypeDef] = ...,
        WirelessGatewayLogOptions: Sequence[WirelessGatewayLogOptionTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Set default log level, or log levels by resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_log_levels_by_resource_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_log_levels_by_resource_types)
        """

    def update_multicast_group(
        self,
        *,
        Id: str,
        Name: str = ...,
        Description: str = ...,
        LoRaWAN: LoRaWANMulticastTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Updates properties of a multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_multicast_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_multicast_group)
        """

    def update_network_analyzer_configuration(
        self,
        *,
        ConfigurationName: str,
        TraceContent: TraceContentTypeDef = ...,
        WirelessDevicesToAdd: Sequence[str] = ...,
        WirelessDevicesToRemove: Sequence[str] = ...,
        WirelessGatewaysToAdd: Sequence[str] = ...,
        WirelessGatewaysToRemove: Sequence[str] = ...,
        Description: str = ...
    ) -> Dict[str, Any]:
        """
        Update network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_network_analyzer_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_network_analyzer_configuration)
        """

    def update_partner_account(
        self,
        *,
        Sidewalk: SidewalkUpdateAccountTypeDef,
        PartnerAccountId: str,
        PartnerType: Literal["Sidewalk"]
    ) -> Dict[str, Any]:
        """
        Updates properties of a partner account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_partner_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_partner_account)
        """

    def update_resource_event_configuration(
        self,
        *,
        Identifier: str,
        IdentifierType: IdentifierTypeType,
        PartnerType: Literal["Sidewalk"] = ...,
        DeviceRegistrationState: DeviceRegistrationStateEventConfigurationTypeDef = ...,
        Proximity: ProximityEventConfigurationTypeDef = ...,
        Join: JoinEventConfigurationTypeDef = ...,
        ConnectionStatus: ConnectionStatusEventConfigurationTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Update the event configuration for a particular resource identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_resource_event_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_resource_event_configuration)
        """

    def update_wireless_device(
        self,
        *,
        Id: str,
        DestinationName: str = ...,
        Name: str = ...,
        Description: str = ...,
        LoRaWAN: LoRaWANUpdateDeviceTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Updates properties of a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_wireless_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_wireless_device)
        """

    def update_wireless_gateway(
        self,
        *,
        Id: str,
        Name: str = ...,
        Description: str = ...,
        JoinEuiFilters: Sequence[Sequence[str]] = ...,
        NetIdFilters: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Updates properties of a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client.update_wireless_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/client/#update_wireless_gateway)
        """
