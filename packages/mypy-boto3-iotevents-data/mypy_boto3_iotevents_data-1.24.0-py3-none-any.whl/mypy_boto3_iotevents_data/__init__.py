"""
Main interface for iotevents-data service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotevents_data import (
        Client,
        IoTEventsDataClient,
    )

    session = Session()
    client: IoTEventsDataClient = session.client("iotevents-data")
    ```
"""
from .client import IoTEventsDataClient

Client = IoTEventsDataClient


__all__ = ("Client", "IoTEventsDataClient")
