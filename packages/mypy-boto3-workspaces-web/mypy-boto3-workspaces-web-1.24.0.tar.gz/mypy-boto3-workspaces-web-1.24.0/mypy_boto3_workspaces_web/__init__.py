"""
Main interface for workspaces-web service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workspaces_web import (
        Client,
        WorkSpacesWebClient,
    )

    session = Session()
    client: WorkSpacesWebClient = session.client("workspaces-web")
    ```
"""
from .client import WorkSpacesWebClient

Client = WorkSpacesWebClient


__all__ = ("Client", "WorkSpacesWebClient")
