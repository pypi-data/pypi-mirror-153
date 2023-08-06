"""
Type annotations for ssm-contacts service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm_contacts.client import SSMContactsClient
    from mypy_boto3_ssm_contacts.paginator import (
        ListContactChannelsPaginator,
        ListContactsPaginator,
        ListEngagementsPaginator,
        ListPageReceiptsPaginator,
        ListPagesByContactPaginator,
        ListPagesByEngagementPaginator,
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
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ContactTypeType
from .type_defs import (
    ListContactChannelsResultTypeDef,
    ListContactsResultTypeDef,
    ListEngagementsResultTypeDef,
    ListPageReceiptsResultTypeDef,
    ListPagesByContactResultTypeDef,
    ListPagesByEngagementResultTypeDef,
    PaginatorConfigTypeDef,
    TimeRangeTypeDef,
)

__all__ = (
    "ListContactChannelsPaginator",
    "ListContactsPaginator",
    "ListEngagementsPaginator",
    "ListPageReceiptsPaginator",
    "ListPagesByContactPaginator",
    "ListPagesByEngagementPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListContactChannelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContactChannels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactchannelspaginator)
    """

    def paginate(
        self, *, ContactId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactChannelsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContactChannels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactchannelspaginator)
        """


class ListContactsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContacts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactspaginator)
    """

    def paginate(
        self,
        *,
        AliasPrefix: str = ...,
        Type: ContactTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContacts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactspaginator)
        """


class ListEngagementsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListEngagements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listengagementspaginator)
    """

    def paginate(
        self,
        *,
        IncidentId: str = ...,
        TimeRangeValue: TimeRangeTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEngagementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListEngagements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listengagementspaginator)
        """


class ListPageReceiptsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageReceipts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagereceiptspaginator)
    """

    def paginate(
        self, *, PageId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPageReceiptsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageReceipts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagereceiptspaginator)
        """


class ListPagesByContactPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByContact)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbycontactpaginator)
    """

    def paginate(
        self, *, ContactId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPagesByContactResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByContact.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbycontactpaginator)
        """


class ListPagesByEngagementPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByEngagement)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbyengagementpaginator)
    """

    def paginate(
        self, *, EngagementId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPagesByEngagementResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByEngagement.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbyengagementpaginator)
        """
