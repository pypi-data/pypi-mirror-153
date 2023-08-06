"""
Type annotations for textract service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/type_defs/)

Usage::

    ```python
    from mypy_boto3_textract.type_defs import DocumentMetadataTypeDef

    data: DocumentMetadataTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BlockTypeType,
    ContentClassifierType,
    EntityTypeType,
    FeatureTypeType,
    JobStatusType,
    RelationshipTypeType,
    SelectionStatusType,
    TextTypeType,
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
    "DocumentMetadataTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "ResponseMetadataTypeDef",
    "NormalizedValueTypeDef",
    "QueryTypeDef",
    "RelationshipTypeDef",
    "BoundingBoxTypeDef",
    "S3ObjectTypeDef",
    "ExpenseTypeTypeDef",
    "PointTypeDef",
    "GetDocumentAnalysisRequestRequestTypeDef",
    "WarningTypeDef",
    "GetDocumentTextDetectionRequestRequestTypeDef",
    "GetExpenseAnalysisRequestRequestTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "NotificationChannelTypeDef",
    "OutputConfigTypeDef",
    "StartDocumentAnalysisResponseTypeDef",
    "StartDocumentTextDetectionResponseTypeDef",
    "StartExpenseAnalysisResponseTypeDef",
    "AnalyzeIDDetectionsTypeDef",
    "QueriesConfigTypeDef",
    "DocumentLocationTypeDef",
    "DocumentTypeDef",
    "GeometryTypeDef",
    "HumanLoopConfigTypeDef",
    "IdentityDocumentFieldTypeDef",
    "StartDocumentAnalysisRequestRequestTypeDef",
    "StartDocumentTextDetectionRequestRequestTypeDef",
    "StartExpenseAnalysisRequestRequestTypeDef",
    "AnalyzeExpenseRequestRequestTypeDef",
    "AnalyzeIDRequestRequestTypeDef",
    "DetectDocumentTextRequestRequestTypeDef",
    "BlockTypeDef",
    "ExpenseDetectionTypeDef",
    "AnalyzeDocumentRequestRequestTypeDef",
    "IdentityDocumentTypeDef",
    "AnalyzeDocumentResponseTypeDef",
    "DetectDocumentTextResponseTypeDef",
    "GetDocumentAnalysisResponseTypeDef",
    "GetDocumentTextDetectionResponseTypeDef",
    "ExpenseFieldTypeDef",
    "AnalyzeIDResponseTypeDef",
    "LineItemFieldsTypeDef",
    "LineItemGroupTypeDef",
    "ExpenseDocumentTypeDef",
    "AnalyzeExpenseResponseTypeDef",
    "GetExpenseAnalysisResponseTypeDef",
)

DocumentMetadataTypeDef = TypedDict(
    "DocumentMetadataTypeDef",
    {
        "Pages": int,
    },
    total=False,
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

NormalizedValueTypeDef = TypedDict(
    "NormalizedValueTypeDef",
    {
        "Value": str,
        "ValueType": Literal["DATE"],
    },
    total=False,
)

_RequiredQueryTypeDef = TypedDict(
    "_RequiredQueryTypeDef",
    {
        "Text": str,
    },
)
_OptionalQueryTypeDef = TypedDict(
    "_OptionalQueryTypeDef",
    {
        "Alias": str,
        "Pages": Sequence[str],
    },
    total=False,
)


class QueryTypeDef(_RequiredQueryTypeDef, _OptionalQueryTypeDef):
    pass


RelationshipTypeDef = TypedDict(
    "RelationshipTypeDef",
    {
        "Type": RelationshipTypeType,
        "Ids": List[str],
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

S3ObjectTypeDef = TypedDict(
    "S3ObjectTypeDef",
    {
        "Bucket": str,
        "Name": str,
        "Version": str,
    },
    total=False,
)

ExpenseTypeTypeDef = TypedDict(
    "ExpenseTypeTypeDef",
    {
        "Text": str,
        "Confidence": float,
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

_RequiredGetDocumentAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredGetDocumentAnalysisRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetDocumentAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalGetDocumentAnalysisRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetDocumentAnalysisRequestRequestTypeDef(
    _RequiredGetDocumentAnalysisRequestRequestTypeDef,
    _OptionalGetDocumentAnalysisRequestRequestTypeDef,
):
    pass


WarningTypeDef = TypedDict(
    "WarningTypeDef",
    {
        "ErrorCode": str,
        "Pages": List[int],
    },
    total=False,
)

_RequiredGetDocumentTextDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetDocumentTextDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetDocumentTextDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetDocumentTextDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetDocumentTextDetectionRequestRequestTypeDef(
    _RequiredGetDocumentTextDetectionRequestRequestTypeDef,
    _OptionalGetDocumentTextDetectionRequestRequestTypeDef,
):
    pass


_RequiredGetExpenseAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredGetExpenseAnalysisRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetExpenseAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalGetExpenseAnalysisRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetExpenseAnalysisRequestRequestTypeDef(
    _RequiredGetExpenseAnalysisRequestRequestTypeDef,
    _OptionalGetExpenseAnalysisRequestRequestTypeDef,
):
    pass


HumanLoopDataAttributesTypeDef = TypedDict(
    "HumanLoopDataAttributesTypeDef",
    {
        "ContentClassifiers": Sequence[ContentClassifierType],
    },
    total=False,
)

NotificationChannelTypeDef = TypedDict(
    "NotificationChannelTypeDef",
    {
        "SNSTopicArn": str,
        "RoleArn": str,
    },
)

_RequiredOutputConfigTypeDef = TypedDict(
    "_RequiredOutputConfigTypeDef",
    {
        "S3Bucket": str,
    },
)
_OptionalOutputConfigTypeDef = TypedDict(
    "_OptionalOutputConfigTypeDef",
    {
        "S3Prefix": str,
    },
    total=False,
)


class OutputConfigTypeDef(_RequiredOutputConfigTypeDef, _OptionalOutputConfigTypeDef):
    pass


StartDocumentAnalysisResponseTypeDef = TypedDict(
    "StartDocumentAnalysisResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDocumentTextDetectionResponseTypeDef = TypedDict(
    "StartDocumentTextDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartExpenseAnalysisResponseTypeDef = TypedDict(
    "StartExpenseAnalysisResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAnalyzeIDDetectionsTypeDef = TypedDict(
    "_RequiredAnalyzeIDDetectionsTypeDef",
    {
        "Text": str,
    },
)
_OptionalAnalyzeIDDetectionsTypeDef = TypedDict(
    "_OptionalAnalyzeIDDetectionsTypeDef",
    {
        "NormalizedValue": NormalizedValueTypeDef,
        "Confidence": float,
    },
    total=False,
)


class AnalyzeIDDetectionsTypeDef(
    _RequiredAnalyzeIDDetectionsTypeDef, _OptionalAnalyzeIDDetectionsTypeDef
):
    pass


QueriesConfigTypeDef = TypedDict(
    "QueriesConfigTypeDef",
    {
        "Queries": Sequence[QueryTypeDef],
    },
)

DocumentLocationTypeDef = TypedDict(
    "DocumentLocationTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

DocumentTypeDef = TypedDict(
    "DocumentTypeDef",
    {
        "Bytes": Union[str, bytes, IO[Any], StreamingBody],
        "S3Object": S3ObjectTypeDef,
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


IdentityDocumentFieldTypeDef = TypedDict(
    "IdentityDocumentFieldTypeDef",
    {
        "Type": AnalyzeIDDetectionsTypeDef,
        "ValueDetection": AnalyzeIDDetectionsTypeDef,
    },
    total=False,
)

_RequiredStartDocumentAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredStartDocumentAnalysisRequestRequestTypeDef",
    {
        "DocumentLocation": DocumentLocationTypeDef,
        "FeatureTypes": Sequence[FeatureTypeType],
    },
)
_OptionalStartDocumentAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalStartDocumentAnalysisRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "JobTag": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "OutputConfig": OutputConfigTypeDef,
        "KMSKeyId": str,
        "QueriesConfig": QueriesConfigTypeDef,
    },
    total=False,
)


class StartDocumentAnalysisRequestRequestTypeDef(
    _RequiredStartDocumentAnalysisRequestRequestTypeDef,
    _OptionalStartDocumentAnalysisRequestRequestTypeDef,
):
    pass


_RequiredStartDocumentTextDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartDocumentTextDetectionRequestRequestTypeDef",
    {
        "DocumentLocation": DocumentLocationTypeDef,
    },
)
_OptionalStartDocumentTextDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartDocumentTextDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "JobTag": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "OutputConfig": OutputConfigTypeDef,
        "KMSKeyId": str,
    },
    total=False,
)


class StartDocumentTextDetectionRequestRequestTypeDef(
    _RequiredStartDocumentTextDetectionRequestRequestTypeDef,
    _OptionalStartDocumentTextDetectionRequestRequestTypeDef,
):
    pass


_RequiredStartExpenseAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredStartExpenseAnalysisRequestRequestTypeDef",
    {
        "DocumentLocation": DocumentLocationTypeDef,
    },
)
_OptionalStartExpenseAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalStartExpenseAnalysisRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "JobTag": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "OutputConfig": OutputConfigTypeDef,
        "KMSKeyId": str,
    },
    total=False,
)


class StartExpenseAnalysisRequestRequestTypeDef(
    _RequiredStartExpenseAnalysisRequestRequestTypeDef,
    _OptionalStartExpenseAnalysisRequestRequestTypeDef,
):
    pass


AnalyzeExpenseRequestRequestTypeDef = TypedDict(
    "AnalyzeExpenseRequestRequestTypeDef",
    {
        "Document": DocumentTypeDef,
    },
)

AnalyzeIDRequestRequestTypeDef = TypedDict(
    "AnalyzeIDRequestRequestTypeDef",
    {
        "DocumentPages": Sequence[DocumentTypeDef],
    },
)

DetectDocumentTextRequestRequestTypeDef = TypedDict(
    "DetectDocumentTextRequestRequestTypeDef",
    {
        "Document": DocumentTypeDef,
    },
)

BlockTypeDef = TypedDict(
    "BlockTypeDef",
    {
        "BlockType": BlockTypeType,
        "Confidence": float,
        "Text": str,
        "TextType": TextTypeType,
        "RowIndex": int,
        "ColumnIndex": int,
        "RowSpan": int,
        "ColumnSpan": int,
        "Geometry": GeometryTypeDef,
        "Id": str,
        "Relationships": List[RelationshipTypeDef],
        "EntityTypes": List[EntityTypeType],
        "SelectionStatus": SelectionStatusType,
        "Page": int,
        "Query": QueryTypeDef,
    },
    total=False,
)

ExpenseDetectionTypeDef = TypedDict(
    "ExpenseDetectionTypeDef",
    {
        "Text": str,
        "Geometry": GeometryTypeDef,
        "Confidence": float,
    },
    total=False,
)

_RequiredAnalyzeDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredAnalyzeDocumentRequestRequestTypeDef",
    {
        "Document": DocumentTypeDef,
        "FeatureTypes": Sequence[FeatureTypeType],
    },
)
_OptionalAnalyzeDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalAnalyzeDocumentRequestRequestTypeDef",
    {
        "HumanLoopConfig": HumanLoopConfigTypeDef,
        "QueriesConfig": QueriesConfigTypeDef,
    },
    total=False,
)


class AnalyzeDocumentRequestRequestTypeDef(
    _RequiredAnalyzeDocumentRequestRequestTypeDef, _OptionalAnalyzeDocumentRequestRequestTypeDef
):
    pass


IdentityDocumentTypeDef = TypedDict(
    "IdentityDocumentTypeDef",
    {
        "DocumentIndex": int,
        "IdentityDocumentFields": List[IdentityDocumentFieldTypeDef],
    },
    total=False,
)

AnalyzeDocumentResponseTypeDef = TypedDict(
    "AnalyzeDocumentResponseTypeDef",
    {
        "DocumentMetadata": DocumentMetadataTypeDef,
        "Blocks": List[BlockTypeDef],
        "HumanLoopActivationOutput": HumanLoopActivationOutputTypeDef,
        "AnalyzeDocumentModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectDocumentTextResponseTypeDef = TypedDict(
    "DetectDocumentTextResponseTypeDef",
    {
        "DocumentMetadata": DocumentMetadataTypeDef,
        "Blocks": List[BlockTypeDef],
        "DetectDocumentTextModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDocumentAnalysisResponseTypeDef = TypedDict(
    "GetDocumentAnalysisResponseTypeDef",
    {
        "DocumentMetadata": DocumentMetadataTypeDef,
        "JobStatus": JobStatusType,
        "NextToken": str,
        "Blocks": List[BlockTypeDef],
        "Warnings": List[WarningTypeDef],
        "StatusMessage": str,
        "AnalyzeDocumentModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDocumentTextDetectionResponseTypeDef = TypedDict(
    "GetDocumentTextDetectionResponseTypeDef",
    {
        "DocumentMetadata": DocumentMetadataTypeDef,
        "JobStatus": JobStatusType,
        "NextToken": str,
        "Blocks": List[BlockTypeDef],
        "Warnings": List[WarningTypeDef],
        "StatusMessage": str,
        "DetectDocumentTextModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExpenseFieldTypeDef = TypedDict(
    "ExpenseFieldTypeDef",
    {
        "Type": ExpenseTypeTypeDef,
        "LabelDetection": ExpenseDetectionTypeDef,
        "ValueDetection": ExpenseDetectionTypeDef,
        "PageNumber": int,
    },
    total=False,
)

AnalyzeIDResponseTypeDef = TypedDict(
    "AnalyzeIDResponseTypeDef",
    {
        "IdentityDocuments": List[IdentityDocumentTypeDef],
        "DocumentMetadata": DocumentMetadataTypeDef,
        "AnalyzeIDModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LineItemFieldsTypeDef = TypedDict(
    "LineItemFieldsTypeDef",
    {
        "LineItemExpenseFields": List[ExpenseFieldTypeDef],
    },
    total=False,
)

LineItemGroupTypeDef = TypedDict(
    "LineItemGroupTypeDef",
    {
        "LineItemGroupIndex": int,
        "LineItems": List[LineItemFieldsTypeDef],
    },
    total=False,
)

ExpenseDocumentTypeDef = TypedDict(
    "ExpenseDocumentTypeDef",
    {
        "ExpenseIndex": int,
        "SummaryFields": List[ExpenseFieldTypeDef],
        "LineItemGroups": List[LineItemGroupTypeDef],
    },
    total=False,
)

AnalyzeExpenseResponseTypeDef = TypedDict(
    "AnalyzeExpenseResponseTypeDef",
    {
        "DocumentMetadata": DocumentMetadataTypeDef,
        "ExpenseDocuments": List[ExpenseDocumentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExpenseAnalysisResponseTypeDef = TypedDict(
    "GetExpenseAnalysisResponseTypeDef",
    {
        "DocumentMetadata": DocumentMetadataTypeDef,
        "JobStatus": JobStatusType,
        "NextToken": str,
        "ExpenseDocuments": List[ExpenseDocumentTypeDef],
        "Warnings": List[WarningTypeDef],
        "StatusMessage": str,
        "AnalyzeExpenseModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
