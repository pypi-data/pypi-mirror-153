"""
Type annotations for rekognition service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/type_defs/)

Usage::

    ```python
    from mypy_boto3_rekognition.type_defs import AgeRangeTypeDef

    data: AgeRangeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AttributeType,
    BodyPartType,
    CelebrityRecognitionSortByType,
    ContentClassifierType,
    ContentModerationSortByType,
    DatasetStatusMessageCodeType,
    DatasetStatusType,
    DatasetTypeType,
    EmotionNameType,
    FaceAttributesType,
    FaceSearchSortByType,
    GenderTypeType,
    KnownGenderTypeType,
    LabelDetectionSortByType,
    LandmarkTypeType,
    OrientationCorrectionType,
    PersonTrackingSortByType,
    ProjectStatusType,
    ProjectVersionStatusType,
    ProtectiveEquipmentTypeType,
    QualityFilterType,
    ReasonType,
    SegmentTypeType,
    StreamProcessorParameterToDeleteType,
    StreamProcessorStatusType,
    TechnicalCueTypeType,
    TextTypesType,
    VideoColorRangeType,
    VideoJobStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AgeRangeTypeDef",
    "AudioMetadataTypeDef",
    "BeardTypeDef",
    "BlackFrameTypeDef",
    "BoundingBoxTypeDef",
    "KnownGenderTypeDef",
    "ResponseMetadataTypeDef",
    "EmotionTypeDef",
    "ImageQualityTypeDef",
    "LandmarkTypeDef",
    "PoseTypeDef",
    "SmileTypeDef",
    "ConnectedHomeSettingsForUpdateTypeDef",
    "ConnectedHomeSettingsTypeDef",
    "ModerationLabelTypeDef",
    "CoversBodyPartTypeDef",
    "CreateCollectionRequestRequestTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "OutputConfigTypeDef",
    "StreamProcessorDataSharingPreferenceTypeDef",
    "StreamProcessorNotificationChannelTypeDef",
    "DatasetChangesTypeDef",
    "DatasetStatsTypeDef",
    "DatasetLabelStatsTypeDef",
    "DatasetMetadataTypeDef",
    "DeleteCollectionRequestRequestTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteFacesRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteProjectVersionRequestRequestTypeDef",
    "DeleteStreamProcessorRequestRequestTypeDef",
    "DescribeCollectionRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "WaiterConfigTypeDef",
    "DescribeProjectVersionsRequestRequestTypeDef",
    "DescribeProjectsRequestRequestTypeDef",
    "DescribeStreamProcessorRequestRequestTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "ProtectiveEquipmentSummarizationAttributesTypeDef",
    "ProtectiveEquipmentSummaryTypeDef",
    "DetectionFilterTypeDef",
    "DistributeDatasetTypeDef",
    "EyeOpenTypeDef",
    "EyeglassesTypeDef",
    "GenderTypeDef",
    "MouthOpenTypeDef",
    "MustacheTypeDef",
    "SunglassesTypeDef",
    "FaceSearchSettingsTypeDef",
    "PointTypeDef",
    "GetCelebrityInfoRequestRequestTypeDef",
    "GetCelebrityRecognitionRequestRequestTypeDef",
    "VideoMetadataTypeDef",
    "GetContentModerationRequestRequestTypeDef",
    "GetFaceDetectionRequestRequestTypeDef",
    "GetFaceSearchRequestRequestTypeDef",
    "GetLabelDetectionRequestRequestTypeDef",
    "GetPersonTrackingRequestRequestTypeDef",
    "GetSegmentDetectionRequestRequestTypeDef",
    "SegmentTypeInfoTypeDef",
    "GetTextDetectionRequestRequestTypeDef",
    "S3ObjectTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "KinesisDataStreamTypeDef",
    "KinesisVideoStreamStartSelectorTypeDef",
    "KinesisVideoStreamTypeDef",
    "ParentTypeDef",
    "ListCollectionsRequestRequestTypeDef",
    "ListDatasetEntriesRequestRequestTypeDef",
    "ListDatasetLabelsRequestRequestTypeDef",
    "ListFacesRequestRequestTypeDef",
    "ListStreamProcessorsRequestRequestTypeDef",
    "StreamProcessorTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "NotificationChannelTypeDef",
    "S3DestinationTypeDef",
    "SearchFacesRequestRequestTypeDef",
    "ShotSegmentTypeDef",
    "TechnicalCueSegmentTypeDef",
    "StartProjectVersionRequestRequestTypeDef",
    "StartShotDetectionFilterTypeDef",
    "StreamProcessingStopSelectorTypeDef",
    "StopProjectVersionRequestRequestTypeDef",
    "StopStreamProcessorRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "StartTechnicalCueDetectionFilterTypeDef",
    "ComparedSourceImageFaceTypeDef",
    "FaceTypeDef",
    "InstanceTypeDef",
    "CreateCollectionResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateProjectVersionResponseTypeDef",
    "CreateStreamProcessorResponseTypeDef",
    "DeleteCollectionResponseTypeDef",
    "DeleteFacesResponseTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteProjectVersionResponseTypeDef",
    "DescribeCollectionResponseTypeDef",
    "GetCelebrityInfoResponseTypeDef",
    "ListCollectionsResponseTypeDef",
    "ListDatasetEntriesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartCelebrityRecognitionResponseTypeDef",
    "StartContentModerationResponseTypeDef",
    "StartFaceDetectionResponseTypeDef",
    "StartFaceSearchResponseTypeDef",
    "StartLabelDetectionResponseTypeDef",
    "StartPersonTrackingResponseTypeDef",
    "StartProjectVersionResponseTypeDef",
    "StartSegmentDetectionResponseTypeDef",
    "StartStreamProcessorResponseTypeDef",
    "StartTextDetectionResponseTypeDef",
    "StopProjectVersionResponseTypeDef",
    "ComparedFaceTypeDef",
    "StreamProcessorSettingsForUpdateTypeDef",
    "ContentModerationDetectionTypeDef",
    "EquipmentDetectionTypeDef",
    "UpdateDatasetEntriesRequestRequestTypeDef",
    "DatasetDescriptionTypeDef",
    "DatasetLabelDescriptionTypeDef",
    "ProjectDescriptionTypeDef",
    "DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef",
    "DescribeProjectsRequestDescribeProjectsPaginateTypeDef",
    "ListCollectionsRequestListCollectionsPaginateTypeDef",
    "ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    "ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef",
    "ListFacesRequestListFacesPaginateTypeDef",
    "ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef",
    "DescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef",
    "DescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef",
    "DetectModerationLabelsResponseTypeDef",
    "DistributeDatasetEntriesRequestRequestTypeDef",
    "FaceDetailTypeDef",
    "StreamProcessorSettingsTypeDef",
    "GeometryTypeDef",
    "RegionOfInterestTypeDef",
    "GroundTruthManifestTypeDef",
    "ImageTypeDef",
    "SummaryTypeDef",
    "VideoTypeDef",
    "HumanLoopConfigTypeDef",
    "StreamProcessingStartSelectorTypeDef",
    "StreamProcessorInputTypeDef",
    "ListStreamProcessorsResponseTypeDef",
    "StreamProcessorOutputTypeDef",
    "SegmentDetectionTypeDef",
    "StartSegmentDetectionFiltersTypeDef",
    "FaceMatchTypeDef",
    "ListFacesResponseTypeDef",
    "LabelTypeDef",
    "CelebrityTypeDef",
    "CompareFacesMatchTypeDef",
    "GetContentModerationResponseTypeDef",
    "ProtectiveEquipmentBodyPartTypeDef",
    "DescribeDatasetResponseTypeDef",
    "ListDatasetLabelsResponseTypeDef",
    "DescribeProjectsResponseTypeDef",
    "CelebrityDetailTypeDef",
    "DetectFacesResponseTypeDef",
    "FaceDetectionTypeDef",
    "FaceRecordTypeDef",
    "PersonDetailTypeDef",
    "UnindexedFaceTypeDef",
    "CustomLabelTypeDef",
    "TextDetectionTypeDef",
    "DetectTextFiltersTypeDef",
    "StartTextDetectionFiltersTypeDef",
    "UpdateStreamProcessorRequestRequestTypeDef",
    "AssetTypeDef",
    "DatasetSourceTypeDef",
    "CompareFacesRequestRequestTypeDef",
    "DetectCustomLabelsRequestRequestTypeDef",
    "DetectFacesRequestRequestTypeDef",
    "DetectLabelsRequestRequestTypeDef",
    "DetectProtectiveEquipmentRequestRequestTypeDef",
    "IndexFacesRequestRequestTypeDef",
    "RecognizeCelebritiesRequestRequestTypeDef",
    "SearchFacesByImageRequestRequestTypeDef",
    "EvaluationResultTypeDef",
    "StartCelebrityRecognitionRequestRequestTypeDef",
    "StartContentModerationRequestRequestTypeDef",
    "StartFaceDetectionRequestRequestTypeDef",
    "StartFaceSearchRequestRequestTypeDef",
    "StartLabelDetectionRequestRequestTypeDef",
    "StartPersonTrackingRequestRequestTypeDef",
    "DetectModerationLabelsRequestRequestTypeDef",
    "StartStreamProcessorRequestRequestTypeDef",
    "CreateStreamProcessorRequestRequestTypeDef",
    "DescribeStreamProcessorResponseTypeDef",
    "GetSegmentDetectionResponseTypeDef",
    "StartSegmentDetectionRequestRequestTypeDef",
    "SearchFacesByImageResponseTypeDef",
    "SearchFacesResponseTypeDef",
    "DetectLabelsResponseTypeDef",
    "LabelDetectionTypeDef",
    "RecognizeCelebritiesResponseTypeDef",
    "CompareFacesResponseTypeDef",
    "ProtectiveEquipmentPersonTypeDef",
    "CelebrityRecognitionTypeDef",
    "GetFaceDetectionResponseTypeDef",
    "PersonDetectionTypeDef",
    "PersonMatchTypeDef",
    "IndexFacesResponseTypeDef",
    "DetectCustomLabelsResponseTypeDef",
    "DetectTextResponseTypeDef",
    "TextDetectionResultTypeDef",
    "DetectTextRequestRequestTypeDef",
    "StartTextDetectionRequestRequestTypeDef",
    "TestingDataTypeDef",
    "TrainingDataTypeDef",
    "ValidationDataTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "GetLabelDetectionResponseTypeDef",
    "DetectProtectiveEquipmentResponseTypeDef",
    "GetCelebrityRecognitionResponseTypeDef",
    "GetPersonTrackingResponseTypeDef",
    "GetFaceSearchResponseTypeDef",
    "GetTextDetectionResponseTypeDef",
    "CreateProjectVersionRequestRequestTypeDef",
    "TestingDataResultTypeDef",
    "TrainingDataResultTypeDef",
    "ProjectVersionDescriptionTypeDef",
    "DescribeProjectVersionsResponseTypeDef",
)

AgeRangeTypeDef = TypedDict(
    "AgeRangeTypeDef",
    {
        "Low": int,
        "High": int,
    },
    total=False,
)

AudioMetadataTypeDef = TypedDict(
    "AudioMetadataTypeDef",
    {
        "Codec": str,
        "DurationMillis": int,
        "SampleRate": int,
        "NumberOfChannels": int,
    },
    total=False,
)

BeardTypeDef = TypedDict(
    "BeardTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

BlackFrameTypeDef = TypedDict(
    "BlackFrameTypeDef",
    {
        "MaxPixelThreshold": float,
        "MinCoveragePercentage": float,
    },
    total=False,
)

BoundingBoxTypeDef = TypedDict(
    "BoundingBoxTypeDef",
    {
        "Width": float,
        "Height": float,
        "Left": float,
        "Top": float,
    },
    total=False,
)

KnownGenderTypeDef = TypedDict(
    "KnownGenderTypeDef",
    {
        "Type": KnownGenderTypeType,
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

EmotionTypeDef = TypedDict(
    "EmotionTypeDef",
    {
        "Type": EmotionNameType,
        "Confidence": float,
    },
    total=False,
)

ImageQualityTypeDef = TypedDict(
    "ImageQualityTypeDef",
    {
        "Brightness": float,
        "Sharpness": float,
    },
    total=False,
)

LandmarkTypeDef = TypedDict(
    "LandmarkTypeDef",
    {
        "Type": LandmarkTypeType,
        "X": float,
        "Y": float,
    },
    total=False,
)

PoseTypeDef = TypedDict(
    "PoseTypeDef",
    {
        "Roll": float,
        "Yaw": float,
        "Pitch": float,
    },
    total=False,
)

SmileTypeDef = TypedDict(
    "SmileTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

ConnectedHomeSettingsForUpdateTypeDef = TypedDict(
    "ConnectedHomeSettingsForUpdateTypeDef",
    {
        "Labels": Sequence[str],
        "MinConfidence": float,
    },
    total=False,
)

_RequiredConnectedHomeSettingsTypeDef = TypedDict(
    "_RequiredConnectedHomeSettingsTypeDef",
    {
        "Labels": Sequence[str],
    },
)
_OptionalConnectedHomeSettingsTypeDef = TypedDict(
    "_OptionalConnectedHomeSettingsTypeDef",
    {
        "MinConfidence": float,
    },
    total=False,
)


class ConnectedHomeSettingsTypeDef(
    _RequiredConnectedHomeSettingsTypeDef, _OptionalConnectedHomeSettingsTypeDef
):
    pass


ModerationLabelTypeDef = TypedDict(
    "ModerationLabelTypeDef",
    {
        "Confidence": float,
        "Name": str,
        "ParentName": str,
    },
    total=False,
)

CoversBodyPartTypeDef = TypedDict(
    "CoversBodyPartTypeDef",
    {
        "Confidence": float,
        "Value": bool,
    },
    total=False,
)

_RequiredCreateCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCollectionRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalCreateCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCollectionRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateCollectionRequestRequestTypeDef(
    _RequiredCreateCollectionRequestRequestTypeDef, _OptionalCreateCollectionRequestRequestTypeDef
):
    pass


CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)

OutputConfigTypeDef = TypedDict(
    "OutputConfigTypeDef",
    {
        "S3Bucket": str,
        "S3KeyPrefix": str,
    },
    total=False,
)

StreamProcessorDataSharingPreferenceTypeDef = TypedDict(
    "StreamProcessorDataSharingPreferenceTypeDef",
    {
        "OptIn": bool,
    },
)

StreamProcessorNotificationChannelTypeDef = TypedDict(
    "StreamProcessorNotificationChannelTypeDef",
    {
        "SNSTopicArn": str,
    },
)

DatasetChangesTypeDef = TypedDict(
    "DatasetChangesTypeDef",
    {
        "GroundTruth": Union[str, bytes, IO[Any], StreamingBody],
    },
)

DatasetStatsTypeDef = TypedDict(
    "DatasetStatsTypeDef",
    {
        "LabeledEntries": int,
        "TotalEntries": int,
        "TotalLabels": int,
        "ErrorEntries": int,
    },
    total=False,
)

DatasetLabelStatsTypeDef = TypedDict(
    "DatasetLabelStatsTypeDef",
    {
        "EntryCount": int,
        "BoundingBoxCount": int,
    },
    total=False,
)

DatasetMetadataTypeDef = TypedDict(
    "DatasetMetadataTypeDef",
    {
        "CreationTimestamp": datetime,
        "DatasetType": DatasetTypeType,
        "DatasetArn": str,
        "Status": DatasetStatusType,
        "StatusMessage": str,
        "StatusMessageCode": DatasetStatusMessageCodeType,
    },
    total=False,
)

DeleteCollectionRequestRequestTypeDef = TypedDict(
    "DeleteCollectionRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)

DeleteFacesRequestRequestTypeDef = TypedDict(
    "DeleteFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "FaceIds": Sequence[str],
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "ProjectArn": str,
    },
)

DeleteProjectVersionRequestRequestTypeDef = TypedDict(
    "DeleteProjectVersionRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
    },
)

DeleteStreamProcessorRequestRequestTypeDef = TypedDict(
    "DeleteStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeCollectionRequestRequestTypeDef = TypedDict(
    "DescribeCollectionRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
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

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

_RequiredDescribeProjectVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestRequestTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestRequestTypeDef",
    {
        "VersionNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeProjectVersionsRequestRequestTypeDef(
    _RequiredDescribeProjectVersionsRequestRequestTypeDef,
    _OptionalDescribeProjectVersionsRequestRequestTypeDef,
):
    pass


DescribeProjectsRequestRequestTypeDef = TypedDict(
    "DescribeProjectsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ProjectNames": Sequence[str],
    },
    total=False,
)

DescribeStreamProcessorRequestRequestTypeDef = TypedDict(
    "DescribeStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

HumanLoopActivationOutputTypeDef = TypedDict(
    "HumanLoopActivationOutputTypeDef",
    {
        "HumanLoopArn": str,
        "HumanLoopActivationReasons": List[str],
        "HumanLoopActivationConditionsEvaluationResults": str,
    },
    total=False,
)

ProtectiveEquipmentSummarizationAttributesTypeDef = TypedDict(
    "ProtectiveEquipmentSummarizationAttributesTypeDef",
    {
        "MinConfidence": float,
        "RequiredEquipmentTypes": Sequence[ProtectiveEquipmentTypeType],
    },
)

ProtectiveEquipmentSummaryTypeDef = TypedDict(
    "ProtectiveEquipmentSummaryTypeDef",
    {
        "PersonsWithRequiredEquipment": List[int],
        "PersonsWithoutRequiredEquipment": List[int],
        "PersonsIndeterminate": List[int],
    },
    total=False,
)

DetectionFilterTypeDef = TypedDict(
    "DetectionFilterTypeDef",
    {
        "MinConfidence": float,
        "MinBoundingBoxHeight": float,
        "MinBoundingBoxWidth": float,
    },
    total=False,
)

DistributeDatasetTypeDef = TypedDict(
    "DistributeDatasetTypeDef",
    {
        "Arn": str,
    },
)

EyeOpenTypeDef = TypedDict(
    "EyeOpenTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

EyeglassesTypeDef = TypedDict(
    "EyeglassesTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

GenderTypeDef = TypedDict(
    "GenderTypeDef",
    {
        "Value": GenderTypeType,
        "Confidence": float,
    },
    total=False,
)

MouthOpenTypeDef = TypedDict(
    "MouthOpenTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

MustacheTypeDef = TypedDict(
    "MustacheTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

SunglassesTypeDef = TypedDict(
    "SunglassesTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

FaceSearchSettingsTypeDef = TypedDict(
    "FaceSearchSettingsTypeDef",
    {
        "CollectionId": str,
        "FaceMatchThreshold": float,
    },
    total=False,
)

PointTypeDef = TypedDict(
    "PointTypeDef",
    {
        "X": float,
        "Y": float,
    },
    total=False,
)

GetCelebrityInfoRequestRequestTypeDef = TypedDict(
    "GetCelebrityInfoRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredGetCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_RequiredGetCelebrityRecognitionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_OptionalGetCelebrityRecognitionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": CelebrityRecognitionSortByType,
    },
    total=False,
)


class GetCelebrityRecognitionRequestRequestTypeDef(
    _RequiredGetCelebrityRecognitionRequestRequestTypeDef,
    _OptionalGetCelebrityRecognitionRequestRequestTypeDef,
):
    pass


VideoMetadataTypeDef = TypedDict(
    "VideoMetadataTypeDef",
    {
        "Codec": str,
        "DurationMillis": int,
        "Format": str,
        "FrameRate": float,
        "FrameHeight": int,
        "FrameWidth": int,
        "ColorRange": VideoColorRangeType,
    },
    total=False,
)

_RequiredGetContentModerationRequestRequestTypeDef = TypedDict(
    "_RequiredGetContentModerationRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetContentModerationRequestRequestTypeDef = TypedDict(
    "_OptionalGetContentModerationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": ContentModerationSortByType,
    },
    total=False,
)


class GetContentModerationRequestRequestTypeDef(
    _RequiredGetContentModerationRequestRequestTypeDef,
    _OptionalGetContentModerationRequestRequestTypeDef,
):
    pass


_RequiredGetFaceDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetFaceDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetFaceDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetFaceDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetFaceDetectionRequestRequestTypeDef(
    _RequiredGetFaceDetectionRequestRequestTypeDef, _OptionalGetFaceDetectionRequestRequestTypeDef
):
    pass


_RequiredGetFaceSearchRequestRequestTypeDef = TypedDict(
    "_RequiredGetFaceSearchRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetFaceSearchRequestRequestTypeDef = TypedDict(
    "_OptionalGetFaceSearchRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": FaceSearchSortByType,
    },
    total=False,
)


class GetFaceSearchRequestRequestTypeDef(
    _RequiredGetFaceSearchRequestRequestTypeDef, _OptionalGetFaceSearchRequestRequestTypeDef
):
    pass


_RequiredGetLabelDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetLabelDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetLabelDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetLabelDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": LabelDetectionSortByType,
    },
    total=False,
)


class GetLabelDetectionRequestRequestTypeDef(
    _RequiredGetLabelDetectionRequestRequestTypeDef, _OptionalGetLabelDetectionRequestRequestTypeDef
):
    pass


_RequiredGetPersonTrackingRequestRequestTypeDef = TypedDict(
    "_RequiredGetPersonTrackingRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetPersonTrackingRequestRequestTypeDef = TypedDict(
    "_OptionalGetPersonTrackingRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": PersonTrackingSortByType,
    },
    total=False,
)


class GetPersonTrackingRequestRequestTypeDef(
    _RequiredGetPersonTrackingRequestRequestTypeDef, _OptionalGetPersonTrackingRequestRequestTypeDef
):
    pass


_RequiredGetSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetSegmentDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetSegmentDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetSegmentDetectionRequestRequestTypeDef(
    _RequiredGetSegmentDetectionRequestRequestTypeDef,
    _OptionalGetSegmentDetectionRequestRequestTypeDef,
):
    pass


SegmentTypeInfoTypeDef = TypedDict(
    "SegmentTypeInfoTypeDef",
    {
        "Type": SegmentTypeType,
        "ModelVersion": str,
    },
    total=False,
)

_RequiredGetTextDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetTextDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetTextDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetTextDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetTextDetectionRequestRequestTypeDef(
    _RequiredGetTextDetectionRequestRequestTypeDef, _OptionalGetTextDetectionRequestRequestTypeDef
):
    pass


S3ObjectTypeDef = TypedDict(
    "S3ObjectTypeDef",
    {
        "Bucket": str,
        "Name": str,
        "Version": str,
    },
    total=False,
)

HumanLoopDataAttributesTypeDef = TypedDict(
    "HumanLoopDataAttributesTypeDef",
    {
        "ContentClassifiers": Sequence[ContentClassifierType],
    },
    total=False,
)

KinesisDataStreamTypeDef = TypedDict(
    "KinesisDataStreamTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

KinesisVideoStreamStartSelectorTypeDef = TypedDict(
    "KinesisVideoStreamStartSelectorTypeDef",
    {
        "ProducerTimestamp": int,
        "FragmentNumber": str,
    },
    total=False,
)

KinesisVideoStreamTypeDef = TypedDict(
    "KinesisVideoStreamTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

ParentTypeDef = TypedDict(
    "ParentTypeDef",
    {
        "Name": str,
    },
    total=False,
)

ListCollectionsRequestRequestTypeDef = TypedDict(
    "ListCollectionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetEntriesRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetEntriesRequestRequestTypeDef",
    {
        "ContainsLabels": Sequence[str],
        "Labeled": bool,
        "SourceRefContains": str,
        "HasErrors": bool,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDatasetEntriesRequestRequestTypeDef(
    _RequiredListDatasetEntriesRequestRequestTypeDef,
    _OptionalListDatasetEntriesRequestRequestTypeDef,
):
    pass


_RequiredListDatasetLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetLabelsRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetLabelsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDatasetLabelsRequestRequestTypeDef(
    _RequiredListDatasetLabelsRequestRequestTypeDef, _OptionalListDatasetLabelsRequestRequestTypeDef
):
    pass


_RequiredListFacesRequestRequestTypeDef = TypedDict(
    "_RequiredListFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListFacesRequestRequestTypeDef = TypedDict(
    "_OptionalListFacesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListFacesRequestRequestTypeDef(
    _RequiredListFacesRequestRequestTypeDef, _OptionalListFacesRequestRequestTypeDef
):
    pass


ListStreamProcessorsRequestRequestTypeDef = TypedDict(
    "ListStreamProcessorsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

StreamProcessorTypeDef = TypedDict(
    "StreamProcessorTypeDef",
    {
        "Name": str,
        "Status": StreamProcessorStatusType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

NotificationChannelTypeDef = TypedDict(
    "NotificationChannelTypeDef",
    {
        "SNSTopicArn": str,
        "RoleArn": str,
    },
)

S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef",
    {
        "Bucket": str,
        "KeyPrefix": str,
    },
    total=False,
)

_RequiredSearchFacesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "FaceId": str,
    },
)
_OptionalSearchFacesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFacesRequestRequestTypeDef",
    {
        "MaxFaces": int,
        "FaceMatchThreshold": float,
    },
    total=False,
)


class SearchFacesRequestRequestTypeDef(
    _RequiredSearchFacesRequestRequestTypeDef, _OptionalSearchFacesRequestRequestTypeDef
):
    pass


ShotSegmentTypeDef = TypedDict(
    "ShotSegmentTypeDef",
    {
        "Index": int,
        "Confidence": float,
    },
    total=False,
)

TechnicalCueSegmentTypeDef = TypedDict(
    "TechnicalCueSegmentTypeDef",
    {
        "Type": TechnicalCueTypeType,
        "Confidence": float,
    },
    total=False,
)

StartProjectVersionRequestRequestTypeDef = TypedDict(
    "StartProjectVersionRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
        "MinInferenceUnits": int,
    },
)

StartShotDetectionFilterTypeDef = TypedDict(
    "StartShotDetectionFilterTypeDef",
    {
        "MinSegmentConfidence": float,
    },
    total=False,
)

StreamProcessingStopSelectorTypeDef = TypedDict(
    "StreamProcessingStopSelectorTypeDef",
    {
        "MaxDurationInSeconds": int,
    },
    total=False,
)

StopProjectVersionRequestRequestTypeDef = TypedDict(
    "StopProjectVersionRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
    },
)

StopStreamProcessorRequestRequestTypeDef = TypedDict(
    "StopStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

StartTechnicalCueDetectionFilterTypeDef = TypedDict(
    "StartTechnicalCueDetectionFilterTypeDef",
    {
        "MinSegmentConfidence": float,
        "BlackFrame": BlackFrameTypeDef,
    },
    total=False,
)

ComparedSourceImageFaceTypeDef = TypedDict(
    "ComparedSourceImageFaceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
    },
    total=False,
)

FaceTypeDef = TypedDict(
    "FaceTypeDef",
    {
        "FaceId": str,
        "BoundingBox": BoundingBoxTypeDef,
        "ImageId": str,
        "ExternalImageId": str,
        "Confidence": float,
        "IndexFacesModelVersion": str,
    },
    total=False,
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
    },
    total=False,
)

CreateCollectionResponseTypeDef = TypedDict(
    "CreateCollectionResponseTypeDef",
    {
        "StatusCode": int,
        "CollectionArn": str,
        "FaceModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "ProjectArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectVersionResponseTypeDef = TypedDict(
    "CreateProjectVersionResponseTypeDef",
    {
        "ProjectVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamProcessorResponseTypeDef = TypedDict(
    "CreateStreamProcessorResponseTypeDef",
    {
        "StreamProcessorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCollectionResponseTypeDef = TypedDict(
    "DeleteCollectionResponseTypeDef",
    {
        "StatusCode": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFacesResponseTypeDef = TypedDict(
    "DeleteFacesResponseTypeDef",
    {
        "DeletedFaces": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectResponseTypeDef = TypedDict(
    "DeleteProjectResponseTypeDef",
    {
        "Status": ProjectStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectVersionResponseTypeDef = TypedDict(
    "DeleteProjectVersionResponseTypeDef",
    {
        "Status": ProjectVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCollectionResponseTypeDef = TypedDict(
    "DescribeCollectionResponseTypeDef",
    {
        "FaceCount": int,
        "FaceModelVersion": str,
        "CollectionARN": str,
        "CreationTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCelebrityInfoResponseTypeDef = TypedDict(
    "GetCelebrityInfoResponseTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "KnownGender": KnownGenderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCollectionsResponseTypeDef = TypedDict(
    "ListCollectionsResponseTypeDef",
    {
        "CollectionIds": List[str],
        "NextToken": str,
        "FaceModelVersions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasetEntriesResponseTypeDef = TypedDict(
    "ListDatasetEntriesResponseTypeDef",
    {
        "DatasetEntries": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartCelebrityRecognitionResponseTypeDef = TypedDict(
    "StartCelebrityRecognitionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartContentModerationResponseTypeDef = TypedDict(
    "StartContentModerationResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFaceDetectionResponseTypeDef = TypedDict(
    "StartFaceDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFaceSearchResponseTypeDef = TypedDict(
    "StartFaceSearchResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartLabelDetectionResponseTypeDef = TypedDict(
    "StartLabelDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartPersonTrackingResponseTypeDef = TypedDict(
    "StartPersonTrackingResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartProjectVersionResponseTypeDef = TypedDict(
    "StartProjectVersionResponseTypeDef",
    {
        "Status": ProjectVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSegmentDetectionResponseTypeDef = TypedDict(
    "StartSegmentDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartStreamProcessorResponseTypeDef = TypedDict(
    "StartStreamProcessorResponseTypeDef",
    {
        "SessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTextDetectionResponseTypeDef = TypedDict(
    "StartTextDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopProjectVersionResponseTypeDef = TypedDict(
    "StopProjectVersionResponseTypeDef",
    {
        "Status": ProjectVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ComparedFaceTypeDef = TypedDict(
    "ComparedFaceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Landmarks": List[LandmarkTypeDef],
        "Pose": PoseTypeDef,
        "Quality": ImageQualityTypeDef,
        "Emotions": List[EmotionTypeDef],
        "Smile": SmileTypeDef,
    },
    total=False,
)

StreamProcessorSettingsForUpdateTypeDef = TypedDict(
    "StreamProcessorSettingsForUpdateTypeDef",
    {
        "ConnectedHomeForUpdate": ConnectedHomeSettingsForUpdateTypeDef,
    },
    total=False,
)

ContentModerationDetectionTypeDef = TypedDict(
    "ContentModerationDetectionTypeDef",
    {
        "Timestamp": int,
        "ModerationLabel": ModerationLabelTypeDef,
    },
    total=False,
)

EquipmentDetectionTypeDef = TypedDict(
    "EquipmentDetectionTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Type": ProtectiveEquipmentTypeType,
        "CoversBodyPart": CoversBodyPartTypeDef,
    },
    total=False,
)

UpdateDatasetEntriesRequestRequestTypeDef = TypedDict(
    "UpdateDatasetEntriesRequestRequestTypeDef",
    {
        "DatasetArn": str,
        "Changes": DatasetChangesTypeDef,
    },
)

DatasetDescriptionTypeDef = TypedDict(
    "DatasetDescriptionTypeDef",
    {
        "CreationTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
        "Status": DatasetStatusType,
        "StatusMessage": str,
        "StatusMessageCode": DatasetStatusMessageCodeType,
        "DatasetStats": DatasetStatsTypeDef,
    },
    total=False,
)

DatasetLabelDescriptionTypeDef = TypedDict(
    "DatasetLabelDescriptionTypeDef",
    {
        "LabelName": str,
        "LabelStats": DatasetLabelStatsTypeDef,
    },
    total=False,
)

ProjectDescriptionTypeDef = TypedDict(
    "ProjectDescriptionTypeDef",
    {
        "ProjectArn": str,
        "CreationTimestamp": datetime,
        "Status": ProjectStatusType,
        "Datasets": List[DatasetMetadataTypeDef],
    },
    total=False,
)

_RequiredDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef",
    {
        "VersionNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef(
    _RequiredDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef,
    _OptionalDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef,
):
    pass


DescribeProjectsRequestDescribeProjectsPaginateTypeDef = TypedDict(
    "DescribeProjectsRequestDescribeProjectsPaginateTypeDef",
    {
        "ProjectNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCollectionsRequestListCollectionsPaginateTypeDef = TypedDict(
    "ListCollectionsRequestListCollectionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef = TypedDict(
    "_RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef = TypedDict(
    "_OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    {
        "ContainsLabels": Sequence[str],
        "Labeled": bool,
        "SourceRefContains": str,
        "HasErrors": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef(
    _RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    _OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
):
    pass


_RequiredListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef = TypedDict(
    "_RequiredListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef = TypedDict(
    "_OptionalListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef(
    _RequiredListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef,
    _OptionalListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef,
):
    pass


_RequiredListFacesRequestListFacesPaginateTypeDef = TypedDict(
    "_RequiredListFacesRequestListFacesPaginateTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListFacesRequestListFacesPaginateTypeDef = TypedDict(
    "_OptionalListFacesRequestListFacesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFacesRequestListFacesPaginateTypeDef(
    _RequiredListFacesRequestListFacesPaginateTypeDef,
    _OptionalListFacesRequestListFacesPaginateTypeDef,
):
    pass


ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef = TypedDict(
    "ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef",
    {
        "VersionNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef(
    _RequiredDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef,
    _OptionalDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef,
):
    pass


_RequiredDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef",
    {
        "VersionNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef(
    _RequiredDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef,
    _OptionalDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef,
):
    pass


DetectModerationLabelsResponseTypeDef = TypedDict(
    "DetectModerationLabelsResponseTypeDef",
    {
        "ModerationLabels": List[ModerationLabelTypeDef],
        "ModerationModelVersion": str,
        "HumanLoopActivationOutput": HumanLoopActivationOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DistributeDatasetEntriesRequestRequestTypeDef = TypedDict(
    "DistributeDatasetEntriesRequestRequestTypeDef",
    {
        "Datasets": Sequence[DistributeDatasetTypeDef],
    },
)

FaceDetailTypeDef = TypedDict(
    "FaceDetailTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "AgeRange": AgeRangeTypeDef,
        "Smile": SmileTypeDef,
        "Eyeglasses": EyeglassesTypeDef,
        "Sunglasses": SunglassesTypeDef,
        "Gender": GenderTypeDef,
        "Beard": BeardTypeDef,
        "Mustache": MustacheTypeDef,
        "EyesOpen": EyeOpenTypeDef,
        "MouthOpen": MouthOpenTypeDef,
        "Emotions": List[EmotionTypeDef],
        "Landmarks": List[LandmarkTypeDef],
        "Pose": PoseTypeDef,
        "Quality": ImageQualityTypeDef,
        "Confidence": float,
    },
    total=False,
)

StreamProcessorSettingsTypeDef = TypedDict(
    "StreamProcessorSettingsTypeDef",
    {
        "FaceSearch": FaceSearchSettingsTypeDef,
        "ConnectedHome": ConnectedHomeSettingsTypeDef,
    },
    total=False,
)

GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Polygon": List[PointTypeDef],
    },
    total=False,
)

RegionOfInterestTypeDef = TypedDict(
    "RegionOfInterestTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Polygon": Sequence[PointTypeDef],
    },
    total=False,
)

GroundTruthManifestTypeDef = TypedDict(
    "GroundTruthManifestTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "Bytes": Union[str, bytes, IO[Any], StreamingBody],
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

SummaryTypeDef = TypedDict(
    "SummaryTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

VideoTypeDef = TypedDict(
    "VideoTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

_RequiredHumanLoopConfigTypeDef = TypedDict(
    "_RequiredHumanLoopConfigTypeDef",
    {
        "HumanLoopName": str,
        "FlowDefinitionArn": str,
    },
)
_OptionalHumanLoopConfigTypeDef = TypedDict(
    "_OptionalHumanLoopConfigTypeDef",
    {
        "DataAttributes": HumanLoopDataAttributesTypeDef,
    },
    total=False,
)


class HumanLoopConfigTypeDef(_RequiredHumanLoopConfigTypeDef, _OptionalHumanLoopConfigTypeDef):
    pass


StreamProcessingStartSelectorTypeDef = TypedDict(
    "StreamProcessingStartSelectorTypeDef",
    {
        "KVSStreamStartSelector": KinesisVideoStreamStartSelectorTypeDef,
    },
    total=False,
)

StreamProcessorInputTypeDef = TypedDict(
    "StreamProcessorInputTypeDef",
    {
        "KinesisVideoStream": KinesisVideoStreamTypeDef,
    },
    total=False,
)

ListStreamProcessorsResponseTypeDef = TypedDict(
    "ListStreamProcessorsResponseTypeDef",
    {
        "NextToken": str,
        "StreamProcessors": List[StreamProcessorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StreamProcessorOutputTypeDef = TypedDict(
    "StreamProcessorOutputTypeDef",
    {
        "KinesisDataStream": KinesisDataStreamTypeDef,
        "S3Destination": S3DestinationTypeDef,
    },
    total=False,
)

SegmentDetectionTypeDef = TypedDict(
    "SegmentDetectionTypeDef",
    {
        "Type": SegmentTypeType,
        "StartTimestampMillis": int,
        "EndTimestampMillis": int,
        "DurationMillis": int,
        "StartTimecodeSMPTE": str,
        "EndTimecodeSMPTE": str,
        "DurationSMPTE": str,
        "TechnicalCueSegment": TechnicalCueSegmentTypeDef,
        "ShotSegment": ShotSegmentTypeDef,
        "StartFrameNumber": int,
        "EndFrameNumber": int,
        "DurationFrames": int,
    },
    total=False,
)

StartSegmentDetectionFiltersTypeDef = TypedDict(
    "StartSegmentDetectionFiltersTypeDef",
    {
        "TechnicalCueFilter": StartTechnicalCueDetectionFilterTypeDef,
        "ShotFilter": StartShotDetectionFilterTypeDef,
    },
    total=False,
)

FaceMatchTypeDef = TypedDict(
    "FaceMatchTypeDef",
    {
        "Similarity": float,
        "Face": FaceTypeDef,
    },
    total=False,
)

ListFacesResponseTypeDef = TypedDict(
    "ListFacesResponseTypeDef",
    {
        "Faces": List[FaceTypeDef],
        "NextToken": str,
        "FaceModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LabelTypeDef = TypedDict(
    "LabelTypeDef",
    {
        "Name": str,
        "Confidence": float,
        "Instances": List[InstanceTypeDef],
        "Parents": List[ParentTypeDef],
    },
    total=False,
)

CelebrityTypeDef = TypedDict(
    "CelebrityTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "Id": str,
        "Face": ComparedFaceTypeDef,
        "MatchConfidence": float,
        "KnownGender": KnownGenderTypeDef,
    },
    total=False,
)

CompareFacesMatchTypeDef = TypedDict(
    "CompareFacesMatchTypeDef",
    {
        "Similarity": float,
        "Face": ComparedFaceTypeDef,
    },
    total=False,
)

GetContentModerationResponseTypeDef = TypedDict(
    "GetContentModerationResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "ModerationLabels": List[ContentModerationDetectionTypeDef],
        "NextToken": str,
        "ModerationModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProtectiveEquipmentBodyPartTypeDef = TypedDict(
    "ProtectiveEquipmentBodyPartTypeDef",
    {
        "Name": BodyPartType,
        "Confidence": float,
        "EquipmentDetections": List[EquipmentDetectionTypeDef],
    },
    total=False,
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetDescription": DatasetDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasetLabelsResponseTypeDef = TypedDict(
    "ListDatasetLabelsResponseTypeDef",
    {
        "DatasetLabelDescriptions": List[DatasetLabelDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProjectsResponseTypeDef = TypedDict(
    "DescribeProjectsResponseTypeDef",
    {
        "ProjectDescriptions": List[ProjectDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CelebrityDetailTypeDef = TypedDict(
    "CelebrityDetailTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "Id": str,
        "Confidence": float,
        "BoundingBox": BoundingBoxTypeDef,
        "Face": FaceDetailTypeDef,
        "KnownGender": KnownGenderTypeDef,
    },
    total=False,
)

DetectFacesResponseTypeDef = TypedDict(
    "DetectFacesResponseTypeDef",
    {
        "FaceDetails": List[FaceDetailTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FaceDetectionTypeDef = TypedDict(
    "FaceDetectionTypeDef",
    {
        "Timestamp": int,
        "Face": FaceDetailTypeDef,
    },
    total=False,
)

FaceRecordTypeDef = TypedDict(
    "FaceRecordTypeDef",
    {
        "Face": FaceTypeDef,
        "FaceDetail": FaceDetailTypeDef,
    },
    total=False,
)

PersonDetailTypeDef = TypedDict(
    "PersonDetailTypeDef",
    {
        "Index": int,
        "BoundingBox": BoundingBoxTypeDef,
        "Face": FaceDetailTypeDef,
    },
    total=False,
)

UnindexedFaceTypeDef = TypedDict(
    "UnindexedFaceTypeDef",
    {
        "Reasons": List[ReasonType],
        "FaceDetail": FaceDetailTypeDef,
    },
    total=False,
)

CustomLabelTypeDef = TypedDict(
    "CustomLabelTypeDef",
    {
        "Name": str,
        "Confidence": float,
        "Geometry": GeometryTypeDef,
    },
    total=False,
)

TextDetectionTypeDef = TypedDict(
    "TextDetectionTypeDef",
    {
        "DetectedText": str,
        "Type": TextTypesType,
        "Id": int,
        "ParentId": int,
        "Confidence": float,
        "Geometry": GeometryTypeDef,
    },
    total=False,
)

DetectTextFiltersTypeDef = TypedDict(
    "DetectTextFiltersTypeDef",
    {
        "WordFilter": DetectionFilterTypeDef,
        "RegionsOfInterest": Sequence[RegionOfInterestTypeDef],
    },
    total=False,
)

StartTextDetectionFiltersTypeDef = TypedDict(
    "StartTextDetectionFiltersTypeDef",
    {
        "WordFilter": DetectionFilterTypeDef,
        "RegionsOfInterest": Sequence[RegionOfInterestTypeDef],
    },
    total=False,
)

_RequiredUpdateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStreamProcessorRequestRequestTypeDef",
    {
        "SettingsForUpdate": StreamProcessorSettingsForUpdateTypeDef,
        "RegionsOfInterestForUpdate": Sequence[RegionOfInterestTypeDef],
        "DataSharingPreferenceForUpdate": StreamProcessorDataSharingPreferenceTypeDef,
        "ParametersToDelete": Sequence[StreamProcessorParameterToDeleteType],
    },
    total=False,
)


class UpdateStreamProcessorRequestRequestTypeDef(
    _RequiredUpdateStreamProcessorRequestRequestTypeDef,
    _OptionalUpdateStreamProcessorRequestRequestTypeDef,
):
    pass


AssetTypeDef = TypedDict(
    "AssetTypeDef",
    {
        "GroundTruthManifest": GroundTruthManifestTypeDef,
    },
    total=False,
)

DatasetSourceTypeDef = TypedDict(
    "DatasetSourceTypeDef",
    {
        "GroundTruthManifest": GroundTruthManifestTypeDef,
        "DatasetArn": str,
    },
    total=False,
)

_RequiredCompareFacesRequestRequestTypeDef = TypedDict(
    "_RequiredCompareFacesRequestRequestTypeDef",
    {
        "SourceImage": ImageTypeDef,
        "TargetImage": ImageTypeDef,
    },
)
_OptionalCompareFacesRequestRequestTypeDef = TypedDict(
    "_OptionalCompareFacesRequestRequestTypeDef",
    {
        "SimilarityThreshold": float,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class CompareFacesRequestRequestTypeDef(
    _RequiredCompareFacesRequestRequestTypeDef, _OptionalCompareFacesRequestRequestTypeDef
):
    pass


_RequiredDetectCustomLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDetectCustomLabelsRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
        "Image": ImageTypeDef,
    },
)
_OptionalDetectCustomLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDetectCustomLabelsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "MinConfidence": float,
    },
    total=False,
)


class DetectCustomLabelsRequestRequestTypeDef(
    _RequiredDetectCustomLabelsRequestRequestTypeDef,
    _OptionalDetectCustomLabelsRequestRequestTypeDef,
):
    pass


_RequiredDetectFacesRequestRequestTypeDef = TypedDict(
    "_RequiredDetectFacesRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectFacesRequestRequestTypeDef = TypedDict(
    "_OptionalDetectFacesRequestRequestTypeDef",
    {
        "Attributes": Sequence[AttributeType],
    },
    total=False,
)


class DetectFacesRequestRequestTypeDef(
    _RequiredDetectFacesRequestRequestTypeDef, _OptionalDetectFacesRequestRequestTypeDef
):
    pass


_RequiredDetectLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDetectLabelsRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDetectLabelsRequestRequestTypeDef",
    {
        "MaxLabels": int,
        "MinConfidence": float,
    },
    total=False,
)


class DetectLabelsRequestRequestTypeDef(
    _RequiredDetectLabelsRequestRequestTypeDef, _OptionalDetectLabelsRequestRequestTypeDef
):
    pass


_RequiredDetectProtectiveEquipmentRequestRequestTypeDef = TypedDict(
    "_RequiredDetectProtectiveEquipmentRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectProtectiveEquipmentRequestRequestTypeDef = TypedDict(
    "_OptionalDetectProtectiveEquipmentRequestRequestTypeDef",
    {
        "SummarizationAttributes": ProtectiveEquipmentSummarizationAttributesTypeDef,
    },
    total=False,
)


class DetectProtectiveEquipmentRequestRequestTypeDef(
    _RequiredDetectProtectiveEquipmentRequestRequestTypeDef,
    _OptionalDetectProtectiveEquipmentRequestRequestTypeDef,
):
    pass


_RequiredIndexFacesRequestRequestTypeDef = TypedDict(
    "_RequiredIndexFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "Image": ImageTypeDef,
    },
)
_OptionalIndexFacesRequestRequestTypeDef = TypedDict(
    "_OptionalIndexFacesRequestRequestTypeDef",
    {
        "ExternalImageId": str,
        "DetectionAttributes": Sequence[AttributeType],
        "MaxFaces": int,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class IndexFacesRequestRequestTypeDef(
    _RequiredIndexFacesRequestRequestTypeDef, _OptionalIndexFacesRequestRequestTypeDef
):
    pass


RecognizeCelebritiesRequestRequestTypeDef = TypedDict(
    "RecognizeCelebritiesRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)

_RequiredSearchFacesByImageRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFacesByImageRequestRequestTypeDef",
    {
        "CollectionId": str,
        "Image": ImageTypeDef,
    },
)
_OptionalSearchFacesByImageRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFacesByImageRequestRequestTypeDef",
    {
        "MaxFaces": int,
        "FaceMatchThreshold": float,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class SearchFacesByImageRequestRequestTypeDef(
    _RequiredSearchFacesByImageRequestRequestTypeDef,
    _OptionalSearchFacesByImageRequestRequestTypeDef,
):
    pass


EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef",
    {
        "F1Score": float,
        "Summary": SummaryTypeDef,
    },
    total=False,
)

_RequiredStartCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_RequiredStartCelebrityRecognitionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_OptionalStartCelebrityRecognitionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartCelebrityRecognitionRequestRequestTypeDef(
    _RequiredStartCelebrityRecognitionRequestRequestTypeDef,
    _OptionalStartCelebrityRecognitionRequestRequestTypeDef,
):
    pass


_RequiredStartContentModerationRequestRequestTypeDef = TypedDict(
    "_RequiredStartContentModerationRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartContentModerationRequestRequestTypeDef = TypedDict(
    "_OptionalStartContentModerationRequestRequestTypeDef",
    {
        "MinConfidence": float,
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartContentModerationRequestRequestTypeDef(
    _RequiredStartContentModerationRequestRequestTypeDef,
    _OptionalStartContentModerationRequestRequestTypeDef,
):
    pass


_RequiredStartFaceDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartFaceDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartFaceDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartFaceDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "FaceAttributes": FaceAttributesType,
        "JobTag": str,
    },
    total=False,
)


class StartFaceDetectionRequestRequestTypeDef(
    _RequiredStartFaceDetectionRequestRequestTypeDef,
    _OptionalStartFaceDetectionRequestRequestTypeDef,
):
    pass


_RequiredStartFaceSearchRequestRequestTypeDef = TypedDict(
    "_RequiredStartFaceSearchRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
        "CollectionId": str,
    },
)
_OptionalStartFaceSearchRequestRequestTypeDef = TypedDict(
    "_OptionalStartFaceSearchRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "FaceMatchThreshold": float,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartFaceSearchRequestRequestTypeDef(
    _RequiredStartFaceSearchRequestRequestTypeDef, _OptionalStartFaceSearchRequestRequestTypeDef
):
    pass


_RequiredStartLabelDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartLabelDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartLabelDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartLabelDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "MinConfidence": float,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartLabelDetectionRequestRequestTypeDef(
    _RequiredStartLabelDetectionRequestRequestTypeDef,
    _OptionalStartLabelDetectionRequestRequestTypeDef,
):
    pass


_RequiredStartPersonTrackingRequestRequestTypeDef = TypedDict(
    "_RequiredStartPersonTrackingRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartPersonTrackingRequestRequestTypeDef = TypedDict(
    "_OptionalStartPersonTrackingRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartPersonTrackingRequestRequestTypeDef(
    _RequiredStartPersonTrackingRequestRequestTypeDef,
    _OptionalStartPersonTrackingRequestRequestTypeDef,
):
    pass


_RequiredDetectModerationLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDetectModerationLabelsRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectModerationLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDetectModerationLabelsRequestRequestTypeDef",
    {
        "MinConfidence": float,
        "HumanLoopConfig": HumanLoopConfigTypeDef,
    },
    total=False,
)


class DetectModerationLabelsRequestRequestTypeDef(
    _RequiredDetectModerationLabelsRequestRequestTypeDef,
    _OptionalDetectModerationLabelsRequestRequestTypeDef,
):
    pass


_RequiredStartStreamProcessorRequestRequestTypeDef = TypedDict(
    "_RequiredStartStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalStartStreamProcessorRequestRequestTypeDef = TypedDict(
    "_OptionalStartStreamProcessorRequestRequestTypeDef",
    {
        "StartSelector": StreamProcessingStartSelectorTypeDef,
        "StopSelector": StreamProcessingStopSelectorTypeDef,
    },
    total=False,
)


class StartStreamProcessorRequestRequestTypeDef(
    _RequiredStartStreamProcessorRequestRequestTypeDef,
    _OptionalStartStreamProcessorRequestRequestTypeDef,
):
    pass


_RequiredCreateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamProcessorRequestRequestTypeDef",
    {
        "Input": StreamProcessorInputTypeDef,
        "Output": StreamProcessorOutputTypeDef,
        "Name": str,
        "Settings": StreamProcessorSettingsTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamProcessorRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "NotificationChannel": StreamProcessorNotificationChannelTypeDef,
        "KmsKeyId": str,
        "RegionsOfInterest": Sequence[RegionOfInterestTypeDef],
        "DataSharingPreference": StreamProcessorDataSharingPreferenceTypeDef,
    },
    total=False,
)


class CreateStreamProcessorRequestRequestTypeDef(
    _RequiredCreateStreamProcessorRequestRequestTypeDef,
    _OptionalCreateStreamProcessorRequestRequestTypeDef,
):
    pass


DescribeStreamProcessorResponseTypeDef = TypedDict(
    "DescribeStreamProcessorResponseTypeDef",
    {
        "Name": str,
        "StreamProcessorArn": str,
        "Status": StreamProcessorStatusType,
        "StatusMessage": str,
        "CreationTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "Input": StreamProcessorInputTypeDef,
        "Output": StreamProcessorOutputTypeDef,
        "RoleArn": str,
        "Settings": StreamProcessorSettingsTypeDef,
        "NotificationChannel": StreamProcessorNotificationChannelTypeDef,
        "KmsKeyId": str,
        "RegionsOfInterest": List[RegionOfInterestTypeDef],
        "DataSharingPreference": StreamProcessorDataSharingPreferenceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSegmentDetectionResponseTypeDef = TypedDict(
    "GetSegmentDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": List[VideoMetadataTypeDef],
        "AudioMetadata": List[AudioMetadataTypeDef],
        "NextToken": str,
        "Segments": List[SegmentDetectionTypeDef],
        "SelectedSegmentTypes": List[SegmentTypeInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartSegmentDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
        "SegmentTypes": Sequence[SegmentTypeType],
    },
)
_OptionalStartSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartSegmentDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
        "Filters": StartSegmentDetectionFiltersTypeDef,
    },
    total=False,
)


class StartSegmentDetectionRequestRequestTypeDef(
    _RequiredStartSegmentDetectionRequestRequestTypeDef,
    _OptionalStartSegmentDetectionRequestRequestTypeDef,
):
    pass


SearchFacesByImageResponseTypeDef = TypedDict(
    "SearchFacesByImageResponseTypeDef",
    {
        "SearchedFaceBoundingBox": BoundingBoxTypeDef,
        "SearchedFaceConfidence": float,
        "FaceMatches": List[FaceMatchTypeDef],
        "FaceModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchFacesResponseTypeDef = TypedDict(
    "SearchFacesResponseTypeDef",
    {
        "SearchedFaceId": str,
        "FaceMatches": List[FaceMatchTypeDef],
        "FaceModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectLabelsResponseTypeDef = TypedDict(
    "DetectLabelsResponseTypeDef",
    {
        "Labels": List[LabelTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "LabelModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LabelDetectionTypeDef = TypedDict(
    "LabelDetectionTypeDef",
    {
        "Timestamp": int,
        "Label": LabelTypeDef,
    },
    total=False,
)

RecognizeCelebritiesResponseTypeDef = TypedDict(
    "RecognizeCelebritiesResponseTypeDef",
    {
        "CelebrityFaces": List[CelebrityTypeDef],
        "UnrecognizedFaces": List[ComparedFaceTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CompareFacesResponseTypeDef = TypedDict(
    "CompareFacesResponseTypeDef",
    {
        "SourceImageFace": ComparedSourceImageFaceTypeDef,
        "FaceMatches": List[CompareFacesMatchTypeDef],
        "UnmatchedFaces": List[ComparedFaceTypeDef],
        "SourceImageOrientationCorrection": OrientationCorrectionType,
        "TargetImageOrientationCorrection": OrientationCorrectionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProtectiveEquipmentPersonTypeDef = TypedDict(
    "ProtectiveEquipmentPersonTypeDef",
    {
        "BodyParts": List[ProtectiveEquipmentBodyPartTypeDef],
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Id": int,
    },
    total=False,
)

CelebrityRecognitionTypeDef = TypedDict(
    "CelebrityRecognitionTypeDef",
    {
        "Timestamp": int,
        "Celebrity": CelebrityDetailTypeDef,
    },
    total=False,
)

GetFaceDetectionResponseTypeDef = TypedDict(
    "GetFaceDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Faces": List[FaceDetectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PersonDetectionTypeDef = TypedDict(
    "PersonDetectionTypeDef",
    {
        "Timestamp": int,
        "Person": PersonDetailTypeDef,
    },
    total=False,
)

PersonMatchTypeDef = TypedDict(
    "PersonMatchTypeDef",
    {
        "Timestamp": int,
        "Person": PersonDetailTypeDef,
        "FaceMatches": List[FaceMatchTypeDef],
    },
    total=False,
)

IndexFacesResponseTypeDef = TypedDict(
    "IndexFacesResponseTypeDef",
    {
        "FaceRecords": List[FaceRecordTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "FaceModelVersion": str,
        "UnindexedFaces": List[UnindexedFaceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectCustomLabelsResponseTypeDef = TypedDict(
    "DetectCustomLabelsResponseTypeDef",
    {
        "CustomLabels": List[CustomLabelTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectTextResponseTypeDef = TypedDict(
    "DetectTextResponseTypeDef",
    {
        "TextDetections": List[TextDetectionTypeDef],
        "TextModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TextDetectionResultTypeDef = TypedDict(
    "TextDetectionResultTypeDef",
    {
        "Timestamp": int,
        "TextDetection": TextDetectionTypeDef,
    },
    total=False,
)

_RequiredDetectTextRequestRequestTypeDef = TypedDict(
    "_RequiredDetectTextRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectTextRequestRequestTypeDef = TypedDict(
    "_OptionalDetectTextRequestRequestTypeDef",
    {
        "Filters": DetectTextFiltersTypeDef,
    },
    total=False,
)


class DetectTextRequestRequestTypeDef(
    _RequiredDetectTextRequestRequestTypeDef, _OptionalDetectTextRequestRequestTypeDef
):
    pass


_RequiredStartTextDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartTextDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartTextDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartTextDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
        "Filters": StartTextDetectionFiltersTypeDef,
    },
    total=False,
)


class StartTextDetectionRequestRequestTypeDef(
    _RequiredStartTextDetectionRequestRequestTypeDef,
    _OptionalStartTextDetectionRequestRequestTypeDef,
):
    pass


TestingDataTypeDef = TypedDict(
    "TestingDataTypeDef",
    {
        "Assets": Sequence[AssetTypeDef],
        "AutoCreate": bool,
    },
    total=False,
)

TrainingDataTypeDef = TypedDict(
    "TrainingDataTypeDef",
    {
        "Assets": Sequence[AssetTypeDef],
    },
    total=False,
)

ValidationDataTypeDef = TypedDict(
    "ValidationDataTypeDef",
    {
        "Assets": List[AssetTypeDef],
    },
    total=False,
)

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "DatasetType": DatasetTypeType,
        "ProjectArn": str,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "DatasetSource": DatasetSourceTypeDef,
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


GetLabelDetectionResponseTypeDef = TypedDict(
    "GetLabelDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Labels": List[LabelDetectionTypeDef],
        "LabelModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectProtectiveEquipmentResponseTypeDef = TypedDict(
    "DetectProtectiveEquipmentResponseTypeDef",
    {
        "ProtectiveEquipmentModelVersion": str,
        "Persons": List[ProtectiveEquipmentPersonTypeDef],
        "Summary": ProtectiveEquipmentSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCelebrityRecognitionResponseTypeDef = TypedDict(
    "GetCelebrityRecognitionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Celebrities": List[CelebrityRecognitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPersonTrackingResponseTypeDef = TypedDict(
    "GetPersonTrackingResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Persons": List[PersonDetectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFaceSearchResponseTypeDef = TypedDict(
    "GetFaceSearchResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "NextToken": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "Persons": List[PersonMatchTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTextDetectionResponseTypeDef = TypedDict(
    "GetTextDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "TextDetections": List[TextDetectionResultTypeDef],
        "NextToken": str,
        "TextModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateProjectVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectVersionRequestRequestTypeDef",
    {
        "ProjectArn": str,
        "VersionName": str,
        "OutputConfig": OutputConfigTypeDef,
    },
)
_OptionalCreateProjectVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectVersionRequestRequestTypeDef",
    {
        "TrainingData": TrainingDataTypeDef,
        "TestingData": TestingDataTypeDef,
        "Tags": Mapping[str, str],
        "KmsKeyId": str,
    },
    total=False,
)


class CreateProjectVersionRequestRequestTypeDef(
    _RequiredCreateProjectVersionRequestRequestTypeDef,
    _OptionalCreateProjectVersionRequestRequestTypeDef,
):
    pass


TestingDataResultTypeDef = TypedDict(
    "TestingDataResultTypeDef",
    {
        "Input": TestingDataTypeDef,
        "Output": TestingDataTypeDef,
        "Validation": ValidationDataTypeDef,
    },
    total=False,
)

TrainingDataResultTypeDef = TypedDict(
    "TrainingDataResultTypeDef",
    {
        "Input": TrainingDataTypeDef,
        "Output": TrainingDataTypeDef,
        "Validation": ValidationDataTypeDef,
    },
    total=False,
)

ProjectVersionDescriptionTypeDef = TypedDict(
    "ProjectVersionDescriptionTypeDef",
    {
        "ProjectVersionArn": str,
        "CreationTimestamp": datetime,
        "MinInferenceUnits": int,
        "Status": ProjectVersionStatusType,
        "StatusMessage": str,
        "BillableTrainingTimeInSeconds": int,
        "TrainingEndTimestamp": datetime,
        "OutputConfig": OutputConfigTypeDef,
        "TrainingDataResult": TrainingDataResultTypeDef,
        "TestingDataResult": TestingDataResultTypeDef,
        "EvaluationResult": EvaluationResultTypeDef,
        "ManifestSummary": GroundTruthManifestTypeDef,
        "KmsKeyId": str,
    },
    total=False,
)

DescribeProjectVersionsResponseTypeDef = TypedDict(
    "DescribeProjectVersionsResponseTypeDef",
    {
        "ProjectVersionDescriptions": List[ProjectVersionDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
