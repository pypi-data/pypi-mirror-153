"""
Type annotations for comprehendmedical service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehendmedical/type_defs/)

Usage::

    ```python
    from mypy_boto3_comprehendmedical.type_defs import TraitTypeDef

    data: TraitTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Union

from .literals import (
    AttributeNameType,
    EntitySubTypeType,
    EntityTypeType,
    ICD10CMAttributeTypeType,
    ICD10CMEntityTypeType,
    ICD10CMRelationshipTypeType,
    ICD10CMTraitNameType,
    JobStatusType,
    RelationshipTypeType,
    RxNormAttributeTypeType,
    RxNormEntityTypeType,
    SNOMEDCTAttributeTypeType,
    SNOMEDCTEntityCategoryType,
    SNOMEDCTEntityTypeType,
    SNOMEDCTRelationshipTypeType,
    SNOMEDCTTraitNameType,
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
    "TraitTypeDef",
    "CharactersTypeDef",
    "ComprehendMedicalAsyncJobFilterTypeDef",
    "InputDataConfigTypeDef",
    "OutputDataConfigTypeDef",
    "DescribeEntitiesDetectionV2JobRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeICD10CMInferenceJobRequestRequestTypeDef",
    "DescribePHIDetectionJobRequestRequestTypeDef",
    "DescribeRxNormInferenceJobRequestRequestTypeDef",
    "DescribeSNOMEDCTInferenceJobRequestRequestTypeDef",
    "DetectEntitiesRequestRequestTypeDef",
    "DetectEntitiesV2RequestRequestTypeDef",
    "DetectPHIRequestRequestTypeDef",
    "ICD10CMTraitTypeDef",
    "ICD10CMConceptTypeDef",
    "InferICD10CMRequestRequestTypeDef",
    "InferRxNormRequestRequestTypeDef",
    "InferSNOMEDCTRequestRequestTypeDef",
    "SNOMEDCTDetailsTypeDef",
    "RxNormTraitTypeDef",
    "RxNormConceptTypeDef",
    "SNOMEDCTConceptTypeDef",
    "SNOMEDCTTraitTypeDef",
    "StopEntitiesDetectionV2JobRequestRequestTypeDef",
    "StopICD10CMInferenceJobRequestRequestTypeDef",
    "StopPHIDetectionJobRequestRequestTypeDef",
    "StopRxNormInferenceJobRequestRequestTypeDef",
    "StopSNOMEDCTInferenceJobRequestRequestTypeDef",
    "AttributeTypeDef",
    "ListEntitiesDetectionV2JobsRequestRequestTypeDef",
    "ListICD10CMInferenceJobsRequestRequestTypeDef",
    "ListPHIDetectionJobsRequestRequestTypeDef",
    "ListRxNormInferenceJobsRequestRequestTypeDef",
    "ListSNOMEDCTInferenceJobsRequestRequestTypeDef",
    "ComprehendMedicalAsyncJobPropertiesTypeDef",
    "StartEntitiesDetectionV2JobRequestRequestTypeDef",
    "StartICD10CMInferenceJobRequestRequestTypeDef",
    "StartPHIDetectionJobRequestRequestTypeDef",
    "StartRxNormInferenceJobRequestRequestTypeDef",
    "StartSNOMEDCTInferenceJobRequestRequestTypeDef",
    "StartEntitiesDetectionV2JobResponseTypeDef",
    "StartICD10CMInferenceJobResponseTypeDef",
    "StartPHIDetectionJobResponseTypeDef",
    "StartRxNormInferenceJobResponseTypeDef",
    "StartSNOMEDCTInferenceJobResponseTypeDef",
    "StopEntitiesDetectionV2JobResponseTypeDef",
    "StopICD10CMInferenceJobResponseTypeDef",
    "StopPHIDetectionJobResponseTypeDef",
    "StopRxNormInferenceJobResponseTypeDef",
    "StopSNOMEDCTInferenceJobResponseTypeDef",
    "ICD10CMAttributeTypeDef",
    "RxNormAttributeTypeDef",
    "SNOMEDCTAttributeTypeDef",
    "EntityTypeDef",
    "UnmappedAttributeTypeDef",
    "DescribeEntitiesDetectionV2JobResponseTypeDef",
    "DescribeICD10CMInferenceJobResponseTypeDef",
    "DescribePHIDetectionJobResponseTypeDef",
    "DescribeRxNormInferenceJobResponseTypeDef",
    "DescribeSNOMEDCTInferenceJobResponseTypeDef",
    "ListEntitiesDetectionV2JobsResponseTypeDef",
    "ListICD10CMInferenceJobsResponseTypeDef",
    "ListPHIDetectionJobsResponseTypeDef",
    "ListRxNormInferenceJobsResponseTypeDef",
    "ListSNOMEDCTInferenceJobsResponseTypeDef",
    "ICD10CMEntityTypeDef",
    "RxNormEntityTypeDef",
    "SNOMEDCTEntityTypeDef",
    "DetectPHIResponseTypeDef",
    "DetectEntitiesResponseTypeDef",
    "DetectEntitiesV2ResponseTypeDef",
    "InferICD10CMResponseTypeDef",
    "InferRxNormResponseTypeDef",
    "InferSNOMEDCTResponseTypeDef",
)

TraitTypeDef = TypedDict(
    "TraitTypeDef",
    {
        "Name": AttributeNameType,
        "Score": float,
    },
    total=False,
)

CharactersTypeDef = TypedDict(
    "CharactersTypeDef",
    {
        "OriginalTextCharacters": int,
    },
    total=False,
)

ComprehendMedicalAsyncJobFilterTypeDef = TypedDict(
    "ComprehendMedicalAsyncJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

_RequiredInputDataConfigTypeDef = TypedDict(
    "_RequiredInputDataConfigTypeDef",
    {
        "S3Bucket": str,
    },
)
_OptionalInputDataConfigTypeDef = TypedDict(
    "_OptionalInputDataConfigTypeDef",
    {
        "S3Key": str,
    },
    total=False,
)


class InputDataConfigTypeDef(_RequiredInputDataConfigTypeDef, _OptionalInputDataConfigTypeDef):
    pass


_RequiredOutputDataConfigTypeDef = TypedDict(
    "_RequiredOutputDataConfigTypeDef",
    {
        "S3Bucket": str,
    },
)
_OptionalOutputDataConfigTypeDef = TypedDict(
    "_OptionalOutputDataConfigTypeDef",
    {
        "S3Key": str,
    },
    total=False,
)


class OutputDataConfigTypeDef(_RequiredOutputDataConfigTypeDef, _OptionalOutputDataConfigTypeDef):
    pass


DescribeEntitiesDetectionV2JobRequestRequestTypeDef = TypedDict(
    "DescribeEntitiesDetectionV2JobRequestRequestTypeDef",
    {
        "JobId": str,
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

DescribeICD10CMInferenceJobRequestRequestTypeDef = TypedDict(
    "DescribeICD10CMInferenceJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribePHIDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribePHIDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeRxNormInferenceJobRequestRequestTypeDef = TypedDict(
    "DescribeRxNormInferenceJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeSNOMEDCTInferenceJobRequestRequestTypeDef = TypedDict(
    "DescribeSNOMEDCTInferenceJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DetectEntitiesRequestRequestTypeDef = TypedDict(
    "DetectEntitiesRequestRequestTypeDef",
    {
        "Text": str,
    },
)

DetectEntitiesV2RequestRequestTypeDef = TypedDict(
    "DetectEntitiesV2RequestRequestTypeDef",
    {
        "Text": str,
    },
)

DetectPHIRequestRequestTypeDef = TypedDict(
    "DetectPHIRequestRequestTypeDef",
    {
        "Text": str,
    },
)

ICD10CMTraitTypeDef = TypedDict(
    "ICD10CMTraitTypeDef",
    {
        "Name": ICD10CMTraitNameType,
        "Score": float,
    },
    total=False,
)

ICD10CMConceptTypeDef = TypedDict(
    "ICD10CMConceptTypeDef",
    {
        "Description": str,
        "Code": str,
        "Score": float,
    },
    total=False,
)

InferICD10CMRequestRequestTypeDef = TypedDict(
    "InferICD10CMRequestRequestTypeDef",
    {
        "Text": str,
    },
)

InferRxNormRequestRequestTypeDef = TypedDict(
    "InferRxNormRequestRequestTypeDef",
    {
        "Text": str,
    },
)

InferSNOMEDCTRequestRequestTypeDef = TypedDict(
    "InferSNOMEDCTRequestRequestTypeDef",
    {
        "Text": str,
    },
)

SNOMEDCTDetailsTypeDef = TypedDict(
    "SNOMEDCTDetailsTypeDef",
    {
        "Edition": str,
        "Language": str,
        "VersionDate": str,
    },
    total=False,
)

RxNormTraitTypeDef = TypedDict(
    "RxNormTraitTypeDef",
    {
        "Name": Literal["NEGATION"],
        "Score": float,
    },
    total=False,
)

RxNormConceptTypeDef = TypedDict(
    "RxNormConceptTypeDef",
    {
        "Description": str,
        "Code": str,
        "Score": float,
    },
    total=False,
)

SNOMEDCTConceptTypeDef = TypedDict(
    "SNOMEDCTConceptTypeDef",
    {
        "Description": str,
        "Code": str,
        "Score": float,
    },
    total=False,
)

SNOMEDCTTraitTypeDef = TypedDict(
    "SNOMEDCTTraitTypeDef",
    {
        "Name": SNOMEDCTTraitNameType,
        "Score": float,
    },
    total=False,
)

StopEntitiesDetectionV2JobRequestRequestTypeDef = TypedDict(
    "StopEntitiesDetectionV2JobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopICD10CMInferenceJobRequestRequestTypeDef = TypedDict(
    "StopICD10CMInferenceJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopPHIDetectionJobRequestRequestTypeDef = TypedDict(
    "StopPHIDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopRxNormInferenceJobRequestRequestTypeDef = TypedDict(
    "StopRxNormInferenceJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopSNOMEDCTInferenceJobRequestRequestTypeDef = TypedDict(
    "StopSNOMEDCTInferenceJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "Type": EntitySubTypeType,
        "Score": float,
        "RelationshipScore": float,
        "RelationshipType": RelationshipTypeType,
        "Id": int,
        "BeginOffset": int,
        "EndOffset": int,
        "Text": str,
        "Category": EntityTypeType,
        "Traits": List[TraitTypeDef],
    },
    total=False,
)

ListEntitiesDetectionV2JobsRequestRequestTypeDef = TypedDict(
    "ListEntitiesDetectionV2JobsRequestRequestTypeDef",
    {
        "Filter": ComprehendMedicalAsyncJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListICD10CMInferenceJobsRequestRequestTypeDef = TypedDict(
    "ListICD10CMInferenceJobsRequestRequestTypeDef",
    {
        "Filter": ComprehendMedicalAsyncJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListPHIDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListPHIDetectionJobsRequestRequestTypeDef",
    {
        "Filter": ComprehendMedicalAsyncJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListRxNormInferenceJobsRequestRequestTypeDef = TypedDict(
    "ListRxNormInferenceJobsRequestRequestTypeDef",
    {
        "Filter": ComprehendMedicalAsyncJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListSNOMEDCTInferenceJobsRequestRequestTypeDef = TypedDict(
    "ListSNOMEDCTInferenceJobsRequestRequestTypeDef",
    {
        "Filter": ComprehendMedicalAsyncJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ComprehendMedicalAsyncJobPropertiesTypeDef = TypedDict(
    "ComprehendMedicalAsyncJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "ExpirationTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "LanguageCode": Literal["en"],
        "DataAccessRoleArn": str,
        "ManifestFilePath": str,
        "KMSKey": str,
        "ModelVersion": str,
    },
    total=False,
)

_RequiredStartEntitiesDetectionV2JobRequestRequestTypeDef = TypedDict(
    "_RequiredStartEntitiesDetectionV2JobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": Literal["en"],
    },
)
_OptionalStartEntitiesDetectionV2JobRequestRequestTypeDef = TypedDict(
    "_OptionalStartEntitiesDetectionV2JobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "KMSKey": str,
    },
    total=False,
)


class StartEntitiesDetectionV2JobRequestRequestTypeDef(
    _RequiredStartEntitiesDetectionV2JobRequestRequestTypeDef,
    _OptionalStartEntitiesDetectionV2JobRequestRequestTypeDef,
):
    pass


_RequiredStartICD10CMInferenceJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartICD10CMInferenceJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": Literal["en"],
    },
)
_OptionalStartICD10CMInferenceJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartICD10CMInferenceJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "KMSKey": str,
    },
    total=False,
)


class StartICD10CMInferenceJobRequestRequestTypeDef(
    _RequiredStartICD10CMInferenceJobRequestRequestTypeDef,
    _OptionalStartICD10CMInferenceJobRequestRequestTypeDef,
):
    pass


_RequiredStartPHIDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartPHIDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": Literal["en"],
    },
)
_OptionalStartPHIDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartPHIDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "KMSKey": str,
    },
    total=False,
)


class StartPHIDetectionJobRequestRequestTypeDef(
    _RequiredStartPHIDetectionJobRequestRequestTypeDef,
    _OptionalStartPHIDetectionJobRequestRequestTypeDef,
):
    pass


_RequiredStartRxNormInferenceJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartRxNormInferenceJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": Literal["en"],
    },
)
_OptionalStartRxNormInferenceJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartRxNormInferenceJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "KMSKey": str,
    },
    total=False,
)


class StartRxNormInferenceJobRequestRequestTypeDef(
    _RequiredStartRxNormInferenceJobRequestRequestTypeDef,
    _OptionalStartRxNormInferenceJobRequestRequestTypeDef,
):
    pass


_RequiredStartSNOMEDCTInferenceJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartSNOMEDCTInferenceJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": Literal["en"],
    },
)
_OptionalStartSNOMEDCTInferenceJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartSNOMEDCTInferenceJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "KMSKey": str,
    },
    total=False,
)


class StartSNOMEDCTInferenceJobRequestRequestTypeDef(
    _RequiredStartSNOMEDCTInferenceJobRequestRequestTypeDef,
    _OptionalStartSNOMEDCTInferenceJobRequestRequestTypeDef,
):
    pass


StartEntitiesDetectionV2JobResponseTypeDef = TypedDict(
    "StartEntitiesDetectionV2JobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartICD10CMInferenceJobResponseTypeDef = TypedDict(
    "StartICD10CMInferenceJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartPHIDetectionJobResponseTypeDef = TypedDict(
    "StartPHIDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartRxNormInferenceJobResponseTypeDef = TypedDict(
    "StartRxNormInferenceJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSNOMEDCTInferenceJobResponseTypeDef = TypedDict(
    "StartSNOMEDCTInferenceJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopEntitiesDetectionV2JobResponseTypeDef = TypedDict(
    "StopEntitiesDetectionV2JobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopICD10CMInferenceJobResponseTypeDef = TypedDict(
    "StopICD10CMInferenceJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopPHIDetectionJobResponseTypeDef = TypedDict(
    "StopPHIDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopRxNormInferenceJobResponseTypeDef = TypedDict(
    "StopRxNormInferenceJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopSNOMEDCTInferenceJobResponseTypeDef = TypedDict(
    "StopSNOMEDCTInferenceJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ICD10CMAttributeTypeDef = TypedDict(
    "ICD10CMAttributeTypeDef",
    {
        "Type": ICD10CMAttributeTypeType,
        "Score": float,
        "RelationshipScore": float,
        "Id": int,
        "BeginOffset": int,
        "EndOffset": int,
        "Text": str,
        "Traits": List[ICD10CMTraitTypeDef],
        "Category": ICD10CMEntityTypeType,
        "RelationshipType": ICD10CMRelationshipTypeType,
    },
    total=False,
)

RxNormAttributeTypeDef = TypedDict(
    "RxNormAttributeTypeDef",
    {
        "Type": RxNormAttributeTypeType,
        "Score": float,
        "RelationshipScore": float,
        "Id": int,
        "BeginOffset": int,
        "EndOffset": int,
        "Text": str,
        "Traits": List[RxNormTraitTypeDef],
    },
    total=False,
)

SNOMEDCTAttributeTypeDef = TypedDict(
    "SNOMEDCTAttributeTypeDef",
    {
        "Category": SNOMEDCTEntityCategoryType,
        "Type": SNOMEDCTAttributeTypeType,
        "Score": float,
        "RelationshipScore": float,
        "RelationshipType": SNOMEDCTRelationshipTypeType,
        "Id": int,
        "BeginOffset": int,
        "EndOffset": int,
        "Text": str,
        "Traits": List[SNOMEDCTTraitTypeDef],
        "SNOMEDCTConcepts": List[SNOMEDCTConceptTypeDef],
    },
    total=False,
)

EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Id": int,
        "BeginOffset": int,
        "EndOffset": int,
        "Score": float,
        "Text": str,
        "Category": EntityTypeType,
        "Type": EntitySubTypeType,
        "Traits": List[TraitTypeDef],
        "Attributes": List[AttributeTypeDef],
    },
    total=False,
)

UnmappedAttributeTypeDef = TypedDict(
    "UnmappedAttributeTypeDef",
    {
        "Type": EntityTypeType,
        "Attribute": AttributeTypeDef,
    },
    total=False,
)

DescribeEntitiesDetectionV2JobResponseTypeDef = TypedDict(
    "DescribeEntitiesDetectionV2JobResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobProperties": ComprehendMedicalAsyncJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeICD10CMInferenceJobResponseTypeDef = TypedDict(
    "DescribeICD10CMInferenceJobResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobProperties": ComprehendMedicalAsyncJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePHIDetectionJobResponseTypeDef = TypedDict(
    "DescribePHIDetectionJobResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobProperties": ComprehendMedicalAsyncJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRxNormInferenceJobResponseTypeDef = TypedDict(
    "DescribeRxNormInferenceJobResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobProperties": ComprehendMedicalAsyncJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSNOMEDCTInferenceJobResponseTypeDef = TypedDict(
    "DescribeSNOMEDCTInferenceJobResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobProperties": ComprehendMedicalAsyncJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEntitiesDetectionV2JobsResponseTypeDef = TypedDict(
    "ListEntitiesDetectionV2JobsResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobPropertiesList": List[ComprehendMedicalAsyncJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListICD10CMInferenceJobsResponseTypeDef = TypedDict(
    "ListICD10CMInferenceJobsResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobPropertiesList": List[ComprehendMedicalAsyncJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPHIDetectionJobsResponseTypeDef = TypedDict(
    "ListPHIDetectionJobsResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobPropertiesList": List[ComprehendMedicalAsyncJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRxNormInferenceJobsResponseTypeDef = TypedDict(
    "ListRxNormInferenceJobsResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobPropertiesList": List[ComprehendMedicalAsyncJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSNOMEDCTInferenceJobsResponseTypeDef = TypedDict(
    "ListSNOMEDCTInferenceJobsResponseTypeDef",
    {
        "ComprehendMedicalAsyncJobPropertiesList": List[ComprehendMedicalAsyncJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ICD10CMEntityTypeDef = TypedDict(
    "ICD10CMEntityTypeDef",
    {
        "Id": int,
        "Text": str,
        "Category": Literal["MEDICAL_CONDITION"],
        "Type": ICD10CMEntityTypeType,
        "Score": float,
        "BeginOffset": int,
        "EndOffset": int,
        "Attributes": List[ICD10CMAttributeTypeDef],
        "Traits": List[ICD10CMTraitTypeDef],
        "ICD10CMConcepts": List[ICD10CMConceptTypeDef],
    },
    total=False,
)

RxNormEntityTypeDef = TypedDict(
    "RxNormEntityTypeDef",
    {
        "Id": int,
        "Text": str,
        "Category": Literal["MEDICATION"],
        "Type": RxNormEntityTypeType,
        "Score": float,
        "BeginOffset": int,
        "EndOffset": int,
        "Attributes": List[RxNormAttributeTypeDef],
        "Traits": List[RxNormTraitTypeDef],
        "RxNormConcepts": List[RxNormConceptTypeDef],
    },
    total=False,
)

SNOMEDCTEntityTypeDef = TypedDict(
    "SNOMEDCTEntityTypeDef",
    {
        "Id": int,
        "Text": str,
        "Category": SNOMEDCTEntityCategoryType,
        "Type": SNOMEDCTEntityTypeType,
        "Score": float,
        "BeginOffset": int,
        "EndOffset": int,
        "Attributes": List[SNOMEDCTAttributeTypeDef],
        "Traits": List[SNOMEDCTTraitTypeDef],
        "SNOMEDCTConcepts": List[SNOMEDCTConceptTypeDef],
    },
    total=False,
)

DetectPHIResponseTypeDef = TypedDict(
    "DetectPHIResponseTypeDef",
    {
        "Entities": List[EntityTypeDef],
        "PaginationToken": str,
        "ModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectEntitiesResponseTypeDef = TypedDict(
    "DetectEntitiesResponseTypeDef",
    {
        "Entities": List[EntityTypeDef],
        "UnmappedAttributes": List[UnmappedAttributeTypeDef],
        "PaginationToken": str,
        "ModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectEntitiesV2ResponseTypeDef = TypedDict(
    "DetectEntitiesV2ResponseTypeDef",
    {
        "Entities": List[EntityTypeDef],
        "UnmappedAttributes": List[UnmappedAttributeTypeDef],
        "PaginationToken": str,
        "ModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InferICD10CMResponseTypeDef = TypedDict(
    "InferICD10CMResponseTypeDef",
    {
        "Entities": List[ICD10CMEntityTypeDef],
        "PaginationToken": str,
        "ModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InferRxNormResponseTypeDef = TypedDict(
    "InferRxNormResponseTypeDef",
    {
        "Entities": List[RxNormEntityTypeDef],
        "PaginationToken": str,
        "ModelVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InferSNOMEDCTResponseTypeDef = TypedDict(
    "InferSNOMEDCTResponseTypeDef",
    {
        "Entities": List[SNOMEDCTEntityTypeDef],
        "PaginationToken": str,
        "ModelVersion": str,
        "SNOMEDCTDetails": SNOMEDCTDetailsTypeDef,
        "Characters": CharactersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
