"""
Main interface for sagemaker-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_runtime import (
        Client,
        SageMakerRuntimeClient,
    )

    session = Session()
    client: SageMakerRuntimeClient = session.client("sagemaker-runtime")
    ```
"""
from .client import SageMakerRuntimeClient

Client = SageMakerRuntimeClient


__all__ = ("Client", "SageMakerRuntimeClient")
