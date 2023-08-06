"""
Main interface for ssm-contacts service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ssm_contacts import (
        Client,
        ListContactChannelsPaginator,
        ListContactsPaginator,
        ListEngagementsPaginator,
        ListPageReceiptsPaginator,
        ListPagesByContactPaginator,
        ListPagesByEngagementPaginator,
        SSMContactsClient,
    )

    session = Session()
    client: SSMContactsClient = session.client("ssm-contacts")

    list_contact_channels_paginator: ListContactChannelsPaginator = client.get_paginator("list_contact_channels")
    list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
    list_engagements_paginator: ListEngagementsPaginator = client.get_paginator("list_engagements")
    list_page_receipts_paginator: ListPageReceiptsPaginator = client.get_paginator("list_page_receipts")
    list_pages_by_contact_paginator: ListPagesByContactPaginator = client.get_paginator("list_pages_by_contact")
    list_pages_by_engagement_paginator: ListPagesByEngagementPaginator = client.get_paginator("list_pages_by_engagement")
    ```
"""
from .client import SSMContactsClient
from .paginator import (
    ListContactChannelsPaginator,
    ListContactsPaginator,
    ListEngagementsPaginator,
    ListPageReceiptsPaginator,
    ListPagesByContactPaginator,
    ListPagesByEngagementPaginator,
)

Client = SSMContactsClient


__all__ = (
    "Client",
    "ListContactChannelsPaginator",
    "ListContactsPaginator",
    "ListEngagementsPaginator",
    "ListPageReceiptsPaginator",
    "ListPagesByContactPaginator",
    "ListPagesByEngagementPaginator",
    "SSMContactsClient",
)
