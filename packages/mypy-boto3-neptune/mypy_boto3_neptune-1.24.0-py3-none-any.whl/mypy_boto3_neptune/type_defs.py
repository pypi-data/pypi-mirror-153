"""
Type annotations for neptune service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptune/type_defs/)

Usage::

    ```python
    from mypy_boto3_neptune.type_defs import AddRoleToDBClusterMessageRequestTypeDef

    data: AddRoleToDBClusterMessageRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import ApplyMethodType, SourceTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AddRoleToDBClusterMessageRequestTypeDef",
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    "EventSubscriptionTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "AvailabilityZoneTypeDef",
    "CharacterSetTypeDef",
    "CloudwatchLogsExportConfigurationTypeDef",
    "DBClusterParameterGroupTypeDef",
    "DBClusterSnapshotTypeDef",
    "DBParameterGroupTypeDef",
    "DBClusterEndpointTypeDef",
    "DBClusterMemberTypeDef",
    "DBClusterOptionGroupStatusTypeDef",
    "ParameterTypeDef",
    "DBClusterRoleTypeDef",
    "DBClusterSnapshotAttributeTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "TimezoneTypeDef",
    "UpgradeTargetTypeDef",
    "DBInstanceStatusInfoTypeDef",
    "DBParameterGroupStatusTypeDef",
    "DBSecurityGroupMembershipTypeDef",
    "DomainMembershipTypeDef",
    "EndpointTypeDef",
    "OptionGroupMembershipTypeDef",
    "DeleteDBClusterEndpointMessageRequestTypeDef",
    "DeleteDBClusterMessageRequestTypeDef",
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    "DeleteDBInstanceMessageRequestTypeDef",
    "DeleteDBParameterGroupMessageRequestTypeDef",
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeValidDBInstanceModificationsMessageRequestTypeDef",
    "DoubleRangeTypeDef",
    "EventCategoriesMapTypeDef",
    "EventTypeDef",
    "FailoverDBClusterMessageRequestTypeDef",
    "ModifyDBClusterEndpointMessageRequestTypeDef",
    "ModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    "ModifyDBSubnetGroupMessageRequestTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "PendingCloudwatchLogsExportsTypeDef",
    "PendingMaintenanceActionTypeDef",
    "PromoteReadReplicaDBClusterMessageRequestTypeDef",
    "RangeTypeDef",
    "RebootDBInstanceMessageRequestTypeDef",
    "RemoveRoleFromDBClusterMessageRequestTypeDef",
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "StartDBClusterMessageRequestTypeDef",
    "StopDBClusterMessageRequestTypeDef",
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    "CreateDBClusterEndpointOutputTypeDef",
    "CreateEventSubscriptionResultTypeDef",
    "DBClusterParameterGroupNameMessageTypeDef",
    "DBParameterGroupNameMessageTypeDef",
    "DeleteDBClusterEndpointOutputTypeDef",
    "DeleteEventSubscriptionResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventSubscriptionsMessageTypeDef",
    "ModifyDBClusterEndpointOutputTypeDef",
    "ModifyEventSubscriptionResultTypeDef",
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "CopyDBClusterParameterGroupMessageRequestTypeDef",
    "CopyDBClusterSnapshotMessageRequestTypeDef",
    "CopyDBParameterGroupMessageRequestTypeDef",
    "CreateDBClusterEndpointMessageRequestTypeDef",
    "CreateDBClusterMessageRequestTypeDef",
    "CreateDBClusterParameterGroupMessageRequestTypeDef",
    "CreateDBClusterSnapshotMessageRequestTypeDef",
    "CreateDBInstanceMessageRequestTypeDef",
    "CreateDBParameterGroupMessageRequestTypeDef",
    "CreateDBSubnetGroupMessageRequestTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "RestoreDBClusterFromSnapshotMessageRequestTypeDef",
    "RestoreDBClusterToPointInTimeMessageRequestTypeDef",
    "TagListMessageTypeDef",
    "OrderableDBInstanceOptionTypeDef",
    "SubnetTypeDef",
    "ModifyDBClusterMessageRequestTypeDef",
    "ModifyDBInstanceMessageRequestTypeDef",
    "CopyDBClusterParameterGroupResultTypeDef",
    "CreateDBClusterParameterGroupResultTypeDef",
    "DBClusterParameterGroupsMessageTypeDef",
    "CopyDBClusterSnapshotResultTypeDef",
    "CreateDBClusterSnapshotResultTypeDef",
    "DBClusterSnapshotMessageTypeDef",
    "DeleteDBClusterSnapshotResultTypeDef",
    "CopyDBParameterGroupResultTypeDef",
    "CreateDBParameterGroupResultTypeDef",
    "DBParameterGroupsMessageTypeDef",
    "DBClusterEndpointMessageTypeDef",
    "DBClusterParameterGroupDetailsTypeDef",
    "DBParameterGroupDetailsTypeDef",
    "EngineDefaultsTypeDef",
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    "ModifyDBParameterGroupMessageRequestTypeDef",
    "ResetDBClusterParameterGroupMessageRequestTypeDef",
    "ResetDBParameterGroupMessageRequestTypeDef",
    "DBClusterSnapshotAttributesResultTypeDef",
    "DBClusterTypeDef",
    "DBEngineVersionTypeDef",
    "DescribeDBClusterEndpointsMessageRequestTypeDef",
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    "DescribeDBClusterParametersMessageRequestTypeDef",
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    "DescribeDBClustersMessageRequestTypeDef",
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    "DescribeDBInstancesMessageRequestTypeDef",
    "DescribeDBParameterGroupsMessageRequestTypeDef",
    "DescribeDBParametersMessageRequestTypeDef",
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    "DescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    "DescribeEngineDefaultParametersMessageRequestTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef",
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    "DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    "DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef",
    "DescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    "DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    "EventCategoriesMessageTypeDef",
    "EventsMessageTypeDef",
    "PendingModifiedValuesTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "ValidStorageOptionsTypeDef",
    "OrderableDBInstanceOptionsMessageTypeDef",
    "DBSubnetGroupTypeDef",
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    "DescribeEngineDefaultParametersResultTypeDef",
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    "CreateDBClusterResultTypeDef",
    "DBClusterMessageTypeDef",
    "DeleteDBClusterResultTypeDef",
    "FailoverDBClusterResultTypeDef",
    "ModifyDBClusterResultTypeDef",
    "PromoteReadReplicaDBClusterResultTypeDef",
    "RestoreDBClusterFromSnapshotResultTypeDef",
    "RestoreDBClusterToPointInTimeResultTypeDef",
    "StartDBClusterResultTypeDef",
    "StopDBClusterResultTypeDef",
    "DBEngineVersionMessageTypeDef",
    "ApplyPendingMaintenanceActionResultTypeDef",
    "PendingMaintenanceActionsMessageTypeDef",
    "ValidDBInstanceModificationsMessageTypeDef",
    "CreateDBSubnetGroupResultTypeDef",
    "DBInstanceTypeDef",
    "DBSubnetGroupMessageTypeDef",
    "ModifyDBSubnetGroupResultTypeDef",
    "DescribeValidDBInstanceModificationsResultTypeDef",
    "CreateDBInstanceResultTypeDef",
    "DBInstanceMessageTypeDef",
    "DeleteDBInstanceResultTypeDef",
    "ModifyDBInstanceResultTypeDef",
    "RebootDBInstanceResultTypeDef",
)

_RequiredAddRoleToDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredAddRoleToDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "RoleArn": str,
    },
)
_OptionalAddRoleToDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalAddRoleToDBClusterMessageRequestTypeDef",
    {
        "FeatureName": str,
    },
    total=False,
)


class AddRoleToDBClusterMessageRequestTypeDef(
    _RequiredAddRoleToDBClusterMessageRequestTypeDef,
    _OptionalAddRoleToDBClusterMessageRequestTypeDef,
):
    pass


AddSourceIdentifierToSubscriptionMessageRequestTypeDef = TypedDict(
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SourceIdentifier": str,
    },
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": str,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Enabled": bool,
        "EventSubscriptionArn": str,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ApplyPendingMaintenanceActionMessageRequestTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "ApplyAction": str,
        "OptInType": str,
    },
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

CharacterSetTypeDef = TypedDict(
    "CharacterSetTypeDef",
    {
        "CharacterSetName": str,
        "CharacterSetDescription": str,
    },
    total=False,
)

CloudwatchLogsExportConfigurationTypeDef = TypedDict(
    "CloudwatchLogsExportConfigurationTypeDef",
    {
        "EnableLogTypes": Sequence[str],
        "DisableLogTypes": Sequence[str],
    },
    total=False,
)

DBClusterParameterGroupTypeDef = TypedDict(
    "DBClusterParameterGroupTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
        "DBClusterParameterGroupArn": str,
    },
    total=False,
)

DBClusterSnapshotTypeDef = TypedDict(
    "DBClusterSnapshotTypeDef",
    {
        "AvailabilityZones": List[str],
        "DBClusterSnapshotIdentifier": str,
        "DBClusterIdentifier": str,
        "SnapshotCreateTime": datetime,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "VpcId": str,
        "ClusterCreateTime": datetime,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "PercentProgress": int,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DBClusterSnapshotArn": str,
        "SourceDBClusterSnapshotArn": str,
        "IAMDatabaseAuthenticationEnabled": bool,
    },
    total=False,
)

DBParameterGroupTypeDef = TypedDict(
    "DBParameterGroupTypeDef",
    {
        "DBParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
        "DBParameterGroupArn": str,
    },
    total=False,
)

DBClusterEndpointTypeDef = TypedDict(
    "DBClusterEndpointTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
        "DBClusterIdentifier": str,
        "DBClusterEndpointResourceIdentifier": str,
        "Endpoint": str,
        "Status": str,
        "EndpointType": str,
        "CustomEndpointType": str,
        "StaticMembers": List[str],
        "ExcludedMembers": List[str],
        "DBClusterEndpointArn": str,
    },
    total=False,
)

DBClusterMemberTypeDef = TypedDict(
    "DBClusterMemberTypeDef",
    {
        "DBInstanceIdentifier": str,
        "IsClusterWriter": bool,
        "DBClusterParameterGroupStatus": str,
        "PromotionTier": int,
    },
    total=False,
)

DBClusterOptionGroupStatusTypeDef = TypedDict(
    "DBClusterOptionGroupStatusTypeDef",
    {
        "DBClusterOptionGroupName": str,
        "Status": str,
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
        "ApplyType": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "MinimumEngineVersion": str,
        "ApplyMethod": ApplyMethodType,
    },
    total=False,
)

DBClusterRoleTypeDef = TypedDict(
    "DBClusterRoleTypeDef",
    {
        "RoleArn": str,
        "Status": str,
        "FeatureName": str,
    },
    total=False,
)

DBClusterSnapshotAttributeTypeDef = TypedDict(
    "DBClusterSnapshotAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": List[str],
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

TimezoneTypeDef = TypedDict(
    "TimezoneTypeDef",
    {
        "TimezoneName": str,
    },
    total=False,
)

UpgradeTargetTypeDef = TypedDict(
    "UpgradeTargetTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "Description": str,
        "AutoUpgrade": bool,
        "IsMajorVersionUpgrade": bool,
    },
    total=False,
)

DBInstanceStatusInfoTypeDef = TypedDict(
    "DBInstanceStatusInfoTypeDef",
    {
        "StatusType": str,
        "Normal": bool,
        "Status": str,
        "Message": str,
    },
    total=False,
)

DBParameterGroupStatusTypeDef = TypedDict(
    "DBParameterGroupStatusTypeDef",
    {
        "DBParameterGroupName": str,
        "ParameterApplyStatus": str,
    },
    total=False,
)

DBSecurityGroupMembershipTypeDef = TypedDict(
    "DBSecurityGroupMembershipTypeDef",
    {
        "DBSecurityGroupName": str,
        "Status": str,
    },
    total=False,
)

DomainMembershipTypeDef = TypedDict(
    "DomainMembershipTypeDef",
    {
        "Domain": str,
        "Status": str,
        "FQDN": str,
        "IAMRoleName": str,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "HostedZoneId": str,
    },
    total=False,
)

OptionGroupMembershipTypeDef = TypedDict(
    "OptionGroupMembershipTypeDef",
    {
        "OptionGroupName": str,
        "Status": str,
    },
    total=False,
)

DeleteDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterEndpointMessageRequestTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
    },
)

_RequiredDeleteDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalDeleteDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteDBClusterMessageRequestTypeDef",
    {
        "SkipFinalSnapshot": bool,
        "FinalDBSnapshotIdentifier": str,
    },
    total=False,
)


class DeleteDBClusterMessageRequestTypeDef(
    _RequiredDeleteDBClusterMessageRequestTypeDef, _OptionalDeleteDBClusterMessageRequestTypeDef
):
    pass


DeleteDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)

DeleteDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
    },
)

_RequiredDeleteDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalDeleteDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteDBInstanceMessageRequestTypeDef",
    {
        "SkipFinalSnapshot": bool,
        "FinalDBSnapshotIdentifier": str,
    },
    total=False,
)


class DeleteDBInstanceMessageRequestTypeDef(
    _RequiredDeleteDBInstanceMessageRequestTypeDef, _OptionalDeleteDBInstanceMessageRequestTypeDef
):
    pass


DeleteDBParameterGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
    },
)

DeleteDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
    },
)

DeleteEventSubscriptionMessageRequestTypeDef = TypedDict(
    "DeleteEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
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

DescribeDBClusterSnapshotAttributesMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeValidDBInstanceModificationsMessageRequestTypeDef = TypedDict(
    "DescribeValidDBInstanceModificationsMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)

DoubleRangeTypeDef = TypedDict(
    "DoubleRangeTypeDef",
    {
        "From": float,
        "To": float,
    },
    total=False,
)

EventCategoriesMapTypeDef = TypedDict(
    "EventCategoriesMapTypeDef",
    {
        "SourceType": str,
        "EventCategories": List[str],
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
        "Date": datetime,
        "SourceArn": str,
    },
    total=False,
)

FailoverDBClusterMessageRequestTypeDef = TypedDict(
    "FailoverDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "TargetDBInstanceIdentifier": str,
    },
    total=False,
)

_RequiredModifyDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterEndpointMessageRequestTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
    },
)
_OptionalModifyDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterEndpointMessageRequestTypeDef",
    {
        "EndpointType": str,
        "StaticMembers": Sequence[str],
        "ExcludedMembers": Sequence[str],
    },
    total=False,
)


class ModifyDBClusterEndpointMessageRequestTypeDef(
    _RequiredModifyDBClusterEndpointMessageRequestTypeDef,
    _OptionalModifyDBClusterEndpointMessageRequestTypeDef,
):
    pass


_RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "AttributeName": str,
    },
)
_OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    {
        "ValuesToAdd": Sequence[str],
        "ValuesToRemove": Sequence[str],
    },
    total=False,
)


class ModifyDBClusterSnapshotAttributeMessageRequestTypeDef(
    _RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
    _OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
):
    pass


_RequiredModifyDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalModifyDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupDescription": str,
    },
    total=False,
)


class ModifyDBSubnetGroupMessageRequestTypeDef(
    _RequiredModifyDBSubnetGroupMessageRequestTypeDef,
    _OptionalModifyDBSubnetGroupMessageRequestTypeDef,
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
        "EventCategories": Sequence[str],
        "Enabled": bool,
    },
    total=False,
)


class ModifyEventSubscriptionMessageRequestTypeDef(
    _RequiredModifyEventSubscriptionMessageRequestTypeDef,
    _OptionalModifyEventSubscriptionMessageRequestTypeDef,
):
    pass


PendingCloudwatchLogsExportsTypeDef = TypedDict(
    "PendingCloudwatchLogsExportsTypeDef",
    {
        "LogTypesToEnable": List[str],
        "LogTypesToDisable": List[str],
    },
    total=False,
)

PendingMaintenanceActionTypeDef = TypedDict(
    "PendingMaintenanceActionTypeDef",
    {
        "Action": str,
        "AutoAppliedAfterDate": datetime,
        "ForcedApplyDate": datetime,
        "OptInStatus": str,
        "CurrentApplyDate": datetime,
        "Description": str,
    },
    total=False,
)

PromoteReadReplicaDBClusterMessageRequestTypeDef = TypedDict(
    "PromoteReadReplicaDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

RangeTypeDef = TypedDict(
    "RangeTypeDef",
    {
        "From": int,
        "To": int,
        "Step": int,
    },
    total=False,
)

_RequiredRebootDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredRebootDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalRebootDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalRebootDBInstanceMessageRequestTypeDef",
    {
        "ForceFailover": bool,
    },
    total=False,
)


class RebootDBInstanceMessageRequestTypeDef(
    _RequiredRebootDBInstanceMessageRequestTypeDef, _OptionalRebootDBInstanceMessageRequestTypeDef
):
    pass


_RequiredRemoveRoleFromDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredRemoveRoleFromDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "RoleArn": str,
    },
)
_OptionalRemoveRoleFromDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalRemoveRoleFromDBClusterMessageRequestTypeDef",
    {
        "FeatureName": str,
    },
    total=False,
)


class RemoveRoleFromDBClusterMessageRequestTypeDef(
    _RequiredRemoveRoleFromDBClusterMessageRequestTypeDef,
    _OptionalRemoveRoleFromDBClusterMessageRequestTypeDef,
):
    pass


RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef = TypedDict(
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SourceIdentifier": str,
    },
)

RemoveTagsFromResourceMessageRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
        "TagKeys": Sequence[str],
    },
)

StartDBClusterMessageRequestTypeDef = TypedDict(
    "StartDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

StopDBClusterMessageRequestTypeDef = TypedDict(
    "StopDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

AddSourceIdentifierToSubscriptionResultTypeDef = TypedDict(
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterEndpointOutputTypeDef = TypedDict(
    "CreateDBClusterEndpointOutputTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
        "DBClusterIdentifier": str,
        "DBClusterEndpointResourceIdentifier": str,
        "Endpoint": str,
        "Status": str,
        "EndpointType": str,
        "CustomEndpointType": str,
        "StaticMembers": List[str],
        "ExcludedMembers": List[str],
        "DBClusterEndpointArn": str,
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

DBClusterParameterGroupNameMessageTypeDef = TypedDict(
    "DBClusterParameterGroupNameMessageTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBParameterGroupNameMessageTypeDef = TypedDict(
    "DBParameterGroupNameMessageTypeDef",
    {
        "DBParameterGroupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterEndpointOutputTypeDef = TypedDict(
    "DeleteDBClusterEndpointOutputTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
        "DBClusterIdentifier": str,
        "DBClusterEndpointResourceIdentifier": str,
        "Endpoint": str,
        "Status": str,
        "EndpointType": str,
        "CustomEndpointType": str,
        "StaticMembers": List[str],
        "ExcludedMembers": List[str],
        "DBClusterEndpointArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEventSubscriptionResultTypeDef = TypedDict(
    "DeleteEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
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

ModifyDBClusterEndpointOutputTypeDef = TypedDict(
    "ModifyDBClusterEndpointOutputTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
        "DBClusterIdentifier": str,
        "DBClusterEndpointResourceIdentifier": str,
        "Endpoint": str,
        "Status": str,
        "EndpointType": str,
        "CustomEndpointType": str,
        "StaticMembers": List[str],
        "ExcludedMembers": List[str],
        "DBClusterEndpointArn": str,
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

RemoveSourceIdentifierFromSubscriptionResultTypeDef = TypedDict(
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsToResourceMessageRequestTypeDef = TypedDict(
    "AddTagsToResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCopyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "SourceDBClusterParameterGroupIdentifier": str,
        "TargetDBClusterParameterGroupIdentifier": str,
        "TargetDBClusterParameterGroupDescription": str,
    },
)
_OptionalCopyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredCopyDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalCopyDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCopyDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBClusterSnapshotMessageRequestTypeDef",
    {
        "SourceDBClusterSnapshotIdentifier": str,
        "TargetDBClusterSnapshotIdentifier": str,
    },
)
_OptionalCopyDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBClusterSnapshotMessageRequestTypeDef",
    {
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "CopyTags": bool,
        "Tags": Sequence[TagTypeDef],
        "SourceRegion": str,
    },
    total=False,
)


class CopyDBClusterSnapshotMessageRequestTypeDef(
    _RequiredCopyDBClusterSnapshotMessageRequestTypeDef,
    _OptionalCopyDBClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCopyDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBParameterGroupMessageRequestTypeDef",
    {
        "SourceDBParameterGroupIdentifier": str,
        "TargetDBParameterGroupIdentifier": str,
        "TargetDBParameterGroupDescription": str,
    },
)
_OptionalCopyDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyDBParameterGroupMessageRequestTypeDef(
    _RequiredCopyDBParameterGroupMessageRequestTypeDef,
    _OptionalCopyDBParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterEndpointMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterEndpointIdentifier": str,
        "EndpointType": str,
    },
)
_OptionalCreateDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterEndpointMessageRequestTypeDef",
    {
        "StaticMembers": Sequence[str],
        "ExcludedMembers": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterEndpointMessageRequestTypeDef(
    _RequiredCreateDBClusterEndpointMessageRequestTypeDef,
    _OptionalCreateDBClusterEndpointMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Engine": str,
    },
)
_OptionalCreateDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterMessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "BackupRetentionPeriod": int,
        "CharacterSetName": str,
        "CopyTagsToSnapshot": bool,
        "DatabaseName": str,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "DBSubnetGroupName": str,
        "EngineVersion": str,
        "Port": int,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "OptionGroupName": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReplicationSourceIdentifier": str,
        "Tags": Sequence[TagTypeDef],
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DeletionProtection": bool,
        "SourceRegion": str,
    },
    total=False,
)


class CreateDBClusterMessageRequestTypeDef(
    _RequiredCreateDBClusterMessageRequestTypeDef, _OptionalCreateDBClusterMessageRequestTypeDef
):
    pass


_RequiredCreateDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
    },
)
_OptionalCreateDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredCreateDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalCreateDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterSnapshotMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "DBClusterIdentifier": str,
    },
)
_OptionalCreateDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterSnapshotMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterSnapshotMessageRequestTypeDef(
    _RequiredCreateDBClusterSnapshotMessageRequestTypeDef,
    _OptionalCreateDBClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCreateDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
    },
)
_OptionalCreateDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBInstanceMessageRequestTypeDef",
    {
        "DBName": str,
        "AllocatedStorage": int,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "DBSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "AvailabilityZone": str,
        "DBSubnetGroupName": str,
        "PreferredMaintenanceWindow": str,
        "DBParameterGroupName": str,
        "BackupRetentionPeriod": int,
        "PreferredBackupWindow": str,
        "Port": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupName": str,
        "CharacterSetName": str,
        "PubliclyAccessible": bool,
        "Tags": Sequence[TagTypeDef],
        "DBClusterIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "TdeCredentialPassword": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "Domain": str,
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "DomainIAMRoleName": str,
        "PromotionTier": int,
        "Timezone": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DeletionProtection": bool,
    },
    total=False,
)


class CreateDBInstanceMessageRequestTypeDef(
    _RequiredCreateDBInstanceMessageRequestTypeDef, _OptionalCreateDBInstanceMessageRequestTypeDef
):
    pass


_RequiredCreateDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
    },
)
_OptionalCreateDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBParameterGroupMessageRequestTypeDef(
    _RequiredCreateDBParameterGroupMessageRequestTypeDef,
    _OptionalCreateDBParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "DBSubnetGroupDescription": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBSubnetGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBSubnetGroupMessageRequestTypeDef(
    _RequiredCreateDBSubnetGroupMessageRequestTypeDef,
    _OptionalCreateDBSubnetGroupMessageRequestTypeDef,
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
        "EventCategories": Sequence[str],
        "SourceIds": Sequence[str],
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


_RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "Engine": str,
    },
)
_OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "EngineVersion": str,
        "Port": int,
        "DBSubnetGroupName": str,
        "DatabaseName": str,
        "OptionGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DBClusterParameterGroupName": str,
        "DeletionProtection": bool,
        "CopyTagsToSnapshot": bool,
    },
    total=False,
)


class RestoreDBClusterFromSnapshotMessageRequestTypeDef(
    _RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef,
    _OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef,
):
    pass


_RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "SourceDBClusterIdentifier": str,
    },
)
_OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef",
    {
        "RestoreType": str,
        "RestoreToTime": Union[datetime, str],
        "UseLatestRestorableTime": bool,
        "Port": int,
        "DBSubnetGroupName": str,
        "OptionGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DBClusterParameterGroupName": str,
        "DeletionProtection": bool,
    },
    total=False,
)


class RestoreDBClusterToPointInTimeMessageRequestTypeDef(
    _RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef,
    _OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef,
):
    pass


TagListMessageTypeDef = TypedDict(
    "TagListMessageTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OrderableDBInstanceOptionTypeDef = TypedDict(
    "OrderableDBInstanceOptionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "MultiAZCapable": bool,
        "ReadReplicaCapable": bool,
        "Vpc": bool,
        "SupportsStorageEncryption": bool,
        "StorageType": str,
        "SupportsIops": bool,
        "SupportsEnhancedMonitoring": bool,
        "SupportsIAMDatabaseAuthentication": bool,
        "SupportsPerformanceInsights": bool,
        "MinStorageSize": int,
        "MaxStorageSize": int,
        "MinIopsPerDbInstance": int,
        "MaxIopsPerDbInstance": int,
        "MinIopsPerGib": float,
        "MaxIopsPerGib": float,
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

_RequiredModifyDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalModifyDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterMessageRequestTypeDef",
    {
        "NewDBClusterIdentifier": str,
        "ApplyImmediately": bool,
        "BackupRetentionPeriod": int,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Port": int,
        "MasterUserPassword": str,
        "OptionGroupName": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "EnableIAMDatabaseAuthentication": bool,
        "CloudwatchLogsExportConfiguration": CloudwatchLogsExportConfigurationTypeDef,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
        "DBInstanceParameterGroupName": str,
        "DeletionProtection": bool,
        "CopyTagsToSnapshot": bool,
    },
    total=False,
)


class ModifyDBClusterMessageRequestTypeDef(
    _RequiredModifyDBClusterMessageRequestTypeDef, _OptionalModifyDBClusterMessageRequestTypeDef
):
    pass


_RequiredModifyDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalModifyDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBInstanceMessageRequestTypeDef",
    {
        "AllocatedStorage": int,
        "DBInstanceClass": str,
        "DBSubnetGroupName": str,
        "DBSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "ApplyImmediately": bool,
        "MasterUserPassword": str,
        "DBParameterGroupName": str,
        "BackupRetentionPeriod": int,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupName": str,
        "NewDBInstanceIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "TdeCredentialPassword": str,
        "CACertificateIdentifier": str,
        "Domain": str,
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "DBPortNumber": int,
        "PubliclyAccessible": bool,
        "MonitoringRoleArn": str,
        "DomainIAMRoleName": str,
        "PromotionTier": int,
        "EnableIAMDatabaseAuthentication": bool,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "CloudwatchLogsExportConfiguration": CloudwatchLogsExportConfigurationTypeDef,
        "DeletionProtection": bool,
    },
    total=False,
)


class ModifyDBInstanceMessageRequestTypeDef(
    _RequiredModifyDBInstanceMessageRequestTypeDef, _OptionalModifyDBInstanceMessageRequestTypeDef
):
    pass


CopyDBClusterParameterGroupResultTypeDef = TypedDict(
    "CopyDBClusterParameterGroupResultTypeDef",
    {
        "DBClusterParameterGroup": DBClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterParameterGroupResultTypeDef = TypedDict(
    "CreateDBClusterParameterGroupResultTypeDef",
    {
        "DBClusterParameterGroup": DBClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupsMessageTypeDef = TypedDict(
    "DBClusterParameterGroupsMessageTypeDef",
    {
        "Marker": str,
        "DBClusterParameterGroups": List[DBClusterParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyDBClusterSnapshotResultTypeDef = TypedDict(
    "CopyDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterSnapshotResultTypeDef = TypedDict(
    "CreateDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterSnapshotMessageTypeDef = TypedDict(
    "DBClusterSnapshotMessageTypeDef",
    {
        "Marker": str,
        "DBClusterSnapshots": List[DBClusterSnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterSnapshotResultTypeDef = TypedDict(
    "DeleteDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyDBParameterGroupResultTypeDef = TypedDict(
    "CopyDBParameterGroupResultTypeDef",
    {
        "DBParameterGroup": DBParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBParameterGroupResultTypeDef = TypedDict(
    "CreateDBParameterGroupResultTypeDef",
    {
        "DBParameterGroup": DBParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBParameterGroupsMessageTypeDef = TypedDict(
    "DBParameterGroupsMessageTypeDef",
    {
        "Marker": str,
        "DBParameterGroups": List[DBParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterEndpointMessageTypeDef = TypedDict(
    "DBClusterEndpointMessageTypeDef",
    {
        "Marker": str,
        "DBClusterEndpoints": List[DBClusterEndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupDetailsTypeDef = TypedDict(
    "DBClusterParameterGroupDetailsTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBParameterGroupDetailsTypeDef = TypedDict(
    "DBParameterGroupDetailsTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EngineDefaultsTypeDef = TypedDict(
    "EngineDefaultsTypeDef",
    {
        "DBParameterGroupFamily": str,
        "Marker": str,
        "Parameters": List[ParameterTypeDef],
    },
    total=False,
)

ModifyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Parameters": Sequence[ParameterTypeDef],
    },
)

ModifyDBParameterGroupMessageRequestTypeDef = TypedDict(
    "ModifyDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
        "Parameters": Sequence[ParameterTypeDef],
    },
)

_RequiredResetDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredResetDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalResetDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalResetDBClusterParameterGroupMessageRequestTypeDef",
    {
        "ResetAllParameters": bool,
        "Parameters": Sequence[ParameterTypeDef],
    },
    total=False,
)


class ResetDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredResetDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalResetDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredResetDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredResetDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
    },
)
_OptionalResetDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalResetDBParameterGroupMessageRequestTypeDef",
    {
        "ResetAllParameters": bool,
        "Parameters": Sequence[ParameterTypeDef],
    },
    total=False,
)


class ResetDBParameterGroupMessageRequestTypeDef(
    _RequiredResetDBParameterGroupMessageRequestTypeDef,
    _OptionalResetDBParameterGroupMessageRequestTypeDef,
):
    pass


DBClusterSnapshotAttributesResultTypeDef = TypedDict(
    "DBClusterSnapshotAttributesResultTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "DBClusterSnapshotAttributes": List[DBClusterSnapshotAttributeTypeDef],
    },
    total=False,
)

DBClusterTypeDef = TypedDict(
    "DBClusterTypeDef",
    {
        "AllocatedStorage": int,
        "AvailabilityZones": List[str],
        "BackupRetentionPeriod": int,
        "CharacterSetName": str,
        "DatabaseName": str,
        "DBClusterIdentifier": str,
        "DBClusterParameterGroup": str,
        "DBSubnetGroup": str,
        "Status": str,
        "PercentProgress": str,
        "EarliestRestorableTime": datetime,
        "Endpoint": str,
        "ReaderEndpoint": str,
        "MultiAZ": bool,
        "Engine": str,
        "EngineVersion": str,
        "LatestRestorableTime": datetime,
        "Port": int,
        "MasterUsername": str,
        "DBClusterOptionGroupMemberships": List[DBClusterOptionGroupStatusTypeDef],
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReplicationSourceIdentifier": str,
        "ReadReplicaIdentifiers": List[str],
        "DBClusterMembers": List[DBClusterMemberTypeDef],
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "HostedZoneId": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterResourceId": str,
        "DBClusterArn": str,
        "AssociatedRoles": List[DBClusterRoleTypeDef],
        "IAMDatabaseAuthenticationEnabled": bool,
        "CloneGroupId": str,
        "ClusterCreateTime": datetime,
        "CopyTagsToSnapshot": bool,
        "EnabledCloudwatchLogsExports": List[str],
        "DeletionProtection": bool,
        "CrossAccountClone": bool,
        "AutomaticRestartTime": datetime,
    },
    total=False,
)

DBEngineVersionTypeDef = TypedDict(
    "DBEngineVersionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "DBEngineDescription": str,
        "DBEngineVersionDescription": str,
        "DefaultCharacterSet": CharacterSetTypeDef,
        "SupportedCharacterSets": List[CharacterSetTypeDef],
        "ValidUpgradeTarget": List[UpgradeTargetTypeDef],
        "SupportedTimezones": List[TimezoneTypeDef],
        "ExportableLogTypes": List[str],
        "SupportsLogExportsToCloudwatchLogs": bool,
        "SupportsReadReplica": bool,
    },
    total=False,
)

DescribeDBClusterEndpointsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterEndpointsMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterEndpointIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBClusterParameterGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBClusterParametersMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalDescribeDBClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBClusterParametersMessageRequestTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBClusterParametersMessageRequestTypeDef(
    _RequiredDescribeDBClusterParametersMessageRequestTypeDef,
    _OptionalDescribeDBClusterParametersMessageRequestTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
    },
    total=False,
)

DescribeDBClustersMessageRequestTypeDef = TypedDict(
    "DescribeDBClustersMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBEngineVersionsMessageRequestTypeDef = TypedDict(
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "DefaultOnly": bool,
        "ListSupportedCharacterSets": bool,
        "ListSupportedTimezones": bool,
    },
    total=False,
)

DescribeDBInstancesMessageRequestTypeDef = TypedDict(
    "DescribeDBInstancesMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBParameterGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBParameterGroupsMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBParametersMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
    },
)
_OptionalDescribeDBParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBParametersMessageRequestTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBParametersMessageRequestTypeDef(
    _RequiredDescribeDBParametersMessageRequestTypeDef,
    _OptionalDescribeDBParametersMessageRequestTypeDef,
):
    pass


DescribeDBSubnetGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeEngineDefaultClusterParametersMessageRequestTypeDef(
    _RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef,
    _OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef,
):
    pass


_RequiredDescribeEngineDefaultParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultParametersMessageRequestTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultParametersMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeEngineDefaultParametersMessageRequestTypeDef(
    _RequiredDescribeEngineDefaultParametersMessageRequestTypeDef,
    _OptionalDescribeEngineDefaultParametersMessageRequestTypeDef,
):
    pass


DescribeEventCategoriesMessageRequestTypeDef = TypedDict(
    "DescribeEventCategoriesMessageRequestTypeDef",
    {
        "SourceType": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

DescribeEventSubscriptionsMessageRequestTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
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
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    {
        "Engine": str,
    },
)
_OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    {
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "Vpc": bool,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeOrderableDBInstanceOptionsMessageRequestTypeDef(
    _RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
    _OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
):
    pass


DescribePendingMaintenanceActionsMessageRequestTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

_RequiredListTagsForResourceMessageRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
    },
)
_OptionalListTagsForResourceMessageRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class ListTagsForResourceMessageRequestTypeDef(
    _RequiredListTagsForResourceMessageRequestTypeDef,
    _OptionalListTagsForResourceMessageRequestTypeDef,
):
    pass


DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef = TypedDict(
    "DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterEndpointIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef(
    _RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
    _OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "IncludeShared": bool,
        "IncludePublic": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef = TypedDict(
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef = TypedDict(
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "Filters": Sequence[FilterTypeDef],
        "DefaultOnly": bool,
        "ListSupportedCharacterSets": bool,
        "ListSupportedTimezones": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef = TypedDict(
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef",
    {
        "DBParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    {
        "DBParameterGroupName": str,
    },
)
_OptionalDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBParametersMessageDescribeDBParametersPaginateTypeDef(
    _RequiredDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef,
    _OptionalDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef,
):
    pass


DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    {
        "DBSubnetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef(
    _RequiredDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef,
    _OptionalDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef,
):
    pass


DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
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
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    {
        "Engine": str,
    },
)
_OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    {
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "Vpc": bool,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef(
    _RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
    _OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
):
    pass


DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef = (
    TypedDict(
        "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
        {
            "ResourceIdentifier": str,
            "Filters": Sequence[FilterTypeDef],
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef = TypedDict(
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef = TypedDict(
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

EventCategoriesMessageTypeDef = TypedDict(
    "EventCategoriesMessageTypeDef",
    {
        "EventCategoriesMapList": List[EventCategoriesMapTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventsMessageTypeDef = TypedDict(
    "EventsMessageTypeDef",
    {
        "Marker": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PendingModifiedValuesTypeDef = TypedDict(
    "PendingModifiedValuesTypeDef",
    {
        "DBInstanceClass": str,
        "AllocatedStorage": int,
        "MasterUserPassword": str,
        "Port": int,
        "BackupRetentionPeriod": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "DBInstanceIdentifier": str,
        "StorageType": str,
        "CACertificateIdentifier": str,
        "DBSubnetGroupName": str,
        "PendingCloudwatchLogsExports": PendingCloudwatchLogsExportsTypeDef,
    },
    total=False,
)

ResourcePendingMaintenanceActionsTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionsTypeDef",
    {
        "ResourceIdentifier": str,
        "PendingMaintenanceActionDetails": List[PendingMaintenanceActionTypeDef],
    },
    total=False,
)

ValidStorageOptionsTypeDef = TypedDict(
    "ValidStorageOptionsTypeDef",
    {
        "StorageType": str,
        "StorageSize": List[RangeTypeDef],
        "ProvisionedIops": List[RangeTypeDef],
        "IopsToStorageRatio": List[DoubleRangeTypeDef],
    },
    total=False,
)

OrderableDBInstanceOptionsMessageTypeDef = TypedDict(
    "OrderableDBInstanceOptionsMessageTypeDef",
    {
        "OrderableDBInstanceOptions": List[OrderableDBInstanceOptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBSubnetGroupTypeDef = TypedDict(
    "DBSubnetGroupTypeDef",
    {
        "DBSubnetGroupName": str,
        "DBSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetTypeDef],
        "DBSubnetGroupArn": str,
    },
    total=False,
)

DescribeEngineDefaultClusterParametersResultTypeDef = TypedDict(
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    {
        "EngineDefaults": EngineDefaultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEngineDefaultParametersResultTypeDef = TypedDict(
    "DescribeEngineDefaultParametersResultTypeDef",
    {
        "EngineDefaults": EngineDefaultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBClusterSnapshotAttributesResultTypeDef = TypedDict(
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    {
        "DBClusterSnapshotAttributesResult": DBClusterSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBClusterSnapshotAttributeResultTypeDef = TypedDict(
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    {
        "DBClusterSnapshotAttributesResult": DBClusterSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterResultTypeDef = TypedDict(
    "CreateDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterMessageTypeDef = TypedDict(
    "DBClusterMessageTypeDef",
    {
        "Marker": str,
        "DBClusters": List[DBClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterResultTypeDef = TypedDict(
    "DeleteDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FailoverDBClusterResultTypeDef = TypedDict(
    "FailoverDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBClusterResultTypeDef = TypedDict(
    "ModifyDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PromoteReadReplicaDBClusterResultTypeDef = TypedDict(
    "PromoteReadReplicaDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterFromSnapshotResultTypeDef = TypedDict(
    "RestoreDBClusterFromSnapshotResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterToPointInTimeResultTypeDef = TypedDict(
    "RestoreDBClusterToPointInTimeResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDBClusterResultTypeDef = TypedDict(
    "StartDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDBClusterResultTypeDef = TypedDict(
    "StopDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBEngineVersionMessageTypeDef = TypedDict(
    "DBEngineVersionMessageTypeDef",
    {
        "Marker": str,
        "DBEngineVersions": List[DBEngineVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ApplyPendingMaintenanceActionResultTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionResultTypeDef",
    {
        "ResourcePendingMaintenanceActions": ResourcePendingMaintenanceActionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PendingMaintenanceActionsMessageTypeDef = TypedDict(
    "PendingMaintenanceActionsMessageTypeDef",
    {
        "PendingMaintenanceActions": List[ResourcePendingMaintenanceActionsTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidDBInstanceModificationsMessageTypeDef = TypedDict(
    "ValidDBInstanceModificationsMessageTypeDef",
    {
        "Storage": List[ValidStorageOptionsTypeDef],
    },
    total=False,
)

CreateDBSubnetGroupResultTypeDef = TypedDict(
    "CreateDBSubnetGroupResultTypeDef",
    {
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceTypeDef = TypedDict(
    "DBInstanceTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
        "DBInstanceStatus": str,
        "MasterUsername": str,
        "DBName": str,
        "Endpoint": EndpointTypeDef,
        "AllocatedStorage": int,
        "InstanceCreateTime": datetime,
        "PreferredBackupWindow": str,
        "BackupRetentionPeriod": int,
        "DBSecurityGroups": List[DBSecurityGroupMembershipTypeDef],
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "DBParameterGroups": List[DBParameterGroupStatusTypeDef],
        "AvailabilityZone": str,
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": PendingModifiedValuesTypeDef,
        "LatestRestorableTime": datetime,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "ReadReplicaSourceDBInstanceIdentifier": str,
        "ReadReplicaDBInstanceIdentifiers": List[str],
        "ReadReplicaDBClusterIdentifiers": List[str],
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupMemberships": List[OptionGroupMembershipTypeDef],
        "CharacterSetName": str,
        "SecondaryAvailabilityZone": str,
        "PubliclyAccessible": bool,
        "StatusInfos": List[DBInstanceStatusInfoTypeDef],
        "StorageType": str,
        "TdeCredentialArn": str,
        "DbInstancePort": int,
        "DBClusterIdentifier": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbiResourceId": str,
        "CACertificateIdentifier": str,
        "DomainMemberships": List[DomainMembershipTypeDef],
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "EnhancedMonitoringResourceArn": str,
        "MonitoringRoleArn": str,
        "PromotionTier": int,
        "DBInstanceArn": str,
        "Timezone": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "PerformanceInsightsEnabled": bool,
        "PerformanceInsightsKMSKeyId": str,
        "EnabledCloudwatchLogsExports": List[str],
        "DeletionProtection": bool,
    },
    total=False,
)

DBSubnetGroupMessageTypeDef = TypedDict(
    "DBSubnetGroupMessageTypeDef",
    {
        "Marker": str,
        "DBSubnetGroups": List[DBSubnetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBSubnetGroupResultTypeDef = TypedDict(
    "ModifyDBSubnetGroupResultTypeDef",
    {
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeValidDBInstanceModificationsResultTypeDef = TypedDict(
    "DescribeValidDBInstanceModificationsResultTypeDef",
    {
        "ValidDBInstanceModificationsMessage": ValidDBInstanceModificationsMessageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBInstanceResultTypeDef = TypedDict(
    "CreateDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceMessageTypeDef = TypedDict(
    "DBInstanceMessageTypeDef",
    {
        "Marker": str,
        "DBInstances": List[DBInstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBInstanceResultTypeDef = TypedDict(
    "DeleteDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBInstanceResultTypeDef = TypedDict(
    "ModifyDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootDBInstanceResultTypeDef = TypedDict(
    "RebootDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
