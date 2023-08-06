"""
Main interface for pinpoint service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pinpoint import (
        Client,
        PinpointClient,
    )

    session = Session()
    client: PinpointClient = session.client("pinpoint")
    ```
"""
from .client import PinpointClient

Client = PinpointClient


__all__ = ("Client", "PinpointClient")
