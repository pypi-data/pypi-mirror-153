"""
Main interface for kendra service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kendra import (
        Client,
        kendraClient,
    )

    session = Session()
    client: kendraClient = session.client("kendra")
    ```
"""
from .client import kendraClient

Client = kendraClient


__all__ = ("Client", "kendraClient")
