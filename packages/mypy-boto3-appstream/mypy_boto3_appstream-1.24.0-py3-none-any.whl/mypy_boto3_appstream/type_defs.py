"""
Type annotations for appstream service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/type_defs/)

Usage::

    ```python
    from mypy_boto3_appstream.type_defs import AccessEndpointTypeDef

    data: AccessEndpointTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ActionType,
    ApplicationAttributeType,
    AppVisibilityType,
    AuthenticationTypeType,
    FleetAttributeType,
    FleetErrorCodeType,
    FleetStateType,
    FleetTypeType,
    ImageBuilderStateChangeReasonCodeType,
    ImageBuilderStateType,
    ImageStateChangeReasonCodeType,
    ImageStateType,
    MessageActionType,
    PermissionType,
    PlatformTypeType,
    SessionConnectionStateType,
    SessionStateType,
    StackAttributeType,
    StackErrorCodeType,
    StorageConnectorTypeType,
    StreamViewType,
    UsageReportExecutionErrorCodeType,
    UserStackAssociationErrorCodeType,
    VisibilityTypeType,
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
    "AccessEndpointTypeDef",
    "S3LocationTypeDef",
    "ApplicationFleetAssociationTypeDef",
    "ApplicationSettingsResponseTypeDef",
    "ApplicationSettingsTypeDef",
    "AssociateApplicationFleetRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateApplicationToEntitlementRequestRequestTypeDef",
    "AssociateFleetRequestRequestTypeDef",
    "UserStackAssociationTypeDef",
    "ComputeCapacityStatusTypeDef",
    "ComputeCapacityTypeDef",
    "CopyImageRequestRequestTypeDef",
    "ServiceAccountCredentialsTypeDef",
    "EntitlementAttributeTypeDef",
    "DomainJoinInfoTypeDef",
    "VpcConfigTypeDef",
    "CreateImageBuilderStreamingURLRequestRequestTypeDef",
    "StorageConnectorTypeDef",
    "UserSettingTypeDef",
    "CreateStreamingURLRequestRequestTypeDef",
    "CreateUpdatedImageRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DeleteAppBlockRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteDirectoryConfigRequestRequestTypeDef",
    "DeleteEntitlementRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteImageBuilderRequestRequestTypeDef",
    "DeleteImagePermissionsRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteStackRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeAppBlocksRequestRequestTypeDef",
    "DescribeApplicationFleetAssociationsRequestRequestTypeDef",
    "DescribeApplicationsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDirectoryConfigsRequestRequestTypeDef",
    "DescribeEntitlementsRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeFleetsRequestRequestTypeDef",
    "DescribeImageBuildersRequestRequestTypeDef",
    "DescribeImagePermissionsRequestRequestTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "DescribeSessionsRequestRequestTypeDef",
    "DescribeStacksRequestRequestTypeDef",
    "DescribeUsageReportSubscriptionsRequestRequestTypeDef",
    "DescribeUserStackAssociationsRequestRequestTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "UserTypeDef",
    "DisableUserRequestRequestTypeDef",
    "DisassociateApplicationFleetRequestRequestTypeDef",
    "DisassociateApplicationFromEntitlementRequestRequestTypeDef",
    "DisassociateFleetRequestRequestTypeDef",
    "EnableUserRequestRequestTypeDef",
    "EntitledApplicationTypeDef",
    "ExpireSessionRequestRequestTypeDef",
    "FleetErrorTypeDef",
    "ImageBuilderStateChangeReasonTypeDef",
    "NetworkAccessConfigurationTypeDef",
    "ResourceErrorTypeDef",
    "ImagePermissionsTypeDef",
    "ImageStateChangeReasonTypeDef",
    "LastReportGenerationExecutionErrorTypeDef",
    "ListAssociatedFleetsRequestRequestTypeDef",
    "ListAssociatedStacksRequestRequestTypeDef",
    "ListEntitledApplicationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StackErrorTypeDef",
    "StartFleetRequestRequestTypeDef",
    "StartImageBuilderRequestRequestTypeDef",
    "StopFleetRequestRequestTypeDef",
    "StopImageBuilderRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ApplicationTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ScriptDetailsTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "AssociateApplicationFleetResultTypeDef",
    "CopyImageResponseTypeDef",
    "CreateImageBuilderStreamingURLResultTypeDef",
    "CreateStreamingURLResultTypeDef",
    "CreateUsageReportSubscriptionResultTypeDef",
    "DescribeApplicationFleetAssociationsResultTypeDef",
    "ListAssociatedFleetsResultTypeDef",
    "ListAssociatedStacksResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "BatchAssociateUserStackRequestRequestTypeDef",
    "BatchDisassociateUserStackRequestRequestTypeDef",
    "DescribeUserStackAssociationsResultTypeDef",
    "UserStackAssociationErrorTypeDef",
    "CreateDirectoryConfigRequestRequestTypeDef",
    "DirectoryConfigTypeDef",
    "UpdateDirectoryConfigRequestRequestTypeDef",
    "CreateEntitlementRequestRequestTypeDef",
    "EntitlementTypeDef",
    "UpdateEntitlementRequestRequestTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "CreateImageBuilderRequestRequestTypeDef",
    "UpdateFleetRequestRequestTypeDef",
    "CreateStackRequestRequestTypeDef",
    "UpdateStackRequestRequestTypeDef",
    "DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef",
    "DescribeFleetsRequestDescribeFleetsPaginateTypeDef",
    "DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef",
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    "DescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    "DescribeStacksRequestDescribeStacksPaginateTypeDef",
    "DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef",
    "DescribeUsersRequestDescribeUsersPaginateTypeDef",
    "ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef",
    "ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef",
    "DescribeFleetsRequestFleetStartedWaitTypeDef",
    "DescribeFleetsRequestFleetStoppedWaitTypeDef",
    "DescribeUsersResultTypeDef",
    "ListEntitledApplicationsResultTypeDef",
    "FleetTypeDef",
    "SessionTypeDef",
    "ImageBuilderTypeDef",
    "SharedImagePermissionsTypeDef",
    "UpdateImagePermissionsRequestRequestTypeDef",
    "UsageReportSubscriptionTypeDef",
    "StackTypeDef",
    "CreateApplicationResultTypeDef",
    "DescribeApplicationsResultTypeDef",
    "ImageTypeDef",
    "UpdateApplicationResultTypeDef",
    "AppBlockTypeDef",
    "CreateAppBlockRequestRequestTypeDef",
    "BatchAssociateUserStackResultTypeDef",
    "BatchDisassociateUserStackResultTypeDef",
    "CreateDirectoryConfigResultTypeDef",
    "DescribeDirectoryConfigsResultTypeDef",
    "UpdateDirectoryConfigResultTypeDef",
    "CreateEntitlementResultTypeDef",
    "DescribeEntitlementsResultTypeDef",
    "UpdateEntitlementResultTypeDef",
    "CreateFleetResultTypeDef",
    "DescribeFleetsResultTypeDef",
    "UpdateFleetResultTypeDef",
    "DescribeSessionsResultTypeDef",
    "CreateImageBuilderResultTypeDef",
    "DeleteImageBuilderResultTypeDef",
    "DescribeImageBuildersResultTypeDef",
    "StartImageBuilderResultTypeDef",
    "StopImageBuilderResultTypeDef",
    "DescribeImagePermissionsResultTypeDef",
    "DescribeUsageReportSubscriptionsResultTypeDef",
    "CreateStackResultTypeDef",
    "DescribeStacksResultTypeDef",
    "UpdateStackResultTypeDef",
    "CreateUpdatedImageResultTypeDef",
    "DeleteImageResultTypeDef",
    "DescribeImagesResultTypeDef",
    "CreateAppBlockResultTypeDef",
    "DescribeAppBlocksResultTypeDef",
)

_RequiredAccessEndpointTypeDef = TypedDict(
    "_RequiredAccessEndpointTypeDef",
    {
        "EndpointType": Literal["STREAMING"],
    },
)
_OptionalAccessEndpointTypeDef = TypedDict(
    "_OptionalAccessEndpointTypeDef",
    {
        "VpceId": str,
    },
    total=False,
)


class AccessEndpointTypeDef(_RequiredAccessEndpointTypeDef, _OptionalAccessEndpointTypeDef):
    pass


S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "S3Bucket": str,
        "S3Key": str,
    },
)

ApplicationFleetAssociationTypeDef = TypedDict(
    "ApplicationFleetAssociationTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
    },
)

ApplicationSettingsResponseTypeDef = TypedDict(
    "ApplicationSettingsResponseTypeDef",
    {
        "Enabled": bool,
        "SettingsGroup": str,
        "S3BucketName": str,
    },
    total=False,
)

_RequiredApplicationSettingsTypeDef = TypedDict(
    "_RequiredApplicationSettingsTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalApplicationSettingsTypeDef = TypedDict(
    "_OptionalApplicationSettingsTypeDef",
    {
        "SettingsGroup": str,
    },
    total=False,
)


class ApplicationSettingsTypeDef(
    _RequiredApplicationSettingsTypeDef, _OptionalApplicationSettingsTypeDef
):
    pass


AssociateApplicationFleetRequestRequestTypeDef = TypedDict(
    "AssociateApplicationFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
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

AssociateApplicationToEntitlementRequestRequestTypeDef = TypedDict(
    "AssociateApplicationToEntitlementRequestRequestTypeDef",
    {
        "StackName": str,
        "EntitlementName": str,
        "ApplicationIdentifier": str,
    },
)

AssociateFleetRequestRequestTypeDef = TypedDict(
    "AssociateFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "StackName": str,
    },
)

_RequiredUserStackAssociationTypeDef = TypedDict(
    "_RequiredUserStackAssociationTypeDef",
    {
        "StackName": str,
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalUserStackAssociationTypeDef = TypedDict(
    "_OptionalUserStackAssociationTypeDef",
    {
        "SendEmailNotification": bool,
    },
    total=False,
)


class UserStackAssociationTypeDef(
    _RequiredUserStackAssociationTypeDef, _OptionalUserStackAssociationTypeDef
):
    pass


_RequiredComputeCapacityStatusTypeDef = TypedDict(
    "_RequiredComputeCapacityStatusTypeDef",
    {
        "Desired": int,
    },
)
_OptionalComputeCapacityStatusTypeDef = TypedDict(
    "_OptionalComputeCapacityStatusTypeDef",
    {
        "Running": int,
        "InUse": int,
        "Available": int,
    },
    total=False,
)


class ComputeCapacityStatusTypeDef(
    _RequiredComputeCapacityStatusTypeDef, _OptionalComputeCapacityStatusTypeDef
):
    pass


ComputeCapacityTypeDef = TypedDict(
    "ComputeCapacityTypeDef",
    {
        "DesiredInstances": int,
    },
)

_RequiredCopyImageRequestRequestTypeDef = TypedDict(
    "_RequiredCopyImageRequestRequestTypeDef",
    {
        "SourceImageName": str,
        "DestinationImageName": str,
        "DestinationRegion": str,
    },
)
_OptionalCopyImageRequestRequestTypeDef = TypedDict(
    "_OptionalCopyImageRequestRequestTypeDef",
    {
        "DestinationImageDescription": str,
    },
    total=False,
)


class CopyImageRequestRequestTypeDef(
    _RequiredCopyImageRequestRequestTypeDef, _OptionalCopyImageRequestRequestTypeDef
):
    pass


ServiceAccountCredentialsTypeDef = TypedDict(
    "ServiceAccountCredentialsTypeDef",
    {
        "AccountName": str,
        "AccountPassword": str,
    },
)

EntitlementAttributeTypeDef = TypedDict(
    "EntitlementAttributeTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

DomainJoinInfoTypeDef = TypedDict(
    "DomainJoinInfoTypeDef",
    {
        "DirectoryName": str,
        "OrganizationalUnitDistinguishedName": str,
    },
    total=False,
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

_RequiredCreateImageBuilderStreamingURLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageBuilderStreamingURLRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateImageBuilderStreamingURLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageBuilderStreamingURLRequestRequestTypeDef",
    {
        "Validity": int,
    },
    total=False,
)


class CreateImageBuilderStreamingURLRequestRequestTypeDef(
    _RequiredCreateImageBuilderStreamingURLRequestRequestTypeDef,
    _OptionalCreateImageBuilderStreamingURLRequestRequestTypeDef,
):
    pass


_RequiredStorageConnectorTypeDef = TypedDict(
    "_RequiredStorageConnectorTypeDef",
    {
        "ConnectorType": StorageConnectorTypeType,
    },
)
_OptionalStorageConnectorTypeDef = TypedDict(
    "_OptionalStorageConnectorTypeDef",
    {
        "ResourceIdentifier": str,
        "Domains": Sequence[str],
    },
    total=False,
)


class StorageConnectorTypeDef(_RequiredStorageConnectorTypeDef, _OptionalStorageConnectorTypeDef):
    pass


UserSettingTypeDef = TypedDict(
    "UserSettingTypeDef",
    {
        "Action": ActionType,
        "Permission": PermissionType,
    },
)

_RequiredCreateStreamingURLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamingURLRequestRequestTypeDef",
    {
        "StackName": str,
        "FleetName": str,
        "UserId": str,
    },
)
_OptionalCreateStreamingURLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamingURLRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "Validity": int,
        "SessionContext": str,
    },
    total=False,
)


class CreateStreamingURLRequestRequestTypeDef(
    _RequiredCreateStreamingURLRequestRequestTypeDef,
    _OptionalCreateStreamingURLRequestRequestTypeDef,
):
    pass


_RequiredCreateUpdatedImageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUpdatedImageRequestRequestTypeDef",
    {
        "existingImageName": str,
        "newImageName": str,
    },
)
_OptionalCreateUpdatedImageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUpdatedImageRequestRequestTypeDef",
    {
        "newImageDescription": str,
        "newImageDisplayName": str,
        "newImageTags": Mapping[str, str],
        "dryRun": bool,
    },
    total=False,
)


class CreateUpdatedImageRequestRequestTypeDef(
    _RequiredCreateUpdatedImageRequestRequestTypeDef,
    _OptionalCreateUpdatedImageRequestRequestTypeDef,
):
    pass


_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "MessageAction": MessageActionType,
        "FirstName": str,
        "LastName": str,
    },
    total=False,
)


class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass


DeleteAppBlockRequestRequestTypeDef = TypedDict(
    "DeleteAppBlockRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteDirectoryConfigRequestRequestTypeDef = TypedDict(
    "DeleteDirectoryConfigRequestRequestTypeDef",
    {
        "DirectoryName": str,
    },
)

DeleteEntitlementRequestRequestTypeDef = TypedDict(
    "DeleteEntitlementRequestRequestTypeDef",
    {
        "Name": str,
        "StackName": str,
    },
)

DeleteFleetRequestRequestTypeDef = TypedDict(
    "DeleteFleetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteImageBuilderRequestRequestTypeDef = TypedDict(
    "DeleteImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteImagePermissionsRequestRequestTypeDef = TypedDict(
    "DeleteImagePermissionsRequestRequestTypeDef",
    {
        "Name": str,
        "SharedAccountId": str,
    },
)

DeleteImageRequestRequestTypeDef = TypedDict(
    "DeleteImageRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteStackRequestRequestTypeDef = TypedDict(
    "DeleteStackRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)

DescribeAppBlocksRequestRequestTypeDef = TypedDict(
    "DescribeAppBlocksRequestRequestTypeDef",
    {
        "Arns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeApplicationFleetAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeApplicationFleetAssociationsRequestRequestTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeApplicationsRequestRequestTypeDef = TypedDict(
    "DescribeApplicationsRequestRequestTypeDef",
    {
        "Arns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
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

DescribeDirectoryConfigsRequestRequestTypeDef = TypedDict(
    "DescribeDirectoryConfigsRequestRequestTypeDef",
    {
        "DirectoryNames": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeEntitlementsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEntitlementsRequestRequestTypeDef",
    {
        "StackName": str,
    },
)
_OptionalDescribeEntitlementsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEntitlementsRequestRequestTypeDef",
    {
        "Name": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeEntitlementsRequestRequestTypeDef(
    _RequiredDescribeEntitlementsRequestRequestTypeDef,
    _OptionalDescribeEntitlementsRequestRequestTypeDef,
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

DescribeFleetsRequestRequestTypeDef = TypedDict(
    "DescribeFleetsRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
    },
    total=False,
)

DescribeImageBuildersRequestRequestTypeDef = TypedDict(
    "DescribeImageBuildersRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeImagePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImagePermissionsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDescribeImagePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImagePermissionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "SharedAwsAccountIds": Sequence[str],
        "NextToken": str,
    },
    total=False,
)


class DescribeImagePermissionsRequestRequestTypeDef(
    _RequiredDescribeImagePermissionsRequestRequestTypeDef,
    _OptionalDescribeImagePermissionsRequestRequestTypeDef,
):
    pass


DescribeImagesRequestRequestTypeDef = TypedDict(
    "DescribeImagesRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "Arns": Sequence[str],
        "Type": VisibilityTypeType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredDescribeSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSessionsRequestRequestTypeDef",
    {
        "StackName": str,
        "FleetName": str,
    },
)
_OptionalDescribeSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSessionsRequestRequestTypeDef",
    {
        "UserId": str,
        "NextToken": str,
        "Limit": int,
        "AuthenticationType": AuthenticationTypeType,
    },
    total=False,
)


class DescribeSessionsRequestRequestTypeDef(
    _RequiredDescribeSessionsRequestRequestTypeDef, _OptionalDescribeSessionsRequestRequestTypeDef
):
    pass


DescribeStacksRequestRequestTypeDef = TypedDict(
    "DescribeStacksRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
    },
    total=False,
)

DescribeUsageReportSubscriptionsRequestRequestTypeDef = TypedDict(
    "DescribeUsageReportSubscriptionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeUserStackAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeUserStackAssociationsRequestRequestTypeDef",
    {
        "StackName": str,
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeUsersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeUsersRequestRequestTypeDef",
    {
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalDescribeUsersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeUsersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeUsersRequestRequestTypeDef(
    _RequiredDescribeUsersRequestRequestTypeDef, _OptionalDescribeUsersRequestRequestTypeDef
):
    pass


_RequiredUserTypeDef = TypedDict(
    "_RequiredUserTypeDef",
    {
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Enabled": bool,
        "Status": str,
        "FirstName": str,
        "LastName": str,
        "CreatedTime": datetime,
    },
    total=False,
)


class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass


DisableUserRequestRequestTypeDef = TypedDict(
    "DisableUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)

DisassociateApplicationFleetRequestRequestTypeDef = TypedDict(
    "DisassociateApplicationFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
    },
)

DisassociateApplicationFromEntitlementRequestRequestTypeDef = TypedDict(
    "DisassociateApplicationFromEntitlementRequestRequestTypeDef",
    {
        "StackName": str,
        "EntitlementName": str,
        "ApplicationIdentifier": str,
    },
)

DisassociateFleetRequestRequestTypeDef = TypedDict(
    "DisassociateFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "StackName": str,
    },
)

EnableUserRequestRequestTypeDef = TypedDict(
    "EnableUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)

EntitledApplicationTypeDef = TypedDict(
    "EntitledApplicationTypeDef",
    {
        "ApplicationIdentifier": str,
    },
)

ExpireSessionRequestRequestTypeDef = TypedDict(
    "ExpireSessionRequestRequestTypeDef",
    {
        "SessionId": str,
    },
)

FleetErrorTypeDef = TypedDict(
    "FleetErrorTypeDef",
    {
        "ErrorCode": FleetErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

ImageBuilderStateChangeReasonTypeDef = TypedDict(
    "ImageBuilderStateChangeReasonTypeDef",
    {
        "Code": ImageBuilderStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

NetworkAccessConfigurationTypeDef = TypedDict(
    "NetworkAccessConfigurationTypeDef",
    {
        "EniPrivateIpAddress": str,
        "EniId": str,
    },
    total=False,
)

ResourceErrorTypeDef = TypedDict(
    "ResourceErrorTypeDef",
    {
        "ErrorCode": FleetErrorCodeType,
        "ErrorMessage": str,
        "ErrorTimestamp": datetime,
    },
    total=False,
)

ImagePermissionsTypeDef = TypedDict(
    "ImagePermissionsTypeDef",
    {
        "allowFleet": bool,
        "allowImageBuilder": bool,
    },
    total=False,
)

ImageStateChangeReasonTypeDef = TypedDict(
    "ImageStateChangeReasonTypeDef",
    {
        "Code": ImageStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

LastReportGenerationExecutionErrorTypeDef = TypedDict(
    "LastReportGenerationExecutionErrorTypeDef",
    {
        "ErrorCode": UsageReportExecutionErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredListAssociatedFleetsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedFleetsRequestRequestTypeDef",
    {
        "StackName": str,
    },
)
_OptionalListAssociatedFleetsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedFleetsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListAssociatedFleetsRequestRequestTypeDef(
    _RequiredListAssociatedFleetsRequestRequestTypeDef,
    _OptionalListAssociatedFleetsRequestRequestTypeDef,
):
    pass


_RequiredListAssociatedStacksRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedStacksRequestRequestTypeDef",
    {
        "FleetName": str,
    },
)
_OptionalListAssociatedStacksRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedStacksRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListAssociatedStacksRequestRequestTypeDef(
    _RequiredListAssociatedStacksRequestRequestTypeDef,
    _OptionalListAssociatedStacksRequestRequestTypeDef,
):
    pass


_RequiredListEntitledApplicationsRequestRequestTypeDef = TypedDict(
    "_RequiredListEntitledApplicationsRequestRequestTypeDef",
    {
        "StackName": str,
        "EntitlementName": str,
    },
)
_OptionalListEntitledApplicationsRequestRequestTypeDef = TypedDict(
    "_OptionalListEntitledApplicationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListEntitledApplicationsRequestRequestTypeDef(
    _RequiredListEntitledApplicationsRequestRequestTypeDef,
    _OptionalListEntitledApplicationsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

StackErrorTypeDef = TypedDict(
    "StackErrorTypeDef",
    {
        "ErrorCode": StackErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

StartFleetRequestRequestTypeDef = TypedDict(
    "StartFleetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredStartImageBuilderRequestRequestTypeDef = TypedDict(
    "_RequiredStartImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalStartImageBuilderRequestRequestTypeDef = TypedDict(
    "_OptionalStartImageBuilderRequestRequestTypeDef",
    {
        "AppstreamAgentVersion": str,
    },
    total=False,
)


class StartImageBuilderRequestRequestTypeDef(
    _RequiredStartImageBuilderRequestRequestTypeDef, _OptionalStartImageBuilderRequestRequestTypeDef
):
    pass


StopFleetRequestRequestTypeDef = TypedDict(
    "StopFleetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopImageBuilderRequestRequestTypeDef = TypedDict(
    "StopImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
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

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Name": str,
        "DisplayName": str,
        "IconURL": str,
        "LaunchPath": str,
        "LaunchParameters": str,
        "Enabled": bool,
        "Metadata": Dict[str, str],
        "WorkingDirectory": str,
        "Description": str,
        "Arn": str,
        "AppBlockArn": str,
        "IconS3Location": S3LocationTypeDef,
        "Platforms": List[PlatformTypeType],
        "InstanceFamilies": List[str],
        "CreatedTime": datetime,
    },
    total=False,
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "Name": str,
        "IconS3Location": S3LocationTypeDef,
        "LaunchPath": str,
        "Platforms": Sequence[PlatformTypeType],
        "InstanceFamilies": Sequence[str],
        "AppBlockArn": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "WorkingDirectory": str,
        "LaunchParameters": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


_RequiredScriptDetailsTypeDef = TypedDict(
    "_RequiredScriptDetailsTypeDef",
    {
        "ScriptS3Location": S3LocationTypeDef,
        "ExecutablePath": str,
        "TimeoutInSeconds": int,
    },
)
_OptionalScriptDetailsTypeDef = TypedDict(
    "_OptionalScriptDetailsTypeDef",
    {
        "ExecutableParameters": str,
    },
    total=False,
)


class ScriptDetailsTypeDef(_RequiredScriptDetailsTypeDef, _OptionalScriptDetailsTypeDef):
    pass


_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "IconS3Location": S3LocationTypeDef,
        "LaunchPath": str,
        "WorkingDirectory": str,
        "LaunchParameters": str,
        "AppBlockArn": str,
        "AttributesToDelete": Sequence[ApplicationAttributeType],
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


AssociateApplicationFleetResultTypeDef = TypedDict(
    "AssociateApplicationFleetResultTypeDef",
    {
        "ApplicationFleetAssociation": ApplicationFleetAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyImageResponseTypeDef = TypedDict(
    "CopyImageResponseTypeDef",
    {
        "DestinationImageName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImageBuilderStreamingURLResultTypeDef = TypedDict(
    "CreateImageBuilderStreamingURLResultTypeDef",
    {
        "StreamingURL": str,
        "Expires": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamingURLResultTypeDef = TypedDict(
    "CreateStreamingURLResultTypeDef",
    {
        "StreamingURL": str,
        "Expires": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUsageReportSubscriptionResultTypeDef = TypedDict(
    "CreateUsageReportSubscriptionResultTypeDef",
    {
        "S3BucketName": str,
        "Schedule": Literal["DAILY"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeApplicationFleetAssociationsResultTypeDef = TypedDict(
    "DescribeApplicationFleetAssociationsResultTypeDef",
    {
        "ApplicationFleetAssociations": List[ApplicationFleetAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedFleetsResultTypeDef = TypedDict(
    "ListAssociatedFleetsResultTypeDef",
    {
        "Names": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedStacksResultTypeDef = TypedDict(
    "ListAssociatedStacksResultTypeDef",
    {
        "Names": List[str],
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

BatchAssociateUserStackRequestRequestTypeDef = TypedDict(
    "BatchAssociateUserStackRequestRequestTypeDef",
    {
        "UserStackAssociations": Sequence[UserStackAssociationTypeDef],
    },
)

BatchDisassociateUserStackRequestRequestTypeDef = TypedDict(
    "BatchDisassociateUserStackRequestRequestTypeDef",
    {
        "UserStackAssociations": Sequence[UserStackAssociationTypeDef],
    },
)

DescribeUserStackAssociationsResultTypeDef = TypedDict(
    "DescribeUserStackAssociationsResultTypeDef",
    {
        "UserStackAssociations": List[UserStackAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UserStackAssociationErrorTypeDef = TypedDict(
    "UserStackAssociationErrorTypeDef",
    {
        "UserStackAssociation": UserStackAssociationTypeDef,
        "ErrorCode": UserStackAssociationErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredCreateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDirectoryConfigRequestRequestTypeDef",
    {
        "DirectoryName": str,
        "OrganizationalUnitDistinguishedNames": Sequence[str],
    },
)
_OptionalCreateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDirectoryConfigRequestRequestTypeDef",
    {
        "ServiceAccountCredentials": ServiceAccountCredentialsTypeDef,
    },
    total=False,
)


class CreateDirectoryConfigRequestRequestTypeDef(
    _RequiredCreateDirectoryConfigRequestRequestTypeDef,
    _OptionalCreateDirectoryConfigRequestRequestTypeDef,
):
    pass


_RequiredDirectoryConfigTypeDef = TypedDict(
    "_RequiredDirectoryConfigTypeDef",
    {
        "DirectoryName": str,
    },
)
_OptionalDirectoryConfigTypeDef = TypedDict(
    "_OptionalDirectoryConfigTypeDef",
    {
        "OrganizationalUnitDistinguishedNames": List[str],
        "ServiceAccountCredentials": ServiceAccountCredentialsTypeDef,
        "CreatedTime": datetime,
    },
    total=False,
)


class DirectoryConfigTypeDef(_RequiredDirectoryConfigTypeDef, _OptionalDirectoryConfigTypeDef):
    pass


_RequiredUpdateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDirectoryConfigRequestRequestTypeDef",
    {
        "DirectoryName": str,
    },
)
_OptionalUpdateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDirectoryConfigRequestRequestTypeDef",
    {
        "OrganizationalUnitDistinguishedNames": Sequence[str],
        "ServiceAccountCredentials": ServiceAccountCredentialsTypeDef,
    },
    total=False,
)


class UpdateDirectoryConfigRequestRequestTypeDef(
    _RequiredUpdateDirectoryConfigRequestRequestTypeDef,
    _OptionalUpdateDirectoryConfigRequestRequestTypeDef,
):
    pass


_RequiredCreateEntitlementRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEntitlementRequestRequestTypeDef",
    {
        "Name": str,
        "StackName": str,
        "AppVisibility": AppVisibilityType,
        "Attributes": Sequence[EntitlementAttributeTypeDef],
    },
)
_OptionalCreateEntitlementRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEntitlementRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CreateEntitlementRequestRequestTypeDef(
    _RequiredCreateEntitlementRequestRequestTypeDef, _OptionalCreateEntitlementRequestRequestTypeDef
):
    pass


_RequiredEntitlementTypeDef = TypedDict(
    "_RequiredEntitlementTypeDef",
    {
        "Name": str,
        "StackName": str,
        "AppVisibility": AppVisibilityType,
        "Attributes": List[EntitlementAttributeTypeDef],
    },
)
_OptionalEntitlementTypeDef = TypedDict(
    "_OptionalEntitlementTypeDef",
    {
        "Description": str,
        "CreatedTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)


class EntitlementTypeDef(_RequiredEntitlementTypeDef, _OptionalEntitlementTypeDef):
    pass


_RequiredUpdateEntitlementRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEntitlementRequestRequestTypeDef",
    {
        "Name": str,
        "StackName": str,
    },
)
_OptionalUpdateEntitlementRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEntitlementRequestRequestTypeDef",
    {
        "Description": str,
        "AppVisibility": AppVisibilityType,
        "Attributes": Sequence[EntitlementAttributeTypeDef],
    },
    total=False,
)


class UpdateEntitlementRequestRequestTypeDef(
    _RequiredUpdateEntitlementRequestRequestTypeDef, _OptionalUpdateEntitlementRequestRequestTypeDef
):
    pass


_RequiredCreateFleetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFleetRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceType": str,
    },
)
_OptionalCreateFleetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFleetRequestRequestTypeDef",
    {
        "ImageName": str,
        "ImageArn": str,
        "FleetType": FleetTypeType,
        "ComputeCapacity": ComputeCapacityTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "MaxUserDurationInSeconds": int,
        "DisconnectTimeoutInSeconds": int,
        "Description": str,
        "DisplayName": str,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "Tags": Mapping[str, str],
        "IdleDisconnectTimeoutInSeconds": int,
        "IamRoleArn": str,
        "StreamView": StreamViewType,
        "Platform": PlatformTypeType,
        "MaxConcurrentSessions": int,
        "UsbDeviceFilterStrings": Sequence[str],
        "SessionScriptS3Location": S3LocationTypeDef,
    },
    total=False,
)


class CreateFleetRequestRequestTypeDef(
    _RequiredCreateFleetRequestRequestTypeDef, _OptionalCreateFleetRequestRequestTypeDef
):
    pass


_RequiredCreateImageBuilderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceType": str,
    },
)
_OptionalCreateImageBuilderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageBuilderRequestRequestTypeDef",
    {
        "ImageName": str,
        "ImageArn": str,
        "Description": str,
        "DisplayName": str,
        "VpcConfig": VpcConfigTypeDef,
        "IamRoleArn": str,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "AppstreamAgentVersion": str,
        "Tags": Mapping[str, str],
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
    },
    total=False,
)


class CreateImageBuilderRequestRequestTypeDef(
    _RequiredCreateImageBuilderRequestRequestTypeDef,
    _OptionalCreateImageBuilderRequestRequestTypeDef,
):
    pass


UpdateFleetRequestRequestTypeDef = TypedDict(
    "UpdateFleetRequestRequestTypeDef",
    {
        "ImageName": str,
        "ImageArn": str,
        "Name": str,
        "InstanceType": str,
        "ComputeCapacity": ComputeCapacityTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "MaxUserDurationInSeconds": int,
        "DisconnectTimeoutInSeconds": int,
        "DeleteVpcConfig": bool,
        "Description": str,
        "DisplayName": str,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "IdleDisconnectTimeoutInSeconds": int,
        "AttributesToDelete": Sequence[FleetAttributeType],
        "IamRoleArn": str,
        "StreamView": StreamViewType,
        "Platform": PlatformTypeType,
        "MaxConcurrentSessions": int,
        "UsbDeviceFilterStrings": Sequence[str],
        "SessionScriptS3Location": S3LocationTypeDef,
    },
    total=False,
)

_RequiredCreateStackRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStackRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateStackRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStackRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "StorageConnectors": Sequence[StorageConnectorTypeDef],
        "RedirectURL": str,
        "FeedbackURL": str,
        "UserSettings": Sequence[UserSettingTypeDef],
        "ApplicationSettings": ApplicationSettingsTypeDef,
        "Tags": Mapping[str, str],
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
        "EmbedHostDomains": Sequence[str],
    },
    total=False,
)


class CreateStackRequestRequestTypeDef(
    _RequiredCreateStackRequestRequestTypeDef, _OptionalCreateStackRequestRequestTypeDef
):
    pass


_RequiredUpdateStackRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStackRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateStackRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStackRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "StorageConnectors": Sequence[StorageConnectorTypeDef],
        "DeleteStorageConnectors": bool,
        "RedirectURL": str,
        "FeedbackURL": str,
        "AttributesToDelete": Sequence[StackAttributeType],
        "UserSettings": Sequence[UserSettingTypeDef],
        "ApplicationSettings": ApplicationSettingsTypeDef,
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
        "EmbedHostDomains": Sequence[str],
    },
    total=False,
)


class UpdateStackRequestRequestTypeDef(
    _RequiredUpdateStackRequestRequestTypeDef, _OptionalUpdateStackRequestRequestTypeDef
):
    pass


DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef = TypedDict(
    "DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef",
    {
        "DirectoryNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeFleetsRequestDescribeFleetsPaginateTypeDef = TypedDict(
    "DescribeFleetsRequestDescribeFleetsPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef = TypedDict(
    "DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeImagesRequestDescribeImagesPaginateTypeDef = TypedDict(
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    {
        "Names": Sequence[str],
        "Arns": Sequence[str],
        "Type": VisibilityTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    {
        "StackName": str,
        "FleetName": str,
    },
)
_OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    {
        "UserId": str,
        "AuthenticationType": AuthenticationTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeSessionsRequestDescribeSessionsPaginateTypeDef(
    _RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    _OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef,
):
    pass


DescribeStacksRequestDescribeStacksPaginateTypeDef = TypedDict(
    "DescribeStacksRequestDescribeStacksPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef = TypedDict(
    "DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef",
    {
        "StackName": str,
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeUsersRequestDescribeUsersPaginateTypeDef = TypedDict(
    "_RequiredDescribeUsersRequestDescribeUsersPaginateTypeDef",
    {
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalDescribeUsersRequestDescribeUsersPaginateTypeDef = TypedDict(
    "_OptionalDescribeUsersRequestDescribeUsersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeUsersRequestDescribeUsersPaginateTypeDef(
    _RequiredDescribeUsersRequestDescribeUsersPaginateTypeDef,
    _OptionalDescribeUsersRequestDescribeUsersPaginateTypeDef,
):
    pass


_RequiredListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef",
    {
        "StackName": str,
    },
)
_OptionalListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef(
    _RequiredListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef,
    _OptionalListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef,
):
    pass


_RequiredListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef",
    {
        "FleetName": str,
    },
)
_OptionalListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef(
    _RequiredListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef,
    _OptionalListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef,
):
    pass


DescribeFleetsRequestFleetStartedWaitTypeDef = TypedDict(
    "DescribeFleetsRequestFleetStartedWaitTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeFleetsRequestFleetStoppedWaitTypeDef = TypedDict(
    "DescribeFleetsRequestFleetStoppedWaitTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeUsersResultTypeDef = TypedDict(
    "DescribeUsersResultTypeDef",
    {
        "Users": List[UserTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEntitledApplicationsResultTypeDef = TypedDict(
    "ListEntitledApplicationsResultTypeDef",
    {
        "EntitledApplications": List[EntitledApplicationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFleetTypeDef = TypedDict(
    "_RequiredFleetTypeDef",
    {
        "Arn": str,
        "Name": str,
        "InstanceType": str,
        "ComputeCapacityStatus": ComputeCapacityStatusTypeDef,
        "State": FleetStateType,
    },
)
_OptionalFleetTypeDef = TypedDict(
    "_OptionalFleetTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "ImageName": str,
        "ImageArn": str,
        "FleetType": FleetTypeType,
        "MaxUserDurationInSeconds": int,
        "DisconnectTimeoutInSeconds": int,
        "VpcConfig": VpcConfigTypeDef,
        "CreatedTime": datetime,
        "FleetErrors": List[FleetErrorTypeDef],
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "IdleDisconnectTimeoutInSeconds": int,
        "IamRoleArn": str,
        "StreamView": StreamViewType,
        "Platform": PlatformTypeType,
        "MaxConcurrentSessions": int,
        "UsbDeviceFilterStrings": List[str],
        "SessionScriptS3Location": S3LocationTypeDef,
    },
    total=False,
)


class FleetTypeDef(_RequiredFleetTypeDef, _OptionalFleetTypeDef):
    pass


_RequiredSessionTypeDef = TypedDict(
    "_RequiredSessionTypeDef",
    {
        "Id": str,
        "UserId": str,
        "StackName": str,
        "FleetName": str,
        "State": SessionStateType,
    },
)
_OptionalSessionTypeDef = TypedDict(
    "_OptionalSessionTypeDef",
    {
        "ConnectionState": SessionConnectionStateType,
        "StartTime": datetime,
        "MaxExpirationTime": datetime,
        "AuthenticationType": AuthenticationTypeType,
        "NetworkAccessConfiguration": NetworkAccessConfigurationTypeDef,
    },
    total=False,
)


class SessionTypeDef(_RequiredSessionTypeDef, _OptionalSessionTypeDef):
    pass


_RequiredImageBuilderTypeDef = TypedDict(
    "_RequiredImageBuilderTypeDef",
    {
        "Name": str,
    },
)
_OptionalImageBuilderTypeDef = TypedDict(
    "_OptionalImageBuilderTypeDef",
    {
        "Arn": str,
        "ImageArn": str,
        "Description": str,
        "DisplayName": str,
        "VpcConfig": VpcConfigTypeDef,
        "InstanceType": str,
        "Platform": PlatformTypeType,
        "IamRoleArn": str,
        "State": ImageBuilderStateType,
        "StateChangeReason": ImageBuilderStateChangeReasonTypeDef,
        "CreatedTime": datetime,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "NetworkAccessConfiguration": NetworkAccessConfigurationTypeDef,
        "ImageBuilderErrors": List[ResourceErrorTypeDef],
        "AppstreamAgentVersion": str,
        "AccessEndpoints": List[AccessEndpointTypeDef],
    },
    total=False,
)


class ImageBuilderTypeDef(_RequiredImageBuilderTypeDef, _OptionalImageBuilderTypeDef):
    pass


SharedImagePermissionsTypeDef = TypedDict(
    "SharedImagePermissionsTypeDef",
    {
        "sharedAccountId": str,
        "imagePermissions": ImagePermissionsTypeDef,
    },
)

UpdateImagePermissionsRequestRequestTypeDef = TypedDict(
    "UpdateImagePermissionsRequestRequestTypeDef",
    {
        "Name": str,
        "SharedAccountId": str,
        "ImagePermissions": ImagePermissionsTypeDef,
    },
)

UsageReportSubscriptionTypeDef = TypedDict(
    "UsageReportSubscriptionTypeDef",
    {
        "S3BucketName": str,
        "Schedule": Literal["DAILY"],
        "LastGeneratedReportDate": datetime,
        "SubscriptionErrors": List[LastReportGenerationExecutionErrorTypeDef],
    },
    total=False,
)

_RequiredStackTypeDef = TypedDict(
    "_RequiredStackTypeDef",
    {
        "Name": str,
    },
)
_OptionalStackTypeDef = TypedDict(
    "_OptionalStackTypeDef",
    {
        "Arn": str,
        "Description": str,
        "DisplayName": str,
        "CreatedTime": datetime,
        "StorageConnectors": List[StorageConnectorTypeDef],
        "RedirectURL": str,
        "FeedbackURL": str,
        "StackErrors": List[StackErrorTypeDef],
        "UserSettings": List[UserSettingTypeDef],
        "ApplicationSettings": ApplicationSettingsResponseTypeDef,
        "AccessEndpoints": List[AccessEndpointTypeDef],
        "EmbedHostDomains": List[str],
    },
    total=False,
)


class StackTypeDef(_RequiredStackTypeDef, _OptionalStackTypeDef):
    pass


CreateApplicationResultTypeDef = TypedDict(
    "CreateApplicationResultTypeDef",
    {
        "Application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeApplicationsResultTypeDef = TypedDict(
    "DescribeApplicationsResultTypeDef",
    {
        "Applications": List[ApplicationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImageTypeDef = TypedDict(
    "_RequiredImageTypeDef",
    {
        "Name": str,
    },
)
_OptionalImageTypeDef = TypedDict(
    "_OptionalImageTypeDef",
    {
        "Arn": str,
        "BaseImageArn": str,
        "DisplayName": str,
        "State": ImageStateType,
        "Visibility": VisibilityTypeType,
        "ImageBuilderSupported": bool,
        "ImageBuilderName": str,
        "Platform": PlatformTypeType,
        "Description": str,
        "StateChangeReason": ImageStateChangeReasonTypeDef,
        "Applications": List[ApplicationTypeDef],
        "CreatedTime": datetime,
        "PublicBaseImageReleasedDate": datetime,
        "AppstreamAgentVersion": str,
        "ImagePermissions": ImagePermissionsTypeDef,
        "ImageErrors": List[ResourceErrorTypeDef],
    },
    total=False,
)


class ImageTypeDef(_RequiredImageTypeDef, _OptionalImageTypeDef):
    pass


UpdateApplicationResultTypeDef = TypedDict(
    "UpdateApplicationResultTypeDef",
    {
        "Application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAppBlockTypeDef = TypedDict(
    "_RequiredAppBlockTypeDef",
    {
        "Name": str,
        "Arn": str,
        "SetupScriptDetails": ScriptDetailsTypeDef,
    },
)
_OptionalAppBlockTypeDef = TypedDict(
    "_OptionalAppBlockTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "SourceS3Location": S3LocationTypeDef,
        "CreatedTime": datetime,
    },
    total=False,
)


class AppBlockTypeDef(_RequiredAppBlockTypeDef, _OptionalAppBlockTypeDef):
    pass


_RequiredCreateAppBlockRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppBlockRequestRequestTypeDef",
    {
        "Name": str,
        "SourceS3Location": S3LocationTypeDef,
        "SetupScriptDetails": ScriptDetailsTypeDef,
    },
)
_OptionalCreateAppBlockRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppBlockRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateAppBlockRequestRequestTypeDef(
    _RequiredCreateAppBlockRequestRequestTypeDef, _OptionalCreateAppBlockRequestRequestTypeDef
):
    pass


BatchAssociateUserStackResultTypeDef = TypedDict(
    "BatchAssociateUserStackResultTypeDef",
    {
        "errors": List[UserStackAssociationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateUserStackResultTypeDef = TypedDict(
    "BatchDisassociateUserStackResultTypeDef",
    {
        "errors": List[UserStackAssociationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDirectoryConfigResultTypeDef = TypedDict(
    "CreateDirectoryConfigResultTypeDef",
    {
        "DirectoryConfig": DirectoryConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDirectoryConfigsResultTypeDef = TypedDict(
    "DescribeDirectoryConfigsResultTypeDef",
    {
        "DirectoryConfigs": List[DirectoryConfigTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDirectoryConfigResultTypeDef = TypedDict(
    "UpdateDirectoryConfigResultTypeDef",
    {
        "DirectoryConfig": DirectoryConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEntitlementResultTypeDef = TypedDict(
    "CreateEntitlementResultTypeDef",
    {
        "Entitlement": EntitlementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEntitlementsResultTypeDef = TypedDict(
    "DescribeEntitlementsResultTypeDef",
    {
        "Entitlements": List[EntitlementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEntitlementResultTypeDef = TypedDict(
    "UpdateEntitlementResultTypeDef",
    {
        "Entitlement": EntitlementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFleetResultTypeDef = TypedDict(
    "CreateFleetResultTypeDef",
    {
        "Fleet": FleetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetsResultTypeDef = TypedDict(
    "DescribeFleetsResultTypeDef",
    {
        "Fleets": List[FleetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFleetResultTypeDef = TypedDict(
    "UpdateFleetResultTypeDef",
    {
        "Fleet": FleetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSessionsResultTypeDef = TypedDict(
    "DescribeSessionsResultTypeDef",
    {
        "Sessions": List[SessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImageBuilderResultTypeDef = TypedDict(
    "CreateImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImageBuilderResultTypeDef = TypedDict(
    "DeleteImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImageBuildersResultTypeDef = TypedDict(
    "DescribeImageBuildersResultTypeDef",
    {
        "ImageBuilders": List[ImageBuilderTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartImageBuilderResultTypeDef = TypedDict(
    "StartImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopImageBuilderResultTypeDef = TypedDict(
    "StopImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImagePermissionsResultTypeDef = TypedDict(
    "DescribeImagePermissionsResultTypeDef",
    {
        "Name": str,
        "SharedImagePermissionsList": List[SharedImagePermissionsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUsageReportSubscriptionsResultTypeDef = TypedDict(
    "DescribeUsageReportSubscriptionsResultTypeDef",
    {
        "UsageReportSubscriptions": List[UsageReportSubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStackResultTypeDef = TypedDict(
    "CreateStackResultTypeDef",
    {
        "Stack": StackTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStacksResultTypeDef = TypedDict(
    "DescribeStacksResultTypeDef",
    {
        "Stacks": List[StackTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStackResultTypeDef = TypedDict(
    "UpdateStackResultTypeDef",
    {
        "Stack": StackTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUpdatedImageResultTypeDef = TypedDict(
    "CreateUpdatedImageResultTypeDef",
    {
        "image": ImageTypeDef,
        "canUpdateImage": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImageResultTypeDef = TypedDict(
    "DeleteImageResultTypeDef",
    {
        "Image": ImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImagesResultTypeDef = TypedDict(
    "DescribeImagesResultTypeDef",
    {
        "Images": List[ImageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppBlockResultTypeDef = TypedDict(
    "CreateAppBlockResultTypeDef",
    {
        "AppBlock": AppBlockTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppBlocksResultTypeDef = TypedDict(
    "DescribeAppBlocksResultTypeDef",
    {
        "AppBlocks": List[AppBlockTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
