"""
Main interface for iotsecuretunneling service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotsecuretunneling import (
        Client,
        IoTSecureTunnelingClient,
    )

    session = Session()
    client: IoTSecureTunnelingClient = session.client("iotsecuretunneling")
    ```
"""
from .client import IoTSecureTunnelingClient

Client = IoTSecureTunnelingClient


__all__ = ("Client", "IoTSecureTunnelingClient")
