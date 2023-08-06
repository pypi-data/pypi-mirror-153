"""
Type annotations for sns service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/type_defs/)

Usage::

    ```python
    from mypy_boto3_sns.type_defs import AddPermissionInputRequestTypeDef

    data: AddPermissionInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    LanguageCodeStringType,
    NumberCapabilityType,
    RouteTypeType,
    SMSSandboxPhoneNumberVerificationStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AddPermissionInputRequestTypeDef",
    "AddPermissionInputTopicAddPermissionTypeDef",
    "BatchResultErrorEntryTypeDef",
    "CheckIfPhoneNumberIsOptedOutInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ConfirmSubscriptionInputRequestTypeDef",
    "ConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef",
    "CreatePlatformApplicationInputRequestTypeDef",
    "CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef",
    "CreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef",
    "CreatePlatformEndpointInputRequestTypeDef",
    "CreateSMSSandboxPhoneNumberInputRequestTypeDef",
    "TagTypeDef",
    "DeleteEndpointInputRequestTypeDef",
    "DeletePlatformApplicationInputRequestTypeDef",
    "DeleteSMSSandboxPhoneNumberInputRequestTypeDef",
    "DeleteTopicInputRequestTypeDef",
    "EndpointTypeDef",
    "GetEndpointAttributesInputRequestTypeDef",
    "GetPlatformApplicationAttributesInputRequestTypeDef",
    "GetSMSAttributesInputRequestTypeDef",
    "GetSubscriptionAttributesInputRequestTypeDef",
    "GetTopicAttributesInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListEndpointsByPlatformApplicationInputRequestTypeDef",
    "ListOriginationNumbersRequestRequestTypeDef",
    "PhoneNumberInformationTypeDef",
    "ListPhoneNumbersOptedOutInputRequestTypeDef",
    "ListPlatformApplicationsInputRequestTypeDef",
    "PlatformApplicationTypeDef",
    "ListSMSSandboxPhoneNumbersInputRequestTypeDef",
    "SMSSandboxPhoneNumberTypeDef",
    "ListSubscriptionsByTopicInputRequestTypeDef",
    "SubscriptionTypeDef",
    "ListSubscriptionsInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTopicsInputRequestTypeDef",
    "TopicTypeDef",
    "MessageAttributeValueTypeDef",
    "OptInPhoneNumberInputRequestTypeDef",
    "PublishBatchResultEntryTypeDef",
    "RemovePermissionInputRequestTypeDef",
    "RemovePermissionInputTopicRemovePermissionTypeDef",
    "ServiceResourcePlatformApplicationRequestTypeDef",
    "ServiceResourcePlatformEndpointRequestTypeDef",
    "ServiceResourceSubscriptionRequestTypeDef",
    "ServiceResourceTopicRequestTypeDef",
    "SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef",
    "SetEndpointAttributesInputRequestTypeDef",
    "SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef",
    "SetPlatformApplicationAttributesInputRequestTypeDef",
    "SetSMSAttributesInputRequestTypeDef",
    "SetSubscriptionAttributesInputRequestTypeDef",
    "SetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef",
    "SetTopicAttributesInputRequestTypeDef",
    "SetTopicAttributesInputTopicSetAttributesTypeDef",
    "SubscribeInputRequestTypeDef",
    "SubscribeInputTopicSubscribeTypeDef",
    "UnsubscribeInputRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "VerifySMSSandboxPhoneNumberInputRequestTypeDef",
    "CheckIfPhoneNumberIsOptedOutResponseTypeDef",
    "ConfirmSubscriptionResponseTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreatePlatformApplicationResponseTypeDef",
    "CreateTopicResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetEndpointAttributesResponseTypeDef",
    "GetPlatformApplicationAttributesResponseTypeDef",
    "GetSMSAttributesResponseTypeDef",
    "GetSMSSandboxAccountStatusResultTypeDef",
    "GetSubscriptionAttributesResponseTypeDef",
    "GetTopicAttributesResponseTypeDef",
    "ListPhoneNumbersOptedOutResponseTypeDef",
    "PublishResponseTypeDef",
    "SubscribeResponseTypeDef",
    "CreateTopicInputRequestTypeDef",
    "CreateTopicInputServiceResourceCreateTopicTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListEndpointsByPlatformApplicationResponseTypeDef",
    "ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef",
    "ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef",
    "ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef",
    "ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef",
    "ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef",
    "ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef",
    "ListSubscriptionsInputListSubscriptionsPaginateTypeDef",
    "ListTopicsInputListTopicsPaginateTypeDef",
    "ListOriginationNumbersResultTypeDef",
    "ListPlatformApplicationsResponseTypeDef",
    "ListSMSSandboxPhoneNumbersResultTypeDef",
    "ListSubscriptionsByTopicResponseTypeDef",
    "ListSubscriptionsResponseTypeDef",
    "ListTopicsResponseTypeDef",
    "PublishBatchRequestEntryTypeDef",
    "PublishInputPlatformEndpointPublishTypeDef",
    "PublishInputRequestTypeDef",
    "PublishInputTopicPublishTypeDef",
    "PublishBatchResponseTypeDef",
    "PublishBatchInputRequestTypeDef",
)

AddPermissionInputRequestTypeDef = TypedDict(
    "AddPermissionInputRequestTypeDef",
    {
        "TopicArn": str,
        "Label": str,
        "AWSAccountId": Sequence[str],
        "ActionName": Sequence[str],
    },
)

AddPermissionInputTopicAddPermissionTypeDef = TypedDict(
    "AddPermissionInputTopicAddPermissionTypeDef",
    {
        "Label": str,
        "AWSAccountId": Sequence[str],
        "ActionName": Sequence[str],
    },
)

_RequiredBatchResultErrorEntryTypeDef = TypedDict(
    "_RequiredBatchResultErrorEntryTypeDef",
    {
        "Id": str,
        "Code": str,
        "SenderFault": bool,
    },
)
_OptionalBatchResultErrorEntryTypeDef = TypedDict(
    "_OptionalBatchResultErrorEntryTypeDef",
    {
        "Message": str,
    },
    total=False,
)


class BatchResultErrorEntryTypeDef(
    _RequiredBatchResultErrorEntryTypeDef, _OptionalBatchResultErrorEntryTypeDef
):
    pass


CheckIfPhoneNumberIsOptedOutInputRequestTypeDef = TypedDict(
    "CheckIfPhoneNumberIsOptedOutInputRequestTypeDef",
    {
        "phoneNumber": str,
    },
)

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

_RequiredConfirmSubscriptionInputRequestTypeDef = TypedDict(
    "_RequiredConfirmSubscriptionInputRequestTypeDef",
    {
        "TopicArn": str,
        "Token": str,
    },
)
_OptionalConfirmSubscriptionInputRequestTypeDef = TypedDict(
    "_OptionalConfirmSubscriptionInputRequestTypeDef",
    {
        "AuthenticateOnUnsubscribe": str,
    },
    total=False,
)


class ConfirmSubscriptionInputRequestTypeDef(
    _RequiredConfirmSubscriptionInputRequestTypeDef, _OptionalConfirmSubscriptionInputRequestTypeDef
):
    pass


_RequiredConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef = TypedDict(
    "_RequiredConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef",
    {
        "Token": str,
    },
)
_OptionalConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef = TypedDict(
    "_OptionalConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef",
    {
        "AuthenticateOnUnsubscribe": str,
    },
    total=False,
)


class ConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef(
    _RequiredConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef,
    _OptionalConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef,
):
    pass


CreatePlatformApplicationInputRequestTypeDef = TypedDict(
    "CreatePlatformApplicationInputRequestTypeDef",
    {
        "Name": str,
        "Platform": str,
        "Attributes": Mapping[str, str],
    },
)

CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef = TypedDict(
    "CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef",
    {
        "Name": str,
        "Platform": str,
        "Attributes": Mapping[str, str],
    },
)

_RequiredCreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef = TypedDict(
    "_RequiredCreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef",
    {
        "Token": str,
    },
)
_OptionalCreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef = TypedDict(
    "_OptionalCreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef",
    {
        "CustomUserData": str,
        "Attributes": Mapping[str, str],
    },
    total=False,
)


class CreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef(
    _RequiredCreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef,
    _OptionalCreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef,
):
    pass


_RequiredCreatePlatformEndpointInputRequestTypeDef = TypedDict(
    "_RequiredCreatePlatformEndpointInputRequestTypeDef",
    {
        "PlatformApplicationArn": str,
        "Token": str,
    },
)
_OptionalCreatePlatformEndpointInputRequestTypeDef = TypedDict(
    "_OptionalCreatePlatformEndpointInputRequestTypeDef",
    {
        "CustomUserData": str,
        "Attributes": Mapping[str, str],
    },
    total=False,
)


class CreatePlatformEndpointInputRequestTypeDef(
    _RequiredCreatePlatformEndpointInputRequestTypeDef,
    _OptionalCreatePlatformEndpointInputRequestTypeDef,
):
    pass


_RequiredCreateSMSSandboxPhoneNumberInputRequestTypeDef = TypedDict(
    "_RequiredCreateSMSSandboxPhoneNumberInputRequestTypeDef",
    {
        "PhoneNumber": str,
    },
)
_OptionalCreateSMSSandboxPhoneNumberInputRequestTypeDef = TypedDict(
    "_OptionalCreateSMSSandboxPhoneNumberInputRequestTypeDef",
    {
        "LanguageCode": LanguageCodeStringType,
    },
    total=False,
)


class CreateSMSSandboxPhoneNumberInputRequestTypeDef(
    _RequiredCreateSMSSandboxPhoneNumberInputRequestTypeDef,
    _OptionalCreateSMSSandboxPhoneNumberInputRequestTypeDef,
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteEndpointInputRequestTypeDef = TypedDict(
    "DeleteEndpointInputRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

DeletePlatformApplicationInputRequestTypeDef = TypedDict(
    "DeletePlatformApplicationInputRequestTypeDef",
    {
        "PlatformApplicationArn": str,
    },
)

DeleteSMSSandboxPhoneNumberInputRequestTypeDef = TypedDict(
    "DeleteSMSSandboxPhoneNumberInputRequestTypeDef",
    {
        "PhoneNumber": str,
    },
)

DeleteTopicInputRequestTypeDef = TypedDict(
    "DeleteTopicInputRequestTypeDef",
    {
        "TopicArn": str,
    },
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "EndpointArn": str,
        "Attributes": Dict[str, str],
    },
    total=False,
)

GetEndpointAttributesInputRequestTypeDef = TypedDict(
    "GetEndpointAttributesInputRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

GetPlatformApplicationAttributesInputRequestTypeDef = TypedDict(
    "GetPlatformApplicationAttributesInputRequestTypeDef",
    {
        "PlatformApplicationArn": str,
    },
)

GetSMSAttributesInputRequestTypeDef = TypedDict(
    "GetSMSAttributesInputRequestTypeDef",
    {
        "attributes": Sequence[str],
    },
    total=False,
)

GetSubscriptionAttributesInputRequestTypeDef = TypedDict(
    "GetSubscriptionAttributesInputRequestTypeDef",
    {
        "SubscriptionArn": str,
    },
)

GetTopicAttributesInputRequestTypeDef = TypedDict(
    "GetTopicAttributesInputRequestTypeDef",
    {
        "TopicArn": str,
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

_RequiredListEndpointsByPlatformApplicationInputRequestTypeDef = TypedDict(
    "_RequiredListEndpointsByPlatformApplicationInputRequestTypeDef",
    {
        "PlatformApplicationArn": str,
    },
)
_OptionalListEndpointsByPlatformApplicationInputRequestTypeDef = TypedDict(
    "_OptionalListEndpointsByPlatformApplicationInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListEndpointsByPlatformApplicationInputRequestTypeDef(
    _RequiredListEndpointsByPlatformApplicationInputRequestTypeDef,
    _OptionalListEndpointsByPlatformApplicationInputRequestTypeDef,
):
    pass


ListOriginationNumbersRequestRequestTypeDef = TypedDict(
    "ListOriginationNumbersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

PhoneNumberInformationTypeDef = TypedDict(
    "PhoneNumberInformationTypeDef",
    {
        "CreatedAt": datetime,
        "PhoneNumber": str,
        "Status": str,
        "Iso2CountryCode": str,
        "RouteType": RouteTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
    },
    total=False,
)

ListPhoneNumbersOptedOutInputRequestTypeDef = TypedDict(
    "ListPhoneNumbersOptedOutInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

ListPlatformApplicationsInputRequestTypeDef = TypedDict(
    "ListPlatformApplicationsInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

PlatformApplicationTypeDef = TypedDict(
    "PlatformApplicationTypeDef",
    {
        "PlatformApplicationArn": str,
        "Attributes": Dict[str, str],
    },
    total=False,
)

ListSMSSandboxPhoneNumbersInputRequestTypeDef = TypedDict(
    "ListSMSSandboxPhoneNumbersInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SMSSandboxPhoneNumberTypeDef = TypedDict(
    "SMSSandboxPhoneNumberTypeDef",
    {
        "PhoneNumber": str,
        "Status": SMSSandboxPhoneNumberVerificationStatusType,
    },
    total=False,
)

_RequiredListSubscriptionsByTopicInputRequestTypeDef = TypedDict(
    "_RequiredListSubscriptionsByTopicInputRequestTypeDef",
    {
        "TopicArn": str,
    },
)
_OptionalListSubscriptionsByTopicInputRequestTypeDef = TypedDict(
    "_OptionalListSubscriptionsByTopicInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListSubscriptionsByTopicInputRequestTypeDef(
    _RequiredListSubscriptionsByTopicInputRequestTypeDef,
    _OptionalListSubscriptionsByTopicInputRequestTypeDef,
):
    pass


SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "SubscriptionArn": str,
        "Owner": str,
        "Protocol": str,
        "Endpoint": str,
        "TopicArn": str,
    },
    total=False,
)

ListSubscriptionsInputRequestTypeDef = TypedDict(
    "ListSubscriptionsInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTopicsInputRequestTypeDef = TypedDict(
    "ListTopicsInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

TopicTypeDef = TypedDict(
    "TopicTypeDef",
    {
        "TopicArn": str,
    },
    total=False,
)

_RequiredMessageAttributeValueTypeDef = TypedDict(
    "_RequiredMessageAttributeValueTypeDef",
    {
        "DataType": str,
    },
)
_OptionalMessageAttributeValueTypeDef = TypedDict(
    "_OptionalMessageAttributeValueTypeDef",
    {
        "StringValue": str,
        "BinaryValue": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class MessageAttributeValueTypeDef(
    _RequiredMessageAttributeValueTypeDef, _OptionalMessageAttributeValueTypeDef
):
    pass


OptInPhoneNumberInputRequestTypeDef = TypedDict(
    "OptInPhoneNumberInputRequestTypeDef",
    {
        "phoneNumber": str,
    },
)

PublishBatchResultEntryTypeDef = TypedDict(
    "PublishBatchResultEntryTypeDef",
    {
        "Id": str,
        "MessageId": str,
        "SequenceNumber": str,
    },
    total=False,
)

RemovePermissionInputRequestTypeDef = TypedDict(
    "RemovePermissionInputRequestTypeDef",
    {
        "TopicArn": str,
        "Label": str,
    },
)

RemovePermissionInputTopicRemovePermissionTypeDef = TypedDict(
    "RemovePermissionInputTopicRemovePermissionTypeDef",
    {
        "Label": str,
    },
)

ServiceResourcePlatformApplicationRequestTypeDef = TypedDict(
    "ServiceResourcePlatformApplicationRequestTypeDef",
    {
        "arn": str,
    },
)

ServiceResourcePlatformEndpointRequestTypeDef = TypedDict(
    "ServiceResourcePlatformEndpointRequestTypeDef",
    {
        "arn": str,
    },
)

ServiceResourceSubscriptionRequestTypeDef = TypedDict(
    "ServiceResourceSubscriptionRequestTypeDef",
    {
        "arn": str,
    },
)

ServiceResourceTopicRequestTypeDef = TypedDict(
    "ServiceResourceTopicRequestTypeDef",
    {
        "arn": str,
    },
)

SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef = TypedDict(
    "SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef",
    {
        "Attributes": Mapping[str, str],
    },
)

SetEndpointAttributesInputRequestTypeDef = TypedDict(
    "SetEndpointAttributesInputRequestTypeDef",
    {
        "EndpointArn": str,
        "Attributes": Mapping[str, str],
    },
)

SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef = TypedDict(
    "SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef",
    {
        "Attributes": Mapping[str, str],
    },
)

SetPlatformApplicationAttributesInputRequestTypeDef = TypedDict(
    "SetPlatformApplicationAttributesInputRequestTypeDef",
    {
        "PlatformApplicationArn": str,
        "Attributes": Mapping[str, str],
    },
)

SetSMSAttributesInputRequestTypeDef = TypedDict(
    "SetSMSAttributesInputRequestTypeDef",
    {
        "attributes": Mapping[str, str],
    },
)

_RequiredSetSubscriptionAttributesInputRequestTypeDef = TypedDict(
    "_RequiredSetSubscriptionAttributesInputRequestTypeDef",
    {
        "SubscriptionArn": str,
        "AttributeName": str,
    },
)
_OptionalSetSubscriptionAttributesInputRequestTypeDef = TypedDict(
    "_OptionalSetSubscriptionAttributesInputRequestTypeDef",
    {
        "AttributeValue": str,
    },
    total=False,
)


class SetSubscriptionAttributesInputRequestTypeDef(
    _RequiredSetSubscriptionAttributesInputRequestTypeDef,
    _OptionalSetSubscriptionAttributesInputRequestTypeDef,
):
    pass


_RequiredSetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef = TypedDict(
    "_RequiredSetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef",
    {
        "AttributeName": str,
    },
)
_OptionalSetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef = TypedDict(
    "_OptionalSetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef",
    {
        "AttributeValue": str,
    },
    total=False,
)


class SetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef(
    _RequiredSetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef,
    _OptionalSetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef,
):
    pass


_RequiredSetTopicAttributesInputRequestTypeDef = TypedDict(
    "_RequiredSetTopicAttributesInputRequestTypeDef",
    {
        "TopicArn": str,
        "AttributeName": str,
    },
)
_OptionalSetTopicAttributesInputRequestTypeDef = TypedDict(
    "_OptionalSetTopicAttributesInputRequestTypeDef",
    {
        "AttributeValue": str,
    },
    total=False,
)


class SetTopicAttributesInputRequestTypeDef(
    _RequiredSetTopicAttributesInputRequestTypeDef, _OptionalSetTopicAttributesInputRequestTypeDef
):
    pass


_RequiredSetTopicAttributesInputTopicSetAttributesTypeDef = TypedDict(
    "_RequiredSetTopicAttributesInputTopicSetAttributesTypeDef",
    {
        "AttributeName": str,
    },
)
_OptionalSetTopicAttributesInputTopicSetAttributesTypeDef = TypedDict(
    "_OptionalSetTopicAttributesInputTopicSetAttributesTypeDef",
    {
        "AttributeValue": str,
    },
    total=False,
)


class SetTopicAttributesInputTopicSetAttributesTypeDef(
    _RequiredSetTopicAttributesInputTopicSetAttributesTypeDef,
    _OptionalSetTopicAttributesInputTopicSetAttributesTypeDef,
):
    pass


_RequiredSubscribeInputRequestTypeDef = TypedDict(
    "_RequiredSubscribeInputRequestTypeDef",
    {
        "TopicArn": str,
        "Protocol": str,
    },
)
_OptionalSubscribeInputRequestTypeDef = TypedDict(
    "_OptionalSubscribeInputRequestTypeDef",
    {
        "Endpoint": str,
        "Attributes": Mapping[str, str],
        "ReturnSubscriptionArn": bool,
    },
    total=False,
)


class SubscribeInputRequestTypeDef(
    _RequiredSubscribeInputRequestTypeDef, _OptionalSubscribeInputRequestTypeDef
):
    pass


_RequiredSubscribeInputTopicSubscribeTypeDef = TypedDict(
    "_RequiredSubscribeInputTopicSubscribeTypeDef",
    {
        "Protocol": str,
    },
)
_OptionalSubscribeInputTopicSubscribeTypeDef = TypedDict(
    "_OptionalSubscribeInputTopicSubscribeTypeDef",
    {
        "Endpoint": str,
        "Attributes": Mapping[str, str],
        "ReturnSubscriptionArn": bool,
    },
    total=False,
)


class SubscribeInputTopicSubscribeTypeDef(
    _RequiredSubscribeInputTopicSubscribeTypeDef, _OptionalSubscribeInputTopicSubscribeTypeDef
):
    pass


UnsubscribeInputRequestTypeDef = TypedDict(
    "UnsubscribeInputRequestTypeDef",
    {
        "SubscriptionArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

VerifySMSSandboxPhoneNumberInputRequestTypeDef = TypedDict(
    "VerifySMSSandboxPhoneNumberInputRequestTypeDef",
    {
        "PhoneNumber": str,
        "OneTimePassword": str,
    },
)

CheckIfPhoneNumberIsOptedOutResponseTypeDef = TypedDict(
    "CheckIfPhoneNumberIsOptedOutResponseTypeDef",
    {
        "isOptedOut": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfirmSubscriptionResponseTypeDef = TypedDict(
    "ConfirmSubscriptionResponseTypeDef",
    {
        "SubscriptionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEndpointResponseTypeDef = TypedDict(
    "CreateEndpointResponseTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePlatformApplicationResponseTypeDef = TypedDict(
    "CreatePlatformApplicationResponseTypeDef",
    {
        "PlatformApplicationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTopicResponseTypeDef = TypedDict(
    "CreateTopicResponseTypeDef",
    {
        "TopicArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEndpointAttributesResponseTypeDef = TypedDict(
    "GetEndpointAttributesResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPlatformApplicationAttributesResponseTypeDef = TypedDict(
    "GetPlatformApplicationAttributesResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSMSAttributesResponseTypeDef = TypedDict(
    "GetSMSAttributesResponseTypeDef",
    {
        "attributes": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSMSSandboxAccountStatusResultTypeDef = TypedDict(
    "GetSMSSandboxAccountStatusResultTypeDef",
    {
        "IsInSandbox": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSubscriptionAttributesResponseTypeDef = TypedDict(
    "GetSubscriptionAttributesResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTopicAttributesResponseTypeDef = TypedDict(
    "GetTopicAttributesResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPhoneNumbersOptedOutResponseTypeDef = TypedDict(
    "ListPhoneNumbersOptedOutResponseTypeDef",
    {
        "phoneNumbers": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublishResponseTypeDef = TypedDict(
    "PublishResponseTypeDef",
    {
        "MessageId": str,
        "SequenceNumber": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubscribeResponseTypeDef = TypedDict(
    "SubscribeResponseTypeDef",
    {
        "SubscriptionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateTopicInputRequestTypeDef = TypedDict(
    "_RequiredCreateTopicInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateTopicInputRequestTypeDef = TypedDict(
    "_OptionalCreateTopicInputRequestTypeDef",
    {
        "Attributes": Mapping[str, str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateTopicInputRequestTypeDef(
    _RequiredCreateTopicInputRequestTypeDef, _OptionalCreateTopicInputRequestTypeDef
):
    pass


_RequiredCreateTopicInputServiceResourceCreateTopicTypeDef = TypedDict(
    "_RequiredCreateTopicInputServiceResourceCreateTopicTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateTopicInputServiceResourceCreateTopicTypeDef = TypedDict(
    "_OptionalCreateTopicInputServiceResourceCreateTopicTypeDef",
    {
        "Attributes": Mapping[str, str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateTopicInputServiceResourceCreateTopicTypeDef(
    _RequiredCreateTopicInputServiceResourceCreateTopicTypeDef,
    _OptionalCreateTopicInputServiceResourceCreateTopicTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListEndpointsByPlatformApplicationResponseTypeDef = TypedDict(
    "ListEndpointsByPlatformApplicationResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef = TypedDict(
    "_RequiredListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef",
    {
        "PlatformApplicationArn": str,
    },
)
_OptionalListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef = TypedDict(
    "_OptionalListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef(
    _RequiredListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef,
    _OptionalListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef,
):
    pass


ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef = TypedDict(
    "ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef = TypedDict(
    "ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef = TypedDict(
    "ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef = TypedDict(
    "ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef = TypedDict(
    "_RequiredListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef",
    {
        "TopicArn": str,
    },
)
_OptionalListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef = TypedDict(
    "_OptionalListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef(
    _RequiredListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef,
    _OptionalListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef,
):
    pass


ListSubscriptionsInputListSubscriptionsPaginateTypeDef = TypedDict(
    "ListSubscriptionsInputListSubscriptionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTopicsInputListTopicsPaginateTypeDef = TypedDict(
    "ListTopicsInputListTopicsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOriginationNumbersResultTypeDef = TypedDict(
    "ListOriginationNumbersResultTypeDef",
    {
        "NextToken": str,
        "PhoneNumbers": List[PhoneNumberInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPlatformApplicationsResponseTypeDef = TypedDict(
    "ListPlatformApplicationsResponseTypeDef",
    {
        "PlatformApplications": List[PlatformApplicationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSMSSandboxPhoneNumbersResultTypeDef = TypedDict(
    "ListSMSSandboxPhoneNumbersResultTypeDef",
    {
        "PhoneNumbers": List[SMSSandboxPhoneNumberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscriptionsByTopicResponseTypeDef = TypedDict(
    "ListSubscriptionsByTopicResponseTypeDef",
    {
        "Subscriptions": List[SubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscriptionsResponseTypeDef = TypedDict(
    "ListSubscriptionsResponseTypeDef",
    {
        "Subscriptions": List[SubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTopicsResponseTypeDef = TypedDict(
    "ListTopicsResponseTypeDef",
    {
        "Topics": List[TopicTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPublishBatchRequestEntryTypeDef = TypedDict(
    "_RequiredPublishBatchRequestEntryTypeDef",
    {
        "Id": str,
        "Message": str,
    },
)
_OptionalPublishBatchRequestEntryTypeDef = TypedDict(
    "_OptionalPublishBatchRequestEntryTypeDef",
    {
        "Subject": str,
        "MessageStructure": str,
        "MessageAttributes": Mapping[str, MessageAttributeValueTypeDef],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class PublishBatchRequestEntryTypeDef(
    _RequiredPublishBatchRequestEntryTypeDef, _OptionalPublishBatchRequestEntryTypeDef
):
    pass


_RequiredPublishInputPlatformEndpointPublishTypeDef = TypedDict(
    "_RequiredPublishInputPlatformEndpointPublishTypeDef",
    {
        "Message": str,
    },
)
_OptionalPublishInputPlatformEndpointPublishTypeDef = TypedDict(
    "_OptionalPublishInputPlatformEndpointPublishTypeDef",
    {
        "TopicArn": str,
        "PhoneNumber": str,
        "Subject": str,
        "MessageStructure": str,
        "MessageAttributes": Mapping[str, MessageAttributeValueTypeDef],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class PublishInputPlatformEndpointPublishTypeDef(
    _RequiredPublishInputPlatformEndpointPublishTypeDef,
    _OptionalPublishInputPlatformEndpointPublishTypeDef,
):
    pass


_RequiredPublishInputRequestTypeDef = TypedDict(
    "_RequiredPublishInputRequestTypeDef",
    {
        "Message": str,
    },
)
_OptionalPublishInputRequestTypeDef = TypedDict(
    "_OptionalPublishInputRequestTypeDef",
    {
        "TopicArn": str,
        "TargetArn": str,
        "PhoneNumber": str,
        "Subject": str,
        "MessageStructure": str,
        "MessageAttributes": Mapping[str, MessageAttributeValueTypeDef],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class PublishInputRequestTypeDef(
    _RequiredPublishInputRequestTypeDef, _OptionalPublishInputRequestTypeDef
):
    pass


_RequiredPublishInputTopicPublishTypeDef = TypedDict(
    "_RequiredPublishInputTopicPublishTypeDef",
    {
        "Message": str,
    },
)
_OptionalPublishInputTopicPublishTypeDef = TypedDict(
    "_OptionalPublishInputTopicPublishTypeDef",
    {
        "TargetArn": str,
        "PhoneNumber": str,
        "Subject": str,
        "MessageStructure": str,
        "MessageAttributes": Mapping[str, MessageAttributeValueTypeDef],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class PublishInputTopicPublishTypeDef(
    _RequiredPublishInputTopicPublishTypeDef, _OptionalPublishInputTopicPublishTypeDef
):
    pass


PublishBatchResponseTypeDef = TypedDict(
    "PublishBatchResponseTypeDef",
    {
        "Successful": List[PublishBatchResultEntryTypeDef],
        "Failed": List[BatchResultErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublishBatchInputRequestTypeDef = TypedDict(
    "PublishBatchInputRequestTypeDef",
    {
        "TopicArn": str,
        "PublishBatchRequestEntries": Sequence[PublishBatchRequestEntryTypeDef],
    },
)
