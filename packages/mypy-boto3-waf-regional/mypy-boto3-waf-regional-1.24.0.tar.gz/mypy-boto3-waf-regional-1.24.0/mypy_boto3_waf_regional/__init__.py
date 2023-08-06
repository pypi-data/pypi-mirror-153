"""
Main interface for waf-regional service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_waf_regional import (
        Client,
        WAFRegionalClient,
    )

    session = Session()
    client: WAFRegionalClient = session.client("waf-regional")
    ```
"""
from .client import WAFRegionalClient

Client = WAFRegionalClient


__all__ = ("Client", "WAFRegionalClient")
