"""
Main interface for amplifybackend service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amplifybackend import (
        AmplifyBackendClient,
        Client,
        ListBackendJobsPaginator,
    )

    session = Session()
    client: AmplifyBackendClient = session.client("amplifybackend")

    list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```
"""
from .client import AmplifyBackendClient
from .paginator import ListBackendJobsPaginator

Client = AmplifyBackendClient


__all__ = ("AmplifyBackendClient", "Client", "ListBackendJobsPaginator")
