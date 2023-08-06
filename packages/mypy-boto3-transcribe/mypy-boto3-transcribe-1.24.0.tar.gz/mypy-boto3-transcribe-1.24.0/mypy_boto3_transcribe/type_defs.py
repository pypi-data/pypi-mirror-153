"""
Type annotations for transcribe service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transcribe/type_defs/)

Usage::

    ```python
    from mypy_boto3_transcribe.type_defs import AbsoluteTimeRangeTypeDef

    data: AbsoluteTimeRangeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BaseModelNameType,
    CallAnalyticsJobStatusType,
    CLMLanguageCodeType,
    LanguageCodeType,
    MediaFormatType,
    ModelStatusType,
    OutputLocationTypeType,
    ParticipantRoleType,
    PiiEntityTypeType,
    RedactionOutputType,
    SentimentValueType,
    SubtitleFormatType,
    TranscriptionJobStatusType,
    TypeType,
    VocabularyFilterMethodType,
    VocabularyStateType,
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
    "AbsoluteTimeRangeTypeDef",
    "ContentRedactionTypeDef",
    "LanguageIdSettingsTypeDef",
    "CallAnalyticsJobSummaryTypeDef",
    "ChannelDefinitionTypeDef",
    "MediaTypeDef",
    "TranscriptTypeDef",
    "ResponseMetadataTypeDef",
    "InputDataConfigTypeDef",
    "TagTypeDef",
    "DeleteCallAnalyticsCategoryRequestRequestTypeDef",
    "DeleteCallAnalyticsJobRequestRequestTypeDef",
    "DeleteLanguageModelRequestRequestTypeDef",
    "DeleteMedicalTranscriptionJobRequestRequestTypeDef",
    "DeleteMedicalVocabularyRequestRequestTypeDef",
    "DeleteTranscriptionJobRequestRequestTypeDef",
    "DeleteVocabularyFilterRequestRequestTypeDef",
    "DeleteVocabularyRequestRequestTypeDef",
    "DescribeLanguageModelRequestRequestTypeDef",
    "GetCallAnalyticsCategoryRequestRequestTypeDef",
    "GetCallAnalyticsJobRequestRequestTypeDef",
    "GetMedicalTranscriptionJobRequestRequestTypeDef",
    "GetMedicalVocabularyRequestRequestTypeDef",
    "GetTranscriptionJobRequestRequestTypeDef",
    "GetVocabularyFilterRequestRequestTypeDef",
    "GetVocabularyRequestRequestTypeDef",
    "RelativeTimeRangeTypeDef",
    "JobExecutionSettingsTypeDef",
    "LanguageCodeItemTypeDef",
    "ListCallAnalyticsCategoriesRequestRequestTypeDef",
    "ListCallAnalyticsJobsRequestRequestTypeDef",
    "ListLanguageModelsRequestRequestTypeDef",
    "ListMedicalTranscriptionJobsRequestRequestTypeDef",
    "MedicalTranscriptionJobSummaryTypeDef",
    "ListMedicalVocabulariesRequestRequestTypeDef",
    "VocabularyInfoTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTranscriptionJobsRequestRequestTypeDef",
    "ListVocabulariesRequestRequestTypeDef",
    "ListVocabularyFiltersRequestRequestTypeDef",
    "VocabularyFilterInfoTypeDef",
    "MedicalTranscriptTypeDef",
    "MedicalTranscriptionSettingTypeDef",
    "ModelSettingsTypeDef",
    "SettingsTypeDef",
    "SubtitlesTypeDef",
    "SubtitlesOutputTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateMedicalVocabularyRequestRequestTypeDef",
    "UpdateVocabularyFilterRequestRequestTypeDef",
    "UpdateVocabularyRequestRequestTypeDef",
    "CallAnalyticsJobSettingsTypeDef",
    "CreateMedicalVocabularyResponseTypeDef",
    "CreateVocabularyFilterResponseTypeDef",
    "CreateVocabularyResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetMedicalVocabularyResponseTypeDef",
    "GetVocabularyFilterResponseTypeDef",
    "GetVocabularyResponseTypeDef",
    "ListCallAnalyticsJobsResponseTypeDef",
    "UpdateMedicalVocabularyResponseTypeDef",
    "UpdateVocabularyFilterResponseTypeDef",
    "UpdateVocabularyResponseTypeDef",
    "CreateLanguageModelResponseTypeDef",
    "LanguageModelTypeDef",
    "CreateLanguageModelRequestRequestTypeDef",
    "CreateMedicalVocabularyRequestRequestTypeDef",
    "CreateVocabularyFilterRequestRequestTypeDef",
    "CreateVocabularyRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "InterruptionFilterTypeDef",
    "NonTalkTimeFilterTypeDef",
    "SentimentFilterTypeDef",
    "TranscriptFilterTypeDef",
    "ListMedicalTranscriptionJobsResponseTypeDef",
    "ListMedicalVocabulariesResponseTypeDef",
    "ListVocabulariesResponseTypeDef",
    "ListVocabularyFiltersResponseTypeDef",
    "MedicalTranscriptionJobTypeDef",
    "StartMedicalTranscriptionJobRequestRequestTypeDef",
    "TranscriptionJobSummaryTypeDef",
    "StartTranscriptionJobRequestRequestTypeDef",
    "TranscriptionJobTypeDef",
    "CallAnalyticsJobTypeDef",
    "StartCallAnalyticsJobRequestRequestTypeDef",
    "DescribeLanguageModelResponseTypeDef",
    "ListLanguageModelsResponseTypeDef",
    "RuleTypeDef",
    "GetMedicalTranscriptionJobResponseTypeDef",
    "StartMedicalTranscriptionJobResponseTypeDef",
    "ListTranscriptionJobsResponseTypeDef",
    "GetTranscriptionJobResponseTypeDef",
    "StartTranscriptionJobResponseTypeDef",
    "GetCallAnalyticsJobResponseTypeDef",
    "StartCallAnalyticsJobResponseTypeDef",
    "CategoryPropertiesTypeDef",
    "CreateCallAnalyticsCategoryRequestRequestTypeDef",
    "UpdateCallAnalyticsCategoryRequestRequestTypeDef",
    "CreateCallAnalyticsCategoryResponseTypeDef",
    "GetCallAnalyticsCategoryResponseTypeDef",
    "ListCallAnalyticsCategoriesResponseTypeDef",
    "UpdateCallAnalyticsCategoryResponseTypeDef",
)

AbsoluteTimeRangeTypeDef = TypedDict(
    "AbsoluteTimeRangeTypeDef",
    {
        "StartTime": int,
        "EndTime": int,
        "First": int,
        "Last": int,
    },
    total=False,
)

_RequiredContentRedactionTypeDef = TypedDict(
    "_RequiredContentRedactionTypeDef",
    {
        "RedactionType": Literal["PII"],
        "RedactionOutput": RedactionOutputType,
    },
)
_OptionalContentRedactionTypeDef = TypedDict(
    "_OptionalContentRedactionTypeDef",
    {
        "PiiEntityTypes": List[PiiEntityTypeType],
    },
    total=False,
)


class ContentRedactionTypeDef(_RequiredContentRedactionTypeDef, _OptionalContentRedactionTypeDef):
    pass


LanguageIdSettingsTypeDef = TypedDict(
    "LanguageIdSettingsTypeDef",
    {
        "VocabularyName": str,
        "VocabularyFilterName": str,
        "LanguageModelName": str,
    },
    total=False,
)

CallAnalyticsJobSummaryTypeDef = TypedDict(
    "CallAnalyticsJobSummaryTypeDef",
    {
        "CallAnalyticsJobName": str,
        "CreationTime": datetime,
        "StartTime": datetime,
        "CompletionTime": datetime,
        "LanguageCode": LanguageCodeType,
        "CallAnalyticsJobStatus": CallAnalyticsJobStatusType,
        "FailureReason": str,
    },
    total=False,
)

ChannelDefinitionTypeDef = TypedDict(
    "ChannelDefinitionTypeDef",
    {
        "ChannelId": int,
        "ParticipantRole": ParticipantRoleType,
    },
    total=False,
)

MediaTypeDef = TypedDict(
    "MediaTypeDef",
    {
        "MediaFileUri": str,
        "RedactedMediaFileUri": str,
    },
    total=False,
)

TranscriptTypeDef = TypedDict(
    "TranscriptTypeDef",
    {
        "TranscriptFileUri": str,
        "RedactedTranscriptFileUri": str,
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

_RequiredInputDataConfigTypeDef = TypedDict(
    "_RequiredInputDataConfigTypeDef",
    {
        "S3Uri": str,
        "DataAccessRoleArn": str,
    },
)
_OptionalInputDataConfigTypeDef = TypedDict(
    "_OptionalInputDataConfigTypeDef",
    {
        "TuningDataS3Uri": str,
    },
    total=False,
)


class InputDataConfigTypeDef(_RequiredInputDataConfigTypeDef, _OptionalInputDataConfigTypeDef):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteCallAnalyticsCategoryRequestRequestTypeDef = TypedDict(
    "DeleteCallAnalyticsCategoryRequestRequestTypeDef",
    {
        "CategoryName": str,
    },
)

DeleteCallAnalyticsJobRequestRequestTypeDef = TypedDict(
    "DeleteCallAnalyticsJobRequestRequestTypeDef",
    {
        "CallAnalyticsJobName": str,
    },
)

DeleteLanguageModelRequestRequestTypeDef = TypedDict(
    "DeleteLanguageModelRequestRequestTypeDef",
    {
        "ModelName": str,
    },
)

DeleteMedicalTranscriptionJobRequestRequestTypeDef = TypedDict(
    "DeleteMedicalTranscriptionJobRequestRequestTypeDef",
    {
        "MedicalTranscriptionJobName": str,
    },
)

DeleteMedicalVocabularyRequestRequestTypeDef = TypedDict(
    "DeleteMedicalVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
    },
)

DeleteTranscriptionJobRequestRequestTypeDef = TypedDict(
    "DeleteTranscriptionJobRequestRequestTypeDef",
    {
        "TranscriptionJobName": str,
    },
)

DeleteVocabularyFilterRequestRequestTypeDef = TypedDict(
    "DeleteVocabularyFilterRequestRequestTypeDef",
    {
        "VocabularyFilterName": str,
    },
)

DeleteVocabularyRequestRequestTypeDef = TypedDict(
    "DeleteVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
    },
)

DescribeLanguageModelRequestRequestTypeDef = TypedDict(
    "DescribeLanguageModelRequestRequestTypeDef",
    {
        "ModelName": str,
    },
)

GetCallAnalyticsCategoryRequestRequestTypeDef = TypedDict(
    "GetCallAnalyticsCategoryRequestRequestTypeDef",
    {
        "CategoryName": str,
    },
)

GetCallAnalyticsJobRequestRequestTypeDef = TypedDict(
    "GetCallAnalyticsJobRequestRequestTypeDef",
    {
        "CallAnalyticsJobName": str,
    },
)

GetMedicalTranscriptionJobRequestRequestTypeDef = TypedDict(
    "GetMedicalTranscriptionJobRequestRequestTypeDef",
    {
        "MedicalTranscriptionJobName": str,
    },
)

GetMedicalVocabularyRequestRequestTypeDef = TypedDict(
    "GetMedicalVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
    },
)

GetTranscriptionJobRequestRequestTypeDef = TypedDict(
    "GetTranscriptionJobRequestRequestTypeDef",
    {
        "TranscriptionJobName": str,
    },
)

GetVocabularyFilterRequestRequestTypeDef = TypedDict(
    "GetVocabularyFilterRequestRequestTypeDef",
    {
        "VocabularyFilterName": str,
    },
)

GetVocabularyRequestRequestTypeDef = TypedDict(
    "GetVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
    },
)

RelativeTimeRangeTypeDef = TypedDict(
    "RelativeTimeRangeTypeDef",
    {
        "StartPercentage": int,
        "EndPercentage": int,
        "First": int,
        "Last": int,
    },
    total=False,
)

JobExecutionSettingsTypeDef = TypedDict(
    "JobExecutionSettingsTypeDef",
    {
        "AllowDeferredExecution": bool,
        "DataAccessRoleArn": str,
    },
    total=False,
)

LanguageCodeItemTypeDef = TypedDict(
    "LanguageCodeItemTypeDef",
    {
        "LanguageCode": LanguageCodeType,
        "DurationInSeconds": float,
    },
    total=False,
)

ListCallAnalyticsCategoriesRequestRequestTypeDef = TypedDict(
    "ListCallAnalyticsCategoriesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListCallAnalyticsJobsRequestRequestTypeDef = TypedDict(
    "ListCallAnalyticsJobsRequestRequestTypeDef",
    {
        "Status": CallAnalyticsJobStatusType,
        "JobNameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListLanguageModelsRequestRequestTypeDef = TypedDict(
    "ListLanguageModelsRequestRequestTypeDef",
    {
        "StatusEquals": ModelStatusType,
        "NameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListMedicalTranscriptionJobsRequestRequestTypeDef = TypedDict(
    "ListMedicalTranscriptionJobsRequestRequestTypeDef",
    {
        "Status": TranscriptionJobStatusType,
        "JobNameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MedicalTranscriptionJobSummaryTypeDef = TypedDict(
    "MedicalTranscriptionJobSummaryTypeDef",
    {
        "MedicalTranscriptionJobName": str,
        "CreationTime": datetime,
        "StartTime": datetime,
        "CompletionTime": datetime,
        "LanguageCode": LanguageCodeType,
        "TranscriptionJobStatus": TranscriptionJobStatusType,
        "FailureReason": str,
        "OutputLocationType": OutputLocationTypeType,
        "Specialty": Literal["PRIMARYCARE"],
        "ContentIdentificationType": Literal["PHI"],
        "Type": TypeType,
    },
    total=False,
)

ListMedicalVocabulariesRequestRequestTypeDef = TypedDict(
    "ListMedicalVocabulariesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "StateEquals": VocabularyStateType,
        "NameContains": str,
    },
    total=False,
)

VocabularyInfoTypeDef = TypedDict(
    "VocabularyInfoTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
        "VocabularyState": VocabularyStateType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTranscriptionJobsRequestRequestTypeDef = TypedDict(
    "ListTranscriptionJobsRequestRequestTypeDef",
    {
        "Status": TranscriptionJobStatusType,
        "JobNameContains": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListVocabulariesRequestRequestTypeDef = TypedDict(
    "ListVocabulariesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "StateEquals": VocabularyStateType,
        "NameContains": str,
    },
    total=False,
)

ListVocabularyFiltersRequestRequestTypeDef = TypedDict(
    "ListVocabularyFiltersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "NameContains": str,
    },
    total=False,
)

VocabularyFilterInfoTypeDef = TypedDict(
    "VocabularyFilterInfoTypeDef",
    {
        "VocabularyFilterName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
    },
    total=False,
)

MedicalTranscriptTypeDef = TypedDict(
    "MedicalTranscriptTypeDef",
    {
        "TranscriptFileUri": str,
    },
    total=False,
)

MedicalTranscriptionSettingTypeDef = TypedDict(
    "MedicalTranscriptionSettingTypeDef",
    {
        "ShowSpeakerLabels": bool,
        "MaxSpeakerLabels": int,
        "ChannelIdentification": bool,
        "ShowAlternatives": bool,
        "MaxAlternatives": int,
        "VocabularyName": str,
    },
    total=False,
)

ModelSettingsTypeDef = TypedDict(
    "ModelSettingsTypeDef",
    {
        "LanguageModelName": str,
    },
    total=False,
)

SettingsTypeDef = TypedDict(
    "SettingsTypeDef",
    {
        "VocabularyName": str,
        "ShowSpeakerLabels": bool,
        "MaxSpeakerLabels": int,
        "ChannelIdentification": bool,
        "ShowAlternatives": bool,
        "MaxAlternatives": int,
        "VocabularyFilterName": str,
        "VocabularyFilterMethod": VocabularyFilterMethodType,
    },
    total=False,
)

SubtitlesTypeDef = TypedDict(
    "SubtitlesTypeDef",
    {
        "Formats": Sequence[SubtitleFormatType],
        "OutputStartIndex": int,
    },
    total=False,
)

SubtitlesOutputTypeDef = TypedDict(
    "SubtitlesOutputTypeDef",
    {
        "Formats": List[SubtitleFormatType],
        "SubtitleFileUris": List[str],
        "OutputStartIndex": int,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateMedicalVocabularyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMedicalVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalUpdateMedicalVocabularyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMedicalVocabularyRequestRequestTypeDef",
    {
        "VocabularyFileUri": str,
    },
    total=False,
)


class UpdateMedicalVocabularyRequestRequestTypeDef(
    _RequiredUpdateMedicalVocabularyRequestRequestTypeDef,
    _OptionalUpdateMedicalVocabularyRequestRequestTypeDef,
):
    pass


_RequiredUpdateVocabularyFilterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVocabularyFilterRequestRequestTypeDef",
    {
        "VocabularyFilterName": str,
    },
)
_OptionalUpdateVocabularyFilterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVocabularyFilterRequestRequestTypeDef",
    {
        "Words": Sequence[str],
        "VocabularyFilterFileUri": str,
    },
    total=False,
)


class UpdateVocabularyFilterRequestRequestTypeDef(
    _RequiredUpdateVocabularyFilterRequestRequestTypeDef,
    _OptionalUpdateVocabularyFilterRequestRequestTypeDef,
):
    pass


_RequiredUpdateVocabularyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalUpdateVocabularyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVocabularyRequestRequestTypeDef",
    {
        "Phrases": Sequence[str],
        "VocabularyFileUri": str,
    },
    total=False,
)


class UpdateVocabularyRequestRequestTypeDef(
    _RequiredUpdateVocabularyRequestRequestTypeDef, _OptionalUpdateVocabularyRequestRequestTypeDef
):
    pass


CallAnalyticsJobSettingsTypeDef = TypedDict(
    "CallAnalyticsJobSettingsTypeDef",
    {
        "VocabularyName": str,
        "VocabularyFilterName": str,
        "VocabularyFilterMethod": VocabularyFilterMethodType,
        "LanguageModelName": str,
        "ContentRedaction": ContentRedactionTypeDef,
        "LanguageOptions": List[LanguageCodeType],
        "LanguageIdSettings": Dict[LanguageCodeType, LanguageIdSettingsTypeDef],
    },
    total=False,
)

CreateMedicalVocabularyResponseTypeDef = TypedDict(
    "CreateMedicalVocabularyResponseTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "VocabularyState": VocabularyStateType,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVocabularyFilterResponseTypeDef = TypedDict(
    "CreateVocabularyFilterResponseTypeDef",
    {
        "VocabularyFilterName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVocabularyResponseTypeDef = TypedDict(
    "CreateVocabularyResponseTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "VocabularyState": VocabularyStateType,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMedicalVocabularyResponseTypeDef = TypedDict(
    "GetMedicalVocabularyResponseTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "VocabularyState": VocabularyStateType,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "DownloadUri": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVocabularyFilterResponseTypeDef = TypedDict(
    "GetVocabularyFilterResponseTypeDef",
    {
        "VocabularyFilterName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
        "DownloadUri": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVocabularyResponseTypeDef = TypedDict(
    "GetVocabularyResponseTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "VocabularyState": VocabularyStateType,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "DownloadUri": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCallAnalyticsJobsResponseTypeDef = TypedDict(
    "ListCallAnalyticsJobsResponseTypeDef",
    {
        "Status": CallAnalyticsJobStatusType,
        "NextToken": str,
        "CallAnalyticsJobSummaries": List[CallAnalyticsJobSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMedicalVocabularyResponseTypeDef = TypedDict(
    "UpdateMedicalVocabularyResponseTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
        "VocabularyState": VocabularyStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVocabularyFilterResponseTypeDef = TypedDict(
    "UpdateVocabularyFilterResponseTypeDef",
    {
        "VocabularyFilterName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVocabularyResponseTypeDef = TypedDict(
    "UpdateVocabularyResponseTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "LastModifiedTime": datetime,
        "VocabularyState": VocabularyStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLanguageModelResponseTypeDef = TypedDict(
    "CreateLanguageModelResponseTypeDef",
    {
        "LanguageCode": CLMLanguageCodeType,
        "BaseModelName": BaseModelNameType,
        "ModelName": str,
        "InputDataConfig": InputDataConfigTypeDef,
        "ModelStatus": ModelStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LanguageModelTypeDef = TypedDict(
    "LanguageModelTypeDef",
    {
        "ModelName": str,
        "CreateTime": datetime,
        "LastModifiedTime": datetime,
        "LanguageCode": CLMLanguageCodeType,
        "BaseModelName": BaseModelNameType,
        "ModelStatus": ModelStatusType,
        "UpgradeAvailability": bool,
        "FailureReason": str,
        "InputDataConfig": InputDataConfigTypeDef,
    },
    total=False,
)

_RequiredCreateLanguageModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLanguageModelRequestRequestTypeDef",
    {
        "LanguageCode": CLMLanguageCodeType,
        "BaseModelName": BaseModelNameType,
        "ModelName": str,
        "InputDataConfig": InputDataConfigTypeDef,
    },
)
_OptionalCreateLanguageModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLanguageModelRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateLanguageModelRequestRequestTypeDef(
    _RequiredCreateLanguageModelRequestRequestTypeDef,
    _OptionalCreateLanguageModelRequestRequestTypeDef,
):
    pass


_RequiredCreateMedicalVocabularyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMedicalVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
        "VocabularyFileUri": str,
    },
)
_OptionalCreateMedicalVocabularyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMedicalVocabularyRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMedicalVocabularyRequestRequestTypeDef(
    _RequiredCreateMedicalVocabularyRequestRequestTypeDef,
    _OptionalCreateMedicalVocabularyRequestRequestTypeDef,
):
    pass


_RequiredCreateVocabularyFilterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVocabularyFilterRequestRequestTypeDef",
    {
        "VocabularyFilterName": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalCreateVocabularyFilterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVocabularyFilterRequestRequestTypeDef",
    {
        "Words": Sequence[str],
        "VocabularyFilterFileUri": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateVocabularyFilterRequestRequestTypeDef(
    _RequiredCreateVocabularyFilterRequestRequestTypeDef,
    _OptionalCreateVocabularyFilterRequestRequestTypeDef,
):
    pass


_RequiredCreateVocabularyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVocabularyRequestRequestTypeDef",
    {
        "VocabularyName": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalCreateVocabularyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVocabularyRequestRequestTypeDef",
    {
        "Phrases": Sequence[str],
        "VocabularyFileUri": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateVocabularyRequestRequestTypeDef(
    _RequiredCreateVocabularyRequestRequestTypeDef, _OptionalCreateVocabularyRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceArn": str,
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

InterruptionFilterTypeDef = TypedDict(
    "InterruptionFilterTypeDef",
    {
        "Threshold": int,
        "ParticipantRole": ParticipantRoleType,
        "AbsoluteTimeRange": AbsoluteTimeRangeTypeDef,
        "RelativeTimeRange": RelativeTimeRangeTypeDef,
        "Negate": bool,
    },
    total=False,
)

NonTalkTimeFilterTypeDef = TypedDict(
    "NonTalkTimeFilterTypeDef",
    {
        "Threshold": int,
        "AbsoluteTimeRange": AbsoluteTimeRangeTypeDef,
        "RelativeTimeRange": RelativeTimeRangeTypeDef,
        "Negate": bool,
    },
    total=False,
)

_RequiredSentimentFilterTypeDef = TypedDict(
    "_RequiredSentimentFilterTypeDef",
    {
        "Sentiments": Sequence[SentimentValueType],
    },
)
_OptionalSentimentFilterTypeDef = TypedDict(
    "_OptionalSentimentFilterTypeDef",
    {
        "AbsoluteTimeRange": AbsoluteTimeRangeTypeDef,
        "RelativeTimeRange": RelativeTimeRangeTypeDef,
        "ParticipantRole": ParticipantRoleType,
        "Negate": bool,
    },
    total=False,
)


class SentimentFilterTypeDef(_RequiredSentimentFilterTypeDef, _OptionalSentimentFilterTypeDef):
    pass


_RequiredTranscriptFilterTypeDef = TypedDict(
    "_RequiredTranscriptFilterTypeDef",
    {
        "TranscriptFilterType": Literal["EXACT"],
        "Targets": Sequence[str],
    },
)
_OptionalTranscriptFilterTypeDef = TypedDict(
    "_OptionalTranscriptFilterTypeDef",
    {
        "AbsoluteTimeRange": AbsoluteTimeRangeTypeDef,
        "RelativeTimeRange": RelativeTimeRangeTypeDef,
        "ParticipantRole": ParticipantRoleType,
        "Negate": bool,
    },
    total=False,
)


class TranscriptFilterTypeDef(_RequiredTranscriptFilterTypeDef, _OptionalTranscriptFilterTypeDef):
    pass


ListMedicalTranscriptionJobsResponseTypeDef = TypedDict(
    "ListMedicalTranscriptionJobsResponseTypeDef",
    {
        "Status": TranscriptionJobStatusType,
        "NextToken": str,
        "MedicalTranscriptionJobSummaries": List[MedicalTranscriptionJobSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMedicalVocabulariesResponseTypeDef = TypedDict(
    "ListMedicalVocabulariesResponseTypeDef",
    {
        "Status": VocabularyStateType,
        "NextToken": str,
        "Vocabularies": List[VocabularyInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVocabulariesResponseTypeDef = TypedDict(
    "ListVocabulariesResponseTypeDef",
    {
        "Status": VocabularyStateType,
        "NextToken": str,
        "Vocabularies": List[VocabularyInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVocabularyFiltersResponseTypeDef = TypedDict(
    "ListVocabularyFiltersResponseTypeDef",
    {
        "NextToken": str,
        "VocabularyFilters": List[VocabularyFilterInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MedicalTranscriptionJobTypeDef = TypedDict(
    "MedicalTranscriptionJobTypeDef",
    {
        "MedicalTranscriptionJobName": str,
        "TranscriptionJobStatus": TranscriptionJobStatusType,
        "LanguageCode": LanguageCodeType,
        "MediaSampleRateHertz": int,
        "MediaFormat": MediaFormatType,
        "Media": MediaTypeDef,
        "Transcript": MedicalTranscriptTypeDef,
        "StartTime": datetime,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "FailureReason": str,
        "Settings": MedicalTranscriptionSettingTypeDef,
        "ContentIdentificationType": Literal["PHI"],
        "Specialty": Literal["PRIMARYCARE"],
        "Type": TypeType,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

_RequiredStartMedicalTranscriptionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartMedicalTranscriptionJobRequestRequestTypeDef",
    {
        "MedicalTranscriptionJobName": str,
        "LanguageCode": LanguageCodeType,
        "Media": MediaTypeDef,
        "OutputBucketName": str,
        "Specialty": Literal["PRIMARYCARE"],
        "Type": TypeType,
    },
)
_OptionalStartMedicalTranscriptionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartMedicalTranscriptionJobRequestRequestTypeDef",
    {
        "MediaSampleRateHertz": int,
        "MediaFormat": MediaFormatType,
        "OutputKey": str,
        "OutputEncryptionKMSKeyId": str,
        "KMSEncryptionContext": Mapping[str, str],
        "Settings": MedicalTranscriptionSettingTypeDef,
        "ContentIdentificationType": Literal["PHI"],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class StartMedicalTranscriptionJobRequestRequestTypeDef(
    _RequiredStartMedicalTranscriptionJobRequestRequestTypeDef,
    _OptionalStartMedicalTranscriptionJobRequestRequestTypeDef,
):
    pass


TranscriptionJobSummaryTypeDef = TypedDict(
    "TranscriptionJobSummaryTypeDef",
    {
        "TranscriptionJobName": str,
        "CreationTime": datetime,
        "StartTime": datetime,
        "CompletionTime": datetime,
        "LanguageCode": LanguageCodeType,
        "TranscriptionJobStatus": TranscriptionJobStatusType,
        "FailureReason": str,
        "OutputLocationType": OutputLocationTypeType,
        "ContentRedaction": ContentRedactionTypeDef,
        "ModelSettings": ModelSettingsTypeDef,
        "IdentifyLanguage": bool,
        "IdentifyMultipleLanguages": bool,
        "IdentifiedLanguageScore": float,
        "LanguageCodes": List[LanguageCodeItemTypeDef],
    },
    total=False,
)

_RequiredStartTranscriptionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartTranscriptionJobRequestRequestTypeDef",
    {
        "TranscriptionJobName": str,
        "Media": MediaTypeDef,
    },
)
_OptionalStartTranscriptionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartTranscriptionJobRequestRequestTypeDef",
    {
        "LanguageCode": LanguageCodeType,
        "MediaSampleRateHertz": int,
        "MediaFormat": MediaFormatType,
        "OutputBucketName": str,
        "OutputKey": str,
        "OutputEncryptionKMSKeyId": str,
        "KMSEncryptionContext": Mapping[str, str],
        "Settings": SettingsTypeDef,
        "ModelSettings": ModelSettingsTypeDef,
        "JobExecutionSettings": JobExecutionSettingsTypeDef,
        "ContentRedaction": ContentRedactionTypeDef,
        "IdentifyLanguage": bool,
        "IdentifyMultipleLanguages": bool,
        "LanguageOptions": Sequence[LanguageCodeType],
        "Subtitles": SubtitlesTypeDef,
        "Tags": Sequence[TagTypeDef],
        "LanguageIdSettings": Mapping[LanguageCodeType, LanguageIdSettingsTypeDef],
    },
    total=False,
)


class StartTranscriptionJobRequestRequestTypeDef(
    _RequiredStartTranscriptionJobRequestRequestTypeDef,
    _OptionalStartTranscriptionJobRequestRequestTypeDef,
):
    pass


TranscriptionJobTypeDef = TypedDict(
    "TranscriptionJobTypeDef",
    {
        "TranscriptionJobName": str,
        "TranscriptionJobStatus": TranscriptionJobStatusType,
        "LanguageCode": LanguageCodeType,
        "MediaSampleRateHertz": int,
        "MediaFormat": MediaFormatType,
        "Media": MediaTypeDef,
        "Transcript": TranscriptTypeDef,
        "StartTime": datetime,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "FailureReason": str,
        "Settings": SettingsTypeDef,
        "ModelSettings": ModelSettingsTypeDef,
        "JobExecutionSettings": JobExecutionSettingsTypeDef,
        "ContentRedaction": ContentRedactionTypeDef,
        "IdentifyLanguage": bool,
        "IdentifyMultipleLanguages": bool,
        "LanguageOptions": List[LanguageCodeType],
        "IdentifiedLanguageScore": float,
        "LanguageCodes": List[LanguageCodeItemTypeDef],
        "Tags": List[TagTypeDef],
        "Subtitles": SubtitlesOutputTypeDef,
        "LanguageIdSettings": Dict[LanguageCodeType, LanguageIdSettingsTypeDef],
    },
    total=False,
)

CallAnalyticsJobTypeDef = TypedDict(
    "CallAnalyticsJobTypeDef",
    {
        "CallAnalyticsJobName": str,
        "CallAnalyticsJobStatus": CallAnalyticsJobStatusType,
        "LanguageCode": LanguageCodeType,
        "MediaSampleRateHertz": int,
        "MediaFormat": MediaFormatType,
        "Media": MediaTypeDef,
        "Transcript": TranscriptTypeDef,
        "StartTime": datetime,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "FailureReason": str,
        "DataAccessRoleArn": str,
        "IdentifiedLanguageScore": float,
        "Settings": CallAnalyticsJobSettingsTypeDef,
        "ChannelDefinitions": List[ChannelDefinitionTypeDef],
    },
    total=False,
)

_RequiredStartCallAnalyticsJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartCallAnalyticsJobRequestRequestTypeDef",
    {
        "CallAnalyticsJobName": str,
        "Media": MediaTypeDef,
    },
)
_OptionalStartCallAnalyticsJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartCallAnalyticsJobRequestRequestTypeDef",
    {
        "OutputLocation": str,
        "OutputEncryptionKMSKeyId": str,
        "DataAccessRoleArn": str,
        "Settings": CallAnalyticsJobSettingsTypeDef,
        "ChannelDefinitions": Sequence[ChannelDefinitionTypeDef],
    },
    total=False,
)


class StartCallAnalyticsJobRequestRequestTypeDef(
    _RequiredStartCallAnalyticsJobRequestRequestTypeDef,
    _OptionalStartCallAnalyticsJobRequestRequestTypeDef,
):
    pass


DescribeLanguageModelResponseTypeDef = TypedDict(
    "DescribeLanguageModelResponseTypeDef",
    {
        "LanguageModel": LanguageModelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLanguageModelsResponseTypeDef = TypedDict(
    "ListLanguageModelsResponseTypeDef",
    {
        "NextToken": str,
        "Models": List[LanguageModelTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "NonTalkTimeFilter": NonTalkTimeFilterTypeDef,
        "InterruptionFilter": InterruptionFilterTypeDef,
        "TranscriptFilter": TranscriptFilterTypeDef,
        "SentimentFilter": SentimentFilterTypeDef,
    },
    total=False,
)

GetMedicalTranscriptionJobResponseTypeDef = TypedDict(
    "GetMedicalTranscriptionJobResponseTypeDef",
    {
        "MedicalTranscriptionJob": MedicalTranscriptionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMedicalTranscriptionJobResponseTypeDef = TypedDict(
    "StartMedicalTranscriptionJobResponseTypeDef",
    {
        "MedicalTranscriptionJob": MedicalTranscriptionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTranscriptionJobsResponseTypeDef = TypedDict(
    "ListTranscriptionJobsResponseTypeDef",
    {
        "Status": TranscriptionJobStatusType,
        "NextToken": str,
        "TranscriptionJobSummaries": List[TranscriptionJobSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTranscriptionJobResponseTypeDef = TypedDict(
    "GetTranscriptionJobResponseTypeDef",
    {
        "TranscriptionJob": TranscriptionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTranscriptionJobResponseTypeDef = TypedDict(
    "StartTranscriptionJobResponseTypeDef",
    {
        "TranscriptionJob": TranscriptionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCallAnalyticsJobResponseTypeDef = TypedDict(
    "GetCallAnalyticsJobResponseTypeDef",
    {
        "CallAnalyticsJob": CallAnalyticsJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartCallAnalyticsJobResponseTypeDef = TypedDict(
    "StartCallAnalyticsJobResponseTypeDef",
    {
        "CallAnalyticsJob": CallAnalyticsJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CategoryPropertiesTypeDef = TypedDict(
    "CategoryPropertiesTypeDef",
    {
        "CategoryName": str,
        "Rules": List[RuleTypeDef],
        "CreateTime": datetime,
        "LastUpdateTime": datetime,
    },
    total=False,
)

CreateCallAnalyticsCategoryRequestRequestTypeDef = TypedDict(
    "CreateCallAnalyticsCategoryRequestRequestTypeDef",
    {
        "CategoryName": str,
        "Rules": Sequence[RuleTypeDef],
    },
)

UpdateCallAnalyticsCategoryRequestRequestTypeDef = TypedDict(
    "UpdateCallAnalyticsCategoryRequestRequestTypeDef",
    {
        "CategoryName": str,
        "Rules": Sequence[RuleTypeDef],
    },
)

CreateCallAnalyticsCategoryResponseTypeDef = TypedDict(
    "CreateCallAnalyticsCategoryResponseTypeDef",
    {
        "CategoryProperties": CategoryPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCallAnalyticsCategoryResponseTypeDef = TypedDict(
    "GetCallAnalyticsCategoryResponseTypeDef",
    {
        "CategoryProperties": CategoryPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCallAnalyticsCategoriesResponseTypeDef = TypedDict(
    "ListCallAnalyticsCategoriesResponseTypeDef",
    {
        "NextToken": str,
        "Categories": List[CategoryPropertiesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCallAnalyticsCategoryResponseTypeDef = TypedDict(
    "UpdateCallAnalyticsCategoryResponseTypeDef",
    {
        "CategoryProperties": CategoryPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
