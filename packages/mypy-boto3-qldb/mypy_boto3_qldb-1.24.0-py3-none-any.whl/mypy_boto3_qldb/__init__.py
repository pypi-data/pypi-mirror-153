"""
Main interface for qldb service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_qldb import (
        Client,
        QLDBClient,
    )

    session = Session()
    client: QLDBClient = session.client("qldb")
    ```
"""
from .client import QLDBClient

Client = QLDBClient


__all__ = ("Client", "QLDBClient")
