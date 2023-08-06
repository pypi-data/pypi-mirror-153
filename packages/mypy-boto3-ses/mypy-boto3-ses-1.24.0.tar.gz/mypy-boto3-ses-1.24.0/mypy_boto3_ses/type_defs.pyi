"""
Type annotations for ses service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ses/type_defs/)

Usage::

    ```python
    from mypy_boto3_ses.type_defs import AddHeaderActionTypeDef

    data: AddHeaderActionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BehaviorOnMXFailureType,
    BounceTypeType,
    BulkEmailStatusType,
    ConfigurationSetAttributeType,
    CustomMailFromStatusType,
    DimensionValueSourceType,
    DsnActionType,
    EventTypeType,
    IdentityTypeType,
    InvocationTypeType,
    NotificationTypeType,
    ReceiptFilterPolicyType,
    SNSActionEncodingType,
    TlsPolicyType,
    VerificationStatusType,
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
    "AddHeaderActionTypeDef",
    "ContentTypeDef",
    "BounceActionTypeDef",
    "BulkEmailDestinationStatusTypeDef",
    "DestinationTypeDef",
    "MessageTagTypeDef",
    "CloneReceiptRuleSetRequestRequestTypeDef",
    "CloudWatchDimensionConfigurationTypeDef",
    "ConfigurationSetTypeDef",
    "TrackingOptionsTypeDef",
    "CreateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "CreateReceiptRuleSetRequestRequestTypeDef",
    "TemplateTypeDef",
    "CustomVerificationEmailTemplateTypeDef",
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "DeleteCustomVerificationEmailTemplateRequestRequestTypeDef",
    "DeleteIdentityPolicyRequestRequestTypeDef",
    "DeleteIdentityRequestRequestTypeDef",
    "DeleteReceiptFilterRequestRequestTypeDef",
    "DeleteReceiptRuleRequestRequestTypeDef",
    "DeleteReceiptRuleSetRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteVerifiedEmailAddressRequestRequestTypeDef",
    "DeliveryOptionsTypeDef",
    "ReceiptRuleSetMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeConfigurationSetRequestRequestTypeDef",
    "ReputationOptionsTypeDef",
    "DescribeReceiptRuleRequestRequestTypeDef",
    "DescribeReceiptRuleSetRequestRequestTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "SNSDestinationTypeDef",
    "ExtensionFieldTypeDef",
    "GetCustomVerificationEmailTemplateRequestRequestTypeDef",
    "GetIdentityDkimAttributesRequestRequestTypeDef",
    "IdentityDkimAttributesTypeDef",
    "GetIdentityMailFromDomainAttributesRequestRequestTypeDef",
    "IdentityMailFromDomainAttributesTypeDef",
    "GetIdentityNotificationAttributesRequestRequestTypeDef",
    "IdentityNotificationAttributesTypeDef",
    "GetIdentityPoliciesRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetIdentityVerificationAttributesRequestRequestTypeDef",
    "IdentityVerificationAttributesTypeDef",
    "SendDataPointTypeDef",
    "GetTemplateRequestRequestTypeDef",
    "LambdaActionTypeDef",
    "PaginatorConfigTypeDef",
    "ListConfigurationSetsRequestRequestTypeDef",
    "ListCustomVerificationEmailTemplatesRequestRequestTypeDef",
    "ListIdentitiesRequestRequestTypeDef",
    "ListIdentityPoliciesRequestRequestTypeDef",
    "ListReceiptRuleSetsRequestRequestTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "TemplateMetadataTypeDef",
    "PutIdentityPolicyRequestRequestTypeDef",
    "RawMessageTypeDef",
    "S3ActionTypeDef",
    "SNSActionTypeDef",
    "StopActionTypeDef",
    "WorkmailActionTypeDef",
    "ReceiptIpFilterTypeDef",
    "ReorderReceiptRuleSetRequestRequestTypeDef",
    "SendCustomVerificationEmailRequestRequestTypeDef",
    "SetActiveReceiptRuleSetRequestRequestTypeDef",
    "SetIdentityDkimEnabledRequestRequestTypeDef",
    "SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef",
    "SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef",
    "SetIdentityMailFromDomainRequestRequestTypeDef",
    "SetIdentityNotificationTopicRequestRequestTypeDef",
    "SetReceiptRulePositionRequestRequestTypeDef",
    "TestRenderTemplateRequestRequestTypeDef",
    "UpdateAccountSendingEnabledRequestRequestTypeDef",
    "UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef",
    "UpdateConfigurationSetSendingEnabledRequestRequestTypeDef",
    "UpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "VerifyDomainDkimRequestRequestTypeDef",
    "VerifyDomainIdentityRequestRequestTypeDef",
    "VerifyEmailAddressRequestRequestTypeDef",
    "VerifyEmailIdentityRequestRequestTypeDef",
    "BodyTypeDef",
    "BulkEmailDestinationTypeDef",
    "SendTemplatedEmailRequestRequestTypeDef",
    "CloudWatchDestinationTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "CreateConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "PutConfigurationSetDeliveryOptionsRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAccountSendingEnabledResponseTypeDef",
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    "GetIdentityPoliciesResponseTypeDef",
    "GetSendQuotaResponseTypeDef",
    "GetTemplateResponseTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    "ListIdentitiesResponseTypeDef",
    "ListIdentityPoliciesResponseTypeDef",
    "ListReceiptRuleSetsResponseTypeDef",
    "ListVerifiedEmailAddressesResponseTypeDef",
    "SendBounceResponseTypeDef",
    "SendBulkTemplatedEmailResponseTypeDef",
    "SendCustomVerificationEmailResponseTypeDef",
    "SendEmailResponseTypeDef",
    "SendRawEmailResponseTypeDef",
    "SendTemplatedEmailResponseTypeDef",
    "TestRenderTemplateResponseTypeDef",
    "VerifyDomainDkimResponseTypeDef",
    "VerifyDomainIdentityResponseTypeDef",
    "MessageDsnTypeDef",
    "RecipientDsnFieldsTypeDef",
    "GetIdentityDkimAttributesResponseTypeDef",
    "GetIdentityMailFromDomainAttributesResponseTypeDef",
    "GetIdentityNotificationAttributesResponseTypeDef",
    "GetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef",
    "GetIdentityVerificationAttributesResponseTypeDef",
    "GetSendStatisticsResponseTypeDef",
    "ListConfigurationSetsRequestListConfigurationSetsPaginateTypeDef",
    "ListCustomVerificationEmailTemplatesRequestListCustomVerificationEmailTemplatesPaginateTypeDef",
    "ListIdentitiesRequestListIdentitiesPaginateTypeDef",
    "ListReceiptRuleSetsRequestListReceiptRuleSetsPaginateTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListTemplatesResponseTypeDef",
    "SendRawEmailRequestRequestTypeDef",
    "ReceiptActionTypeDef",
    "ReceiptFilterTypeDef",
    "MessageTypeDef",
    "SendBulkTemplatedEmailRequestRequestTypeDef",
    "EventDestinationTypeDef",
    "BouncedRecipientInfoTypeDef",
    "ReceiptRuleTypeDef",
    "CreateReceiptFilterRequestRequestTypeDef",
    "ListReceiptFiltersResponseTypeDef",
    "SendEmailRequestRequestTypeDef",
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    "DescribeConfigurationSetResponseTypeDef",
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    "SendBounceRequestRequestTypeDef",
    "CreateReceiptRuleRequestRequestTypeDef",
    "DescribeActiveReceiptRuleSetResponseTypeDef",
    "DescribeReceiptRuleResponseTypeDef",
    "DescribeReceiptRuleSetResponseTypeDef",
    "UpdateReceiptRuleRequestRequestTypeDef",
)

AddHeaderActionTypeDef = TypedDict(
    "AddHeaderActionTypeDef",
    {
        "HeaderName": str,
        "HeaderValue": str,
    },
)

_RequiredContentTypeDef = TypedDict(
    "_RequiredContentTypeDef",
    {
        "Data": str,
    },
)
_OptionalContentTypeDef = TypedDict(
    "_OptionalContentTypeDef",
    {
        "Charset": str,
    },
    total=False,
)

class ContentTypeDef(_RequiredContentTypeDef, _OptionalContentTypeDef):
    pass

_RequiredBounceActionTypeDef = TypedDict(
    "_RequiredBounceActionTypeDef",
    {
        "SmtpReplyCode": str,
        "Message": str,
        "Sender": str,
    },
)
_OptionalBounceActionTypeDef = TypedDict(
    "_OptionalBounceActionTypeDef",
    {
        "TopicArn": str,
        "StatusCode": str,
    },
    total=False,
)

class BounceActionTypeDef(_RequiredBounceActionTypeDef, _OptionalBounceActionTypeDef):
    pass

BulkEmailDestinationStatusTypeDef = TypedDict(
    "BulkEmailDestinationStatusTypeDef",
    {
        "Status": BulkEmailStatusType,
        "Error": str,
        "MessageId": str,
    },
    total=False,
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "ToAddresses": Sequence[str],
        "CcAddresses": Sequence[str],
        "BccAddresses": Sequence[str],
    },
    total=False,
)

MessageTagTypeDef = TypedDict(
    "MessageTagTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

CloneReceiptRuleSetRequestRequestTypeDef = TypedDict(
    "CloneReceiptRuleSetRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "OriginalRuleSetName": str,
    },
)

CloudWatchDimensionConfigurationTypeDef = TypedDict(
    "CloudWatchDimensionConfigurationTypeDef",
    {
        "DimensionName": str,
        "DimensionValueSource": DimensionValueSourceType,
        "DefaultDimensionValue": str,
    },
)

ConfigurationSetTypeDef = TypedDict(
    "ConfigurationSetTypeDef",
    {
        "Name": str,
    },
)

TrackingOptionsTypeDef = TypedDict(
    "TrackingOptionsTypeDef",
    {
        "CustomRedirectDomain": str,
    },
    total=False,
)

CreateCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "CreateCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "TemplateContent": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
)

CreateReceiptRuleSetRequestRequestTypeDef = TypedDict(
    "CreateReceiptRuleSetRequestRequestTypeDef",
    {
        "RuleSetName": str,
    },
)

_RequiredTemplateTypeDef = TypedDict(
    "_RequiredTemplateTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalTemplateTypeDef = TypedDict(
    "_OptionalTemplateTypeDef",
    {
        "SubjectPart": str,
        "TextPart": str,
        "HtmlPart": str,
    },
    total=False,
)

class TemplateTypeDef(_RequiredTemplateTypeDef, _OptionalTemplateTypeDef):
    pass

CustomVerificationEmailTemplateTypeDef = TypedDict(
    "CustomVerificationEmailTemplateTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
    total=False,
)

DeleteConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
    },
)

DeleteConfigurationSetRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "DeleteCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

DeleteIdentityPolicyRequestRequestTypeDef = TypedDict(
    "DeleteIdentityPolicyRequestRequestTypeDef",
    {
        "Identity": str,
        "PolicyName": str,
    },
)

DeleteIdentityRequestRequestTypeDef = TypedDict(
    "DeleteIdentityRequestRequestTypeDef",
    {
        "Identity": str,
    },
)

DeleteReceiptFilterRequestRequestTypeDef = TypedDict(
    "DeleteReceiptFilterRequestRequestTypeDef",
    {
        "FilterName": str,
    },
)

DeleteReceiptRuleRequestRequestTypeDef = TypedDict(
    "DeleteReceiptRuleRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "RuleName": str,
    },
)

DeleteReceiptRuleSetRequestRequestTypeDef = TypedDict(
    "DeleteReceiptRuleSetRequestRequestTypeDef",
    {
        "RuleSetName": str,
    },
)

DeleteTemplateRequestRequestTypeDef = TypedDict(
    "DeleteTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

DeleteVerifiedEmailAddressRequestRequestTypeDef = TypedDict(
    "DeleteVerifiedEmailAddressRequestRequestTypeDef",
    {
        "EmailAddress": str,
    },
)

DeliveryOptionsTypeDef = TypedDict(
    "DeliveryOptionsTypeDef",
    {
        "TlsPolicy": TlsPolicyType,
    },
    total=False,
)

ReceiptRuleSetMetadataTypeDef = TypedDict(
    "ReceiptRuleSetMetadataTypeDef",
    {
        "Name": str,
        "CreatedTimestamp": datetime,
    },
    total=False,
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

_RequiredDescribeConfigurationSetRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalDescribeConfigurationSetRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetAttributeNames": Sequence[ConfigurationSetAttributeType],
    },
    total=False,
)

class DescribeConfigurationSetRequestRequestTypeDef(
    _RequiredDescribeConfigurationSetRequestRequestTypeDef,
    _OptionalDescribeConfigurationSetRequestRequestTypeDef,
):
    pass

ReputationOptionsTypeDef = TypedDict(
    "ReputationOptionsTypeDef",
    {
        "SendingEnabled": bool,
        "ReputationMetricsEnabled": bool,
        "LastFreshStart": datetime,
    },
    total=False,
)

DescribeReceiptRuleRequestRequestTypeDef = TypedDict(
    "DescribeReceiptRuleRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "RuleName": str,
    },
)

DescribeReceiptRuleSetRequestRequestTypeDef = TypedDict(
    "DescribeReceiptRuleSetRequestRequestTypeDef",
    {
        "RuleSetName": str,
    },
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef",
    {
        "IAMRoleARN": str,
        "DeliveryStreamARN": str,
    },
)

SNSDestinationTypeDef = TypedDict(
    "SNSDestinationTypeDef",
    {
        "TopicARN": str,
    },
)

ExtensionFieldTypeDef = TypedDict(
    "ExtensionFieldTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

GetCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "GetCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

GetIdentityDkimAttributesRequestRequestTypeDef = TypedDict(
    "GetIdentityDkimAttributesRequestRequestTypeDef",
    {
        "Identities": Sequence[str],
    },
)

_RequiredIdentityDkimAttributesTypeDef = TypedDict(
    "_RequiredIdentityDkimAttributesTypeDef",
    {
        "DkimEnabled": bool,
        "DkimVerificationStatus": VerificationStatusType,
    },
)
_OptionalIdentityDkimAttributesTypeDef = TypedDict(
    "_OptionalIdentityDkimAttributesTypeDef",
    {
        "DkimTokens": List[str],
    },
    total=False,
)

class IdentityDkimAttributesTypeDef(
    _RequiredIdentityDkimAttributesTypeDef, _OptionalIdentityDkimAttributesTypeDef
):
    pass

GetIdentityMailFromDomainAttributesRequestRequestTypeDef = TypedDict(
    "GetIdentityMailFromDomainAttributesRequestRequestTypeDef",
    {
        "Identities": Sequence[str],
    },
)

IdentityMailFromDomainAttributesTypeDef = TypedDict(
    "IdentityMailFromDomainAttributesTypeDef",
    {
        "MailFromDomain": str,
        "MailFromDomainStatus": CustomMailFromStatusType,
        "BehaviorOnMXFailure": BehaviorOnMXFailureType,
    },
)

GetIdentityNotificationAttributesRequestRequestTypeDef = TypedDict(
    "GetIdentityNotificationAttributesRequestRequestTypeDef",
    {
        "Identities": Sequence[str],
    },
)

_RequiredIdentityNotificationAttributesTypeDef = TypedDict(
    "_RequiredIdentityNotificationAttributesTypeDef",
    {
        "BounceTopic": str,
        "ComplaintTopic": str,
        "DeliveryTopic": str,
        "ForwardingEnabled": bool,
    },
)
_OptionalIdentityNotificationAttributesTypeDef = TypedDict(
    "_OptionalIdentityNotificationAttributesTypeDef",
    {
        "HeadersInBounceNotificationsEnabled": bool,
        "HeadersInComplaintNotificationsEnabled": bool,
        "HeadersInDeliveryNotificationsEnabled": bool,
    },
    total=False,
)

class IdentityNotificationAttributesTypeDef(
    _RequiredIdentityNotificationAttributesTypeDef, _OptionalIdentityNotificationAttributesTypeDef
):
    pass

GetIdentityPoliciesRequestRequestTypeDef = TypedDict(
    "GetIdentityPoliciesRequestRequestTypeDef",
    {
        "Identity": str,
        "PolicyNames": Sequence[str],
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

GetIdentityVerificationAttributesRequestRequestTypeDef = TypedDict(
    "GetIdentityVerificationAttributesRequestRequestTypeDef",
    {
        "Identities": Sequence[str],
    },
)

_RequiredIdentityVerificationAttributesTypeDef = TypedDict(
    "_RequiredIdentityVerificationAttributesTypeDef",
    {
        "VerificationStatus": VerificationStatusType,
    },
)
_OptionalIdentityVerificationAttributesTypeDef = TypedDict(
    "_OptionalIdentityVerificationAttributesTypeDef",
    {
        "VerificationToken": str,
    },
    total=False,
)

class IdentityVerificationAttributesTypeDef(
    _RequiredIdentityVerificationAttributesTypeDef, _OptionalIdentityVerificationAttributesTypeDef
):
    pass

SendDataPointTypeDef = TypedDict(
    "SendDataPointTypeDef",
    {
        "Timestamp": datetime,
        "DeliveryAttempts": int,
        "Bounces": int,
        "Complaints": int,
        "Rejects": int,
    },
    total=False,
)

GetTemplateRequestRequestTypeDef = TypedDict(
    "GetTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

_RequiredLambdaActionTypeDef = TypedDict(
    "_RequiredLambdaActionTypeDef",
    {
        "FunctionArn": str,
    },
)
_OptionalLambdaActionTypeDef = TypedDict(
    "_OptionalLambdaActionTypeDef",
    {
        "TopicArn": str,
        "InvocationType": InvocationTypeType,
    },
    total=False,
)

class LambdaActionTypeDef(_RequiredLambdaActionTypeDef, _OptionalLambdaActionTypeDef):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListConfigurationSetsRequestRequestTypeDef = TypedDict(
    "ListConfigurationSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxItems": int,
    },
    total=False,
)

ListCustomVerificationEmailTemplatesRequestRequestTypeDef = TypedDict(
    "ListCustomVerificationEmailTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListIdentitiesRequestRequestTypeDef = TypedDict(
    "ListIdentitiesRequestRequestTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "NextToken": str,
        "MaxItems": int,
    },
    total=False,
)

ListIdentityPoliciesRequestRequestTypeDef = TypedDict(
    "ListIdentityPoliciesRequestRequestTypeDef",
    {
        "Identity": str,
    },
)

ListReceiptRuleSetsRequestRequestTypeDef = TypedDict(
    "ListReceiptRuleSetsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListTemplatesRequestRequestTypeDef = TypedDict(
    "ListTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxItems": int,
    },
    total=False,
)

TemplateMetadataTypeDef = TypedDict(
    "TemplateMetadataTypeDef",
    {
        "Name": str,
        "CreatedTimestamp": datetime,
    },
    total=False,
)

PutIdentityPolicyRequestRequestTypeDef = TypedDict(
    "PutIdentityPolicyRequestRequestTypeDef",
    {
        "Identity": str,
        "PolicyName": str,
        "Policy": str,
    },
)

RawMessageTypeDef = TypedDict(
    "RawMessageTypeDef",
    {
        "Data": Union[str, bytes, IO[Any], StreamingBody],
    },
)

_RequiredS3ActionTypeDef = TypedDict(
    "_RequiredS3ActionTypeDef",
    {
        "BucketName": str,
    },
)
_OptionalS3ActionTypeDef = TypedDict(
    "_OptionalS3ActionTypeDef",
    {
        "TopicArn": str,
        "ObjectKeyPrefix": str,
        "KmsKeyArn": str,
    },
    total=False,
)

class S3ActionTypeDef(_RequiredS3ActionTypeDef, _OptionalS3ActionTypeDef):
    pass

_RequiredSNSActionTypeDef = TypedDict(
    "_RequiredSNSActionTypeDef",
    {
        "TopicArn": str,
    },
)
_OptionalSNSActionTypeDef = TypedDict(
    "_OptionalSNSActionTypeDef",
    {
        "Encoding": SNSActionEncodingType,
    },
    total=False,
)

class SNSActionTypeDef(_RequiredSNSActionTypeDef, _OptionalSNSActionTypeDef):
    pass

_RequiredStopActionTypeDef = TypedDict(
    "_RequiredStopActionTypeDef",
    {
        "Scope": Literal["RuleSet"],
    },
)
_OptionalStopActionTypeDef = TypedDict(
    "_OptionalStopActionTypeDef",
    {
        "TopicArn": str,
    },
    total=False,
)

class StopActionTypeDef(_RequiredStopActionTypeDef, _OptionalStopActionTypeDef):
    pass

_RequiredWorkmailActionTypeDef = TypedDict(
    "_RequiredWorkmailActionTypeDef",
    {
        "OrganizationArn": str,
    },
)
_OptionalWorkmailActionTypeDef = TypedDict(
    "_OptionalWorkmailActionTypeDef",
    {
        "TopicArn": str,
    },
    total=False,
)

class WorkmailActionTypeDef(_RequiredWorkmailActionTypeDef, _OptionalWorkmailActionTypeDef):
    pass

ReceiptIpFilterTypeDef = TypedDict(
    "ReceiptIpFilterTypeDef",
    {
        "Policy": ReceiptFilterPolicyType,
        "Cidr": str,
    },
)

ReorderReceiptRuleSetRequestRequestTypeDef = TypedDict(
    "ReorderReceiptRuleSetRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "RuleNames": Sequence[str],
    },
)

_RequiredSendCustomVerificationEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendCustomVerificationEmailRequestRequestTypeDef",
    {
        "EmailAddress": str,
        "TemplateName": str,
    },
)
_OptionalSendCustomVerificationEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendCustomVerificationEmailRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
    total=False,
)

class SendCustomVerificationEmailRequestRequestTypeDef(
    _RequiredSendCustomVerificationEmailRequestRequestTypeDef,
    _OptionalSendCustomVerificationEmailRequestRequestTypeDef,
):
    pass

SetActiveReceiptRuleSetRequestRequestTypeDef = TypedDict(
    "SetActiveReceiptRuleSetRequestRequestTypeDef",
    {
        "RuleSetName": str,
    },
    total=False,
)

SetIdentityDkimEnabledRequestRequestTypeDef = TypedDict(
    "SetIdentityDkimEnabledRequestRequestTypeDef",
    {
        "Identity": str,
        "DkimEnabled": bool,
    },
)

SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef = TypedDict(
    "SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef",
    {
        "Identity": str,
        "ForwardingEnabled": bool,
    },
)

SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef = TypedDict(
    "SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef",
    {
        "Identity": str,
        "NotificationType": NotificationTypeType,
        "Enabled": bool,
    },
)

_RequiredSetIdentityMailFromDomainRequestRequestTypeDef = TypedDict(
    "_RequiredSetIdentityMailFromDomainRequestRequestTypeDef",
    {
        "Identity": str,
    },
)
_OptionalSetIdentityMailFromDomainRequestRequestTypeDef = TypedDict(
    "_OptionalSetIdentityMailFromDomainRequestRequestTypeDef",
    {
        "MailFromDomain": str,
        "BehaviorOnMXFailure": BehaviorOnMXFailureType,
    },
    total=False,
)

class SetIdentityMailFromDomainRequestRequestTypeDef(
    _RequiredSetIdentityMailFromDomainRequestRequestTypeDef,
    _OptionalSetIdentityMailFromDomainRequestRequestTypeDef,
):
    pass

_RequiredSetIdentityNotificationTopicRequestRequestTypeDef = TypedDict(
    "_RequiredSetIdentityNotificationTopicRequestRequestTypeDef",
    {
        "Identity": str,
        "NotificationType": NotificationTypeType,
    },
)
_OptionalSetIdentityNotificationTopicRequestRequestTypeDef = TypedDict(
    "_OptionalSetIdentityNotificationTopicRequestRequestTypeDef",
    {
        "SnsTopic": str,
    },
    total=False,
)

class SetIdentityNotificationTopicRequestRequestTypeDef(
    _RequiredSetIdentityNotificationTopicRequestRequestTypeDef,
    _OptionalSetIdentityNotificationTopicRequestRequestTypeDef,
):
    pass

_RequiredSetReceiptRulePositionRequestRequestTypeDef = TypedDict(
    "_RequiredSetReceiptRulePositionRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "RuleName": str,
    },
)
_OptionalSetReceiptRulePositionRequestRequestTypeDef = TypedDict(
    "_OptionalSetReceiptRulePositionRequestRequestTypeDef",
    {
        "After": str,
    },
    total=False,
)

class SetReceiptRulePositionRequestRequestTypeDef(
    _RequiredSetReceiptRulePositionRequestRequestTypeDef,
    _OptionalSetReceiptRulePositionRequestRequestTypeDef,
):
    pass

TestRenderTemplateRequestRequestTypeDef = TypedDict(
    "TestRenderTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "TemplateData": str,
    },
)

UpdateAccountSendingEnabledRequestRequestTypeDef = TypedDict(
    "UpdateAccountSendingEnabledRequestRequestTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "Enabled": bool,
    },
)

UpdateConfigurationSetSendingEnabledRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationSetSendingEnabledRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "Enabled": bool,
    },
)

_RequiredUpdateCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalUpdateCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "TemplateContent": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
    total=False,
)

class UpdateCustomVerificationEmailTemplateRequestRequestTypeDef(
    _RequiredUpdateCustomVerificationEmailTemplateRequestRequestTypeDef,
    _OptionalUpdateCustomVerificationEmailTemplateRequestRequestTypeDef,
):
    pass

VerifyDomainDkimRequestRequestTypeDef = TypedDict(
    "VerifyDomainDkimRequestRequestTypeDef",
    {
        "Domain": str,
    },
)

VerifyDomainIdentityRequestRequestTypeDef = TypedDict(
    "VerifyDomainIdentityRequestRequestTypeDef",
    {
        "Domain": str,
    },
)

VerifyEmailAddressRequestRequestTypeDef = TypedDict(
    "VerifyEmailAddressRequestRequestTypeDef",
    {
        "EmailAddress": str,
    },
)

VerifyEmailIdentityRequestRequestTypeDef = TypedDict(
    "VerifyEmailIdentityRequestRequestTypeDef",
    {
        "EmailAddress": str,
    },
)

BodyTypeDef = TypedDict(
    "BodyTypeDef",
    {
        "Text": ContentTypeDef,
        "Html": ContentTypeDef,
    },
    total=False,
)

_RequiredBulkEmailDestinationTypeDef = TypedDict(
    "_RequiredBulkEmailDestinationTypeDef",
    {
        "Destination": DestinationTypeDef,
    },
)
_OptionalBulkEmailDestinationTypeDef = TypedDict(
    "_OptionalBulkEmailDestinationTypeDef",
    {
        "ReplacementTags": Sequence[MessageTagTypeDef],
        "ReplacementTemplateData": str,
    },
    total=False,
)

class BulkEmailDestinationTypeDef(
    _RequiredBulkEmailDestinationTypeDef, _OptionalBulkEmailDestinationTypeDef
):
    pass

_RequiredSendTemplatedEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendTemplatedEmailRequestRequestTypeDef",
    {
        "Source": str,
        "Destination": DestinationTypeDef,
        "Template": str,
        "TemplateData": str,
    },
)
_OptionalSendTemplatedEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendTemplatedEmailRequestRequestTypeDef",
    {
        "ReplyToAddresses": Sequence[str],
        "ReturnPath": str,
        "SourceArn": str,
        "ReturnPathArn": str,
        "Tags": Sequence[MessageTagTypeDef],
        "ConfigurationSetName": str,
        "TemplateArn": str,
    },
    total=False,
)

class SendTemplatedEmailRequestRequestTypeDef(
    _RequiredSendTemplatedEmailRequestRequestTypeDef,
    _OptionalSendTemplatedEmailRequestRequestTypeDef,
):
    pass

CloudWatchDestinationTypeDef = TypedDict(
    "CloudWatchDestinationTypeDef",
    {
        "DimensionConfigurations": Sequence[CloudWatchDimensionConfigurationTypeDef],
    },
)

CreateConfigurationSetRequestRequestTypeDef = TypedDict(
    "CreateConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSet": ConfigurationSetTypeDef,
    },
)

CreateConfigurationSetTrackingOptionsRequestRequestTypeDef = TypedDict(
    "CreateConfigurationSetTrackingOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "TrackingOptions": TrackingOptionsTypeDef,
    },
)

UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "TrackingOptions": TrackingOptionsTypeDef,
    },
)

CreateTemplateRequestRequestTypeDef = TypedDict(
    "CreateTemplateRequestRequestTypeDef",
    {
        "Template": TemplateTypeDef,
    },
)

UpdateTemplateRequestRequestTypeDef = TypedDict(
    "UpdateTemplateRequestRequestTypeDef",
    {
        "Template": TemplateTypeDef,
    },
)

_RequiredPutConfigurationSetDeliveryOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredPutConfigurationSetDeliveryOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalPutConfigurationSetDeliveryOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalPutConfigurationSetDeliveryOptionsRequestRequestTypeDef",
    {
        "DeliveryOptions": DeliveryOptionsTypeDef,
    },
    total=False,
)

class PutConfigurationSetDeliveryOptionsRequestRequestTypeDef(
    _RequiredPutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
    _OptionalPutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
):
    pass

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountSendingEnabledResponseTypeDef = TypedDict(
    "GetAccountSendingEnabledResponseTypeDef",
    {
        "Enabled": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCustomVerificationEmailTemplateResponseTypeDef = TypedDict(
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "TemplateContent": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIdentityPoliciesResponseTypeDef = TypedDict(
    "GetIdentityPoliciesResponseTypeDef",
    {
        "Policies": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSendQuotaResponseTypeDef = TypedDict(
    "GetSendQuotaResponseTypeDef",
    {
        "Max24HourSend": float,
        "MaxSendRate": float,
        "SentLast24Hours": float,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTemplateResponseTypeDef = TypedDict(
    "GetTemplateResponseTypeDef",
    {
        "Template": TemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationSetsResponseTypeDef = TypedDict(
    "ListConfigurationSetsResponseTypeDef",
    {
        "ConfigurationSets": List[ConfigurationSetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomVerificationEmailTemplatesResponseTypeDef = TypedDict(
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    {
        "CustomVerificationEmailTemplates": List[CustomVerificationEmailTemplateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIdentitiesResponseTypeDef = TypedDict(
    "ListIdentitiesResponseTypeDef",
    {
        "Identities": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIdentityPoliciesResponseTypeDef = TypedDict(
    "ListIdentityPoliciesResponseTypeDef",
    {
        "PolicyNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReceiptRuleSetsResponseTypeDef = TypedDict(
    "ListReceiptRuleSetsResponseTypeDef",
    {
        "RuleSets": List[ReceiptRuleSetMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVerifiedEmailAddressesResponseTypeDef = TypedDict(
    "ListVerifiedEmailAddressesResponseTypeDef",
    {
        "VerifiedEmailAddresses": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendBounceResponseTypeDef = TypedDict(
    "SendBounceResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendBulkTemplatedEmailResponseTypeDef = TypedDict(
    "SendBulkTemplatedEmailResponseTypeDef",
    {
        "Status": List[BulkEmailDestinationStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendCustomVerificationEmailResponseTypeDef = TypedDict(
    "SendCustomVerificationEmailResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendEmailResponseTypeDef = TypedDict(
    "SendEmailResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendRawEmailResponseTypeDef = TypedDict(
    "SendRawEmailResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendTemplatedEmailResponseTypeDef = TypedDict(
    "SendTemplatedEmailResponseTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestRenderTemplateResponseTypeDef = TypedDict(
    "TestRenderTemplateResponseTypeDef",
    {
        "RenderedTemplate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyDomainDkimResponseTypeDef = TypedDict(
    "VerifyDomainDkimResponseTypeDef",
    {
        "DkimTokens": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyDomainIdentityResponseTypeDef = TypedDict(
    "VerifyDomainIdentityResponseTypeDef",
    {
        "VerificationToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMessageDsnTypeDef = TypedDict(
    "_RequiredMessageDsnTypeDef",
    {
        "ReportingMta": str,
    },
)
_OptionalMessageDsnTypeDef = TypedDict(
    "_OptionalMessageDsnTypeDef",
    {
        "ArrivalDate": Union[datetime, str],
        "ExtensionFields": Sequence[ExtensionFieldTypeDef],
    },
    total=False,
)

class MessageDsnTypeDef(_RequiredMessageDsnTypeDef, _OptionalMessageDsnTypeDef):
    pass

_RequiredRecipientDsnFieldsTypeDef = TypedDict(
    "_RequiredRecipientDsnFieldsTypeDef",
    {
        "Action": DsnActionType,
        "Status": str,
    },
)
_OptionalRecipientDsnFieldsTypeDef = TypedDict(
    "_OptionalRecipientDsnFieldsTypeDef",
    {
        "FinalRecipient": str,
        "RemoteMta": str,
        "DiagnosticCode": str,
        "LastAttemptDate": Union[datetime, str],
        "ExtensionFields": Sequence[ExtensionFieldTypeDef],
    },
    total=False,
)

class RecipientDsnFieldsTypeDef(
    _RequiredRecipientDsnFieldsTypeDef, _OptionalRecipientDsnFieldsTypeDef
):
    pass

GetIdentityDkimAttributesResponseTypeDef = TypedDict(
    "GetIdentityDkimAttributesResponseTypeDef",
    {
        "DkimAttributes": Dict[str, IdentityDkimAttributesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIdentityMailFromDomainAttributesResponseTypeDef = TypedDict(
    "GetIdentityMailFromDomainAttributesResponseTypeDef",
    {
        "MailFromDomainAttributes": Dict[str, IdentityMailFromDomainAttributesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIdentityNotificationAttributesResponseTypeDef = TypedDict(
    "GetIdentityNotificationAttributesResponseTypeDef",
    {
        "NotificationAttributes": Dict[str, IdentityNotificationAttributesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef = TypedDict(
    "_RequiredGetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef",
    {
        "Identities": Sequence[str],
    },
)
_OptionalGetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef = TypedDict(
    "_OptionalGetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef(
    _RequiredGetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef,
    _OptionalGetIdentityVerificationAttributesRequestIdentityExistsWaitTypeDef,
):
    pass

GetIdentityVerificationAttributesResponseTypeDef = TypedDict(
    "GetIdentityVerificationAttributesResponseTypeDef",
    {
        "VerificationAttributes": Dict[str, IdentityVerificationAttributesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSendStatisticsResponseTypeDef = TypedDict(
    "GetSendStatisticsResponseTypeDef",
    {
        "SendDataPoints": List[SendDataPointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationSetsRequestListConfigurationSetsPaginateTypeDef = TypedDict(
    "ListConfigurationSetsRequestListConfigurationSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCustomVerificationEmailTemplatesRequestListCustomVerificationEmailTemplatesPaginateTypeDef = TypedDict(
    "ListCustomVerificationEmailTemplatesRequestListCustomVerificationEmailTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListIdentitiesRequestListIdentitiesPaginateTypeDef = TypedDict(
    "ListIdentitiesRequestListIdentitiesPaginateTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListReceiptRuleSetsRequestListReceiptRuleSetsPaginateTypeDef = TypedDict(
    "ListReceiptRuleSetsRequestListReceiptRuleSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "TemplatesMetadata": List[TemplateMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSendRawEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendRawEmailRequestRequestTypeDef",
    {
        "RawMessage": RawMessageTypeDef,
    },
)
_OptionalSendRawEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendRawEmailRequestRequestTypeDef",
    {
        "Source": str,
        "Destinations": Sequence[str],
        "FromArn": str,
        "SourceArn": str,
        "ReturnPathArn": str,
        "Tags": Sequence[MessageTagTypeDef],
        "ConfigurationSetName": str,
    },
    total=False,
)

class SendRawEmailRequestRequestTypeDef(
    _RequiredSendRawEmailRequestRequestTypeDef, _OptionalSendRawEmailRequestRequestTypeDef
):
    pass

ReceiptActionTypeDef = TypedDict(
    "ReceiptActionTypeDef",
    {
        "S3Action": S3ActionTypeDef,
        "BounceAction": BounceActionTypeDef,
        "WorkmailAction": WorkmailActionTypeDef,
        "LambdaAction": LambdaActionTypeDef,
        "StopAction": StopActionTypeDef,
        "AddHeaderAction": AddHeaderActionTypeDef,
        "SNSAction": SNSActionTypeDef,
    },
    total=False,
)

ReceiptFilterTypeDef = TypedDict(
    "ReceiptFilterTypeDef",
    {
        "Name": str,
        "IpFilter": ReceiptIpFilterTypeDef,
    },
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "Subject": ContentTypeDef,
        "Body": BodyTypeDef,
    },
)

_RequiredSendBulkTemplatedEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendBulkTemplatedEmailRequestRequestTypeDef",
    {
        "Source": str,
        "Template": str,
        "Destinations": Sequence[BulkEmailDestinationTypeDef],
    },
)
_OptionalSendBulkTemplatedEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendBulkTemplatedEmailRequestRequestTypeDef",
    {
        "SourceArn": str,
        "ReplyToAddresses": Sequence[str],
        "ReturnPath": str,
        "ReturnPathArn": str,
        "ConfigurationSetName": str,
        "DefaultTags": Sequence[MessageTagTypeDef],
        "TemplateArn": str,
        "DefaultTemplateData": str,
    },
    total=False,
)

class SendBulkTemplatedEmailRequestRequestTypeDef(
    _RequiredSendBulkTemplatedEmailRequestRequestTypeDef,
    _OptionalSendBulkTemplatedEmailRequestRequestTypeDef,
):
    pass

_RequiredEventDestinationTypeDef = TypedDict(
    "_RequiredEventDestinationTypeDef",
    {
        "Name": str,
        "MatchingEventTypes": Sequence[EventTypeType],
    },
)
_OptionalEventDestinationTypeDef = TypedDict(
    "_OptionalEventDestinationTypeDef",
    {
        "Enabled": bool,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "CloudWatchDestination": CloudWatchDestinationTypeDef,
        "SNSDestination": SNSDestinationTypeDef,
    },
    total=False,
)

class EventDestinationTypeDef(_RequiredEventDestinationTypeDef, _OptionalEventDestinationTypeDef):
    pass

_RequiredBouncedRecipientInfoTypeDef = TypedDict(
    "_RequiredBouncedRecipientInfoTypeDef",
    {
        "Recipient": str,
    },
)
_OptionalBouncedRecipientInfoTypeDef = TypedDict(
    "_OptionalBouncedRecipientInfoTypeDef",
    {
        "RecipientArn": str,
        "BounceType": BounceTypeType,
        "RecipientDsnFields": RecipientDsnFieldsTypeDef,
    },
    total=False,
)

class BouncedRecipientInfoTypeDef(
    _RequiredBouncedRecipientInfoTypeDef, _OptionalBouncedRecipientInfoTypeDef
):
    pass

_RequiredReceiptRuleTypeDef = TypedDict(
    "_RequiredReceiptRuleTypeDef",
    {
        "Name": str,
    },
)
_OptionalReceiptRuleTypeDef = TypedDict(
    "_OptionalReceiptRuleTypeDef",
    {
        "Enabled": bool,
        "TlsPolicy": TlsPolicyType,
        "Recipients": Sequence[str],
        "Actions": Sequence[ReceiptActionTypeDef],
        "ScanEnabled": bool,
    },
    total=False,
)

class ReceiptRuleTypeDef(_RequiredReceiptRuleTypeDef, _OptionalReceiptRuleTypeDef):
    pass

CreateReceiptFilterRequestRequestTypeDef = TypedDict(
    "CreateReceiptFilterRequestRequestTypeDef",
    {
        "Filter": ReceiptFilterTypeDef,
    },
)

ListReceiptFiltersResponseTypeDef = TypedDict(
    "ListReceiptFiltersResponseTypeDef",
    {
        "Filters": List[ReceiptFilterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSendEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendEmailRequestRequestTypeDef",
    {
        "Source": str,
        "Destination": DestinationTypeDef,
        "Message": MessageTypeDef,
    },
)
_OptionalSendEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendEmailRequestRequestTypeDef",
    {
        "ReplyToAddresses": Sequence[str],
        "ReturnPath": str,
        "SourceArn": str,
        "ReturnPathArn": str,
        "Tags": Sequence[MessageTagTypeDef],
        "ConfigurationSetName": str,
    },
    total=False,
)

class SendEmailRequestRequestTypeDef(
    _RequiredSendEmailRequestRequestTypeDef, _OptionalSendEmailRequestRequestTypeDef
):
    pass

CreateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
    },
)

DescribeConfigurationSetResponseTypeDef = TypedDict(
    "DescribeConfigurationSetResponseTypeDef",
    {
        "ConfigurationSet": ConfigurationSetTypeDef,
        "EventDestinations": List[EventDestinationTypeDef],
        "TrackingOptions": TrackingOptionsTypeDef,
        "DeliveryOptions": DeliveryOptionsTypeDef,
        "ReputationOptions": ReputationOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
    },
)

_RequiredSendBounceRequestRequestTypeDef = TypedDict(
    "_RequiredSendBounceRequestRequestTypeDef",
    {
        "OriginalMessageId": str,
        "BounceSender": str,
        "BouncedRecipientInfoList": Sequence[BouncedRecipientInfoTypeDef],
    },
)
_OptionalSendBounceRequestRequestTypeDef = TypedDict(
    "_OptionalSendBounceRequestRequestTypeDef",
    {
        "Explanation": str,
        "MessageDsn": MessageDsnTypeDef,
        "BounceSenderArn": str,
    },
    total=False,
)

class SendBounceRequestRequestTypeDef(
    _RequiredSendBounceRequestRequestTypeDef, _OptionalSendBounceRequestRequestTypeDef
):
    pass

_RequiredCreateReceiptRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReceiptRuleRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "Rule": ReceiptRuleTypeDef,
    },
)
_OptionalCreateReceiptRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReceiptRuleRequestRequestTypeDef",
    {
        "After": str,
    },
    total=False,
)

class CreateReceiptRuleRequestRequestTypeDef(
    _RequiredCreateReceiptRuleRequestRequestTypeDef, _OptionalCreateReceiptRuleRequestRequestTypeDef
):
    pass

DescribeActiveReceiptRuleSetResponseTypeDef = TypedDict(
    "DescribeActiveReceiptRuleSetResponseTypeDef",
    {
        "Metadata": ReceiptRuleSetMetadataTypeDef,
        "Rules": List[ReceiptRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeReceiptRuleResponseTypeDef = TypedDict(
    "DescribeReceiptRuleResponseTypeDef",
    {
        "Rule": ReceiptRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeReceiptRuleSetResponseTypeDef = TypedDict(
    "DescribeReceiptRuleSetResponseTypeDef",
    {
        "Metadata": ReceiptRuleSetMetadataTypeDef,
        "Rules": List[ReceiptRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateReceiptRuleRequestRequestTypeDef = TypedDict(
    "UpdateReceiptRuleRequestRequestTypeDef",
    {
        "RuleSetName": str,
        "Rule": ReceiptRuleTypeDef,
    },
)
