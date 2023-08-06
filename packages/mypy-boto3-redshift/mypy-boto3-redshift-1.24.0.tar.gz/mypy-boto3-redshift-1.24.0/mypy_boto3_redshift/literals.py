"""
Type annotations for redshift service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/literals/)

Usage::

    ```python
    from mypy_boto3_redshift.literals import ActionTypeType

    data: ActionTypeType = "recommend-node-config"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ActionTypeType",
    "AquaConfigurationStatusType",
    "AquaStatusType",
    "AuthorizationStatusType",
    "ClusterAvailableWaiterName",
    "ClusterDeletedWaiterName",
    "ClusterRestoredWaiterName",
    "DataShareStatusForConsumerType",
    "DataShareStatusForProducerType",
    "DataShareStatusType",
    "DescribeClusterDbRevisionsPaginatorName",
    "DescribeClusterParameterGroupsPaginatorName",
    "DescribeClusterParametersPaginatorName",
    "DescribeClusterSecurityGroupsPaginatorName",
    "DescribeClusterSnapshotsPaginatorName",
    "DescribeClusterSubnetGroupsPaginatorName",
    "DescribeClusterTracksPaginatorName",
    "DescribeClusterVersionsPaginatorName",
    "DescribeClustersPaginatorName",
    "DescribeDataSharesForConsumerPaginatorName",
    "DescribeDataSharesForProducerPaginatorName",
    "DescribeDataSharesPaginatorName",
    "DescribeDefaultClusterParametersPaginatorName",
    "DescribeEndpointAccessPaginatorName",
    "DescribeEndpointAuthorizationPaginatorName",
    "DescribeEventSubscriptionsPaginatorName",
    "DescribeEventsPaginatorName",
    "DescribeHsmClientCertificatesPaginatorName",
    "DescribeHsmConfigurationsPaginatorName",
    "DescribeNodeConfigurationOptionsPaginatorName",
    "DescribeOrderableClusterOptionsPaginatorName",
    "DescribeReservedNodeExchangeStatusPaginatorName",
    "DescribeReservedNodeOfferingsPaginatorName",
    "DescribeReservedNodesPaginatorName",
    "DescribeScheduledActionsPaginatorName",
    "DescribeSnapshotCopyGrantsPaginatorName",
    "DescribeSnapshotSchedulesPaginatorName",
    "DescribeTableRestoreStatusPaginatorName",
    "DescribeTagsPaginatorName",
    "DescribeUsageLimitsPaginatorName",
    "GetReservedNodeExchangeConfigurationOptionsPaginatorName",
    "GetReservedNodeExchangeOfferingsPaginatorName",
    "LogDestinationTypeType",
    "ModeType",
    "NodeConfigurationOptionsFilterNameType",
    "OperatorTypeType",
    "ParameterApplyTypeType",
    "PartnerIntegrationStatusType",
    "ReservedNodeExchangeActionTypeType",
    "ReservedNodeExchangeStatusTypeType",
    "ReservedNodeOfferingTypeType",
    "ScheduleStateType",
    "ScheduledActionFilterNameType",
    "ScheduledActionStateType",
    "ScheduledActionTypeValuesType",
    "SnapshotAttributeToSortByType",
    "SnapshotAvailableWaiterName",
    "SortByOrderType",
    "SourceTypeType",
    "TableRestoreStatusTypeType",
    "UsageLimitBreachActionType",
    "UsageLimitFeatureTypeType",
    "UsageLimitLimitTypeType",
    "UsageLimitPeriodType",
    "RedshiftServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
    "RegionName",
)


ActionTypeType = Literal["recommend-node-config", "resize-cluster", "restore-cluster"]
AquaConfigurationStatusType = Literal["auto", "disabled", "enabled"]
AquaStatusType = Literal["applying", "disabled", "enabled"]
AuthorizationStatusType = Literal["Authorized", "Revoking"]
ClusterAvailableWaiterName = Literal["cluster_available"]
ClusterDeletedWaiterName = Literal["cluster_deleted"]
ClusterRestoredWaiterName = Literal["cluster_restored"]
DataShareStatusForConsumerType = Literal["ACTIVE", "AVAILABLE"]
DataShareStatusForProducerType = Literal[
    "ACTIVE", "AUTHORIZED", "DEAUTHORIZED", "PENDING_AUTHORIZATION", "REJECTED"
]
DataShareStatusType = Literal[
    "ACTIVE", "AUTHORIZED", "AVAILABLE", "DEAUTHORIZED", "PENDING_AUTHORIZATION", "REJECTED"
]
DescribeClusterDbRevisionsPaginatorName = Literal["describe_cluster_db_revisions"]
DescribeClusterParameterGroupsPaginatorName = Literal["describe_cluster_parameter_groups"]
DescribeClusterParametersPaginatorName = Literal["describe_cluster_parameters"]
DescribeClusterSecurityGroupsPaginatorName = Literal["describe_cluster_security_groups"]
DescribeClusterSnapshotsPaginatorName = Literal["describe_cluster_snapshots"]
DescribeClusterSubnetGroupsPaginatorName = Literal["describe_cluster_subnet_groups"]
DescribeClusterTracksPaginatorName = Literal["describe_cluster_tracks"]
DescribeClusterVersionsPaginatorName = Literal["describe_cluster_versions"]
DescribeClustersPaginatorName = Literal["describe_clusters"]
DescribeDataSharesForConsumerPaginatorName = Literal["describe_data_shares_for_consumer"]
DescribeDataSharesForProducerPaginatorName = Literal["describe_data_shares_for_producer"]
DescribeDataSharesPaginatorName = Literal["describe_data_shares"]
DescribeDefaultClusterParametersPaginatorName = Literal["describe_default_cluster_parameters"]
DescribeEndpointAccessPaginatorName = Literal["describe_endpoint_access"]
DescribeEndpointAuthorizationPaginatorName = Literal["describe_endpoint_authorization"]
DescribeEventSubscriptionsPaginatorName = Literal["describe_event_subscriptions"]
DescribeEventsPaginatorName = Literal["describe_events"]
DescribeHsmClientCertificatesPaginatorName = Literal["describe_hsm_client_certificates"]
DescribeHsmConfigurationsPaginatorName = Literal["describe_hsm_configurations"]
DescribeNodeConfigurationOptionsPaginatorName = Literal["describe_node_configuration_options"]
DescribeOrderableClusterOptionsPaginatorName = Literal["describe_orderable_cluster_options"]
DescribeReservedNodeExchangeStatusPaginatorName = Literal["describe_reserved_node_exchange_status"]
DescribeReservedNodeOfferingsPaginatorName = Literal["describe_reserved_node_offerings"]
DescribeReservedNodesPaginatorName = Literal["describe_reserved_nodes"]
DescribeScheduledActionsPaginatorName = Literal["describe_scheduled_actions"]
DescribeSnapshotCopyGrantsPaginatorName = Literal["describe_snapshot_copy_grants"]
DescribeSnapshotSchedulesPaginatorName = Literal["describe_snapshot_schedules"]
DescribeTableRestoreStatusPaginatorName = Literal["describe_table_restore_status"]
DescribeTagsPaginatorName = Literal["describe_tags"]
DescribeUsageLimitsPaginatorName = Literal["describe_usage_limits"]
GetReservedNodeExchangeConfigurationOptionsPaginatorName = Literal[
    "get_reserved_node_exchange_configuration_options"
]
GetReservedNodeExchangeOfferingsPaginatorName = Literal["get_reserved_node_exchange_offerings"]
LogDestinationTypeType = Literal["cloudwatch", "s3"]
ModeType = Literal["high-performance", "standard"]
NodeConfigurationOptionsFilterNameType = Literal[
    "EstimatedDiskUtilizationPercent", "Mode", "NodeType", "NumberOfNodes"
]
OperatorTypeType = Literal["between", "eq", "ge", "gt", "in", "le", "lt"]
ParameterApplyTypeType = Literal["dynamic", "static"]
PartnerIntegrationStatusType = Literal["Active", "ConnectionFailure", "Inactive", "RuntimeFailure"]
ReservedNodeExchangeActionTypeType = Literal["resize-cluster", "restore-cluster"]
ReservedNodeExchangeStatusTypeType = Literal[
    "FAILED", "IN_PROGRESS", "PENDING", "REQUESTED", "RETRYING", "SUCCEEDED"
]
ReservedNodeOfferingTypeType = Literal["Regular", "Upgradable"]
ScheduleStateType = Literal["ACTIVE", "FAILED", "MODIFYING"]
ScheduledActionFilterNameType = Literal["cluster-identifier", "iam-role"]
ScheduledActionStateType = Literal["ACTIVE", "DISABLED"]
ScheduledActionTypeValuesType = Literal["PauseCluster", "ResizeCluster", "ResumeCluster"]
SnapshotAttributeToSortByType = Literal["CREATE_TIME", "SOURCE_TYPE", "TOTAL_SIZE"]
SnapshotAvailableWaiterName = Literal["snapshot_available"]
SortByOrderType = Literal["ASC", "DESC"]
SourceTypeType = Literal[
    "cluster",
    "cluster-parameter-group",
    "cluster-security-group",
    "cluster-snapshot",
    "scheduled-action",
]
TableRestoreStatusTypeType = Literal["CANCELED", "FAILED", "IN_PROGRESS", "PENDING", "SUCCEEDED"]
UsageLimitBreachActionType = Literal["disable", "emit-metric", "log"]
UsageLimitFeatureTypeType = Literal["concurrency-scaling", "cross-region-datasharing", "spectrum"]
UsageLimitLimitTypeType = Literal["data-scanned", "time"]
UsageLimitPeriodType = Literal["daily", "monthly", "weekly"]
RedshiftServiceName = Literal["redshift"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "backup-gateway",
    "batch",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "drs",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "gamesparks",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector2",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhubstrategy",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opensearch",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "panorama",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "polly",
    "pricing",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resiliencehub",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "voice-id",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "describe_cluster_db_revisions",
    "describe_cluster_parameter_groups",
    "describe_cluster_parameters",
    "describe_cluster_security_groups",
    "describe_cluster_snapshots",
    "describe_cluster_subnet_groups",
    "describe_cluster_tracks",
    "describe_cluster_versions",
    "describe_clusters",
    "describe_data_shares",
    "describe_data_shares_for_consumer",
    "describe_data_shares_for_producer",
    "describe_default_cluster_parameters",
    "describe_endpoint_access",
    "describe_endpoint_authorization",
    "describe_event_subscriptions",
    "describe_events",
    "describe_hsm_client_certificates",
    "describe_hsm_configurations",
    "describe_node_configuration_options",
    "describe_orderable_cluster_options",
    "describe_reserved_node_exchange_status",
    "describe_reserved_node_offerings",
    "describe_reserved_nodes",
    "describe_scheduled_actions",
    "describe_snapshot_copy_grants",
    "describe_snapshot_schedules",
    "describe_table_restore_status",
    "describe_tags",
    "describe_usage_limits",
    "get_reserved_node_exchange_configuration_options",
    "get_reserved_node_exchange_offerings",
]
WaiterName = Literal[
    "cluster_available", "cluster_deleted", "cluster_restored", "snapshot_available"
]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
