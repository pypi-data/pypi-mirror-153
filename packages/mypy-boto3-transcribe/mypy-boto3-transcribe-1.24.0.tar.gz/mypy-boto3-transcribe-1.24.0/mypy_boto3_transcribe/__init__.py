"""
Main interface for transcribe service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_transcribe import (
        Client,
        TranscribeServiceClient,
    )

    session = Session()
    client: TranscribeServiceClient = session.client("transcribe")
    ```
"""
from .client import TranscribeServiceClient

Client = TranscribeServiceClient


__all__ = ("Client", "TranscribeServiceClient")
