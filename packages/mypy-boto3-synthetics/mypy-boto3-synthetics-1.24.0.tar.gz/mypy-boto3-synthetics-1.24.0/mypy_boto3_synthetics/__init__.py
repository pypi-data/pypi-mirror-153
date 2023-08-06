"""
Main interface for synthetics service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_synthetics import (
        Client,
        SyntheticsClient,
    )

    session = Session()
    client: SyntheticsClient = session.client("synthetics")
    ```
"""
from .client import SyntheticsClient

Client = SyntheticsClient


__all__ = ("Client", "SyntheticsClient")
