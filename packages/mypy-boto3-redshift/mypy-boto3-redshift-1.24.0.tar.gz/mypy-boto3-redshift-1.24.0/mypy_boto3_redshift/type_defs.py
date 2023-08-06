"""
Type annotations for redshift service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift/type_defs/)

Usage::

    ```python
    from mypy_boto3_redshift.type_defs import AcceptReservedNodeExchangeInputMessageRequestTypeDef

    data: AcceptReservedNodeExchangeInputMessageRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ActionTypeType,
    AquaConfigurationStatusType,
    AquaStatusType,
    AuthorizationStatusType,
    DataShareStatusForConsumerType,
    DataShareStatusForProducerType,
    DataShareStatusType,
    LogDestinationTypeType,
    ModeType,
    NodeConfigurationOptionsFilterNameType,
    OperatorTypeType,
    ParameterApplyTypeType,
    PartnerIntegrationStatusType,
    ReservedNodeExchangeActionTypeType,
    ReservedNodeExchangeStatusTypeType,
    ReservedNodeOfferingTypeType,
    ScheduledActionFilterNameType,
    ScheduledActionStateType,
    ScheduledActionTypeValuesType,
    ScheduleStateType,
    SnapshotAttributeToSortByType,
    SortByOrderType,
    SourceTypeType,
    TableRestoreStatusTypeType,
    UsageLimitBreachActionType,
    UsageLimitFeatureTypeType,
    UsageLimitLimitTypeType,
    UsageLimitPeriodType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptReservedNodeExchangeInputMessageRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AttributeValueTargetTypeDef",
    "AccountWithRestoreAccessTypeDef",
    "AquaConfigurationTypeDef",
    "AssociateDataShareConsumerMessageRequestTypeDef",
    "AuthenticationProfileTypeDef",
    "AuthorizeClusterSecurityGroupIngressMessageRequestTypeDef",
    "AuthorizeDataShareMessageRequestTypeDef",
    "AuthorizeEndpointAccessMessageRequestTypeDef",
    "AuthorizeSnapshotAccessMessageRequestTypeDef",
    "SupportedPlatformTypeDef",
    "DeleteClusterSnapshotMessageTypeDef",
    "SnapshotErrorMessageTypeDef",
    "BatchModifyClusterSnapshotsMessageRequestTypeDef",
    "CancelResizeMessageRequestTypeDef",
    "ClusterAssociatedToScheduleTypeDef",
    "RevisionTargetTypeDef",
    "ClusterIamRoleTypeDef",
    "ClusterNodeTypeDef",
    "ParameterTypeDef",
    "ClusterParameterStatusTypeDef",
    "TagTypeDef",
    "ClusterSecurityGroupMembershipTypeDef",
    "ClusterSnapshotCopyStatusTypeDef",
    "DataTransferProgressTypeDef",
    "DeferredMaintenanceWindowTypeDef",
    "ElasticIpStatusTypeDef",
    "HsmStatusTypeDef",
    "PendingModifiedValuesTypeDef",
    "ReservedNodeExchangeStatusTypeDef",
    "ResizeInfoTypeDef",
    "RestoreStatusTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "ClusterVersionTypeDef",
    "CopyClusterSnapshotMessageRequestTypeDef",
    "CreateAuthenticationProfileMessageRequestTypeDef",
    "CreateEndpointAccessMessageRequestTypeDef",
    "DataShareAssociationTypeDef",
    "DeauthorizeDataShareMessageRequestTypeDef",
    "DeleteAuthenticationProfileMessageRequestTypeDef",
    "DeleteClusterMessageRequestTypeDef",
    "DeleteClusterParameterGroupMessageRequestTypeDef",
    "DeleteClusterSecurityGroupMessageRequestTypeDef",
    "DeleteClusterSnapshotMessageRequestTypeDef",
    "DeleteClusterSubnetGroupMessageRequestTypeDef",
    "DeleteEndpointAccessMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteHsmClientCertificateMessageRequestTypeDef",
    "DeleteHsmConfigurationMessageRequestTypeDef",
    "DeleteScheduledActionMessageRequestTypeDef",
    "DeleteSnapshotCopyGrantMessageRequestTypeDef",
    "DeleteSnapshotScheduleMessageRequestTypeDef",
    "DeleteTagsMessageRequestTypeDef",
    "DeleteUsageLimitMessageRequestTypeDef",
    "DescribeAccountAttributesMessageRequestTypeDef",
    "DescribeAuthenticationProfilesMessageRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeClusterDbRevisionsMessageRequestTypeDef",
    "DescribeClusterParameterGroupsMessageRequestTypeDef",
    "DescribeClusterParametersMessageRequestTypeDef",
    "DescribeClusterSecurityGroupsMessageRequestTypeDef",
    "SnapshotSortingEntityTypeDef",
    "WaiterConfigTypeDef",
    "DescribeClusterSubnetGroupsMessageRequestTypeDef",
    "DescribeClusterTracksMessageRequestTypeDef",
    "DescribeClusterVersionsMessageRequestTypeDef",
    "DescribeClustersMessageRequestTypeDef",
    "DescribeDataSharesForConsumerMessageRequestTypeDef",
    "DescribeDataSharesForProducerMessageRequestTypeDef",
    "DescribeDataSharesMessageRequestTypeDef",
    "DescribeDefaultClusterParametersMessageRequestTypeDef",
    "DescribeEndpointAccessMessageRequestTypeDef",
    "DescribeEndpointAuthorizationMessageRequestTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeHsmClientCertificatesMessageRequestTypeDef",
    "DescribeHsmConfigurationsMessageRequestTypeDef",
    "DescribeLoggingStatusMessageRequestTypeDef",
    "NodeConfigurationOptionsFilterTypeDef",
    "DescribeOrderableClusterOptionsMessageRequestTypeDef",
    "DescribePartnersInputMessageRequestTypeDef",
    "PartnerIntegrationInfoTypeDef",
    "DescribeReservedNodeExchangeStatusInputMessageRequestTypeDef",
    "DescribeReservedNodeOfferingsMessageRequestTypeDef",
    "DescribeReservedNodesMessageRequestTypeDef",
    "DescribeResizeMessageRequestTypeDef",
    "ScheduledActionFilterTypeDef",
    "DescribeSnapshotCopyGrantsMessageRequestTypeDef",
    "DescribeSnapshotSchedulesMessageRequestTypeDef",
    "DescribeTableRestoreStatusMessageRequestTypeDef",
    "DescribeTagsMessageRequestTypeDef",
    "DescribeUsageLimitsMessageRequestTypeDef",
    "DisableLoggingMessageRequestTypeDef",
    "DisableSnapshotCopyMessageRequestTypeDef",
    "DisassociateDataShareConsumerMessageRequestTypeDef",
    "EnableLoggingMessageRequestTypeDef",
    "EnableSnapshotCopyMessageRequestTypeDef",
    "EndpointAuthorizationTypeDef",
    "EventInfoMapTypeDef",
    "EventTypeDef",
    "GetClusterCredentialsMessageRequestTypeDef",
    "GetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef",
    "GetReservedNodeExchangeOfferingsInputMessageRequestTypeDef",
    "ModifyAquaInputMessageRequestTypeDef",
    "ModifyAuthenticationProfileMessageRequestTypeDef",
    "ModifyClusterDbRevisionMessageRequestTypeDef",
    "ModifyClusterIamRolesMessageRequestTypeDef",
    "ModifyClusterMaintenanceMessageRequestTypeDef",
    "ModifyClusterMessageRequestTypeDef",
    "ModifyClusterSnapshotMessageRequestTypeDef",
    "ModifyClusterSnapshotScheduleMessageRequestTypeDef",
    "ModifyClusterSubnetGroupMessageRequestTypeDef",
    "ModifyEndpointAccessMessageRequestTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifySnapshotCopyRetentionPeriodMessageRequestTypeDef",
    "ModifySnapshotScheduleMessageRequestTypeDef",
    "ModifyUsageLimitMessageRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "NodeConfigurationOptionTypeDef",
    "PartnerIntegrationInputMessageRequestTypeDef",
    "PauseClusterMessageRequestTypeDef",
    "PauseClusterMessageTypeDef",
    "PurchaseReservedNodeOfferingMessageRequestTypeDef",
    "RebootClusterMessageRequestTypeDef",
    "RecurringChargeTypeDef",
    "RejectDataShareMessageRequestTypeDef",
    "ResizeClusterMessageRequestTypeDef",
    "ResizeClusterMessageTypeDef",
    "RestoreFromClusterSnapshotMessageRequestTypeDef",
    "RestoreTableFromClusterSnapshotMessageRequestTypeDef",
    "TableRestoreStatusTypeDef",
    "ResumeClusterMessageRequestTypeDef",
    "ResumeClusterMessageTypeDef",
    "RevokeClusterSecurityGroupIngressMessageRequestTypeDef",
    "RevokeEndpointAccessMessageRequestTypeDef",
    "RevokeSnapshotAccessMessageRequestTypeDef",
    "RotateEncryptionKeyMessageRequestTypeDef",
    "SupportedOperationTypeDef",
    "UpdatePartnerStatusInputMessageRequestTypeDef",
    "ClusterCredentialsTypeDef",
    "ClusterParameterGroupNameMessageTypeDef",
    "CreateAuthenticationProfileResultTypeDef",
    "CustomerStorageMessageTypeDef",
    "DeleteAuthenticationProfileResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointAuthorizationResponseMetadataTypeDef",
    "LoggingStatusTypeDef",
    "ModifyAuthenticationProfileResultTypeDef",
    "PartnerIntegrationOutputMessageTypeDef",
    "ResizeProgressMessageTypeDef",
    "AccountAttributeTypeDef",
    "ModifyAquaOutputMessageTypeDef",
    "DescribeAuthenticationProfilesResultTypeDef",
    "AvailabilityZoneTypeDef",
    "BatchDeleteClusterSnapshotsRequestRequestTypeDef",
    "BatchDeleteClusterSnapshotsResultTypeDef",
    "BatchModifyClusterSnapshotsOutputMessageTypeDef",
    "ClusterDbRevisionTypeDef",
    "ClusterParameterGroupDetailsTypeDef",
    "DefaultClusterParametersTypeDef",
    "ModifyClusterParameterGroupMessageRequestTypeDef",
    "ResetClusterParameterGroupMessageRequestTypeDef",
    "ClusterParameterGroupStatusTypeDef",
    "ClusterParameterGroupTypeDef",
    "CreateClusterMessageRequestTypeDef",
    "CreateClusterParameterGroupMessageRequestTypeDef",
    "CreateClusterSecurityGroupMessageRequestTypeDef",
    "CreateClusterSnapshotMessageRequestTypeDef",
    "CreateClusterSubnetGroupMessageRequestTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "CreateHsmClientCertificateMessageRequestTypeDef",
    "CreateHsmConfigurationMessageRequestTypeDef",
    "CreateSnapshotCopyGrantMessageRequestTypeDef",
    "CreateSnapshotScheduleMessageRequestTypeDef",
    "CreateTagsMessageRequestTypeDef",
    "CreateUsageLimitMessageRequestTypeDef",
    "EC2SecurityGroupTypeDef",
    "EventSubscriptionTypeDef",
    "HsmClientCertificateTypeDef",
    "HsmConfigurationTypeDef",
    "IPRangeTypeDef",
    "SnapshotCopyGrantTypeDef",
    "SnapshotScheduleResponseMetadataTypeDef",
    "SnapshotScheduleTypeDef",
    "SnapshotTypeDef",
    "TaggedResourceTypeDef",
    "UsageLimitResponseMetadataTypeDef",
    "UsageLimitTypeDef",
    "DescribeReservedNodeExchangeStatusOutputMessageTypeDef",
    "ClusterVersionsMessageTypeDef",
    "DataShareResponseMetadataTypeDef",
    "DataShareTypeDef",
    "DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef",
    "DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef",
    "DescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef",
    "DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef",
    "DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef",
    "DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef",
    "DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef",
    "DescribeClustersMessageDescribeClustersPaginateTypeDef",
    "DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef",
    "DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef",
    "DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef",
    "DescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef",
    "DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef",
    "DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef",
    "DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef",
    "DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef",
    "DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef",
    "DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef",
    "DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef",
    "DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef",
    "DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef",
    "DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef",
    "DescribeTagsMessageDescribeTagsPaginateTypeDef",
    "DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef",
    "GetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef",
    "GetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef",
    "DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef",
    "DescribeClusterSnapshotsMessageRequestTypeDef",
    "DescribeClusterSnapshotsMessageSnapshotAvailableWaitTypeDef",
    "DescribeClustersMessageClusterAvailableWaitTypeDef",
    "DescribeClustersMessageClusterDeletedWaitTypeDef",
    "DescribeClustersMessageClusterRestoredWaitTypeDef",
    "DescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef",
    "DescribeNodeConfigurationOptionsMessageRequestTypeDef",
    "DescribePartnersOutputMessageTypeDef",
    "DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef",
    "DescribeScheduledActionsMessageRequestTypeDef",
    "EndpointAuthorizationListTypeDef",
    "EventCategoriesMapTypeDef",
    "EventsMessageTypeDef",
    "VpcEndpointTypeDef",
    "NodeConfigurationOptionsMessageTypeDef",
    "ReservedNodeOfferingTypeDef",
    "ReservedNodeTypeDef",
    "RestoreTableFromClusterSnapshotResultTypeDef",
    "TableRestoreStatusMessageTypeDef",
    "ScheduledActionTypeTypeDef",
    "UpdateTargetTypeDef",
    "AccountAttributeListTypeDef",
    "OrderableClusterOptionTypeDef",
    "SubnetTypeDef",
    "ClusterDbRevisionsMessageTypeDef",
    "DescribeDefaultClusterParametersResultTypeDef",
    "ClusterParameterGroupsMessageTypeDef",
    "CreateClusterParameterGroupResultTypeDef",
    "CreateEventSubscriptionResultTypeDef",
    "EventSubscriptionsMessageTypeDef",
    "ModifyEventSubscriptionResultTypeDef",
    "CreateHsmClientCertificateResultTypeDef",
    "HsmClientCertificateMessageTypeDef",
    "CreateHsmConfigurationResultTypeDef",
    "HsmConfigurationMessageTypeDef",
    "ClusterSecurityGroupTypeDef",
    "CreateSnapshotCopyGrantResultTypeDef",
    "SnapshotCopyGrantMessageTypeDef",
    "DescribeSnapshotSchedulesOutputMessageTypeDef",
    "AuthorizeSnapshotAccessResultTypeDef",
    "CopyClusterSnapshotResultTypeDef",
    "CreateClusterSnapshotResultTypeDef",
    "DeleteClusterSnapshotResultTypeDef",
    "ModifyClusterSnapshotResultTypeDef",
    "RevokeSnapshotAccessResultTypeDef",
    "SnapshotMessageTypeDef",
    "TaggedResourceListMessageTypeDef",
    "UsageLimitListTypeDef",
    "DescribeDataSharesForConsumerResultTypeDef",
    "DescribeDataSharesForProducerResultTypeDef",
    "DescribeDataSharesResultTypeDef",
    "EventCategoriesMessageTypeDef",
    "EndpointAccessResponseMetadataTypeDef",
    "EndpointAccessTypeDef",
    "EndpointTypeDef",
    "GetReservedNodeExchangeOfferingsOutputMessageTypeDef",
    "ReservedNodeOfferingsMessageTypeDef",
    "AcceptReservedNodeExchangeOutputMessageTypeDef",
    "PurchaseReservedNodeOfferingResultTypeDef",
    "ReservedNodeConfigurationOptionTypeDef",
    "ReservedNodesMessageTypeDef",
    "CreateScheduledActionMessageRequestTypeDef",
    "ModifyScheduledActionMessageRequestTypeDef",
    "ScheduledActionResponseMetadataTypeDef",
    "ScheduledActionTypeDef",
    "MaintenanceTrackTypeDef",
    "OrderableClusterOptionsMessageTypeDef",
    "ClusterSubnetGroupTypeDef",
    "AuthorizeClusterSecurityGroupIngressResultTypeDef",
    "ClusterSecurityGroupMessageTypeDef",
    "CreateClusterSecurityGroupResultTypeDef",
    "RevokeClusterSecurityGroupIngressResultTypeDef",
    "EndpointAccessListTypeDef",
    "ClusterTypeDef",
    "GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef",
    "ScheduledActionsMessageTypeDef",
    "TrackListMessageTypeDef",
    "ClusterSubnetGroupMessageTypeDef",
    "CreateClusterSubnetGroupResultTypeDef",
    "ModifyClusterSubnetGroupResultTypeDef",
    "ClustersMessageTypeDef",
    "CreateClusterResultTypeDef",
    "DeleteClusterResultTypeDef",
    "DisableSnapshotCopyResultTypeDef",
    "EnableSnapshotCopyResultTypeDef",
    "ModifyClusterDbRevisionResultTypeDef",
    "ModifyClusterIamRolesResultTypeDef",
    "ModifyClusterMaintenanceResultTypeDef",
    "ModifyClusterResultTypeDef",
    "ModifySnapshotCopyRetentionPeriodResultTypeDef",
    "PauseClusterResultTypeDef",
    "RebootClusterResultTypeDef",
    "ResizeClusterResultTypeDef",
    "RestoreFromClusterSnapshotResultTypeDef",
    "ResumeClusterResultTypeDef",
    "RotateEncryptionKeyResultTypeDef",
)

AcceptReservedNodeExchangeInputMessageRequestTypeDef = TypedDict(
    "AcceptReservedNodeExchangeInputMessageRequestTypeDef",
    {
        "ReservedNodeId": str,
        "TargetReservedNodeOfferingId": str,
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

AttributeValueTargetTypeDef = TypedDict(
    "AttributeValueTargetTypeDef",
    {
        "AttributeValue": str,
    },
    total=False,
)

AccountWithRestoreAccessTypeDef = TypedDict(
    "AccountWithRestoreAccessTypeDef",
    {
        "AccountId": str,
        "AccountAlias": str,
    },
    total=False,
)

AquaConfigurationTypeDef = TypedDict(
    "AquaConfigurationTypeDef",
    {
        "AquaStatus": AquaStatusType,
        "AquaConfigurationStatus": AquaConfigurationStatusType,
    },
    total=False,
)

_RequiredAssociateDataShareConsumerMessageRequestTypeDef = TypedDict(
    "_RequiredAssociateDataShareConsumerMessageRequestTypeDef",
    {
        "DataShareArn": str,
    },
)
_OptionalAssociateDataShareConsumerMessageRequestTypeDef = TypedDict(
    "_OptionalAssociateDataShareConsumerMessageRequestTypeDef",
    {
        "AssociateEntireAccount": bool,
        "ConsumerArn": str,
        "ConsumerRegion": str,
    },
    total=False,
)


class AssociateDataShareConsumerMessageRequestTypeDef(
    _RequiredAssociateDataShareConsumerMessageRequestTypeDef,
    _OptionalAssociateDataShareConsumerMessageRequestTypeDef,
):
    pass


AuthenticationProfileTypeDef = TypedDict(
    "AuthenticationProfileTypeDef",
    {
        "AuthenticationProfileName": str,
        "AuthenticationProfileContent": str,
    },
    total=False,
)

_RequiredAuthorizeClusterSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_RequiredAuthorizeClusterSecurityGroupIngressMessageRequestTypeDef",
    {
        "ClusterSecurityGroupName": str,
    },
)
_OptionalAuthorizeClusterSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_OptionalAuthorizeClusterSecurityGroupIngressMessageRequestTypeDef",
    {
        "CIDRIP": str,
        "EC2SecurityGroupName": str,
        "EC2SecurityGroupOwnerId": str,
    },
    total=False,
)


class AuthorizeClusterSecurityGroupIngressMessageRequestTypeDef(
    _RequiredAuthorizeClusterSecurityGroupIngressMessageRequestTypeDef,
    _OptionalAuthorizeClusterSecurityGroupIngressMessageRequestTypeDef,
):
    pass


AuthorizeDataShareMessageRequestTypeDef = TypedDict(
    "AuthorizeDataShareMessageRequestTypeDef",
    {
        "DataShareArn": str,
        "ConsumerIdentifier": str,
    },
)

_RequiredAuthorizeEndpointAccessMessageRequestTypeDef = TypedDict(
    "_RequiredAuthorizeEndpointAccessMessageRequestTypeDef",
    {
        "Account": str,
    },
)
_OptionalAuthorizeEndpointAccessMessageRequestTypeDef = TypedDict(
    "_OptionalAuthorizeEndpointAccessMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "VpcIds": Sequence[str],
    },
    total=False,
)


class AuthorizeEndpointAccessMessageRequestTypeDef(
    _RequiredAuthorizeEndpointAccessMessageRequestTypeDef,
    _OptionalAuthorizeEndpointAccessMessageRequestTypeDef,
):
    pass


_RequiredAuthorizeSnapshotAccessMessageRequestTypeDef = TypedDict(
    "_RequiredAuthorizeSnapshotAccessMessageRequestTypeDef",
    {
        "SnapshotIdentifier": str,
        "AccountWithRestoreAccess": str,
    },
)
_OptionalAuthorizeSnapshotAccessMessageRequestTypeDef = TypedDict(
    "_OptionalAuthorizeSnapshotAccessMessageRequestTypeDef",
    {
        "SnapshotClusterIdentifier": str,
    },
    total=False,
)


class AuthorizeSnapshotAccessMessageRequestTypeDef(
    _RequiredAuthorizeSnapshotAccessMessageRequestTypeDef,
    _OptionalAuthorizeSnapshotAccessMessageRequestTypeDef,
):
    pass


SupportedPlatformTypeDef = TypedDict(
    "SupportedPlatformTypeDef",
    {
        "Name": str,
    },
    total=False,
)

_RequiredDeleteClusterSnapshotMessageTypeDef = TypedDict(
    "_RequiredDeleteClusterSnapshotMessageTypeDef",
    {
        "SnapshotIdentifier": str,
    },
)
_OptionalDeleteClusterSnapshotMessageTypeDef = TypedDict(
    "_OptionalDeleteClusterSnapshotMessageTypeDef",
    {
        "SnapshotClusterIdentifier": str,
    },
    total=False,
)


class DeleteClusterSnapshotMessageTypeDef(
    _RequiredDeleteClusterSnapshotMessageTypeDef, _OptionalDeleteClusterSnapshotMessageTypeDef
):
    pass


SnapshotErrorMessageTypeDef = TypedDict(
    "SnapshotErrorMessageTypeDef",
    {
        "SnapshotIdentifier": str,
        "SnapshotClusterIdentifier": str,
        "FailureCode": str,
        "FailureReason": str,
    },
    total=False,
)

_RequiredBatchModifyClusterSnapshotsMessageRequestTypeDef = TypedDict(
    "_RequiredBatchModifyClusterSnapshotsMessageRequestTypeDef",
    {
        "SnapshotIdentifierList": Sequence[str],
    },
)
_OptionalBatchModifyClusterSnapshotsMessageRequestTypeDef = TypedDict(
    "_OptionalBatchModifyClusterSnapshotsMessageRequestTypeDef",
    {
        "ManualSnapshotRetentionPeriod": int,
        "Force": bool,
    },
    total=False,
)


class BatchModifyClusterSnapshotsMessageRequestTypeDef(
    _RequiredBatchModifyClusterSnapshotsMessageRequestTypeDef,
    _OptionalBatchModifyClusterSnapshotsMessageRequestTypeDef,
):
    pass


CancelResizeMessageRequestTypeDef = TypedDict(
    "CancelResizeMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

ClusterAssociatedToScheduleTypeDef = TypedDict(
    "ClusterAssociatedToScheduleTypeDef",
    {
        "ClusterIdentifier": str,
        "ScheduleAssociationState": ScheduleStateType,
    },
    total=False,
)

RevisionTargetTypeDef = TypedDict(
    "RevisionTargetTypeDef",
    {
        "DatabaseRevision": str,
        "Description": str,
        "DatabaseRevisionReleaseDate": datetime,
    },
    total=False,
)

ClusterIamRoleTypeDef = TypedDict(
    "ClusterIamRoleTypeDef",
    {
        "IamRoleArn": str,
        "ApplyStatus": str,
    },
    total=False,
)

ClusterNodeTypeDef = TypedDict(
    "ClusterNodeTypeDef",
    {
        "NodeRole": str,
        "PrivateIPAddress": str,
        "PublicIPAddress": str,
    },
    total=False,
)

ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
        "Description": str,
        "Source": str,
        "DataType": str,
        "AllowedValues": str,
        "ApplyType": ParameterApplyTypeType,
        "IsModifiable": bool,
        "MinimumEngineVersion": str,
    },
    total=False,
)

ClusterParameterStatusTypeDef = TypedDict(
    "ClusterParameterStatusTypeDef",
    {
        "ParameterName": str,
        "ParameterApplyStatus": str,
        "ParameterApplyErrorDescription": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ClusterSecurityGroupMembershipTypeDef = TypedDict(
    "ClusterSecurityGroupMembershipTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "Status": str,
    },
    total=False,
)

ClusterSnapshotCopyStatusTypeDef = TypedDict(
    "ClusterSnapshotCopyStatusTypeDef",
    {
        "DestinationRegion": str,
        "RetentionPeriod": int,
        "ManualSnapshotRetentionPeriod": int,
        "SnapshotCopyGrantName": str,
    },
    total=False,
)

DataTransferProgressTypeDef = TypedDict(
    "DataTransferProgressTypeDef",
    {
        "Status": str,
        "CurrentRateInMegaBytesPerSecond": float,
        "TotalDataInMegaBytes": int,
        "DataTransferredInMegaBytes": int,
        "EstimatedTimeToCompletionInSeconds": int,
        "ElapsedTimeInSeconds": int,
    },
    total=False,
)

DeferredMaintenanceWindowTypeDef = TypedDict(
    "DeferredMaintenanceWindowTypeDef",
    {
        "DeferMaintenanceIdentifier": str,
        "DeferMaintenanceStartTime": datetime,
        "DeferMaintenanceEndTime": datetime,
    },
    total=False,
)

ElasticIpStatusTypeDef = TypedDict(
    "ElasticIpStatusTypeDef",
    {
        "ElasticIp": str,
        "Status": str,
    },
    total=False,
)

HsmStatusTypeDef = TypedDict(
    "HsmStatusTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
        "HsmConfigurationIdentifier": str,
        "Status": str,
    },
    total=False,
)

PendingModifiedValuesTypeDef = TypedDict(
    "PendingModifiedValuesTypeDef",
    {
        "MasterUserPassword": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "ClusterType": str,
        "ClusterVersion": str,
        "AutomatedSnapshotRetentionPeriod": int,
        "ClusterIdentifier": str,
        "PubliclyAccessible": bool,
        "EnhancedVpcRouting": bool,
        "MaintenanceTrackName": str,
        "EncryptionType": str,
    },
    total=False,
)

ReservedNodeExchangeStatusTypeDef = TypedDict(
    "ReservedNodeExchangeStatusTypeDef",
    {
        "ReservedNodeExchangeRequestId": str,
        "Status": ReservedNodeExchangeStatusTypeType,
        "RequestTime": datetime,
        "SourceReservedNodeId": str,
        "SourceReservedNodeType": str,
        "SourceReservedNodeCount": int,
        "TargetReservedNodeOfferingId": str,
        "TargetReservedNodeType": str,
        "TargetReservedNodeCount": int,
    },
    total=False,
)

ResizeInfoTypeDef = TypedDict(
    "ResizeInfoTypeDef",
    {
        "ResizeType": str,
        "AllowCancelResize": bool,
    },
    total=False,
)

RestoreStatusTypeDef = TypedDict(
    "RestoreStatusTypeDef",
    {
        "Status": str,
        "CurrentRestoreRateInMegaBytesPerSecond": float,
        "SnapshotSizeInMegaBytes": int,
        "ProgressInMegaBytes": int,
        "ElapsedTimeInSeconds": int,
        "EstimatedTimeToCompletionInSeconds": int,
    },
    total=False,
)

VpcSecurityGroupMembershipTypeDef = TypedDict(
    "VpcSecurityGroupMembershipTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

ClusterVersionTypeDef = TypedDict(
    "ClusterVersionTypeDef",
    {
        "ClusterVersion": str,
        "ClusterParameterGroupFamily": str,
        "Description": str,
    },
    total=False,
)

_RequiredCopyClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCopyClusterSnapshotMessageRequestTypeDef",
    {
        "SourceSnapshotIdentifier": str,
        "TargetSnapshotIdentifier": str,
    },
)
_OptionalCopyClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCopyClusterSnapshotMessageRequestTypeDef",
    {
        "SourceSnapshotClusterIdentifier": str,
        "ManualSnapshotRetentionPeriod": int,
    },
    total=False,
)


class CopyClusterSnapshotMessageRequestTypeDef(
    _RequiredCopyClusterSnapshotMessageRequestTypeDef,
    _OptionalCopyClusterSnapshotMessageRequestTypeDef,
):
    pass


CreateAuthenticationProfileMessageRequestTypeDef = TypedDict(
    "CreateAuthenticationProfileMessageRequestTypeDef",
    {
        "AuthenticationProfileName": str,
        "AuthenticationProfileContent": str,
    },
)

_RequiredCreateEndpointAccessMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointAccessMessageRequestTypeDef",
    {
        "EndpointName": str,
        "SubnetGroupName": str,
    },
)
_OptionalCreateEndpointAccessMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointAccessMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "ResourceOwner": str,
        "VpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)


class CreateEndpointAccessMessageRequestTypeDef(
    _RequiredCreateEndpointAccessMessageRequestTypeDef,
    _OptionalCreateEndpointAccessMessageRequestTypeDef,
):
    pass


DataShareAssociationTypeDef = TypedDict(
    "DataShareAssociationTypeDef",
    {
        "ConsumerIdentifier": str,
        "Status": DataShareStatusType,
        "ConsumerRegion": str,
        "CreatedDate": datetime,
        "StatusChangeDate": datetime,
    },
    total=False,
)

DeauthorizeDataShareMessageRequestTypeDef = TypedDict(
    "DeauthorizeDataShareMessageRequestTypeDef",
    {
        "DataShareArn": str,
        "ConsumerIdentifier": str,
    },
)

DeleteAuthenticationProfileMessageRequestTypeDef = TypedDict(
    "DeleteAuthenticationProfileMessageRequestTypeDef",
    {
        "AuthenticationProfileName": str,
    },
)

_RequiredDeleteClusterMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalDeleteClusterMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteClusterMessageRequestTypeDef",
    {
        "SkipFinalClusterSnapshot": bool,
        "FinalClusterSnapshotIdentifier": str,
        "FinalClusterSnapshotRetentionPeriod": int,
    },
    total=False,
)


class DeleteClusterMessageRequestTypeDef(
    _RequiredDeleteClusterMessageRequestTypeDef, _OptionalDeleteClusterMessageRequestTypeDef
):
    pass


DeleteClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "DeleteClusterParameterGroupMessageRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)

DeleteClusterSecurityGroupMessageRequestTypeDef = TypedDict(
    "DeleteClusterSecurityGroupMessageRequestTypeDef",
    {
        "ClusterSecurityGroupName": str,
    },
)

_RequiredDeleteClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteClusterSnapshotMessageRequestTypeDef",
    {
        "SnapshotIdentifier": str,
    },
)
_OptionalDeleteClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteClusterSnapshotMessageRequestTypeDef",
    {
        "SnapshotClusterIdentifier": str,
    },
    total=False,
)


class DeleteClusterSnapshotMessageRequestTypeDef(
    _RequiredDeleteClusterSnapshotMessageRequestTypeDef,
    _OptionalDeleteClusterSnapshotMessageRequestTypeDef,
):
    pass


DeleteClusterSubnetGroupMessageRequestTypeDef = TypedDict(
    "DeleteClusterSubnetGroupMessageRequestTypeDef",
    {
        "ClusterSubnetGroupName": str,
    },
)

DeleteEndpointAccessMessageRequestTypeDef = TypedDict(
    "DeleteEndpointAccessMessageRequestTypeDef",
    {
        "EndpointName": str,
    },
)

DeleteEventSubscriptionMessageRequestTypeDef = TypedDict(
    "DeleteEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)

DeleteHsmClientCertificateMessageRequestTypeDef = TypedDict(
    "DeleteHsmClientCertificateMessageRequestTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
    },
)

DeleteHsmConfigurationMessageRequestTypeDef = TypedDict(
    "DeleteHsmConfigurationMessageRequestTypeDef",
    {
        "HsmConfigurationIdentifier": str,
    },
)

DeleteScheduledActionMessageRequestTypeDef = TypedDict(
    "DeleteScheduledActionMessageRequestTypeDef",
    {
        "ScheduledActionName": str,
    },
)

DeleteSnapshotCopyGrantMessageRequestTypeDef = TypedDict(
    "DeleteSnapshotCopyGrantMessageRequestTypeDef",
    {
        "SnapshotCopyGrantName": str,
    },
)

DeleteSnapshotScheduleMessageRequestTypeDef = TypedDict(
    "DeleteSnapshotScheduleMessageRequestTypeDef",
    {
        "ScheduleIdentifier": str,
    },
)

DeleteTagsMessageRequestTypeDef = TypedDict(
    "DeleteTagsMessageRequestTypeDef",
    {
        "ResourceName": str,
        "TagKeys": Sequence[str],
    },
)

DeleteUsageLimitMessageRequestTypeDef = TypedDict(
    "DeleteUsageLimitMessageRequestTypeDef",
    {
        "UsageLimitId": str,
    },
)

DescribeAccountAttributesMessageRequestTypeDef = TypedDict(
    "DescribeAccountAttributesMessageRequestTypeDef",
    {
        "AttributeNames": Sequence[str],
    },
    total=False,
)

DescribeAuthenticationProfilesMessageRequestTypeDef = TypedDict(
    "DescribeAuthenticationProfilesMessageRequestTypeDef",
    {
        "AuthenticationProfileName": str,
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

DescribeClusterDbRevisionsMessageRequestTypeDef = TypedDict(
    "DescribeClusterDbRevisionsMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeClusterParameterGroupsMessageRequestTypeDef = TypedDict(
    "DescribeClusterParameterGroupsMessageRequestTypeDef",
    {
        "ParameterGroupName": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

_RequiredDescribeClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeClusterParametersMessageRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalDescribeClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeClusterParametersMessageRequestTypeDef",
    {
        "Source": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeClusterParametersMessageRequestTypeDef(
    _RequiredDescribeClusterParametersMessageRequestTypeDef,
    _OptionalDescribeClusterParametersMessageRequestTypeDef,
):
    pass


DescribeClusterSecurityGroupsMessageRequestTypeDef = TypedDict(
    "DescribeClusterSecurityGroupsMessageRequestTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

_RequiredSnapshotSortingEntityTypeDef = TypedDict(
    "_RequiredSnapshotSortingEntityTypeDef",
    {
        "Attribute": SnapshotAttributeToSortByType,
    },
)
_OptionalSnapshotSortingEntityTypeDef = TypedDict(
    "_OptionalSnapshotSortingEntityTypeDef",
    {
        "SortOrder": SortByOrderType,
    },
    total=False,
)


class SnapshotSortingEntityTypeDef(
    _RequiredSnapshotSortingEntityTypeDef, _OptionalSnapshotSortingEntityTypeDef
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeClusterSubnetGroupsMessageRequestTypeDef = TypedDict(
    "DescribeClusterSubnetGroupsMessageRequestTypeDef",
    {
        "ClusterSubnetGroupName": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeClusterTracksMessageRequestTypeDef = TypedDict(
    "DescribeClusterTracksMessageRequestTypeDef",
    {
        "MaintenanceTrackName": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeClusterVersionsMessageRequestTypeDef = TypedDict(
    "DescribeClusterVersionsMessageRequestTypeDef",
    {
        "ClusterVersion": str,
        "ClusterParameterGroupFamily": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeClustersMessageRequestTypeDef = TypedDict(
    "DescribeClustersMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeDataSharesForConsumerMessageRequestTypeDef = TypedDict(
    "DescribeDataSharesForConsumerMessageRequestTypeDef",
    {
        "ConsumerArn": str,
        "Status": DataShareStatusForConsumerType,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDataSharesForProducerMessageRequestTypeDef = TypedDict(
    "DescribeDataSharesForProducerMessageRequestTypeDef",
    {
        "ProducerArn": str,
        "Status": DataShareStatusForProducerType,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDataSharesMessageRequestTypeDef = TypedDict(
    "DescribeDataSharesMessageRequestTypeDef",
    {
        "DataShareArn": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDefaultClusterParametersMessageRequestTypeDef",
    {
        "ParameterGroupFamily": str,
    },
)
_OptionalDescribeDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDefaultClusterParametersMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDefaultClusterParametersMessageRequestTypeDef(
    _RequiredDescribeDefaultClusterParametersMessageRequestTypeDef,
    _OptionalDescribeDefaultClusterParametersMessageRequestTypeDef,
):
    pass


DescribeEndpointAccessMessageRequestTypeDef = TypedDict(
    "DescribeEndpointAccessMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "ResourceOwner": str,
        "EndpointName": str,
        "VpcId": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEndpointAuthorizationMessageRequestTypeDef = TypedDict(
    "DescribeEndpointAuthorizationMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "Account": str,
        "Grantee": bool,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventCategoriesMessageRequestTypeDef = TypedDict(
    "DescribeEventCategoriesMessageRequestTypeDef",
    {
        "SourceType": str,
    },
    total=False,
)

DescribeEventSubscriptionsMessageRequestTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeEventsMessageRequestTypeDef = TypedDict(
    "DescribeEventsMessageRequestTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeHsmClientCertificatesMessageRequestTypeDef = TypedDict(
    "DescribeHsmClientCertificatesMessageRequestTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeHsmConfigurationsMessageRequestTypeDef = TypedDict(
    "DescribeHsmConfigurationsMessageRequestTypeDef",
    {
        "HsmConfigurationIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeLoggingStatusMessageRequestTypeDef = TypedDict(
    "DescribeLoggingStatusMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

NodeConfigurationOptionsFilterTypeDef = TypedDict(
    "NodeConfigurationOptionsFilterTypeDef",
    {
        "Name": NodeConfigurationOptionsFilterNameType,
        "Operator": OperatorTypeType,
        "Values": Sequence[str],
    },
    total=False,
)

DescribeOrderableClusterOptionsMessageRequestTypeDef = TypedDict(
    "DescribeOrderableClusterOptionsMessageRequestTypeDef",
    {
        "ClusterVersion": str,
        "NodeType": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribePartnersInputMessageRequestTypeDef = TypedDict(
    "_RequiredDescribePartnersInputMessageRequestTypeDef",
    {
        "AccountId": str,
        "ClusterIdentifier": str,
    },
)
_OptionalDescribePartnersInputMessageRequestTypeDef = TypedDict(
    "_OptionalDescribePartnersInputMessageRequestTypeDef",
    {
        "DatabaseName": str,
        "PartnerName": str,
    },
    total=False,
)


class DescribePartnersInputMessageRequestTypeDef(
    _RequiredDescribePartnersInputMessageRequestTypeDef,
    _OptionalDescribePartnersInputMessageRequestTypeDef,
):
    pass


PartnerIntegrationInfoTypeDef = TypedDict(
    "PartnerIntegrationInfoTypeDef",
    {
        "DatabaseName": str,
        "PartnerName": str,
        "Status": PartnerIntegrationStatusType,
        "StatusMessage": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

DescribeReservedNodeExchangeStatusInputMessageRequestTypeDef = TypedDict(
    "DescribeReservedNodeExchangeStatusInputMessageRequestTypeDef",
    {
        "ReservedNodeId": str,
        "ReservedNodeExchangeRequestId": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReservedNodeOfferingsMessageRequestTypeDef = TypedDict(
    "DescribeReservedNodeOfferingsMessageRequestTypeDef",
    {
        "ReservedNodeOfferingId": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReservedNodesMessageRequestTypeDef = TypedDict(
    "DescribeReservedNodesMessageRequestTypeDef",
    {
        "ReservedNodeId": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeResizeMessageRequestTypeDef = TypedDict(
    "DescribeResizeMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

ScheduledActionFilterTypeDef = TypedDict(
    "ScheduledActionFilterTypeDef",
    {
        "Name": ScheduledActionFilterNameType,
        "Values": Sequence[str],
    },
)

DescribeSnapshotCopyGrantsMessageRequestTypeDef = TypedDict(
    "DescribeSnapshotCopyGrantsMessageRequestTypeDef",
    {
        "SnapshotCopyGrantName": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeSnapshotSchedulesMessageRequestTypeDef = TypedDict(
    "DescribeSnapshotSchedulesMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "ScheduleIdentifier": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeTableRestoreStatusMessageRequestTypeDef = TypedDict(
    "DescribeTableRestoreStatusMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "TableRestoreRequestId": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeTagsMessageRequestTypeDef = TypedDict(
    "DescribeTagsMessageRequestTypeDef",
    {
        "ResourceName": str,
        "ResourceType": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DescribeUsageLimitsMessageRequestTypeDef = TypedDict(
    "DescribeUsageLimitsMessageRequestTypeDef",
    {
        "UsageLimitId": str,
        "ClusterIdentifier": str,
        "FeatureType": UsageLimitFeatureTypeType,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
    },
    total=False,
)

DisableLoggingMessageRequestTypeDef = TypedDict(
    "DisableLoggingMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

DisableSnapshotCopyMessageRequestTypeDef = TypedDict(
    "DisableSnapshotCopyMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

_RequiredDisassociateDataShareConsumerMessageRequestTypeDef = TypedDict(
    "_RequiredDisassociateDataShareConsumerMessageRequestTypeDef",
    {
        "DataShareArn": str,
    },
)
_OptionalDisassociateDataShareConsumerMessageRequestTypeDef = TypedDict(
    "_OptionalDisassociateDataShareConsumerMessageRequestTypeDef",
    {
        "DisassociateEntireAccount": bool,
        "ConsumerArn": str,
        "ConsumerRegion": str,
    },
    total=False,
)


class DisassociateDataShareConsumerMessageRequestTypeDef(
    _RequiredDisassociateDataShareConsumerMessageRequestTypeDef,
    _OptionalDisassociateDataShareConsumerMessageRequestTypeDef,
):
    pass


_RequiredEnableLoggingMessageRequestTypeDef = TypedDict(
    "_RequiredEnableLoggingMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalEnableLoggingMessageRequestTypeDef = TypedDict(
    "_OptionalEnableLoggingMessageRequestTypeDef",
    {
        "BucketName": str,
        "S3KeyPrefix": str,
        "LogDestinationType": LogDestinationTypeType,
        "LogExports": Sequence[str],
    },
    total=False,
)


class EnableLoggingMessageRequestTypeDef(
    _RequiredEnableLoggingMessageRequestTypeDef, _OptionalEnableLoggingMessageRequestTypeDef
):
    pass


_RequiredEnableSnapshotCopyMessageRequestTypeDef = TypedDict(
    "_RequiredEnableSnapshotCopyMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "DestinationRegion": str,
    },
)
_OptionalEnableSnapshotCopyMessageRequestTypeDef = TypedDict(
    "_OptionalEnableSnapshotCopyMessageRequestTypeDef",
    {
        "RetentionPeriod": int,
        "SnapshotCopyGrantName": str,
        "ManualSnapshotRetentionPeriod": int,
    },
    total=False,
)


class EnableSnapshotCopyMessageRequestTypeDef(
    _RequiredEnableSnapshotCopyMessageRequestTypeDef,
    _OptionalEnableSnapshotCopyMessageRequestTypeDef,
):
    pass


EndpointAuthorizationTypeDef = TypedDict(
    "EndpointAuthorizationTypeDef",
    {
        "Grantor": str,
        "Grantee": str,
        "ClusterIdentifier": str,
        "AuthorizeTime": datetime,
        "ClusterStatus": str,
        "Status": AuthorizationStatusType,
        "AllowedAllVPCs": bool,
        "AllowedVPCs": List[str],
        "EndpointCount": int,
    },
    total=False,
)

EventInfoMapTypeDef = TypedDict(
    "EventInfoMapTypeDef",
    {
        "EventId": str,
        "EventCategories": List[str],
        "EventDescription": str,
        "Severity": str,
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "Message": str,
        "EventCategories": List[str],
        "Severity": str,
        "Date": datetime,
        "EventId": str,
    },
    total=False,
)

_RequiredGetClusterCredentialsMessageRequestTypeDef = TypedDict(
    "_RequiredGetClusterCredentialsMessageRequestTypeDef",
    {
        "DbUser": str,
        "ClusterIdentifier": str,
    },
)
_OptionalGetClusterCredentialsMessageRequestTypeDef = TypedDict(
    "_OptionalGetClusterCredentialsMessageRequestTypeDef",
    {
        "DbName": str,
        "DurationSeconds": int,
        "AutoCreate": bool,
        "DbGroups": Sequence[str],
    },
    total=False,
)


class GetClusterCredentialsMessageRequestTypeDef(
    _RequiredGetClusterCredentialsMessageRequestTypeDef,
    _OptionalGetClusterCredentialsMessageRequestTypeDef,
):
    pass


_RequiredGetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef = TypedDict(
    "_RequiredGetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef",
    {
        "ActionType": ReservedNodeExchangeActionTypeType,
    },
)
_OptionalGetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef = TypedDict(
    "_OptionalGetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class GetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef(
    _RequiredGetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef,
    _OptionalGetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef,
):
    pass


_RequiredGetReservedNodeExchangeOfferingsInputMessageRequestTypeDef = TypedDict(
    "_RequiredGetReservedNodeExchangeOfferingsInputMessageRequestTypeDef",
    {
        "ReservedNodeId": str,
    },
)
_OptionalGetReservedNodeExchangeOfferingsInputMessageRequestTypeDef = TypedDict(
    "_OptionalGetReservedNodeExchangeOfferingsInputMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class GetReservedNodeExchangeOfferingsInputMessageRequestTypeDef(
    _RequiredGetReservedNodeExchangeOfferingsInputMessageRequestTypeDef,
    _OptionalGetReservedNodeExchangeOfferingsInputMessageRequestTypeDef,
):
    pass


_RequiredModifyAquaInputMessageRequestTypeDef = TypedDict(
    "_RequiredModifyAquaInputMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalModifyAquaInputMessageRequestTypeDef = TypedDict(
    "_OptionalModifyAquaInputMessageRequestTypeDef",
    {
        "AquaConfigurationStatus": AquaConfigurationStatusType,
    },
    total=False,
)


class ModifyAquaInputMessageRequestTypeDef(
    _RequiredModifyAquaInputMessageRequestTypeDef, _OptionalModifyAquaInputMessageRequestTypeDef
):
    pass


ModifyAuthenticationProfileMessageRequestTypeDef = TypedDict(
    "ModifyAuthenticationProfileMessageRequestTypeDef",
    {
        "AuthenticationProfileName": str,
        "AuthenticationProfileContent": str,
    },
)

ModifyClusterDbRevisionMessageRequestTypeDef = TypedDict(
    "ModifyClusterDbRevisionMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "RevisionTarget": str,
    },
)

_RequiredModifyClusterIamRolesMessageRequestTypeDef = TypedDict(
    "_RequiredModifyClusterIamRolesMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalModifyClusterIamRolesMessageRequestTypeDef = TypedDict(
    "_OptionalModifyClusterIamRolesMessageRequestTypeDef",
    {
        "AddIamRoles": Sequence[str],
        "RemoveIamRoles": Sequence[str],
        "DefaultIamRoleArn": str,
    },
    total=False,
)


class ModifyClusterIamRolesMessageRequestTypeDef(
    _RequiredModifyClusterIamRolesMessageRequestTypeDef,
    _OptionalModifyClusterIamRolesMessageRequestTypeDef,
):
    pass


_RequiredModifyClusterMaintenanceMessageRequestTypeDef = TypedDict(
    "_RequiredModifyClusterMaintenanceMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalModifyClusterMaintenanceMessageRequestTypeDef = TypedDict(
    "_OptionalModifyClusterMaintenanceMessageRequestTypeDef",
    {
        "DeferMaintenance": bool,
        "DeferMaintenanceIdentifier": str,
        "DeferMaintenanceStartTime": Union[datetime, str],
        "DeferMaintenanceEndTime": Union[datetime, str],
        "DeferMaintenanceDuration": int,
    },
    total=False,
)


class ModifyClusterMaintenanceMessageRequestTypeDef(
    _RequiredModifyClusterMaintenanceMessageRequestTypeDef,
    _OptionalModifyClusterMaintenanceMessageRequestTypeDef,
):
    pass


_RequiredModifyClusterMessageRequestTypeDef = TypedDict(
    "_RequiredModifyClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalModifyClusterMessageRequestTypeDef = TypedDict(
    "_OptionalModifyClusterMessageRequestTypeDef",
    {
        "ClusterType": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "ClusterSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "MasterUserPassword": str,
        "ClusterParameterGroupName": str,
        "AutomatedSnapshotRetentionPeriod": int,
        "ManualSnapshotRetentionPeriod": int,
        "PreferredMaintenanceWindow": str,
        "ClusterVersion": str,
        "AllowVersionUpgrade": bool,
        "HsmClientCertificateIdentifier": str,
        "HsmConfigurationIdentifier": str,
        "NewClusterIdentifier": str,
        "PubliclyAccessible": bool,
        "ElasticIp": str,
        "EnhancedVpcRouting": bool,
        "MaintenanceTrackName": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "AvailabilityZoneRelocation": bool,
        "AvailabilityZone": str,
        "Port": int,
    },
    total=False,
)


class ModifyClusterMessageRequestTypeDef(
    _RequiredModifyClusterMessageRequestTypeDef, _OptionalModifyClusterMessageRequestTypeDef
):
    pass


_RequiredModifyClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredModifyClusterSnapshotMessageRequestTypeDef",
    {
        "SnapshotIdentifier": str,
    },
)
_OptionalModifyClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalModifyClusterSnapshotMessageRequestTypeDef",
    {
        "ManualSnapshotRetentionPeriod": int,
        "Force": bool,
    },
    total=False,
)


class ModifyClusterSnapshotMessageRequestTypeDef(
    _RequiredModifyClusterSnapshotMessageRequestTypeDef,
    _OptionalModifyClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredModifyClusterSnapshotScheduleMessageRequestTypeDef = TypedDict(
    "_RequiredModifyClusterSnapshotScheduleMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalModifyClusterSnapshotScheduleMessageRequestTypeDef = TypedDict(
    "_OptionalModifyClusterSnapshotScheduleMessageRequestTypeDef",
    {
        "ScheduleIdentifier": str,
        "DisassociateSchedule": bool,
    },
    total=False,
)


class ModifyClusterSnapshotScheduleMessageRequestTypeDef(
    _RequiredModifyClusterSnapshotScheduleMessageRequestTypeDef,
    _OptionalModifyClusterSnapshotScheduleMessageRequestTypeDef,
):
    pass


_RequiredModifyClusterSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyClusterSubnetGroupMessageRequestTypeDef",
    {
        "ClusterSubnetGroupName": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalModifyClusterSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyClusterSubnetGroupMessageRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class ModifyClusterSubnetGroupMessageRequestTypeDef(
    _RequiredModifyClusterSubnetGroupMessageRequestTypeDef,
    _OptionalModifyClusterSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredModifyEndpointAccessMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEndpointAccessMessageRequestTypeDef",
    {
        "EndpointName": str,
    },
)
_OptionalModifyEndpointAccessMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEndpointAccessMessageRequestTypeDef",
    {
        "VpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)


class ModifyEndpointAccessMessageRequestTypeDef(
    _RequiredModifyEndpointAccessMessageRequestTypeDef,
    _OptionalModifyEndpointAccessMessageRequestTypeDef,
):
    pass


_RequiredModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)
_OptionalModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SnsTopicArn": str,
        "SourceType": str,
        "SourceIds": Sequence[str],
        "EventCategories": Sequence[str],
        "Severity": str,
        "Enabled": bool,
    },
    total=False,
)


class ModifyEventSubscriptionMessageRequestTypeDef(
    _RequiredModifyEventSubscriptionMessageRequestTypeDef,
    _OptionalModifyEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredModifySnapshotCopyRetentionPeriodMessageRequestTypeDef = TypedDict(
    "_RequiredModifySnapshotCopyRetentionPeriodMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "RetentionPeriod": int,
    },
)
_OptionalModifySnapshotCopyRetentionPeriodMessageRequestTypeDef = TypedDict(
    "_OptionalModifySnapshotCopyRetentionPeriodMessageRequestTypeDef",
    {
        "Manual": bool,
    },
    total=False,
)


class ModifySnapshotCopyRetentionPeriodMessageRequestTypeDef(
    _RequiredModifySnapshotCopyRetentionPeriodMessageRequestTypeDef,
    _OptionalModifySnapshotCopyRetentionPeriodMessageRequestTypeDef,
):
    pass


ModifySnapshotScheduleMessageRequestTypeDef = TypedDict(
    "ModifySnapshotScheduleMessageRequestTypeDef",
    {
        "ScheduleIdentifier": str,
        "ScheduleDefinitions": Sequence[str],
    },
)

_RequiredModifyUsageLimitMessageRequestTypeDef = TypedDict(
    "_RequiredModifyUsageLimitMessageRequestTypeDef",
    {
        "UsageLimitId": str,
    },
)
_OptionalModifyUsageLimitMessageRequestTypeDef = TypedDict(
    "_OptionalModifyUsageLimitMessageRequestTypeDef",
    {
        "Amount": int,
        "BreachAction": UsageLimitBreachActionType,
    },
    total=False,
)


class ModifyUsageLimitMessageRequestTypeDef(
    _RequiredModifyUsageLimitMessageRequestTypeDef, _OptionalModifyUsageLimitMessageRequestTypeDef
):
    pass


NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "NetworkInterfaceId": str,
        "SubnetId": str,
        "PrivateIpAddress": str,
        "AvailabilityZone": str,
    },
    total=False,
)

NodeConfigurationOptionTypeDef = TypedDict(
    "NodeConfigurationOptionTypeDef",
    {
        "NodeType": str,
        "NumberOfNodes": int,
        "EstimatedDiskUtilizationPercent": float,
        "Mode": ModeType,
    },
    total=False,
)

PartnerIntegrationInputMessageRequestTypeDef = TypedDict(
    "PartnerIntegrationInputMessageRequestTypeDef",
    {
        "AccountId": str,
        "ClusterIdentifier": str,
        "DatabaseName": str,
        "PartnerName": str,
    },
)

PauseClusterMessageRequestTypeDef = TypedDict(
    "PauseClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

PauseClusterMessageTypeDef = TypedDict(
    "PauseClusterMessageTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

_RequiredPurchaseReservedNodeOfferingMessageRequestTypeDef = TypedDict(
    "_RequiredPurchaseReservedNodeOfferingMessageRequestTypeDef",
    {
        "ReservedNodeOfferingId": str,
    },
)
_OptionalPurchaseReservedNodeOfferingMessageRequestTypeDef = TypedDict(
    "_OptionalPurchaseReservedNodeOfferingMessageRequestTypeDef",
    {
        "NodeCount": int,
    },
    total=False,
)


class PurchaseReservedNodeOfferingMessageRequestTypeDef(
    _RequiredPurchaseReservedNodeOfferingMessageRequestTypeDef,
    _OptionalPurchaseReservedNodeOfferingMessageRequestTypeDef,
):
    pass


RebootClusterMessageRequestTypeDef = TypedDict(
    "RebootClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

RecurringChargeTypeDef = TypedDict(
    "RecurringChargeTypeDef",
    {
        "RecurringChargeAmount": float,
        "RecurringChargeFrequency": str,
    },
    total=False,
)

RejectDataShareMessageRequestTypeDef = TypedDict(
    "RejectDataShareMessageRequestTypeDef",
    {
        "DataShareArn": str,
    },
)

_RequiredResizeClusterMessageRequestTypeDef = TypedDict(
    "_RequiredResizeClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalResizeClusterMessageRequestTypeDef = TypedDict(
    "_OptionalResizeClusterMessageRequestTypeDef",
    {
        "ClusterType": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "Classic": bool,
        "ReservedNodeId": str,
        "TargetReservedNodeOfferingId": str,
    },
    total=False,
)


class ResizeClusterMessageRequestTypeDef(
    _RequiredResizeClusterMessageRequestTypeDef, _OptionalResizeClusterMessageRequestTypeDef
):
    pass


_RequiredResizeClusterMessageTypeDef = TypedDict(
    "_RequiredResizeClusterMessageTypeDef",
    {
        "ClusterIdentifier": str,
    },
)
_OptionalResizeClusterMessageTypeDef = TypedDict(
    "_OptionalResizeClusterMessageTypeDef",
    {
        "ClusterType": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "Classic": bool,
        "ReservedNodeId": str,
        "TargetReservedNodeOfferingId": str,
    },
    total=False,
)


class ResizeClusterMessageTypeDef(
    _RequiredResizeClusterMessageTypeDef, _OptionalResizeClusterMessageTypeDef
):
    pass


_RequiredRestoreFromClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreFromClusterSnapshotMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
    },
)
_OptionalRestoreFromClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreFromClusterSnapshotMessageRequestTypeDef",
    {
        "SnapshotClusterIdentifier": str,
        "Port": int,
        "AvailabilityZone": str,
        "AllowVersionUpgrade": bool,
        "ClusterSubnetGroupName": str,
        "PubliclyAccessible": bool,
        "OwnerAccount": str,
        "HsmClientCertificateIdentifier": str,
        "HsmConfigurationIdentifier": str,
        "ElasticIp": str,
        "ClusterParameterGroupName": str,
        "ClusterSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "PreferredMaintenanceWindow": str,
        "AutomatedSnapshotRetentionPeriod": int,
        "ManualSnapshotRetentionPeriod": int,
        "KmsKeyId": str,
        "NodeType": str,
        "EnhancedVpcRouting": bool,
        "AdditionalInfo": str,
        "IamRoles": Sequence[str],
        "MaintenanceTrackName": str,
        "SnapshotScheduleIdentifier": str,
        "NumberOfNodes": int,
        "AvailabilityZoneRelocation": bool,
        "AquaConfigurationStatus": AquaConfigurationStatusType,
        "DefaultIamRoleArn": str,
        "ReservedNodeId": str,
        "TargetReservedNodeOfferingId": str,
        "Encrypted": bool,
    },
    total=False,
)


class RestoreFromClusterSnapshotMessageRequestTypeDef(
    _RequiredRestoreFromClusterSnapshotMessageRequestTypeDef,
    _OptionalRestoreFromClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredRestoreTableFromClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreTableFromClusterSnapshotMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "SourceDatabaseName": str,
        "SourceTableName": str,
        "NewTableName": str,
    },
)
_OptionalRestoreTableFromClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreTableFromClusterSnapshotMessageRequestTypeDef",
    {
        "SourceSchemaName": str,
        "TargetDatabaseName": str,
        "TargetSchemaName": str,
        "EnableCaseSensitiveIdentifier": bool,
    },
    total=False,
)


class RestoreTableFromClusterSnapshotMessageRequestTypeDef(
    _RequiredRestoreTableFromClusterSnapshotMessageRequestTypeDef,
    _OptionalRestoreTableFromClusterSnapshotMessageRequestTypeDef,
):
    pass


TableRestoreStatusTypeDef = TypedDict(
    "TableRestoreStatusTypeDef",
    {
        "TableRestoreRequestId": str,
        "Status": TableRestoreStatusTypeType,
        "Message": str,
        "RequestTime": datetime,
        "ProgressInMegaBytes": int,
        "TotalDataInMegaBytes": int,
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "SourceDatabaseName": str,
        "SourceSchemaName": str,
        "SourceTableName": str,
        "TargetDatabaseName": str,
        "TargetSchemaName": str,
        "NewTableName": str,
    },
    total=False,
)

ResumeClusterMessageRequestTypeDef = TypedDict(
    "ResumeClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

ResumeClusterMessageTypeDef = TypedDict(
    "ResumeClusterMessageTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

_RequiredRevokeClusterSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_RequiredRevokeClusterSecurityGroupIngressMessageRequestTypeDef",
    {
        "ClusterSecurityGroupName": str,
    },
)
_OptionalRevokeClusterSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_OptionalRevokeClusterSecurityGroupIngressMessageRequestTypeDef",
    {
        "CIDRIP": str,
        "EC2SecurityGroupName": str,
        "EC2SecurityGroupOwnerId": str,
    },
    total=False,
)


class RevokeClusterSecurityGroupIngressMessageRequestTypeDef(
    _RequiredRevokeClusterSecurityGroupIngressMessageRequestTypeDef,
    _OptionalRevokeClusterSecurityGroupIngressMessageRequestTypeDef,
):
    pass


RevokeEndpointAccessMessageRequestTypeDef = TypedDict(
    "RevokeEndpointAccessMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "Account": str,
        "VpcIds": Sequence[str],
        "Force": bool,
    },
    total=False,
)

_RequiredRevokeSnapshotAccessMessageRequestTypeDef = TypedDict(
    "_RequiredRevokeSnapshotAccessMessageRequestTypeDef",
    {
        "SnapshotIdentifier": str,
        "AccountWithRestoreAccess": str,
    },
)
_OptionalRevokeSnapshotAccessMessageRequestTypeDef = TypedDict(
    "_OptionalRevokeSnapshotAccessMessageRequestTypeDef",
    {
        "SnapshotClusterIdentifier": str,
    },
    total=False,
)


class RevokeSnapshotAccessMessageRequestTypeDef(
    _RequiredRevokeSnapshotAccessMessageRequestTypeDef,
    _OptionalRevokeSnapshotAccessMessageRequestTypeDef,
):
    pass


RotateEncryptionKeyMessageRequestTypeDef = TypedDict(
    "RotateEncryptionKeyMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
    },
)

SupportedOperationTypeDef = TypedDict(
    "SupportedOperationTypeDef",
    {
        "OperationName": str,
    },
    total=False,
)

_RequiredUpdatePartnerStatusInputMessageRequestTypeDef = TypedDict(
    "_RequiredUpdatePartnerStatusInputMessageRequestTypeDef",
    {
        "AccountId": str,
        "ClusterIdentifier": str,
        "DatabaseName": str,
        "PartnerName": str,
        "Status": PartnerIntegrationStatusType,
    },
)
_OptionalUpdatePartnerStatusInputMessageRequestTypeDef = TypedDict(
    "_OptionalUpdatePartnerStatusInputMessageRequestTypeDef",
    {
        "StatusMessage": str,
    },
    total=False,
)


class UpdatePartnerStatusInputMessageRequestTypeDef(
    _RequiredUpdatePartnerStatusInputMessageRequestTypeDef,
    _OptionalUpdatePartnerStatusInputMessageRequestTypeDef,
):
    pass


ClusterCredentialsTypeDef = TypedDict(
    "ClusterCredentialsTypeDef",
    {
        "DbUser": str,
        "DbPassword": str,
        "Expiration": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterParameterGroupNameMessageTypeDef = TypedDict(
    "ClusterParameterGroupNameMessageTypeDef",
    {
        "ParameterGroupName": str,
        "ParameterGroupStatus": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAuthenticationProfileResultTypeDef = TypedDict(
    "CreateAuthenticationProfileResultTypeDef",
    {
        "AuthenticationProfileName": str,
        "AuthenticationProfileContent": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomerStorageMessageTypeDef = TypedDict(
    "CustomerStorageMessageTypeDef",
    {
        "TotalBackupSizeInMegaBytes": float,
        "TotalProvisionedStorageInMegaBytes": float,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAuthenticationProfileResultTypeDef = TypedDict(
    "DeleteAuthenticationProfileResultTypeDef",
    {
        "AuthenticationProfileName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointAuthorizationResponseMetadataTypeDef = TypedDict(
    "EndpointAuthorizationResponseMetadataTypeDef",
    {
        "Grantor": str,
        "Grantee": str,
        "ClusterIdentifier": str,
        "AuthorizeTime": datetime,
        "ClusterStatus": str,
        "Status": AuthorizationStatusType,
        "AllowedAllVPCs": bool,
        "AllowedVPCs": List[str],
        "EndpointCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoggingStatusTypeDef = TypedDict(
    "LoggingStatusTypeDef",
    {
        "LoggingEnabled": bool,
        "BucketName": str,
        "S3KeyPrefix": str,
        "LastSuccessfulDeliveryTime": datetime,
        "LastFailureTime": datetime,
        "LastFailureMessage": str,
        "LogDestinationType": LogDestinationTypeType,
        "LogExports": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyAuthenticationProfileResultTypeDef = TypedDict(
    "ModifyAuthenticationProfileResultTypeDef",
    {
        "AuthenticationProfileName": str,
        "AuthenticationProfileContent": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PartnerIntegrationOutputMessageTypeDef = TypedDict(
    "PartnerIntegrationOutputMessageTypeDef",
    {
        "DatabaseName": str,
        "PartnerName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResizeProgressMessageTypeDef = TypedDict(
    "ResizeProgressMessageTypeDef",
    {
        "TargetNodeType": str,
        "TargetNumberOfNodes": int,
        "TargetClusterType": str,
        "Status": str,
        "ImportTablesCompleted": List[str],
        "ImportTablesInProgress": List[str],
        "ImportTablesNotStarted": List[str],
        "AvgResizeRateInMegaBytesPerSecond": float,
        "TotalResizeDataInMegaBytes": int,
        "ProgressInMegaBytes": int,
        "ElapsedTimeInSeconds": int,
        "EstimatedTimeToCompletionInSeconds": int,
        "ResizeType": str,
        "Message": str,
        "TargetEncryptionType": str,
        "DataTransferProgressPercent": float,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AccountAttributeTypeDef = TypedDict(
    "AccountAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": List[AttributeValueTargetTypeDef],
    },
    total=False,
)

ModifyAquaOutputMessageTypeDef = TypedDict(
    "ModifyAquaOutputMessageTypeDef",
    {
        "AquaConfiguration": AquaConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAuthenticationProfilesResultTypeDef = TypedDict(
    "DescribeAuthenticationProfilesResultTypeDef",
    {
        "AuthenticationProfiles": List[AuthenticationProfileTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
        "SupportedPlatforms": List[SupportedPlatformTypeDef],
    },
    total=False,
)

BatchDeleteClusterSnapshotsRequestRequestTypeDef = TypedDict(
    "BatchDeleteClusterSnapshotsRequestRequestTypeDef",
    {
        "Identifiers": Sequence[DeleteClusterSnapshotMessageTypeDef],
    },
)

BatchDeleteClusterSnapshotsResultTypeDef = TypedDict(
    "BatchDeleteClusterSnapshotsResultTypeDef",
    {
        "Resources": List[str],
        "Errors": List[SnapshotErrorMessageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchModifyClusterSnapshotsOutputMessageTypeDef = TypedDict(
    "BatchModifyClusterSnapshotsOutputMessageTypeDef",
    {
        "Resources": List[str],
        "Errors": List[SnapshotErrorMessageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterDbRevisionTypeDef = TypedDict(
    "ClusterDbRevisionTypeDef",
    {
        "ClusterIdentifier": str,
        "CurrentDatabaseRevision": str,
        "DatabaseRevisionReleaseDate": datetime,
        "RevisionTargets": List[RevisionTargetTypeDef],
    },
    total=False,
)

ClusterParameterGroupDetailsTypeDef = TypedDict(
    "ClusterParameterGroupDetailsTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefaultClusterParametersTypeDef = TypedDict(
    "DefaultClusterParametersTypeDef",
    {
        "ParameterGroupFamily": str,
        "Marker": str,
        "Parameters": List[ParameterTypeDef],
    },
    total=False,
)

ModifyClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "ModifyClusterParameterGroupMessageRequestTypeDef",
    {
        "ParameterGroupName": str,
        "Parameters": Sequence[ParameterTypeDef],
    },
)

_RequiredResetClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredResetClusterParameterGroupMessageRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalResetClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalResetClusterParameterGroupMessageRequestTypeDef",
    {
        "ResetAllParameters": bool,
        "Parameters": Sequence[ParameterTypeDef],
    },
    total=False,
)


class ResetClusterParameterGroupMessageRequestTypeDef(
    _RequiredResetClusterParameterGroupMessageRequestTypeDef,
    _OptionalResetClusterParameterGroupMessageRequestTypeDef,
):
    pass


ClusterParameterGroupStatusTypeDef = TypedDict(
    "ClusterParameterGroupStatusTypeDef",
    {
        "ParameterGroupName": str,
        "ParameterApplyStatus": str,
        "ClusterParameterStatusList": List[ClusterParameterStatusTypeDef],
    },
    total=False,
)

ClusterParameterGroupTypeDef = TypedDict(
    "ClusterParameterGroupTypeDef",
    {
        "ParameterGroupName": str,
        "ParameterGroupFamily": str,
        "Description": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

_RequiredCreateClusterMessageRequestTypeDef = TypedDict(
    "_RequiredCreateClusterMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "NodeType": str,
        "MasterUsername": str,
        "MasterUserPassword": str,
    },
)
_OptionalCreateClusterMessageRequestTypeDef = TypedDict(
    "_OptionalCreateClusterMessageRequestTypeDef",
    {
        "DBName": str,
        "ClusterType": str,
        "ClusterSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "ClusterSubnetGroupName": str,
        "AvailabilityZone": str,
        "PreferredMaintenanceWindow": str,
        "ClusterParameterGroupName": str,
        "AutomatedSnapshotRetentionPeriod": int,
        "ManualSnapshotRetentionPeriod": int,
        "Port": int,
        "ClusterVersion": str,
        "AllowVersionUpgrade": bool,
        "NumberOfNodes": int,
        "PubliclyAccessible": bool,
        "Encrypted": bool,
        "HsmClientCertificateIdentifier": str,
        "HsmConfigurationIdentifier": str,
        "ElasticIp": str,
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnhancedVpcRouting": bool,
        "AdditionalInfo": str,
        "IamRoles": Sequence[str],
        "MaintenanceTrackName": str,
        "SnapshotScheduleIdentifier": str,
        "AvailabilityZoneRelocation": bool,
        "AquaConfigurationStatus": AquaConfigurationStatusType,
        "DefaultIamRoleArn": str,
        "LoadSampleData": str,
    },
    total=False,
)


class CreateClusterMessageRequestTypeDef(
    _RequiredCreateClusterMessageRequestTypeDef, _OptionalCreateClusterMessageRequestTypeDef
):
    pass


_RequiredCreateClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateClusterParameterGroupMessageRequestTypeDef",
    {
        "ParameterGroupName": str,
        "ParameterGroupFamily": str,
        "Description": str,
    },
)
_OptionalCreateClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateClusterParameterGroupMessageRequestTypeDef(
    _RequiredCreateClusterParameterGroupMessageRequestTypeDef,
    _OptionalCreateClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateClusterSecurityGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateClusterSecurityGroupMessageRequestTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "Description": str,
    },
)
_OptionalCreateClusterSecurityGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateClusterSecurityGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateClusterSecurityGroupMessageRequestTypeDef(
    _RequiredCreateClusterSecurityGroupMessageRequestTypeDef,
    _OptionalCreateClusterSecurityGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCreateClusterSnapshotMessageRequestTypeDef",
    {
        "SnapshotIdentifier": str,
        "ClusterIdentifier": str,
    },
)
_OptionalCreateClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCreateClusterSnapshotMessageRequestTypeDef",
    {
        "ManualSnapshotRetentionPeriod": int,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateClusterSnapshotMessageRequestTypeDef(
    _RequiredCreateClusterSnapshotMessageRequestTypeDef,
    _OptionalCreateClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCreateClusterSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateClusterSubnetGroupMessageRequestTypeDef",
    {
        "ClusterSubnetGroupName": str,
        "Description": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateClusterSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateClusterSubnetGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateClusterSubnetGroupMessageRequestTypeDef(
    _RequiredCreateClusterSubnetGroupMessageRequestTypeDef,
    _OptionalCreateClusterSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SnsTopicArn": str,
    },
)
_OptionalCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SourceType": str,
        "SourceIds": Sequence[str],
        "EventCategories": Sequence[str],
        "Severity": str,
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEventSubscriptionMessageRequestTypeDef(
    _RequiredCreateEventSubscriptionMessageRequestTypeDef,
    _OptionalCreateEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredCreateHsmClientCertificateMessageRequestTypeDef = TypedDict(
    "_RequiredCreateHsmClientCertificateMessageRequestTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
    },
)
_OptionalCreateHsmClientCertificateMessageRequestTypeDef = TypedDict(
    "_OptionalCreateHsmClientCertificateMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateHsmClientCertificateMessageRequestTypeDef(
    _RequiredCreateHsmClientCertificateMessageRequestTypeDef,
    _OptionalCreateHsmClientCertificateMessageRequestTypeDef,
):
    pass


_RequiredCreateHsmConfigurationMessageRequestTypeDef = TypedDict(
    "_RequiredCreateHsmConfigurationMessageRequestTypeDef",
    {
        "HsmConfigurationIdentifier": str,
        "Description": str,
        "HsmIpAddress": str,
        "HsmPartitionName": str,
        "HsmPartitionPassword": str,
        "HsmServerPublicCertificate": str,
    },
)
_OptionalCreateHsmConfigurationMessageRequestTypeDef = TypedDict(
    "_OptionalCreateHsmConfigurationMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateHsmConfigurationMessageRequestTypeDef(
    _RequiredCreateHsmConfigurationMessageRequestTypeDef,
    _OptionalCreateHsmConfigurationMessageRequestTypeDef,
):
    pass


_RequiredCreateSnapshotCopyGrantMessageRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotCopyGrantMessageRequestTypeDef",
    {
        "SnapshotCopyGrantName": str,
    },
)
_OptionalCreateSnapshotCopyGrantMessageRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotCopyGrantMessageRequestTypeDef",
    {
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSnapshotCopyGrantMessageRequestTypeDef(
    _RequiredCreateSnapshotCopyGrantMessageRequestTypeDef,
    _OptionalCreateSnapshotCopyGrantMessageRequestTypeDef,
):
    pass


CreateSnapshotScheduleMessageRequestTypeDef = TypedDict(
    "CreateSnapshotScheduleMessageRequestTypeDef",
    {
        "ScheduleDefinitions": Sequence[str],
        "ScheduleIdentifier": str,
        "ScheduleDescription": str,
        "Tags": Sequence[TagTypeDef],
        "DryRun": bool,
        "NextInvocations": int,
    },
    total=False,
)

CreateTagsMessageRequestTypeDef = TypedDict(
    "CreateTagsMessageRequestTypeDef",
    {
        "ResourceName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateUsageLimitMessageRequestTypeDef = TypedDict(
    "_RequiredCreateUsageLimitMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "FeatureType": UsageLimitFeatureTypeType,
        "LimitType": UsageLimitLimitTypeType,
        "Amount": int,
    },
)
_OptionalCreateUsageLimitMessageRequestTypeDef = TypedDict(
    "_OptionalCreateUsageLimitMessageRequestTypeDef",
    {
        "Period": UsageLimitPeriodType,
        "BreachAction": UsageLimitBreachActionType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUsageLimitMessageRequestTypeDef(
    _RequiredCreateUsageLimitMessageRequestTypeDef, _OptionalCreateUsageLimitMessageRequestTypeDef
):
    pass


EC2SecurityGroupTypeDef = TypedDict(
    "EC2SecurityGroupTypeDef",
    {
        "Status": str,
        "EC2SecurityGroupName": str,
        "EC2SecurityGroupOwnerId": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": datetime,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Severity": str,
        "Enabled": bool,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

HsmClientCertificateTypeDef = TypedDict(
    "HsmClientCertificateTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
        "HsmClientCertificatePublicKey": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

HsmConfigurationTypeDef = TypedDict(
    "HsmConfigurationTypeDef",
    {
        "HsmConfigurationIdentifier": str,
        "Description": str,
        "HsmIpAddress": str,
        "HsmPartitionName": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

IPRangeTypeDef = TypedDict(
    "IPRangeTypeDef",
    {
        "Status": str,
        "CIDRIP": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

SnapshotCopyGrantTypeDef = TypedDict(
    "SnapshotCopyGrantTypeDef",
    {
        "SnapshotCopyGrantName": str,
        "KmsKeyId": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

SnapshotScheduleResponseMetadataTypeDef = TypedDict(
    "SnapshotScheduleResponseMetadataTypeDef",
    {
        "ScheduleDefinitions": List[str],
        "ScheduleIdentifier": str,
        "ScheduleDescription": str,
        "Tags": List[TagTypeDef],
        "NextInvocations": List[datetime],
        "AssociatedClusterCount": int,
        "AssociatedClusters": List[ClusterAssociatedToScheduleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SnapshotScheduleTypeDef = TypedDict(
    "SnapshotScheduleTypeDef",
    {
        "ScheduleDefinitions": List[str],
        "ScheduleIdentifier": str,
        "ScheduleDescription": str,
        "Tags": List[TagTypeDef],
        "NextInvocations": List[datetime],
        "AssociatedClusterCount": int,
        "AssociatedClusters": List[ClusterAssociatedToScheduleTypeDef],
    },
    total=False,
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "SnapshotIdentifier": str,
        "ClusterIdentifier": str,
        "SnapshotCreateTime": datetime,
        "Status": str,
        "Port": int,
        "AvailabilityZone": str,
        "ClusterCreateTime": datetime,
        "MasterUsername": str,
        "ClusterVersion": str,
        "EngineFullVersion": str,
        "SnapshotType": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "DBName": str,
        "VpcId": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "EncryptedWithHSM": bool,
        "AccountsWithRestoreAccess": List[AccountWithRestoreAccessTypeDef],
        "OwnerAccount": str,
        "TotalBackupSizeInMegaBytes": float,
        "ActualIncrementalBackupSizeInMegaBytes": float,
        "BackupProgressInMegaBytes": float,
        "CurrentBackupRateInMegaBytesPerSecond": float,
        "EstimatedSecondsToCompletion": int,
        "ElapsedTimeInSeconds": int,
        "SourceRegion": str,
        "Tags": List[TagTypeDef],
        "RestorableNodeTypes": List[str],
        "EnhancedVpcRouting": bool,
        "MaintenanceTrackName": str,
        "ManualSnapshotRetentionPeriod": int,
        "ManualSnapshotRemainingDays": int,
        "SnapshotRetentionStartTime": datetime,
    },
    total=False,
)

TaggedResourceTypeDef = TypedDict(
    "TaggedResourceTypeDef",
    {
        "Tag": TagTypeDef,
        "ResourceName": str,
        "ResourceType": str,
    },
    total=False,
)

UsageLimitResponseMetadataTypeDef = TypedDict(
    "UsageLimitResponseMetadataTypeDef",
    {
        "UsageLimitId": str,
        "ClusterIdentifier": str,
        "FeatureType": UsageLimitFeatureTypeType,
        "LimitType": UsageLimitLimitTypeType,
        "Amount": int,
        "Period": UsageLimitPeriodType,
        "BreachAction": UsageLimitBreachActionType,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UsageLimitTypeDef = TypedDict(
    "UsageLimitTypeDef",
    {
        "UsageLimitId": str,
        "ClusterIdentifier": str,
        "FeatureType": UsageLimitFeatureTypeType,
        "LimitType": UsageLimitLimitTypeType,
        "Amount": int,
        "Period": UsageLimitPeriodType,
        "BreachAction": UsageLimitBreachActionType,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

DescribeReservedNodeExchangeStatusOutputMessageTypeDef = TypedDict(
    "DescribeReservedNodeExchangeStatusOutputMessageTypeDef",
    {
        "ReservedNodeExchangeStatusDetails": List[ReservedNodeExchangeStatusTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterVersionsMessageTypeDef = TypedDict(
    "ClusterVersionsMessageTypeDef",
    {
        "Marker": str,
        "ClusterVersions": List[ClusterVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataShareResponseMetadataTypeDef = TypedDict(
    "DataShareResponseMetadataTypeDef",
    {
        "DataShareArn": str,
        "ProducerArn": str,
        "AllowPubliclyAccessibleConsumers": bool,
        "DataShareAssociations": List[DataShareAssociationTypeDef],
        "ManagedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataShareTypeDef = TypedDict(
    "DataShareTypeDef",
    {
        "DataShareArn": str,
        "ProducerArn": str,
        "AllowPubliclyAccessibleConsumers": bool,
        "DataShareAssociations": List[DataShareAssociationTypeDef],
        "ManagedBy": str,
    },
    total=False,
)

DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef = TypedDict(
    "DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef",
    {
        "ParameterGroupName": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalDescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef",
    {
        "Source": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef(
    _RequiredDescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef,
    _OptionalDescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef,
):
    pass


DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef = TypedDict(
    "DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef",
    {
        "ClusterSubnetGroupName": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef = TypedDict(
    "DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef",
    {
        "MaintenanceTrackName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef = TypedDict(
    "DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef",
    {
        "ClusterVersion": str,
        "ClusterParameterGroupFamily": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClustersMessageDescribeClustersPaginateTypeDef = TypedDict(
    "DescribeClustersMessageDescribeClustersPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef = TypedDict(
    "DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef",
    {
        "ConsumerArn": str,
        "Status": DataShareStatusForConsumerType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef = TypedDict(
    "DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef",
    {
        "ProducerArn": str,
        "Status": DataShareStatusForProducerType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef = TypedDict(
    "DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef",
    {
        "DataShareArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef",
    {
        "ParameterGroupFamily": str,
    },
)
_OptionalDescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef(
    _RequiredDescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef,
    _OptionalDescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef,
):
    pass


DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef = TypedDict(
    "DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "ResourceOwner": str,
        "EndpointName": str,
        "VpcId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef = TypedDict(
    "DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "Account": str,
        "Grantee": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    {
        "SubscriptionName": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventsMessageDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef = TypedDict(
    "DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef = TypedDict(
    "DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef",
    {
        "HsmConfigurationIdentifier": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef = TypedDict(
    "DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef",
    {
        "ClusterVersion": str,
        "NodeType": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef = TypedDict(
    "DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef",
    {
        "ReservedNodeId": str,
        "ReservedNodeExchangeRequestId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef = TypedDict(
    "DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef",
    {
        "ReservedNodeOfferingId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef = TypedDict(
    "DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef",
    {
        "ReservedNodeId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef = TypedDict(
    "DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef",
    {
        "SnapshotCopyGrantName": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef = TypedDict(
    "DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "ScheduleIdentifier": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef = TypedDict(
    "DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "TableRestoreRequestId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeTagsMessageDescribeTagsPaginateTypeDef = TypedDict(
    "DescribeTagsMessageDescribeTagsPaginateTypeDef",
    {
        "ResourceName": str,
        "ResourceType": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef = TypedDict(
    "DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef",
    {
        "UsageLimitId": str,
        "ClusterIdentifier": str,
        "FeatureType": UsageLimitFeatureTypeType,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef = TypedDict(
    "_RequiredGetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef",
    {
        "ActionType": ReservedNodeExchangeActionTypeType,
    },
)
_OptionalGetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef = TypedDict(
    "_OptionalGetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef(
    _RequiredGetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef,
    _OptionalGetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef,
):
    pass


_RequiredGetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef = TypedDict(
    "_RequiredGetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef",
    {
        "ReservedNodeId": str,
    },
)
_OptionalGetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef = TypedDict(
    "_OptionalGetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef(
    _RequiredGetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef,
    _OptionalGetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef,
):
    pass


DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef = TypedDict(
    "DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "SnapshotType": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "OwnerAccount": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "ClusterExists": bool,
        "SortingEntities": Sequence[SnapshotSortingEntityTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClusterSnapshotsMessageRequestTypeDef = TypedDict(
    "DescribeClusterSnapshotsMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "SnapshotType": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "MaxRecords": int,
        "Marker": str,
        "OwnerAccount": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "ClusterExists": bool,
        "SortingEntities": Sequence[SnapshotSortingEntityTypeDef],
    },
    total=False,
)

DescribeClusterSnapshotsMessageSnapshotAvailableWaitTypeDef = TypedDict(
    "DescribeClusterSnapshotsMessageSnapshotAvailableWaitTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "SnapshotType": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "MaxRecords": int,
        "Marker": str,
        "OwnerAccount": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "ClusterExists": bool,
        "SortingEntities": Sequence[SnapshotSortingEntityTypeDef],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeClustersMessageClusterAvailableWaitTypeDef = TypedDict(
    "DescribeClustersMessageClusterAvailableWaitTypeDef",
    {
        "ClusterIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeClustersMessageClusterDeletedWaitTypeDef = TypedDict(
    "DescribeClustersMessageClusterDeletedWaitTypeDef",
    {
        "ClusterIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeClustersMessageClusterRestoredWaitTypeDef = TypedDict(
    "DescribeClustersMessageClusterRestoredWaitTypeDef",
    {
        "ClusterIdentifier": str,
        "MaxRecords": int,
        "Marker": str,
        "TagKeys": Sequence[str],
        "TagValues": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef",
    {
        "ActionType": ActionTypeType,
    },
)
_OptionalDescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "OwnerAccount": str,
        "Filters": Sequence[NodeConfigurationOptionsFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef(
    _RequiredDescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef,
    _OptionalDescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef,
):
    pass


_RequiredDescribeNodeConfigurationOptionsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeNodeConfigurationOptionsMessageRequestTypeDef",
    {
        "ActionType": ActionTypeType,
    },
)
_OptionalDescribeNodeConfigurationOptionsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeNodeConfigurationOptionsMessageRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "OwnerAccount": str,
        "Filters": Sequence[NodeConfigurationOptionsFilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)


class DescribeNodeConfigurationOptionsMessageRequestTypeDef(
    _RequiredDescribeNodeConfigurationOptionsMessageRequestTypeDef,
    _OptionalDescribeNodeConfigurationOptionsMessageRequestTypeDef,
):
    pass


DescribePartnersOutputMessageTypeDef = TypedDict(
    "DescribePartnersOutputMessageTypeDef",
    {
        "PartnerIntegrationInfoList": List[PartnerIntegrationInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef = TypedDict(
    "DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef",
    {
        "ScheduledActionName": str,
        "TargetActionType": ScheduledActionTypeValuesType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Active": bool,
        "Filters": Sequence[ScheduledActionFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeScheduledActionsMessageRequestTypeDef = TypedDict(
    "DescribeScheduledActionsMessageRequestTypeDef",
    {
        "ScheduledActionName": str,
        "TargetActionType": ScheduledActionTypeValuesType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Active": bool,
        "Filters": Sequence[ScheduledActionFilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

EndpointAuthorizationListTypeDef = TypedDict(
    "EndpointAuthorizationListTypeDef",
    {
        "EndpointAuthorizationList": List[EndpointAuthorizationTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventCategoriesMapTypeDef = TypedDict(
    "EventCategoriesMapTypeDef",
    {
        "SourceType": str,
        "Events": List[EventInfoMapTypeDef],
    },
    total=False,
)

EventsMessageTypeDef = TypedDict(
    "EventsMessageTypeDef",
    {
        "Marker": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VpcEndpointTypeDef = TypedDict(
    "VpcEndpointTypeDef",
    {
        "VpcEndpointId": str,
        "VpcId": str,
        "NetworkInterfaces": List[NetworkInterfaceTypeDef],
    },
    total=False,
)

NodeConfigurationOptionsMessageTypeDef = TypedDict(
    "NodeConfigurationOptionsMessageTypeDef",
    {
        "NodeConfigurationOptionList": List[NodeConfigurationOptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservedNodeOfferingTypeDef = TypedDict(
    "ReservedNodeOfferingTypeDef",
    {
        "ReservedNodeOfferingId": str,
        "NodeType": str,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CurrencyCode": str,
        "OfferingType": str,
        "RecurringCharges": List[RecurringChargeTypeDef],
        "ReservedNodeOfferingType": ReservedNodeOfferingTypeType,
    },
    total=False,
)

ReservedNodeTypeDef = TypedDict(
    "ReservedNodeTypeDef",
    {
        "ReservedNodeId": str,
        "ReservedNodeOfferingId": str,
        "NodeType": str,
        "StartTime": datetime,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CurrencyCode": str,
        "NodeCount": int,
        "State": str,
        "OfferingType": str,
        "RecurringCharges": List[RecurringChargeTypeDef],
        "ReservedNodeOfferingType": ReservedNodeOfferingTypeType,
    },
    total=False,
)

RestoreTableFromClusterSnapshotResultTypeDef = TypedDict(
    "RestoreTableFromClusterSnapshotResultTypeDef",
    {
        "TableRestoreStatus": TableRestoreStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TableRestoreStatusMessageTypeDef = TypedDict(
    "TableRestoreStatusMessageTypeDef",
    {
        "TableRestoreStatusDetails": List[TableRestoreStatusTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScheduledActionTypeTypeDef = TypedDict(
    "ScheduledActionTypeTypeDef",
    {
        "ResizeCluster": ResizeClusterMessageTypeDef,
        "PauseCluster": PauseClusterMessageTypeDef,
        "ResumeCluster": ResumeClusterMessageTypeDef,
    },
    total=False,
)

UpdateTargetTypeDef = TypedDict(
    "UpdateTargetTypeDef",
    {
        "MaintenanceTrackName": str,
        "DatabaseVersion": str,
        "SupportedOperations": List[SupportedOperationTypeDef],
    },
    total=False,
)

AccountAttributeListTypeDef = TypedDict(
    "AccountAttributeListTypeDef",
    {
        "AccountAttributes": List[AccountAttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OrderableClusterOptionTypeDef = TypedDict(
    "OrderableClusterOptionTypeDef",
    {
        "ClusterVersion": str,
        "ClusterType": str,
        "NodeType": str,
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
    },
    total=False,
)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AvailabilityZoneTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

ClusterDbRevisionsMessageTypeDef = TypedDict(
    "ClusterDbRevisionsMessageTypeDef",
    {
        "Marker": str,
        "ClusterDbRevisions": List[ClusterDbRevisionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDefaultClusterParametersResultTypeDef = TypedDict(
    "DescribeDefaultClusterParametersResultTypeDef",
    {
        "DefaultClusterParameters": DefaultClusterParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterParameterGroupsMessageTypeDef = TypedDict(
    "ClusterParameterGroupsMessageTypeDef",
    {
        "Marker": str,
        "ParameterGroups": List[ClusterParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterParameterGroupResultTypeDef = TypedDict(
    "CreateClusterParameterGroupResultTypeDef",
    {
        "ClusterParameterGroup": ClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEventSubscriptionResultTypeDef = TypedDict(
    "CreateEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventSubscriptionsMessageTypeDef = TypedDict(
    "EventSubscriptionsMessageTypeDef",
    {
        "Marker": str,
        "EventSubscriptionsList": List[EventSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyEventSubscriptionResultTypeDef = TypedDict(
    "ModifyEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHsmClientCertificateResultTypeDef = TypedDict(
    "CreateHsmClientCertificateResultTypeDef",
    {
        "HsmClientCertificate": HsmClientCertificateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HsmClientCertificateMessageTypeDef = TypedDict(
    "HsmClientCertificateMessageTypeDef",
    {
        "Marker": str,
        "HsmClientCertificates": List[HsmClientCertificateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHsmConfigurationResultTypeDef = TypedDict(
    "CreateHsmConfigurationResultTypeDef",
    {
        "HsmConfiguration": HsmConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HsmConfigurationMessageTypeDef = TypedDict(
    "HsmConfigurationMessageTypeDef",
    {
        "Marker": str,
        "HsmConfigurations": List[HsmConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterSecurityGroupTypeDef = TypedDict(
    "ClusterSecurityGroupTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "Description": str,
        "EC2SecurityGroups": List[EC2SecurityGroupTypeDef],
        "IPRanges": List[IPRangeTypeDef],
        "Tags": List[TagTypeDef],
    },
    total=False,
)

CreateSnapshotCopyGrantResultTypeDef = TypedDict(
    "CreateSnapshotCopyGrantResultTypeDef",
    {
        "SnapshotCopyGrant": SnapshotCopyGrantTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SnapshotCopyGrantMessageTypeDef = TypedDict(
    "SnapshotCopyGrantMessageTypeDef",
    {
        "Marker": str,
        "SnapshotCopyGrants": List[SnapshotCopyGrantTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSnapshotSchedulesOutputMessageTypeDef = TypedDict(
    "DescribeSnapshotSchedulesOutputMessageTypeDef",
    {
        "SnapshotSchedules": List[SnapshotScheduleTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AuthorizeSnapshotAccessResultTypeDef = TypedDict(
    "AuthorizeSnapshotAccessResultTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyClusterSnapshotResultTypeDef = TypedDict(
    "CopyClusterSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterSnapshotResultTypeDef = TypedDict(
    "CreateClusterSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterSnapshotResultTypeDef = TypedDict(
    "DeleteClusterSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterSnapshotResultTypeDef = TypedDict(
    "ModifyClusterSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RevokeSnapshotAccessResultTypeDef = TypedDict(
    "RevokeSnapshotAccessResultTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SnapshotMessageTypeDef = TypedDict(
    "SnapshotMessageTypeDef",
    {
        "Marker": str,
        "Snapshots": List[SnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TaggedResourceListMessageTypeDef = TypedDict(
    "TaggedResourceListMessageTypeDef",
    {
        "TaggedResources": List[TaggedResourceTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UsageLimitListTypeDef = TypedDict(
    "UsageLimitListTypeDef",
    {
        "UsageLimits": List[UsageLimitTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSharesForConsumerResultTypeDef = TypedDict(
    "DescribeDataSharesForConsumerResultTypeDef",
    {
        "DataShares": List[DataShareTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSharesForProducerResultTypeDef = TypedDict(
    "DescribeDataSharesForProducerResultTypeDef",
    {
        "DataShares": List[DataShareTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSharesResultTypeDef = TypedDict(
    "DescribeDataSharesResultTypeDef",
    {
        "DataShares": List[DataShareTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventCategoriesMessageTypeDef = TypedDict(
    "EventCategoriesMessageTypeDef",
    {
        "EventCategoriesMapList": List[EventCategoriesMapTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointAccessResponseMetadataTypeDef = TypedDict(
    "EndpointAccessResponseMetadataTypeDef",
    {
        "ClusterIdentifier": str,
        "ResourceOwner": str,
        "SubnetGroupName": str,
        "EndpointStatus": str,
        "EndpointName": str,
        "EndpointCreateTime": datetime,
        "Port": int,
        "Address": str,
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "VpcEndpoint": VpcEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointAccessTypeDef = TypedDict(
    "EndpointAccessTypeDef",
    {
        "ClusterIdentifier": str,
        "ResourceOwner": str,
        "SubnetGroupName": str,
        "EndpointStatus": str,
        "EndpointName": str,
        "EndpointCreateTime": datetime,
        "Port": int,
        "Address": str,
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "VpcEndpoint": VpcEndpointTypeDef,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "VpcEndpoints": List[VpcEndpointTypeDef],
    },
    total=False,
)

GetReservedNodeExchangeOfferingsOutputMessageTypeDef = TypedDict(
    "GetReservedNodeExchangeOfferingsOutputMessageTypeDef",
    {
        "Marker": str,
        "ReservedNodeOfferings": List[ReservedNodeOfferingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservedNodeOfferingsMessageTypeDef = TypedDict(
    "ReservedNodeOfferingsMessageTypeDef",
    {
        "Marker": str,
        "ReservedNodeOfferings": List[ReservedNodeOfferingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AcceptReservedNodeExchangeOutputMessageTypeDef = TypedDict(
    "AcceptReservedNodeExchangeOutputMessageTypeDef",
    {
        "ExchangedReservedNode": ReservedNodeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PurchaseReservedNodeOfferingResultTypeDef = TypedDict(
    "PurchaseReservedNodeOfferingResultTypeDef",
    {
        "ReservedNode": ReservedNodeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservedNodeConfigurationOptionTypeDef = TypedDict(
    "ReservedNodeConfigurationOptionTypeDef",
    {
        "SourceReservedNode": ReservedNodeTypeDef,
        "TargetReservedNodeCount": int,
        "TargetReservedNodeOffering": ReservedNodeOfferingTypeDef,
    },
    total=False,
)

ReservedNodesMessageTypeDef = TypedDict(
    "ReservedNodesMessageTypeDef",
    {
        "Marker": str,
        "ReservedNodes": List[ReservedNodeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateScheduledActionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateScheduledActionMessageRequestTypeDef",
    {
        "ScheduledActionName": str,
        "TargetAction": ScheduledActionTypeTypeDef,
        "Schedule": str,
        "IamRole": str,
    },
)
_OptionalCreateScheduledActionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateScheduledActionMessageRequestTypeDef",
    {
        "ScheduledActionDescription": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Enable": bool,
    },
    total=False,
)


class CreateScheduledActionMessageRequestTypeDef(
    _RequiredCreateScheduledActionMessageRequestTypeDef,
    _OptionalCreateScheduledActionMessageRequestTypeDef,
):
    pass


_RequiredModifyScheduledActionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyScheduledActionMessageRequestTypeDef",
    {
        "ScheduledActionName": str,
    },
)
_OptionalModifyScheduledActionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyScheduledActionMessageRequestTypeDef",
    {
        "TargetAction": ScheduledActionTypeTypeDef,
        "Schedule": str,
        "IamRole": str,
        "ScheduledActionDescription": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Enable": bool,
    },
    total=False,
)


class ModifyScheduledActionMessageRequestTypeDef(
    _RequiredModifyScheduledActionMessageRequestTypeDef,
    _OptionalModifyScheduledActionMessageRequestTypeDef,
):
    pass


ScheduledActionResponseMetadataTypeDef = TypedDict(
    "ScheduledActionResponseMetadataTypeDef",
    {
        "ScheduledActionName": str,
        "TargetAction": ScheduledActionTypeTypeDef,
        "Schedule": str,
        "IamRole": str,
        "ScheduledActionDescription": str,
        "State": ScheduledActionStateType,
        "NextInvocations": List[datetime],
        "StartTime": datetime,
        "EndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScheduledActionTypeDef = TypedDict(
    "ScheduledActionTypeDef",
    {
        "ScheduledActionName": str,
        "TargetAction": ScheduledActionTypeTypeDef,
        "Schedule": str,
        "IamRole": str,
        "ScheduledActionDescription": str,
        "State": ScheduledActionStateType,
        "NextInvocations": List[datetime],
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

MaintenanceTrackTypeDef = TypedDict(
    "MaintenanceTrackTypeDef",
    {
        "MaintenanceTrackName": str,
        "DatabaseVersion": str,
        "UpdateTargets": List[UpdateTargetTypeDef],
    },
    total=False,
)

OrderableClusterOptionsMessageTypeDef = TypedDict(
    "OrderableClusterOptionsMessageTypeDef",
    {
        "OrderableClusterOptions": List[OrderableClusterOptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterSubnetGroupTypeDef = TypedDict(
    "ClusterSubnetGroupTypeDef",
    {
        "ClusterSubnetGroupName": str,
        "Description": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetTypeDef],
        "Tags": List[TagTypeDef],
    },
    total=False,
)

AuthorizeClusterSecurityGroupIngressResultTypeDef = TypedDict(
    "AuthorizeClusterSecurityGroupIngressResultTypeDef",
    {
        "ClusterSecurityGroup": ClusterSecurityGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterSecurityGroupMessageTypeDef = TypedDict(
    "ClusterSecurityGroupMessageTypeDef",
    {
        "Marker": str,
        "ClusterSecurityGroups": List[ClusterSecurityGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterSecurityGroupResultTypeDef = TypedDict(
    "CreateClusterSecurityGroupResultTypeDef",
    {
        "ClusterSecurityGroup": ClusterSecurityGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RevokeClusterSecurityGroupIngressResultTypeDef = TypedDict(
    "RevokeClusterSecurityGroupIngressResultTypeDef",
    {
        "ClusterSecurityGroup": ClusterSecurityGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointAccessListTypeDef = TypedDict(
    "EndpointAccessListTypeDef",
    {
        "EndpointAccessList": List[EndpointAccessTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "ClusterIdentifier": str,
        "NodeType": str,
        "ClusterStatus": str,
        "ClusterAvailabilityStatus": str,
        "ModifyStatus": str,
        "MasterUsername": str,
        "DBName": str,
        "Endpoint": EndpointTypeDef,
        "ClusterCreateTime": datetime,
        "AutomatedSnapshotRetentionPeriod": int,
        "ManualSnapshotRetentionPeriod": int,
        "ClusterSecurityGroups": List[ClusterSecurityGroupMembershipTypeDef],
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "ClusterParameterGroups": List[ClusterParameterGroupStatusTypeDef],
        "ClusterSubnetGroupName": str,
        "VpcId": str,
        "AvailabilityZone": str,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": PendingModifiedValuesTypeDef,
        "ClusterVersion": str,
        "AllowVersionUpgrade": bool,
        "NumberOfNodes": int,
        "PubliclyAccessible": bool,
        "Encrypted": bool,
        "RestoreStatus": RestoreStatusTypeDef,
        "DataTransferProgress": DataTransferProgressTypeDef,
        "HsmStatus": HsmStatusTypeDef,
        "ClusterSnapshotCopyStatus": ClusterSnapshotCopyStatusTypeDef,
        "ClusterPublicKey": str,
        "ClusterNodes": List[ClusterNodeTypeDef],
        "ElasticIpStatus": ElasticIpStatusTypeDef,
        "ClusterRevisionNumber": str,
        "Tags": List[TagTypeDef],
        "KmsKeyId": str,
        "EnhancedVpcRouting": bool,
        "IamRoles": List[ClusterIamRoleTypeDef],
        "PendingActions": List[str],
        "MaintenanceTrackName": str,
        "ElasticResizeNumberOfNodeOptions": str,
        "DeferredMaintenanceWindows": List[DeferredMaintenanceWindowTypeDef],
        "SnapshotScheduleIdentifier": str,
        "SnapshotScheduleState": ScheduleStateType,
        "ExpectedNextSnapshotScheduleTime": datetime,
        "ExpectedNextSnapshotScheduleTimeStatus": str,
        "NextMaintenanceWindowStartTime": datetime,
        "ResizeInfo": ResizeInfoTypeDef,
        "AvailabilityZoneRelocationStatus": str,
        "ClusterNamespaceArn": str,
        "TotalStorageCapacityInMegaBytes": int,
        "AquaConfiguration": AquaConfigurationTypeDef,
        "DefaultIamRoleArn": str,
        "ReservedNodeExchangeStatus": ReservedNodeExchangeStatusTypeDef,
    },
    total=False,
)

GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef = TypedDict(
    "GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef",
    {
        "Marker": str,
        "ReservedNodeConfigurationOptionList": List[ReservedNodeConfigurationOptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScheduledActionsMessageTypeDef = TypedDict(
    "ScheduledActionsMessageTypeDef",
    {
        "Marker": str,
        "ScheduledActions": List[ScheduledActionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TrackListMessageTypeDef = TypedDict(
    "TrackListMessageTypeDef",
    {
        "MaintenanceTracks": List[MaintenanceTrackTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterSubnetGroupMessageTypeDef = TypedDict(
    "ClusterSubnetGroupMessageTypeDef",
    {
        "Marker": str,
        "ClusterSubnetGroups": List[ClusterSubnetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterSubnetGroupResultTypeDef = TypedDict(
    "CreateClusterSubnetGroupResultTypeDef",
    {
        "ClusterSubnetGroup": ClusterSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterSubnetGroupResultTypeDef = TypedDict(
    "ModifyClusterSubnetGroupResultTypeDef",
    {
        "ClusterSubnetGroup": ClusterSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClustersMessageTypeDef = TypedDict(
    "ClustersMessageTypeDef",
    {
        "Marker": str,
        "Clusters": List[ClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResultTypeDef = TypedDict(
    "CreateClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResultTypeDef = TypedDict(
    "DeleteClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisableSnapshotCopyResultTypeDef = TypedDict(
    "DisableSnapshotCopyResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableSnapshotCopyResultTypeDef = TypedDict(
    "EnableSnapshotCopyResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterDbRevisionResultTypeDef = TypedDict(
    "ModifyClusterDbRevisionResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterIamRolesResultTypeDef = TypedDict(
    "ModifyClusterIamRolesResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterMaintenanceResultTypeDef = TypedDict(
    "ModifyClusterMaintenanceResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterResultTypeDef = TypedDict(
    "ModifyClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifySnapshotCopyRetentionPeriodResultTypeDef = TypedDict(
    "ModifySnapshotCopyRetentionPeriodResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PauseClusterResultTypeDef = TypedDict(
    "PauseClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootClusterResultTypeDef = TypedDict(
    "RebootClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResizeClusterResultTypeDef = TypedDict(
    "ResizeClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreFromClusterSnapshotResultTypeDef = TypedDict(
    "RestoreFromClusterSnapshotResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResumeClusterResultTypeDef = TypedDict(
    "ResumeClusterResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RotateEncryptionKeyResultTypeDef = TypedDict(
    "RotateEncryptionKeyResultTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
