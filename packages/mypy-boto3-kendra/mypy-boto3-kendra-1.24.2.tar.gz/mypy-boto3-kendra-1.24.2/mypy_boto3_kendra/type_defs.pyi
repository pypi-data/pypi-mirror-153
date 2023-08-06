"""
Type annotations for kendra service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/type_defs/)

Usage::

    ```python
    from mypy_boto3_kendra.type_defs import AccessControlListConfigurationTypeDef

    data: AccessControlListConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ConditionOperatorType,
    ConfluenceAttachmentFieldNameType,
    ConfluenceBlogFieldNameType,
    ConfluencePageFieldNameType,
    ConfluenceSpaceFieldNameType,
    ConfluenceVersionType,
    ContentTypeType,
    DatabaseEngineTypeType,
    DataSourceStatusType,
    DataSourceSyncJobStatusType,
    DataSourceTypeType,
    DocumentAttributeValueTypeType,
    DocumentStatusType,
    EntityTypeType,
    ErrorCodeType,
    ExperienceStatusType,
    FaqFileFormatType,
    FaqStatusType,
    HighlightTypeType,
    IndexEditionType,
    IndexStatusType,
    IntervalType,
    IssueSubEntityType,
    KeyLocationType,
    MetricTypeType,
    ModeType,
    OrderType,
    PersonaType,
    PrincipalMappingStatusType,
    PrincipalTypeType,
    QueryIdentifiersEnclosingOptionType,
    QueryResultTypeType,
    QuerySuggestionsBlockListStatusType,
    QuerySuggestionsStatusType,
    ReadAccessTypeType,
    RelevanceTypeType,
    SalesforceChatterFeedIncludeFilterTypeType,
    SalesforceKnowledgeArticleStateType,
    SalesforceStandardObjectNameType,
    ScoreConfidenceType,
    ServiceNowAuthenticationTypeType,
    ServiceNowBuildVersionTypeType,
    SharePointVersionType,
    SlackEntityType,
    SortOrderType,
    ThesaurusStatusType,
    TypeType,
    UserContextPolicyType,
    UserGroupResolutionModeType,
    WebCrawlerModeType,
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
    "AccessControlListConfigurationTypeDef",
    "AclConfigurationTypeDef",
    "EntityConfigurationTypeDef",
    "FailedEntityTypeDef",
    "ResponseMetadataTypeDef",
    "EntityPersonaConfigurationTypeDef",
    "BasicAuthenticationConfigurationTypeDef",
    "DataSourceSyncJobMetricTargetTypeDef",
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    "BatchGetDocumentStatusResponseErrorTypeDef",
    "StatusTypeDef",
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    "DataSourceToIndexFieldMappingTypeDef",
    "DataSourceVpcConfigurationTypeDef",
    "CapacityUnitsConfigurationTypeDef",
    "ClearQuerySuggestionsRequestRequestTypeDef",
    "ClickFeedbackTypeDef",
    "ConfluenceAttachmentToIndexFieldMappingTypeDef",
    "ConfluenceBlogToIndexFieldMappingTypeDef",
    "ConfluencePageToIndexFieldMappingTypeDef",
    "ConfluenceSpaceToIndexFieldMappingTypeDef",
    "ConnectionConfigurationTypeDef",
    "ContentSourceConfigurationTypeDef",
    "CorrectionTypeDef",
    "TagTypeDef",
    "S3PathTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "UserGroupResolutionConfigurationTypeDef",
    "DataSourceGroupTypeDef",
    "DataSourceSummaryTypeDef",
    "DataSourceSyncJobMetricsTypeDef",
    "SqlConfigurationTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteExperienceRequestRequestTypeDef",
    "DeleteFaqRequestRequestTypeDef",
    "DeleteIndexRequestRequestTypeDef",
    "DeletePrincipalMappingRequestRequestTypeDef",
    "DeleteQuerySuggestionsBlockListRequestRequestTypeDef",
    "DeleteThesaurusRequestRequestTypeDef",
    "DescribeDataSourceRequestRequestTypeDef",
    "DescribeExperienceRequestRequestTypeDef",
    "ExperienceEndpointTypeDef",
    "DescribeFaqRequestRequestTypeDef",
    "DescribeIndexRequestRequestTypeDef",
    "DescribePrincipalMappingRequestRequestTypeDef",
    "GroupOrderingIdSummaryTypeDef",
    "DescribeQuerySuggestionsBlockListRequestRequestTypeDef",
    "DescribeQuerySuggestionsConfigRequestRequestTypeDef",
    "DescribeThesaurusRequestRequestTypeDef",
    "DisassociatePersonasFromEntitiesRequestRequestTypeDef",
    "DocumentAttributeValueTypeDef",
    "RelevanceTypeDef",
    "SearchTypeDef",
    "PrincipalTypeDef",
    "DocumentsMetadataConfigurationTypeDef",
    "EntityDisplayDataTypeDef",
    "UserIdentityConfigurationTypeDef",
    "FacetResultTypeDef",
    "FacetTypeDef",
    "FaqStatisticsTypeDef",
    "FaqSummaryTypeDef",
    "GetQuerySuggestionsRequestRequestTypeDef",
    "GetSnapshotsRequestRequestTypeDef",
    "TimeRangeTypeDef",
    "GitHubDocumentCrawlPropertiesTypeDef",
    "SaaSConfigurationTypeDef",
    "MemberGroupTypeDef",
    "MemberUserTypeDef",
    "GroupSummaryTypeDef",
    "HighlightTypeDef",
    "IndexConfigurationSummaryTypeDef",
    "TextDocumentStatisticsTypeDef",
    "JsonTokenTypeConfigurationTypeDef",
    "JwtTokenTypeConfigurationTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListEntityPersonasRequestRequestTypeDef",
    "PersonasSummaryTypeDef",
    "ListExperienceEntitiesRequestRequestTypeDef",
    "ListExperiencesRequestRequestTypeDef",
    "ListFaqsRequestRequestTypeDef",
    "ListGroupsOlderThanOrderingIdRequestRequestTypeDef",
    "ListIndicesRequestRequestTypeDef",
    "ListQuerySuggestionsBlockListsRequestRequestTypeDef",
    "QuerySuggestionsBlockListSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListThesauriRequestRequestTypeDef",
    "ThesaurusSummaryTypeDef",
    "ProxyConfigurationTypeDef",
    "SortingConfigurationTypeDef",
    "SpellCorrectionConfigurationTypeDef",
    "ScoreAttributesTypeDef",
    "WarningTypeDef",
    "RelevanceFeedbackTypeDef",
    "SeedUrlConfigurationTypeDef",
    "SiteMapsConfigurationTypeDef",
    "StartDataSourceSyncJobRequestRequestTypeDef",
    "StopDataSourceSyncJobRequestRequestTypeDef",
    "SuggestionHighlightTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateQuerySuggestionsConfigRequestRequestTypeDef",
    "AssociateEntitiesToExperienceRequestRequestTypeDef",
    "DisassociateEntitiesFromExperienceRequestRequestTypeDef",
    "AssociateEntitiesToExperienceResponseTypeDef",
    "AssociatePersonasToEntitiesResponseTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateExperienceResponseTypeDef",
    "CreateFaqResponseTypeDef",
    "CreateIndexResponseTypeDef",
    "CreateQuerySuggestionsBlockListResponseTypeDef",
    "CreateThesaurusResponseTypeDef",
    "DescribeQuerySuggestionsConfigResponseTypeDef",
    "DisassociateEntitiesFromExperienceResponseTypeDef",
    "DisassociatePersonasFromEntitiesResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "StartDataSourceSyncJobResponseTypeDef",
    "AssociatePersonasToEntitiesRequestRequestTypeDef",
    "AuthenticationConfigurationTypeDef",
    "BatchDeleteDocumentRequestRequestTypeDef",
    "BatchDeleteDocumentResponseTypeDef",
    "BatchGetDocumentStatusResponseTypeDef",
    "BatchPutDocumentResponseTypeDef",
    "ColumnConfigurationTypeDef",
    "GoogleDriveConfigurationTypeDef",
    "SalesforceChatterFeedConfigurationTypeDef",
    "SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    "SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    "SalesforceStandardObjectAttachmentConfigurationTypeDef",
    "SalesforceStandardObjectConfigurationTypeDef",
    "ServiceNowKnowledgeArticleConfigurationTypeDef",
    "ServiceNowServiceCatalogConfigurationTypeDef",
    "WorkDocsConfigurationTypeDef",
    "BoxConfigurationTypeDef",
    "FsxConfigurationTypeDef",
    "JiraConfigurationTypeDef",
    "QuipConfigurationTypeDef",
    "SlackConfigurationTypeDef",
    "ConfluenceAttachmentConfigurationTypeDef",
    "ConfluenceBlogConfigurationTypeDef",
    "ConfluencePageConfigurationTypeDef",
    "ConfluenceSpaceConfigurationTypeDef",
    "SpellCorrectedQueryTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateFaqRequestRequestTypeDef",
    "CreateQuerySuggestionsBlockListRequestRequestTypeDef",
    "CreateThesaurusRequestRequestTypeDef",
    "DescribeFaqResponseTypeDef",
    "DescribeQuerySuggestionsBlockListResponseTypeDef",
    "DescribeThesaurusResponseTypeDef",
    "OnPremiseConfigurationTypeDef",
    "OneDriveUsersTypeDef",
    "SharePointConfigurationTypeDef",
    "UpdateQuerySuggestionsBlockListRequestRequestTypeDef",
    "UpdateThesaurusRequestRequestTypeDef",
    "UserContextTypeDef",
    "ListDataSourcesResponseTypeDef",
    "DataSourceSyncJobTypeDef",
    "ExperiencesSummaryTypeDef",
    "DescribePrincipalMappingResponseTypeDef",
    "DocumentAttributeConditionTypeDef",
    "DocumentAttributeTargetTypeDef",
    "DocumentAttributeTypeDef",
    "DocumentAttributeValueCountPairTypeDef",
    "DocumentRelevanceConfigurationTypeDef",
    "DocumentMetadataConfigurationTypeDef",
    "HierarchicalPrincipalTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "ExperienceEntitiesSummaryTypeDef",
    "ExperienceConfigurationTypeDef",
    "ListFaqsResponseTypeDef",
    "GetSnapshotsResponseTypeDef",
    "ListDataSourceSyncJobsRequestRequestTypeDef",
    "GroupMembersTypeDef",
    "ListGroupsOlderThanOrderingIdResponseTypeDef",
    "TextWithHighlightsTypeDef",
    "ListIndicesResponseTypeDef",
    "IndexStatisticsTypeDef",
    "UserTokenConfigurationTypeDef",
    "ListEntityPersonasResponseTypeDef",
    "ListQuerySuggestionsBlockListsResponseTypeDef",
    "ListThesauriResponseTypeDef",
    "SubmitFeedbackRequestRequestTypeDef",
    "UrlsTypeDef",
    "SuggestionTextWithHighlightsTypeDef",
    "DatabaseConfigurationTypeDef",
    "SalesforceKnowledgeArticleConfigurationTypeDef",
    "ServiceNowConfigurationTypeDef",
    "ConfluenceConfigurationTypeDef",
    "GitHubConfigurationTypeDef",
    "OneDriveConfigurationTypeDef",
    "ListDataSourceSyncJobsResponseTypeDef",
    "ListExperiencesResponseTypeDef",
    "HookConfigurationTypeDef",
    "InlineCustomDocumentEnrichmentConfigurationTypeDef",
    "AttributeFilterTypeDef",
    "DocumentInfoTypeDef",
    "QueryRequestRequestTypeDef",
    "DocumentTypeDef",
    "ListExperienceEntitiesResponseTypeDef",
    "CreateExperienceRequestRequestTypeDef",
    "DescribeExperienceResponseTypeDef",
    "UpdateExperienceRequestRequestTypeDef",
    "PutPrincipalMappingRequestRequestTypeDef",
    "AdditionalResultAttributeValueTypeDef",
    "CreateIndexRequestRequestTypeDef",
    "DescribeIndexResponseTypeDef",
    "UpdateIndexRequestRequestTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "SuggestionValueTypeDef",
    "SalesforceConfigurationTypeDef",
    "CustomDocumentEnrichmentConfigurationTypeDef",
    "BatchGetDocumentStatusRequestRequestTypeDef",
    "AdditionalResultAttributeTypeDef",
    "SuggestionTypeDef",
    "DataSourceConfigurationTypeDef",
    "BatchPutDocumentRequestRequestTypeDef",
    "QueryResultItemTypeDef",
    "GetQuerySuggestionsResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "QueryResultTypeDef",
)

AccessControlListConfigurationTypeDef = TypedDict(
    "AccessControlListConfigurationTypeDef",
    {
        "KeyPath": str,
    },
    total=False,
)

AclConfigurationTypeDef = TypedDict(
    "AclConfigurationTypeDef",
    {
        "AllowedGroupsColumnName": str,
    },
)

EntityConfigurationTypeDef = TypedDict(
    "EntityConfigurationTypeDef",
    {
        "EntityId": str,
        "EntityType": EntityTypeType,
    },
)

FailedEntityTypeDef = TypedDict(
    "FailedEntityTypeDef",
    {
        "EntityId": str,
        "ErrorMessage": str,
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

EntityPersonaConfigurationTypeDef = TypedDict(
    "EntityPersonaConfigurationTypeDef",
    {
        "EntityId": str,
        "Persona": PersonaType,
    },
)

BasicAuthenticationConfigurationTypeDef = TypedDict(
    "BasicAuthenticationConfigurationTypeDef",
    {
        "Host": str,
        "Port": int,
        "Credentials": str,
    },
)

_RequiredDataSourceSyncJobMetricTargetTypeDef = TypedDict(
    "_RequiredDataSourceSyncJobMetricTargetTypeDef",
    {
        "DataSourceId": str,
    },
)
_OptionalDataSourceSyncJobMetricTargetTypeDef = TypedDict(
    "_OptionalDataSourceSyncJobMetricTargetTypeDef",
    {
        "DataSourceSyncJobId": str,
    },
    total=False,
)

class DataSourceSyncJobMetricTargetTypeDef(
    _RequiredDataSourceSyncJobMetricTargetTypeDef, _OptionalDataSourceSyncJobMetricTargetTypeDef
):
    pass

BatchDeleteDocumentResponseFailedDocumentTypeDef = TypedDict(
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    {
        "Id": str,
        "ErrorCode": ErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

BatchGetDocumentStatusResponseErrorTypeDef = TypedDict(
    "BatchGetDocumentStatusResponseErrorTypeDef",
    {
        "DocumentId": str,
        "ErrorCode": ErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

StatusTypeDef = TypedDict(
    "StatusTypeDef",
    {
        "DocumentId": str,
        "DocumentStatus": DocumentStatusType,
        "FailureCode": str,
        "FailureReason": str,
    },
    total=False,
)

BatchPutDocumentResponseFailedDocumentTypeDef = TypedDict(
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    {
        "Id": str,
        "ErrorCode": ErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredDataSourceToIndexFieldMappingTypeDef = TypedDict(
    "_RequiredDataSourceToIndexFieldMappingTypeDef",
    {
        "DataSourceFieldName": str,
        "IndexFieldName": str,
    },
)
_OptionalDataSourceToIndexFieldMappingTypeDef = TypedDict(
    "_OptionalDataSourceToIndexFieldMappingTypeDef",
    {
        "DateFieldFormat": str,
    },
    total=False,
)

class DataSourceToIndexFieldMappingTypeDef(
    _RequiredDataSourceToIndexFieldMappingTypeDef, _OptionalDataSourceToIndexFieldMappingTypeDef
):
    pass

DataSourceVpcConfigurationTypeDef = TypedDict(
    "DataSourceVpcConfigurationTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
)

CapacityUnitsConfigurationTypeDef = TypedDict(
    "CapacityUnitsConfigurationTypeDef",
    {
        "StorageCapacityUnits": int,
        "QueryCapacityUnits": int,
    },
)

ClearQuerySuggestionsRequestRequestTypeDef = TypedDict(
    "ClearQuerySuggestionsRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)

ClickFeedbackTypeDef = TypedDict(
    "ClickFeedbackTypeDef",
    {
        "ResultId": str,
        "ClickTime": Union[datetime, str],
    },
)

ConfluenceAttachmentToIndexFieldMappingTypeDef = TypedDict(
    "ConfluenceAttachmentToIndexFieldMappingTypeDef",
    {
        "DataSourceFieldName": ConfluenceAttachmentFieldNameType,
        "DateFieldFormat": str,
        "IndexFieldName": str,
    },
    total=False,
)

ConfluenceBlogToIndexFieldMappingTypeDef = TypedDict(
    "ConfluenceBlogToIndexFieldMappingTypeDef",
    {
        "DataSourceFieldName": ConfluenceBlogFieldNameType,
        "DateFieldFormat": str,
        "IndexFieldName": str,
    },
    total=False,
)

ConfluencePageToIndexFieldMappingTypeDef = TypedDict(
    "ConfluencePageToIndexFieldMappingTypeDef",
    {
        "DataSourceFieldName": ConfluencePageFieldNameType,
        "DateFieldFormat": str,
        "IndexFieldName": str,
    },
    total=False,
)

ConfluenceSpaceToIndexFieldMappingTypeDef = TypedDict(
    "ConfluenceSpaceToIndexFieldMappingTypeDef",
    {
        "DataSourceFieldName": ConfluenceSpaceFieldNameType,
        "DateFieldFormat": str,
        "IndexFieldName": str,
    },
    total=False,
)

ConnectionConfigurationTypeDef = TypedDict(
    "ConnectionConfigurationTypeDef",
    {
        "DatabaseHost": str,
        "DatabasePort": int,
        "DatabaseName": str,
        "TableName": str,
        "SecretArn": str,
    },
)

ContentSourceConfigurationTypeDef = TypedDict(
    "ContentSourceConfigurationTypeDef",
    {
        "DataSourceIds": Sequence[str],
        "FaqIds": Sequence[str],
        "DirectPutContent": bool,
    },
    total=False,
)

CorrectionTypeDef = TypedDict(
    "CorrectionTypeDef",
    {
        "BeginOffset": int,
        "EndOffset": int,
        "Term": str,
        "CorrectedTerm": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

S3PathTypeDef = TypedDict(
    "S3PathTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

UserGroupResolutionConfigurationTypeDef = TypedDict(
    "UserGroupResolutionConfigurationTypeDef",
    {
        "UserGroupResolutionMode": UserGroupResolutionModeType,
    },
)

DataSourceGroupTypeDef = TypedDict(
    "DataSourceGroupTypeDef",
    {
        "GroupId": str,
        "DataSourceId": str,
    },
)

DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Type": DataSourceTypeType,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": DataSourceStatusType,
        "LanguageCode": str,
    },
    total=False,
)

DataSourceSyncJobMetricsTypeDef = TypedDict(
    "DataSourceSyncJobMetricsTypeDef",
    {
        "DocumentsAdded": str,
        "DocumentsModified": str,
        "DocumentsDeleted": str,
        "DocumentsFailed": str,
        "DocumentsScanned": str,
    },
    total=False,
)

SqlConfigurationTypeDef = TypedDict(
    "SqlConfigurationTypeDef",
    {
        "QueryIdentifiersEnclosingOption": QueryIdentifiersEnclosingOptionType,
    },
    total=False,
)

DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DeleteExperienceRequestRequestTypeDef = TypedDict(
    "DeleteExperienceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DeleteFaqRequestRequestTypeDef = TypedDict(
    "DeleteFaqRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DeleteIndexRequestRequestTypeDef = TypedDict(
    "DeleteIndexRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredDeletePrincipalMappingRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePrincipalMappingRequestRequestTypeDef",
    {
        "IndexId": str,
        "GroupId": str,
    },
)
_OptionalDeletePrincipalMappingRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePrincipalMappingRequestRequestTypeDef",
    {
        "DataSourceId": str,
        "OrderingId": int,
    },
    total=False,
)

class DeletePrincipalMappingRequestRequestTypeDef(
    _RequiredDeletePrincipalMappingRequestRequestTypeDef,
    _OptionalDeletePrincipalMappingRequestRequestTypeDef,
):
    pass

DeleteQuerySuggestionsBlockListRequestRequestTypeDef = TypedDict(
    "DeleteQuerySuggestionsBlockListRequestRequestTypeDef",
    {
        "IndexId": str,
        "Id": str,
    },
)

DeleteThesaurusRequestRequestTypeDef = TypedDict(
    "DeleteThesaurusRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DescribeDataSourceRequestRequestTypeDef = TypedDict(
    "DescribeDataSourceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DescribeExperienceRequestRequestTypeDef = TypedDict(
    "DescribeExperienceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

ExperienceEndpointTypeDef = TypedDict(
    "ExperienceEndpointTypeDef",
    {
        "EndpointType": Literal["HOME"],
        "Endpoint": str,
    },
    total=False,
)

DescribeFaqRequestRequestTypeDef = TypedDict(
    "DescribeFaqRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DescribeIndexRequestRequestTypeDef = TypedDict(
    "DescribeIndexRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredDescribePrincipalMappingRequestRequestTypeDef = TypedDict(
    "_RequiredDescribePrincipalMappingRequestRequestTypeDef",
    {
        "IndexId": str,
        "GroupId": str,
    },
)
_OptionalDescribePrincipalMappingRequestRequestTypeDef = TypedDict(
    "_OptionalDescribePrincipalMappingRequestRequestTypeDef",
    {
        "DataSourceId": str,
    },
    total=False,
)

class DescribePrincipalMappingRequestRequestTypeDef(
    _RequiredDescribePrincipalMappingRequestRequestTypeDef,
    _OptionalDescribePrincipalMappingRequestRequestTypeDef,
):
    pass

GroupOrderingIdSummaryTypeDef = TypedDict(
    "GroupOrderingIdSummaryTypeDef",
    {
        "Status": PrincipalMappingStatusType,
        "LastUpdatedAt": datetime,
        "ReceivedAt": datetime,
        "OrderingId": int,
        "FailureReason": str,
    },
    total=False,
)

DescribeQuerySuggestionsBlockListRequestRequestTypeDef = TypedDict(
    "DescribeQuerySuggestionsBlockListRequestRequestTypeDef",
    {
        "IndexId": str,
        "Id": str,
    },
)

DescribeQuerySuggestionsConfigRequestRequestTypeDef = TypedDict(
    "DescribeQuerySuggestionsConfigRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)

DescribeThesaurusRequestRequestTypeDef = TypedDict(
    "DescribeThesaurusRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

DisassociatePersonasFromEntitiesRequestRequestTypeDef = TypedDict(
    "DisassociatePersonasFromEntitiesRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "EntityIds": Sequence[str],
    },
)

DocumentAttributeValueTypeDef = TypedDict(
    "DocumentAttributeValueTypeDef",
    {
        "StringValue": str,
        "StringListValue": Sequence[str],
        "LongValue": int,
        "DateValue": Union[datetime, str],
    },
    total=False,
)

RelevanceTypeDef = TypedDict(
    "RelevanceTypeDef",
    {
        "Freshness": bool,
        "Importance": int,
        "Duration": str,
        "RankOrder": OrderType,
        "ValueImportanceMap": Dict[str, int],
    },
    total=False,
)

SearchTypeDef = TypedDict(
    "SearchTypeDef",
    {
        "Facetable": bool,
        "Searchable": bool,
        "Displayable": bool,
        "Sortable": bool,
    },
    total=False,
)

_RequiredPrincipalTypeDef = TypedDict(
    "_RequiredPrincipalTypeDef",
    {
        "Name": str,
        "Type": PrincipalTypeType,
        "Access": ReadAccessTypeType,
    },
)
_OptionalPrincipalTypeDef = TypedDict(
    "_OptionalPrincipalTypeDef",
    {
        "DataSourceId": str,
    },
    total=False,
)

class PrincipalTypeDef(_RequiredPrincipalTypeDef, _OptionalPrincipalTypeDef):
    pass

DocumentsMetadataConfigurationTypeDef = TypedDict(
    "DocumentsMetadataConfigurationTypeDef",
    {
        "S3Prefix": str,
    },
    total=False,
)

EntityDisplayDataTypeDef = TypedDict(
    "EntityDisplayDataTypeDef",
    {
        "UserName": str,
        "GroupName": str,
        "IdentifiedUserName": str,
        "FirstName": str,
        "LastName": str,
    },
    total=False,
)

UserIdentityConfigurationTypeDef = TypedDict(
    "UserIdentityConfigurationTypeDef",
    {
        "IdentityAttributeName": str,
    },
    total=False,
)

FacetResultTypeDef = TypedDict(
    "FacetResultTypeDef",
    {
        "DocumentAttributeKey": str,
        "DocumentAttributeValueType": DocumentAttributeValueTypeType,
        "DocumentAttributeValueCountPairs": List[Dict[str, Any]],
    },
    total=False,
)

FacetTypeDef = TypedDict(
    "FacetTypeDef",
    {
        "DocumentAttributeKey": str,
        "Facets": Sequence[Dict[str, Any]],
        "MaxResults": int,
    },
    total=False,
)

FaqStatisticsTypeDef = TypedDict(
    "FaqStatisticsTypeDef",
    {
        "IndexedQuestionAnswersCount": int,
    },
)

FaqSummaryTypeDef = TypedDict(
    "FaqSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": FaqStatusType,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "FileFormat": FaqFileFormatType,
        "LanguageCode": str,
    },
    total=False,
)

_RequiredGetQuerySuggestionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetQuerySuggestionsRequestRequestTypeDef",
    {
        "IndexId": str,
        "QueryText": str,
    },
)
_OptionalGetQuerySuggestionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetQuerySuggestionsRequestRequestTypeDef",
    {
        "MaxSuggestionsCount": int,
    },
    total=False,
)

class GetQuerySuggestionsRequestRequestTypeDef(
    _RequiredGetQuerySuggestionsRequestRequestTypeDef,
    _OptionalGetQuerySuggestionsRequestRequestTypeDef,
):
    pass

_RequiredGetSnapshotsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSnapshotsRequestRequestTypeDef",
    {
        "IndexId": str,
        "Interval": IntervalType,
        "MetricType": MetricTypeType,
    },
)
_OptionalGetSnapshotsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSnapshotsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class GetSnapshotsRequestRequestTypeDef(
    _RequiredGetSnapshotsRequestRequestTypeDef, _OptionalGetSnapshotsRequestRequestTypeDef
):
    pass

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

GitHubDocumentCrawlPropertiesTypeDef = TypedDict(
    "GitHubDocumentCrawlPropertiesTypeDef",
    {
        "CrawlRepositoryDocuments": bool,
        "CrawlIssue": bool,
        "CrawlIssueComment": bool,
        "CrawlIssueCommentAttachment": bool,
        "CrawlPullRequest": bool,
        "CrawlPullRequestComment": bool,
        "CrawlPullRequestCommentAttachment": bool,
    },
    total=False,
)

SaaSConfigurationTypeDef = TypedDict(
    "SaaSConfigurationTypeDef",
    {
        "OrganizationName": str,
        "HostUrl": str,
    },
)

_RequiredMemberGroupTypeDef = TypedDict(
    "_RequiredMemberGroupTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalMemberGroupTypeDef = TypedDict(
    "_OptionalMemberGroupTypeDef",
    {
        "DataSourceId": str,
    },
    total=False,
)

class MemberGroupTypeDef(_RequiredMemberGroupTypeDef, _OptionalMemberGroupTypeDef):
    pass

MemberUserTypeDef = TypedDict(
    "MemberUserTypeDef",
    {
        "UserId": str,
    },
)

GroupSummaryTypeDef = TypedDict(
    "GroupSummaryTypeDef",
    {
        "GroupId": str,
        "OrderingId": int,
    },
    total=False,
)

_RequiredHighlightTypeDef = TypedDict(
    "_RequiredHighlightTypeDef",
    {
        "BeginOffset": int,
        "EndOffset": int,
    },
)
_OptionalHighlightTypeDef = TypedDict(
    "_OptionalHighlightTypeDef",
    {
        "TopAnswer": bool,
        "Type": HighlightTypeType,
    },
    total=False,
)

class HighlightTypeDef(_RequiredHighlightTypeDef, _OptionalHighlightTypeDef):
    pass

_RequiredIndexConfigurationSummaryTypeDef = TypedDict(
    "_RequiredIndexConfigurationSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": IndexStatusType,
    },
)
_OptionalIndexConfigurationSummaryTypeDef = TypedDict(
    "_OptionalIndexConfigurationSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Edition": IndexEditionType,
    },
    total=False,
)

class IndexConfigurationSummaryTypeDef(
    _RequiredIndexConfigurationSummaryTypeDef, _OptionalIndexConfigurationSummaryTypeDef
):
    pass

TextDocumentStatisticsTypeDef = TypedDict(
    "TextDocumentStatisticsTypeDef",
    {
        "IndexedTextDocumentsCount": int,
        "IndexedTextBytes": int,
    },
)

JsonTokenTypeConfigurationTypeDef = TypedDict(
    "JsonTokenTypeConfigurationTypeDef",
    {
        "UserNameAttributeField": str,
        "GroupAttributeField": str,
    },
)

_RequiredJwtTokenTypeConfigurationTypeDef = TypedDict(
    "_RequiredJwtTokenTypeConfigurationTypeDef",
    {
        "KeyLocation": KeyLocationType,
    },
)
_OptionalJwtTokenTypeConfigurationTypeDef = TypedDict(
    "_OptionalJwtTokenTypeConfigurationTypeDef",
    {
        "URL": str,
        "SecretManagerArn": str,
        "UserNameAttributeField": str,
        "GroupAttributeField": str,
        "Issuer": str,
        "ClaimRegex": str,
    },
    total=False,
)

class JwtTokenTypeConfigurationTypeDef(
    _RequiredJwtTokenTypeConfigurationTypeDef, _OptionalJwtTokenTypeConfigurationTypeDef
):
    pass

_RequiredListDataSourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSourcesRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalListDataSourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSourcesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListDataSourcesRequestRequestTypeDef(
    _RequiredListDataSourcesRequestRequestTypeDef, _OptionalListDataSourcesRequestRequestTypeDef
):
    pass

_RequiredListEntityPersonasRequestRequestTypeDef = TypedDict(
    "_RequiredListEntityPersonasRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)
_OptionalListEntityPersonasRequestRequestTypeDef = TypedDict(
    "_OptionalListEntityPersonasRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListEntityPersonasRequestRequestTypeDef(
    _RequiredListEntityPersonasRequestRequestTypeDef,
    _OptionalListEntityPersonasRequestRequestTypeDef,
):
    pass

PersonasSummaryTypeDef = TypedDict(
    "PersonasSummaryTypeDef",
    {
        "EntityId": str,
        "Persona": PersonaType,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

_RequiredListExperienceEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredListExperienceEntitiesRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)
_OptionalListExperienceEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalListExperienceEntitiesRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class ListExperienceEntitiesRequestRequestTypeDef(
    _RequiredListExperienceEntitiesRequestRequestTypeDef,
    _OptionalListExperienceEntitiesRequestRequestTypeDef,
):
    pass

_RequiredListExperiencesRequestRequestTypeDef = TypedDict(
    "_RequiredListExperiencesRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalListExperiencesRequestRequestTypeDef = TypedDict(
    "_OptionalListExperiencesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListExperiencesRequestRequestTypeDef(
    _RequiredListExperiencesRequestRequestTypeDef, _OptionalListExperiencesRequestRequestTypeDef
):
    pass

_RequiredListFaqsRequestRequestTypeDef = TypedDict(
    "_RequiredListFaqsRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalListFaqsRequestRequestTypeDef = TypedDict(
    "_OptionalListFaqsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListFaqsRequestRequestTypeDef(
    _RequiredListFaqsRequestRequestTypeDef, _OptionalListFaqsRequestRequestTypeDef
):
    pass

_RequiredListGroupsOlderThanOrderingIdRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupsOlderThanOrderingIdRequestRequestTypeDef",
    {
        "IndexId": str,
        "OrderingId": int,
    },
)
_OptionalListGroupsOlderThanOrderingIdRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupsOlderThanOrderingIdRequestRequestTypeDef",
    {
        "DataSourceId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListGroupsOlderThanOrderingIdRequestRequestTypeDef(
    _RequiredListGroupsOlderThanOrderingIdRequestRequestTypeDef,
    _OptionalListGroupsOlderThanOrderingIdRequestRequestTypeDef,
):
    pass

ListIndicesRequestRequestTypeDef = TypedDict(
    "ListIndicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListQuerySuggestionsBlockListsRequestRequestTypeDef = TypedDict(
    "_RequiredListQuerySuggestionsBlockListsRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalListQuerySuggestionsBlockListsRequestRequestTypeDef = TypedDict(
    "_OptionalListQuerySuggestionsBlockListsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListQuerySuggestionsBlockListsRequestRequestTypeDef(
    _RequiredListQuerySuggestionsBlockListsRequestRequestTypeDef,
    _OptionalListQuerySuggestionsBlockListsRequestRequestTypeDef,
):
    pass

QuerySuggestionsBlockListSummaryTypeDef = TypedDict(
    "QuerySuggestionsBlockListSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": QuerySuggestionsBlockListStatusType,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "ItemCount": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

_RequiredListThesauriRequestRequestTypeDef = TypedDict(
    "_RequiredListThesauriRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalListThesauriRequestRequestTypeDef = TypedDict(
    "_OptionalListThesauriRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListThesauriRequestRequestTypeDef(
    _RequiredListThesauriRequestRequestTypeDef, _OptionalListThesauriRequestRequestTypeDef
):
    pass

ThesaurusSummaryTypeDef = TypedDict(
    "ThesaurusSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": ThesaurusStatusType,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

_RequiredProxyConfigurationTypeDef = TypedDict(
    "_RequiredProxyConfigurationTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)
_OptionalProxyConfigurationTypeDef = TypedDict(
    "_OptionalProxyConfigurationTypeDef",
    {
        "Credentials": str,
    },
    total=False,
)

class ProxyConfigurationTypeDef(
    _RequiredProxyConfigurationTypeDef, _OptionalProxyConfigurationTypeDef
):
    pass

SortingConfigurationTypeDef = TypedDict(
    "SortingConfigurationTypeDef",
    {
        "DocumentAttributeKey": str,
        "SortOrder": SortOrderType,
    },
)

SpellCorrectionConfigurationTypeDef = TypedDict(
    "SpellCorrectionConfigurationTypeDef",
    {
        "IncludeQuerySpellCheckSuggestions": bool,
    },
)

ScoreAttributesTypeDef = TypedDict(
    "ScoreAttributesTypeDef",
    {
        "ScoreConfidence": ScoreConfidenceType,
    },
    total=False,
)

WarningTypeDef = TypedDict(
    "WarningTypeDef",
    {
        "Message": str,
        "Code": Literal["QUERY_LANGUAGE_INVALID_SYNTAX"],
    },
    total=False,
)

RelevanceFeedbackTypeDef = TypedDict(
    "RelevanceFeedbackTypeDef",
    {
        "ResultId": str,
        "RelevanceValue": RelevanceTypeType,
    },
)

_RequiredSeedUrlConfigurationTypeDef = TypedDict(
    "_RequiredSeedUrlConfigurationTypeDef",
    {
        "SeedUrls": Sequence[str],
    },
)
_OptionalSeedUrlConfigurationTypeDef = TypedDict(
    "_OptionalSeedUrlConfigurationTypeDef",
    {
        "WebCrawlerMode": WebCrawlerModeType,
    },
    total=False,
)

class SeedUrlConfigurationTypeDef(
    _RequiredSeedUrlConfigurationTypeDef, _OptionalSeedUrlConfigurationTypeDef
):
    pass

SiteMapsConfigurationTypeDef = TypedDict(
    "SiteMapsConfigurationTypeDef",
    {
        "SiteMaps": Sequence[str],
    },
)

StartDataSourceSyncJobRequestRequestTypeDef = TypedDict(
    "StartDataSourceSyncJobRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

StopDataSourceSyncJobRequestRequestTypeDef = TypedDict(
    "StopDataSourceSyncJobRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)

SuggestionHighlightTypeDef = TypedDict(
    "SuggestionHighlightTypeDef",
    {
        "BeginOffset": int,
        "EndOffset": int,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateQuerySuggestionsConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQuerySuggestionsConfigRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalUpdateQuerySuggestionsConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQuerySuggestionsConfigRequestRequestTypeDef",
    {
        "Mode": ModeType,
        "QueryLogLookBackWindowInDays": int,
        "IncludeQueriesWithoutUserInformation": bool,
        "MinimumNumberOfQueryingUsers": int,
        "MinimumQueryCount": int,
    },
    total=False,
)

class UpdateQuerySuggestionsConfigRequestRequestTypeDef(
    _RequiredUpdateQuerySuggestionsConfigRequestRequestTypeDef,
    _OptionalUpdateQuerySuggestionsConfigRequestRequestTypeDef,
):
    pass

AssociateEntitiesToExperienceRequestRequestTypeDef = TypedDict(
    "AssociateEntitiesToExperienceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "EntityList": Sequence[EntityConfigurationTypeDef],
    },
)

DisassociateEntitiesFromExperienceRequestRequestTypeDef = TypedDict(
    "DisassociateEntitiesFromExperienceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "EntityList": Sequence[EntityConfigurationTypeDef],
    },
)

AssociateEntitiesToExperienceResponseTypeDef = TypedDict(
    "AssociateEntitiesToExperienceResponseTypeDef",
    {
        "FailedEntityList": List[FailedEntityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociatePersonasToEntitiesResponseTypeDef = TypedDict(
    "AssociatePersonasToEntitiesResponseTypeDef",
    {
        "FailedEntityList": List[FailedEntityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExperienceResponseTypeDef = TypedDict(
    "CreateExperienceResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFaqResponseTypeDef = TypedDict(
    "CreateFaqResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIndexResponseTypeDef = TypedDict(
    "CreateIndexResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateQuerySuggestionsBlockListResponseTypeDef = TypedDict(
    "CreateQuerySuggestionsBlockListResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThesaurusResponseTypeDef = TypedDict(
    "CreateThesaurusResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeQuerySuggestionsConfigResponseTypeDef = TypedDict(
    "DescribeQuerySuggestionsConfigResponseTypeDef",
    {
        "Mode": ModeType,
        "Status": QuerySuggestionsStatusType,
        "QueryLogLookBackWindowInDays": int,
        "IncludeQueriesWithoutUserInformation": bool,
        "MinimumNumberOfQueryingUsers": int,
        "MinimumQueryCount": int,
        "LastSuggestionsBuildTime": datetime,
        "LastClearTime": datetime,
        "TotalSuggestionsCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateEntitiesFromExperienceResponseTypeDef = TypedDict(
    "DisassociateEntitiesFromExperienceResponseTypeDef",
    {
        "FailedEntityList": List[FailedEntityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociatePersonasFromEntitiesResponseTypeDef = TypedDict(
    "DisassociatePersonasFromEntitiesResponseTypeDef",
    {
        "FailedEntityList": List[FailedEntityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDataSourceSyncJobResponseTypeDef = TypedDict(
    "StartDataSourceSyncJobResponseTypeDef",
    {
        "ExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociatePersonasToEntitiesRequestRequestTypeDef = TypedDict(
    "AssociatePersonasToEntitiesRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Personas": Sequence[EntityPersonaConfigurationTypeDef],
    },
)

AuthenticationConfigurationTypeDef = TypedDict(
    "AuthenticationConfigurationTypeDef",
    {
        "BasicAuthentication": Sequence[BasicAuthenticationConfigurationTypeDef],
    },
    total=False,
)

_RequiredBatchDeleteDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteDocumentRequestRequestTypeDef",
    {
        "IndexId": str,
        "DocumentIdList": Sequence[str],
    },
)
_OptionalBatchDeleteDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteDocumentRequestRequestTypeDef",
    {
        "DataSourceSyncJobMetricTarget": DataSourceSyncJobMetricTargetTypeDef,
    },
    total=False,
)

class BatchDeleteDocumentRequestRequestTypeDef(
    _RequiredBatchDeleteDocumentRequestRequestTypeDef,
    _OptionalBatchDeleteDocumentRequestRequestTypeDef,
):
    pass

BatchDeleteDocumentResponseTypeDef = TypedDict(
    "BatchDeleteDocumentResponseTypeDef",
    {
        "FailedDocuments": List[BatchDeleteDocumentResponseFailedDocumentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetDocumentStatusResponseTypeDef = TypedDict(
    "BatchGetDocumentStatusResponseTypeDef",
    {
        "Errors": List[BatchGetDocumentStatusResponseErrorTypeDef],
        "DocumentStatusList": List[StatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutDocumentResponseTypeDef = TypedDict(
    "BatchPutDocumentResponseTypeDef",
    {
        "FailedDocuments": List[BatchPutDocumentResponseFailedDocumentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredColumnConfigurationTypeDef = TypedDict(
    "_RequiredColumnConfigurationTypeDef",
    {
        "DocumentIdColumnName": str,
        "DocumentDataColumnName": str,
        "ChangeDetectingColumns": Sequence[str],
    },
)
_OptionalColumnConfigurationTypeDef = TypedDict(
    "_OptionalColumnConfigurationTypeDef",
    {
        "DocumentTitleColumnName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class ColumnConfigurationTypeDef(
    _RequiredColumnConfigurationTypeDef, _OptionalColumnConfigurationTypeDef
):
    pass

_RequiredGoogleDriveConfigurationTypeDef = TypedDict(
    "_RequiredGoogleDriveConfigurationTypeDef",
    {
        "SecretArn": str,
    },
)
_OptionalGoogleDriveConfigurationTypeDef = TypedDict(
    "_OptionalGoogleDriveConfigurationTypeDef",
    {
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "ExcludeMimeTypes": Sequence[str],
        "ExcludeUserAccounts": Sequence[str],
        "ExcludeSharedDrives": Sequence[str],
    },
    total=False,
)

class GoogleDriveConfigurationTypeDef(
    _RequiredGoogleDriveConfigurationTypeDef, _OptionalGoogleDriveConfigurationTypeDef
):
    pass

_RequiredSalesforceChatterFeedConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceChatterFeedConfigurationTypeDef",
    {
        "DocumentDataFieldName": str,
    },
)
_OptionalSalesforceChatterFeedConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceChatterFeedConfigurationTypeDef",
    {
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "IncludeFilterTypes": Sequence[SalesforceChatterFeedIncludeFilterTypeType],
    },
    total=False,
)

class SalesforceChatterFeedConfigurationTypeDef(
    _RequiredSalesforceChatterFeedConfigurationTypeDef,
    _OptionalSalesforceChatterFeedConfigurationTypeDef,
):
    pass

_RequiredSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    {
        "Name": str,
        "DocumentDataFieldName": str,
    },
)
_OptionalSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    {
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef(
    _RequiredSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef,
    _OptionalSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef,
):
    pass

_RequiredSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    {
        "DocumentDataFieldName": str,
    },
)
_OptionalSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    {
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef(
    _RequiredSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
    _OptionalSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
):
    pass

SalesforceStandardObjectAttachmentConfigurationTypeDef = TypedDict(
    "SalesforceStandardObjectAttachmentConfigurationTypeDef",
    {
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

_RequiredSalesforceStandardObjectConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceStandardObjectConfigurationTypeDef",
    {
        "Name": SalesforceStandardObjectNameType,
        "DocumentDataFieldName": str,
    },
)
_OptionalSalesforceStandardObjectConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceStandardObjectConfigurationTypeDef",
    {
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class SalesforceStandardObjectConfigurationTypeDef(
    _RequiredSalesforceStandardObjectConfigurationTypeDef,
    _OptionalSalesforceStandardObjectConfigurationTypeDef,
):
    pass

_RequiredServiceNowKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_RequiredServiceNowKnowledgeArticleConfigurationTypeDef",
    {
        "DocumentDataFieldName": str,
    },
)
_OptionalServiceNowKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_OptionalServiceNowKnowledgeArticleConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "IncludeAttachmentFilePatterns": Sequence[str],
        "ExcludeAttachmentFilePatterns": Sequence[str],
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "FilterQuery": str,
    },
    total=False,
)

class ServiceNowKnowledgeArticleConfigurationTypeDef(
    _RequiredServiceNowKnowledgeArticleConfigurationTypeDef,
    _OptionalServiceNowKnowledgeArticleConfigurationTypeDef,
):
    pass

_RequiredServiceNowServiceCatalogConfigurationTypeDef = TypedDict(
    "_RequiredServiceNowServiceCatalogConfigurationTypeDef",
    {
        "DocumentDataFieldName": str,
    },
)
_OptionalServiceNowServiceCatalogConfigurationTypeDef = TypedDict(
    "_OptionalServiceNowServiceCatalogConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "IncludeAttachmentFilePatterns": Sequence[str],
        "ExcludeAttachmentFilePatterns": Sequence[str],
        "DocumentTitleFieldName": str,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class ServiceNowServiceCatalogConfigurationTypeDef(
    _RequiredServiceNowServiceCatalogConfigurationTypeDef,
    _OptionalServiceNowServiceCatalogConfigurationTypeDef,
):
    pass

_RequiredWorkDocsConfigurationTypeDef = TypedDict(
    "_RequiredWorkDocsConfigurationTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalWorkDocsConfigurationTypeDef = TypedDict(
    "_OptionalWorkDocsConfigurationTypeDef",
    {
        "CrawlComments": bool,
        "UseChangeLog": bool,
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class WorkDocsConfigurationTypeDef(
    _RequiredWorkDocsConfigurationTypeDef, _OptionalWorkDocsConfigurationTypeDef
):
    pass

_RequiredBoxConfigurationTypeDef = TypedDict(
    "_RequiredBoxConfigurationTypeDef",
    {
        "EnterpriseId": str,
        "SecretArn": str,
    },
)
_OptionalBoxConfigurationTypeDef = TypedDict(
    "_OptionalBoxConfigurationTypeDef",
    {
        "UseChangeLog": bool,
        "CrawlComments": bool,
        "CrawlTasks": bool,
        "CrawlWebLinks": bool,
        "FileFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "TaskFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "CommentFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "WebLinkFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
    },
    total=False,
)

class BoxConfigurationTypeDef(_RequiredBoxConfigurationTypeDef, _OptionalBoxConfigurationTypeDef):
    pass

_RequiredFsxConfigurationTypeDef = TypedDict(
    "_RequiredFsxConfigurationTypeDef",
    {
        "FileSystemId": str,
        "FileSystemType": Literal["WINDOWS"],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
    },
)
_OptionalFsxConfigurationTypeDef = TypedDict(
    "_OptionalFsxConfigurationTypeDef",
    {
        "SecretArn": str,
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class FsxConfigurationTypeDef(_RequiredFsxConfigurationTypeDef, _OptionalFsxConfigurationTypeDef):
    pass

_RequiredJiraConfigurationTypeDef = TypedDict(
    "_RequiredJiraConfigurationTypeDef",
    {
        "JiraAccountUrl": str,
        "SecretArn": str,
    },
)
_OptionalJiraConfigurationTypeDef = TypedDict(
    "_OptionalJiraConfigurationTypeDef",
    {
        "UseChangeLog": bool,
        "Project": Sequence[str],
        "IssueType": Sequence[str],
        "Status": Sequence[str],
        "IssueSubEntityFilter": Sequence[IssueSubEntityType],
        "AttachmentFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "CommentFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "IssueFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "ProjectFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "WorkLogFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
    },
    total=False,
)

class JiraConfigurationTypeDef(
    _RequiredJiraConfigurationTypeDef, _OptionalJiraConfigurationTypeDef
):
    pass

_RequiredQuipConfigurationTypeDef = TypedDict(
    "_RequiredQuipConfigurationTypeDef",
    {
        "Domain": str,
        "SecretArn": str,
    },
)
_OptionalQuipConfigurationTypeDef = TypedDict(
    "_OptionalQuipConfigurationTypeDef",
    {
        "CrawlFileComments": bool,
        "CrawlChatRooms": bool,
        "CrawlAttachments": bool,
        "FolderIds": Sequence[str],
        "ThreadFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "MessageFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "AttachmentFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
    },
    total=False,
)

class QuipConfigurationTypeDef(
    _RequiredQuipConfigurationTypeDef, _OptionalQuipConfigurationTypeDef
):
    pass

_RequiredSlackConfigurationTypeDef = TypedDict(
    "_RequiredSlackConfigurationTypeDef",
    {
        "TeamId": str,
        "SecretArn": str,
        "SlackEntityList": Sequence[SlackEntityType],
        "SinceCrawlDate": str,
    },
)
_OptionalSlackConfigurationTypeDef = TypedDict(
    "_OptionalSlackConfigurationTypeDef",
    {
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "UseChangeLog": bool,
        "CrawlBotMessage": bool,
        "ExcludeArchived": bool,
        "LookBackPeriod": int,
        "PrivateChannelFilter": Sequence[str],
        "PublicChannelFilter": Sequence[str],
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)

class SlackConfigurationTypeDef(
    _RequiredSlackConfigurationTypeDef, _OptionalSlackConfigurationTypeDef
):
    pass

ConfluenceAttachmentConfigurationTypeDef = TypedDict(
    "ConfluenceAttachmentConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "AttachmentFieldMappings": Sequence[ConfluenceAttachmentToIndexFieldMappingTypeDef],
    },
    total=False,
)

ConfluenceBlogConfigurationTypeDef = TypedDict(
    "ConfluenceBlogConfigurationTypeDef",
    {
        "BlogFieldMappings": Sequence[ConfluenceBlogToIndexFieldMappingTypeDef],
    },
    total=False,
)

ConfluencePageConfigurationTypeDef = TypedDict(
    "ConfluencePageConfigurationTypeDef",
    {
        "PageFieldMappings": Sequence[ConfluencePageToIndexFieldMappingTypeDef],
    },
    total=False,
)

ConfluenceSpaceConfigurationTypeDef = TypedDict(
    "ConfluenceSpaceConfigurationTypeDef",
    {
        "CrawlPersonalSpaces": bool,
        "CrawlArchivedSpaces": bool,
        "IncludeSpaces": Sequence[str],
        "ExcludeSpaces": Sequence[str],
        "SpaceFieldMappings": Sequence[ConfluenceSpaceToIndexFieldMappingTypeDef],
    },
    total=False,
)

SpellCorrectedQueryTypeDef = TypedDict(
    "SpellCorrectedQueryTypeDef",
    {
        "SuggestedQueryText": str,
        "Corrections": List[CorrectionTypeDef],
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateFaqRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFaqRequestRequestTypeDef",
    {
        "IndexId": str,
        "Name": str,
        "S3Path": S3PathTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateFaqRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFaqRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "FileFormat": FaqFileFormatType,
        "ClientToken": str,
        "LanguageCode": str,
    },
    total=False,
)

class CreateFaqRequestRequestTypeDef(
    _RequiredCreateFaqRequestRequestTypeDef, _OptionalCreateFaqRequestRequestTypeDef
):
    pass

_RequiredCreateQuerySuggestionsBlockListRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQuerySuggestionsBlockListRequestRequestTypeDef",
    {
        "IndexId": str,
        "Name": str,
        "SourceS3Path": S3PathTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateQuerySuggestionsBlockListRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQuerySuggestionsBlockListRequestRequestTypeDef",
    {
        "Description": str,
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateQuerySuggestionsBlockListRequestRequestTypeDef(
    _RequiredCreateQuerySuggestionsBlockListRequestRequestTypeDef,
    _OptionalCreateQuerySuggestionsBlockListRequestRequestTypeDef,
):
    pass

_RequiredCreateThesaurusRequestRequestTypeDef = TypedDict(
    "_RequiredCreateThesaurusRequestRequestTypeDef",
    {
        "IndexId": str,
        "Name": str,
        "RoleArn": str,
        "SourceS3Path": S3PathTypeDef,
    },
)
_OptionalCreateThesaurusRequestRequestTypeDef = TypedDict(
    "_OptionalCreateThesaurusRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
    },
    total=False,
)

class CreateThesaurusRequestRequestTypeDef(
    _RequiredCreateThesaurusRequestRequestTypeDef, _OptionalCreateThesaurusRequestRequestTypeDef
):
    pass

DescribeFaqResponseTypeDef = TypedDict(
    "DescribeFaqResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Description": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "S3Path": S3PathTypeDef,
        "Status": FaqStatusType,
        "RoleArn": str,
        "ErrorMessage": str,
        "FileFormat": FaqFileFormatType,
        "LanguageCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeQuerySuggestionsBlockListResponseTypeDef = TypedDict(
    "DescribeQuerySuggestionsBlockListResponseTypeDef",
    {
        "IndexId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "Status": QuerySuggestionsBlockListStatusType,
        "ErrorMessage": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "SourceS3Path": S3PathTypeDef,
        "ItemCount": int,
        "FileSizeBytes": int,
        "RoleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThesaurusResponseTypeDef = TypedDict(
    "DescribeThesaurusResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Description": str,
        "Status": ThesaurusStatusType,
        "ErrorMessage": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "RoleArn": str,
        "SourceS3Path": S3PathTypeDef,
        "FileSizeBytes": int,
        "TermCount": int,
        "SynonymRuleCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OnPremiseConfigurationTypeDef = TypedDict(
    "OnPremiseConfigurationTypeDef",
    {
        "HostUrl": str,
        "OrganizationName": str,
        "SslCertificateS3Path": S3PathTypeDef,
    },
)

OneDriveUsersTypeDef = TypedDict(
    "OneDriveUsersTypeDef",
    {
        "OneDriveUserList": Sequence[str],
        "OneDriveUserS3Path": S3PathTypeDef,
    },
    total=False,
)

_RequiredSharePointConfigurationTypeDef = TypedDict(
    "_RequiredSharePointConfigurationTypeDef",
    {
        "SharePointVersion": SharePointVersionType,
        "Urls": Sequence[str],
        "SecretArn": str,
    },
)
_OptionalSharePointConfigurationTypeDef = TypedDict(
    "_OptionalSharePointConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "UseChangeLog": bool,
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "DocumentTitleFieldName": str,
        "DisableLocalGroups": bool,
        "SslCertificateS3Path": S3PathTypeDef,
    },
    total=False,
)

class SharePointConfigurationTypeDef(
    _RequiredSharePointConfigurationTypeDef, _OptionalSharePointConfigurationTypeDef
):
    pass

_RequiredUpdateQuerySuggestionsBlockListRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQuerySuggestionsBlockListRequestRequestTypeDef",
    {
        "IndexId": str,
        "Id": str,
    },
)
_OptionalUpdateQuerySuggestionsBlockListRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQuerySuggestionsBlockListRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "SourceS3Path": S3PathTypeDef,
        "RoleArn": str,
    },
    total=False,
)

class UpdateQuerySuggestionsBlockListRequestRequestTypeDef(
    _RequiredUpdateQuerySuggestionsBlockListRequestRequestTypeDef,
    _OptionalUpdateQuerySuggestionsBlockListRequestRequestTypeDef,
):
    pass

_RequiredUpdateThesaurusRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThesaurusRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)
_OptionalUpdateThesaurusRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThesaurusRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "RoleArn": str,
        "SourceS3Path": S3PathTypeDef,
    },
    total=False,
)

class UpdateThesaurusRequestRequestTypeDef(
    _RequiredUpdateThesaurusRequestRequestTypeDef, _OptionalUpdateThesaurusRequestRequestTypeDef
):
    pass

UserContextTypeDef = TypedDict(
    "UserContextTypeDef",
    {
        "Token": str,
        "UserId": str,
        "Groups": Sequence[str],
        "DataSourceGroups": Sequence[DataSourceGroupTypeDef],
    },
    total=False,
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "SummaryItems": List[DataSourceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataSourceSyncJobTypeDef = TypedDict(
    "DataSourceSyncJobTypeDef",
    {
        "ExecutionId": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Status": DataSourceSyncJobStatusType,
        "ErrorMessage": str,
        "ErrorCode": ErrorCodeType,
        "DataSourceErrorCode": str,
        "Metrics": DataSourceSyncJobMetricsTypeDef,
    },
    total=False,
)

ExperiencesSummaryTypeDef = TypedDict(
    "ExperiencesSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "CreatedAt": datetime,
        "Status": ExperienceStatusType,
        "Endpoints": List[ExperienceEndpointTypeDef],
    },
    total=False,
)

DescribePrincipalMappingResponseTypeDef = TypedDict(
    "DescribePrincipalMappingResponseTypeDef",
    {
        "IndexId": str,
        "DataSourceId": str,
        "GroupId": str,
        "GroupOrderingIdSummaries": List[GroupOrderingIdSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDocumentAttributeConditionTypeDef = TypedDict(
    "_RequiredDocumentAttributeConditionTypeDef",
    {
        "ConditionDocumentAttributeKey": str,
        "Operator": ConditionOperatorType,
    },
)
_OptionalDocumentAttributeConditionTypeDef = TypedDict(
    "_OptionalDocumentAttributeConditionTypeDef",
    {
        "ConditionOnValue": DocumentAttributeValueTypeDef,
    },
    total=False,
)

class DocumentAttributeConditionTypeDef(
    _RequiredDocumentAttributeConditionTypeDef, _OptionalDocumentAttributeConditionTypeDef
):
    pass

DocumentAttributeTargetTypeDef = TypedDict(
    "DocumentAttributeTargetTypeDef",
    {
        "TargetDocumentAttributeKey": str,
        "TargetDocumentAttributeValueDeletion": bool,
        "TargetDocumentAttributeValue": DocumentAttributeValueTypeDef,
    },
    total=False,
)

DocumentAttributeTypeDef = TypedDict(
    "DocumentAttributeTypeDef",
    {
        "Key": str,
        "Value": DocumentAttributeValueTypeDef,
    },
)

DocumentAttributeValueCountPairTypeDef = TypedDict(
    "DocumentAttributeValueCountPairTypeDef",
    {
        "DocumentAttributeValue": DocumentAttributeValueTypeDef,
        "Count": int,
        "FacetResults": List[Dict[str, Any]],
    },
    total=False,
)

DocumentRelevanceConfigurationTypeDef = TypedDict(
    "DocumentRelevanceConfigurationTypeDef",
    {
        "Name": str,
        "Relevance": RelevanceTypeDef,
    },
)

_RequiredDocumentMetadataConfigurationTypeDef = TypedDict(
    "_RequiredDocumentMetadataConfigurationTypeDef",
    {
        "Name": str,
        "Type": DocumentAttributeValueTypeType,
    },
)
_OptionalDocumentMetadataConfigurationTypeDef = TypedDict(
    "_OptionalDocumentMetadataConfigurationTypeDef",
    {
        "Relevance": RelevanceTypeDef,
        "Search": SearchTypeDef,
    },
    total=False,
)

class DocumentMetadataConfigurationTypeDef(
    _RequiredDocumentMetadataConfigurationTypeDef, _OptionalDocumentMetadataConfigurationTypeDef
):
    pass

HierarchicalPrincipalTypeDef = TypedDict(
    "HierarchicalPrincipalTypeDef",
    {
        "PrincipalList": Sequence[PrincipalTypeDef],
    },
)

_RequiredS3DataSourceConfigurationTypeDef = TypedDict(
    "_RequiredS3DataSourceConfigurationTypeDef",
    {
        "BucketName": str,
    },
)
_OptionalS3DataSourceConfigurationTypeDef = TypedDict(
    "_OptionalS3DataSourceConfigurationTypeDef",
    {
        "InclusionPrefixes": Sequence[str],
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "DocumentsMetadataConfiguration": DocumentsMetadataConfigurationTypeDef,
        "AccessControlListConfiguration": AccessControlListConfigurationTypeDef,
    },
    total=False,
)

class S3DataSourceConfigurationTypeDef(
    _RequiredS3DataSourceConfigurationTypeDef, _OptionalS3DataSourceConfigurationTypeDef
):
    pass

ExperienceEntitiesSummaryTypeDef = TypedDict(
    "ExperienceEntitiesSummaryTypeDef",
    {
        "EntityId": str,
        "EntityType": EntityTypeType,
        "DisplayData": EntityDisplayDataTypeDef,
    },
    total=False,
)

ExperienceConfigurationTypeDef = TypedDict(
    "ExperienceConfigurationTypeDef",
    {
        "ContentSourceConfiguration": ContentSourceConfigurationTypeDef,
        "UserIdentityConfiguration": UserIdentityConfigurationTypeDef,
    },
    total=False,
)

ListFaqsResponseTypeDef = TypedDict(
    "ListFaqsResponseTypeDef",
    {
        "NextToken": str,
        "FaqSummaryItems": List[FaqSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSnapshotsResponseTypeDef = TypedDict(
    "GetSnapshotsResponseTypeDef",
    {
        "SnapShotTimeFilter": TimeRangeTypeDef,
        "SnapshotsDataHeader": List[str],
        "SnapshotsData": List[List[str]],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListDataSourceSyncJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSourceSyncJobsRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)
_OptionalListDataSourceSyncJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSourceSyncJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "StartTimeFilter": TimeRangeTypeDef,
        "StatusFilter": DataSourceSyncJobStatusType,
    },
    total=False,
)

class ListDataSourceSyncJobsRequestRequestTypeDef(
    _RequiredListDataSourceSyncJobsRequestRequestTypeDef,
    _OptionalListDataSourceSyncJobsRequestRequestTypeDef,
):
    pass

GroupMembersTypeDef = TypedDict(
    "GroupMembersTypeDef",
    {
        "MemberGroups": Sequence[MemberGroupTypeDef],
        "MemberUsers": Sequence[MemberUserTypeDef],
        "S3PathforGroupMembers": S3PathTypeDef,
    },
    total=False,
)

ListGroupsOlderThanOrderingIdResponseTypeDef = TypedDict(
    "ListGroupsOlderThanOrderingIdResponseTypeDef",
    {
        "GroupsSummaries": List[GroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TextWithHighlightsTypeDef = TypedDict(
    "TextWithHighlightsTypeDef",
    {
        "Text": str,
        "Highlights": List[HighlightTypeDef],
    },
    total=False,
)

ListIndicesResponseTypeDef = TypedDict(
    "ListIndicesResponseTypeDef",
    {
        "IndexConfigurationSummaryItems": List[IndexConfigurationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IndexStatisticsTypeDef = TypedDict(
    "IndexStatisticsTypeDef",
    {
        "FaqStatistics": FaqStatisticsTypeDef,
        "TextDocumentStatistics": TextDocumentStatisticsTypeDef,
    },
)

UserTokenConfigurationTypeDef = TypedDict(
    "UserTokenConfigurationTypeDef",
    {
        "JwtTokenTypeConfiguration": JwtTokenTypeConfigurationTypeDef,
        "JsonTokenTypeConfiguration": JsonTokenTypeConfigurationTypeDef,
    },
    total=False,
)

ListEntityPersonasResponseTypeDef = TypedDict(
    "ListEntityPersonasResponseTypeDef",
    {
        "SummaryItems": List[PersonasSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQuerySuggestionsBlockListsResponseTypeDef = TypedDict(
    "ListQuerySuggestionsBlockListsResponseTypeDef",
    {
        "BlockListSummaryItems": List[QuerySuggestionsBlockListSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThesauriResponseTypeDef = TypedDict(
    "ListThesauriResponseTypeDef",
    {
        "NextToken": str,
        "ThesaurusSummaryItems": List[ThesaurusSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSubmitFeedbackRequestRequestTypeDef = TypedDict(
    "_RequiredSubmitFeedbackRequestRequestTypeDef",
    {
        "IndexId": str,
        "QueryId": str,
    },
)
_OptionalSubmitFeedbackRequestRequestTypeDef = TypedDict(
    "_OptionalSubmitFeedbackRequestRequestTypeDef",
    {
        "ClickFeedbackItems": Sequence[ClickFeedbackTypeDef],
        "RelevanceFeedbackItems": Sequence[RelevanceFeedbackTypeDef],
    },
    total=False,
)

class SubmitFeedbackRequestRequestTypeDef(
    _RequiredSubmitFeedbackRequestRequestTypeDef, _OptionalSubmitFeedbackRequestRequestTypeDef
):
    pass

UrlsTypeDef = TypedDict(
    "UrlsTypeDef",
    {
        "SeedUrlConfiguration": SeedUrlConfigurationTypeDef,
        "SiteMapsConfiguration": SiteMapsConfigurationTypeDef,
    },
    total=False,
)

SuggestionTextWithHighlightsTypeDef = TypedDict(
    "SuggestionTextWithHighlightsTypeDef",
    {
        "Text": str,
        "Highlights": List[SuggestionHighlightTypeDef],
    },
    total=False,
)

_RequiredDatabaseConfigurationTypeDef = TypedDict(
    "_RequiredDatabaseConfigurationTypeDef",
    {
        "DatabaseEngineType": DatabaseEngineTypeType,
        "ConnectionConfiguration": ConnectionConfigurationTypeDef,
        "ColumnConfiguration": ColumnConfigurationTypeDef,
    },
)
_OptionalDatabaseConfigurationTypeDef = TypedDict(
    "_OptionalDatabaseConfigurationTypeDef",
    {
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "AclConfiguration": AclConfigurationTypeDef,
        "SqlConfiguration": SqlConfigurationTypeDef,
    },
    total=False,
)

class DatabaseConfigurationTypeDef(
    _RequiredDatabaseConfigurationTypeDef, _OptionalDatabaseConfigurationTypeDef
):
    pass

_RequiredSalesforceKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceKnowledgeArticleConfigurationTypeDef",
    {
        "IncludedStates": Sequence[SalesforceKnowledgeArticleStateType],
    },
)
_OptionalSalesforceKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceKnowledgeArticleConfigurationTypeDef",
    {
        "StandardKnowledgeArticleTypeConfiguration": SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
        "CustomKnowledgeArticleTypeConfigurations": Sequence[
            SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef
        ],
    },
    total=False,
)

class SalesforceKnowledgeArticleConfigurationTypeDef(
    _RequiredSalesforceKnowledgeArticleConfigurationTypeDef,
    _OptionalSalesforceKnowledgeArticleConfigurationTypeDef,
):
    pass

_RequiredServiceNowConfigurationTypeDef = TypedDict(
    "_RequiredServiceNowConfigurationTypeDef",
    {
        "HostUrl": str,
        "SecretArn": str,
        "ServiceNowBuildVersion": ServiceNowBuildVersionTypeType,
    },
)
_OptionalServiceNowConfigurationTypeDef = TypedDict(
    "_OptionalServiceNowConfigurationTypeDef",
    {
        "KnowledgeArticleConfiguration": ServiceNowKnowledgeArticleConfigurationTypeDef,
        "ServiceCatalogConfiguration": ServiceNowServiceCatalogConfigurationTypeDef,
        "AuthenticationType": ServiceNowAuthenticationTypeType,
    },
    total=False,
)

class ServiceNowConfigurationTypeDef(
    _RequiredServiceNowConfigurationTypeDef, _OptionalServiceNowConfigurationTypeDef
):
    pass

_RequiredConfluenceConfigurationTypeDef = TypedDict(
    "_RequiredConfluenceConfigurationTypeDef",
    {
        "ServerUrl": str,
        "SecretArn": str,
        "Version": ConfluenceVersionType,
    },
)
_OptionalConfluenceConfigurationTypeDef = TypedDict(
    "_OptionalConfluenceConfigurationTypeDef",
    {
        "SpaceConfiguration": ConfluenceSpaceConfigurationTypeDef,
        "PageConfiguration": ConfluencePageConfigurationTypeDef,
        "BlogConfiguration": ConfluenceBlogConfigurationTypeDef,
        "AttachmentConfiguration": ConfluenceAttachmentConfigurationTypeDef,
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
    },
    total=False,
)

class ConfluenceConfigurationTypeDef(
    _RequiredConfluenceConfigurationTypeDef, _OptionalConfluenceConfigurationTypeDef
):
    pass

_RequiredGitHubConfigurationTypeDef = TypedDict(
    "_RequiredGitHubConfigurationTypeDef",
    {
        "SecretArn": str,
    },
)
_OptionalGitHubConfigurationTypeDef = TypedDict(
    "_OptionalGitHubConfigurationTypeDef",
    {
        "SaaSConfiguration": SaaSConfigurationTypeDef,
        "OnPremiseConfiguration": OnPremiseConfigurationTypeDef,
        "Type": TypeType,
        "UseChangeLog": bool,
        "GitHubDocumentCrawlProperties": GitHubDocumentCrawlPropertiesTypeDef,
        "RepositoryFilter": Sequence[str],
        "InclusionFolderNamePatterns": Sequence[str],
        "InclusionFileTypePatterns": Sequence[str],
        "InclusionFileNamePatterns": Sequence[str],
        "ExclusionFolderNamePatterns": Sequence[str],
        "ExclusionFileTypePatterns": Sequence[str],
        "ExclusionFileNamePatterns": Sequence[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "GitHubRepositoryConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
        "GitHubCommitConfigurationFieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "GitHubIssueDocumentConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
        "GitHubIssueCommentConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
        "GitHubIssueAttachmentConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
        "GitHubPullRequestCommentConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
        "GitHubPullRequestDocumentConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
        "GitHubPullRequestDocumentAttachmentConfigurationFieldMappings": Sequence[
            DataSourceToIndexFieldMappingTypeDef
        ],
    },
    total=False,
)

class GitHubConfigurationTypeDef(
    _RequiredGitHubConfigurationTypeDef, _OptionalGitHubConfigurationTypeDef
):
    pass

_RequiredOneDriveConfigurationTypeDef = TypedDict(
    "_RequiredOneDriveConfigurationTypeDef",
    {
        "TenantDomain": str,
        "SecretArn": str,
        "OneDriveUsers": OneDriveUsersTypeDef,
    },
)
_OptionalOneDriveConfigurationTypeDef = TypedDict(
    "_OptionalOneDriveConfigurationTypeDef",
    {
        "InclusionPatterns": Sequence[str],
        "ExclusionPatterns": Sequence[str],
        "FieldMappings": Sequence[DataSourceToIndexFieldMappingTypeDef],
        "DisableLocalGroups": bool,
    },
    total=False,
)

class OneDriveConfigurationTypeDef(
    _RequiredOneDriveConfigurationTypeDef, _OptionalOneDriveConfigurationTypeDef
):
    pass

ListDataSourceSyncJobsResponseTypeDef = TypedDict(
    "ListDataSourceSyncJobsResponseTypeDef",
    {
        "History": List[DataSourceSyncJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListExperiencesResponseTypeDef = TypedDict(
    "ListExperiencesResponseTypeDef",
    {
        "SummaryItems": List[ExperiencesSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredHookConfigurationTypeDef = TypedDict(
    "_RequiredHookConfigurationTypeDef",
    {
        "LambdaArn": str,
        "S3Bucket": str,
    },
)
_OptionalHookConfigurationTypeDef = TypedDict(
    "_OptionalHookConfigurationTypeDef",
    {
        "InvocationCondition": DocumentAttributeConditionTypeDef,
    },
    total=False,
)

class HookConfigurationTypeDef(
    _RequiredHookConfigurationTypeDef, _OptionalHookConfigurationTypeDef
):
    pass

InlineCustomDocumentEnrichmentConfigurationTypeDef = TypedDict(
    "InlineCustomDocumentEnrichmentConfigurationTypeDef",
    {
        "Condition": DocumentAttributeConditionTypeDef,
        "Target": DocumentAttributeTargetTypeDef,
        "DocumentContentDeletion": bool,
    },
    total=False,
)

AttributeFilterTypeDef = TypedDict(
    "AttributeFilterTypeDef",
    {
        "AndAllFilters": Sequence[Dict[str, Any]],
        "OrAllFilters": Sequence[Dict[str, Any]],
        "NotFilter": Dict[str, Any],
        "EqualsTo": DocumentAttributeTypeDef,
        "ContainsAll": DocumentAttributeTypeDef,
        "ContainsAny": DocumentAttributeTypeDef,
        "GreaterThan": DocumentAttributeTypeDef,
        "GreaterThanOrEquals": DocumentAttributeTypeDef,
        "LessThan": DocumentAttributeTypeDef,
        "LessThanOrEquals": DocumentAttributeTypeDef,
    },
    total=False,
)

_RequiredDocumentInfoTypeDef = TypedDict(
    "_RequiredDocumentInfoTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalDocumentInfoTypeDef = TypedDict(
    "_OptionalDocumentInfoTypeDef",
    {
        "Attributes": Sequence[DocumentAttributeTypeDef],
    },
    total=False,
)

class DocumentInfoTypeDef(_RequiredDocumentInfoTypeDef, _OptionalDocumentInfoTypeDef):
    pass

_RequiredQueryRequestRequestTypeDef = TypedDict(
    "_RequiredQueryRequestRequestTypeDef",
    {
        "IndexId": str,
    },
)
_OptionalQueryRequestRequestTypeDef = TypedDict(
    "_OptionalQueryRequestRequestTypeDef",
    {
        "QueryText": str,
        "AttributeFilter": "AttributeFilterTypeDef",
        "Facets": Sequence["FacetTypeDef"],
        "RequestedDocumentAttributes": Sequence[str],
        "QueryResultTypeFilter": QueryResultTypeType,
        "DocumentRelevanceOverrideConfigurations": Sequence[DocumentRelevanceConfigurationTypeDef],
        "PageNumber": int,
        "PageSize": int,
        "SortingConfiguration": SortingConfigurationTypeDef,
        "UserContext": UserContextTypeDef,
        "VisitorId": str,
        "SpellCorrectionConfiguration": SpellCorrectionConfigurationTypeDef,
    },
    total=False,
)

class QueryRequestRequestTypeDef(
    _RequiredQueryRequestRequestTypeDef, _OptionalQueryRequestRequestTypeDef
):
    pass

_RequiredDocumentTypeDef = TypedDict(
    "_RequiredDocumentTypeDef",
    {
        "Id": str,
    },
)
_OptionalDocumentTypeDef = TypedDict(
    "_OptionalDocumentTypeDef",
    {
        "Title": str,
        "Blob": Union[str, bytes, IO[Any], StreamingBody],
        "S3Path": S3PathTypeDef,
        "Attributes": Sequence[DocumentAttributeTypeDef],
        "AccessControlList": Sequence[PrincipalTypeDef],
        "HierarchicalAccessControlList": Sequence[HierarchicalPrincipalTypeDef],
        "ContentType": ContentTypeType,
    },
    total=False,
)

class DocumentTypeDef(_RequiredDocumentTypeDef, _OptionalDocumentTypeDef):
    pass

ListExperienceEntitiesResponseTypeDef = TypedDict(
    "ListExperienceEntitiesResponseTypeDef",
    {
        "SummaryItems": List[ExperienceEntitiesSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateExperienceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExperienceRequestRequestTypeDef",
    {
        "Name": str,
        "IndexId": str,
    },
)
_OptionalCreateExperienceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExperienceRequestRequestTypeDef",
    {
        "RoleArn": str,
        "Configuration": ExperienceConfigurationTypeDef,
        "Description": str,
        "ClientToken": str,
    },
    total=False,
)

class CreateExperienceRequestRequestTypeDef(
    _RequiredCreateExperienceRequestRequestTypeDef, _OptionalCreateExperienceRequestRequestTypeDef
):
    pass

DescribeExperienceResponseTypeDef = TypedDict(
    "DescribeExperienceResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Endpoints": List[ExperienceEndpointTypeDef],
        "Configuration": ExperienceConfigurationTypeDef,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Description": str,
        "Status": ExperienceStatusType,
        "RoleArn": str,
        "ErrorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateExperienceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateExperienceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)
_OptionalUpdateExperienceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateExperienceRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
        "Configuration": ExperienceConfigurationTypeDef,
        "Description": str,
    },
    total=False,
)

class UpdateExperienceRequestRequestTypeDef(
    _RequiredUpdateExperienceRequestRequestTypeDef, _OptionalUpdateExperienceRequestRequestTypeDef
):
    pass

_RequiredPutPrincipalMappingRequestRequestTypeDef = TypedDict(
    "_RequiredPutPrincipalMappingRequestRequestTypeDef",
    {
        "IndexId": str,
        "GroupId": str,
        "GroupMembers": GroupMembersTypeDef,
    },
)
_OptionalPutPrincipalMappingRequestRequestTypeDef = TypedDict(
    "_OptionalPutPrincipalMappingRequestRequestTypeDef",
    {
        "DataSourceId": str,
        "OrderingId": int,
        "RoleArn": str,
    },
    total=False,
)

class PutPrincipalMappingRequestRequestTypeDef(
    _RequiredPutPrincipalMappingRequestRequestTypeDef,
    _OptionalPutPrincipalMappingRequestRequestTypeDef,
):
    pass

AdditionalResultAttributeValueTypeDef = TypedDict(
    "AdditionalResultAttributeValueTypeDef",
    {
        "TextWithHighlightsValue": TextWithHighlightsTypeDef,
    },
    total=False,
)

_RequiredCreateIndexRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIndexRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
    },
)
_OptionalCreateIndexRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIndexRequestRequestTypeDef",
    {
        "Edition": IndexEditionType,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "Description": str,
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
        "UserTokenConfigurations": Sequence[UserTokenConfigurationTypeDef],
        "UserContextPolicy": UserContextPolicyType,
        "UserGroupResolutionConfiguration": UserGroupResolutionConfigurationTypeDef,
    },
    total=False,
)

class CreateIndexRequestRequestTypeDef(
    _RequiredCreateIndexRequestRequestTypeDef, _OptionalCreateIndexRequestRequestTypeDef
):
    pass

DescribeIndexResponseTypeDef = TypedDict(
    "DescribeIndexResponseTypeDef",
    {
        "Name": str,
        "Id": str,
        "Edition": IndexEditionType,
        "RoleArn": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "Status": IndexStatusType,
        "Description": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "DocumentMetadataConfigurations": List[DocumentMetadataConfigurationTypeDef],
        "IndexStatistics": IndexStatisticsTypeDef,
        "ErrorMessage": str,
        "CapacityUnits": CapacityUnitsConfigurationTypeDef,
        "UserTokenConfigurations": List[UserTokenConfigurationTypeDef],
        "UserContextPolicy": UserContextPolicyType,
        "UserGroupResolutionConfiguration": UserGroupResolutionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateIndexRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIndexRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateIndexRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIndexRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
        "Description": str,
        "DocumentMetadataConfigurationUpdates": Sequence[DocumentMetadataConfigurationTypeDef],
        "CapacityUnits": CapacityUnitsConfigurationTypeDef,
        "UserTokenConfigurations": Sequence[UserTokenConfigurationTypeDef],
        "UserContextPolicy": UserContextPolicyType,
        "UserGroupResolutionConfiguration": UserGroupResolutionConfigurationTypeDef,
    },
    total=False,
)

class UpdateIndexRequestRequestTypeDef(
    _RequiredUpdateIndexRequestRequestTypeDef, _OptionalUpdateIndexRequestRequestTypeDef
):
    pass

_RequiredWebCrawlerConfigurationTypeDef = TypedDict(
    "_RequiredWebCrawlerConfigurationTypeDef",
    {
        "Urls": UrlsTypeDef,
    },
)
_OptionalWebCrawlerConfigurationTypeDef = TypedDict(
    "_OptionalWebCrawlerConfigurationTypeDef",
    {
        "CrawlDepth": int,
        "MaxLinksPerPage": int,
        "MaxContentSizePerPageInMegaBytes": float,
        "MaxUrlsPerMinuteCrawlRate": int,
        "UrlInclusionPatterns": Sequence[str],
        "UrlExclusionPatterns": Sequence[str],
        "ProxyConfiguration": ProxyConfigurationTypeDef,
        "AuthenticationConfiguration": AuthenticationConfigurationTypeDef,
    },
    total=False,
)

class WebCrawlerConfigurationTypeDef(
    _RequiredWebCrawlerConfigurationTypeDef, _OptionalWebCrawlerConfigurationTypeDef
):
    pass

SuggestionValueTypeDef = TypedDict(
    "SuggestionValueTypeDef",
    {
        "Text": SuggestionTextWithHighlightsTypeDef,
    },
    total=False,
)

_RequiredSalesforceConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceConfigurationTypeDef",
    {
        "ServerUrl": str,
        "SecretArn": str,
    },
)
_OptionalSalesforceConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceConfigurationTypeDef",
    {
        "StandardObjectConfigurations": Sequence[SalesforceStandardObjectConfigurationTypeDef],
        "KnowledgeArticleConfiguration": SalesforceKnowledgeArticleConfigurationTypeDef,
        "ChatterFeedConfiguration": SalesforceChatterFeedConfigurationTypeDef,
        "CrawlAttachments": bool,
        "StandardObjectAttachmentConfiguration": SalesforceStandardObjectAttachmentConfigurationTypeDef,
        "IncludeAttachmentFilePatterns": Sequence[str],
        "ExcludeAttachmentFilePatterns": Sequence[str],
    },
    total=False,
)

class SalesforceConfigurationTypeDef(
    _RequiredSalesforceConfigurationTypeDef, _OptionalSalesforceConfigurationTypeDef
):
    pass

CustomDocumentEnrichmentConfigurationTypeDef = TypedDict(
    "CustomDocumentEnrichmentConfigurationTypeDef",
    {
        "InlineConfigurations": Sequence[InlineCustomDocumentEnrichmentConfigurationTypeDef],
        "PreExtractionHookConfiguration": HookConfigurationTypeDef,
        "PostExtractionHookConfiguration": HookConfigurationTypeDef,
        "RoleArn": str,
    },
    total=False,
)

BatchGetDocumentStatusRequestRequestTypeDef = TypedDict(
    "BatchGetDocumentStatusRequestRequestTypeDef",
    {
        "IndexId": str,
        "DocumentInfoList": Sequence[DocumentInfoTypeDef],
    },
)

AdditionalResultAttributeTypeDef = TypedDict(
    "AdditionalResultAttributeTypeDef",
    {
        "Key": str,
        "ValueType": Literal["TEXT_WITH_HIGHLIGHTS_VALUE"],
        "Value": AdditionalResultAttributeValueTypeDef,
    },
)

SuggestionTypeDef = TypedDict(
    "SuggestionTypeDef",
    {
        "Id": str,
        "Value": SuggestionValueTypeDef,
    },
    total=False,
)

DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "S3Configuration": S3DataSourceConfigurationTypeDef,
        "SharePointConfiguration": SharePointConfigurationTypeDef,
        "DatabaseConfiguration": DatabaseConfigurationTypeDef,
        "SalesforceConfiguration": SalesforceConfigurationTypeDef,
        "OneDriveConfiguration": OneDriveConfigurationTypeDef,
        "ServiceNowConfiguration": ServiceNowConfigurationTypeDef,
        "ConfluenceConfiguration": ConfluenceConfigurationTypeDef,
        "GoogleDriveConfiguration": GoogleDriveConfigurationTypeDef,
        "WebCrawlerConfiguration": WebCrawlerConfigurationTypeDef,
        "WorkDocsConfiguration": WorkDocsConfigurationTypeDef,
        "FsxConfiguration": FsxConfigurationTypeDef,
        "SlackConfiguration": SlackConfigurationTypeDef,
        "BoxConfiguration": BoxConfigurationTypeDef,
        "QuipConfiguration": QuipConfigurationTypeDef,
        "JiraConfiguration": JiraConfigurationTypeDef,
        "GitHubConfiguration": GitHubConfigurationTypeDef,
    },
    total=False,
)

_RequiredBatchPutDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredBatchPutDocumentRequestRequestTypeDef",
    {
        "IndexId": str,
        "Documents": Sequence[DocumentTypeDef],
    },
)
_OptionalBatchPutDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalBatchPutDocumentRequestRequestTypeDef",
    {
        "RoleArn": str,
        "CustomDocumentEnrichmentConfiguration": CustomDocumentEnrichmentConfigurationTypeDef,
    },
    total=False,
)

class BatchPutDocumentRequestRequestTypeDef(
    _RequiredBatchPutDocumentRequestRequestTypeDef, _OptionalBatchPutDocumentRequestRequestTypeDef
):
    pass

QueryResultItemTypeDef = TypedDict(
    "QueryResultItemTypeDef",
    {
        "Id": str,
        "Type": QueryResultTypeType,
        "AdditionalAttributes": List[AdditionalResultAttributeTypeDef],
        "DocumentId": str,
        "DocumentTitle": TextWithHighlightsTypeDef,
        "DocumentExcerpt": TextWithHighlightsTypeDef,
        "DocumentURI": str,
        "DocumentAttributes": List[DocumentAttributeTypeDef],
        "ScoreAttributes": ScoreAttributesTypeDef,
        "FeedbackToken": str,
    },
    total=False,
)

GetQuerySuggestionsResponseTypeDef = TypedDict(
    "GetQuerySuggestionsResponseTypeDef",
    {
        "QuerySuggestionsId": str,
        "Suggestions": List[SuggestionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSourceRequestRequestTypeDef",
    {
        "Name": str,
        "IndexId": str,
        "Type": DataSourceTypeType,
    },
)
_OptionalCreateDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSourceRequestRequestTypeDef",
    {
        "Configuration": DataSourceConfigurationTypeDef,
        "Description": str,
        "Schedule": str,
        "RoleArn": str,
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
        "LanguageCode": str,
        "CustomDocumentEnrichmentConfiguration": CustomDocumentEnrichmentConfigurationTypeDef,
    },
    total=False,
)

class CreateDataSourceRequestRequestTypeDef(
    _RequiredCreateDataSourceRequestRequestTypeDef, _OptionalCreateDataSourceRequestRequestTypeDef
):
    pass

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "Configuration": DataSourceConfigurationTypeDef,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Description": str,
        "Status": DataSourceStatusType,
        "Schedule": str,
        "RoleArn": str,
        "ErrorMessage": str,
        "LanguageCode": str,
        "CustomDocumentEnrichmentConfiguration": CustomDocumentEnrichmentConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSourceRequestRequestTypeDef",
    {
        "Id": str,
        "IndexId": str,
    },
)
_OptionalUpdateDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSourceRequestRequestTypeDef",
    {
        "Name": str,
        "Configuration": DataSourceConfigurationTypeDef,
        "Description": str,
        "Schedule": str,
        "RoleArn": str,
        "LanguageCode": str,
        "CustomDocumentEnrichmentConfiguration": CustomDocumentEnrichmentConfigurationTypeDef,
    },
    total=False,
)

class UpdateDataSourceRequestRequestTypeDef(
    _RequiredUpdateDataSourceRequestRequestTypeDef, _OptionalUpdateDataSourceRequestRequestTypeDef
):
    pass

QueryResultTypeDef = TypedDict(
    "QueryResultTypeDef",
    {
        "QueryId": str,
        "ResultItems": List[QueryResultItemTypeDef],
        "FacetResults": List["FacetResultTypeDef"],
        "TotalNumberOfResults": int,
        "Warnings": List[WarningTypeDef],
        "SpellCorrectedQueries": List[SpellCorrectedQueryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
