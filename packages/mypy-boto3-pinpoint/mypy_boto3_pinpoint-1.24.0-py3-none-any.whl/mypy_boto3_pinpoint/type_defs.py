"""
Type annotations for pinpoint service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/type_defs/)

Usage::

    ```python
    from mypy_boto3_pinpoint.type_defs import ADMChannelRequestTypeDef

    data: ADMChannelRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ActionType,
    AlignmentType,
    AttributeTypeType,
    ButtonActionType,
    CampaignStatusType,
    ChannelTypeType,
    DeliveryStatusType,
    DimensionTypeType,
    DurationType,
    EndpointTypesElementType,
    FilterTypeType,
    FormatType,
    FrequencyType,
    IncludeType,
    JobStatusType,
    LayoutType,
    MessageTypeType,
    ModeType,
    OperatorType,
    RecencyTypeType,
    SegmentTypeType,
    SourceTypeType,
    StateType,
    TemplateTypeType,
    TypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ADMChannelRequestTypeDef",
    "ADMChannelResponseTypeDef",
    "ADMMessageTypeDef",
    "APNSChannelRequestTypeDef",
    "APNSChannelResponseTypeDef",
    "APNSMessageTypeDef",
    "APNSPushNotificationTemplateTypeDef",
    "APNSSandboxChannelRequestTypeDef",
    "APNSSandboxChannelResponseTypeDef",
    "APNSVoipChannelRequestTypeDef",
    "APNSVoipChannelResponseTypeDef",
    "APNSVoipSandboxChannelRequestTypeDef",
    "APNSVoipSandboxChannelResponseTypeDef",
    "ActivityResponseTypeDef",
    "ContactCenterActivityTypeDef",
    "HoldoutActivityTypeDef",
    "AddressConfigurationTypeDef",
    "AndroidPushNotificationTemplateTypeDef",
    "ApplicationResponseTypeDef",
    "CampaignHookTypeDef",
    "CampaignLimitsTypeDef",
    "QuietTimeTypeDef",
    "AttributeDimensionTypeDef",
    "AttributesResourceTypeDef",
    "BaiduChannelRequestTypeDef",
    "BaiduChannelResponseTypeDef",
    "BaiduMessageTypeDef",
    "CampaignCustomMessageTypeDef",
    "CampaignEmailMessageTypeDef",
    "CampaignStateTypeDef",
    "CustomDeliveryConfigurationTypeDef",
    "CampaignSmsMessageTypeDef",
    "ChannelResponseTypeDef",
    "WaitTimeTypeDef",
    "CreateApplicationRequestTypeDef",
    "ResponseMetadataTypeDef",
    "EmailTemplateRequestTypeDef",
    "CreateTemplateMessageBodyTypeDef",
    "ExportJobRequestTypeDef",
    "ImportJobRequestTypeDef",
    "TemplateCreateMessageBodyTypeDef",
    "CreateRecommenderConfigurationTypeDef",
    "RecommenderConfigurationResponseTypeDef",
    "SMSTemplateRequestTypeDef",
    "VoiceTemplateRequestTypeDef",
    "JourneyCustomMessageTypeDef",
    "DefaultButtonConfigurationTypeDef",
    "DefaultMessageTypeDef",
    "DefaultPushNotificationMessageTypeDef",
    "DefaultPushNotificationTemplateTypeDef",
    "DeleteAdmChannelRequestRequestTypeDef",
    "DeleteApnsChannelRequestRequestTypeDef",
    "DeleteApnsSandboxChannelRequestRequestTypeDef",
    "DeleteApnsVoipChannelRequestRequestTypeDef",
    "DeleteApnsVoipSandboxChannelRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteBaiduChannelRequestRequestTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteEmailChannelRequestRequestTypeDef",
    "EmailChannelResponseTypeDef",
    "DeleteEmailTemplateRequestRequestTypeDef",
    "MessageBodyTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "DeleteEventStreamRequestRequestTypeDef",
    "EventStreamTypeDef",
    "DeleteGcmChannelRequestRequestTypeDef",
    "GCMChannelResponseTypeDef",
    "DeleteInAppTemplateRequestRequestTypeDef",
    "DeleteJourneyRequestRequestTypeDef",
    "DeletePushTemplateRequestRequestTypeDef",
    "DeleteRecommenderConfigurationRequestRequestTypeDef",
    "DeleteSegmentRequestRequestTypeDef",
    "DeleteSmsChannelRequestRequestTypeDef",
    "SMSChannelResponseTypeDef",
    "DeleteSmsTemplateRequestRequestTypeDef",
    "DeleteUserEndpointsRequestRequestTypeDef",
    "DeleteVoiceChannelRequestRequestTypeDef",
    "VoiceChannelResponseTypeDef",
    "DeleteVoiceTemplateRequestRequestTypeDef",
    "GCMMessageTypeDef",
    "SMSMessageTypeDef",
    "VoiceMessageTypeDef",
    "EmailChannelRequestTypeDef",
    "JourneyEmailMessageTypeDef",
    "RawEmailTypeDef",
    "EmailTemplateResponseTypeDef",
    "EndpointDemographicTypeDef",
    "EndpointLocationTypeDef",
    "EndpointUserTypeDef",
    "EndpointItemResponseTypeDef",
    "EndpointMessageResultTypeDef",
    "EndpointSendConfigurationTypeDef",
    "MetricDimensionTypeDef",
    "SetDimensionTypeDef",
    "EventItemResponseTypeDef",
    "SessionTypeDef",
    "ExportJobResourceTypeDef",
    "GCMChannelRequestTypeDef",
    "GPSCoordinatesTypeDef",
    "GetAdmChannelRequestRequestTypeDef",
    "GetApnsChannelRequestRequestTypeDef",
    "GetApnsSandboxChannelRequestRequestTypeDef",
    "GetApnsVoipChannelRequestRequestTypeDef",
    "GetApnsVoipSandboxChannelRequestRequestTypeDef",
    "GetAppRequestRequestTypeDef",
    "GetApplicationDateRangeKpiRequestRequestTypeDef",
    "GetApplicationSettingsRequestRequestTypeDef",
    "GetAppsRequestRequestTypeDef",
    "GetBaiduChannelRequestRequestTypeDef",
    "GetCampaignActivitiesRequestRequestTypeDef",
    "GetCampaignDateRangeKpiRequestRequestTypeDef",
    "GetCampaignRequestRequestTypeDef",
    "GetCampaignVersionRequestRequestTypeDef",
    "GetCampaignVersionsRequestRequestTypeDef",
    "GetCampaignsRequestRequestTypeDef",
    "GetChannelsRequestRequestTypeDef",
    "GetEmailChannelRequestRequestTypeDef",
    "GetEmailTemplateRequestRequestTypeDef",
    "GetEndpointRequestRequestTypeDef",
    "GetEventStreamRequestRequestTypeDef",
    "GetExportJobRequestRequestTypeDef",
    "GetExportJobsRequestRequestTypeDef",
    "GetGcmChannelRequestRequestTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetImportJobsRequestRequestTypeDef",
    "GetInAppMessagesRequestRequestTypeDef",
    "GetInAppTemplateRequestRequestTypeDef",
    "GetJourneyDateRangeKpiRequestRequestTypeDef",
    "GetJourneyExecutionActivityMetricsRequestRequestTypeDef",
    "JourneyExecutionActivityMetricsResponseTypeDef",
    "GetJourneyExecutionMetricsRequestRequestTypeDef",
    "JourneyExecutionMetricsResponseTypeDef",
    "GetJourneyRequestRequestTypeDef",
    "GetPushTemplateRequestRequestTypeDef",
    "GetRecommenderConfigurationRequestRequestTypeDef",
    "GetRecommenderConfigurationsRequestRequestTypeDef",
    "GetSegmentExportJobsRequestRequestTypeDef",
    "GetSegmentImportJobsRequestRequestTypeDef",
    "GetSegmentRequestRequestTypeDef",
    "GetSegmentVersionRequestRequestTypeDef",
    "GetSegmentVersionsRequestRequestTypeDef",
    "GetSegmentsRequestRequestTypeDef",
    "GetSmsChannelRequestRequestTypeDef",
    "GetSmsTemplateRequestRequestTypeDef",
    "SMSTemplateResponseTypeDef",
    "GetUserEndpointsRequestRequestTypeDef",
    "GetVoiceChannelRequestRequestTypeDef",
    "GetVoiceTemplateRequestRequestTypeDef",
    "VoiceTemplateResponseTypeDef",
    "ImportJobResourceTypeDef",
    "InAppMessageBodyConfigTypeDef",
    "OverrideButtonConfigurationTypeDef",
    "InAppMessageHeaderConfigTypeDef",
    "JourneyChannelSettingsTypeDef",
    "JourneyLimitsTypeDef",
    "JourneyPushMessageTypeDef",
    "JourneyScheduleTypeDef",
    "JourneySMSMessageTypeDef",
    "JourneyStateRequestTypeDef",
    "ListJourneysRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagsModelTypeDef",
    "ListTemplateVersionsRequestRequestTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "MessageTypeDef",
    "MessageResultTypeDef",
    "NumberValidateRequestTypeDef",
    "NumberValidateResponseTypeDef",
    "WriteEventStreamTypeDef",
    "RandomSplitEntryTypeDef",
    "RecencyDimensionTypeDef",
    "UpdateAttributesRequestTypeDef",
    "ResultRowValueTypeDef",
    "SMSChannelRequestTypeDef",
    "SegmentConditionTypeDef",
    "SegmentReferenceTypeDef",
    "SegmentImportResourceTypeDef",
    "SendOTPMessageRequestParametersTypeDef",
    "SimpleEmailPartTypeDef",
    "TemplateActiveVersionRequestTypeDef",
    "TemplateTypeDef",
    "TemplateResponseTypeDef",
    "TemplateVersionResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateRecommenderConfigurationTypeDef",
    "VoiceChannelRequestTypeDef",
    "VerificationResponseTypeDef",
    "VerifyOTPMessageRequestParametersTypeDef",
    "UpdateAdmChannelRequestRequestTypeDef",
    "UpdateApnsChannelRequestRequestTypeDef",
    "UpdateApnsSandboxChannelRequestRequestTypeDef",
    "UpdateApnsVoipChannelRequestRequestTypeDef",
    "UpdateApnsVoipSandboxChannelRequestRequestTypeDef",
    "ActivitiesResponseTypeDef",
    "ApplicationsResponseTypeDef",
    "ApplicationSettingsResourceTypeDef",
    "WriteApplicationSettingsRequestTypeDef",
    "UpdateBaiduChannelRequestRequestTypeDef",
    "ChannelsResponseTypeDef",
    "WaitActivityTypeDef",
    "CreateAppRequestRequestTypeDef",
    "CreateAppResponseTypeDef",
    "DeleteAdmChannelResponseTypeDef",
    "DeleteApnsChannelResponseTypeDef",
    "DeleteApnsSandboxChannelResponseTypeDef",
    "DeleteApnsVoipChannelResponseTypeDef",
    "DeleteApnsVoipSandboxChannelResponseTypeDef",
    "DeleteAppResponseTypeDef",
    "DeleteBaiduChannelResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAdmChannelResponseTypeDef",
    "GetApnsChannelResponseTypeDef",
    "GetApnsSandboxChannelResponseTypeDef",
    "GetApnsVoipChannelResponseTypeDef",
    "GetApnsVoipSandboxChannelResponseTypeDef",
    "GetAppResponseTypeDef",
    "GetBaiduChannelResponseTypeDef",
    "RemoveAttributesResponseTypeDef",
    "UpdateAdmChannelResponseTypeDef",
    "UpdateApnsChannelResponseTypeDef",
    "UpdateApnsSandboxChannelResponseTypeDef",
    "UpdateApnsVoipChannelResponseTypeDef",
    "UpdateApnsVoipSandboxChannelResponseTypeDef",
    "UpdateBaiduChannelResponseTypeDef",
    "CreateEmailTemplateRequestRequestTypeDef",
    "UpdateEmailTemplateRequestRequestTypeDef",
    "CreateEmailTemplateResponseTypeDef",
    "CreatePushTemplateResponseTypeDef",
    "CreateSmsTemplateResponseTypeDef",
    "CreateVoiceTemplateResponseTypeDef",
    "CreateExportJobRequestRequestTypeDef",
    "CreateImportJobRequestRequestTypeDef",
    "CreateInAppTemplateResponseTypeDef",
    "CreateRecommenderConfigurationRequestRequestTypeDef",
    "CreateRecommenderConfigurationResponseTypeDef",
    "DeleteRecommenderConfigurationResponseTypeDef",
    "GetRecommenderConfigurationResponseTypeDef",
    "ListRecommenderConfigurationsResponseTypeDef",
    "UpdateRecommenderConfigurationResponseTypeDef",
    "CreateSmsTemplateRequestRequestTypeDef",
    "UpdateSmsTemplateRequestRequestTypeDef",
    "CreateVoiceTemplateRequestRequestTypeDef",
    "UpdateVoiceTemplateRequestRequestTypeDef",
    "CustomMessageActivityTypeDef",
    "PushNotificationTemplateRequestTypeDef",
    "PushNotificationTemplateResponseTypeDef",
    "DeleteEmailChannelResponseTypeDef",
    "GetEmailChannelResponseTypeDef",
    "UpdateEmailChannelResponseTypeDef",
    "DeleteEmailTemplateResponseTypeDef",
    "DeleteInAppTemplateResponseTypeDef",
    "DeletePushTemplateResponseTypeDef",
    "DeleteSmsTemplateResponseTypeDef",
    "DeleteVoiceTemplateResponseTypeDef",
    "UpdateEmailTemplateResponseTypeDef",
    "UpdateEndpointResponseTypeDef",
    "UpdateEndpointsBatchResponseTypeDef",
    "UpdateInAppTemplateResponseTypeDef",
    "UpdatePushTemplateResponseTypeDef",
    "UpdateSmsTemplateResponseTypeDef",
    "UpdateTemplateActiveVersionResponseTypeDef",
    "UpdateVoiceTemplateResponseTypeDef",
    "DeleteEventStreamResponseTypeDef",
    "GetEventStreamResponseTypeDef",
    "PutEventStreamResponseTypeDef",
    "DeleteGcmChannelResponseTypeDef",
    "GetGcmChannelResponseTypeDef",
    "UpdateGcmChannelResponseTypeDef",
    "DeleteSmsChannelResponseTypeDef",
    "GetSmsChannelResponseTypeDef",
    "UpdateSmsChannelResponseTypeDef",
    "DeleteVoiceChannelResponseTypeDef",
    "GetVoiceChannelResponseTypeDef",
    "UpdateVoiceChannelResponseTypeDef",
    "UpdateEmailChannelRequestRequestTypeDef",
    "EmailMessageActivityTypeDef",
    "GetEmailTemplateResponseTypeDef",
    "EndpointBatchItemTypeDef",
    "EndpointRequestTypeDef",
    "EndpointResponseTypeDef",
    "PublicEndpointTypeDef",
    "SendUsersMessageResponseTypeDef",
    "EventDimensionsTypeDef",
    "SegmentDemographicsTypeDef",
    "ItemResponseTypeDef",
    "EventTypeDef",
    "ExportJobResponseTypeDef",
    "UpdateGcmChannelRequestRequestTypeDef",
    "GPSPointDimensionTypeDef",
    "GetJourneyExecutionActivityMetricsResponseTypeDef",
    "GetJourneyExecutionMetricsResponseTypeDef",
    "GetSmsTemplateResponseTypeDef",
    "GetVoiceTemplateResponseTypeDef",
    "ImportJobResponseTypeDef",
    "InAppMessageButtonTypeDef",
    "PushMessageActivityTypeDef",
    "SMSMessageActivityTypeDef",
    "UpdateJourneyStateRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "MessageResponseTypeDef",
    "PhoneNumberValidateRequestRequestTypeDef",
    "PhoneNumberValidateResponseTypeDef",
    "PutEventStreamRequestRequestTypeDef",
    "RandomSplitActivityTypeDef",
    "SegmentBehaviorsTypeDef",
    "RemoveAttributesRequestRequestTypeDef",
    "ResultRowTypeDef",
    "UpdateSmsChannelRequestRequestTypeDef",
    "SendOTPMessageRequestRequestTypeDef",
    "SimpleEmailTypeDef",
    "UpdateTemplateActiveVersionRequestRequestTypeDef",
    "TemplateConfigurationTypeDef",
    "TemplatesResponseTypeDef",
    "TemplateVersionsResponseTypeDef",
    "UpdateRecommenderConfigurationRequestRequestTypeDef",
    "UpdateVoiceChannelRequestRequestTypeDef",
    "VerifyOTPMessageResponseTypeDef",
    "VerifyOTPMessageRequestRequestTypeDef",
    "GetCampaignActivitiesResponseTypeDef",
    "GetAppsResponseTypeDef",
    "GetApplicationSettingsResponseTypeDef",
    "UpdateApplicationSettingsResponseTypeDef",
    "UpdateApplicationSettingsRequestRequestTypeDef",
    "GetChannelsResponseTypeDef",
    "GetRecommenderConfigurationsResponseTypeDef",
    "CreatePushTemplateRequestRequestTypeDef",
    "UpdatePushTemplateRequestRequestTypeDef",
    "GetPushTemplateResponseTypeDef",
    "EndpointBatchRequestTypeDef",
    "UpdateEndpointRequestRequestTypeDef",
    "DeleteEndpointResponseTypeDef",
    "EndpointsResponseTypeDef",
    "GetEndpointResponseTypeDef",
    "SendUsersMessagesResponseTypeDef",
    "CampaignEventFilterTypeDef",
    "EventConditionTypeDef",
    "EventFilterTypeDef",
    "EventsResponseTypeDef",
    "EventsBatchTypeDef",
    "CreateExportJobResponseTypeDef",
    "ExportJobsResponseTypeDef",
    "GetExportJobResponseTypeDef",
    "SegmentLocationTypeDef",
    "CreateImportJobResponseTypeDef",
    "GetImportJobResponseTypeDef",
    "ImportJobsResponseTypeDef",
    "InAppMessageContentTypeDef",
    "SendMessagesResponseTypeDef",
    "SendOTPMessageResponseTypeDef",
    "BaseKpiResultTypeDef",
    "EmailMessageTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "UpdateEndpointsBatchRequestRequestTypeDef",
    "DeleteUserEndpointsResponseTypeDef",
    "GetUserEndpointsResponseTypeDef",
    "InAppCampaignScheduleTypeDef",
    "ScheduleTypeDef",
    "EventStartConditionTypeDef",
    "PutEventsResponseTypeDef",
    "EventsRequestTypeDef",
    "GetExportJobsResponseTypeDef",
    "GetSegmentExportJobsResponseTypeDef",
    "SegmentDimensionsTypeDef",
    "GetImportJobsResponseTypeDef",
    "GetSegmentImportJobsResponseTypeDef",
    "CampaignInAppMessageTypeDef",
    "InAppMessageTypeDef",
    "InAppTemplateRequestTypeDef",
    "InAppTemplateResponseTypeDef",
    "ApplicationDateRangeKpiResponseTypeDef",
    "CampaignDateRangeKpiResponseTypeDef",
    "JourneyDateRangeKpiResponseTypeDef",
    "DirectMessageConfigurationTypeDef",
    "StartConditionTypeDef",
    "PutEventsRequestRequestTypeDef",
    "SegmentGroupTypeDef",
    "SimpleConditionTypeDef",
    "MessageConfigurationTypeDef",
    "InAppMessageCampaignTypeDef",
    "CreateInAppTemplateRequestRequestTypeDef",
    "UpdateInAppTemplateRequestRequestTypeDef",
    "GetInAppTemplateResponseTypeDef",
    "GetApplicationDateRangeKpiResponseTypeDef",
    "GetCampaignDateRangeKpiResponseTypeDef",
    "GetJourneyDateRangeKpiResponseTypeDef",
    "MessageRequestTypeDef",
    "SendUsersMessageRequestTypeDef",
    "SegmentGroupListTypeDef",
    "ConditionTypeDef",
    "MultiConditionalBranchTypeDef",
    "TreatmentResourceTypeDef",
    "WriteTreatmentResourceTypeDef",
    "InAppMessagesResponseTypeDef",
    "SendMessagesRequestRequestTypeDef",
    "SendUsersMessagesRequestRequestTypeDef",
    "SegmentResponseTypeDef",
    "WriteSegmentRequestTypeDef",
    "ConditionalSplitActivityTypeDef",
    "MultiConditionalSplitActivityTypeDef",
    "CampaignResponseTypeDef",
    "WriteCampaignRequestTypeDef",
    "GetInAppMessagesResponseTypeDef",
    "CreateSegmentResponseTypeDef",
    "DeleteSegmentResponseTypeDef",
    "GetSegmentResponseTypeDef",
    "GetSegmentVersionResponseTypeDef",
    "SegmentsResponseTypeDef",
    "UpdateSegmentResponseTypeDef",
    "CreateSegmentRequestRequestTypeDef",
    "UpdateSegmentRequestRequestTypeDef",
    "ActivityTypeDef",
    "CampaignsResponseTypeDef",
    "CreateCampaignResponseTypeDef",
    "DeleteCampaignResponseTypeDef",
    "GetCampaignResponseTypeDef",
    "GetCampaignVersionResponseTypeDef",
    "UpdateCampaignResponseTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "UpdateCampaignRequestRequestTypeDef",
    "GetSegmentVersionsResponseTypeDef",
    "GetSegmentsResponseTypeDef",
    "JourneyResponseTypeDef",
    "WriteJourneyRequestTypeDef",
    "GetCampaignVersionsResponseTypeDef",
    "GetCampaignsResponseTypeDef",
    "CreateJourneyResponseTypeDef",
    "DeleteJourneyResponseTypeDef",
    "GetJourneyResponseTypeDef",
    "JourneysResponseTypeDef",
    "UpdateJourneyResponseTypeDef",
    "UpdateJourneyStateResponseTypeDef",
    "CreateJourneyRequestRequestTypeDef",
    "UpdateJourneyRequestRequestTypeDef",
    "ListJourneysResponseTypeDef",
)

_RequiredADMChannelRequestTypeDef = TypedDict(
    "_RequiredADMChannelRequestTypeDef",
    {
        "ClientId": str,
        "ClientSecret": str,
    },
)
_OptionalADMChannelRequestTypeDef = TypedDict(
    "_OptionalADMChannelRequestTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)


class ADMChannelRequestTypeDef(
    _RequiredADMChannelRequestTypeDef, _OptionalADMChannelRequestTypeDef
):
    pass


_RequiredADMChannelResponseTypeDef = TypedDict(
    "_RequiredADMChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalADMChannelResponseTypeDef = TypedDict(
    "_OptionalADMChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class ADMChannelResponseTypeDef(
    _RequiredADMChannelResponseTypeDef, _OptionalADMChannelResponseTypeDef
):
    pass


ADMMessageTypeDef = TypedDict(
    "ADMMessageTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "ConsolidationKey": str,
        "Data": Mapping[str, str],
        "ExpiresAfter": str,
        "IconReference": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "MD5": str,
        "RawContent": str,
        "SilentPush": bool,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "Title": str,
        "Url": str,
    },
    total=False,
)

APNSChannelRequestTypeDef = TypedDict(
    "APNSChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

_RequiredAPNSChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalAPNSChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSChannelResponseTypeDef(
    _RequiredAPNSChannelResponseTypeDef, _OptionalAPNSChannelResponseTypeDef
):
    pass


APNSMessageTypeDef = TypedDict(
    "APNSMessageTypeDef",
    {
        "APNSPushType": str,
        "Action": ActionType,
        "Badge": int,
        "Body": str,
        "Category": str,
        "CollapseId": str,
        "Data": Mapping[str, str],
        "MediaUrl": str,
        "PreferredAuthenticationMethod": str,
        "Priority": str,
        "RawContent": str,
        "SilentPush": bool,
        "Sound": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "ThreadId": str,
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

APNSPushNotificationTemplateTypeDef = TypedDict(
    "APNSPushNotificationTemplateTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "MediaUrl": str,
        "RawContent": str,
        "Sound": str,
        "Title": str,
        "Url": str,
    },
    total=False,
)

APNSSandboxChannelRequestTypeDef = TypedDict(
    "APNSSandboxChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

_RequiredAPNSSandboxChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSSandboxChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalAPNSSandboxChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSSandboxChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSSandboxChannelResponseTypeDef(
    _RequiredAPNSSandboxChannelResponseTypeDef, _OptionalAPNSSandboxChannelResponseTypeDef
):
    pass


APNSVoipChannelRequestTypeDef = TypedDict(
    "APNSVoipChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

_RequiredAPNSVoipChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSVoipChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalAPNSVoipChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSVoipChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSVoipChannelResponseTypeDef(
    _RequiredAPNSVoipChannelResponseTypeDef, _OptionalAPNSVoipChannelResponseTypeDef
):
    pass


APNSVoipSandboxChannelRequestTypeDef = TypedDict(
    "APNSVoipSandboxChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

_RequiredAPNSVoipSandboxChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSVoipSandboxChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalAPNSVoipSandboxChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSVoipSandboxChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSVoipSandboxChannelResponseTypeDef(
    _RequiredAPNSVoipSandboxChannelResponseTypeDef, _OptionalAPNSVoipSandboxChannelResponseTypeDef
):
    pass


_RequiredActivityResponseTypeDef = TypedDict(
    "_RequiredActivityResponseTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
        "Id": str,
    },
)
_OptionalActivityResponseTypeDef = TypedDict(
    "_OptionalActivityResponseTypeDef",
    {
        "End": str,
        "Result": str,
        "ScheduledStart": str,
        "Start": str,
        "State": str,
        "SuccessfulEndpointCount": int,
        "TimezonesCompletedCount": int,
        "TimezonesTotalCount": int,
        "TotalEndpointCount": int,
        "TreatmentId": str,
    },
    total=False,
)


class ActivityResponseTypeDef(_RequiredActivityResponseTypeDef, _OptionalActivityResponseTypeDef):
    pass


ContactCenterActivityTypeDef = TypedDict(
    "ContactCenterActivityTypeDef",
    {
        "NextActivity": str,
    },
    total=False,
)

_RequiredHoldoutActivityTypeDef = TypedDict(
    "_RequiredHoldoutActivityTypeDef",
    {
        "Percentage": int,
    },
)
_OptionalHoldoutActivityTypeDef = TypedDict(
    "_OptionalHoldoutActivityTypeDef",
    {
        "NextActivity": str,
    },
    total=False,
)


class HoldoutActivityTypeDef(_RequiredHoldoutActivityTypeDef, _OptionalHoldoutActivityTypeDef):
    pass


AddressConfigurationTypeDef = TypedDict(
    "AddressConfigurationTypeDef",
    {
        "BodyOverride": str,
        "ChannelType": ChannelTypeType,
        "Context": Mapping[str, str],
        "RawContent": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "TitleOverride": str,
    },
    total=False,
)

AndroidPushNotificationTemplateTypeDef = TypedDict(
    "AndroidPushNotificationTemplateTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "RawContent": str,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Title": str,
        "Url": str,
    },
    total=False,
)

_RequiredApplicationResponseTypeDef = TypedDict(
    "_RequiredApplicationResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
    },
)
_OptionalApplicationResponseTypeDef = TypedDict(
    "_OptionalApplicationResponseTypeDef",
    {
        "tags": Dict[str, str],
        "CreationDate": str,
    },
    total=False,
)


class ApplicationResponseTypeDef(
    _RequiredApplicationResponseTypeDef, _OptionalApplicationResponseTypeDef
):
    pass


CampaignHookTypeDef = TypedDict(
    "CampaignHookTypeDef",
    {
        "LambdaFunctionName": str,
        "Mode": ModeType,
        "WebUrl": str,
    },
    total=False,
)

CampaignLimitsTypeDef = TypedDict(
    "CampaignLimitsTypeDef",
    {
        "Daily": int,
        "MaximumDuration": int,
        "MessagesPerSecond": int,
        "Total": int,
        "Session": int,
    },
    total=False,
)

QuietTimeTypeDef = TypedDict(
    "QuietTimeTypeDef",
    {
        "End": str,
        "Start": str,
    },
    total=False,
)

_RequiredAttributeDimensionTypeDef = TypedDict(
    "_RequiredAttributeDimensionTypeDef",
    {
        "Values": Sequence[str],
    },
)
_OptionalAttributeDimensionTypeDef = TypedDict(
    "_OptionalAttributeDimensionTypeDef",
    {
        "AttributeType": AttributeTypeType,
    },
    total=False,
)


class AttributeDimensionTypeDef(
    _RequiredAttributeDimensionTypeDef, _OptionalAttributeDimensionTypeDef
):
    pass


_RequiredAttributesResourceTypeDef = TypedDict(
    "_RequiredAttributesResourceTypeDef",
    {
        "ApplicationId": str,
        "AttributeType": str,
    },
)
_OptionalAttributesResourceTypeDef = TypedDict(
    "_OptionalAttributesResourceTypeDef",
    {
        "Attributes": List[str],
    },
    total=False,
)


class AttributesResourceTypeDef(
    _RequiredAttributesResourceTypeDef, _OptionalAttributesResourceTypeDef
):
    pass


_RequiredBaiduChannelRequestTypeDef = TypedDict(
    "_RequiredBaiduChannelRequestTypeDef",
    {
        "ApiKey": str,
        "SecretKey": str,
    },
)
_OptionalBaiduChannelRequestTypeDef = TypedDict(
    "_OptionalBaiduChannelRequestTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)


class BaiduChannelRequestTypeDef(
    _RequiredBaiduChannelRequestTypeDef, _OptionalBaiduChannelRequestTypeDef
):
    pass


_RequiredBaiduChannelResponseTypeDef = TypedDict(
    "_RequiredBaiduChannelResponseTypeDef",
    {
        "Credential": str,
        "Platform": str,
    },
)
_OptionalBaiduChannelResponseTypeDef = TypedDict(
    "_OptionalBaiduChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class BaiduChannelResponseTypeDef(
    _RequiredBaiduChannelResponseTypeDef, _OptionalBaiduChannelResponseTypeDef
):
    pass


BaiduMessageTypeDef = TypedDict(
    "BaiduMessageTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "Data": Mapping[str, str],
        "IconReference": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "RawContent": str,
        "SilentPush": bool,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

CampaignCustomMessageTypeDef = TypedDict(
    "CampaignCustomMessageTypeDef",
    {
        "Data": str,
    },
    total=False,
)

CampaignEmailMessageTypeDef = TypedDict(
    "CampaignEmailMessageTypeDef",
    {
        "Body": str,
        "FromAddress": str,
        "HtmlBody": str,
        "Title": str,
    },
    total=False,
)

CampaignStateTypeDef = TypedDict(
    "CampaignStateTypeDef",
    {
        "CampaignStatus": CampaignStatusType,
    },
    total=False,
)

_RequiredCustomDeliveryConfigurationTypeDef = TypedDict(
    "_RequiredCustomDeliveryConfigurationTypeDef",
    {
        "DeliveryUri": str,
    },
)
_OptionalCustomDeliveryConfigurationTypeDef = TypedDict(
    "_OptionalCustomDeliveryConfigurationTypeDef",
    {
        "EndpointTypes": Sequence[EndpointTypesElementType],
    },
    total=False,
)


class CustomDeliveryConfigurationTypeDef(
    _RequiredCustomDeliveryConfigurationTypeDef, _OptionalCustomDeliveryConfigurationTypeDef
):
    pass


CampaignSmsMessageTypeDef = TypedDict(
    "CampaignSmsMessageTypeDef",
    {
        "Body": str,
        "MessageType": MessageTypeType,
        "OriginationNumber": str,
        "SenderId": str,
        "EntityId": str,
        "TemplateId": str,
    },
    total=False,
)

ChannelResponseTypeDef = TypedDict(
    "ChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)

WaitTimeTypeDef = TypedDict(
    "WaitTimeTypeDef",
    {
        "WaitFor": str,
        "WaitUntil": str,
    },
    total=False,
)

_RequiredCreateApplicationRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateApplicationRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestTypeDef(
    _RequiredCreateApplicationRequestTypeDef, _OptionalCreateApplicationRequestTypeDef
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

EmailTemplateRequestTypeDef = TypedDict(
    "EmailTemplateRequestTypeDef",
    {
        "DefaultSubstitutions": str,
        "HtmlPart": str,
        "RecommenderId": str,
        "Subject": str,
        "tags": Mapping[str, str],
        "TemplateDescription": str,
        "TextPart": str,
    },
    total=False,
)

CreateTemplateMessageBodyTypeDef = TypedDict(
    "CreateTemplateMessageBodyTypeDef",
    {
        "Arn": str,
        "Message": str,
        "RequestID": str,
    },
    total=False,
)

_RequiredExportJobRequestTypeDef = TypedDict(
    "_RequiredExportJobRequestTypeDef",
    {
        "RoleArn": str,
        "S3UrlPrefix": str,
    },
)
_OptionalExportJobRequestTypeDef = TypedDict(
    "_OptionalExportJobRequestTypeDef",
    {
        "SegmentId": str,
        "SegmentVersion": int,
    },
    total=False,
)


class ExportJobRequestTypeDef(_RequiredExportJobRequestTypeDef, _OptionalExportJobRequestTypeDef):
    pass


_RequiredImportJobRequestTypeDef = TypedDict(
    "_RequiredImportJobRequestTypeDef",
    {
        "Format": FormatType,
        "RoleArn": str,
        "S3Url": str,
    },
)
_OptionalImportJobRequestTypeDef = TypedDict(
    "_OptionalImportJobRequestTypeDef",
    {
        "DefineSegment": bool,
        "ExternalId": str,
        "RegisterEndpoints": bool,
        "SegmentId": str,
        "SegmentName": str,
    },
    total=False,
)


class ImportJobRequestTypeDef(_RequiredImportJobRequestTypeDef, _OptionalImportJobRequestTypeDef):
    pass


TemplateCreateMessageBodyTypeDef = TypedDict(
    "TemplateCreateMessageBodyTypeDef",
    {
        "Arn": str,
        "Message": str,
        "RequestID": str,
    },
    total=False,
)

_RequiredCreateRecommenderConfigurationTypeDef = TypedDict(
    "_RequiredCreateRecommenderConfigurationTypeDef",
    {
        "RecommendationProviderRoleArn": str,
        "RecommendationProviderUri": str,
    },
)
_OptionalCreateRecommenderConfigurationTypeDef = TypedDict(
    "_OptionalCreateRecommenderConfigurationTypeDef",
    {
        "Attributes": Mapping[str, str],
        "Description": str,
        "Name": str,
        "RecommendationProviderIdType": str,
        "RecommendationTransformerUri": str,
        "RecommendationsDisplayName": str,
        "RecommendationsPerMessage": int,
    },
    total=False,
)


class CreateRecommenderConfigurationTypeDef(
    _RequiredCreateRecommenderConfigurationTypeDef, _OptionalCreateRecommenderConfigurationTypeDef
):
    pass


_RequiredRecommenderConfigurationResponseTypeDef = TypedDict(
    "_RequiredRecommenderConfigurationResponseTypeDef",
    {
        "CreationDate": str,
        "Id": str,
        "LastModifiedDate": str,
        "RecommendationProviderRoleArn": str,
        "RecommendationProviderUri": str,
    },
)
_OptionalRecommenderConfigurationResponseTypeDef = TypedDict(
    "_OptionalRecommenderConfigurationResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "Description": str,
        "Name": str,
        "RecommendationProviderIdType": str,
        "RecommendationTransformerUri": str,
        "RecommendationsDisplayName": str,
        "RecommendationsPerMessage": int,
    },
    total=False,
)


class RecommenderConfigurationResponseTypeDef(
    _RequiredRecommenderConfigurationResponseTypeDef,
    _OptionalRecommenderConfigurationResponseTypeDef,
):
    pass


SMSTemplateRequestTypeDef = TypedDict(
    "SMSTemplateRequestTypeDef",
    {
        "Body": str,
        "DefaultSubstitutions": str,
        "RecommenderId": str,
        "tags": Mapping[str, str],
        "TemplateDescription": str,
    },
    total=False,
)

VoiceTemplateRequestTypeDef = TypedDict(
    "VoiceTemplateRequestTypeDef",
    {
        "Body": str,
        "DefaultSubstitutions": str,
        "LanguageCode": str,
        "tags": Mapping[str, str],
        "TemplateDescription": str,
        "VoiceId": str,
    },
    total=False,
)

JourneyCustomMessageTypeDef = TypedDict(
    "JourneyCustomMessageTypeDef",
    {
        "Data": str,
    },
    total=False,
)

_RequiredDefaultButtonConfigurationTypeDef = TypedDict(
    "_RequiredDefaultButtonConfigurationTypeDef",
    {
        "ButtonAction": ButtonActionType,
        "Text": str,
    },
)
_OptionalDefaultButtonConfigurationTypeDef = TypedDict(
    "_OptionalDefaultButtonConfigurationTypeDef",
    {
        "BackgroundColor": str,
        "BorderRadius": int,
        "Link": str,
        "TextColor": str,
    },
    total=False,
)


class DefaultButtonConfigurationTypeDef(
    _RequiredDefaultButtonConfigurationTypeDef, _OptionalDefaultButtonConfigurationTypeDef
):
    pass


DefaultMessageTypeDef = TypedDict(
    "DefaultMessageTypeDef",
    {
        "Body": str,
        "Substitutions": Mapping[str, Sequence[str]],
    },
    total=False,
)

DefaultPushNotificationMessageTypeDef = TypedDict(
    "DefaultPushNotificationMessageTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "Data": Mapping[str, str],
        "SilentPush": bool,
        "Substitutions": Mapping[str, Sequence[str]],
        "Title": str,
        "Url": str,
    },
    total=False,
)

DefaultPushNotificationTemplateTypeDef = TypedDict(
    "DefaultPushNotificationTemplateTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "Sound": str,
        "Title": str,
        "Url": str,
    },
    total=False,
)

DeleteAdmChannelRequestRequestTypeDef = TypedDict(
    "DeleteAdmChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteApnsChannelRequestRequestTypeDef = TypedDict(
    "DeleteApnsChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteApnsSandboxChannelRequestRequestTypeDef = TypedDict(
    "DeleteApnsSandboxChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteApnsVoipChannelRequestRequestTypeDef = TypedDict(
    "DeleteApnsVoipChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteApnsVoipSandboxChannelRequestRequestTypeDef = TypedDict(
    "DeleteApnsVoipSandboxChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteAppRequestRequestTypeDef = TypedDict(
    "DeleteAppRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteBaiduChannelRequestRequestTypeDef = TypedDict(
    "DeleteBaiduChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteCampaignRequestRequestTypeDef = TypedDict(
    "DeleteCampaignRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
    },
)

DeleteEmailChannelRequestRequestTypeDef = TypedDict(
    "DeleteEmailChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredEmailChannelResponseTypeDef = TypedDict(
    "_RequiredEmailChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalEmailChannelResponseTypeDef = TypedDict(
    "_OptionalEmailChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationSet": str,
        "CreationDate": str,
        "Enabled": bool,
        "FromAddress": str,
        "HasCredential": bool,
        "Id": str,
        "Identity": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "MessagesPerSecond": int,
        "RoleArn": str,
        "Version": int,
    },
    total=False,
)


class EmailChannelResponseTypeDef(
    _RequiredEmailChannelResponseTypeDef, _OptionalEmailChannelResponseTypeDef
):
    pass


_RequiredDeleteEmailTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalDeleteEmailTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteEmailTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class DeleteEmailTemplateRequestRequestTypeDef(
    _RequiredDeleteEmailTemplateRequestRequestTypeDef,
    _OptionalDeleteEmailTemplateRequestRequestTypeDef,
):
    pass


MessageBodyTypeDef = TypedDict(
    "MessageBodyTypeDef",
    {
        "Message": str,
        "RequestID": str,
    },
    total=False,
)

DeleteEndpointRequestRequestTypeDef = TypedDict(
    "DeleteEndpointRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EndpointId": str,
    },
)

DeleteEventStreamRequestRequestTypeDef = TypedDict(
    "DeleteEventStreamRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredEventStreamTypeDef = TypedDict(
    "_RequiredEventStreamTypeDef",
    {
        "ApplicationId": str,
        "DestinationStreamArn": str,
        "RoleArn": str,
    },
)
_OptionalEventStreamTypeDef = TypedDict(
    "_OptionalEventStreamTypeDef",
    {
        "ExternalId": str,
        "LastModifiedDate": str,
        "LastUpdatedBy": str,
    },
    total=False,
)


class EventStreamTypeDef(_RequiredEventStreamTypeDef, _OptionalEventStreamTypeDef):
    pass


DeleteGcmChannelRequestRequestTypeDef = TypedDict(
    "DeleteGcmChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGCMChannelResponseTypeDef = TypedDict(
    "_RequiredGCMChannelResponseTypeDef",
    {
        "Credential": str,
        "Platform": str,
    },
)
_OptionalGCMChannelResponseTypeDef = TypedDict(
    "_OptionalGCMChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class GCMChannelResponseTypeDef(
    _RequiredGCMChannelResponseTypeDef, _OptionalGCMChannelResponseTypeDef
):
    pass


_RequiredDeleteInAppTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteInAppTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalDeleteInAppTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteInAppTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class DeleteInAppTemplateRequestRequestTypeDef(
    _RequiredDeleteInAppTemplateRequestRequestTypeDef,
    _OptionalDeleteInAppTemplateRequestRequestTypeDef,
):
    pass


DeleteJourneyRequestRequestTypeDef = TypedDict(
    "DeleteJourneyRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
    },
)

_RequiredDeletePushTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePushTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalDeletePushTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePushTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class DeletePushTemplateRequestRequestTypeDef(
    _RequiredDeletePushTemplateRequestRequestTypeDef,
    _OptionalDeletePushTemplateRequestRequestTypeDef,
):
    pass


DeleteRecommenderConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteRecommenderConfigurationRequestRequestTypeDef",
    {
        "RecommenderId": str,
    },
)

DeleteSegmentRequestRequestTypeDef = TypedDict(
    "DeleteSegmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
    },
)

DeleteSmsChannelRequestRequestTypeDef = TypedDict(
    "DeleteSmsChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredSMSChannelResponseTypeDef = TypedDict(
    "_RequiredSMSChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalSMSChannelResponseTypeDef = TypedDict(
    "_OptionalSMSChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "PromotionalMessagesPerSecond": int,
        "SenderId": str,
        "ShortCode": str,
        "TransactionalMessagesPerSecond": int,
        "Version": int,
    },
    total=False,
)


class SMSChannelResponseTypeDef(
    _RequiredSMSChannelResponseTypeDef, _OptionalSMSChannelResponseTypeDef
):
    pass


_RequiredDeleteSmsTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSmsTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalDeleteSmsTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSmsTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class DeleteSmsTemplateRequestRequestTypeDef(
    _RequiredDeleteSmsTemplateRequestRequestTypeDef, _OptionalDeleteSmsTemplateRequestRequestTypeDef
):
    pass


DeleteUserEndpointsRequestRequestTypeDef = TypedDict(
    "DeleteUserEndpointsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "UserId": str,
    },
)

DeleteVoiceChannelRequestRequestTypeDef = TypedDict(
    "DeleteVoiceChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredVoiceChannelResponseTypeDef = TypedDict(
    "_RequiredVoiceChannelResponseTypeDef",
    {
        "Platform": str,
    },
)
_OptionalVoiceChannelResponseTypeDef = TypedDict(
    "_OptionalVoiceChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class VoiceChannelResponseTypeDef(
    _RequiredVoiceChannelResponseTypeDef, _OptionalVoiceChannelResponseTypeDef
):
    pass


_RequiredDeleteVoiceTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteVoiceTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalDeleteVoiceTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteVoiceTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class DeleteVoiceTemplateRequestRequestTypeDef(
    _RequiredDeleteVoiceTemplateRequestRequestTypeDef,
    _OptionalDeleteVoiceTemplateRequestRequestTypeDef,
):
    pass


GCMMessageTypeDef = TypedDict(
    "GCMMessageTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "CollapseKey": str,
        "Data": Mapping[str, str],
        "IconReference": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "Priority": str,
        "RawContent": str,
        "RestrictedPackageName": str,
        "SilentPush": bool,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

SMSMessageTypeDef = TypedDict(
    "SMSMessageTypeDef",
    {
        "Body": str,
        "Keyword": str,
        "MediaUrl": str,
        "MessageType": MessageTypeType,
        "OriginationNumber": str,
        "SenderId": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "EntityId": str,
        "TemplateId": str,
    },
    total=False,
)

VoiceMessageTypeDef = TypedDict(
    "VoiceMessageTypeDef",
    {
        "Body": str,
        "LanguageCode": str,
        "OriginationNumber": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "VoiceId": str,
    },
    total=False,
)

_RequiredEmailChannelRequestTypeDef = TypedDict(
    "_RequiredEmailChannelRequestTypeDef",
    {
        "FromAddress": str,
        "Identity": str,
    },
)
_OptionalEmailChannelRequestTypeDef = TypedDict(
    "_OptionalEmailChannelRequestTypeDef",
    {
        "ConfigurationSet": str,
        "Enabled": bool,
        "RoleArn": str,
    },
    total=False,
)


class EmailChannelRequestTypeDef(
    _RequiredEmailChannelRequestTypeDef, _OptionalEmailChannelRequestTypeDef
):
    pass


JourneyEmailMessageTypeDef = TypedDict(
    "JourneyEmailMessageTypeDef",
    {
        "FromAddress": str,
    },
    total=False,
)

RawEmailTypeDef = TypedDict(
    "RawEmailTypeDef",
    {
        "Data": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)

_RequiredEmailTemplateResponseTypeDef = TypedDict(
    "_RequiredEmailTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": TemplateTypeType,
    },
)
_OptionalEmailTemplateResponseTypeDef = TypedDict(
    "_OptionalEmailTemplateResponseTypeDef",
    {
        "Arn": str,
        "DefaultSubstitutions": str,
        "HtmlPart": str,
        "RecommenderId": str,
        "Subject": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "TextPart": str,
        "Version": str,
    },
    total=False,
)


class EmailTemplateResponseTypeDef(
    _RequiredEmailTemplateResponseTypeDef, _OptionalEmailTemplateResponseTypeDef
):
    pass


EndpointDemographicTypeDef = TypedDict(
    "EndpointDemographicTypeDef",
    {
        "AppVersion": str,
        "Locale": str,
        "Make": str,
        "Model": str,
        "ModelVersion": str,
        "Platform": str,
        "PlatformVersion": str,
        "Timezone": str,
    },
    total=False,
)

EndpointLocationTypeDef = TypedDict(
    "EndpointLocationTypeDef",
    {
        "City": str,
        "Country": str,
        "Latitude": float,
        "Longitude": float,
        "PostalCode": str,
        "Region": str,
    },
    total=False,
)

EndpointUserTypeDef = TypedDict(
    "EndpointUserTypeDef",
    {
        "UserAttributes": Dict[str, List[str]],
        "UserId": str,
    },
    total=False,
)

EndpointItemResponseTypeDef = TypedDict(
    "EndpointItemResponseTypeDef",
    {
        "Message": str,
        "StatusCode": int,
    },
    total=False,
)

_RequiredEndpointMessageResultTypeDef = TypedDict(
    "_RequiredEndpointMessageResultTypeDef",
    {
        "DeliveryStatus": DeliveryStatusType,
        "StatusCode": int,
    },
)
_OptionalEndpointMessageResultTypeDef = TypedDict(
    "_OptionalEndpointMessageResultTypeDef",
    {
        "Address": str,
        "MessageId": str,
        "StatusMessage": str,
        "UpdatedToken": str,
    },
    total=False,
)


class EndpointMessageResultTypeDef(
    _RequiredEndpointMessageResultTypeDef, _OptionalEndpointMessageResultTypeDef
):
    pass


EndpointSendConfigurationTypeDef = TypedDict(
    "EndpointSendConfigurationTypeDef",
    {
        "BodyOverride": str,
        "Context": Mapping[str, str],
        "RawContent": str,
        "Substitutions": Mapping[str, Sequence[str]],
        "TitleOverride": str,
    },
    total=False,
)

MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "ComparisonOperator": str,
        "Value": float,
    },
)

_RequiredSetDimensionTypeDef = TypedDict(
    "_RequiredSetDimensionTypeDef",
    {
        "Values": Sequence[str],
    },
)
_OptionalSetDimensionTypeDef = TypedDict(
    "_OptionalSetDimensionTypeDef",
    {
        "DimensionType": DimensionTypeType,
    },
    total=False,
)


class SetDimensionTypeDef(_RequiredSetDimensionTypeDef, _OptionalSetDimensionTypeDef):
    pass


EventItemResponseTypeDef = TypedDict(
    "EventItemResponseTypeDef",
    {
        "Message": str,
        "StatusCode": int,
    },
    total=False,
)

_RequiredSessionTypeDef = TypedDict(
    "_RequiredSessionTypeDef",
    {
        "Id": str,
        "StartTimestamp": str,
    },
)
_OptionalSessionTypeDef = TypedDict(
    "_OptionalSessionTypeDef",
    {
        "Duration": int,
        "StopTimestamp": str,
    },
    total=False,
)


class SessionTypeDef(_RequiredSessionTypeDef, _OptionalSessionTypeDef):
    pass


_RequiredExportJobResourceTypeDef = TypedDict(
    "_RequiredExportJobResourceTypeDef",
    {
        "RoleArn": str,
        "S3UrlPrefix": str,
    },
)
_OptionalExportJobResourceTypeDef = TypedDict(
    "_OptionalExportJobResourceTypeDef",
    {
        "SegmentId": str,
        "SegmentVersion": int,
    },
    total=False,
)


class ExportJobResourceTypeDef(
    _RequiredExportJobResourceTypeDef, _OptionalExportJobResourceTypeDef
):
    pass


_RequiredGCMChannelRequestTypeDef = TypedDict(
    "_RequiredGCMChannelRequestTypeDef",
    {
        "ApiKey": str,
    },
)
_OptionalGCMChannelRequestTypeDef = TypedDict(
    "_OptionalGCMChannelRequestTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)


class GCMChannelRequestTypeDef(
    _RequiredGCMChannelRequestTypeDef, _OptionalGCMChannelRequestTypeDef
):
    pass


GPSCoordinatesTypeDef = TypedDict(
    "GPSCoordinatesTypeDef",
    {
        "Latitude": float,
        "Longitude": float,
    },
)

GetAdmChannelRequestRequestTypeDef = TypedDict(
    "GetAdmChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetApnsChannelRequestRequestTypeDef = TypedDict(
    "GetApnsChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetApnsSandboxChannelRequestRequestTypeDef = TypedDict(
    "GetApnsSandboxChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetApnsVoipChannelRequestRequestTypeDef = TypedDict(
    "GetApnsVoipChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetApnsVoipSandboxChannelRequestRequestTypeDef = TypedDict(
    "GetApnsVoipSandboxChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetAppRequestRequestTypeDef = TypedDict(
    "GetAppRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGetApplicationDateRangeKpiRequestRequestTypeDef = TypedDict(
    "_RequiredGetApplicationDateRangeKpiRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "KpiName": str,
    },
)
_OptionalGetApplicationDateRangeKpiRequestRequestTypeDef = TypedDict(
    "_OptionalGetApplicationDateRangeKpiRequestRequestTypeDef",
    {
        "EndTime": Union[datetime, str],
        "NextToken": str,
        "PageSize": str,
        "StartTime": Union[datetime, str],
    },
    total=False,
)


class GetApplicationDateRangeKpiRequestRequestTypeDef(
    _RequiredGetApplicationDateRangeKpiRequestRequestTypeDef,
    _OptionalGetApplicationDateRangeKpiRequestRequestTypeDef,
):
    pass


GetApplicationSettingsRequestRequestTypeDef = TypedDict(
    "GetApplicationSettingsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetAppsRequestRequestTypeDef = TypedDict(
    "GetAppsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)

GetBaiduChannelRequestRequestTypeDef = TypedDict(
    "GetBaiduChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGetCampaignActivitiesRequestRequestTypeDef = TypedDict(
    "_RequiredGetCampaignActivitiesRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
    },
)
_OptionalGetCampaignActivitiesRequestRequestTypeDef = TypedDict(
    "_OptionalGetCampaignActivitiesRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetCampaignActivitiesRequestRequestTypeDef(
    _RequiredGetCampaignActivitiesRequestRequestTypeDef,
    _OptionalGetCampaignActivitiesRequestRequestTypeDef,
):
    pass


_RequiredGetCampaignDateRangeKpiRequestRequestTypeDef = TypedDict(
    "_RequiredGetCampaignDateRangeKpiRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
        "KpiName": str,
    },
)
_OptionalGetCampaignDateRangeKpiRequestRequestTypeDef = TypedDict(
    "_OptionalGetCampaignDateRangeKpiRequestRequestTypeDef",
    {
        "EndTime": Union[datetime, str],
        "NextToken": str,
        "PageSize": str,
        "StartTime": Union[datetime, str],
    },
    total=False,
)


class GetCampaignDateRangeKpiRequestRequestTypeDef(
    _RequiredGetCampaignDateRangeKpiRequestRequestTypeDef,
    _OptionalGetCampaignDateRangeKpiRequestRequestTypeDef,
):
    pass


GetCampaignRequestRequestTypeDef = TypedDict(
    "GetCampaignRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
    },
)

GetCampaignVersionRequestRequestTypeDef = TypedDict(
    "GetCampaignVersionRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
        "Version": str,
    },
)

_RequiredGetCampaignVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetCampaignVersionsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
    },
)
_OptionalGetCampaignVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetCampaignVersionsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetCampaignVersionsRequestRequestTypeDef(
    _RequiredGetCampaignVersionsRequestRequestTypeDef,
    _OptionalGetCampaignVersionsRequestRequestTypeDef,
):
    pass


_RequiredGetCampaignsRequestRequestTypeDef = TypedDict(
    "_RequiredGetCampaignsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalGetCampaignsRequestRequestTypeDef = TypedDict(
    "_OptionalGetCampaignsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetCampaignsRequestRequestTypeDef(
    _RequiredGetCampaignsRequestRequestTypeDef, _OptionalGetCampaignsRequestRequestTypeDef
):
    pass


GetChannelsRequestRequestTypeDef = TypedDict(
    "GetChannelsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetEmailChannelRequestRequestTypeDef = TypedDict(
    "GetEmailChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGetEmailTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetEmailTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalGetEmailTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetEmailTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetEmailTemplateRequestRequestTypeDef(
    _RequiredGetEmailTemplateRequestRequestTypeDef, _OptionalGetEmailTemplateRequestRequestTypeDef
):
    pass


GetEndpointRequestRequestTypeDef = TypedDict(
    "GetEndpointRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EndpointId": str,
    },
)

GetEventStreamRequestRequestTypeDef = TypedDict(
    "GetEventStreamRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetExportJobRequestRequestTypeDef = TypedDict(
    "GetExportJobRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JobId": str,
    },
)

_RequiredGetExportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredGetExportJobsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalGetExportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalGetExportJobsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetExportJobsRequestRequestTypeDef(
    _RequiredGetExportJobsRequestRequestTypeDef, _OptionalGetExportJobsRequestRequestTypeDef
):
    pass


GetGcmChannelRequestRequestTypeDef = TypedDict(
    "GetGcmChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetImportJobRequestRequestTypeDef = TypedDict(
    "GetImportJobRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JobId": str,
    },
)

_RequiredGetImportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredGetImportJobsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalGetImportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalGetImportJobsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetImportJobsRequestRequestTypeDef(
    _RequiredGetImportJobsRequestRequestTypeDef, _OptionalGetImportJobsRequestRequestTypeDef
):
    pass


GetInAppMessagesRequestRequestTypeDef = TypedDict(
    "GetInAppMessagesRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EndpointId": str,
    },
)

_RequiredGetInAppTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetInAppTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalGetInAppTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetInAppTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetInAppTemplateRequestRequestTypeDef(
    _RequiredGetInAppTemplateRequestRequestTypeDef, _OptionalGetInAppTemplateRequestRequestTypeDef
):
    pass


_RequiredGetJourneyDateRangeKpiRequestRequestTypeDef = TypedDict(
    "_RequiredGetJourneyDateRangeKpiRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
        "KpiName": str,
    },
)
_OptionalGetJourneyDateRangeKpiRequestRequestTypeDef = TypedDict(
    "_OptionalGetJourneyDateRangeKpiRequestRequestTypeDef",
    {
        "EndTime": Union[datetime, str],
        "NextToken": str,
        "PageSize": str,
        "StartTime": Union[datetime, str],
    },
    total=False,
)


class GetJourneyDateRangeKpiRequestRequestTypeDef(
    _RequiredGetJourneyDateRangeKpiRequestRequestTypeDef,
    _OptionalGetJourneyDateRangeKpiRequestRequestTypeDef,
):
    pass


_RequiredGetJourneyExecutionActivityMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredGetJourneyExecutionActivityMetricsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyActivityId": str,
        "JourneyId": str,
    },
)
_OptionalGetJourneyExecutionActivityMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalGetJourneyExecutionActivityMetricsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": str,
    },
    total=False,
)


class GetJourneyExecutionActivityMetricsRequestRequestTypeDef(
    _RequiredGetJourneyExecutionActivityMetricsRequestRequestTypeDef,
    _OptionalGetJourneyExecutionActivityMetricsRequestRequestTypeDef,
):
    pass


JourneyExecutionActivityMetricsResponseTypeDef = TypedDict(
    "JourneyExecutionActivityMetricsResponseTypeDef",
    {
        "ActivityType": str,
        "ApplicationId": str,
        "JourneyActivityId": str,
        "JourneyId": str,
        "LastEvaluatedTime": str,
        "Metrics": Dict[str, str],
    },
)

_RequiredGetJourneyExecutionMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredGetJourneyExecutionMetricsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
    },
)
_OptionalGetJourneyExecutionMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalGetJourneyExecutionMetricsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": str,
    },
    total=False,
)


class GetJourneyExecutionMetricsRequestRequestTypeDef(
    _RequiredGetJourneyExecutionMetricsRequestRequestTypeDef,
    _OptionalGetJourneyExecutionMetricsRequestRequestTypeDef,
):
    pass


JourneyExecutionMetricsResponseTypeDef = TypedDict(
    "JourneyExecutionMetricsResponseTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
        "LastEvaluatedTime": str,
        "Metrics": Dict[str, str],
    },
)

GetJourneyRequestRequestTypeDef = TypedDict(
    "GetJourneyRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
    },
)

_RequiredGetPushTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetPushTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalGetPushTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetPushTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetPushTemplateRequestRequestTypeDef(
    _RequiredGetPushTemplateRequestRequestTypeDef, _OptionalGetPushTemplateRequestRequestTypeDef
):
    pass


GetRecommenderConfigurationRequestRequestTypeDef = TypedDict(
    "GetRecommenderConfigurationRequestRequestTypeDef",
    {
        "RecommenderId": str,
    },
)

GetRecommenderConfigurationsRequestRequestTypeDef = TypedDict(
    "GetRecommenderConfigurationsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)

_RequiredGetSegmentExportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSegmentExportJobsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
    },
)
_OptionalGetSegmentExportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSegmentExportJobsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetSegmentExportJobsRequestRequestTypeDef(
    _RequiredGetSegmentExportJobsRequestRequestTypeDef,
    _OptionalGetSegmentExportJobsRequestRequestTypeDef,
):
    pass


_RequiredGetSegmentImportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSegmentImportJobsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
    },
)
_OptionalGetSegmentImportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSegmentImportJobsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetSegmentImportJobsRequestRequestTypeDef(
    _RequiredGetSegmentImportJobsRequestRequestTypeDef,
    _OptionalGetSegmentImportJobsRequestRequestTypeDef,
):
    pass


GetSegmentRequestRequestTypeDef = TypedDict(
    "GetSegmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
    },
)

GetSegmentVersionRequestRequestTypeDef = TypedDict(
    "GetSegmentVersionRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
        "Version": str,
    },
)

_RequiredGetSegmentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSegmentVersionsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
    },
)
_OptionalGetSegmentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSegmentVersionsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetSegmentVersionsRequestRequestTypeDef(
    _RequiredGetSegmentVersionsRequestRequestTypeDef,
    _OptionalGetSegmentVersionsRequestRequestTypeDef,
):
    pass


_RequiredGetSegmentsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSegmentsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalGetSegmentsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSegmentsRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class GetSegmentsRequestRequestTypeDef(
    _RequiredGetSegmentsRequestRequestTypeDef, _OptionalGetSegmentsRequestRequestTypeDef
):
    pass


GetSmsChannelRequestRequestTypeDef = TypedDict(
    "GetSmsChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGetSmsTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetSmsTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalGetSmsTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetSmsTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetSmsTemplateRequestRequestTypeDef(
    _RequiredGetSmsTemplateRequestRequestTypeDef, _OptionalGetSmsTemplateRequestRequestTypeDef
):
    pass


_RequiredSMSTemplateResponseTypeDef = TypedDict(
    "_RequiredSMSTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": TemplateTypeType,
    },
)
_OptionalSMSTemplateResponseTypeDef = TypedDict(
    "_OptionalSMSTemplateResponseTypeDef",
    {
        "Arn": str,
        "Body": str,
        "DefaultSubstitutions": str,
        "RecommenderId": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class SMSTemplateResponseTypeDef(
    _RequiredSMSTemplateResponseTypeDef, _OptionalSMSTemplateResponseTypeDef
):
    pass


GetUserEndpointsRequestRequestTypeDef = TypedDict(
    "GetUserEndpointsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "UserId": str,
    },
)

GetVoiceChannelRequestRequestTypeDef = TypedDict(
    "GetVoiceChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGetVoiceTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetVoiceTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
    },
)
_OptionalGetVoiceTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetVoiceTemplateRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetVoiceTemplateRequestRequestTypeDef(
    _RequiredGetVoiceTemplateRequestRequestTypeDef, _OptionalGetVoiceTemplateRequestRequestTypeDef
):
    pass


_RequiredVoiceTemplateResponseTypeDef = TypedDict(
    "_RequiredVoiceTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": TemplateTypeType,
    },
)
_OptionalVoiceTemplateResponseTypeDef = TypedDict(
    "_OptionalVoiceTemplateResponseTypeDef",
    {
        "Arn": str,
        "Body": str,
        "DefaultSubstitutions": str,
        "LanguageCode": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
        "VoiceId": str,
    },
    total=False,
)


class VoiceTemplateResponseTypeDef(
    _RequiredVoiceTemplateResponseTypeDef, _OptionalVoiceTemplateResponseTypeDef
):
    pass


_RequiredImportJobResourceTypeDef = TypedDict(
    "_RequiredImportJobResourceTypeDef",
    {
        "Format": FormatType,
        "RoleArn": str,
        "S3Url": str,
    },
)
_OptionalImportJobResourceTypeDef = TypedDict(
    "_OptionalImportJobResourceTypeDef",
    {
        "DefineSegment": bool,
        "ExternalId": str,
        "RegisterEndpoints": bool,
        "SegmentId": str,
        "SegmentName": str,
    },
    total=False,
)


class ImportJobResourceTypeDef(
    _RequiredImportJobResourceTypeDef, _OptionalImportJobResourceTypeDef
):
    pass


InAppMessageBodyConfigTypeDef = TypedDict(
    "InAppMessageBodyConfigTypeDef",
    {
        "Alignment": AlignmentType,
        "Body": str,
        "TextColor": str,
    },
)

_RequiredOverrideButtonConfigurationTypeDef = TypedDict(
    "_RequiredOverrideButtonConfigurationTypeDef",
    {
        "ButtonAction": ButtonActionType,
    },
)
_OptionalOverrideButtonConfigurationTypeDef = TypedDict(
    "_OptionalOverrideButtonConfigurationTypeDef",
    {
        "Link": str,
    },
    total=False,
)


class OverrideButtonConfigurationTypeDef(
    _RequiredOverrideButtonConfigurationTypeDef, _OptionalOverrideButtonConfigurationTypeDef
):
    pass


InAppMessageHeaderConfigTypeDef = TypedDict(
    "InAppMessageHeaderConfigTypeDef",
    {
        "Alignment": AlignmentType,
        "Header": str,
        "TextColor": str,
    },
)

JourneyChannelSettingsTypeDef = TypedDict(
    "JourneyChannelSettingsTypeDef",
    {
        "ConnectCampaignArn": str,
        "ConnectCampaignExecutionRoleArn": str,
    },
    total=False,
)

JourneyLimitsTypeDef = TypedDict(
    "JourneyLimitsTypeDef",
    {
        "DailyCap": int,
        "EndpointReentryCap": int,
        "MessagesPerSecond": int,
        "EndpointReentryInterval": str,
    },
    total=False,
)

JourneyPushMessageTypeDef = TypedDict(
    "JourneyPushMessageTypeDef",
    {
        "TimeToLive": str,
    },
    total=False,
)

JourneyScheduleTypeDef = TypedDict(
    "JourneyScheduleTypeDef",
    {
        "EndTime": Union[datetime, str],
        "StartTime": Union[datetime, str],
        "Timezone": str,
    },
    total=False,
)

JourneySMSMessageTypeDef = TypedDict(
    "JourneySMSMessageTypeDef",
    {
        "MessageType": MessageTypeType,
        "OriginationNumber": str,
        "SenderId": str,
        "EntityId": str,
        "TemplateId": str,
    },
    total=False,
)

JourneyStateRequestTypeDef = TypedDict(
    "JourneyStateRequestTypeDef",
    {
        "State": StateType,
    },
    total=False,
)

_RequiredListJourneysRequestRequestTypeDef = TypedDict(
    "_RequiredListJourneysRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListJourneysRequestRequestTypeDef = TypedDict(
    "_OptionalListJourneysRequestRequestTypeDef",
    {
        "PageSize": str,
        "Token": str,
    },
    total=False,
)


class ListJourneysRequestRequestTypeDef(
    _RequiredListJourneysRequestRequestTypeDef, _OptionalListJourneysRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

TagsModelTypeDef = TypedDict(
    "TagsModelTypeDef",
    {
        "tags": Dict[str, str],
    },
)

_RequiredListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateVersionsRequestRequestTypeDef",
    {
        "TemplateName": str,
        "TemplateType": str,
    },
)
_OptionalListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": str,
    },
    total=False,
)


class ListTemplateVersionsRequestRequestTypeDef(
    _RequiredListTemplateVersionsRequestRequestTypeDef,
    _OptionalListTemplateVersionsRequestRequestTypeDef,
):
    pass


ListTemplatesRequestRequestTypeDef = TypedDict(
    "ListTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "PageSize": str,
        "Prefix": str,
        "TemplateType": str,
    },
    total=False,
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "Action": ActionType,
        "Body": str,
        "ImageIconUrl": str,
        "ImageSmallIconUrl": str,
        "ImageUrl": str,
        "JsonBody": str,
        "MediaUrl": str,
        "RawContent": str,
        "SilentPush": bool,
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

_RequiredMessageResultTypeDef = TypedDict(
    "_RequiredMessageResultTypeDef",
    {
        "DeliveryStatus": DeliveryStatusType,
        "StatusCode": int,
    },
)
_OptionalMessageResultTypeDef = TypedDict(
    "_OptionalMessageResultTypeDef",
    {
        "MessageId": str,
        "StatusMessage": str,
        "UpdatedToken": str,
    },
    total=False,
)


class MessageResultTypeDef(_RequiredMessageResultTypeDef, _OptionalMessageResultTypeDef):
    pass


NumberValidateRequestTypeDef = TypedDict(
    "NumberValidateRequestTypeDef",
    {
        "IsoCountryCode": str,
        "PhoneNumber": str,
    },
    total=False,
)

NumberValidateResponseTypeDef = TypedDict(
    "NumberValidateResponseTypeDef",
    {
        "Carrier": str,
        "City": str,
        "CleansedPhoneNumberE164": str,
        "CleansedPhoneNumberNational": str,
        "Country": str,
        "CountryCodeIso2": str,
        "CountryCodeNumeric": str,
        "County": str,
        "OriginalCountryCodeIso2": str,
        "OriginalPhoneNumber": str,
        "PhoneType": str,
        "PhoneTypeCode": int,
        "Timezone": str,
        "ZipCode": str,
    },
    total=False,
)

WriteEventStreamTypeDef = TypedDict(
    "WriteEventStreamTypeDef",
    {
        "DestinationStreamArn": str,
        "RoleArn": str,
    },
)

RandomSplitEntryTypeDef = TypedDict(
    "RandomSplitEntryTypeDef",
    {
        "NextActivity": str,
        "Percentage": int,
    },
    total=False,
)

RecencyDimensionTypeDef = TypedDict(
    "RecencyDimensionTypeDef",
    {
        "Duration": DurationType,
        "RecencyType": RecencyTypeType,
    },
)

UpdateAttributesRequestTypeDef = TypedDict(
    "UpdateAttributesRequestTypeDef",
    {
        "Blacklist": Sequence[str],
    },
    total=False,
)

ResultRowValueTypeDef = TypedDict(
    "ResultRowValueTypeDef",
    {
        "Key": str,
        "Type": str,
        "Value": str,
    },
)

SMSChannelRequestTypeDef = TypedDict(
    "SMSChannelRequestTypeDef",
    {
        "Enabled": bool,
        "SenderId": str,
        "ShortCode": str,
    },
    total=False,
)

SegmentConditionTypeDef = TypedDict(
    "SegmentConditionTypeDef",
    {
        "SegmentId": str,
    },
)

_RequiredSegmentReferenceTypeDef = TypedDict(
    "_RequiredSegmentReferenceTypeDef",
    {
        "Id": str,
    },
)
_OptionalSegmentReferenceTypeDef = TypedDict(
    "_OptionalSegmentReferenceTypeDef",
    {
        "Version": int,
    },
    total=False,
)


class SegmentReferenceTypeDef(_RequiredSegmentReferenceTypeDef, _OptionalSegmentReferenceTypeDef):
    pass


_RequiredSegmentImportResourceTypeDef = TypedDict(
    "_RequiredSegmentImportResourceTypeDef",
    {
        "ExternalId": str,
        "Format": FormatType,
        "RoleArn": str,
        "S3Url": str,
        "Size": int,
    },
)
_OptionalSegmentImportResourceTypeDef = TypedDict(
    "_OptionalSegmentImportResourceTypeDef",
    {
        "ChannelCounts": Dict[str, int],
    },
    total=False,
)


class SegmentImportResourceTypeDef(
    _RequiredSegmentImportResourceTypeDef, _OptionalSegmentImportResourceTypeDef
):
    pass


_RequiredSendOTPMessageRequestParametersTypeDef = TypedDict(
    "_RequiredSendOTPMessageRequestParametersTypeDef",
    {
        "BrandName": str,
        "Channel": str,
        "DestinationIdentity": str,
        "OriginationIdentity": str,
        "ReferenceId": str,
    },
)
_OptionalSendOTPMessageRequestParametersTypeDef = TypedDict(
    "_OptionalSendOTPMessageRequestParametersTypeDef",
    {
        "AllowedAttempts": int,
        "CodeLength": int,
        "EntityId": str,
        "Language": str,
        "TemplateId": str,
        "ValidityPeriod": int,
    },
    total=False,
)


class SendOTPMessageRequestParametersTypeDef(
    _RequiredSendOTPMessageRequestParametersTypeDef, _OptionalSendOTPMessageRequestParametersTypeDef
):
    pass


SimpleEmailPartTypeDef = TypedDict(
    "SimpleEmailPartTypeDef",
    {
        "Charset": str,
        "Data": str,
    },
    total=False,
)

TemplateActiveVersionRequestTypeDef = TypedDict(
    "TemplateActiveVersionRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)

TemplateTypeDef = TypedDict(
    "TemplateTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)

_RequiredTemplateResponseTypeDef = TypedDict(
    "_RequiredTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": TemplateTypeType,
    },
)
_OptionalTemplateResponseTypeDef = TypedDict(
    "_OptionalTemplateResponseTypeDef",
    {
        "Arn": str,
        "DefaultSubstitutions": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class TemplateResponseTypeDef(_RequiredTemplateResponseTypeDef, _OptionalTemplateResponseTypeDef):
    pass


_RequiredTemplateVersionResponseTypeDef = TypedDict(
    "_RequiredTemplateVersionResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": str,
    },
)
_OptionalTemplateVersionResponseTypeDef = TypedDict(
    "_OptionalTemplateVersionResponseTypeDef",
    {
        "DefaultSubstitutions": str,
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class TemplateVersionResponseTypeDef(
    _RequiredTemplateVersionResponseTypeDef, _OptionalTemplateVersionResponseTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateRecommenderConfigurationTypeDef = TypedDict(
    "_RequiredUpdateRecommenderConfigurationTypeDef",
    {
        "RecommendationProviderRoleArn": str,
        "RecommendationProviderUri": str,
    },
)
_OptionalUpdateRecommenderConfigurationTypeDef = TypedDict(
    "_OptionalUpdateRecommenderConfigurationTypeDef",
    {
        "Attributes": Mapping[str, str],
        "Description": str,
        "Name": str,
        "RecommendationProviderIdType": str,
        "RecommendationTransformerUri": str,
        "RecommendationsDisplayName": str,
        "RecommendationsPerMessage": int,
    },
    total=False,
)


class UpdateRecommenderConfigurationTypeDef(
    _RequiredUpdateRecommenderConfigurationTypeDef, _OptionalUpdateRecommenderConfigurationTypeDef
):
    pass


VoiceChannelRequestTypeDef = TypedDict(
    "VoiceChannelRequestTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

VerificationResponseTypeDef = TypedDict(
    "VerificationResponseTypeDef",
    {
        "Valid": bool,
    },
    total=False,
)

VerifyOTPMessageRequestParametersTypeDef = TypedDict(
    "VerifyOTPMessageRequestParametersTypeDef",
    {
        "DestinationIdentity": str,
        "Otp": str,
        "ReferenceId": str,
    },
)

UpdateAdmChannelRequestRequestTypeDef = TypedDict(
    "UpdateAdmChannelRequestRequestTypeDef",
    {
        "ADMChannelRequest": ADMChannelRequestTypeDef,
        "ApplicationId": str,
    },
)

UpdateApnsChannelRequestRequestTypeDef = TypedDict(
    "UpdateApnsChannelRequestRequestTypeDef",
    {
        "APNSChannelRequest": APNSChannelRequestTypeDef,
        "ApplicationId": str,
    },
)

UpdateApnsSandboxChannelRequestRequestTypeDef = TypedDict(
    "UpdateApnsSandboxChannelRequestRequestTypeDef",
    {
        "APNSSandboxChannelRequest": APNSSandboxChannelRequestTypeDef,
        "ApplicationId": str,
    },
)

UpdateApnsVoipChannelRequestRequestTypeDef = TypedDict(
    "UpdateApnsVoipChannelRequestRequestTypeDef",
    {
        "APNSVoipChannelRequest": APNSVoipChannelRequestTypeDef,
        "ApplicationId": str,
    },
)

UpdateApnsVoipSandboxChannelRequestRequestTypeDef = TypedDict(
    "UpdateApnsVoipSandboxChannelRequestRequestTypeDef",
    {
        "APNSVoipSandboxChannelRequest": APNSVoipSandboxChannelRequestTypeDef,
        "ApplicationId": str,
    },
)

_RequiredActivitiesResponseTypeDef = TypedDict(
    "_RequiredActivitiesResponseTypeDef",
    {
        "Item": List[ActivityResponseTypeDef],
    },
)
_OptionalActivitiesResponseTypeDef = TypedDict(
    "_OptionalActivitiesResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ActivitiesResponseTypeDef(
    _RequiredActivitiesResponseTypeDef, _OptionalActivitiesResponseTypeDef
):
    pass


ApplicationsResponseTypeDef = TypedDict(
    "ApplicationsResponseTypeDef",
    {
        "Item": List[ApplicationResponseTypeDef],
        "NextToken": str,
    },
    total=False,
)

_RequiredApplicationSettingsResourceTypeDef = TypedDict(
    "_RequiredApplicationSettingsResourceTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalApplicationSettingsResourceTypeDef = TypedDict(
    "_OptionalApplicationSettingsResourceTypeDef",
    {
        "CampaignHook": CampaignHookTypeDef,
        "LastModifiedDate": str,
        "Limits": CampaignLimitsTypeDef,
        "QuietTime": QuietTimeTypeDef,
    },
    total=False,
)


class ApplicationSettingsResourceTypeDef(
    _RequiredApplicationSettingsResourceTypeDef, _OptionalApplicationSettingsResourceTypeDef
):
    pass


WriteApplicationSettingsRequestTypeDef = TypedDict(
    "WriteApplicationSettingsRequestTypeDef",
    {
        "CampaignHook": CampaignHookTypeDef,
        "CloudWatchMetricsEnabled": bool,
        "EventTaggingEnabled": bool,
        "Limits": CampaignLimitsTypeDef,
        "QuietTime": QuietTimeTypeDef,
    },
    total=False,
)

UpdateBaiduChannelRequestRequestTypeDef = TypedDict(
    "UpdateBaiduChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "BaiduChannelRequest": BaiduChannelRequestTypeDef,
    },
)

ChannelsResponseTypeDef = TypedDict(
    "ChannelsResponseTypeDef",
    {
        "Channels": Dict[str, ChannelResponseTypeDef],
    },
)

WaitActivityTypeDef = TypedDict(
    "WaitActivityTypeDef",
    {
        "NextActivity": str,
        "WaitTime": WaitTimeTypeDef,
    },
    total=False,
)

CreateAppRequestRequestTypeDef = TypedDict(
    "CreateAppRequestRequestTypeDef",
    {
        "CreateApplicationRequest": CreateApplicationRequestTypeDef,
    },
)

CreateAppResponseTypeDef = TypedDict(
    "CreateAppResponseTypeDef",
    {
        "ApplicationResponse": ApplicationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAdmChannelResponseTypeDef = TypedDict(
    "DeleteAdmChannelResponseTypeDef",
    {
        "ADMChannelResponse": ADMChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApnsChannelResponseTypeDef = TypedDict(
    "DeleteApnsChannelResponseTypeDef",
    {
        "APNSChannelResponse": APNSChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApnsSandboxChannelResponseTypeDef = TypedDict(
    "DeleteApnsSandboxChannelResponseTypeDef",
    {
        "APNSSandboxChannelResponse": APNSSandboxChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApnsVoipChannelResponseTypeDef = TypedDict(
    "DeleteApnsVoipChannelResponseTypeDef",
    {
        "APNSVoipChannelResponse": APNSVoipChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApnsVoipSandboxChannelResponseTypeDef = TypedDict(
    "DeleteApnsVoipSandboxChannelResponseTypeDef",
    {
        "APNSVoipSandboxChannelResponse": APNSVoipSandboxChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppResponseTypeDef = TypedDict(
    "DeleteAppResponseTypeDef",
    {
        "ApplicationResponse": ApplicationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBaiduChannelResponseTypeDef = TypedDict(
    "DeleteBaiduChannelResponseTypeDef",
    {
        "BaiduChannelResponse": BaiduChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAdmChannelResponseTypeDef = TypedDict(
    "GetAdmChannelResponseTypeDef",
    {
        "ADMChannelResponse": ADMChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApnsChannelResponseTypeDef = TypedDict(
    "GetApnsChannelResponseTypeDef",
    {
        "APNSChannelResponse": APNSChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApnsSandboxChannelResponseTypeDef = TypedDict(
    "GetApnsSandboxChannelResponseTypeDef",
    {
        "APNSSandboxChannelResponse": APNSSandboxChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApnsVoipChannelResponseTypeDef = TypedDict(
    "GetApnsVoipChannelResponseTypeDef",
    {
        "APNSVoipChannelResponse": APNSVoipChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApnsVoipSandboxChannelResponseTypeDef = TypedDict(
    "GetApnsVoipSandboxChannelResponseTypeDef",
    {
        "APNSVoipSandboxChannelResponse": APNSVoipSandboxChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppResponseTypeDef = TypedDict(
    "GetAppResponseTypeDef",
    {
        "ApplicationResponse": ApplicationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBaiduChannelResponseTypeDef = TypedDict(
    "GetBaiduChannelResponseTypeDef",
    {
        "BaiduChannelResponse": BaiduChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveAttributesResponseTypeDef = TypedDict(
    "RemoveAttributesResponseTypeDef",
    {
        "AttributesResource": AttributesResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAdmChannelResponseTypeDef = TypedDict(
    "UpdateAdmChannelResponseTypeDef",
    {
        "ADMChannelResponse": ADMChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApnsChannelResponseTypeDef = TypedDict(
    "UpdateApnsChannelResponseTypeDef",
    {
        "APNSChannelResponse": APNSChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApnsSandboxChannelResponseTypeDef = TypedDict(
    "UpdateApnsSandboxChannelResponseTypeDef",
    {
        "APNSSandboxChannelResponse": APNSSandboxChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApnsVoipChannelResponseTypeDef = TypedDict(
    "UpdateApnsVoipChannelResponseTypeDef",
    {
        "APNSVoipChannelResponse": APNSVoipChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApnsVoipSandboxChannelResponseTypeDef = TypedDict(
    "UpdateApnsVoipSandboxChannelResponseTypeDef",
    {
        "APNSVoipSandboxChannelResponse": APNSVoipSandboxChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBaiduChannelResponseTypeDef = TypedDict(
    "UpdateBaiduChannelResponseTypeDef",
    {
        "BaiduChannelResponse": BaiduChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEmailTemplateRequestRequestTypeDef = TypedDict(
    "CreateEmailTemplateRequestRequestTypeDef",
    {
        "EmailTemplateRequest": EmailTemplateRequestTypeDef,
        "TemplateName": str,
    },
)

_RequiredUpdateEmailTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEmailTemplateRequestRequestTypeDef",
    {
        "EmailTemplateRequest": EmailTemplateRequestTypeDef,
        "TemplateName": str,
    },
)
_OptionalUpdateEmailTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEmailTemplateRequestRequestTypeDef",
    {
        "CreateNewVersion": bool,
        "Version": str,
    },
    total=False,
)


class UpdateEmailTemplateRequestRequestTypeDef(
    _RequiredUpdateEmailTemplateRequestRequestTypeDef,
    _OptionalUpdateEmailTemplateRequestRequestTypeDef,
):
    pass


CreateEmailTemplateResponseTypeDef = TypedDict(
    "CreateEmailTemplateResponseTypeDef",
    {
        "CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePushTemplateResponseTypeDef = TypedDict(
    "CreatePushTemplateResponseTypeDef",
    {
        "CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSmsTemplateResponseTypeDef = TypedDict(
    "CreateSmsTemplateResponseTypeDef",
    {
        "CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVoiceTemplateResponseTypeDef = TypedDict(
    "CreateVoiceTemplateResponseTypeDef",
    {
        "CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExportJobRequestRequestTypeDef = TypedDict(
    "CreateExportJobRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ExportJobRequest": ExportJobRequestTypeDef,
    },
)

CreateImportJobRequestRequestTypeDef = TypedDict(
    "CreateImportJobRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ImportJobRequest": ImportJobRequestTypeDef,
    },
)

CreateInAppTemplateResponseTypeDef = TypedDict(
    "CreateInAppTemplateResponseTypeDef",
    {
        "TemplateCreateMessageBody": TemplateCreateMessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecommenderConfigurationRequestRequestTypeDef = TypedDict(
    "CreateRecommenderConfigurationRequestRequestTypeDef",
    {
        "CreateRecommenderConfiguration": CreateRecommenderConfigurationTypeDef,
    },
)

CreateRecommenderConfigurationResponseTypeDef = TypedDict(
    "CreateRecommenderConfigurationResponseTypeDef",
    {
        "RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRecommenderConfigurationResponseTypeDef = TypedDict(
    "DeleteRecommenderConfigurationResponseTypeDef",
    {
        "RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecommenderConfigurationResponseTypeDef = TypedDict(
    "GetRecommenderConfigurationResponseTypeDef",
    {
        "RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListRecommenderConfigurationsResponseTypeDef = TypedDict(
    "_RequiredListRecommenderConfigurationsResponseTypeDef",
    {
        "Item": List[RecommenderConfigurationResponseTypeDef],
    },
)
_OptionalListRecommenderConfigurationsResponseTypeDef = TypedDict(
    "_OptionalListRecommenderConfigurationsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListRecommenderConfigurationsResponseTypeDef(
    _RequiredListRecommenderConfigurationsResponseTypeDef,
    _OptionalListRecommenderConfigurationsResponseTypeDef,
):
    pass


UpdateRecommenderConfigurationResponseTypeDef = TypedDict(
    "UpdateRecommenderConfigurationResponseTypeDef",
    {
        "RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSmsTemplateRequestRequestTypeDef = TypedDict(
    "CreateSmsTemplateRequestRequestTypeDef",
    {
        "SMSTemplateRequest": SMSTemplateRequestTypeDef,
        "TemplateName": str,
    },
)

_RequiredUpdateSmsTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSmsTemplateRequestRequestTypeDef",
    {
        "SMSTemplateRequest": SMSTemplateRequestTypeDef,
        "TemplateName": str,
    },
)
_OptionalUpdateSmsTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSmsTemplateRequestRequestTypeDef",
    {
        "CreateNewVersion": bool,
        "Version": str,
    },
    total=False,
)


class UpdateSmsTemplateRequestRequestTypeDef(
    _RequiredUpdateSmsTemplateRequestRequestTypeDef, _OptionalUpdateSmsTemplateRequestRequestTypeDef
):
    pass


CreateVoiceTemplateRequestRequestTypeDef = TypedDict(
    "CreateVoiceTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "VoiceTemplateRequest": VoiceTemplateRequestTypeDef,
    },
)

_RequiredUpdateVoiceTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVoiceTemplateRequestRequestTypeDef",
    {
        "TemplateName": str,
        "VoiceTemplateRequest": VoiceTemplateRequestTypeDef,
    },
)
_OptionalUpdateVoiceTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVoiceTemplateRequestRequestTypeDef",
    {
        "CreateNewVersion": bool,
        "Version": str,
    },
    total=False,
)


class UpdateVoiceTemplateRequestRequestTypeDef(
    _RequiredUpdateVoiceTemplateRequestRequestTypeDef,
    _OptionalUpdateVoiceTemplateRequestRequestTypeDef,
):
    pass


CustomMessageActivityTypeDef = TypedDict(
    "CustomMessageActivityTypeDef",
    {
        "DeliveryUri": str,
        "EndpointTypes": Sequence[EndpointTypesElementType],
        "MessageConfig": JourneyCustomMessageTypeDef,
        "NextActivity": str,
        "TemplateName": str,
        "TemplateVersion": str,
    },
    total=False,
)

PushNotificationTemplateRequestTypeDef = TypedDict(
    "PushNotificationTemplateRequestTypeDef",
    {
        "ADM": AndroidPushNotificationTemplateTypeDef,
        "APNS": APNSPushNotificationTemplateTypeDef,
        "Baidu": AndroidPushNotificationTemplateTypeDef,
        "Default": DefaultPushNotificationTemplateTypeDef,
        "DefaultSubstitutions": str,
        "GCM": AndroidPushNotificationTemplateTypeDef,
        "RecommenderId": str,
        "tags": Mapping[str, str],
        "TemplateDescription": str,
    },
    total=False,
)

_RequiredPushNotificationTemplateResponseTypeDef = TypedDict(
    "_RequiredPushNotificationTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": TemplateTypeType,
    },
)
_OptionalPushNotificationTemplateResponseTypeDef = TypedDict(
    "_OptionalPushNotificationTemplateResponseTypeDef",
    {
        "ADM": AndroidPushNotificationTemplateTypeDef,
        "APNS": APNSPushNotificationTemplateTypeDef,
        "Arn": str,
        "Baidu": AndroidPushNotificationTemplateTypeDef,
        "Default": DefaultPushNotificationTemplateTypeDef,
        "DefaultSubstitutions": str,
        "GCM": AndroidPushNotificationTemplateTypeDef,
        "RecommenderId": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class PushNotificationTemplateResponseTypeDef(
    _RequiredPushNotificationTemplateResponseTypeDef,
    _OptionalPushNotificationTemplateResponseTypeDef,
):
    pass


DeleteEmailChannelResponseTypeDef = TypedDict(
    "DeleteEmailChannelResponseTypeDef",
    {
        "EmailChannelResponse": EmailChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEmailChannelResponseTypeDef = TypedDict(
    "GetEmailChannelResponseTypeDef",
    {
        "EmailChannelResponse": EmailChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEmailChannelResponseTypeDef = TypedDict(
    "UpdateEmailChannelResponseTypeDef",
    {
        "EmailChannelResponse": EmailChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEmailTemplateResponseTypeDef = TypedDict(
    "DeleteEmailTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInAppTemplateResponseTypeDef = TypedDict(
    "DeleteInAppTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePushTemplateResponseTypeDef = TypedDict(
    "DeletePushTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSmsTemplateResponseTypeDef = TypedDict(
    "DeleteSmsTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVoiceTemplateResponseTypeDef = TypedDict(
    "DeleteVoiceTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEmailTemplateResponseTypeDef = TypedDict(
    "UpdateEmailTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEndpointResponseTypeDef = TypedDict(
    "UpdateEndpointResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEndpointsBatchResponseTypeDef = TypedDict(
    "UpdateEndpointsBatchResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInAppTemplateResponseTypeDef = TypedDict(
    "UpdateInAppTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePushTemplateResponseTypeDef = TypedDict(
    "UpdatePushTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSmsTemplateResponseTypeDef = TypedDict(
    "UpdateSmsTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateActiveVersionResponseTypeDef = TypedDict(
    "UpdateTemplateActiveVersionResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVoiceTemplateResponseTypeDef = TypedDict(
    "UpdateVoiceTemplateResponseTypeDef",
    {
        "MessageBody": MessageBodyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEventStreamResponseTypeDef = TypedDict(
    "DeleteEventStreamResponseTypeDef",
    {
        "EventStream": EventStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEventStreamResponseTypeDef = TypedDict(
    "GetEventStreamResponseTypeDef",
    {
        "EventStream": EventStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutEventStreamResponseTypeDef = TypedDict(
    "PutEventStreamResponseTypeDef",
    {
        "EventStream": EventStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGcmChannelResponseTypeDef = TypedDict(
    "DeleteGcmChannelResponseTypeDef",
    {
        "GCMChannelResponse": GCMChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGcmChannelResponseTypeDef = TypedDict(
    "GetGcmChannelResponseTypeDef",
    {
        "GCMChannelResponse": GCMChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGcmChannelResponseTypeDef = TypedDict(
    "UpdateGcmChannelResponseTypeDef",
    {
        "GCMChannelResponse": GCMChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSmsChannelResponseTypeDef = TypedDict(
    "DeleteSmsChannelResponseTypeDef",
    {
        "SMSChannelResponse": SMSChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSmsChannelResponseTypeDef = TypedDict(
    "GetSmsChannelResponseTypeDef",
    {
        "SMSChannelResponse": SMSChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSmsChannelResponseTypeDef = TypedDict(
    "UpdateSmsChannelResponseTypeDef",
    {
        "SMSChannelResponse": SMSChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVoiceChannelResponseTypeDef = TypedDict(
    "DeleteVoiceChannelResponseTypeDef",
    {
        "VoiceChannelResponse": VoiceChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVoiceChannelResponseTypeDef = TypedDict(
    "GetVoiceChannelResponseTypeDef",
    {
        "VoiceChannelResponse": VoiceChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVoiceChannelResponseTypeDef = TypedDict(
    "UpdateVoiceChannelResponseTypeDef",
    {
        "VoiceChannelResponse": VoiceChannelResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEmailChannelRequestRequestTypeDef = TypedDict(
    "UpdateEmailChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EmailChannelRequest": EmailChannelRequestTypeDef,
    },
)

EmailMessageActivityTypeDef = TypedDict(
    "EmailMessageActivityTypeDef",
    {
        "MessageConfig": JourneyEmailMessageTypeDef,
        "NextActivity": str,
        "TemplateName": str,
        "TemplateVersion": str,
    },
    total=False,
)

GetEmailTemplateResponseTypeDef = TypedDict(
    "GetEmailTemplateResponseTypeDef",
    {
        "EmailTemplateResponse": EmailTemplateResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointBatchItemTypeDef = TypedDict(
    "EndpointBatchItemTypeDef",
    {
        "Address": str,
        "Attributes": Mapping[str, Sequence[str]],
        "ChannelType": ChannelTypeType,
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Id": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Mapping[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

EndpointRequestTypeDef = TypedDict(
    "EndpointRequestTypeDef",
    {
        "Address": str,
        "Attributes": Mapping[str, Sequence[str]],
        "ChannelType": ChannelTypeType,
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Mapping[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

EndpointResponseTypeDef = TypedDict(
    "EndpointResponseTypeDef",
    {
        "Address": str,
        "ApplicationId": str,
        "Attributes": Dict[str, List[str]],
        "ChannelType": ChannelTypeType,
        "CohortId": str,
        "CreationDate": str,
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Id": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Dict[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

PublicEndpointTypeDef = TypedDict(
    "PublicEndpointTypeDef",
    {
        "Address": str,
        "Attributes": Mapping[str, Sequence[str]],
        "ChannelType": ChannelTypeType,
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Mapping[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

_RequiredSendUsersMessageResponseTypeDef = TypedDict(
    "_RequiredSendUsersMessageResponseTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalSendUsersMessageResponseTypeDef = TypedDict(
    "_OptionalSendUsersMessageResponseTypeDef",
    {
        "RequestId": str,
        "Result": Dict[str, Dict[str, EndpointMessageResultTypeDef]],
    },
    total=False,
)


class SendUsersMessageResponseTypeDef(
    _RequiredSendUsersMessageResponseTypeDef, _OptionalSendUsersMessageResponseTypeDef
):
    pass


EventDimensionsTypeDef = TypedDict(
    "EventDimensionsTypeDef",
    {
        "Attributes": Mapping[str, AttributeDimensionTypeDef],
        "EventType": SetDimensionTypeDef,
        "Metrics": Mapping[str, MetricDimensionTypeDef],
    },
    total=False,
)

SegmentDemographicsTypeDef = TypedDict(
    "SegmentDemographicsTypeDef",
    {
        "AppVersion": SetDimensionTypeDef,
        "Channel": SetDimensionTypeDef,
        "DeviceType": SetDimensionTypeDef,
        "Make": SetDimensionTypeDef,
        "Model": SetDimensionTypeDef,
        "Platform": SetDimensionTypeDef,
    },
    total=False,
)

ItemResponseTypeDef = TypedDict(
    "ItemResponseTypeDef",
    {
        "EndpointItemResponse": EndpointItemResponseTypeDef,
        "EventsItemResponse": Dict[str, EventItemResponseTypeDef],
    },
    total=False,
)

_RequiredEventTypeDef = TypedDict(
    "_RequiredEventTypeDef",
    {
        "EventType": str,
        "Timestamp": str,
    },
)
_OptionalEventTypeDef = TypedDict(
    "_OptionalEventTypeDef",
    {
        "AppPackageName": str,
        "AppTitle": str,
        "AppVersionCode": str,
        "Attributes": Mapping[str, str],
        "ClientSdkVersion": str,
        "Metrics": Mapping[str, float],
        "SdkName": str,
        "Session": SessionTypeDef,
    },
    total=False,
)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass


_RequiredExportJobResponseTypeDef = TypedDict(
    "_RequiredExportJobResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Definition": ExportJobResourceTypeDef,
        "Id": str,
        "JobStatus": JobStatusType,
        "Type": str,
    },
)
_OptionalExportJobResponseTypeDef = TypedDict(
    "_OptionalExportJobResponseTypeDef",
    {
        "CompletedPieces": int,
        "CompletionDate": str,
        "FailedPieces": int,
        "Failures": List[str],
        "TotalFailures": int,
        "TotalPieces": int,
        "TotalProcessed": int,
    },
    total=False,
)


class ExportJobResponseTypeDef(
    _RequiredExportJobResponseTypeDef, _OptionalExportJobResponseTypeDef
):
    pass


UpdateGcmChannelRequestRequestTypeDef = TypedDict(
    "UpdateGcmChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "GCMChannelRequest": GCMChannelRequestTypeDef,
    },
)

_RequiredGPSPointDimensionTypeDef = TypedDict(
    "_RequiredGPSPointDimensionTypeDef",
    {
        "Coordinates": GPSCoordinatesTypeDef,
    },
)
_OptionalGPSPointDimensionTypeDef = TypedDict(
    "_OptionalGPSPointDimensionTypeDef",
    {
        "RangeInKilometers": float,
    },
    total=False,
)


class GPSPointDimensionTypeDef(
    _RequiredGPSPointDimensionTypeDef, _OptionalGPSPointDimensionTypeDef
):
    pass


GetJourneyExecutionActivityMetricsResponseTypeDef = TypedDict(
    "GetJourneyExecutionActivityMetricsResponseTypeDef",
    {
        "JourneyExecutionActivityMetricsResponse": JourneyExecutionActivityMetricsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJourneyExecutionMetricsResponseTypeDef = TypedDict(
    "GetJourneyExecutionMetricsResponseTypeDef",
    {
        "JourneyExecutionMetricsResponse": JourneyExecutionMetricsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSmsTemplateResponseTypeDef = TypedDict(
    "GetSmsTemplateResponseTypeDef",
    {
        "SMSTemplateResponse": SMSTemplateResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVoiceTemplateResponseTypeDef = TypedDict(
    "GetVoiceTemplateResponseTypeDef",
    {
        "VoiceTemplateResponse": VoiceTemplateResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImportJobResponseTypeDef = TypedDict(
    "_RequiredImportJobResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Definition": ImportJobResourceTypeDef,
        "Id": str,
        "JobStatus": JobStatusType,
        "Type": str,
    },
)
_OptionalImportJobResponseTypeDef = TypedDict(
    "_OptionalImportJobResponseTypeDef",
    {
        "CompletedPieces": int,
        "CompletionDate": str,
        "FailedPieces": int,
        "Failures": List[str],
        "TotalFailures": int,
        "TotalPieces": int,
        "TotalProcessed": int,
    },
    total=False,
)


class ImportJobResponseTypeDef(
    _RequiredImportJobResponseTypeDef, _OptionalImportJobResponseTypeDef
):
    pass


InAppMessageButtonTypeDef = TypedDict(
    "InAppMessageButtonTypeDef",
    {
        "Android": OverrideButtonConfigurationTypeDef,
        "DefaultConfig": DefaultButtonConfigurationTypeDef,
        "IOS": OverrideButtonConfigurationTypeDef,
        "Web": OverrideButtonConfigurationTypeDef,
    },
    total=False,
)

PushMessageActivityTypeDef = TypedDict(
    "PushMessageActivityTypeDef",
    {
        "MessageConfig": JourneyPushMessageTypeDef,
        "NextActivity": str,
        "TemplateName": str,
        "TemplateVersion": str,
    },
    total=False,
)

SMSMessageActivityTypeDef = TypedDict(
    "SMSMessageActivityTypeDef",
    {
        "MessageConfig": JourneySMSMessageTypeDef,
        "NextActivity": str,
        "TemplateName": str,
        "TemplateVersion": str,
    },
    total=False,
)

UpdateJourneyStateRequestRequestTypeDef = TypedDict(
    "UpdateJourneyStateRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
        "JourneyStateRequest": JourneyStateRequestTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "TagsModel": TagsModelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagsModel": TagsModelTypeDef,
    },
)

_RequiredMessageResponseTypeDef = TypedDict(
    "_RequiredMessageResponseTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalMessageResponseTypeDef = TypedDict(
    "_OptionalMessageResponseTypeDef",
    {
        "EndpointResult": Dict[str, EndpointMessageResultTypeDef],
        "RequestId": str,
        "Result": Dict[str, MessageResultTypeDef],
    },
    total=False,
)


class MessageResponseTypeDef(_RequiredMessageResponseTypeDef, _OptionalMessageResponseTypeDef):
    pass


PhoneNumberValidateRequestRequestTypeDef = TypedDict(
    "PhoneNumberValidateRequestRequestTypeDef",
    {
        "NumberValidateRequest": NumberValidateRequestTypeDef,
    },
)

PhoneNumberValidateResponseTypeDef = TypedDict(
    "PhoneNumberValidateResponseTypeDef",
    {
        "NumberValidateResponse": NumberValidateResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutEventStreamRequestRequestTypeDef = TypedDict(
    "PutEventStreamRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "WriteEventStream": WriteEventStreamTypeDef,
    },
)

RandomSplitActivityTypeDef = TypedDict(
    "RandomSplitActivityTypeDef",
    {
        "Branches": Sequence[RandomSplitEntryTypeDef],
    },
    total=False,
)

SegmentBehaviorsTypeDef = TypedDict(
    "SegmentBehaviorsTypeDef",
    {
        "Recency": RecencyDimensionTypeDef,
    },
    total=False,
)

RemoveAttributesRequestRequestTypeDef = TypedDict(
    "RemoveAttributesRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "AttributeType": str,
        "UpdateAttributesRequest": UpdateAttributesRequestTypeDef,
    },
)

ResultRowTypeDef = TypedDict(
    "ResultRowTypeDef",
    {
        "GroupedBys": List[ResultRowValueTypeDef],
        "Values": List[ResultRowValueTypeDef],
    },
)

UpdateSmsChannelRequestRequestTypeDef = TypedDict(
    "UpdateSmsChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SMSChannelRequest": SMSChannelRequestTypeDef,
    },
)

SendOTPMessageRequestRequestTypeDef = TypedDict(
    "SendOTPMessageRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SendOTPMessageRequestParameters": SendOTPMessageRequestParametersTypeDef,
    },
)

SimpleEmailTypeDef = TypedDict(
    "SimpleEmailTypeDef",
    {
        "HtmlPart": SimpleEmailPartTypeDef,
        "Subject": SimpleEmailPartTypeDef,
        "TextPart": SimpleEmailPartTypeDef,
    },
    total=False,
)

UpdateTemplateActiveVersionRequestRequestTypeDef = TypedDict(
    "UpdateTemplateActiveVersionRequestRequestTypeDef",
    {
        "TemplateActiveVersionRequest": TemplateActiveVersionRequestTypeDef,
        "TemplateName": str,
        "TemplateType": str,
    },
)

TemplateConfigurationTypeDef = TypedDict(
    "TemplateConfigurationTypeDef",
    {
        "EmailTemplate": TemplateTypeDef,
        "PushTemplate": TemplateTypeDef,
        "SMSTemplate": TemplateTypeDef,
        "VoiceTemplate": TemplateTypeDef,
    },
    total=False,
)

_RequiredTemplatesResponseTypeDef = TypedDict(
    "_RequiredTemplatesResponseTypeDef",
    {
        "Item": List[TemplateResponseTypeDef],
    },
)
_OptionalTemplatesResponseTypeDef = TypedDict(
    "_OptionalTemplatesResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class TemplatesResponseTypeDef(
    _RequiredTemplatesResponseTypeDef, _OptionalTemplatesResponseTypeDef
):
    pass


_RequiredTemplateVersionsResponseTypeDef = TypedDict(
    "_RequiredTemplateVersionsResponseTypeDef",
    {
        "Item": List[TemplateVersionResponseTypeDef],
    },
)
_OptionalTemplateVersionsResponseTypeDef = TypedDict(
    "_OptionalTemplateVersionsResponseTypeDef",
    {
        "Message": str,
        "NextToken": str,
        "RequestID": str,
    },
    total=False,
)


class TemplateVersionsResponseTypeDef(
    _RequiredTemplateVersionsResponseTypeDef, _OptionalTemplateVersionsResponseTypeDef
):
    pass


UpdateRecommenderConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateRecommenderConfigurationRequestRequestTypeDef",
    {
        "RecommenderId": str,
        "UpdateRecommenderConfiguration": UpdateRecommenderConfigurationTypeDef,
    },
)

UpdateVoiceChannelRequestRequestTypeDef = TypedDict(
    "UpdateVoiceChannelRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "VoiceChannelRequest": VoiceChannelRequestTypeDef,
    },
)

VerifyOTPMessageResponseTypeDef = TypedDict(
    "VerifyOTPMessageResponseTypeDef",
    {
        "VerificationResponse": VerificationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyOTPMessageRequestRequestTypeDef = TypedDict(
    "VerifyOTPMessageRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "VerifyOTPMessageRequestParameters": VerifyOTPMessageRequestParametersTypeDef,
    },
)

GetCampaignActivitiesResponseTypeDef = TypedDict(
    "GetCampaignActivitiesResponseTypeDef",
    {
        "ActivitiesResponse": ActivitiesResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppsResponseTypeDef = TypedDict(
    "GetAppsResponseTypeDef",
    {
        "ApplicationsResponse": ApplicationsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationSettingsResponseTypeDef = TypedDict(
    "GetApplicationSettingsResponseTypeDef",
    {
        "ApplicationSettingsResource": ApplicationSettingsResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationSettingsResponseTypeDef = TypedDict(
    "UpdateApplicationSettingsResponseTypeDef",
    {
        "ApplicationSettingsResource": ApplicationSettingsResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationSettingsRequestRequestTypeDef = TypedDict(
    "UpdateApplicationSettingsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "WriteApplicationSettingsRequest": WriteApplicationSettingsRequestTypeDef,
    },
)

GetChannelsResponseTypeDef = TypedDict(
    "GetChannelsResponseTypeDef",
    {
        "ChannelsResponse": ChannelsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecommenderConfigurationsResponseTypeDef = TypedDict(
    "GetRecommenderConfigurationsResponseTypeDef",
    {
        "ListRecommenderConfigurationsResponse": ListRecommenderConfigurationsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePushTemplateRequestRequestTypeDef = TypedDict(
    "CreatePushTemplateRequestRequestTypeDef",
    {
        "PushNotificationTemplateRequest": PushNotificationTemplateRequestTypeDef,
        "TemplateName": str,
    },
)

_RequiredUpdatePushTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePushTemplateRequestRequestTypeDef",
    {
        "PushNotificationTemplateRequest": PushNotificationTemplateRequestTypeDef,
        "TemplateName": str,
    },
)
_OptionalUpdatePushTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePushTemplateRequestRequestTypeDef",
    {
        "CreateNewVersion": bool,
        "Version": str,
    },
    total=False,
)


class UpdatePushTemplateRequestRequestTypeDef(
    _RequiredUpdatePushTemplateRequestRequestTypeDef,
    _OptionalUpdatePushTemplateRequestRequestTypeDef,
):
    pass


GetPushTemplateResponseTypeDef = TypedDict(
    "GetPushTemplateResponseTypeDef",
    {
        "PushNotificationTemplateResponse": PushNotificationTemplateResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointBatchRequestTypeDef = TypedDict(
    "EndpointBatchRequestTypeDef",
    {
        "Item": Sequence[EndpointBatchItemTypeDef],
    },
)

UpdateEndpointRequestRequestTypeDef = TypedDict(
    "UpdateEndpointRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EndpointId": str,
        "EndpointRequest": EndpointRequestTypeDef,
    },
)

DeleteEndpointResponseTypeDef = TypedDict(
    "DeleteEndpointResponseTypeDef",
    {
        "EndpointResponse": EndpointResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointsResponseTypeDef = TypedDict(
    "EndpointsResponseTypeDef",
    {
        "Item": List[EndpointResponseTypeDef],
    },
)

GetEndpointResponseTypeDef = TypedDict(
    "GetEndpointResponseTypeDef",
    {
        "EndpointResponse": EndpointResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendUsersMessagesResponseTypeDef = TypedDict(
    "SendUsersMessagesResponseTypeDef",
    {
        "SendUsersMessageResponse": SendUsersMessageResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CampaignEventFilterTypeDef = TypedDict(
    "CampaignEventFilterTypeDef",
    {
        "Dimensions": EventDimensionsTypeDef,
        "FilterType": FilterTypeType,
    },
)

EventConditionTypeDef = TypedDict(
    "EventConditionTypeDef",
    {
        "Dimensions": EventDimensionsTypeDef,
        "MessageActivity": str,
    },
    total=False,
)

EventFilterTypeDef = TypedDict(
    "EventFilterTypeDef",
    {
        "Dimensions": EventDimensionsTypeDef,
        "FilterType": FilterTypeType,
    },
)

EventsResponseTypeDef = TypedDict(
    "EventsResponseTypeDef",
    {
        "Results": Dict[str, ItemResponseTypeDef],
    },
    total=False,
)

EventsBatchTypeDef = TypedDict(
    "EventsBatchTypeDef",
    {
        "Endpoint": PublicEndpointTypeDef,
        "Events": Mapping[str, EventTypeDef],
    },
)

CreateExportJobResponseTypeDef = TypedDict(
    "CreateExportJobResponseTypeDef",
    {
        "ExportJobResponse": ExportJobResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredExportJobsResponseTypeDef = TypedDict(
    "_RequiredExportJobsResponseTypeDef",
    {
        "Item": List[ExportJobResponseTypeDef],
    },
)
_OptionalExportJobsResponseTypeDef = TypedDict(
    "_OptionalExportJobsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ExportJobsResponseTypeDef(
    _RequiredExportJobsResponseTypeDef, _OptionalExportJobsResponseTypeDef
):
    pass


GetExportJobResponseTypeDef = TypedDict(
    "GetExportJobResponseTypeDef",
    {
        "ExportJobResponse": ExportJobResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SegmentLocationTypeDef = TypedDict(
    "SegmentLocationTypeDef",
    {
        "Country": SetDimensionTypeDef,
        "GPSPoint": GPSPointDimensionTypeDef,
    },
    total=False,
)

CreateImportJobResponseTypeDef = TypedDict(
    "CreateImportJobResponseTypeDef",
    {
        "ImportJobResponse": ImportJobResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetImportJobResponseTypeDef = TypedDict(
    "GetImportJobResponseTypeDef",
    {
        "ImportJobResponse": ImportJobResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImportJobsResponseTypeDef = TypedDict(
    "_RequiredImportJobsResponseTypeDef",
    {
        "Item": List[ImportJobResponseTypeDef],
    },
)
_OptionalImportJobsResponseTypeDef = TypedDict(
    "_OptionalImportJobsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ImportJobsResponseTypeDef(
    _RequiredImportJobsResponseTypeDef, _OptionalImportJobsResponseTypeDef
):
    pass


InAppMessageContentTypeDef = TypedDict(
    "InAppMessageContentTypeDef",
    {
        "BackgroundColor": str,
        "BodyConfig": InAppMessageBodyConfigTypeDef,
        "HeaderConfig": InAppMessageHeaderConfigTypeDef,
        "ImageUrl": str,
        "PrimaryBtn": InAppMessageButtonTypeDef,
        "SecondaryBtn": InAppMessageButtonTypeDef,
    },
    total=False,
)

SendMessagesResponseTypeDef = TypedDict(
    "SendMessagesResponseTypeDef",
    {
        "MessageResponse": MessageResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendOTPMessageResponseTypeDef = TypedDict(
    "SendOTPMessageResponseTypeDef",
    {
        "MessageResponse": MessageResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BaseKpiResultTypeDef = TypedDict(
    "BaseKpiResultTypeDef",
    {
        "Rows": List[ResultRowTypeDef],
    },
)

EmailMessageTypeDef = TypedDict(
    "EmailMessageTypeDef",
    {
        "Body": str,
        "FeedbackForwardingAddress": str,
        "FromAddress": str,
        "RawEmail": RawEmailTypeDef,
        "ReplyToAddresses": Sequence[str],
        "SimpleEmail": SimpleEmailTypeDef,
        "Substitutions": Mapping[str, Sequence[str]],
    },
    total=False,
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "TemplatesResponse": TemplatesResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateVersionsResponseTypeDef = TypedDict(
    "ListTemplateVersionsResponseTypeDef",
    {
        "TemplateVersionsResponse": TemplateVersionsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEndpointsBatchRequestRequestTypeDef = TypedDict(
    "UpdateEndpointsBatchRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EndpointBatchRequest": EndpointBatchRequestTypeDef,
    },
)

DeleteUserEndpointsResponseTypeDef = TypedDict(
    "DeleteUserEndpointsResponseTypeDef",
    {
        "EndpointsResponse": EndpointsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserEndpointsResponseTypeDef = TypedDict(
    "GetUserEndpointsResponseTypeDef",
    {
        "EndpointsResponse": EndpointsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InAppCampaignScheduleTypeDef = TypedDict(
    "InAppCampaignScheduleTypeDef",
    {
        "EndDate": str,
        "EventFilter": CampaignEventFilterTypeDef,
        "QuietTime": QuietTimeTypeDef,
    },
    total=False,
)

_RequiredScheduleTypeDef = TypedDict(
    "_RequiredScheduleTypeDef",
    {
        "StartTime": str,
    },
)
_OptionalScheduleTypeDef = TypedDict(
    "_OptionalScheduleTypeDef",
    {
        "EndTime": str,
        "EventFilter": CampaignEventFilterTypeDef,
        "Frequency": FrequencyType,
        "IsLocalTime": bool,
        "QuietTime": QuietTimeTypeDef,
        "Timezone": str,
    },
    total=False,
)


class ScheduleTypeDef(_RequiredScheduleTypeDef, _OptionalScheduleTypeDef):
    pass


EventStartConditionTypeDef = TypedDict(
    "EventStartConditionTypeDef",
    {
        "EventFilter": EventFilterTypeDef,
        "SegmentId": str,
    },
    total=False,
)

PutEventsResponseTypeDef = TypedDict(
    "PutEventsResponseTypeDef",
    {
        "EventsResponse": EventsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventsRequestTypeDef = TypedDict(
    "EventsRequestTypeDef",
    {
        "BatchItem": Mapping[str, EventsBatchTypeDef],
    },
)

GetExportJobsResponseTypeDef = TypedDict(
    "GetExportJobsResponseTypeDef",
    {
        "ExportJobsResponse": ExportJobsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSegmentExportJobsResponseTypeDef = TypedDict(
    "GetSegmentExportJobsResponseTypeDef",
    {
        "ExportJobsResponse": ExportJobsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SegmentDimensionsTypeDef = TypedDict(
    "SegmentDimensionsTypeDef",
    {
        "Attributes": Mapping[str, AttributeDimensionTypeDef],
        "Behavior": SegmentBehaviorsTypeDef,
        "Demographic": SegmentDemographicsTypeDef,
        "Location": SegmentLocationTypeDef,
        "Metrics": Mapping[str, MetricDimensionTypeDef],
        "UserAttributes": Mapping[str, AttributeDimensionTypeDef],
    },
    total=False,
)

GetImportJobsResponseTypeDef = TypedDict(
    "GetImportJobsResponseTypeDef",
    {
        "ImportJobsResponse": ImportJobsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSegmentImportJobsResponseTypeDef = TypedDict(
    "GetSegmentImportJobsResponseTypeDef",
    {
        "ImportJobsResponse": ImportJobsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CampaignInAppMessageTypeDef = TypedDict(
    "CampaignInAppMessageTypeDef",
    {
        "Body": str,
        "Content": Sequence[InAppMessageContentTypeDef],
        "CustomConfig": Mapping[str, str],
        "Layout": LayoutType,
    },
    total=False,
)

InAppMessageTypeDef = TypedDict(
    "InAppMessageTypeDef",
    {
        "Content": List[InAppMessageContentTypeDef],
        "CustomConfig": Dict[str, str],
        "Layout": LayoutType,
    },
    total=False,
)

InAppTemplateRequestTypeDef = TypedDict(
    "InAppTemplateRequestTypeDef",
    {
        "Content": Sequence[InAppMessageContentTypeDef],
        "CustomConfig": Mapping[str, str],
        "Layout": LayoutType,
        "tags": Mapping[str, str],
        "TemplateDescription": str,
    },
    total=False,
)

_RequiredInAppTemplateResponseTypeDef = TypedDict(
    "_RequiredInAppTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": TemplateTypeType,
    },
)
_OptionalInAppTemplateResponseTypeDef = TypedDict(
    "_OptionalInAppTemplateResponseTypeDef",
    {
        "Arn": str,
        "Content": List[InAppMessageContentTypeDef],
        "CustomConfig": Dict[str, str],
        "Layout": LayoutType,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class InAppTemplateResponseTypeDef(
    _RequiredInAppTemplateResponseTypeDef, _OptionalInAppTemplateResponseTypeDef
):
    pass


_RequiredApplicationDateRangeKpiResponseTypeDef = TypedDict(
    "_RequiredApplicationDateRangeKpiResponseTypeDef",
    {
        "ApplicationId": str,
        "EndTime": datetime,
        "KpiName": str,
        "KpiResult": BaseKpiResultTypeDef,
        "StartTime": datetime,
    },
)
_OptionalApplicationDateRangeKpiResponseTypeDef = TypedDict(
    "_OptionalApplicationDateRangeKpiResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ApplicationDateRangeKpiResponseTypeDef(
    _RequiredApplicationDateRangeKpiResponseTypeDef, _OptionalApplicationDateRangeKpiResponseTypeDef
):
    pass


_RequiredCampaignDateRangeKpiResponseTypeDef = TypedDict(
    "_RequiredCampaignDateRangeKpiResponseTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
        "EndTime": datetime,
        "KpiName": str,
        "KpiResult": BaseKpiResultTypeDef,
        "StartTime": datetime,
    },
)
_OptionalCampaignDateRangeKpiResponseTypeDef = TypedDict(
    "_OptionalCampaignDateRangeKpiResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class CampaignDateRangeKpiResponseTypeDef(
    _RequiredCampaignDateRangeKpiResponseTypeDef, _OptionalCampaignDateRangeKpiResponseTypeDef
):
    pass


_RequiredJourneyDateRangeKpiResponseTypeDef = TypedDict(
    "_RequiredJourneyDateRangeKpiResponseTypeDef",
    {
        "ApplicationId": str,
        "EndTime": datetime,
        "JourneyId": str,
        "KpiName": str,
        "KpiResult": BaseKpiResultTypeDef,
        "StartTime": datetime,
    },
)
_OptionalJourneyDateRangeKpiResponseTypeDef = TypedDict(
    "_OptionalJourneyDateRangeKpiResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class JourneyDateRangeKpiResponseTypeDef(
    _RequiredJourneyDateRangeKpiResponseTypeDef, _OptionalJourneyDateRangeKpiResponseTypeDef
):
    pass


DirectMessageConfigurationTypeDef = TypedDict(
    "DirectMessageConfigurationTypeDef",
    {
        "ADMMessage": ADMMessageTypeDef,
        "APNSMessage": APNSMessageTypeDef,
        "BaiduMessage": BaiduMessageTypeDef,
        "DefaultMessage": DefaultMessageTypeDef,
        "DefaultPushNotificationMessage": DefaultPushNotificationMessageTypeDef,
        "EmailMessage": EmailMessageTypeDef,
        "GCMMessage": GCMMessageTypeDef,
        "SMSMessage": SMSMessageTypeDef,
        "VoiceMessage": VoiceMessageTypeDef,
    },
    total=False,
)

StartConditionTypeDef = TypedDict(
    "StartConditionTypeDef",
    {
        "Description": str,
        "EventStartCondition": EventStartConditionTypeDef,
        "SegmentStartCondition": SegmentConditionTypeDef,
    },
    total=False,
)

PutEventsRequestRequestTypeDef = TypedDict(
    "PutEventsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EventsRequest": EventsRequestTypeDef,
    },
)

SegmentGroupTypeDef = TypedDict(
    "SegmentGroupTypeDef",
    {
        "Dimensions": Sequence[SegmentDimensionsTypeDef],
        "SourceSegments": Sequence[SegmentReferenceTypeDef],
        "SourceType": SourceTypeType,
        "Type": TypeType,
    },
    total=False,
)

SimpleConditionTypeDef = TypedDict(
    "SimpleConditionTypeDef",
    {
        "EventCondition": EventConditionTypeDef,
        "SegmentCondition": SegmentConditionTypeDef,
        "SegmentDimensions": SegmentDimensionsTypeDef,
    },
    total=False,
)

MessageConfigurationTypeDef = TypedDict(
    "MessageConfigurationTypeDef",
    {
        "ADMMessage": MessageTypeDef,
        "APNSMessage": MessageTypeDef,
        "BaiduMessage": MessageTypeDef,
        "CustomMessage": CampaignCustomMessageTypeDef,
        "DefaultMessage": MessageTypeDef,
        "EmailMessage": CampaignEmailMessageTypeDef,
        "GCMMessage": MessageTypeDef,
        "SMSMessage": CampaignSmsMessageTypeDef,
        "InAppMessage": CampaignInAppMessageTypeDef,
    },
    total=False,
)

InAppMessageCampaignTypeDef = TypedDict(
    "InAppMessageCampaignTypeDef",
    {
        "CampaignId": str,
        "DailyCap": int,
        "InAppMessage": InAppMessageTypeDef,
        "Priority": int,
        "Schedule": InAppCampaignScheduleTypeDef,
        "SessionCap": int,
        "TotalCap": int,
        "TreatmentId": str,
    },
    total=False,
)

CreateInAppTemplateRequestRequestTypeDef = TypedDict(
    "CreateInAppTemplateRequestRequestTypeDef",
    {
        "InAppTemplateRequest": InAppTemplateRequestTypeDef,
        "TemplateName": str,
    },
)

_RequiredUpdateInAppTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInAppTemplateRequestRequestTypeDef",
    {
        "InAppTemplateRequest": InAppTemplateRequestTypeDef,
        "TemplateName": str,
    },
)
_OptionalUpdateInAppTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInAppTemplateRequestRequestTypeDef",
    {
        "CreateNewVersion": bool,
        "Version": str,
    },
    total=False,
)


class UpdateInAppTemplateRequestRequestTypeDef(
    _RequiredUpdateInAppTemplateRequestRequestTypeDef,
    _OptionalUpdateInAppTemplateRequestRequestTypeDef,
):
    pass


GetInAppTemplateResponseTypeDef = TypedDict(
    "GetInAppTemplateResponseTypeDef",
    {
        "InAppTemplateResponse": InAppTemplateResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationDateRangeKpiResponseTypeDef = TypedDict(
    "GetApplicationDateRangeKpiResponseTypeDef",
    {
        "ApplicationDateRangeKpiResponse": ApplicationDateRangeKpiResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCampaignDateRangeKpiResponseTypeDef = TypedDict(
    "GetCampaignDateRangeKpiResponseTypeDef",
    {
        "CampaignDateRangeKpiResponse": CampaignDateRangeKpiResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJourneyDateRangeKpiResponseTypeDef = TypedDict(
    "GetJourneyDateRangeKpiResponseTypeDef",
    {
        "JourneyDateRangeKpiResponse": JourneyDateRangeKpiResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMessageRequestTypeDef = TypedDict(
    "_RequiredMessageRequestTypeDef",
    {
        "MessageConfiguration": DirectMessageConfigurationTypeDef,
    },
)
_OptionalMessageRequestTypeDef = TypedDict(
    "_OptionalMessageRequestTypeDef",
    {
        "Addresses": Mapping[str, AddressConfigurationTypeDef],
        "Context": Mapping[str, str],
        "Endpoints": Mapping[str, EndpointSendConfigurationTypeDef],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TraceId": str,
    },
    total=False,
)


class MessageRequestTypeDef(_RequiredMessageRequestTypeDef, _OptionalMessageRequestTypeDef):
    pass


_RequiredSendUsersMessageRequestTypeDef = TypedDict(
    "_RequiredSendUsersMessageRequestTypeDef",
    {
        "MessageConfiguration": DirectMessageConfigurationTypeDef,
        "Users": Mapping[str, EndpointSendConfigurationTypeDef],
    },
)
_OptionalSendUsersMessageRequestTypeDef = TypedDict(
    "_OptionalSendUsersMessageRequestTypeDef",
    {
        "Context": Mapping[str, str],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TraceId": str,
    },
    total=False,
)


class SendUsersMessageRequestTypeDef(
    _RequiredSendUsersMessageRequestTypeDef, _OptionalSendUsersMessageRequestTypeDef
):
    pass


SegmentGroupListTypeDef = TypedDict(
    "SegmentGroupListTypeDef",
    {
        "Groups": Sequence[SegmentGroupTypeDef],
        "Include": IncludeType,
    },
    total=False,
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "Conditions": Sequence[SimpleConditionTypeDef],
        "Operator": OperatorType,
    },
    total=False,
)

MultiConditionalBranchTypeDef = TypedDict(
    "MultiConditionalBranchTypeDef",
    {
        "Condition": SimpleConditionTypeDef,
        "NextActivity": str,
    },
    total=False,
)

_RequiredTreatmentResourceTypeDef = TypedDict(
    "_RequiredTreatmentResourceTypeDef",
    {
        "Id": str,
        "SizePercent": int,
    },
)
_OptionalTreatmentResourceTypeDef = TypedDict(
    "_OptionalTreatmentResourceTypeDef",
    {
        "CustomDeliveryConfiguration": CustomDeliveryConfigurationTypeDef,
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Schedule": ScheduleTypeDef,
        "State": CampaignStateTypeDef,
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
    },
    total=False,
)


class TreatmentResourceTypeDef(
    _RequiredTreatmentResourceTypeDef, _OptionalTreatmentResourceTypeDef
):
    pass


_RequiredWriteTreatmentResourceTypeDef = TypedDict(
    "_RequiredWriteTreatmentResourceTypeDef",
    {
        "SizePercent": int,
    },
)
_OptionalWriteTreatmentResourceTypeDef = TypedDict(
    "_OptionalWriteTreatmentResourceTypeDef",
    {
        "CustomDeliveryConfiguration": CustomDeliveryConfigurationTypeDef,
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Schedule": ScheduleTypeDef,
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
    },
    total=False,
)


class WriteTreatmentResourceTypeDef(
    _RequiredWriteTreatmentResourceTypeDef, _OptionalWriteTreatmentResourceTypeDef
):
    pass


InAppMessagesResponseTypeDef = TypedDict(
    "InAppMessagesResponseTypeDef",
    {
        "InAppMessageCampaigns": List[InAppMessageCampaignTypeDef],
    },
    total=False,
)

SendMessagesRequestRequestTypeDef = TypedDict(
    "SendMessagesRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "MessageRequest": MessageRequestTypeDef,
    },
)

SendUsersMessagesRequestRequestTypeDef = TypedDict(
    "SendUsersMessagesRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SendUsersMessageRequest": SendUsersMessageRequestTypeDef,
    },
)

_RequiredSegmentResponseTypeDef = TypedDict(
    "_RequiredSegmentResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreationDate": str,
        "Id": str,
        "SegmentType": SegmentTypeType,
    },
)
_OptionalSegmentResponseTypeDef = TypedDict(
    "_OptionalSegmentResponseTypeDef",
    {
        "Dimensions": SegmentDimensionsTypeDef,
        "ImportDefinition": SegmentImportResourceTypeDef,
        "LastModifiedDate": str,
        "Name": str,
        "SegmentGroups": SegmentGroupListTypeDef,
        "tags": Dict[str, str],
        "Version": int,
    },
    total=False,
)


class SegmentResponseTypeDef(_RequiredSegmentResponseTypeDef, _OptionalSegmentResponseTypeDef):
    pass


WriteSegmentRequestTypeDef = TypedDict(
    "WriteSegmentRequestTypeDef",
    {
        "Dimensions": SegmentDimensionsTypeDef,
        "Name": str,
        "SegmentGroups": SegmentGroupListTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

ConditionalSplitActivityTypeDef = TypedDict(
    "ConditionalSplitActivityTypeDef",
    {
        "Condition": ConditionTypeDef,
        "EvaluationWaitTime": WaitTimeTypeDef,
        "FalseActivity": str,
        "TrueActivity": str,
    },
    total=False,
)

MultiConditionalSplitActivityTypeDef = TypedDict(
    "MultiConditionalSplitActivityTypeDef",
    {
        "Branches": Sequence[MultiConditionalBranchTypeDef],
        "DefaultActivity": str,
        "EvaluationWaitTime": WaitTimeTypeDef,
    },
    total=False,
)

_RequiredCampaignResponseTypeDef = TypedDict(
    "_RequiredCampaignResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreationDate": str,
        "Id": str,
        "LastModifiedDate": str,
        "SegmentId": str,
        "SegmentVersion": int,
    },
)
_OptionalCampaignResponseTypeDef = TypedDict(
    "_OptionalCampaignResponseTypeDef",
    {
        "AdditionalTreatments": List[TreatmentResourceTypeDef],
        "CustomDeliveryConfiguration": CustomDeliveryConfigurationTypeDef,
        "DefaultState": CampaignStateTypeDef,
        "Description": str,
        "HoldoutPercent": int,
        "Hook": CampaignHookTypeDef,
        "IsPaused": bool,
        "Limits": CampaignLimitsTypeDef,
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Name": str,
        "Schedule": ScheduleTypeDef,
        "State": CampaignStateTypeDef,
        "tags": Dict[str, str],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
        "Version": int,
        "Priority": int,
    },
    total=False,
)


class CampaignResponseTypeDef(_RequiredCampaignResponseTypeDef, _OptionalCampaignResponseTypeDef):
    pass


WriteCampaignRequestTypeDef = TypedDict(
    "WriteCampaignRequestTypeDef",
    {
        "AdditionalTreatments": Sequence[WriteTreatmentResourceTypeDef],
        "CustomDeliveryConfiguration": CustomDeliveryConfigurationTypeDef,
        "Description": str,
        "HoldoutPercent": int,
        "Hook": CampaignHookTypeDef,
        "IsPaused": bool,
        "Limits": CampaignLimitsTypeDef,
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Name": str,
        "Schedule": ScheduleTypeDef,
        "SegmentId": str,
        "SegmentVersion": int,
        "tags": Mapping[str, str],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
        "Priority": int,
    },
    total=False,
)

GetInAppMessagesResponseTypeDef = TypedDict(
    "GetInAppMessagesResponseTypeDef",
    {
        "InAppMessagesResponse": InAppMessagesResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSegmentResponseTypeDef = TypedDict(
    "CreateSegmentResponseTypeDef",
    {
        "SegmentResponse": SegmentResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSegmentResponseTypeDef = TypedDict(
    "DeleteSegmentResponseTypeDef",
    {
        "SegmentResponse": SegmentResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSegmentResponseTypeDef = TypedDict(
    "GetSegmentResponseTypeDef",
    {
        "SegmentResponse": SegmentResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSegmentVersionResponseTypeDef = TypedDict(
    "GetSegmentVersionResponseTypeDef",
    {
        "SegmentResponse": SegmentResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSegmentsResponseTypeDef = TypedDict(
    "_RequiredSegmentsResponseTypeDef",
    {
        "Item": List[SegmentResponseTypeDef],
    },
)
_OptionalSegmentsResponseTypeDef = TypedDict(
    "_OptionalSegmentsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class SegmentsResponseTypeDef(_RequiredSegmentsResponseTypeDef, _OptionalSegmentsResponseTypeDef):
    pass


UpdateSegmentResponseTypeDef = TypedDict(
    "UpdateSegmentResponseTypeDef",
    {
        "SegmentResponse": SegmentResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSegmentRequestRequestTypeDef = TypedDict(
    "CreateSegmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "WriteSegmentRequest": WriteSegmentRequestTypeDef,
    },
)

UpdateSegmentRequestRequestTypeDef = TypedDict(
    "UpdateSegmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SegmentId": str,
        "WriteSegmentRequest": WriteSegmentRequestTypeDef,
    },
)

ActivityTypeDef = TypedDict(
    "ActivityTypeDef",
    {
        "CUSTOM": CustomMessageActivityTypeDef,
        "ConditionalSplit": ConditionalSplitActivityTypeDef,
        "Description": str,
        "EMAIL": EmailMessageActivityTypeDef,
        "Holdout": HoldoutActivityTypeDef,
        "MultiCondition": MultiConditionalSplitActivityTypeDef,
        "PUSH": PushMessageActivityTypeDef,
        "RandomSplit": RandomSplitActivityTypeDef,
        "SMS": SMSMessageActivityTypeDef,
        "Wait": WaitActivityTypeDef,
        "ContactCenter": ContactCenterActivityTypeDef,
    },
    total=False,
)

_RequiredCampaignsResponseTypeDef = TypedDict(
    "_RequiredCampaignsResponseTypeDef",
    {
        "Item": List[CampaignResponseTypeDef],
    },
)
_OptionalCampaignsResponseTypeDef = TypedDict(
    "_OptionalCampaignsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class CampaignsResponseTypeDef(
    _RequiredCampaignsResponseTypeDef, _OptionalCampaignsResponseTypeDef
):
    pass


CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef",
    {
        "CampaignResponse": CampaignResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCampaignResponseTypeDef = TypedDict(
    "DeleteCampaignResponseTypeDef",
    {
        "CampaignResponse": CampaignResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCampaignResponseTypeDef = TypedDict(
    "GetCampaignResponseTypeDef",
    {
        "CampaignResponse": CampaignResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCampaignVersionResponseTypeDef = TypedDict(
    "GetCampaignVersionResponseTypeDef",
    {
        "CampaignResponse": CampaignResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCampaignResponseTypeDef = TypedDict(
    "UpdateCampaignResponseTypeDef",
    {
        "CampaignResponse": CampaignResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCampaignRequestRequestTypeDef = TypedDict(
    "CreateCampaignRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "WriteCampaignRequest": WriteCampaignRequestTypeDef,
    },
)

UpdateCampaignRequestRequestTypeDef = TypedDict(
    "UpdateCampaignRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
        "WriteCampaignRequest": WriteCampaignRequestTypeDef,
    },
)

GetSegmentVersionsResponseTypeDef = TypedDict(
    "GetSegmentVersionsResponseTypeDef",
    {
        "SegmentsResponse": SegmentsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSegmentsResponseTypeDef = TypedDict(
    "GetSegmentsResponseTypeDef",
    {
        "SegmentsResponse": SegmentsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJourneyResponseTypeDef = TypedDict(
    "_RequiredJourneyResponseTypeDef",
    {
        "ApplicationId": str,
        "Id": str,
        "Name": str,
    },
)
_OptionalJourneyResponseTypeDef = TypedDict(
    "_OptionalJourneyResponseTypeDef",
    {
        "Activities": Dict[str, ActivityTypeDef],
        "CreationDate": str,
        "LastModifiedDate": str,
        "Limits": JourneyLimitsTypeDef,
        "LocalTime": bool,
        "QuietTime": QuietTimeTypeDef,
        "RefreshFrequency": str,
        "Schedule": JourneyScheduleTypeDef,
        "StartActivity": str,
        "StartCondition": StartConditionTypeDef,
        "State": StateType,
        "tags": Dict[str, str],
        "WaitForQuietTime": bool,
        "RefreshOnSegmentUpdate": bool,
        "JourneyChannelSettings": JourneyChannelSettingsTypeDef,
    },
    total=False,
)


class JourneyResponseTypeDef(_RequiredJourneyResponseTypeDef, _OptionalJourneyResponseTypeDef):
    pass


_RequiredWriteJourneyRequestTypeDef = TypedDict(
    "_RequiredWriteJourneyRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalWriteJourneyRequestTypeDef = TypedDict(
    "_OptionalWriteJourneyRequestTypeDef",
    {
        "Activities": Mapping[str, ActivityTypeDef],
        "CreationDate": str,
        "LastModifiedDate": str,
        "Limits": JourneyLimitsTypeDef,
        "LocalTime": bool,
        "QuietTime": QuietTimeTypeDef,
        "RefreshFrequency": str,
        "Schedule": JourneyScheduleTypeDef,
        "StartActivity": str,
        "StartCondition": StartConditionTypeDef,
        "State": StateType,
        "WaitForQuietTime": bool,
        "RefreshOnSegmentUpdate": bool,
        "JourneyChannelSettings": JourneyChannelSettingsTypeDef,
    },
    total=False,
)


class WriteJourneyRequestTypeDef(
    _RequiredWriteJourneyRequestTypeDef, _OptionalWriteJourneyRequestTypeDef
):
    pass


GetCampaignVersionsResponseTypeDef = TypedDict(
    "GetCampaignVersionsResponseTypeDef",
    {
        "CampaignsResponse": CampaignsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCampaignsResponseTypeDef = TypedDict(
    "GetCampaignsResponseTypeDef",
    {
        "CampaignsResponse": CampaignsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJourneyResponseTypeDef = TypedDict(
    "CreateJourneyResponseTypeDef",
    {
        "JourneyResponse": JourneyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteJourneyResponseTypeDef = TypedDict(
    "DeleteJourneyResponseTypeDef",
    {
        "JourneyResponse": JourneyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJourneyResponseTypeDef = TypedDict(
    "GetJourneyResponseTypeDef",
    {
        "JourneyResponse": JourneyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJourneysResponseTypeDef = TypedDict(
    "_RequiredJourneysResponseTypeDef",
    {
        "Item": List[JourneyResponseTypeDef],
    },
)
_OptionalJourneysResponseTypeDef = TypedDict(
    "_OptionalJourneysResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class JourneysResponseTypeDef(_RequiredJourneysResponseTypeDef, _OptionalJourneysResponseTypeDef):
    pass


UpdateJourneyResponseTypeDef = TypedDict(
    "UpdateJourneyResponseTypeDef",
    {
        "JourneyResponse": JourneyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJourneyStateResponseTypeDef = TypedDict(
    "UpdateJourneyStateResponseTypeDef",
    {
        "JourneyResponse": JourneyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJourneyRequestRequestTypeDef = TypedDict(
    "CreateJourneyRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "WriteJourneyRequest": WriteJourneyRequestTypeDef,
    },
)

UpdateJourneyRequestRequestTypeDef = TypedDict(
    "UpdateJourneyRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "JourneyId": str,
        "WriteJourneyRequest": WriteJourneyRequestTypeDef,
    },
)

ListJourneysResponseTypeDef = TypedDict(
    "ListJourneysResponseTypeDef",
    {
        "JourneysResponse": JourneysResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
