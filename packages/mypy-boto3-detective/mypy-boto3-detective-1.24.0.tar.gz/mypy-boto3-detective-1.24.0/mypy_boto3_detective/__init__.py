"""
Main interface for detective service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_detective import (
        Client,
        DetectiveClient,
    )

    session = Session()
    client: DetectiveClient = session.client("detective")
    ```
"""
from .client import DetectiveClient

Client = DetectiveClient


__all__ = ("Client", "DetectiveClient")
