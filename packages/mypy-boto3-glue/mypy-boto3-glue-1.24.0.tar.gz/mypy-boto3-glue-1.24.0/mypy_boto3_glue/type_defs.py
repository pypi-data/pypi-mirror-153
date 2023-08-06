"""
Type annotations for glue service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/type_defs/)

Usage::

    ```python
    from mypy_boto3_glue.type_defs import NotificationPropertyTypeDef

    data: NotificationPropertyTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AggFunctionType,
    BackfillErrorCodeType,
    BlueprintRunStateType,
    BlueprintStatusType,
    CatalogEncryptionModeType,
    CloudWatchEncryptionModeType,
    ColumnStatisticsTypeType,
    ComparatorType,
    CompatibilityType,
    CompressionTypeType,
    ConnectionPropertyKeyType,
    ConnectionTypeType,
    CrawlerLineageSettingsType,
    CrawlerStateType,
    CrawlStateType,
    CsvHeaderOptionType,
    DataFormatType,
    DeleteBehaviorType,
    EnableHybridValuesType,
    ExistConditionType,
    FilterLogicalOperatorType,
    FilterOperationType,
    FilterValueTypeType,
    GlueRecordTypeType,
    JDBCDataTypeType,
    JobBookmarksEncryptionModeType,
    JobRunStateType,
    JoinTypeType,
    LanguageType,
    LastCrawlStatusType,
    LogicalType,
    MLUserDataEncryptionModeStringType,
    NodeTypeType,
    ParquetCompressionTypeType,
    PartitionIndexStatusType,
    PermissionType,
    PermissionTypeType,
    PiiTypeType,
    PrincipalTypeType,
    QuoteCharType,
    RecrawlBehaviorType,
    RegistryStatusType,
    ResourceShareTypeType,
    ResourceTypeType,
    S3EncryptionModeType,
    ScheduleStateType,
    SchemaStatusType,
    SchemaVersionStatusType,
    SeparatorType,
    SessionStatusType,
    SortDirectionTypeType,
    SortType,
    StartingPositionType,
    StatementStateType,
    TargetFormatType,
    TaskRunSortColumnTypeType,
    TaskStatusTypeType,
    TaskTypeType,
    TransformSortColumnTypeType,
    TransformStatusTypeType,
    TriggerStateType,
    TriggerTypeType,
    UnionTypeType,
    UpdateBehaviorType,
    UpdateCatalogBehaviorType,
    WorkerTypeType,
    WorkflowRunStatusType,
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
    "NotificationPropertyTypeDef",
    "AggregateOperationTypeDef",
    "ApplyMappingTypeDef",
    "AuditContextTypeDef",
    "PartitionValueListTypeDef",
    "BasicCatalogTargetTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteConnectionRequestRequestTypeDef",
    "ErrorDetailTypeDef",
    "BatchDeleteTableRequestRequestTypeDef",
    "BatchDeleteTableVersionRequestRequestTypeDef",
    "BatchGetBlueprintsRequestRequestTypeDef",
    "BatchGetCrawlersRequestRequestTypeDef",
    "BatchGetCustomEntityTypesRequestRequestTypeDef",
    "CustomEntityTypeTypeDef",
    "BatchGetDevEndpointsRequestRequestTypeDef",
    "DevEndpointTypeDef",
    "BatchGetJobsRequestRequestTypeDef",
    "BatchGetTriggersRequestRequestTypeDef",
    "BatchGetWorkflowsRequestRequestTypeDef",
    "BatchStopJobRunRequestRequestTypeDef",
    "BatchStopJobRunSuccessfulSubmissionTypeDef",
    "BinaryColumnStatisticsDataTypeDef",
    "BlueprintDetailsTypeDef",
    "BlueprintRunTypeDef",
    "LastActiveDefinitionTypeDef",
    "BooleanColumnStatisticsDataTypeDef",
    "CancelMLTaskRunRequestRequestTypeDef",
    "CancelStatementRequestRequestTypeDef",
    "CatalogEntryTypeDef",
    "CatalogImportStatusTypeDef",
    "KafkaStreamingSourceOptionsTypeDef",
    "StreamingDataPreviewOptionsTypeDef",
    "KinesisStreamingSourceOptionsTypeDef",
    "CatalogSchemaChangePolicyTypeDef",
    "CatalogSourceTypeDef",
    "CatalogTargetTypeDef",
    "CheckSchemaVersionValidityInputRequestTypeDef",
    "CsvClassifierTypeDef",
    "GrokClassifierTypeDef",
    "JsonClassifierTypeDef",
    "XMLClassifierTypeDef",
    "CloudWatchEncryptionTypeDef",
    "DropDuplicatesTypeDef",
    "DropFieldsTypeDef",
    "DynamoDBCatalogSourceTypeDef",
    "FillMissingValuesTypeDef",
    "MergeTypeDef",
    "MicrosoftSQLServerCatalogSourceTypeDef",
    "MicrosoftSQLServerCatalogTargetTypeDef",
    "MySQLCatalogSourceTypeDef",
    "MySQLCatalogTargetTypeDef",
    "OracleSQLCatalogSourceTypeDef",
    "OracleSQLCatalogTargetTypeDef",
    "PIIDetectionTypeDef",
    "PostgreSQLCatalogSourceTypeDef",
    "PostgreSQLCatalogTargetTypeDef",
    "RedshiftSourceTypeDef",
    "RelationalCatalogSourceTypeDef",
    "RenameFieldTypeDef",
    "SelectFieldsTypeDef",
    "SelectFromCollectionTypeDef",
    "SpigotTypeDef",
    "SplitFieldsTypeDef",
    "UnionTypeDef",
    "CodeGenEdgeTypeDef",
    "CodeGenNodeArgTypeDef",
    "ColumnImportanceTypeDef",
    "ColumnRowFilterTypeDef",
    "DateColumnStatisticsDataTypeDef",
    "DoubleColumnStatisticsDataTypeDef",
    "LongColumnStatisticsDataTypeDef",
    "StringColumnStatisticsDataTypeDef",
    "ColumnTypeDef",
    "ConditionTypeDef",
    "ConfusionMatrixTypeDef",
    "PhysicalConnectionRequirementsTypeDef",
    "ConnectionPasswordEncryptionTypeDef",
    "ConnectionsListTypeDef",
    "CrawlTypeDef",
    "CrawlerMetricsTypeDef",
    "DeltaTargetTypeDef",
    "DynamoDBTargetTypeDef",
    "JdbcTargetTypeDef",
    "MongoDBTargetTypeDef",
    "S3TargetTypeDef",
    "LakeFormationConfigurationTypeDef",
    "LastCrawlInfoTypeDef",
    "LineageConfigurationTypeDef",
    "RecrawlPolicyTypeDef",
    "ScheduleTypeDef",
    "SchemaChangePolicyTypeDef",
    "CreateBlueprintRequestRequestTypeDef",
    "CreateCsvClassifierRequestTypeDef",
    "CreateGrokClassifierRequestTypeDef",
    "CreateJsonClassifierRequestTypeDef",
    "CreateXMLClassifierRequestTypeDef",
    "CreateCustomEntityTypeRequestRequestTypeDef",
    "CreateDevEndpointRequestRequestTypeDef",
    "ExecutionPropertyTypeDef",
    "JobCommandTypeDef",
    "GlueTableTypeDef",
    "PartitionIndexTypeDef",
    "CreateRegistryInputRequestTypeDef",
    "RegistryIdTypeDef",
    "SessionCommandTypeDef",
    "EventBatchingConditionTypeDef",
    "CreateWorkflowRequestRequestTypeDef",
    "EncryptionAtRestTypeDef",
    "DataLakePrincipalTypeDef",
    "DatabaseIdentifierTypeDef",
    "DatatypeTypeDef",
    "DecimalNumberTypeDef",
    "DeleteBlueprintRequestRequestTypeDef",
    "DeleteClassifierRequestRequestTypeDef",
    "DeleteColumnStatisticsForPartitionRequestRequestTypeDef",
    "DeleteColumnStatisticsForTableRequestRequestTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "DeleteCrawlerRequestRequestTypeDef",
    "DeleteCustomEntityTypeRequestRequestTypeDef",
    "DeleteDatabaseRequestRequestTypeDef",
    "DeleteDevEndpointRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteMLTransformRequestRequestTypeDef",
    "DeletePartitionIndexRequestRequestTypeDef",
    "DeletePartitionRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "SchemaIdTypeDef",
    "DeleteSecurityConfigurationRequestRequestTypeDef",
    "DeleteSessionRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "DeleteTableVersionRequestRequestTypeDef",
    "DeleteTriggerRequestRequestTypeDef",
    "DeleteUserDefinedFunctionRequestRequestTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "DevEndpointCustomLibrariesTypeDef",
    "DirectSchemaChangePolicyTypeDef",
    "NullCheckBoxListTypeDef",
    "EdgeTypeDef",
    "JobBookmarksEncryptionTypeDef",
    "S3EncryptionTypeDef",
    "ErrorDetailsTypeDef",
    "ExportLabelsTaskRunPropertiesTypeDef",
    "FilterValueTypeDef",
    "FindMatchesParametersTypeDef",
    "FindMatchesTaskRunPropertiesTypeDef",
    "GetBlueprintRequestRequestTypeDef",
    "GetBlueprintRunRequestRequestTypeDef",
    "GetBlueprintRunsRequestRequestTypeDef",
    "GetCatalogImportStatusRequestRequestTypeDef",
    "GetClassifierRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetClassifiersRequestRequestTypeDef",
    "GetColumnStatisticsForPartitionRequestRequestTypeDef",
    "GetColumnStatisticsForTableRequestRequestTypeDef",
    "GetConnectionRequestRequestTypeDef",
    "GetConnectionsFilterTypeDef",
    "GetCrawlerMetricsRequestRequestTypeDef",
    "GetCrawlerRequestRequestTypeDef",
    "GetCrawlersRequestRequestTypeDef",
    "GetCustomEntityTypeRequestRequestTypeDef",
    "GetDataCatalogEncryptionSettingsRequestRequestTypeDef",
    "GetDatabaseRequestRequestTypeDef",
    "GetDatabasesRequestRequestTypeDef",
    "GetDataflowGraphRequestRequestTypeDef",
    "GetDevEndpointRequestRequestTypeDef",
    "GetDevEndpointsRequestRequestTypeDef",
    "GetJobBookmarkRequestRequestTypeDef",
    "JobBookmarkEntryTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobRunRequestRequestTypeDef",
    "GetJobRunsRequestRequestTypeDef",
    "GetJobsRequestRequestTypeDef",
    "GetMLTaskRunRequestRequestTypeDef",
    "TaskRunFilterCriteriaTypeDef",
    "TaskRunSortCriteriaTypeDef",
    "GetMLTransformRequestRequestTypeDef",
    "SchemaColumnTypeDef",
    "TransformSortCriteriaTypeDef",
    "MappingEntryTypeDef",
    "GetPartitionIndexesRequestRequestTypeDef",
    "GetPartitionRequestRequestTypeDef",
    "SegmentTypeDef",
    "GetResourcePoliciesRequestRequestTypeDef",
    "GluePolicyTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "SchemaVersionNumberTypeDef",
    "GetSecurityConfigurationRequestRequestTypeDef",
    "GetSecurityConfigurationsRequestRequestTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetStatementRequestRequestTypeDef",
    "GetTableRequestRequestTypeDef",
    "GetTableVersionRequestRequestTypeDef",
    "GetTableVersionsRequestRequestTypeDef",
    "GetTablesRequestRequestTypeDef",
    "GetTagsRequestRequestTypeDef",
    "GetTriggerRequestRequestTypeDef",
    "GetTriggersRequestRequestTypeDef",
    "GetUserDefinedFunctionRequestRequestTypeDef",
    "GetUserDefinedFunctionsRequestRequestTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "GetWorkflowRunPropertiesRequestRequestTypeDef",
    "GetWorkflowRunRequestRequestTypeDef",
    "GetWorkflowRunsRequestRequestTypeDef",
    "GlueStudioSchemaColumnTypeDef",
    "S3SourceAdditionalOptionsTypeDef",
    "ImportCatalogToGlueRequestRequestTypeDef",
    "ImportLabelsTaskRunPropertiesTypeDef",
    "JDBCConnectorOptionsTypeDef",
    "PredecessorTypeDef",
    "JoinColumnTypeDef",
    "KeySchemaElementTypeDef",
    "LabelingSetGenerationTaskRunPropertiesTypeDef",
    "ListBlueprintsRequestRequestTypeDef",
    "ListCrawlersRequestRequestTypeDef",
    "ListCustomEntityTypesRequestRequestTypeDef",
    "ListDevEndpointsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListRegistriesInputRequestTypeDef",
    "RegistryListItemTypeDef",
    "SchemaVersionListItemTypeDef",
    "SchemaListItemTypeDef",
    "ListSessionsRequestRequestTypeDef",
    "ListStatementsRequestRequestTypeDef",
    "ListTriggersRequestRequestTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "MLUserDataEncryptionTypeDef",
    "MappingTypeDef",
    "OtherMetadataValueListItemTypeDef",
    "MetadataKeyValuePairTypeDef",
    "OrderTypeDef",
    "PropertyPredicateTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutWorkflowRunPropertiesRequestRequestTypeDef",
    "UpsertRedshiftTargetOptionsTypeDef",
    "ResetJobBookmarkRequestRequestTypeDef",
    "ResourceUriTypeDef",
    "ResumeWorkflowRunRequestRequestTypeDef",
    "RunStatementRequestRequestTypeDef",
    "S3DirectSourceAdditionalOptionsTypeDef",
    "SortCriterionTypeDef",
    "SerDeInfoTypeDef",
    "SkewedInfoTypeDef",
    "SqlAliasTypeDef",
    "StartBlueprintRunRequestRequestTypeDef",
    "StartCrawlerRequestRequestTypeDef",
    "StartCrawlerScheduleRequestRequestTypeDef",
    "StartExportLabelsTaskRunRequestRequestTypeDef",
    "StartImportLabelsTaskRunRequestRequestTypeDef",
    "StartMLEvaluationTaskRunRequestRequestTypeDef",
    "StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef",
    "StartTriggerRequestRequestTypeDef",
    "StartWorkflowRunRequestRequestTypeDef",
    "StartingEventBatchConditionTypeDef",
    "StatementOutputDataTypeDef",
    "StopCrawlerRequestRequestTypeDef",
    "StopCrawlerScheduleRequestRequestTypeDef",
    "StopSessionRequestRequestTypeDef",
    "StopTriggerRequestRequestTypeDef",
    "StopWorkflowRunRequestRequestTypeDef",
    "TableIdentifierTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBlueprintRequestRequestTypeDef",
    "UpdateCsvClassifierRequestTypeDef",
    "UpdateGrokClassifierRequestTypeDef",
    "UpdateJsonClassifierRequestTypeDef",
    "UpdateXMLClassifierRequestTypeDef",
    "UpdateCrawlerScheduleRequestRequestTypeDef",
    "UpdateWorkflowRequestRequestTypeDef",
    "WorkflowRunStatisticsTypeDef",
    "ActionTypeDef",
    "StartJobRunRequestRequestTypeDef",
    "AggregateTypeDef",
    "GetUnfilteredPartitionMetadataRequestRequestTypeDef",
    "GetUnfilteredTableMetadataRequestRequestTypeDef",
    "BackfillErrorTypeDef",
    "BatchDeletePartitionRequestRequestTypeDef",
    "BatchGetPartitionRequestRequestTypeDef",
    "CancelMLTaskRunResponseTypeDef",
    "CheckSchemaVersionValidityResponseTypeDef",
    "CreateBlueprintResponseTypeDef",
    "CreateCustomEntityTypeResponseTypeDef",
    "CreateDevEndpointResponseTypeDef",
    "CreateJobResponseTypeDef",
    "CreateMLTransformResponseTypeDef",
    "CreateRegistryResponseTypeDef",
    "CreateSchemaResponseTypeDef",
    "CreateScriptResponseTypeDef",
    "CreateSecurityConfigurationResponseTypeDef",
    "CreateTriggerResponseTypeDef",
    "CreateWorkflowResponseTypeDef",
    "DeleteBlueprintResponseTypeDef",
    "DeleteCustomEntityTypeResponseTypeDef",
    "DeleteJobResponseTypeDef",
    "DeleteMLTransformResponseTypeDef",
    "DeleteRegistryResponseTypeDef",
    "DeleteSchemaResponseTypeDef",
    "DeleteSessionResponseTypeDef",
    "DeleteTriggerResponseTypeDef",
    "DeleteWorkflowResponseTypeDef",
    "GetCustomEntityTypeResponseTypeDef",
    "GetPlanResponseTypeDef",
    "GetRegistryResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetSchemaByDefinitionResponseTypeDef",
    "GetSchemaResponseTypeDef",
    "GetSchemaVersionResponseTypeDef",
    "GetSchemaVersionsDiffResponseTypeDef",
    "GetTagsResponseTypeDef",
    "GetWorkflowRunPropertiesResponseTypeDef",
    "ListBlueprintsResponseTypeDef",
    "ListCrawlersResponseTypeDef",
    "ListDevEndpointsResponseTypeDef",
    "ListJobsResponseTypeDef",
    "ListMLTransformsResponseTypeDef",
    "ListTriggersResponseTypeDef",
    "ListWorkflowsResponseTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "PutSchemaVersionMetadataResponseTypeDef",
    "RegisterSchemaVersionResponseTypeDef",
    "RemoveSchemaVersionMetadataResponseTypeDef",
    "ResumeWorkflowRunResponseTypeDef",
    "RunStatementResponseTypeDef",
    "StartBlueprintRunResponseTypeDef",
    "StartExportLabelsTaskRunResponseTypeDef",
    "StartImportLabelsTaskRunResponseTypeDef",
    "StartJobRunResponseTypeDef",
    "StartMLEvaluationTaskRunResponseTypeDef",
    "StartMLLabelingSetGenerationTaskRunResponseTypeDef",
    "StartTriggerResponseTypeDef",
    "StartWorkflowRunResponseTypeDef",
    "StopSessionResponseTypeDef",
    "StopTriggerResponseTypeDef",
    "UpdateBlueprintResponseTypeDef",
    "UpdateJobResponseTypeDef",
    "UpdateMLTransformResponseTypeDef",
    "UpdateRegistryResponseTypeDef",
    "UpdateSchemaResponseTypeDef",
    "UpdateWorkflowResponseTypeDef",
    "BatchDeleteConnectionResponseTypeDef",
    "BatchStopJobRunErrorTypeDef",
    "BatchUpdatePartitionFailureEntryTypeDef",
    "ColumnErrorTypeDef",
    "PartitionErrorTypeDef",
    "TableErrorTypeDef",
    "TableVersionErrorTypeDef",
    "BatchGetCustomEntityTypesResponseTypeDef",
    "ListCustomEntityTypesResponseTypeDef",
    "BatchGetDevEndpointsResponseTypeDef",
    "GetDevEndpointResponseTypeDef",
    "GetDevEndpointsResponseTypeDef",
    "GetBlueprintRunResponseTypeDef",
    "GetBlueprintRunsResponseTypeDef",
    "BlueprintTypeDef",
    "GetCatalogImportStatusResponseTypeDef",
    "CatalogKafkaSourceTypeDef",
    "DirectKafkaSourceTypeDef",
    "CatalogKinesisSourceTypeDef",
    "DirectKinesisSourceTypeDef",
    "GovernedCatalogTargetTypeDef",
    "S3CatalogTargetTypeDef",
    "ClassifierTypeDef",
    "CodeGenNodeTypeDef",
    "LocationTypeDef",
    "PredicateTypeDef",
    "FindMatchesMetricsTypeDef",
    "ConnectionInputTypeDef",
    "ConnectionTypeDef",
    "CrawlerNodeDetailsTypeDef",
    "GetCrawlerMetricsResponseTypeDef",
    "CrawlerTargetsTypeDef",
    "CreateClassifierRequestRequestTypeDef",
    "CreatePartitionIndexRequestRequestTypeDef",
    "CreateSchemaInputRequestTypeDef",
    "DeleteRegistryInputRequestTypeDef",
    "GetRegistryInputRequestTypeDef",
    "ListSchemasInputRequestTypeDef",
    "UpdateRegistryInputRequestTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "SessionTypeDef",
    "DataCatalogEncryptionSettingsTypeDef",
    "PrincipalPermissionsTypeDef",
    "NullValueFieldTypeDef",
    "DecimalColumnStatisticsDataTypeDef",
    "DeleteSchemaInputRequestTypeDef",
    "DeleteSchemaVersionsInputRequestTypeDef",
    "GetSchemaByDefinitionInputRequestTypeDef",
    "GetSchemaInputRequestTypeDef",
    "ListSchemaVersionsInputRequestTypeDef",
    "RegisterSchemaVersionInputRequestTypeDef",
    "SchemaReferenceTypeDef",
    "UpdateDevEndpointRequestRequestTypeDef",
    "S3DirectTargetTypeDef",
    "S3GlueParquetTargetTypeDef",
    "EncryptionConfigurationTypeDef",
    "SchemaVersionErrorItemTypeDef",
    "FilterExpressionTypeDef",
    "TransformParametersTypeDef",
    "GetClassifiersRequestGetClassifiersPaginateTypeDef",
    "GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef",
    "GetCrawlersRequestGetCrawlersPaginateTypeDef",
    "GetDatabasesRequestGetDatabasesPaginateTypeDef",
    "GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef",
    "GetJobRunsRequestGetJobRunsPaginateTypeDef",
    "GetJobsRequestGetJobsPaginateTypeDef",
    "GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef",
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    "GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef",
    "GetTableVersionsRequestGetTableVersionsPaginateTypeDef",
    "GetTablesRequestGetTablesPaginateTypeDef",
    "GetTriggersRequestGetTriggersPaginateTypeDef",
    "GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef",
    "ListRegistriesInputListRegistriesPaginateTypeDef",
    "ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef",
    "ListSchemasInputListSchemasPaginateTypeDef",
    "GetConnectionsRequestGetConnectionsPaginateTypeDef",
    "GetConnectionsRequestRequestTypeDef",
    "GetJobBookmarkResponseTypeDef",
    "ResetJobBookmarkResponseTypeDef",
    "GetMLTaskRunsRequestRequestTypeDef",
    "TransformFilterCriteriaTypeDef",
    "GetMappingResponseTypeDef",
    "GetPartitionsRequestGetPartitionsPaginateTypeDef",
    "GetPartitionsRequestRequestTypeDef",
    "GetUnfilteredPartitionsMetadataRequestRequestTypeDef",
    "GetResourcePoliciesResponseTypeDef",
    "GetSchemaVersionInputRequestTypeDef",
    "GetSchemaVersionsDiffInputRequestTypeDef",
    "UpdateSchemaInputRequestTypeDef",
    "GlueSchemaTypeDef",
    "GovernedCatalogSourceTypeDef",
    "S3CatalogSourceTypeDef",
    "JobRunTypeDef",
    "JoinTypeDef",
    "TaskRunPropertiesTypeDef",
    "ListRegistriesResponseTypeDef",
    "ListSchemaVersionsResponseTypeDef",
    "ListSchemasResponseTypeDef",
    "TransformEncryptionTypeDef",
    "MetadataInfoTypeDef",
    "PutSchemaVersionMetadataInputRequestTypeDef",
    "QuerySchemaVersionMetadataInputRequestTypeDef",
    "RemoveSchemaVersionMetadataInputRequestTypeDef",
    "RedshiftTargetTypeDef",
    "UserDefinedFunctionInputTypeDef",
    "UserDefinedFunctionTypeDef",
    "SearchTablesRequestRequestTypeDef",
    "StatementOutputTypeDef",
    "UpdateClassifierRequestRequestTypeDef",
    "PartitionIndexDescriptorTypeDef",
    "BatchStopJobRunResponseTypeDef",
    "BatchUpdatePartitionResponseTypeDef",
    "BatchCreatePartitionResponseTypeDef",
    "BatchDeletePartitionResponseTypeDef",
    "BatchDeleteTableResponseTypeDef",
    "BatchDeleteTableVersionResponseTypeDef",
    "BatchGetBlueprintsResponseTypeDef",
    "GetBlueprintResponseTypeDef",
    "GetClassifierResponseTypeDef",
    "GetClassifiersResponseTypeDef",
    "CreateScriptRequestRequestTypeDef",
    "GetDataflowGraphResponseTypeDef",
    "GetMappingRequestRequestTypeDef",
    "GetPlanRequestRequestTypeDef",
    "CreateTriggerRequestRequestTypeDef",
    "TriggerTypeDef",
    "TriggerUpdateTypeDef",
    "EvaluationMetricsTypeDef",
    "CreateConnectionRequestRequestTypeDef",
    "UpdateConnectionRequestRequestTypeDef",
    "GetConnectionResponseTypeDef",
    "GetConnectionsResponseTypeDef",
    "CrawlerTypeDef",
    "CreateCrawlerRequestRequestTypeDef",
    "UpdateCrawlerRequestRequestTypeDef",
    "CreateSessionResponseTypeDef",
    "GetSessionResponseTypeDef",
    "ListSessionsResponseTypeDef",
    "GetDataCatalogEncryptionSettingsResponseTypeDef",
    "PutDataCatalogEncryptionSettingsRequestRequestTypeDef",
    "DatabaseInputTypeDef",
    "DatabaseTypeDef",
    "DropNullFieldsTypeDef",
    "ColumnStatisticsDataTypeDef",
    "StorageDescriptorTypeDef",
    "CreateSecurityConfigurationRequestRequestTypeDef",
    "SecurityConfigurationTypeDef",
    "DeleteSchemaVersionsResponseTypeDef",
    "FilterTypeDef",
    "UpdateMLTransformRequestRequestTypeDef",
    "GetMLTransformsRequestRequestTypeDef",
    "ListMLTransformsRequestRequestTypeDef",
    "AthenaConnectorSourceTypeDef",
    "CustomCodeTypeDef",
    "JDBCConnectorSourceTypeDef",
    "JDBCConnectorTargetTypeDef",
    "S3CsvSourceTypeDef",
    "S3JsonSourceTypeDef",
    "S3ParquetSourceTypeDef",
    "SparkConnectorSourceTypeDef",
    "SparkConnectorTargetTypeDef",
    "SparkSQLTypeDef",
    "GetJobRunResponseTypeDef",
    "GetJobRunsResponseTypeDef",
    "JobNodeDetailsTypeDef",
    "GetMLTaskRunResponseTypeDef",
    "TaskRunTypeDef",
    "CreateMLTransformRequestRequestTypeDef",
    "QuerySchemaVersionMetadataResponseTypeDef",
    "CreateUserDefinedFunctionRequestRequestTypeDef",
    "UpdateUserDefinedFunctionRequestRequestTypeDef",
    "GetUserDefinedFunctionResponseTypeDef",
    "GetUserDefinedFunctionsResponseTypeDef",
    "StatementTypeDef",
    "GetPartitionIndexesResponseTypeDef",
    "BatchGetTriggersResponseTypeDef",
    "GetTriggerResponseTypeDef",
    "GetTriggersResponseTypeDef",
    "TriggerNodeDetailsTypeDef",
    "UpdateTriggerResponseTypeDef",
    "UpdateTriggerRequestRequestTypeDef",
    "GetMLTransformResponseTypeDef",
    "MLTransformTypeDef",
    "BatchGetCrawlersResponseTypeDef",
    "GetCrawlerResponseTypeDef",
    "GetCrawlersResponseTypeDef",
    "CreateDatabaseRequestRequestTypeDef",
    "UpdateDatabaseRequestRequestTypeDef",
    "GetDatabaseResponseTypeDef",
    "GetDatabasesResponseTypeDef",
    "ColumnStatisticsTypeDef",
    "PartitionInputTypeDef",
    "PartitionTypeDef",
    "TableInputTypeDef",
    "TableTypeDef",
    "GetSecurityConfigurationResponseTypeDef",
    "GetSecurityConfigurationsResponseTypeDef",
    "CodeGenConfigurationNodeTypeDef",
    "GetMLTaskRunsResponseTypeDef",
    "GetStatementResponseTypeDef",
    "ListStatementsResponseTypeDef",
    "NodeTypeDef",
    "GetMLTransformsResponseTypeDef",
    "ColumnStatisticsErrorTypeDef",
    "GetColumnStatisticsForPartitionResponseTypeDef",
    "GetColumnStatisticsForTableResponseTypeDef",
    "UpdateColumnStatisticsForPartitionRequestRequestTypeDef",
    "UpdateColumnStatisticsForTableRequestRequestTypeDef",
    "BatchCreatePartitionRequestRequestTypeDef",
    "BatchUpdatePartitionRequestEntryTypeDef",
    "CreatePartitionRequestRequestTypeDef",
    "UpdatePartitionRequestRequestTypeDef",
    "BatchGetPartitionResponseTypeDef",
    "GetPartitionResponseTypeDef",
    "GetPartitionsResponseTypeDef",
    "GetUnfilteredPartitionMetadataResponseTypeDef",
    "UnfilteredPartitionTypeDef",
    "CreateTableRequestRequestTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "GetTableResponseTypeDef",
    "GetTablesResponseTypeDef",
    "GetUnfilteredTableMetadataResponseTypeDef",
    "SearchTablesResponseTypeDef",
    "TableVersionTypeDef",
    "CreateJobRequestRequestTypeDef",
    "JobTypeDef",
    "JobUpdateTypeDef",
    "WorkflowGraphTypeDef",
    "UpdateColumnStatisticsForPartitionResponseTypeDef",
    "UpdateColumnStatisticsForTableResponseTypeDef",
    "BatchUpdatePartitionRequestRequestTypeDef",
    "GetUnfilteredPartitionsMetadataResponseTypeDef",
    "GetTableVersionResponseTypeDef",
    "GetTableVersionsResponseTypeDef",
    "BatchGetJobsResponseTypeDef",
    "GetJobResponseTypeDef",
    "GetJobsResponseTypeDef",
    "UpdateJobRequestRequestTypeDef",
    "WorkflowRunTypeDef",
    "GetWorkflowRunResponseTypeDef",
    "GetWorkflowRunsResponseTypeDef",
    "WorkflowTypeDef",
    "BatchGetWorkflowsResponseTypeDef",
    "GetWorkflowResponseTypeDef",
)

NotificationPropertyTypeDef = TypedDict(
    "NotificationPropertyTypeDef",
    {
        "NotifyDelayAfter": int,
    },
    total=False,
)

AggregateOperationTypeDef = TypedDict(
    "AggregateOperationTypeDef",
    {
        "Column": List[str],
        "AggFunc": AggFunctionType,
    },
)

ApplyMappingTypeDef = TypedDict(
    "ApplyMappingTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Mapping": List["MappingTypeDef"],
    },
)

AuditContextTypeDef = TypedDict(
    "AuditContextTypeDef",
    {
        "AdditionalAuditContext": str,
        "RequestedColumns": Sequence[str],
        "AllColumnsRequested": bool,
    },
    total=False,
)

PartitionValueListTypeDef = TypedDict(
    "PartitionValueListTypeDef",
    {
        "Values": Sequence[str],
    },
)

BasicCatalogTargetTypeDef = TypedDict(
    "BasicCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
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

_RequiredBatchDeleteConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteConnectionRequestRequestTypeDef",
    {
        "ConnectionNameList": Sequence[str],
    },
)
_OptionalBatchDeleteConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteConnectionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class BatchDeleteConnectionRequestRequestTypeDef(
    _RequiredBatchDeleteConnectionRequestRequestTypeDef,
    _OptionalBatchDeleteConnectionRequestRequestTypeDef,
):
    pass


ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredBatchDeleteTableRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TablesToDelete": Sequence[str],
    },
)
_OptionalBatchDeleteTableRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteTableRequestRequestTypeDef",
    {
        "CatalogId": str,
        "TransactionId": str,
    },
    total=False,
)


class BatchDeleteTableRequestRequestTypeDef(
    _RequiredBatchDeleteTableRequestRequestTypeDef, _OptionalBatchDeleteTableRequestRequestTypeDef
):
    pass


_RequiredBatchDeleteTableVersionRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteTableVersionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "VersionIds": Sequence[str],
    },
)
_OptionalBatchDeleteTableVersionRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteTableVersionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class BatchDeleteTableVersionRequestRequestTypeDef(
    _RequiredBatchDeleteTableVersionRequestRequestTypeDef,
    _OptionalBatchDeleteTableVersionRequestRequestTypeDef,
):
    pass


_RequiredBatchGetBlueprintsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetBlueprintsRequestRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)
_OptionalBatchGetBlueprintsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetBlueprintsRequestRequestTypeDef",
    {
        "IncludeBlueprint": bool,
        "IncludeParameterSpec": bool,
    },
    total=False,
)


class BatchGetBlueprintsRequestRequestTypeDef(
    _RequiredBatchGetBlueprintsRequestRequestTypeDef,
    _OptionalBatchGetBlueprintsRequestRequestTypeDef,
):
    pass


BatchGetCrawlersRequestRequestTypeDef = TypedDict(
    "BatchGetCrawlersRequestRequestTypeDef",
    {
        "CrawlerNames": Sequence[str],
    },
)

BatchGetCustomEntityTypesRequestRequestTypeDef = TypedDict(
    "BatchGetCustomEntityTypesRequestRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)

_RequiredCustomEntityTypeTypeDef = TypedDict(
    "_RequiredCustomEntityTypeTypeDef",
    {
        "Name": str,
        "RegexString": str,
    },
)
_OptionalCustomEntityTypeTypeDef = TypedDict(
    "_OptionalCustomEntityTypeTypeDef",
    {
        "ContextWords": List[str],
    },
    total=False,
)


class CustomEntityTypeTypeDef(_RequiredCustomEntityTypeTypeDef, _OptionalCustomEntityTypeTypeDef):
    pass


BatchGetDevEndpointsRequestRequestTypeDef = TypedDict(
    "BatchGetDevEndpointsRequestRequestTypeDef",
    {
        "DevEndpointNames": Sequence[str],
    },
)

DevEndpointTypeDef = TypedDict(
    "DevEndpointTypeDef",
    {
        "EndpointName": str,
        "RoleArn": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
        "YarnEndpointAddress": str,
        "PrivateAddress": str,
        "ZeppelinRemoteSparkInterpreterPort": int,
        "PublicAddress": str,
        "Status": str,
        "WorkerType": WorkerTypeType,
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "NumberOfNodes": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
        "FailureReason": str,
        "LastUpdateStatus": str,
        "CreatedTimestamp": datetime,
        "LastModifiedTimestamp": datetime,
        "PublicKey": str,
        "PublicKeys": List[str],
        "SecurityConfiguration": str,
        "Arguments": Dict[str, str],
    },
    total=False,
)

BatchGetJobsRequestRequestTypeDef = TypedDict(
    "BatchGetJobsRequestRequestTypeDef",
    {
        "JobNames": Sequence[str],
    },
)

BatchGetTriggersRequestRequestTypeDef = TypedDict(
    "BatchGetTriggersRequestRequestTypeDef",
    {
        "TriggerNames": Sequence[str],
    },
)

_RequiredBatchGetWorkflowsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetWorkflowsRequestRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)
_OptionalBatchGetWorkflowsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetWorkflowsRequestRequestTypeDef",
    {
        "IncludeGraph": bool,
    },
    total=False,
)


class BatchGetWorkflowsRequestRequestTypeDef(
    _RequiredBatchGetWorkflowsRequestRequestTypeDef, _OptionalBatchGetWorkflowsRequestRequestTypeDef
):
    pass


BatchStopJobRunRequestRequestTypeDef = TypedDict(
    "BatchStopJobRunRequestRequestTypeDef",
    {
        "JobName": str,
        "JobRunIds": Sequence[str],
    },
)

BatchStopJobRunSuccessfulSubmissionTypeDef = TypedDict(
    "BatchStopJobRunSuccessfulSubmissionTypeDef",
    {
        "JobName": str,
        "JobRunId": str,
    },
    total=False,
)

BinaryColumnStatisticsDataTypeDef = TypedDict(
    "BinaryColumnStatisticsDataTypeDef",
    {
        "MaximumLength": int,
        "AverageLength": float,
        "NumberOfNulls": int,
    },
)

BlueprintDetailsTypeDef = TypedDict(
    "BlueprintDetailsTypeDef",
    {
        "BlueprintName": str,
        "RunId": str,
    },
    total=False,
)

BlueprintRunTypeDef = TypedDict(
    "BlueprintRunTypeDef",
    {
        "BlueprintName": str,
        "RunId": str,
        "WorkflowName": str,
        "State": BlueprintRunStateType,
        "StartedOn": datetime,
        "CompletedOn": datetime,
        "ErrorMessage": str,
        "RollbackErrorMessage": str,
        "Parameters": str,
        "RoleArn": str,
    },
    total=False,
)

LastActiveDefinitionTypeDef = TypedDict(
    "LastActiveDefinitionTypeDef",
    {
        "Description": str,
        "LastModifiedOn": datetime,
        "ParameterSpec": str,
        "BlueprintLocation": str,
        "BlueprintServiceLocation": str,
    },
    total=False,
)

BooleanColumnStatisticsDataTypeDef = TypedDict(
    "BooleanColumnStatisticsDataTypeDef",
    {
        "NumberOfTrues": int,
        "NumberOfFalses": int,
        "NumberOfNulls": int,
    },
)

CancelMLTaskRunRequestRequestTypeDef = TypedDict(
    "CancelMLTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
    },
)

_RequiredCancelStatementRequestRequestTypeDef = TypedDict(
    "_RequiredCancelStatementRequestRequestTypeDef",
    {
        "SessionId": str,
        "Id": int,
    },
)
_OptionalCancelStatementRequestRequestTypeDef = TypedDict(
    "_OptionalCancelStatementRequestRequestTypeDef",
    {
        "RequestOrigin": str,
    },
    total=False,
)


class CancelStatementRequestRequestTypeDef(
    _RequiredCancelStatementRequestRequestTypeDef, _OptionalCancelStatementRequestRequestTypeDef
):
    pass


CatalogEntryTypeDef = TypedDict(
    "CatalogEntryTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)

CatalogImportStatusTypeDef = TypedDict(
    "CatalogImportStatusTypeDef",
    {
        "ImportCompleted": bool,
        "ImportTime": datetime,
        "ImportedBy": str,
    },
    total=False,
)

KafkaStreamingSourceOptionsTypeDef = TypedDict(
    "KafkaStreamingSourceOptionsTypeDef",
    {
        "BootstrapServers": str,
        "SecurityProtocol": str,
        "ConnectionName": str,
        "TopicName": str,
        "Assign": str,
        "SubscribePattern": str,
        "Classification": str,
        "Delimiter": str,
        "StartingOffsets": str,
        "EndingOffsets": str,
        "PollTimeoutMs": int,
        "NumRetries": int,
        "RetryIntervalMs": int,
        "MaxOffsetsPerTrigger": int,
        "MinPartitions": int,
    },
    total=False,
)

StreamingDataPreviewOptionsTypeDef = TypedDict(
    "StreamingDataPreviewOptionsTypeDef",
    {
        "PollingTime": int,
        "RecordPollingLimit": int,
    },
    total=False,
)

KinesisStreamingSourceOptionsTypeDef = TypedDict(
    "KinesisStreamingSourceOptionsTypeDef",
    {
        "EndpointUrl": str,
        "StreamName": str,
        "Classification": str,
        "Delimiter": str,
        "StartingPosition": StartingPositionType,
        "MaxFetchTimeInMs": int,
        "MaxFetchRecordsPerShard": int,
        "MaxRecordPerRead": int,
        "AddIdleTimeBetweenReads": bool,
        "IdleTimeBetweenReadsInMs": int,
        "DescribeShardInterval": int,
        "NumRetries": int,
        "RetryIntervalMs": int,
        "MaxRetryIntervalMs": int,
        "AvoidEmptyBatches": bool,
        "StreamArn": str,
        "RoleArn": str,
        "RoleSessionName": str,
    },
    total=False,
)

CatalogSchemaChangePolicyTypeDef = TypedDict(
    "CatalogSchemaChangePolicyTypeDef",
    {
        "EnableUpdateCatalog": bool,
        "UpdateBehavior": UpdateCatalogBehaviorType,
    },
    total=False,
)

CatalogSourceTypeDef = TypedDict(
    "CatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

_RequiredCatalogTargetTypeDef = TypedDict(
    "_RequiredCatalogTargetTypeDef",
    {
        "DatabaseName": str,
        "Tables": List[str],
    },
)
_OptionalCatalogTargetTypeDef = TypedDict(
    "_OptionalCatalogTargetTypeDef",
    {
        "ConnectionName": str,
    },
    total=False,
)


class CatalogTargetTypeDef(_RequiredCatalogTargetTypeDef, _OptionalCatalogTargetTypeDef):
    pass


CheckSchemaVersionValidityInputRequestTypeDef = TypedDict(
    "CheckSchemaVersionValidityInputRequestTypeDef",
    {
        "DataFormat": DataFormatType,
        "SchemaDefinition": str,
    },
)

_RequiredCsvClassifierTypeDef = TypedDict(
    "_RequiredCsvClassifierTypeDef",
    {
        "Name": str,
    },
)
_OptionalCsvClassifierTypeDef = TypedDict(
    "_OptionalCsvClassifierTypeDef",
    {
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "Version": int,
        "Delimiter": str,
        "QuoteSymbol": str,
        "ContainsHeader": CsvHeaderOptionType,
        "Header": List[str],
        "DisableValueTrimming": bool,
        "AllowSingleColumn": bool,
    },
    total=False,
)


class CsvClassifierTypeDef(_RequiredCsvClassifierTypeDef, _OptionalCsvClassifierTypeDef):
    pass


_RequiredGrokClassifierTypeDef = TypedDict(
    "_RequiredGrokClassifierTypeDef",
    {
        "Name": str,
        "Classification": str,
        "GrokPattern": str,
    },
)
_OptionalGrokClassifierTypeDef = TypedDict(
    "_OptionalGrokClassifierTypeDef",
    {
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "Version": int,
        "CustomPatterns": str,
    },
    total=False,
)


class GrokClassifierTypeDef(_RequiredGrokClassifierTypeDef, _OptionalGrokClassifierTypeDef):
    pass


_RequiredJsonClassifierTypeDef = TypedDict(
    "_RequiredJsonClassifierTypeDef",
    {
        "Name": str,
        "JsonPath": str,
    },
)
_OptionalJsonClassifierTypeDef = TypedDict(
    "_OptionalJsonClassifierTypeDef",
    {
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "Version": int,
    },
    total=False,
)


class JsonClassifierTypeDef(_RequiredJsonClassifierTypeDef, _OptionalJsonClassifierTypeDef):
    pass


_RequiredXMLClassifierTypeDef = TypedDict(
    "_RequiredXMLClassifierTypeDef",
    {
        "Name": str,
        "Classification": str,
    },
)
_OptionalXMLClassifierTypeDef = TypedDict(
    "_OptionalXMLClassifierTypeDef",
    {
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "Version": int,
        "RowTag": str,
    },
    total=False,
)


class XMLClassifierTypeDef(_RequiredXMLClassifierTypeDef, _OptionalXMLClassifierTypeDef):
    pass


CloudWatchEncryptionTypeDef = TypedDict(
    "CloudWatchEncryptionTypeDef",
    {
        "CloudWatchEncryptionMode": CloudWatchEncryptionModeType,
        "KmsKeyArn": str,
    },
    total=False,
)

_RequiredDropDuplicatesTypeDef = TypedDict(
    "_RequiredDropDuplicatesTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
    },
)
_OptionalDropDuplicatesTypeDef = TypedDict(
    "_OptionalDropDuplicatesTypeDef",
    {
        "Columns": List[List[str]],
    },
    total=False,
)


class DropDuplicatesTypeDef(_RequiredDropDuplicatesTypeDef, _OptionalDropDuplicatesTypeDef):
    pass


DropFieldsTypeDef = TypedDict(
    "DropFieldsTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)

DynamoDBCatalogSourceTypeDef = TypedDict(
    "DynamoDBCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

_RequiredFillMissingValuesTypeDef = TypedDict(
    "_RequiredFillMissingValuesTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ImputedPath": str,
    },
)
_OptionalFillMissingValuesTypeDef = TypedDict(
    "_OptionalFillMissingValuesTypeDef",
    {
        "FilledPath": str,
    },
    total=False,
)


class FillMissingValuesTypeDef(
    _RequiredFillMissingValuesTypeDef, _OptionalFillMissingValuesTypeDef
):
    pass


MergeTypeDef = TypedDict(
    "MergeTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Source": str,
        "PrimaryKeys": List[List[str]],
    },
)

MicrosoftSQLServerCatalogSourceTypeDef = TypedDict(
    "MicrosoftSQLServerCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

MicrosoftSQLServerCatalogTargetTypeDef = TypedDict(
    "MicrosoftSQLServerCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)

MySQLCatalogSourceTypeDef = TypedDict(
    "MySQLCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

MySQLCatalogTargetTypeDef = TypedDict(
    "MySQLCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)

OracleSQLCatalogSourceTypeDef = TypedDict(
    "OracleSQLCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

OracleSQLCatalogTargetTypeDef = TypedDict(
    "OracleSQLCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)

_RequiredPIIDetectionTypeDef = TypedDict(
    "_RequiredPIIDetectionTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "PiiType": PiiTypeType,
        "EntityTypesToDetect": List[str],
    },
)
_OptionalPIIDetectionTypeDef = TypedDict(
    "_OptionalPIIDetectionTypeDef",
    {
        "OutputColumnName": str,
        "SampleFraction": float,
        "ThresholdFraction": float,
        "MaskValue": str,
    },
    total=False,
)


class PIIDetectionTypeDef(_RequiredPIIDetectionTypeDef, _OptionalPIIDetectionTypeDef):
    pass


PostgreSQLCatalogSourceTypeDef = TypedDict(
    "PostgreSQLCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

PostgreSQLCatalogTargetTypeDef = TypedDict(
    "PostgreSQLCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)

_RequiredRedshiftSourceTypeDef = TypedDict(
    "_RequiredRedshiftSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
_OptionalRedshiftSourceTypeDef = TypedDict(
    "_OptionalRedshiftSourceTypeDef",
    {
        "RedshiftTmpDir": str,
        "TmpDirIAMRole": str,
    },
    total=False,
)


class RedshiftSourceTypeDef(_RequiredRedshiftSourceTypeDef, _OptionalRedshiftSourceTypeDef):
    pass


RelationalCatalogSourceTypeDef = TypedDict(
    "RelationalCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)

RenameFieldTypeDef = TypedDict(
    "RenameFieldTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "SourcePath": List[str],
        "TargetPath": List[str],
    },
)

SelectFieldsTypeDef = TypedDict(
    "SelectFieldsTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)

SelectFromCollectionTypeDef = TypedDict(
    "SelectFromCollectionTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Index": int,
    },
)

_RequiredSpigotTypeDef = TypedDict(
    "_RequiredSpigotTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
    },
)
_OptionalSpigotTypeDef = TypedDict(
    "_OptionalSpigotTypeDef",
    {
        "Topk": int,
        "Prob": float,
    },
    total=False,
)


class SpigotTypeDef(_RequiredSpigotTypeDef, _OptionalSpigotTypeDef):
    pass


SplitFieldsTypeDef = TypedDict(
    "SplitFieldsTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)

UnionTypeDef = TypedDict(
    "UnionTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "UnionType": UnionTypeType,
    },
)

_RequiredCodeGenEdgeTypeDef = TypedDict(
    "_RequiredCodeGenEdgeTypeDef",
    {
        "Source": str,
        "Target": str,
    },
)
_OptionalCodeGenEdgeTypeDef = TypedDict(
    "_OptionalCodeGenEdgeTypeDef",
    {
        "TargetParameter": str,
    },
    total=False,
)


class CodeGenEdgeTypeDef(_RequiredCodeGenEdgeTypeDef, _OptionalCodeGenEdgeTypeDef):
    pass


_RequiredCodeGenNodeArgTypeDef = TypedDict(
    "_RequiredCodeGenNodeArgTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
_OptionalCodeGenNodeArgTypeDef = TypedDict(
    "_OptionalCodeGenNodeArgTypeDef",
    {
        "Param": bool,
    },
    total=False,
)


class CodeGenNodeArgTypeDef(_RequiredCodeGenNodeArgTypeDef, _OptionalCodeGenNodeArgTypeDef):
    pass


ColumnImportanceTypeDef = TypedDict(
    "ColumnImportanceTypeDef",
    {
        "ColumnName": str,
        "Importance": float,
    },
    total=False,
)

ColumnRowFilterTypeDef = TypedDict(
    "ColumnRowFilterTypeDef",
    {
        "ColumnName": str,
        "RowFilterExpression": str,
    },
    total=False,
)

_RequiredDateColumnStatisticsDataTypeDef = TypedDict(
    "_RequiredDateColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
    },
)
_OptionalDateColumnStatisticsDataTypeDef = TypedDict(
    "_OptionalDateColumnStatisticsDataTypeDef",
    {
        "MinimumValue": datetime,
        "MaximumValue": datetime,
    },
    total=False,
)


class DateColumnStatisticsDataTypeDef(
    _RequiredDateColumnStatisticsDataTypeDef, _OptionalDateColumnStatisticsDataTypeDef
):
    pass


_RequiredDoubleColumnStatisticsDataTypeDef = TypedDict(
    "_RequiredDoubleColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
    },
)
_OptionalDoubleColumnStatisticsDataTypeDef = TypedDict(
    "_OptionalDoubleColumnStatisticsDataTypeDef",
    {
        "MinimumValue": float,
        "MaximumValue": float,
    },
    total=False,
)


class DoubleColumnStatisticsDataTypeDef(
    _RequiredDoubleColumnStatisticsDataTypeDef, _OptionalDoubleColumnStatisticsDataTypeDef
):
    pass


_RequiredLongColumnStatisticsDataTypeDef = TypedDict(
    "_RequiredLongColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
    },
)
_OptionalLongColumnStatisticsDataTypeDef = TypedDict(
    "_OptionalLongColumnStatisticsDataTypeDef",
    {
        "MinimumValue": int,
        "MaximumValue": int,
    },
    total=False,
)


class LongColumnStatisticsDataTypeDef(
    _RequiredLongColumnStatisticsDataTypeDef, _OptionalLongColumnStatisticsDataTypeDef
):
    pass


StringColumnStatisticsDataTypeDef = TypedDict(
    "StringColumnStatisticsDataTypeDef",
    {
        "MaximumLength": int,
        "AverageLength": float,
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
    },
)

_RequiredColumnTypeDef = TypedDict(
    "_RequiredColumnTypeDef",
    {
        "Name": str,
    },
)
_OptionalColumnTypeDef = TypedDict(
    "_OptionalColumnTypeDef",
    {
        "Type": str,
        "Comment": str,
        "Parameters": Mapping[str, str],
    },
    total=False,
)


class ColumnTypeDef(_RequiredColumnTypeDef, _OptionalColumnTypeDef):
    pass


ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "LogicalOperator": Literal["EQUALS"],
        "JobName": str,
        "State": JobRunStateType,
        "CrawlerName": str,
        "CrawlState": CrawlStateType,
    },
    total=False,
)

ConfusionMatrixTypeDef = TypedDict(
    "ConfusionMatrixTypeDef",
    {
        "NumTruePositives": int,
        "NumFalsePositives": int,
        "NumTrueNegatives": int,
        "NumFalseNegatives": int,
    },
    total=False,
)

PhysicalConnectionRequirementsTypeDef = TypedDict(
    "PhysicalConnectionRequirementsTypeDef",
    {
        "SubnetId": str,
        "SecurityGroupIdList": Sequence[str],
        "AvailabilityZone": str,
    },
    total=False,
)

_RequiredConnectionPasswordEncryptionTypeDef = TypedDict(
    "_RequiredConnectionPasswordEncryptionTypeDef",
    {
        "ReturnConnectionPasswordEncrypted": bool,
    },
)
_OptionalConnectionPasswordEncryptionTypeDef = TypedDict(
    "_OptionalConnectionPasswordEncryptionTypeDef",
    {
        "AwsKmsKeyId": str,
    },
    total=False,
)


class ConnectionPasswordEncryptionTypeDef(
    _RequiredConnectionPasswordEncryptionTypeDef, _OptionalConnectionPasswordEncryptionTypeDef
):
    pass


ConnectionsListTypeDef = TypedDict(
    "ConnectionsListTypeDef",
    {
        "Connections": List[str],
    },
    total=False,
)

CrawlTypeDef = TypedDict(
    "CrawlTypeDef",
    {
        "State": CrawlStateType,
        "StartedOn": datetime,
        "CompletedOn": datetime,
        "ErrorMessage": str,
        "LogGroup": str,
        "LogStream": str,
    },
    total=False,
)

CrawlerMetricsTypeDef = TypedDict(
    "CrawlerMetricsTypeDef",
    {
        "CrawlerName": str,
        "TimeLeftSeconds": float,
        "StillEstimating": bool,
        "LastRuntimeSeconds": float,
        "MedianRuntimeSeconds": float,
        "TablesCreated": int,
        "TablesUpdated": int,
        "TablesDeleted": int,
    },
    total=False,
)

DeltaTargetTypeDef = TypedDict(
    "DeltaTargetTypeDef",
    {
        "DeltaTables": List[str],
        "ConnectionName": str,
        "WriteManifest": bool,
    },
    total=False,
)

DynamoDBTargetTypeDef = TypedDict(
    "DynamoDBTargetTypeDef",
    {
        "Path": str,
        "scanAll": bool,
        "scanRate": float,
    },
    total=False,
)

JdbcTargetTypeDef = TypedDict(
    "JdbcTargetTypeDef",
    {
        "ConnectionName": str,
        "Path": str,
        "Exclusions": List[str],
    },
    total=False,
)

MongoDBTargetTypeDef = TypedDict(
    "MongoDBTargetTypeDef",
    {
        "ConnectionName": str,
        "Path": str,
        "ScanAll": bool,
    },
    total=False,
)

S3TargetTypeDef = TypedDict(
    "S3TargetTypeDef",
    {
        "Path": str,
        "Exclusions": List[str],
        "ConnectionName": str,
        "SampleSize": int,
        "EventQueueArn": str,
        "DlqEventQueueArn": str,
    },
    total=False,
)

LakeFormationConfigurationTypeDef = TypedDict(
    "LakeFormationConfigurationTypeDef",
    {
        "UseLakeFormationCredentials": bool,
        "AccountId": str,
    },
    total=False,
)

LastCrawlInfoTypeDef = TypedDict(
    "LastCrawlInfoTypeDef",
    {
        "Status": LastCrawlStatusType,
        "ErrorMessage": str,
        "LogGroup": str,
        "LogStream": str,
        "MessagePrefix": str,
        "StartTime": datetime,
    },
    total=False,
)

LineageConfigurationTypeDef = TypedDict(
    "LineageConfigurationTypeDef",
    {
        "CrawlerLineageSettings": CrawlerLineageSettingsType,
    },
    total=False,
)

RecrawlPolicyTypeDef = TypedDict(
    "RecrawlPolicyTypeDef",
    {
        "RecrawlBehavior": RecrawlBehaviorType,
    },
    total=False,
)

ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {
        "ScheduleExpression": str,
        "State": ScheduleStateType,
    },
    total=False,
)

SchemaChangePolicyTypeDef = TypedDict(
    "SchemaChangePolicyTypeDef",
    {
        "UpdateBehavior": UpdateBehaviorType,
        "DeleteBehavior": DeleteBehaviorType,
    },
    total=False,
)

_RequiredCreateBlueprintRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBlueprintRequestRequestTypeDef",
    {
        "Name": str,
        "BlueprintLocation": str,
    },
)
_OptionalCreateBlueprintRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBlueprintRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateBlueprintRequestRequestTypeDef(
    _RequiredCreateBlueprintRequestRequestTypeDef, _OptionalCreateBlueprintRequestRequestTypeDef
):
    pass


_RequiredCreateCsvClassifierRequestTypeDef = TypedDict(
    "_RequiredCreateCsvClassifierRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateCsvClassifierRequestTypeDef = TypedDict(
    "_OptionalCreateCsvClassifierRequestTypeDef",
    {
        "Delimiter": str,
        "QuoteSymbol": str,
        "ContainsHeader": CsvHeaderOptionType,
        "Header": Sequence[str],
        "DisableValueTrimming": bool,
        "AllowSingleColumn": bool,
    },
    total=False,
)


class CreateCsvClassifierRequestTypeDef(
    _RequiredCreateCsvClassifierRequestTypeDef, _OptionalCreateCsvClassifierRequestTypeDef
):
    pass


_RequiredCreateGrokClassifierRequestTypeDef = TypedDict(
    "_RequiredCreateGrokClassifierRequestTypeDef",
    {
        "Classification": str,
        "Name": str,
        "GrokPattern": str,
    },
)
_OptionalCreateGrokClassifierRequestTypeDef = TypedDict(
    "_OptionalCreateGrokClassifierRequestTypeDef",
    {
        "CustomPatterns": str,
    },
    total=False,
)


class CreateGrokClassifierRequestTypeDef(
    _RequiredCreateGrokClassifierRequestTypeDef, _OptionalCreateGrokClassifierRequestTypeDef
):
    pass


CreateJsonClassifierRequestTypeDef = TypedDict(
    "CreateJsonClassifierRequestTypeDef",
    {
        "Name": str,
        "JsonPath": str,
    },
)

_RequiredCreateXMLClassifierRequestTypeDef = TypedDict(
    "_RequiredCreateXMLClassifierRequestTypeDef",
    {
        "Classification": str,
        "Name": str,
    },
)
_OptionalCreateXMLClassifierRequestTypeDef = TypedDict(
    "_OptionalCreateXMLClassifierRequestTypeDef",
    {
        "RowTag": str,
    },
    total=False,
)


class CreateXMLClassifierRequestTypeDef(
    _RequiredCreateXMLClassifierRequestTypeDef, _OptionalCreateXMLClassifierRequestTypeDef
):
    pass


_RequiredCreateCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCustomEntityTypeRequestRequestTypeDef",
    {
        "Name": str,
        "RegexString": str,
    },
)
_OptionalCreateCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCustomEntityTypeRequestRequestTypeDef",
    {
        "ContextWords": Sequence[str],
    },
    total=False,
)


class CreateCustomEntityTypeRequestRequestTypeDef(
    _RequiredCreateCustomEntityTypeRequestRequestTypeDef,
    _OptionalCreateCustomEntityTypeRequestRequestTypeDef,
):
    pass


_RequiredCreateDevEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
        "RoleArn": str,
    },
)
_OptionalCreateDevEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDevEndpointRequestRequestTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetId": str,
        "PublicKey": str,
        "PublicKeys": Sequence[str],
        "NumberOfNodes": int,
        "WorkerType": WorkerTypeType,
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
        "SecurityConfiguration": str,
        "Tags": Mapping[str, str],
        "Arguments": Mapping[str, str],
    },
    total=False,
)


class CreateDevEndpointRequestRequestTypeDef(
    _RequiredCreateDevEndpointRequestRequestTypeDef, _OptionalCreateDevEndpointRequestRequestTypeDef
):
    pass


ExecutionPropertyTypeDef = TypedDict(
    "ExecutionPropertyTypeDef",
    {
        "MaxConcurrentRuns": int,
    },
    total=False,
)

JobCommandTypeDef = TypedDict(
    "JobCommandTypeDef",
    {
        "Name": str,
        "ScriptLocation": str,
        "PythonVersion": str,
    },
    total=False,
)

_RequiredGlueTableTypeDef = TypedDict(
    "_RequiredGlueTableTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGlueTableTypeDef = TypedDict(
    "_OptionalGlueTableTypeDef",
    {
        "CatalogId": str,
        "ConnectionName": str,
    },
    total=False,
)


class GlueTableTypeDef(_RequiredGlueTableTypeDef, _OptionalGlueTableTypeDef):
    pass


PartitionIndexTypeDef = TypedDict(
    "PartitionIndexTypeDef",
    {
        "Keys": Sequence[str],
        "IndexName": str,
    },
)

_RequiredCreateRegistryInputRequestTypeDef = TypedDict(
    "_RequiredCreateRegistryInputRequestTypeDef",
    {
        "RegistryName": str,
    },
)
_OptionalCreateRegistryInputRequestTypeDef = TypedDict(
    "_OptionalCreateRegistryInputRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateRegistryInputRequestTypeDef(
    _RequiredCreateRegistryInputRequestTypeDef, _OptionalCreateRegistryInputRequestTypeDef
):
    pass


RegistryIdTypeDef = TypedDict(
    "RegistryIdTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
    },
    total=False,
)

SessionCommandTypeDef = TypedDict(
    "SessionCommandTypeDef",
    {
        "Name": str,
        "PythonVersion": str,
    },
    total=False,
)

_RequiredEventBatchingConditionTypeDef = TypedDict(
    "_RequiredEventBatchingConditionTypeDef",
    {
        "BatchSize": int,
    },
)
_OptionalEventBatchingConditionTypeDef = TypedDict(
    "_OptionalEventBatchingConditionTypeDef",
    {
        "BatchWindow": int,
    },
    total=False,
)


class EventBatchingConditionTypeDef(
    _RequiredEventBatchingConditionTypeDef, _OptionalEventBatchingConditionTypeDef
):
    pass


_RequiredCreateWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkflowRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkflowRequestRequestTypeDef",
    {
        "Description": str,
        "DefaultRunProperties": Mapping[str, str],
        "Tags": Mapping[str, str],
        "MaxConcurrentRuns": int,
    },
    total=False,
)


class CreateWorkflowRequestRequestTypeDef(
    _RequiredCreateWorkflowRequestRequestTypeDef, _OptionalCreateWorkflowRequestRequestTypeDef
):
    pass


_RequiredEncryptionAtRestTypeDef = TypedDict(
    "_RequiredEncryptionAtRestTypeDef",
    {
        "CatalogEncryptionMode": CatalogEncryptionModeType,
    },
)
_OptionalEncryptionAtRestTypeDef = TypedDict(
    "_OptionalEncryptionAtRestTypeDef",
    {
        "SseAwsKmsKeyId": str,
    },
    total=False,
)


class EncryptionAtRestTypeDef(_RequiredEncryptionAtRestTypeDef, _OptionalEncryptionAtRestTypeDef):
    pass


DataLakePrincipalTypeDef = TypedDict(
    "DataLakePrincipalTypeDef",
    {
        "DataLakePrincipalIdentifier": str,
    },
    total=False,
)

DatabaseIdentifierTypeDef = TypedDict(
    "DatabaseIdentifierTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
    },
    total=False,
)

DatatypeTypeDef = TypedDict(
    "DatatypeTypeDef",
    {
        "Id": str,
        "Label": str,
    },
)

DecimalNumberTypeDef = TypedDict(
    "DecimalNumberTypeDef",
    {
        "UnscaledValue": bytes,
        "Scale": int,
    },
)

DeleteBlueprintRequestRequestTypeDef = TypedDict(
    "DeleteBlueprintRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteClassifierRequestRequestTypeDef = TypedDict(
    "DeleteClassifierRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDeleteColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "ColumnName": str,
    },
)
_OptionalDeleteColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeleteColumnStatisticsForPartitionRequestRequestTypeDef(
    _RequiredDeleteColumnStatisticsForPartitionRequestRequestTypeDef,
    _OptionalDeleteColumnStatisticsForPartitionRequestRequestTypeDef,
):
    pass


_RequiredDeleteColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteColumnStatisticsForTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "ColumnName": str,
    },
)
_OptionalDeleteColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteColumnStatisticsForTableRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeleteColumnStatisticsForTableRequestRequestTypeDef(
    _RequiredDeleteColumnStatisticsForTableRequestRequestTypeDef,
    _OptionalDeleteColumnStatisticsForTableRequestRequestTypeDef,
):
    pass


_RequiredDeleteConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteConnectionRequestRequestTypeDef",
    {
        "ConnectionName": str,
    },
)
_OptionalDeleteConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteConnectionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeleteConnectionRequestRequestTypeDef(
    _RequiredDeleteConnectionRequestRequestTypeDef, _OptionalDeleteConnectionRequestRequestTypeDef
):
    pass


DeleteCrawlerRequestRequestTypeDef = TypedDict(
    "DeleteCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "DeleteCustomEntityTypeRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDeleteDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDatabaseRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDeleteDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDatabaseRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeleteDatabaseRequestRequestTypeDef(
    _RequiredDeleteDatabaseRequestRequestTypeDef, _OptionalDeleteDatabaseRequestRequestTypeDef
):
    pass


DeleteDevEndpointRequestRequestTypeDef = TypedDict(
    "DeleteDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
    },
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
)

DeleteMLTransformRequestRequestTypeDef = TypedDict(
    "DeleteMLTransformRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)

_RequiredDeletePartitionIndexRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePartitionIndexRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "IndexName": str,
    },
)
_OptionalDeletePartitionIndexRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePartitionIndexRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeletePartitionIndexRequestRequestTypeDef(
    _RequiredDeletePartitionIndexRequestRequestTypeDef,
    _OptionalDeletePartitionIndexRequestRequestTypeDef,
):
    pass


_RequiredDeletePartitionRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
    },
)
_OptionalDeletePartitionRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeletePartitionRequestRequestTypeDef(
    _RequiredDeletePartitionRequestRequestTypeDef, _OptionalDeletePartitionRequestRequestTypeDef
):
    pass


DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "PolicyHashCondition": str,
        "ResourceArn": str,
    },
    total=False,
)

SchemaIdTypeDef = TypedDict(
    "SchemaIdTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
    },
    total=False,
)

DeleteSecurityConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteSecurityConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDeleteSessionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSessionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteSessionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSessionRequestRequestTypeDef",
    {
        "RequestOrigin": str,
    },
    total=False,
)


class DeleteSessionRequestRequestTypeDef(
    _RequiredDeleteSessionRequestRequestTypeDef, _OptionalDeleteSessionRequestRequestTypeDef
):
    pass


_RequiredDeleteTableRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "Name": str,
    },
)
_OptionalDeleteTableRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTableRequestRequestTypeDef",
    {
        "CatalogId": str,
        "TransactionId": str,
    },
    total=False,
)


class DeleteTableRequestRequestTypeDef(
    _RequiredDeleteTableRequestRequestTypeDef, _OptionalDeleteTableRequestRequestTypeDef
):
    pass


_RequiredDeleteTableVersionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTableVersionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "VersionId": str,
    },
)
_OptionalDeleteTableVersionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTableVersionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeleteTableVersionRequestRequestTypeDef(
    _RequiredDeleteTableVersionRequestRequestTypeDef,
    _OptionalDeleteTableVersionRequestRequestTypeDef,
):
    pass


DeleteTriggerRequestRequestTypeDef = TypedDict(
    "DeleteTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDeleteUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionName": str,
    },
)
_OptionalDeleteUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteUserDefinedFunctionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class DeleteUserDefinedFunctionRequestRequestTypeDef(
    _RequiredDeleteUserDefinedFunctionRequestRequestTypeDef,
    _OptionalDeleteUserDefinedFunctionRequestRequestTypeDef,
):
    pass


DeleteWorkflowRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DevEndpointCustomLibrariesTypeDef = TypedDict(
    "DevEndpointCustomLibrariesTypeDef",
    {
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
    },
    total=False,
)

DirectSchemaChangePolicyTypeDef = TypedDict(
    "DirectSchemaChangePolicyTypeDef",
    {
        "EnableUpdateCatalog": bool,
        "UpdateBehavior": UpdateCatalogBehaviorType,
        "Table": str,
        "Database": str,
    },
    total=False,
)

NullCheckBoxListTypeDef = TypedDict(
    "NullCheckBoxListTypeDef",
    {
        "IsEmpty": bool,
        "IsNullString": bool,
        "IsNegOne": bool,
    },
    total=False,
)

EdgeTypeDef = TypedDict(
    "EdgeTypeDef",
    {
        "SourceId": str,
        "DestinationId": str,
    },
    total=False,
)

JobBookmarksEncryptionTypeDef = TypedDict(
    "JobBookmarksEncryptionTypeDef",
    {
        "JobBookmarksEncryptionMode": JobBookmarksEncryptionModeType,
        "KmsKeyArn": str,
    },
    total=False,
)

S3EncryptionTypeDef = TypedDict(
    "S3EncryptionTypeDef",
    {
        "S3EncryptionMode": S3EncryptionModeType,
        "KmsKeyArn": str,
    },
    total=False,
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

ExportLabelsTaskRunPropertiesTypeDef = TypedDict(
    "ExportLabelsTaskRunPropertiesTypeDef",
    {
        "OutputS3Path": str,
    },
    total=False,
)

FilterValueTypeDef = TypedDict(
    "FilterValueTypeDef",
    {
        "Type": FilterValueTypeType,
        "Value": List[str],
    },
)

FindMatchesParametersTypeDef = TypedDict(
    "FindMatchesParametersTypeDef",
    {
        "PrimaryKeyColumnName": str,
        "PrecisionRecallTradeoff": float,
        "AccuracyCostTradeoff": float,
        "EnforceProvidedLabels": bool,
    },
    total=False,
)

FindMatchesTaskRunPropertiesTypeDef = TypedDict(
    "FindMatchesTaskRunPropertiesTypeDef",
    {
        "JobId": str,
        "JobName": str,
        "JobRunId": str,
    },
    total=False,
)

_RequiredGetBlueprintRequestRequestTypeDef = TypedDict(
    "_RequiredGetBlueprintRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetBlueprintRequestRequestTypeDef = TypedDict(
    "_OptionalGetBlueprintRequestRequestTypeDef",
    {
        "IncludeBlueprint": bool,
        "IncludeParameterSpec": bool,
    },
    total=False,
)


class GetBlueprintRequestRequestTypeDef(
    _RequiredGetBlueprintRequestRequestTypeDef, _OptionalGetBlueprintRequestRequestTypeDef
):
    pass


GetBlueprintRunRequestRequestTypeDef = TypedDict(
    "GetBlueprintRunRequestRequestTypeDef",
    {
        "BlueprintName": str,
        "RunId": str,
    },
)

_RequiredGetBlueprintRunsRequestRequestTypeDef = TypedDict(
    "_RequiredGetBlueprintRunsRequestRequestTypeDef",
    {
        "BlueprintName": str,
    },
)
_OptionalGetBlueprintRunsRequestRequestTypeDef = TypedDict(
    "_OptionalGetBlueprintRunsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetBlueprintRunsRequestRequestTypeDef(
    _RequiredGetBlueprintRunsRequestRequestTypeDef, _OptionalGetBlueprintRunsRequestRequestTypeDef
):
    pass


GetCatalogImportStatusRequestRequestTypeDef = TypedDict(
    "GetCatalogImportStatusRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

GetClassifierRequestRequestTypeDef = TypedDict(
    "GetClassifierRequestRequestTypeDef",
    {
        "Name": str,
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

GetClassifiersRequestRequestTypeDef = TypedDict(
    "GetClassifiersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredGetColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "_RequiredGetColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "ColumnNames": Sequence[str],
    },
)
_OptionalGetColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "_OptionalGetColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class GetColumnStatisticsForPartitionRequestRequestTypeDef(
    _RequiredGetColumnStatisticsForPartitionRequestRequestTypeDef,
    _OptionalGetColumnStatisticsForPartitionRequestRequestTypeDef,
):
    pass


_RequiredGetColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "_RequiredGetColumnStatisticsForTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "ColumnNames": Sequence[str],
    },
)
_OptionalGetColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "_OptionalGetColumnStatisticsForTableRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class GetColumnStatisticsForTableRequestRequestTypeDef(
    _RequiredGetColumnStatisticsForTableRequestRequestTypeDef,
    _OptionalGetColumnStatisticsForTableRequestRequestTypeDef,
):
    pass


_RequiredGetConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetConnectionRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetConnectionRequestRequestTypeDef",
    {
        "CatalogId": str,
        "HidePassword": bool,
    },
    total=False,
)


class GetConnectionRequestRequestTypeDef(
    _RequiredGetConnectionRequestRequestTypeDef, _OptionalGetConnectionRequestRequestTypeDef
):
    pass


GetConnectionsFilterTypeDef = TypedDict(
    "GetConnectionsFilterTypeDef",
    {
        "MatchCriteria": Sequence[str],
        "ConnectionType": ConnectionTypeType,
    },
    total=False,
)

GetCrawlerMetricsRequestRequestTypeDef = TypedDict(
    "GetCrawlerMetricsRequestRequestTypeDef",
    {
        "CrawlerNameList": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

GetCrawlerRequestRequestTypeDef = TypedDict(
    "GetCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetCrawlersRequestRequestTypeDef = TypedDict(
    "GetCrawlersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

GetCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "GetCustomEntityTypeRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetDataCatalogEncryptionSettingsRequestRequestTypeDef = TypedDict(
    "GetDataCatalogEncryptionSettingsRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

_RequiredGetDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredGetDatabaseRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalGetDatabaseRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class GetDatabaseRequestRequestTypeDef(
    _RequiredGetDatabaseRequestRequestTypeDef, _OptionalGetDatabaseRequestRequestTypeDef
):
    pass


GetDatabasesRequestRequestTypeDef = TypedDict(
    "GetDatabasesRequestRequestTypeDef",
    {
        "CatalogId": str,
        "NextToken": str,
        "MaxResults": int,
        "ResourceShareType": ResourceShareTypeType,
    },
    total=False,
)

GetDataflowGraphRequestRequestTypeDef = TypedDict(
    "GetDataflowGraphRequestRequestTypeDef",
    {
        "PythonScript": str,
    },
    total=False,
)

GetDevEndpointRequestRequestTypeDef = TypedDict(
    "GetDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
    },
)

GetDevEndpointsRequestRequestTypeDef = TypedDict(
    "GetDevEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredGetJobBookmarkRequestRequestTypeDef = TypedDict(
    "_RequiredGetJobBookmarkRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
_OptionalGetJobBookmarkRequestRequestTypeDef = TypedDict(
    "_OptionalGetJobBookmarkRequestRequestTypeDef",
    {
        "RunId": str,
    },
    total=False,
)


class GetJobBookmarkRequestRequestTypeDef(
    _RequiredGetJobBookmarkRequestRequestTypeDef, _OptionalGetJobBookmarkRequestRequestTypeDef
):
    pass


JobBookmarkEntryTypeDef = TypedDict(
    "JobBookmarkEntryTypeDef",
    {
        "JobName": str,
        "Version": int,
        "Run": int,
        "Attempt": int,
        "PreviousRunId": str,
        "RunId": str,
        "JobBookmark": str,
    },
    total=False,
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
)

_RequiredGetJobRunRequestRequestTypeDef = TypedDict(
    "_RequiredGetJobRunRequestRequestTypeDef",
    {
        "JobName": str,
        "RunId": str,
    },
)
_OptionalGetJobRunRequestRequestTypeDef = TypedDict(
    "_OptionalGetJobRunRequestRequestTypeDef",
    {
        "PredecessorsIncluded": bool,
    },
    total=False,
)


class GetJobRunRequestRequestTypeDef(
    _RequiredGetJobRunRequestRequestTypeDef, _OptionalGetJobRunRequestRequestTypeDef
):
    pass


_RequiredGetJobRunsRequestRequestTypeDef = TypedDict(
    "_RequiredGetJobRunsRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
_OptionalGetJobRunsRequestRequestTypeDef = TypedDict(
    "_OptionalGetJobRunsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetJobRunsRequestRequestTypeDef(
    _RequiredGetJobRunsRequestRequestTypeDef, _OptionalGetJobRunsRequestRequestTypeDef
):
    pass


GetJobsRequestRequestTypeDef = TypedDict(
    "GetJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetMLTaskRunRequestRequestTypeDef = TypedDict(
    "GetMLTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
    },
)

TaskRunFilterCriteriaTypeDef = TypedDict(
    "TaskRunFilterCriteriaTypeDef",
    {
        "TaskRunType": TaskTypeType,
        "Status": TaskStatusTypeType,
        "StartedBefore": Union[datetime, str],
        "StartedAfter": Union[datetime, str],
    },
    total=False,
)

TaskRunSortCriteriaTypeDef = TypedDict(
    "TaskRunSortCriteriaTypeDef",
    {
        "Column": TaskRunSortColumnTypeType,
        "SortDirection": SortDirectionTypeType,
    },
)

GetMLTransformRequestRequestTypeDef = TypedDict(
    "GetMLTransformRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)

SchemaColumnTypeDef = TypedDict(
    "SchemaColumnTypeDef",
    {
        "Name": str,
        "DataType": str,
    },
    total=False,
)

TransformSortCriteriaTypeDef = TypedDict(
    "TransformSortCriteriaTypeDef",
    {
        "Column": TransformSortColumnTypeType,
        "SortDirection": SortDirectionTypeType,
    },
)

MappingEntryTypeDef = TypedDict(
    "MappingEntryTypeDef",
    {
        "SourceTable": str,
        "SourcePath": str,
        "SourceType": str,
        "TargetTable": str,
        "TargetPath": str,
        "TargetType": str,
    },
    total=False,
)

_RequiredGetPartitionIndexesRequestRequestTypeDef = TypedDict(
    "_RequiredGetPartitionIndexesRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetPartitionIndexesRequestRequestTypeDef = TypedDict(
    "_OptionalGetPartitionIndexesRequestRequestTypeDef",
    {
        "CatalogId": str,
        "NextToken": str,
    },
    total=False,
)


class GetPartitionIndexesRequestRequestTypeDef(
    _RequiredGetPartitionIndexesRequestRequestTypeDef,
    _OptionalGetPartitionIndexesRequestRequestTypeDef,
):
    pass


_RequiredGetPartitionRequestRequestTypeDef = TypedDict(
    "_RequiredGetPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
    },
)
_OptionalGetPartitionRequestRequestTypeDef = TypedDict(
    "_OptionalGetPartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class GetPartitionRequestRequestTypeDef(
    _RequiredGetPartitionRequestRequestTypeDef, _OptionalGetPartitionRequestRequestTypeDef
):
    pass


SegmentTypeDef = TypedDict(
    "SegmentTypeDef",
    {
        "SegmentNumber": int,
        "TotalSegments": int,
    },
)

GetResourcePoliciesRequestRequestTypeDef = TypedDict(
    "GetResourcePoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GluePolicyTypeDef = TypedDict(
    "GluePolicyTypeDef",
    {
        "PolicyInJson": str,
        "PolicyHash": str,
        "CreateTime": datetime,
        "UpdateTime": datetime,
    },
    total=False,
)

GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
    total=False,
)

SchemaVersionNumberTypeDef = TypedDict(
    "SchemaVersionNumberTypeDef",
    {
        "LatestVersion": bool,
        "VersionNumber": int,
    },
    total=False,
)

GetSecurityConfigurationRequestRequestTypeDef = TypedDict(
    "GetSecurityConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetSecurityConfigurationsRequestRequestTypeDef = TypedDict(
    "GetSecurityConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredGetSessionRequestRequestTypeDef = TypedDict(
    "_RequiredGetSessionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalGetSessionRequestRequestTypeDef = TypedDict(
    "_OptionalGetSessionRequestRequestTypeDef",
    {
        "RequestOrigin": str,
    },
    total=False,
)


class GetSessionRequestRequestTypeDef(
    _RequiredGetSessionRequestRequestTypeDef, _OptionalGetSessionRequestRequestTypeDef
):
    pass


_RequiredGetStatementRequestRequestTypeDef = TypedDict(
    "_RequiredGetStatementRequestRequestTypeDef",
    {
        "SessionId": str,
        "Id": int,
    },
)
_OptionalGetStatementRequestRequestTypeDef = TypedDict(
    "_OptionalGetStatementRequestRequestTypeDef",
    {
        "RequestOrigin": str,
    },
    total=False,
)


class GetStatementRequestRequestTypeDef(
    _RequiredGetStatementRequestRequestTypeDef, _OptionalGetStatementRequestRequestTypeDef
):
    pass


_RequiredGetTableRequestRequestTypeDef = TypedDict(
    "_RequiredGetTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "Name": str,
    },
)
_OptionalGetTableRequestRequestTypeDef = TypedDict(
    "_OptionalGetTableRequestRequestTypeDef",
    {
        "CatalogId": str,
        "TransactionId": str,
        "QueryAsOfTime": Union[datetime, str],
    },
    total=False,
)


class GetTableRequestRequestTypeDef(
    _RequiredGetTableRequestRequestTypeDef, _OptionalGetTableRequestRequestTypeDef
):
    pass


_RequiredGetTableVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetTableVersionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetTableVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetTableVersionRequestRequestTypeDef",
    {
        "CatalogId": str,
        "VersionId": str,
    },
    total=False,
)


class GetTableVersionRequestRequestTypeDef(
    _RequiredGetTableVersionRequestRequestTypeDef, _OptionalGetTableVersionRequestRequestTypeDef
):
    pass


_RequiredGetTableVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetTableVersionsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetTableVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetTableVersionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetTableVersionsRequestRequestTypeDef(
    _RequiredGetTableVersionsRequestRequestTypeDef, _OptionalGetTableVersionsRequestRequestTypeDef
):
    pass


_RequiredGetTablesRequestRequestTypeDef = TypedDict(
    "_RequiredGetTablesRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)
_OptionalGetTablesRequestRequestTypeDef = TypedDict(
    "_OptionalGetTablesRequestRequestTypeDef",
    {
        "CatalogId": str,
        "Expression": str,
        "NextToken": str,
        "MaxResults": int,
        "TransactionId": str,
        "QueryAsOfTime": Union[datetime, str],
    },
    total=False,
)


class GetTablesRequestRequestTypeDef(
    _RequiredGetTablesRequestRequestTypeDef, _OptionalGetTablesRequestRequestTypeDef
):
    pass


GetTagsRequestRequestTypeDef = TypedDict(
    "GetTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

GetTriggerRequestRequestTypeDef = TypedDict(
    "GetTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetTriggersRequestRequestTypeDef = TypedDict(
    "GetTriggersRequestRequestTypeDef",
    {
        "NextToken": str,
        "DependentJobName": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredGetUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredGetUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionName": str,
    },
)
_OptionalGetUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalGetUserDefinedFunctionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class GetUserDefinedFunctionRequestRequestTypeDef(
    _RequiredGetUserDefinedFunctionRequestRequestTypeDef,
    _OptionalGetUserDefinedFunctionRequestRequestTypeDef,
):
    pass


_RequiredGetUserDefinedFunctionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetUserDefinedFunctionsRequestRequestTypeDef",
    {
        "Pattern": str,
    },
)
_OptionalGetUserDefinedFunctionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetUserDefinedFunctionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetUserDefinedFunctionsRequestRequestTypeDef(
    _RequiredGetUserDefinedFunctionsRequestRequestTypeDef,
    _OptionalGetUserDefinedFunctionsRequestRequestTypeDef,
):
    pass


_RequiredGetWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredGetWorkflowRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalGetWorkflowRequestRequestTypeDef",
    {
        "IncludeGraph": bool,
    },
    total=False,
)


class GetWorkflowRequestRequestTypeDef(
    _RequiredGetWorkflowRequestRequestTypeDef, _OptionalGetWorkflowRequestRequestTypeDef
):
    pass


GetWorkflowRunPropertiesRequestRequestTypeDef = TypedDict(
    "GetWorkflowRunPropertiesRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)

_RequiredGetWorkflowRunRequestRequestTypeDef = TypedDict(
    "_RequiredGetWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)
_OptionalGetWorkflowRunRequestRequestTypeDef = TypedDict(
    "_OptionalGetWorkflowRunRequestRequestTypeDef",
    {
        "IncludeGraph": bool,
    },
    total=False,
)


class GetWorkflowRunRequestRequestTypeDef(
    _RequiredGetWorkflowRunRequestRequestTypeDef, _OptionalGetWorkflowRunRequestRequestTypeDef
):
    pass


_RequiredGetWorkflowRunsRequestRequestTypeDef = TypedDict(
    "_RequiredGetWorkflowRunsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetWorkflowRunsRequestRequestTypeDef = TypedDict(
    "_OptionalGetWorkflowRunsRequestRequestTypeDef",
    {
        "IncludeGraph": bool,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetWorkflowRunsRequestRequestTypeDef(
    _RequiredGetWorkflowRunsRequestRequestTypeDef, _OptionalGetWorkflowRunsRequestRequestTypeDef
):
    pass


_RequiredGlueStudioSchemaColumnTypeDef = TypedDict(
    "_RequiredGlueStudioSchemaColumnTypeDef",
    {
        "Name": str,
    },
)
_OptionalGlueStudioSchemaColumnTypeDef = TypedDict(
    "_OptionalGlueStudioSchemaColumnTypeDef",
    {
        "Type": str,
    },
    total=False,
)


class GlueStudioSchemaColumnTypeDef(
    _RequiredGlueStudioSchemaColumnTypeDef, _OptionalGlueStudioSchemaColumnTypeDef
):
    pass


S3SourceAdditionalOptionsTypeDef = TypedDict(
    "S3SourceAdditionalOptionsTypeDef",
    {
        "BoundedSize": int,
        "BoundedFiles": int,
    },
    total=False,
)

ImportCatalogToGlueRequestRequestTypeDef = TypedDict(
    "ImportCatalogToGlueRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)

ImportLabelsTaskRunPropertiesTypeDef = TypedDict(
    "ImportLabelsTaskRunPropertiesTypeDef",
    {
        "InputS3Path": str,
        "Replace": bool,
    },
    total=False,
)

JDBCConnectorOptionsTypeDef = TypedDict(
    "JDBCConnectorOptionsTypeDef",
    {
        "FilterPredicate": str,
        "PartitionColumn": str,
        "LowerBound": int,
        "UpperBound": int,
        "NumPartitions": int,
        "JobBookmarkKeys": List[str],
        "JobBookmarkKeysSortOrder": str,
        "DataTypeMapping": Dict[JDBCDataTypeType, GlueRecordTypeType],
    },
    total=False,
)

PredecessorTypeDef = TypedDict(
    "PredecessorTypeDef",
    {
        "JobName": str,
        "RunId": str,
    },
    total=False,
)

JoinColumnTypeDef = TypedDict(
    "JoinColumnTypeDef",
    {
        "From": str,
        "Keys": List[List[str]],
    },
)

KeySchemaElementTypeDef = TypedDict(
    "KeySchemaElementTypeDef",
    {
        "Name": str,
        "Type": str,
    },
)

LabelingSetGenerationTaskRunPropertiesTypeDef = TypedDict(
    "LabelingSetGenerationTaskRunPropertiesTypeDef",
    {
        "OutputS3Path": str,
    },
    total=False,
)

ListBlueprintsRequestRequestTypeDef = TypedDict(
    "ListBlueprintsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Tags": Mapping[str, str],
    },
    total=False,
)

ListCrawlersRequestRequestTypeDef = TypedDict(
    "ListCrawlersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

ListCustomEntityTypesRequestRequestTypeDef = TypedDict(
    "ListCustomEntityTypesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDevEndpointsRequestRequestTypeDef = TypedDict(
    "ListDevEndpointsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Tags": Mapping[str, str],
    },
    total=False,
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Tags": Mapping[str, str],
    },
    total=False,
)

ListRegistriesInputRequestTypeDef = TypedDict(
    "ListRegistriesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

RegistryListItemTypeDef = TypedDict(
    "RegistryListItemTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "Description": str,
        "Status": RegistryStatusType,
        "CreatedTime": str,
        "UpdatedTime": str,
    },
    total=False,
)

SchemaVersionListItemTypeDef = TypedDict(
    "SchemaVersionListItemTypeDef",
    {
        "SchemaArn": str,
        "SchemaVersionId": str,
        "VersionNumber": int,
        "Status": SchemaVersionStatusType,
        "CreatedTime": str,
    },
    total=False,
)

SchemaListItemTypeDef = TypedDict(
    "SchemaListItemTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
        "SchemaArn": str,
        "Description": str,
        "SchemaStatus": SchemaStatusType,
        "CreatedTime": str,
        "UpdatedTime": str,
    },
    total=False,
)

ListSessionsRequestRequestTypeDef = TypedDict(
    "ListSessionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Tags": Mapping[str, str],
        "RequestOrigin": str,
    },
    total=False,
)

_RequiredListStatementsRequestRequestTypeDef = TypedDict(
    "_RequiredListStatementsRequestRequestTypeDef",
    {
        "SessionId": str,
    },
)
_OptionalListStatementsRequestRequestTypeDef = TypedDict(
    "_OptionalListStatementsRequestRequestTypeDef",
    {
        "RequestOrigin": str,
        "NextToken": str,
    },
    total=False,
)


class ListStatementsRequestRequestTypeDef(
    _RequiredListStatementsRequestRequestTypeDef, _OptionalListStatementsRequestRequestTypeDef
):
    pass


ListTriggersRequestRequestTypeDef = TypedDict(
    "ListTriggersRequestRequestTypeDef",
    {
        "NextToken": str,
        "DependentJobName": str,
        "MaxResults": int,
        "Tags": Mapping[str, str],
    },
    total=False,
)

ListWorkflowsRequestRequestTypeDef = TypedDict(
    "ListWorkflowsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredMLUserDataEncryptionTypeDef = TypedDict(
    "_RequiredMLUserDataEncryptionTypeDef",
    {
        "MlUserDataEncryptionMode": MLUserDataEncryptionModeStringType,
    },
)
_OptionalMLUserDataEncryptionTypeDef = TypedDict(
    "_OptionalMLUserDataEncryptionTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class MLUserDataEncryptionTypeDef(
    _RequiredMLUserDataEncryptionTypeDef, _OptionalMLUserDataEncryptionTypeDef
):
    pass


MappingTypeDef = TypedDict(
    "MappingTypeDef",
    {
        "ToKey": str,
        "FromPath": List[str],
        "FromType": str,
        "ToType": str,
        "Dropped": bool,
        "Children": List[Dict[str, Any]],
    },
    total=False,
)

OtherMetadataValueListItemTypeDef = TypedDict(
    "OtherMetadataValueListItemTypeDef",
    {
        "MetadataValue": str,
        "CreatedTime": str,
    },
    total=False,
)

MetadataKeyValuePairTypeDef = TypedDict(
    "MetadataKeyValuePairTypeDef",
    {
        "MetadataKey": str,
        "MetadataValue": str,
    },
    total=False,
)

OrderTypeDef = TypedDict(
    "OrderTypeDef",
    {
        "Column": str,
        "SortOrder": int,
    },
)

PropertyPredicateTypeDef = TypedDict(
    "PropertyPredicateTypeDef",
    {
        "Key": str,
        "Value": str,
        "Comparator": ComparatorType,
    },
    total=False,
)

_RequiredPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutResourcePolicyRequestRequestTypeDef",
    {
        "PolicyInJson": str,
    },
)
_OptionalPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "PolicyHashCondition": str,
        "PolicyExistsCondition": ExistConditionType,
        "EnableHybrid": EnableHybridValuesType,
    },
    total=False,
)


class PutResourcePolicyRequestRequestTypeDef(
    _RequiredPutResourcePolicyRequestRequestTypeDef, _OptionalPutResourcePolicyRequestRequestTypeDef
):
    pass


PutWorkflowRunPropertiesRequestRequestTypeDef = TypedDict(
    "PutWorkflowRunPropertiesRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
        "RunProperties": Mapping[str, str],
    },
)

UpsertRedshiftTargetOptionsTypeDef = TypedDict(
    "UpsertRedshiftTargetOptionsTypeDef",
    {
        "TableLocation": str,
        "ConnectionName": str,
        "UpsertKeys": List[str],
    },
    total=False,
)

_RequiredResetJobBookmarkRequestRequestTypeDef = TypedDict(
    "_RequiredResetJobBookmarkRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
_OptionalResetJobBookmarkRequestRequestTypeDef = TypedDict(
    "_OptionalResetJobBookmarkRequestRequestTypeDef",
    {
        "RunId": str,
    },
    total=False,
)


class ResetJobBookmarkRequestRequestTypeDef(
    _RequiredResetJobBookmarkRequestRequestTypeDef, _OptionalResetJobBookmarkRequestRequestTypeDef
):
    pass


ResourceUriTypeDef = TypedDict(
    "ResourceUriTypeDef",
    {
        "ResourceType": ResourceTypeType,
        "Uri": str,
    },
    total=False,
)

ResumeWorkflowRunRequestRequestTypeDef = TypedDict(
    "ResumeWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
        "NodeIds": Sequence[str],
    },
)

_RequiredRunStatementRequestRequestTypeDef = TypedDict(
    "_RequiredRunStatementRequestRequestTypeDef",
    {
        "SessionId": str,
        "Code": str,
    },
)
_OptionalRunStatementRequestRequestTypeDef = TypedDict(
    "_OptionalRunStatementRequestRequestTypeDef",
    {
        "RequestOrigin": str,
    },
    total=False,
)


class RunStatementRequestRequestTypeDef(
    _RequiredRunStatementRequestRequestTypeDef, _OptionalRunStatementRequestRequestTypeDef
):
    pass


S3DirectSourceAdditionalOptionsTypeDef = TypedDict(
    "S3DirectSourceAdditionalOptionsTypeDef",
    {
        "BoundedSize": int,
        "BoundedFiles": int,
        "EnableSamplePath": bool,
        "SamplePath": str,
    },
    total=False,
)

SortCriterionTypeDef = TypedDict(
    "SortCriterionTypeDef",
    {
        "FieldName": str,
        "Sort": SortType,
    },
    total=False,
)

SerDeInfoTypeDef = TypedDict(
    "SerDeInfoTypeDef",
    {
        "Name": str,
        "SerializationLibrary": str,
        "Parameters": Mapping[str, str],
    },
    total=False,
)

SkewedInfoTypeDef = TypedDict(
    "SkewedInfoTypeDef",
    {
        "SkewedColumnNames": Sequence[str],
        "SkewedColumnValues": Sequence[str],
        "SkewedColumnValueLocationMaps": Mapping[str, str],
    },
    total=False,
)

SqlAliasTypeDef = TypedDict(
    "SqlAliasTypeDef",
    {
        "From": str,
        "Alias": str,
    },
)

_RequiredStartBlueprintRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartBlueprintRunRequestRequestTypeDef",
    {
        "BlueprintName": str,
        "RoleArn": str,
    },
)
_OptionalStartBlueprintRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartBlueprintRunRequestRequestTypeDef",
    {
        "Parameters": str,
    },
    total=False,
)


class StartBlueprintRunRequestRequestTypeDef(
    _RequiredStartBlueprintRunRequestRequestTypeDef, _OptionalStartBlueprintRunRequestRequestTypeDef
):
    pass


StartCrawlerRequestRequestTypeDef = TypedDict(
    "StartCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StartCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "StartCrawlerScheduleRequestRequestTypeDef",
    {
        "CrawlerName": str,
    },
)

StartExportLabelsTaskRunRequestRequestTypeDef = TypedDict(
    "StartExportLabelsTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "OutputS3Path": str,
    },
)

_RequiredStartImportLabelsTaskRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartImportLabelsTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "InputS3Path": str,
    },
)
_OptionalStartImportLabelsTaskRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartImportLabelsTaskRunRequestRequestTypeDef",
    {
        "ReplaceAllLabels": bool,
    },
    total=False,
)


class StartImportLabelsTaskRunRequestRequestTypeDef(
    _RequiredStartImportLabelsTaskRunRequestRequestTypeDef,
    _OptionalStartImportLabelsTaskRunRequestRequestTypeDef,
):
    pass


StartMLEvaluationTaskRunRequestRequestTypeDef = TypedDict(
    "StartMLEvaluationTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)

StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef = TypedDict(
    "StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "OutputS3Path": str,
    },
)

StartTriggerRequestRequestTypeDef = TypedDict(
    "StartTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredStartWorkflowRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalStartWorkflowRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartWorkflowRunRequestRequestTypeDef",
    {
        "RunProperties": Mapping[str, str],
    },
    total=False,
)


class StartWorkflowRunRequestRequestTypeDef(
    _RequiredStartWorkflowRunRequestRequestTypeDef, _OptionalStartWorkflowRunRequestRequestTypeDef
):
    pass


StartingEventBatchConditionTypeDef = TypedDict(
    "StartingEventBatchConditionTypeDef",
    {
        "BatchSize": int,
        "BatchWindow": int,
    },
    total=False,
)

StatementOutputDataTypeDef = TypedDict(
    "StatementOutputDataTypeDef",
    {
        "TextPlain": str,
    },
    total=False,
)

StopCrawlerRequestRequestTypeDef = TypedDict(
    "StopCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "StopCrawlerScheduleRequestRequestTypeDef",
    {
        "CrawlerName": str,
    },
)

_RequiredStopSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStopSessionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalStopSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStopSessionRequestRequestTypeDef",
    {
        "RequestOrigin": str,
    },
    total=False,
)


class StopSessionRequestRequestTypeDef(
    _RequiredStopSessionRequestRequestTypeDef, _OptionalStopSessionRequestRequestTypeDef
):
    pass


StopTriggerRequestRequestTypeDef = TypedDict(
    "StopTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopWorkflowRunRequestRequestTypeDef = TypedDict(
    "StopWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)

TableIdentifierTypeDef = TypedDict(
    "TableIdentifierTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "Name": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagsToAdd": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagsToRemove": Sequence[str],
    },
)

_RequiredUpdateBlueprintRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBlueprintRequestRequestTypeDef",
    {
        "Name": str,
        "BlueprintLocation": str,
    },
)
_OptionalUpdateBlueprintRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBlueprintRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateBlueprintRequestRequestTypeDef(
    _RequiredUpdateBlueprintRequestRequestTypeDef, _OptionalUpdateBlueprintRequestRequestTypeDef
):
    pass


_RequiredUpdateCsvClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateCsvClassifierRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateCsvClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateCsvClassifierRequestTypeDef",
    {
        "Delimiter": str,
        "QuoteSymbol": str,
        "ContainsHeader": CsvHeaderOptionType,
        "Header": Sequence[str],
        "DisableValueTrimming": bool,
        "AllowSingleColumn": bool,
    },
    total=False,
)


class UpdateCsvClassifierRequestTypeDef(
    _RequiredUpdateCsvClassifierRequestTypeDef, _OptionalUpdateCsvClassifierRequestTypeDef
):
    pass


_RequiredUpdateGrokClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateGrokClassifierRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateGrokClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateGrokClassifierRequestTypeDef",
    {
        "Classification": str,
        "GrokPattern": str,
        "CustomPatterns": str,
    },
    total=False,
)


class UpdateGrokClassifierRequestTypeDef(
    _RequiredUpdateGrokClassifierRequestTypeDef, _OptionalUpdateGrokClassifierRequestTypeDef
):
    pass


_RequiredUpdateJsonClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateJsonClassifierRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateJsonClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateJsonClassifierRequestTypeDef",
    {
        "JsonPath": str,
    },
    total=False,
)


class UpdateJsonClassifierRequestTypeDef(
    _RequiredUpdateJsonClassifierRequestTypeDef, _OptionalUpdateJsonClassifierRequestTypeDef
):
    pass


_RequiredUpdateXMLClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateXMLClassifierRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateXMLClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateXMLClassifierRequestTypeDef",
    {
        "Classification": str,
        "RowTag": str,
    },
    total=False,
)


class UpdateXMLClassifierRequestTypeDef(
    _RequiredUpdateXMLClassifierRequestTypeDef, _OptionalUpdateXMLClassifierRequestTypeDef
):
    pass


_RequiredUpdateCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCrawlerScheduleRequestRequestTypeDef",
    {
        "CrawlerName": str,
    },
)
_OptionalUpdateCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCrawlerScheduleRequestRequestTypeDef",
    {
        "Schedule": str,
    },
    total=False,
)


class UpdateCrawlerScheduleRequestRequestTypeDef(
    _RequiredUpdateCrawlerScheduleRequestRequestTypeDef,
    _OptionalUpdateCrawlerScheduleRequestRequestTypeDef,
):
    pass


_RequiredUpdateWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkflowRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkflowRequestRequestTypeDef",
    {
        "Description": str,
        "DefaultRunProperties": Mapping[str, str],
        "MaxConcurrentRuns": int,
    },
    total=False,
)


class UpdateWorkflowRequestRequestTypeDef(
    _RequiredUpdateWorkflowRequestRequestTypeDef, _OptionalUpdateWorkflowRequestRequestTypeDef
):
    pass


WorkflowRunStatisticsTypeDef = TypedDict(
    "WorkflowRunStatisticsTypeDef",
    {
        "TotalActions": int,
        "TimeoutActions": int,
        "FailedActions": int,
        "StoppedActions": int,
        "SucceededActions": int,
        "RunningActions": int,
    },
    total=False,
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "JobName": str,
        "Arguments": Dict[str, str],
        "Timeout": int,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "CrawlerName": str,
    },
    total=False,
)

_RequiredStartJobRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartJobRunRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
_OptionalStartJobRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartJobRunRequestRequestTypeDef",
    {
        "JobRunId": str,
        "Arguments": Mapping[str, str],
        "AllocatedCapacity": int,
        "Timeout": int,
        "MaxCapacity": float,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
    },
    total=False,
)


class StartJobRunRequestRequestTypeDef(
    _RequiredStartJobRunRequestRequestTypeDef, _OptionalStartJobRunRequestRequestTypeDef
):
    pass


AggregateTypeDef = TypedDict(
    "AggregateTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Groups": List[List[str]],
        "Aggs": List[AggregateOperationTypeDef],
    },
)

_RequiredGetUnfilteredPartitionMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredGetUnfilteredPartitionMetadataRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
    },
)
_OptionalGetUnfilteredPartitionMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalGetUnfilteredPartitionMetadataRequestRequestTypeDef",
    {
        "AuditContext": AuditContextTypeDef,
    },
    total=False,
)


class GetUnfilteredPartitionMetadataRequestRequestTypeDef(
    _RequiredGetUnfilteredPartitionMetadataRequestRequestTypeDef,
    _OptionalGetUnfilteredPartitionMetadataRequestRequestTypeDef,
):
    pass


_RequiredGetUnfilteredTableMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredGetUnfilteredTableMetadataRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "Name": str,
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
    },
)
_OptionalGetUnfilteredTableMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalGetUnfilteredTableMetadataRequestRequestTypeDef",
    {
        "AuditContext": AuditContextTypeDef,
    },
    total=False,
)


class GetUnfilteredTableMetadataRequestRequestTypeDef(
    _RequiredGetUnfilteredTableMetadataRequestRequestTypeDef,
    _OptionalGetUnfilteredTableMetadataRequestRequestTypeDef,
):
    pass


BackfillErrorTypeDef = TypedDict(
    "BackfillErrorTypeDef",
    {
        "Code": BackfillErrorCodeType,
        "Partitions": List[PartitionValueListTypeDef],
    },
    total=False,
)

_RequiredBatchDeletePartitionRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeletePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionsToDelete": Sequence[PartitionValueListTypeDef],
    },
)
_OptionalBatchDeletePartitionRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeletePartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class BatchDeletePartitionRequestRequestTypeDef(
    _RequiredBatchDeletePartitionRequestRequestTypeDef,
    _OptionalBatchDeletePartitionRequestRequestTypeDef,
):
    pass


_RequiredBatchGetPartitionRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionsToGet": Sequence[PartitionValueListTypeDef],
    },
)
_OptionalBatchGetPartitionRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetPartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class BatchGetPartitionRequestRequestTypeDef(
    _RequiredBatchGetPartitionRequestRequestTypeDef, _OptionalBatchGetPartitionRequestRequestTypeDef
):
    pass


CancelMLTaskRunResponseTypeDef = TypedDict(
    "CancelMLTaskRunResponseTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": TaskStatusTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CheckSchemaVersionValidityResponseTypeDef = TypedDict(
    "CheckSchemaVersionValidityResponseTypeDef",
    {
        "Valid": bool,
        "Error": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBlueprintResponseTypeDef = TypedDict(
    "CreateBlueprintResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomEntityTypeResponseTypeDef = TypedDict(
    "CreateCustomEntityTypeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDevEndpointResponseTypeDef = TypedDict(
    "CreateDevEndpointResponseTypeDef",
    {
        "EndpointName": str,
        "Status": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
        "RoleArn": str,
        "YarnEndpointAddress": str,
        "ZeppelinRemoteSparkInterpreterPort": int,
        "NumberOfNodes": int,
        "WorkerType": WorkerTypeType,
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
        "FailureReason": str,
        "SecurityConfiguration": str,
        "CreatedTimestamp": datetime,
        "Arguments": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMLTransformResponseTypeDef = TypedDict(
    "CreateMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRegistryResponseTypeDef = TypedDict(
    "CreateRegistryResponseTypeDef",
    {
        "RegistryArn": str,
        "RegistryName": str,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSchemaResponseTypeDef = TypedDict(
    "CreateSchemaResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "SchemaName": str,
        "SchemaArn": str,
        "Description": str,
        "DataFormat": DataFormatType,
        "Compatibility": CompatibilityType,
        "SchemaCheckpoint": int,
        "LatestSchemaVersion": int,
        "NextSchemaVersion": int,
        "SchemaStatus": SchemaStatusType,
        "Tags": Dict[str, str],
        "SchemaVersionId": str,
        "SchemaVersionStatus": SchemaVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateScriptResponseTypeDef = TypedDict(
    "CreateScriptResponseTypeDef",
    {
        "PythonScript": str,
        "ScalaCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSecurityConfigurationResponseTypeDef = TypedDict(
    "CreateSecurityConfigurationResponseTypeDef",
    {
        "Name": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTriggerResponseTypeDef = TypedDict(
    "CreateTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkflowResponseTypeDef = TypedDict(
    "CreateWorkflowResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBlueprintResponseTypeDef = TypedDict(
    "DeleteBlueprintResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCustomEntityTypeResponseTypeDef = TypedDict(
    "DeleteCustomEntityTypeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteJobResponseTypeDef = TypedDict(
    "DeleteJobResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMLTransformResponseTypeDef = TypedDict(
    "DeleteMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRegistryResponseTypeDef = TypedDict(
    "DeleteRegistryResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "Status": RegistryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSchemaResponseTypeDef = TypedDict(
    "DeleteSchemaResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "Status": SchemaStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSessionResponseTypeDef = TypedDict(
    "DeleteSessionResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTriggerResponseTypeDef = TypedDict(
    "DeleteTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteWorkflowResponseTypeDef = TypedDict(
    "DeleteWorkflowResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCustomEntityTypeResponseTypeDef = TypedDict(
    "GetCustomEntityTypeResponseTypeDef",
    {
        "Name": str,
        "RegexString": str,
        "ContextWords": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPlanResponseTypeDef = TypedDict(
    "GetPlanResponseTypeDef",
    {
        "PythonScript": str,
        "ScalaCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRegistryResponseTypeDef = TypedDict(
    "GetRegistryResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "Description": str,
        "Status": RegistryStatusType,
        "CreatedTime": str,
        "UpdatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "PolicyInJson": str,
        "PolicyHash": str,
        "CreateTime": datetime,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaByDefinitionResponseTypeDef = TypedDict(
    "GetSchemaByDefinitionResponseTypeDef",
    {
        "SchemaVersionId": str,
        "SchemaArn": str,
        "DataFormat": DataFormatType,
        "Status": SchemaVersionStatusType,
        "CreatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaResponseTypeDef = TypedDict(
    "GetSchemaResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "SchemaName": str,
        "SchemaArn": str,
        "Description": str,
        "DataFormat": DataFormatType,
        "Compatibility": CompatibilityType,
        "SchemaCheckpoint": int,
        "LatestSchemaVersion": int,
        "NextSchemaVersion": int,
        "SchemaStatus": SchemaStatusType,
        "CreatedTime": str,
        "UpdatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaVersionResponseTypeDef = TypedDict(
    "GetSchemaVersionResponseTypeDef",
    {
        "SchemaVersionId": str,
        "SchemaDefinition": str,
        "DataFormat": DataFormatType,
        "SchemaArn": str,
        "VersionNumber": int,
        "Status": SchemaVersionStatusType,
        "CreatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaVersionsDiffResponseTypeDef = TypedDict(
    "GetSchemaVersionsDiffResponseTypeDef",
    {
        "Diff": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTagsResponseTypeDef = TypedDict(
    "GetTagsResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorkflowRunPropertiesResponseTypeDef = TypedDict(
    "GetWorkflowRunPropertiesResponseTypeDef",
    {
        "RunProperties": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBlueprintsResponseTypeDef = TypedDict(
    "ListBlueprintsResponseTypeDef",
    {
        "Blueprints": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCrawlersResponseTypeDef = TypedDict(
    "ListCrawlersResponseTypeDef",
    {
        "CrawlerNames": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDevEndpointsResponseTypeDef = TypedDict(
    "ListDevEndpointsResponseTypeDef",
    {
        "DevEndpointNames": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "JobNames": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMLTransformsResponseTypeDef = TypedDict(
    "ListMLTransformsResponseTypeDef",
    {
        "TransformIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTriggersResponseTypeDef = TypedDict(
    "ListTriggersResponseTypeDef",
    {
        "TriggerNames": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorkflowsResponseTypeDef = TypedDict(
    "ListWorkflowsResponseTypeDef",
    {
        "Workflows": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef",
    {
        "PolicyHash": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSchemaVersionMetadataResponseTypeDef = TypedDict(
    "PutSchemaVersionMetadataResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
        "LatestVersion": bool,
        "VersionNumber": int,
        "SchemaVersionId": str,
        "MetadataKey": str,
        "MetadataValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterSchemaVersionResponseTypeDef = TypedDict(
    "RegisterSchemaVersionResponseTypeDef",
    {
        "SchemaVersionId": str,
        "VersionNumber": int,
        "Status": SchemaVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveSchemaVersionMetadataResponseTypeDef = TypedDict(
    "RemoveSchemaVersionMetadataResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
        "LatestVersion": bool,
        "VersionNumber": int,
        "SchemaVersionId": str,
        "MetadataKey": str,
        "MetadataValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResumeWorkflowRunResponseTypeDef = TypedDict(
    "ResumeWorkflowRunResponseTypeDef",
    {
        "RunId": str,
        "NodeIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RunStatementResponseTypeDef = TypedDict(
    "RunStatementResponseTypeDef",
    {
        "Id": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartBlueprintRunResponseTypeDef = TypedDict(
    "StartBlueprintRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartExportLabelsTaskRunResponseTypeDef = TypedDict(
    "StartExportLabelsTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartImportLabelsTaskRunResponseTypeDef = TypedDict(
    "StartImportLabelsTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartJobRunResponseTypeDef = TypedDict(
    "StartJobRunResponseTypeDef",
    {
        "JobRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMLEvaluationTaskRunResponseTypeDef = TypedDict(
    "StartMLEvaluationTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMLLabelingSetGenerationTaskRunResponseTypeDef = TypedDict(
    "StartMLLabelingSetGenerationTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTriggerResponseTypeDef = TypedDict(
    "StartTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartWorkflowRunResponseTypeDef = TypedDict(
    "StartWorkflowRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopSessionResponseTypeDef = TypedDict(
    "StopSessionResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopTriggerResponseTypeDef = TypedDict(
    "StopTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBlueprintResponseTypeDef = TypedDict(
    "UpdateBlueprintResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobResponseTypeDef = TypedDict(
    "UpdateJobResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMLTransformResponseTypeDef = TypedDict(
    "UpdateMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRegistryResponseTypeDef = TypedDict(
    "UpdateRegistryResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSchemaResponseTypeDef = TypedDict(
    "UpdateSchemaResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorkflowResponseTypeDef = TypedDict(
    "UpdateWorkflowResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteConnectionResponseTypeDef = TypedDict(
    "BatchDeleteConnectionResponseTypeDef",
    {
        "Succeeded": List[str],
        "Errors": Dict[str, ErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchStopJobRunErrorTypeDef = TypedDict(
    "BatchStopJobRunErrorTypeDef",
    {
        "JobName": str,
        "JobRunId": str,
        "ErrorDetail": ErrorDetailTypeDef,
    },
    total=False,
)

BatchUpdatePartitionFailureEntryTypeDef = TypedDict(
    "BatchUpdatePartitionFailureEntryTypeDef",
    {
        "PartitionValueList": List[str],
        "ErrorDetail": ErrorDetailTypeDef,
    },
    total=False,
)

ColumnErrorTypeDef = TypedDict(
    "ColumnErrorTypeDef",
    {
        "ColumnName": str,
        "Error": ErrorDetailTypeDef,
    },
    total=False,
)

PartitionErrorTypeDef = TypedDict(
    "PartitionErrorTypeDef",
    {
        "PartitionValues": List[str],
        "ErrorDetail": ErrorDetailTypeDef,
    },
    total=False,
)

TableErrorTypeDef = TypedDict(
    "TableErrorTypeDef",
    {
        "TableName": str,
        "ErrorDetail": ErrorDetailTypeDef,
    },
    total=False,
)

TableVersionErrorTypeDef = TypedDict(
    "TableVersionErrorTypeDef",
    {
        "TableName": str,
        "VersionId": str,
        "ErrorDetail": ErrorDetailTypeDef,
    },
    total=False,
)

BatchGetCustomEntityTypesResponseTypeDef = TypedDict(
    "BatchGetCustomEntityTypesResponseTypeDef",
    {
        "CustomEntityTypes": List[CustomEntityTypeTypeDef],
        "CustomEntityTypesNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomEntityTypesResponseTypeDef = TypedDict(
    "ListCustomEntityTypesResponseTypeDef",
    {
        "CustomEntityTypes": List[CustomEntityTypeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetDevEndpointsResponseTypeDef = TypedDict(
    "BatchGetDevEndpointsResponseTypeDef",
    {
        "DevEndpoints": List[DevEndpointTypeDef],
        "DevEndpointsNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDevEndpointResponseTypeDef = TypedDict(
    "GetDevEndpointResponseTypeDef",
    {
        "DevEndpoint": DevEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDevEndpointsResponseTypeDef = TypedDict(
    "GetDevEndpointsResponseTypeDef",
    {
        "DevEndpoints": List[DevEndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBlueprintRunResponseTypeDef = TypedDict(
    "GetBlueprintRunResponseTypeDef",
    {
        "BlueprintRun": BlueprintRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBlueprintRunsResponseTypeDef = TypedDict(
    "GetBlueprintRunsResponseTypeDef",
    {
        "BlueprintRuns": List[BlueprintRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BlueprintTypeDef = TypedDict(
    "BlueprintTypeDef",
    {
        "Name": str,
        "Description": str,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "ParameterSpec": str,
        "BlueprintLocation": str,
        "BlueprintServiceLocation": str,
        "Status": BlueprintStatusType,
        "ErrorMessage": str,
        "LastActiveDefinition": LastActiveDefinitionTypeDef,
    },
    total=False,
)

GetCatalogImportStatusResponseTypeDef = TypedDict(
    "GetCatalogImportStatusResponseTypeDef",
    {
        "ImportStatus": CatalogImportStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCatalogKafkaSourceTypeDef = TypedDict(
    "_RequiredCatalogKafkaSourceTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
    },
)
_OptionalCatalogKafkaSourceTypeDef = TypedDict(
    "_OptionalCatalogKafkaSourceTypeDef",
    {
        "WindowSize": int,
        "DetectSchema": bool,
        "StreamingOptions": KafkaStreamingSourceOptionsTypeDef,
        "DataPreviewOptions": StreamingDataPreviewOptionsTypeDef,
    },
    total=False,
)


class CatalogKafkaSourceTypeDef(
    _RequiredCatalogKafkaSourceTypeDef, _OptionalCatalogKafkaSourceTypeDef
):
    pass


_RequiredDirectKafkaSourceTypeDef = TypedDict(
    "_RequiredDirectKafkaSourceTypeDef",
    {
        "Name": str,
    },
)
_OptionalDirectKafkaSourceTypeDef = TypedDict(
    "_OptionalDirectKafkaSourceTypeDef",
    {
        "StreamingOptions": KafkaStreamingSourceOptionsTypeDef,
        "WindowSize": int,
        "DetectSchema": bool,
        "DataPreviewOptions": StreamingDataPreviewOptionsTypeDef,
    },
    total=False,
)


class DirectKafkaSourceTypeDef(
    _RequiredDirectKafkaSourceTypeDef, _OptionalDirectKafkaSourceTypeDef
):
    pass


_RequiredCatalogKinesisSourceTypeDef = TypedDict(
    "_RequiredCatalogKinesisSourceTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
    },
)
_OptionalCatalogKinesisSourceTypeDef = TypedDict(
    "_OptionalCatalogKinesisSourceTypeDef",
    {
        "WindowSize": int,
        "DetectSchema": bool,
        "StreamingOptions": KinesisStreamingSourceOptionsTypeDef,
        "DataPreviewOptions": StreamingDataPreviewOptionsTypeDef,
    },
    total=False,
)


class CatalogKinesisSourceTypeDef(
    _RequiredCatalogKinesisSourceTypeDef, _OptionalCatalogKinesisSourceTypeDef
):
    pass


_RequiredDirectKinesisSourceTypeDef = TypedDict(
    "_RequiredDirectKinesisSourceTypeDef",
    {
        "Name": str,
    },
)
_OptionalDirectKinesisSourceTypeDef = TypedDict(
    "_OptionalDirectKinesisSourceTypeDef",
    {
        "WindowSize": int,
        "DetectSchema": bool,
        "StreamingOptions": KinesisStreamingSourceOptionsTypeDef,
        "DataPreviewOptions": StreamingDataPreviewOptionsTypeDef,
    },
    total=False,
)


class DirectKinesisSourceTypeDef(
    _RequiredDirectKinesisSourceTypeDef, _OptionalDirectKinesisSourceTypeDef
):
    pass


_RequiredGovernedCatalogTargetTypeDef = TypedDict(
    "_RequiredGovernedCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
    },
)
_OptionalGovernedCatalogTargetTypeDef = TypedDict(
    "_OptionalGovernedCatalogTargetTypeDef",
    {
        "PartitionKeys": List[List[str]],
        "SchemaChangePolicy": CatalogSchemaChangePolicyTypeDef,
    },
    total=False,
)


class GovernedCatalogTargetTypeDef(
    _RequiredGovernedCatalogTargetTypeDef, _OptionalGovernedCatalogTargetTypeDef
):
    pass


_RequiredS3CatalogTargetTypeDef = TypedDict(
    "_RequiredS3CatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
    },
)
_OptionalS3CatalogTargetTypeDef = TypedDict(
    "_OptionalS3CatalogTargetTypeDef",
    {
        "PartitionKeys": List[List[str]],
        "SchemaChangePolicy": CatalogSchemaChangePolicyTypeDef,
    },
    total=False,
)


class S3CatalogTargetTypeDef(_RequiredS3CatalogTargetTypeDef, _OptionalS3CatalogTargetTypeDef):
    pass


ClassifierTypeDef = TypedDict(
    "ClassifierTypeDef",
    {
        "GrokClassifier": GrokClassifierTypeDef,
        "XMLClassifier": XMLClassifierTypeDef,
        "JsonClassifier": JsonClassifierTypeDef,
        "CsvClassifier": CsvClassifierTypeDef,
    },
    total=False,
)

_RequiredCodeGenNodeTypeDef = TypedDict(
    "_RequiredCodeGenNodeTypeDef",
    {
        "Id": str,
        "NodeType": str,
        "Args": Sequence[CodeGenNodeArgTypeDef],
    },
)
_OptionalCodeGenNodeTypeDef = TypedDict(
    "_OptionalCodeGenNodeTypeDef",
    {
        "LineNumber": int,
    },
    total=False,
)


class CodeGenNodeTypeDef(_RequiredCodeGenNodeTypeDef, _OptionalCodeGenNodeTypeDef):
    pass


LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "Jdbc": Sequence[CodeGenNodeArgTypeDef],
        "S3": Sequence[CodeGenNodeArgTypeDef],
        "DynamoDB": Sequence[CodeGenNodeArgTypeDef],
    },
    total=False,
)

PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "Logical": LogicalType,
        "Conditions": List[ConditionTypeDef],
    },
    total=False,
)

FindMatchesMetricsTypeDef = TypedDict(
    "FindMatchesMetricsTypeDef",
    {
        "AreaUnderPRCurve": float,
        "Precision": float,
        "Recall": float,
        "F1": float,
        "ConfusionMatrix": ConfusionMatrixTypeDef,
        "ColumnImportances": List[ColumnImportanceTypeDef],
    },
    total=False,
)

_RequiredConnectionInputTypeDef = TypedDict(
    "_RequiredConnectionInputTypeDef",
    {
        "Name": str,
        "ConnectionType": ConnectionTypeType,
        "ConnectionProperties": Mapping[ConnectionPropertyKeyType, str],
    },
)
_OptionalConnectionInputTypeDef = TypedDict(
    "_OptionalConnectionInputTypeDef",
    {
        "Description": str,
        "MatchCriteria": Sequence[str],
        "PhysicalConnectionRequirements": PhysicalConnectionRequirementsTypeDef,
    },
    total=False,
)


class ConnectionInputTypeDef(_RequiredConnectionInputTypeDef, _OptionalConnectionInputTypeDef):
    pass


ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "Name": str,
        "Description": str,
        "ConnectionType": ConnectionTypeType,
        "MatchCriteria": List[str],
        "ConnectionProperties": Dict[ConnectionPropertyKeyType, str],
        "PhysicalConnectionRequirements": PhysicalConnectionRequirementsTypeDef,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
        "LastUpdatedBy": str,
    },
    total=False,
)

CrawlerNodeDetailsTypeDef = TypedDict(
    "CrawlerNodeDetailsTypeDef",
    {
        "Crawls": List[CrawlTypeDef],
    },
    total=False,
)

GetCrawlerMetricsResponseTypeDef = TypedDict(
    "GetCrawlerMetricsResponseTypeDef",
    {
        "CrawlerMetricsList": List[CrawlerMetricsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CrawlerTargetsTypeDef = TypedDict(
    "CrawlerTargetsTypeDef",
    {
        "S3Targets": List[S3TargetTypeDef],
        "JdbcTargets": List[JdbcTargetTypeDef],
        "MongoDBTargets": List[MongoDBTargetTypeDef],
        "DynamoDBTargets": List[DynamoDBTargetTypeDef],
        "CatalogTargets": List[CatalogTargetTypeDef],
        "DeltaTargets": List[DeltaTargetTypeDef],
    },
    total=False,
)

CreateClassifierRequestRequestTypeDef = TypedDict(
    "CreateClassifierRequestRequestTypeDef",
    {
        "GrokClassifier": CreateGrokClassifierRequestTypeDef,
        "XMLClassifier": CreateXMLClassifierRequestTypeDef,
        "JsonClassifier": CreateJsonClassifierRequestTypeDef,
        "CsvClassifier": CreateCsvClassifierRequestTypeDef,
    },
    total=False,
)

_RequiredCreatePartitionIndexRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePartitionIndexRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionIndex": PartitionIndexTypeDef,
    },
)
_OptionalCreatePartitionIndexRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePartitionIndexRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class CreatePartitionIndexRequestRequestTypeDef(
    _RequiredCreatePartitionIndexRequestRequestTypeDef,
    _OptionalCreatePartitionIndexRequestRequestTypeDef,
):
    pass


_RequiredCreateSchemaInputRequestTypeDef = TypedDict(
    "_RequiredCreateSchemaInputRequestTypeDef",
    {
        "SchemaName": str,
        "DataFormat": DataFormatType,
    },
)
_OptionalCreateSchemaInputRequestTypeDef = TypedDict(
    "_OptionalCreateSchemaInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
        "Compatibility": CompatibilityType,
        "Description": str,
        "Tags": Mapping[str, str],
        "SchemaDefinition": str,
    },
    total=False,
)


class CreateSchemaInputRequestTypeDef(
    _RequiredCreateSchemaInputRequestTypeDef, _OptionalCreateSchemaInputRequestTypeDef
):
    pass


DeleteRegistryInputRequestTypeDef = TypedDict(
    "DeleteRegistryInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
    },
)

GetRegistryInputRequestTypeDef = TypedDict(
    "GetRegistryInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
    },
)

ListSchemasInputRequestTypeDef = TypedDict(
    "ListSchemasInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

UpdateRegistryInputRequestTypeDef = TypedDict(
    "UpdateRegistryInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
        "Description": str,
    },
)

_RequiredCreateSessionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSessionRequestRequestTypeDef",
    {
        "Id": str,
        "Role": str,
        "Command": SessionCommandTypeDef,
    },
)
_OptionalCreateSessionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSessionRequestRequestTypeDef",
    {
        "Description": str,
        "Timeout": int,
        "IdleTimeout": int,
        "DefaultArguments": Mapping[str, str],
        "Connections": ConnectionsListTypeDef,
        "MaxCapacity": float,
        "NumberOfWorkers": int,
        "WorkerType": WorkerTypeType,
        "SecurityConfiguration": str,
        "GlueVersion": str,
        "Tags": Mapping[str, str],
        "RequestOrigin": str,
    },
    total=False,
)


class CreateSessionRequestRequestTypeDef(
    _RequiredCreateSessionRequestRequestTypeDef, _OptionalCreateSessionRequestRequestTypeDef
):
    pass


SessionTypeDef = TypedDict(
    "SessionTypeDef",
    {
        "Id": str,
        "CreatedOn": datetime,
        "Status": SessionStatusType,
        "ErrorMessage": str,
        "Description": str,
        "Role": str,
        "Command": SessionCommandTypeDef,
        "DefaultArguments": Dict[str, str],
        "Connections": ConnectionsListTypeDef,
        "Progress": float,
        "MaxCapacity": float,
        "SecurityConfiguration": str,
        "GlueVersion": str,
    },
    total=False,
)

DataCatalogEncryptionSettingsTypeDef = TypedDict(
    "DataCatalogEncryptionSettingsTypeDef",
    {
        "EncryptionAtRest": EncryptionAtRestTypeDef,
        "ConnectionPasswordEncryption": ConnectionPasswordEncryptionTypeDef,
    },
    total=False,
)

PrincipalPermissionsTypeDef = TypedDict(
    "PrincipalPermissionsTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Permissions": Sequence[PermissionType],
    },
    total=False,
)

NullValueFieldTypeDef = TypedDict(
    "NullValueFieldTypeDef",
    {
        "Value": str,
        "Datatype": DatatypeTypeDef,
    },
)

_RequiredDecimalColumnStatisticsDataTypeDef = TypedDict(
    "_RequiredDecimalColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
    },
)
_OptionalDecimalColumnStatisticsDataTypeDef = TypedDict(
    "_OptionalDecimalColumnStatisticsDataTypeDef",
    {
        "MinimumValue": DecimalNumberTypeDef,
        "MaximumValue": DecimalNumberTypeDef,
    },
    total=False,
)


class DecimalColumnStatisticsDataTypeDef(
    _RequiredDecimalColumnStatisticsDataTypeDef, _OptionalDecimalColumnStatisticsDataTypeDef
):
    pass


DeleteSchemaInputRequestTypeDef = TypedDict(
    "DeleteSchemaInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)

DeleteSchemaVersionsInputRequestTypeDef = TypedDict(
    "DeleteSchemaVersionsInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "Versions": str,
    },
)

GetSchemaByDefinitionInputRequestTypeDef = TypedDict(
    "GetSchemaByDefinitionInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaDefinition": str,
    },
)

GetSchemaInputRequestTypeDef = TypedDict(
    "GetSchemaInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)

_RequiredListSchemaVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListSchemaVersionsInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)
_OptionalListSchemaVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListSchemaVersionsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListSchemaVersionsInputRequestTypeDef(
    _RequiredListSchemaVersionsInputRequestTypeDef, _OptionalListSchemaVersionsInputRequestTypeDef
):
    pass


RegisterSchemaVersionInputRequestTypeDef = TypedDict(
    "RegisterSchemaVersionInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaDefinition": str,
    },
)

SchemaReferenceTypeDef = TypedDict(
    "SchemaReferenceTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaVersionId": str,
        "SchemaVersionNumber": int,
    },
    total=False,
)

_RequiredUpdateDevEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
    },
)
_OptionalUpdateDevEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDevEndpointRequestRequestTypeDef",
    {
        "PublicKey": str,
        "AddPublicKeys": Sequence[str],
        "DeletePublicKeys": Sequence[str],
        "CustomLibraries": DevEndpointCustomLibrariesTypeDef,
        "UpdateEtlLibraries": bool,
        "DeleteArguments": Sequence[str],
        "AddArguments": Mapping[str, str],
    },
    total=False,
)


class UpdateDevEndpointRequestRequestTypeDef(
    _RequiredUpdateDevEndpointRequestRequestTypeDef, _OptionalUpdateDevEndpointRequestRequestTypeDef
):
    pass


_RequiredS3DirectTargetTypeDef = TypedDict(
    "_RequiredS3DirectTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Format": TargetFormatType,
    },
)
_OptionalS3DirectTargetTypeDef = TypedDict(
    "_OptionalS3DirectTargetTypeDef",
    {
        "PartitionKeys": List[List[str]],
        "Compression": str,
        "SchemaChangePolicy": DirectSchemaChangePolicyTypeDef,
    },
    total=False,
)


class S3DirectTargetTypeDef(_RequiredS3DirectTargetTypeDef, _OptionalS3DirectTargetTypeDef):
    pass


_RequiredS3GlueParquetTargetTypeDef = TypedDict(
    "_RequiredS3GlueParquetTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
    },
)
_OptionalS3GlueParquetTargetTypeDef = TypedDict(
    "_OptionalS3GlueParquetTargetTypeDef",
    {
        "PartitionKeys": List[List[str]],
        "Compression": ParquetCompressionTypeType,
        "SchemaChangePolicy": DirectSchemaChangePolicyTypeDef,
    },
    total=False,
)


class S3GlueParquetTargetTypeDef(
    _RequiredS3GlueParquetTargetTypeDef, _OptionalS3GlueParquetTargetTypeDef
):
    pass


EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "S3Encryption": Sequence[S3EncryptionTypeDef],
        "CloudWatchEncryption": CloudWatchEncryptionTypeDef,
        "JobBookmarksEncryption": JobBookmarksEncryptionTypeDef,
    },
    total=False,
)

SchemaVersionErrorItemTypeDef = TypedDict(
    "SchemaVersionErrorItemTypeDef",
    {
        "VersionNumber": int,
        "ErrorDetails": ErrorDetailsTypeDef,
    },
    total=False,
)

_RequiredFilterExpressionTypeDef = TypedDict(
    "_RequiredFilterExpressionTypeDef",
    {
        "Operation": FilterOperationType,
        "Values": List[FilterValueTypeDef],
    },
)
_OptionalFilterExpressionTypeDef = TypedDict(
    "_OptionalFilterExpressionTypeDef",
    {
        "Negated": bool,
    },
    total=False,
)


class FilterExpressionTypeDef(_RequiredFilterExpressionTypeDef, _OptionalFilterExpressionTypeDef):
    pass


_RequiredTransformParametersTypeDef = TypedDict(
    "_RequiredTransformParametersTypeDef",
    {
        "TransformType": Literal["FIND_MATCHES"],
    },
)
_OptionalTransformParametersTypeDef = TypedDict(
    "_OptionalTransformParametersTypeDef",
    {
        "FindMatchesParameters": FindMatchesParametersTypeDef,
    },
    total=False,
)


class TransformParametersTypeDef(
    _RequiredTransformParametersTypeDef, _OptionalTransformParametersTypeDef
):
    pass


GetClassifiersRequestGetClassifiersPaginateTypeDef = TypedDict(
    "GetClassifiersRequestGetClassifiersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef = TypedDict(
    "GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef",
    {
        "CrawlerNameList": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetCrawlersRequestGetCrawlersPaginateTypeDef = TypedDict(
    "GetCrawlersRequestGetCrawlersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetDatabasesRequestGetDatabasesPaginateTypeDef = TypedDict(
    "GetDatabasesRequestGetDatabasesPaginateTypeDef",
    {
        "CatalogId": str,
        "ResourceShareType": ResourceShareTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef = TypedDict(
    "GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetJobRunsRequestGetJobRunsPaginateTypeDef = TypedDict(
    "_RequiredGetJobRunsRequestGetJobRunsPaginateTypeDef",
    {
        "JobName": str,
    },
)
_OptionalGetJobRunsRequestGetJobRunsPaginateTypeDef = TypedDict(
    "_OptionalGetJobRunsRequestGetJobRunsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetJobRunsRequestGetJobRunsPaginateTypeDef(
    _RequiredGetJobRunsRequestGetJobRunsPaginateTypeDef,
    _OptionalGetJobRunsRequestGetJobRunsPaginateTypeDef,
):
    pass


GetJobsRequestGetJobsPaginateTypeDef = TypedDict(
    "GetJobsRequestGetJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef = TypedDict(
    "_RequiredGetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef = TypedDict(
    "_OptionalGetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef",
    {
        "CatalogId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef(
    _RequiredGetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef,
    _OptionalGetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef,
):
    pass


GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef = TypedDict(
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef = TypedDict(
    "GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetTableVersionsRequestGetTableVersionsPaginateTypeDef = TypedDict(
    "_RequiredGetTableVersionsRequestGetTableVersionsPaginateTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetTableVersionsRequestGetTableVersionsPaginateTypeDef = TypedDict(
    "_OptionalGetTableVersionsRequestGetTableVersionsPaginateTypeDef",
    {
        "CatalogId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetTableVersionsRequestGetTableVersionsPaginateTypeDef(
    _RequiredGetTableVersionsRequestGetTableVersionsPaginateTypeDef,
    _OptionalGetTableVersionsRequestGetTableVersionsPaginateTypeDef,
):
    pass


_RequiredGetTablesRequestGetTablesPaginateTypeDef = TypedDict(
    "_RequiredGetTablesRequestGetTablesPaginateTypeDef",
    {
        "DatabaseName": str,
    },
)
_OptionalGetTablesRequestGetTablesPaginateTypeDef = TypedDict(
    "_OptionalGetTablesRequestGetTablesPaginateTypeDef",
    {
        "CatalogId": str,
        "Expression": str,
        "TransactionId": str,
        "QueryAsOfTime": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetTablesRequestGetTablesPaginateTypeDef(
    _RequiredGetTablesRequestGetTablesPaginateTypeDef,
    _OptionalGetTablesRequestGetTablesPaginateTypeDef,
):
    pass


GetTriggersRequestGetTriggersPaginateTypeDef = TypedDict(
    "GetTriggersRequestGetTriggersPaginateTypeDef",
    {
        "DependentJobName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef = TypedDict(
    "_RequiredGetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef",
    {
        "Pattern": str,
    },
)
_OptionalGetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef = TypedDict(
    "_OptionalGetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef(
    _RequiredGetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef,
    _OptionalGetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef,
):
    pass


ListRegistriesInputListRegistriesPaginateTypeDef = TypedDict(
    "ListRegistriesInputListRegistriesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSchemaVersionsInputListSchemaVersionsPaginateTypeDef = TypedDict(
    "_RequiredListSchemaVersionsInputListSchemaVersionsPaginateTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)
_OptionalListSchemaVersionsInputListSchemaVersionsPaginateTypeDef = TypedDict(
    "_OptionalListSchemaVersionsInputListSchemaVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef(
    _RequiredListSchemaVersionsInputListSchemaVersionsPaginateTypeDef,
    _OptionalListSchemaVersionsInputListSchemaVersionsPaginateTypeDef,
):
    pass


ListSchemasInputListSchemasPaginateTypeDef = TypedDict(
    "ListSchemasInputListSchemasPaginateTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetConnectionsRequestGetConnectionsPaginateTypeDef = TypedDict(
    "GetConnectionsRequestGetConnectionsPaginateTypeDef",
    {
        "CatalogId": str,
        "Filter": GetConnectionsFilterTypeDef,
        "HidePassword": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetConnectionsRequestRequestTypeDef = TypedDict(
    "GetConnectionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "Filter": GetConnectionsFilterTypeDef,
        "HidePassword": bool,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetJobBookmarkResponseTypeDef = TypedDict(
    "GetJobBookmarkResponseTypeDef",
    {
        "JobBookmarkEntry": JobBookmarkEntryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResetJobBookmarkResponseTypeDef = TypedDict(
    "ResetJobBookmarkResponseTypeDef",
    {
        "JobBookmarkEntry": JobBookmarkEntryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetMLTaskRunsRequestRequestTypeDef = TypedDict(
    "_RequiredGetMLTaskRunsRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)
_OptionalGetMLTaskRunsRequestRequestTypeDef = TypedDict(
    "_OptionalGetMLTaskRunsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filter": TaskRunFilterCriteriaTypeDef,
        "Sort": TaskRunSortCriteriaTypeDef,
    },
    total=False,
)


class GetMLTaskRunsRequestRequestTypeDef(
    _RequiredGetMLTaskRunsRequestRequestTypeDef, _OptionalGetMLTaskRunsRequestRequestTypeDef
):
    pass


TransformFilterCriteriaTypeDef = TypedDict(
    "TransformFilterCriteriaTypeDef",
    {
        "Name": str,
        "TransformType": Literal["FIND_MATCHES"],
        "Status": TransformStatusTypeType,
        "GlueVersion": str,
        "CreatedBefore": Union[datetime, str],
        "CreatedAfter": Union[datetime, str],
        "LastModifiedBefore": Union[datetime, str],
        "LastModifiedAfter": Union[datetime, str],
        "Schema": Sequence[SchemaColumnTypeDef],
    },
    total=False,
)

GetMappingResponseTypeDef = TypedDict(
    "GetMappingResponseTypeDef",
    {
        "Mapping": List[MappingEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetPartitionsRequestGetPartitionsPaginateTypeDef = TypedDict(
    "_RequiredGetPartitionsRequestGetPartitionsPaginateTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetPartitionsRequestGetPartitionsPaginateTypeDef = TypedDict(
    "_OptionalGetPartitionsRequestGetPartitionsPaginateTypeDef",
    {
        "CatalogId": str,
        "Expression": str,
        "Segment": SegmentTypeDef,
        "ExcludeColumnSchema": bool,
        "TransactionId": str,
        "QueryAsOfTime": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetPartitionsRequestGetPartitionsPaginateTypeDef(
    _RequiredGetPartitionsRequestGetPartitionsPaginateTypeDef,
    _OptionalGetPartitionsRequestGetPartitionsPaginateTypeDef,
):
    pass


_RequiredGetPartitionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetPartitionsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalGetPartitionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetPartitionsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "Expression": str,
        "NextToken": str,
        "Segment": SegmentTypeDef,
        "MaxResults": int,
        "ExcludeColumnSchema": bool,
        "TransactionId": str,
        "QueryAsOfTime": Union[datetime, str],
    },
    total=False,
)


class GetPartitionsRequestRequestTypeDef(
    _RequiredGetPartitionsRequestRequestTypeDef, _OptionalGetPartitionsRequestRequestTypeDef
):
    pass


_RequiredGetUnfilteredPartitionsMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredGetUnfilteredPartitionsMetadataRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
    },
)
_OptionalGetUnfilteredPartitionsMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalGetUnfilteredPartitionsMetadataRequestRequestTypeDef",
    {
        "Expression": str,
        "AuditContext": AuditContextTypeDef,
        "NextToken": str,
        "Segment": SegmentTypeDef,
        "MaxResults": int,
    },
    total=False,
)


class GetUnfilteredPartitionsMetadataRequestRequestTypeDef(
    _RequiredGetUnfilteredPartitionsMetadataRequestRequestTypeDef,
    _OptionalGetUnfilteredPartitionsMetadataRequestRequestTypeDef,
):
    pass


GetResourcePoliciesResponseTypeDef = TypedDict(
    "GetResourcePoliciesResponseTypeDef",
    {
        "GetResourcePoliciesResponseList": List[GluePolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaVersionInputRequestTypeDef = TypedDict(
    "GetSchemaVersionInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaVersionId": str,
        "SchemaVersionNumber": SchemaVersionNumberTypeDef,
    },
    total=False,
)

GetSchemaVersionsDiffInputRequestTypeDef = TypedDict(
    "GetSchemaVersionsDiffInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "FirstSchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SecondSchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SchemaDiffType": Literal["SYNTAX_DIFF"],
    },
)

_RequiredUpdateSchemaInputRequestTypeDef = TypedDict(
    "_RequiredUpdateSchemaInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)
_OptionalUpdateSchemaInputRequestTypeDef = TypedDict(
    "_OptionalUpdateSchemaInputRequestTypeDef",
    {
        "SchemaVersionNumber": SchemaVersionNumberTypeDef,
        "Compatibility": CompatibilityType,
        "Description": str,
    },
    total=False,
)


class UpdateSchemaInputRequestTypeDef(
    _RequiredUpdateSchemaInputRequestTypeDef, _OptionalUpdateSchemaInputRequestTypeDef
):
    pass


GlueSchemaTypeDef = TypedDict(
    "GlueSchemaTypeDef",
    {
        "Columns": List[GlueStudioSchemaColumnTypeDef],
    },
    total=False,
)

_RequiredGovernedCatalogSourceTypeDef = TypedDict(
    "_RequiredGovernedCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
_OptionalGovernedCatalogSourceTypeDef = TypedDict(
    "_OptionalGovernedCatalogSourceTypeDef",
    {
        "PartitionPredicate": str,
        "AdditionalOptions": S3SourceAdditionalOptionsTypeDef,
    },
    total=False,
)


class GovernedCatalogSourceTypeDef(
    _RequiredGovernedCatalogSourceTypeDef, _OptionalGovernedCatalogSourceTypeDef
):
    pass


_RequiredS3CatalogSourceTypeDef = TypedDict(
    "_RequiredS3CatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
_OptionalS3CatalogSourceTypeDef = TypedDict(
    "_OptionalS3CatalogSourceTypeDef",
    {
        "PartitionPredicate": str,
        "AdditionalOptions": S3SourceAdditionalOptionsTypeDef,
    },
    total=False,
)


class S3CatalogSourceTypeDef(_RequiredS3CatalogSourceTypeDef, _OptionalS3CatalogSourceTypeDef):
    pass


JobRunTypeDef = TypedDict(
    "JobRunTypeDef",
    {
        "Id": str,
        "Attempt": int,
        "PreviousRunId": str,
        "TriggerName": str,
        "JobName": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "JobRunState": JobRunStateType,
        "Arguments": Dict[str, str],
        "ErrorMessage": str,
        "PredecessorRuns": List[PredecessorTypeDef],
        "AllocatedCapacity": int,
        "ExecutionTime": int,
        "Timeout": int,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "SecurityConfiguration": str,
        "LogGroupName": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
        "DPUSeconds": float,
    },
    total=False,
)

JoinTypeDef = TypedDict(
    "JoinTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "JoinType": JoinTypeType,
        "Columns": List[JoinColumnTypeDef],
    },
)

TaskRunPropertiesTypeDef = TypedDict(
    "TaskRunPropertiesTypeDef",
    {
        "TaskType": TaskTypeType,
        "ImportLabelsTaskRunProperties": ImportLabelsTaskRunPropertiesTypeDef,
        "ExportLabelsTaskRunProperties": ExportLabelsTaskRunPropertiesTypeDef,
        "LabelingSetGenerationTaskRunProperties": LabelingSetGenerationTaskRunPropertiesTypeDef,
        "FindMatchesTaskRunProperties": FindMatchesTaskRunPropertiesTypeDef,
    },
    total=False,
)

ListRegistriesResponseTypeDef = TypedDict(
    "ListRegistriesResponseTypeDef",
    {
        "Registries": List[RegistryListItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemaVersionsResponseTypeDef = TypedDict(
    "ListSchemaVersionsResponseTypeDef",
    {
        "Schemas": List[SchemaVersionListItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemasResponseTypeDef = TypedDict(
    "ListSchemasResponseTypeDef",
    {
        "Schemas": List[SchemaListItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TransformEncryptionTypeDef = TypedDict(
    "TransformEncryptionTypeDef",
    {
        "MlUserDataEncryption": MLUserDataEncryptionTypeDef,
        "TaskRunSecurityConfigurationName": str,
    },
    total=False,
)

MetadataInfoTypeDef = TypedDict(
    "MetadataInfoTypeDef",
    {
        "MetadataValue": str,
        "CreatedTime": str,
        "OtherMetadataValueList": List[OtherMetadataValueListItemTypeDef],
    },
    total=False,
)

_RequiredPutSchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "_RequiredPutSchemaVersionMetadataInputRequestTypeDef",
    {
        "MetadataKeyValue": MetadataKeyValuePairTypeDef,
    },
)
_OptionalPutSchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "_OptionalPutSchemaVersionMetadataInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SchemaVersionId": str,
    },
    total=False,
)


class PutSchemaVersionMetadataInputRequestTypeDef(
    _RequiredPutSchemaVersionMetadataInputRequestTypeDef,
    _OptionalPutSchemaVersionMetadataInputRequestTypeDef,
):
    pass


QuerySchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "QuerySchemaVersionMetadataInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SchemaVersionId": str,
        "MetadataList": Sequence[MetadataKeyValuePairTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredRemoveSchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "_RequiredRemoveSchemaVersionMetadataInputRequestTypeDef",
    {
        "MetadataKeyValue": MetadataKeyValuePairTypeDef,
    },
)
_OptionalRemoveSchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "_OptionalRemoveSchemaVersionMetadataInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SchemaVersionId": str,
    },
    total=False,
)


class RemoveSchemaVersionMetadataInputRequestTypeDef(
    _RequiredRemoveSchemaVersionMetadataInputRequestTypeDef,
    _OptionalRemoveSchemaVersionMetadataInputRequestTypeDef,
):
    pass


_RequiredRedshiftTargetTypeDef = TypedDict(
    "_RequiredRedshiftTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
_OptionalRedshiftTargetTypeDef = TypedDict(
    "_OptionalRedshiftTargetTypeDef",
    {
        "RedshiftTmpDir": str,
        "TmpDirIAMRole": str,
        "UpsertRedshiftOptions": UpsertRedshiftTargetOptionsTypeDef,
    },
    total=False,
)


class RedshiftTargetTypeDef(_RequiredRedshiftTargetTypeDef, _OptionalRedshiftTargetTypeDef):
    pass


UserDefinedFunctionInputTypeDef = TypedDict(
    "UserDefinedFunctionInputTypeDef",
    {
        "FunctionName": str,
        "ClassName": str,
        "OwnerName": str,
        "OwnerType": PrincipalTypeType,
        "ResourceUris": Sequence[ResourceUriTypeDef],
    },
    total=False,
)

UserDefinedFunctionTypeDef = TypedDict(
    "UserDefinedFunctionTypeDef",
    {
        "FunctionName": str,
        "DatabaseName": str,
        "ClassName": str,
        "OwnerName": str,
        "OwnerType": PrincipalTypeType,
        "CreateTime": datetime,
        "ResourceUris": List[ResourceUriTypeDef],
        "CatalogId": str,
    },
    total=False,
)

SearchTablesRequestRequestTypeDef = TypedDict(
    "SearchTablesRequestRequestTypeDef",
    {
        "CatalogId": str,
        "NextToken": str,
        "Filters": Sequence[PropertyPredicateTypeDef],
        "SearchText": str,
        "SortCriteria": Sequence[SortCriterionTypeDef],
        "MaxResults": int,
        "ResourceShareType": ResourceShareTypeType,
    },
    total=False,
)

StatementOutputTypeDef = TypedDict(
    "StatementOutputTypeDef",
    {
        "Data": StatementOutputDataTypeDef,
        "ExecutionCount": int,
        "Status": StatementStateType,
        "ErrorName": str,
        "ErrorValue": str,
        "Traceback": List[str],
    },
    total=False,
)

UpdateClassifierRequestRequestTypeDef = TypedDict(
    "UpdateClassifierRequestRequestTypeDef",
    {
        "GrokClassifier": UpdateGrokClassifierRequestTypeDef,
        "XMLClassifier": UpdateXMLClassifierRequestTypeDef,
        "JsonClassifier": UpdateJsonClassifierRequestTypeDef,
        "CsvClassifier": UpdateCsvClassifierRequestTypeDef,
    },
    total=False,
)

_RequiredPartitionIndexDescriptorTypeDef = TypedDict(
    "_RequiredPartitionIndexDescriptorTypeDef",
    {
        "IndexName": str,
        "Keys": List[KeySchemaElementTypeDef],
        "IndexStatus": PartitionIndexStatusType,
    },
)
_OptionalPartitionIndexDescriptorTypeDef = TypedDict(
    "_OptionalPartitionIndexDescriptorTypeDef",
    {
        "BackfillErrors": List[BackfillErrorTypeDef],
    },
    total=False,
)


class PartitionIndexDescriptorTypeDef(
    _RequiredPartitionIndexDescriptorTypeDef, _OptionalPartitionIndexDescriptorTypeDef
):
    pass


BatchStopJobRunResponseTypeDef = TypedDict(
    "BatchStopJobRunResponseTypeDef",
    {
        "SuccessfulSubmissions": List[BatchStopJobRunSuccessfulSubmissionTypeDef],
        "Errors": List[BatchStopJobRunErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdatePartitionResponseTypeDef = TypedDict(
    "BatchUpdatePartitionResponseTypeDef",
    {
        "Errors": List[BatchUpdatePartitionFailureEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchCreatePartitionResponseTypeDef = TypedDict(
    "BatchCreatePartitionResponseTypeDef",
    {
        "Errors": List[PartitionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeletePartitionResponseTypeDef = TypedDict(
    "BatchDeletePartitionResponseTypeDef",
    {
        "Errors": List[PartitionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteTableResponseTypeDef = TypedDict(
    "BatchDeleteTableResponseTypeDef",
    {
        "Errors": List[TableErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteTableVersionResponseTypeDef = TypedDict(
    "BatchDeleteTableVersionResponseTypeDef",
    {
        "Errors": List[TableVersionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetBlueprintsResponseTypeDef = TypedDict(
    "BatchGetBlueprintsResponseTypeDef",
    {
        "Blueprints": List[BlueprintTypeDef],
        "MissingBlueprints": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBlueprintResponseTypeDef = TypedDict(
    "GetBlueprintResponseTypeDef",
    {
        "Blueprint": BlueprintTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetClassifierResponseTypeDef = TypedDict(
    "GetClassifierResponseTypeDef",
    {
        "Classifier": ClassifierTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetClassifiersResponseTypeDef = TypedDict(
    "GetClassifiersResponseTypeDef",
    {
        "Classifiers": List[ClassifierTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateScriptRequestRequestTypeDef = TypedDict(
    "CreateScriptRequestRequestTypeDef",
    {
        "DagNodes": Sequence[CodeGenNodeTypeDef],
        "DagEdges": Sequence[CodeGenEdgeTypeDef],
        "Language": LanguageType,
    },
    total=False,
)

GetDataflowGraphResponseTypeDef = TypedDict(
    "GetDataflowGraphResponseTypeDef",
    {
        "DagNodes": List[CodeGenNodeTypeDef],
        "DagEdges": List[CodeGenEdgeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetMappingRequestRequestTypeDef = TypedDict(
    "_RequiredGetMappingRequestRequestTypeDef",
    {
        "Source": CatalogEntryTypeDef,
    },
)
_OptionalGetMappingRequestRequestTypeDef = TypedDict(
    "_OptionalGetMappingRequestRequestTypeDef",
    {
        "Sinks": Sequence[CatalogEntryTypeDef],
        "Location": LocationTypeDef,
    },
    total=False,
)


class GetMappingRequestRequestTypeDef(
    _RequiredGetMappingRequestRequestTypeDef, _OptionalGetMappingRequestRequestTypeDef
):
    pass


_RequiredGetPlanRequestRequestTypeDef = TypedDict(
    "_RequiredGetPlanRequestRequestTypeDef",
    {
        "Mapping": Sequence[MappingEntryTypeDef],
        "Source": CatalogEntryTypeDef,
    },
)
_OptionalGetPlanRequestRequestTypeDef = TypedDict(
    "_OptionalGetPlanRequestRequestTypeDef",
    {
        "Sinks": Sequence[CatalogEntryTypeDef],
        "Location": LocationTypeDef,
        "Language": LanguageType,
        "AdditionalPlanOptionsMap": Mapping[str, str],
    },
    total=False,
)


class GetPlanRequestRequestTypeDef(
    _RequiredGetPlanRequestRequestTypeDef, _OptionalGetPlanRequestRequestTypeDef
):
    pass


_RequiredCreateTriggerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTriggerRequestRequestTypeDef",
    {
        "Name": str,
        "Type": TriggerTypeType,
        "Actions": Sequence[ActionTypeDef],
    },
)
_OptionalCreateTriggerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTriggerRequestRequestTypeDef",
    {
        "WorkflowName": str,
        "Schedule": str,
        "Predicate": PredicateTypeDef,
        "Description": str,
        "StartOnCreation": bool,
        "Tags": Mapping[str, str],
        "EventBatchingCondition": EventBatchingConditionTypeDef,
    },
    total=False,
)


class CreateTriggerRequestRequestTypeDef(
    _RequiredCreateTriggerRequestRequestTypeDef, _OptionalCreateTriggerRequestRequestTypeDef
):
    pass


TriggerTypeDef = TypedDict(
    "TriggerTypeDef",
    {
        "Name": str,
        "WorkflowName": str,
        "Id": str,
        "Type": TriggerTypeType,
        "State": TriggerStateType,
        "Description": str,
        "Schedule": str,
        "Actions": List[ActionTypeDef],
        "Predicate": PredicateTypeDef,
        "EventBatchingCondition": EventBatchingConditionTypeDef,
    },
    total=False,
)

TriggerUpdateTypeDef = TypedDict(
    "TriggerUpdateTypeDef",
    {
        "Name": str,
        "Description": str,
        "Schedule": str,
        "Actions": Sequence[ActionTypeDef],
        "Predicate": PredicateTypeDef,
        "EventBatchingCondition": EventBatchingConditionTypeDef,
    },
    total=False,
)

_RequiredEvaluationMetricsTypeDef = TypedDict(
    "_RequiredEvaluationMetricsTypeDef",
    {
        "TransformType": Literal["FIND_MATCHES"],
    },
)
_OptionalEvaluationMetricsTypeDef = TypedDict(
    "_OptionalEvaluationMetricsTypeDef",
    {
        "FindMatchesMetrics": FindMatchesMetricsTypeDef,
    },
    total=False,
)


class EvaluationMetricsTypeDef(
    _RequiredEvaluationMetricsTypeDef, _OptionalEvaluationMetricsTypeDef
):
    pass


_RequiredCreateConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConnectionRequestRequestTypeDef",
    {
        "ConnectionInput": ConnectionInputTypeDef,
    },
)
_OptionalCreateConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConnectionRequestRequestTypeDef",
    {
        "CatalogId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateConnectionRequestRequestTypeDef(
    _RequiredCreateConnectionRequestRequestTypeDef, _OptionalCreateConnectionRequestRequestTypeDef
):
    pass


_RequiredUpdateConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConnectionRequestRequestTypeDef",
    {
        "Name": str,
        "ConnectionInput": ConnectionInputTypeDef,
    },
)
_OptionalUpdateConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConnectionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class UpdateConnectionRequestRequestTypeDef(
    _RequiredUpdateConnectionRequestRequestTypeDef, _OptionalUpdateConnectionRequestRequestTypeDef
):
    pass


GetConnectionResponseTypeDef = TypedDict(
    "GetConnectionResponseTypeDef",
    {
        "Connection": ConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectionsResponseTypeDef = TypedDict(
    "GetConnectionsResponseTypeDef",
    {
        "ConnectionList": List[ConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CrawlerTypeDef = TypedDict(
    "CrawlerTypeDef",
    {
        "Name": str,
        "Role": str,
        "Targets": CrawlerTargetsTypeDef,
        "DatabaseName": str,
        "Description": str,
        "Classifiers": List[str],
        "RecrawlPolicy": RecrawlPolicyTypeDef,
        "SchemaChangePolicy": SchemaChangePolicyTypeDef,
        "LineageConfiguration": LineageConfigurationTypeDef,
        "State": CrawlerStateType,
        "TablePrefix": str,
        "Schedule": ScheduleTypeDef,
        "CrawlElapsedTime": int,
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "LastCrawl": LastCrawlInfoTypeDef,
        "Version": int,
        "Configuration": str,
        "CrawlerSecurityConfiguration": str,
        "LakeFormationConfiguration": LakeFormationConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateCrawlerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCrawlerRequestRequestTypeDef",
    {
        "Name": str,
        "Role": str,
        "Targets": CrawlerTargetsTypeDef,
    },
)
_OptionalCreateCrawlerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCrawlerRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "Description": str,
        "Schedule": str,
        "Classifiers": Sequence[str],
        "TablePrefix": str,
        "SchemaChangePolicy": SchemaChangePolicyTypeDef,
        "RecrawlPolicy": RecrawlPolicyTypeDef,
        "LineageConfiguration": LineageConfigurationTypeDef,
        "LakeFormationConfiguration": LakeFormationConfigurationTypeDef,
        "Configuration": str,
        "CrawlerSecurityConfiguration": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateCrawlerRequestRequestTypeDef(
    _RequiredCreateCrawlerRequestRequestTypeDef, _OptionalCreateCrawlerRequestRequestTypeDef
):
    pass


_RequiredUpdateCrawlerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateCrawlerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCrawlerRequestRequestTypeDef",
    {
        "Role": str,
        "DatabaseName": str,
        "Description": str,
        "Targets": CrawlerTargetsTypeDef,
        "Schedule": str,
        "Classifiers": Sequence[str],
        "TablePrefix": str,
        "SchemaChangePolicy": SchemaChangePolicyTypeDef,
        "RecrawlPolicy": RecrawlPolicyTypeDef,
        "LineageConfiguration": LineageConfigurationTypeDef,
        "LakeFormationConfiguration": LakeFormationConfigurationTypeDef,
        "Configuration": str,
        "CrawlerSecurityConfiguration": str,
    },
    total=False,
)


class UpdateCrawlerRequestRequestTypeDef(
    _RequiredUpdateCrawlerRequestRequestTypeDef, _OptionalUpdateCrawlerRequestRequestTypeDef
):
    pass


CreateSessionResponseTypeDef = TypedDict(
    "CreateSessionResponseTypeDef",
    {
        "Session": SessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "Session": SessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSessionsResponseTypeDef = TypedDict(
    "ListSessionsResponseTypeDef",
    {
        "Ids": List[str],
        "Sessions": List[SessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataCatalogEncryptionSettingsResponseTypeDef = TypedDict(
    "GetDataCatalogEncryptionSettingsResponseTypeDef",
    {
        "DataCatalogEncryptionSettings": DataCatalogEncryptionSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutDataCatalogEncryptionSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredPutDataCatalogEncryptionSettingsRequestRequestTypeDef",
    {
        "DataCatalogEncryptionSettings": DataCatalogEncryptionSettingsTypeDef,
    },
)
_OptionalPutDataCatalogEncryptionSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalPutDataCatalogEncryptionSettingsRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class PutDataCatalogEncryptionSettingsRequestRequestTypeDef(
    _RequiredPutDataCatalogEncryptionSettingsRequestRequestTypeDef,
    _OptionalPutDataCatalogEncryptionSettingsRequestRequestTypeDef,
):
    pass


_RequiredDatabaseInputTypeDef = TypedDict(
    "_RequiredDatabaseInputTypeDef",
    {
        "Name": str,
    },
)
_OptionalDatabaseInputTypeDef = TypedDict(
    "_OptionalDatabaseInputTypeDef",
    {
        "Description": str,
        "LocationUri": str,
        "Parameters": Mapping[str, str],
        "CreateTableDefaultPermissions": Sequence[PrincipalPermissionsTypeDef],
        "TargetDatabase": DatabaseIdentifierTypeDef,
    },
    total=False,
)


class DatabaseInputTypeDef(_RequiredDatabaseInputTypeDef, _OptionalDatabaseInputTypeDef):
    pass


_RequiredDatabaseTypeDef = TypedDict(
    "_RequiredDatabaseTypeDef",
    {
        "Name": str,
    },
)
_OptionalDatabaseTypeDef = TypedDict(
    "_OptionalDatabaseTypeDef",
    {
        "Description": str,
        "LocationUri": str,
        "Parameters": Dict[str, str],
        "CreateTime": datetime,
        "CreateTableDefaultPermissions": List[PrincipalPermissionsTypeDef],
        "TargetDatabase": DatabaseIdentifierTypeDef,
        "CatalogId": str,
    },
    total=False,
)


class DatabaseTypeDef(_RequiredDatabaseTypeDef, _OptionalDatabaseTypeDef):
    pass


_RequiredDropNullFieldsTypeDef = TypedDict(
    "_RequiredDropNullFieldsTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
    },
)
_OptionalDropNullFieldsTypeDef = TypedDict(
    "_OptionalDropNullFieldsTypeDef",
    {
        "NullCheckBoxList": NullCheckBoxListTypeDef,
        "NullTextList": List[NullValueFieldTypeDef],
    },
    total=False,
)


class DropNullFieldsTypeDef(_RequiredDropNullFieldsTypeDef, _OptionalDropNullFieldsTypeDef):
    pass


_RequiredColumnStatisticsDataTypeDef = TypedDict(
    "_RequiredColumnStatisticsDataTypeDef",
    {
        "Type": ColumnStatisticsTypeType,
    },
)
_OptionalColumnStatisticsDataTypeDef = TypedDict(
    "_OptionalColumnStatisticsDataTypeDef",
    {
        "BooleanColumnStatisticsData": BooleanColumnStatisticsDataTypeDef,
        "DateColumnStatisticsData": DateColumnStatisticsDataTypeDef,
        "DecimalColumnStatisticsData": DecimalColumnStatisticsDataTypeDef,
        "DoubleColumnStatisticsData": DoubleColumnStatisticsDataTypeDef,
        "LongColumnStatisticsData": LongColumnStatisticsDataTypeDef,
        "StringColumnStatisticsData": StringColumnStatisticsDataTypeDef,
        "BinaryColumnStatisticsData": BinaryColumnStatisticsDataTypeDef,
    },
    total=False,
)


class ColumnStatisticsDataTypeDef(
    _RequiredColumnStatisticsDataTypeDef, _OptionalColumnStatisticsDataTypeDef
):
    pass


StorageDescriptorTypeDef = TypedDict(
    "StorageDescriptorTypeDef",
    {
        "Columns": Sequence[ColumnTypeDef],
        "Location": str,
        "AdditionalLocations": Sequence[str],
        "InputFormat": str,
        "OutputFormat": str,
        "Compressed": bool,
        "NumberOfBuckets": int,
        "SerdeInfo": SerDeInfoTypeDef,
        "BucketColumns": Sequence[str],
        "SortColumns": Sequence[OrderTypeDef],
        "Parameters": Mapping[str, str],
        "SkewedInfo": SkewedInfoTypeDef,
        "StoredAsSubDirectories": bool,
        "SchemaReference": SchemaReferenceTypeDef,
    },
    total=False,
)

CreateSecurityConfigurationRequestRequestTypeDef = TypedDict(
    "CreateSecurityConfigurationRequestRequestTypeDef",
    {
        "Name": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
)

SecurityConfigurationTypeDef = TypedDict(
    "SecurityConfigurationTypeDef",
    {
        "Name": str,
        "CreatedTimeStamp": datetime,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)

DeleteSchemaVersionsResponseTypeDef = TypedDict(
    "DeleteSchemaVersionsResponseTypeDef",
    {
        "SchemaVersionErrors": List[SchemaVersionErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "LogicalOperator": FilterLogicalOperatorType,
        "Filters": List[FilterExpressionTypeDef],
    },
)

_RequiredUpdateMLTransformRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMLTransformRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)
_OptionalUpdateMLTransformRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMLTransformRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Parameters": TransformParametersTypeDef,
        "Role": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
    },
    total=False,
)


class UpdateMLTransformRequestRequestTypeDef(
    _RequiredUpdateMLTransformRequestRequestTypeDef, _OptionalUpdateMLTransformRequestRequestTypeDef
):
    pass


GetMLTransformsRequestRequestTypeDef = TypedDict(
    "GetMLTransformsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filter": TransformFilterCriteriaTypeDef,
        "Sort": TransformSortCriteriaTypeDef,
    },
    total=False,
)

ListMLTransformsRequestRequestTypeDef = TypedDict(
    "ListMLTransformsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filter": TransformFilterCriteriaTypeDef,
        "Sort": TransformSortCriteriaTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)

_RequiredAthenaConnectorSourceTypeDef = TypedDict(
    "_RequiredAthenaConnectorSourceTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "SchemaName": str,
    },
)
_OptionalAthenaConnectorSourceTypeDef = TypedDict(
    "_OptionalAthenaConnectorSourceTypeDef",
    {
        "ConnectionTable": str,
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class AthenaConnectorSourceTypeDef(
    _RequiredAthenaConnectorSourceTypeDef, _OptionalAthenaConnectorSourceTypeDef
):
    pass


_RequiredCustomCodeTypeDef = TypedDict(
    "_RequiredCustomCodeTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Code": str,
        "ClassName": str,
    },
)
_OptionalCustomCodeTypeDef = TypedDict(
    "_OptionalCustomCodeTypeDef",
    {
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class CustomCodeTypeDef(_RequiredCustomCodeTypeDef, _OptionalCustomCodeTypeDef):
    pass


_RequiredJDBCConnectorSourceTypeDef = TypedDict(
    "_RequiredJDBCConnectorSourceTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
    },
)
_OptionalJDBCConnectorSourceTypeDef = TypedDict(
    "_OptionalJDBCConnectorSourceTypeDef",
    {
        "AdditionalOptions": JDBCConnectorOptionsTypeDef,
        "ConnectionTable": str,
        "Query": str,
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class JDBCConnectorSourceTypeDef(
    _RequiredJDBCConnectorSourceTypeDef, _OptionalJDBCConnectorSourceTypeDef
):
    pass


_RequiredJDBCConnectorTargetTypeDef = TypedDict(
    "_RequiredJDBCConnectorTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ConnectionName": str,
        "ConnectionTable": str,
        "ConnectorName": str,
        "ConnectionType": str,
    },
)
_OptionalJDBCConnectorTargetTypeDef = TypedDict(
    "_OptionalJDBCConnectorTargetTypeDef",
    {
        "AdditionalOptions": Dict[str, str],
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class JDBCConnectorTargetTypeDef(
    _RequiredJDBCConnectorTargetTypeDef, _OptionalJDBCConnectorTargetTypeDef
):
    pass


_RequiredS3CsvSourceTypeDef = TypedDict(
    "_RequiredS3CsvSourceTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "Separator": SeparatorType,
        "QuoteChar": QuoteCharType,
    },
)
_OptionalS3CsvSourceTypeDef = TypedDict(
    "_OptionalS3CsvSourceTypeDef",
    {
        "CompressionType": CompressionTypeType,
        "Exclusions": List[str],
        "GroupSize": str,
        "GroupFiles": str,
        "Recurse": bool,
        "MaxBand": int,
        "MaxFilesInBand": int,
        "AdditionalOptions": S3DirectSourceAdditionalOptionsTypeDef,
        "Escaper": str,
        "Multiline": bool,
        "WithHeader": bool,
        "WriteHeader": bool,
        "SkipFirst": bool,
        "OptimizePerformance": bool,
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class S3CsvSourceTypeDef(_RequiredS3CsvSourceTypeDef, _OptionalS3CsvSourceTypeDef):
    pass


_RequiredS3JsonSourceTypeDef = TypedDict(
    "_RequiredS3JsonSourceTypeDef",
    {
        "Name": str,
        "Paths": List[str],
    },
)
_OptionalS3JsonSourceTypeDef = TypedDict(
    "_OptionalS3JsonSourceTypeDef",
    {
        "CompressionType": CompressionTypeType,
        "Exclusions": List[str],
        "GroupSize": str,
        "GroupFiles": str,
        "Recurse": bool,
        "MaxBand": int,
        "MaxFilesInBand": int,
        "AdditionalOptions": S3DirectSourceAdditionalOptionsTypeDef,
        "JsonPath": str,
        "Multiline": bool,
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class S3JsonSourceTypeDef(_RequiredS3JsonSourceTypeDef, _OptionalS3JsonSourceTypeDef):
    pass


_RequiredS3ParquetSourceTypeDef = TypedDict(
    "_RequiredS3ParquetSourceTypeDef",
    {
        "Name": str,
        "Paths": List[str],
    },
)
_OptionalS3ParquetSourceTypeDef = TypedDict(
    "_OptionalS3ParquetSourceTypeDef",
    {
        "CompressionType": ParquetCompressionTypeType,
        "Exclusions": List[str],
        "GroupSize": str,
        "GroupFiles": str,
        "Recurse": bool,
        "MaxBand": int,
        "MaxFilesInBand": int,
        "AdditionalOptions": S3DirectSourceAdditionalOptionsTypeDef,
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class S3ParquetSourceTypeDef(_RequiredS3ParquetSourceTypeDef, _OptionalS3ParquetSourceTypeDef):
    pass


_RequiredSparkConnectorSourceTypeDef = TypedDict(
    "_RequiredSparkConnectorSourceTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
    },
)
_OptionalSparkConnectorSourceTypeDef = TypedDict(
    "_OptionalSparkConnectorSourceTypeDef",
    {
        "AdditionalOptions": Dict[str, str],
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class SparkConnectorSourceTypeDef(
    _RequiredSparkConnectorSourceTypeDef, _OptionalSparkConnectorSourceTypeDef
):
    pass


_RequiredSparkConnectorTargetTypeDef = TypedDict(
    "_RequiredSparkConnectorTargetTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
    },
)
_OptionalSparkConnectorTargetTypeDef = TypedDict(
    "_OptionalSparkConnectorTargetTypeDef",
    {
        "AdditionalOptions": Dict[str, str],
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class SparkConnectorTargetTypeDef(
    _RequiredSparkConnectorTargetTypeDef, _OptionalSparkConnectorTargetTypeDef
):
    pass


_RequiredSparkSQLTypeDef = TypedDict(
    "_RequiredSparkSQLTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "SqlQuery": str,
        "SqlAliases": List[SqlAliasTypeDef],
    },
)
_OptionalSparkSQLTypeDef = TypedDict(
    "_OptionalSparkSQLTypeDef",
    {
        "OutputSchemas": List[GlueSchemaTypeDef],
    },
    total=False,
)


class SparkSQLTypeDef(_RequiredSparkSQLTypeDef, _OptionalSparkSQLTypeDef):
    pass


GetJobRunResponseTypeDef = TypedDict(
    "GetJobRunResponseTypeDef",
    {
        "JobRun": JobRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobRunsResponseTypeDef = TypedDict(
    "GetJobRunsResponseTypeDef",
    {
        "JobRuns": List[JobRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobNodeDetailsTypeDef = TypedDict(
    "JobNodeDetailsTypeDef",
    {
        "JobRuns": List[JobRunTypeDef],
    },
    total=False,
)

GetMLTaskRunResponseTypeDef = TypedDict(
    "GetMLTaskRunResponseTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": TaskStatusTypeType,
        "LogGroupName": str,
        "Properties": TaskRunPropertiesTypeDef,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TaskRunTypeDef = TypedDict(
    "TaskRunTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": TaskStatusTypeType,
        "LogGroupName": str,
        "Properties": TaskRunPropertiesTypeDef,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
    },
    total=False,
)

_RequiredCreateMLTransformRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMLTransformRequestRequestTypeDef",
    {
        "Name": str,
        "InputRecordTables": Sequence[GlueTableTypeDef],
        "Parameters": TransformParametersTypeDef,
        "Role": str,
    },
)
_OptionalCreateMLTransformRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMLTransformRequestRequestTypeDef",
    {
        "Description": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
        "Tags": Mapping[str, str],
        "TransformEncryption": TransformEncryptionTypeDef,
    },
    total=False,
)


class CreateMLTransformRequestRequestTypeDef(
    _RequiredCreateMLTransformRequestRequestTypeDef, _OptionalCreateMLTransformRequestRequestTypeDef
):
    pass


QuerySchemaVersionMetadataResponseTypeDef = TypedDict(
    "QuerySchemaVersionMetadataResponseTypeDef",
    {
        "MetadataInfoMap": Dict[str, MetadataInfoTypeDef],
        "SchemaVersionId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionInput": UserDefinedFunctionInputTypeDef,
    },
)
_OptionalCreateUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserDefinedFunctionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class CreateUserDefinedFunctionRequestRequestTypeDef(
    _RequiredCreateUserDefinedFunctionRequestRequestTypeDef,
    _OptionalCreateUserDefinedFunctionRequestRequestTypeDef,
):
    pass


_RequiredUpdateUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionName": str,
        "FunctionInput": UserDefinedFunctionInputTypeDef,
    },
)
_OptionalUpdateUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserDefinedFunctionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class UpdateUserDefinedFunctionRequestRequestTypeDef(
    _RequiredUpdateUserDefinedFunctionRequestRequestTypeDef,
    _OptionalUpdateUserDefinedFunctionRequestRequestTypeDef,
):
    pass


GetUserDefinedFunctionResponseTypeDef = TypedDict(
    "GetUserDefinedFunctionResponseTypeDef",
    {
        "UserDefinedFunction": UserDefinedFunctionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserDefinedFunctionsResponseTypeDef = TypedDict(
    "GetUserDefinedFunctionsResponseTypeDef",
    {
        "UserDefinedFunctions": List[UserDefinedFunctionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StatementTypeDef = TypedDict(
    "StatementTypeDef",
    {
        "Id": int,
        "Code": str,
        "State": StatementStateType,
        "Output": StatementOutputTypeDef,
        "Progress": float,
        "StartedOn": int,
        "CompletedOn": int,
    },
    total=False,
)

GetPartitionIndexesResponseTypeDef = TypedDict(
    "GetPartitionIndexesResponseTypeDef",
    {
        "PartitionIndexDescriptorList": List[PartitionIndexDescriptorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetTriggersResponseTypeDef = TypedDict(
    "BatchGetTriggersResponseTypeDef",
    {
        "Triggers": List[TriggerTypeDef],
        "TriggersNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTriggerResponseTypeDef = TypedDict(
    "GetTriggerResponseTypeDef",
    {
        "Trigger": TriggerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTriggersResponseTypeDef = TypedDict(
    "GetTriggersResponseTypeDef",
    {
        "Triggers": List[TriggerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TriggerNodeDetailsTypeDef = TypedDict(
    "TriggerNodeDetailsTypeDef",
    {
        "Trigger": TriggerTypeDef,
    },
    total=False,
)

UpdateTriggerResponseTypeDef = TypedDict(
    "UpdateTriggerResponseTypeDef",
    {
        "Trigger": TriggerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTriggerRequestRequestTypeDef = TypedDict(
    "UpdateTriggerRequestRequestTypeDef",
    {
        "Name": str,
        "TriggerUpdate": TriggerUpdateTypeDef,
    },
)

GetMLTransformResponseTypeDef = TypedDict(
    "GetMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "Name": str,
        "Description": str,
        "Status": TransformStatusTypeType,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "InputRecordTables": List[GlueTableTypeDef],
        "Parameters": TransformParametersTypeDef,
        "EvaluationMetrics": EvaluationMetricsTypeDef,
        "LabelCount": int,
        "Schema": List[SchemaColumnTypeDef],
        "Role": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
        "TransformEncryption": TransformEncryptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MLTransformTypeDef = TypedDict(
    "MLTransformTypeDef",
    {
        "TransformId": str,
        "Name": str,
        "Description": str,
        "Status": TransformStatusTypeType,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "InputRecordTables": List[GlueTableTypeDef],
        "Parameters": TransformParametersTypeDef,
        "EvaluationMetrics": EvaluationMetricsTypeDef,
        "LabelCount": int,
        "Schema": List[SchemaColumnTypeDef],
        "Role": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
        "TransformEncryption": TransformEncryptionTypeDef,
    },
    total=False,
)

BatchGetCrawlersResponseTypeDef = TypedDict(
    "BatchGetCrawlersResponseTypeDef",
    {
        "Crawlers": List[CrawlerTypeDef],
        "CrawlersNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCrawlerResponseTypeDef = TypedDict(
    "GetCrawlerResponseTypeDef",
    {
        "Crawler": CrawlerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCrawlersResponseTypeDef = TypedDict(
    "GetCrawlersResponseTypeDef",
    {
        "Crawlers": List[CrawlerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatabaseRequestRequestTypeDef",
    {
        "DatabaseInput": DatabaseInputTypeDef,
    },
)
_OptionalCreateDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatabaseRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class CreateDatabaseRequestRequestTypeDef(
    _RequiredCreateDatabaseRequestRequestTypeDef, _OptionalCreateDatabaseRequestRequestTypeDef
):
    pass


_RequiredUpdateDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDatabaseRequestRequestTypeDef",
    {
        "Name": str,
        "DatabaseInput": DatabaseInputTypeDef,
    },
)
_OptionalUpdateDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDatabaseRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class UpdateDatabaseRequestRequestTypeDef(
    _RequiredUpdateDatabaseRequestRequestTypeDef, _OptionalUpdateDatabaseRequestRequestTypeDef
):
    pass


GetDatabaseResponseTypeDef = TypedDict(
    "GetDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDatabasesResponseTypeDef = TypedDict(
    "GetDatabasesResponseTypeDef",
    {
        "DatabaseList": List[DatabaseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ColumnStatisticsTypeDef = TypedDict(
    "ColumnStatisticsTypeDef",
    {
        "ColumnName": str,
        "ColumnType": str,
        "AnalyzedTime": datetime,
        "StatisticsData": ColumnStatisticsDataTypeDef,
    },
)

PartitionInputTypeDef = TypedDict(
    "PartitionInputTypeDef",
    {
        "Values": Sequence[str],
        "LastAccessTime": Union[datetime, str],
        "StorageDescriptor": StorageDescriptorTypeDef,
        "Parameters": Mapping[str, str],
        "LastAnalyzedTime": Union[datetime, str],
    },
    total=False,
)

PartitionTypeDef = TypedDict(
    "PartitionTypeDef",
    {
        "Values": List[str],
        "DatabaseName": str,
        "TableName": str,
        "CreationTime": datetime,
        "LastAccessTime": datetime,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "Parameters": Dict[str, str],
        "LastAnalyzedTime": datetime,
        "CatalogId": str,
    },
    total=False,
)

_RequiredTableInputTypeDef = TypedDict(
    "_RequiredTableInputTypeDef",
    {
        "Name": str,
    },
)
_OptionalTableInputTypeDef = TypedDict(
    "_OptionalTableInputTypeDef",
    {
        "Description": str,
        "Owner": str,
        "LastAccessTime": Union[datetime, str],
        "LastAnalyzedTime": Union[datetime, str],
        "Retention": int,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "PartitionKeys": Sequence[ColumnTypeDef],
        "ViewOriginalText": str,
        "ViewExpandedText": str,
        "TableType": str,
        "Parameters": Mapping[str, str],
        "TargetTable": TableIdentifierTypeDef,
    },
    total=False,
)


class TableInputTypeDef(_RequiredTableInputTypeDef, _OptionalTableInputTypeDef):
    pass


_RequiredTableTypeDef = TypedDict(
    "_RequiredTableTypeDef",
    {
        "Name": str,
    },
)
_OptionalTableTypeDef = TypedDict(
    "_OptionalTableTypeDef",
    {
        "DatabaseName": str,
        "Description": str,
        "Owner": str,
        "CreateTime": datetime,
        "UpdateTime": datetime,
        "LastAccessTime": datetime,
        "LastAnalyzedTime": datetime,
        "Retention": int,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "PartitionKeys": List[ColumnTypeDef],
        "ViewOriginalText": str,
        "ViewExpandedText": str,
        "TableType": str,
        "Parameters": Dict[str, str],
        "CreatedBy": str,
        "IsRegisteredWithLakeFormation": bool,
        "TargetTable": TableIdentifierTypeDef,
        "CatalogId": str,
        "VersionId": str,
    },
    total=False,
)


class TableTypeDef(_RequiredTableTypeDef, _OptionalTableTypeDef):
    pass


GetSecurityConfigurationResponseTypeDef = TypedDict(
    "GetSecurityConfigurationResponseTypeDef",
    {
        "SecurityConfiguration": SecurityConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSecurityConfigurationsResponseTypeDef = TypedDict(
    "GetSecurityConfigurationsResponseTypeDef",
    {
        "SecurityConfigurations": List[SecurityConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CodeGenConfigurationNodeTypeDef = TypedDict(
    "CodeGenConfigurationNodeTypeDef",
    {
        "AthenaConnectorSource": AthenaConnectorSourceTypeDef,
        "JDBCConnectorSource": JDBCConnectorSourceTypeDef,
        "SparkConnectorSource": SparkConnectorSourceTypeDef,
        "CatalogSource": CatalogSourceTypeDef,
        "RedshiftSource": RedshiftSourceTypeDef,
        "S3CatalogSource": S3CatalogSourceTypeDef,
        "S3CsvSource": S3CsvSourceTypeDef,
        "S3JsonSource": S3JsonSourceTypeDef,
        "S3ParquetSource": S3ParquetSourceTypeDef,
        "RelationalCatalogSource": RelationalCatalogSourceTypeDef,
        "DynamoDBCatalogSource": DynamoDBCatalogSourceTypeDef,
        "JDBCConnectorTarget": JDBCConnectorTargetTypeDef,
        "SparkConnectorTarget": SparkConnectorTargetTypeDef,
        "CatalogTarget": BasicCatalogTargetTypeDef,
        "RedshiftTarget": RedshiftTargetTypeDef,
        "S3CatalogTarget": S3CatalogTargetTypeDef,
        "S3GlueParquetTarget": S3GlueParquetTargetTypeDef,
        "S3DirectTarget": S3DirectTargetTypeDef,
        "ApplyMapping": ApplyMappingTypeDef,
        "SelectFields": SelectFieldsTypeDef,
        "DropFields": DropFieldsTypeDef,
        "RenameField": RenameFieldTypeDef,
        "Spigot": SpigotTypeDef,
        "Join": JoinTypeDef,
        "SplitFields": SplitFieldsTypeDef,
        "SelectFromCollection": SelectFromCollectionTypeDef,
        "FillMissingValues": FillMissingValuesTypeDef,
        "Filter": FilterTypeDef,
        "CustomCode": CustomCodeTypeDef,
        "SparkSQL": SparkSQLTypeDef,
        "DirectKinesisSource": DirectKinesisSourceTypeDef,
        "DirectKafkaSource": DirectKafkaSourceTypeDef,
        "CatalogKinesisSource": CatalogKinesisSourceTypeDef,
        "CatalogKafkaSource": CatalogKafkaSourceTypeDef,
        "DropNullFields": DropNullFieldsTypeDef,
        "Merge": MergeTypeDef,
        "Union": UnionTypeDef,
        "PIIDetection": PIIDetectionTypeDef,
        "Aggregate": AggregateTypeDef,
        "DropDuplicates": DropDuplicatesTypeDef,
        "GovernedCatalogTarget": GovernedCatalogTargetTypeDef,
        "GovernedCatalogSource": GovernedCatalogSourceTypeDef,
        "MicrosoftSQLServerCatalogSource": MicrosoftSQLServerCatalogSourceTypeDef,
        "MySQLCatalogSource": MySQLCatalogSourceTypeDef,
        "OracleSQLCatalogSource": OracleSQLCatalogSourceTypeDef,
        "PostgreSQLCatalogSource": PostgreSQLCatalogSourceTypeDef,
        "MicrosoftSQLServerCatalogTarget": MicrosoftSQLServerCatalogTargetTypeDef,
        "MySQLCatalogTarget": MySQLCatalogTargetTypeDef,
        "OracleSQLCatalogTarget": OracleSQLCatalogTargetTypeDef,
        "PostgreSQLCatalogTarget": PostgreSQLCatalogTargetTypeDef,
    },
    total=False,
)

GetMLTaskRunsResponseTypeDef = TypedDict(
    "GetMLTaskRunsResponseTypeDef",
    {
        "TaskRuns": List[TaskRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStatementResponseTypeDef = TypedDict(
    "GetStatementResponseTypeDef",
    {
        "Statement": StatementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStatementsResponseTypeDef = TypedDict(
    "ListStatementsResponseTypeDef",
    {
        "Statements": List[StatementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "Type": NodeTypeType,
        "Name": str,
        "UniqueId": str,
        "TriggerDetails": TriggerNodeDetailsTypeDef,
        "JobDetails": JobNodeDetailsTypeDef,
        "CrawlerDetails": CrawlerNodeDetailsTypeDef,
    },
    total=False,
)

GetMLTransformsResponseTypeDef = TypedDict(
    "GetMLTransformsResponseTypeDef",
    {
        "Transforms": List[MLTransformTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ColumnStatisticsErrorTypeDef = TypedDict(
    "ColumnStatisticsErrorTypeDef",
    {
        "ColumnStatistics": ColumnStatisticsTypeDef,
        "Error": ErrorDetailTypeDef,
    },
    total=False,
)

GetColumnStatisticsForPartitionResponseTypeDef = TypedDict(
    "GetColumnStatisticsForPartitionResponseTypeDef",
    {
        "ColumnStatisticsList": List[ColumnStatisticsTypeDef],
        "Errors": List[ColumnErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetColumnStatisticsForTableResponseTypeDef = TypedDict(
    "GetColumnStatisticsForTableResponseTypeDef",
    {
        "ColumnStatisticsList": List[ColumnStatisticsTypeDef],
        "Errors": List[ColumnErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "ColumnStatisticsList": Sequence[ColumnStatisticsTypeDef],
    },
)
_OptionalUpdateColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class UpdateColumnStatisticsForPartitionRequestRequestTypeDef(
    _RequiredUpdateColumnStatisticsForPartitionRequestRequestTypeDef,
    _OptionalUpdateColumnStatisticsForPartitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateColumnStatisticsForTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "ColumnStatisticsList": Sequence[ColumnStatisticsTypeDef],
    },
)
_OptionalUpdateColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateColumnStatisticsForTableRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class UpdateColumnStatisticsForTableRequestRequestTypeDef(
    _RequiredUpdateColumnStatisticsForTableRequestRequestTypeDef,
    _OptionalUpdateColumnStatisticsForTableRequestRequestTypeDef,
):
    pass


_RequiredBatchCreatePartitionRequestRequestTypeDef = TypedDict(
    "_RequiredBatchCreatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionInputList": Sequence[PartitionInputTypeDef],
    },
)
_OptionalBatchCreatePartitionRequestRequestTypeDef = TypedDict(
    "_OptionalBatchCreatePartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class BatchCreatePartitionRequestRequestTypeDef(
    _RequiredBatchCreatePartitionRequestRequestTypeDef,
    _OptionalBatchCreatePartitionRequestRequestTypeDef,
):
    pass


BatchUpdatePartitionRequestEntryTypeDef = TypedDict(
    "BatchUpdatePartitionRequestEntryTypeDef",
    {
        "PartitionValueList": Sequence[str],
        "PartitionInput": PartitionInputTypeDef,
    },
)

_RequiredCreatePartitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionInput": PartitionInputTypeDef,
    },
)
_OptionalCreatePartitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class CreatePartitionRequestRequestTypeDef(
    _RequiredCreatePartitionRequestRequestTypeDef, _OptionalCreatePartitionRequestRequestTypeDef
):
    pass


_RequiredUpdatePartitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValueList": Sequence[str],
        "PartitionInput": PartitionInputTypeDef,
    },
)
_OptionalUpdatePartitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class UpdatePartitionRequestRequestTypeDef(
    _RequiredUpdatePartitionRequestRequestTypeDef, _OptionalUpdatePartitionRequestRequestTypeDef
):
    pass


BatchGetPartitionResponseTypeDef = TypedDict(
    "BatchGetPartitionResponseTypeDef",
    {
        "Partitions": List[PartitionTypeDef],
        "UnprocessedKeys": List[PartitionValueListTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPartitionResponseTypeDef = TypedDict(
    "GetPartitionResponseTypeDef",
    {
        "Partition": PartitionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPartitionsResponseTypeDef = TypedDict(
    "GetPartitionsResponseTypeDef",
    {
        "Partitions": List[PartitionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUnfilteredPartitionMetadataResponseTypeDef = TypedDict(
    "GetUnfilteredPartitionMetadataResponseTypeDef",
    {
        "Partition": PartitionTypeDef,
        "AuthorizedColumns": List[str],
        "IsRegisteredWithLakeFormation": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UnfilteredPartitionTypeDef = TypedDict(
    "UnfilteredPartitionTypeDef",
    {
        "Partition": PartitionTypeDef,
        "AuthorizedColumns": List[str],
        "IsRegisteredWithLakeFormation": bool,
    },
    total=False,
)

_RequiredCreateTableRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableInput": TableInputTypeDef,
    },
)
_OptionalCreateTableRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTableRequestRequestTypeDef",
    {
        "CatalogId": str,
        "PartitionIndexes": Sequence[PartitionIndexTypeDef],
        "TransactionId": str,
    },
    total=False,
)


class CreateTableRequestRequestTypeDef(
    _RequiredCreateTableRequestRequestTypeDef, _OptionalCreateTableRequestRequestTypeDef
):
    pass


_RequiredUpdateTableRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableInput": TableInputTypeDef,
    },
)
_OptionalUpdateTableRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableRequestRequestTypeDef",
    {
        "CatalogId": str,
        "SkipArchive": bool,
        "TransactionId": str,
        "VersionId": str,
    },
    total=False,
)


class UpdateTableRequestRequestTypeDef(
    _RequiredUpdateTableRequestRequestTypeDef, _OptionalUpdateTableRequestRequestTypeDef
):
    pass


GetTableResponseTypeDef = TypedDict(
    "GetTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTablesResponseTypeDef = TypedDict(
    "GetTablesResponseTypeDef",
    {
        "TableList": List[TableTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUnfilteredTableMetadataResponseTypeDef = TypedDict(
    "GetUnfilteredTableMetadataResponseTypeDef",
    {
        "Table": TableTypeDef,
        "AuthorizedColumns": List[str],
        "IsRegisteredWithLakeFormation": bool,
        "CellFilters": List[ColumnRowFilterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchTablesResponseTypeDef = TypedDict(
    "SearchTablesResponseTypeDef",
    {
        "NextToken": str,
        "TableList": List[TableTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TableVersionTypeDef = TypedDict(
    "TableVersionTypeDef",
    {
        "Table": TableTypeDef,
        "VersionId": str,
    },
    total=False,
)

_RequiredCreateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobRequestRequestTypeDef",
    {
        "Name": str,
        "Role": str,
        "Command": JobCommandTypeDef,
    },
)
_OptionalCreateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobRequestRequestTypeDef",
    {
        "Description": str,
        "LogUri": str,
        "ExecutionProperty": ExecutionPropertyTypeDef,
        "DefaultArguments": Mapping[str, str],
        "NonOverridableArguments": Mapping[str, str],
        "Connections": ConnectionsListTypeDef,
        "MaxRetries": int,
        "AllocatedCapacity": int,
        "Timeout": int,
        "MaxCapacity": float,
        "SecurityConfiguration": str,
        "Tags": Mapping[str, str],
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "WorkerType": WorkerTypeType,
        "CodeGenConfigurationNodes": Mapping[str, CodeGenConfigurationNodeTypeDef],
    },
    total=False,
)


class CreateJobRequestRequestTypeDef(
    _RequiredCreateJobRequestRequestTypeDef, _OptionalCreateJobRequestRequestTypeDef
):
    pass


JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "Name": str,
        "Description": str,
        "LogUri": str,
        "Role": str,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "ExecutionProperty": ExecutionPropertyTypeDef,
        "Command": JobCommandTypeDef,
        "DefaultArguments": Dict[str, str],
        "NonOverridableArguments": Dict[str, str],
        "Connections": ConnectionsListTypeDef,
        "MaxRetries": int,
        "AllocatedCapacity": int,
        "Timeout": int,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
        "CodeGenConfigurationNodes": Dict[str, CodeGenConfigurationNodeTypeDef],
    },
    total=False,
)

JobUpdateTypeDef = TypedDict(
    "JobUpdateTypeDef",
    {
        "Description": str,
        "LogUri": str,
        "Role": str,
        "ExecutionProperty": ExecutionPropertyTypeDef,
        "Command": JobCommandTypeDef,
        "DefaultArguments": Mapping[str, str],
        "NonOverridableArguments": Mapping[str, str],
        "Connections": ConnectionsListTypeDef,
        "MaxRetries": int,
        "AllocatedCapacity": int,
        "Timeout": int,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
        "CodeGenConfigurationNodes": Mapping[str, CodeGenConfigurationNodeTypeDef],
    },
    total=False,
)

WorkflowGraphTypeDef = TypedDict(
    "WorkflowGraphTypeDef",
    {
        "Nodes": List[NodeTypeDef],
        "Edges": List[EdgeTypeDef],
    },
    total=False,
)

UpdateColumnStatisticsForPartitionResponseTypeDef = TypedDict(
    "UpdateColumnStatisticsForPartitionResponseTypeDef",
    {
        "Errors": List[ColumnStatisticsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateColumnStatisticsForTableResponseTypeDef = TypedDict(
    "UpdateColumnStatisticsForTableResponseTypeDef",
    {
        "Errors": List[ColumnStatisticsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchUpdatePartitionRequestRequestTypeDef = TypedDict(
    "_RequiredBatchUpdatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "Entries": Sequence[BatchUpdatePartitionRequestEntryTypeDef],
    },
)
_OptionalBatchUpdatePartitionRequestRequestTypeDef = TypedDict(
    "_OptionalBatchUpdatePartitionRequestRequestTypeDef",
    {
        "CatalogId": str,
    },
    total=False,
)


class BatchUpdatePartitionRequestRequestTypeDef(
    _RequiredBatchUpdatePartitionRequestRequestTypeDef,
    _OptionalBatchUpdatePartitionRequestRequestTypeDef,
):
    pass


GetUnfilteredPartitionsMetadataResponseTypeDef = TypedDict(
    "GetUnfilteredPartitionsMetadataResponseTypeDef",
    {
        "UnfilteredPartitions": List[UnfilteredPartitionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTableVersionResponseTypeDef = TypedDict(
    "GetTableVersionResponseTypeDef",
    {
        "TableVersion": TableVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTableVersionsResponseTypeDef = TypedDict(
    "GetTableVersionsResponseTypeDef",
    {
        "TableVersions": List[TableVersionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetJobsResponseTypeDef = TypedDict(
    "BatchGetJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "JobsNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobsResponseTypeDef = TypedDict(
    "GetJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobRequestRequestTypeDef = TypedDict(
    "UpdateJobRequestRequestTypeDef",
    {
        "JobName": str,
        "JobUpdate": JobUpdateTypeDef,
    },
)

WorkflowRunTypeDef = TypedDict(
    "WorkflowRunTypeDef",
    {
        "Name": str,
        "WorkflowRunId": str,
        "PreviousRunId": str,
        "WorkflowRunProperties": Dict[str, str],
        "StartedOn": datetime,
        "CompletedOn": datetime,
        "Status": WorkflowRunStatusType,
        "ErrorMessage": str,
        "Statistics": WorkflowRunStatisticsTypeDef,
        "Graph": WorkflowGraphTypeDef,
        "StartingEventBatchCondition": StartingEventBatchConditionTypeDef,
    },
    total=False,
)

GetWorkflowRunResponseTypeDef = TypedDict(
    "GetWorkflowRunResponseTypeDef",
    {
        "Run": WorkflowRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorkflowRunsResponseTypeDef = TypedDict(
    "GetWorkflowRunsResponseTypeDef",
    {
        "Runs": List[WorkflowRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef",
    {
        "Name": str,
        "Description": str,
        "DefaultRunProperties": Dict[str, str],
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "LastRun": WorkflowRunTypeDef,
        "Graph": WorkflowGraphTypeDef,
        "MaxConcurrentRuns": int,
        "BlueprintDetails": BlueprintDetailsTypeDef,
    },
    total=False,
)

BatchGetWorkflowsResponseTypeDef = TypedDict(
    "BatchGetWorkflowsResponseTypeDef",
    {
        "Workflows": List[WorkflowTypeDef],
        "MissingWorkflows": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorkflowResponseTypeDef = TypedDict(
    "GetWorkflowResponseTypeDef",
    {
        "Workflow": WorkflowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
