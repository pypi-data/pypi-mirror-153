"""
Main interface for auditmanager service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_auditmanager import (
        AuditManagerClient,
        Client,
    )

    session = Session()
    client: AuditManagerClient = session.client("auditmanager")
    ```
"""
from .client import AuditManagerClient

Client = AuditManagerClient


__all__ = ("AuditManagerClient", "Client")
