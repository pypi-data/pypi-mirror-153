"""
Main interface for rds-data service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_rds_data import (
        Client,
        RDSDataServiceClient,
    )

    session = Session()
    client: RDSDataServiceClient = session.client("rds-data")
    ```
"""
from .client import RDSDataServiceClient

Client = RDSDataServiceClient


__all__ = ("Client", "RDSDataServiceClient")
