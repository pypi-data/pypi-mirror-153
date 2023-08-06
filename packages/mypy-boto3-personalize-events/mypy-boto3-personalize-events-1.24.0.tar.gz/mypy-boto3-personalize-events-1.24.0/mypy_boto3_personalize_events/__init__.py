"""
Main interface for personalize-events service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_personalize_events import (
        Client,
        PersonalizeEventsClient,
    )

    session = Session()
    client: PersonalizeEventsClient = session.client("personalize-events")
    ```
"""
from .client import PersonalizeEventsClient

Client = PersonalizeEventsClient


__all__ = ("Client", "PersonalizeEventsClient")
