"""
Main interface for compute-optimizer service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_compute_optimizer import (
        Client,
        ComputeOptimizerClient,
    )

    session = Session()
    client: ComputeOptimizerClient = session.client("compute-optimizer")
    ```
"""
from .client import ComputeOptimizerClient

Client = ComputeOptimizerClient


__all__ = ("Client", "ComputeOptimizerClient")
