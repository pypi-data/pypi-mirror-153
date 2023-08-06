"""
Main interface for chime-sdk-media-pipelines service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime_sdk_media_pipelines import (
        ChimeSDKMediaPipelinesClient,
        Client,
    )

    session = Session()
    client: ChimeSDKMediaPipelinesClient = session.client("chime-sdk-media-pipelines")
    ```
"""
from .client import ChimeSDKMediaPipelinesClient

Client = ChimeSDKMediaPipelinesClient

__all__ = ("ChimeSDKMediaPipelinesClient", "Client")
