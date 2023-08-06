"""
Main interface for cloudtrail service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudtrail import (
        Client,
        CloudTrailClient,
        ListPublicKeysPaginator,
        ListTagsPaginator,
        ListTrailsPaginator,
        LookupEventsPaginator,
    )

    session = Session()
    client: CloudTrailClient = session.client("cloudtrail")

    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    list_trails_paginator: ListTrailsPaginator = client.get_paginator("list_trails")
    lookup_events_paginator: LookupEventsPaginator = client.get_paginator("lookup_events")
    ```
"""
from .client import CloudTrailClient
from .paginator import (
    ListPublicKeysPaginator,
    ListTagsPaginator,
    ListTrailsPaginator,
    LookupEventsPaginator,
)

Client = CloudTrailClient


__all__ = (
    "Client",
    "CloudTrailClient",
    "ListPublicKeysPaginator",
    "ListTagsPaginator",
    "ListTrailsPaginator",
    "LookupEventsPaginator",
)
