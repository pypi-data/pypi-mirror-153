"""
Main interface for iotdeviceadvisor service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotdeviceadvisor import (
        Client,
        IoTDeviceAdvisorClient,
    )

    session = Session()
    client: IoTDeviceAdvisorClient = session.client("iotdeviceadvisor")
    ```
"""
from .client import IoTDeviceAdvisorClient

Client = IoTDeviceAdvisorClient


__all__ = ("Client", "IoTDeviceAdvisorClient")
