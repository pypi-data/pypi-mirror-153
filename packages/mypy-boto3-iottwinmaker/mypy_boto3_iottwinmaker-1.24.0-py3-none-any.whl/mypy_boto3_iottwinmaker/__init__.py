"""
Main interface for iottwinmaker service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iottwinmaker import (
        Client,
        IoTTwinMakerClient,
    )

    session = Session()
    client: IoTTwinMakerClient = session.client("iottwinmaker")
    ```
"""
from .client import IoTTwinMakerClient

Client = IoTTwinMakerClient


__all__ = ("Client", "IoTTwinMakerClient")
