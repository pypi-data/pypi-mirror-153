"""
Type annotations for iot service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot.client import IoTClient
    from mypy_boto3_iot.paginator import (
        GetBehaviorModelTrainingSummariesPaginator,
        ListActiveViolationsPaginator,
        ListAttachedPoliciesPaginator,
        ListAuditFindingsPaginator,
        ListAuditMitigationActionsExecutionsPaginator,
        ListAuditMitigationActionsTasksPaginator,
        ListAuditSuppressionsPaginator,
        ListAuditTasksPaginator,
        ListAuthorizersPaginator,
        ListBillingGroupsPaginator,
        ListCACertificatesPaginator,
        ListCertificatesPaginator,
        ListCertificatesByCAPaginator,
        ListCustomMetricsPaginator,
        ListDetectMitigationActionsExecutionsPaginator,
        ListDetectMitigationActionsTasksPaginator,
        ListDimensionsPaginator,
        ListDomainConfigurationsPaginator,
        ListFleetMetricsPaginator,
        ListIndicesPaginator,
        ListJobExecutionsForJobPaginator,
        ListJobExecutionsForThingPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListMetricValuesPaginator,
        ListMitigationActionsPaginator,
        ListOTAUpdatesPaginator,
        ListOutgoingCertificatesPaginator,
        ListPoliciesPaginator,
        ListPolicyPrincipalsPaginator,
        ListPrincipalPoliciesPaginator,
        ListPrincipalThingsPaginator,
        ListProvisioningTemplateVersionsPaginator,
        ListProvisioningTemplatesPaginator,
        ListRoleAliasesPaginator,
        ListScheduledAuditsPaginator,
        ListSecurityProfilesPaginator,
        ListSecurityProfilesForTargetPaginator,
        ListStreamsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
        ListTargetsForSecurityProfilePaginator,
        ListThingGroupsPaginator,
        ListThingGroupsForThingPaginator,
        ListThingPrincipalsPaginator,
        ListThingRegistrationTaskReportsPaginator,
        ListThingRegistrationTasksPaginator,
        ListThingTypesPaginator,
        ListThingsPaginator,
        ListThingsInBillingGroupPaginator,
        ListThingsInThingGroupPaginator,
        ListTopicRuleDestinationsPaginator,
        ListTopicRulesPaginator,
        ListV2LoggingLevelsPaginator,
        ListViolationEventsPaginator,
    )

    session = Session()
    client: IoTClient = session.client("iot")

    get_behavior_model_training_summaries_paginator: GetBehaviorModelTrainingSummariesPaginator = client.get_paginator("get_behavior_model_training_summaries")
    list_active_violations_paginator: ListActiveViolationsPaginator = client.get_paginator("list_active_violations")
    list_attached_policies_paginator: ListAttachedPoliciesPaginator = client.get_paginator("list_attached_policies")
    list_audit_findings_paginator: ListAuditFindingsPaginator = client.get_paginator("list_audit_findings")
    list_audit_mitigation_actions_executions_paginator: ListAuditMitigationActionsExecutionsPaginator = client.get_paginator("list_audit_mitigation_actions_executions")
    list_audit_mitigation_actions_tasks_paginator: ListAuditMitigationActionsTasksPaginator = client.get_paginator("list_audit_mitigation_actions_tasks")
    list_audit_suppressions_paginator: ListAuditSuppressionsPaginator = client.get_paginator("list_audit_suppressions")
    list_audit_tasks_paginator: ListAuditTasksPaginator = client.get_paginator("list_audit_tasks")
    list_authorizers_paginator: ListAuthorizersPaginator = client.get_paginator("list_authorizers")
    list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
    list_ca_certificates_paginator: ListCACertificatesPaginator = client.get_paginator("list_ca_certificates")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    list_certificates_by_ca_paginator: ListCertificatesByCAPaginator = client.get_paginator("list_certificates_by_ca")
    list_custom_metrics_paginator: ListCustomMetricsPaginator = client.get_paginator("list_custom_metrics")
    list_detect_mitigation_actions_executions_paginator: ListDetectMitigationActionsExecutionsPaginator = client.get_paginator("list_detect_mitigation_actions_executions")
    list_detect_mitigation_actions_tasks_paginator: ListDetectMitigationActionsTasksPaginator = client.get_paginator("list_detect_mitigation_actions_tasks")
    list_dimensions_paginator: ListDimensionsPaginator = client.get_paginator("list_dimensions")
    list_domain_configurations_paginator: ListDomainConfigurationsPaginator = client.get_paginator("list_domain_configurations")
    list_fleet_metrics_paginator: ListFleetMetricsPaginator = client.get_paginator("list_fleet_metrics")
    list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
    list_job_executions_for_job_paginator: ListJobExecutionsForJobPaginator = client.get_paginator("list_job_executions_for_job")
    list_job_executions_for_thing_paginator: ListJobExecutionsForThingPaginator = client.get_paginator("list_job_executions_for_thing")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_metric_values_paginator: ListMetricValuesPaginator = client.get_paginator("list_metric_values")
    list_mitigation_actions_paginator: ListMitigationActionsPaginator = client.get_paginator("list_mitigation_actions")
    list_ota_updates_paginator: ListOTAUpdatesPaginator = client.get_paginator("list_ota_updates")
    list_outgoing_certificates_paginator: ListOutgoingCertificatesPaginator = client.get_paginator("list_outgoing_certificates")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_principals_paginator: ListPolicyPrincipalsPaginator = client.get_paginator("list_policy_principals")
    list_principal_policies_paginator: ListPrincipalPoliciesPaginator = client.get_paginator("list_principal_policies")
    list_principal_things_paginator: ListPrincipalThingsPaginator = client.get_paginator("list_principal_things")
    list_provisioning_template_versions_paginator: ListProvisioningTemplateVersionsPaginator = client.get_paginator("list_provisioning_template_versions")
    list_provisioning_templates_paginator: ListProvisioningTemplatesPaginator = client.get_paginator("list_provisioning_templates")
    list_role_aliases_paginator: ListRoleAliasesPaginator = client.get_paginator("list_role_aliases")
    list_scheduled_audits_paginator: ListScheduledAuditsPaginator = client.get_paginator("list_scheduled_audits")
    list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
    list_security_profiles_for_target_paginator: ListSecurityProfilesForTargetPaginator = client.get_paginator("list_security_profiles_for_target")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
    list_targets_for_security_profile_paginator: ListTargetsForSecurityProfilePaginator = client.get_paginator("list_targets_for_security_profile")
    list_thing_groups_paginator: ListThingGroupsPaginator = client.get_paginator("list_thing_groups")
    list_thing_groups_for_thing_paginator: ListThingGroupsForThingPaginator = client.get_paginator("list_thing_groups_for_thing")
    list_thing_principals_paginator: ListThingPrincipalsPaginator = client.get_paginator("list_thing_principals")
    list_thing_registration_task_reports_paginator: ListThingRegistrationTaskReportsPaginator = client.get_paginator("list_thing_registration_task_reports")
    list_thing_registration_tasks_paginator: ListThingRegistrationTasksPaginator = client.get_paginator("list_thing_registration_tasks")
    list_thing_types_paginator: ListThingTypesPaginator = client.get_paginator("list_thing_types")
    list_things_paginator: ListThingsPaginator = client.get_paginator("list_things")
    list_things_in_billing_group_paginator: ListThingsInBillingGroupPaginator = client.get_paginator("list_things_in_billing_group")
    list_things_in_thing_group_paginator: ListThingsInThingGroupPaginator = client.get_paginator("list_things_in_thing_group")
    list_topic_rule_destinations_paginator: ListTopicRuleDestinationsPaginator = client.get_paginator("list_topic_rule_destinations")
    list_topic_rules_paginator: ListTopicRulesPaginator = client.get_paginator("list_topic_rules")
    list_v2_logging_levels_paginator: ListV2LoggingLevelsPaginator = client.get_paginator("list_v2_logging_levels")
    list_violation_events_paginator: ListViolationEventsPaginator = client.get_paginator("list_violation_events")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    AuditMitigationActionsExecutionStatusType,
    AuditMitigationActionsTaskStatusType,
    AuditTaskStatusType,
    AuditTaskTypeType,
    AuthorizerStatusType,
    BehaviorCriteriaTypeType,
    DimensionValueOperatorType,
    JobExecutionStatusType,
    JobStatusType,
    LogTargetTypeType,
    MitigationActionTypeType,
    OTAUpdateStatusType,
    ReportTypeType,
    ServiceTypeType,
    StatusType,
    TargetSelectionType,
    VerificationStateType,
)
from .type_defs import (
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListMetricValuesResponseTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsResponseTypeDef,
    PaginatorConfigTypeDef,
    ResourceIdentifierTypeDef,
)

__all__ = (
    "GetBehaviorModelTrainingSummariesPaginator",
    "ListActiveViolationsPaginator",
    "ListAttachedPoliciesPaginator",
    "ListAuditFindingsPaginator",
    "ListAuditMitigationActionsExecutionsPaginator",
    "ListAuditMitigationActionsTasksPaginator",
    "ListAuditSuppressionsPaginator",
    "ListAuditTasksPaginator",
    "ListAuthorizersPaginator",
    "ListBillingGroupsPaginator",
    "ListCACertificatesPaginator",
    "ListCertificatesPaginator",
    "ListCertificatesByCAPaginator",
    "ListCustomMetricsPaginator",
    "ListDetectMitigationActionsExecutionsPaginator",
    "ListDetectMitigationActionsTasksPaginator",
    "ListDimensionsPaginator",
    "ListDomainConfigurationsPaginator",
    "ListFleetMetricsPaginator",
    "ListIndicesPaginator",
    "ListJobExecutionsForJobPaginator",
    "ListJobExecutionsForThingPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListMetricValuesPaginator",
    "ListMitigationActionsPaginator",
    "ListOTAUpdatesPaginator",
    "ListOutgoingCertificatesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyPrincipalsPaginator",
    "ListPrincipalPoliciesPaginator",
    "ListPrincipalThingsPaginator",
    "ListProvisioningTemplateVersionsPaginator",
    "ListProvisioningTemplatesPaginator",
    "ListRoleAliasesPaginator",
    "ListScheduledAuditsPaginator",
    "ListSecurityProfilesPaginator",
    "ListSecurityProfilesForTargetPaginator",
    "ListStreamsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
    "ListTargetsForSecurityProfilePaginator",
    "ListThingGroupsPaginator",
    "ListThingGroupsForThingPaginator",
    "ListThingPrincipalsPaginator",
    "ListThingRegistrationTaskReportsPaginator",
    "ListThingRegistrationTasksPaginator",
    "ListThingTypesPaginator",
    "ListThingsPaginator",
    "ListThingsInBillingGroupPaginator",
    "ListThingsInThingGroupPaginator",
    "ListTopicRuleDestinationsPaginator",
    "ListTopicRulesPaginator",
    "ListV2LoggingLevelsPaginator",
    "ListViolationEventsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetBehaviorModelTrainingSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.GetBehaviorModelTrainingSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
    """

    def paginate(
        self, *, securityProfileName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBehaviorModelTrainingSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.GetBehaviorModelTrainingSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
        """


class ListActiveViolationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListActiveViolations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listactiveviolationspaginator)
    """

    def paginate(
        self,
        *,
        thingName: str = ...,
        securityProfileName: str = ...,
        behaviorCriteriaType: BehaviorCriteriaTypeType = ...,
        listSuppressedAlerts: bool = ...,
        verificationState: VerificationStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActiveViolationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListActiveViolations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listactiveviolationspaginator)
        """


class ListAttachedPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAttachedPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listattachedpoliciespaginator)
    """

    def paginate(
        self, *, target: str, recursive: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttachedPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAttachedPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listattachedpoliciespaginator)
        """


class ListAuditFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditfindingspaginator)
    """

    def paginate(
        self,
        *,
        taskId: str = ...,
        checkName: str = ...,
        resourceIdentifier: ResourceIdentifierTypeDef = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        listSuppressedFindings: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditfindingspaginator)
        """


class ListAuditMitigationActionsExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionsexecutionspaginator)
    """

    def paginate(
        self,
        *,
        taskId: str,
        findingId: str,
        actionStatus: AuditMitigationActionsExecutionStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionsexecutionspaginator)
        """


class ListAuditMitigationActionsTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionstaskspaginator)
    """

    def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        auditTaskId: str = ...,
        findingId: str = ...,
        taskStatus: AuditMitigationActionsTaskStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionstaskspaginator)
        """


class ListAuditSuppressionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditSuppressions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditsuppressionspaginator)
    """

    def paginate(
        self,
        *,
        checkName: str = ...,
        resourceIdentifier: ResourceIdentifierTypeDef = ...,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditSuppressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditSuppressions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditsuppressionspaginator)
        """


class ListAuditTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listaudittaskspaginator)
    """

    def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        taskType: AuditTaskTypeType = ...,
        taskStatus: AuditTaskStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listaudittaskspaginator)
        """


class ListAuthorizersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuthorizers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauthorizerspaginator)
    """

    def paginate(
        self,
        *,
        ascendingOrder: bool = ...,
        status: AuthorizerStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuthorizers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauthorizerspaginator)
        """


class ListBillingGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListBillingGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listbillinggroupspaginator)
    """

    def paginate(
        self, *, namePrefixFilter: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBillingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListBillingGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listbillinggroupspaginator)
        """


class ListCACertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCACertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcacertificatespaginator)
    """

    def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCACertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCACertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcacertificatespaginator)
        """


class ListCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatespaginator)
    """

    def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatespaginator)
        """


class ListCertificatesByCAPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificatesByCA)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatesbycapaginator)
    """

    def paginate(
        self,
        *,
        caCertificateId: str,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificatesByCAResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificatesByCA.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatesbycapaginator)
        """


class ListCustomMetricsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCustomMetrics)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcustommetricspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCustomMetrics.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcustommetricspaginator)
        """


class ListDetectMitigationActionsExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
    """

    def paginate(
        self,
        *,
        taskId: str = ...,
        violationId: str = ...,
        thingName: str = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDetectMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
        """


class ListDetectMitigationActionsTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionstaskspaginator)
    """

    def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDetectMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionstaskspaginator)
        """


class ListDimensionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDimensions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdimensionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDimensionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDimensions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdimensionspaginator)
        """


class ListDomainConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDomainConfigurations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdomainconfigurationspaginator)
    """

    def paginate(
        self, *, serviceType: ServiceTypeType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDomainConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDomainConfigurations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdomainconfigurationspaginator)
        """


class ListFleetMetricsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListFleetMetrics)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listfleetmetricspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFleetMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListFleetMetrics.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listfleetmetricspaginator)
        """


class ListIndicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListIndices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listindicespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListIndices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listindicespaginator)
        """


class ListJobExecutionsForJobPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForJob)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforjobpaginator)
    """

    def paginate(
        self,
        *,
        jobId: str,
        status: JobExecutionStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobExecutionsForJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForJob.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforjobpaginator)
        """


class ListJobExecutionsForThingPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForThing)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforthingpaginator)
    """

    def paginate(
        self,
        *,
        thingName: str,
        status: JobExecutionStatusType = ...,
        namespaceId: str = ...,
        jobId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobExecutionsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForThing.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforthingpaginator)
        """


class ListJobTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobtemplatespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobtemplatespaginator)
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobspaginator)
    """

    def paginate(
        self,
        *,
        status: JobStatusType = ...,
        targetSelection: TargetSelectionType = ...,
        thingGroupName: str = ...,
        thingGroupId: str = ...,
        namespaceId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobspaginator)
        """


class ListMetricValuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListMetricValues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmetricvaluespaginator)
    """

    def paginate(
        self,
        *,
        thingName: str,
        metricName: str,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        dimensionName: str = ...,
        dimensionValueOperator: DimensionValueOperatorType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMetricValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListMetricValues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmetricvaluespaginator)
        """


class ListMitigationActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListMitigationActions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmitigationactionspaginator)
    """

    def paginate(
        self,
        *,
        actionType: MitigationActionTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMitigationActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListMitigationActions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmitigationactionspaginator)
        """


class ListOTAUpdatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOTAUpdates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listotaupdatespaginator)
    """

    def paginate(
        self,
        *,
        otaUpdateStatus: OTAUpdateStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOTAUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOTAUpdates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listotaupdatespaginator)
        """


class ListOutgoingCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOutgoingCertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listoutgoingcertificatespaginator)
    """

    def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOutgoingCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOutgoingCertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listoutgoingcertificatespaginator)
        """


class ListPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpoliciespaginator)
    """

    def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpoliciespaginator)
        """


class ListPolicyPrincipalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicyPrincipals)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpolicyprincipalspaginator)
    """

    def paginate(
        self,
        *,
        policyName: str,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPolicyPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicyPrincipals.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpolicyprincipalspaginator)
        """


class ListPrincipalPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalpoliciespaginator)
    """

    def paginate(
        self,
        *,
        principal: str,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPrincipalPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalpoliciespaginator)
        """


class ListPrincipalThingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalThings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalthingspaginator)
    """

    def paginate(
        self, *, principal: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPrincipalThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalThings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalthingspaginator)
        """


class ListProvisioningTemplateVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplateVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplateversionspaginator)
    """

    def paginate(
        self, *, templateName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisioningTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplateVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplateversionspaginator)
        """


class ListProvisioningTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplatespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisioningTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplatespaginator)
        """


class ListRoleAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListRoleAliases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listrolealiasespaginator)
    """

    def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRoleAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListRoleAliases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listrolealiasespaginator)
        """


class ListScheduledAuditsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListScheduledAudits)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listscheduledauditspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListScheduledAuditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListScheduledAudits.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listscheduledauditspaginator)
        """


class ListSecurityProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilespaginator)
    """

    def paginate(
        self,
        *,
        dimensionName: str = ...,
        metricName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilespaginator)
        """


class ListSecurityProfilesForTargetPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfilesForTarget)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilesfortargetpaginator)
    """

    def paginate(
        self,
        *,
        securityProfileTargetArn: str,
        recursive: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityProfilesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfilesForTarget.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilesfortargetpaginator)
        """


class ListStreamsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListStreams)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#liststreamspaginator)
    """

    def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListStreams.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#liststreamspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtagsforresourcepaginator)
        """


class ListTargetsForPolicyPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForPolicy)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforpolicypaginator)
    """

    def paginate(
        self, *, policyName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForPolicy.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforpolicypaginator)
        """


class ListTargetsForSecurityProfilePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForSecurityProfile)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforsecurityprofilepaginator)
    """

    def paginate(
        self, *, securityProfileName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetsForSecurityProfileResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForSecurityProfile.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforsecurityprofilepaginator)
        """


class ListThingGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupspaginator)
    """

    def paginate(
        self,
        *,
        parentGroup: str = ...,
        namePrefixFilter: str = ...,
        recursive: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupspaginator)
        """


class ListThingGroupsForThingPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroupsForThing)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupsforthingpaginator)
    """

    def paginate(
        self, *, thingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingGroupsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroupsForThing.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupsforthingpaginator)
        """


class ListThingPrincipalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingPrincipals)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingprincipalspaginator)
    """

    def paginate(
        self, *, thingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingPrincipals.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingprincipalspaginator)
        """


class ListThingRegistrationTaskReportsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTaskReports)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskreportspaginator)
    """

    def paginate(
        self,
        *,
        taskId: str,
        reportType: ReportTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingRegistrationTaskReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTaskReports.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskreportspaginator)
        """


class ListThingRegistrationTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskspaginator)
    """

    def paginate(
        self, *, status: StatusType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingRegistrationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskspaginator)
        """


class ListThingTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingTypes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingtypespaginator)
    """

    def paginate(
        self, *, thingTypeName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingTypes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingtypespaginator)
        """


class ListThingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingspaginator)
    """

    def paginate(
        self,
        *,
        attributeName: str = ...,
        attributeValue: str = ...,
        thingTypeName: str = ...,
        usePrefixAttributeValue: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingspaginator)
        """


class ListThingsInBillingGroupPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInBillingGroup)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinbillinggrouppaginator)
    """

    def paginate(
        self, *, billingGroupName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingsInBillingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInBillingGroup.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinbillinggrouppaginator)
        """


class ListThingsInThingGroupPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInThingGroup)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinthinggrouppaginator)
    """

    def paginate(
        self,
        *,
        thingGroupName: str,
        recursive: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingsInThingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInThingGroup.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinthinggrouppaginator)
        """


class ListTopicRuleDestinationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRuleDestinations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicruledestinationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTopicRuleDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRuleDestinations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicruledestinationspaginator)
        """


class ListTopicRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicrulespaginator)
    """

    def paginate(
        self,
        *,
        topic: str = ...,
        ruleDisabled: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTopicRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicrulespaginator)
        """


class ListV2LoggingLevelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListV2LoggingLevels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listv2logginglevelspaginator)
    """

    def paginate(
        self, *, targetType: LogTargetTypeType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListV2LoggingLevelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListV2LoggingLevels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listv2logginglevelspaginator)
        """


class ListViolationEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListViolationEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listviolationeventspaginator)
    """

    def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        thingName: str = ...,
        securityProfileName: str = ...,
        behaviorCriteriaType: BehaviorCriteriaTypeType = ...,
        listSuppressedAlerts: bool = ...,
        verificationState: VerificationStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListViolationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListViolationEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listviolationeventspaginator)
        """
