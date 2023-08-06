"""
Main interface for frauddetector service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_frauddetector import (
        Client,
        FraudDetectorClient,
    )

    session = Session()
    client: FraudDetectorClient = session.client("frauddetector")
    ```
"""
from .client import FraudDetectorClient

Client = FraudDetectorClient


__all__ = ("Client", "FraudDetectorClient")
