"""
Type annotations for workspaces service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/type_defs/)

Usage::

    ```python
    from mypy_boto3_workspaces.type_defs import AccountModificationTypeDef

    data: AccountModificationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AccessPropertyValueType,
    ApplicationType,
    AssociationStatusType,
    ClientDeviceTypeType,
    ComputeType,
    ConnectionAliasStateType,
    ConnectionStateType,
    DedicatedTenancyModificationStateEnumType,
    DedicatedTenancySupportResultEnumType,
    ImageTypeType,
    ModificationResourceEnumType,
    ModificationStateEnumType,
    OperatingSystemTypeType,
    ReconnectEnumType,
    RunningModeType,
    TargetWorkspaceStateType,
    TenancyType,
    WorkspaceDirectoryStateType,
    WorkspaceDirectoryTypeType,
    WorkspaceImageIngestionProcessType,
    WorkspaceImageRequiredTenancyType,
    WorkspaceImageStateType,
    WorkspaceStateType,
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
    "AccountModificationTypeDef",
    "AssociateConnectionAliasRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateIpGroupsRequestRequestTypeDef",
    "IpRuleItemTypeDef",
    "ClientPropertiesTypeDef",
    "ComputeTypeTypeDef",
    "ConnectClientAddInTypeDef",
    "ConnectionAliasAssociationTypeDef",
    "ConnectionAliasPermissionTypeDef",
    "TagTypeDef",
    "CreateConnectClientAddInRequestRequestTypeDef",
    "RootStorageTypeDef",
    "UserStorageTypeDef",
    "DefaultClientBrandingAttributesTypeDef",
    "DefaultImportClientBrandingAttributesTypeDef",
    "DefaultWorkspaceCreationPropertiesTypeDef",
    "DeleteClientBrandingRequestRequestTypeDef",
    "DeleteConnectClientAddInRequestRequestTypeDef",
    "DeleteConnectionAliasRequestRequestTypeDef",
    "DeleteIpGroupRequestRequestTypeDef",
    "DeleteTagsRequestRequestTypeDef",
    "DeleteWorkspaceBundleRequestRequestTypeDef",
    "DeleteWorkspaceImageRequestRequestTypeDef",
    "DeregisterWorkspaceDirectoryRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAccountModificationsRequestRequestTypeDef",
    "DescribeClientBrandingRequestRequestTypeDef",
    "IosClientBrandingAttributesTypeDef",
    "DescribeClientPropertiesRequestRequestTypeDef",
    "DescribeConnectClientAddInsRequestRequestTypeDef",
    "DescribeConnectionAliasPermissionsRequestRequestTypeDef",
    "DescribeConnectionAliasesRequestRequestTypeDef",
    "DescribeIpGroupsRequestRequestTypeDef",
    "DescribeTagsRequestRequestTypeDef",
    "DescribeWorkspaceBundlesRequestRequestTypeDef",
    "DescribeWorkspaceDirectoriesRequestRequestTypeDef",
    "DescribeWorkspaceImagePermissionsRequestRequestTypeDef",
    "ImagePermissionTypeDef",
    "DescribeWorkspaceImagesRequestRequestTypeDef",
    "DescribeWorkspaceSnapshotsRequestRequestTypeDef",
    "SnapshotTypeDef",
    "DescribeWorkspacesConnectionStatusRequestRequestTypeDef",
    "WorkspaceConnectionStatusTypeDef",
    "DescribeWorkspacesRequestRequestTypeDef",
    "DisassociateConnectionAliasRequestRequestTypeDef",
    "DisassociateIpGroupsRequestRequestTypeDef",
    "FailedWorkspaceChangeRequestTypeDef",
    "IosImportClientBrandingAttributesTypeDef",
    "ListAvailableManagementCidrRangesRequestRequestTypeDef",
    "MigrateWorkspaceRequestRequestTypeDef",
    "ModificationStateTypeDef",
    "ModifyAccountRequestRequestTypeDef",
    "SelfservicePermissionsTypeDef",
    "WorkspaceAccessPropertiesTypeDef",
    "WorkspaceCreationPropertiesTypeDef",
    "WorkspacePropertiesTypeDef",
    "ModifyWorkspaceStateRequestRequestTypeDef",
    "OperatingSystemTypeDef",
    "RebootRequestTypeDef",
    "RebuildRequestTypeDef",
    "RestoreWorkspaceRequestRequestTypeDef",
    "RevokeIpRulesRequestRequestTypeDef",
    "StartRequestTypeDef",
    "StopRequestTypeDef",
    "TerminateRequestTypeDef",
    "UpdateConnectClientAddInRequestRequestTypeDef",
    "UpdateResultTypeDef",
    "UpdateWorkspaceBundleRequestRequestTypeDef",
    "UpdateWorkspaceImagePermissionRequestRequestTypeDef",
    "AssociateConnectionAliasResultTypeDef",
    "CopyWorkspaceImageResultTypeDef",
    "CreateConnectClientAddInResultTypeDef",
    "CreateConnectionAliasResultTypeDef",
    "CreateIpGroupResultTypeDef",
    "CreateUpdatedWorkspaceImageResultTypeDef",
    "DescribeAccountModificationsResultTypeDef",
    "DescribeAccountResultTypeDef",
    "ImportWorkspaceImageResultTypeDef",
    "ListAvailableManagementCidrRangesResultTypeDef",
    "MigrateWorkspaceResultTypeDef",
    "AuthorizeIpRulesRequestRequestTypeDef",
    "UpdateRulesOfIpGroupRequestRequestTypeDef",
    "WorkspacesIpGroupTypeDef",
    "ClientPropertiesResultTypeDef",
    "ModifyClientPropertiesRequestRequestTypeDef",
    "DescribeConnectClientAddInsResultTypeDef",
    "ConnectionAliasTypeDef",
    "DescribeConnectionAliasPermissionsResultTypeDef",
    "UpdateConnectionAliasPermissionRequestRequestTypeDef",
    "CopyWorkspaceImageRequestRequestTypeDef",
    "CreateConnectionAliasRequestRequestTypeDef",
    "CreateIpGroupRequestRequestTypeDef",
    "CreateTagsRequestRequestTypeDef",
    "CreateUpdatedWorkspaceImageRequestRequestTypeDef",
    "DescribeTagsResultTypeDef",
    "ImportWorkspaceImageRequestRequestTypeDef",
    "RegisterWorkspaceDirectoryRequestRequestTypeDef",
    "CreateWorkspaceBundleRequestRequestTypeDef",
    "WorkspaceBundleTypeDef",
    "DescribeAccountModificationsRequestDescribeAccountModificationsPaginateTypeDef",
    "DescribeIpGroupsRequestDescribeIpGroupsPaginateTypeDef",
    "DescribeWorkspaceBundlesRequestDescribeWorkspaceBundlesPaginateTypeDef",
    "DescribeWorkspaceDirectoriesRequestDescribeWorkspaceDirectoriesPaginateTypeDef",
    "DescribeWorkspaceImagesRequestDescribeWorkspaceImagesPaginateTypeDef",
    "DescribeWorkspacesConnectionStatusRequestDescribeWorkspacesConnectionStatusPaginateTypeDef",
    "DescribeWorkspacesRequestDescribeWorkspacesPaginateTypeDef",
    "ListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef",
    "DescribeClientBrandingResultTypeDef",
    "ImportClientBrandingResultTypeDef",
    "DescribeWorkspaceImagePermissionsResultTypeDef",
    "DescribeWorkspaceSnapshotsResultTypeDef",
    "DescribeWorkspacesConnectionStatusResultTypeDef",
    "RebootWorkspacesResultTypeDef",
    "RebuildWorkspacesResultTypeDef",
    "StartWorkspacesResultTypeDef",
    "StopWorkspacesResultTypeDef",
    "TerminateWorkspacesResultTypeDef",
    "ImportClientBrandingRequestRequestTypeDef",
    "ModifySelfservicePermissionsRequestRequestTypeDef",
    "ModifyWorkspaceAccessPropertiesRequestRequestTypeDef",
    "WorkspaceDirectoryTypeDef",
    "ModifyWorkspaceCreationPropertiesRequestRequestTypeDef",
    "ModifyWorkspacePropertiesRequestRequestTypeDef",
    "WorkspaceRequestTypeDef",
    "WorkspaceTypeDef",
    "RebootWorkspacesRequestRequestTypeDef",
    "RebuildWorkspacesRequestRequestTypeDef",
    "StartWorkspacesRequestRequestTypeDef",
    "StopWorkspacesRequestRequestTypeDef",
    "TerminateWorkspacesRequestRequestTypeDef",
    "WorkspaceImageTypeDef",
    "DescribeIpGroupsResultTypeDef",
    "DescribeClientPropertiesResultTypeDef",
    "DescribeConnectionAliasesResultTypeDef",
    "CreateWorkspaceBundleResultTypeDef",
    "DescribeWorkspaceBundlesResultTypeDef",
    "DescribeWorkspaceDirectoriesResultTypeDef",
    "CreateWorkspacesRequestRequestTypeDef",
    "FailedCreateWorkspaceRequestTypeDef",
    "DescribeWorkspacesResultTypeDef",
    "DescribeWorkspaceImagesResultTypeDef",
    "CreateWorkspacesResultTypeDef",
)

AccountModificationTypeDef = TypedDict(
    "AccountModificationTypeDef",
    {
        "ModificationState": DedicatedTenancyModificationStateEnumType,
        "DedicatedTenancySupport": DedicatedTenancySupportResultEnumType,
        "DedicatedTenancyManagementCidrRange": str,
        "StartTime": datetime,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

AssociateConnectionAliasRequestRequestTypeDef = TypedDict(
    "AssociateConnectionAliasRequestRequestTypeDef",
    {
        "AliasId": str,
        "ResourceId": str,
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

AssociateIpGroupsRequestRequestTypeDef = TypedDict(
    "AssociateIpGroupsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "GroupIds": Sequence[str],
    },
)

IpRuleItemTypeDef = TypedDict(
    "IpRuleItemTypeDef",
    {
        "ipRule": str,
        "ruleDesc": str,
    },
    total=False,
)

ClientPropertiesTypeDef = TypedDict(
    "ClientPropertiesTypeDef",
    {
        "ReconnectEnabled": ReconnectEnumType,
    },
    total=False,
)

ComputeTypeTypeDef = TypedDict(
    "ComputeTypeTypeDef",
    {
        "Name": ComputeType,
    },
    total=False,
)

ConnectClientAddInTypeDef = TypedDict(
    "ConnectClientAddInTypeDef",
    {
        "AddInId": str,
        "ResourceId": str,
        "Name": str,
        "URL": str,
    },
    total=False,
)

ConnectionAliasAssociationTypeDef = TypedDict(
    "ConnectionAliasAssociationTypeDef",
    {
        "AssociationStatus": AssociationStatusType,
        "AssociatedAccountId": str,
        "ResourceId": str,
        "ConnectionIdentifier": str,
    },
    total=False,
)

ConnectionAliasPermissionTypeDef = TypedDict(
    "ConnectionAliasPermissionTypeDef",
    {
        "SharedAccountId": str,
        "AllowAssociation": bool,
    },
)

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


CreateConnectClientAddInRequestRequestTypeDef = TypedDict(
    "CreateConnectClientAddInRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Name": str,
        "URL": str,
    },
)

RootStorageTypeDef = TypedDict(
    "RootStorageTypeDef",
    {
        "Capacity": str,
    },
    total=False,
)

UserStorageTypeDef = TypedDict(
    "UserStorageTypeDef",
    {
        "Capacity": str,
    },
    total=False,
)

DefaultClientBrandingAttributesTypeDef = TypedDict(
    "DefaultClientBrandingAttributesTypeDef",
    {
        "LogoUrl": str,
        "SupportEmail": str,
        "SupportLink": str,
        "ForgotPasswordLink": str,
        "LoginMessage": Dict[str, str],
    },
    total=False,
)

DefaultImportClientBrandingAttributesTypeDef = TypedDict(
    "DefaultImportClientBrandingAttributesTypeDef",
    {
        "Logo": Union[str, bytes, IO[Any], StreamingBody],
        "SupportEmail": str,
        "SupportLink": str,
        "ForgotPasswordLink": str,
        "LoginMessage": Mapping[str, str],
    },
    total=False,
)

DefaultWorkspaceCreationPropertiesTypeDef = TypedDict(
    "DefaultWorkspaceCreationPropertiesTypeDef",
    {
        "EnableWorkDocs": bool,
        "EnableInternetAccess": bool,
        "DefaultOu": str,
        "CustomSecurityGroupId": str,
        "UserEnabledAsLocalAdministrator": bool,
        "EnableMaintenanceMode": bool,
    },
    total=False,
)

DeleteClientBrandingRequestRequestTypeDef = TypedDict(
    "DeleteClientBrandingRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Platforms": Sequence[ClientDeviceTypeType],
    },
)

DeleteConnectClientAddInRequestRequestTypeDef = TypedDict(
    "DeleteConnectClientAddInRequestRequestTypeDef",
    {
        "AddInId": str,
        "ResourceId": str,
    },
)

DeleteConnectionAliasRequestRequestTypeDef = TypedDict(
    "DeleteConnectionAliasRequestRequestTypeDef",
    {
        "AliasId": str,
    },
)

DeleteIpGroupRequestRequestTypeDef = TypedDict(
    "DeleteIpGroupRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

DeleteTagsRequestRequestTypeDef = TypedDict(
    "DeleteTagsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagKeys": Sequence[str],
    },
)

DeleteWorkspaceBundleRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceBundleRequestRequestTypeDef",
    {
        "BundleId": str,
    },
    total=False,
)

DeleteWorkspaceImageRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceImageRequestRequestTypeDef",
    {
        "ImageId": str,
    },
)

DeregisterWorkspaceDirectoryRequestRequestTypeDef = TypedDict(
    "DeregisterWorkspaceDirectoryRequestRequestTypeDef",
    {
        "DirectoryId": str,
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

DescribeAccountModificationsRequestRequestTypeDef = TypedDict(
    "DescribeAccountModificationsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

DescribeClientBrandingRequestRequestTypeDef = TypedDict(
    "DescribeClientBrandingRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

IosClientBrandingAttributesTypeDef = TypedDict(
    "IosClientBrandingAttributesTypeDef",
    {
        "LogoUrl": str,
        "Logo2xUrl": str,
        "Logo3xUrl": str,
        "SupportEmail": str,
        "SupportLink": str,
        "ForgotPasswordLink": str,
        "LoginMessage": Dict[str, str],
    },
    total=False,
)

DescribeClientPropertiesRequestRequestTypeDef = TypedDict(
    "DescribeClientPropertiesRequestRequestTypeDef",
    {
        "ResourceIds": Sequence[str],
    },
)

_RequiredDescribeConnectClientAddInsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeConnectClientAddInsRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalDescribeConnectClientAddInsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeConnectClientAddInsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeConnectClientAddInsRequestRequestTypeDef(
    _RequiredDescribeConnectClientAddInsRequestRequestTypeDef,
    _OptionalDescribeConnectClientAddInsRequestRequestTypeDef,
):
    pass


_RequiredDescribeConnectionAliasPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeConnectionAliasPermissionsRequestRequestTypeDef",
    {
        "AliasId": str,
    },
)
_OptionalDescribeConnectionAliasPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeConnectionAliasPermissionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeConnectionAliasPermissionsRequestRequestTypeDef(
    _RequiredDescribeConnectionAliasPermissionsRequestRequestTypeDef,
    _OptionalDescribeConnectionAliasPermissionsRequestRequestTypeDef,
):
    pass


DescribeConnectionAliasesRequestRequestTypeDef = TypedDict(
    "DescribeConnectionAliasesRequestRequestTypeDef",
    {
        "AliasIds": Sequence[str],
        "ResourceId": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeIpGroupsRequestRequestTypeDef = TypedDict(
    "DescribeIpGroupsRequestRequestTypeDef",
    {
        "GroupIds": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeTagsRequestRequestTypeDef = TypedDict(
    "DescribeTagsRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

DescribeWorkspaceBundlesRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceBundlesRequestRequestTypeDef",
    {
        "BundleIds": Sequence[str],
        "Owner": str,
        "NextToken": str,
    },
    total=False,
)

DescribeWorkspaceDirectoriesRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceDirectoriesRequestRequestTypeDef",
    {
        "DirectoryIds": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeWorkspaceImagePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeWorkspaceImagePermissionsRequestRequestTypeDef",
    {
        "ImageId": str,
    },
)
_OptionalDescribeWorkspaceImagePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeWorkspaceImagePermissionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeWorkspaceImagePermissionsRequestRequestTypeDef(
    _RequiredDescribeWorkspaceImagePermissionsRequestRequestTypeDef,
    _OptionalDescribeWorkspaceImagePermissionsRequestRequestTypeDef,
):
    pass


ImagePermissionTypeDef = TypedDict(
    "ImagePermissionTypeDef",
    {
        "SharedAccountId": str,
    },
    total=False,
)

DescribeWorkspaceImagesRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceImagesRequestRequestTypeDef",
    {
        "ImageIds": Sequence[str],
        "ImageType": ImageTypeType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeWorkspaceSnapshotsRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceSnapshotsRequestRequestTypeDef",
    {
        "WorkspaceId": str,
    },
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "SnapshotTime": datetime,
    },
    total=False,
)

DescribeWorkspacesConnectionStatusRequestRequestTypeDef = TypedDict(
    "DescribeWorkspacesConnectionStatusRequestRequestTypeDef",
    {
        "WorkspaceIds": Sequence[str],
        "NextToken": str,
    },
    total=False,
)

WorkspaceConnectionStatusTypeDef = TypedDict(
    "WorkspaceConnectionStatusTypeDef",
    {
        "WorkspaceId": str,
        "ConnectionState": ConnectionStateType,
        "ConnectionStateCheckTimestamp": datetime,
        "LastKnownUserConnectionTimestamp": datetime,
    },
    total=False,
)

DescribeWorkspacesRequestRequestTypeDef = TypedDict(
    "DescribeWorkspacesRequestRequestTypeDef",
    {
        "WorkspaceIds": Sequence[str],
        "DirectoryId": str,
        "UserName": str,
        "BundleId": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DisassociateConnectionAliasRequestRequestTypeDef = TypedDict(
    "DisassociateConnectionAliasRequestRequestTypeDef",
    {
        "AliasId": str,
    },
)

DisassociateIpGroupsRequestRequestTypeDef = TypedDict(
    "DisassociateIpGroupsRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "GroupIds": Sequence[str],
    },
)

FailedWorkspaceChangeRequestTypeDef = TypedDict(
    "FailedWorkspaceChangeRequestTypeDef",
    {
        "WorkspaceId": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

IosImportClientBrandingAttributesTypeDef = TypedDict(
    "IosImportClientBrandingAttributesTypeDef",
    {
        "Logo": Union[str, bytes, IO[Any], StreamingBody],
        "Logo2x": Union[str, bytes, IO[Any], StreamingBody],
        "Logo3x": Union[str, bytes, IO[Any], StreamingBody],
        "SupportEmail": str,
        "SupportLink": str,
        "ForgotPasswordLink": str,
        "LoginMessage": Mapping[str, str],
    },
    total=False,
)

_RequiredListAvailableManagementCidrRangesRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableManagementCidrRangesRequestRequestTypeDef",
    {
        "ManagementCidrRangeConstraint": str,
    },
)
_OptionalListAvailableManagementCidrRangesRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableManagementCidrRangesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAvailableManagementCidrRangesRequestRequestTypeDef(
    _RequiredListAvailableManagementCidrRangesRequestRequestTypeDef,
    _OptionalListAvailableManagementCidrRangesRequestRequestTypeDef,
):
    pass


MigrateWorkspaceRequestRequestTypeDef = TypedDict(
    "MigrateWorkspaceRequestRequestTypeDef",
    {
        "SourceWorkspaceId": str,
        "BundleId": str,
    },
)

ModificationStateTypeDef = TypedDict(
    "ModificationStateTypeDef",
    {
        "Resource": ModificationResourceEnumType,
        "State": ModificationStateEnumType,
    },
    total=False,
)

ModifyAccountRequestRequestTypeDef = TypedDict(
    "ModifyAccountRequestRequestTypeDef",
    {
        "DedicatedTenancySupport": Literal["ENABLED"],
        "DedicatedTenancyManagementCidrRange": str,
    },
    total=False,
)

SelfservicePermissionsTypeDef = TypedDict(
    "SelfservicePermissionsTypeDef",
    {
        "RestartWorkspace": ReconnectEnumType,
        "IncreaseVolumeSize": ReconnectEnumType,
        "ChangeComputeType": ReconnectEnumType,
        "SwitchRunningMode": ReconnectEnumType,
        "RebuildWorkspace": ReconnectEnumType,
    },
    total=False,
)

WorkspaceAccessPropertiesTypeDef = TypedDict(
    "WorkspaceAccessPropertiesTypeDef",
    {
        "DeviceTypeWindows": AccessPropertyValueType,
        "DeviceTypeOsx": AccessPropertyValueType,
        "DeviceTypeWeb": AccessPropertyValueType,
        "DeviceTypeIos": AccessPropertyValueType,
        "DeviceTypeAndroid": AccessPropertyValueType,
        "DeviceTypeChromeOs": AccessPropertyValueType,
        "DeviceTypeZeroClient": AccessPropertyValueType,
        "DeviceTypeLinux": AccessPropertyValueType,
    },
    total=False,
)

WorkspaceCreationPropertiesTypeDef = TypedDict(
    "WorkspaceCreationPropertiesTypeDef",
    {
        "EnableWorkDocs": bool,
        "EnableInternetAccess": bool,
        "DefaultOu": str,
        "CustomSecurityGroupId": str,
        "UserEnabledAsLocalAdministrator": bool,
        "EnableMaintenanceMode": bool,
    },
    total=False,
)

WorkspacePropertiesTypeDef = TypedDict(
    "WorkspacePropertiesTypeDef",
    {
        "RunningMode": RunningModeType,
        "RunningModeAutoStopTimeoutInMinutes": int,
        "RootVolumeSizeGib": int,
        "UserVolumeSizeGib": int,
        "ComputeTypeName": ComputeType,
    },
    total=False,
)

ModifyWorkspaceStateRequestRequestTypeDef = TypedDict(
    "ModifyWorkspaceStateRequestRequestTypeDef",
    {
        "WorkspaceId": str,
        "WorkspaceState": TargetWorkspaceStateType,
    },
)

OperatingSystemTypeDef = TypedDict(
    "OperatingSystemTypeDef",
    {
        "Type": OperatingSystemTypeType,
    },
    total=False,
)

RebootRequestTypeDef = TypedDict(
    "RebootRequestTypeDef",
    {
        "WorkspaceId": str,
    },
)

RebuildRequestTypeDef = TypedDict(
    "RebuildRequestTypeDef",
    {
        "WorkspaceId": str,
    },
)

RestoreWorkspaceRequestRequestTypeDef = TypedDict(
    "RestoreWorkspaceRequestRequestTypeDef",
    {
        "WorkspaceId": str,
    },
)

RevokeIpRulesRequestRequestTypeDef = TypedDict(
    "RevokeIpRulesRequestRequestTypeDef",
    {
        "GroupId": str,
        "UserRules": Sequence[str],
    },
)

StartRequestTypeDef = TypedDict(
    "StartRequestTypeDef",
    {
        "WorkspaceId": str,
    },
    total=False,
)

StopRequestTypeDef = TypedDict(
    "StopRequestTypeDef",
    {
        "WorkspaceId": str,
    },
    total=False,
)

TerminateRequestTypeDef = TypedDict(
    "TerminateRequestTypeDef",
    {
        "WorkspaceId": str,
    },
)

_RequiredUpdateConnectClientAddInRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConnectClientAddInRequestRequestTypeDef",
    {
        "AddInId": str,
        "ResourceId": str,
    },
)
_OptionalUpdateConnectClientAddInRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConnectClientAddInRequestRequestTypeDef",
    {
        "Name": str,
        "URL": str,
    },
    total=False,
)


class UpdateConnectClientAddInRequestRequestTypeDef(
    _RequiredUpdateConnectClientAddInRequestRequestTypeDef,
    _OptionalUpdateConnectClientAddInRequestRequestTypeDef,
):
    pass


UpdateResultTypeDef = TypedDict(
    "UpdateResultTypeDef",
    {
        "UpdateAvailable": bool,
        "Description": str,
    },
    total=False,
)

UpdateWorkspaceBundleRequestRequestTypeDef = TypedDict(
    "UpdateWorkspaceBundleRequestRequestTypeDef",
    {
        "BundleId": str,
        "ImageId": str,
    },
    total=False,
)

UpdateWorkspaceImagePermissionRequestRequestTypeDef = TypedDict(
    "UpdateWorkspaceImagePermissionRequestRequestTypeDef",
    {
        "ImageId": str,
        "AllowCopyImage": bool,
        "SharedAccountId": str,
    },
)

AssociateConnectionAliasResultTypeDef = TypedDict(
    "AssociateConnectionAliasResultTypeDef",
    {
        "ConnectionIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyWorkspaceImageResultTypeDef = TypedDict(
    "CopyWorkspaceImageResultTypeDef",
    {
        "ImageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConnectClientAddInResultTypeDef = TypedDict(
    "CreateConnectClientAddInResultTypeDef",
    {
        "AddInId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConnectionAliasResultTypeDef = TypedDict(
    "CreateConnectionAliasResultTypeDef",
    {
        "AliasId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIpGroupResultTypeDef = TypedDict(
    "CreateIpGroupResultTypeDef",
    {
        "GroupId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUpdatedWorkspaceImageResultTypeDef = TypedDict(
    "CreateUpdatedWorkspaceImageResultTypeDef",
    {
        "ImageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountModificationsResultTypeDef = TypedDict(
    "DescribeAccountModificationsResultTypeDef",
    {
        "AccountModifications": List[AccountModificationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountResultTypeDef = TypedDict(
    "DescribeAccountResultTypeDef",
    {
        "DedicatedTenancySupport": DedicatedTenancySupportResultEnumType,
        "DedicatedTenancyManagementCidrRange": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportWorkspaceImageResultTypeDef = TypedDict(
    "ImportWorkspaceImageResultTypeDef",
    {
        "ImageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAvailableManagementCidrRangesResultTypeDef = TypedDict(
    "ListAvailableManagementCidrRangesResultTypeDef",
    {
        "ManagementCidrRanges": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MigrateWorkspaceResultTypeDef = TypedDict(
    "MigrateWorkspaceResultTypeDef",
    {
        "SourceWorkspaceId": str,
        "TargetWorkspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AuthorizeIpRulesRequestRequestTypeDef = TypedDict(
    "AuthorizeIpRulesRequestRequestTypeDef",
    {
        "GroupId": str,
        "UserRules": Sequence[IpRuleItemTypeDef],
    },
)

UpdateRulesOfIpGroupRequestRequestTypeDef = TypedDict(
    "UpdateRulesOfIpGroupRequestRequestTypeDef",
    {
        "GroupId": str,
        "UserRules": Sequence[IpRuleItemTypeDef],
    },
)

WorkspacesIpGroupTypeDef = TypedDict(
    "WorkspacesIpGroupTypeDef",
    {
        "groupId": str,
        "groupName": str,
        "groupDesc": str,
        "userRules": List[IpRuleItemTypeDef],
    },
    total=False,
)

ClientPropertiesResultTypeDef = TypedDict(
    "ClientPropertiesResultTypeDef",
    {
        "ResourceId": str,
        "ClientProperties": ClientPropertiesTypeDef,
    },
    total=False,
)

ModifyClientPropertiesRequestRequestTypeDef = TypedDict(
    "ModifyClientPropertiesRequestRequestTypeDef",
    {
        "ResourceId": str,
        "ClientProperties": ClientPropertiesTypeDef,
    },
)

DescribeConnectClientAddInsResultTypeDef = TypedDict(
    "DescribeConnectClientAddInsResultTypeDef",
    {
        "AddIns": List[ConnectClientAddInTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConnectionAliasTypeDef = TypedDict(
    "ConnectionAliasTypeDef",
    {
        "ConnectionString": str,
        "AliasId": str,
        "State": ConnectionAliasStateType,
        "OwnerAccountId": str,
        "Associations": List[ConnectionAliasAssociationTypeDef],
    },
    total=False,
)

DescribeConnectionAliasPermissionsResultTypeDef = TypedDict(
    "DescribeConnectionAliasPermissionsResultTypeDef",
    {
        "AliasId": str,
        "ConnectionAliasPermissions": List[ConnectionAliasPermissionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConnectionAliasPermissionRequestRequestTypeDef = TypedDict(
    "UpdateConnectionAliasPermissionRequestRequestTypeDef",
    {
        "AliasId": str,
        "ConnectionAliasPermission": ConnectionAliasPermissionTypeDef,
    },
)

_RequiredCopyWorkspaceImageRequestRequestTypeDef = TypedDict(
    "_RequiredCopyWorkspaceImageRequestRequestTypeDef",
    {
        "Name": str,
        "SourceImageId": str,
        "SourceRegion": str,
    },
)
_OptionalCopyWorkspaceImageRequestRequestTypeDef = TypedDict(
    "_OptionalCopyWorkspaceImageRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyWorkspaceImageRequestRequestTypeDef(
    _RequiredCopyWorkspaceImageRequestRequestTypeDef,
    _OptionalCopyWorkspaceImageRequestRequestTypeDef,
):
    pass


_RequiredCreateConnectionAliasRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConnectionAliasRequestRequestTypeDef",
    {
        "ConnectionString": str,
    },
)
_OptionalCreateConnectionAliasRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConnectionAliasRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateConnectionAliasRequestRequestTypeDef(
    _RequiredCreateConnectionAliasRequestRequestTypeDef,
    _OptionalCreateConnectionAliasRequestRequestTypeDef,
):
    pass


_RequiredCreateIpGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIpGroupRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalCreateIpGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIpGroupRequestRequestTypeDef",
    {
        "GroupDesc": str,
        "UserRules": Sequence[IpRuleItemTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateIpGroupRequestRequestTypeDef(
    _RequiredCreateIpGroupRequestRequestTypeDef, _OptionalCreateIpGroupRequestRequestTypeDef
):
    pass


CreateTagsRequestRequestTypeDef = TypedDict(
    "CreateTagsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateUpdatedWorkspaceImageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUpdatedWorkspaceImageRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "SourceImageId": str,
    },
)
_OptionalCreateUpdatedWorkspaceImageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUpdatedWorkspaceImageRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUpdatedWorkspaceImageRequestRequestTypeDef(
    _RequiredCreateUpdatedWorkspaceImageRequestRequestTypeDef,
    _OptionalCreateUpdatedWorkspaceImageRequestRequestTypeDef,
):
    pass


DescribeTagsResultTypeDef = TypedDict(
    "DescribeTagsResultTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImportWorkspaceImageRequestRequestTypeDef = TypedDict(
    "_RequiredImportWorkspaceImageRequestRequestTypeDef",
    {
        "Ec2ImageId": str,
        "IngestionProcess": WorkspaceImageIngestionProcessType,
        "ImageName": str,
        "ImageDescription": str,
    },
)
_OptionalImportWorkspaceImageRequestRequestTypeDef = TypedDict(
    "_OptionalImportWorkspaceImageRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "Applications": Sequence[ApplicationType],
    },
    total=False,
)


class ImportWorkspaceImageRequestRequestTypeDef(
    _RequiredImportWorkspaceImageRequestRequestTypeDef,
    _OptionalImportWorkspaceImageRequestRequestTypeDef,
):
    pass


_RequiredRegisterWorkspaceDirectoryRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterWorkspaceDirectoryRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "EnableWorkDocs": bool,
    },
)
_OptionalRegisterWorkspaceDirectoryRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterWorkspaceDirectoryRequestRequestTypeDef",
    {
        "SubnetIds": Sequence[str],
        "EnableSelfService": bool,
        "Tenancy": TenancyType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class RegisterWorkspaceDirectoryRequestRequestTypeDef(
    _RequiredRegisterWorkspaceDirectoryRequestRequestTypeDef,
    _OptionalRegisterWorkspaceDirectoryRequestRequestTypeDef,
):
    pass


_RequiredCreateWorkspaceBundleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkspaceBundleRequestRequestTypeDef",
    {
        "BundleName": str,
        "BundleDescription": str,
        "ImageId": str,
        "ComputeType": ComputeTypeTypeDef,
        "UserStorage": UserStorageTypeDef,
    },
)
_OptionalCreateWorkspaceBundleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkspaceBundleRequestRequestTypeDef",
    {
        "RootStorage": RootStorageTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWorkspaceBundleRequestRequestTypeDef(
    _RequiredCreateWorkspaceBundleRequestRequestTypeDef,
    _OptionalCreateWorkspaceBundleRequestRequestTypeDef,
):
    pass


WorkspaceBundleTypeDef = TypedDict(
    "WorkspaceBundleTypeDef",
    {
        "BundleId": str,
        "Name": str,
        "Owner": str,
        "Description": str,
        "ImageId": str,
        "RootStorage": RootStorageTypeDef,
        "UserStorage": UserStorageTypeDef,
        "ComputeType": ComputeTypeTypeDef,
        "LastUpdatedTime": datetime,
        "CreationTime": datetime,
    },
    total=False,
)

DescribeAccountModificationsRequestDescribeAccountModificationsPaginateTypeDef = TypedDict(
    "DescribeAccountModificationsRequestDescribeAccountModificationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeIpGroupsRequestDescribeIpGroupsPaginateTypeDef = TypedDict(
    "DescribeIpGroupsRequestDescribeIpGroupsPaginateTypeDef",
    {
        "GroupIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeWorkspaceBundlesRequestDescribeWorkspaceBundlesPaginateTypeDef = TypedDict(
    "DescribeWorkspaceBundlesRequestDescribeWorkspaceBundlesPaginateTypeDef",
    {
        "BundleIds": Sequence[str],
        "Owner": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeWorkspaceDirectoriesRequestDescribeWorkspaceDirectoriesPaginateTypeDef = TypedDict(
    "DescribeWorkspaceDirectoriesRequestDescribeWorkspaceDirectoriesPaginateTypeDef",
    {
        "DirectoryIds": Sequence[str],
        "Limit": int,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeWorkspaceImagesRequestDescribeWorkspaceImagesPaginateTypeDef = TypedDict(
    "DescribeWorkspaceImagesRequestDescribeWorkspaceImagesPaginateTypeDef",
    {
        "ImageIds": Sequence[str],
        "ImageType": ImageTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeWorkspacesConnectionStatusRequestDescribeWorkspacesConnectionStatusPaginateTypeDef = TypedDict(
    "DescribeWorkspacesConnectionStatusRequestDescribeWorkspacesConnectionStatusPaginateTypeDef",
    {
        "WorkspaceIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeWorkspacesRequestDescribeWorkspacesPaginateTypeDef = TypedDict(
    "DescribeWorkspacesRequestDescribeWorkspacesPaginateTypeDef",
    {
        "WorkspaceIds": Sequence[str],
        "DirectoryId": str,
        "UserName": str,
        "BundleId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef = TypedDict(
    "_RequiredListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef",
    {
        "ManagementCidrRangeConstraint": str,
    },
)
_OptionalListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef = TypedDict(
    "_OptionalListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef(
    _RequiredListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef,
    _OptionalListAvailableManagementCidrRangesRequestListAvailableManagementCidrRangesPaginateTypeDef,
):
    pass


DescribeClientBrandingResultTypeDef = TypedDict(
    "DescribeClientBrandingResultTypeDef",
    {
        "DeviceTypeWindows": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeOsx": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeAndroid": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeIos": IosClientBrandingAttributesTypeDef,
        "DeviceTypeLinux": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeWeb": DefaultClientBrandingAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportClientBrandingResultTypeDef = TypedDict(
    "ImportClientBrandingResultTypeDef",
    {
        "DeviceTypeWindows": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeOsx": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeAndroid": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeIos": IosClientBrandingAttributesTypeDef,
        "DeviceTypeLinux": DefaultClientBrandingAttributesTypeDef,
        "DeviceTypeWeb": DefaultClientBrandingAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceImagePermissionsResultTypeDef = TypedDict(
    "DescribeWorkspaceImagePermissionsResultTypeDef",
    {
        "ImageId": str,
        "ImagePermissions": List[ImagePermissionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceSnapshotsResultTypeDef = TypedDict(
    "DescribeWorkspaceSnapshotsResultTypeDef",
    {
        "RebuildSnapshots": List[SnapshotTypeDef],
        "RestoreSnapshots": List[SnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspacesConnectionStatusResultTypeDef = TypedDict(
    "DescribeWorkspacesConnectionStatusResultTypeDef",
    {
        "WorkspacesConnectionStatus": List[WorkspaceConnectionStatusTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootWorkspacesResultTypeDef = TypedDict(
    "RebootWorkspacesResultTypeDef",
    {
        "FailedRequests": List[FailedWorkspaceChangeRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebuildWorkspacesResultTypeDef = TypedDict(
    "RebuildWorkspacesResultTypeDef",
    {
        "FailedRequests": List[FailedWorkspaceChangeRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartWorkspacesResultTypeDef = TypedDict(
    "StartWorkspacesResultTypeDef",
    {
        "FailedRequests": List[FailedWorkspaceChangeRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopWorkspacesResultTypeDef = TypedDict(
    "StopWorkspacesResultTypeDef",
    {
        "FailedRequests": List[FailedWorkspaceChangeRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TerminateWorkspacesResultTypeDef = TypedDict(
    "TerminateWorkspacesResultTypeDef",
    {
        "FailedRequests": List[FailedWorkspaceChangeRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImportClientBrandingRequestRequestTypeDef = TypedDict(
    "_RequiredImportClientBrandingRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalImportClientBrandingRequestRequestTypeDef = TypedDict(
    "_OptionalImportClientBrandingRequestRequestTypeDef",
    {
        "DeviceTypeWindows": DefaultImportClientBrandingAttributesTypeDef,
        "DeviceTypeOsx": DefaultImportClientBrandingAttributesTypeDef,
        "DeviceTypeAndroid": DefaultImportClientBrandingAttributesTypeDef,
        "DeviceTypeIos": IosImportClientBrandingAttributesTypeDef,
        "DeviceTypeLinux": DefaultImportClientBrandingAttributesTypeDef,
        "DeviceTypeWeb": DefaultImportClientBrandingAttributesTypeDef,
    },
    total=False,
)


class ImportClientBrandingRequestRequestTypeDef(
    _RequiredImportClientBrandingRequestRequestTypeDef,
    _OptionalImportClientBrandingRequestRequestTypeDef,
):
    pass


ModifySelfservicePermissionsRequestRequestTypeDef = TypedDict(
    "ModifySelfservicePermissionsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "SelfservicePermissions": SelfservicePermissionsTypeDef,
    },
)

ModifyWorkspaceAccessPropertiesRequestRequestTypeDef = TypedDict(
    "ModifyWorkspaceAccessPropertiesRequestRequestTypeDef",
    {
        "ResourceId": str,
        "WorkspaceAccessProperties": WorkspaceAccessPropertiesTypeDef,
    },
)

WorkspaceDirectoryTypeDef = TypedDict(
    "WorkspaceDirectoryTypeDef",
    {
        "DirectoryId": str,
        "Alias": str,
        "DirectoryName": str,
        "RegistrationCode": str,
        "SubnetIds": List[str],
        "DnsIpAddresses": List[str],
        "CustomerUserName": str,
        "IamRoleId": str,
        "DirectoryType": WorkspaceDirectoryTypeType,
        "WorkspaceSecurityGroupId": str,
        "State": WorkspaceDirectoryStateType,
        "WorkspaceCreationProperties": DefaultWorkspaceCreationPropertiesTypeDef,
        "ipGroupIds": List[str],
        "WorkspaceAccessProperties": WorkspaceAccessPropertiesTypeDef,
        "Tenancy": TenancyType,
        "SelfservicePermissions": SelfservicePermissionsTypeDef,
    },
    total=False,
)

ModifyWorkspaceCreationPropertiesRequestRequestTypeDef = TypedDict(
    "ModifyWorkspaceCreationPropertiesRequestRequestTypeDef",
    {
        "ResourceId": str,
        "WorkspaceCreationProperties": WorkspaceCreationPropertiesTypeDef,
    },
)

ModifyWorkspacePropertiesRequestRequestTypeDef = TypedDict(
    "ModifyWorkspacePropertiesRequestRequestTypeDef",
    {
        "WorkspaceId": str,
        "WorkspaceProperties": WorkspacePropertiesTypeDef,
    },
)

_RequiredWorkspaceRequestTypeDef = TypedDict(
    "_RequiredWorkspaceRequestTypeDef",
    {
        "DirectoryId": str,
        "UserName": str,
        "BundleId": str,
    },
)
_OptionalWorkspaceRequestTypeDef = TypedDict(
    "_OptionalWorkspaceRequestTypeDef",
    {
        "VolumeEncryptionKey": str,
        "UserVolumeEncryptionEnabled": bool,
        "RootVolumeEncryptionEnabled": bool,
        "WorkspaceProperties": WorkspacePropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class WorkspaceRequestTypeDef(_RequiredWorkspaceRequestTypeDef, _OptionalWorkspaceRequestTypeDef):
    pass


WorkspaceTypeDef = TypedDict(
    "WorkspaceTypeDef",
    {
        "WorkspaceId": str,
        "DirectoryId": str,
        "UserName": str,
        "IpAddress": str,
        "State": WorkspaceStateType,
        "BundleId": str,
        "SubnetId": str,
        "ErrorMessage": str,
        "ErrorCode": str,
        "ComputerName": str,
        "VolumeEncryptionKey": str,
        "UserVolumeEncryptionEnabled": bool,
        "RootVolumeEncryptionEnabled": bool,
        "WorkspaceProperties": WorkspacePropertiesTypeDef,
        "ModificationStates": List[ModificationStateTypeDef],
    },
    total=False,
)

RebootWorkspacesRequestRequestTypeDef = TypedDict(
    "RebootWorkspacesRequestRequestTypeDef",
    {
        "RebootWorkspaceRequests": Sequence[RebootRequestTypeDef],
    },
)

RebuildWorkspacesRequestRequestTypeDef = TypedDict(
    "RebuildWorkspacesRequestRequestTypeDef",
    {
        "RebuildWorkspaceRequests": Sequence[RebuildRequestTypeDef],
    },
)

StartWorkspacesRequestRequestTypeDef = TypedDict(
    "StartWorkspacesRequestRequestTypeDef",
    {
        "StartWorkspaceRequests": Sequence[StartRequestTypeDef],
    },
)

StopWorkspacesRequestRequestTypeDef = TypedDict(
    "StopWorkspacesRequestRequestTypeDef",
    {
        "StopWorkspaceRequests": Sequence[StopRequestTypeDef],
    },
)

TerminateWorkspacesRequestRequestTypeDef = TypedDict(
    "TerminateWorkspacesRequestRequestTypeDef",
    {
        "TerminateWorkspaceRequests": Sequence[TerminateRequestTypeDef],
    },
)

WorkspaceImageTypeDef = TypedDict(
    "WorkspaceImageTypeDef",
    {
        "ImageId": str,
        "Name": str,
        "Description": str,
        "OperatingSystem": OperatingSystemTypeDef,
        "State": WorkspaceImageStateType,
        "RequiredTenancy": WorkspaceImageRequiredTenancyType,
        "ErrorCode": str,
        "ErrorMessage": str,
        "Created": datetime,
        "OwnerAccountId": str,
        "Updates": UpdateResultTypeDef,
    },
    total=False,
)

DescribeIpGroupsResultTypeDef = TypedDict(
    "DescribeIpGroupsResultTypeDef",
    {
        "Result": List[WorkspacesIpGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClientPropertiesResultTypeDef = TypedDict(
    "DescribeClientPropertiesResultTypeDef",
    {
        "ClientPropertiesList": List[ClientPropertiesResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConnectionAliasesResultTypeDef = TypedDict(
    "DescribeConnectionAliasesResultTypeDef",
    {
        "ConnectionAliases": List[ConnectionAliasTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkspaceBundleResultTypeDef = TypedDict(
    "CreateWorkspaceBundleResultTypeDef",
    {
        "WorkspaceBundle": WorkspaceBundleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceBundlesResultTypeDef = TypedDict(
    "DescribeWorkspaceBundlesResultTypeDef",
    {
        "Bundles": List[WorkspaceBundleTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceDirectoriesResultTypeDef = TypedDict(
    "DescribeWorkspaceDirectoriesResultTypeDef",
    {
        "Directories": List[WorkspaceDirectoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkspacesRequestRequestTypeDef = TypedDict(
    "CreateWorkspacesRequestRequestTypeDef",
    {
        "Workspaces": Sequence[WorkspaceRequestTypeDef],
    },
)

FailedCreateWorkspaceRequestTypeDef = TypedDict(
    "FailedCreateWorkspaceRequestTypeDef",
    {
        "WorkspaceRequest": WorkspaceRequestTypeDef,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

DescribeWorkspacesResultTypeDef = TypedDict(
    "DescribeWorkspacesResultTypeDef",
    {
        "Workspaces": List[WorkspaceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceImagesResultTypeDef = TypedDict(
    "DescribeWorkspaceImagesResultTypeDef",
    {
        "Images": List[WorkspaceImageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkspacesResultTypeDef = TypedDict(
    "CreateWorkspacesResultTypeDef",
    {
        "FailedRequests": List[FailedCreateWorkspaceRequestTypeDef],
        "PendingRequests": List[WorkspaceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
