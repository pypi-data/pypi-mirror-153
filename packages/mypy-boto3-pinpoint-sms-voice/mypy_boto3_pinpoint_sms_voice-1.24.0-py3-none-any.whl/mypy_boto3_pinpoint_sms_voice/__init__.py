"""
Main interface for pinpoint-sms-voice service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pinpoint_sms_voice import (
        Client,
        PinpointSMSVoiceClient,
    )

    session = Session()
    client: PinpointSMSVoiceClient = session.client("pinpoint-sms-voice")
    ```
"""
from .client import PinpointSMSVoiceClient

Client = PinpointSMSVoiceClient


__all__ = ("Client", "PinpointSMSVoiceClient")
