"""
Type annotations for translate service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_translate/type_defs/)

Usage::

    ```python
    from mypy_boto3_translate.type_defs import TermTypeDef

    data: TermTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DirectionalityType,
    FormalityType,
    JobStatusType,
    ParallelDataFormatType,
    ParallelDataStatusType,
    TerminologyDataFormatType,
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
    "TermTypeDef",
    "EncryptionKeyTypeDef",
    "ParallelDataConfigTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteParallelDataRequestRequestTypeDef",
    "DeleteTerminologyRequestRequestTypeDef",
    "DescribeTextTranslationJobRequestRequestTypeDef",
    "GetParallelDataRequestRequestTypeDef",
    "ParallelDataDataLocationTypeDef",
    "GetTerminologyRequestRequestTypeDef",
    "TerminologyDataLocationTypeDef",
    "TerminologyDataTypeDef",
    "InputDataConfigTypeDef",
    "JobDetailsTypeDef",
    "ListParallelDataRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListTerminologiesRequestRequestTypeDef",
    "TextTranslationJobFilterTypeDef",
    "TranslationSettingsTypeDef",
    "StopTextTranslationJobRequestRequestTypeDef",
    "AppliedTerminologyTypeDef",
    "OutputDataConfigTypeDef",
    "TerminologyPropertiesTypeDef",
    "CreateParallelDataRequestRequestTypeDef",
    "ParallelDataPropertiesTypeDef",
    "UpdateParallelDataRequestRequestTypeDef",
    "CreateParallelDataResponseTypeDef",
    "DeleteParallelDataResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "StartTextTranslationJobResponseTypeDef",
    "StopTextTranslationJobResponseTypeDef",
    "UpdateParallelDataResponseTypeDef",
    "ImportTerminologyRequestRequestTypeDef",
    "ListTerminologiesRequestListTerminologiesPaginateTypeDef",
    "ListTextTranslationJobsRequestRequestTypeDef",
    "TranslateTextRequestRequestTypeDef",
    "TranslateTextResponseTypeDef",
    "StartTextTranslationJobRequestRequestTypeDef",
    "TextTranslationJobPropertiesTypeDef",
    "GetTerminologyResponseTypeDef",
    "ImportTerminologyResponseTypeDef",
    "ListTerminologiesResponseTypeDef",
    "GetParallelDataResponseTypeDef",
    "ListParallelDataResponseTypeDef",
    "DescribeTextTranslationJobResponseTypeDef",
    "ListTextTranslationJobsResponseTypeDef",
)

TermTypeDef = TypedDict(
    "TermTypeDef",
    {
        "SourceText": str,
        "TargetText": str,
    },
    total=False,
)

EncryptionKeyTypeDef = TypedDict(
    "EncryptionKeyTypeDef",
    {
        "Type": Literal["KMS"],
        "Id": str,
    },
)

ParallelDataConfigTypeDef = TypedDict(
    "ParallelDataConfigTypeDef",
    {
        "S3Uri": str,
        "Format": ParallelDataFormatType,
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

DeleteParallelDataRequestRequestTypeDef = TypedDict(
    "DeleteParallelDataRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteTerminologyRequestRequestTypeDef = TypedDict(
    "DeleteTerminologyRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeTextTranslationJobRequestRequestTypeDef = TypedDict(
    "DescribeTextTranslationJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetParallelDataRequestRequestTypeDef = TypedDict(
    "GetParallelDataRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ParallelDataDataLocationTypeDef = TypedDict(
    "ParallelDataDataLocationTypeDef",
    {
        "RepositoryType": str,
        "Location": str,
    },
)

_RequiredGetTerminologyRequestRequestTypeDef = TypedDict(
    "_RequiredGetTerminologyRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetTerminologyRequestRequestTypeDef = TypedDict(
    "_OptionalGetTerminologyRequestRequestTypeDef",
    {
        "TerminologyDataFormat": TerminologyDataFormatType,
    },
    total=False,
)


class GetTerminologyRequestRequestTypeDef(
    _RequiredGetTerminologyRequestRequestTypeDef, _OptionalGetTerminologyRequestRequestTypeDef
):
    pass


TerminologyDataLocationTypeDef = TypedDict(
    "TerminologyDataLocationTypeDef",
    {
        "RepositoryType": str,
        "Location": str,
    },
)

_RequiredTerminologyDataTypeDef = TypedDict(
    "_RequiredTerminologyDataTypeDef",
    {
        "File": Union[str, bytes, IO[Any], StreamingBody],
        "Format": TerminologyDataFormatType,
    },
)
_OptionalTerminologyDataTypeDef = TypedDict(
    "_OptionalTerminologyDataTypeDef",
    {
        "Directionality": DirectionalityType,
    },
    total=False,
)


class TerminologyDataTypeDef(_RequiredTerminologyDataTypeDef, _OptionalTerminologyDataTypeDef):
    pass


InputDataConfigTypeDef = TypedDict(
    "InputDataConfigTypeDef",
    {
        "S3Uri": str,
        "ContentType": str,
    },
)

JobDetailsTypeDef = TypedDict(
    "JobDetailsTypeDef",
    {
        "TranslatedDocumentsCount": int,
        "DocumentsWithErrorsCount": int,
        "InputDocumentsCount": int,
    },
    total=False,
)

ListParallelDataRequestRequestTypeDef = TypedDict(
    "ListParallelDataRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
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

ListTerminologiesRequestRequestTypeDef = TypedDict(
    "ListTerminologiesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

TextTranslationJobFilterTypeDef = TypedDict(
    "TextTranslationJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmittedBeforeTime": Union[datetime, str],
        "SubmittedAfterTime": Union[datetime, str],
    },
    total=False,
)

TranslationSettingsTypeDef = TypedDict(
    "TranslationSettingsTypeDef",
    {
        "Formality": FormalityType,
        "Profanity": Literal["MASK"],
    },
    total=False,
)

StopTextTranslationJobRequestRequestTypeDef = TypedDict(
    "StopTextTranslationJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

AppliedTerminologyTypeDef = TypedDict(
    "AppliedTerminologyTypeDef",
    {
        "Name": str,
        "Terms": List[TermTypeDef],
    },
    total=False,
)

_RequiredOutputDataConfigTypeDef = TypedDict(
    "_RequiredOutputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalOutputDataConfigTypeDef = TypedDict(
    "_OptionalOutputDataConfigTypeDef",
    {
        "EncryptionKey": EncryptionKeyTypeDef,
    },
    total=False,
)


class OutputDataConfigTypeDef(_RequiredOutputDataConfigTypeDef, _OptionalOutputDataConfigTypeDef):
    pass


TerminologyPropertiesTypeDef = TypedDict(
    "TerminologyPropertiesTypeDef",
    {
        "Name": str,
        "Description": str,
        "Arn": str,
        "SourceLanguageCode": str,
        "TargetLanguageCodes": List[str],
        "EncryptionKey": EncryptionKeyTypeDef,
        "SizeBytes": int,
        "TermCount": int,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Directionality": DirectionalityType,
        "Message": str,
        "SkippedTermCount": int,
        "Format": TerminologyDataFormatType,
    },
    total=False,
)

_RequiredCreateParallelDataRequestRequestTypeDef = TypedDict(
    "_RequiredCreateParallelDataRequestRequestTypeDef",
    {
        "Name": str,
        "ParallelDataConfig": ParallelDataConfigTypeDef,
        "ClientToken": str,
    },
)
_OptionalCreateParallelDataRequestRequestTypeDef = TypedDict(
    "_OptionalCreateParallelDataRequestRequestTypeDef",
    {
        "Description": str,
        "EncryptionKey": EncryptionKeyTypeDef,
    },
    total=False,
)


class CreateParallelDataRequestRequestTypeDef(
    _RequiredCreateParallelDataRequestRequestTypeDef,
    _OptionalCreateParallelDataRequestRequestTypeDef,
):
    pass


ParallelDataPropertiesTypeDef = TypedDict(
    "ParallelDataPropertiesTypeDef",
    {
        "Name": str,
        "Arn": str,
        "Description": str,
        "Status": ParallelDataStatusType,
        "SourceLanguageCode": str,
        "TargetLanguageCodes": List[str],
        "ParallelDataConfig": ParallelDataConfigTypeDef,
        "Message": str,
        "ImportedDataSize": int,
        "ImportedRecordCount": int,
        "FailedRecordCount": int,
        "SkippedRecordCount": int,
        "EncryptionKey": EncryptionKeyTypeDef,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "LatestUpdateAttemptStatus": ParallelDataStatusType,
        "LatestUpdateAttemptAt": datetime,
    },
    total=False,
)

_RequiredUpdateParallelDataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateParallelDataRequestRequestTypeDef",
    {
        "Name": str,
        "ParallelDataConfig": ParallelDataConfigTypeDef,
        "ClientToken": str,
    },
)
_OptionalUpdateParallelDataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateParallelDataRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateParallelDataRequestRequestTypeDef(
    _RequiredUpdateParallelDataRequestRequestTypeDef,
    _OptionalUpdateParallelDataRequestRequestTypeDef,
):
    pass


CreateParallelDataResponseTypeDef = TypedDict(
    "CreateParallelDataResponseTypeDef",
    {
        "Name": str,
        "Status": ParallelDataStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteParallelDataResponseTypeDef = TypedDict(
    "DeleteParallelDataResponseTypeDef",
    {
        "Name": str,
        "Status": ParallelDataStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTextTranslationJobResponseTypeDef = TypedDict(
    "StartTextTranslationJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopTextTranslationJobResponseTypeDef = TypedDict(
    "StopTextTranslationJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateParallelDataResponseTypeDef = TypedDict(
    "UpdateParallelDataResponseTypeDef",
    {
        "Name": str,
        "Status": ParallelDataStatusType,
        "LatestUpdateAttemptStatus": ParallelDataStatusType,
        "LatestUpdateAttemptAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImportTerminologyRequestRequestTypeDef = TypedDict(
    "_RequiredImportTerminologyRequestRequestTypeDef",
    {
        "Name": str,
        "MergeStrategy": Literal["OVERWRITE"],
        "TerminologyData": TerminologyDataTypeDef,
    },
)
_OptionalImportTerminologyRequestRequestTypeDef = TypedDict(
    "_OptionalImportTerminologyRequestRequestTypeDef",
    {
        "Description": str,
        "EncryptionKey": EncryptionKeyTypeDef,
    },
    total=False,
)


class ImportTerminologyRequestRequestTypeDef(
    _RequiredImportTerminologyRequestRequestTypeDef, _OptionalImportTerminologyRequestRequestTypeDef
):
    pass


ListTerminologiesRequestListTerminologiesPaginateTypeDef = TypedDict(
    "ListTerminologiesRequestListTerminologiesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTextTranslationJobsRequestRequestTypeDef = TypedDict(
    "ListTextTranslationJobsRequestRequestTypeDef",
    {
        "Filter": TextTranslationJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredTranslateTextRequestRequestTypeDef = TypedDict(
    "_RequiredTranslateTextRequestRequestTypeDef",
    {
        "Text": str,
        "SourceLanguageCode": str,
        "TargetLanguageCode": str,
    },
)
_OptionalTranslateTextRequestRequestTypeDef = TypedDict(
    "_OptionalTranslateTextRequestRequestTypeDef",
    {
        "TerminologyNames": Sequence[str],
        "Settings": TranslationSettingsTypeDef,
    },
    total=False,
)


class TranslateTextRequestRequestTypeDef(
    _RequiredTranslateTextRequestRequestTypeDef, _OptionalTranslateTextRequestRequestTypeDef
):
    pass


TranslateTextResponseTypeDef = TypedDict(
    "TranslateTextResponseTypeDef",
    {
        "TranslatedText": str,
        "SourceLanguageCode": str,
        "TargetLanguageCode": str,
        "AppliedTerminologies": List[AppliedTerminologyTypeDef],
        "AppliedSettings": TranslationSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartTextTranslationJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartTextTranslationJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "SourceLanguageCode": str,
        "TargetLanguageCodes": Sequence[str],
        "ClientToken": str,
    },
)
_OptionalStartTextTranslationJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartTextTranslationJobRequestRequestTypeDef",
    {
        "JobName": str,
        "TerminologyNames": Sequence[str],
        "ParallelDataNames": Sequence[str],
        "Settings": TranslationSettingsTypeDef,
    },
    total=False,
)


class StartTextTranslationJobRequestRequestTypeDef(
    _RequiredStartTextTranslationJobRequestRequestTypeDef,
    _OptionalStartTextTranslationJobRequestRequestTypeDef,
):
    pass


TextTranslationJobPropertiesTypeDef = TypedDict(
    "TextTranslationJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "JobDetails": JobDetailsTypeDef,
        "SourceLanguageCode": str,
        "TargetLanguageCodes": List[str],
        "TerminologyNames": List[str],
        "ParallelDataNames": List[str],
        "Message": str,
        "SubmittedTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "Settings": TranslationSettingsTypeDef,
    },
    total=False,
)

GetTerminologyResponseTypeDef = TypedDict(
    "GetTerminologyResponseTypeDef",
    {
        "TerminologyProperties": TerminologyPropertiesTypeDef,
        "TerminologyDataLocation": TerminologyDataLocationTypeDef,
        "AuxiliaryDataLocation": TerminologyDataLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportTerminologyResponseTypeDef = TypedDict(
    "ImportTerminologyResponseTypeDef",
    {
        "TerminologyProperties": TerminologyPropertiesTypeDef,
        "AuxiliaryDataLocation": TerminologyDataLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTerminologiesResponseTypeDef = TypedDict(
    "ListTerminologiesResponseTypeDef",
    {
        "TerminologyPropertiesList": List[TerminologyPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetParallelDataResponseTypeDef = TypedDict(
    "GetParallelDataResponseTypeDef",
    {
        "ParallelDataProperties": ParallelDataPropertiesTypeDef,
        "DataLocation": ParallelDataDataLocationTypeDef,
        "AuxiliaryDataLocation": ParallelDataDataLocationTypeDef,
        "LatestUpdateAttemptAuxiliaryDataLocation": ParallelDataDataLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListParallelDataResponseTypeDef = TypedDict(
    "ListParallelDataResponseTypeDef",
    {
        "ParallelDataPropertiesList": List[ParallelDataPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTextTranslationJobResponseTypeDef = TypedDict(
    "DescribeTextTranslationJobResponseTypeDef",
    {
        "TextTranslationJobProperties": TextTranslationJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTextTranslationJobsResponseTypeDef = TypedDict(
    "ListTextTranslationJobsResponseTypeDef",
    {
        "TextTranslationJobPropertiesList": List[TextTranslationJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
