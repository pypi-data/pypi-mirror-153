"""
Type annotations for migrationhubstrategy service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient

    session = Session()
    client: MigrationHubStrategyRecommendationsClient = session.client("migrationhubstrategy")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ApplicationComponentCriteriaType,
    DataSourceTypeType,
    InclusionStatusType,
    OutputFormatType,
    ServerCriteriaType,
    SortOrderType,
)
from .paginator import (
    GetServerDetailsPaginator,
    ListApplicationComponentsPaginator,
    ListCollectorsPaginator,
    ListImportFileTaskPaginator,
    ListServersPaginator,
)
from .type_defs import (
    ApplicationPreferencesTypeDef,
    DatabasePreferencesTypeDef,
    GetApplicationComponentDetailsResponseTypeDef,
    GetApplicationComponentStrategiesResponseTypeDef,
    GetAssessmentResponseTypeDef,
    GetImportFileTaskResponseTypeDef,
    GetPortfolioPreferencesResponseTypeDef,
    GetPortfolioSummaryResponseTypeDef,
    GetRecommendationReportDetailsResponseTypeDef,
    GetServerDetailsResponseTypeDef,
    GetServerStrategiesResponseTypeDef,
    GroupTypeDef,
    ListApplicationComponentsResponseTypeDef,
    ListCollectorsResponseTypeDef,
    ListImportFileTaskResponseTypeDef,
    ListServersResponseTypeDef,
    PrioritizeBusinessGoalsTypeDef,
    SourceCodeTypeDef,
    StartAssessmentResponseTypeDef,
    StartImportFileTaskResponseTypeDef,
    StartRecommendationReportGenerationResponseTypeDef,
    StrategyOptionTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MigrationHubStrategyRecommendationsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLinkedRoleLockClientException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MigrationHubStrategyRecommendationsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubStrategyRecommendationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#generate_presigned_url)
        """

    def get_application_component_details(
        self, *, applicationComponentId: str
    ) -> GetApplicationComponentDetailsResponseTypeDef:
        """
        Retrieves details about an application component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_application_component_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_application_component_details)
        """

    def get_application_component_strategies(
        self, *, applicationComponentId: str
    ) -> GetApplicationComponentStrategiesResponseTypeDef:
        """
        Retrieves a list of all the recommended strategies and tools for an application
        component running on a server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_application_component_strategies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_application_component_strategies)
        """

    def get_assessment(self, *, id: str) -> GetAssessmentResponseTypeDef:
        """
        Retrieves the status of an on-going assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_assessment)
        """

    def get_import_file_task(self, *, id: str) -> GetImportFileTaskResponseTypeDef:
        """
        Retrieves the details about a specific import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_import_file_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_import_file_task)
        """

    def get_portfolio_preferences(self) -> GetPortfolioPreferencesResponseTypeDef:
        """
        Retrieves your migration and modernization preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_portfolio_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_portfolio_preferences)
        """

    def get_portfolio_summary(self) -> GetPortfolioSummaryResponseTypeDef:
        """
        Retrieves overall summary including the number of servers to rehost and the
        overall number of anti-patterns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_portfolio_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_portfolio_summary)
        """

    def get_recommendation_report_details(
        self, *, id: str
    ) -> GetRecommendationReportDetailsResponseTypeDef:
        """
        Retrieves detailed information about the specified recommendation report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_recommendation_report_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_recommendation_report_details)
        """

    def get_server_details(
        self, *, serverId: str, maxResults: int = ..., nextToken: str = ...
    ) -> GetServerDetailsResponseTypeDef:
        """
        Retrieves detailed information about a specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_server_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_server_details)
        """

    def get_server_strategies(self, *, serverId: str) -> GetServerStrategiesResponseTypeDef:
        """
        Retrieves recommended strategies and tools for the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_server_strategies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_server_strategies)
        """

    def list_application_components(
        self,
        *,
        applicationComponentCriteria: ApplicationComponentCriteriaType = ...,
        filterValue: str = ...,
        groupIdFilter: Sequence[GroupTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sort: SortOrderType = ...
    ) -> ListApplicationComponentsResponseTypeDef:
        """
        Retrieves a list of all the application components (processes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_application_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_application_components)
        """

    def list_collectors(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListCollectorsResponseTypeDef:
        """
        Retrieves a list of all the installed collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_collectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_collectors)
        """

    def list_import_file_task(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListImportFileTaskResponseTypeDef:
        """
        Retrieves a list of all the imports performed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_import_file_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_import_file_task)
        """

    def list_servers(
        self,
        *,
        filterValue: str = ...,
        groupIdFilter: Sequence[GroupTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        serverCriteria: ServerCriteriaType = ...,
        sort: SortOrderType = ...
    ) -> ListServersResponseTypeDef:
        """
        Returns a list of all the servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_servers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_servers)
        """

    def put_portfolio_preferences(
        self,
        *,
        applicationPreferences: ApplicationPreferencesTypeDef = ...,
        databasePreferences: DatabasePreferencesTypeDef = ...,
        prioritizeBusinessGoals: PrioritizeBusinessGoalsTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Saves the specified migration and modernization preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.put_portfolio_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#put_portfolio_preferences)
        """

    def start_assessment(
        self, *, s3bucketForAnalysisData: str = ..., s3bucketForReportData: str = ...
    ) -> StartAssessmentResponseTypeDef:
        """
        Starts the assessment of an on-premises environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.start_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#start_assessment)
        """

    def start_import_file_task(
        self,
        *,
        S3Bucket: str,
        name: str,
        s3key: str,
        dataSourceType: DataSourceTypeType = ...,
        groupId: Sequence[GroupTypeDef] = ...,
        s3bucketForReportData: str = ...
    ) -> StartImportFileTaskResponseTypeDef:
        """
        Starts a file import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.start_import_file_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#start_import_file_task)
        """

    def start_recommendation_report_generation(
        self, *, groupIdFilter: Sequence[GroupTypeDef] = ..., outputFormat: OutputFormatType = ...
    ) -> StartRecommendationReportGenerationResponseTypeDef:
        """
        Starts generating a recommendation report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.start_recommendation_report_generation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#start_recommendation_report_generation)
        """

    def stop_assessment(self, *, assessmentId: str) -> Dict[str, Any]:
        """
        Stops the assessment of an on-premises environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.stop_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#stop_assessment)
        """

    def update_application_component_config(
        self,
        *,
        applicationComponentId: str,
        inclusionStatus: InclusionStatusType = ...,
        secretsManagerKey: str = ...,
        sourceCodeList: Sequence[SourceCodeTypeDef] = ...,
        strategyOption: StrategyOptionTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Updates the configuration of an application component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.update_application_component_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#update_application_component_config)
        """

    def update_server_config(
        self, *, serverId: str, strategyOption: StrategyOptionTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Updates the configuration of the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.update_server_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#update_server_config)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_server_details"]
    ) -> GetServerDetailsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_components"]
    ) -> ListApplicationComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_collectors"]) -> ListCollectorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_file_task"]
    ) -> ListImportFileTaskPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """
