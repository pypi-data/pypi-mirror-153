"""
Main interface for kinesis-video-media service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_media import (
        Client,
        KinesisVideoMediaClient,
    )

    session = Session()
    client: KinesisVideoMediaClient = session.client("kinesis-video-media")
    ```
"""
from .client import KinesisVideoMediaClient

Client = KinesisVideoMediaClient


__all__ = ("Client", "KinesisVideoMediaClient")
