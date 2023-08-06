"""
Type annotations for inspector service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/type_defs/)

Usage::

    ```python
    from mypy_boto3_inspector.type_defs import AttributeTypeDef

    data: AttributeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AgentHealthCodeType,
    AgentHealthType,
    AssessmentRunNotificationSnsStatusCodeType,
    AssessmentRunStateType,
    FailedItemErrorCodeType,
    InspectorEventType,
    PreviewStatusType,
    ReportFileFormatType,
    ReportStatusType,
    ReportTypeType,
    ScopeTypeType,
    SeverityType,
    StopActionType,
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
    "AttributeTypeDef",
    "FailedItemDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "AgentFilterTypeDef",
    "AgentPreviewTypeDef",
    "TelemetryMetadataTypeDef",
    "DurationRangeTypeDef",
    "TimestampRangeTypeDef",
    "AssessmentRunNotificationTypeDef",
    "AssessmentRunStateChangeTypeDef",
    "AssessmentTargetFilterTypeDef",
    "AssessmentTargetTypeDef",
    "TagTypeDef",
    "CreateAssessmentTargetRequestRequestTypeDef",
    "CreateExclusionsPreviewRequestRequestTypeDef",
    "ResourceGroupTagTypeDef",
    "DeleteAssessmentRunRequestRequestTypeDef",
    "DeleteAssessmentTargetRequestRequestTypeDef",
    "DeleteAssessmentTemplateRequestRequestTypeDef",
    "DescribeAssessmentRunsRequestRequestTypeDef",
    "DescribeAssessmentTargetsRequestRequestTypeDef",
    "DescribeAssessmentTemplatesRequestRequestTypeDef",
    "DescribeExclusionsRequestRequestTypeDef",
    "DescribeFindingsRequestRequestTypeDef",
    "DescribeResourceGroupsRequestRequestTypeDef",
    "DescribeRulesPackagesRequestRequestTypeDef",
    "RulesPackageTypeDef",
    "EventSubscriptionTypeDef",
    "ScopeTypeDef",
    "InspectorServiceAttributesTypeDef",
    "GetAssessmentReportRequestRequestTypeDef",
    "GetExclusionsPreviewRequestRequestTypeDef",
    "GetTelemetryMetadataRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListEventSubscriptionsRequestRequestTypeDef",
    "ListExclusionsRequestRequestTypeDef",
    "ListRulesPackagesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PrivateIpTypeDef",
    "SecurityGroupTypeDef",
    "PreviewAgentsRequestRequestTypeDef",
    "RegisterCrossAccountAccessRoleRequestRequestTypeDef",
    "RemoveAttributesFromFindingsRequestRequestTypeDef",
    "StartAssessmentRunRequestRequestTypeDef",
    "StopAssessmentRunRequestRequestTypeDef",
    "SubscribeToEventRequestRequestTypeDef",
    "UnsubscribeFromEventRequestRequestTypeDef",
    "UpdateAssessmentTargetRequestRequestTypeDef",
    "AddAttributesToFindingsRequestRequestTypeDef",
    "AssessmentTemplateTypeDef",
    "CreateAssessmentTemplateRequestRequestTypeDef",
    "AddAttributesToFindingsResponseTypeDef",
    "CreateAssessmentTargetResponseTypeDef",
    "CreateAssessmentTemplateResponseTypeDef",
    "CreateExclusionsPreviewResponseTypeDef",
    "CreateResourceGroupResponseTypeDef",
    "DescribeCrossAccountAccessRoleResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAssessmentReportResponseTypeDef",
    "ListAssessmentRunsResponseTypeDef",
    "ListAssessmentTargetsResponseTypeDef",
    "ListAssessmentTemplatesResponseTypeDef",
    "ListExclusionsResponseTypeDef",
    "ListFindingsResponseTypeDef",
    "ListRulesPackagesResponseTypeDef",
    "RemoveAttributesFromFindingsResponseTypeDef",
    "StartAssessmentRunResponseTypeDef",
    "ListAssessmentRunAgentsRequestRequestTypeDef",
    "PreviewAgentsResponseTypeDef",
    "AssessmentRunAgentTypeDef",
    "GetTelemetryMetadataResponseTypeDef",
    "AssessmentTemplateFilterTypeDef",
    "AssessmentRunFilterTypeDef",
    "FindingFilterTypeDef",
    "AssessmentRunTypeDef",
    "ListAssessmentTargetsRequestRequestTypeDef",
    "DescribeAssessmentTargetsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SetTagsForResourceRequestRequestTypeDef",
    "CreateResourceGroupRequestRequestTypeDef",
    "ResourceGroupTypeDef",
    "DescribeRulesPackagesResponseTypeDef",
    "SubscriptionTypeDef",
    "ExclusionPreviewTypeDef",
    "ExclusionTypeDef",
    "ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef",
    "ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef",
    "ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef",
    "ListExclusionsRequestListExclusionsPaginateTypeDef",
    "ListRulesPackagesRequestListRulesPackagesPaginateTypeDef",
    "PreviewAgentsRequestPreviewAgentsPaginateTypeDef",
    "NetworkInterfaceTypeDef",
    "DescribeAssessmentTemplatesResponseTypeDef",
    "ListAssessmentRunAgentsResponseTypeDef",
    "ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef",
    "ListAssessmentTemplatesRequestRequestTypeDef",
    "ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef",
    "ListAssessmentRunsRequestRequestTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "DescribeAssessmentRunsResponseTypeDef",
    "DescribeResourceGroupsResponseTypeDef",
    "ListEventSubscriptionsResponseTypeDef",
    "GetExclusionsPreviewResponseTypeDef",
    "DescribeExclusionsResponseTypeDef",
    "AssetAttributesTypeDef",
    "FindingTypeDef",
    "DescribeFindingsResponseTypeDef",
)

_RequiredAttributeTypeDef = TypedDict(
    "_RequiredAttributeTypeDef",
    {
        "key": str,
    },
)
_OptionalAttributeTypeDef = TypedDict(
    "_OptionalAttributeTypeDef",
    {
        "value": str,
    },
    total=False,
)

class AttributeTypeDef(_RequiredAttributeTypeDef, _OptionalAttributeTypeDef):
    pass

FailedItemDetailsTypeDef = TypedDict(
    "FailedItemDetailsTypeDef",
    {
        "failureCode": FailedItemErrorCodeType,
        "retryable": bool,
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

AgentFilterTypeDef = TypedDict(
    "AgentFilterTypeDef",
    {
        "agentHealths": Sequence[AgentHealthType],
        "agentHealthCodes": Sequence[AgentHealthCodeType],
    },
)

_RequiredAgentPreviewTypeDef = TypedDict(
    "_RequiredAgentPreviewTypeDef",
    {
        "agentId": str,
    },
)
_OptionalAgentPreviewTypeDef = TypedDict(
    "_OptionalAgentPreviewTypeDef",
    {
        "hostname": str,
        "autoScalingGroup": str,
        "agentHealth": AgentHealthType,
        "agentVersion": str,
        "operatingSystem": str,
        "kernelVersion": str,
        "ipv4Address": str,
    },
    total=False,
)

class AgentPreviewTypeDef(_RequiredAgentPreviewTypeDef, _OptionalAgentPreviewTypeDef):
    pass

_RequiredTelemetryMetadataTypeDef = TypedDict(
    "_RequiredTelemetryMetadataTypeDef",
    {
        "messageType": str,
        "count": int,
    },
)
_OptionalTelemetryMetadataTypeDef = TypedDict(
    "_OptionalTelemetryMetadataTypeDef",
    {
        "dataSize": int,
    },
    total=False,
)

class TelemetryMetadataTypeDef(
    _RequiredTelemetryMetadataTypeDef, _OptionalTelemetryMetadataTypeDef
):
    pass

DurationRangeTypeDef = TypedDict(
    "DurationRangeTypeDef",
    {
        "minSeconds": int,
        "maxSeconds": int,
    },
    total=False,
)

TimestampRangeTypeDef = TypedDict(
    "TimestampRangeTypeDef",
    {
        "beginDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
    total=False,
)

_RequiredAssessmentRunNotificationTypeDef = TypedDict(
    "_RequiredAssessmentRunNotificationTypeDef",
    {
        "date": datetime,
        "event": InspectorEventType,
        "error": bool,
    },
)
_OptionalAssessmentRunNotificationTypeDef = TypedDict(
    "_OptionalAssessmentRunNotificationTypeDef",
    {
        "message": str,
        "snsTopicArn": str,
        "snsPublishStatusCode": AssessmentRunNotificationSnsStatusCodeType,
    },
    total=False,
)

class AssessmentRunNotificationTypeDef(
    _RequiredAssessmentRunNotificationTypeDef, _OptionalAssessmentRunNotificationTypeDef
):
    pass

AssessmentRunStateChangeTypeDef = TypedDict(
    "AssessmentRunStateChangeTypeDef",
    {
        "stateChangedAt": datetime,
        "state": AssessmentRunStateType,
    },
)

AssessmentTargetFilterTypeDef = TypedDict(
    "AssessmentTargetFilterTypeDef",
    {
        "assessmentTargetNamePattern": str,
    },
    total=False,
)

_RequiredAssessmentTargetTypeDef = TypedDict(
    "_RequiredAssessmentTargetTypeDef",
    {
        "arn": str,
        "name": str,
        "createdAt": datetime,
        "updatedAt": datetime,
    },
)
_OptionalAssessmentTargetTypeDef = TypedDict(
    "_OptionalAssessmentTargetTypeDef",
    {
        "resourceGroupArn": str,
    },
    total=False,
)

class AssessmentTargetTypeDef(_RequiredAssessmentTargetTypeDef, _OptionalAssessmentTargetTypeDef):
    pass

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "value": str,
    },
    total=False,
)

class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass

_RequiredCreateAssessmentTargetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssessmentTargetRequestRequestTypeDef",
    {
        "assessmentTargetName": str,
    },
)
_OptionalCreateAssessmentTargetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssessmentTargetRequestRequestTypeDef",
    {
        "resourceGroupArn": str,
    },
    total=False,
)

class CreateAssessmentTargetRequestRequestTypeDef(
    _RequiredCreateAssessmentTargetRequestRequestTypeDef,
    _OptionalCreateAssessmentTargetRequestRequestTypeDef,
):
    pass

CreateExclusionsPreviewRequestRequestTypeDef = TypedDict(
    "CreateExclusionsPreviewRequestRequestTypeDef",
    {
        "assessmentTemplateArn": str,
    },
)

_RequiredResourceGroupTagTypeDef = TypedDict(
    "_RequiredResourceGroupTagTypeDef",
    {
        "key": str,
    },
)
_OptionalResourceGroupTagTypeDef = TypedDict(
    "_OptionalResourceGroupTagTypeDef",
    {
        "value": str,
    },
    total=False,
)

class ResourceGroupTagTypeDef(_RequiredResourceGroupTagTypeDef, _OptionalResourceGroupTagTypeDef):
    pass

DeleteAssessmentRunRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentRunRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
    },
)

DeleteAssessmentTargetRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentTargetRequestRequestTypeDef",
    {
        "assessmentTargetArn": str,
    },
)

DeleteAssessmentTemplateRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentTemplateRequestRequestTypeDef",
    {
        "assessmentTemplateArn": str,
    },
)

DescribeAssessmentRunsRequestRequestTypeDef = TypedDict(
    "DescribeAssessmentRunsRequestRequestTypeDef",
    {
        "assessmentRunArns": Sequence[str],
    },
)

DescribeAssessmentTargetsRequestRequestTypeDef = TypedDict(
    "DescribeAssessmentTargetsRequestRequestTypeDef",
    {
        "assessmentTargetArns": Sequence[str],
    },
)

DescribeAssessmentTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeAssessmentTemplatesRequestRequestTypeDef",
    {
        "assessmentTemplateArns": Sequence[str],
    },
)

_RequiredDescribeExclusionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeExclusionsRequestRequestTypeDef",
    {
        "exclusionArns": Sequence[str],
    },
)
_OptionalDescribeExclusionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeExclusionsRequestRequestTypeDef",
    {
        "locale": Literal["EN_US"],
    },
    total=False,
)

class DescribeExclusionsRequestRequestTypeDef(
    _RequiredDescribeExclusionsRequestRequestTypeDef,
    _OptionalDescribeExclusionsRequestRequestTypeDef,
):
    pass

_RequiredDescribeFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeFindingsRequestRequestTypeDef",
    {
        "findingArns": Sequence[str],
    },
)
_OptionalDescribeFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeFindingsRequestRequestTypeDef",
    {
        "locale": Literal["EN_US"],
    },
    total=False,
)

class DescribeFindingsRequestRequestTypeDef(
    _RequiredDescribeFindingsRequestRequestTypeDef, _OptionalDescribeFindingsRequestRequestTypeDef
):
    pass

DescribeResourceGroupsRequestRequestTypeDef = TypedDict(
    "DescribeResourceGroupsRequestRequestTypeDef",
    {
        "resourceGroupArns": Sequence[str],
    },
)

_RequiredDescribeRulesPackagesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRulesPackagesRequestRequestTypeDef",
    {
        "rulesPackageArns": Sequence[str],
    },
)
_OptionalDescribeRulesPackagesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRulesPackagesRequestRequestTypeDef",
    {
        "locale": Literal["EN_US"],
    },
    total=False,
)

class DescribeRulesPackagesRequestRequestTypeDef(
    _RequiredDescribeRulesPackagesRequestRequestTypeDef,
    _OptionalDescribeRulesPackagesRequestRequestTypeDef,
):
    pass

_RequiredRulesPackageTypeDef = TypedDict(
    "_RequiredRulesPackageTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "provider": str,
    },
)
_OptionalRulesPackageTypeDef = TypedDict(
    "_OptionalRulesPackageTypeDef",
    {
        "description": str,
    },
    total=False,
)

class RulesPackageTypeDef(_RequiredRulesPackageTypeDef, _OptionalRulesPackageTypeDef):
    pass

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "event": InspectorEventType,
        "subscribedAt": datetime,
    },
)

ScopeTypeDef = TypedDict(
    "ScopeTypeDef",
    {
        "key": ScopeTypeType,
        "value": str,
    },
    total=False,
)

_RequiredInspectorServiceAttributesTypeDef = TypedDict(
    "_RequiredInspectorServiceAttributesTypeDef",
    {
        "schemaVersion": int,
    },
)
_OptionalInspectorServiceAttributesTypeDef = TypedDict(
    "_OptionalInspectorServiceAttributesTypeDef",
    {
        "assessmentRunArn": str,
        "rulesPackageArn": str,
    },
    total=False,
)

class InspectorServiceAttributesTypeDef(
    _RequiredInspectorServiceAttributesTypeDef, _OptionalInspectorServiceAttributesTypeDef
):
    pass

GetAssessmentReportRequestRequestTypeDef = TypedDict(
    "GetAssessmentReportRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
        "reportFileFormat": ReportFileFormatType,
        "reportType": ReportTypeType,
    },
)

_RequiredGetExclusionsPreviewRequestRequestTypeDef = TypedDict(
    "_RequiredGetExclusionsPreviewRequestRequestTypeDef",
    {
        "assessmentTemplateArn": str,
        "previewToken": str,
    },
)
_OptionalGetExclusionsPreviewRequestRequestTypeDef = TypedDict(
    "_OptionalGetExclusionsPreviewRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "locale": Literal["EN_US"],
    },
    total=False,
)

class GetExclusionsPreviewRequestRequestTypeDef(
    _RequiredGetExclusionsPreviewRequestRequestTypeDef,
    _OptionalGetExclusionsPreviewRequestRequestTypeDef,
):
    pass

GetTelemetryMetadataRequestRequestTypeDef = TypedDict(
    "GetTelemetryMetadataRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
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

ListEventSubscriptionsRequestRequestTypeDef = TypedDict(
    "ListEventSubscriptionsRequestRequestTypeDef",
    {
        "resourceArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListExclusionsRequestRequestTypeDef = TypedDict(
    "_RequiredListExclusionsRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
    },
)
_OptionalListExclusionsRequestRequestTypeDef = TypedDict(
    "_OptionalListExclusionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListExclusionsRequestRequestTypeDef(
    _RequiredListExclusionsRequestRequestTypeDef, _OptionalListExclusionsRequestRequestTypeDef
):
    pass

ListRulesPackagesRequestRequestTypeDef = TypedDict(
    "ListRulesPackagesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

PrivateIpTypeDef = TypedDict(
    "PrivateIpTypeDef",
    {
        "privateDnsName": str,
        "privateIpAddress": str,
    },
    total=False,
)

SecurityGroupTypeDef = TypedDict(
    "SecurityGroupTypeDef",
    {
        "groupName": str,
        "groupId": str,
    },
    total=False,
)

_RequiredPreviewAgentsRequestRequestTypeDef = TypedDict(
    "_RequiredPreviewAgentsRequestRequestTypeDef",
    {
        "previewAgentsArn": str,
    },
)
_OptionalPreviewAgentsRequestRequestTypeDef = TypedDict(
    "_OptionalPreviewAgentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class PreviewAgentsRequestRequestTypeDef(
    _RequiredPreviewAgentsRequestRequestTypeDef, _OptionalPreviewAgentsRequestRequestTypeDef
):
    pass

RegisterCrossAccountAccessRoleRequestRequestTypeDef = TypedDict(
    "RegisterCrossAccountAccessRoleRequestRequestTypeDef",
    {
        "roleArn": str,
    },
)

RemoveAttributesFromFindingsRequestRequestTypeDef = TypedDict(
    "RemoveAttributesFromFindingsRequestRequestTypeDef",
    {
        "findingArns": Sequence[str],
        "attributeKeys": Sequence[str],
    },
)

_RequiredStartAssessmentRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartAssessmentRunRequestRequestTypeDef",
    {
        "assessmentTemplateArn": str,
    },
)
_OptionalStartAssessmentRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartAssessmentRunRequestRequestTypeDef",
    {
        "assessmentRunName": str,
    },
    total=False,
)

class StartAssessmentRunRequestRequestTypeDef(
    _RequiredStartAssessmentRunRequestRequestTypeDef,
    _OptionalStartAssessmentRunRequestRequestTypeDef,
):
    pass

_RequiredStopAssessmentRunRequestRequestTypeDef = TypedDict(
    "_RequiredStopAssessmentRunRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
    },
)
_OptionalStopAssessmentRunRequestRequestTypeDef = TypedDict(
    "_OptionalStopAssessmentRunRequestRequestTypeDef",
    {
        "stopAction": StopActionType,
    },
    total=False,
)

class StopAssessmentRunRequestRequestTypeDef(
    _RequiredStopAssessmentRunRequestRequestTypeDef, _OptionalStopAssessmentRunRequestRequestTypeDef
):
    pass

SubscribeToEventRequestRequestTypeDef = TypedDict(
    "SubscribeToEventRequestRequestTypeDef",
    {
        "resourceArn": str,
        "event": InspectorEventType,
        "topicArn": str,
    },
)

UnsubscribeFromEventRequestRequestTypeDef = TypedDict(
    "UnsubscribeFromEventRequestRequestTypeDef",
    {
        "resourceArn": str,
        "event": InspectorEventType,
        "topicArn": str,
    },
)

_RequiredUpdateAssessmentTargetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssessmentTargetRequestRequestTypeDef",
    {
        "assessmentTargetArn": str,
        "assessmentTargetName": str,
    },
)
_OptionalUpdateAssessmentTargetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssessmentTargetRequestRequestTypeDef",
    {
        "resourceGroupArn": str,
    },
    total=False,
)

class UpdateAssessmentTargetRequestRequestTypeDef(
    _RequiredUpdateAssessmentTargetRequestRequestTypeDef,
    _OptionalUpdateAssessmentTargetRequestRequestTypeDef,
):
    pass

AddAttributesToFindingsRequestRequestTypeDef = TypedDict(
    "AddAttributesToFindingsRequestRequestTypeDef",
    {
        "findingArns": Sequence[str],
        "attributes": Sequence[AttributeTypeDef],
    },
)

_RequiredAssessmentTemplateTypeDef = TypedDict(
    "_RequiredAssessmentTemplateTypeDef",
    {
        "arn": str,
        "name": str,
        "assessmentTargetArn": str,
        "durationInSeconds": int,
        "rulesPackageArns": List[str],
        "userAttributesForFindings": List[AttributeTypeDef],
        "assessmentRunCount": int,
        "createdAt": datetime,
    },
)
_OptionalAssessmentTemplateTypeDef = TypedDict(
    "_OptionalAssessmentTemplateTypeDef",
    {
        "lastAssessmentRunArn": str,
    },
    total=False,
)

class AssessmentTemplateTypeDef(
    _RequiredAssessmentTemplateTypeDef, _OptionalAssessmentTemplateTypeDef
):
    pass

_RequiredCreateAssessmentTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssessmentTemplateRequestRequestTypeDef",
    {
        "assessmentTargetArn": str,
        "assessmentTemplateName": str,
        "durationInSeconds": int,
        "rulesPackageArns": Sequence[str],
    },
)
_OptionalCreateAssessmentTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssessmentTemplateRequestRequestTypeDef",
    {
        "userAttributesForFindings": Sequence[AttributeTypeDef],
    },
    total=False,
)

class CreateAssessmentTemplateRequestRequestTypeDef(
    _RequiredCreateAssessmentTemplateRequestRequestTypeDef,
    _OptionalCreateAssessmentTemplateRequestRequestTypeDef,
):
    pass

AddAttributesToFindingsResponseTypeDef = TypedDict(
    "AddAttributesToFindingsResponseTypeDef",
    {
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssessmentTargetResponseTypeDef = TypedDict(
    "CreateAssessmentTargetResponseTypeDef",
    {
        "assessmentTargetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssessmentTemplateResponseTypeDef = TypedDict(
    "CreateAssessmentTemplateResponseTypeDef",
    {
        "assessmentTemplateArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExclusionsPreviewResponseTypeDef = TypedDict(
    "CreateExclusionsPreviewResponseTypeDef",
    {
        "previewToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourceGroupResponseTypeDef = TypedDict(
    "CreateResourceGroupResponseTypeDef",
    {
        "resourceGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCrossAccountAccessRoleResponseTypeDef = TypedDict(
    "DescribeCrossAccountAccessRoleResponseTypeDef",
    {
        "roleArn": str,
        "valid": bool,
        "registeredAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssessmentReportResponseTypeDef = TypedDict(
    "GetAssessmentReportResponseTypeDef",
    {
        "status": ReportStatusType,
        "url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentRunsResponseTypeDef = TypedDict(
    "ListAssessmentRunsResponseTypeDef",
    {
        "assessmentRunArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentTargetsResponseTypeDef = TypedDict(
    "ListAssessmentTargetsResponseTypeDef",
    {
        "assessmentTargetArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentTemplatesResponseTypeDef = TypedDict(
    "ListAssessmentTemplatesResponseTypeDef",
    {
        "assessmentTemplateArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListExclusionsResponseTypeDef = TypedDict(
    "ListExclusionsResponseTypeDef",
    {
        "exclusionArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "findingArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRulesPackagesResponseTypeDef = TypedDict(
    "ListRulesPackagesResponseTypeDef",
    {
        "rulesPackageArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveAttributesFromFindingsResponseTypeDef = TypedDict(
    "RemoveAttributesFromFindingsResponseTypeDef",
    {
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssessmentRunResponseTypeDef = TypedDict(
    "StartAssessmentRunResponseTypeDef",
    {
        "assessmentRunArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAssessmentRunAgentsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssessmentRunAgentsRequestRequestTypeDef",
    {
        "assessmentRunArn": str,
    },
)
_OptionalListAssessmentRunAgentsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssessmentRunAgentsRequestRequestTypeDef",
    {
        "filter": AgentFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListAssessmentRunAgentsRequestRequestTypeDef(
    _RequiredListAssessmentRunAgentsRequestRequestTypeDef,
    _OptionalListAssessmentRunAgentsRequestRequestTypeDef,
):
    pass

PreviewAgentsResponseTypeDef = TypedDict(
    "PreviewAgentsResponseTypeDef",
    {
        "agentPreviews": List[AgentPreviewTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssessmentRunAgentTypeDef = TypedDict(
    "_RequiredAssessmentRunAgentTypeDef",
    {
        "agentId": str,
        "assessmentRunArn": str,
        "agentHealth": AgentHealthType,
        "agentHealthCode": AgentHealthCodeType,
        "telemetryMetadata": List[TelemetryMetadataTypeDef],
    },
)
_OptionalAssessmentRunAgentTypeDef = TypedDict(
    "_OptionalAssessmentRunAgentTypeDef",
    {
        "agentHealthDetails": str,
        "autoScalingGroup": str,
    },
    total=False,
)

class AssessmentRunAgentTypeDef(
    _RequiredAssessmentRunAgentTypeDef, _OptionalAssessmentRunAgentTypeDef
):
    pass

GetTelemetryMetadataResponseTypeDef = TypedDict(
    "GetTelemetryMetadataResponseTypeDef",
    {
        "telemetryMetadata": List[TelemetryMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssessmentTemplateFilterTypeDef = TypedDict(
    "AssessmentTemplateFilterTypeDef",
    {
        "namePattern": str,
        "durationRange": DurationRangeTypeDef,
        "rulesPackageArns": Sequence[str],
    },
    total=False,
)

AssessmentRunFilterTypeDef = TypedDict(
    "AssessmentRunFilterTypeDef",
    {
        "namePattern": str,
        "states": Sequence[AssessmentRunStateType],
        "durationRange": DurationRangeTypeDef,
        "rulesPackageArns": Sequence[str],
        "startTimeRange": TimestampRangeTypeDef,
        "completionTimeRange": TimestampRangeTypeDef,
        "stateChangeTimeRange": TimestampRangeTypeDef,
    },
    total=False,
)

FindingFilterTypeDef = TypedDict(
    "FindingFilterTypeDef",
    {
        "agentIds": Sequence[str],
        "autoScalingGroups": Sequence[str],
        "ruleNames": Sequence[str],
        "severities": Sequence[SeverityType],
        "rulesPackageArns": Sequence[str],
        "attributes": Sequence[AttributeTypeDef],
        "userAttributes": Sequence[AttributeTypeDef],
        "creationTimeRange": TimestampRangeTypeDef,
    },
    total=False,
)

_RequiredAssessmentRunTypeDef = TypedDict(
    "_RequiredAssessmentRunTypeDef",
    {
        "arn": str,
        "name": str,
        "assessmentTemplateArn": str,
        "state": AssessmentRunStateType,
        "durationInSeconds": int,
        "rulesPackageArns": List[str],
        "userAttributesForFindings": List[AttributeTypeDef],
        "createdAt": datetime,
        "stateChangedAt": datetime,
        "dataCollected": bool,
        "stateChanges": List[AssessmentRunStateChangeTypeDef],
        "notifications": List[AssessmentRunNotificationTypeDef],
        "findingCounts": Dict[SeverityType, int],
    },
)
_OptionalAssessmentRunTypeDef = TypedDict(
    "_OptionalAssessmentRunTypeDef",
    {
        "startedAt": datetime,
        "completedAt": datetime,
    },
    total=False,
)

class AssessmentRunTypeDef(_RequiredAssessmentRunTypeDef, _OptionalAssessmentRunTypeDef):
    pass

ListAssessmentTargetsRequestRequestTypeDef = TypedDict(
    "ListAssessmentTargetsRequestRequestTypeDef",
    {
        "filter": AssessmentTargetFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

DescribeAssessmentTargetsResponseTypeDef = TypedDict(
    "DescribeAssessmentTargetsResponseTypeDef",
    {
        "assessmentTargets": List[AssessmentTargetTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSetTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredSetTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalSetTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalSetTagsForResourceRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class SetTagsForResourceRequestRequestTypeDef(
    _RequiredSetTagsForResourceRequestRequestTypeDef,
    _OptionalSetTagsForResourceRequestRequestTypeDef,
):
    pass

CreateResourceGroupRequestRequestTypeDef = TypedDict(
    "CreateResourceGroupRequestRequestTypeDef",
    {
        "resourceGroupTags": Sequence[ResourceGroupTagTypeDef],
    },
)

ResourceGroupTypeDef = TypedDict(
    "ResourceGroupTypeDef",
    {
        "arn": str,
        "tags": List[ResourceGroupTagTypeDef],
        "createdAt": datetime,
    },
)

DescribeRulesPackagesResponseTypeDef = TypedDict(
    "DescribeRulesPackagesResponseTypeDef",
    {
        "rulesPackages": List[RulesPackageTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "resourceArn": str,
        "topicArn": str,
        "eventSubscriptions": List[EventSubscriptionTypeDef],
    },
)

_RequiredExclusionPreviewTypeDef = TypedDict(
    "_RequiredExclusionPreviewTypeDef",
    {
        "title": str,
        "description": str,
        "recommendation": str,
        "scopes": List[ScopeTypeDef],
    },
)
_OptionalExclusionPreviewTypeDef = TypedDict(
    "_OptionalExclusionPreviewTypeDef",
    {
        "attributes": List[AttributeTypeDef],
    },
    total=False,
)

class ExclusionPreviewTypeDef(_RequiredExclusionPreviewTypeDef, _OptionalExclusionPreviewTypeDef):
    pass

_RequiredExclusionTypeDef = TypedDict(
    "_RequiredExclusionTypeDef",
    {
        "arn": str,
        "title": str,
        "description": str,
        "recommendation": str,
        "scopes": List[ScopeTypeDef],
    },
)
_OptionalExclusionTypeDef = TypedDict(
    "_OptionalExclusionTypeDef",
    {
        "attributes": List[AttributeTypeDef],
    },
    total=False,
)

class ExclusionTypeDef(_RequiredExclusionTypeDef, _OptionalExclusionTypeDef):
    pass

_RequiredListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef = TypedDict(
    "_RequiredListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef",
    {
        "assessmentRunArn": str,
    },
)
_OptionalListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef = TypedDict(
    "_OptionalListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef",
    {
        "filter": AgentFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef(
    _RequiredListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef,
    _OptionalListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef,
):
    pass

ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef = TypedDict(
    "ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef",
    {
        "filter": AssessmentTargetFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef = TypedDict(
    "ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef",
    {
        "resourceArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListExclusionsRequestListExclusionsPaginateTypeDef = TypedDict(
    "_RequiredListExclusionsRequestListExclusionsPaginateTypeDef",
    {
        "assessmentRunArn": str,
    },
)
_OptionalListExclusionsRequestListExclusionsPaginateTypeDef = TypedDict(
    "_OptionalListExclusionsRequestListExclusionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListExclusionsRequestListExclusionsPaginateTypeDef(
    _RequiredListExclusionsRequestListExclusionsPaginateTypeDef,
    _OptionalListExclusionsRequestListExclusionsPaginateTypeDef,
):
    pass

ListRulesPackagesRequestListRulesPackagesPaginateTypeDef = TypedDict(
    "ListRulesPackagesRequestListRulesPackagesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredPreviewAgentsRequestPreviewAgentsPaginateTypeDef = TypedDict(
    "_RequiredPreviewAgentsRequestPreviewAgentsPaginateTypeDef",
    {
        "previewAgentsArn": str,
    },
)
_OptionalPreviewAgentsRequestPreviewAgentsPaginateTypeDef = TypedDict(
    "_OptionalPreviewAgentsRequestPreviewAgentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class PreviewAgentsRequestPreviewAgentsPaginateTypeDef(
    _RequiredPreviewAgentsRequestPreviewAgentsPaginateTypeDef,
    _OptionalPreviewAgentsRequestPreviewAgentsPaginateTypeDef,
):
    pass

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "networkInterfaceId": str,
        "subnetId": str,
        "vpcId": str,
        "privateDnsName": str,
        "privateIpAddress": str,
        "privateIpAddresses": List[PrivateIpTypeDef],
        "publicDnsName": str,
        "publicIp": str,
        "ipv6Addresses": List[str],
        "securityGroups": List[SecurityGroupTypeDef],
    },
    total=False,
)

DescribeAssessmentTemplatesResponseTypeDef = TypedDict(
    "DescribeAssessmentTemplatesResponseTypeDef",
    {
        "assessmentTemplates": List[AssessmentTemplateTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentRunAgentsResponseTypeDef = TypedDict(
    "ListAssessmentRunAgentsResponseTypeDef",
    {
        "assessmentRunAgents": List[AssessmentRunAgentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef = TypedDict(
    "ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef",
    {
        "assessmentTargetArns": Sequence[str],
        "filter": AssessmentTemplateFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAssessmentTemplatesRequestRequestTypeDef = TypedDict(
    "ListAssessmentTemplatesRequestRequestTypeDef",
    {
        "assessmentTargetArns": Sequence[str],
        "filter": AssessmentTemplateFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef = TypedDict(
    "ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef",
    {
        "assessmentTemplateArns": Sequence[str],
        "filter": AssessmentRunFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAssessmentRunsRequestRequestTypeDef = TypedDict(
    "ListAssessmentRunsRequestRequestTypeDef",
    {
        "assessmentTemplateArns": Sequence[str],
        "filter": AssessmentRunFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "ListFindingsRequestListFindingsPaginateTypeDef",
    {
        "assessmentRunArns": Sequence[str],
        "filter": FindingFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFindingsRequestRequestTypeDef = TypedDict(
    "ListFindingsRequestRequestTypeDef",
    {
        "assessmentRunArns": Sequence[str],
        "filter": FindingFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

DescribeAssessmentRunsResponseTypeDef = TypedDict(
    "DescribeAssessmentRunsResponseTypeDef",
    {
        "assessmentRuns": List[AssessmentRunTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResourceGroupsResponseTypeDef = TypedDict(
    "DescribeResourceGroupsResponseTypeDef",
    {
        "resourceGroups": List[ResourceGroupTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEventSubscriptionsResponseTypeDef = TypedDict(
    "ListEventSubscriptionsResponseTypeDef",
    {
        "subscriptions": List[SubscriptionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExclusionsPreviewResponseTypeDef = TypedDict(
    "GetExclusionsPreviewResponseTypeDef",
    {
        "previewStatus": PreviewStatusType,
        "exclusionPreviews": List[ExclusionPreviewTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeExclusionsResponseTypeDef = TypedDict(
    "DescribeExclusionsResponseTypeDef",
    {
        "exclusions": Dict[str, ExclusionTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssetAttributesTypeDef = TypedDict(
    "_RequiredAssetAttributesTypeDef",
    {
        "schemaVersion": int,
    },
)
_OptionalAssetAttributesTypeDef = TypedDict(
    "_OptionalAssetAttributesTypeDef",
    {
        "agentId": str,
        "autoScalingGroup": str,
        "amiId": str,
        "hostname": str,
        "ipv4Addresses": List[str],
        "tags": List[TagTypeDef],
        "networkInterfaces": List[NetworkInterfaceTypeDef],
    },
    total=False,
)

class AssetAttributesTypeDef(_RequiredAssetAttributesTypeDef, _OptionalAssetAttributesTypeDef):
    pass

_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "arn": str,
        "attributes": List[AttributeTypeDef],
        "userAttributes": List[AttributeTypeDef],
        "createdAt": datetime,
        "updatedAt": datetime,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "schemaVersion": int,
        "service": str,
        "serviceAttributes": InspectorServiceAttributesTypeDef,
        "assetType": Literal["ec2-instance"],
        "assetAttributes": AssetAttributesTypeDef,
        "id": str,
        "title": str,
        "description": str,
        "recommendation": str,
        "severity": SeverityType,
        "numericSeverity": float,
        "confidence": int,
        "indicatorOfCompromise": bool,
    },
    total=False,
)

class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass

DescribeFindingsResponseTypeDef = TypedDict(
    "DescribeFindingsResponseTypeDef",
    {
        "findings": List[FindingTypeDef],
        "failedItems": Dict[str, FailedItemDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
