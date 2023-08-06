"""
Type annotations for healthlake service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/type_defs/)

Usage::

    ```python
    from mypy_boto3_healthlake.type_defs import PreloadDataConfigTypeDef

    data: PreloadDataConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import CmkTypeType, DatastoreStatusType, JobStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "PreloadDataConfigTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DatastoreFilterTypeDef",
    "DeleteFHIRDatastoreRequestRequestTypeDef",
    "DescribeFHIRDatastoreRequestRequestTypeDef",
    "DescribeFHIRExportJobRequestRequestTypeDef",
    "DescribeFHIRImportJobRequestRequestTypeDef",
    "InputDataConfigTypeDef",
    "KmsEncryptionConfigTypeDef",
    "ListFHIRExportJobsRequestRequestTypeDef",
    "ListFHIRImportJobsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "S3ConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateFHIRDatastoreResponseTypeDef",
    "DeleteFHIRDatastoreResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartFHIRExportJobResponseTypeDef",
    "StartFHIRImportJobResponseTypeDef",
    "ListFHIRDatastoresRequestRequestTypeDef",
    "SseConfigurationTypeDef",
    "OutputDataConfigTypeDef",
    "CreateFHIRDatastoreRequestRequestTypeDef",
    "DatastorePropertiesTypeDef",
    "ExportJobPropertiesTypeDef",
    "ImportJobPropertiesTypeDef",
    "StartFHIRExportJobRequestRequestTypeDef",
    "StartFHIRImportJobRequestRequestTypeDef",
    "DescribeFHIRDatastoreResponseTypeDef",
    "ListFHIRDatastoresResponseTypeDef",
    "DescribeFHIRExportJobResponseTypeDef",
    "ListFHIRExportJobsResponseTypeDef",
    "DescribeFHIRImportJobResponseTypeDef",
    "ListFHIRImportJobsResponseTypeDef",
)

PreloadDataConfigTypeDef = TypedDict(
    "PreloadDataConfigTypeDef",
    {
        "PreloadDataType": Literal["SYNTHEA"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

DatastoreFilterTypeDef = TypedDict(
    "DatastoreFilterTypeDef",
    {
        "DatastoreName": str,
        "DatastoreStatus": DatastoreStatusType,
        "CreatedBefore": Union[datetime, str],
        "CreatedAfter": Union[datetime, str],
    },
    total=False,
)

DeleteFHIRDatastoreRequestRequestTypeDef = TypedDict(
    "DeleteFHIRDatastoreRequestRequestTypeDef",
    {
        "DatastoreId": str,
    },
    total=False,
)

DescribeFHIRDatastoreRequestRequestTypeDef = TypedDict(
    "DescribeFHIRDatastoreRequestRequestTypeDef",
    {
        "DatastoreId": str,
    },
    total=False,
)

DescribeFHIRExportJobRequestRequestTypeDef = TypedDict(
    "DescribeFHIRExportJobRequestRequestTypeDef",
    {
        "DatastoreId": str,
        "JobId": str,
    },
)

DescribeFHIRImportJobRequestRequestTypeDef = TypedDict(
    "DescribeFHIRImportJobRequestRequestTypeDef",
    {
        "DatastoreId": str,
        "JobId": str,
    },
)

InputDataConfigTypeDef = TypedDict(
    "InputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
    total=False,
)

_RequiredKmsEncryptionConfigTypeDef = TypedDict(
    "_RequiredKmsEncryptionConfigTypeDef",
    {
        "CmkType": CmkTypeType,
    },
)
_OptionalKmsEncryptionConfigTypeDef = TypedDict(
    "_OptionalKmsEncryptionConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class KmsEncryptionConfigTypeDef(
    _RequiredKmsEncryptionConfigTypeDef, _OptionalKmsEncryptionConfigTypeDef
):
    pass


_RequiredListFHIRExportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListFHIRExportJobsRequestRequestTypeDef",
    {
        "DatastoreId": str,
    },
)
_OptionalListFHIRExportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListFHIRExportJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmittedBefore": Union[datetime, str],
        "SubmittedAfter": Union[datetime, str],
    },
    total=False,
)


class ListFHIRExportJobsRequestRequestTypeDef(
    _RequiredListFHIRExportJobsRequestRequestTypeDef,
    _OptionalListFHIRExportJobsRequestRequestTypeDef,
):
    pass


_RequiredListFHIRImportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListFHIRImportJobsRequestRequestTypeDef",
    {
        "DatastoreId": str,
    },
)
_OptionalListFHIRImportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListFHIRImportJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmittedBefore": Union[datetime, str],
        "SubmittedAfter": Union[datetime, str],
    },
    total=False,
)


class ListFHIRImportJobsRequestRequestTypeDef(
    _RequiredListFHIRImportJobsRequestRequestTypeDef,
    _OptionalListFHIRImportJobsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

S3ConfigurationTypeDef = TypedDict(
    "S3ConfigurationTypeDef",
    {
        "S3Uri": str,
        "KmsKeyId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateFHIRDatastoreResponseTypeDef = TypedDict(
    "CreateFHIRDatastoreResponseTypeDef",
    {
        "DatastoreId": str,
        "DatastoreArn": str,
        "DatastoreStatus": DatastoreStatusType,
        "DatastoreEndpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFHIRDatastoreResponseTypeDef = TypedDict(
    "DeleteFHIRDatastoreResponseTypeDef",
    {
        "DatastoreId": str,
        "DatastoreArn": str,
        "DatastoreStatus": DatastoreStatusType,
        "DatastoreEndpoint": str,
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

StartFHIRExportJobResponseTypeDef = TypedDict(
    "StartFHIRExportJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "DatastoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFHIRImportJobResponseTypeDef = TypedDict(
    "StartFHIRImportJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "DatastoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFHIRDatastoresRequestRequestTypeDef = TypedDict(
    "ListFHIRDatastoresRequestRequestTypeDef",
    {
        "Filter": DatastoreFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SseConfigurationTypeDef = TypedDict(
    "SseConfigurationTypeDef",
    {
        "KmsEncryptionConfig": KmsEncryptionConfigTypeDef,
    },
)

OutputDataConfigTypeDef = TypedDict(
    "OutputDataConfigTypeDef",
    {
        "S3Configuration": S3ConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateFHIRDatastoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFHIRDatastoreRequestRequestTypeDef",
    {
        "DatastoreTypeVersion": Literal["R4"],
    },
)
_OptionalCreateFHIRDatastoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFHIRDatastoreRequestRequestTypeDef",
    {
        "DatastoreName": str,
        "SseConfiguration": SseConfigurationTypeDef,
        "PreloadDataConfig": PreloadDataConfigTypeDef,
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFHIRDatastoreRequestRequestTypeDef(
    _RequiredCreateFHIRDatastoreRequestRequestTypeDef,
    _OptionalCreateFHIRDatastoreRequestRequestTypeDef,
):
    pass


_RequiredDatastorePropertiesTypeDef = TypedDict(
    "_RequiredDatastorePropertiesTypeDef",
    {
        "DatastoreId": str,
        "DatastoreArn": str,
        "DatastoreStatus": DatastoreStatusType,
        "DatastoreTypeVersion": Literal["R4"],
        "DatastoreEndpoint": str,
    },
)
_OptionalDatastorePropertiesTypeDef = TypedDict(
    "_OptionalDatastorePropertiesTypeDef",
    {
        "DatastoreName": str,
        "CreatedAt": datetime,
        "SseConfiguration": SseConfigurationTypeDef,
        "PreloadDataConfig": PreloadDataConfigTypeDef,
    },
    total=False,
)


class DatastorePropertiesTypeDef(
    _RequiredDatastorePropertiesTypeDef, _OptionalDatastorePropertiesTypeDef
):
    pass


_RequiredExportJobPropertiesTypeDef = TypedDict(
    "_RequiredExportJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "SubmitTime": datetime,
        "DatastoreId": str,
        "OutputDataConfig": OutputDataConfigTypeDef,
    },
)
_OptionalExportJobPropertiesTypeDef = TypedDict(
    "_OptionalExportJobPropertiesTypeDef",
    {
        "JobName": str,
        "EndTime": datetime,
        "DataAccessRoleArn": str,
        "Message": str,
    },
    total=False,
)


class ExportJobPropertiesTypeDef(
    _RequiredExportJobPropertiesTypeDef, _OptionalExportJobPropertiesTypeDef
):
    pass


_RequiredImportJobPropertiesTypeDef = TypedDict(
    "_RequiredImportJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "SubmitTime": datetime,
        "DatastoreId": str,
        "InputDataConfig": InputDataConfigTypeDef,
    },
)
_OptionalImportJobPropertiesTypeDef = TypedDict(
    "_OptionalImportJobPropertiesTypeDef",
    {
        "JobName": str,
        "EndTime": datetime,
        "JobOutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "Message": str,
    },
    total=False,
)


class ImportJobPropertiesTypeDef(
    _RequiredImportJobPropertiesTypeDef, _OptionalImportJobPropertiesTypeDef
):
    pass


_RequiredStartFHIRExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartFHIRExportJobRequestRequestTypeDef",
    {
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DatastoreId": str,
        "DataAccessRoleArn": str,
        "ClientToken": str,
    },
)
_OptionalStartFHIRExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartFHIRExportJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
    total=False,
)


class StartFHIRExportJobRequestRequestTypeDef(
    _RequiredStartFHIRExportJobRequestRequestTypeDef,
    _OptionalStartFHIRExportJobRequestRequestTypeDef,
):
    pass


_RequiredStartFHIRImportJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartFHIRImportJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "JobOutputDataConfig": OutputDataConfigTypeDef,
        "DatastoreId": str,
        "DataAccessRoleArn": str,
        "ClientToken": str,
    },
)
_OptionalStartFHIRImportJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartFHIRImportJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
    total=False,
)


class StartFHIRImportJobRequestRequestTypeDef(
    _RequiredStartFHIRImportJobRequestRequestTypeDef,
    _OptionalStartFHIRImportJobRequestRequestTypeDef,
):
    pass


DescribeFHIRDatastoreResponseTypeDef = TypedDict(
    "DescribeFHIRDatastoreResponseTypeDef",
    {
        "DatastoreProperties": DatastorePropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFHIRDatastoresResponseTypeDef = TypedDict(
    "ListFHIRDatastoresResponseTypeDef",
    {
        "DatastorePropertiesList": List[DatastorePropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFHIRExportJobResponseTypeDef = TypedDict(
    "DescribeFHIRExportJobResponseTypeDef",
    {
        "ExportJobProperties": ExportJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFHIRExportJobsResponseTypeDef = TypedDict(
    "ListFHIRExportJobsResponseTypeDef",
    {
        "ExportJobPropertiesList": List[ExportJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFHIRImportJobResponseTypeDef = TypedDict(
    "DescribeFHIRImportJobResponseTypeDef",
    {
        "ImportJobProperties": ImportJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFHIRImportJobsResponseTypeDef = TypedDict(
    "ListFHIRImportJobsResponseTypeDef",
    {
        "ImportJobPropertiesList": List[ImportJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
