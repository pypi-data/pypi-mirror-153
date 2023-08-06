"""
Main interface for customer-profiles service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_customer_profiles import (
        Client,
        CustomerProfilesClient,
    )

    session = Session()
    client: CustomerProfilesClient = session.client("customer-profiles")
    ```
"""
from .client import CustomerProfilesClient

Client = CustomerProfilesClient


__all__ = ("Client", "CustomerProfilesClient")
