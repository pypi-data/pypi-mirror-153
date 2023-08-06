"""
Type annotations for connectparticipant service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectparticipant/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectparticipant.type_defs import AttachmentItemTypeDef

    data: AttachmentItemTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import (
    ArtifactStatusType,
    ChatItemTypeType,
    ConnectionTypeType,
    ParticipantRoleType,
    ScanDirectionType,
    SortKeyType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AttachmentItemTypeDef",
    "CompleteAttachmentUploadRequestRequestTypeDef",
    "ConnectionCredentialsTypeDef",
    "CreateParticipantConnectionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "WebsocketTypeDef",
    "DisconnectParticipantRequestRequestTypeDef",
    "GetAttachmentRequestRequestTypeDef",
    "StartPositionTypeDef",
    "SendEventRequestRequestTypeDef",
    "SendMessageRequestRequestTypeDef",
    "StartAttachmentUploadRequestRequestTypeDef",
    "UploadMetadataTypeDef",
    "ItemTypeDef",
    "GetAttachmentResponseTypeDef",
    "SendEventResponseTypeDef",
    "SendMessageResponseTypeDef",
    "CreateParticipantConnectionResponseTypeDef",
    "GetTranscriptRequestRequestTypeDef",
    "StartAttachmentUploadResponseTypeDef",
    "GetTranscriptResponseTypeDef",
)

AttachmentItemTypeDef = TypedDict(
    "AttachmentItemTypeDef",
    {
        "ContentType": str,
        "AttachmentId": str,
        "AttachmentName": str,
        "Status": ArtifactStatusType,
    },
    total=False,
)

CompleteAttachmentUploadRequestRequestTypeDef = TypedDict(
    "CompleteAttachmentUploadRequestRequestTypeDef",
    {
        "AttachmentIds": Sequence[str],
        "ClientToken": str,
        "ConnectionToken": str,
    },
)

ConnectionCredentialsTypeDef = TypedDict(
    "ConnectionCredentialsTypeDef",
    {
        "ConnectionToken": str,
        "Expiry": str,
    },
    total=False,
)

_RequiredCreateParticipantConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateParticipantConnectionRequestRequestTypeDef",
    {
        "Type": Sequence[ConnectionTypeType],
        "ParticipantToken": str,
    },
)
_OptionalCreateParticipantConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateParticipantConnectionRequestRequestTypeDef",
    {
        "ConnectParticipant": bool,
    },
    total=False,
)


class CreateParticipantConnectionRequestRequestTypeDef(
    _RequiredCreateParticipantConnectionRequestRequestTypeDef,
    _OptionalCreateParticipantConnectionRequestRequestTypeDef,
):
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

WebsocketTypeDef = TypedDict(
    "WebsocketTypeDef",
    {
        "Url": str,
        "ConnectionExpiry": str,
    },
    total=False,
)

_RequiredDisconnectParticipantRequestRequestTypeDef = TypedDict(
    "_RequiredDisconnectParticipantRequestRequestTypeDef",
    {
        "ConnectionToken": str,
    },
)
_OptionalDisconnectParticipantRequestRequestTypeDef = TypedDict(
    "_OptionalDisconnectParticipantRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class DisconnectParticipantRequestRequestTypeDef(
    _RequiredDisconnectParticipantRequestRequestTypeDef,
    _OptionalDisconnectParticipantRequestRequestTypeDef,
):
    pass


GetAttachmentRequestRequestTypeDef = TypedDict(
    "GetAttachmentRequestRequestTypeDef",
    {
        "AttachmentId": str,
        "ConnectionToken": str,
    },
)

StartPositionTypeDef = TypedDict(
    "StartPositionTypeDef",
    {
        "Id": str,
        "AbsoluteTime": str,
        "MostRecent": int,
    },
    total=False,
)

_RequiredSendEventRequestRequestTypeDef = TypedDict(
    "_RequiredSendEventRequestRequestTypeDef",
    {
        "ContentType": str,
        "ConnectionToken": str,
    },
)
_OptionalSendEventRequestRequestTypeDef = TypedDict(
    "_OptionalSendEventRequestRequestTypeDef",
    {
        "Content": str,
        "ClientToken": str,
    },
    total=False,
)


class SendEventRequestRequestTypeDef(
    _RequiredSendEventRequestRequestTypeDef, _OptionalSendEventRequestRequestTypeDef
):
    pass


_RequiredSendMessageRequestRequestTypeDef = TypedDict(
    "_RequiredSendMessageRequestRequestTypeDef",
    {
        "ContentType": str,
        "Content": str,
        "ConnectionToken": str,
    },
)
_OptionalSendMessageRequestRequestTypeDef = TypedDict(
    "_OptionalSendMessageRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class SendMessageRequestRequestTypeDef(
    _RequiredSendMessageRequestRequestTypeDef, _OptionalSendMessageRequestRequestTypeDef
):
    pass


StartAttachmentUploadRequestRequestTypeDef = TypedDict(
    "StartAttachmentUploadRequestRequestTypeDef",
    {
        "ContentType": str,
        "AttachmentSizeInBytes": int,
        "AttachmentName": str,
        "ClientToken": str,
        "ConnectionToken": str,
    },
)

UploadMetadataTypeDef = TypedDict(
    "UploadMetadataTypeDef",
    {
        "Url": str,
        "UrlExpiry": str,
        "HeadersToInclude": Dict[str, str],
    },
    total=False,
)

ItemTypeDef = TypedDict(
    "ItemTypeDef",
    {
        "AbsoluteTime": str,
        "Content": str,
        "ContentType": str,
        "Id": str,
        "Type": ChatItemTypeType,
        "ParticipantId": str,
        "DisplayName": str,
        "ParticipantRole": ParticipantRoleType,
        "Attachments": List[AttachmentItemTypeDef],
    },
    total=False,
)

GetAttachmentResponseTypeDef = TypedDict(
    "GetAttachmentResponseTypeDef",
    {
        "Url": str,
        "UrlExpiry": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendEventResponseTypeDef = TypedDict(
    "SendEventResponseTypeDef",
    {
        "Id": str,
        "AbsoluteTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendMessageResponseTypeDef = TypedDict(
    "SendMessageResponseTypeDef",
    {
        "Id": str,
        "AbsoluteTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateParticipantConnectionResponseTypeDef = TypedDict(
    "CreateParticipantConnectionResponseTypeDef",
    {
        "Websocket": WebsocketTypeDef,
        "ConnectionCredentials": ConnectionCredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetTranscriptRequestRequestTypeDef = TypedDict(
    "_RequiredGetTranscriptRequestRequestTypeDef",
    {
        "ConnectionToken": str,
    },
)
_OptionalGetTranscriptRequestRequestTypeDef = TypedDict(
    "_OptionalGetTranscriptRequestRequestTypeDef",
    {
        "ContactId": str,
        "MaxResults": int,
        "NextToken": str,
        "ScanDirection": ScanDirectionType,
        "SortOrder": SortKeyType,
        "StartPosition": StartPositionTypeDef,
    },
    total=False,
)


class GetTranscriptRequestRequestTypeDef(
    _RequiredGetTranscriptRequestRequestTypeDef, _OptionalGetTranscriptRequestRequestTypeDef
):
    pass


StartAttachmentUploadResponseTypeDef = TypedDict(
    "StartAttachmentUploadResponseTypeDef",
    {
        "AttachmentId": str,
        "UploadMetadata": UploadMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTranscriptResponseTypeDef = TypedDict(
    "GetTranscriptResponseTypeDef",
    {
        "InitialContactId": str,
        "Transcript": List[ItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
