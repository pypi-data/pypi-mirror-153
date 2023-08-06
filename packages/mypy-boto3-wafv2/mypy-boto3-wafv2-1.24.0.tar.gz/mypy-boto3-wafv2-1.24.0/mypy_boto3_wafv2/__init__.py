"""
Main interface for wafv2 service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_wafv2 import (
        Client,
        WAFV2Client,
    )

    session = Session()
    client: WAFV2Client = session.client("wafv2")
    ```
"""
from .client import WAFV2Client

Client = WAFV2Client


__all__ = ("Client", "WAFV2Client")
