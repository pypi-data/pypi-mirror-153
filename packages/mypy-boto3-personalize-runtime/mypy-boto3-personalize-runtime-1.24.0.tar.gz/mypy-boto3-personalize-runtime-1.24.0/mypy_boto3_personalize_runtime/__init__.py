"""
Main interface for personalize-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_personalize_runtime import (
        Client,
        PersonalizeRuntimeClient,
    )

    session = Session()
    client: PersonalizeRuntimeClient = session.client("personalize-runtime")
    ```
"""
from .client import PersonalizeRuntimeClient

Client = PersonalizeRuntimeClient


__all__ = ("Client", "PersonalizeRuntimeClient")
