"""
Main interface for pi service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pi import (
        Client,
        PIClient,
    )

    session = Session()
    client: PIClient = session.client("pi")
    ```
"""
from .client import PIClient

Client = PIClient


__all__ = ("Client", "PIClient")
