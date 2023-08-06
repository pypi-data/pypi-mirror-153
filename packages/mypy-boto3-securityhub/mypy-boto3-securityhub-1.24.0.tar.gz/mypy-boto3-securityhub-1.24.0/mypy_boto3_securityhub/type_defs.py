"""
Type annotations for securityhub service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/type_defs/)

Usage::

    ```python
    from mypy_boto3_securityhub.type_defs import AcceptAdministratorInvitationRequestRequestTypeDef

    data: AcceptAdministratorInvitationRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AdminStatusType,
    AutoEnableStandardsType,
    AwsIamAccessKeyStatusType,
    AwsS3BucketNotificationConfigurationS3KeyFilterRuleNameType,
    ComplianceStatusType,
    ControlStatusType,
    IntegrationTypeType,
    MalwareStateType,
    MalwareTypeType,
    MapFilterComparisonType,
    NetworkDirectionType,
    PartitionType,
    RecordStateType,
    SeverityLabelType,
    SeverityRatingType,
    SortOrderType,
    StandardsStatusType,
    StatusReasonCodeType,
    StringFilterComparisonType,
    ThreatIntelIndicatorCategoryType,
    ThreatIntelIndicatorTypeType,
    VerificationStateType,
    WorkflowStateType,
    WorkflowStatusType,
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
    "AcceptAdministratorInvitationRequestRequestTypeDef",
    "AcceptInvitationRequestRequestTypeDef",
    "AccountDetailsTypeDef",
    "ActionLocalIpDetailsTypeDef",
    "ActionLocalPortDetailsTypeDef",
    "CityTypeDef",
    "CountryTypeDef",
    "GeoLocationTypeDef",
    "IpOrganizationDetailsTypeDef",
    "ActionRemotePortDetailsTypeDef",
    "ActionTargetTypeDef",
    "DnsRequestActionTypeDef",
    "AdjustmentTypeDef",
    "AdminAccountTypeDef",
    "AvailabilityZoneTypeDef",
    "AwsApiCallActionDomainDetailsTypeDef",
    "AwsApiGatewayAccessLogSettingsTypeDef",
    "AwsApiGatewayCanarySettingsTypeDef",
    "AwsApiGatewayEndpointConfigurationTypeDef",
    "AwsApiGatewayMethodSettingsTypeDef",
    "AwsCorsConfigurationTypeDef",
    "AwsApiGatewayV2RouteSettingsTypeDef",
    "AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef",
    "AwsCertificateManagerCertificateExtendedKeyUsageTypeDef",
    "AwsCertificateManagerCertificateKeyUsageTypeDef",
    "AwsCertificateManagerCertificateOptionsTypeDef",
    "AwsCertificateManagerCertificateResourceRecordTypeDef",
    "AwsCloudFrontDistributionCacheBehaviorTypeDef",
    "AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef",
    "AwsCloudFrontDistributionLoggingTypeDef",
    "AwsCloudFrontDistributionViewerCertificateTypeDef",
    "AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef",
    "AwsCloudFrontDistributionOriginS3OriginConfigTypeDef",
    "AwsCloudTrailTrailDetailsTypeDef",
    "AwsCodeBuildProjectArtifactsDetailsTypeDef",
    "AwsCodeBuildProjectSourceTypeDef",
    "AwsCodeBuildProjectVpcConfigTypeDef",
    "AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef",
    "AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef",
    "AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef",
    "AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef",
    "AwsDynamoDbTableAttributeDefinitionTypeDef",
    "AwsDynamoDbTableBillingModeSummaryTypeDef",
    "AwsDynamoDbTableKeySchemaTypeDef",
    "AwsDynamoDbTableProvisionedThroughputTypeDef",
    "AwsDynamoDbTableRestoreSummaryTypeDef",
    "AwsDynamoDbTableSseDescriptionTypeDef",
    "AwsDynamoDbTableStreamSpecificationTypeDef",
    "AwsDynamoDbTableProjectionTypeDef",
    "AwsDynamoDbTableProvisionedThroughputOverrideTypeDef",
    "AwsEc2EipDetailsTypeDef",
    "AwsEc2InstanceNetworkInterfacesDetailsTypeDef",
    "AwsEc2NetworkAclAssociationTypeDef",
    "IcmpTypeCodeTypeDef",
    "PortRangeFromToTypeDef",
    "AwsEc2NetworkInterfaceAttachmentTypeDef",
    "AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef",
    "AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef",
    "AwsEc2NetworkInterfaceSecurityGroupTypeDef",
    "AwsEc2SecurityGroupIpRangeTypeDef",
    "AwsEc2SecurityGroupIpv6RangeTypeDef",
    "AwsEc2SecurityGroupPrefixListIdTypeDef",
    "AwsEc2SecurityGroupUserIdGroupPairTypeDef",
    "Ipv6CidrBlockAssociationTypeDef",
    "AwsEc2VolumeAttachmentTypeDef",
    "CidrBlockAssociationTypeDef",
    "AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef",
    "AwsEc2VpnConnectionRoutesDetailsTypeDef",
    "AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef",
    "AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef",
    "AwsEcrRepositoryLifecyclePolicyDetailsTypeDef",
    "AwsEcsClusterClusterSettingsDetailsTypeDef",
    "AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef",
    "AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef",
    "AwsEcsServiceCapacityProviderStrategyDetailsTypeDef",
    "AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef",
    "AwsEcsServiceDeploymentControllerDetailsTypeDef",
    "AwsEcsServiceLoadBalancersDetailsTypeDef",
    "AwsEcsServicePlacementConstraintsDetailsTypeDef",
    "AwsEcsServicePlacementStrategiesDetailsTypeDef",
    "AwsEcsServiceServiceRegistriesDetailsTypeDef",
    "AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef",
    "AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef",
    "AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef",
    "AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesHostDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef",
    "AwsEksClusterResourcesVpcConfigDetailsTypeDef",
    "AwsEksClusterLoggingClusterLoggingDetailsTypeDef",
    "AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef",
    "AwsElasticBeanstalkEnvironmentOptionSettingTypeDef",
    "AwsElasticBeanstalkEnvironmentTierTypeDef",
    "AwsElasticsearchDomainDomainEndpointOptionsTypeDef",
    "AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef",
    "AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef",
    "AwsElasticsearchDomainServiceSoftwareOptionsTypeDef",
    "AwsElasticsearchDomainVPCOptionsTypeDef",
    "AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef",
    "AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef",
    "AwsElbAppCookieStickinessPolicyTypeDef",
    "AwsElbLbCookieStickinessPolicyTypeDef",
    "AwsElbLoadBalancerAccessLogTypeDef",
    "AwsElbLoadBalancerAdditionalAttributeTypeDef",
    "AwsElbLoadBalancerConnectionDrainingTypeDef",
    "AwsElbLoadBalancerConnectionSettingsTypeDef",
    "AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef",
    "AwsElbLoadBalancerBackendServerDescriptionTypeDef",
    "AwsElbLoadBalancerHealthCheckTypeDef",
    "AwsElbLoadBalancerInstanceTypeDef",
    "AwsElbLoadBalancerSourceSecurityGroupTypeDef",
    "AwsElbLoadBalancerListenerTypeDef",
    "AwsElbv2LoadBalancerAttributeTypeDef",
    "LoadBalancerStateTypeDef",
    "AwsIamAccessKeySessionContextAttributesTypeDef",
    "AwsIamAccessKeySessionContextSessionIssuerTypeDef",
    "AwsIamAttachedManagedPolicyTypeDef",
    "AwsIamGroupPolicyTypeDef",
    "AwsIamInstanceProfileRoleTypeDef",
    "AwsIamPermissionsBoundaryTypeDef",
    "AwsIamPolicyVersionTypeDef",
    "AwsIamRolePolicyTypeDef",
    "AwsIamUserPolicyTypeDef",
    "AwsKmsKeyDetailsTypeDef",
    "AwsLambdaFunctionCodeTypeDef",
    "AwsLambdaFunctionDeadLetterConfigTypeDef",
    "AwsLambdaFunctionLayerTypeDef",
    "AwsLambdaFunctionTracingConfigTypeDef",
    "AwsLambdaFunctionVpcConfigTypeDef",
    "AwsLambdaFunctionEnvironmentErrorTypeDef",
    "AwsLambdaLayerVersionDetailsTypeDef",
    "AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef",
    "AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef",
    "AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainLogPublishingOptionTypeDef",
    "AwsRdsDbClusterAssociatedRoleTypeDef",
    "AwsRdsDbClusterMemberTypeDef",
    "AwsRdsDbClusterOptionGroupMembershipTypeDef",
    "AwsRdsDbDomainMembershipTypeDef",
    "AwsRdsDbInstanceVpcSecurityGroupTypeDef",
    "AwsRdsDbClusterSnapshotDetailsTypeDef",
    "AwsRdsDbInstanceAssociatedRoleTypeDef",
    "AwsRdsDbInstanceEndpointTypeDef",
    "AwsRdsDbOptionGroupMembershipTypeDef",
    "AwsRdsDbParameterGroupTypeDef",
    "AwsRdsDbProcessorFeatureTypeDef",
    "AwsRdsDbStatusInfoTypeDef",
    "AwsRdsPendingCloudWatchLogsExportsTypeDef",
    "AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef",
    "AwsRdsDbSecurityGroupIpRangeTypeDef",
    "AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef",
    "AwsRdsEventSubscriptionDetailsTypeDef",
    "AwsRedshiftClusterClusterNodeTypeDef",
    "AwsRedshiftClusterClusterParameterStatusTypeDef",
    "AwsRedshiftClusterClusterSecurityGroupTypeDef",
    "AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef",
    "AwsRedshiftClusterDeferredMaintenanceWindowTypeDef",
    "AwsRedshiftClusterElasticIpStatusTypeDef",
    "AwsRedshiftClusterEndpointTypeDef",
    "AwsRedshiftClusterHsmStatusTypeDef",
    "AwsRedshiftClusterIamRoleTypeDef",
    "AwsRedshiftClusterLoggingStatusTypeDef",
    "AwsRedshiftClusterPendingModifiedValuesTypeDef",
    "AwsRedshiftClusterResizeInfoTypeDef",
    "AwsRedshiftClusterRestoreStatusTypeDef",
    "AwsRedshiftClusterVpcSecurityGroupTypeDef",
    "AwsS3AccountPublicAccessBlockDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef",
    "AwsS3BucketBucketVersioningConfigurationTypeDef",
    "AwsS3BucketLoggingConfigurationTypeDef",
    "AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef",
    "AwsS3BucketServerSideEncryptionByDefaultTypeDef",
    "AwsS3BucketWebsiteConfigurationRedirectToTypeDef",
    "AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef",
    "AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef",
    "AwsS3ObjectDetailsTypeDef",
    "AwsSecretsManagerSecretRotationRulesTypeDef",
    "BooleanFilterTypeDef",
    "IpFilterTypeDef",
    "KeywordFilterTypeDef",
    "MapFilterTypeDef",
    "NumberFilterTypeDef",
    "StringFilterTypeDef",
    "AwsSecurityFindingIdentifierTypeDef",
    "MalwareTypeDef",
    "NoteTypeDef",
    "PatchSummaryTypeDef",
    "ProcessDetailsTypeDef",
    "RelatedFindingTypeDef",
    "SeverityTypeDef",
    "ThreatIntelIndicatorTypeDef",
    "WorkflowTypeDef",
    "AwsSnsTopicSubscriptionTypeDef",
    "AwsSqsQueueDetailsTypeDef",
    "AwsSsmComplianceSummaryTypeDef",
    "AwsWafRateBasedRuleMatchPredicateTypeDef",
    "AwsWafRegionalRateBasedRuleMatchPredicateTypeDef",
    "WafActionTypeDef",
    "WafExcludedRuleTypeDef",
    "WafOverrideActionTypeDef",
    "AwsXrayEncryptionConfigDetailsTypeDef",
    "BatchDisableStandardsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StandardsSubscriptionRequestTypeDef",
    "ImportFindingsErrorTypeDef",
    "NoteUpdateTypeDef",
    "SeverityUpdateTypeDef",
    "WorkflowUpdateTypeDef",
    "CellTypeDef",
    "ClassificationStatusTypeDef",
    "StatusReasonTypeDef",
    "ContainerDetailsTypeDef",
    "CreateActionTargetRequestRequestTypeDef",
    "CreateFindingAggregatorRequestRequestTypeDef",
    "ResultTypeDef",
    "DateRangeTypeDef",
    "DeclineInvitationsRequestRequestTypeDef",
    "DeleteActionTargetRequestRequestTypeDef",
    "DeleteFindingAggregatorRequestRequestTypeDef",
    "DeleteInsightRequestRequestTypeDef",
    "DeleteInvitationsRequestRequestTypeDef",
    "DeleteMembersRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeActionTargetsRequestRequestTypeDef",
    "DescribeHubRequestRequestTypeDef",
    "DescribeProductsRequestRequestTypeDef",
    "ProductTypeDef",
    "DescribeStandardsControlsRequestRequestTypeDef",
    "StandardsControlTypeDef",
    "DescribeStandardsRequestRequestTypeDef",
    "StandardTypeDef",
    "DisableImportFindingsForProductRequestRequestTypeDef",
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    "DisassociateMembersRequestRequestTypeDef",
    "EnableImportFindingsForProductRequestRequestTypeDef",
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    "EnableSecurityHubRequestRequestTypeDef",
    "FindingAggregatorTypeDef",
    "FindingProviderSeverityTypeDef",
    "FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef",
    "FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef",
    "InvitationTypeDef",
    "GetEnabledStandardsRequestRequestTypeDef",
    "GetFindingAggregatorRequestRequestTypeDef",
    "SortCriterionTypeDef",
    "GetInsightResultsRequestRequestTypeDef",
    "GetInsightsRequestRequestTypeDef",
    "GetMembersRequestRequestTypeDef",
    "MemberTypeDef",
    "InsightResultValueTypeDef",
    "InviteMembersRequestRequestTypeDef",
    "ListEnabledProductsForImportRequestRequestTypeDef",
    "ListFindingAggregatorsRequestRequestTypeDef",
    "ListInvitationsRequestRequestTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PortRangeTypeDef",
    "RangeTypeDef",
    "RecordTypeDef",
    "RecommendationTypeDef",
    "RuleGroupSourceListDetailsTypeDef",
    "RuleGroupSourceStatefulRulesHeaderDetailsTypeDef",
    "RuleGroupSourceStatefulRulesOptionsDetailsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef",
    "RuleGroupVariablesIpSetsDetailsTypeDef",
    "RuleGroupVariablesPortSetsDetailsTypeDef",
    "SoftwarePackageTypeDef",
    "StandardsStatusReasonTypeDef",
    "StatelessCustomPublishMetricActionDimensionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateActionTargetRequestRequestTypeDef",
    "UpdateFindingAggregatorRequestRequestTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateSecurityHubConfigurationRequestRequestTypeDef",
    "UpdateStandardsControlRequestRequestTypeDef",
    "VulnerabilityVendorTypeDef",
    "CreateMembersRequestRequestTypeDef",
    "ActionRemoteIpDetailsTypeDef",
    "CvssTypeDef",
    "AwsApiGatewayRestApiDetailsTypeDef",
    "AwsApiGatewayStageDetailsTypeDef",
    "AwsApiGatewayV2ApiDetailsTypeDef",
    "AwsApiGatewayV2StageDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef",
    "AwsCertificateManagerCertificateDomainValidationOptionTypeDef",
    "AwsCloudFrontDistributionCacheBehaviorsTypeDef",
    "AwsCloudFrontDistributionOriginGroupFailoverTypeDef",
    "AwsCloudFrontDistributionOriginItemTypeDef",
    "AwsCodeBuildProjectEnvironmentTypeDef",
    "AwsCodeBuildProjectLogsConfigDetailsTypeDef",
    "AwsDynamoDbTableGlobalSecondaryIndexTypeDef",
    "AwsDynamoDbTableLocalSecondaryIndexTypeDef",
    "AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEc2NetworkAclEntryTypeDef",
    "AwsEc2NetworkInterfaceDetailsTypeDef",
    "AwsEc2SecurityGroupIpPermissionTypeDef",
    "AwsEc2SubnetDetailsTypeDef",
    "AwsEc2VolumeDetailsTypeDef",
    "AwsEc2VpcDetailsTypeDef",
    "AwsEc2VpcEndpointServiceDetailsTypeDef",
    "AwsEc2VpnConnectionOptionsDetailsTypeDef",
    "AwsEcrRepositoryDetailsTypeDef",
    "AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef",
    "AwsEcsServiceDeploymentConfigurationDetailsTypeDef",
    "AwsEcsServiceNetworkConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef",
    "AwsEksClusterLoggingDetailsTypeDef",
    "AwsElasticBeanstalkEnvironmentDetailsTypeDef",
    "AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef",
    "AwsElasticsearchDomainLogPublishingOptionsTypeDef",
    "AwsElbLoadBalancerPoliciesTypeDef",
    "AwsElbLoadBalancerAttributesTypeDef",
    "AwsElbLoadBalancerListenerDescriptionTypeDef",
    "AwsElbv2LoadBalancerDetailsTypeDef",
    "AwsIamAccessKeySessionContextTypeDef",
    "AwsIamGroupDetailsTypeDef",
    "AwsIamInstanceProfileTypeDef",
    "AwsIamPolicyDetailsTypeDef",
    "AwsIamUserDetailsTypeDef",
    "AwsLambdaFunctionEnvironmentTypeDef",
    "AwsNetworkFirewallFirewallDetailsTypeDef",
    "AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef",
    "AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef",
    "AwsRdsDbClusterDetailsTypeDef",
    "AwsRdsDbSnapshotDetailsTypeDef",
    "AwsRdsDbPendingModifiedValuesTypeDef",
    "AwsRdsDbSecurityGroupDetailsTypeDef",
    "AwsRdsDbSubnetGroupSubnetTypeDef",
    "AwsRedshiftClusterClusterParameterGroupTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef",
    "AwsS3BucketServerSideEncryptionRuleTypeDef",
    "AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef",
    "AwsSecretsManagerSecretDetailsTypeDef",
    "BatchUpdateFindingsUnprocessedFindingTypeDef",
    "AwsSnsTopicDetailsTypeDef",
    "AwsSsmPatchTypeDef",
    "AwsWafRateBasedRuleDetailsTypeDef",
    "AwsWafRegionalRateBasedRuleDetailsTypeDef",
    "AwsWafWebAclRuleTypeDef",
    "CreateActionTargetResponseTypeDef",
    "CreateFindingAggregatorResponseTypeDef",
    "CreateInsightResponseTypeDef",
    "DeleteActionTargetResponseTypeDef",
    "DeleteInsightResponseTypeDef",
    "DescribeActionTargetsResponseTypeDef",
    "DescribeHubResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "EnableImportFindingsForProductResponseTypeDef",
    "GetFindingAggregatorResponseTypeDef",
    "GetInvitationsCountResponseTypeDef",
    "ListEnabledProductsForImportResponseTypeDef",
    "ListOrganizationAdminAccountsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateFindingAggregatorResponseTypeDef",
    "BatchEnableStandardsRequestRequestTypeDef",
    "BatchImportFindingsResponseTypeDef",
    "BatchUpdateFindingsRequestRequestTypeDef",
    "ComplianceTypeDef",
    "CreateMembersResponseTypeDef",
    "DeclineInvitationsResponseTypeDef",
    "DeleteInvitationsResponseTypeDef",
    "DeleteMembersResponseTypeDef",
    "InviteMembersResponseTypeDef",
    "DateFilterTypeDef",
    "DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef",
    "DescribeProductsRequestDescribeProductsPaginateTypeDef",
    "DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef",
    "DescribeStandardsRequestDescribeStandardsPaginateTypeDef",
    "GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef",
    "GetInsightsRequestGetInsightsPaginateTypeDef",
    "ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef",
    "ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef",
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    "DescribeProductsResponseTypeDef",
    "DescribeStandardsControlsResponseTypeDef",
    "DescribeStandardsResponseTypeDef",
    "ListFindingAggregatorsResponseTypeDef",
    "FindingProviderFieldsTypeDef",
    "GetAdministratorAccountResponseTypeDef",
    "GetMasterAccountResponseTypeDef",
    "ListInvitationsResponseTypeDef",
    "GetMembersResponseTypeDef",
    "ListMembersResponseTypeDef",
    "InsightResultsTypeDef",
    "NetworkPathComponentDetailsTypeDef",
    "NetworkTypeDef",
    "PageTypeDef",
    "RemediationTypeDef",
    "RuleGroupSourceStatefulRulesDetailsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesTypeDef",
    "RuleGroupVariablesTypeDef",
    "StandardsSubscriptionTypeDef",
    "StatelessCustomPublishMetricActionTypeDef",
    "AwsApiCallActionTypeDef",
    "NetworkConnectionActionTypeDef",
    "PortProbeDetailTypeDef",
    "VulnerabilityTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationDetailsTypeDef",
    "AwsCertificateManagerCertificateRenewalSummaryTypeDef",
    "AwsCloudFrontDistributionOriginGroupTypeDef",
    "AwsCloudFrontDistributionOriginsTypeDef",
    "AwsCodeBuildProjectDetailsTypeDef",
    "AwsDynamoDbTableReplicaTypeDef",
    "AwsEc2NetworkAclDetailsTypeDef",
    "AwsEc2SecurityGroupDetailsTypeDef",
    "AwsEc2VpnConnectionDetailsTypeDef",
    "AwsEcsClusterConfigurationDetailsTypeDef",
    "AwsEcsServiceDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesDetailsTypeDef",
    "AwsEksClusterDetailsTypeDef",
    "AwsElasticsearchDomainDetailsTypeDef",
    "AwsElbLoadBalancerDetailsTypeDef",
    "AwsIamAccessKeyDetailsTypeDef",
    "AwsIamRoleDetailsTypeDef",
    "AwsLambdaFunctionDetailsTypeDef",
    "AwsOpenSearchServiceDomainDetailsTypeDef",
    "AwsRdsDbSubnetGroupTypeDef",
    "AwsRedshiftClusterDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationFilterTypeDef",
    "AwsS3BucketServerSideEncryptionConfigurationTypeDef",
    "AwsS3BucketWebsiteConfigurationTypeDef",
    "BatchUpdateFindingsResponseTypeDef",
    "AwsSsmPatchComplianceDetailsTypeDef",
    "AwsWafWebAclDetailsTypeDef",
    "AwsSecurityFindingFiltersTypeDef",
    "GetInsightResultsResponseTypeDef",
    "NetworkHeaderTypeDef",
    "OccurrencesTypeDef",
    "RuleGroupSourceStatelessRuleDefinitionTypeDef",
    "BatchDisableStandardsResponseTypeDef",
    "BatchEnableStandardsResponseTypeDef",
    "GetEnabledStandardsResponseTypeDef",
    "StatelessCustomActionDefinitionTypeDef",
    "PortProbeActionTypeDef",
    "AwsAutoScalingAutoScalingGroupDetailsTypeDef",
    "AwsCertificateManagerCertificateDetailsTypeDef",
    "AwsCloudFrontDistributionOriginGroupsTypeDef",
    "AwsDynamoDbTableDetailsTypeDef",
    "AwsEcsClusterDetailsTypeDef",
    "AwsEcsTaskDefinitionDetailsTypeDef",
    "AwsRdsDbInstanceDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationDetailTypeDef",
    "CreateInsightRequestRequestTypeDef",
    "GetFindingsRequestGetFindingsPaginateTypeDef",
    "GetFindingsRequestRequestTypeDef",
    "InsightTypeDef",
    "UpdateFindingsRequestRequestTypeDef",
    "UpdateInsightRequestRequestTypeDef",
    "NetworkPathComponentTypeDef",
    "CustomDataIdentifiersDetectionsTypeDef",
    "SensitiveDataDetectionsTypeDef",
    "RuleGroupSourceStatelessRulesDetailsTypeDef",
    "FirewallPolicyStatelessCustomActionsDetailsTypeDef",
    "RuleGroupSourceCustomActionsDetailsTypeDef",
    "ActionTypeDef",
    "AwsCloudFrontDistributionDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationTypeDef",
    "GetInsightsResponseTypeDef",
    "CustomDataIdentifiersResultTypeDef",
    "SensitiveDataResultTypeDef",
    "FirewallPolicyDetailsTypeDef",
    "RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef",
    "ClassificationResultTypeDef",
    "AwsNetworkFirewallFirewallPolicyDetailsTypeDef",
    "RuleGroupSourceTypeDef",
    "AwsS3BucketDetailsTypeDef",
    "DataClassificationDetailsTypeDef",
    "RuleGroupDetailsTypeDef",
    "AwsNetworkFirewallRuleGroupDetailsTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceTypeDef",
    "AwsSecurityFindingTypeDef",
    "BatchImportFindingsRequestRequestTypeDef",
    "GetFindingsResponseTypeDef",
)

AcceptAdministratorInvitationRequestRequestTypeDef = TypedDict(
    "AcceptAdministratorInvitationRequestRequestTypeDef",
    {
        "AdministratorId": str,
        "InvitationId": str,
    },
)

AcceptInvitationRequestRequestTypeDef = TypedDict(
    "AcceptInvitationRequestRequestTypeDef",
    {
        "MasterId": str,
        "InvitationId": str,
    },
)

_RequiredAccountDetailsTypeDef = TypedDict(
    "_RequiredAccountDetailsTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalAccountDetailsTypeDef = TypedDict(
    "_OptionalAccountDetailsTypeDef",
    {
        "Email": str,
    },
    total=False,
)


class AccountDetailsTypeDef(_RequiredAccountDetailsTypeDef, _OptionalAccountDetailsTypeDef):
    pass


ActionLocalIpDetailsTypeDef = TypedDict(
    "ActionLocalIpDetailsTypeDef",
    {
        "IpAddressV4": str,
    },
    total=False,
)

ActionLocalPortDetailsTypeDef = TypedDict(
    "ActionLocalPortDetailsTypeDef",
    {
        "Port": int,
        "PortName": str,
    },
    total=False,
)

CityTypeDef = TypedDict(
    "CityTypeDef",
    {
        "CityName": str,
    },
    total=False,
)

CountryTypeDef = TypedDict(
    "CountryTypeDef",
    {
        "CountryCode": str,
        "CountryName": str,
    },
    total=False,
)

GeoLocationTypeDef = TypedDict(
    "GeoLocationTypeDef",
    {
        "Lon": float,
        "Lat": float,
    },
    total=False,
)

IpOrganizationDetailsTypeDef = TypedDict(
    "IpOrganizationDetailsTypeDef",
    {
        "Asn": int,
        "AsnOrg": str,
        "Isp": str,
        "Org": str,
    },
    total=False,
)

ActionRemotePortDetailsTypeDef = TypedDict(
    "ActionRemotePortDetailsTypeDef",
    {
        "Port": int,
        "PortName": str,
    },
    total=False,
)

ActionTargetTypeDef = TypedDict(
    "ActionTargetTypeDef",
    {
        "ActionTargetArn": str,
        "Name": str,
        "Description": str,
    },
)

DnsRequestActionTypeDef = TypedDict(
    "DnsRequestActionTypeDef",
    {
        "Domain": str,
        "Protocol": str,
        "Blocked": bool,
    },
    total=False,
)

AdjustmentTypeDef = TypedDict(
    "AdjustmentTypeDef",
    {
        "Metric": str,
        "Reason": str,
    },
    total=False,
)

AdminAccountTypeDef = TypedDict(
    "AdminAccountTypeDef",
    {
        "AccountId": str,
        "Status": AdminStatusType,
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "ZoneName": str,
        "SubnetId": str,
    },
    total=False,
)

AwsApiCallActionDomainDetailsTypeDef = TypedDict(
    "AwsApiCallActionDomainDetailsTypeDef",
    {
        "Domain": str,
    },
    total=False,
)

AwsApiGatewayAccessLogSettingsTypeDef = TypedDict(
    "AwsApiGatewayAccessLogSettingsTypeDef",
    {
        "Format": str,
        "DestinationArn": str,
    },
    total=False,
)

AwsApiGatewayCanarySettingsTypeDef = TypedDict(
    "AwsApiGatewayCanarySettingsTypeDef",
    {
        "PercentTraffic": float,
        "DeploymentId": str,
        "StageVariableOverrides": Mapping[str, str],
        "UseStageCache": bool,
    },
    total=False,
)

AwsApiGatewayEndpointConfigurationTypeDef = TypedDict(
    "AwsApiGatewayEndpointConfigurationTypeDef",
    {
        "Types": Sequence[str],
    },
    total=False,
)

AwsApiGatewayMethodSettingsTypeDef = TypedDict(
    "AwsApiGatewayMethodSettingsTypeDef",
    {
        "MetricsEnabled": bool,
        "LoggingLevel": str,
        "DataTraceEnabled": bool,
        "ThrottlingBurstLimit": int,
        "ThrottlingRateLimit": float,
        "CachingEnabled": bool,
        "CacheTtlInSeconds": int,
        "CacheDataEncrypted": bool,
        "RequireAuthorizationForCacheControl": bool,
        "UnauthorizedCacheControlHeaderStrategy": str,
        "HttpMethod": str,
        "ResourcePath": str,
    },
    total=False,
)

AwsCorsConfigurationTypeDef = TypedDict(
    "AwsCorsConfigurationTypeDef",
    {
        "AllowOrigins": Sequence[str],
        "AllowCredentials": bool,
        "ExposeHeaders": Sequence[str],
        "MaxAge": int,
        "AllowMethods": Sequence[str],
        "AllowHeaders": Sequence[str],
    },
    total=False,
)

AwsApiGatewayV2RouteSettingsTypeDef = TypedDict(
    "AwsApiGatewayV2RouteSettingsTypeDef",
    {
        "DetailedMetricsEnabled": bool,
        "LoggingLevel": str,
        "DataTraceEnabled": bool,
        "ThrottlingBurstLimit": int,
        "ThrottlingRateLimit": float,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef",
    {
        "Value": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef",
    {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "Version": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef",
    {
        "OnDemandAllocationStrategy": str,
        "OnDemandBaseCapacity": int,
        "OnDemandPercentageAboveBaseCapacity": int,
        "SpotAllocationStrategy": str,
        "SpotInstancePools": int,
        "SpotMaxPrice": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef",
    {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "Version": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef",
    {
        "InstanceType": str,
        "WeightedCapacity": str,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef",
    {
        "DeleteOnTermination": bool,
        "Encrypted": bool,
        "Iops": int,
        "SnapshotId": str,
        "VolumeSize": int,
        "VolumeType": str,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef",
    {
        "HttpEndpoint": str,
        "HttpPutResponseHopLimit": int,
        "HttpTokens": str,
    },
    total=False,
)

AwsCertificateManagerCertificateExtendedKeyUsageTypeDef = TypedDict(
    "AwsCertificateManagerCertificateExtendedKeyUsageTypeDef",
    {
        "Name": str,
        "OId": str,
    },
    total=False,
)

AwsCertificateManagerCertificateKeyUsageTypeDef = TypedDict(
    "AwsCertificateManagerCertificateKeyUsageTypeDef",
    {
        "Name": str,
    },
    total=False,
)

AwsCertificateManagerCertificateOptionsTypeDef = TypedDict(
    "AwsCertificateManagerCertificateOptionsTypeDef",
    {
        "CertificateTransparencyLoggingPreference": str,
    },
    total=False,
)

AwsCertificateManagerCertificateResourceRecordTypeDef = TypedDict(
    "AwsCertificateManagerCertificateResourceRecordTypeDef",
    {
        "Name": str,
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsCloudFrontDistributionCacheBehaviorTypeDef = TypedDict(
    "AwsCloudFrontDistributionCacheBehaviorTypeDef",
    {
        "ViewerProtocolPolicy": str,
    },
    total=False,
)

AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef = TypedDict(
    "AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef",
    {
        "ViewerProtocolPolicy": str,
    },
    total=False,
)

AwsCloudFrontDistributionLoggingTypeDef = TypedDict(
    "AwsCloudFrontDistributionLoggingTypeDef",
    {
        "Bucket": str,
        "Enabled": bool,
        "IncludeCookies": bool,
        "Prefix": str,
    },
    total=False,
)

AwsCloudFrontDistributionViewerCertificateTypeDef = TypedDict(
    "AwsCloudFrontDistributionViewerCertificateTypeDef",
    {
        "AcmCertificateArn": str,
        "Certificate": str,
        "CertificateSource": str,
        "CloudFrontDefaultCertificate": bool,
        "IamCertificateId": str,
        "MinimumProtocolVersion": str,
        "SslSupportMethod": str,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef",
    {
        "Items": Sequence[int],
        "Quantity": int,
    },
    total=False,
)

AwsCloudFrontDistributionOriginS3OriginConfigTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginS3OriginConfigTypeDef",
    {
        "OriginAccessIdentity": str,
    },
    total=False,
)

AwsCloudTrailTrailDetailsTypeDef = TypedDict(
    "AwsCloudTrailTrailDetailsTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "HasCustomEventSelectors": bool,
        "HomeRegion": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "IsOrganizationTrail": bool,
        "KmsKeyId": str,
        "LogFileValidationEnabled": bool,
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicArn": str,
        "SnsTopicName": str,
        "TrailArn": str,
    },
    total=False,
)

AwsCodeBuildProjectArtifactsDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectArtifactsDetailsTypeDef",
    {
        "ArtifactIdentifier": str,
        "EncryptionDisabled": bool,
        "Location": str,
        "Name": str,
        "NamespaceType": str,
        "OverrideArtifactName": bool,
        "Packaging": str,
        "Path": str,
        "Type": str,
    },
    total=False,
)

AwsCodeBuildProjectSourceTypeDef = TypedDict(
    "AwsCodeBuildProjectSourceTypeDef",
    {
        "Type": str,
        "Location": str,
        "GitCloneDepth": int,
        "InsecureSsl": bool,
    },
    total=False,
)

AwsCodeBuildProjectVpcConfigTypeDef = TypedDict(
    "AwsCodeBuildProjectVpcConfigTypeDef",
    {
        "VpcId": str,
        "Subnets": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef",
    {
        "Name": str,
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef",
    {
        "Credential": str,
        "CredentialProvider": str,
    },
    total=False,
)

AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef",
    {
        "GroupName": str,
        "Status": str,
        "StreamName": str,
    },
    total=False,
)

AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef",
    {
        "EncryptionDisabled": bool,
        "Location": str,
        "Status": str,
    },
    total=False,
)

AwsDynamoDbTableAttributeDefinitionTypeDef = TypedDict(
    "AwsDynamoDbTableAttributeDefinitionTypeDef",
    {
        "AttributeName": str,
        "AttributeType": str,
    },
    total=False,
)

AwsDynamoDbTableBillingModeSummaryTypeDef = TypedDict(
    "AwsDynamoDbTableBillingModeSummaryTypeDef",
    {
        "BillingMode": str,
        "LastUpdateToPayPerRequestDateTime": str,
    },
    total=False,
)

AwsDynamoDbTableKeySchemaTypeDef = TypedDict(
    "AwsDynamoDbTableKeySchemaTypeDef",
    {
        "AttributeName": str,
        "KeyType": str,
    },
    total=False,
)

AwsDynamoDbTableProvisionedThroughputTypeDef = TypedDict(
    "AwsDynamoDbTableProvisionedThroughputTypeDef",
    {
        "LastDecreaseDateTime": str,
        "LastIncreaseDateTime": str,
        "NumberOfDecreasesToday": int,
        "ReadCapacityUnits": int,
        "WriteCapacityUnits": int,
    },
    total=False,
)

AwsDynamoDbTableRestoreSummaryTypeDef = TypedDict(
    "AwsDynamoDbTableRestoreSummaryTypeDef",
    {
        "SourceBackupArn": str,
        "SourceTableArn": str,
        "RestoreDateTime": str,
        "RestoreInProgress": bool,
    },
    total=False,
)

AwsDynamoDbTableSseDescriptionTypeDef = TypedDict(
    "AwsDynamoDbTableSseDescriptionTypeDef",
    {
        "InaccessibleEncryptionDateTime": str,
        "Status": str,
        "SseType": str,
        "KmsMasterKeyArn": str,
    },
    total=False,
)

AwsDynamoDbTableStreamSpecificationTypeDef = TypedDict(
    "AwsDynamoDbTableStreamSpecificationTypeDef",
    {
        "StreamEnabled": bool,
        "StreamViewType": str,
    },
    total=False,
)

AwsDynamoDbTableProjectionTypeDef = TypedDict(
    "AwsDynamoDbTableProjectionTypeDef",
    {
        "NonKeyAttributes": Sequence[str],
        "ProjectionType": str,
    },
    total=False,
)

AwsDynamoDbTableProvisionedThroughputOverrideTypeDef = TypedDict(
    "AwsDynamoDbTableProvisionedThroughputOverrideTypeDef",
    {
        "ReadCapacityUnits": int,
    },
    total=False,
)

AwsEc2EipDetailsTypeDef = TypedDict(
    "AwsEc2EipDetailsTypeDef",
    {
        "InstanceId": str,
        "PublicIp": str,
        "AllocationId": str,
        "AssociationId": str,
        "Domain": str,
        "PublicIpv4Pool": str,
        "NetworkBorderGroup": str,
        "NetworkInterfaceId": str,
        "NetworkInterfaceOwnerId": str,
        "PrivateIpAddress": str,
    },
    total=False,
)

AwsEc2InstanceNetworkInterfacesDetailsTypeDef = TypedDict(
    "AwsEc2InstanceNetworkInterfacesDetailsTypeDef",
    {
        "NetworkInterfaceId": str,
    },
    total=False,
)

AwsEc2NetworkAclAssociationTypeDef = TypedDict(
    "AwsEc2NetworkAclAssociationTypeDef",
    {
        "NetworkAclAssociationId": str,
        "NetworkAclId": str,
        "SubnetId": str,
    },
    total=False,
)

IcmpTypeCodeTypeDef = TypedDict(
    "IcmpTypeCodeTypeDef",
    {
        "Code": int,
        "Type": int,
    },
    total=False,
)

PortRangeFromToTypeDef = TypedDict(
    "PortRangeFromToTypeDef",
    {
        "From": int,
        "To": int,
    },
    total=False,
)

AwsEc2NetworkInterfaceAttachmentTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceAttachmentTypeDef",
    {
        "AttachTime": str,
        "AttachmentId": str,
        "DeleteOnTermination": bool,
        "DeviceIndex": int,
        "InstanceId": str,
        "InstanceOwnerId": str,
        "Status": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef",
    {
        "IpV6Address": str,
    },
    total=False,
)

AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef = TypedDict(
    "AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef",
    {
        "PrivateIpAddress": str,
        "PrivateDnsName": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceSecurityGroupTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceSecurityGroupTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpRangeTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpRangeTypeDef",
    {
        "CidrIp": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpv6RangeTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpv6RangeTypeDef",
    {
        "CidrIpv6": str,
    },
    total=False,
)

AwsEc2SecurityGroupPrefixListIdTypeDef = TypedDict(
    "AwsEc2SecurityGroupPrefixListIdTypeDef",
    {
        "PrefixListId": str,
    },
    total=False,
)

AwsEc2SecurityGroupUserIdGroupPairTypeDef = TypedDict(
    "AwsEc2SecurityGroupUserIdGroupPairTypeDef",
    {
        "GroupId": str,
        "GroupName": str,
        "PeeringStatus": str,
        "UserId": str,
        "VpcId": str,
        "VpcPeeringConnectionId": str,
    },
    total=False,
)

Ipv6CidrBlockAssociationTypeDef = TypedDict(
    "Ipv6CidrBlockAssociationTypeDef",
    {
        "AssociationId": str,
        "Ipv6CidrBlock": str,
        "CidrBlockState": str,
    },
    total=False,
)

AwsEc2VolumeAttachmentTypeDef = TypedDict(
    "AwsEc2VolumeAttachmentTypeDef",
    {
        "AttachTime": str,
        "DeleteOnTermination": bool,
        "InstanceId": str,
        "Status": str,
    },
    total=False,
)

CidrBlockAssociationTypeDef = TypedDict(
    "CidrBlockAssociationTypeDef",
    {
        "AssociationId": str,
        "CidrBlock": str,
        "CidrBlockState": str,
    },
    total=False,
)

AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef = TypedDict(
    "AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef",
    {
        "ServiceType": str,
    },
    total=False,
)

AwsEc2VpnConnectionRoutesDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionRoutesDetailsTypeDef",
    {
        "DestinationCidrBlock": str,
        "State": str,
    },
    total=False,
)

AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef",
    {
        "AcceptedRouteCount": int,
        "CertificateArn": str,
        "LastStatusChange": str,
        "OutsideIpAddress": str,
        "Status": str,
        "StatusMessage": str,
    },
    total=False,
)

AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef",
    {
        "DpdTimeoutSeconds": int,
        "IkeVersions": Sequence[str],
        "OutsideIpAddress": str,
        "Phase1DhGroupNumbers": Sequence[int],
        "Phase1EncryptionAlgorithms": Sequence[str],
        "Phase1IntegrityAlgorithms": Sequence[str],
        "Phase1LifetimeSeconds": int,
        "Phase2DhGroupNumbers": Sequence[int],
        "Phase2EncryptionAlgorithms": Sequence[str],
        "Phase2IntegrityAlgorithms": Sequence[str],
        "Phase2LifetimeSeconds": int,
        "PreSharedKey": str,
        "RekeyFuzzPercentage": int,
        "RekeyMarginTimeSeconds": int,
        "ReplayWindowSize": int,
        "TunnelInsideCidr": str,
    },
    total=False,
)

AwsEcrContainerImageDetailsTypeDef = TypedDict(
    "AwsEcrContainerImageDetailsTypeDef",
    {
        "RegistryId": str,
        "RepositoryName": str,
        "Architecture": str,
        "ImageDigest": str,
        "ImageTags": Sequence[str],
        "ImagePublishedAt": str,
    },
    total=False,
)

AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef = TypedDict(
    "AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef",
    {
        "ScanOnPush": bool,
    },
    total=False,
)

AwsEcrRepositoryLifecyclePolicyDetailsTypeDef = TypedDict(
    "AwsEcrRepositoryLifecyclePolicyDetailsTypeDef",
    {
        "LifecyclePolicyText": str,
        "RegistryId": str,
    },
    total=False,
)

AwsEcsClusterClusterSettingsDetailsTypeDef = TypedDict(
    "AwsEcsClusterClusterSettingsDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef",
    {
        "CloudWatchEncryptionEnabled": bool,
        "CloudWatchLogGroupName": str,
        "S3BucketName": str,
        "S3EncryptionEnabled": bool,
        "S3KeyPrefix": str,
    },
    total=False,
)

AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef = TypedDict(
    "AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef",
    {
        "Base": int,
        "CapacityProvider": str,
        "Weight": int,
    },
    total=False,
)

AwsEcsServiceCapacityProviderStrategyDetailsTypeDef = TypedDict(
    "AwsEcsServiceCapacityProviderStrategyDetailsTypeDef",
    {
        "Base": int,
        "CapacityProvider": str,
        "Weight": int,
    },
    total=False,
)

AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef = TypedDict(
    "AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef",
    {
        "Enable": bool,
        "Rollback": bool,
    },
    total=False,
)

AwsEcsServiceDeploymentControllerDetailsTypeDef = TypedDict(
    "AwsEcsServiceDeploymentControllerDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsEcsServiceLoadBalancersDetailsTypeDef = TypedDict(
    "AwsEcsServiceLoadBalancersDetailsTypeDef",
    {
        "ContainerName": str,
        "ContainerPort": int,
        "LoadBalancerName": str,
        "TargetGroupArn": str,
    },
    total=False,
)

AwsEcsServicePlacementConstraintsDetailsTypeDef = TypedDict(
    "AwsEcsServicePlacementConstraintsDetailsTypeDef",
    {
        "Expression": str,
        "Type": str,
    },
    total=False,
)

AwsEcsServicePlacementStrategiesDetailsTypeDef = TypedDict(
    "AwsEcsServicePlacementStrategiesDetailsTypeDef",
    {
        "Field": str,
        "Type": str,
    },
    total=False,
)

AwsEcsServiceServiceRegistriesDetailsTypeDef = TypedDict(
    "AwsEcsServiceServiceRegistriesDetailsTypeDef",
    {
        "ContainerName": str,
        "ContainerPort": int,
        "Port": int,
        "RegistryArn": str,
    },
    total=False,
)

AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef",
    {
        "AssignPublicIp": str,
        "SecurityGroups": Sequence[str],
        "Subnets": Sequence[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef",
    {
        "Condition": str,
        "ContainerName": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef",
    {
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef",
    {
        "Hostname": str,
        "IpAddress": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef",
    {
        "Options": Mapping[str, str],
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef",
    {
        "Command": Sequence[str],
        "Interval": int,
        "Retries": int,
        "StartPeriod": int,
        "Timeout": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef",
    {
        "ContainerPath": str,
        "ReadOnly": bool,
        "SourceVolume": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef",
    {
        "ContainerPort": int,
        "HostPort": int,
        "Protocol": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef",
    {
        "CredentialsParameter": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef",
    {
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef",
    {
        "Name": str,
        "ValueFrom": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef",
    {
        "Namespace": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef",
    {
        "HardLimit": int,
        "Name": str,
        "SoftLimit": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef",
    {
        "ReadOnly": bool,
        "SourceContainer": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef",
    {
        "Add": Sequence[str],
        "Drop": Sequence[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef",
    {
        "ContainerPath": str,
        "HostPath": str,
        "Permissions": Sequence[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef",
    {
        "ContainerPath": str,
        "MountOptions": Sequence[str],
        "Size": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef",
    {
        "Name": str,
        "ValueFrom": str,
    },
    total=False,
)

AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef",
    {
        "DeviceName": str,
        "DeviceType": str,
    },
    total=False,
)

AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef",
    {
        "Expression": str,
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef",
    {
        "Autoprovision": bool,
        "Driver": str,
        "DriverOpts": Mapping[str, str],
        "Labels": Mapping[str, str],
        "Scope": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesHostDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesHostDetailsTypeDef",
    {
        "SourcePath": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef",
    {
        "AccessPointId": str,
        "Iam": str,
    },
    total=False,
)

AwsEksClusterResourcesVpcConfigDetailsTypeDef = TypedDict(
    "AwsEksClusterResourcesVpcConfigDetailsTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
    },
    total=False,
)

AwsEksClusterLoggingClusterLoggingDetailsTypeDef = TypedDict(
    "AwsEksClusterLoggingClusterLoggingDetailsTypeDef",
    {
        "Enabled": bool,
        "Types": Sequence[str],
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef",
    {
        "EnvironmentName": str,
        "LinkName": str,
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentOptionSettingTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentOptionSettingTypeDef",
    {
        "Namespace": str,
        "OptionName": str,
        "ResourceName": str,
        "Value": str,
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentTierTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentTierTypeDef",
    {
        "Name": str,
        "Type": str,
        "Version": str,
    },
    total=False,
)

AwsElasticsearchDomainDomainEndpointOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainDomainEndpointOptionsTypeDef",
    {
        "EnforceHTTPS": bool,
        "TLSSecurityPolicy": str,
    },
    total=False,
)

AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef",
    {
        "Enabled": bool,
        "KmsKeyId": str,
    },
    total=False,
)

AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsElasticsearchDomainServiceSoftwareOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainServiceSoftwareOptionsTypeDef",
    {
        "AutomatedUpdateDate": str,
        "Cancellable": bool,
        "CurrentVersion": str,
        "Description": str,
        "NewVersion": str,
        "UpdateAvailable": bool,
        "UpdateStatus": str,
    },
    total=False,
)

AwsElasticsearchDomainVPCOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainVPCOptionsTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
        "VPCId": str,
    },
    total=False,
)

AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef",
    {
        "AvailabilityZoneCount": int,
    },
    total=False,
)

AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef = TypedDict(
    "AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "Enabled": bool,
    },
    total=False,
)

AwsElbAppCookieStickinessPolicyTypeDef = TypedDict(
    "AwsElbAppCookieStickinessPolicyTypeDef",
    {
        "CookieName": str,
        "PolicyName": str,
    },
    total=False,
)

AwsElbLbCookieStickinessPolicyTypeDef = TypedDict(
    "AwsElbLbCookieStickinessPolicyTypeDef",
    {
        "CookieExpirationPeriod": int,
        "PolicyName": str,
    },
    total=False,
)

AwsElbLoadBalancerAccessLogTypeDef = TypedDict(
    "AwsElbLoadBalancerAccessLogTypeDef",
    {
        "EmitInterval": int,
        "Enabled": bool,
        "S3BucketName": str,
        "S3BucketPrefix": str,
    },
    total=False,
)

AwsElbLoadBalancerAdditionalAttributeTypeDef = TypedDict(
    "AwsElbLoadBalancerAdditionalAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AwsElbLoadBalancerConnectionDrainingTypeDef = TypedDict(
    "AwsElbLoadBalancerConnectionDrainingTypeDef",
    {
        "Enabled": bool,
        "Timeout": int,
    },
    total=False,
)

AwsElbLoadBalancerConnectionSettingsTypeDef = TypedDict(
    "AwsElbLoadBalancerConnectionSettingsTypeDef",
    {
        "IdleTimeout": int,
    },
    total=False,
)

AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef = TypedDict(
    "AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsElbLoadBalancerBackendServerDescriptionTypeDef = TypedDict(
    "AwsElbLoadBalancerBackendServerDescriptionTypeDef",
    {
        "InstancePort": int,
        "PolicyNames": Sequence[str],
    },
    total=False,
)

AwsElbLoadBalancerHealthCheckTypeDef = TypedDict(
    "AwsElbLoadBalancerHealthCheckTypeDef",
    {
        "HealthyThreshold": int,
        "Interval": int,
        "Target": str,
        "Timeout": int,
        "UnhealthyThreshold": int,
    },
    total=False,
)

AwsElbLoadBalancerInstanceTypeDef = TypedDict(
    "AwsElbLoadBalancerInstanceTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)

AwsElbLoadBalancerSourceSecurityGroupTypeDef = TypedDict(
    "AwsElbLoadBalancerSourceSecurityGroupTypeDef",
    {
        "GroupName": str,
        "OwnerAlias": str,
    },
    total=False,
)

AwsElbLoadBalancerListenerTypeDef = TypedDict(
    "AwsElbLoadBalancerListenerTypeDef",
    {
        "InstancePort": int,
        "InstanceProtocol": str,
        "LoadBalancerPort": int,
        "Protocol": str,
        "SslCertificateId": str,
    },
    total=False,
)

AwsElbv2LoadBalancerAttributeTypeDef = TypedDict(
    "AwsElbv2LoadBalancerAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

LoadBalancerStateTypeDef = TypedDict(
    "LoadBalancerStateTypeDef",
    {
        "Code": str,
        "Reason": str,
    },
    total=False,
)

AwsIamAccessKeySessionContextAttributesTypeDef = TypedDict(
    "AwsIamAccessKeySessionContextAttributesTypeDef",
    {
        "MfaAuthenticated": bool,
        "CreationDate": str,
    },
    total=False,
)

AwsIamAccessKeySessionContextSessionIssuerTypeDef = TypedDict(
    "AwsIamAccessKeySessionContextSessionIssuerTypeDef",
    {
        "Type": str,
        "PrincipalId": str,
        "Arn": str,
        "AccountId": str,
        "UserName": str,
    },
    total=False,
)

AwsIamAttachedManagedPolicyTypeDef = TypedDict(
    "AwsIamAttachedManagedPolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyArn": str,
    },
    total=False,
)

AwsIamGroupPolicyTypeDef = TypedDict(
    "AwsIamGroupPolicyTypeDef",
    {
        "PolicyName": str,
    },
    total=False,
)

AwsIamInstanceProfileRoleTypeDef = TypedDict(
    "AwsIamInstanceProfileRoleTypeDef",
    {
        "Arn": str,
        "AssumeRolePolicyDocument": str,
        "CreateDate": str,
        "Path": str,
        "RoleId": str,
        "RoleName": str,
    },
    total=False,
)

AwsIamPermissionsBoundaryTypeDef = TypedDict(
    "AwsIamPermissionsBoundaryTypeDef",
    {
        "PermissionsBoundaryArn": str,
        "PermissionsBoundaryType": str,
    },
    total=False,
)

AwsIamPolicyVersionTypeDef = TypedDict(
    "AwsIamPolicyVersionTypeDef",
    {
        "VersionId": str,
        "IsDefaultVersion": bool,
        "CreateDate": str,
    },
    total=False,
)

AwsIamRolePolicyTypeDef = TypedDict(
    "AwsIamRolePolicyTypeDef",
    {
        "PolicyName": str,
    },
    total=False,
)

AwsIamUserPolicyTypeDef = TypedDict(
    "AwsIamUserPolicyTypeDef",
    {
        "PolicyName": str,
    },
    total=False,
)

AwsKmsKeyDetailsTypeDef = TypedDict(
    "AwsKmsKeyDetailsTypeDef",
    {
        "AWSAccountId": str,
        "CreationDate": float,
        "KeyId": str,
        "KeyManager": str,
        "KeyState": str,
        "Origin": str,
        "Description": str,
        "KeyRotationStatus": bool,
    },
    total=False,
)

AwsLambdaFunctionCodeTypeDef = TypedDict(
    "AwsLambdaFunctionCodeTypeDef",
    {
        "S3Bucket": str,
        "S3Key": str,
        "S3ObjectVersion": str,
        "ZipFile": str,
    },
    total=False,
)

AwsLambdaFunctionDeadLetterConfigTypeDef = TypedDict(
    "AwsLambdaFunctionDeadLetterConfigTypeDef",
    {
        "TargetArn": str,
    },
    total=False,
)

AwsLambdaFunctionLayerTypeDef = TypedDict(
    "AwsLambdaFunctionLayerTypeDef",
    {
        "Arn": str,
        "CodeSize": int,
    },
    total=False,
)

AwsLambdaFunctionTracingConfigTypeDef = TypedDict(
    "AwsLambdaFunctionTracingConfigTypeDef",
    {
        "Mode": str,
    },
    total=False,
)

AwsLambdaFunctionVpcConfigTypeDef = TypedDict(
    "AwsLambdaFunctionVpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
        "VpcId": str,
    },
    total=False,
)

AwsLambdaFunctionEnvironmentErrorTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentErrorTypeDef",
    {
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

AwsLambdaLayerVersionDetailsTypeDef = TypedDict(
    "AwsLambdaLayerVersionDetailsTypeDef",
    {
        "Version": int,
        "CompatibleRuntimes": Sequence[str],
        "CreatedDate": str,
    },
    total=False,
)

AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef",
    {
        "SubnetId": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef",
    {
        "AvailabilityZoneCount": int,
    },
    total=False,
)

AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef",
    {
        "CustomEndpointCertificateArn": str,
        "CustomEndpointEnabled": bool,
        "EnforceHTTPS": bool,
        "CustomEndpoint": str,
        "TLSSecurityPolicy": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef",
    {
        "Enabled": bool,
        "KmsKeyId": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef",
    {
        "AutomatedUpdateDate": str,
        "Cancellable": bool,
        "CurrentVersion": str,
        "Description": str,
        "NewVersion": str,
        "UpdateAvailable": bool,
        "UpdateStatus": str,
        "OptionalDeployment": bool,
    },
    total=False,
)

AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
    },
    total=False,
)

AwsOpenSearchServiceDomainLogPublishingOptionTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainLogPublishingOptionTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "Enabled": bool,
    },
    total=False,
)

AwsRdsDbClusterAssociatedRoleTypeDef = TypedDict(
    "AwsRdsDbClusterAssociatedRoleTypeDef",
    {
        "RoleArn": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbClusterMemberTypeDef = TypedDict(
    "AwsRdsDbClusterMemberTypeDef",
    {
        "IsClusterWriter": bool,
        "PromotionTier": int,
        "DbInstanceIdentifier": str,
        "DbClusterParameterGroupStatus": str,
    },
    total=False,
)

AwsRdsDbClusterOptionGroupMembershipTypeDef = TypedDict(
    "AwsRdsDbClusterOptionGroupMembershipTypeDef",
    {
        "DbClusterOptionGroupName": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbDomainMembershipTypeDef = TypedDict(
    "AwsRdsDbDomainMembershipTypeDef",
    {
        "Domain": str,
        "Status": str,
        "Fqdn": str,
        "IamRoleName": str,
    },
    total=False,
)

AwsRdsDbInstanceVpcSecurityGroupTypeDef = TypedDict(
    "AwsRdsDbInstanceVpcSecurityGroupTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbClusterSnapshotDetailsTypeDef = TypedDict(
    "AwsRdsDbClusterSnapshotDetailsTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "SnapshotCreateTime": str,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "VpcId": str,
        "ClusterCreateTime": str,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "PercentProgress": int,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterIdentifier": str,
        "DbClusterSnapshotIdentifier": str,
        "IamDatabaseAuthenticationEnabled": bool,
    },
    total=False,
)

AwsRdsDbInstanceAssociatedRoleTypeDef = TypedDict(
    "AwsRdsDbInstanceAssociatedRoleTypeDef",
    {
        "RoleArn": str,
        "FeatureName": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbInstanceEndpointTypeDef = TypedDict(
    "AwsRdsDbInstanceEndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "HostedZoneId": str,
    },
    total=False,
)

AwsRdsDbOptionGroupMembershipTypeDef = TypedDict(
    "AwsRdsDbOptionGroupMembershipTypeDef",
    {
        "OptionGroupName": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbParameterGroupTypeDef = TypedDict(
    "AwsRdsDbParameterGroupTypeDef",
    {
        "DbParameterGroupName": str,
        "ParameterApplyStatus": str,
    },
    total=False,
)

AwsRdsDbProcessorFeatureTypeDef = TypedDict(
    "AwsRdsDbProcessorFeatureTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsRdsDbStatusInfoTypeDef = TypedDict(
    "AwsRdsDbStatusInfoTypeDef",
    {
        "StatusType": str,
        "Normal": bool,
        "Status": str,
        "Message": str,
    },
    total=False,
)

AwsRdsPendingCloudWatchLogsExportsTypeDef = TypedDict(
    "AwsRdsPendingCloudWatchLogsExportsTypeDef",
    {
        "LogTypesToEnable": Sequence[str],
        "LogTypesToDisable": Sequence[str],
    },
    total=False,
)

AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef",
    {
        "Ec2SecurityGroupId": str,
        "Ec2SecurityGroupName": str,
        "Ec2SecurityGroupOwnerId": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbSecurityGroupIpRangeTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupIpRangeTypeDef",
    {
        "CidrIp": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

AwsRdsEventSubscriptionDetailsTypeDef = TypedDict(
    "AwsRdsEventSubscriptionDetailsTypeDef",
    {
        "CustSubscriptionId": str,
        "CustomerAwsId": str,
        "Enabled": bool,
        "EventCategoriesList": Sequence[str],
        "EventSubscriptionArn": str,
        "SnsTopicArn": str,
        "SourceIdsList": Sequence[str],
        "SourceType": str,
        "Status": str,
        "SubscriptionCreationTime": str,
    },
    total=False,
)

AwsRedshiftClusterClusterNodeTypeDef = TypedDict(
    "AwsRedshiftClusterClusterNodeTypeDef",
    {
        "NodeRole": str,
        "PrivateIpAddress": str,
        "PublicIpAddress": str,
    },
    total=False,
)

AwsRedshiftClusterClusterParameterStatusTypeDef = TypedDict(
    "AwsRedshiftClusterClusterParameterStatusTypeDef",
    {
        "ParameterName": str,
        "ParameterApplyStatus": str,
        "ParameterApplyErrorDescription": str,
    },
    total=False,
)

AwsRedshiftClusterClusterSecurityGroupTypeDef = TypedDict(
    "AwsRedshiftClusterClusterSecurityGroupTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef = TypedDict(
    "AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef",
    {
        "DestinationRegion": str,
        "ManualSnapshotRetentionPeriod": int,
        "RetentionPeriod": int,
        "SnapshotCopyGrantName": str,
    },
    total=False,
)

AwsRedshiftClusterDeferredMaintenanceWindowTypeDef = TypedDict(
    "AwsRedshiftClusterDeferredMaintenanceWindowTypeDef",
    {
        "DeferMaintenanceEndTime": str,
        "DeferMaintenanceIdentifier": str,
        "DeferMaintenanceStartTime": str,
    },
    total=False,
)

AwsRedshiftClusterElasticIpStatusTypeDef = TypedDict(
    "AwsRedshiftClusterElasticIpStatusTypeDef",
    {
        "ElasticIp": str,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterEndpointTypeDef = TypedDict(
    "AwsRedshiftClusterEndpointTypeDef",
    {
        "Address": str,
        "Port": int,
    },
    total=False,
)

AwsRedshiftClusterHsmStatusTypeDef = TypedDict(
    "AwsRedshiftClusterHsmStatusTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
        "HsmConfigurationIdentifier": str,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterIamRoleTypeDef = TypedDict(
    "AwsRedshiftClusterIamRoleTypeDef",
    {
        "ApplyStatus": str,
        "IamRoleArn": str,
    },
    total=False,
)

AwsRedshiftClusterLoggingStatusTypeDef = TypedDict(
    "AwsRedshiftClusterLoggingStatusTypeDef",
    {
        "BucketName": str,
        "LastFailureMessage": str,
        "LastFailureTime": str,
        "LastSuccessfulDeliveryTime": str,
        "LoggingEnabled": bool,
        "S3KeyPrefix": str,
    },
    total=False,
)

AwsRedshiftClusterPendingModifiedValuesTypeDef = TypedDict(
    "AwsRedshiftClusterPendingModifiedValuesTypeDef",
    {
        "AutomatedSnapshotRetentionPeriod": int,
        "ClusterIdentifier": str,
        "ClusterType": str,
        "ClusterVersion": str,
        "EncryptionType": str,
        "EnhancedVpcRouting": bool,
        "MaintenanceTrackName": str,
        "MasterUserPassword": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "PubliclyAccessible": bool,
    },
    total=False,
)

AwsRedshiftClusterResizeInfoTypeDef = TypedDict(
    "AwsRedshiftClusterResizeInfoTypeDef",
    {
        "AllowCancelResize": bool,
        "ResizeType": str,
    },
    total=False,
)

AwsRedshiftClusterRestoreStatusTypeDef = TypedDict(
    "AwsRedshiftClusterRestoreStatusTypeDef",
    {
        "CurrentRestoreRateInMegaBytesPerSecond": float,
        "ElapsedTimeInSeconds": int,
        "EstimatedTimeToCompletionInSeconds": int,
        "ProgressInMegaBytes": int,
        "SnapshotSizeInMegaBytes": int,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterVpcSecurityGroupTypeDef = TypedDict(
    "AwsRedshiftClusterVpcSecurityGroupTypeDef",
    {
        "Status": str,
        "VpcSecurityGroupId": str,
    },
    total=False,
)

AwsS3AccountPublicAccessBlockDetailsTypeDef = TypedDict(
    "AwsS3AccountPublicAccessBlockDetailsTypeDef",
    {
        "BlockPublicAcls": bool,
        "BlockPublicPolicy": bool,
        "IgnorePublicAcls": bool,
        "RestrictPublicBuckets": bool,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef = (
    TypedDict(
        "AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef",
        {
            "DaysAfterInitiation": int,
        },
        total=False,
    )
)

AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef",
    {
        "Days": int,
        "StorageClass": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef",
    {
        "Date": str,
        "Days": int,
        "StorageClass": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AwsS3BucketBucketVersioningConfigurationTypeDef = TypedDict(
    "AwsS3BucketBucketVersioningConfigurationTypeDef",
    {
        "IsMfaDeleteEnabled": bool,
        "Status": str,
    },
    total=False,
)

AwsS3BucketLoggingConfigurationTypeDef = TypedDict(
    "AwsS3BucketLoggingConfigurationTypeDef",
    {
        "DestinationBucketName": str,
        "LogFilePrefix": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef",
    {
        "Name": AwsS3BucketNotificationConfigurationS3KeyFilterRuleNameType,
        "Value": str,
    },
    total=False,
)

AwsS3BucketServerSideEncryptionByDefaultTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionByDefaultTypeDef",
    {
        "SSEAlgorithm": str,
        "KMSMasterKeyID": str,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRedirectToTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRedirectToTypeDef",
    {
        "Hostname": str,
        "Protocol": str,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef",
    {
        "HttpErrorCodeReturnedEquals": str,
        "KeyPrefixEquals": str,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef",
    {
        "Hostname": str,
        "HttpRedirectCode": str,
        "Protocol": str,
        "ReplaceKeyPrefixWith": str,
        "ReplaceKeyWith": str,
    },
    total=False,
)

AwsS3ObjectDetailsTypeDef = TypedDict(
    "AwsS3ObjectDetailsTypeDef",
    {
        "LastModified": str,
        "ETag": str,
        "VersionId": str,
        "ContentType": str,
        "ServerSideEncryption": str,
        "SSEKMSKeyId": str,
    },
    total=False,
)

AwsSecretsManagerSecretRotationRulesTypeDef = TypedDict(
    "AwsSecretsManagerSecretRotationRulesTypeDef",
    {
        "AutomaticallyAfterDays": int,
    },
    total=False,
)

BooleanFilterTypeDef = TypedDict(
    "BooleanFilterTypeDef",
    {
        "Value": bool,
    },
    total=False,
)

IpFilterTypeDef = TypedDict(
    "IpFilterTypeDef",
    {
        "Cidr": str,
    },
    total=False,
)

KeywordFilterTypeDef = TypedDict(
    "KeywordFilterTypeDef",
    {
        "Value": str,
    },
    total=False,
)

MapFilterTypeDef = TypedDict(
    "MapFilterTypeDef",
    {
        "Key": str,
        "Value": str,
        "Comparison": MapFilterComparisonType,
    },
    total=False,
)

NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef",
    {
        "Gte": float,
        "Lte": float,
        "Eq": float,
    },
    total=False,
)

StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef",
    {
        "Value": str,
        "Comparison": StringFilterComparisonType,
    },
    total=False,
)

AwsSecurityFindingIdentifierTypeDef = TypedDict(
    "AwsSecurityFindingIdentifierTypeDef",
    {
        "Id": str,
        "ProductArn": str,
    },
)

_RequiredMalwareTypeDef = TypedDict(
    "_RequiredMalwareTypeDef",
    {
        "Name": str,
    },
)
_OptionalMalwareTypeDef = TypedDict(
    "_OptionalMalwareTypeDef",
    {
        "Type": MalwareTypeType,
        "Path": str,
        "State": MalwareStateType,
    },
    total=False,
)


class MalwareTypeDef(_RequiredMalwareTypeDef, _OptionalMalwareTypeDef):
    pass


NoteTypeDef = TypedDict(
    "NoteTypeDef",
    {
        "Text": str,
        "UpdatedBy": str,
        "UpdatedAt": str,
    },
)

_RequiredPatchSummaryTypeDef = TypedDict(
    "_RequiredPatchSummaryTypeDef",
    {
        "Id": str,
    },
)
_OptionalPatchSummaryTypeDef = TypedDict(
    "_OptionalPatchSummaryTypeDef",
    {
        "InstalledCount": int,
        "MissingCount": int,
        "FailedCount": int,
        "InstalledOtherCount": int,
        "InstalledRejectedCount": int,
        "InstalledPendingReboot": int,
        "OperationStartTime": str,
        "OperationEndTime": str,
        "RebootOption": str,
        "Operation": str,
    },
    total=False,
)


class PatchSummaryTypeDef(_RequiredPatchSummaryTypeDef, _OptionalPatchSummaryTypeDef):
    pass


ProcessDetailsTypeDef = TypedDict(
    "ProcessDetailsTypeDef",
    {
        "Name": str,
        "Path": str,
        "Pid": int,
        "ParentPid": int,
        "LaunchedAt": str,
        "TerminatedAt": str,
    },
    total=False,
)

RelatedFindingTypeDef = TypedDict(
    "RelatedFindingTypeDef",
    {
        "ProductArn": str,
        "Id": str,
    },
)

SeverityTypeDef = TypedDict(
    "SeverityTypeDef",
    {
        "Product": float,
        "Label": SeverityLabelType,
        "Normalized": int,
        "Original": str,
    },
    total=False,
)

ThreatIntelIndicatorTypeDef = TypedDict(
    "ThreatIntelIndicatorTypeDef",
    {
        "Type": ThreatIntelIndicatorTypeType,
        "Value": str,
        "Category": ThreatIntelIndicatorCategoryType,
        "LastObservedAt": str,
        "Source": str,
        "SourceUrl": str,
    },
    total=False,
)

WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef",
    {
        "Status": WorkflowStatusType,
    },
    total=False,
)

AwsSnsTopicSubscriptionTypeDef = TypedDict(
    "AwsSnsTopicSubscriptionTypeDef",
    {
        "Endpoint": str,
        "Protocol": str,
    },
    total=False,
)

AwsSqsQueueDetailsTypeDef = TypedDict(
    "AwsSqsQueueDetailsTypeDef",
    {
        "KmsDataKeyReusePeriodSeconds": int,
        "KmsMasterKeyId": str,
        "QueueName": str,
        "DeadLetterTargetArn": str,
    },
    total=False,
)

AwsSsmComplianceSummaryTypeDef = TypedDict(
    "AwsSsmComplianceSummaryTypeDef",
    {
        "Status": str,
        "CompliantCriticalCount": int,
        "CompliantHighCount": int,
        "CompliantMediumCount": int,
        "ExecutionType": str,
        "NonCompliantCriticalCount": int,
        "CompliantInformationalCount": int,
        "NonCompliantInformationalCount": int,
        "CompliantUnspecifiedCount": int,
        "NonCompliantLowCount": int,
        "NonCompliantHighCount": int,
        "CompliantLowCount": int,
        "ComplianceType": str,
        "PatchBaselineId": str,
        "OverallSeverity": str,
        "NonCompliantMediumCount": int,
        "NonCompliantUnspecifiedCount": int,
        "PatchGroup": str,
    },
    total=False,
)

AwsWafRateBasedRuleMatchPredicateTypeDef = TypedDict(
    "AwsWafRateBasedRuleMatchPredicateTypeDef",
    {
        "DataId": str,
        "Negated": bool,
        "Type": str,
    },
    total=False,
)

AwsWafRegionalRateBasedRuleMatchPredicateTypeDef = TypedDict(
    "AwsWafRegionalRateBasedRuleMatchPredicateTypeDef",
    {
        "DataId": str,
        "Negated": bool,
        "Type": str,
    },
    total=False,
)

WafActionTypeDef = TypedDict(
    "WafActionTypeDef",
    {
        "Type": str,
    },
    total=False,
)

WafExcludedRuleTypeDef = TypedDict(
    "WafExcludedRuleTypeDef",
    {
        "RuleId": str,
    },
    total=False,
)

WafOverrideActionTypeDef = TypedDict(
    "WafOverrideActionTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsXrayEncryptionConfigDetailsTypeDef = TypedDict(
    "AwsXrayEncryptionConfigDetailsTypeDef",
    {
        "KeyId": str,
        "Status": str,
        "Type": str,
    },
    total=False,
)

BatchDisableStandardsRequestRequestTypeDef = TypedDict(
    "BatchDisableStandardsRequestRequestTypeDef",
    {
        "StandardsSubscriptionArns": Sequence[str],
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

_RequiredStandardsSubscriptionRequestTypeDef = TypedDict(
    "_RequiredStandardsSubscriptionRequestTypeDef",
    {
        "StandardsArn": str,
    },
)
_OptionalStandardsSubscriptionRequestTypeDef = TypedDict(
    "_OptionalStandardsSubscriptionRequestTypeDef",
    {
        "StandardsInput": Mapping[str, str],
    },
    total=False,
)


class StandardsSubscriptionRequestTypeDef(
    _RequiredStandardsSubscriptionRequestTypeDef, _OptionalStandardsSubscriptionRequestTypeDef
):
    pass


ImportFindingsErrorTypeDef = TypedDict(
    "ImportFindingsErrorTypeDef",
    {
        "Id": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
)

NoteUpdateTypeDef = TypedDict(
    "NoteUpdateTypeDef",
    {
        "Text": str,
        "UpdatedBy": str,
    },
)

SeverityUpdateTypeDef = TypedDict(
    "SeverityUpdateTypeDef",
    {
        "Normalized": int,
        "Product": float,
        "Label": SeverityLabelType,
    },
    total=False,
)

WorkflowUpdateTypeDef = TypedDict(
    "WorkflowUpdateTypeDef",
    {
        "Status": WorkflowStatusType,
    },
    total=False,
)

CellTypeDef = TypedDict(
    "CellTypeDef",
    {
        "Column": int,
        "Row": int,
        "ColumnName": str,
        "CellReference": str,
    },
    total=False,
)

ClassificationStatusTypeDef = TypedDict(
    "ClassificationStatusTypeDef",
    {
        "Code": str,
        "Reason": str,
    },
    total=False,
)

_RequiredStatusReasonTypeDef = TypedDict(
    "_RequiredStatusReasonTypeDef",
    {
        "ReasonCode": str,
    },
)
_OptionalStatusReasonTypeDef = TypedDict(
    "_OptionalStatusReasonTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class StatusReasonTypeDef(_RequiredStatusReasonTypeDef, _OptionalStatusReasonTypeDef):
    pass


ContainerDetailsTypeDef = TypedDict(
    "ContainerDetailsTypeDef",
    {
        "Name": str,
        "ImageId": str,
        "ImageName": str,
        "LaunchedAt": str,
    },
    total=False,
)

CreateActionTargetRequestRequestTypeDef = TypedDict(
    "CreateActionTargetRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Id": str,
    },
)

_RequiredCreateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFindingAggregatorRequestRequestTypeDef",
    {
        "RegionLinkingMode": str,
    },
)
_OptionalCreateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFindingAggregatorRequestRequestTypeDef",
    {
        "Regions": Sequence[str],
    },
    total=False,
)


class CreateFindingAggregatorRequestRequestTypeDef(
    _RequiredCreateFindingAggregatorRequestRequestTypeDef,
    _OptionalCreateFindingAggregatorRequestRequestTypeDef,
):
    pass


ResultTypeDef = TypedDict(
    "ResultTypeDef",
    {
        "AccountId": str,
        "ProcessingResult": str,
    },
    total=False,
)

DateRangeTypeDef = TypedDict(
    "DateRangeTypeDef",
    {
        "Value": int,
        "Unit": Literal["DAYS"],
    },
    total=False,
)

DeclineInvitationsRequestRequestTypeDef = TypedDict(
    "DeclineInvitationsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

DeleteActionTargetRequestRequestTypeDef = TypedDict(
    "DeleteActionTargetRequestRequestTypeDef",
    {
        "ActionTargetArn": str,
    },
)

DeleteFindingAggregatorRequestRequestTypeDef = TypedDict(
    "DeleteFindingAggregatorRequestRequestTypeDef",
    {
        "FindingAggregatorArn": str,
    },
)

DeleteInsightRequestRequestTypeDef = TypedDict(
    "DeleteInsightRequestRequestTypeDef",
    {
        "InsightArn": str,
    },
)

DeleteInvitationsRequestRequestTypeDef = TypedDict(
    "DeleteInvitationsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

DeleteMembersRequestRequestTypeDef = TypedDict(
    "DeleteMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
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

DescribeActionTargetsRequestRequestTypeDef = TypedDict(
    "DescribeActionTargetsRequestRequestTypeDef",
    {
        "ActionTargetArns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeHubRequestRequestTypeDef = TypedDict(
    "DescribeHubRequestRequestTypeDef",
    {
        "HubArn": str,
    },
    total=False,
)

DescribeProductsRequestRequestTypeDef = TypedDict(
    "DescribeProductsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ProductArn": str,
    },
    total=False,
)

_RequiredProductTypeDef = TypedDict(
    "_RequiredProductTypeDef",
    {
        "ProductArn": str,
    },
)
_OptionalProductTypeDef = TypedDict(
    "_OptionalProductTypeDef",
    {
        "ProductName": str,
        "CompanyName": str,
        "Description": str,
        "Categories": List[str],
        "IntegrationTypes": List[IntegrationTypeType],
        "MarketplaceUrl": str,
        "ActivationUrl": str,
        "ProductSubscriptionResourcePolicy": str,
    },
    total=False,
)


class ProductTypeDef(_RequiredProductTypeDef, _OptionalProductTypeDef):
    pass


_RequiredDescribeStandardsControlsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeStandardsControlsRequestRequestTypeDef",
    {
        "StandardsSubscriptionArn": str,
    },
)
_OptionalDescribeStandardsControlsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeStandardsControlsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeStandardsControlsRequestRequestTypeDef(
    _RequiredDescribeStandardsControlsRequestRequestTypeDef,
    _OptionalDescribeStandardsControlsRequestRequestTypeDef,
):
    pass


StandardsControlTypeDef = TypedDict(
    "StandardsControlTypeDef",
    {
        "StandardsControlArn": str,
        "ControlStatus": ControlStatusType,
        "DisabledReason": str,
        "ControlStatusUpdatedAt": datetime,
        "ControlId": str,
        "Title": str,
        "Description": str,
        "RemediationUrl": str,
        "SeverityRating": SeverityRatingType,
        "RelatedRequirements": List[str],
    },
    total=False,
)

DescribeStandardsRequestRequestTypeDef = TypedDict(
    "DescribeStandardsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

StandardTypeDef = TypedDict(
    "StandardTypeDef",
    {
        "StandardsArn": str,
        "Name": str,
        "Description": str,
        "EnabledByDefault": bool,
    },
    total=False,
)

DisableImportFindingsForProductRequestRequestTypeDef = TypedDict(
    "DisableImportFindingsForProductRequestRequestTypeDef",
    {
        "ProductSubscriptionArn": str,
    },
)

DisableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AdminAccountId": str,
    },
)

DisassociateMembersRequestRequestTypeDef = TypedDict(
    "DisassociateMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

EnableImportFindingsForProductRequestRequestTypeDef = TypedDict(
    "EnableImportFindingsForProductRequestRequestTypeDef",
    {
        "ProductArn": str,
    },
)

EnableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AdminAccountId": str,
    },
)

EnableSecurityHubRequestRequestTypeDef = TypedDict(
    "EnableSecurityHubRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "EnableDefaultStandards": bool,
    },
    total=False,
)

FindingAggregatorTypeDef = TypedDict(
    "FindingAggregatorTypeDef",
    {
        "FindingAggregatorArn": str,
    },
    total=False,
)

FindingProviderSeverityTypeDef = TypedDict(
    "FindingProviderSeverityTypeDef",
    {
        "Label": SeverityLabelType,
        "Original": str,
    },
    total=False,
)

FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef = TypedDict(
    "FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef",
    {
        "ResourceArn": str,
    },
    total=False,
)

FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef = TypedDict(
    "FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef",
    {
        "Priority": int,
        "ResourceArn": str,
    },
    total=False,
)

InvitationTypeDef = TypedDict(
    "InvitationTypeDef",
    {
        "AccountId": str,
        "InvitationId": str,
        "InvitedAt": datetime,
        "MemberStatus": str,
    },
    total=False,
)

GetEnabledStandardsRequestRequestTypeDef = TypedDict(
    "GetEnabledStandardsRequestRequestTypeDef",
    {
        "StandardsSubscriptionArns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetFindingAggregatorRequestRequestTypeDef = TypedDict(
    "GetFindingAggregatorRequestRequestTypeDef",
    {
        "FindingAggregatorArn": str,
    },
)

SortCriterionTypeDef = TypedDict(
    "SortCriterionTypeDef",
    {
        "Field": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

GetInsightResultsRequestRequestTypeDef = TypedDict(
    "GetInsightResultsRequestRequestTypeDef",
    {
        "InsightArn": str,
    },
)

GetInsightsRequestRequestTypeDef = TypedDict(
    "GetInsightsRequestRequestTypeDef",
    {
        "InsightArns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetMembersRequestRequestTypeDef = TypedDict(
    "GetMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "AccountId": str,
        "Email": str,
        "MasterId": str,
        "AdministratorId": str,
        "MemberStatus": str,
        "InvitedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

InsightResultValueTypeDef = TypedDict(
    "InsightResultValueTypeDef",
    {
        "GroupByAttributeValue": str,
        "Count": int,
    },
)

InviteMembersRequestRequestTypeDef = TypedDict(
    "InviteMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

ListEnabledProductsForImportRequestRequestTypeDef = TypedDict(
    "ListEnabledProductsForImportRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListFindingAggregatorsRequestRequestTypeDef = TypedDict(
    "ListFindingAggregatorsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListInvitationsRequestRequestTypeDef = TypedDict(
    "ListInvitationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "OnlyAssociated": bool,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListOrganizationAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "Begin": int,
        "End": int,
    },
    total=False,
)

RangeTypeDef = TypedDict(
    "RangeTypeDef",
    {
        "Start": int,
        "End": int,
        "StartColumn": int,
    },
    total=False,
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "JsonPath": str,
        "RecordIndex": int,
    },
    total=False,
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Text": str,
        "Url": str,
    },
    total=False,
)

RuleGroupSourceListDetailsTypeDef = TypedDict(
    "RuleGroupSourceListDetailsTypeDef",
    {
        "GeneratedRulesType": str,
        "TargetTypes": Sequence[str],
        "Targets": Sequence[str],
    },
    total=False,
)

RuleGroupSourceStatefulRulesHeaderDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesHeaderDetailsTypeDef",
    {
        "Destination": str,
        "DestinationPort": str,
        "Direction": str,
        "Protocol": str,
        "Source": str,
        "SourcePort": str,
    },
    total=False,
)

RuleGroupSourceStatefulRulesOptionsDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesOptionsDetailsTypeDef",
    {
        "Keyword": str,
        "Settings": Sequence[str],
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef",
    {
        "AddressDefinition": str,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef",
    {
        "AddressDefinition": str,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef",
    {
        "Flags": Sequence[str],
        "Masks": Sequence[str],
    },
    total=False,
)

RuleGroupVariablesIpSetsDetailsTypeDef = TypedDict(
    "RuleGroupVariablesIpSetsDetailsTypeDef",
    {
        "Definition": Sequence[str],
    },
    total=False,
)

RuleGroupVariablesPortSetsDetailsTypeDef = TypedDict(
    "RuleGroupVariablesPortSetsDetailsTypeDef",
    {
        "Definition": Sequence[str],
    },
    total=False,
)

SoftwarePackageTypeDef = TypedDict(
    "SoftwarePackageTypeDef",
    {
        "Name": str,
        "Version": str,
        "Epoch": str,
        "Release": str,
        "Architecture": str,
        "PackageManager": str,
        "FilePath": str,
    },
    total=False,
)

StandardsStatusReasonTypeDef = TypedDict(
    "StandardsStatusReasonTypeDef",
    {
        "StatusReasonCode": StatusReasonCodeType,
    },
)

StatelessCustomPublishMetricActionDimensionTypeDef = TypedDict(
    "StatelessCustomPublishMetricActionDimensionTypeDef",
    {
        "Value": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateActionTargetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateActionTargetRequestRequestTypeDef",
    {
        "ActionTargetArn": str,
    },
)
_OptionalUpdateActionTargetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateActionTargetRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)


class UpdateActionTargetRequestRequestTypeDef(
    _RequiredUpdateActionTargetRequestRequestTypeDef,
    _OptionalUpdateActionTargetRequestRequestTypeDef,
):
    pass


_RequiredUpdateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFindingAggregatorRequestRequestTypeDef",
    {
        "FindingAggregatorArn": str,
        "RegionLinkingMode": str,
    },
)
_OptionalUpdateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFindingAggregatorRequestRequestTypeDef",
    {
        "Regions": Sequence[str],
    },
    total=False,
)


class UpdateFindingAggregatorRequestRequestTypeDef(
    _RequiredUpdateFindingAggregatorRequestRequestTypeDef,
    _OptionalUpdateFindingAggregatorRequestRequestTypeDef,
):
    pass


_RequiredUpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "AutoEnable": bool,
    },
)
_OptionalUpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "AutoEnableStandards": AutoEnableStandardsType,
    },
    total=False,
)


class UpdateOrganizationConfigurationRequestRequestTypeDef(
    _RequiredUpdateOrganizationConfigurationRequestRequestTypeDef,
    _OptionalUpdateOrganizationConfigurationRequestRequestTypeDef,
):
    pass


UpdateSecurityHubConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateSecurityHubConfigurationRequestRequestTypeDef",
    {
        "AutoEnableControls": bool,
    },
    total=False,
)

_RequiredUpdateStandardsControlRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStandardsControlRequestRequestTypeDef",
    {
        "StandardsControlArn": str,
    },
)
_OptionalUpdateStandardsControlRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStandardsControlRequestRequestTypeDef",
    {
        "ControlStatus": ControlStatusType,
        "DisabledReason": str,
    },
    total=False,
)


class UpdateStandardsControlRequestRequestTypeDef(
    _RequiredUpdateStandardsControlRequestRequestTypeDef,
    _OptionalUpdateStandardsControlRequestRequestTypeDef,
):
    pass


_RequiredVulnerabilityVendorTypeDef = TypedDict(
    "_RequiredVulnerabilityVendorTypeDef",
    {
        "Name": str,
    },
)
_OptionalVulnerabilityVendorTypeDef = TypedDict(
    "_OptionalVulnerabilityVendorTypeDef",
    {
        "Url": str,
        "VendorSeverity": str,
        "VendorCreatedAt": str,
        "VendorUpdatedAt": str,
    },
    total=False,
)


class VulnerabilityVendorTypeDef(
    _RequiredVulnerabilityVendorTypeDef, _OptionalVulnerabilityVendorTypeDef
):
    pass


CreateMembersRequestRequestTypeDef = TypedDict(
    "CreateMembersRequestRequestTypeDef",
    {
        "AccountDetails": Sequence[AccountDetailsTypeDef],
    },
)

ActionRemoteIpDetailsTypeDef = TypedDict(
    "ActionRemoteIpDetailsTypeDef",
    {
        "IpAddressV4": str,
        "Organization": IpOrganizationDetailsTypeDef,
        "Country": CountryTypeDef,
        "City": CityTypeDef,
        "GeoLocation": GeoLocationTypeDef,
    },
    total=False,
)

CvssTypeDef = TypedDict(
    "CvssTypeDef",
    {
        "Version": str,
        "BaseScore": float,
        "BaseVector": str,
        "Source": str,
        "Adjustments": Sequence[AdjustmentTypeDef],
    },
    total=False,
)

AwsApiGatewayRestApiDetailsTypeDef = TypedDict(
    "AwsApiGatewayRestApiDetailsTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "CreatedDate": str,
        "Version": str,
        "BinaryMediaTypes": Sequence[str],
        "MinimumCompressionSize": int,
        "ApiKeySource": str,
        "EndpointConfiguration": AwsApiGatewayEndpointConfigurationTypeDef,
    },
    total=False,
)

AwsApiGatewayStageDetailsTypeDef = TypedDict(
    "AwsApiGatewayStageDetailsTypeDef",
    {
        "DeploymentId": str,
        "ClientCertificateId": str,
        "StageName": str,
        "Description": str,
        "CacheClusterEnabled": bool,
        "CacheClusterSize": str,
        "CacheClusterStatus": str,
        "MethodSettings": Sequence[AwsApiGatewayMethodSettingsTypeDef],
        "Variables": Mapping[str, str],
        "DocumentationVersion": str,
        "AccessLogSettings": AwsApiGatewayAccessLogSettingsTypeDef,
        "CanarySettings": AwsApiGatewayCanarySettingsTypeDef,
        "TracingEnabled": bool,
        "CreatedDate": str,
        "LastUpdatedDate": str,
        "WebAclArn": str,
    },
    total=False,
)

AwsApiGatewayV2ApiDetailsTypeDef = TypedDict(
    "AwsApiGatewayV2ApiDetailsTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CreatedDate": str,
        "Description": str,
        "Version": str,
        "Name": str,
        "ProtocolType": str,
        "RouteSelectionExpression": str,
        "CorsConfiguration": AwsCorsConfigurationTypeDef,
    },
    total=False,
)

AwsApiGatewayV2StageDetailsTypeDef = TypedDict(
    "AwsApiGatewayV2StageDetailsTypeDef",
    {
        "ClientCertificateId": str,
        "CreatedDate": str,
        "Description": str,
        "DefaultRouteSettings": AwsApiGatewayV2RouteSettingsTypeDef,
        "DeploymentId": str,
        "LastUpdatedDate": str,
        "RouteSettings": AwsApiGatewayV2RouteSettingsTypeDef,
        "StageName": str,
        "StageVariables": Mapping[str, str],
        "AccessLogSettings": AwsApiGatewayAccessLogSettingsTypeDef,
        "AutoDeploy": bool,
        "LastDeploymentStatusMessage": str,
        "ApiGatewayManaged": bool,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef",
    {
        "LaunchTemplateSpecification": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef,
        "Overrides": Sequence[
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef
        ],
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef",
    {
        "DeviceName": str,
        "Ebs": AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef,
        "NoDevice": bool,
        "VirtualName": str,
    },
    total=False,
)

AwsCertificateManagerCertificateDomainValidationOptionTypeDef = TypedDict(
    "AwsCertificateManagerCertificateDomainValidationOptionTypeDef",
    {
        "DomainName": str,
        "ResourceRecord": AwsCertificateManagerCertificateResourceRecordTypeDef,
        "ValidationDomain": str,
        "ValidationEmails": Sequence[str],
        "ValidationMethod": str,
        "ValidationStatus": str,
    },
    total=False,
)

AwsCloudFrontDistributionCacheBehaviorsTypeDef = TypedDict(
    "AwsCloudFrontDistributionCacheBehaviorsTypeDef",
    {
        "Items": Sequence[AwsCloudFrontDistributionCacheBehaviorTypeDef],
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupFailoverTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupFailoverTypeDef",
    {
        "StatusCodes": AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginItemTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginItemTypeDef",
    {
        "DomainName": str,
        "Id": str,
        "OriginPath": str,
        "S3OriginConfig": AwsCloudFrontDistributionOriginS3OriginConfigTypeDef,
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentTypeDef",
    {
        "Certificate": str,
        "EnvironmentVariables": Sequence[
            AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef
        ],
        "PrivilegedMode": bool,
        "ImagePullCredentialsType": str,
        "RegistryCredential": AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef,
        "Type": str,
    },
    total=False,
)

AwsCodeBuildProjectLogsConfigDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectLogsConfigDetailsTypeDef",
    {
        "CloudWatchLogs": AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef,
        "S3Logs": AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef,
    },
    total=False,
)

AwsDynamoDbTableGlobalSecondaryIndexTypeDef = TypedDict(
    "AwsDynamoDbTableGlobalSecondaryIndexTypeDef",
    {
        "Backfilling": bool,
        "IndexArn": str,
        "IndexName": str,
        "IndexSizeBytes": int,
        "IndexStatus": str,
        "ItemCount": int,
        "KeySchema": Sequence[AwsDynamoDbTableKeySchemaTypeDef],
        "Projection": AwsDynamoDbTableProjectionTypeDef,
        "ProvisionedThroughput": AwsDynamoDbTableProvisionedThroughputTypeDef,
    },
    total=False,
)

AwsDynamoDbTableLocalSecondaryIndexTypeDef = TypedDict(
    "AwsDynamoDbTableLocalSecondaryIndexTypeDef",
    {
        "IndexArn": str,
        "IndexName": str,
        "KeySchema": Sequence[AwsDynamoDbTableKeySchemaTypeDef],
        "Projection": AwsDynamoDbTableProjectionTypeDef,
    },
    total=False,
)

AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef = TypedDict(
    "AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef",
    {
        "IndexName": str,
        "ProvisionedThroughputOverride": AwsDynamoDbTableProvisionedThroughputOverrideTypeDef,
    },
    total=False,
)

AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "Type": str,
        "ImageId": str,
        "IpV4Addresses": Sequence[str],
        "IpV6Addresses": Sequence[str],
        "KeyName": str,
        "IamInstanceProfileArn": str,
        "VpcId": str,
        "SubnetId": str,
        "LaunchedAt": str,
        "NetworkInterfaces": Sequence[AwsEc2InstanceNetworkInterfacesDetailsTypeDef],
    },
    total=False,
)

AwsEc2NetworkAclEntryTypeDef = TypedDict(
    "AwsEc2NetworkAclEntryTypeDef",
    {
        "CidrBlock": str,
        "Egress": bool,
        "IcmpTypeCode": IcmpTypeCodeTypeDef,
        "Ipv6CidrBlock": str,
        "PortRange": PortRangeFromToTypeDef,
        "Protocol": str,
        "RuleAction": str,
        "RuleNumber": int,
    },
    total=False,
)

AwsEc2NetworkInterfaceDetailsTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceDetailsTypeDef",
    {
        "Attachment": AwsEc2NetworkInterfaceAttachmentTypeDef,
        "NetworkInterfaceId": str,
        "SecurityGroups": Sequence[AwsEc2NetworkInterfaceSecurityGroupTypeDef],
        "SourceDestCheck": bool,
        "IpV6Addresses": Sequence[AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef],
        "PrivateIpAddresses": Sequence[AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef],
        "PublicDnsName": str,
        "PublicIp": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpPermissionTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpPermissionTypeDef",
    {
        "IpProtocol": str,
        "FromPort": int,
        "ToPort": int,
        "UserIdGroupPairs": Sequence[AwsEc2SecurityGroupUserIdGroupPairTypeDef],
        "IpRanges": Sequence[AwsEc2SecurityGroupIpRangeTypeDef],
        "Ipv6Ranges": Sequence[AwsEc2SecurityGroupIpv6RangeTypeDef],
        "PrefixListIds": Sequence[AwsEc2SecurityGroupPrefixListIdTypeDef],
    },
    total=False,
)

AwsEc2SubnetDetailsTypeDef = TypedDict(
    "AwsEc2SubnetDetailsTypeDef",
    {
        "AssignIpv6AddressOnCreation": bool,
        "AvailabilityZone": str,
        "AvailabilityZoneId": str,
        "AvailableIpAddressCount": int,
        "CidrBlock": str,
        "DefaultForAz": bool,
        "MapPublicIpOnLaunch": bool,
        "OwnerId": str,
        "State": str,
        "SubnetArn": str,
        "SubnetId": str,
        "VpcId": str,
        "Ipv6CidrBlockAssociationSet": Sequence[Ipv6CidrBlockAssociationTypeDef],
    },
    total=False,
)

AwsEc2VolumeDetailsTypeDef = TypedDict(
    "AwsEc2VolumeDetailsTypeDef",
    {
        "CreateTime": str,
        "Encrypted": bool,
        "Size": int,
        "SnapshotId": str,
        "Status": str,
        "KmsKeyId": str,
        "Attachments": Sequence[AwsEc2VolumeAttachmentTypeDef],
    },
    total=False,
)

AwsEc2VpcDetailsTypeDef = TypedDict(
    "AwsEc2VpcDetailsTypeDef",
    {
        "CidrBlockAssociationSet": Sequence[CidrBlockAssociationTypeDef],
        "Ipv6CidrBlockAssociationSet": Sequence[Ipv6CidrBlockAssociationTypeDef],
        "DhcpOptionsId": str,
        "State": str,
    },
    total=False,
)

AwsEc2VpcEndpointServiceDetailsTypeDef = TypedDict(
    "AwsEc2VpcEndpointServiceDetailsTypeDef",
    {
        "AcceptanceRequired": bool,
        "AvailabilityZones": Sequence[str],
        "BaseEndpointDnsNames": Sequence[str],
        "ManagesVpcEndpoints": bool,
        "GatewayLoadBalancerArns": Sequence[str],
        "NetworkLoadBalancerArns": Sequence[str],
        "PrivateDnsName": str,
        "ServiceId": str,
        "ServiceName": str,
        "ServiceState": str,
        "ServiceType": Sequence[AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef],
    },
    total=False,
)

AwsEc2VpnConnectionOptionsDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionOptionsDetailsTypeDef",
    {
        "StaticRoutesOnly": bool,
        "TunnelOptions": Sequence[AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef],
    },
    total=False,
)

AwsEcrRepositoryDetailsTypeDef = TypedDict(
    "AwsEcrRepositoryDetailsTypeDef",
    {
        "Arn": str,
        "ImageScanningConfiguration": AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef,
        "ImageTagMutability": str,
        "LifecyclePolicy": AwsEcrRepositoryLifecyclePolicyDetailsTypeDef,
        "RepositoryName": str,
        "RepositoryPolicyText": str,
    },
    total=False,
)

AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef",
    {
        "KmsKeyId": str,
        "LogConfiguration": AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef,
        "Logging": str,
    },
    total=False,
)

AwsEcsServiceDeploymentConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsServiceDeploymentConfigurationDetailsTypeDef",
    {
        "DeploymentCircuitBreaker": AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef,
        "MaximumPercent": int,
        "MinimumHealthyPercent": int,
    },
    total=False,
)

AwsEcsServiceNetworkConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsServiceNetworkConfigurationDetailsTypeDef",
    {
        "AwsVpcConfiguration": AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef",
    {
        "Capabilities": AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef,
        "Devices": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef
        ],
        "InitProcessEnabled": bool,
        "MaxSwap": int,
        "SharedMemorySize": int,
        "Swappiness": int,
        "Tmpfs": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef",
    {
        "LogDriver": str,
        "Options": Mapping[str, str],
        "SecretOptions": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef",
    {
        "ContainerName": str,
        "ProxyConfigurationProperties": Sequence[
            AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef
        ],
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef",
    {
        "AuthorizationConfig": AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef,
        "FilesystemId": str,
        "RootDirectory": str,
        "TransitEncryption": str,
        "TransitEncryptionPort": int,
    },
    total=False,
)

AwsEksClusterLoggingDetailsTypeDef = TypedDict(
    "AwsEksClusterLoggingDetailsTypeDef",
    {
        "ClusterLogging": Sequence[AwsEksClusterLoggingClusterLoggingDetailsTypeDef],
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentDetailsTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentDetailsTypeDef",
    {
        "ApplicationName": str,
        "Cname": str,
        "DateCreated": str,
        "DateUpdated": str,
        "Description": str,
        "EndpointUrl": str,
        "EnvironmentArn": str,
        "EnvironmentId": str,
        "EnvironmentLinks": Sequence[AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef],
        "EnvironmentName": str,
        "OptionSettings": Sequence[AwsElasticBeanstalkEnvironmentOptionSettingTypeDef],
        "PlatformArn": str,
        "SolutionStackName": str,
        "Status": str,
        "Tier": AwsElasticBeanstalkEnvironmentTierTypeDef,
        "VersionLabel": str,
    },
    total=False,
)

AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef",
    {
        "DedicatedMasterCount": int,
        "DedicatedMasterEnabled": bool,
        "DedicatedMasterType": str,
        "InstanceCount": int,
        "InstanceType": str,
        "ZoneAwarenessConfig": AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef,
        "ZoneAwarenessEnabled": bool,
    },
    total=False,
)

AwsElasticsearchDomainLogPublishingOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainLogPublishingOptionsTypeDef",
    {
        "IndexSlowLogs": AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef,
        "SearchSlowLogs": AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef,
        "AuditLogs": AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef,
    },
    total=False,
)

AwsElbLoadBalancerPoliciesTypeDef = TypedDict(
    "AwsElbLoadBalancerPoliciesTypeDef",
    {
        "AppCookieStickinessPolicies": Sequence[AwsElbAppCookieStickinessPolicyTypeDef],
        "LbCookieStickinessPolicies": Sequence[AwsElbLbCookieStickinessPolicyTypeDef],
        "OtherPolicies": Sequence[str],
    },
    total=False,
)

AwsElbLoadBalancerAttributesTypeDef = TypedDict(
    "AwsElbLoadBalancerAttributesTypeDef",
    {
        "AccessLog": AwsElbLoadBalancerAccessLogTypeDef,
        "ConnectionDraining": AwsElbLoadBalancerConnectionDrainingTypeDef,
        "ConnectionSettings": AwsElbLoadBalancerConnectionSettingsTypeDef,
        "CrossZoneLoadBalancing": AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef,
        "AdditionalAttributes": Sequence[AwsElbLoadBalancerAdditionalAttributeTypeDef],
    },
    total=False,
)

AwsElbLoadBalancerListenerDescriptionTypeDef = TypedDict(
    "AwsElbLoadBalancerListenerDescriptionTypeDef",
    {
        "Listener": AwsElbLoadBalancerListenerTypeDef,
        "PolicyNames": Sequence[str],
    },
    total=False,
)

AwsElbv2LoadBalancerDetailsTypeDef = TypedDict(
    "AwsElbv2LoadBalancerDetailsTypeDef",
    {
        "AvailabilityZones": Sequence[AvailabilityZoneTypeDef],
        "CanonicalHostedZoneId": str,
        "CreatedTime": str,
        "DNSName": str,
        "IpAddressType": str,
        "Scheme": str,
        "SecurityGroups": Sequence[str],
        "State": LoadBalancerStateTypeDef,
        "Type": str,
        "VpcId": str,
        "LoadBalancerAttributes": Sequence[AwsElbv2LoadBalancerAttributeTypeDef],
    },
    total=False,
)

AwsIamAccessKeySessionContextTypeDef = TypedDict(
    "AwsIamAccessKeySessionContextTypeDef",
    {
        "Attributes": AwsIamAccessKeySessionContextAttributesTypeDef,
        "SessionIssuer": AwsIamAccessKeySessionContextSessionIssuerTypeDef,
    },
    total=False,
)

AwsIamGroupDetailsTypeDef = TypedDict(
    "AwsIamGroupDetailsTypeDef",
    {
        "AttachedManagedPolicies": Sequence[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "GroupId": str,
        "GroupName": str,
        "GroupPolicyList": Sequence[AwsIamGroupPolicyTypeDef],
        "Path": str,
    },
    total=False,
)

AwsIamInstanceProfileTypeDef = TypedDict(
    "AwsIamInstanceProfileTypeDef",
    {
        "Arn": str,
        "CreateDate": str,
        "InstanceProfileId": str,
        "InstanceProfileName": str,
        "Path": str,
        "Roles": Sequence[AwsIamInstanceProfileRoleTypeDef],
    },
    total=False,
)

AwsIamPolicyDetailsTypeDef = TypedDict(
    "AwsIamPolicyDetailsTypeDef",
    {
        "AttachmentCount": int,
        "CreateDate": str,
        "DefaultVersionId": str,
        "Description": str,
        "IsAttachable": bool,
        "Path": str,
        "PermissionsBoundaryUsageCount": int,
        "PolicyId": str,
        "PolicyName": str,
        "PolicyVersionList": Sequence[AwsIamPolicyVersionTypeDef],
        "UpdateDate": str,
    },
    total=False,
)

AwsIamUserDetailsTypeDef = TypedDict(
    "AwsIamUserDetailsTypeDef",
    {
        "AttachedManagedPolicies": Sequence[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "GroupList": Sequence[str],
        "Path": str,
        "PermissionsBoundary": AwsIamPermissionsBoundaryTypeDef,
        "UserId": str,
        "UserName": str,
        "UserPolicyList": Sequence[AwsIamUserPolicyTypeDef],
    },
    total=False,
)

AwsLambdaFunctionEnvironmentTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentTypeDef",
    {
        "Variables": Mapping[str, str],
        "Error": AwsLambdaFunctionEnvironmentErrorTypeDef,
    },
    total=False,
)

AwsNetworkFirewallFirewallDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallDetailsTypeDef",
    {
        "DeleteProtection": bool,
        "Description": str,
        "FirewallArn": str,
        "FirewallId": str,
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "FirewallPolicyChangeProtection": bool,
        "SubnetChangeProtection": bool,
        "SubnetMappings": Sequence[AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef],
        "VpcId": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef",
    {
        "InstanceCount": int,
        "WarmEnabled": bool,
        "WarmCount": int,
        "DedicatedMasterEnabled": bool,
        "ZoneAwarenessConfig": AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef,
        "DedicatedMasterCount": int,
        "InstanceType": str,
        "WarmType": str,
        "ZoneAwarenessEnabled": bool,
        "DedicatedMasterType": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef",
    {
        "IndexSlowLogs": AwsOpenSearchServiceDomainLogPublishingOptionTypeDef,
        "SearchSlowLogs": AwsOpenSearchServiceDomainLogPublishingOptionTypeDef,
        "AuditLogs": AwsOpenSearchServiceDomainLogPublishingOptionTypeDef,
    },
    total=False,
)

AwsRdsDbClusterDetailsTypeDef = TypedDict(
    "AwsRdsDbClusterDetailsTypeDef",
    {
        "AllocatedStorage": int,
        "AvailabilityZones": Sequence[str],
        "BackupRetentionPeriod": int,
        "DatabaseName": str,
        "Status": str,
        "Endpoint": str,
        "ReaderEndpoint": str,
        "CustomEndpoints": Sequence[str],
        "MultiAz": bool,
        "Engine": str,
        "EngineVersion": str,
        "Port": int,
        "MasterUsername": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReadReplicaIdentifiers": Sequence[str],
        "VpcSecurityGroups": Sequence[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
        "HostedZoneId": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterResourceId": str,
        "AssociatedRoles": Sequence[AwsRdsDbClusterAssociatedRoleTypeDef],
        "ClusterCreateTime": str,
        "EnabledCloudWatchLogsExports": Sequence[str],
        "EngineMode": str,
        "DeletionProtection": bool,
        "HttpEndpointEnabled": bool,
        "ActivityStreamStatus": str,
        "CopyTagsToSnapshot": bool,
        "CrossAccountClone": bool,
        "DomainMemberships": Sequence[AwsRdsDbDomainMembershipTypeDef],
        "DbClusterParameterGroup": str,
        "DbSubnetGroup": str,
        "DbClusterOptionGroupMemberships": Sequence[AwsRdsDbClusterOptionGroupMembershipTypeDef],
        "DbClusterIdentifier": str,
        "DbClusterMembers": Sequence[AwsRdsDbClusterMemberTypeDef],
        "IamDatabaseAuthenticationEnabled": bool,
    },
    total=False,
)

AwsRdsDbSnapshotDetailsTypeDef = TypedDict(
    "AwsRdsDbSnapshotDetailsTypeDef",
    {
        "DbSnapshotIdentifier": str,
        "DbInstanceIdentifier": str,
        "SnapshotCreateTime": str,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "InstanceCreateTime": str,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "Iops": int,
        "OptionGroupName": str,
        "PercentProgress": int,
        "SourceRegion": str,
        "SourceDbSnapshotIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "Timezone": str,
        "IamDatabaseAuthenticationEnabled": bool,
        "ProcessorFeatures": Sequence[AwsRdsDbProcessorFeatureTypeDef],
        "DbiResourceId": str,
    },
    total=False,
)

AwsRdsDbPendingModifiedValuesTypeDef = TypedDict(
    "AwsRdsDbPendingModifiedValuesTypeDef",
    {
        "DbInstanceClass": str,
        "AllocatedStorage": int,
        "MasterUserPassword": str,
        "Port": int,
        "BackupRetentionPeriod": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "DbInstanceIdentifier": str,
        "StorageType": str,
        "CaCertificateIdentifier": str,
        "DbSubnetGroupName": str,
        "PendingCloudWatchLogsExports": AwsRdsPendingCloudWatchLogsExportsTypeDef,
        "ProcessorFeatures": Sequence[AwsRdsDbProcessorFeatureTypeDef],
    },
    total=False,
)

AwsRdsDbSecurityGroupDetailsTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupDetailsTypeDef",
    {
        "DbSecurityGroupArn": str,
        "DbSecurityGroupDescription": str,
        "DbSecurityGroupName": str,
        "Ec2SecurityGroups": Sequence[AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef],
        "IpRanges": Sequence[AwsRdsDbSecurityGroupIpRangeTypeDef],
        "OwnerId": str,
        "VpcId": str,
    },
    total=False,
)

AwsRdsDbSubnetGroupSubnetTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupSubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

AwsRedshiftClusterClusterParameterGroupTypeDef = TypedDict(
    "AwsRedshiftClusterClusterParameterGroupTypeDef",
    {
        "ClusterParameterStatusList": Sequence[AwsRedshiftClusterClusterParameterStatusTypeDef],
        "ParameterApplyStatus": str,
        "ParameterGroupName": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef",
    {
        "Prefix": str,
        "Tag": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef",
    {
        "FilterRules": Sequence[AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef],
    },
    total=False,
)

AwsS3BucketServerSideEncryptionRuleTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionRuleTypeDef",
    {
        "ApplyServerSideEncryptionByDefault": AwsS3BucketServerSideEncryptionByDefaultTypeDef,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef",
    {
        "Condition": AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef,
        "Redirect": AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef,
    },
    total=False,
)

AwsSecretsManagerSecretDetailsTypeDef = TypedDict(
    "AwsSecretsManagerSecretDetailsTypeDef",
    {
        "RotationRules": AwsSecretsManagerSecretRotationRulesTypeDef,
        "RotationOccurredWithinFrequency": bool,
        "KmsKeyId": str,
        "RotationEnabled": bool,
        "RotationLambdaArn": str,
        "Deleted": bool,
        "Name": str,
        "Description": str,
    },
    total=False,
)

BatchUpdateFindingsUnprocessedFindingTypeDef = TypedDict(
    "BatchUpdateFindingsUnprocessedFindingTypeDef",
    {
        "FindingIdentifier": AwsSecurityFindingIdentifierTypeDef,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
)

AwsSnsTopicDetailsTypeDef = TypedDict(
    "AwsSnsTopicDetailsTypeDef",
    {
        "KmsMasterKeyId": str,
        "Subscription": Sequence[AwsSnsTopicSubscriptionTypeDef],
        "TopicName": str,
        "Owner": str,
    },
    total=False,
)

AwsSsmPatchTypeDef = TypedDict(
    "AwsSsmPatchTypeDef",
    {
        "ComplianceSummary": AwsSsmComplianceSummaryTypeDef,
    },
    total=False,
)

AwsWafRateBasedRuleDetailsTypeDef = TypedDict(
    "AwsWafRateBasedRuleDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RateKey": str,
        "RateLimit": int,
        "RuleId": str,
        "MatchPredicates": Sequence[AwsWafRateBasedRuleMatchPredicateTypeDef],
    },
    total=False,
)

AwsWafRegionalRateBasedRuleDetailsTypeDef = TypedDict(
    "AwsWafRegionalRateBasedRuleDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RateKey": str,
        "RateLimit": int,
        "RuleId": str,
        "MatchPredicates": Sequence[AwsWafRegionalRateBasedRuleMatchPredicateTypeDef],
    },
    total=False,
)

AwsWafWebAclRuleTypeDef = TypedDict(
    "AwsWafWebAclRuleTypeDef",
    {
        "Action": WafActionTypeDef,
        "ExcludedRules": Sequence[WafExcludedRuleTypeDef],
        "OverrideAction": WafOverrideActionTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

CreateActionTargetResponseTypeDef = TypedDict(
    "CreateActionTargetResponseTypeDef",
    {
        "ActionTargetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFindingAggregatorResponseTypeDef = TypedDict(
    "CreateFindingAggregatorResponseTypeDef",
    {
        "FindingAggregatorArn": str,
        "FindingAggregationRegion": str,
        "RegionLinkingMode": str,
        "Regions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInsightResponseTypeDef = TypedDict(
    "CreateInsightResponseTypeDef",
    {
        "InsightArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteActionTargetResponseTypeDef = TypedDict(
    "DeleteActionTargetResponseTypeDef",
    {
        "ActionTargetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInsightResponseTypeDef = TypedDict(
    "DeleteInsightResponseTypeDef",
    {
        "InsightArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeActionTargetsResponseTypeDef = TypedDict(
    "DescribeActionTargetsResponseTypeDef",
    {
        "ActionTargets": List[ActionTargetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHubResponseTypeDef = TypedDict(
    "DescribeHubResponseTypeDef",
    {
        "HubArn": str,
        "SubscribedAt": str,
        "AutoEnableControls": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "AutoEnable": bool,
        "MemberAccountLimitReached": bool,
        "AutoEnableStandards": AutoEnableStandardsType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableImportFindingsForProductResponseTypeDef = TypedDict(
    "EnableImportFindingsForProductResponseTypeDef",
    {
        "ProductSubscriptionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFindingAggregatorResponseTypeDef = TypedDict(
    "GetFindingAggregatorResponseTypeDef",
    {
        "FindingAggregatorArn": str,
        "FindingAggregationRegion": str,
        "RegionLinkingMode": str,
        "Regions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInvitationsCountResponseTypeDef = TypedDict(
    "GetInvitationsCountResponseTypeDef",
    {
        "InvitationsCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnabledProductsForImportResponseTypeDef = TypedDict(
    "ListEnabledProductsForImportResponseTypeDef",
    {
        "ProductSubscriptions": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOrganizationAdminAccountsResponseTypeDef = TypedDict(
    "ListOrganizationAdminAccountsResponseTypeDef",
    {
        "AdminAccounts": List[AdminAccountTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFindingAggregatorResponseTypeDef = TypedDict(
    "UpdateFindingAggregatorResponseTypeDef",
    {
        "FindingAggregatorArn": str,
        "FindingAggregationRegion": str,
        "RegionLinkingMode": str,
        "Regions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEnableStandardsRequestRequestTypeDef = TypedDict(
    "BatchEnableStandardsRequestRequestTypeDef",
    {
        "StandardsSubscriptionRequests": Sequence[StandardsSubscriptionRequestTypeDef],
    },
)

BatchImportFindingsResponseTypeDef = TypedDict(
    "BatchImportFindingsResponseTypeDef",
    {
        "FailedCount": int,
        "SuccessCount": int,
        "FailedFindings": List[ImportFindingsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchUpdateFindingsRequestRequestTypeDef",
    {
        "FindingIdentifiers": Sequence[AwsSecurityFindingIdentifierTypeDef],
    },
)
_OptionalBatchUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchUpdateFindingsRequestRequestTypeDef",
    {
        "Note": NoteUpdateTypeDef,
        "Severity": SeverityUpdateTypeDef,
        "VerificationState": VerificationStateType,
        "Confidence": int,
        "Criticality": int,
        "Types": Sequence[str],
        "UserDefinedFields": Mapping[str, str],
        "Workflow": WorkflowUpdateTypeDef,
        "RelatedFindings": Sequence[RelatedFindingTypeDef],
    },
    total=False,
)


class BatchUpdateFindingsRequestRequestTypeDef(
    _RequiredBatchUpdateFindingsRequestRequestTypeDef,
    _OptionalBatchUpdateFindingsRequestRequestTypeDef,
):
    pass


ComplianceTypeDef = TypedDict(
    "ComplianceTypeDef",
    {
        "Status": ComplianceStatusType,
        "RelatedRequirements": Sequence[str],
        "StatusReasons": Sequence[StatusReasonTypeDef],
    },
    total=False,
)

CreateMembersResponseTypeDef = TypedDict(
    "CreateMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeclineInvitationsResponseTypeDef = TypedDict(
    "DeclineInvitationsResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInvitationsResponseTypeDef = TypedDict(
    "DeleteInvitationsResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMembersResponseTypeDef = TypedDict(
    "DeleteMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InviteMembersResponseTypeDef = TypedDict(
    "InviteMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef",
    {
        "Start": str,
        "End": str,
        "DateRange": DateRangeTypeDef,
    },
    total=False,
)

DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef = TypedDict(
    "DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef",
    {
        "ActionTargetArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeProductsRequestDescribeProductsPaginateTypeDef = TypedDict(
    "DescribeProductsRequestDescribeProductsPaginateTypeDef",
    {
        "ProductArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef = TypedDict(
    "_RequiredDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef",
    {
        "StandardsSubscriptionArn": str,
    },
)
_OptionalDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef = TypedDict(
    "_OptionalDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef(
    _RequiredDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef,
    _OptionalDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef,
):
    pass


DescribeStandardsRequestDescribeStandardsPaginateTypeDef = TypedDict(
    "DescribeStandardsRequestDescribeStandardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef = TypedDict(
    "GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef",
    {
        "StandardsSubscriptionArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetInsightsRequestGetInsightsPaginateTypeDef = TypedDict(
    "GetInsightsRequestGetInsightsPaginateTypeDef",
    {
        "InsightArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef = TypedDict(
    "ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef = TypedDict(
    "ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListInvitationsRequestListInvitationsPaginateTypeDef = TypedDict(
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "ListMembersRequestListMembersPaginateTypeDef",
    {
        "OnlyAssociated": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeProductsResponseTypeDef = TypedDict(
    "DescribeProductsResponseTypeDef",
    {
        "Products": List[ProductTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStandardsControlsResponseTypeDef = TypedDict(
    "DescribeStandardsControlsResponseTypeDef",
    {
        "Controls": List[StandardsControlTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStandardsResponseTypeDef = TypedDict(
    "DescribeStandardsResponseTypeDef",
    {
        "Standards": List[StandardTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingAggregatorsResponseTypeDef = TypedDict(
    "ListFindingAggregatorsResponseTypeDef",
    {
        "FindingAggregators": List[FindingAggregatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FindingProviderFieldsTypeDef = TypedDict(
    "FindingProviderFieldsTypeDef",
    {
        "Confidence": int,
        "Criticality": int,
        "RelatedFindings": Sequence[RelatedFindingTypeDef],
        "Severity": FindingProviderSeverityTypeDef,
        "Types": Sequence[str],
    },
    total=False,
)

GetAdministratorAccountResponseTypeDef = TypedDict(
    "GetAdministratorAccountResponseTypeDef",
    {
        "Administrator": InvitationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMasterAccountResponseTypeDef = TypedDict(
    "GetMasterAccountResponseTypeDef",
    {
        "Master": InvitationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInvitationsResponseTypeDef = TypedDict(
    "ListInvitationsResponseTypeDef",
    {
        "Invitations": List[InvitationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMembersResponseTypeDef = TypedDict(
    "GetMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InsightResultsTypeDef = TypedDict(
    "InsightResultsTypeDef",
    {
        "InsightArn": str,
        "GroupByAttribute": str,
        "ResultValues": List[InsightResultValueTypeDef],
    },
)

NetworkPathComponentDetailsTypeDef = TypedDict(
    "NetworkPathComponentDetailsTypeDef",
    {
        "Address": Sequence[str],
        "PortRanges": Sequence[PortRangeTypeDef],
    },
    total=False,
)

NetworkTypeDef = TypedDict(
    "NetworkTypeDef",
    {
        "Direction": NetworkDirectionType,
        "Protocol": str,
        "OpenPortRange": PortRangeTypeDef,
        "SourceIpV4": str,
        "SourceIpV6": str,
        "SourcePort": int,
        "SourceDomain": str,
        "SourceMac": str,
        "DestinationIpV4": str,
        "DestinationIpV6": str,
        "DestinationPort": int,
        "DestinationDomain": str,
    },
    total=False,
)

PageTypeDef = TypedDict(
    "PageTypeDef",
    {
        "PageNumber": int,
        "LineRange": RangeTypeDef,
        "OffsetRange": RangeTypeDef,
    },
    total=False,
)

RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "Recommendation": RecommendationTypeDef,
    },
    total=False,
)

RuleGroupSourceStatefulRulesDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesDetailsTypeDef",
    {
        "Action": str,
        "Header": RuleGroupSourceStatefulRulesHeaderDetailsTypeDef,
        "RuleOptions": Sequence[RuleGroupSourceStatefulRulesOptionsDetailsTypeDef],
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesTypeDef",
    {
        "DestinationPorts": Sequence[
            RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef
        ],
        "Destinations": Sequence[RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef],
        "Protocols": Sequence[int],
        "SourcePorts": Sequence[RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef],
        "Sources": Sequence[RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef],
        "TcpFlags": Sequence[RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef],
    },
    total=False,
)

RuleGroupVariablesTypeDef = TypedDict(
    "RuleGroupVariablesTypeDef",
    {
        "IpSets": RuleGroupVariablesIpSetsDetailsTypeDef,
        "PortSets": RuleGroupVariablesPortSetsDetailsTypeDef,
    },
    total=False,
)

_RequiredStandardsSubscriptionTypeDef = TypedDict(
    "_RequiredStandardsSubscriptionTypeDef",
    {
        "StandardsSubscriptionArn": str,
        "StandardsArn": str,
        "StandardsInput": Dict[str, str],
        "StandardsStatus": StandardsStatusType,
    },
)
_OptionalStandardsSubscriptionTypeDef = TypedDict(
    "_OptionalStandardsSubscriptionTypeDef",
    {
        "StandardsStatusReason": StandardsStatusReasonTypeDef,
    },
    total=False,
)


class StandardsSubscriptionTypeDef(
    _RequiredStandardsSubscriptionTypeDef, _OptionalStandardsSubscriptionTypeDef
):
    pass


StatelessCustomPublishMetricActionTypeDef = TypedDict(
    "StatelessCustomPublishMetricActionTypeDef",
    {
        "Dimensions": Sequence[StatelessCustomPublishMetricActionDimensionTypeDef],
    },
    total=False,
)

AwsApiCallActionTypeDef = TypedDict(
    "AwsApiCallActionTypeDef",
    {
        "Api": str,
        "ServiceName": str,
        "CallerType": str,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
        "DomainDetails": AwsApiCallActionDomainDetailsTypeDef,
        "AffectedResources": Mapping[str, str],
        "FirstSeen": str,
        "LastSeen": str,
    },
    total=False,
)

NetworkConnectionActionTypeDef = TypedDict(
    "NetworkConnectionActionTypeDef",
    {
        "ConnectionDirection": str,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
        "RemotePortDetails": ActionRemotePortDetailsTypeDef,
        "LocalPortDetails": ActionLocalPortDetailsTypeDef,
        "Protocol": str,
        "Blocked": bool,
    },
    total=False,
)

PortProbeDetailTypeDef = TypedDict(
    "PortProbeDetailTypeDef",
    {
        "LocalPortDetails": ActionLocalPortDetailsTypeDef,
        "LocalIpDetails": ActionLocalIpDetailsTypeDef,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
    },
    total=False,
)

_RequiredVulnerabilityTypeDef = TypedDict(
    "_RequiredVulnerabilityTypeDef",
    {
        "Id": str,
    },
)
_OptionalVulnerabilityTypeDef = TypedDict(
    "_OptionalVulnerabilityTypeDef",
    {
        "VulnerablePackages": Sequence[SoftwarePackageTypeDef],
        "Cvss": Sequence[CvssTypeDef],
        "RelatedVulnerabilities": Sequence[str],
        "Vendor": VulnerabilityVendorTypeDef,
        "ReferenceUrls": Sequence[str],
    },
    total=False,
)


class VulnerabilityTypeDef(_RequiredVulnerabilityTypeDef, _OptionalVulnerabilityTypeDef):
    pass


AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef",
    {
        "InstancesDistribution": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef,
        "LaunchTemplate": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationDetailsTypeDef",
    {
        "AssociatePublicIpAddress": bool,
        "BlockDeviceMappings": Sequence[
            AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef
        ],
        "ClassicLinkVpcId": str,
        "ClassicLinkVpcSecurityGroups": Sequence[str],
        "CreatedTime": str,
        "EbsOptimized": bool,
        "IamInstanceProfile": str,
        "ImageId": str,
        "InstanceMonitoring": AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef,
        "InstanceType": str,
        "KernelId": str,
        "KeyName": str,
        "LaunchConfigurationName": str,
        "PlacementTenancy": str,
        "RamdiskId": str,
        "SecurityGroups": Sequence[str],
        "SpotPrice": str,
        "UserData": str,
        "MetadataOptions": AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef,
    },
    total=False,
)

AwsCertificateManagerCertificateRenewalSummaryTypeDef = TypedDict(
    "AwsCertificateManagerCertificateRenewalSummaryTypeDef",
    {
        "DomainValidationOptions": Sequence[
            AwsCertificateManagerCertificateDomainValidationOptionTypeDef
        ],
        "RenewalStatus": str,
        "RenewalStatusReason": str,
        "UpdatedAt": str,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupTypeDef",
    {
        "FailoverCriteria": AwsCloudFrontDistributionOriginGroupFailoverTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginsTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginsTypeDef",
    {
        "Items": Sequence[AwsCloudFrontDistributionOriginItemTypeDef],
    },
    total=False,
)

AwsCodeBuildProjectDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectDetailsTypeDef",
    {
        "EncryptionKey": str,
        "Artifacts": Sequence[AwsCodeBuildProjectArtifactsDetailsTypeDef],
        "Environment": AwsCodeBuildProjectEnvironmentTypeDef,
        "Name": str,
        "Source": AwsCodeBuildProjectSourceTypeDef,
        "ServiceRole": str,
        "LogsConfig": AwsCodeBuildProjectLogsConfigDetailsTypeDef,
        "VpcConfig": AwsCodeBuildProjectVpcConfigTypeDef,
        "SecondaryArtifacts": Sequence[AwsCodeBuildProjectArtifactsDetailsTypeDef],
    },
    total=False,
)

AwsDynamoDbTableReplicaTypeDef = TypedDict(
    "AwsDynamoDbTableReplicaTypeDef",
    {
        "GlobalSecondaryIndexes": Sequence[AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef],
        "KmsMasterKeyId": str,
        "ProvisionedThroughputOverride": AwsDynamoDbTableProvisionedThroughputOverrideTypeDef,
        "RegionName": str,
        "ReplicaStatus": str,
        "ReplicaStatusDescription": str,
    },
    total=False,
)

AwsEc2NetworkAclDetailsTypeDef = TypedDict(
    "AwsEc2NetworkAclDetailsTypeDef",
    {
        "IsDefault": bool,
        "NetworkAclId": str,
        "OwnerId": str,
        "VpcId": str,
        "Associations": Sequence[AwsEc2NetworkAclAssociationTypeDef],
        "Entries": Sequence[AwsEc2NetworkAclEntryTypeDef],
    },
    total=False,
)

AwsEc2SecurityGroupDetailsTypeDef = TypedDict(
    "AwsEc2SecurityGroupDetailsTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
        "OwnerId": str,
        "VpcId": str,
        "IpPermissions": Sequence[AwsEc2SecurityGroupIpPermissionTypeDef],
        "IpPermissionsEgress": Sequence[AwsEc2SecurityGroupIpPermissionTypeDef],
    },
    total=False,
)

AwsEc2VpnConnectionDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionDetailsTypeDef",
    {
        "VpnConnectionId": str,
        "State": str,
        "CustomerGatewayId": str,
        "CustomerGatewayConfiguration": str,
        "Type": str,
        "VpnGatewayId": str,
        "Category": str,
        "VgwTelemetry": Sequence[AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef],
        "Options": AwsEc2VpnConnectionOptionsDetailsTypeDef,
        "Routes": Sequence[AwsEc2VpnConnectionRoutesDetailsTypeDef],
        "TransitGatewayId": str,
    },
    total=False,
)

AwsEcsClusterConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsClusterConfigurationDetailsTypeDef",
    {
        "ExecuteCommandConfiguration": AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef,
    },
    total=False,
)

AwsEcsServiceDetailsTypeDef = TypedDict(
    "AwsEcsServiceDetailsTypeDef",
    {
        "CapacityProviderStrategy": Sequence[AwsEcsServiceCapacityProviderStrategyDetailsTypeDef],
        "Cluster": str,
        "DeploymentConfiguration": AwsEcsServiceDeploymentConfigurationDetailsTypeDef,
        "DeploymentController": AwsEcsServiceDeploymentControllerDetailsTypeDef,
        "DesiredCount": int,
        "EnableEcsManagedTags": bool,
        "EnableExecuteCommand": bool,
        "HealthCheckGracePeriodSeconds": int,
        "LaunchType": str,
        "LoadBalancers": Sequence[AwsEcsServiceLoadBalancersDetailsTypeDef],
        "Name": str,
        "NetworkConfiguration": AwsEcsServiceNetworkConfigurationDetailsTypeDef,
        "PlacementConstraints": Sequence[AwsEcsServicePlacementConstraintsDetailsTypeDef],
        "PlacementStrategies": Sequence[AwsEcsServicePlacementStrategiesDetailsTypeDef],
        "PlatformVersion": str,
        "PropagateTags": str,
        "Role": str,
        "SchedulingStrategy": str,
        "ServiceArn": str,
        "ServiceName": str,
        "ServiceRegistries": Sequence[AwsEcsServiceServiceRegistriesDetailsTypeDef],
        "TaskDefinition": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef",
    {
        "Command": Sequence[str],
        "Cpu": int,
        "DependsOn": Sequence[AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef],
        "DisableNetworking": bool,
        "DnsSearchDomains": Sequence[str],
        "DnsServers": Sequence[str],
        "DockerLabels": Mapping[str, str],
        "DockerSecurityOptions": Sequence[str],
        "EntryPoint": Sequence[str],
        "Environment": Sequence[AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef],
        "EnvironmentFiles": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef
        ],
        "Essential": bool,
        "ExtraHosts": Sequence[AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef],
        "FirelensConfiguration": AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef,
        "HealthCheck": AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef,
        "Hostname": str,
        "Image": str,
        "Interactive": bool,
        "Links": Sequence[str],
        "LinuxParameters": AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef,
        "LogConfiguration": AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef,
        "Memory": int,
        "MemoryReservation": int,
        "MountPoints": Sequence[AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef],
        "Name": str,
        "PortMappings": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef
        ],
        "Privileged": bool,
        "PseudoTerminal": bool,
        "ReadonlyRootFilesystem": bool,
        "RepositoryCredentials": AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef,
        "ResourceRequirements": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef
        ],
        "Secrets": Sequence[AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef],
        "StartTimeout": int,
        "StopTimeout": int,
        "SystemControls": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef
        ],
        "Ulimits": Sequence[AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef],
        "User": str,
        "VolumesFrom": Sequence[AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef],
        "WorkingDirectory": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesDetailsTypeDef",
    {
        "DockerVolumeConfiguration": AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef,
        "EfsVolumeConfiguration": AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef,
        "Host": AwsEcsTaskDefinitionVolumesHostDetailsTypeDef,
        "Name": str,
    },
    total=False,
)

AwsEksClusterDetailsTypeDef = TypedDict(
    "AwsEksClusterDetailsTypeDef",
    {
        "Arn": str,
        "CertificateAuthorityData": str,
        "ClusterStatus": str,
        "Endpoint": str,
        "Name": str,
        "ResourcesVpcConfig": AwsEksClusterResourcesVpcConfigDetailsTypeDef,
        "RoleArn": str,
        "Version": str,
        "Logging": AwsEksClusterLoggingDetailsTypeDef,
    },
    total=False,
)

AwsElasticsearchDomainDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainDetailsTypeDef",
    {
        "AccessPolicies": str,
        "DomainEndpointOptions": AwsElasticsearchDomainDomainEndpointOptionsTypeDef,
        "DomainId": str,
        "DomainName": str,
        "Endpoint": str,
        "Endpoints": Mapping[str, str],
        "ElasticsearchVersion": str,
        "ElasticsearchClusterConfig": AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef,
        "EncryptionAtRestOptions": AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef,
        "LogPublishingOptions": AwsElasticsearchDomainLogPublishingOptionsTypeDef,
        "NodeToNodeEncryptionOptions": AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef,
        "ServiceSoftwareOptions": AwsElasticsearchDomainServiceSoftwareOptionsTypeDef,
        "VPCOptions": AwsElasticsearchDomainVPCOptionsTypeDef,
    },
    total=False,
)

AwsElbLoadBalancerDetailsTypeDef = TypedDict(
    "AwsElbLoadBalancerDetailsTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "BackendServerDescriptions": Sequence[AwsElbLoadBalancerBackendServerDescriptionTypeDef],
        "CanonicalHostedZoneName": str,
        "CanonicalHostedZoneNameID": str,
        "CreatedTime": str,
        "DnsName": str,
        "HealthCheck": AwsElbLoadBalancerHealthCheckTypeDef,
        "Instances": Sequence[AwsElbLoadBalancerInstanceTypeDef],
        "ListenerDescriptions": Sequence[AwsElbLoadBalancerListenerDescriptionTypeDef],
        "LoadBalancerAttributes": AwsElbLoadBalancerAttributesTypeDef,
        "LoadBalancerName": str,
        "Policies": AwsElbLoadBalancerPoliciesTypeDef,
        "Scheme": str,
        "SecurityGroups": Sequence[str],
        "SourceSecurityGroup": AwsElbLoadBalancerSourceSecurityGroupTypeDef,
        "Subnets": Sequence[str],
        "VpcId": str,
    },
    total=False,
)

AwsIamAccessKeyDetailsTypeDef = TypedDict(
    "AwsIamAccessKeyDetailsTypeDef",
    {
        "UserName": str,
        "Status": AwsIamAccessKeyStatusType,
        "CreatedAt": str,
        "PrincipalId": str,
        "PrincipalType": str,
        "PrincipalName": str,
        "AccountId": str,
        "AccessKeyId": str,
        "SessionContext": AwsIamAccessKeySessionContextTypeDef,
    },
    total=False,
)

AwsIamRoleDetailsTypeDef = TypedDict(
    "AwsIamRoleDetailsTypeDef",
    {
        "AssumeRolePolicyDocument": str,
        "AttachedManagedPolicies": Sequence[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "InstanceProfileList": Sequence[AwsIamInstanceProfileTypeDef],
        "PermissionsBoundary": AwsIamPermissionsBoundaryTypeDef,
        "RoleId": str,
        "RoleName": str,
        "RolePolicyList": Sequence[AwsIamRolePolicyTypeDef],
        "MaxSessionDuration": int,
        "Path": str,
    },
    total=False,
)

AwsLambdaFunctionDetailsTypeDef = TypedDict(
    "AwsLambdaFunctionDetailsTypeDef",
    {
        "Code": AwsLambdaFunctionCodeTypeDef,
        "CodeSha256": str,
        "DeadLetterConfig": AwsLambdaFunctionDeadLetterConfigTypeDef,
        "Environment": AwsLambdaFunctionEnvironmentTypeDef,
        "FunctionName": str,
        "Handler": str,
        "KmsKeyArn": str,
        "LastModified": str,
        "Layers": Sequence[AwsLambdaFunctionLayerTypeDef],
        "MasterArn": str,
        "MemorySize": int,
        "RevisionId": str,
        "Role": str,
        "Runtime": str,
        "Timeout": int,
        "TracingConfig": AwsLambdaFunctionTracingConfigTypeDef,
        "VpcConfig": AwsLambdaFunctionVpcConfigTypeDef,
        "Version": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainDetailsTypeDef",
    {
        "Arn": str,
        "AccessPolicies": str,
        "DomainName": str,
        "Id": str,
        "DomainEndpoint": str,
        "EngineVersion": str,
        "EncryptionAtRestOptions": AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef,
        "NodeToNodeEncryptionOptions": AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef,
        "ServiceSoftwareOptions": AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef,
        "ClusterConfig": AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef,
        "DomainEndpointOptions": AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef,
        "VpcOptions": AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef,
        "LogPublishingOptions": AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef,
        "DomainEndpoints": Mapping[str, str],
    },
    total=False,
)

AwsRdsDbSubnetGroupTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupTypeDef",
    {
        "DbSubnetGroupName": str,
        "DbSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": Sequence[AwsRdsDbSubnetGroupSubnetTypeDef],
        "DbSubnetGroupArn": str,
    },
    total=False,
)

AwsRedshiftClusterDetailsTypeDef = TypedDict(
    "AwsRedshiftClusterDetailsTypeDef",
    {
        "AllowVersionUpgrade": bool,
        "AutomatedSnapshotRetentionPeriod": int,
        "AvailabilityZone": str,
        "ClusterAvailabilityStatus": str,
        "ClusterCreateTime": str,
        "ClusterIdentifier": str,
        "ClusterNodes": Sequence[AwsRedshiftClusterClusterNodeTypeDef],
        "ClusterParameterGroups": Sequence[AwsRedshiftClusterClusterParameterGroupTypeDef],
        "ClusterPublicKey": str,
        "ClusterRevisionNumber": str,
        "ClusterSecurityGroups": Sequence[AwsRedshiftClusterClusterSecurityGroupTypeDef],
        "ClusterSnapshotCopyStatus": AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef,
        "ClusterStatus": str,
        "ClusterSubnetGroupName": str,
        "ClusterVersion": str,
        "DBName": str,
        "DeferredMaintenanceWindows": Sequence[AwsRedshiftClusterDeferredMaintenanceWindowTypeDef],
        "ElasticIpStatus": AwsRedshiftClusterElasticIpStatusTypeDef,
        "ElasticResizeNumberOfNodeOptions": str,
        "Encrypted": bool,
        "Endpoint": AwsRedshiftClusterEndpointTypeDef,
        "EnhancedVpcRouting": bool,
        "ExpectedNextSnapshotScheduleTime": str,
        "ExpectedNextSnapshotScheduleTimeStatus": str,
        "HsmStatus": AwsRedshiftClusterHsmStatusTypeDef,
        "IamRoles": Sequence[AwsRedshiftClusterIamRoleTypeDef],
        "KmsKeyId": str,
        "MaintenanceTrackName": str,
        "ManualSnapshotRetentionPeriod": int,
        "MasterUsername": str,
        "NextMaintenanceWindowStartTime": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "PendingActions": Sequence[str],
        "PendingModifiedValues": AwsRedshiftClusterPendingModifiedValuesTypeDef,
        "PreferredMaintenanceWindow": str,
        "PubliclyAccessible": bool,
        "ResizeInfo": AwsRedshiftClusterResizeInfoTypeDef,
        "RestoreStatus": AwsRedshiftClusterRestoreStatusTypeDef,
        "SnapshotScheduleIdentifier": str,
        "SnapshotScheduleState": str,
        "VpcId": str,
        "VpcSecurityGroups": Sequence[AwsRedshiftClusterVpcSecurityGroupTypeDef],
        "LoggingStatus": AwsRedshiftClusterLoggingStatusTypeDef,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef",
    {
        "Operands": Sequence[
            AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef
        ],
        "Prefix": str,
        "Tag": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationFilterTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationFilterTypeDef",
    {
        "S3KeyFilter": AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef,
    },
    total=False,
)

AwsS3BucketServerSideEncryptionConfigurationTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionConfigurationTypeDef",
    {
        "Rules": Sequence[AwsS3BucketServerSideEncryptionRuleTypeDef],
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationTypeDef",
    {
        "ErrorDocument": str,
        "IndexDocumentSuffix": str,
        "RedirectAllRequestsTo": AwsS3BucketWebsiteConfigurationRedirectToTypeDef,
        "RoutingRules": Sequence[AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef],
    },
    total=False,
)

BatchUpdateFindingsResponseTypeDef = TypedDict(
    "BatchUpdateFindingsResponseTypeDef",
    {
        "ProcessedFindings": List[AwsSecurityFindingIdentifierTypeDef],
        "UnprocessedFindings": List[BatchUpdateFindingsUnprocessedFindingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AwsSsmPatchComplianceDetailsTypeDef = TypedDict(
    "AwsSsmPatchComplianceDetailsTypeDef",
    {
        "Patch": AwsSsmPatchTypeDef,
    },
    total=False,
)

AwsWafWebAclDetailsTypeDef = TypedDict(
    "AwsWafWebAclDetailsTypeDef",
    {
        "Name": str,
        "DefaultAction": str,
        "Rules": Sequence[AwsWafWebAclRuleTypeDef],
        "WebAclId": str,
    },
    total=False,
)

AwsSecurityFindingFiltersTypeDef = TypedDict(
    "AwsSecurityFindingFiltersTypeDef",
    {
        "ProductArn": Sequence[StringFilterTypeDef],
        "AwsAccountId": Sequence[StringFilterTypeDef],
        "Id": Sequence[StringFilterTypeDef],
        "GeneratorId": Sequence[StringFilterTypeDef],
        "Region": Sequence[StringFilterTypeDef],
        "Type": Sequence[StringFilterTypeDef],
        "FirstObservedAt": Sequence[DateFilterTypeDef],
        "LastObservedAt": Sequence[DateFilterTypeDef],
        "CreatedAt": Sequence[DateFilterTypeDef],
        "UpdatedAt": Sequence[DateFilterTypeDef],
        "SeverityProduct": Sequence[NumberFilterTypeDef],
        "SeverityNormalized": Sequence[NumberFilterTypeDef],
        "SeverityLabel": Sequence[StringFilterTypeDef],
        "Confidence": Sequence[NumberFilterTypeDef],
        "Criticality": Sequence[NumberFilterTypeDef],
        "Title": Sequence[StringFilterTypeDef],
        "Description": Sequence[StringFilterTypeDef],
        "RecommendationText": Sequence[StringFilterTypeDef],
        "SourceUrl": Sequence[StringFilterTypeDef],
        "ProductFields": Sequence[MapFilterTypeDef],
        "ProductName": Sequence[StringFilterTypeDef],
        "CompanyName": Sequence[StringFilterTypeDef],
        "UserDefinedFields": Sequence[MapFilterTypeDef],
        "MalwareName": Sequence[StringFilterTypeDef],
        "MalwareType": Sequence[StringFilterTypeDef],
        "MalwarePath": Sequence[StringFilterTypeDef],
        "MalwareState": Sequence[StringFilterTypeDef],
        "NetworkDirection": Sequence[StringFilterTypeDef],
        "NetworkProtocol": Sequence[StringFilterTypeDef],
        "NetworkSourceIpV4": Sequence[IpFilterTypeDef],
        "NetworkSourceIpV6": Sequence[IpFilterTypeDef],
        "NetworkSourcePort": Sequence[NumberFilterTypeDef],
        "NetworkSourceDomain": Sequence[StringFilterTypeDef],
        "NetworkSourceMac": Sequence[StringFilterTypeDef],
        "NetworkDestinationIpV4": Sequence[IpFilterTypeDef],
        "NetworkDestinationIpV6": Sequence[IpFilterTypeDef],
        "NetworkDestinationPort": Sequence[NumberFilterTypeDef],
        "NetworkDestinationDomain": Sequence[StringFilterTypeDef],
        "ProcessName": Sequence[StringFilterTypeDef],
        "ProcessPath": Sequence[StringFilterTypeDef],
        "ProcessPid": Sequence[NumberFilterTypeDef],
        "ProcessParentPid": Sequence[NumberFilterTypeDef],
        "ProcessLaunchedAt": Sequence[DateFilterTypeDef],
        "ProcessTerminatedAt": Sequence[DateFilterTypeDef],
        "ThreatIntelIndicatorType": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorValue": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorCategory": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorLastObservedAt": Sequence[DateFilterTypeDef],
        "ThreatIntelIndicatorSource": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorSourceUrl": Sequence[StringFilterTypeDef],
        "ResourceType": Sequence[StringFilterTypeDef],
        "ResourceId": Sequence[StringFilterTypeDef],
        "ResourcePartition": Sequence[StringFilterTypeDef],
        "ResourceRegion": Sequence[StringFilterTypeDef],
        "ResourceTags": Sequence[MapFilterTypeDef],
        "ResourceAwsEc2InstanceType": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceImageId": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceIpV4Addresses": Sequence[IpFilterTypeDef],
        "ResourceAwsEc2InstanceIpV6Addresses": Sequence[IpFilterTypeDef],
        "ResourceAwsEc2InstanceKeyName": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceIamInstanceProfileArn": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceVpcId": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceSubnetId": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceLaunchedAt": Sequence[DateFilterTypeDef],
        "ResourceAwsS3BucketOwnerId": Sequence[StringFilterTypeDef],
        "ResourceAwsS3BucketOwnerName": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyUserName": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyPrincipalName": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyStatus": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyCreatedAt": Sequence[DateFilterTypeDef],
        "ResourceAwsIamUserUserName": Sequence[StringFilterTypeDef],
        "ResourceContainerName": Sequence[StringFilterTypeDef],
        "ResourceContainerImageId": Sequence[StringFilterTypeDef],
        "ResourceContainerImageName": Sequence[StringFilterTypeDef],
        "ResourceContainerLaunchedAt": Sequence[DateFilterTypeDef],
        "ResourceDetailsOther": Sequence[MapFilterTypeDef],
        "ComplianceStatus": Sequence[StringFilterTypeDef],
        "VerificationState": Sequence[StringFilterTypeDef],
        "WorkflowState": Sequence[StringFilterTypeDef],
        "WorkflowStatus": Sequence[StringFilterTypeDef],
        "RecordState": Sequence[StringFilterTypeDef],
        "RelatedFindingsProductArn": Sequence[StringFilterTypeDef],
        "RelatedFindingsId": Sequence[StringFilterTypeDef],
        "NoteText": Sequence[StringFilterTypeDef],
        "NoteUpdatedAt": Sequence[DateFilterTypeDef],
        "NoteUpdatedBy": Sequence[StringFilterTypeDef],
        "Keyword": Sequence[KeywordFilterTypeDef],
        "FindingProviderFieldsConfidence": Sequence[NumberFilterTypeDef],
        "FindingProviderFieldsCriticality": Sequence[NumberFilterTypeDef],
        "FindingProviderFieldsRelatedFindingsId": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsRelatedFindingsProductArn": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsSeverityLabel": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsSeverityOriginal": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsTypes": Sequence[StringFilterTypeDef],
        "Sample": Sequence[BooleanFilterTypeDef],
    },
    total=False,
)

GetInsightResultsResponseTypeDef = TypedDict(
    "GetInsightResultsResponseTypeDef",
    {
        "InsightResults": InsightResultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkHeaderTypeDef = TypedDict(
    "NetworkHeaderTypeDef",
    {
        "Protocol": str,
        "Destination": NetworkPathComponentDetailsTypeDef,
        "Source": NetworkPathComponentDetailsTypeDef,
    },
    total=False,
)

OccurrencesTypeDef = TypedDict(
    "OccurrencesTypeDef",
    {
        "LineRanges": Sequence[RangeTypeDef],
        "OffsetRanges": Sequence[RangeTypeDef],
        "Pages": Sequence[PageTypeDef],
        "Records": Sequence[RecordTypeDef],
        "Cells": Sequence[CellTypeDef],
    },
    total=False,
)

RuleGroupSourceStatelessRuleDefinitionTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleDefinitionTypeDef",
    {
        "Actions": Sequence[str],
        "MatchAttributes": RuleGroupSourceStatelessRuleMatchAttributesTypeDef,
    },
    total=False,
)

BatchDisableStandardsResponseTypeDef = TypedDict(
    "BatchDisableStandardsResponseTypeDef",
    {
        "StandardsSubscriptions": List[StandardsSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEnableStandardsResponseTypeDef = TypedDict(
    "BatchEnableStandardsResponseTypeDef",
    {
        "StandardsSubscriptions": List[StandardsSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnabledStandardsResponseTypeDef = TypedDict(
    "GetEnabledStandardsResponseTypeDef",
    {
        "StandardsSubscriptions": List[StandardsSubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StatelessCustomActionDefinitionTypeDef = TypedDict(
    "StatelessCustomActionDefinitionTypeDef",
    {
        "PublishMetricAction": StatelessCustomPublishMetricActionTypeDef,
    },
    total=False,
)

PortProbeActionTypeDef = TypedDict(
    "PortProbeActionTypeDef",
    {
        "PortProbeDetails": Sequence[PortProbeDetailTypeDef],
        "Blocked": bool,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupDetailsTypeDef",
    {
        "LaunchConfigurationName": str,
        "LoadBalancerNames": Sequence[str],
        "HealthCheckType": str,
        "HealthCheckGracePeriod": int,
        "CreatedTime": str,
        "MixedInstancesPolicy": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef,
        "AvailabilityZones": Sequence[
            AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef
        ],
        "LaunchTemplate": AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef,
        "CapacityRebalance": bool,
    },
    total=False,
)

AwsCertificateManagerCertificateDetailsTypeDef = TypedDict(
    "AwsCertificateManagerCertificateDetailsTypeDef",
    {
        "CertificateAuthorityArn": str,
        "CreatedAt": str,
        "DomainName": str,
        "DomainValidationOptions": Sequence[
            AwsCertificateManagerCertificateDomainValidationOptionTypeDef
        ],
        "ExtendedKeyUsages": Sequence[AwsCertificateManagerCertificateExtendedKeyUsageTypeDef],
        "FailureReason": str,
        "ImportedAt": str,
        "InUseBy": Sequence[str],
        "IssuedAt": str,
        "Issuer": str,
        "KeyAlgorithm": str,
        "KeyUsages": Sequence[AwsCertificateManagerCertificateKeyUsageTypeDef],
        "NotAfter": str,
        "NotBefore": str,
        "Options": AwsCertificateManagerCertificateOptionsTypeDef,
        "RenewalEligibility": str,
        "RenewalSummary": AwsCertificateManagerCertificateRenewalSummaryTypeDef,
        "Serial": str,
        "SignatureAlgorithm": str,
        "Status": str,
        "Subject": str,
        "SubjectAlternativeNames": Sequence[str],
        "Type": str,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupsTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupsTypeDef",
    {
        "Items": Sequence[AwsCloudFrontDistributionOriginGroupTypeDef],
    },
    total=False,
)

AwsDynamoDbTableDetailsTypeDef = TypedDict(
    "AwsDynamoDbTableDetailsTypeDef",
    {
        "AttributeDefinitions": Sequence[AwsDynamoDbTableAttributeDefinitionTypeDef],
        "BillingModeSummary": AwsDynamoDbTableBillingModeSummaryTypeDef,
        "CreationDateTime": str,
        "GlobalSecondaryIndexes": Sequence[AwsDynamoDbTableGlobalSecondaryIndexTypeDef],
        "GlobalTableVersion": str,
        "ItemCount": int,
        "KeySchema": Sequence[AwsDynamoDbTableKeySchemaTypeDef],
        "LatestStreamArn": str,
        "LatestStreamLabel": str,
        "LocalSecondaryIndexes": Sequence[AwsDynamoDbTableLocalSecondaryIndexTypeDef],
        "ProvisionedThroughput": AwsDynamoDbTableProvisionedThroughputTypeDef,
        "Replicas": Sequence[AwsDynamoDbTableReplicaTypeDef],
        "RestoreSummary": AwsDynamoDbTableRestoreSummaryTypeDef,
        "SseDescription": AwsDynamoDbTableSseDescriptionTypeDef,
        "StreamSpecification": AwsDynamoDbTableStreamSpecificationTypeDef,
        "TableId": str,
        "TableName": str,
        "TableSizeBytes": int,
        "TableStatus": str,
    },
    total=False,
)

AwsEcsClusterDetailsTypeDef = TypedDict(
    "AwsEcsClusterDetailsTypeDef",
    {
        "CapacityProviders": Sequence[str],
        "ClusterSettings": Sequence[AwsEcsClusterClusterSettingsDetailsTypeDef],
        "Configuration": AwsEcsClusterConfigurationDetailsTypeDef,
        "DefaultCapacityProviderStrategy": Sequence[
            AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionDetailsTypeDef",
    {
        "ContainerDefinitions": Sequence[AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef],
        "Cpu": str,
        "ExecutionRoleArn": str,
        "Family": str,
        "InferenceAccelerators": Sequence[AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef],
        "IpcMode": str,
        "Memory": str,
        "NetworkMode": str,
        "PidMode": str,
        "PlacementConstraints": Sequence[AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef],
        "ProxyConfiguration": AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef,
        "RequiresCompatibilities": Sequence[str],
        "TaskRoleArn": str,
        "Volumes": Sequence[AwsEcsTaskDefinitionVolumesDetailsTypeDef],
    },
    total=False,
)

AwsRdsDbInstanceDetailsTypeDef = TypedDict(
    "AwsRdsDbInstanceDetailsTypeDef",
    {
        "AssociatedRoles": Sequence[AwsRdsDbInstanceAssociatedRoleTypeDef],
        "CACertificateIdentifier": str,
        "DBClusterIdentifier": str,
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "DbInstancePort": int,
        "DbiResourceId": str,
        "DBName": str,
        "DeletionProtection": bool,
        "Endpoint": AwsRdsDbInstanceEndpointTypeDef,
        "Engine": str,
        "EngineVersion": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "InstanceCreateTime": str,
        "KmsKeyId": str,
        "PubliclyAccessible": bool,
        "StorageEncrypted": bool,
        "TdeCredentialArn": str,
        "VpcSecurityGroups": Sequence[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
        "MultiAz": bool,
        "EnhancedMonitoringResourceArn": str,
        "DbInstanceStatus": str,
        "MasterUsername": str,
        "AllocatedStorage": int,
        "PreferredBackupWindow": str,
        "BackupRetentionPeriod": int,
        "DbSecurityGroups": Sequence[str],
        "DbParameterGroups": Sequence[AwsRdsDbParameterGroupTypeDef],
        "AvailabilityZone": str,
        "DbSubnetGroup": AwsRdsDbSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": AwsRdsDbPendingModifiedValuesTypeDef,
        "LatestRestorableTime": str,
        "AutoMinorVersionUpgrade": bool,
        "ReadReplicaSourceDBInstanceIdentifier": str,
        "ReadReplicaDBInstanceIdentifiers": Sequence[str],
        "ReadReplicaDBClusterIdentifiers": Sequence[str],
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupMemberships": Sequence[AwsRdsDbOptionGroupMembershipTypeDef],
        "CharacterSetName": str,
        "SecondaryAvailabilityZone": str,
        "StatusInfos": Sequence[AwsRdsDbStatusInfoTypeDef],
        "StorageType": str,
        "DomainMemberships": Sequence[AwsRdsDbDomainMembershipTypeDef],
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "PromotionTier": int,
        "Timezone": str,
        "PerformanceInsightsEnabled": bool,
        "PerformanceInsightsKmsKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnabledCloudWatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[AwsRdsDbProcessorFeatureTypeDef],
        "ListenerEndpoint": AwsRdsDbInstanceEndpointTypeDef,
        "MaxAllocatedStorage": int,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef",
    {
        "Predicate": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationDetailTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationDetailTypeDef",
    {
        "Events": Sequence[str],
        "Filter": AwsS3BucketNotificationConfigurationFilterTypeDef,
        "Destination": str,
        "Type": str,
    },
    total=False,
)

CreateInsightRequestRequestTypeDef = TypedDict(
    "CreateInsightRequestRequestTypeDef",
    {
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
)

GetFindingsRequestGetFindingsPaginateTypeDef = TypedDict(
    "GetFindingsRequestGetFindingsPaginateTypeDef",
    {
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "SortCriteria": Sequence[SortCriterionTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetFindingsRequestRequestTypeDef = TypedDict(
    "GetFindingsRequestRequestTypeDef",
    {
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "SortCriteria": Sequence[SortCriterionTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

InsightTypeDef = TypedDict(
    "InsightTypeDef",
    {
        "InsightArn": str,
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
)

_RequiredUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFindingsRequestRequestTypeDef",
    {
        "Filters": AwsSecurityFindingFiltersTypeDef,
    },
)
_OptionalUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFindingsRequestRequestTypeDef",
    {
        "Note": NoteUpdateTypeDef,
        "RecordState": RecordStateType,
    },
    total=False,
)


class UpdateFindingsRequestRequestTypeDef(
    _RequiredUpdateFindingsRequestRequestTypeDef, _OptionalUpdateFindingsRequestRequestTypeDef
):
    pass


_RequiredUpdateInsightRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInsightRequestRequestTypeDef",
    {
        "InsightArn": str,
    },
)
_OptionalUpdateInsightRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInsightRequestRequestTypeDef",
    {
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
    total=False,
)


class UpdateInsightRequestRequestTypeDef(
    _RequiredUpdateInsightRequestRequestTypeDef, _OptionalUpdateInsightRequestRequestTypeDef
):
    pass


NetworkPathComponentTypeDef = TypedDict(
    "NetworkPathComponentTypeDef",
    {
        "ComponentId": str,
        "ComponentType": str,
        "Egress": NetworkHeaderTypeDef,
        "Ingress": NetworkHeaderTypeDef,
    },
    total=False,
)

CustomDataIdentifiersDetectionsTypeDef = TypedDict(
    "CustomDataIdentifiersDetectionsTypeDef",
    {
        "Count": int,
        "Arn": str,
        "Name": str,
        "Occurrences": OccurrencesTypeDef,
    },
    total=False,
)

SensitiveDataDetectionsTypeDef = TypedDict(
    "SensitiveDataDetectionsTypeDef",
    {
        "Count": int,
        "Type": str,
        "Occurrences": OccurrencesTypeDef,
    },
    total=False,
)

RuleGroupSourceStatelessRulesDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRulesDetailsTypeDef",
    {
        "Priority": int,
        "RuleDefinition": RuleGroupSourceStatelessRuleDefinitionTypeDef,
    },
    total=False,
)

FirewallPolicyStatelessCustomActionsDetailsTypeDef = TypedDict(
    "FirewallPolicyStatelessCustomActionsDetailsTypeDef",
    {
        "ActionDefinition": StatelessCustomActionDefinitionTypeDef,
        "ActionName": str,
    },
    total=False,
)

RuleGroupSourceCustomActionsDetailsTypeDef = TypedDict(
    "RuleGroupSourceCustomActionsDetailsTypeDef",
    {
        "ActionDefinition": StatelessCustomActionDefinitionTypeDef,
        "ActionName": str,
    },
    total=False,
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ActionType": str,
        "NetworkConnectionAction": NetworkConnectionActionTypeDef,
        "AwsApiCallAction": AwsApiCallActionTypeDef,
        "DnsRequestAction": DnsRequestActionTypeDef,
        "PortProbeAction": PortProbeActionTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionDetailsTypeDef = TypedDict(
    "AwsCloudFrontDistributionDetailsTypeDef",
    {
        "CacheBehaviors": AwsCloudFrontDistributionCacheBehaviorsTypeDef,
        "DefaultCacheBehavior": AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef,
        "DefaultRootObject": str,
        "DomainName": str,
        "ETag": str,
        "LastModifiedTime": str,
        "Logging": AwsCloudFrontDistributionLoggingTypeDef,
        "Origins": AwsCloudFrontDistributionOriginsTypeDef,
        "OriginGroups": AwsCloudFrontDistributionOriginGroupsTypeDef,
        "ViewerCertificate": AwsCloudFrontDistributionViewerCertificateTypeDef,
        "Status": str,
        "WebAclId": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef",
    {
        "AbortIncompleteMultipartUpload": AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef,
        "ExpirationDate": str,
        "ExpirationInDays": int,
        "ExpiredObjectDeleteMarker": bool,
        "Filter": AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef,
        "ID": str,
        "NoncurrentVersionExpirationInDays": int,
        "NoncurrentVersionTransitions": Sequence[
            AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef
        ],
        "Prefix": str,
        "Status": str,
        "Transitions": Sequence[
            AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef
        ],
    },
    total=False,
)

AwsS3BucketNotificationConfigurationTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationTypeDef",
    {
        "Configurations": Sequence[AwsS3BucketNotificationConfigurationDetailTypeDef],
    },
    total=False,
)

GetInsightsResponseTypeDef = TypedDict(
    "GetInsightsResponseTypeDef",
    {
        "Insights": List[InsightTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomDataIdentifiersResultTypeDef = TypedDict(
    "CustomDataIdentifiersResultTypeDef",
    {
        "Detections": Sequence[CustomDataIdentifiersDetectionsTypeDef],
        "TotalCount": int,
    },
    total=False,
)

SensitiveDataResultTypeDef = TypedDict(
    "SensitiveDataResultTypeDef",
    {
        "Category": str,
        "Detections": Sequence[SensitiveDataDetectionsTypeDef],
        "TotalCount": int,
    },
    total=False,
)

FirewallPolicyDetailsTypeDef = TypedDict(
    "FirewallPolicyDetailsTypeDef",
    {
        "StatefulRuleGroupReferences": Sequence[
            FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef
        ],
        "StatelessCustomActions": Sequence[FirewallPolicyStatelessCustomActionsDetailsTypeDef],
        "StatelessDefaultActions": Sequence[str],
        "StatelessFragmentDefaultActions": Sequence[str],
        "StatelessRuleGroupReferences": Sequence[
            FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef
        ],
    },
    total=False,
)

RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef",
    {
        "CustomActions": Sequence[RuleGroupSourceCustomActionsDetailsTypeDef],
        "StatelessRules": Sequence[RuleGroupSourceStatelessRulesDetailsTypeDef],
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef",
    {
        "Rules": Sequence[AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef],
    },
    total=False,
)

ClassificationResultTypeDef = TypedDict(
    "ClassificationResultTypeDef",
    {
        "MimeType": str,
        "SizeClassified": int,
        "AdditionalOccurrences": bool,
        "Status": ClassificationStatusTypeDef,
        "SensitiveData": Sequence[SensitiveDataResultTypeDef],
        "CustomDataIdentifiers": CustomDataIdentifiersResultTypeDef,
    },
    total=False,
)

AwsNetworkFirewallFirewallPolicyDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallPolicyDetailsTypeDef",
    {
        "FirewallPolicy": FirewallPolicyDetailsTypeDef,
        "FirewallPolicyArn": str,
        "FirewallPolicyId": str,
        "FirewallPolicyName": str,
        "Description": str,
    },
    total=False,
)

RuleGroupSourceTypeDef = TypedDict(
    "RuleGroupSourceTypeDef",
    {
        "RulesSourceList": RuleGroupSourceListDetailsTypeDef,
        "RulesString": str,
        "StatefulRules": Sequence[RuleGroupSourceStatefulRulesDetailsTypeDef],
        "StatelessRulesAndCustomActions": RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef,
    },
    total=False,
)

AwsS3BucketDetailsTypeDef = TypedDict(
    "AwsS3BucketDetailsTypeDef",
    {
        "OwnerId": str,
        "OwnerName": str,
        "OwnerAccountId": str,
        "CreatedAt": str,
        "ServerSideEncryptionConfiguration": AwsS3BucketServerSideEncryptionConfigurationTypeDef,
        "BucketLifecycleConfiguration": AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef,
        "PublicAccessBlockConfiguration": AwsS3AccountPublicAccessBlockDetailsTypeDef,
        "AccessControlList": str,
        "BucketLoggingConfiguration": AwsS3BucketLoggingConfigurationTypeDef,
        "BucketWebsiteConfiguration": AwsS3BucketWebsiteConfigurationTypeDef,
        "BucketNotificationConfiguration": AwsS3BucketNotificationConfigurationTypeDef,
        "BucketVersioningConfiguration": AwsS3BucketBucketVersioningConfigurationTypeDef,
    },
    total=False,
)

DataClassificationDetailsTypeDef = TypedDict(
    "DataClassificationDetailsTypeDef",
    {
        "DetailedResultsLocation": str,
        "Result": ClassificationResultTypeDef,
    },
    total=False,
)

RuleGroupDetailsTypeDef = TypedDict(
    "RuleGroupDetailsTypeDef",
    {
        "RuleVariables": RuleGroupVariablesTypeDef,
        "RulesSource": RuleGroupSourceTypeDef,
    },
    total=False,
)

AwsNetworkFirewallRuleGroupDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallRuleGroupDetailsTypeDef",
    {
        "Capacity": int,
        "Description": str,
        "RuleGroup": RuleGroupDetailsTypeDef,
        "RuleGroupArn": str,
        "RuleGroupId": str,
        "RuleGroupName": str,
        "Type": str,
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "AwsAutoScalingAutoScalingGroup": AwsAutoScalingAutoScalingGroupDetailsTypeDef,
        "AwsCodeBuildProject": AwsCodeBuildProjectDetailsTypeDef,
        "AwsCloudFrontDistribution": AwsCloudFrontDistributionDetailsTypeDef,
        "AwsEc2Instance": AwsEc2InstanceDetailsTypeDef,
        "AwsEc2NetworkInterface": AwsEc2NetworkInterfaceDetailsTypeDef,
        "AwsEc2SecurityGroup": AwsEc2SecurityGroupDetailsTypeDef,
        "AwsEc2Volume": AwsEc2VolumeDetailsTypeDef,
        "AwsEc2Vpc": AwsEc2VpcDetailsTypeDef,
        "AwsEc2Eip": AwsEc2EipDetailsTypeDef,
        "AwsEc2Subnet": AwsEc2SubnetDetailsTypeDef,
        "AwsEc2NetworkAcl": AwsEc2NetworkAclDetailsTypeDef,
        "AwsElbv2LoadBalancer": AwsElbv2LoadBalancerDetailsTypeDef,
        "AwsElasticBeanstalkEnvironment": AwsElasticBeanstalkEnvironmentDetailsTypeDef,
        "AwsElasticsearchDomain": AwsElasticsearchDomainDetailsTypeDef,
        "AwsS3Bucket": AwsS3BucketDetailsTypeDef,
        "AwsS3AccountPublicAccessBlock": AwsS3AccountPublicAccessBlockDetailsTypeDef,
        "AwsS3Object": AwsS3ObjectDetailsTypeDef,
        "AwsSecretsManagerSecret": AwsSecretsManagerSecretDetailsTypeDef,
        "AwsIamAccessKey": AwsIamAccessKeyDetailsTypeDef,
        "AwsIamUser": AwsIamUserDetailsTypeDef,
        "AwsIamPolicy": AwsIamPolicyDetailsTypeDef,
        "AwsApiGatewayV2Stage": AwsApiGatewayV2StageDetailsTypeDef,
        "AwsApiGatewayV2Api": AwsApiGatewayV2ApiDetailsTypeDef,
        "AwsDynamoDbTable": AwsDynamoDbTableDetailsTypeDef,
        "AwsApiGatewayStage": AwsApiGatewayStageDetailsTypeDef,
        "AwsApiGatewayRestApi": AwsApiGatewayRestApiDetailsTypeDef,
        "AwsCloudTrailTrail": AwsCloudTrailTrailDetailsTypeDef,
        "AwsSsmPatchCompliance": AwsSsmPatchComplianceDetailsTypeDef,
        "AwsCertificateManagerCertificate": AwsCertificateManagerCertificateDetailsTypeDef,
        "AwsRedshiftCluster": AwsRedshiftClusterDetailsTypeDef,
        "AwsElbLoadBalancer": AwsElbLoadBalancerDetailsTypeDef,
        "AwsIamGroup": AwsIamGroupDetailsTypeDef,
        "AwsIamRole": AwsIamRoleDetailsTypeDef,
        "AwsKmsKey": AwsKmsKeyDetailsTypeDef,
        "AwsLambdaFunction": AwsLambdaFunctionDetailsTypeDef,
        "AwsLambdaLayerVersion": AwsLambdaLayerVersionDetailsTypeDef,
        "AwsRdsDbInstance": AwsRdsDbInstanceDetailsTypeDef,
        "AwsSnsTopic": AwsSnsTopicDetailsTypeDef,
        "AwsSqsQueue": AwsSqsQueueDetailsTypeDef,
        "AwsWafWebAcl": AwsWafWebAclDetailsTypeDef,
        "AwsRdsDbSnapshot": AwsRdsDbSnapshotDetailsTypeDef,
        "AwsRdsDbClusterSnapshot": AwsRdsDbClusterSnapshotDetailsTypeDef,
        "AwsRdsDbCluster": AwsRdsDbClusterDetailsTypeDef,
        "AwsEcsCluster": AwsEcsClusterDetailsTypeDef,
        "AwsEcsTaskDefinition": AwsEcsTaskDefinitionDetailsTypeDef,
        "Container": ContainerDetailsTypeDef,
        "Other": Mapping[str, str],
        "AwsRdsEventSubscription": AwsRdsEventSubscriptionDetailsTypeDef,
        "AwsEcsService": AwsEcsServiceDetailsTypeDef,
        "AwsAutoScalingLaunchConfiguration": AwsAutoScalingLaunchConfigurationDetailsTypeDef,
        "AwsEc2VpnConnection": AwsEc2VpnConnectionDetailsTypeDef,
        "AwsEcrContainerImage": AwsEcrContainerImageDetailsTypeDef,
        "AwsOpenSearchServiceDomain": AwsOpenSearchServiceDomainDetailsTypeDef,
        "AwsEc2VpcEndpointService": AwsEc2VpcEndpointServiceDetailsTypeDef,
        "AwsXrayEncryptionConfig": AwsXrayEncryptionConfigDetailsTypeDef,
        "AwsWafRateBasedRule": AwsWafRateBasedRuleDetailsTypeDef,
        "AwsWafRegionalRateBasedRule": AwsWafRegionalRateBasedRuleDetailsTypeDef,
        "AwsEcrRepository": AwsEcrRepositoryDetailsTypeDef,
        "AwsEksCluster": AwsEksClusterDetailsTypeDef,
        "AwsNetworkFirewallFirewallPolicy": AwsNetworkFirewallFirewallPolicyDetailsTypeDef,
        "AwsNetworkFirewallFirewall": AwsNetworkFirewallFirewallDetailsTypeDef,
        "AwsNetworkFirewallRuleGroup": AwsNetworkFirewallRuleGroupDetailsTypeDef,
        "AwsRdsDbSecurityGroup": AwsRdsDbSecurityGroupDetailsTypeDef,
    },
    total=False,
)

_RequiredResourceTypeDef = TypedDict(
    "_RequiredResourceTypeDef",
    {
        "Type": str,
        "Id": str,
    },
)
_OptionalResourceTypeDef = TypedDict(
    "_OptionalResourceTypeDef",
    {
        "Partition": PartitionType,
        "Region": str,
        "ResourceRole": str,
        "Tags": Mapping[str, str],
        "DataClassification": DataClassificationDetailsTypeDef,
        "Details": ResourceDetailsTypeDef,
    },
    total=False,
)


class ResourceTypeDef(_RequiredResourceTypeDef, _OptionalResourceTypeDef):
    pass


_RequiredAwsSecurityFindingTypeDef = TypedDict(
    "_RequiredAwsSecurityFindingTypeDef",
    {
        "SchemaVersion": str,
        "Id": str,
        "ProductArn": str,
        "GeneratorId": str,
        "AwsAccountId": str,
        "CreatedAt": str,
        "UpdatedAt": str,
        "Title": str,
        "Description": str,
        "Resources": Sequence[ResourceTypeDef],
    },
)
_OptionalAwsSecurityFindingTypeDef = TypedDict(
    "_OptionalAwsSecurityFindingTypeDef",
    {
        "ProductName": str,
        "CompanyName": str,
        "Region": str,
        "Types": Sequence[str],
        "FirstObservedAt": str,
        "LastObservedAt": str,
        "Severity": SeverityTypeDef,
        "Confidence": int,
        "Criticality": int,
        "Remediation": RemediationTypeDef,
        "SourceUrl": str,
        "ProductFields": Mapping[str, str],
        "UserDefinedFields": Mapping[str, str],
        "Malware": Sequence[MalwareTypeDef],
        "Network": NetworkTypeDef,
        "NetworkPath": Sequence[NetworkPathComponentTypeDef],
        "Process": ProcessDetailsTypeDef,
        "ThreatIntelIndicators": Sequence[ThreatIntelIndicatorTypeDef],
        "Compliance": ComplianceTypeDef,
        "VerificationState": VerificationStateType,
        "WorkflowState": WorkflowStateType,
        "Workflow": WorkflowTypeDef,
        "RecordState": RecordStateType,
        "RelatedFindings": Sequence[RelatedFindingTypeDef],
        "Note": NoteTypeDef,
        "Vulnerabilities": Sequence[VulnerabilityTypeDef],
        "PatchSummary": PatchSummaryTypeDef,
        "Action": ActionTypeDef,
        "FindingProviderFields": FindingProviderFieldsTypeDef,
        "Sample": bool,
    },
    total=False,
)


class AwsSecurityFindingTypeDef(
    _RequiredAwsSecurityFindingTypeDef, _OptionalAwsSecurityFindingTypeDef
):
    pass


BatchImportFindingsRequestRequestTypeDef = TypedDict(
    "BatchImportFindingsRequestRequestTypeDef",
    {
        "Findings": Sequence[AwsSecurityFindingTypeDef],
    },
)

GetFindingsResponseTypeDef = TypedDict(
    "GetFindingsResponseTypeDef",
    {
        "Findings": List[AwsSecurityFindingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
