"""
Main interface for resiliencehub service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resiliencehub import (
        Client,
        ResilienceHubClient,
    )

    session = Session()
    client: ResilienceHubClient = session.client("resiliencehub")
    ```
"""
from .client import ResilienceHubClient

Client = ResilienceHubClient


__all__ = ("Client", "ResilienceHubClient")
