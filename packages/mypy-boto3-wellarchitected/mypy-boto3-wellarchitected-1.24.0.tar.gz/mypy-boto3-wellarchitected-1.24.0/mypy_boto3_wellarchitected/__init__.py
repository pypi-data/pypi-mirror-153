"""
Main interface for wellarchitected service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_wellarchitected import (
        Client,
        WellArchitectedClient,
    )

    session = Session()
    client: WellArchitectedClient = session.client("wellarchitected")
    ```
"""
from .client import WellArchitectedClient

Client = WellArchitectedClient


__all__ = ("Client", "WellArchitectedClient")
