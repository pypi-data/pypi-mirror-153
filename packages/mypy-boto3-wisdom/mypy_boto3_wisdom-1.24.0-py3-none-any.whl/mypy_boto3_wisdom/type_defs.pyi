"""
Type annotations for wisdom service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/type_defs/)

Usage::

    ```python
    from mypy_boto3_wisdom.type_defs import AppIntegrationsConfigurationTypeDef

    data: AppIntegrationsConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AssistantStatusType,
    ContentStatusType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    RecommendationSourceTypeType,
    RelevanceLevelType,
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
    "AppIntegrationsConfigurationTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "ContentDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "CreateContentRequestRequestTypeDef",
    "RenderingConfigurationTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "SessionDataTypeDef",
    "DeleteAssistantAssociationRequestRequestTypeDef",
    "DeleteAssistantRequestRequestTypeDef",
    "DeleteContentRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "HighlightTypeDef",
    "FilterTypeDef",
    "GetAssistantAssociationRequestRequestTypeDef",
    "GetAssistantRequestRequestTypeDef",
    "GetContentRequestRequestTypeDef",
    "GetContentSummaryRequestRequestTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetSessionRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListAssistantAssociationsRequestRequestTypeDef",
    "ListAssistantsRequestRequestTypeDef",
    "ListContentsRequestRequestTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    "QueryAssistantRequestRequestTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "SessionSummaryTypeDef",
    "StartContentUploadRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateContentRequestRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "SourceConfigurationTypeDef",
    "CreateAssistantAssociationRequestRequestTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantDataTypeDef",
    "AssistantSummaryTypeDef",
    "CreateAssistantRequestRequestTypeDef",
    "CreateContentResponseTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryResponseTypeDef",
    "ListContentsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SearchContentResponseTypeDef",
    "StartContentUploadResponseTypeDef",
    "UpdateContentResponseTypeDef",
    "CreateSessionResponseTypeDef",
    "GetSessionResponseTypeDef",
    "DocumentTextTypeDef",
    "SearchExpressionTypeDef",
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    "ListContentsRequestListContentsPaginateTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "RecommendationTriggerDataTypeDef",
    "SearchSessionsResponseTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "CreateAssistantResponseTypeDef",
    "GetAssistantResponseTypeDef",
    "ListAssistantsResponseTypeDef",
    "DocumentTypeDef",
    "SearchContentRequestRequestTypeDef",
    "SearchContentRequestSearchContentPaginateTypeDef",
    "SearchSessionsRequestRequestTypeDef",
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    "RecommendationTriggerTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "RecommendationDataTypeDef",
    "ResultDataTypeDef",
    "GetRecommendationsResponseTypeDef",
    "QueryAssistantResponseTypeDef",
)

AppIntegrationsConfigurationTypeDef = TypedDict(
    "AppIntegrationsConfigurationTypeDef",
    {
        "appIntegrationArn": str,
        "objectFields": Sequence[str],
    },
)

AssistantAssociationInputDataTypeDef = TypedDict(
    "AssistantAssociationInputDataTypeDef",
    {
        "knowledgeBaseId": str,
    },
    total=False,
)

KnowledgeBaseAssociationDataTypeDef = TypedDict(
    "KnowledgeBaseAssociationDataTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
    },
    total=False,
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "kmsKeyId": str,
    },
    total=False,
)

_RequiredContentDataTypeDef = TypedDict(
    "_RequiredContentDataTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "contentType": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "metadata": Dict[str, str],
        "name": str,
        "revisionId": str,
        "status": ContentStatusType,
        "title": str,
        "url": str,
        "urlExpiry": datetime,
    },
)
_OptionalContentDataTypeDef = TypedDict(
    "_OptionalContentDataTypeDef",
    {
        "linkOutUri": str,
        "tags": Dict[str, str],
    },
    total=False,
)

class ContentDataTypeDef(_RequiredContentDataTypeDef, _OptionalContentDataTypeDef):
    pass

ContentReferenceTypeDef = TypedDict(
    "ContentReferenceTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
    },
    total=False,
)

_RequiredContentSummaryTypeDef = TypedDict(
    "_RequiredContentSummaryTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "contentType": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "metadata": Dict[str, str],
        "name": str,
        "revisionId": str,
        "status": ContentStatusType,
        "title": str,
    },
)
_OptionalContentSummaryTypeDef = TypedDict(
    "_OptionalContentSummaryTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)

class ContentSummaryTypeDef(_RequiredContentSummaryTypeDef, _OptionalContentSummaryTypeDef):
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

_RequiredCreateContentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContentRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "name": str,
        "uploadId": str,
    },
)
_OptionalCreateContentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContentRequestRequestTypeDef",
    {
        "clientToken": str,
        "metadata": Mapping[str, str],
        "overrideLinkOutUri": str,
        "tags": Mapping[str, str],
        "title": str,
    },
    total=False,
)

class CreateContentRequestRequestTypeDef(
    _RequiredCreateContentRequestRequestTypeDef, _OptionalCreateContentRequestRequestTypeDef
):
    pass

RenderingConfigurationTypeDef = TypedDict(
    "RenderingConfigurationTypeDef",
    {
        "templateUri": str,
    },
    total=False,
)

_RequiredCreateSessionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "name": str,
    },
)
_OptionalCreateSessionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSessionRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateSessionRequestRequestTypeDef(
    _RequiredCreateSessionRequestRequestTypeDef, _OptionalCreateSessionRequestRequestTypeDef
):
    pass

_RequiredSessionDataTypeDef = TypedDict(
    "_RequiredSessionDataTypeDef",
    {
        "name": str,
        "sessionArn": str,
        "sessionId": str,
    },
)
_OptionalSessionDataTypeDef = TypedDict(
    "_OptionalSessionDataTypeDef",
    {
        "description": str,
        "tags": Dict[str, str],
    },
    total=False,
)

class SessionDataTypeDef(_RequiredSessionDataTypeDef, _OptionalSessionDataTypeDef):
    pass

DeleteAssistantAssociationRequestRequestTypeDef = TypedDict(
    "DeleteAssistantAssociationRequestRequestTypeDef",
    {
        "assistantAssociationId": str,
        "assistantId": str,
    },
)

DeleteAssistantRequestRequestTypeDef = TypedDict(
    "DeleteAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)

DeleteContentRequestRequestTypeDef = TypedDict(
    "DeleteContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)

DeleteKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)

HighlightTypeDef = TypedDict(
    "HighlightTypeDef",
    {
        "beginOffsetInclusive": int,
        "endOffsetExclusive": int,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)

GetAssistantAssociationRequestRequestTypeDef = TypedDict(
    "GetAssistantAssociationRequestRequestTypeDef",
    {
        "assistantAssociationId": str,
        "assistantId": str,
    },
)

GetAssistantRequestRequestTypeDef = TypedDict(
    "GetAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)

GetContentRequestRequestTypeDef = TypedDict(
    "GetContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)

GetContentSummaryRequestRequestTypeDef = TypedDict(
    "GetContentSummaryRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)

GetKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)

_RequiredGetRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredGetRecommendationsRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
    },
)
_OptionalGetRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalGetRecommendationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "waitTimeSeconds": int,
    },
    total=False,
)

class GetRecommendationsRequestRequestTypeDef(
    _RequiredGetRecommendationsRequestRequestTypeDef,
    _OptionalGetRecommendationsRequestRequestTypeDef,
):
    pass

GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
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

_RequiredListAssistantAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssistantAssociationsRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)
_OptionalListAssistantAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssistantAssociationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListAssistantAssociationsRequestRequestTypeDef(
    _RequiredListAssistantAssociationsRequestRequestTypeDef,
    _OptionalListAssistantAssociationsRequestRequestTypeDef,
):
    pass

ListAssistantsRequestRequestTypeDef = TypedDict(
    "ListAssistantsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListContentsRequestRequestTypeDef = TypedDict(
    "_RequiredListContentsRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
_OptionalListContentsRequestRequestTypeDef = TypedDict(
    "_OptionalListContentsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListContentsRequestRequestTypeDef(
    _RequiredListContentsRequestRequestTypeDef, _OptionalListContentsRequestRequestTypeDef
):
    pass

ListKnowledgeBasesRequestRequestTypeDef = TypedDict(
    "ListKnowledgeBasesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

NotifyRecommendationsReceivedErrorTypeDef = TypedDict(
    "NotifyRecommendationsReceivedErrorTypeDef",
    {
        "message": str,
        "recommendationId": str,
    },
    total=False,
)

NotifyRecommendationsReceivedRequestRequestTypeDef = TypedDict(
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    {
        "assistantId": str,
        "recommendationIds": Sequence[str],
        "sessionId": str,
    },
)

_RequiredQueryAssistantRequestRequestTypeDef = TypedDict(
    "_RequiredQueryAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
        "queryText": str,
    },
)
_OptionalQueryAssistantRequestRequestTypeDef = TypedDict(
    "_OptionalQueryAssistantRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class QueryAssistantRequestRequestTypeDef(
    _RequiredQueryAssistantRequestRequestTypeDef, _OptionalQueryAssistantRequestRequestTypeDef
):
    pass

QueryRecommendationTriggerDataTypeDef = TypedDict(
    "QueryRecommendationTriggerDataTypeDef",
    {
        "text": str,
    },
    total=False,
)

RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef = TypedDict(
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)

SessionSummaryTypeDef = TypedDict(
    "SessionSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "sessionArn": str,
        "sessionId": str,
    },
)

StartContentUploadRequestRequestTypeDef = TypedDict(
    "StartContentUploadRequestRequestTypeDef",
    {
        "contentType": str,
        "knowledgeBaseId": str,
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

_RequiredUpdateContentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)
_OptionalUpdateContentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContentRequestRequestTypeDef",
    {
        "metadata": Mapping[str, str],
        "overrideLinkOutUri": str,
        "removeOverrideLinkOutUri": bool,
        "revisionId": str,
        "title": str,
        "uploadId": str,
    },
    total=False,
)

class UpdateContentRequestRequestTypeDef(
    _RequiredUpdateContentRequestRequestTypeDef, _OptionalUpdateContentRequestRequestTypeDef
):
    pass

UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef = TypedDict(
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "templateUri": str,
    },
)

SourceConfigurationTypeDef = TypedDict(
    "SourceConfigurationTypeDef",
    {
        "appIntegrations": AppIntegrationsConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateAssistantAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssistantAssociationRequestRequestTypeDef",
    {
        "assistantId": str,
        "association": AssistantAssociationInputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
    },
)
_OptionalCreateAssistantAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssistantAssociationRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateAssistantAssociationRequestRequestTypeDef(
    _RequiredCreateAssistantAssociationRequestRequestTypeDef,
    _OptionalCreateAssistantAssociationRequestRequestTypeDef,
):
    pass

AssistantAssociationOutputDataTypeDef = TypedDict(
    "AssistantAssociationOutputDataTypeDef",
    {
        "knowledgeBaseAssociation": KnowledgeBaseAssociationDataTypeDef,
    },
    total=False,
)

_RequiredAssistantDataTypeDef = TypedDict(
    "_RequiredAssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
    },
)
_OptionalAssistantDataTypeDef = TypedDict(
    "_OptionalAssistantDataTypeDef",
    {
        "description": str,
        "serverSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

class AssistantDataTypeDef(_RequiredAssistantDataTypeDef, _OptionalAssistantDataTypeDef):
    pass

_RequiredAssistantSummaryTypeDef = TypedDict(
    "_RequiredAssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
    },
)
_OptionalAssistantSummaryTypeDef = TypedDict(
    "_OptionalAssistantSummaryTypeDef",
    {
        "description": str,
        "serverSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

class AssistantSummaryTypeDef(_RequiredAssistantSummaryTypeDef, _OptionalAssistantSummaryTypeDef):
    pass

_RequiredCreateAssistantRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssistantRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
    },
)
_OptionalCreateAssistantRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssistantRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "serverSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateAssistantRequestRequestTypeDef(
    _RequiredCreateAssistantRequestRequestTypeDef, _OptionalCreateAssistantRequestRequestTypeDef
):
    pass

CreateContentResponseTypeDef = TypedDict(
    "CreateContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContentResponseTypeDef = TypedDict(
    "GetContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContentSummaryResponseTypeDef = TypedDict(
    "GetContentSummaryResponseTypeDef",
    {
        "contentSummary": ContentSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContentsResponseTypeDef = TypedDict(
    "ListContentsResponseTypeDef",
    {
        "contentSummaries": List[ContentSummaryTypeDef],
        "nextToken": str,
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

SearchContentResponseTypeDef = TypedDict(
    "SearchContentResponseTypeDef",
    {
        "contentSummaries": List[ContentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartContentUploadResponseTypeDef = TypedDict(
    "StartContentUploadResponseTypeDef",
    {
        "headersToInclude": Dict[str, str],
        "uploadId": str,
        "url": str,
        "urlExpiry": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateContentResponseTypeDef = TypedDict(
    "UpdateContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSessionResponseTypeDef = TypedDict(
    "CreateSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DocumentTextTypeDef = TypedDict(
    "DocumentTextTypeDef",
    {
        "highlights": List[HighlightTypeDef],
        "text": str,
    },
    total=False,
)

SearchExpressionTypeDef = TypedDict(
    "SearchExpressionTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
    },
)

_RequiredListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef = TypedDict(
    "_RequiredListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    {
        "assistantId": str,
    },
)
_OptionalListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef = TypedDict(
    "_OptionalListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef(
    _RequiredListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef,
    _OptionalListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef,
):
    pass

ListAssistantsRequestListAssistantsPaginateTypeDef = TypedDict(
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListContentsRequestListContentsPaginateTypeDef = TypedDict(
    "_RequiredListContentsRequestListContentsPaginateTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
_OptionalListContentsRequestListContentsPaginateTypeDef = TypedDict(
    "_OptionalListContentsRequestListContentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListContentsRequestListContentsPaginateTypeDef(
    _RequiredListContentsRequestListContentsPaginateTypeDef,
    _OptionalListContentsRequestListContentsPaginateTypeDef,
):
    pass

ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredQueryAssistantRequestQueryAssistantPaginateTypeDef = TypedDict(
    "_RequiredQueryAssistantRequestQueryAssistantPaginateTypeDef",
    {
        "assistantId": str,
        "queryText": str,
    },
)
_OptionalQueryAssistantRequestQueryAssistantPaginateTypeDef = TypedDict(
    "_OptionalQueryAssistantRequestQueryAssistantPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class QueryAssistantRequestQueryAssistantPaginateTypeDef(
    _RequiredQueryAssistantRequestQueryAssistantPaginateTypeDef,
    _OptionalQueryAssistantRequestQueryAssistantPaginateTypeDef,
):
    pass

NotifyRecommendationsReceivedResponseTypeDef = TypedDict(
    "NotifyRecommendationsReceivedResponseTypeDef",
    {
        "errors": List[NotifyRecommendationsReceivedErrorTypeDef],
        "recommendationIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecommendationTriggerDataTypeDef = TypedDict(
    "RecommendationTriggerDataTypeDef",
    {
        "query": QueryRecommendationTriggerDataTypeDef,
    },
    total=False,
)

SearchSessionsResponseTypeDef = TypedDict(
    "SearchSessionsResponseTypeDef",
    {
        "nextToken": str,
        "sessionSummaries": List[SessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
    },
)
_OptionalCreateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKnowledgeBaseRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "renderingConfiguration": RenderingConfigurationTypeDef,
        "serverSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "sourceConfiguration": SourceConfigurationTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateKnowledgeBaseRequestRequestTypeDef(
    _RequiredCreateKnowledgeBaseRequestRequestTypeDef,
    _OptionalCreateKnowledgeBaseRequestRequestTypeDef,
):
    pass

_RequiredKnowledgeBaseDataTypeDef = TypedDict(
    "_RequiredKnowledgeBaseDataTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
    },
)
_OptionalKnowledgeBaseDataTypeDef = TypedDict(
    "_OptionalKnowledgeBaseDataTypeDef",
    {
        "description": str,
        "lastContentModificationTime": datetime,
        "renderingConfiguration": RenderingConfigurationTypeDef,
        "serverSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "sourceConfiguration": SourceConfigurationTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

class KnowledgeBaseDataTypeDef(
    _RequiredKnowledgeBaseDataTypeDef, _OptionalKnowledgeBaseDataTypeDef
):
    pass

_RequiredKnowledgeBaseSummaryTypeDef = TypedDict(
    "_RequiredKnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
    },
)
_OptionalKnowledgeBaseSummaryTypeDef = TypedDict(
    "_OptionalKnowledgeBaseSummaryTypeDef",
    {
        "description": str,
        "renderingConfiguration": RenderingConfigurationTypeDef,
        "serverSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "sourceConfiguration": SourceConfigurationTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

class KnowledgeBaseSummaryTypeDef(
    _RequiredKnowledgeBaseSummaryTypeDef, _OptionalKnowledgeBaseSummaryTypeDef
):
    pass

_RequiredAssistantAssociationDataTypeDef = TypedDict(
    "_RequiredAssistantAssociationDataTypeDef",
    {
        "assistantArn": str,
        "assistantAssociationArn": str,
        "assistantAssociationId": str,
        "assistantId": str,
        "associationData": AssistantAssociationOutputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
    },
)
_OptionalAssistantAssociationDataTypeDef = TypedDict(
    "_OptionalAssistantAssociationDataTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)

class AssistantAssociationDataTypeDef(
    _RequiredAssistantAssociationDataTypeDef, _OptionalAssistantAssociationDataTypeDef
):
    pass

_RequiredAssistantAssociationSummaryTypeDef = TypedDict(
    "_RequiredAssistantAssociationSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantAssociationArn": str,
        "assistantAssociationId": str,
        "assistantId": str,
        "associationData": AssistantAssociationOutputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
    },
)
_OptionalAssistantAssociationSummaryTypeDef = TypedDict(
    "_OptionalAssistantAssociationSummaryTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)

class AssistantAssociationSummaryTypeDef(
    _RequiredAssistantAssociationSummaryTypeDef, _OptionalAssistantAssociationSummaryTypeDef
):
    pass

CreateAssistantResponseTypeDef = TypedDict(
    "CreateAssistantResponseTypeDef",
    {
        "assistant": AssistantDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssistantResponseTypeDef = TypedDict(
    "GetAssistantResponseTypeDef",
    {
        "assistant": AssistantDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssistantsResponseTypeDef = TypedDict(
    "ListAssistantsResponseTypeDef",
    {
        "assistantSummaries": List[AssistantSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDocumentTypeDef = TypedDict(
    "_RequiredDocumentTypeDef",
    {
        "contentReference": ContentReferenceTypeDef,
    },
)
_OptionalDocumentTypeDef = TypedDict(
    "_OptionalDocumentTypeDef",
    {
        "excerpt": DocumentTextTypeDef,
        "title": DocumentTextTypeDef,
    },
    total=False,
)

class DocumentTypeDef(_RequiredDocumentTypeDef, _OptionalDocumentTypeDef):
    pass

_RequiredSearchContentRequestRequestTypeDef = TypedDict(
    "_RequiredSearchContentRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": SearchExpressionTypeDef,
    },
)
_OptionalSearchContentRequestRequestTypeDef = TypedDict(
    "_OptionalSearchContentRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class SearchContentRequestRequestTypeDef(
    _RequiredSearchContentRequestRequestTypeDef, _OptionalSearchContentRequestRequestTypeDef
):
    pass

_RequiredSearchContentRequestSearchContentPaginateTypeDef = TypedDict(
    "_RequiredSearchContentRequestSearchContentPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": SearchExpressionTypeDef,
    },
)
_OptionalSearchContentRequestSearchContentPaginateTypeDef = TypedDict(
    "_OptionalSearchContentRequestSearchContentPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchContentRequestSearchContentPaginateTypeDef(
    _RequiredSearchContentRequestSearchContentPaginateTypeDef,
    _OptionalSearchContentRequestSearchContentPaginateTypeDef,
):
    pass

_RequiredSearchSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchSessionsRequestRequestTypeDef",
    {
        "assistantId": str,
        "searchExpression": SearchExpressionTypeDef,
    },
)
_OptionalSearchSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchSessionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class SearchSessionsRequestRequestTypeDef(
    _RequiredSearchSessionsRequestRequestTypeDef, _OptionalSearchSessionsRequestRequestTypeDef
):
    pass

_RequiredSearchSessionsRequestSearchSessionsPaginateTypeDef = TypedDict(
    "_RequiredSearchSessionsRequestSearchSessionsPaginateTypeDef",
    {
        "assistantId": str,
        "searchExpression": SearchExpressionTypeDef,
    },
)
_OptionalSearchSessionsRequestSearchSessionsPaginateTypeDef = TypedDict(
    "_OptionalSearchSessionsRequestSearchSessionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchSessionsRequestSearchSessionsPaginateTypeDef(
    _RequiredSearchSessionsRequestSearchSessionsPaginateTypeDef,
    _OptionalSearchSessionsRequestSearchSessionsPaginateTypeDef,
):
    pass

RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": Literal["QUERY"],
    },
)

CreateKnowledgeBaseResponseTypeDef = TypedDict(
    "CreateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKnowledgeBaseResponseTypeDef = TypedDict(
    "GetKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKnowledgeBaseTemplateUriResponseTypeDef = TypedDict(
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKnowledgeBasesResponseTypeDef = TypedDict(
    "ListKnowledgeBasesResponseTypeDef",
    {
        "knowledgeBaseSummaries": List[KnowledgeBaseSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssistantAssociationResponseTypeDef = TypedDict(
    "CreateAssistantAssociationResponseTypeDef",
    {
        "assistantAssociation": AssistantAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssistantAssociationResponseTypeDef = TypedDict(
    "GetAssistantAssociationResponseTypeDef",
    {
        "assistantAssociation": AssistantAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssistantAssociationsResponseTypeDef = TypedDict(
    "ListAssistantAssociationsResponseTypeDef",
    {
        "assistantAssociationSummaries": List[AssistantAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRecommendationDataTypeDef = TypedDict(
    "_RequiredRecommendationDataTypeDef",
    {
        "document": DocumentTypeDef,
        "recommendationId": str,
    },
)
_OptionalRecommendationDataTypeDef = TypedDict(
    "_OptionalRecommendationDataTypeDef",
    {
        "relevanceLevel": RelevanceLevelType,
        "relevanceScore": float,
        "type": Literal["KNOWLEDGE_CONTENT"],
    },
    total=False,
)

class RecommendationDataTypeDef(
    _RequiredRecommendationDataTypeDef, _OptionalRecommendationDataTypeDef
):
    pass

_RequiredResultDataTypeDef = TypedDict(
    "_RequiredResultDataTypeDef",
    {
        "document": DocumentTypeDef,
        "resultId": str,
    },
)
_OptionalResultDataTypeDef = TypedDict(
    "_OptionalResultDataTypeDef",
    {
        "relevanceScore": float,
    },
    total=False,
)

class ResultDataTypeDef(_RequiredResultDataTypeDef, _OptionalResultDataTypeDef):
    pass

GetRecommendationsResponseTypeDef = TypedDict(
    "GetRecommendationsResponseTypeDef",
    {
        "recommendations": List[RecommendationDataTypeDef],
        "triggers": List[RecommendationTriggerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

QueryAssistantResponseTypeDef = TypedDict(
    "QueryAssistantResponseTypeDef",
    {
        "nextToken": str,
        "results": List[ResultDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
