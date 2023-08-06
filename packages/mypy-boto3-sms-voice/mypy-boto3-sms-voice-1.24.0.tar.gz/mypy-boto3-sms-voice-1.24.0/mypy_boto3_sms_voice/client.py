"""
Type annotations for sms-voice service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sms_voice.client import PinpointSMSVoiceClient

    session = Session()
    client: PinpointSMSVoiceClient = session.client("sms-voice")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    EventDestinationDefinitionTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    ListConfigurationSetsResponseTypeDef,
    SendVoiceMessageResponseTypeDef,
    VoiceMessageContentTypeDef,
)

__all__ = ("PinpointSMSVoiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class PinpointSMSVoiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PinpointSMSVoiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#can_paginate)
        """

    def create_configuration_set(self, *, ConfigurationSetName: str = ...) -> Dict[str, Any]:
        """
        Create a new configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.create_configuration_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#create_configuration_set)
        """

    def create_configuration_set_event_destination(
        self,
        *,
        ConfigurationSetName: str,
        EventDestination: EventDestinationDefinitionTypeDef = ...,
        EventDestinationName: str = ...
    ) -> Dict[str, Any]:
        """
        Create a new event destination in a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.create_configuration_set_event_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#create_configuration_set_event_destination)
        """

    def delete_configuration_set(self, *, ConfigurationSetName: str) -> Dict[str, Any]:
        """
        Deletes an existing configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.delete_configuration_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#delete_configuration_set)
        """

    def delete_configuration_set_event_destination(
        self, *, ConfigurationSetName: str, EventDestinationName: str
    ) -> Dict[str, Any]:
        """
        Deletes an event destination in a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.delete_configuration_set_event_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#delete_configuration_set_event_destination)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#generate_presigned_url)
        """

    def get_configuration_set_event_destinations(
        self, *, ConfigurationSetName: str
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        Obtain information about an event destination, including the types of events it
        reports, the Amazon Resource Name (ARN) of the destination, and the name of the
        event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.get_configuration_set_event_destinations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#get_configuration_set_event_destinations)
        """

    def list_configuration_sets(
        self, *, NextToken: str = ..., PageSize: str = ...
    ) -> ListConfigurationSetsResponseTypeDef:
        """
        List all of the configuration sets associated with your Amazon Pinpoint account
        in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.list_configuration_sets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#list_configuration_sets)
        """

    def send_voice_message(
        self,
        *,
        CallerId: str = ...,
        ConfigurationSetName: str = ...,
        Content: VoiceMessageContentTypeDef = ...,
        DestinationPhoneNumber: str = ...,
        OriginationPhoneNumber: str = ...
    ) -> SendVoiceMessageResponseTypeDef:
        """
        Create a new voice message and send it to a recipient's phone number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.send_voice_message)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#send_voice_message)
        """

    def update_configuration_set_event_destination(
        self,
        *,
        ConfigurationSetName: str,
        EventDestinationName: str,
        EventDestination: EventDestinationDefinitionTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Update an event destination in a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#PinpointSMSVoice.Client.update_configuration_set_event_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/client/#update_configuration_set_event_destination)
        """
