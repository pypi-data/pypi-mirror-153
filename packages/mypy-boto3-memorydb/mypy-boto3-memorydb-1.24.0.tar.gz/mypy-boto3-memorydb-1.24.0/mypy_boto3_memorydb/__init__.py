"""
Main interface for memorydb service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_memorydb import (
        Client,
        MemoryDBClient,
    )

    session = Session()
    client: MemoryDBClient = session.client("memorydb")
    ```
"""
from .client import MemoryDBClient

Client = MemoryDBClient


__all__ = ("Client", "MemoryDBClient")
