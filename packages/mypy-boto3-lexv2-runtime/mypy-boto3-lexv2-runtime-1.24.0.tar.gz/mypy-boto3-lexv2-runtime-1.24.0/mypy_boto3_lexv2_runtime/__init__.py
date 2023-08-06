"""
Main interface for lexv2-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lexv2_runtime import (
        Client,
        LexRuntimeV2Client,
    )

    session = Session()
    client: LexRuntimeV2Client = session.client("lexv2-runtime")
    ```
"""
from .client import LexRuntimeV2Client

Client = LexRuntimeV2Client


__all__ = ("Client", "LexRuntimeV2Client")
