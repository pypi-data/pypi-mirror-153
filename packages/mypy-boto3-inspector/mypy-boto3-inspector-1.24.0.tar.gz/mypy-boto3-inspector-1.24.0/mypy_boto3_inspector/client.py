"""
Type annotations for inspector service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_inspector.client import InspectorClient

    session = Session()
    client: InspectorClient = session.client("inspector")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import InspectorEventType, ReportFileFormatType, ReportTypeType, StopActionType
from .paginator import (
    ListAssessmentRunAgentsPaginator,
    ListAssessmentRunsPaginator,
    ListAssessmentTargetsPaginator,
    ListAssessmentTemplatesPaginator,
    ListEventSubscriptionsPaginator,
    ListExclusionsPaginator,
    ListFindingsPaginator,
    ListRulesPackagesPaginator,
    PreviewAgentsPaginator,
)
from .type_defs import (
    AddAttributesToFindingsResponseTypeDef,
    AgentFilterTypeDef,
    AssessmentRunFilterTypeDef,
    AssessmentTargetFilterTypeDef,
    AssessmentTemplateFilterTypeDef,
    AttributeTypeDef,
    CreateAssessmentTargetResponseTypeDef,
    CreateAssessmentTemplateResponseTypeDef,
    CreateExclusionsPreviewResponseTypeDef,
    CreateResourceGroupResponseTypeDef,
    DescribeAssessmentRunsResponseTypeDef,
    DescribeAssessmentTargetsResponseTypeDef,
    DescribeAssessmentTemplatesResponseTypeDef,
    DescribeCrossAccountAccessRoleResponseTypeDef,
    DescribeExclusionsResponseTypeDef,
    DescribeFindingsResponseTypeDef,
    DescribeResourceGroupsResponseTypeDef,
    DescribeRulesPackagesResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FindingFilterTypeDef,
    GetAssessmentReportResponseTypeDef,
    GetExclusionsPreviewResponseTypeDef,
    GetTelemetryMetadataResponseTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PreviewAgentsResponseTypeDef,
    RemoveAttributesFromFindingsResponseTypeDef,
    ResourceGroupTagTypeDef,
    StartAssessmentRunResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("InspectorClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AgentsAlreadyRunningAssessmentException: Type[BotocoreClientError]
    AssessmentRunInProgressException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidCrossAccountRoleException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NoSuchEntityException: Type[BotocoreClientError]
    PreviewGenerationInProgressException: Type[BotocoreClientError]
    ServiceTemporarilyUnavailableException: Type[BotocoreClientError]
    UnsupportedFeatureException: Type[BotocoreClientError]


class InspectorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        InspectorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#exceptions)
        """

    def add_attributes_to_findings(
        self, *, findingArns: Sequence[str], attributes: Sequence[AttributeTypeDef]
    ) -> AddAttributesToFindingsResponseTypeDef:
        """
        Assigns attributes (key and value pairs) to the findings that are specified by
        the ARNs of the findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.add_attributes_to_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#add_attributes_to_findings)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#can_paginate)
        """

    def create_assessment_target(
        self, *, assessmentTargetName: str, resourceGroupArn: str = ...
    ) -> CreateAssessmentTargetResponseTypeDef:
        """
        Creates a new assessment target using the ARN of the resource group that is
        generated by  CreateResourceGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_assessment_target)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#create_assessment_target)
        """

    def create_assessment_template(
        self,
        *,
        assessmentTargetArn: str,
        assessmentTemplateName: str,
        durationInSeconds: int,
        rulesPackageArns: Sequence[str],
        userAttributesForFindings: Sequence[AttributeTypeDef] = ...
    ) -> CreateAssessmentTemplateResponseTypeDef:
        """
        Creates an assessment template for the assessment target that is specified by
        the ARN of the assessment target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_assessment_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#create_assessment_template)
        """

    def create_exclusions_preview(
        self, *, assessmentTemplateArn: str
    ) -> CreateExclusionsPreviewResponseTypeDef:
        """
        Starts the generation of an exclusions preview for the specified assessment
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_exclusions_preview)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#create_exclusions_preview)
        """

    def create_resource_group(
        self, *, resourceGroupTags: Sequence[ResourceGroupTagTypeDef]
    ) -> CreateResourceGroupResponseTypeDef:
        """
        Creates a resource group using the specified set of tags (key and value pairs)
        that are used to select the EC2 instances to be included in an Amazon Inspector
        assessment target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_resource_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#create_resource_group)
        """

    def delete_assessment_run(self, *, assessmentRunArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the assessment run that is specified by the ARN of the assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.delete_assessment_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#delete_assessment_run)
        """

    def delete_assessment_target(self, *, assessmentTargetArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the assessment target that is specified by the ARN of the assessment
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.delete_assessment_target)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#delete_assessment_target)
        """

    def delete_assessment_template(
        self, *, assessmentTemplateArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the assessment template that is specified by the ARN of the assessment
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.delete_assessment_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#delete_assessment_template)
        """

    def describe_assessment_runs(
        self, *, assessmentRunArns: Sequence[str]
    ) -> DescribeAssessmentRunsResponseTypeDef:
        """
        Describes the assessment runs that are specified by the ARNs of the assessment
        runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_assessment_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_assessment_runs)
        """

    def describe_assessment_targets(
        self, *, assessmentTargetArns: Sequence[str]
    ) -> DescribeAssessmentTargetsResponseTypeDef:
        """
        Describes the assessment targets that are specified by the ARNs of the
        assessment targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_assessment_targets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_assessment_targets)
        """

    def describe_assessment_templates(
        self, *, assessmentTemplateArns: Sequence[str]
    ) -> DescribeAssessmentTemplatesResponseTypeDef:
        """
        Describes the assessment templates that are specified by the ARNs of the
        assessment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_assessment_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_assessment_templates)
        """

    def describe_cross_account_access_role(self) -> DescribeCrossAccountAccessRoleResponseTypeDef:
        """
        Describes the IAM role that enables Amazon Inspector to access your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_cross_account_access_role)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_cross_account_access_role)
        """

    def describe_exclusions(
        self, *, exclusionArns: Sequence[str], locale: Literal["EN_US"] = ...
    ) -> DescribeExclusionsResponseTypeDef:
        """
        Describes the exclusions that are specified by the exclusions' ARNs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_exclusions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_exclusions)
        """

    def describe_findings(
        self, *, findingArns: Sequence[str], locale: Literal["EN_US"] = ...
    ) -> DescribeFindingsResponseTypeDef:
        """
        Describes the findings that are specified by the ARNs of the findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_findings)
        """

    def describe_resource_groups(
        self, *, resourceGroupArns: Sequence[str]
    ) -> DescribeResourceGroupsResponseTypeDef:
        """
        Describes the resource groups that are specified by the ARNs of the resource
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_resource_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_resource_groups)
        """

    def describe_rules_packages(
        self, *, rulesPackageArns: Sequence[str], locale: Literal["EN_US"] = ...
    ) -> DescribeRulesPackagesResponseTypeDef:
        """
        Describes the rules packages that are specified by the ARNs of the rules
        packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_rules_packages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#describe_rules_packages)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#generate_presigned_url)
        """

    def get_assessment_report(
        self,
        *,
        assessmentRunArn: str,
        reportFileFormat: ReportFileFormatType,
        reportType: ReportTypeType
    ) -> GetAssessmentReportResponseTypeDef:
        """
        Produces an assessment report that includes detailed and comprehensive results
        of a specified assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_assessment_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_assessment_report)
        """

    def get_exclusions_preview(
        self,
        *,
        assessmentTemplateArn: str,
        previewToken: str,
        nextToken: str = ...,
        maxResults: int = ...,
        locale: Literal["EN_US"] = ...
    ) -> GetExclusionsPreviewResponseTypeDef:
        """
        Retrieves the exclusions preview (a list of ExclusionPreview objects) specified
        by the preview token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_exclusions_preview)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_exclusions_preview)
        """

    def get_telemetry_metadata(
        self, *, assessmentRunArn: str
    ) -> GetTelemetryMetadataResponseTypeDef:
        """
        Information about the data that is collected for the specified assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_telemetry_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_telemetry_metadata)
        """

    def list_assessment_run_agents(
        self,
        *,
        assessmentRunArn: str,
        filter: AgentFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentRunAgentsResponseTypeDef:
        """
        Lists the agents of the assessment runs that are specified by the ARNs of the
        assessment runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_run_agents)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_assessment_run_agents)
        """

    def list_assessment_runs(
        self,
        *,
        assessmentTemplateArns: Sequence[str] = ...,
        filter: AssessmentRunFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentRunsResponseTypeDef:
        """
        Lists the assessment runs that correspond to the assessment templates that are
        specified by the ARNs of the assessment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_assessment_runs)
        """

    def list_assessment_targets(
        self,
        *,
        filter: AssessmentTargetFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentTargetsResponseTypeDef:
        """
        Lists the ARNs of the assessment targets within this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_targets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_assessment_targets)
        """

    def list_assessment_templates(
        self,
        *,
        assessmentTargetArns: Sequence[str] = ...,
        filter: AssessmentTemplateFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentTemplatesResponseTypeDef:
        """
        Lists the assessment templates that correspond to the assessment targets that
        are specified by the ARNs of the assessment targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_assessment_templates)
        """

    def list_event_subscriptions(
        self, *, resourceArn: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListEventSubscriptionsResponseTypeDef:
        """
        Lists all the event subscriptions for the assessment template that is specified
        by the ARN of the assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_event_subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_event_subscriptions)
        """

    def list_exclusions(
        self, *, assessmentRunArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListExclusionsResponseTypeDef:
        """
        List exclusions that are generated by the assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_exclusions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_exclusions)
        """

    def list_findings(
        self,
        *,
        assessmentRunArns: Sequence[str] = ...,
        filter: FindingFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListFindingsResponseTypeDef:
        """
        Lists findings that are generated by the assessment runs that are specified by
        the ARNs of the assessment runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_findings)
        """

    def list_rules_packages(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListRulesPackagesResponseTypeDef:
        """
        Lists all available Amazon Inspector rules packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_rules_packages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_rules_packages)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with an assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#list_tags_for_resource)
        """

    def preview_agents(
        self, *, previewAgentsArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> PreviewAgentsResponseTypeDef:
        """
        Previews the agents installed on the EC2 instances that are part of the
        specified assessment target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.preview_agents)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#preview_agents)
        """

    def register_cross_account_access_role(self, *, roleArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Registers the IAM role that grants Amazon Inspector access to AWS Services
        needed to perform security assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.register_cross_account_access_role)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#register_cross_account_access_role)
        """

    def remove_attributes_from_findings(
        self, *, findingArns: Sequence[str], attributeKeys: Sequence[str]
    ) -> RemoveAttributesFromFindingsResponseTypeDef:
        """
        Removes entire attributes (key and value pairs) from the findings that are
        specified by the ARNs of the findings where an attribute with the specified key
        exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.remove_attributes_from_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#remove_attributes_from_findings)
        """

    def set_tags_for_resource(
        self, *, resourceArn: str, tags: Sequence[TagTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets tags (key and value pairs) to the assessment template that is specified by
        the ARN of the assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.set_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#set_tags_for_resource)
        """

    def start_assessment_run(
        self, *, assessmentTemplateArn: str, assessmentRunName: str = ...
    ) -> StartAssessmentRunResponseTypeDef:
        """
        Starts the assessment run specified by the ARN of the assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.start_assessment_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#start_assessment_run)
        """

    def stop_assessment_run(
        self, *, assessmentRunArn: str, stopAction: StopActionType = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops the assessment run that is specified by the ARN of the assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.stop_assessment_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#stop_assessment_run)
        """

    def subscribe_to_event(
        self, *, resourceArn: str, event: InspectorEventType, topicArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables the process of sending Amazon Simple Notification Service (SNS)
        notifications about a specified event to a specified SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.subscribe_to_event)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#subscribe_to_event)
        """

    def unsubscribe_from_event(
        self, *, resourceArn: str, event: InspectorEventType, topicArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the process of sending Amazon Simple Notification Service (SNS)
        notifications about a specified event to a specified SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.unsubscribe_from_event)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#unsubscribe_from_event)
        """

    def update_assessment_target(
        self, *, assessmentTargetArn: str, assessmentTargetName: str, resourceGroupArn: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the assessment target that is specified by the ARN of the assessment
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.update_assessment_target)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#update_assessment_target)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_run_agents"]
    ) -> ListAssessmentRunAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_runs"]
    ) -> ListAssessmentRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_targets"]
    ) -> ListAssessmentTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_templates"]
    ) -> ListAssessmentTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_subscriptions"]
    ) -> ListEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_exclusions"]) -> ListExclusionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rules_packages"]
    ) -> ListRulesPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["preview_agents"]) -> PreviewAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/client/#get_paginator)
        """
