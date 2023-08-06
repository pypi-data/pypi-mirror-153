"""
Main interface for chime-sdk-meetings service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime_sdk_meetings import (
        ChimeSDKMeetingsClient,
        Client,
    )

    session = Session()
    client: ChimeSDKMeetingsClient = session.client("chime-sdk-meetings")
    ```
"""
from .client import ChimeSDKMeetingsClient

Client = ChimeSDKMeetingsClient


__all__ = ("ChimeSDKMeetingsClient", "Client")
