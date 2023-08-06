"""
Main interface for kinesisvideo service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesisvideo import (
        Client,
        KinesisVideoClient,
        ListSignalingChannelsPaginator,
        ListStreamsPaginator,
    )

    session = Session()
    client: KinesisVideoClient = session.client("kinesisvideo")

    list_signaling_channels_paginator: ListSignalingChannelsPaginator = client.get_paginator("list_signaling_channels")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""
from .client import KinesisVideoClient
from .paginator import ListSignalingChannelsPaginator, ListStreamsPaginator

Client = KinesisVideoClient


__all__ = ("Client", "KinesisVideoClient", "ListSignalingChannelsPaginator", "ListStreamsPaginator")
