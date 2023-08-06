"""
Type annotations for chime-sdk-meetings service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime_sdk_meetings.client import ChimeSDKMeetingsClient

    session = Session()
    client: ChimeSDKMeetingsClient = session.client("chime-sdk-meetings")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AttendeeCapabilitiesTypeDef,
    AttendeeIdItemTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    CreateAttendeeRequestItemTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAttendeeResponseTypeDef,
    GetMeetingResponseTypeDef,
    ListAttendeesResponseTypeDef,
    MeetingFeaturesConfigurationTypeDef,
    NotificationsConfigurationTypeDef,
    TranscriptionConfigurationTypeDef,
    UpdateAttendeeCapabilitiesResponseTypeDef,
)

__all__ = ("ChimeSDKMeetingsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class ChimeSDKMeetingsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMeetingsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#exceptions)
        """

    def batch_create_attendee(
        self, *, MeetingId: str, Attendees: Sequence[CreateAttendeeRequestItemTypeDef]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.batch_create_attendee)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#batch_create_attendee)
        """

    def batch_update_attendee_capabilities_except(
        self,
        *,
        MeetingId: str,
        ExcludedAttendeeIds: Sequence[AttendeeIdItemTypeDef],
        Capabilities: AttendeeCapabilitiesTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates `AttendeeCapabilities` except the capabilities listed in an
        `ExcludedAttendeeIds` table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.batch_update_attendee_capabilities_except)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#batch_update_attendee_capabilities_except)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#can_paginate)
        """

    def create_attendee(
        self,
        *,
        MeetingId: str,
        ExternalUserId: str,
        Capabilities: AttendeeCapabilitiesTypeDef = ...
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.create_attendee)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#create_attendee)
        """

    def create_meeting(
        self,
        *,
        ClientRequestToken: str,
        MediaRegion: str,
        ExternalMeetingId: str,
        MeetingHostId: str = ...,
        NotificationsConfiguration: NotificationsConfigurationTypeDef = ...,
        MeetingFeatures: MeetingFeaturesConfigurationTypeDef = ...,
        PrimaryMeetingId: str = ...
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.create_meeting)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#create_meeting)
        """

    def create_meeting_with_attendees(
        self,
        *,
        ClientRequestToken: str,
        MediaRegion: str,
        ExternalMeetingId: str,
        Attendees: Sequence[CreateAttendeeRequestItemTypeDef],
        MeetingHostId: str = ...,
        MeetingFeatures: MeetingFeaturesConfigurationTypeDef = ...,
        NotificationsConfiguration: NotificationsConfigurationTypeDef = ...,
        PrimaryMeetingId: str = ...
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.create_meeting_with_attendees)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#create_meeting_with_attendees)
        """

    def delete_attendee(self, *, MeetingId: str, AttendeeId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their `JoinToken`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.delete_attendee)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#delete_attendee)
        """

    def delete_meeting(self, *, MeetingId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.delete_meeting)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#delete_meeting)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#generate_presigned_url)
        """

    def get_attendee(self, *, MeetingId: str, AttendeeId: str) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.get_attendee)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#get_attendee)
        """

    def get_meeting(self, *, MeetingId: str) -> GetMeetingResponseTypeDef:
        """
        Gets the Amazon Chime SDK meeting details for the specified meeting ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.get_meeting)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#get_meeting)
        """

    def list_attendees(
        self, *, MeetingId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.list_attendees)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#list_attendees)
        """

    def start_meeting_transcription(
        self, *, MeetingId: str, TranscriptionConfiguration: TranscriptionConfigurationTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts transcription for the specified `meetingId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.start_meeting_transcription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#start_meeting_transcription)
        """

    def stop_meeting_transcription(self, *, MeetingId: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops transcription for the specified `meetingId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.stop_meeting_transcription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#stop_meeting_transcription)
        """

    def update_attendee_capabilities(
        self, *, MeetingId: str, AttendeeId: str, Capabilities: AttendeeCapabilitiesTypeDef
    ) -> UpdateAttendeeCapabilitiesResponseTypeDef:
        """
        The capabilties that you want to update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.update_attendee_capabilities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_meetings/client/#update_attendee_capabilities)
        """
