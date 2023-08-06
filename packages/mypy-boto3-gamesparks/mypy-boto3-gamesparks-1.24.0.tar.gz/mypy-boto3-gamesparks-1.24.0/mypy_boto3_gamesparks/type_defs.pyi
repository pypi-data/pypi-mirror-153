"""
Type annotations for gamesparks service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/type_defs/)

Usage::

    ```python
    from mypy_boto3_gamesparks.type_defs import ConnectionTypeDef

    data: ConnectionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DeploymentActionType,
    DeploymentStateType,
    GameStateType,
    GeneratedCodeJobStateType,
    OperationType,
    ResultCodeType,
    StageStateType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ConnectionTypeDef",
    "CreateGameRequestRequestTypeDef",
    "GameDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateStageRequestRequestTypeDef",
    "StageDetailsTypeDef",
    "DeleteGameRequestRequestTypeDef",
    "DeleteStageRequestRequestTypeDef",
    "DeploymentResultTypeDef",
    "DisconnectPlayerRequestRequestTypeDef",
    "ExportSnapshotRequestRequestTypeDef",
    "ExtensionDetailsTypeDef",
    "ExtensionVersionDetailsTypeDef",
    "SectionTypeDef",
    "GameSummaryTypeDef",
    "GeneratedCodeJobDetailsTypeDef",
    "GeneratorTypeDef",
    "GetExtensionRequestRequestTypeDef",
    "GetExtensionVersionRequestRequestTypeDef",
    "GetGameConfigurationRequestRequestTypeDef",
    "GetGameRequestRequestTypeDef",
    "GetGeneratedCodeJobRequestRequestTypeDef",
    "GetPlayerConnectionStatusRequestRequestTypeDef",
    "GetSnapshotRequestRequestTypeDef",
    "GetStageDeploymentRequestRequestTypeDef",
    "GetStageRequestRequestTypeDef",
    "ImportGameConfigurationSourceTypeDef",
    "PaginatorConfigTypeDef",
    "ListExtensionVersionsRequestRequestTypeDef",
    "ListExtensionsRequestRequestTypeDef",
    "ListGamesRequestRequestTypeDef",
    "ListGeneratedCodeJobsRequestRequestTypeDef",
    "ListSnapshotsRequestRequestTypeDef",
    "SnapshotSummaryTypeDef",
    "ListStageDeploymentsRequestRequestTypeDef",
    "ListStagesRequestRequestTypeDef",
    "StageSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "SectionModificationTypeDef",
    "StartStageDeploymentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateGameRequestRequestTypeDef",
    "UpdateSnapshotRequestRequestTypeDef",
    "UpdateStageRequestRequestTypeDef",
    "CreateGameResultTypeDef",
    "DisconnectPlayerResultTypeDef",
    "ExportSnapshotResultTypeDef",
    "GetGameResultTypeDef",
    "GetPlayerConnectionStatusResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "StartGeneratedCodeJobResultTypeDef",
    "UpdateGameResultTypeDef",
    "CreateStageResultTypeDef",
    "GetStageResultTypeDef",
    "UpdateStageResultTypeDef",
    "StageDeploymentDetailsTypeDef",
    "StageDeploymentSummaryTypeDef",
    "GetExtensionResultTypeDef",
    "ListExtensionsResultTypeDef",
    "GetExtensionVersionResultTypeDef",
    "ListExtensionVersionsResultTypeDef",
    "GameConfigurationDetailsTypeDef",
    "SnapshotDetailsTypeDef",
    "ListGamesResultTypeDef",
    "GetGeneratedCodeJobResultTypeDef",
    "ListGeneratedCodeJobsResultTypeDef",
    "StartGeneratedCodeJobRequestRequestTypeDef",
    "ImportGameConfigurationRequestRequestTypeDef",
    "ListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef",
    "ListExtensionsRequestListExtensionsPaginateTypeDef",
    "ListGamesRequestListGamesPaginateTypeDef",
    "ListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef",
    "ListSnapshotsRequestListSnapshotsPaginateTypeDef",
    "ListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef",
    "ListStagesRequestListStagesPaginateTypeDef",
    "ListSnapshotsResultTypeDef",
    "ListStagesResultTypeDef",
    "UpdateGameConfigurationRequestRequestTypeDef",
    "GetStageDeploymentResultTypeDef",
    "StartStageDeploymentResultTypeDef",
    "ListStageDeploymentsResultTypeDef",
    "GetGameConfigurationResultTypeDef",
    "ImportGameConfigurationResultTypeDef",
    "UpdateGameConfigurationResultTypeDef",
    "CreateSnapshotResultTypeDef",
    "GetSnapshotResultTypeDef",
    "UpdateSnapshotResultTypeDef",
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "Created": datetime,
        "Id": str,
    },
    total=False,
)

_RequiredCreateGameRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGameRequestRequestTypeDef",
    {
        "GameName": str,
    },
)
_OptionalCreateGameRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGameRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateGameRequestRequestTypeDef(
    _RequiredCreateGameRequestRequestTypeDef, _OptionalCreateGameRequestRequestTypeDef
):
    pass

GameDetailsTypeDef = TypedDict(
    "GameDetailsTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Description": str,
        "EnableTerminationProtection": bool,
        "LastUpdated": datetime,
        "Name": str,
        "State": GameStateType,
        "Tags": Dict[str, str],
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

_RequiredCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
    },
)
_OptionalCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class CreateSnapshotRequestRequestTypeDef(
    _RequiredCreateSnapshotRequestRequestTypeDef, _OptionalCreateSnapshotRequestRequestTypeDef
):
    pass

_RequiredCreateStageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStageRequestRequestTypeDef",
    {
        "GameName": str,
        "Role": str,
        "StageName": str,
    },
)
_OptionalCreateStageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStageRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateStageRequestRequestTypeDef(
    _RequiredCreateStageRequestRequestTypeDef, _OptionalCreateStageRequestRequestTypeDef
):
    pass

StageDetailsTypeDef = TypedDict(
    "StageDetailsTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Description": str,
        "GameKey": str,
        "LastUpdated": datetime,
        "LogGroup": str,
        "Name": str,
        "Role": str,
        "State": StageStateType,
        "Tags": Dict[str, str],
    },
    total=False,
)

DeleteGameRequestRequestTypeDef = TypedDict(
    "DeleteGameRequestRequestTypeDef",
    {
        "GameName": str,
    },
)

DeleteStageRequestRequestTypeDef = TypedDict(
    "DeleteStageRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)

DeploymentResultTypeDef = TypedDict(
    "DeploymentResultTypeDef",
    {
        "Message": str,
        "ResultCode": ResultCodeType,
    },
    total=False,
)

DisconnectPlayerRequestRequestTypeDef = TypedDict(
    "DisconnectPlayerRequestRequestTypeDef",
    {
        "GameName": str,
        "PlayerId": str,
        "StageName": str,
    },
)

ExportSnapshotRequestRequestTypeDef = TypedDict(
    "ExportSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
    },
)

ExtensionDetailsTypeDef = TypedDict(
    "ExtensionDetailsTypeDef",
    {
        "Description": str,
        "Name": str,
        "Namespace": str,
    },
    total=False,
)

ExtensionVersionDetailsTypeDef = TypedDict(
    "ExtensionVersionDetailsTypeDef",
    {
        "Name": str,
        "Namespace": str,
        "Schema": str,
        "Version": str,
    },
    total=False,
)

SectionTypeDef = TypedDict(
    "SectionTypeDef",
    {
        "Attributes": Dict[str, Any],
        "Name": str,
        "Size": int,
    },
    total=False,
)

GameSummaryTypeDef = TypedDict(
    "GameSummaryTypeDef",
    {
        "Description": str,
        "Name": str,
        "State": GameStateType,
        "Tags": Dict[str, str],
    },
    total=False,
)

GeneratedCodeJobDetailsTypeDef = TypedDict(
    "GeneratedCodeJobDetailsTypeDef",
    {
        "Description": str,
        "ExpirationTime": datetime,
        "GeneratedCodeJobId": str,
        "S3Url": str,
        "Status": GeneratedCodeJobStateType,
    },
    total=False,
)

GeneratorTypeDef = TypedDict(
    "GeneratorTypeDef",
    {
        "GameSdkVersion": str,
        "Language": str,
        "TargetPlatform": str,
    },
    total=False,
)

GetExtensionRequestRequestTypeDef = TypedDict(
    "GetExtensionRequestRequestTypeDef",
    {
        "Name": str,
        "Namespace": str,
    },
)

GetExtensionVersionRequestRequestTypeDef = TypedDict(
    "GetExtensionVersionRequestRequestTypeDef",
    {
        "ExtensionVersion": str,
        "Name": str,
        "Namespace": str,
    },
)

_RequiredGetGameConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetGameConfigurationRequestRequestTypeDef",
    {
        "GameName": str,
    },
)
_OptionalGetGameConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetGameConfigurationRequestRequestTypeDef",
    {
        "Sections": Sequence[str],
    },
    total=False,
)

class GetGameConfigurationRequestRequestTypeDef(
    _RequiredGetGameConfigurationRequestRequestTypeDef,
    _OptionalGetGameConfigurationRequestRequestTypeDef,
):
    pass

GetGameRequestRequestTypeDef = TypedDict(
    "GetGameRequestRequestTypeDef",
    {
        "GameName": str,
    },
)

GetGeneratedCodeJobRequestRequestTypeDef = TypedDict(
    "GetGeneratedCodeJobRequestRequestTypeDef",
    {
        "GameName": str,
        "JobId": str,
        "SnapshotId": str,
    },
)

GetPlayerConnectionStatusRequestRequestTypeDef = TypedDict(
    "GetPlayerConnectionStatusRequestRequestTypeDef",
    {
        "GameName": str,
        "PlayerId": str,
        "StageName": str,
    },
)

_RequiredGetSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredGetSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
    },
)
_OptionalGetSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalGetSnapshotRequestRequestTypeDef",
    {
        "Sections": Sequence[str],
    },
    total=False,
)

class GetSnapshotRequestRequestTypeDef(
    _RequiredGetSnapshotRequestRequestTypeDef, _OptionalGetSnapshotRequestRequestTypeDef
):
    pass

_RequiredGetStageDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredGetStageDeploymentRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)
_OptionalGetStageDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalGetStageDeploymentRequestRequestTypeDef",
    {
        "DeploymentId": str,
    },
    total=False,
)

class GetStageDeploymentRequestRequestTypeDef(
    _RequiredGetStageDeploymentRequestRequestTypeDef,
    _OptionalGetStageDeploymentRequestRequestTypeDef,
):
    pass

GetStageRequestRequestTypeDef = TypedDict(
    "GetStageRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)

ImportGameConfigurationSourceTypeDef = TypedDict(
    "ImportGameConfigurationSourceTypeDef",
    {
        "File": Union[str, bytes, IO[Any], StreamingBody],
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

_RequiredListExtensionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListExtensionVersionsRequestRequestTypeDef",
    {
        "Name": str,
        "Namespace": str,
    },
)
_OptionalListExtensionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListExtensionVersionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListExtensionVersionsRequestRequestTypeDef(
    _RequiredListExtensionVersionsRequestRequestTypeDef,
    _OptionalListExtensionVersionsRequestRequestTypeDef,
):
    pass

ListExtensionsRequestRequestTypeDef = TypedDict(
    "ListExtensionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListGamesRequestRequestTypeDef = TypedDict(
    "ListGamesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListGeneratedCodeJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListGeneratedCodeJobsRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
    },
)
_OptionalListGeneratedCodeJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListGeneratedCodeJobsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListGeneratedCodeJobsRequestRequestTypeDef(
    _RequiredListGeneratedCodeJobsRequestRequestTypeDef,
    _OptionalListGeneratedCodeJobsRequestRequestTypeDef,
):
    pass

_RequiredListSnapshotsRequestRequestTypeDef = TypedDict(
    "_RequiredListSnapshotsRequestRequestTypeDef",
    {
        "GameName": str,
    },
)
_OptionalListSnapshotsRequestRequestTypeDef = TypedDict(
    "_OptionalListSnapshotsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListSnapshotsRequestRequestTypeDef(
    _RequiredListSnapshotsRequestRequestTypeDef, _OptionalListSnapshotsRequestRequestTypeDef
):
    pass

SnapshotSummaryTypeDef = TypedDict(
    "SnapshotSummaryTypeDef",
    {
        "Created": datetime,
        "Description": str,
        "Id": str,
        "LastUpdated": datetime,
    },
    total=False,
)

_RequiredListStageDeploymentsRequestRequestTypeDef = TypedDict(
    "_RequiredListStageDeploymentsRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)
_OptionalListStageDeploymentsRequestRequestTypeDef = TypedDict(
    "_OptionalListStageDeploymentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListStageDeploymentsRequestRequestTypeDef(
    _RequiredListStageDeploymentsRequestRequestTypeDef,
    _OptionalListStageDeploymentsRequestRequestTypeDef,
):
    pass

_RequiredListStagesRequestRequestTypeDef = TypedDict(
    "_RequiredListStagesRequestRequestTypeDef",
    {
        "GameName": str,
    },
)
_OptionalListStagesRequestRequestTypeDef = TypedDict(
    "_OptionalListStagesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListStagesRequestRequestTypeDef(
    _RequiredListStagesRequestRequestTypeDef, _OptionalListStagesRequestRequestTypeDef
):
    pass

StageSummaryTypeDef = TypedDict(
    "StageSummaryTypeDef",
    {
        "Description": str,
        "GameKey": str,
        "Name": str,
        "State": StageStateType,
        "Tags": Dict[str, str],
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredSectionModificationTypeDef = TypedDict(
    "_RequiredSectionModificationTypeDef",
    {
        "Operation": OperationType,
        "Path": str,
        "Section": str,
    },
)
_OptionalSectionModificationTypeDef = TypedDict(
    "_OptionalSectionModificationTypeDef",
    {
        "Value": Mapping[str, Any],
    },
    total=False,
)

class SectionModificationTypeDef(
    _RequiredSectionModificationTypeDef, _OptionalSectionModificationTypeDef
):
    pass

_RequiredStartStageDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredStartStageDeploymentRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
        "StageName": str,
    },
)
_OptionalStartStageDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalStartStageDeploymentRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class StartStageDeploymentRequestRequestTypeDef(
    _RequiredStartStageDeploymentRequestRequestTypeDef,
    _OptionalStartStageDeploymentRequestRequestTypeDef,
):
    pass

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateGameRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGameRequestRequestTypeDef",
    {
        "GameName": str,
    },
)
_OptionalUpdateGameRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGameRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateGameRequestRequestTypeDef(
    _RequiredUpdateGameRequestRequestTypeDef, _OptionalUpdateGameRequestRequestTypeDef
):
    pass

_RequiredUpdateSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
    },
)
_OptionalUpdateSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSnapshotRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateSnapshotRequestRequestTypeDef(
    _RequiredUpdateSnapshotRequestRequestTypeDef, _OptionalUpdateSnapshotRequestRequestTypeDef
):
    pass

_RequiredUpdateStageRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStageRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)
_OptionalUpdateStageRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStageRequestRequestTypeDef",
    {
        "Description": str,
        "Role": str,
    },
    total=False,
)

class UpdateStageRequestRequestTypeDef(
    _RequiredUpdateStageRequestRequestTypeDef, _OptionalUpdateStageRequestRequestTypeDef
):
    pass

CreateGameResultTypeDef = TypedDict(
    "CreateGameResultTypeDef",
    {
        "Game": GameDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisconnectPlayerResultTypeDef = TypedDict(
    "DisconnectPlayerResultTypeDef",
    {
        "DisconnectFailures": List[str],
        "DisconnectSuccesses": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportSnapshotResultTypeDef = TypedDict(
    "ExportSnapshotResultTypeDef",
    {
        "S3Url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGameResultTypeDef = TypedDict(
    "GetGameResultTypeDef",
    {
        "Game": GameDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPlayerConnectionStatusResultTypeDef = TypedDict(
    "GetPlayerConnectionStatusResultTypeDef",
    {
        "Connections": List[ConnectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartGeneratedCodeJobResultTypeDef = TypedDict(
    "StartGeneratedCodeJobResultTypeDef",
    {
        "GeneratedCodeJobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameResultTypeDef = TypedDict(
    "UpdateGameResultTypeDef",
    {
        "Game": GameDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStageResultTypeDef = TypedDict(
    "CreateStageResultTypeDef",
    {
        "Stage": StageDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStageResultTypeDef = TypedDict(
    "GetStageResultTypeDef",
    {
        "Stage": StageDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStageResultTypeDef = TypedDict(
    "UpdateStageResultTypeDef",
    {
        "Stage": StageDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StageDeploymentDetailsTypeDef = TypedDict(
    "StageDeploymentDetailsTypeDef",
    {
        "Created": datetime,
        "DeploymentAction": DeploymentActionType,
        "DeploymentId": str,
        "DeploymentResult": DeploymentResultTypeDef,
        "DeploymentState": DeploymentStateType,
        "LastUpdated": datetime,
        "SnapshotId": str,
    },
    total=False,
)

StageDeploymentSummaryTypeDef = TypedDict(
    "StageDeploymentSummaryTypeDef",
    {
        "DeploymentAction": DeploymentActionType,
        "DeploymentId": str,
        "DeploymentResult": DeploymentResultTypeDef,
        "DeploymentState": DeploymentStateType,
        "LastUpdated": datetime,
        "SnapshotId": str,
    },
    total=False,
)

GetExtensionResultTypeDef = TypedDict(
    "GetExtensionResultTypeDef",
    {
        "Extension": ExtensionDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListExtensionsResultTypeDef = TypedDict(
    "ListExtensionsResultTypeDef",
    {
        "Extensions": List[ExtensionDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExtensionVersionResultTypeDef = TypedDict(
    "GetExtensionVersionResultTypeDef",
    {
        "ExtensionVersion": ExtensionVersionDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListExtensionVersionsResultTypeDef = TypedDict(
    "ListExtensionVersionsResultTypeDef",
    {
        "ExtensionVersions": List[ExtensionVersionDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GameConfigurationDetailsTypeDef = TypedDict(
    "GameConfigurationDetailsTypeDef",
    {
        "Created": datetime,
        "LastUpdated": datetime,
        "Sections": Dict[str, SectionTypeDef],
    },
    total=False,
)

SnapshotDetailsTypeDef = TypedDict(
    "SnapshotDetailsTypeDef",
    {
        "Created": datetime,
        "Description": str,
        "Id": str,
        "LastUpdated": datetime,
        "Sections": Dict[str, SectionTypeDef],
    },
    total=False,
)

ListGamesResultTypeDef = TypedDict(
    "ListGamesResultTypeDef",
    {
        "Games": List[GameSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGeneratedCodeJobResultTypeDef = TypedDict(
    "GetGeneratedCodeJobResultTypeDef",
    {
        "GeneratedCodeJob": GeneratedCodeJobDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGeneratedCodeJobsResultTypeDef = TypedDict(
    "ListGeneratedCodeJobsResultTypeDef",
    {
        "GeneratedCodeJobs": List[GeneratedCodeJobDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartGeneratedCodeJobRequestRequestTypeDef = TypedDict(
    "StartGeneratedCodeJobRequestRequestTypeDef",
    {
        "GameName": str,
        "Generator": GeneratorTypeDef,
        "SnapshotId": str,
    },
)

ImportGameConfigurationRequestRequestTypeDef = TypedDict(
    "ImportGameConfigurationRequestRequestTypeDef",
    {
        "GameName": str,
        "ImportSource": ImportGameConfigurationSourceTypeDef,
    },
)

_RequiredListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef",
    {
        "Name": str,
        "Namespace": str,
    },
)
_OptionalListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef(
    _RequiredListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef,
    _OptionalListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef,
):
    pass

ListExtensionsRequestListExtensionsPaginateTypeDef = TypedDict(
    "ListExtensionsRequestListExtensionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListGamesRequestListGamesPaginateTypeDef = TypedDict(
    "ListGamesRequestListGamesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef = TypedDict(
    "_RequiredListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
    },
)
_OptionalListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef = TypedDict(
    "_OptionalListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef(
    _RequiredListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef,
    _OptionalListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef,
):
    pass

_RequiredListSnapshotsRequestListSnapshotsPaginateTypeDef = TypedDict(
    "_RequiredListSnapshotsRequestListSnapshotsPaginateTypeDef",
    {
        "GameName": str,
    },
)
_OptionalListSnapshotsRequestListSnapshotsPaginateTypeDef = TypedDict(
    "_OptionalListSnapshotsRequestListSnapshotsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSnapshotsRequestListSnapshotsPaginateTypeDef(
    _RequiredListSnapshotsRequestListSnapshotsPaginateTypeDef,
    _OptionalListSnapshotsRequestListSnapshotsPaginateTypeDef,
):
    pass

_RequiredListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef = TypedDict(
    "_RequiredListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)
_OptionalListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef = TypedDict(
    "_OptionalListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef(
    _RequiredListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef,
    _OptionalListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef,
):
    pass

_RequiredListStagesRequestListStagesPaginateTypeDef = TypedDict(
    "_RequiredListStagesRequestListStagesPaginateTypeDef",
    {
        "GameName": str,
    },
)
_OptionalListStagesRequestListStagesPaginateTypeDef = TypedDict(
    "_OptionalListStagesRequestListStagesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListStagesRequestListStagesPaginateTypeDef(
    _RequiredListStagesRequestListStagesPaginateTypeDef,
    _OptionalListStagesRequestListStagesPaginateTypeDef,
):
    pass

ListSnapshotsResultTypeDef = TypedDict(
    "ListSnapshotsResultTypeDef",
    {
        "NextToken": str,
        "Snapshots": List[SnapshotSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStagesResultTypeDef = TypedDict(
    "ListStagesResultTypeDef",
    {
        "NextToken": str,
        "Stages": List[StageSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateGameConfigurationRequestRequestTypeDef",
    {
        "GameName": str,
        "Modifications": Sequence[SectionModificationTypeDef],
    },
)

GetStageDeploymentResultTypeDef = TypedDict(
    "GetStageDeploymentResultTypeDef",
    {
        "StageDeployment": StageDeploymentDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartStageDeploymentResultTypeDef = TypedDict(
    "StartStageDeploymentResultTypeDef",
    {
        "StageDeployment": StageDeploymentDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStageDeploymentsResultTypeDef = TypedDict(
    "ListStageDeploymentsResultTypeDef",
    {
        "NextToken": str,
        "StageDeployments": List[StageDeploymentSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGameConfigurationResultTypeDef = TypedDict(
    "GetGameConfigurationResultTypeDef",
    {
        "GameConfiguration": GameConfigurationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportGameConfigurationResultTypeDef = TypedDict(
    "ImportGameConfigurationResultTypeDef",
    {
        "GameConfiguration": GameConfigurationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameConfigurationResultTypeDef = TypedDict(
    "UpdateGameConfigurationResultTypeDef",
    {
        "GameConfiguration": GameConfigurationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSnapshotResultTypeDef = TypedDict(
    "CreateSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSnapshotResultTypeDef = TypedDict(
    "GetSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSnapshotResultTypeDef = TypedDict(
    "UpdateSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
