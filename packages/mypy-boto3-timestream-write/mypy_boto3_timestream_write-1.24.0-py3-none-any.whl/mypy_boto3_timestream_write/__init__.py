"""
Main interface for timestream-write service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_timestream_write import (
        Client,
        TimestreamWriteClient,
    )

    session = Session()
    client: TimestreamWriteClient = session.client("timestream-write")
    ```
"""
from .client import TimestreamWriteClient

Client = TimestreamWriteClient


__all__ = ("Client", "TimestreamWriteClient")
