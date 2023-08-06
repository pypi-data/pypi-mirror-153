"""
Type annotations for iot-jobs-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_jobs_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_iot_jobs_data.type_defs import DescribeJobExecutionRequestRequestTypeDef

    data: DescribeJobExecutionRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping

from .literals import JobExecutionStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DescribeJobExecutionRequestRequestTypeDef",
    "JobExecutionTypeDef",
    "ResponseMetadataTypeDef",
    "GetPendingJobExecutionsRequestRequestTypeDef",
    "JobExecutionSummaryTypeDef",
    "JobExecutionStateTypeDef",
    "StartNextPendingJobExecutionRequestRequestTypeDef",
    "UpdateJobExecutionRequestRequestTypeDef",
    "DescribeJobExecutionResponseTypeDef",
    "StartNextPendingJobExecutionResponseTypeDef",
    "GetPendingJobExecutionsResponseTypeDef",
    "UpdateJobExecutionResponseTypeDef",
)

_RequiredDescribeJobExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeJobExecutionRequestRequestTypeDef",
    {
        "jobId": str,
        "thingName": str,
    },
)
_OptionalDescribeJobExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeJobExecutionRequestRequestTypeDef",
    {
        "includeJobDocument": bool,
        "executionNumber": int,
    },
    total=False,
)


class DescribeJobExecutionRequestRequestTypeDef(
    _RequiredDescribeJobExecutionRequestRequestTypeDef,
    _OptionalDescribeJobExecutionRequestRequestTypeDef,
):
    pass


JobExecutionTypeDef = TypedDict(
    "JobExecutionTypeDef",
    {
        "jobId": str,
        "thingName": str,
        "status": JobExecutionStatusType,
        "statusDetails": Dict[str, str],
        "queuedAt": int,
        "startedAt": int,
        "lastUpdatedAt": int,
        "approximateSecondsBeforeTimedOut": int,
        "versionNumber": int,
        "executionNumber": int,
        "jobDocument": str,
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

GetPendingJobExecutionsRequestRequestTypeDef = TypedDict(
    "GetPendingJobExecutionsRequestRequestTypeDef",
    {
        "thingName": str,
    },
)

JobExecutionSummaryTypeDef = TypedDict(
    "JobExecutionSummaryTypeDef",
    {
        "jobId": str,
        "queuedAt": int,
        "startedAt": int,
        "lastUpdatedAt": int,
        "versionNumber": int,
        "executionNumber": int,
    },
    total=False,
)

JobExecutionStateTypeDef = TypedDict(
    "JobExecutionStateTypeDef",
    {
        "status": JobExecutionStatusType,
        "statusDetails": Dict[str, str],
        "versionNumber": int,
    },
    total=False,
)

_RequiredStartNextPendingJobExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStartNextPendingJobExecutionRequestRequestTypeDef",
    {
        "thingName": str,
    },
)
_OptionalStartNextPendingJobExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStartNextPendingJobExecutionRequestRequestTypeDef",
    {
        "statusDetails": Mapping[str, str],
        "stepTimeoutInMinutes": int,
    },
    total=False,
)


class StartNextPendingJobExecutionRequestRequestTypeDef(
    _RequiredStartNextPendingJobExecutionRequestRequestTypeDef,
    _OptionalStartNextPendingJobExecutionRequestRequestTypeDef,
):
    pass


_RequiredUpdateJobExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateJobExecutionRequestRequestTypeDef",
    {
        "jobId": str,
        "thingName": str,
        "status": JobExecutionStatusType,
    },
)
_OptionalUpdateJobExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateJobExecutionRequestRequestTypeDef",
    {
        "statusDetails": Mapping[str, str],
        "stepTimeoutInMinutes": int,
        "expectedVersion": int,
        "includeJobExecutionState": bool,
        "includeJobDocument": bool,
        "executionNumber": int,
    },
    total=False,
)


class UpdateJobExecutionRequestRequestTypeDef(
    _RequiredUpdateJobExecutionRequestRequestTypeDef,
    _OptionalUpdateJobExecutionRequestRequestTypeDef,
):
    pass


DescribeJobExecutionResponseTypeDef = TypedDict(
    "DescribeJobExecutionResponseTypeDef",
    {
        "execution": JobExecutionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartNextPendingJobExecutionResponseTypeDef = TypedDict(
    "StartNextPendingJobExecutionResponseTypeDef",
    {
        "execution": JobExecutionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPendingJobExecutionsResponseTypeDef = TypedDict(
    "GetPendingJobExecutionsResponseTypeDef",
    {
        "inProgressJobs": List[JobExecutionSummaryTypeDef],
        "queuedJobs": List[JobExecutionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobExecutionResponseTypeDef = TypedDict(
    "UpdateJobExecutionResponseTypeDef",
    {
        "executionState": JobExecutionStateTypeDef,
        "jobDocument": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
