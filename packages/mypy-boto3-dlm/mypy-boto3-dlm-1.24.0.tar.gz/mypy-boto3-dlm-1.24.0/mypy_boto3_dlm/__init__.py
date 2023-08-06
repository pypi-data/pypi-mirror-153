"""
Main interface for dlm service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dlm import (
        Client,
        DLMClient,
    )

    session = Session()
    client: DLMClient = session.client("dlm")
    ```
"""
from .client import DLMClient

Client = DLMClient


__all__ = ("Client", "DLMClient")
