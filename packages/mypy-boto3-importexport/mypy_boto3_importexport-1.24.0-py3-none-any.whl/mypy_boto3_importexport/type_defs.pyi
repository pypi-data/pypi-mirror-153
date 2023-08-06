"""
Type annotations for importexport service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/type_defs/)

Usage::

    ```python
    from mypy_boto3_importexport.type_defs import ArtifactTypeDef

    data: ArtifactTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import JobTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ArtifactTypeDef",
    "CancelJobInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateJobInputRequestTypeDef",
    "GetShippingLabelInputRequestTypeDef",
    "GetStatusInputRequestTypeDef",
    "JobTypeDef",
    "PaginatorConfigTypeDef",
    "ListJobsInputRequestTypeDef",
    "UpdateJobInputRequestTypeDef",
    "CancelJobOutputTypeDef",
    "CreateJobOutputTypeDef",
    "GetShippingLabelOutputTypeDef",
    "GetStatusOutputTypeDef",
    "UpdateJobOutputTypeDef",
    "ListJobsOutputTypeDef",
    "ListJobsInputListJobsPaginateTypeDef",
)

ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {
        "Description": str,
        "URL": str,
    },
    total=False,
)

_RequiredCancelJobInputRequestTypeDef = TypedDict(
    "_RequiredCancelJobInputRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalCancelJobInputRequestTypeDef = TypedDict(
    "_OptionalCancelJobInputRequestTypeDef",
    {
        "APIVersion": str,
    },
    total=False,
)

class CancelJobInputRequestTypeDef(
    _RequiredCancelJobInputRequestTypeDef, _OptionalCancelJobInputRequestTypeDef
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

_RequiredCreateJobInputRequestTypeDef = TypedDict(
    "_RequiredCreateJobInputRequestTypeDef",
    {
        "JobType": JobTypeType,
        "Manifest": str,
        "ValidateOnly": bool,
    },
)
_OptionalCreateJobInputRequestTypeDef = TypedDict(
    "_OptionalCreateJobInputRequestTypeDef",
    {
        "ManifestAddendum": str,
        "APIVersion": str,
    },
    total=False,
)

class CreateJobInputRequestTypeDef(
    _RequiredCreateJobInputRequestTypeDef, _OptionalCreateJobInputRequestTypeDef
):
    pass

_RequiredGetShippingLabelInputRequestTypeDef = TypedDict(
    "_RequiredGetShippingLabelInputRequestTypeDef",
    {
        "jobIds": Sequence[str],
    },
)
_OptionalGetShippingLabelInputRequestTypeDef = TypedDict(
    "_OptionalGetShippingLabelInputRequestTypeDef",
    {
        "name": str,
        "company": str,
        "phoneNumber": str,
        "country": str,
        "stateOrProvince": str,
        "city": str,
        "postalCode": str,
        "street1": str,
        "street2": str,
        "street3": str,
        "APIVersion": str,
    },
    total=False,
)

class GetShippingLabelInputRequestTypeDef(
    _RequiredGetShippingLabelInputRequestTypeDef, _OptionalGetShippingLabelInputRequestTypeDef
):
    pass

_RequiredGetStatusInputRequestTypeDef = TypedDict(
    "_RequiredGetStatusInputRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetStatusInputRequestTypeDef = TypedDict(
    "_OptionalGetStatusInputRequestTypeDef",
    {
        "APIVersion": str,
    },
    total=False,
)

class GetStatusInputRequestTypeDef(
    _RequiredGetStatusInputRequestTypeDef, _OptionalGetStatusInputRequestTypeDef
):
    pass

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "JobId": str,
        "CreationDate": datetime,
        "IsCanceled": bool,
        "JobType": JobTypeType,
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

ListJobsInputRequestTypeDef = TypedDict(
    "ListJobsInputRequestTypeDef",
    {
        "MaxJobs": int,
        "Marker": str,
        "APIVersion": str,
    },
    total=False,
)

_RequiredUpdateJobInputRequestTypeDef = TypedDict(
    "_RequiredUpdateJobInputRequestTypeDef",
    {
        "JobId": str,
        "Manifest": str,
        "JobType": JobTypeType,
        "ValidateOnly": bool,
    },
)
_OptionalUpdateJobInputRequestTypeDef = TypedDict(
    "_OptionalUpdateJobInputRequestTypeDef",
    {
        "APIVersion": str,
    },
    total=False,
)

class UpdateJobInputRequestTypeDef(
    _RequiredUpdateJobInputRequestTypeDef, _OptionalUpdateJobInputRequestTypeDef
):
    pass

CancelJobOutputTypeDef = TypedDict(
    "CancelJobOutputTypeDef",
    {
        "Success": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobOutputTypeDef = TypedDict(
    "CreateJobOutputTypeDef",
    {
        "JobId": str,
        "JobType": JobTypeType,
        "Signature": str,
        "SignatureFileContents": str,
        "WarningMessage": str,
        "ArtifactList": List[ArtifactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetShippingLabelOutputTypeDef = TypedDict(
    "GetShippingLabelOutputTypeDef",
    {
        "ShippingLabelURL": str,
        "Warning": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStatusOutputTypeDef = TypedDict(
    "GetStatusOutputTypeDef",
    {
        "JobId": str,
        "JobType": JobTypeType,
        "LocationCode": str,
        "LocationMessage": str,
        "ProgressCode": str,
        "ProgressMessage": str,
        "Carrier": str,
        "TrackingNumber": str,
        "LogBucket": str,
        "LogKey": str,
        "ErrorCount": int,
        "Signature": str,
        "SignatureFileContents": str,
        "CurrentManifest": str,
        "CreationDate": datetime,
        "ArtifactList": List[ArtifactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobOutputTypeDef = TypedDict(
    "UpdateJobOutputTypeDef",
    {
        "Success": bool,
        "WarningMessage": str,
        "ArtifactList": List[ArtifactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsOutputTypeDef = TypedDict(
    "ListJobsOutputTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "IsTruncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsInputListJobsPaginateTypeDef = TypedDict(
    "ListJobsInputListJobsPaginateTypeDef",
    {
        "APIVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)
