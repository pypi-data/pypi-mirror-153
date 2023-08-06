"""
Type annotations for sms-voice service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/type_defs/)

Usage::

    ```python
    from mypy_boto3_sms_voice.type_defs import CallInstructionsMessageTypeTypeDef

    data: CallInstructionsMessageTypeTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import EventTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CallInstructionsMessageTypeTypeDef",
    "CloudWatchLogsDestinationTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "SnsDestinationTypeDef",
    "GetConfigurationSetEventDestinationsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ListConfigurationSetsRequestRequestTypeDef",
    "PlainTextMessageTypeTypeDef",
    "SSMLMessageTypeTypeDef",
    "EventDestinationDefinitionTypeDef",
    "EventDestinationTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "SendVoiceMessageResponseTypeDef",
    "VoiceMessageContentTypeDef",
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    "SendVoiceMessageRequestRequestTypeDef",
)

CallInstructionsMessageTypeTypeDef = TypedDict(
    "CallInstructionsMessageTypeTypeDef",
    {
        "Text": str,
    },
    total=False,
)

CloudWatchLogsDestinationTypeDef = TypedDict(
    "CloudWatchLogsDestinationTypeDef",
    {
        "IamRoleArn": str,
        "LogGroupArn": str,
    },
    total=False,
)

CreateConfigurationSetRequestRequestTypeDef = TypedDict(
    "CreateConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
    total=False,
)

DeleteConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
    },
)

DeleteConfigurationSetRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef",
    {
        "DeliveryStreamArn": str,
        "IamRoleArn": str,
    },
    total=False,
)

SnsDestinationTypeDef = TypedDict(
    "SnsDestinationTypeDef",
    {
        "TopicArn": str,
    },
    total=False,
)

GetConfigurationSetEventDestinationsRequestRequestTypeDef = TypedDict(
    "GetConfigurationSetEventDestinationsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
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

ListConfigurationSetsRequestRequestTypeDef = TypedDict(
    "ListConfigurationSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": str,
    },
    total=False,
)

PlainTextMessageTypeTypeDef = TypedDict(
    "PlainTextMessageTypeTypeDef",
    {
        "LanguageCode": str,
        "Text": str,
        "VoiceId": str,
    },
    total=False,
)

SSMLMessageTypeTypeDef = TypedDict(
    "SSMLMessageTypeTypeDef",
    {
        "LanguageCode": str,
        "Text": str,
        "VoiceId": str,
    },
    total=False,
)

EventDestinationDefinitionTypeDef = TypedDict(
    "EventDestinationDefinitionTypeDef",
    {
        "CloudWatchLogsDestination": CloudWatchLogsDestinationTypeDef,
        "Enabled": bool,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "MatchingEventTypes": Sequence[EventTypeType],
        "SnsDestination": SnsDestinationTypeDef,
    },
    total=False,
)

EventDestinationTypeDef = TypedDict(
    "EventDestinationTypeDef",
    {
        "CloudWatchLogsDestination": CloudWatchLogsDestinationTypeDef,
        "Enabled": bool,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "MatchingEventTypes": List[EventTypeType],
        "Name": str,
        "SnsDestination": SnsDestinationTypeDef,
    },
    total=False,
)

ListConfigurationSetsResponseTypeDef = TypedDict(
    "ListConfigurationSetsResponseTypeDef",
    {
        "ConfigurationSets": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendVoiceMessageResponseTypeDef = TypedDict(
    "SendVoiceMessageResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VoiceMessageContentTypeDef = TypedDict(
    "VoiceMessageContentTypeDef",
    {
        "CallInstructionsMessage": CallInstructionsMessageTypeTypeDef,
        "PlainTextMessage": PlainTextMessageTypeTypeDef,
        "SSMLMessage": SSMLMessageTypeTypeDef,
    },
    total=False,
)

_RequiredCreateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalCreateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "EventDestination": EventDestinationDefinitionTypeDef,
        "EventDestinationName": str,
    },
    total=False,
)

class CreateConfigurationSetEventDestinationRequestRequestTypeDef(
    _RequiredCreateConfigurationSetEventDestinationRequestRequestTypeDef,
    _OptionalCreateConfigurationSetEventDestinationRequestRequestTypeDef,
):
    pass

_RequiredUpdateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
    },
)
_OptionalUpdateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "EventDestination": EventDestinationDefinitionTypeDef,
    },
    total=False,
)

class UpdateConfigurationSetEventDestinationRequestRequestTypeDef(
    _RequiredUpdateConfigurationSetEventDestinationRequestRequestTypeDef,
    _OptionalUpdateConfigurationSetEventDestinationRequestRequestTypeDef,
):
    pass

GetConfigurationSetEventDestinationsResponseTypeDef = TypedDict(
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    {
        "EventDestinations": List[EventDestinationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendVoiceMessageRequestRequestTypeDef = TypedDict(
    "SendVoiceMessageRequestRequestTypeDef",
    {
        "CallerId": str,
        "ConfigurationSetName": str,
        "Content": VoiceMessageContentTypeDef,
        "DestinationPhoneNumber": str,
        "OriginationPhoneNumber": str,
    },
    total=False,
)
