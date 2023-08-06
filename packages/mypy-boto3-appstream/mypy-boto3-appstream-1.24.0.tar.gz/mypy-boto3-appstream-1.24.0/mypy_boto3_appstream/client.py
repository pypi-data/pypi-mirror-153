"""
Type annotations for appstream service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appstream.client import AppStreamClient

    session = Session()
    client: AppStreamClient = session.client("appstream")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ApplicationAttributeType,
    AppVisibilityType,
    AuthenticationTypeType,
    FleetAttributeType,
    FleetTypeType,
    MessageActionType,
    PlatformTypeType,
    StackAttributeType,
    StreamViewType,
    VisibilityTypeType,
)
from .paginator import (
    DescribeDirectoryConfigsPaginator,
    DescribeFleetsPaginator,
    DescribeImageBuildersPaginator,
    DescribeImagesPaginator,
    DescribeSessionsPaginator,
    DescribeStacksPaginator,
    DescribeUsersPaginator,
    DescribeUserStackAssociationsPaginator,
    ListAssociatedFleetsPaginator,
    ListAssociatedStacksPaginator,
)
from .type_defs import (
    AccessEndpointTypeDef,
    ApplicationSettingsTypeDef,
    AssociateApplicationFleetResultTypeDef,
    BatchAssociateUserStackResultTypeDef,
    BatchDisassociateUserStackResultTypeDef,
    ComputeCapacityTypeDef,
    CopyImageResponseTypeDef,
    CreateAppBlockResultTypeDef,
    CreateApplicationResultTypeDef,
    CreateDirectoryConfigResultTypeDef,
    CreateEntitlementResultTypeDef,
    CreateFleetResultTypeDef,
    CreateImageBuilderResultTypeDef,
    CreateImageBuilderStreamingURLResultTypeDef,
    CreateStackResultTypeDef,
    CreateStreamingURLResultTypeDef,
    CreateUpdatedImageResultTypeDef,
    CreateUsageReportSubscriptionResultTypeDef,
    DeleteImageBuilderResultTypeDef,
    DeleteImageResultTypeDef,
    DescribeAppBlocksResultTypeDef,
    DescribeApplicationFleetAssociationsResultTypeDef,
    DescribeApplicationsResultTypeDef,
    DescribeDirectoryConfigsResultTypeDef,
    DescribeEntitlementsResultTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagePermissionsResultTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksResultTypeDef,
    DescribeUsageReportSubscriptionsResultTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    DomainJoinInfoTypeDef,
    EntitlementAttributeTypeDef,
    ImagePermissionsTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksResultTypeDef,
    ListEntitledApplicationsResultTypeDef,
    ListTagsForResourceResponseTypeDef,
    S3LocationTypeDef,
    ScriptDetailsTypeDef,
    ServiceAccountCredentialsTypeDef,
    StartImageBuilderResultTypeDef,
    StopImageBuilderResultTypeDef,
    StorageConnectorTypeDef,
    UpdateApplicationResultTypeDef,
    UpdateDirectoryConfigResultTypeDef,
    UpdateEntitlementResultTypeDef,
    UpdateFleetResultTypeDef,
    UpdateStackResultTypeDef,
    UserSettingTypeDef,
    UserStackAssociationTypeDef,
    VpcConfigTypeDef,
)
from .waiter import FleetStartedWaiter, FleetStoppedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppStreamClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    EntitlementAlreadyExistsException: Type[BotocoreClientError]
    EntitlementNotFoundException: Type[BotocoreClientError]
    IncompatibleImageException: Type[BotocoreClientError]
    InvalidAccountStatusException: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidRoleException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    RequestLimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotAvailableException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class AppStreamClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppStreamClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#exceptions)
        """

    def associate_application_fleet(
        self, *, FleetName: str, ApplicationArn: str
    ) -> AssociateApplicationFleetResultTypeDef:
        """
        Associates the specified application with the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_application_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#associate_application_fleet)
        """

    def associate_application_to_entitlement(
        self, *, StackName: str, EntitlementName: str, ApplicationIdentifier: str
    ) -> Dict[str, Any]:
        """
        Associates an application to entitle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_application_to_entitlement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#associate_application_to_entitlement)
        """

    def associate_fleet(self, *, FleetName: str, StackName: str) -> Dict[str, Any]:
        """
        Associates the specified fleet with the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#associate_fleet)
        """

    def batch_associate_user_stack(
        self, *, UserStackAssociations: Sequence[UserStackAssociationTypeDef]
    ) -> BatchAssociateUserStackResultTypeDef:
        """
        Associates the specified users with the specified stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.batch_associate_user_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#batch_associate_user_stack)
        """

    def batch_disassociate_user_stack(
        self, *, UserStackAssociations: Sequence[UserStackAssociationTypeDef]
    ) -> BatchDisassociateUserStackResultTypeDef:
        """
        Disassociates the specified users from the specified stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.batch_disassociate_user_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#batch_disassociate_user_stack)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#can_paginate)
        """

    def copy_image(
        self,
        *,
        SourceImageName: str,
        DestinationImageName: str,
        DestinationRegion: str,
        DestinationImageDescription: str = ...
    ) -> CopyImageResponseTypeDef:
        """
        Copies the image within the same region or to a new region within the same AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.copy_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#copy_image)
        """

    def create_app_block(
        self,
        *,
        Name: str,
        SourceS3Location: S3LocationTypeDef,
        SetupScriptDetails: ScriptDetailsTypeDef,
        Description: str = ...,
        DisplayName: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateAppBlockResultTypeDef:
        """
        Creates an app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_app_block)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_app_block)
        """

    def create_application(
        self,
        *,
        Name: str,
        IconS3Location: S3LocationTypeDef,
        LaunchPath: str,
        Platforms: Sequence[PlatformTypeType],
        InstanceFamilies: Sequence[str],
        AppBlockArn: str,
        DisplayName: str = ...,
        Description: str = ...,
        WorkingDirectory: str = ...,
        LaunchParameters: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateApplicationResultTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_application)
        """

    def create_directory_config(
        self,
        *,
        DirectoryName: str,
        OrganizationalUnitDistinguishedNames: Sequence[str],
        ServiceAccountCredentials: ServiceAccountCredentialsTypeDef = ...
    ) -> CreateDirectoryConfigResultTypeDef:
        """
        Creates a Directory Config object in AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_directory_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_directory_config)
        """

    def create_entitlement(
        self,
        *,
        Name: str,
        StackName: str,
        AppVisibility: AppVisibilityType,
        Attributes: Sequence[EntitlementAttributeTypeDef],
        Description: str = ...
    ) -> CreateEntitlementResultTypeDef:
        """
        Creates a new entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_entitlement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_entitlement)
        """

    def create_fleet(
        self,
        *,
        Name: str,
        InstanceType: str,
        ImageName: str = ...,
        ImageArn: str = ...,
        FleetType: FleetTypeType = ...,
        ComputeCapacity: ComputeCapacityTypeDef = ...,
        VpcConfig: VpcConfigTypeDef = ...,
        MaxUserDurationInSeconds: int = ...,
        DisconnectTimeoutInSeconds: int = ...,
        Description: str = ...,
        DisplayName: str = ...,
        EnableDefaultInternetAccess: bool = ...,
        DomainJoinInfo: DomainJoinInfoTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        IdleDisconnectTimeoutInSeconds: int = ...,
        IamRoleArn: str = ...,
        StreamView: StreamViewType = ...,
        Platform: PlatformTypeType = ...,
        MaxConcurrentSessions: int = ...,
        UsbDeviceFilterStrings: Sequence[str] = ...,
        SessionScriptS3Location: S3LocationTypeDef = ...
    ) -> CreateFleetResultTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_fleet)
        """

    def create_image_builder(
        self,
        *,
        Name: str,
        InstanceType: str,
        ImageName: str = ...,
        ImageArn: str = ...,
        Description: str = ...,
        DisplayName: str = ...,
        VpcConfig: VpcConfigTypeDef = ...,
        IamRoleArn: str = ...,
        EnableDefaultInternetAccess: bool = ...,
        DomainJoinInfo: DomainJoinInfoTypeDef = ...,
        AppstreamAgentVersion: str = ...,
        Tags: Mapping[str, str] = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...
    ) -> CreateImageBuilderResultTypeDef:
        """
        Creates an image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_image_builder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_image_builder)
        """

    def create_image_builder_streaming_url(
        self, *, Name: str, Validity: int = ...
    ) -> CreateImageBuilderStreamingURLResultTypeDef:
        """
        Creates a URL to start an image builder streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_image_builder_streaming_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_image_builder_streaming_url)
        """

    def create_stack(
        self,
        *,
        Name: str,
        Description: str = ...,
        DisplayName: str = ...,
        StorageConnectors: Sequence[StorageConnectorTypeDef] = ...,
        RedirectURL: str = ...,
        FeedbackURL: str = ...,
        UserSettings: Sequence[UserSettingTypeDef] = ...,
        ApplicationSettings: ApplicationSettingsTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
        EmbedHostDomains: Sequence[str] = ...
    ) -> CreateStackResultTypeDef:
        """
        Creates a stack to start streaming applications to users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_stack)
        """

    def create_streaming_url(
        self,
        *,
        StackName: str,
        FleetName: str,
        UserId: str,
        ApplicationId: str = ...,
        Validity: int = ...,
        SessionContext: str = ...
    ) -> CreateStreamingURLResultTypeDef:
        """
        Creates a temporary URL to start an AppStream 2.0 streaming session for the
        specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_streaming_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_streaming_url)
        """

    def create_updated_image(
        self,
        *,
        existingImageName: str,
        newImageName: str,
        newImageDescription: str = ...,
        newImageDisplayName: str = ...,
        newImageTags: Mapping[str, str] = ...,
        dryRun: bool = ...
    ) -> CreateUpdatedImageResultTypeDef:
        """
        Creates a new image with the latest Windows operating system updates, driver
        updates, and AppStream 2.0 agent software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_updated_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_updated_image)
        """

    def create_usage_report_subscription(self) -> CreateUsageReportSubscriptionResultTypeDef:
        """
        Creates a usage report subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_usage_report_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_usage_report_subscription)
        """

    def create_user(
        self,
        *,
        UserName: str,
        AuthenticationType: AuthenticationTypeType,
        MessageAction: MessageActionType = ...,
        FirstName: str = ...,
        LastName: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#create_user)
        """

    def delete_app_block(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_app_block)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_app_block)
        """

    def delete_application(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_application)
        """

    def delete_directory_config(self, *, DirectoryName: str) -> Dict[str, Any]:
        """
        Deletes the specified Directory Config object from AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_directory_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_directory_config)
        """

    def delete_entitlement(self, *, Name: str, StackName: str) -> Dict[str, Any]:
        """
        Deletes the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_entitlement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_entitlement)
        """

    def delete_fleet(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_fleet)
        """

    def delete_image(self, *, Name: str) -> DeleteImageResultTypeDef:
        """
        Deletes the specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_image)
        """

    def delete_image_builder(self, *, Name: str) -> DeleteImageBuilderResultTypeDef:
        """
        Deletes the specified image builder and releases the capacity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_image_builder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_image_builder)
        """

    def delete_image_permissions(self, *, Name: str, SharedAccountId: str) -> Dict[str, Any]:
        """
        Deletes permissions for the specified private image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_image_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_image_permissions)
        """

    def delete_stack(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_stack)
        """

    def delete_usage_report_subscription(self) -> Dict[str, Any]:
        """
        Disables usage report generation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_usage_report_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_usage_report_subscription)
        """

    def delete_user(
        self, *, UserName: str, AuthenticationType: AuthenticationTypeType
    ) -> Dict[str, Any]:
        """
        Deletes a user from the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#delete_user)
        """

    def describe_app_blocks(
        self, *, Arns: Sequence[str] = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeAppBlocksResultTypeDef:
        """
        Retrieves a list that describes one or more app blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_app_blocks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_app_blocks)
        """

    def describe_application_fleet_associations(
        self,
        *,
        FleetName: str = ...,
        ApplicationArn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeApplicationFleetAssociationsResultTypeDef:
        """
        Retrieves a list that describes one or more application fleet associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_application_fleet_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_application_fleet_associations)
        """

    def describe_applications(
        self, *, Arns: Sequence[str] = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeApplicationsResultTypeDef:
        """
        Retrieves a list that describes one or more applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_applications)
        """

    def describe_directory_configs(
        self, *, DirectoryNames: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeDirectoryConfigsResultTypeDef:
        """
        Retrieves a list that describes one or more specified Directory Config objects
        for AppStream 2.0, if the names for these objects are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_directory_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_directory_configs)
        """

    def describe_entitlements(
        self, *, StackName: str, Name: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeEntitlementsResultTypeDef:
        """
        Retrieves a list that describes one of more entitlements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_entitlements)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_entitlements)
        """

    def describe_fleets(
        self, *, Names: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeFleetsResultTypeDef:
        """
        Retrieves a list that describes one or more specified fleets, if the fleet names
        are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_fleets)
        """

    def describe_image_builders(
        self, *, Names: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeImageBuildersResultTypeDef:
        """
        Retrieves a list that describes one or more specified image builders, if the
        image builder names are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_image_builders)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_image_builders)
        """

    def describe_image_permissions(
        self,
        *,
        Name: str,
        MaxResults: int = ...,
        SharedAwsAccountIds: Sequence[str] = ...,
        NextToken: str = ...
    ) -> DescribeImagePermissionsResultTypeDef:
        """
        Retrieves a list that describes the permissions for shared AWS account IDs on a
        private image that you own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_image_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_image_permissions)
        """

    def describe_images(
        self,
        *,
        Names: Sequence[str] = ...,
        Arns: Sequence[str] = ...,
        Type: VisibilityTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> DescribeImagesResultTypeDef:
        """
        Retrieves a list that describes one or more specified images, if the image names
        or image ARNs are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_images)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_images)
        """

    def describe_sessions(
        self,
        *,
        StackName: str,
        FleetName: str,
        UserId: str = ...,
        NextToken: str = ...,
        Limit: int = ...,
        AuthenticationType: AuthenticationTypeType = ...
    ) -> DescribeSessionsResultTypeDef:
        """
        Retrieves a list that describes the streaming sessions for a specified stack and
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_sessions)
        """

    def describe_stacks(
        self, *, Names: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeStacksResultTypeDef:
        """
        Retrieves a list that describes one or more specified stacks, if the stack names
        are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_stacks)
        """

    def describe_usage_report_subscriptions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeUsageReportSubscriptionsResultTypeDef:
        """
        Retrieves a list that describes one or more usage report subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_usage_report_subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_usage_report_subscriptions)
        """

    def describe_user_stack_associations(
        self,
        *,
        StackName: str = ...,
        UserName: str = ...,
        AuthenticationType: AuthenticationTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeUserStackAssociationsResultTypeDef:
        """
        Retrieves a list that describes the UserStackAssociation objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_user_stack_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_user_stack_associations)
        """

    def describe_users(
        self,
        *,
        AuthenticationType: AuthenticationTypeType,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeUsersResultTypeDef:
        """
        Retrieves a list that describes one or more specified users in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#describe_users)
        """

    def disable_user(
        self, *, UserName: str, AuthenticationType: AuthenticationTypeType
    ) -> Dict[str, Any]:
        """
        Disables the specified user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disable_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#disable_user)
        """

    def disassociate_application_fleet(
        self, *, FleetName: str, ApplicationArn: str
    ) -> Dict[str, Any]:
        """
        Disassociates the specified application from the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_application_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#disassociate_application_fleet)
        """

    def disassociate_application_from_entitlement(
        self, *, StackName: str, EntitlementName: str, ApplicationIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified application from the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_application_from_entitlement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#disassociate_application_from_entitlement)
        """

    def disassociate_fleet(self, *, FleetName: str, StackName: str) -> Dict[str, Any]:
        """
        Disassociates the specified fleet from the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#disassociate_fleet)
        """

    def enable_user(
        self, *, UserName: str, AuthenticationType: AuthenticationTypeType
    ) -> Dict[str, Any]:
        """
        Enables a user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.enable_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#enable_user)
        """

    def expire_session(self, *, SessionId: str) -> Dict[str, Any]:
        """
        Immediately stops the specified streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.expire_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#expire_session)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#generate_presigned_url)
        """

    def list_associated_fleets(
        self, *, StackName: str, NextToken: str = ...
    ) -> ListAssociatedFleetsResultTypeDef:
        """
        Retrieves the name of the fleet that is associated with the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_associated_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#list_associated_fleets)
        """

    def list_associated_stacks(
        self, *, FleetName: str, NextToken: str = ...
    ) -> ListAssociatedStacksResultTypeDef:
        """
        Retrieves the name of the stack with which the specified fleet is associated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_associated_stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#list_associated_stacks)
        """

    def list_entitled_applications(
        self, *, StackName: str, EntitlementName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEntitledApplicationsResultTypeDef:
        """
        Retrieves a list of entitled applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_entitled_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#list_entitled_applications)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of all tags for the specified AppStream 2.0 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#list_tags_for_resource)
        """

    def start_fleet(self, *, Name: str) -> Dict[str, Any]:
        """
        Starts the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.start_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#start_fleet)
        """

    def start_image_builder(
        self, *, Name: str, AppstreamAgentVersion: str = ...
    ) -> StartImageBuilderResultTypeDef:
        """
        Starts the specified image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.start_image_builder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#start_image_builder)
        """

    def stop_fleet(self, *, Name: str) -> Dict[str, Any]:
        """
        Stops the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.stop_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#stop_fleet)
        """

    def stop_image_builder(self, *, Name: str) -> StopImageBuilderResultTypeDef:
        """
        Stops the specified image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.stop_image_builder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#stop_image_builder)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified AppStream 2.0 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Disassociates one or more specified tags from the specified AppStream 2.0
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#untag_resource)
        """

    def update_application(
        self,
        *,
        Name: str,
        DisplayName: str = ...,
        Description: str = ...,
        IconS3Location: S3LocationTypeDef = ...,
        LaunchPath: str = ...,
        WorkingDirectory: str = ...,
        LaunchParameters: str = ...,
        AppBlockArn: str = ...,
        AttributesToDelete: Sequence[ApplicationAttributeType] = ...
    ) -> UpdateApplicationResultTypeDef:
        """
        Updates the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#update_application)
        """

    def update_directory_config(
        self,
        *,
        DirectoryName: str,
        OrganizationalUnitDistinguishedNames: Sequence[str] = ...,
        ServiceAccountCredentials: ServiceAccountCredentialsTypeDef = ...
    ) -> UpdateDirectoryConfigResultTypeDef:
        """
        Updates the specified Directory Config object in AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_directory_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#update_directory_config)
        """

    def update_entitlement(
        self,
        *,
        Name: str,
        StackName: str,
        Description: str = ...,
        AppVisibility: AppVisibilityType = ...,
        Attributes: Sequence[EntitlementAttributeTypeDef] = ...
    ) -> UpdateEntitlementResultTypeDef:
        """
        Updates the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_entitlement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#update_entitlement)
        """

    def update_fleet(
        self,
        *,
        ImageName: str = ...,
        ImageArn: str = ...,
        Name: str = ...,
        InstanceType: str = ...,
        ComputeCapacity: ComputeCapacityTypeDef = ...,
        VpcConfig: VpcConfigTypeDef = ...,
        MaxUserDurationInSeconds: int = ...,
        DisconnectTimeoutInSeconds: int = ...,
        DeleteVpcConfig: bool = ...,
        Description: str = ...,
        DisplayName: str = ...,
        EnableDefaultInternetAccess: bool = ...,
        DomainJoinInfo: DomainJoinInfoTypeDef = ...,
        IdleDisconnectTimeoutInSeconds: int = ...,
        AttributesToDelete: Sequence[FleetAttributeType] = ...,
        IamRoleArn: str = ...,
        StreamView: StreamViewType = ...,
        Platform: PlatformTypeType = ...,
        MaxConcurrentSessions: int = ...,
        UsbDeviceFilterStrings: Sequence[str] = ...,
        SessionScriptS3Location: S3LocationTypeDef = ...
    ) -> UpdateFleetResultTypeDef:
        """
        Updates the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#update_fleet)
        """

    def update_image_permissions(
        self, *, Name: str, SharedAccountId: str, ImagePermissions: ImagePermissionsTypeDef
    ) -> Dict[str, Any]:
        """
        Adds or updates permissions for the specified private image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_image_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#update_image_permissions)
        """

    def update_stack(
        self,
        *,
        Name: str,
        DisplayName: str = ...,
        Description: str = ...,
        StorageConnectors: Sequence[StorageConnectorTypeDef] = ...,
        DeleteStorageConnectors: bool = ...,
        RedirectURL: str = ...,
        FeedbackURL: str = ...,
        AttributesToDelete: Sequence[StackAttributeType] = ...,
        UserSettings: Sequence[UserSettingTypeDef] = ...,
        ApplicationSettings: ApplicationSettingsTypeDef = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
        EmbedHostDomains: Sequence[str] = ...
    ) -> UpdateStackResultTypeDef:
        """
        Updates the specified fields for the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#update_stack)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_directory_configs"]
    ) -> DescribeDirectoryConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_fleets"]) -> DescribeFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_image_builders"]
    ) -> DescribeImageBuildersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_images"]) -> DescribeImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_sessions"]
    ) -> DescribeSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_stacks"]) -> DescribeStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_user_stack_associations"]
    ) -> DescribeUserStackAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_users"]) -> DescribeUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_fleets"]
    ) -> ListAssociatedFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_stacks"]
    ) -> ListAssociatedStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_started"]) -> FleetStartedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_stopped"]) -> FleetStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/client/#get_waiter)
        """
