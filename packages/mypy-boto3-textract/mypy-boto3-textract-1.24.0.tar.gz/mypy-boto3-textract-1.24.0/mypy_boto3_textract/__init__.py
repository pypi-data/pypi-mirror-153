"""
Main interface for textract service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_textract import (
        Client,
        TextractClient,
    )

    session = Session()
    client: TextractClient = session.client("textract")
    ```
"""
from .client import TextractClient

Client = TextractClient


__all__ = ("Client", "TextractClient")
