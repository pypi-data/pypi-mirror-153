"""
Main interface for worklink service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_worklink import (
        Client,
        WorkLinkClient,
    )

    session = Session()
    client: WorkLinkClient = session.client("worklink")
    ```
"""
from .client import WorkLinkClient

Client = WorkLinkClient


__all__ = ("Client", "WorkLinkClient")
