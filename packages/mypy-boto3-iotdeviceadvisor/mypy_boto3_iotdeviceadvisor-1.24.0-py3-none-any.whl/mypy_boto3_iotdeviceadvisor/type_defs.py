"""
Type annotations for iotdeviceadvisor service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotdeviceadvisor.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import StatusType, SuiteRunStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "DeleteSuiteDefinitionRequestRequestTypeDef",
    "DeviceUnderTestTypeDef",
    "GetEndpointRequestRequestTypeDef",
    "GetSuiteDefinitionRequestRequestTypeDef",
    "GetSuiteRunReportRequestRequestTypeDef",
    "GetSuiteRunRequestRequestTypeDef",
    "TestCaseRunTypeDef",
    "ListSuiteDefinitionsRequestRequestTypeDef",
    "ListSuiteRunsRequestRequestTypeDef",
    "SuiteRunInformationTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StopSuiteRunRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateSuiteDefinitionResponseTypeDef",
    "GetEndpointResponseTypeDef",
    "GetSuiteRunReportResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartSuiteRunResponseTypeDef",
    "UpdateSuiteDefinitionResponseTypeDef",
    "SuiteDefinitionConfigurationTypeDef",
    "SuiteDefinitionInformationTypeDef",
    "SuiteRunConfigurationTypeDef",
    "GroupResultTypeDef",
    "ListSuiteRunsResponseTypeDef",
    "CreateSuiteDefinitionRequestRequestTypeDef",
    "GetSuiteDefinitionResponseTypeDef",
    "UpdateSuiteDefinitionRequestRequestTypeDef",
    "ListSuiteDefinitionsResponseTypeDef",
    "StartSuiteRunRequestRequestTypeDef",
    "TestResultTypeDef",
    "GetSuiteRunResponseTypeDef",
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

DeleteSuiteDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteSuiteDefinitionRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
    },
)

DeviceUnderTestTypeDef = TypedDict(
    "DeviceUnderTestTypeDef",
    {
        "thingArn": str,
        "certificateArn": str,
    },
    total=False,
)

GetEndpointRequestRequestTypeDef = TypedDict(
    "GetEndpointRequestRequestTypeDef",
    {
        "thingArn": str,
        "certificateArn": str,
    },
    total=False,
)

_RequiredGetSuiteDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredGetSuiteDefinitionRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
    },
)
_OptionalGetSuiteDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalGetSuiteDefinitionRequestRequestTypeDef",
    {
        "suiteDefinitionVersion": str,
    },
    total=False,
)


class GetSuiteDefinitionRequestRequestTypeDef(
    _RequiredGetSuiteDefinitionRequestRequestTypeDef,
    _OptionalGetSuiteDefinitionRequestRequestTypeDef,
):
    pass


GetSuiteRunReportRequestRequestTypeDef = TypedDict(
    "GetSuiteRunReportRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteRunId": str,
    },
)

GetSuiteRunRequestRequestTypeDef = TypedDict(
    "GetSuiteRunRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteRunId": str,
    },
)

TestCaseRunTypeDef = TypedDict(
    "TestCaseRunTypeDef",
    {
        "testCaseRunId": str,
        "testCaseDefinitionId": str,
        "testCaseDefinitionName": str,
        "status": StatusType,
        "startTime": datetime,
        "endTime": datetime,
        "logUrl": str,
        "warnings": str,
        "failure": str,
    },
    total=False,
)

ListSuiteDefinitionsRequestRequestTypeDef = TypedDict(
    "ListSuiteDefinitionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSuiteRunsRequestRequestTypeDef = TypedDict(
    "ListSuiteRunsRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SuiteRunInformationTypeDef = TypedDict(
    "SuiteRunInformationTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionVersion": str,
        "suiteDefinitionName": str,
        "suiteRunId": str,
        "createdAt": datetime,
        "startedAt": datetime,
        "endAt": datetime,
        "status": SuiteRunStatusType,
        "passed": int,
        "failed": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

StopSuiteRunRequestRequestTypeDef = TypedDict(
    "StopSuiteRunRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteRunId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

CreateSuiteDefinitionResponseTypeDef = TypedDict(
    "CreateSuiteDefinitionResponseTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionArn": str,
        "suiteDefinitionName": str,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEndpointResponseTypeDef = TypedDict(
    "GetEndpointResponseTypeDef",
    {
        "endpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSuiteRunReportResponseTypeDef = TypedDict(
    "GetSuiteRunReportResponseTypeDef",
    {
        "qualificationReportDownloadUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSuiteRunResponseTypeDef = TypedDict(
    "StartSuiteRunResponseTypeDef",
    {
        "suiteRunId": str,
        "suiteRunArn": str,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSuiteDefinitionResponseTypeDef = TypedDict(
    "UpdateSuiteDefinitionResponseTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionArn": str,
        "suiteDefinitionName": str,
        "suiteDefinitionVersion": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SuiteDefinitionConfigurationTypeDef = TypedDict(
    "SuiteDefinitionConfigurationTypeDef",
    {
        "suiteDefinitionName": str,
        "devices": Sequence[DeviceUnderTestTypeDef],
        "intendedForQualification": bool,
        "rootGroup": str,
        "devicePermissionRoleArn": str,
    },
    total=False,
)

SuiteDefinitionInformationTypeDef = TypedDict(
    "SuiteDefinitionInformationTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionName": str,
        "defaultDevices": List[DeviceUnderTestTypeDef],
        "intendedForQualification": bool,
        "createdAt": datetime,
    },
    total=False,
)

SuiteRunConfigurationTypeDef = TypedDict(
    "SuiteRunConfigurationTypeDef",
    {
        "primaryDevice": DeviceUnderTestTypeDef,
        "selectedTestList": List[str],
        "parallelRun": bool,
    },
    total=False,
)

GroupResultTypeDef = TypedDict(
    "GroupResultTypeDef",
    {
        "groupId": str,
        "groupName": str,
        "tests": List[TestCaseRunTypeDef],
    },
    total=False,
)

ListSuiteRunsResponseTypeDef = TypedDict(
    "ListSuiteRunsResponseTypeDef",
    {
        "suiteRunsList": List[SuiteRunInformationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSuiteDefinitionRequestRequestTypeDef = TypedDict(
    "CreateSuiteDefinitionRequestRequestTypeDef",
    {
        "suiteDefinitionConfiguration": SuiteDefinitionConfigurationTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetSuiteDefinitionResponseTypeDef = TypedDict(
    "GetSuiteDefinitionResponseTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionArn": str,
        "suiteDefinitionVersion": str,
        "latestVersion": str,
        "suiteDefinitionConfiguration": SuiteDefinitionConfigurationTypeDef,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateSuiteDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSuiteDefinitionRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
    },
)
_OptionalUpdateSuiteDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSuiteDefinitionRequestRequestTypeDef",
    {
        "suiteDefinitionConfiguration": SuiteDefinitionConfigurationTypeDef,
    },
    total=False,
)


class UpdateSuiteDefinitionRequestRequestTypeDef(
    _RequiredUpdateSuiteDefinitionRequestRequestTypeDef,
    _OptionalUpdateSuiteDefinitionRequestRequestTypeDef,
):
    pass


ListSuiteDefinitionsResponseTypeDef = TypedDict(
    "ListSuiteDefinitionsResponseTypeDef",
    {
        "suiteDefinitionInformationList": List[SuiteDefinitionInformationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartSuiteRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartSuiteRunRequestRequestTypeDef",
    {
        "suiteDefinitionId": str,
    },
)
_OptionalStartSuiteRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartSuiteRunRequestRequestTypeDef",
    {
        "suiteDefinitionVersion": str,
        "suiteRunConfiguration": SuiteRunConfigurationTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartSuiteRunRequestRequestTypeDef(
    _RequiredStartSuiteRunRequestRequestTypeDef, _OptionalStartSuiteRunRequestRequestTypeDef
):
    pass


TestResultTypeDef = TypedDict(
    "TestResultTypeDef",
    {
        "groups": List[GroupResultTypeDef],
    },
    total=False,
)

GetSuiteRunResponseTypeDef = TypedDict(
    "GetSuiteRunResponseTypeDef",
    {
        "suiteDefinitionId": str,
        "suiteDefinitionVersion": str,
        "suiteRunId": str,
        "suiteRunArn": str,
        "suiteRunConfiguration": SuiteRunConfigurationTypeDef,
        "testResult": TestResultTypeDef,
        "startTime": datetime,
        "endTime": datetime,
        "status": SuiteRunStatusType,
        "errorReason": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
