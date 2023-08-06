"""
Main interface for dynamodbstreams service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dynamodbstreams import (
        Client,
        DynamoDBStreamsClient,
    )

    session = Session()
    client: DynamoDBStreamsClient = session.client("dynamodbstreams")
    ```
"""
from .client import DynamoDBStreamsClient

Client = DynamoDBStreamsClient


__all__ = ("Client", "DynamoDBStreamsClient")
