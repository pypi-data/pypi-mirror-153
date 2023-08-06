"""
Main interface for firehose service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_firehose import (
        Client,
        FirehoseClient,
    )

    session = Session()
    client: FirehoseClient = session.client("firehose")
    ```
"""
from .client import FirehoseClient

Client = FirehoseClient


__all__ = ("Client", "FirehoseClient")
