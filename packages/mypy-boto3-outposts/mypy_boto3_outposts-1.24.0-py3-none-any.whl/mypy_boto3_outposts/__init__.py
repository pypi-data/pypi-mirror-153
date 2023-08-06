"""
Main interface for outposts service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_outposts import (
        Client,
        OutpostsClient,
    )

    session = Session()
    client: OutpostsClient = session.client("outposts")
    ```
"""
from .client import OutpostsClient

Client = OutpostsClient


__all__ = ("Client", "OutpostsClient")
