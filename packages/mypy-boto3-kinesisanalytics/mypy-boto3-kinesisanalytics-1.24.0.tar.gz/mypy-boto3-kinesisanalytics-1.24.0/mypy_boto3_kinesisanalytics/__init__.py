"""
Main interface for kinesisanalytics service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesisanalytics import (
        Client,
        KinesisAnalyticsClient,
    )

    session = Session()
    client: KinesisAnalyticsClient = session.client("kinesisanalytics")
    ```
"""
from .client import KinesisAnalyticsClient

Client = KinesisAnalyticsClient


__all__ = ("Client", "KinesisAnalyticsClient")
