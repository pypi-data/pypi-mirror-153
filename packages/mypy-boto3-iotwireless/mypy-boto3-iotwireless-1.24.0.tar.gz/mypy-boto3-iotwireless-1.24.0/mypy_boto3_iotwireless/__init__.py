"""
Main interface for iotwireless service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotwireless import (
        Client,
        IoTWirelessClient,
    )

    session = Session()
    client: IoTWirelessClient = session.client("iotwireless")
    ```
"""
from .client import IoTWirelessClient

Client = IoTWirelessClient


__all__ = ("Client", "IoTWirelessClient")
