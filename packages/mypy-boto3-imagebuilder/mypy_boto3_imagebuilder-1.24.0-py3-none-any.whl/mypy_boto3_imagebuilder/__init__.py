"""
Main interface for imagebuilder service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_imagebuilder import (
        Client,
        imagebuilderClient,
    )

    session = Session()
    client: imagebuilderClient = session.client("imagebuilder")
    ```
"""
from .client import imagebuilderClient

Client = imagebuilderClient


__all__ = ("Client", "imagebuilderClient")
