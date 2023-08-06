"""
Type annotations for sesv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_sesv2.type_defs import ReviewDetailsTypeDef

    data: ReviewDetailsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BehaviorOnMxFailureType,
    BulkEmailStatusType,
    ContactLanguageType,
    ContactListImportActionType,
    DataFormatType,
    DeliverabilityDashboardAccountStatusType,
    DeliverabilityTestStatusType,
    DimensionValueSourceType,
    DkimSigningAttributesOriginType,
    DkimSigningKeyLengthType,
    DkimStatusType,
    EventTypeType,
    IdentityTypeType,
    ImportDestinationTypeType,
    JobStatusType,
    MailFromDomainStatusType,
    MailTypeType,
    ReviewStatusType,
    SubscriptionStatusType,
    SuppressionListImportActionType,
    SuppressionListReasonType,
    TlsPolicyType,
    WarmupStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ReviewDetailsTypeDef",
    "BlacklistEntryTypeDef",
    "ContentTypeDef",
    "TemplateTypeDef",
    "BulkEmailEntryResultTypeDef",
    "DestinationTypeDef",
    "MessageTagTypeDef",
    "CloudWatchDimensionConfigurationTypeDef",
    "ContactListDestinationTypeDef",
    "ContactListTypeDef",
    "TopicPreferenceTypeDef",
    "DeliveryOptionsTypeDef",
    "ReputationOptionsTypeDef",
    "SendingOptionsTypeDef",
    "SuppressionOptionsTypeDef",
    "TagTypeDef",
    "TrackingOptionsTypeDef",
    "TopicTypeDef",
    "CreateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateEmailIdentityPolicyRequestRequestTypeDef",
    "DkimSigningAttributesTypeDef",
    "DkimAttributesTypeDef",
    "EmailTemplateContentTypeDef",
    "ImportDataSourceTypeDef",
    "CustomVerificationEmailTemplateMetadataTypeDef",
    "DomainIspPlacementTypeDef",
    "VolumeStatisticsTypeDef",
    "DedicatedIpTypeDef",
    "DeleteConfigurationSetEventDestinationRequestRequestTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "DeleteContactListRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DeleteCustomVerificationEmailTemplateRequestRequestTypeDef",
    "DeleteDedicatedIpPoolRequestRequestTypeDef",
    "DeleteEmailIdentityPolicyRequestRequestTypeDef",
    "DeleteEmailIdentityRequestRequestTypeDef",
    "DeleteEmailTemplateRequestRequestTypeDef",
    "DeleteSuppressedDestinationRequestRequestTypeDef",
    "DeliverabilityTestReportTypeDef",
    "DomainDeliverabilityCampaignTypeDef",
    "InboxPlacementTrackingOptionTypeDef",
    "RawMessageTypeDef",
    "EmailTemplateMetadataTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "PinpointDestinationTypeDef",
    "SnsDestinationTypeDef",
    "FailureInfoTypeDef",
    "SendQuotaTypeDef",
    "SuppressionAttributesTypeDef",
    "GetBlacklistReportsRequestRequestTypeDef",
    "GetConfigurationSetEventDestinationsRequestRequestTypeDef",
    "GetConfigurationSetRequestRequestTypeDef",
    "GetContactListRequestRequestTypeDef",
    "GetContactRequestRequestTypeDef",
    "GetCustomVerificationEmailTemplateRequestRequestTypeDef",
    "GetDedicatedIpRequestRequestTypeDef",
    "GetDedicatedIpsRequestRequestTypeDef",
    "GetDeliverabilityTestReportRequestRequestTypeDef",
    "PlacementStatisticsTypeDef",
    "GetDomainDeliverabilityCampaignRequestRequestTypeDef",
    "GetDomainStatisticsReportRequestRequestTypeDef",
    "GetEmailIdentityPoliciesRequestRequestTypeDef",
    "GetEmailIdentityRequestRequestTypeDef",
    "MailFromAttributesTypeDef",
    "GetEmailTemplateRequestRequestTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetSuppressedDestinationRequestRequestTypeDef",
    "IdentityInfoTypeDef",
    "SuppressionListDestinationTypeDef",
    "ListConfigurationSetsRequestRequestTypeDef",
    "ListContactListsRequestRequestTypeDef",
    "TopicFilterTypeDef",
    "ListCustomVerificationEmailTemplatesRequestRequestTypeDef",
    "ListDedicatedIpPoolsRequestRequestTypeDef",
    "ListDeliverabilityTestReportsRequestRequestTypeDef",
    "ListDomainDeliverabilityCampaignsRequestRequestTypeDef",
    "ListEmailIdentitiesRequestRequestTypeDef",
    "ListEmailTemplatesRequestRequestTypeDef",
    "ListImportJobsRequestRequestTypeDef",
    "ListManagementOptionsTypeDef",
    "ListSuppressedDestinationsRequestRequestTypeDef",
    "SuppressedDestinationSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef",
    "PutAccountDetailsRequestRequestTypeDef",
    "PutAccountSendingAttributesRequestRequestTypeDef",
    "PutAccountSuppressionAttributesRequestRequestTypeDef",
    "PutConfigurationSetDeliveryOptionsRequestRequestTypeDef",
    "PutConfigurationSetReputationOptionsRequestRequestTypeDef",
    "PutConfigurationSetSendingOptionsRequestRequestTypeDef",
    "PutConfigurationSetSuppressionOptionsRequestRequestTypeDef",
    "PutConfigurationSetTrackingOptionsRequestRequestTypeDef",
    "PutDedicatedIpInPoolRequestRequestTypeDef",
    "PutDedicatedIpWarmupAttributesRequestRequestTypeDef",
    "PutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef",
    "PutEmailIdentityDkimAttributesRequestRequestTypeDef",
    "PutEmailIdentityFeedbackAttributesRequestRequestTypeDef",
    "PutEmailIdentityMailFromAttributesRequestRequestTypeDef",
    "PutSuppressedDestinationRequestRequestTypeDef",
    "ReplacementTemplateTypeDef",
    "SendCustomVerificationEmailRequestRequestTypeDef",
    "SuppressedDestinationAttributesTypeDef",
    "TestRenderEmailTemplateRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    "UpdateEmailIdentityPolicyRequestRequestTypeDef",
    "AccountDetailsTypeDef",
    "BodyTypeDef",
    "BulkEmailContentTypeDef",
    "CloudWatchDestinationTypeDef",
    "ContactTypeDef",
    "CreateContactRequestRequestTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "CreateDedicatedIpPoolRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "CreateContactListRequestRequestTypeDef",
    "UpdateContactListRequestRequestTypeDef",
    "CreateDeliverabilityTestReportResponseTypeDef",
    "CreateImportJobResponseTypeDef",
    "GetBlacklistReportsResponseTypeDef",
    "GetConfigurationSetResponseTypeDef",
    "GetContactListResponseTypeDef",
    "GetContactResponseTypeDef",
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    "GetEmailIdentityPoliciesResponseTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "ListContactListsResponseTypeDef",
    "ListDedicatedIpPoolsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutEmailIdentityDkimSigningAttributesResponseTypeDef",
    "SendBulkEmailResponseTypeDef",
    "SendCustomVerificationEmailResponseTypeDef",
    "SendEmailResponseTypeDef",
    "TestRenderEmailTemplateResponseTypeDef",
    "CreateEmailIdentityRequestRequestTypeDef",
    "PutEmailIdentityDkimSigningAttributesRequestRequestTypeDef",
    "CreateEmailIdentityResponseTypeDef",
    "CreateEmailTemplateRequestRequestTypeDef",
    "GetEmailTemplateResponseTypeDef",
    "UpdateEmailTemplateRequestRequestTypeDef",
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    "DailyVolumeTypeDef",
    "OverallVolumeTypeDef",
    "GetDedicatedIpResponseTypeDef",
    "GetDedicatedIpsResponseTypeDef",
    "ListDeliverabilityTestReportsResponseTypeDef",
    "GetDomainDeliverabilityCampaignResponseTypeDef",
    "ListDomainDeliverabilityCampaignsResponseTypeDef",
    "DomainDeliverabilityTrackingOptionTypeDef",
    "ListEmailTemplatesResponseTypeDef",
    "IspPlacementTypeDef",
    "GetEmailIdentityResponseTypeDef",
    "ListEmailIdentitiesResponseTypeDef",
    "ImportDestinationTypeDef",
    "ListContactsFilterTypeDef",
    "ListSuppressedDestinationsResponseTypeDef",
    "ReplacementEmailContentTypeDef",
    "SuppressedDestinationTypeDef",
    "GetAccountResponseTypeDef",
    "MessageTypeDef",
    "EventDestinationDefinitionTypeDef",
    "EventDestinationTypeDef",
    "ListContactsResponseTypeDef",
    "GetDomainStatisticsReportResponseTypeDef",
    "GetDeliverabilityDashboardOptionsResponseTypeDef",
    "PutDeliverabilityDashboardOptionRequestRequestTypeDef",
    "GetDeliverabilityTestReportResponseTypeDef",
    "CreateImportJobRequestRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "ImportJobSummaryTypeDef",
    "ListContactsRequestRequestTypeDef",
    "BulkEmailEntryTypeDef",
    "GetSuppressedDestinationResponseTypeDef",
    "EmailContentTypeDef",
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    "ListImportJobsResponseTypeDef",
    "SendBulkEmailRequestRequestTypeDef",
    "CreateDeliverabilityTestReportRequestRequestTypeDef",
    "SendEmailRequestRequestTypeDef",
)

ReviewDetailsTypeDef = TypedDict(
    "ReviewDetailsTypeDef",
    {
        "Status": ReviewStatusType,
        "CaseId": str,
    },
    total=False,
)

BlacklistEntryTypeDef = TypedDict(
    "BlacklistEntryTypeDef",
    {
        "RblName": str,
        "ListingTime": datetime,
        "Description": str,
    },
    total=False,
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


TemplateTypeDef = TypedDict(
    "TemplateTypeDef",
    {
        "TemplateName": str,
        "TemplateArn": str,
        "TemplateData": str,
    },
    total=False,
)

BulkEmailEntryResultTypeDef = TypedDict(
    "BulkEmailEntryResultTypeDef",
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

CloudWatchDimensionConfigurationTypeDef = TypedDict(
    "CloudWatchDimensionConfigurationTypeDef",
    {
        "DimensionName": str,
        "DimensionValueSource": DimensionValueSourceType,
        "DefaultDimensionValue": str,
    },
)

ContactListDestinationTypeDef = TypedDict(
    "ContactListDestinationTypeDef",
    {
        "ContactListName": str,
        "ContactListImportAction": ContactListImportActionType,
    },
)

ContactListTypeDef = TypedDict(
    "ContactListTypeDef",
    {
        "ContactListName": str,
        "LastUpdatedTimestamp": datetime,
    },
    total=False,
)

TopicPreferenceTypeDef = TypedDict(
    "TopicPreferenceTypeDef",
    {
        "TopicName": str,
        "SubscriptionStatus": SubscriptionStatusType,
    },
)

DeliveryOptionsTypeDef = TypedDict(
    "DeliveryOptionsTypeDef",
    {
        "TlsPolicy": TlsPolicyType,
        "SendingPoolName": str,
    },
    total=False,
)

ReputationOptionsTypeDef = TypedDict(
    "ReputationOptionsTypeDef",
    {
        "ReputationMetricsEnabled": bool,
        "LastFreshStart": Union[datetime, str],
    },
    total=False,
)

SendingOptionsTypeDef = TypedDict(
    "SendingOptionsTypeDef",
    {
        "SendingEnabled": bool,
    },
    total=False,
)

SuppressionOptionsTypeDef = TypedDict(
    "SuppressionOptionsTypeDef",
    {
        "SuppressedReasons": Sequence[SuppressionListReasonType],
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

TrackingOptionsTypeDef = TypedDict(
    "TrackingOptionsTypeDef",
    {
        "CustomRedirectDomain": str,
    },
)

_RequiredTopicTypeDef = TypedDict(
    "_RequiredTopicTypeDef",
    {
        "TopicName": str,
        "DisplayName": str,
        "DefaultSubscriptionStatus": SubscriptionStatusType,
    },
)
_OptionalTopicTypeDef = TypedDict(
    "_OptionalTopicTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class TopicTypeDef(_RequiredTopicTypeDef, _OptionalTopicTypeDef):
    pass


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

CreateEmailIdentityPolicyRequestRequestTypeDef = TypedDict(
    "CreateEmailIdentityPolicyRequestRequestTypeDef",
    {
        "EmailIdentity": str,
        "PolicyName": str,
        "Policy": str,
    },
)

DkimSigningAttributesTypeDef = TypedDict(
    "DkimSigningAttributesTypeDef",
    {
        "DomainSigningSelector": str,
        "DomainSigningPrivateKey": str,
        "NextSigningKeyLength": DkimSigningKeyLengthType,
    },
    total=False,
)

DkimAttributesTypeDef = TypedDict(
    "DkimAttributesTypeDef",
    {
        "SigningEnabled": bool,
        "Status": DkimStatusType,
        "Tokens": List[str],
        "SigningAttributesOrigin": DkimSigningAttributesOriginType,
        "NextSigningKeyLength": DkimSigningKeyLengthType,
        "CurrentSigningKeyLength": DkimSigningKeyLengthType,
        "LastKeyGenerationTimestamp": datetime,
    },
    total=False,
)

EmailTemplateContentTypeDef = TypedDict(
    "EmailTemplateContentTypeDef",
    {
        "Subject": str,
        "Text": str,
        "Html": str,
    },
    total=False,
)

ImportDataSourceTypeDef = TypedDict(
    "ImportDataSourceTypeDef",
    {
        "S3Url": str,
        "DataFormat": DataFormatType,
    },
)

CustomVerificationEmailTemplateMetadataTypeDef = TypedDict(
    "CustomVerificationEmailTemplateMetadataTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
    total=False,
)

DomainIspPlacementTypeDef = TypedDict(
    "DomainIspPlacementTypeDef",
    {
        "IspName": str,
        "InboxRawCount": int,
        "SpamRawCount": int,
        "InboxPercentage": float,
        "SpamPercentage": float,
    },
    total=False,
)

VolumeStatisticsTypeDef = TypedDict(
    "VolumeStatisticsTypeDef",
    {
        "InboxRawCount": int,
        "SpamRawCount": int,
        "ProjectedInbox": int,
        "ProjectedSpam": int,
    },
    total=False,
)

_RequiredDedicatedIpTypeDef = TypedDict(
    "_RequiredDedicatedIpTypeDef",
    {
        "Ip": str,
        "WarmupStatus": WarmupStatusType,
        "WarmupPercentage": int,
    },
)
_OptionalDedicatedIpTypeDef = TypedDict(
    "_OptionalDedicatedIpTypeDef",
    {
        "PoolName": str,
    },
    total=False,
)


class DedicatedIpTypeDef(_RequiredDedicatedIpTypeDef, _OptionalDedicatedIpTypeDef):
    pass


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

DeleteContactListRequestRequestTypeDef = TypedDict(
    "DeleteContactListRequestRequestTypeDef",
    {
        "ContactListName": str,
    },
)

DeleteContactRequestRequestTypeDef = TypedDict(
    "DeleteContactRequestRequestTypeDef",
    {
        "ContactListName": str,
        "EmailAddress": str,
    },
)

DeleteCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "DeleteCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

DeleteDedicatedIpPoolRequestRequestTypeDef = TypedDict(
    "DeleteDedicatedIpPoolRequestRequestTypeDef",
    {
        "PoolName": str,
    },
)

DeleteEmailIdentityPolicyRequestRequestTypeDef = TypedDict(
    "DeleteEmailIdentityPolicyRequestRequestTypeDef",
    {
        "EmailIdentity": str,
        "PolicyName": str,
    },
)

DeleteEmailIdentityRequestRequestTypeDef = TypedDict(
    "DeleteEmailIdentityRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)

DeleteEmailTemplateRequestRequestTypeDef = TypedDict(
    "DeleteEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

DeleteSuppressedDestinationRequestRequestTypeDef = TypedDict(
    "DeleteSuppressedDestinationRequestRequestTypeDef",
    {
        "EmailAddress": str,
    },
)

DeliverabilityTestReportTypeDef = TypedDict(
    "DeliverabilityTestReportTypeDef",
    {
        "ReportId": str,
        "ReportName": str,
        "Subject": str,
        "FromEmailAddress": str,
        "CreateDate": datetime,
        "DeliverabilityTestStatus": DeliverabilityTestStatusType,
    },
    total=False,
)

DomainDeliverabilityCampaignTypeDef = TypedDict(
    "DomainDeliverabilityCampaignTypeDef",
    {
        "CampaignId": str,
        "ImageUrl": str,
        "Subject": str,
        "FromAddress": str,
        "SendingIps": List[str],
        "FirstSeenDateTime": datetime,
        "LastSeenDateTime": datetime,
        "InboxCount": int,
        "SpamCount": int,
        "ReadRate": float,
        "DeleteRate": float,
        "ReadDeleteRate": float,
        "ProjectedVolume": int,
        "Esps": List[str],
    },
    total=False,
)

InboxPlacementTrackingOptionTypeDef = TypedDict(
    "InboxPlacementTrackingOptionTypeDef",
    {
        "Global": bool,
        "TrackedIsps": List[str],
    },
    total=False,
)

RawMessageTypeDef = TypedDict(
    "RawMessageTypeDef",
    {
        "Data": Union[str, bytes, IO[Any], StreamingBody],
    },
)

EmailTemplateMetadataTypeDef = TypedDict(
    "EmailTemplateMetadataTypeDef",
    {
        "TemplateName": str,
        "CreatedTimestamp": datetime,
    },
    total=False,
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef",
    {
        "IamRoleArn": str,
        "DeliveryStreamArn": str,
    },
)

PinpointDestinationTypeDef = TypedDict(
    "PinpointDestinationTypeDef",
    {
        "ApplicationArn": str,
    },
    total=False,
)

SnsDestinationTypeDef = TypedDict(
    "SnsDestinationTypeDef",
    {
        "TopicArn": str,
    },
)

FailureInfoTypeDef = TypedDict(
    "FailureInfoTypeDef",
    {
        "FailedRecordsS3Url": str,
        "ErrorMessage": str,
    },
    total=False,
)

SendQuotaTypeDef = TypedDict(
    "SendQuotaTypeDef",
    {
        "Max24HourSend": float,
        "MaxSendRate": float,
        "SentLast24Hours": float,
    },
    total=False,
)

SuppressionAttributesTypeDef = TypedDict(
    "SuppressionAttributesTypeDef",
    {
        "SuppressedReasons": List[SuppressionListReasonType],
    },
    total=False,
)

GetBlacklistReportsRequestRequestTypeDef = TypedDict(
    "GetBlacklistReportsRequestRequestTypeDef",
    {
        "BlacklistItemNames": Sequence[str],
    },
)

GetConfigurationSetEventDestinationsRequestRequestTypeDef = TypedDict(
    "GetConfigurationSetEventDestinationsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

GetConfigurationSetRequestRequestTypeDef = TypedDict(
    "GetConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

GetContactListRequestRequestTypeDef = TypedDict(
    "GetContactListRequestRequestTypeDef",
    {
        "ContactListName": str,
    },
)

GetContactRequestRequestTypeDef = TypedDict(
    "GetContactRequestRequestTypeDef",
    {
        "ContactListName": str,
        "EmailAddress": str,
    },
)

GetCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "GetCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

GetDedicatedIpRequestRequestTypeDef = TypedDict(
    "GetDedicatedIpRequestRequestTypeDef",
    {
        "Ip": str,
    },
)

GetDedicatedIpsRequestRequestTypeDef = TypedDict(
    "GetDedicatedIpsRequestRequestTypeDef",
    {
        "PoolName": str,
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

GetDeliverabilityTestReportRequestRequestTypeDef = TypedDict(
    "GetDeliverabilityTestReportRequestRequestTypeDef",
    {
        "ReportId": str,
    },
)

PlacementStatisticsTypeDef = TypedDict(
    "PlacementStatisticsTypeDef",
    {
        "InboxPercentage": float,
        "SpamPercentage": float,
        "MissingPercentage": float,
        "SpfPercentage": float,
        "DkimPercentage": float,
    },
    total=False,
)

GetDomainDeliverabilityCampaignRequestRequestTypeDef = TypedDict(
    "GetDomainDeliverabilityCampaignRequestRequestTypeDef",
    {
        "CampaignId": str,
    },
)

GetDomainStatisticsReportRequestRequestTypeDef = TypedDict(
    "GetDomainStatisticsReportRequestRequestTypeDef",
    {
        "Domain": str,
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
    },
)

GetEmailIdentityPoliciesRequestRequestTypeDef = TypedDict(
    "GetEmailIdentityPoliciesRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)

GetEmailIdentityRequestRequestTypeDef = TypedDict(
    "GetEmailIdentityRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)

MailFromAttributesTypeDef = TypedDict(
    "MailFromAttributesTypeDef",
    {
        "MailFromDomain": str,
        "MailFromDomainStatus": MailFromDomainStatusType,
        "BehaviorOnMxFailure": BehaviorOnMxFailureType,
    },
)

GetEmailTemplateRequestRequestTypeDef = TypedDict(
    "GetEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)

GetImportJobRequestRequestTypeDef = TypedDict(
    "GetImportJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetSuppressedDestinationRequestRequestTypeDef = TypedDict(
    "GetSuppressedDestinationRequestRequestTypeDef",
    {
        "EmailAddress": str,
    },
)

IdentityInfoTypeDef = TypedDict(
    "IdentityInfoTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "IdentityName": str,
        "SendingEnabled": bool,
    },
    total=False,
)

SuppressionListDestinationTypeDef = TypedDict(
    "SuppressionListDestinationTypeDef",
    {
        "SuppressionListImportAction": SuppressionListImportActionType,
    },
)

ListConfigurationSetsRequestRequestTypeDef = TypedDict(
    "ListConfigurationSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

ListContactListsRequestRequestTypeDef = TypedDict(
    "ListContactListsRequestRequestTypeDef",
    {
        "PageSize": int,
        "NextToken": str,
    },
    total=False,
)

TopicFilterTypeDef = TypedDict(
    "TopicFilterTypeDef",
    {
        "TopicName": str,
        "UseDefaultIfPreferenceUnavailable": bool,
    },
    total=False,
)

ListCustomVerificationEmailTemplatesRequestRequestTypeDef = TypedDict(
    "ListCustomVerificationEmailTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

ListDedicatedIpPoolsRequestRequestTypeDef = TypedDict(
    "ListDedicatedIpPoolsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

ListDeliverabilityTestReportsRequestRequestTypeDef = TypedDict(
    "ListDeliverabilityTestReportsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

_RequiredListDomainDeliverabilityCampaignsRequestRequestTypeDef = TypedDict(
    "_RequiredListDomainDeliverabilityCampaignsRequestRequestTypeDef",
    {
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
        "SubscribedDomain": str,
    },
)
_OptionalListDomainDeliverabilityCampaignsRequestRequestTypeDef = TypedDict(
    "_OptionalListDomainDeliverabilityCampaignsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)


class ListDomainDeliverabilityCampaignsRequestRequestTypeDef(
    _RequiredListDomainDeliverabilityCampaignsRequestRequestTypeDef,
    _OptionalListDomainDeliverabilityCampaignsRequestRequestTypeDef,
):
    pass


ListEmailIdentitiesRequestRequestTypeDef = TypedDict(
    "ListEmailIdentitiesRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

ListEmailTemplatesRequestRequestTypeDef = TypedDict(
    "ListEmailTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

ListImportJobsRequestRequestTypeDef = TypedDict(
    "ListImportJobsRequestRequestTypeDef",
    {
        "ImportDestinationType": ImportDestinationTypeType,
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

_RequiredListManagementOptionsTypeDef = TypedDict(
    "_RequiredListManagementOptionsTypeDef",
    {
        "ContactListName": str,
    },
)
_OptionalListManagementOptionsTypeDef = TypedDict(
    "_OptionalListManagementOptionsTypeDef",
    {
        "TopicName": str,
    },
    total=False,
)


class ListManagementOptionsTypeDef(
    _RequiredListManagementOptionsTypeDef, _OptionalListManagementOptionsTypeDef
):
    pass


ListSuppressedDestinationsRequestRequestTypeDef = TypedDict(
    "ListSuppressedDestinationsRequestRequestTypeDef",
    {
        "Reasons": Sequence[SuppressionListReasonType],
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
        "NextToken": str,
        "PageSize": int,
    },
    total=False,
)

SuppressedDestinationSummaryTypeDef = TypedDict(
    "SuppressedDestinationSummaryTypeDef",
    {
        "EmailAddress": str,
        "Reason": SuppressionListReasonType,
        "LastUpdateTime": datetime,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef = TypedDict(
    "PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef",
    {
        "AutoWarmupEnabled": bool,
    },
    total=False,
)

_RequiredPutAccountDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredPutAccountDetailsRequestRequestTypeDef",
    {
        "MailType": MailTypeType,
        "WebsiteURL": str,
        "UseCaseDescription": str,
    },
)
_OptionalPutAccountDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalPutAccountDetailsRequestRequestTypeDef",
    {
        "ContactLanguage": ContactLanguageType,
        "AdditionalContactEmailAddresses": Sequence[str],
        "ProductionAccessEnabled": bool,
    },
    total=False,
)


class PutAccountDetailsRequestRequestTypeDef(
    _RequiredPutAccountDetailsRequestRequestTypeDef, _OptionalPutAccountDetailsRequestRequestTypeDef
):
    pass


PutAccountSendingAttributesRequestRequestTypeDef = TypedDict(
    "PutAccountSendingAttributesRequestRequestTypeDef",
    {
        "SendingEnabled": bool,
    },
    total=False,
)

PutAccountSuppressionAttributesRequestRequestTypeDef = TypedDict(
    "PutAccountSuppressionAttributesRequestRequestTypeDef",
    {
        "SuppressedReasons": Sequence[SuppressionListReasonType],
    },
    total=False,
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
        "TlsPolicy": TlsPolicyType,
        "SendingPoolName": str,
    },
    total=False,
)


class PutConfigurationSetDeliveryOptionsRequestRequestTypeDef(
    _RequiredPutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
    _OptionalPutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
):
    pass


_RequiredPutConfigurationSetReputationOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredPutConfigurationSetReputationOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalPutConfigurationSetReputationOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalPutConfigurationSetReputationOptionsRequestRequestTypeDef",
    {
        "ReputationMetricsEnabled": bool,
    },
    total=False,
)


class PutConfigurationSetReputationOptionsRequestRequestTypeDef(
    _RequiredPutConfigurationSetReputationOptionsRequestRequestTypeDef,
    _OptionalPutConfigurationSetReputationOptionsRequestRequestTypeDef,
):
    pass


_RequiredPutConfigurationSetSendingOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredPutConfigurationSetSendingOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalPutConfigurationSetSendingOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalPutConfigurationSetSendingOptionsRequestRequestTypeDef",
    {
        "SendingEnabled": bool,
    },
    total=False,
)


class PutConfigurationSetSendingOptionsRequestRequestTypeDef(
    _RequiredPutConfigurationSetSendingOptionsRequestRequestTypeDef,
    _OptionalPutConfigurationSetSendingOptionsRequestRequestTypeDef,
):
    pass


_RequiredPutConfigurationSetSuppressionOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredPutConfigurationSetSuppressionOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalPutConfigurationSetSuppressionOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalPutConfigurationSetSuppressionOptionsRequestRequestTypeDef",
    {
        "SuppressedReasons": Sequence[SuppressionListReasonType],
    },
    total=False,
)


class PutConfigurationSetSuppressionOptionsRequestRequestTypeDef(
    _RequiredPutConfigurationSetSuppressionOptionsRequestRequestTypeDef,
    _OptionalPutConfigurationSetSuppressionOptionsRequestRequestTypeDef,
):
    pass


_RequiredPutConfigurationSetTrackingOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredPutConfigurationSetTrackingOptionsRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)
_OptionalPutConfigurationSetTrackingOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalPutConfigurationSetTrackingOptionsRequestRequestTypeDef",
    {
        "CustomRedirectDomain": str,
    },
    total=False,
)


class PutConfigurationSetTrackingOptionsRequestRequestTypeDef(
    _RequiredPutConfigurationSetTrackingOptionsRequestRequestTypeDef,
    _OptionalPutConfigurationSetTrackingOptionsRequestRequestTypeDef,
):
    pass


PutDedicatedIpInPoolRequestRequestTypeDef = TypedDict(
    "PutDedicatedIpInPoolRequestRequestTypeDef",
    {
        "Ip": str,
        "DestinationPoolName": str,
    },
)

PutDedicatedIpWarmupAttributesRequestRequestTypeDef = TypedDict(
    "PutDedicatedIpWarmupAttributesRequestRequestTypeDef",
    {
        "Ip": str,
        "WarmupPercentage": int,
    },
)

_RequiredPutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)
_OptionalPutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
    total=False,
)


class PutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef(
    _RequiredPutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef,
    _OptionalPutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef,
):
    pass


_RequiredPutEmailIdentityDkimAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutEmailIdentityDkimAttributesRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)
_OptionalPutEmailIdentityDkimAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutEmailIdentityDkimAttributesRequestRequestTypeDef",
    {
        "SigningEnabled": bool,
    },
    total=False,
)


class PutEmailIdentityDkimAttributesRequestRequestTypeDef(
    _RequiredPutEmailIdentityDkimAttributesRequestRequestTypeDef,
    _OptionalPutEmailIdentityDkimAttributesRequestRequestTypeDef,
):
    pass


_RequiredPutEmailIdentityFeedbackAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutEmailIdentityFeedbackAttributesRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)
_OptionalPutEmailIdentityFeedbackAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutEmailIdentityFeedbackAttributesRequestRequestTypeDef",
    {
        "EmailForwardingEnabled": bool,
    },
    total=False,
)


class PutEmailIdentityFeedbackAttributesRequestRequestTypeDef(
    _RequiredPutEmailIdentityFeedbackAttributesRequestRequestTypeDef,
    _OptionalPutEmailIdentityFeedbackAttributesRequestRequestTypeDef,
):
    pass


_RequiredPutEmailIdentityMailFromAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutEmailIdentityMailFromAttributesRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)
_OptionalPutEmailIdentityMailFromAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutEmailIdentityMailFromAttributesRequestRequestTypeDef",
    {
        "MailFromDomain": str,
        "BehaviorOnMxFailure": BehaviorOnMxFailureType,
    },
    total=False,
)


class PutEmailIdentityMailFromAttributesRequestRequestTypeDef(
    _RequiredPutEmailIdentityMailFromAttributesRequestRequestTypeDef,
    _OptionalPutEmailIdentityMailFromAttributesRequestRequestTypeDef,
):
    pass


PutSuppressedDestinationRequestRequestTypeDef = TypedDict(
    "PutSuppressedDestinationRequestRequestTypeDef",
    {
        "EmailAddress": str,
        "Reason": SuppressionListReasonType,
    },
)

ReplacementTemplateTypeDef = TypedDict(
    "ReplacementTemplateTypeDef",
    {
        "ReplacementTemplateData": str,
    },
    total=False,
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


SuppressedDestinationAttributesTypeDef = TypedDict(
    "SuppressedDestinationAttributesTypeDef",
    {
        "MessageId": str,
        "FeedbackId": str,
    },
    total=False,
)

TestRenderEmailTemplateRequestRequestTypeDef = TypedDict(
    "TestRenderEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "TemplateData": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateCustomVerificationEmailTemplateRequestRequestTypeDef = TypedDict(
    "UpdateCustomVerificationEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "TemplateContent": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
)

UpdateEmailIdentityPolicyRequestRequestTypeDef = TypedDict(
    "UpdateEmailIdentityPolicyRequestRequestTypeDef",
    {
        "EmailIdentity": str,
        "PolicyName": str,
        "Policy": str,
    },
)

AccountDetailsTypeDef = TypedDict(
    "AccountDetailsTypeDef",
    {
        "MailType": MailTypeType,
        "WebsiteURL": str,
        "ContactLanguage": ContactLanguageType,
        "UseCaseDescription": str,
        "AdditionalContactEmailAddresses": List[str],
        "ReviewDetails": ReviewDetailsTypeDef,
    },
    total=False,
)

BodyTypeDef = TypedDict(
    "BodyTypeDef",
    {
        "Text": ContentTypeDef,
        "Html": ContentTypeDef,
    },
    total=False,
)

BulkEmailContentTypeDef = TypedDict(
    "BulkEmailContentTypeDef",
    {
        "Template": TemplateTypeDef,
    },
    total=False,
)

CloudWatchDestinationTypeDef = TypedDict(
    "CloudWatchDestinationTypeDef",
    {
        "DimensionConfigurations": Sequence[CloudWatchDimensionConfigurationTypeDef],
    },
)

ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "EmailAddress": str,
        "TopicPreferences": List[TopicPreferenceTypeDef],
        "TopicDefaultPreferences": List[TopicPreferenceTypeDef],
        "UnsubscribeAll": bool,
        "LastUpdatedTimestamp": datetime,
    },
    total=False,
)

_RequiredCreateContactRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactRequestRequestTypeDef",
    {
        "ContactListName": str,
        "EmailAddress": str,
    },
)
_OptionalCreateContactRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactRequestRequestTypeDef",
    {
        "TopicPreferences": Sequence[TopicPreferenceTypeDef],
        "UnsubscribeAll": bool,
        "AttributesData": str,
    },
    total=False,
)


class CreateContactRequestRequestTypeDef(
    _RequiredCreateContactRequestRequestTypeDef, _OptionalCreateContactRequestRequestTypeDef
):
    pass


_RequiredUpdateContactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactRequestRequestTypeDef",
    {
        "ContactListName": str,
        "EmailAddress": str,
    },
)
_OptionalUpdateContactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactRequestRequestTypeDef",
    {
        "TopicPreferences": Sequence[TopicPreferenceTypeDef],
        "UnsubscribeAll": bool,
        "AttributesData": str,
    },
    total=False,
)


class UpdateContactRequestRequestTypeDef(
    _RequiredUpdateContactRequestRequestTypeDef, _OptionalUpdateContactRequestRequestTypeDef
):
    pass


_RequiredCreateDedicatedIpPoolRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDedicatedIpPoolRequestRequestTypeDef",
    {
        "PoolName": str,
    },
)
_OptionalCreateDedicatedIpPoolRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDedicatedIpPoolRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDedicatedIpPoolRequestRequestTypeDef(
    _RequiredCreateDedicatedIpPoolRequestRequestTypeDef,
    _OptionalCreateDedicatedIpPoolRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
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
        "TrackingOptions": TrackingOptionsTypeDef,
        "DeliveryOptions": DeliveryOptionsTypeDef,
        "ReputationOptions": ReputationOptionsTypeDef,
        "SendingOptions": SendingOptionsTypeDef,
        "Tags": Sequence[TagTypeDef],
        "SuppressionOptions": SuppressionOptionsTypeDef,
    },
    total=False,
)


class CreateConfigurationSetRequestRequestTypeDef(
    _RequiredCreateConfigurationSetRequestRequestTypeDef,
    _OptionalCreateConfigurationSetRequestRequestTypeDef,
):
    pass


_RequiredCreateContactListRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactListRequestRequestTypeDef",
    {
        "ContactListName": str,
    },
)
_OptionalCreateContactListRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactListRequestRequestTypeDef",
    {
        "Topics": Sequence[TopicTypeDef],
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateContactListRequestRequestTypeDef(
    _RequiredCreateContactListRequestRequestTypeDef, _OptionalCreateContactListRequestRequestTypeDef
):
    pass


_RequiredUpdateContactListRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactListRequestRequestTypeDef",
    {
        "ContactListName": str,
    },
)
_OptionalUpdateContactListRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactListRequestRequestTypeDef",
    {
        "Topics": Sequence[TopicTypeDef],
        "Description": str,
    },
    total=False,
)


class UpdateContactListRequestRequestTypeDef(
    _RequiredUpdateContactListRequestRequestTypeDef, _OptionalUpdateContactListRequestRequestTypeDef
):
    pass


CreateDeliverabilityTestReportResponseTypeDef = TypedDict(
    "CreateDeliverabilityTestReportResponseTypeDef",
    {
        "ReportId": str,
        "DeliverabilityTestStatus": DeliverabilityTestStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImportJobResponseTypeDef = TypedDict(
    "CreateImportJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBlacklistReportsResponseTypeDef = TypedDict(
    "GetBlacklistReportsResponseTypeDef",
    {
        "BlacklistReport": Dict[str, List[BlacklistEntryTypeDef]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConfigurationSetResponseTypeDef = TypedDict(
    "GetConfigurationSetResponseTypeDef",
    {
        "ConfigurationSetName": str,
        "TrackingOptions": TrackingOptionsTypeDef,
        "DeliveryOptions": DeliveryOptionsTypeDef,
        "ReputationOptions": ReputationOptionsTypeDef,
        "SendingOptions": SendingOptionsTypeDef,
        "Tags": List[TagTypeDef],
        "SuppressionOptions": SuppressionOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactListResponseTypeDef = TypedDict(
    "GetContactListResponseTypeDef",
    {
        "ContactListName": str,
        "Topics": List[TopicTypeDef],
        "Description": str,
        "CreatedTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactResponseTypeDef = TypedDict(
    "GetContactResponseTypeDef",
    {
        "ContactListName": str,
        "EmailAddress": str,
        "TopicPreferences": List[TopicPreferenceTypeDef],
        "TopicDefaultPreferences": List[TopicPreferenceTypeDef],
        "UnsubscribeAll": bool,
        "AttributesData": str,
        "CreatedTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
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

GetEmailIdentityPoliciesResponseTypeDef = TypedDict(
    "GetEmailIdentityPoliciesResponseTypeDef",
    {
        "Policies": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationSetsResponseTypeDef = TypedDict(
    "ListConfigurationSetsResponseTypeDef",
    {
        "ConfigurationSets": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContactListsResponseTypeDef = TypedDict(
    "ListContactListsResponseTypeDef",
    {
        "ContactLists": List[ContactListTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDedicatedIpPoolsResponseTypeDef = TypedDict(
    "ListDedicatedIpPoolsResponseTypeDef",
    {
        "DedicatedIpPools": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutEmailIdentityDkimSigningAttributesResponseTypeDef = TypedDict(
    "PutEmailIdentityDkimSigningAttributesResponseTypeDef",
    {
        "DkimStatus": DkimStatusType,
        "DkimTokens": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendBulkEmailResponseTypeDef = TypedDict(
    "SendBulkEmailResponseTypeDef",
    {
        "BulkEmailEntryResults": List[BulkEmailEntryResultTypeDef],
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

TestRenderEmailTemplateResponseTypeDef = TypedDict(
    "TestRenderEmailTemplateResponseTypeDef",
    {
        "RenderedTemplate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateEmailIdentityRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEmailIdentityRequestRequestTypeDef",
    {
        "EmailIdentity": str,
    },
)
_OptionalCreateEmailIdentityRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEmailIdentityRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "DkimSigningAttributes": DkimSigningAttributesTypeDef,
        "ConfigurationSetName": str,
    },
    total=False,
)


class CreateEmailIdentityRequestRequestTypeDef(
    _RequiredCreateEmailIdentityRequestRequestTypeDef,
    _OptionalCreateEmailIdentityRequestRequestTypeDef,
):
    pass


_RequiredPutEmailIdentityDkimSigningAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutEmailIdentityDkimSigningAttributesRequestRequestTypeDef",
    {
        "EmailIdentity": str,
        "SigningAttributesOrigin": DkimSigningAttributesOriginType,
    },
)
_OptionalPutEmailIdentityDkimSigningAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutEmailIdentityDkimSigningAttributesRequestRequestTypeDef",
    {
        "SigningAttributes": DkimSigningAttributesTypeDef,
    },
    total=False,
)


class PutEmailIdentityDkimSigningAttributesRequestRequestTypeDef(
    _RequiredPutEmailIdentityDkimSigningAttributesRequestRequestTypeDef,
    _OptionalPutEmailIdentityDkimSigningAttributesRequestRequestTypeDef,
):
    pass


CreateEmailIdentityResponseTypeDef = TypedDict(
    "CreateEmailIdentityResponseTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "VerifiedForSendingStatus": bool,
        "DkimAttributes": DkimAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEmailTemplateRequestRequestTypeDef = TypedDict(
    "CreateEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "TemplateContent": EmailTemplateContentTypeDef,
    },
)

GetEmailTemplateResponseTypeDef = TypedDict(
    "GetEmailTemplateResponseTypeDef",
    {
        "TemplateName": str,
        "TemplateContent": EmailTemplateContentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEmailTemplateRequestRequestTypeDef = TypedDict(
    "UpdateEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "TemplateContent": EmailTemplateContentTypeDef,
    },
)

ListCustomVerificationEmailTemplatesResponseTypeDef = TypedDict(
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    {
        "CustomVerificationEmailTemplates": List[CustomVerificationEmailTemplateMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DailyVolumeTypeDef = TypedDict(
    "DailyVolumeTypeDef",
    {
        "StartDate": datetime,
        "VolumeStatistics": VolumeStatisticsTypeDef,
        "DomainIspPlacements": List[DomainIspPlacementTypeDef],
    },
    total=False,
)

OverallVolumeTypeDef = TypedDict(
    "OverallVolumeTypeDef",
    {
        "VolumeStatistics": VolumeStatisticsTypeDef,
        "ReadRatePercent": float,
        "DomainIspPlacements": List[DomainIspPlacementTypeDef],
    },
    total=False,
)

GetDedicatedIpResponseTypeDef = TypedDict(
    "GetDedicatedIpResponseTypeDef",
    {
        "DedicatedIp": DedicatedIpTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDedicatedIpsResponseTypeDef = TypedDict(
    "GetDedicatedIpsResponseTypeDef",
    {
        "DedicatedIps": List[DedicatedIpTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeliverabilityTestReportsResponseTypeDef = TypedDict(
    "ListDeliverabilityTestReportsResponseTypeDef",
    {
        "DeliverabilityTestReports": List[DeliverabilityTestReportTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDomainDeliverabilityCampaignResponseTypeDef = TypedDict(
    "GetDomainDeliverabilityCampaignResponseTypeDef",
    {
        "DomainDeliverabilityCampaign": DomainDeliverabilityCampaignTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainDeliverabilityCampaignsResponseTypeDef = TypedDict(
    "ListDomainDeliverabilityCampaignsResponseTypeDef",
    {
        "DomainDeliverabilityCampaigns": List[DomainDeliverabilityCampaignTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DomainDeliverabilityTrackingOptionTypeDef = TypedDict(
    "DomainDeliverabilityTrackingOptionTypeDef",
    {
        "Domain": str,
        "SubscriptionStartDate": datetime,
        "InboxPlacementTrackingOption": InboxPlacementTrackingOptionTypeDef,
    },
    total=False,
)

ListEmailTemplatesResponseTypeDef = TypedDict(
    "ListEmailTemplatesResponseTypeDef",
    {
        "TemplatesMetadata": List[EmailTemplateMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IspPlacementTypeDef = TypedDict(
    "IspPlacementTypeDef",
    {
        "IspName": str,
        "PlacementStatistics": PlacementStatisticsTypeDef,
    },
    total=False,
)

GetEmailIdentityResponseTypeDef = TypedDict(
    "GetEmailIdentityResponseTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "FeedbackForwardingStatus": bool,
        "VerifiedForSendingStatus": bool,
        "DkimAttributes": DkimAttributesTypeDef,
        "MailFromAttributes": MailFromAttributesTypeDef,
        "Policies": Dict[str, str],
        "Tags": List[TagTypeDef],
        "ConfigurationSetName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEmailIdentitiesResponseTypeDef = TypedDict(
    "ListEmailIdentitiesResponseTypeDef",
    {
        "EmailIdentities": List[IdentityInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportDestinationTypeDef = TypedDict(
    "ImportDestinationTypeDef",
    {
        "SuppressionListDestination": SuppressionListDestinationTypeDef,
        "ContactListDestination": ContactListDestinationTypeDef,
    },
    total=False,
)

ListContactsFilterTypeDef = TypedDict(
    "ListContactsFilterTypeDef",
    {
        "FilteredStatus": SubscriptionStatusType,
        "TopicFilter": TopicFilterTypeDef,
    },
    total=False,
)

ListSuppressedDestinationsResponseTypeDef = TypedDict(
    "ListSuppressedDestinationsResponseTypeDef",
    {
        "SuppressedDestinationSummaries": List[SuppressedDestinationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplacementEmailContentTypeDef = TypedDict(
    "ReplacementEmailContentTypeDef",
    {
        "ReplacementTemplate": ReplacementTemplateTypeDef,
    },
    total=False,
)

_RequiredSuppressedDestinationTypeDef = TypedDict(
    "_RequiredSuppressedDestinationTypeDef",
    {
        "EmailAddress": str,
        "Reason": SuppressionListReasonType,
        "LastUpdateTime": datetime,
    },
)
_OptionalSuppressedDestinationTypeDef = TypedDict(
    "_OptionalSuppressedDestinationTypeDef",
    {
        "Attributes": SuppressedDestinationAttributesTypeDef,
    },
    total=False,
)


class SuppressedDestinationTypeDef(
    _RequiredSuppressedDestinationTypeDef, _OptionalSuppressedDestinationTypeDef
):
    pass


GetAccountResponseTypeDef = TypedDict(
    "GetAccountResponseTypeDef",
    {
        "DedicatedIpAutoWarmupEnabled": bool,
        "EnforcementStatus": str,
        "ProductionAccessEnabled": bool,
        "SendQuota": SendQuotaTypeDef,
        "SendingEnabled": bool,
        "SuppressionAttributes": SuppressionAttributesTypeDef,
        "Details": AccountDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "Subject": ContentTypeDef,
        "Body": BodyTypeDef,
    },
)

EventDestinationDefinitionTypeDef = TypedDict(
    "EventDestinationDefinitionTypeDef",
    {
        "Enabled": bool,
        "MatchingEventTypes": Sequence[EventTypeType],
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "CloudWatchDestination": CloudWatchDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
        "PinpointDestination": PinpointDestinationTypeDef,
    },
    total=False,
)

_RequiredEventDestinationTypeDef = TypedDict(
    "_RequiredEventDestinationTypeDef",
    {
        "Name": str,
        "MatchingEventTypes": List[EventTypeType],
    },
)
_OptionalEventDestinationTypeDef = TypedDict(
    "_OptionalEventDestinationTypeDef",
    {
        "Enabled": bool,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "CloudWatchDestination": CloudWatchDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
        "PinpointDestination": PinpointDestinationTypeDef,
    },
    total=False,
)


class EventDestinationTypeDef(_RequiredEventDestinationTypeDef, _OptionalEventDestinationTypeDef):
    pass


ListContactsResponseTypeDef = TypedDict(
    "ListContactsResponseTypeDef",
    {
        "Contacts": List[ContactTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDomainStatisticsReportResponseTypeDef = TypedDict(
    "GetDomainStatisticsReportResponseTypeDef",
    {
        "OverallVolume": OverallVolumeTypeDef,
        "DailyVolumes": List[DailyVolumeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeliverabilityDashboardOptionsResponseTypeDef = TypedDict(
    "GetDeliverabilityDashboardOptionsResponseTypeDef",
    {
        "DashboardEnabled": bool,
        "SubscriptionExpiryDate": datetime,
        "AccountStatus": DeliverabilityDashboardAccountStatusType,
        "ActiveSubscribedDomains": List[DomainDeliverabilityTrackingOptionTypeDef],
        "PendingExpirationSubscribedDomains": List[DomainDeliverabilityTrackingOptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutDeliverabilityDashboardOptionRequestRequestTypeDef = TypedDict(
    "_RequiredPutDeliverabilityDashboardOptionRequestRequestTypeDef",
    {
        "DashboardEnabled": bool,
    },
)
_OptionalPutDeliverabilityDashboardOptionRequestRequestTypeDef = TypedDict(
    "_OptionalPutDeliverabilityDashboardOptionRequestRequestTypeDef",
    {
        "SubscribedDomains": Sequence[DomainDeliverabilityTrackingOptionTypeDef],
    },
    total=False,
)


class PutDeliverabilityDashboardOptionRequestRequestTypeDef(
    _RequiredPutDeliverabilityDashboardOptionRequestRequestTypeDef,
    _OptionalPutDeliverabilityDashboardOptionRequestRequestTypeDef,
):
    pass


GetDeliverabilityTestReportResponseTypeDef = TypedDict(
    "GetDeliverabilityTestReportResponseTypeDef",
    {
        "DeliverabilityTestReport": DeliverabilityTestReportTypeDef,
        "OverallPlacement": PlacementStatisticsTypeDef,
        "IspPlacements": List[IspPlacementTypeDef],
        "Message": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImportJobRequestRequestTypeDef = TypedDict(
    "CreateImportJobRequestRequestTypeDef",
    {
        "ImportDestination": ImportDestinationTypeDef,
        "ImportDataSource": ImportDataSourceTypeDef,
    },
)

GetImportJobResponseTypeDef = TypedDict(
    "GetImportJobResponseTypeDef",
    {
        "JobId": str,
        "ImportDestination": ImportDestinationTypeDef,
        "ImportDataSource": ImportDataSourceTypeDef,
        "FailureInfo": FailureInfoTypeDef,
        "JobStatus": JobStatusType,
        "CreatedTimestamp": datetime,
        "CompletedTimestamp": datetime,
        "ProcessedRecordsCount": int,
        "FailedRecordsCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportJobSummaryTypeDef = TypedDict(
    "ImportJobSummaryTypeDef",
    {
        "JobId": str,
        "ImportDestination": ImportDestinationTypeDef,
        "JobStatus": JobStatusType,
        "CreatedTimestamp": datetime,
    },
    total=False,
)

_RequiredListContactsRequestRequestTypeDef = TypedDict(
    "_RequiredListContactsRequestRequestTypeDef",
    {
        "ContactListName": str,
    },
)
_OptionalListContactsRequestRequestTypeDef = TypedDict(
    "_OptionalListContactsRequestRequestTypeDef",
    {
        "Filter": ListContactsFilterTypeDef,
        "PageSize": int,
        "NextToken": str,
    },
    total=False,
)


class ListContactsRequestRequestTypeDef(
    _RequiredListContactsRequestRequestTypeDef, _OptionalListContactsRequestRequestTypeDef
):
    pass


_RequiredBulkEmailEntryTypeDef = TypedDict(
    "_RequiredBulkEmailEntryTypeDef",
    {
        "Destination": DestinationTypeDef,
    },
)
_OptionalBulkEmailEntryTypeDef = TypedDict(
    "_OptionalBulkEmailEntryTypeDef",
    {
        "ReplacementTags": Sequence[MessageTagTypeDef],
        "ReplacementEmailContent": ReplacementEmailContentTypeDef,
    },
    total=False,
)


class BulkEmailEntryTypeDef(_RequiredBulkEmailEntryTypeDef, _OptionalBulkEmailEntryTypeDef):
    pass


GetSuppressedDestinationResponseTypeDef = TypedDict(
    "GetSuppressedDestinationResponseTypeDef",
    {
        "SuppressedDestination": SuppressedDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmailContentTypeDef = TypedDict(
    "EmailContentTypeDef",
    {
        "Simple": MessageTypeDef,
        "Raw": RawMessageTypeDef,
        "Template": TemplateTypeDef,
    },
    total=False,
)

CreateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "CreateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
        "EventDestination": EventDestinationDefinitionTypeDef,
    },
)

UpdateConfigurationSetEventDestinationRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationSetEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
        "EventDestination": EventDestinationDefinitionTypeDef,
    },
)

GetConfigurationSetEventDestinationsResponseTypeDef = TypedDict(
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    {
        "EventDestinations": List[EventDestinationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListImportJobsResponseTypeDef = TypedDict(
    "ListImportJobsResponseTypeDef",
    {
        "ImportJobs": List[ImportJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSendBulkEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendBulkEmailRequestRequestTypeDef",
    {
        "DefaultContent": BulkEmailContentTypeDef,
        "BulkEmailEntries": Sequence[BulkEmailEntryTypeDef],
    },
)
_OptionalSendBulkEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendBulkEmailRequestRequestTypeDef",
    {
        "FromEmailAddress": str,
        "FromEmailAddressIdentityArn": str,
        "ReplyToAddresses": Sequence[str],
        "FeedbackForwardingEmailAddress": str,
        "FeedbackForwardingEmailAddressIdentityArn": str,
        "DefaultEmailTags": Sequence[MessageTagTypeDef],
        "ConfigurationSetName": str,
    },
    total=False,
)


class SendBulkEmailRequestRequestTypeDef(
    _RequiredSendBulkEmailRequestRequestTypeDef, _OptionalSendBulkEmailRequestRequestTypeDef
):
    pass


_RequiredCreateDeliverabilityTestReportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeliverabilityTestReportRequestRequestTypeDef",
    {
        "FromEmailAddress": str,
        "Content": EmailContentTypeDef,
    },
)
_OptionalCreateDeliverabilityTestReportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeliverabilityTestReportRequestRequestTypeDef",
    {
        "ReportName": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDeliverabilityTestReportRequestRequestTypeDef(
    _RequiredCreateDeliverabilityTestReportRequestRequestTypeDef,
    _OptionalCreateDeliverabilityTestReportRequestRequestTypeDef,
):
    pass


_RequiredSendEmailRequestRequestTypeDef = TypedDict(
    "_RequiredSendEmailRequestRequestTypeDef",
    {
        "Content": EmailContentTypeDef,
    },
)
_OptionalSendEmailRequestRequestTypeDef = TypedDict(
    "_OptionalSendEmailRequestRequestTypeDef",
    {
        "FromEmailAddress": str,
        "FromEmailAddressIdentityArn": str,
        "Destination": DestinationTypeDef,
        "ReplyToAddresses": Sequence[str],
        "FeedbackForwardingEmailAddress": str,
        "FeedbackForwardingEmailAddressIdentityArn": str,
        "EmailTags": Sequence[MessageTagTypeDef],
        "ConfigurationSetName": str,
        "ListManagementOptions": ListManagementOptionsTypeDef,
    },
    total=False,
)


class SendEmailRequestRequestTypeDef(
    _RequiredSendEmailRequestRequestTypeDef, _OptionalSendEmailRequestRequestTypeDef
):
    pass
