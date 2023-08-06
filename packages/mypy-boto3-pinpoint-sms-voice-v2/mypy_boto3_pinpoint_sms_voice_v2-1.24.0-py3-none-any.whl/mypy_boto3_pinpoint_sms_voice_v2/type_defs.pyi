"""
Type annotations for pinpoint-sms-voice-v2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/type_defs/)

Usage::

    ```python
    from mypy_boto3_pinpoint_sms_voice_v2.type_defs import AccountAttributeTypeDef

    data: AccountAttributeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccountLimitNameType,
    ConfigurationSetFilterNameType,
    DestinationCountryParameterKeyType,
    EventTypeType,
    KeywordActionType,
    MessageTypeType,
    NumberCapabilityType,
    NumberStatusType,
    NumberTypeType,
    PhoneNumberFilterNameType,
    PoolFilterNameType,
    PoolOriginationIdentitiesFilterNameType,
    PoolStatusType,
    RequestableNumberTypeType,
    SenderIdFilterNameType,
    SpendLimitNameType,
    VoiceIdType,
    VoiceMessageBodyTextTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountAttributeTypeDef",
    "AccountLimitTypeDef",
    "AssociateOriginationIdentityRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CloudWatchLogsDestinationTypeDef",
    "ConfigurationSetFilterTypeDef",
    "TagTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "SnsDestinationTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "DeleteDefaultMessageTypeRequestRequestTypeDef",
    "DeleteDefaultSenderIdRequestRequestTypeDef",
    "DeleteEventDestinationRequestRequestTypeDef",
    "DeleteKeywordRequestRequestTypeDef",
    "DeleteOptOutListRequestRequestTypeDef",
    "DeleteOptedOutNumberRequestRequestTypeDef",
    "DeletePoolRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAccountAttributesRequestRequestTypeDef",
    "DescribeAccountLimitsRequestRequestTypeDef",
    "KeywordFilterTypeDef",
    "KeywordInformationTypeDef",
    "DescribeOptOutListsRequestRequestTypeDef",
    "OptOutListInformationTypeDef",
    "OptedOutFilterTypeDef",
    "OptedOutNumberInformationTypeDef",
    "PhoneNumberFilterTypeDef",
    "PhoneNumberInformationTypeDef",
    "PoolFilterTypeDef",
    "PoolInformationTypeDef",
    "SenderIdAndCountryTypeDef",
    "SenderIdFilterTypeDef",
    "SenderIdInformationTypeDef",
    "DescribeSpendLimitsRequestRequestTypeDef",
    "SpendLimitTypeDef",
    "DisassociateOriginationIdentityRequestRequestTypeDef",
    "PoolOriginationIdentitiesFilterTypeDef",
    "OriginationIdentityMetadataTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutKeywordRequestRequestTypeDef",
    "PutOptedOutNumberRequestRequestTypeDef",
    "ReleasePhoneNumberRequestRequestTypeDef",
    "SendTextMessageRequestRequestTypeDef",
    "SendVoiceMessageRequestRequestTypeDef",
    "SetDefaultMessageTypeRequestRequestTypeDef",
    "SetDefaultSenderIdRequestRequestTypeDef",
    "SetTextMessageSpendLimitOverrideRequestRequestTypeDef",
    "SetVoiceMessageSpendLimitOverrideRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePhoneNumberRequestRequestTypeDef",
    "UpdatePoolRequestRequestTypeDef",
    "AssociateOriginationIdentityResultTypeDef",
    "DeleteDefaultMessageTypeResultTypeDef",
    "DeleteDefaultSenderIdResultTypeDef",
    "DeleteKeywordResultTypeDef",
    "DeleteOptOutListResultTypeDef",
    "DeleteOptedOutNumberResultTypeDef",
    "DeletePoolResultTypeDef",
    "DeleteTextMessageSpendLimitOverrideResultTypeDef",
    "DeleteVoiceMessageSpendLimitOverrideResultTypeDef",
    "DescribeAccountAttributesResultTypeDef",
    "DescribeAccountLimitsResultTypeDef",
    "DisassociateOriginationIdentityResultTypeDef",
    "PutKeywordResultTypeDef",
    "PutOptedOutNumberResultTypeDef",
    "ReleasePhoneNumberResultTypeDef",
    "SendTextMessageResultTypeDef",
    "SendVoiceMessageResultTypeDef",
    "SetDefaultMessageTypeResultTypeDef",
    "SetDefaultSenderIdResultTypeDef",
    "SetTextMessageSpendLimitOverrideResultTypeDef",
    "SetVoiceMessageSpendLimitOverrideResultTypeDef",
    "UpdatePhoneNumberResultTypeDef",
    "UpdatePoolResultTypeDef",
    "DescribeConfigurationSetsRequestRequestTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "CreateConfigurationSetResultTypeDef",
    "CreateOptOutListRequestRequestTypeDef",
    "CreateOptOutListResultTypeDef",
    "CreatePoolRequestRequestTypeDef",
    "CreatePoolResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "RequestPhoneNumberRequestRequestTypeDef",
    "RequestPhoneNumberResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateEventDestinationRequestRequestTypeDef",
    "EventDestinationTypeDef",
    "UpdateEventDestinationRequestRequestTypeDef",
    "DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef",
    "DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef",
    "DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef",
    "DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef",
    "DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef",
    "DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef",
    "DescribeKeywordsRequestRequestTypeDef",
    "DescribeKeywordsResultTypeDef",
    "DescribeOptOutListsResultTypeDef",
    "DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef",
    "DescribeOptedOutNumbersRequestRequestTypeDef",
    "DescribeOptedOutNumbersResultTypeDef",
    "DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef",
    "DescribePhoneNumbersRequestRequestTypeDef",
    "DescribePhoneNumbersResultTypeDef",
    "DescribePoolsRequestDescribePoolsPaginateTypeDef",
    "DescribePoolsRequestRequestTypeDef",
    "DescribePoolsResultTypeDef",
    "DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef",
    "DescribeSenderIdsRequestRequestTypeDef",
    "DescribeSenderIdsResultTypeDef",
    "DescribeSpendLimitsResultTypeDef",
    "ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef",
    "ListPoolOriginationIdentitiesRequestRequestTypeDef",
    "ListPoolOriginationIdentitiesResultTypeDef",
    "ConfigurationSetInformationTypeDef",
    "CreateEventDestinationResultTypeDef",
    "DeleteConfigurationSetResultTypeDef",
    "DeleteEventDestinationResultTypeDef",
    "UpdateEventDestinationResultTypeDef",
    "DescribeConfigurationSetsResultTypeDef",
)

AccountAttributeTypeDef = TypedDict(
    "AccountAttributeTypeDef",
    {
        "Name": Literal["ACCOUNT_TIER"],
        "Value": str,
    },
)

AccountLimitTypeDef = TypedDict(
    "AccountLimitTypeDef",
    {
        "Name": AccountLimitNameType,
        "Used": int,
        "Max": int,
    },
)

_RequiredAssociateOriginationIdentityRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateOriginationIdentityRequestRequestTypeDef",
    {
        "PoolId": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
    },
)
_OptionalAssociateOriginationIdentityRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateOriginationIdentityRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class AssociateOriginationIdentityRequestRequestTypeDef(
    _RequiredAssociateOriginationIdentityRequestRequestTypeDef,
    _OptionalAssociateOriginationIdentityRequestRequestTypeDef,
):
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

CloudWatchLogsDestinationTypeDef = TypedDict(
    "CloudWatchLogsDestinationTypeDef",
    {
        "IamRoleArn": str,
        "LogGroupArn": str,
    },
)

ConfigurationSetFilterTypeDef = TypedDict(
    "ConfigurationSetFilterTypeDef",
    {
        "Name": ConfigurationSetFilterNameType,
        "Values": Sequence[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef",
    {
        "IamRoleArn": str,
        "DeliveryStreamArn": str,
    },
)

SnsDestinationTypeDef = TypedDict(
    "SnsDestinationTypeDef",
    {
        "TopicArn": str,
    },
)

DeleteConfigurationSetRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteDefaultMessageTypeRequestRequestTypeDef = TypedDict(
    "DeleteDefaultMessageTypeRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteDefaultSenderIdRequestRequestTypeDef = TypedDict(
    "DeleteDefaultSenderIdRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteEventDestinationRequestRequestTypeDef = TypedDict(
    "DeleteEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
    },
)

DeleteKeywordRequestRequestTypeDef = TypedDict(
    "DeleteKeywordRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "Keyword": str,
    },
)

DeleteOptOutListRequestRequestTypeDef = TypedDict(
    "DeleteOptOutListRequestRequestTypeDef",
    {
        "OptOutListName": str,
    },
)

DeleteOptedOutNumberRequestRequestTypeDef = TypedDict(
    "DeleteOptedOutNumberRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "OptedOutNumber": str,
    },
)

DeletePoolRequestRequestTypeDef = TypedDict(
    "DeletePoolRequestRequestTypeDef",
    {
        "PoolId": str,
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

DescribeAccountAttributesRequestRequestTypeDef = TypedDict(
    "DescribeAccountAttributesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeAccountLimitsRequestRequestTypeDef = TypedDict(
    "DescribeAccountLimitsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

KeywordFilterTypeDef = TypedDict(
    "KeywordFilterTypeDef",
    {
        "Name": Literal["keyword-action"],
        "Values": Sequence[str],
    },
)

KeywordInformationTypeDef = TypedDict(
    "KeywordInformationTypeDef",
    {
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": KeywordActionType,
    },
)

DescribeOptOutListsRequestRequestTypeDef = TypedDict(
    "DescribeOptOutListsRequestRequestTypeDef",
    {
        "OptOutListNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

OptOutListInformationTypeDef = TypedDict(
    "OptOutListInformationTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "CreatedTimestamp": datetime,
    },
)

OptedOutFilterTypeDef = TypedDict(
    "OptedOutFilterTypeDef",
    {
        "Name": Literal["end-user-opted-out"],
        "Values": Sequence[str],
    },
)

OptedOutNumberInformationTypeDef = TypedDict(
    "OptedOutNumberInformationTypeDef",
    {
        "OptedOutNumber": str,
        "OptedOutTimestamp": datetime,
        "EndUserOptedOut": bool,
    },
)

PhoneNumberFilterTypeDef = TypedDict(
    "PhoneNumberFilterTypeDef",
    {
        "Name": PhoneNumberFilterNameType,
        "Values": Sequence[str],
    },
)

_RequiredPhoneNumberInformationTypeDef = TypedDict(
    "_RequiredPhoneNumberInformationTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": NumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
    },
)
_OptionalPhoneNumberInformationTypeDef = TypedDict(
    "_OptionalPhoneNumberInformationTypeDef",
    {
        "PhoneNumberId": str,
        "TwoWayChannelArn": str,
        "PoolId": str,
    },
    total=False,
)

class PhoneNumberInformationTypeDef(
    _RequiredPhoneNumberInformationTypeDef, _OptionalPhoneNumberInformationTypeDef
):
    pass

PoolFilterTypeDef = TypedDict(
    "PoolFilterTypeDef",
    {
        "Name": PoolFilterNameType,
        "Values": Sequence[str],
    },
)

_RequiredPoolInformationTypeDef = TypedDict(
    "_RequiredPoolInformationTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
    },
)
_OptionalPoolInformationTypeDef = TypedDict(
    "_OptionalPoolInformationTypeDef",
    {
        "TwoWayChannelArn": str,
    },
    total=False,
)

class PoolInformationTypeDef(_RequiredPoolInformationTypeDef, _OptionalPoolInformationTypeDef):
    pass

SenderIdAndCountryTypeDef = TypedDict(
    "SenderIdAndCountryTypeDef",
    {
        "SenderId": str,
        "IsoCountryCode": str,
    },
)

SenderIdFilterTypeDef = TypedDict(
    "SenderIdFilterTypeDef",
    {
        "Name": SenderIdFilterNameType,
        "Values": Sequence[str],
    },
)

SenderIdInformationTypeDef = TypedDict(
    "SenderIdInformationTypeDef",
    {
        "SenderIdArn": str,
        "SenderId": str,
        "IsoCountryCode": str,
        "MessageTypes": List[MessageTypeType],
        "MonthlyLeasingPrice": str,
    },
)

DescribeSpendLimitsRequestRequestTypeDef = TypedDict(
    "DescribeSpendLimitsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SpendLimitTypeDef = TypedDict(
    "SpendLimitTypeDef",
    {
        "Name": SpendLimitNameType,
        "EnforcedLimit": int,
        "MaxLimit": int,
        "Overridden": bool,
    },
)

_RequiredDisassociateOriginationIdentityRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateOriginationIdentityRequestRequestTypeDef",
    {
        "PoolId": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
    },
)
_OptionalDisassociateOriginationIdentityRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateOriginationIdentityRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class DisassociateOriginationIdentityRequestRequestTypeDef(
    _RequiredDisassociateOriginationIdentityRequestRequestTypeDef,
    _OptionalDisassociateOriginationIdentityRequestRequestTypeDef,
):
    pass

PoolOriginationIdentitiesFilterTypeDef = TypedDict(
    "PoolOriginationIdentitiesFilterTypeDef",
    {
        "Name": PoolOriginationIdentitiesFilterNameType,
        "Values": Sequence[str],
    },
)

OriginationIdentityMetadataTypeDef = TypedDict(
    "OriginationIdentityMetadataTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "NumberCapabilities": List[NumberCapabilityType],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredPutKeywordRequestRequestTypeDef = TypedDict(
    "_RequiredPutKeywordRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "Keyword": str,
        "KeywordMessage": str,
    },
)
_OptionalPutKeywordRequestRequestTypeDef = TypedDict(
    "_OptionalPutKeywordRequestRequestTypeDef",
    {
        "KeywordAction": KeywordActionType,
    },
    total=False,
)

class PutKeywordRequestRequestTypeDef(
    _RequiredPutKeywordRequestRequestTypeDef, _OptionalPutKeywordRequestRequestTypeDef
):
    pass

PutOptedOutNumberRequestRequestTypeDef = TypedDict(
    "PutOptedOutNumberRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "OptedOutNumber": str,
    },
)

ReleasePhoneNumberRequestRequestTypeDef = TypedDict(
    "ReleasePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
    },
)

_RequiredSendTextMessageRequestRequestTypeDef = TypedDict(
    "_RequiredSendTextMessageRequestRequestTypeDef",
    {
        "DestinationPhoneNumber": str,
    },
)
_OptionalSendTextMessageRequestRequestTypeDef = TypedDict(
    "_OptionalSendTextMessageRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "MessageBody": str,
        "MessageType": MessageTypeType,
        "Keyword": str,
        "ConfigurationSetName": str,
        "MaxPrice": str,
        "TimeToLive": int,
        "Context": Mapping[str, str],
        "DestinationCountryParameters": Mapping[DestinationCountryParameterKeyType, str],
        "DryRun": bool,
    },
    total=False,
)

class SendTextMessageRequestRequestTypeDef(
    _RequiredSendTextMessageRequestRequestTypeDef, _OptionalSendTextMessageRequestRequestTypeDef
):
    pass

_RequiredSendVoiceMessageRequestRequestTypeDef = TypedDict(
    "_RequiredSendVoiceMessageRequestRequestTypeDef",
    {
        "DestinationPhoneNumber": str,
        "OriginationIdentity": str,
    },
)
_OptionalSendVoiceMessageRequestRequestTypeDef = TypedDict(
    "_OptionalSendVoiceMessageRequestRequestTypeDef",
    {
        "MessageBody": str,
        "MessageBodyTextType": VoiceMessageBodyTextTypeType,
        "VoiceId": VoiceIdType,
        "ConfigurationSetName": str,
        "MaxPricePerMinute": str,
        "TimeToLive": int,
        "Context": Mapping[str, str],
        "DryRun": bool,
    },
    total=False,
)

class SendVoiceMessageRequestRequestTypeDef(
    _RequiredSendVoiceMessageRequestRequestTypeDef, _OptionalSendVoiceMessageRequestRequestTypeDef
):
    pass

SetDefaultMessageTypeRequestRequestTypeDef = TypedDict(
    "SetDefaultMessageTypeRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "MessageType": MessageTypeType,
    },
)

SetDefaultSenderIdRequestRequestTypeDef = TypedDict(
    "SetDefaultSenderIdRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "SenderId": str,
    },
)

SetTextMessageSpendLimitOverrideRequestRequestTypeDef = TypedDict(
    "SetTextMessageSpendLimitOverrideRequestRequestTypeDef",
    {
        "MonthlyLimit": int,
    },
)

SetVoiceMessageSpendLimitOverrideRequestRequestTypeDef = TypedDict(
    "SetVoiceMessageSpendLimitOverrideRequestRequestTypeDef",
    {
        "MonthlyLimit": int,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdatePhoneNumberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
    },
)
_OptionalUpdatePhoneNumberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePhoneNumberRequestRequestTypeDef",
    {
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
    },
    total=False,
)

class UpdatePhoneNumberRequestRequestTypeDef(
    _RequiredUpdatePhoneNumberRequestRequestTypeDef, _OptionalUpdatePhoneNumberRequestRequestTypeDef
):
    pass

_RequiredUpdatePoolRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePoolRequestRequestTypeDef",
    {
        "PoolId": str,
    },
)
_OptionalUpdatePoolRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePoolRequestRequestTypeDef",
    {
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
    },
    total=False,
)

class UpdatePoolRequestRequestTypeDef(
    _RequiredUpdatePoolRequestRequestTypeDef, _OptionalUpdatePoolRequestRequestTypeDef
):
    pass

AssociateOriginationIdentityResultTypeDef = TypedDict(
    "AssociateOriginationIdentityResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDefaultMessageTypeResultTypeDef = TypedDict(
    "DeleteDefaultMessageTypeResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "MessageType": MessageTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDefaultSenderIdResultTypeDef = TypedDict(
    "DeleteDefaultSenderIdResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "SenderId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteKeywordResultTypeDef = TypedDict(
    "DeleteKeywordResultTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": KeywordActionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteOptOutListResultTypeDef = TypedDict(
    "DeleteOptOutListResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteOptedOutNumberResultTypeDef = TypedDict(
    "DeleteOptedOutNumberResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "OptedOutNumber": str,
        "OptedOutTimestamp": datetime,
        "EndUserOptedOut": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePoolResultTypeDef = TypedDict(
    "DeletePoolResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTextMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "DeleteTextMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVoiceMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "DeleteVoiceMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountAttributesResultTypeDef = TypedDict(
    "DescribeAccountAttributesResultTypeDef",
    {
        "AccountAttributes": List[AccountAttributeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountLimitsResultTypeDef = TypedDict(
    "DescribeAccountLimitsResultTypeDef",
    {
        "AccountLimits": List[AccountLimitTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateOriginationIdentityResultTypeDef = TypedDict(
    "DisassociateOriginationIdentityResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutKeywordResultTypeDef = TypedDict(
    "PutKeywordResultTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": KeywordActionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutOptedOutNumberResultTypeDef = TypedDict(
    "PutOptedOutNumberResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "OptedOutNumber": str,
        "OptedOutTimestamp": datetime,
        "EndUserOptedOut": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReleasePhoneNumberResultTypeDef = TypedDict(
    "ReleasePhoneNumberResultTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumberId": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": NumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendTextMessageResultTypeDef = TypedDict(
    "SendTextMessageResultTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendVoiceMessageResultTypeDef = TypedDict(
    "SendVoiceMessageResultTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetDefaultMessageTypeResultTypeDef = TypedDict(
    "SetDefaultMessageTypeResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "MessageType": MessageTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetDefaultSenderIdResultTypeDef = TypedDict(
    "SetDefaultSenderIdResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "SenderId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetTextMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "SetTextMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetVoiceMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "SetVoiceMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePhoneNumberResultTypeDef = TypedDict(
    "UpdatePhoneNumberResultTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumberId": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": NumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePoolResultTypeDef = TypedDict(
    "UpdatePoolResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationSetsRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationSetsRequestRequestTypeDef",
    {
        "ConfigurationSetNames": Sequence[str],
        "Filters": Sequence[ConfigurationSetFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredCreateConfigurationSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalCreateConfigurationSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConfigurationSetRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
    },
    total=False,
)

class CreateConfigurationSetRequestRequestTypeDef(
    _RequiredCreateConfigurationSetRequestRequestTypeDef,
    _OptionalCreateConfigurationSetRequestRequestTypeDef,
):
    pass

CreateConfigurationSetResultTypeDef = TypedDict(
    "CreateConfigurationSetResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateOptOutListRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOptOutListRequestRequestTypeDef",
    {
        "OptOutListName": str,
    },
)
_OptionalCreateOptOutListRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOptOutListRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
    },
    total=False,
)

class CreateOptOutListRequestRequestTypeDef(
    _RequiredCreateOptOutListRequestRequestTypeDef, _OptionalCreateOptOutListRequestRequestTypeDef
):
    pass

CreateOptOutListResultTypeDef = TypedDict(
    "CreateOptOutListResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePoolRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePoolRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
    },
)
_OptionalCreatePoolRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePoolRequestRequestTypeDef",
    {
        "DeletionProtectionEnabled": bool,
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
    },
    total=False,
)

class CreatePoolRequestRequestTypeDef(
    _RequiredCreatePoolRequestRequestTypeDef, _OptionalCreatePoolRequestRequestTypeDef
):
    pass

CreatePoolResultTypeDef = TypedDict(
    "CreatePoolResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRequestPhoneNumberRequestRequestTypeDef = TypedDict(
    "_RequiredRequestPhoneNumberRequestRequestTypeDef",
    {
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": Sequence[NumberCapabilityType],
        "NumberType": RequestableNumberTypeType,
    },
)
_OptionalRequestPhoneNumberRequestRequestTypeDef = TypedDict(
    "_OptionalRequestPhoneNumberRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "PoolId": str,
        "RegistrationId": str,
        "DeletionProtectionEnabled": bool,
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
    },
    total=False,
)

class RequestPhoneNumberRequestRequestTypeDef(
    _RequiredRequestPhoneNumberRequestRequestTypeDef,
    _OptionalRequestPhoneNumberRequestRequestTypeDef,
):
    pass

RequestPhoneNumberResultTypeDef = TypedDict(
    "RequestPhoneNumberResultTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumberId": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": RequestableNumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
        "PoolId": str,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
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

_RequiredCreateEventDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
        "MatchingEventTypes": Sequence[EventTypeType],
    },
)
_OptionalCreateEventDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEventDestinationRequestRequestTypeDef",
    {
        "CloudWatchLogsDestination": CloudWatchLogsDestinationTypeDef,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
        "ClientToken": str,
    },
    total=False,
)

class CreateEventDestinationRequestRequestTypeDef(
    _RequiredCreateEventDestinationRequestRequestTypeDef,
    _OptionalCreateEventDestinationRequestRequestTypeDef,
):
    pass

_RequiredEventDestinationTypeDef = TypedDict(
    "_RequiredEventDestinationTypeDef",
    {
        "EventDestinationName": str,
        "Enabled": bool,
        "MatchingEventTypes": List[EventTypeType],
    },
)
_OptionalEventDestinationTypeDef = TypedDict(
    "_OptionalEventDestinationTypeDef",
    {
        "CloudWatchLogsDestination": CloudWatchLogsDestinationTypeDef,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
    },
    total=False,
)

class EventDestinationTypeDef(_RequiredEventDestinationTypeDef, _OptionalEventDestinationTypeDef):
    pass

_RequiredUpdateEventDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
    },
)
_OptionalUpdateEventDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEventDestinationRequestRequestTypeDef",
    {
        "Enabled": bool,
        "MatchingEventTypes": Sequence[EventTypeType],
        "CloudWatchLogsDestination": CloudWatchLogsDestinationTypeDef,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
    },
    total=False,
)

class UpdateEventDestinationRequestRequestTypeDef(
    _RequiredUpdateEventDestinationRequestRequestTypeDef,
    _OptionalUpdateEventDestinationRequestRequestTypeDef,
):
    pass

DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef = TypedDict(
    "DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef = TypedDict(
    "DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef = TypedDict(
    "DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef",
    {
        "ConfigurationSetNames": Sequence[str],
        "Filters": Sequence[ConfigurationSetFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef = TypedDict(
    "DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef",
    {
        "OptOutListNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef = TypedDict(
    "DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeKeywordsRequestDescribeKeywordsPaginateTypeDef = TypedDict(
    "_RequiredDescribeKeywordsRequestDescribeKeywordsPaginateTypeDef",
    {
        "OriginationIdentity": str,
    },
)
_OptionalDescribeKeywordsRequestDescribeKeywordsPaginateTypeDef = TypedDict(
    "_OptionalDescribeKeywordsRequestDescribeKeywordsPaginateTypeDef",
    {
        "Keywords": Sequence[str],
        "Filters": Sequence[KeywordFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef(
    _RequiredDescribeKeywordsRequestDescribeKeywordsPaginateTypeDef,
    _OptionalDescribeKeywordsRequestDescribeKeywordsPaginateTypeDef,
):
    pass

_RequiredDescribeKeywordsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeKeywordsRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
    },
)
_OptionalDescribeKeywordsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeKeywordsRequestRequestTypeDef",
    {
        "Keywords": Sequence[str],
        "Filters": Sequence[KeywordFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class DescribeKeywordsRequestRequestTypeDef(
    _RequiredDescribeKeywordsRequestRequestTypeDef, _OptionalDescribeKeywordsRequestRequestTypeDef
):
    pass

DescribeKeywordsResultTypeDef = TypedDict(
    "DescribeKeywordsResultTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "Keywords": List[KeywordInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOptOutListsResultTypeDef = TypedDict(
    "DescribeOptOutListsResultTypeDef",
    {
        "OptOutLists": List[OptOutListInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef = TypedDict(
    "_RequiredDescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef",
    {
        "OptOutListName": str,
    },
)
_OptionalDescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef = TypedDict(
    "_OptionalDescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef",
    {
        "OptedOutNumbers": Sequence[str],
        "Filters": Sequence[OptedOutFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef(
    _RequiredDescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef,
    _OptionalDescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef,
):
    pass

_RequiredDescribeOptedOutNumbersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeOptedOutNumbersRequestRequestTypeDef",
    {
        "OptOutListName": str,
    },
)
_OptionalDescribeOptedOutNumbersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeOptedOutNumbersRequestRequestTypeDef",
    {
        "OptedOutNumbers": Sequence[str],
        "Filters": Sequence[OptedOutFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class DescribeOptedOutNumbersRequestRequestTypeDef(
    _RequiredDescribeOptedOutNumbersRequestRequestTypeDef,
    _OptionalDescribeOptedOutNumbersRequestRequestTypeDef,
):
    pass

DescribeOptedOutNumbersResultTypeDef = TypedDict(
    "DescribeOptedOutNumbersResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "OptedOutNumbers": List[OptedOutNumberInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef = TypedDict(
    "DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef",
    {
        "PhoneNumberIds": Sequence[str],
        "Filters": Sequence[PhoneNumberFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribePhoneNumbersRequestRequestTypeDef = TypedDict(
    "DescribePhoneNumbersRequestRequestTypeDef",
    {
        "PhoneNumberIds": Sequence[str],
        "Filters": Sequence[PhoneNumberFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribePhoneNumbersResultTypeDef = TypedDict(
    "DescribePhoneNumbersResultTypeDef",
    {
        "PhoneNumbers": List[PhoneNumberInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePoolsRequestDescribePoolsPaginateTypeDef = TypedDict(
    "DescribePoolsRequestDescribePoolsPaginateTypeDef",
    {
        "PoolIds": Sequence[str],
        "Filters": Sequence[PoolFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribePoolsRequestRequestTypeDef = TypedDict(
    "DescribePoolsRequestRequestTypeDef",
    {
        "PoolIds": Sequence[str],
        "Filters": Sequence[PoolFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribePoolsResultTypeDef = TypedDict(
    "DescribePoolsResultTypeDef",
    {
        "Pools": List[PoolInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef = TypedDict(
    "DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef",
    {
        "SenderIds": Sequence[SenderIdAndCountryTypeDef],
        "Filters": Sequence[SenderIdFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSenderIdsRequestRequestTypeDef = TypedDict(
    "DescribeSenderIdsRequestRequestTypeDef",
    {
        "SenderIds": Sequence[SenderIdAndCountryTypeDef],
        "Filters": Sequence[SenderIdFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeSenderIdsResultTypeDef = TypedDict(
    "DescribeSenderIdsResultTypeDef",
    {
        "SenderIds": List[SenderIdInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSpendLimitsResultTypeDef = TypedDict(
    "DescribeSpendLimitsResultTypeDef",
    {
        "SpendLimits": List[SpendLimitTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef = (
    TypedDict(
        "_RequiredListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef",
        {
            "PoolId": str,
        },
    )
)
_OptionalListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef = (
    TypedDict(
        "_OptionalListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef",
        {
            "Filters": Sequence[PoolOriginationIdentitiesFilterTypeDef],
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

class ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef(
    _RequiredListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef,
    _OptionalListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef,
):
    pass

_RequiredListPoolOriginationIdentitiesRequestRequestTypeDef = TypedDict(
    "_RequiredListPoolOriginationIdentitiesRequestRequestTypeDef",
    {
        "PoolId": str,
    },
)
_OptionalListPoolOriginationIdentitiesRequestRequestTypeDef = TypedDict(
    "_OptionalListPoolOriginationIdentitiesRequestRequestTypeDef",
    {
        "Filters": Sequence[PoolOriginationIdentitiesFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPoolOriginationIdentitiesRequestRequestTypeDef(
    _RequiredListPoolOriginationIdentitiesRequestRequestTypeDef,
    _OptionalListPoolOriginationIdentitiesRequestRequestTypeDef,
):
    pass

ListPoolOriginationIdentitiesResultTypeDef = TypedDict(
    "ListPoolOriginationIdentitiesResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "OriginationIdentities": List[OriginationIdentityMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredConfigurationSetInformationTypeDef = TypedDict(
    "_RequiredConfigurationSetInformationTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestinations": List[EventDestinationTypeDef],
        "CreatedTimestamp": datetime,
    },
)
_OptionalConfigurationSetInformationTypeDef = TypedDict(
    "_OptionalConfigurationSetInformationTypeDef",
    {
        "DefaultMessageType": MessageTypeType,
        "DefaultSenderId": str,
    },
    total=False,
)

class ConfigurationSetInformationTypeDef(
    _RequiredConfigurationSetInformationTypeDef, _OptionalConfigurationSetInformationTypeDef
):
    pass

CreateEventDestinationResultTypeDef = TypedDict(
    "CreateEventDestinationResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteConfigurationSetResultTypeDef = TypedDict(
    "DeleteConfigurationSetResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestinations": List[EventDestinationTypeDef],
        "DefaultMessageType": MessageTypeType,
        "DefaultSenderId": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEventDestinationResultTypeDef = TypedDict(
    "DeleteEventDestinationResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEventDestinationResultTypeDef = TypedDict(
    "UpdateEventDestinationResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationSetsResultTypeDef = TypedDict(
    "DescribeConfigurationSetsResultTypeDef",
    {
        "ConfigurationSets": List[ConfigurationSetInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
