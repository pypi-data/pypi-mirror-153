"""
Main interface for sesv2 service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sesv2 import (
        Client,
        SESV2Client,
    )

    session = Session()
    client: SESV2Client = session.client("sesv2")
    ```
"""
from .client import SESV2Client

Client = SESV2Client


__all__ = ("Client", "SESV2Client")
