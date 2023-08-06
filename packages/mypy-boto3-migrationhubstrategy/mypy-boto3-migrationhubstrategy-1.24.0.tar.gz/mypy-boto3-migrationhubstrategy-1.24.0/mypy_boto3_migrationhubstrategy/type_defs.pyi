"""
Type annotations for migrationhubstrategy service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/type_defs/)

Usage::

    ```python
    from mypy_boto3_migrationhubstrategy.type_defs import AntipatternSeveritySummaryTypeDef

    data: AntipatternSeveritySummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AntipatternReportStatusType,
    ApplicationComponentCriteriaType,
    AppTypeType,
    AssessmentStatusType,
    AwsManagedTargetDestinationType,
    CollectorHealthType,
    DatabaseManagementPreferenceType,
    DataSourceTypeType,
    HeterogeneousTargetDatabaseEngineType,
    ImportFileTaskStatusType,
    InclusionStatusType,
    NoPreferenceTargetDestinationType,
    OSTypeType,
    OutputFormatType,
    RecommendationReportStatusType,
    ResourceSubTypeType,
    RunTimeAssessmentStatusType,
    SelfManageTargetDestinationType,
    ServerCriteriaType,
    ServerOsTypeType,
    SeverityType,
    SortOrderType,
    SrcCodeOrDbAnalysisStatusType,
    StrategyRecommendationType,
    StrategyType,
    TargetDatabaseEngineType,
    TargetDestinationType,
    TransformationToolNameType,
    VersionControlType,
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
    "AntipatternSeveritySummaryTypeDef",
    "DatabaseConfigDetailTypeDef",
    "S3ObjectTypeDef",
    "SourceCodeRepositoryTypeDef",
    "ApplicationComponentSummaryTypeDef",
    "ServerSummaryTypeDef",
    "StrategySummaryTypeDef",
    "AssociatedApplicationTypeDef",
    "AwsManagedResourcesTypeDef",
    "BusinessGoalsTypeDef",
    "CollectorTypeDef",
    "DataCollectionDetailsTypeDef",
    "HeterogeneousTypeDef",
    "HomogeneousTypeDef",
    "NoDatabaseMigrationPreferenceTypeDef",
    "GetApplicationComponentDetailsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetApplicationComponentStrategiesRequestRequestTypeDef",
    "GetAssessmentRequestRequestTypeDef",
    "GetImportFileTaskRequestRequestTypeDef",
    "GetRecommendationReportDetailsRequestRequestTypeDef",
    "RecommendationReportDetailsTypeDef",
    "PaginatorConfigTypeDef",
    "GetServerDetailsRequestRequestTypeDef",
    "GetServerStrategiesRequestRequestTypeDef",
    "GroupTypeDef",
    "ImportFileTaskInformationTypeDef",
    "ListCollectorsRequestRequestTypeDef",
    "ListImportFileTaskRequestRequestTypeDef",
    "NoManagementPreferenceTypeDef",
    "SelfManageResourcesTypeDef",
    "NetworkInfoTypeDef",
    "OSInfoTypeDef",
    "TransformationToolTypeDef",
    "SourceCodeTypeDef",
    "StartAssessmentRequestRequestTypeDef",
    "StopAssessmentRequestRequestTypeDef",
    "StrategyOptionTypeDef",
    "AssessmentSummaryTypeDef",
    "PrioritizeBusinessGoalsTypeDef",
    "DatabaseMigrationPreferenceTypeDef",
    "GetAssessmentResponseTypeDef",
    "GetImportFileTaskResponseTypeDef",
    "ListCollectorsResponseTypeDef",
    "StartAssessmentResponseTypeDef",
    "StartImportFileTaskResponseTypeDef",
    "StartRecommendationReportGenerationResponseTypeDef",
    "GetRecommendationReportDetailsResponseTypeDef",
    "GetServerDetailsRequestGetServerDetailsPaginateTypeDef",
    "ListCollectorsRequestListCollectorsPaginateTypeDef",
    "ListImportFileTaskRequestListImportFileTaskPaginateTypeDef",
    "ListApplicationComponentsRequestListApplicationComponentsPaginateTypeDef",
    "ListApplicationComponentsRequestRequestTypeDef",
    "ListServersRequestListServersPaginateTypeDef",
    "ListServersRequestRequestTypeDef",
    "StartImportFileTaskRequestRequestTypeDef",
    "StartRecommendationReportGenerationRequestRequestTypeDef",
    "ListImportFileTaskResponseTypeDef",
    "ManagementPreferenceTypeDef",
    "SystemInfoTypeDef",
    "RecommendationSetTypeDef",
    "UpdateApplicationComponentConfigRequestRequestTypeDef",
    "UpdateServerConfigRequestRequestTypeDef",
    "GetPortfolioSummaryResponseTypeDef",
    "DatabasePreferencesTypeDef",
    "ApplicationPreferencesTypeDef",
    "ApplicationComponentDetailTypeDef",
    "ApplicationComponentStrategyTypeDef",
    "ServerDetailTypeDef",
    "ServerStrategyTypeDef",
    "GetPortfolioPreferencesResponseTypeDef",
    "PutPortfolioPreferencesRequestRequestTypeDef",
    "GetApplicationComponentDetailsResponseTypeDef",
    "ListApplicationComponentsResponseTypeDef",
    "GetApplicationComponentStrategiesResponseTypeDef",
    "GetServerDetailsResponseTypeDef",
    "ListServersResponseTypeDef",
    "GetServerStrategiesResponseTypeDef",
)

AntipatternSeveritySummaryTypeDef = TypedDict(
    "AntipatternSeveritySummaryTypeDef",
    {
        "count": int,
        "severity": SeverityType,
    },
    total=False,
)

DatabaseConfigDetailTypeDef = TypedDict(
    "DatabaseConfigDetailTypeDef",
    {
        "secretName": str,
    },
    total=False,
)

S3ObjectTypeDef = TypedDict(
    "S3ObjectTypeDef",
    {
        "s3Bucket": str,
        "s3key": str,
    },
    total=False,
)

SourceCodeRepositoryTypeDef = TypedDict(
    "SourceCodeRepositoryTypeDef",
    {
        "branch": str,
        "repository": str,
        "versionControlType": str,
    },
    total=False,
)

ApplicationComponentSummaryTypeDef = TypedDict(
    "ApplicationComponentSummaryTypeDef",
    {
        "appType": AppTypeType,
        "count": int,
    },
    total=False,
)

ServerSummaryTypeDef = TypedDict(
    "ServerSummaryTypeDef",
    {
        "ServerOsType": ServerOsTypeType,
        "count": int,
    },
    total=False,
)

StrategySummaryTypeDef = TypedDict(
    "StrategySummaryTypeDef",
    {
        "count": int,
        "strategy": StrategyType,
    },
    total=False,
)

AssociatedApplicationTypeDef = TypedDict(
    "AssociatedApplicationTypeDef",
    {
        "id": str,
        "name": str,
    },
    total=False,
)

AwsManagedResourcesTypeDef = TypedDict(
    "AwsManagedResourcesTypeDef",
    {
        "targetDestination": List[AwsManagedTargetDestinationType],
    },
)

BusinessGoalsTypeDef = TypedDict(
    "BusinessGoalsTypeDef",
    {
        "licenseCostReduction": int,
        "modernizeInfrastructureWithCloudNativeTechnologies": int,
        "reduceOperationalOverheadWithManagedServices": int,
        "speedOfMigration": int,
    },
    total=False,
)

CollectorTypeDef = TypedDict(
    "CollectorTypeDef",
    {
        "collectorHealth": CollectorHealthType,
        "collectorId": str,
        "collectorVersion": str,
        "hostName": str,
        "ipAddress": str,
        "lastActivityTimeStamp": str,
        "registeredTimeStamp": str,
    },
    total=False,
)

DataCollectionDetailsTypeDef = TypedDict(
    "DataCollectionDetailsTypeDef",
    {
        "completionTime": datetime,
        "failed": int,
        "inProgress": int,
        "servers": int,
        "startTime": datetime,
        "status": AssessmentStatusType,
        "success": int,
    },
    total=False,
)

HeterogeneousTypeDef = TypedDict(
    "HeterogeneousTypeDef",
    {
        "targetDatabaseEngine": List[HeterogeneousTargetDatabaseEngineType],
    },
)

HomogeneousTypeDef = TypedDict(
    "HomogeneousTypeDef",
    {
        "targetDatabaseEngine": List[Literal["None specified"]],
    },
    total=False,
)

NoDatabaseMigrationPreferenceTypeDef = TypedDict(
    "NoDatabaseMigrationPreferenceTypeDef",
    {
        "targetDatabaseEngine": List[TargetDatabaseEngineType],
    },
)

GetApplicationComponentDetailsRequestRequestTypeDef = TypedDict(
    "GetApplicationComponentDetailsRequestRequestTypeDef",
    {
        "applicationComponentId": str,
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

GetApplicationComponentStrategiesRequestRequestTypeDef = TypedDict(
    "GetApplicationComponentStrategiesRequestRequestTypeDef",
    {
        "applicationComponentId": str,
    },
)

GetAssessmentRequestRequestTypeDef = TypedDict(
    "GetAssessmentRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetImportFileTaskRequestRequestTypeDef = TypedDict(
    "GetImportFileTaskRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetRecommendationReportDetailsRequestRequestTypeDef = TypedDict(
    "GetRecommendationReportDetailsRequestRequestTypeDef",
    {
        "id": str,
    },
)

RecommendationReportDetailsTypeDef = TypedDict(
    "RecommendationReportDetailsTypeDef",
    {
        "completionTime": datetime,
        "s3Bucket": str,
        "s3Keys": List[str],
        "startTime": datetime,
        "status": RecommendationReportStatusType,
        "statusMessage": str,
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

_RequiredGetServerDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredGetServerDetailsRequestRequestTypeDef",
    {
        "serverId": str,
    },
)
_OptionalGetServerDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalGetServerDetailsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class GetServerDetailsRequestRequestTypeDef(
    _RequiredGetServerDetailsRequestRequestTypeDef, _OptionalGetServerDetailsRequestRequestTypeDef
):
    pass

GetServerStrategiesRequestRequestTypeDef = TypedDict(
    "GetServerStrategiesRequestRequestTypeDef",
    {
        "serverId": str,
    },
)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "name": Literal["ExternalId"],
        "value": str,
    },
    total=False,
)

ImportFileTaskInformationTypeDef = TypedDict(
    "ImportFileTaskInformationTypeDef",
    {
        "completionTime": datetime,
        "id": str,
        "importName": str,
        "inputS3Bucket": str,
        "inputS3Key": str,
        "numberOfRecordsFailed": int,
        "numberOfRecordsSuccess": int,
        "startTime": datetime,
        "status": ImportFileTaskStatusType,
        "statusReportS3Bucket": str,
        "statusReportS3Key": str,
    },
    total=False,
)

ListCollectorsRequestRequestTypeDef = TypedDict(
    "ListCollectorsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListImportFileTaskRequestRequestTypeDef = TypedDict(
    "ListImportFileTaskRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

NoManagementPreferenceTypeDef = TypedDict(
    "NoManagementPreferenceTypeDef",
    {
        "targetDestination": List[NoPreferenceTargetDestinationType],
    },
)

SelfManageResourcesTypeDef = TypedDict(
    "SelfManageResourcesTypeDef",
    {
        "targetDestination": List[SelfManageTargetDestinationType],
    },
)

NetworkInfoTypeDef = TypedDict(
    "NetworkInfoTypeDef",
    {
        "interfaceName": str,
        "ipAddress": str,
        "macAddress": str,
        "netMask": str,
    },
)

OSInfoTypeDef = TypedDict(
    "OSInfoTypeDef",
    {
        "type": OSTypeType,
        "version": str,
    },
    total=False,
)

TransformationToolTypeDef = TypedDict(
    "TransformationToolTypeDef",
    {
        "description": str,
        "name": TransformationToolNameType,
        "tranformationToolInstallationLink": str,
    },
    total=False,
)

SourceCodeTypeDef = TypedDict(
    "SourceCodeTypeDef",
    {
        "location": str,
        "sourceVersion": str,
        "versionControl": VersionControlType,
    },
    total=False,
)

StartAssessmentRequestRequestTypeDef = TypedDict(
    "StartAssessmentRequestRequestTypeDef",
    {
        "s3bucketForAnalysisData": str,
        "s3bucketForReportData": str,
    },
    total=False,
)

StopAssessmentRequestRequestTypeDef = TypedDict(
    "StopAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)

StrategyOptionTypeDef = TypedDict(
    "StrategyOptionTypeDef",
    {
        "isPreferred": bool,
        "strategy": StrategyType,
        "targetDestination": TargetDestinationType,
        "toolName": TransformationToolNameType,
    },
    total=False,
)

AssessmentSummaryTypeDef = TypedDict(
    "AssessmentSummaryTypeDef",
    {
        "antipatternReportS3Object": S3ObjectTypeDef,
        "antipatternReportStatus": AntipatternReportStatusType,
        "antipatternReportStatusMessage": str,
        "lastAnalyzedTimestamp": datetime,
        "listAntipatternSeveritySummary": List[AntipatternSeveritySummaryTypeDef],
        "listApplicationComponentStrategySummary": List[StrategySummaryTypeDef],
        "listApplicationComponentSummary": List[ApplicationComponentSummaryTypeDef],
        "listServerStrategySummary": List[StrategySummaryTypeDef],
        "listServerSummary": List[ServerSummaryTypeDef],
    },
    total=False,
)

PrioritizeBusinessGoalsTypeDef = TypedDict(
    "PrioritizeBusinessGoalsTypeDef",
    {
        "businessGoals": BusinessGoalsTypeDef,
    },
    total=False,
)

DatabaseMigrationPreferenceTypeDef = TypedDict(
    "DatabaseMigrationPreferenceTypeDef",
    {
        "heterogeneous": HeterogeneousTypeDef,
        "homogeneous": HomogeneousTypeDef,
        "noPreference": NoDatabaseMigrationPreferenceTypeDef,
    },
    total=False,
)

GetAssessmentResponseTypeDef = TypedDict(
    "GetAssessmentResponseTypeDef",
    {
        "dataCollectionDetails": DataCollectionDetailsTypeDef,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetImportFileTaskResponseTypeDef = TypedDict(
    "GetImportFileTaskResponseTypeDef",
    {
        "completionTime": datetime,
        "id": str,
        "importName": str,
        "inputS3Bucket": str,
        "inputS3Key": str,
        "numberOfRecordsFailed": int,
        "numberOfRecordsSuccess": int,
        "startTime": datetime,
        "status": ImportFileTaskStatusType,
        "statusReportS3Bucket": str,
        "statusReportS3Key": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCollectorsResponseTypeDef = TypedDict(
    "ListCollectorsResponseTypeDef",
    {
        "Collectors": List[CollectorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssessmentResponseTypeDef = TypedDict(
    "StartAssessmentResponseTypeDef",
    {
        "assessmentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartImportFileTaskResponseTypeDef = TypedDict(
    "StartImportFileTaskResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartRecommendationReportGenerationResponseTypeDef = TypedDict(
    "StartRecommendationReportGenerationResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecommendationReportDetailsResponseTypeDef = TypedDict(
    "GetRecommendationReportDetailsResponseTypeDef",
    {
        "id": str,
        "recommendationReportDetails": RecommendationReportDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetServerDetailsRequestGetServerDetailsPaginateTypeDef = TypedDict(
    "_RequiredGetServerDetailsRequestGetServerDetailsPaginateTypeDef",
    {
        "serverId": str,
    },
)
_OptionalGetServerDetailsRequestGetServerDetailsPaginateTypeDef = TypedDict(
    "_OptionalGetServerDetailsRequestGetServerDetailsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetServerDetailsRequestGetServerDetailsPaginateTypeDef(
    _RequiredGetServerDetailsRequestGetServerDetailsPaginateTypeDef,
    _OptionalGetServerDetailsRequestGetServerDetailsPaginateTypeDef,
):
    pass

ListCollectorsRequestListCollectorsPaginateTypeDef = TypedDict(
    "ListCollectorsRequestListCollectorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListImportFileTaskRequestListImportFileTaskPaginateTypeDef = TypedDict(
    "ListImportFileTaskRequestListImportFileTaskPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListApplicationComponentsRequestListApplicationComponentsPaginateTypeDef = TypedDict(
    "ListApplicationComponentsRequestListApplicationComponentsPaginateTypeDef",
    {
        "applicationComponentCriteria": ApplicationComponentCriteriaType,
        "filterValue": str,
        "groupIdFilter": Sequence[GroupTypeDef],
        "sort": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListApplicationComponentsRequestRequestTypeDef = TypedDict(
    "ListApplicationComponentsRequestRequestTypeDef",
    {
        "applicationComponentCriteria": ApplicationComponentCriteriaType,
        "filterValue": str,
        "groupIdFilter": Sequence[GroupTypeDef],
        "maxResults": int,
        "nextToken": str,
        "sort": SortOrderType,
    },
    total=False,
)

ListServersRequestListServersPaginateTypeDef = TypedDict(
    "ListServersRequestListServersPaginateTypeDef",
    {
        "filterValue": str,
        "groupIdFilter": Sequence[GroupTypeDef],
        "serverCriteria": ServerCriteriaType,
        "sort": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServersRequestRequestTypeDef = TypedDict(
    "ListServersRequestRequestTypeDef",
    {
        "filterValue": str,
        "groupIdFilter": Sequence[GroupTypeDef],
        "maxResults": int,
        "nextToken": str,
        "serverCriteria": ServerCriteriaType,
        "sort": SortOrderType,
    },
    total=False,
)

_RequiredStartImportFileTaskRequestRequestTypeDef = TypedDict(
    "_RequiredStartImportFileTaskRequestRequestTypeDef",
    {
        "S3Bucket": str,
        "name": str,
        "s3key": str,
    },
)
_OptionalStartImportFileTaskRequestRequestTypeDef = TypedDict(
    "_OptionalStartImportFileTaskRequestRequestTypeDef",
    {
        "dataSourceType": DataSourceTypeType,
        "groupId": Sequence[GroupTypeDef],
        "s3bucketForReportData": str,
    },
    total=False,
)

class StartImportFileTaskRequestRequestTypeDef(
    _RequiredStartImportFileTaskRequestRequestTypeDef,
    _OptionalStartImportFileTaskRequestRequestTypeDef,
):
    pass

StartRecommendationReportGenerationRequestRequestTypeDef = TypedDict(
    "StartRecommendationReportGenerationRequestRequestTypeDef",
    {
        "groupIdFilter": Sequence[GroupTypeDef],
        "outputFormat": OutputFormatType,
    },
    total=False,
)

ListImportFileTaskResponseTypeDef = TypedDict(
    "ListImportFileTaskResponseTypeDef",
    {
        "nextToken": str,
        "taskInfos": List[ImportFileTaskInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ManagementPreferenceTypeDef = TypedDict(
    "ManagementPreferenceTypeDef",
    {
        "awsManagedResources": AwsManagedResourcesTypeDef,
        "noPreference": NoManagementPreferenceTypeDef,
        "selfManageResources": SelfManageResourcesTypeDef,
    },
    total=False,
)

SystemInfoTypeDef = TypedDict(
    "SystemInfoTypeDef",
    {
        "cpuArchitecture": str,
        "fileSystemType": str,
        "networkInfoList": List[NetworkInfoTypeDef],
        "osInfo": OSInfoTypeDef,
    },
    total=False,
)

RecommendationSetTypeDef = TypedDict(
    "RecommendationSetTypeDef",
    {
        "strategy": StrategyType,
        "targetDestination": TargetDestinationType,
        "transformationTool": TransformationToolTypeDef,
    },
    total=False,
)

_RequiredUpdateApplicationComponentConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationComponentConfigRequestRequestTypeDef",
    {
        "applicationComponentId": str,
    },
)
_OptionalUpdateApplicationComponentConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationComponentConfigRequestRequestTypeDef",
    {
        "inclusionStatus": InclusionStatusType,
        "secretsManagerKey": str,
        "sourceCodeList": Sequence[SourceCodeTypeDef],
        "strategyOption": StrategyOptionTypeDef,
    },
    total=False,
)

class UpdateApplicationComponentConfigRequestRequestTypeDef(
    _RequiredUpdateApplicationComponentConfigRequestRequestTypeDef,
    _OptionalUpdateApplicationComponentConfigRequestRequestTypeDef,
):
    pass

_RequiredUpdateServerConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServerConfigRequestRequestTypeDef",
    {
        "serverId": str,
    },
)
_OptionalUpdateServerConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServerConfigRequestRequestTypeDef",
    {
        "strategyOption": StrategyOptionTypeDef,
    },
    total=False,
)

class UpdateServerConfigRequestRequestTypeDef(
    _RequiredUpdateServerConfigRequestRequestTypeDef,
    _OptionalUpdateServerConfigRequestRequestTypeDef,
):
    pass

GetPortfolioSummaryResponseTypeDef = TypedDict(
    "GetPortfolioSummaryResponseTypeDef",
    {
        "assessmentSummary": AssessmentSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatabasePreferencesTypeDef = TypedDict(
    "DatabasePreferencesTypeDef",
    {
        "databaseManagementPreference": DatabaseManagementPreferenceType,
        "databaseMigrationPreference": DatabaseMigrationPreferenceTypeDef,
    },
    total=False,
)

ApplicationPreferencesTypeDef = TypedDict(
    "ApplicationPreferencesTypeDef",
    {
        "managementPreference": ManagementPreferenceTypeDef,
    },
    total=False,
)

ApplicationComponentDetailTypeDef = TypedDict(
    "ApplicationComponentDetailTypeDef",
    {
        "analysisStatus": SrcCodeOrDbAnalysisStatusType,
        "antipatternReportS3Object": S3ObjectTypeDef,
        "antipatternReportStatus": AntipatternReportStatusType,
        "antipatternReportStatusMessage": str,
        "appType": AppTypeType,
        "associatedServerId": str,
        "databaseConfigDetail": DatabaseConfigDetailTypeDef,
        "id": str,
        "inclusionStatus": InclusionStatusType,
        "lastAnalyzedTimestamp": datetime,
        "listAntipatternSeveritySummary": List[AntipatternSeveritySummaryTypeDef],
        "moreServerAssociationExists": bool,
        "name": str,
        "osDriver": str,
        "osVersion": str,
        "recommendationSet": RecommendationSetTypeDef,
        "resourceSubType": ResourceSubTypeType,
        "sourceCodeRepositories": List[SourceCodeRepositoryTypeDef],
        "statusMessage": str,
    },
    total=False,
)

ApplicationComponentStrategyTypeDef = TypedDict(
    "ApplicationComponentStrategyTypeDef",
    {
        "isPreferred": bool,
        "recommendation": RecommendationSetTypeDef,
        "status": StrategyRecommendationType,
    },
    total=False,
)

ServerDetailTypeDef = TypedDict(
    "ServerDetailTypeDef",
    {
        "antipatternReportS3Object": S3ObjectTypeDef,
        "antipatternReportStatus": AntipatternReportStatusType,
        "antipatternReportStatusMessage": str,
        "applicationComponentStrategySummary": List[StrategySummaryTypeDef],
        "dataCollectionStatus": RunTimeAssessmentStatusType,
        "id": str,
        "lastAnalyzedTimestamp": datetime,
        "listAntipatternSeveritySummary": List[AntipatternSeveritySummaryTypeDef],
        "name": str,
        "recommendationSet": RecommendationSetTypeDef,
        "serverType": str,
        "statusMessage": str,
        "systemInfo": SystemInfoTypeDef,
    },
    total=False,
)

ServerStrategyTypeDef = TypedDict(
    "ServerStrategyTypeDef",
    {
        "isPreferred": bool,
        "numberOfApplicationComponents": int,
        "recommendation": RecommendationSetTypeDef,
        "status": StrategyRecommendationType,
    },
    total=False,
)

GetPortfolioPreferencesResponseTypeDef = TypedDict(
    "GetPortfolioPreferencesResponseTypeDef",
    {
        "applicationPreferences": ApplicationPreferencesTypeDef,
        "databasePreferences": DatabasePreferencesTypeDef,
        "prioritizeBusinessGoals": PrioritizeBusinessGoalsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutPortfolioPreferencesRequestRequestTypeDef = TypedDict(
    "PutPortfolioPreferencesRequestRequestTypeDef",
    {
        "applicationPreferences": ApplicationPreferencesTypeDef,
        "databasePreferences": DatabasePreferencesTypeDef,
        "prioritizeBusinessGoals": PrioritizeBusinessGoalsTypeDef,
    },
    total=False,
)

GetApplicationComponentDetailsResponseTypeDef = TypedDict(
    "GetApplicationComponentDetailsResponseTypeDef",
    {
        "applicationComponentDetail": ApplicationComponentDetailTypeDef,
        "associatedApplications": List[AssociatedApplicationTypeDef],
        "associatedServerIds": List[str],
        "moreApplicationResource": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationComponentsResponseTypeDef = TypedDict(
    "ListApplicationComponentsResponseTypeDef",
    {
        "applicationComponentInfos": List[ApplicationComponentDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationComponentStrategiesResponseTypeDef = TypedDict(
    "GetApplicationComponentStrategiesResponseTypeDef",
    {
        "applicationComponentStrategies": List[ApplicationComponentStrategyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServerDetailsResponseTypeDef = TypedDict(
    "GetServerDetailsResponseTypeDef",
    {
        "associatedApplications": List[AssociatedApplicationTypeDef],
        "nextToken": str,
        "serverDetail": ServerDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServersResponseTypeDef = TypedDict(
    "ListServersResponseTypeDef",
    {
        "nextToken": str,
        "serverInfos": List[ServerDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServerStrategiesResponseTypeDef = TypedDict(
    "GetServerStrategiesResponseTypeDef",
    {
        "serverStrategies": List[ServerStrategyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
