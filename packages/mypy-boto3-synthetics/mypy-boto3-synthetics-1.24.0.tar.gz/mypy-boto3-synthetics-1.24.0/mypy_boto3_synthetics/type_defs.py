"""
Type annotations for synthetics service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_synthetics/type_defs/)

Usage::

    ```python
    from mypy_boto3_synthetics.type_defs import S3EncryptionConfigTypeDef

    data: S3EncryptionConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CanaryRunStateReasonCodeType,
    CanaryRunStateType,
    CanaryStateReasonCodeType,
    CanaryStateType,
    EncryptionModeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "S3EncryptionConfigTypeDef",
    "BaseScreenshotTypeDef",
    "CanaryCodeInputTypeDef",
    "CanaryCodeOutputTypeDef",
    "CanaryRunConfigInputTypeDef",
    "CanaryRunConfigOutputTypeDef",
    "CanaryRunStatusTypeDef",
    "CanaryRunTimelineTypeDef",
    "CanaryScheduleInputTypeDef",
    "CanaryScheduleOutputTypeDef",
    "CanaryStatusTypeDef",
    "CanaryTimelineTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigInputTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteCanaryRequestRequestTypeDef",
    "DescribeCanariesLastRunRequestRequestTypeDef",
    "DescribeCanariesRequestRequestTypeDef",
    "DescribeRuntimeVersionsRequestRequestTypeDef",
    "RuntimeVersionTypeDef",
    "GetCanaryRequestRequestTypeDef",
    "GetCanaryRunsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StartCanaryRequestRequestTypeDef",
    "StopCanaryRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ArtifactConfigInputTypeDef",
    "ArtifactConfigOutputTypeDef",
    "VisualReferenceInputTypeDef",
    "VisualReferenceOutputTypeDef",
    "CanaryRunTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "DescribeRuntimeVersionsResponseTypeDef",
    "CreateCanaryRequestRequestTypeDef",
    "UpdateCanaryRequestRequestTypeDef",
    "CanaryTypeDef",
    "CanaryLastRunTypeDef",
    "GetCanaryRunsResponseTypeDef",
    "CreateCanaryResponseTypeDef",
    "DescribeCanariesResponseTypeDef",
    "GetCanaryResponseTypeDef",
    "DescribeCanariesLastRunResponseTypeDef",
)

S3EncryptionConfigTypeDef = TypedDict(
    "S3EncryptionConfigTypeDef",
    {
        "EncryptionMode": EncryptionModeType,
        "KmsKeyArn": str,
    },
    total=False,
)

_RequiredBaseScreenshotTypeDef = TypedDict(
    "_RequiredBaseScreenshotTypeDef",
    {
        "ScreenshotName": str,
    },
)
_OptionalBaseScreenshotTypeDef = TypedDict(
    "_OptionalBaseScreenshotTypeDef",
    {
        "IgnoreCoordinates": List[str],
    },
    total=False,
)


class BaseScreenshotTypeDef(_RequiredBaseScreenshotTypeDef, _OptionalBaseScreenshotTypeDef):
    pass


_RequiredCanaryCodeInputTypeDef = TypedDict(
    "_RequiredCanaryCodeInputTypeDef",
    {
        "Handler": str,
    },
)
_OptionalCanaryCodeInputTypeDef = TypedDict(
    "_OptionalCanaryCodeInputTypeDef",
    {
        "S3Bucket": str,
        "S3Key": str,
        "S3Version": str,
        "ZipFile": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class CanaryCodeInputTypeDef(_RequiredCanaryCodeInputTypeDef, _OptionalCanaryCodeInputTypeDef):
    pass


CanaryCodeOutputTypeDef = TypedDict(
    "CanaryCodeOutputTypeDef",
    {
        "SourceLocationArn": str,
        "Handler": str,
    },
    total=False,
)

CanaryRunConfigInputTypeDef = TypedDict(
    "CanaryRunConfigInputTypeDef",
    {
        "TimeoutInSeconds": int,
        "MemoryInMB": int,
        "ActiveTracing": bool,
        "EnvironmentVariables": Mapping[str, str],
    },
    total=False,
)

CanaryRunConfigOutputTypeDef = TypedDict(
    "CanaryRunConfigOutputTypeDef",
    {
        "TimeoutInSeconds": int,
        "MemoryInMB": int,
        "ActiveTracing": bool,
    },
    total=False,
)

CanaryRunStatusTypeDef = TypedDict(
    "CanaryRunStatusTypeDef",
    {
        "State": CanaryRunStateType,
        "StateReason": str,
        "StateReasonCode": CanaryRunStateReasonCodeType,
    },
    total=False,
)

CanaryRunTimelineTypeDef = TypedDict(
    "CanaryRunTimelineTypeDef",
    {
        "Started": datetime,
        "Completed": datetime,
    },
    total=False,
)

_RequiredCanaryScheduleInputTypeDef = TypedDict(
    "_RequiredCanaryScheduleInputTypeDef",
    {
        "Expression": str,
    },
)
_OptionalCanaryScheduleInputTypeDef = TypedDict(
    "_OptionalCanaryScheduleInputTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)


class CanaryScheduleInputTypeDef(
    _RequiredCanaryScheduleInputTypeDef, _OptionalCanaryScheduleInputTypeDef
):
    pass


CanaryScheduleOutputTypeDef = TypedDict(
    "CanaryScheduleOutputTypeDef",
    {
        "Expression": str,
        "DurationInSeconds": int,
    },
    total=False,
)

CanaryStatusTypeDef = TypedDict(
    "CanaryStatusTypeDef",
    {
        "State": CanaryStateType,
        "StateReason": str,
        "StateReasonCode": CanaryStateReasonCodeType,
    },
    total=False,
)

CanaryTimelineTypeDef = TypedDict(
    "CanaryTimelineTypeDef",
    {
        "Created": datetime,
        "LastModified": datetime,
        "LastStarted": datetime,
        "LastStopped": datetime,
    },
    total=False,
)

VpcConfigOutputTypeDef = TypedDict(
    "VpcConfigOutputTypeDef",
    {
        "VpcId": str,
        "SubnetIds": List[str],
        "SecurityGroupIds": List[str],
    },
    total=False,
)

VpcConfigInputTypeDef = TypedDict(
    "VpcConfigInputTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
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

_RequiredDeleteCanaryRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCanaryRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDeleteCanaryRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCanaryRequestRequestTypeDef",
    {
        "DeleteLambda": bool,
    },
    total=False,
)


class DeleteCanaryRequestRequestTypeDef(
    _RequiredDeleteCanaryRequestRequestTypeDef, _OptionalDeleteCanaryRequestRequestTypeDef
):
    pass


DescribeCanariesLastRunRequestRequestTypeDef = TypedDict(
    "DescribeCanariesLastRunRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Names": Sequence[str],
    },
    total=False,
)

DescribeCanariesRequestRequestTypeDef = TypedDict(
    "DescribeCanariesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Names": Sequence[str],
    },
    total=False,
)

DescribeRuntimeVersionsRequestRequestTypeDef = TypedDict(
    "DescribeRuntimeVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

RuntimeVersionTypeDef = TypedDict(
    "RuntimeVersionTypeDef",
    {
        "VersionName": str,
        "Description": str,
        "ReleaseDate": datetime,
        "DeprecationDate": datetime,
    },
    total=False,
)

GetCanaryRequestRequestTypeDef = TypedDict(
    "GetCanaryRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredGetCanaryRunsRequestRequestTypeDef = TypedDict(
    "_RequiredGetCanaryRunsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetCanaryRunsRequestRequestTypeDef = TypedDict(
    "_OptionalGetCanaryRunsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetCanaryRunsRequestRequestTypeDef(
    _RequiredGetCanaryRunsRequestRequestTypeDef, _OptionalGetCanaryRunsRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

StartCanaryRequestRequestTypeDef = TypedDict(
    "StartCanaryRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopCanaryRequestRequestTypeDef = TypedDict(
    "StopCanaryRequestRequestTypeDef",
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

ArtifactConfigInputTypeDef = TypedDict(
    "ArtifactConfigInputTypeDef",
    {
        "S3Encryption": S3EncryptionConfigTypeDef,
    },
    total=False,
)

ArtifactConfigOutputTypeDef = TypedDict(
    "ArtifactConfigOutputTypeDef",
    {
        "S3Encryption": S3EncryptionConfigTypeDef,
    },
    total=False,
)

_RequiredVisualReferenceInputTypeDef = TypedDict(
    "_RequiredVisualReferenceInputTypeDef",
    {
        "BaseCanaryRunId": str,
    },
)
_OptionalVisualReferenceInputTypeDef = TypedDict(
    "_OptionalVisualReferenceInputTypeDef",
    {
        "BaseScreenshots": Sequence[BaseScreenshotTypeDef],
    },
    total=False,
)


class VisualReferenceInputTypeDef(
    _RequiredVisualReferenceInputTypeDef, _OptionalVisualReferenceInputTypeDef
):
    pass


VisualReferenceOutputTypeDef = TypedDict(
    "VisualReferenceOutputTypeDef",
    {
        "BaseScreenshots": List[BaseScreenshotTypeDef],
        "BaseCanaryRunId": str,
    },
    total=False,
)

CanaryRunTypeDef = TypedDict(
    "CanaryRunTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": CanaryRunStatusTypeDef,
        "Timeline": CanaryRunTimelineTypeDef,
        "ArtifactS3Location": str,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRuntimeVersionsResponseTypeDef = TypedDict(
    "DescribeRuntimeVersionsResponseTypeDef",
    {
        "RuntimeVersions": List[RuntimeVersionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateCanaryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCanaryRequestRequestTypeDef",
    {
        "Name": str,
        "Code": CanaryCodeInputTypeDef,
        "ArtifactS3Location": str,
        "ExecutionRoleArn": str,
        "Schedule": CanaryScheduleInputTypeDef,
        "RuntimeVersion": str,
    },
)
_OptionalCreateCanaryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCanaryRequestRequestTypeDef",
    {
        "RunConfig": CanaryRunConfigInputTypeDef,
        "SuccessRetentionPeriodInDays": int,
        "FailureRetentionPeriodInDays": int,
        "VpcConfig": VpcConfigInputTypeDef,
        "Tags": Mapping[str, str],
        "ArtifactConfig": ArtifactConfigInputTypeDef,
    },
    total=False,
)


class CreateCanaryRequestRequestTypeDef(
    _RequiredCreateCanaryRequestRequestTypeDef, _OptionalCreateCanaryRequestRequestTypeDef
):
    pass


_RequiredUpdateCanaryRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCanaryRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateCanaryRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCanaryRequestRequestTypeDef",
    {
        "Code": CanaryCodeInputTypeDef,
        "ExecutionRoleArn": str,
        "RuntimeVersion": str,
        "Schedule": CanaryScheduleInputTypeDef,
        "RunConfig": CanaryRunConfigInputTypeDef,
        "SuccessRetentionPeriodInDays": int,
        "FailureRetentionPeriodInDays": int,
        "VpcConfig": VpcConfigInputTypeDef,
        "VisualReference": VisualReferenceInputTypeDef,
        "ArtifactS3Location": str,
        "ArtifactConfig": ArtifactConfigInputTypeDef,
    },
    total=False,
)


class UpdateCanaryRequestRequestTypeDef(
    _RequiredUpdateCanaryRequestRequestTypeDef, _OptionalUpdateCanaryRequestRequestTypeDef
):
    pass


CanaryTypeDef = TypedDict(
    "CanaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Code": CanaryCodeOutputTypeDef,
        "ExecutionRoleArn": str,
        "Schedule": CanaryScheduleOutputTypeDef,
        "RunConfig": CanaryRunConfigOutputTypeDef,
        "SuccessRetentionPeriodInDays": int,
        "FailureRetentionPeriodInDays": int,
        "Status": CanaryStatusTypeDef,
        "Timeline": CanaryTimelineTypeDef,
        "ArtifactS3Location": str,
        "EngineArn": str,
        "RuntimeVersion": str,
        "VpcConfig": VpcConfigOutputTypeDef,
        "VisualReference": VisualReferenceOutputTypeDef,
        "Tags": Dict[str, str],
        "ArtifactConfig": ArtifactConfigOutputTypeDef,
    },
    total=False,
)

CanaryLastRunTypeDef = TypedDict(
    "CanaryLastRunTypeDef",
    {
        "CanaryName": str,
        "LastRun": CanaryRunTypeDef,
    },
    total=False,
)

GetCanaryRunsResponseTypeDef = TypedDict(
    "GetCanaryRunsResponseTypeDef",
    {
        "CanaryRuns": List[CanaryRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCanaryResponseTypeDef = TypedDict(
    "CreateCanaryResponseTypeDef",
    {
        "Canary": CanaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCanariesResponseTypeDef = TypedDict(
    "DescribeCanariesResponseTypeDef",
    {
        "Canaries": List[CanaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCanaryResponseTypeDef = TypedDict(
    "GetCanaryResponseTypeDef",
    {
        "Canary": CanaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCanariesLastRunResponseTypeDef = TypedDict(
    "DescribeCanariesLastRunResponseTypeDef",
    {
        "CanariesLastRun": List[CanaryLastRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
