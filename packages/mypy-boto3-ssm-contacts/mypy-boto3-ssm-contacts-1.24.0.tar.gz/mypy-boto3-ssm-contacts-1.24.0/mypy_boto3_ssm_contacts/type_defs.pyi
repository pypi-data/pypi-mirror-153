"""
Type annotations for ssm-contacts service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_contacts.type_defs import AcceptPageRequestRequestTypeDef

    data: AcceptPageRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AcceptCodeValidationType,
    AcceptTypeType,
    ActivationStatusType,
    ChannelTypeType,
    ContactTypeType,
    ReceiptTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AcceptPageRequestRequestTypeDef",
    "ActivateContactChannelRequestRequestTypeDef",
    "ChannelTargetInfoTypeDef",
    "ContactChannelAddressTypeDef",
    "ContactTargetInfoTypeDef",
    "ContactTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "DeactivateContactChannelRequestRequestTypeDef",
    "DeleteContactChannelRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DescribeEngagementRequestRequestTypeDef",
    "DescribePageRequestRequestTypeDef",
    "EngagementTypeDef",
    "GetContactChannelRequestRequestTypeDef",
    "GetContactPolicyRequestRequestTypeDef",
    "GetContactRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListContactChannelsRequestRequestTypeDef",
    "ListContactsRequestRequestTypeDef",
    "TimeRangeTypeDef",
    "ListPageReceiptsRequestRequestTypeDef",
    "ReceiptTypeDef",
    "ListPagesByContactRequestRequestTypeDef",
    "PageTypeDef",
    "ListPagesByEngagementRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutContactPolicyRequestRequestTypeDef",
    "SendActivationCodeRequestRequestTypeDef",
    "StartEngagementRequestRequestTypeDef",
    "StopEngagementRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ContactChannelTypeDef",
    "CreateContactChannelRequestRequestTypeDef",
    "UpdateContactChannelRequestRequestTypeDef",
    "TargetTypeDef",
    "CreateContactChannelResultTypeDef",
    "CreateContactResultTypeDef",
    "DescribeEngagementResultTypeDef",
    "DescribePageResultTypeDef",
    "GetContactChannelResultTypeDef",
    "GetContactPolicyResultTypeDef",
    "ListContactsResultTypeDef",
    "StartEngagementResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListEngagementsResultTypeDef",
    "ListContactChannelsRequestListContactChannelsPaginateTypeDef",
    "ListContactsRequestListContactsPaginateTypeDef",
    "ListPageReceiptsRequestListPageReceiptsPaginateTypeDef",
    "ListPagesByContactRequestListPagesByContactPaginateTypeDef",
    "ListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef",
    "ListEngagementsRequestListEngagementsPaginateTypeDef",
    "ListEngagementsRequestRequestTypeDef",
    "ListPageReceiptsResultTypeDef",
    "ListPagesByContactResultTypeDef",
    "ListPagesByEngagementResultTypeDef",
    "ListContactChannelsResultTypeDef",
    "StageTypeDef",
    "PlanTypeDef",
    "CreateContactRequestRequestTypeDef",
    "GetContactResultTypeDef",
    "UpdateContactRequestRequestTypeDef",
)

_RequiredAcceptPageRequestRequestTypeDef = TypedDict(
    "_RequiredAcceptPageRequestRequestTypeDef",
    {
        "PageId": str,
        "AcceptType": AcceptTypeType,
        "AcceptCode": str,
    },
)
_OptionalAcceptPageRequestRequestTypeDef = TypedDict(
    "_OptionalAcceptPageRequestRequestTypeDef",
    {
        "ContactChannelId": str,
        "Note": str,
        "AcceptCodeValidation": AcceptCodeValidationType,
    },
    total=False,
)

class AcceptPageRequestRequestTypeDef(
    _RequiredAcceptPageRequestRequestTypeDef, _OptionalAcceptPageRequestRequestTypeDef
):
    pass

ActivateContactChannelRequestRequestTypeDef = TypedDict(
    "ActivateContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
        "ActivationCode": str,
    },
)

_RequiredChannelTargetInfoTypeDef = TypedDict(
    "_RequiredChannelTargetInfoTypeDef",
    {
        "ContactChannelId": str,
    },
)
_OptionalChannelTargetInfoTypeDef = TypedDict(
    "_OptionalChannelTargetInfoTypeDef",
    {
        "RetryIntervalInMinutes": int,
    },
    total=False,
)

class ChannelTargetInfoTypeDef(
    _RequiredChannelTargetInfoTypeDef, _OptionalChannelTargetInfoTypeDef
):
    pass

ContactChannelAddressTypeDef = TypedDict(
    "ContactChannelAddressTypeDef",
    {
        "SimpleAddress": str,
    },
    total=False,
)

_RequiredContactTargetInfoTypeDef = TypedDict(
    "_RequiredContactTargetInfoTypeDef",
    {
        "IsEssential": bool,
    },
)
_OptionalContactTargetInfoTypeDef = TypedDict(
    "_OptionalContactTargetInfoTypeDef",
    {
        "ContactId": str,
    },
    total=False,
)

class ContactTargetInfoTypeDef(
    _RequiredContactTargetInfoTypeDef, _OptionalContactTargetInfoTypeDef
):
    pass

_RequiredContactTypeDef = TypedDict(
    "_RequiredContactTypeDef",
    {
        "ContactArn": str,
        "Alias": str,
        "Type": ContactTypeType,
    },
)
_OptionalContactTypeDef = TypedDict(
    "_OptionalContactTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)

class ContactTypeDef(_RequiredContactTypeDef, _OptionalContactTypeDef):
    pass

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

DeactivateContactChannelRequestRequestTypeDef = TypedDict(
    "DeactivateContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

DeleteContactChannelRequestRequestTypeDef = TypedDict(
    "DeleteContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

DeleteContactRequestRequestTypeDef = TypedDict(
    "DeleteContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)

DescribeEngagementRequestRequestTypeDef = TypedDict(
    "DescribeEngagementRequestRequestTypeDef",
    {
        "EngagementId": str,
    },
)

DescribePageRequestRequestTypeDef = TypedDict(
    "DescribePageRequestRequestTypeDef",
    {
        "PageId": str,
    },
)

_RequiredEngagementTypeDef = TypedDict(
    "_RequiredEngagementTypeDef",
    {
        "EngagementArn": str,
        "ContactArn": str,
        "Sender": str,
    },
)
_OptionalEngagementTypeDef = TypedDict(
    "_OptionalEngagementTypeDef",
    {
        "IncidentId": str,
        "StartTime": datetime,
        "StopTime": datetime,
    },
    total=False,
)

class EngagementTypeDef(_RequiredEngagementTypeDef, _OptionalEngagementTypeDef):
    pass

GetContactChannelRequestRequestTypeDef = TypedDict(
    "GetContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

GetContactPolicyRequestRequestTypeDef = TypedDict(
    "GetContactPolicyRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)

GetContactRequestRequestTypeDef = TypedDict(
    "GetContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListContactChannelsRequestRequestTypeDef = TypedDict(
    "_RequiredListContactChannelsRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListContactChannelsRequestRequestTypeDef = TypedDict(
    "_OptionalListContactChannelsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListContactChannelsRequestRequestTypeDef(
    _RequiredListContactChannelsRequestRequestTypeDef,
    _OptionalListContactChannelsRequestRequestTypeDef,
):
    pass

ListContactsRequestRequestTypeDef = TypedDict(
    "ListContactsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "AliasPrefix": str,
        "Type": ContactTypeType,
    },
    total=False,
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
    total=False,
)

_RequiredListPageReceiptsRequestRequestTypeDef = TypedDict(
    "_RequiredListPageReceiptsRequestRequestTypeDef",
    {
        "PageId": str,
    },
)
_OptionalListPageReceiptsRequestRequestTypeDef = TypedDict(
    "_OptionalListPageReceiptsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPageReceiptsRequestRequestTypeDef(
    _RequiredListPageReceiptsRequestRequestTypeDef, _OptionalListPageReceiptsRequestRequestTypeDef
):
    pass

_RequiredReceiptTypeDef = TypedDict(
    "_RequiredReceiptTypeDef",
    {
        "ReceiptType": ReceiptTypeType,
        "ReceiptTime": datetime,
    },
)
_OptionalReceiptTypeDef = TypedDict(
    "_OptionalReceiptTypeDef",
    {
        "ContactChannelArn": str,
        "ReceiptInfo": str,
    },
    total=False,
)

class ReceiptTypeDef(_RequiredReceiptTypeDef, _OptionalReceiptTypeDef):
    pass

_RequiredListPagesByContactRequestRequestTypeDef = TypedDict(
    "_RequiredListPagesByContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListPagesByContactRequestRequestTypeDef = TypedDict(
    "_OptionalListPagesByContactRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPagesByContactRequestRequestTypeDef(
    _RequiredListPagesByContactRequestRequestTypeDef,
    _OptionalListPagesByContactRequestRequestTypeDef,
):
    pass

_RequiredPageTypeDef = TypedDict(
    "_RequiredPageTypeDef",
    {
        "PageArn": str,
        "EngagementArn": str,
        "ContactArn": str,
        "Sender": str,
    },
)
_OptionalPageTypeDef = TypedDict(
    "_OptionalPageTypeDef",
    {
        "IncidentId": str,
        "SentTime": datetime,
        "DeliveryTime": datetime,
        "ReadTime": datetime,
    },
    total=False,
)

class PageTypeDef(_RequiredPageTypeDef, _OptionalPageTypeDef):
    pass

_RequiredListPagesByEngagementRequestRequestTypeDef = TypedDict(
    "_RequiredListPagesByEngagementRequestRequestTypeDef",
    {
        "EngagementId": str,
    },
)
_OptionalListPagesByEngagementRequestRequestTypeDef = TypedDict(
    "_OptionalListPagesByEngagementRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPagesByEngagementRequestRequestTypeDef(
    _RequiredListPagesByEngagementRequestRequestTypeDef,
    _OptionalListPagesByEngagementRequestRequestTypeDef,
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

PutContactPolicyRequestRequestTypeDef = TypedDict(
    "PutContactPolicyRequestRequestTypeDef",
    {
        "ContactArn": str,
        "Policy": str,
    },
)

SendActivationCodeRequestRequestTypeDef = TypedDict(
    "SendActivationCodeRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

_RequiredStartEngagementRequestRequestTypeDef = TypedDict(
    "_RequiredStartEngagementRequestRequestTypeDef",
    {
        "ContactId": str,
        "Sender": str,
        "Subject": str,
        "Content": str,
    },
)
_OptionalStartEngagementRequestRequestTypeDef = TypedDict(
    "_OptionalStartEngagementRequestRequestTypeDef",
    {
        "PublicSubject": str,
        "PublicContent": str,
        "IncidentId": str,
        "IdempotencyToken": str,
    },
    total=False,
)

class StartEngagementRequestRequestTypeDef(
    _RequiredStartEngagementRequestRequestTypeDef, _OptionalStartEngagementRequestRequestTypeDef
):
    pass

_RequiredStopEngagementRequestRequestTypeDef = TypedDict(
    "_RequiredStopEngagementRequestRequestTypeDef",
    {
        "EngagementId": str,
    },
)
_OptionalStopEngagementRequestRequestTypeDef = TypedDict(
    "_OptionalStopEngagementRequestRequestTypeDef",
    {
        "Reason": str,
    },
    total=False,
)

class StopEngagementRequestRequestTypeDef(
    _RequiredStopEngagementRequestRequestTypeDef, _OptionalStopEngagementRequestRequestTypeDef
):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredContactChannelTypeDef = TypedDict(
    "_RequiredContactChannelTypeDef",
    {
        "ContactChannelArn": str,
        "ContactArn": str,
        "Name": str,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "ActivationStatus": ActivationStatusType,
    },
)
_OptionalContactChannelTypeDef = TypedDict(
    "_OptionalContactChannelTypeDef",
    {
        "Type": ChannelTypeType,
    },
    total=False,
)

class ContactChannelTypeDef(_RequiredContactChannelTypeDef, _OptionalContactChannelTypeDef):
    pass

_RequiredCreateContactChannelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactChannelRequestRequestTypeDef",
    {
        "ContactId": str,
        "Name": str,
        "Type": ChannelTypeType,
        "DeliveryAddress": ContactChannelAddressTypeDef,
    },
)
_OptionalCreateContactChannelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactChannelRequestRequestTypeDef",
    {
        "DeferActivation": bool,
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateContactChannelRequestRequestTypeDef(
    _RequiredCreateContactChannelRequestRequestTypeDef,
    _OptionalCreateContactChannelRequestRequestTypeDef,
):
    pass

_RequiredUpdateContactChannelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)
_OptionalUpdateContactChannelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactChannelRequestRequestTypeDef",
    {
        "Name": str,
        "DeliveryAddress": ContactChannelAddressTypeDef,
    },
    total=False,
)

class UpdateContactChannelRequestRequestTypeDef(
    _RequiredUpdateContactChannelRequestRequestTypeDef,
    _OptionalUpdateContactChannelRequestRequestTypeDef,
):
    pass

TargetTypeDef = TypedDict(
    "TargetTypeDef",
    {
        "ChannelTargetInfo": ChannelTargetInfoTypeDef,
        "ContactTargetInfo": ContactTargetInfoTypeDef,
    },
    total=False,
)

CreateContactChannelResultTypeDef = TypedDict(
    "CreateContactChannelResultTypeDef",
    {
        "ContactChannelArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateContactResultTypeDef = TypedDict(
    "CreateContactResultTypeDef",
    {
        "ContactArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEngagementResultTypeDef = TypedDict(
    "DescribeEngagementResultTypeDef",
    {
        "ContactArn": str,
        "EngagementArn": str,
        "Sender": str,
        "Subject": str,
        "Content": str,
        "PublicSubject": str,
        "PublicContent": str,
        "IncidentId": str,
        "StartTime": datetime,
        "StopTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePageResultTypeDef = TypedDict(
    "DescribePageResultTypeDef",
    {
        "PageArn": str,
        "EngagementArn": str,
        "ContactArn": str,
        "Sender": str,
        "Subject": str,
        "Content": str,
        "PublicSubject": str,
        "PublicContent": str,
        "IncidentId": str,
        "SentTime": datetime,
        "ReadTime": datetime,
        "DeliveryTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactChannelResultTypeDef = TypedDict(
    "GetContactChannelResultTypeDef",
    {
        "ContactArn": str,
        "ContactChannelArn": str,
        "Name": str,
        "Type": ChannelTypeType,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "ActivationStatus": ActivationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactPolicyResultTypeDef = TypedDict(
    "GetContactPolicyResultTypeDef",
    {
        "ContactArn": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContactsResultTypeDef = TypedDict(
    "ListContactsResultTypeDef",
    {
        "NextToken": str,
        "Contacts": List[ContactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartEngagementResultTypeDef = TypedDict(
    "StartEngagementResultTypeDef",
    {
        "EngagementArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListEngagementsResultTypeDef = TypedDict(
    "ListEngagementsResultTypeDef",
    {
        "NextToken": str,
        "Engagements": List[EngagementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListContactChannelsRequestListContactChannelsPaginateTypeDef = TypedDict(
    "_RequiredListContactChannelsRequestListContactChannelsPaginateTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListContactChannelsRequestListContactChannelsPaginateTypeDef = TypedDict(
    "_OptionalListContactChannelsRequestListContactChannelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListContactChannelsRequestListContactChannelsPaginateTypeDef(
    _RequiredListContactChannelsRequestListContactChannelsPaginateTypeDef,
    _OptionalListContactChannelsRequestListContactChannelsPaginateTypeDef,
):
    pass

ListContactsRequestListContactsPaginateTypeDef = TypedDict(
    "ListContactsRequestListContactsPaginateTypeDef",
    {
        "AliasPrefix": str,
        "Type": ContactTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPageReceiptsRequestListPageReceiptsPaginateTypeDef = TypedDict(
    "_RequiredListPageReceiptsRequestListPageReceiptsPaginateTypeDef",
    {
        "PageId": str,
    },
)
_OptionalListPageReceiptsRequestListPageReceiptsPaginateTypeDef = TypedDict(
    "_OptionalListPageReceiptsRequestListPageReceiptsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPageReceiptsRequestListPageReceiptsPaginateTypeDef(
    _RequiredListPageReceiptsRequestListPageReceiptsPaginateTypeDef,
    _OptionalListPageReceiptsRequestListPageReceiptsPaginateTypeDef,
):
    pass

_RequiredListPagesByContactRequestListPagesByContactPaginateTypeDef = TypedDict(
    "_RequiredListPagesByContactRequestListPagesByContactPaginateTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListPagesByContactRequestListPagesByContactPaginateTypeDef = TypedDict(
    "_OptionalListPagesByContactRequestListPagesByContactPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPagesByContactRequestListPagesByContactPaginateTypeDef(
    _RequiredListPagesByContactRequestListPagesByContactPaginateTypeDef,
    _OptionalListPagesByContactRequestListPagesByContactPaginateTypeDef,
):
    pass

_RequiredListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef = TypedDict(
    "_RequiredListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef",
    {
        "EngagementId": str,
    },
)
_OptionalListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef = TypedDict(
    "_OptionalListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef(
    _RequiredListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef,
    _OptionalListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef,
):
    pass

ListEngagementsRequestListEngagementsPaginateTypeDef = TypedDict(
    "ListEngagementsRequestListEngagementsPaginateTypeDef",
    {
        "IncidentId": str,
        "TimeRangeValue": TimeRangeTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEngagementsRequestRequestTypeDef = TypedDict(
    "ListEngagementsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "IncidentId": str,
        "TimeRangeValue": TimeRangeTypeDef,
    },
    total=False,
)

ListPageReceiptsResultTypeDef = TypedDict(
    "ListPageReceiptsResultTypeDef",
    {
        "NextToken": str,
        "Receipts": List[ReceiptTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPagesByContactResultTypeDef = TypedDict(
    "ListPagesByContactResultTypeDef",
    {
        "NextToken": str,
        "Pages": List[PageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPagesByEngagementResultTypeDef = TypedDict(
    "ListPagesByEngagementResultTypeDef",
    {
        "NextToken": str,
        "Pages": List[PageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContactChannelsResultTypeDef = TypedDict(
    "ListContactChannelsResultTypeDef",
    {
        "NextToken": str,
        "ContactChannels": List[ContactChannelTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StageTypeDef = TypedDict(
    "StageTypeDef",
    {
        "DurationInMinutes": int,
        "Targets": Sequence[TargetTypeDef],
    },
)

PlanTypeDef = TypedDict(
    "PlanTypeDef",
    {
        "Stages": Sequence[StageTypeDef],
    },
)

_RequiredCreateContactRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactRequestRequestTypeDef",
    {
        "Alias": str,
        "Type": ContactTypeType,
        "Plan": PlanTypeDef,
    },
)
_OptionalCreateContactRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Tags": Sequence[TagTypeDef],
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateContactRequestRequestTypeDef(
    _RequiredCreateContactRequestRequestTypeDef, _OptionalCreateContactRequestRequestTypeDef
):
    pass

GetContactResultTypeDef = TypedDict(
    "GetContactResultTypeDef",
    {
        "ContactArn": str,
        "Alias": str,
        "DisplayName": str,
        "Type": ContactTypeType,
        "Plan": PlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateContactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalUpdateContactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Plan": PlanTypeDef,
    },
    total=False,
)

class UpdateContactRequestRequestTypeDef(
    _RequiredUpdateContactRequestRequestTypeDef, _OptionalUpdateContactRequestRequestTypeDef
):
    pass
