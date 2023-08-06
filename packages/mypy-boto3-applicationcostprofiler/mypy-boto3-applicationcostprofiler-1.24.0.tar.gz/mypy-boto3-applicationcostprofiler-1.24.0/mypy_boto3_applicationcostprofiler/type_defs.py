"""
Type annotations for applicationcostprofiler service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/type_defs/)

Usage::

    ```python
    from mypy_boto3_applicationcostprofiler.type_defs import DeleteReportDefinitionRequestRequestTypeDef

    data: DeleteReportDefinitionRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import FormatType, ReportFrequencyType, S3BucketRegionType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DeleteReportDefinitionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetReportDefinitionRequestRequestTypeDef",
    "S3LocationTypeDef",
    "SourceS3LocationTypeDef",
    "PaginatorConfigTypeDef",
    "ListReportDefinitionsRequestRequestTypeDef",
    "DeleteReportDefinitionResultTypeDef",
    "ImportApplicationUsageResultTypeDef",
    "PutReportDefinitionResultTypeDef",
    "UpdateReportDefinitionResultTypeDef",
    "GetReportDefinitionResultTypeDef",
    "PutReportDefinitionRequestRequestTypeDef",
    "ReportDefinitionTypeDef",
    "UpdateReportDefinitionRequestRequestTypeDef",
    "ImportApplicationUsageRequestRequestTypeDef",
    "ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef",
    "ListReportDefinitionsResultTypeDef",
)

DeleteReportDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteReportDefinitionRequestRequestTypeDef",
    {
        "reportId": str,
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

GetReportDefinitionRequestRequestTypeDef = TypedDict(
    "GetReportDefinitionRequestRequestTypeDef",
    {
        "reportId": str,
    },
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucket": str,
        "prefix": str,
    },
)

_RequiredSourceS3LocationTypeDef = TypedDict(
    "_RequiredSourceS3LocationTypeDef",
    {
        "bucket": str,
        "key": str,
    },
)
_OptionalSourceS3LocationTypeDef = TypedDict(
    "_OptionalSourceS3LocationTypeDef",
    {
        "region": S3BucketRegionType,
    },
    total=False,
)


class SourceS3LocationTypeDef(_RequiredSourceS3LocationTypeDef, _OptionalSourceS3LocationTypeDef):
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

ListReportDefinitionsRequestRequestTypeDef = TypedDict(
    "ListReportDefinitionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

DeleteReportDefinitionResultTypeDef = TypedDict(
    "DeleteReportDefinitionResultTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportApplicationUsageResultTypeDef = TypedDict(
    "ImportApplicationUsageResultTypeDef",
    {
        "importId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutReportDefinitionResultTypeDef = TypedDict(
    "PutReportDefinitionResultTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateReportDefinitionResultTypeDef = TypedDict(
    "UpdateReportDefinitionResultTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReportDefinitionResultTypeDef = TypedDict(
    "GetReportDefinitionResultTypeDef",
    {
        "reportId": str,
        "reportDescription": str,
        "reportFrequency": ReportFrequencyType,
        "format": FormatType,
        "destinationS3Location": S3LocationTypeDef,
        "createdAt": datetime,
        "lastUpdated": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutReportDefinitionRequestRequestTypeDef = TypedDict(
    "PutReportDefinitionRequestRequestTypeDef",
    {
        "reportId": str,
        "reportDescription": str,
        "reportFrequency": ReportFrequencyType,
        "format": FormatType,
        "destinationS3Location": S3LocationTypeDef,
    },
)

ReportDefinitionTypeDef = TypedDict(
    "ReportDefinitionTypeDef",
    {
        "reportId": str,
        "reportDescription": str,
        "reportFrequency": ReportFrequencyType,
        "format": FormatType,
        "destinationS3Location": S3LocationTypeDef,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

UpdateReportDefinitionRequestRequestTypeDef = TypedDict(
    "UpdateReportDefinitionRequestRequestTypeDef",
    {
        "reportId": str,
        "reportDescription": str,
        "reportFrequency": ReportFrequencyType,
        "format": FormatType,
        "destinationS3Location": S3LocationTypeDef,
    },
)

ImportApplicationUsageRequestRequestTypeDef = TypedDict(
    "ImportApplicationUsageRequestRequestTypeDef",
    {
        "sourceS3Location": SourceS3LocationTypeDef,
    },
)

ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef = TypedDict(
    "ListReportDefinitionsRequestListReportDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListReportDefinitionsResultTypeDef = TypedDict(
    "ListReportDefinitionsResultTypeDef",
    {
        "reportDefinitions": List[ReportDefinitionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
