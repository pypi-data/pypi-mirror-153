"""
Type annotations for quicksight service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_quicksight.client import QuickSightClient

    session = Session()
    client: QuickSightClient = session.client("quicksight")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AssignmentStatusType,
    DataSetImportModeType,
    DataSourceTypeType,
    EmbeddingIdentityTypeType,
    IdentityTypeType,
    IngestionTypeType,
    MemberTypeType,
    ThemeTypeType,
    UserRoleType,
)
from .paginator import (
    ListAnalysesPaginator,
    ListDashboardsPaginator,
    ListDashboardVersionsPaginator,
    ListDataSetsPaginator,
    ListDataSourcesPaginator,
    ListIngestionsPaginator,
    ListNamespacesPaginator,
    ListTemplateAliasesPaginator,
    ListTemplatesPaginator,
    ListTemplateVersionsPaginator,
    ListThemesPaginator,
    ListThemeVersionsPaginator,
    SearchAnalysesPaginator,
    SearchDashboardsPaginator,
)
from .type_defs import (
    AccountCustomizationTypeDef,
    AnalysisSearchFilterTypeDef,
    AnalysisSourceEntityTypeDef,
    AnonymousUserEmbeddingExperienceConfigurationTypeDef,
    CancelIngestionResponseTypeDef,
    ColumnGroupTypeDef,
    ColumnLevelPermissionRuleTypeDef,
    CreateAccountCustomizationResponseTypeDef,
    CreateAnalysisResponseTypeDef,
    CreateDashboardResponseTypeDef,
    CreateDataSetResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateFolderMembershipResponseTypeDef,
    CreateFolderResponseTypeDef,
    CreateGroupMembershipResponseTypeDef,
    CreateGroupResponseTypeDef,
    CreateIAMPolicyAssignmentResponseTypeDef,
    CreateIngestionResponseTypeDef,
    CreateNamespaceResponseTypeDef,
    CreateTemplateAliasResponseTypeDef,
    CreateTemplateResponseTypeDef,
    CreateThemeAliasResponseTypeDef,
    CreateThemeResponseTypeDef,
    DashboardPublishOptionsTypeDef,
    DashboardSearchFilterTypeDef,
    DashboardSourceEntityTypeDef,
    DataSetUsageConfigurationTypeDef,
    DataSourceCredentialsTypeDef,
    DataSourceParametersTypeDef,
    DeleteAccountCustomizationResponseTypeDef,
    DeleteAnalysisResponseTypeDef,
    DeleteDashboardResponseTypeDef,
    DeleteDataSetResponseTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteFolderMembershipResponseTypeDef,
    DeleteFolderResponseTypeDef,
    DeleteGroupMembershipResponseTypeDef,
    DeleteGroupResponseTypeDef,
    DeleteIAMPolicyAssignmentResponseTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteTemplateAliasResponseTypeDef,
    DeleteTemplateResponseTypeDef,
    DeleteThemeAliasResponseTypeDef,
    DeleteThemeResponseTypeDef,
    DeleteUserByPrincipalIdResponseTypeDef,
    DeleteUserResponseTypeDef,
    DescribeAccountCustomizationResponseTypeDef,
    DescribeAccountSettingsResponseTypeDef,
    DescribeAnalysisPermissionsResponseTypeDef,
    DescribeAnalysisResponseTypeDef,
    DescribeDashboardPermissionsResponseTypeDef,
    DescribeDashboardResponseTypeDef,
    DescribeDataSetPermissionsResponseTypeDef,
    DescribeDataSetResponseTypeDef,
    DescribeDataSourcePermissionsResponseTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeFolderPermissionsResponseTypeDef,
    DescribeFolderResolvedPermissionsResponseTypeDef,
    DescribeFolderResponseTypeDef,
    DescribeGroupMembershipResponseTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeIAMPolicyAssignmentResponseTypeDef,
    DescribeIngestionResponseTypeDef,
    DescribeIpRestrictionResponseTypeDef,
    DescribeNamespaceResponseTypeDef,
    DescribeTemplateAliasResponseTypeDef,
    DescribeTemplatePermissionsResponseTypeDef,
    DescribeTemplateResponseTypeDef,
    DescribeThemeAliasResponseTypeDef,
    DescribeThemePermissionsResponseTypeDef,
    DescribeThemeResponseTypeDef,
    DescribeUserResponseTypeDef,
    FieldFolderTypeDef,
    FolderSearchFilterTypeDef,
    GenerateEmbedUrlForAnonymousUserResponseTypeDef,
    GenerateEmbedUrlForRegisteredUserResponseTypeDef,
    GetDashboardEmbedUrlResponseTypeDef,
    GetSessionEmbedUrlResponseTypeDef,
    GroupSearchFilterTypeDef,
    ListAnalysesResponseTypeDef,
    ListDashboardsResponseTypeDef,
    ListDashboardVersionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListFolderMembersResponseTypeDef,
    ListFoldersResponseTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListIAMPolicyAssignmentsForUserResponseTypeDef,
    ListIAMPolicyAssignmentsResponseTypeDef,
    ListIngestionsResponseTypeDef,
    ListNamespacesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplateAliasesResponseTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsResponseTypeDef,
    ListThemeAliasesResponseTypeDef,
    ListThemesResponseTypeDef,
    ListThemeVersionsResponseTypeDef,
    ListUserGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
    LogicalTableTypeDef,
    ParametersTypeDef,
    PhysicalTableTypeDef,
    RegisteredUserEmbeddingExperienceConfigurationTypeDef,
    RegisterUserResponseTypeDef,
    ResourcePermissionTypeDef,
    RestoreAnalysisResponseTypeDef,
    RowLevelPermissionDataSetTypeDef,
    RowLevelPermissionTagConfigurationTypeDef,
    SearchAnalysesResponseTypeDef,
    SearchDashboardsResponseTypeDef,
    SearchFoldersResponseTypeDef,
    SearchGroupsResponseTypeDef,
    SessionTagTypeDef,
    SslPropertiesTypeDef,
    TagResourceResponseTypeDef,
    TagTypeDef,
    TemplateSourceEntityTypeDef,
    ThemeConfigurationTypeDef,
    UntagResourceResponseTypeDef,
    UpdateAccountCustomizationResponseTypeDef,
    UpdateAccountSettingsResponseTypeDef,
    UpdateAnalysisPermissionsResponseTypeDef,
    UpdateAnalysisResponseTypeDef,
    UpdateDashboardPermissionsResponseTypeDef,
    UpdateDashboardPublishedVersionResponseTypeDef,
    UpdateDashboardResponseTypeDef,
    UpdateDataSetPermissionsResponseTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateDataSourcePermissionsResponseTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateFolderPermissionsResponseTypeDef,
    UpdateFolderResponseTypeDef,
    UpdateGroupResponseTypeDef,
    UpdateIAMPolicyAssignmentResponseTypeDef,
    UpdateIpRestrictionResponseTypeDef,
    UpdatePublicSharingSettingsResponseTypeDef,
    UpdateTemplateAliasResponseTypeDef,
    UpdateTemplatePermissionsResponseTypeDef,
    UpdateTemplateResponseTypeDef,
    UpdateThemeAliasResponseTypeDef,
    UpdateThemePermissionsResponseTypeDef,
    UpdateThemeResponseTypeDef,
    UpdateUserResponseTypeDef,
    VpcConnectionPropertiesTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("QuickSightClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentUpdatingException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DomainNotWhitelistedException: Type[BotocoreClientError]
    IdentityTypeNotSupportedException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PreconditionNotMetException: Type[BotocoreClientError]
    QuickSightUserNotFoundException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    SessionLifetimeInMinutesInvalidException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedPricingPlanException: Type[BotocoreClientError]
    UnsupportedUserEditionException: Type[BotocoreClientError]


class QuickSightClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QuickSightClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#can_paginate)
        """

    def cancel_ingestion(
        self, *, AwsAccountId: str, DataSetId: str, IngestionId: str
    ) -> CancelIngestionResponseTypeDef:
        """
        Cancels an ongoing ingestion of data into SPICE.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.cancel_ingestion)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#cancel_ingestion)
        """

    def create_account_customization(
        self,
        *,
        AwsAccountId: str,
        AccountCustomization: AccountCustomizationTypeDef,
        Namespace: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateAccountCustomizationResponseTypeDef:
        """
        Creates Amazon QuickSight customizations the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_account_customization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_account_customization)
        """

    def create_analysis(
        self,
        *,
        AwsAccountId: str,
        AnalysisId: str,
        Name: str,
        SourceEntity: AnalysisSourceEntityTypeDef,
        Parameters: ParametersTypeDef = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        ThemeArn: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateAnalysisResponseTypeDef:
        """
        Creates an analysis in Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_analysis)
        """

    def create_dashboard(
        self,
        *,
        AwsAccountId: str,
        DashboardId: str,
        Name: str,
        SourceEntity: DashboardSourceEntityTypeDef,
        Parameters: ParametersTypeDef = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        VersionDescription: str = ...,
        DashboardPublishOptions: DashboardPublishOptionsTypeDef = ...,
        ThemeArn: str = ...
    ) -> CreateDashboardResponseTypeDef:
        """
        Creates a dashboard from a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_dashboard)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_dashboard)
        """

    def create_data_set(
        self,
        *,
        AwsAccountId: str,
        DataSetId: str,
        Name: str,
        PhysicalTableMap: Mapping[str, PhysicalTableTypeDef],
        ImportMode: DataSetImportModeType,
        LogicalTableMap: Mapping[str, LogicalTableTypeDef] = ...,
        ColumnGroups: Sequence[ColumnGroupTypeDef] = ...,
        FieldFolders: Mapping[str, FieldFolderTypeDef] = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        RowLevelPermissionDataSet: RowLevelPermissionDataSetTypeDef = ...,
        RowLevelPermissionTagConfiguration: RowLevelPermissionTagConfigurationTypeDef = ...,
        ColumnLevelPermissionRules: Sequence[ColumnLevelPermissionRuleTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        DataSetUsageConfiguration: DataSetUsageConfigurationTypeDef = ...
    ) -> CreateDataSetResponseTypeDef:
        """
        Creates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_data_set)
        """

    def create_data_source(
        self,
        *,
        AwsAccountId: str,
        DataSourceId: str,
        Name: str,
        Type: DataSourceTypeType,
        DataSourceParameters: DataSourceParametersTypeDef = ...,
        Credentials: DataSourceCredentialsTypeDef = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        VpcConnectionProperties: VpcConnectionPropertiesTypeDef = ...,
        SslProperties: SslPropertiesTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_data_source)
        """

    def create_folder(
        self,
        *,
        AwsAccountId: str,
        FolderId: str,
        Name: str = ...,
        FolderType: Literal["SHARED"] = ...,
        ParentFolderArn: str = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateFolderResponseTypeDef:
        """
        Creates an empty shared folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_folder)
        """

    def create_folder_membership(
        self, *, AwsAccountId: str, FolderId: str, MemberId: str, MemberType: MemberTypeType
    ) -> CreateFolderMembershipResponseTypeDef:
        """
        Adds an asset, such as a dashboard, analysis, or dataset into a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_folder_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_folder_membership)
        """

    def create_group(
        self, *, GroupName: str, AwsAccountId: str, Namespace: str, Description: str = ...
    ) -> CreateGroupResponseTypeDef:
        """
        Creates an Amazon QuickSight group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_group)
        """

    def create_group_membership(
        self, *, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        Adds an Amazon QuickSight user to an Amazon QuickSight group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_group_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_group_membership)
        """

    def create_iam_policy_assignment(
        self,
        *,
        AwsAccountId: str,
        AssignmentName: str,
        AssignmentStatus: AssignmentStatusType,
        Namespace: str,
        PolicyArn: str = ...,
        Identities: Mapping[str, Sequence[str]] = ...
    ) -> CreateIAMPolicyAssignmentResponseTypeDef:
        """
        Creates an assignment with one specified IAM policy, identified by its Amazon
        Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_iam_policy_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_iam_policy_assignment)
        """

    def create_ingestion(
        self,
        *,
        DataSetId: str,
        IngestionId: str,
        AwsAccountId: str,
        IngestionType: IngestionTypeType = ...
    ) -> CreateIngestionResponseTypeDef:
        """
        Creates and starts a new SPICE ingestion for a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_ingestion)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_ingestion)
        """

    def create_namespace(
        self,
        *,
        AwsAccountId: str,
        Namespace: str,
        IdentityStore: Literal["QUICKSIGHT"],
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateNamespaceResponseTypeDef:
        """
        (Enterprise edition only) Creates a new namespace for you to use with Amazon
        QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_namespace)
        """

    def create_template(
        self,
        *,
        AwsAccountId: str,
        TemplateId: str,
        SourceEntity: TemplateSourceEntityTypeDef,
        Name: str = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        VersionDescription: str = ...
    ) -> CreateTemplateResponseTypeDef:
        """
        Creates a template from an existing Amazon QuickSight analysis or template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_template)
        """

    def create_template_alias(
        self, *, AwsAccountId: str, TemplateId: str, AliasName: str, TemplateVersionNumber: int
    ) -> CreateTemplateAliasResponseTypeDef:
        """
        Creates a template alias for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_template_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_template_alias)
        """

    def create_theme(
        self,
        *,
        AwsAccountId: str,
        ThemeId: str,
        Name: str,
        BaseThemeId: str,
        Configuration: ThemeConfigurationTypeDef,
        VersionDescription: str = ...,
        Permissions: Sequence[ResourcePermissionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateThemeResponseTypeDef:
        """
        Creates a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_theme)
        """

    def create_theme_alias(
        self, *, AwsAccountId: str, ThemeId: str, AliasName: str, ThemeVersionNumber: int
    ) -> CreateThemeAliasResponseTypeDef:
        """
        Creates a theme alias for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.create_theme_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#create_theme_alias)
        """

    def delete_account_customization(
        self, *, AwsAccountId: str, Namespace: str = ...
    ) -> DeleteAccountCustomizationResponseTypeDef:
        """
        Deletes all Amazon QuickSight customizations in this Amazon Web Services Region
        for the specified Amazon Web Services account and Amazon QuickSight namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_account_customization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_account_customization)
        """

    def delete_analysis(
        self,
        *,
        AwsAccountId: str,
        AnalysisId: str,
        RecoveryWindowInDays: int = ...,
        ForceDeleteWithoutRecovery: bool = ...
    ) -> DeleteAnalysisResponseTypeDef:
        """
        Deletes an analysis from Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_analysis)
        """

    def delete_dashboard(
        self, *, AwsAccountId: str, DashboardId: str, VersionNumber: int = ...
    ) -> DeleteDashboardResponseTypeDef:
        """
        Deletes a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_dashboard)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_dashboard)
        """

    def delete_data_set(self, *, AwsAccountId: str, DataSetId: str) -> DeleteDataSetResponseTypeDef:
        """
        Deletes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_data_set)
        """

    def delete_data_source(
        self, *, AwsAccountId: str, DataSourceId: str
    ) -> DeleteDataSourceResponseTypeDef:
        """
        Deletes the data source permanently.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_data_source)
        """

    def delete_folder(self, *, AwsAccountId: str, FolderId: str) -> DeleteFolderResponseTypeDef:
        """
        Deletes an empty folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_folder)
        """

    def delete_folder_membership(
        self, *, AwsAccountId: str, FolderId: str, MemberId: str, MemberType: MemberTypeType
    ) -> DeleteFolderMembershipResponseTypeDef:
        """
        Removes an asset, such as a dashboard, analysis, or dataset, from a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_folder_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_folder_membership)
        """

    def delete_group(
        self, *, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DeleteGroupResponseTypeDef:
        """
        Removes a user group from Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_group)
        """

    def delete_group_membership(
        self, *, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DeleteGroupMembershipResponseTypeDef:
        """
        Removes a user from a group so that the user is no longer a member of the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_group_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_group_membership)
        """

    def delete_iam_policy_assignment(
        self, *, AwsAccountId: str, AssignmentName: str, Namespace: str
    ) -> DeleteIAMPolicyAssignmentResponseTypeDef:
        """
        Deletes an existing IAM policy assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_iam_policy_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_iam_policy_assignment)
        """

    def delete_namespace(
        self, *, AwsAccountId: str, Namespace: str
    ) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes a namespace and the users and groups that are associated with the
        namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_namespace)
        """

    def delete_template(
        self, *, AwsAccountId: str, TemplateId: str, VersionNumber: int = ...
    ) -> DeleteTemplateResponseTypeDef:
        """
        Deletes a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_template)
        """

    def delete_template_alias(
        self, *, AwsAccountId: str, TemplateId: str, AliasName: str
    ) -> DeleteTemplateAliasResponseTypeDef:
        """
        Deletes the item that the specified template alias points to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_template_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_template_alias)
        """

    def delete_theme(
        self, *, AwsAccountId: str, ThemeId: str, VersionNumber: int = ...
    ) -> DeleteThemeResponseTypeDef:
        """
        Deletes a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_theme)
        """

    def delete_theme_alias(
        self, *, AwsAccountId: str, ThemeId: str, AliasName: str
    ) -> DeleteThemeAliasResponseTypeDef:
        """
        Deletes the version of the theme that the specified theme alias points to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_theme_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_theme_alias)
        """

    def delete_user(
        self, *, UserName: str, AwsAccountId: str, Namespace: str
    ) -> DeleteUserResponseTypeDef:
        """
        Deletes the Amazon QuickSight user that is associated with the identity of the
        Identity and Access Management (IAM) user or role that's making the call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_user)
        """

    def delete_user_by_principal_id(
        self, *, PrincipalId: str, AwsAccountId: str, Namespace: str
    ) -> DeleteUserByPrincipalIdResponseTypeDef:
        """
        Deletes a user identified by its principal ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.delete_user_by_principal_id)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#delete_user_by_principal_id)
        """

    def describe_account_customization(
        self, *, AwsAccountId: str, Namespace: str = ..., Resolved: bool = ...
    ) -> DescribeAccountCustomizationResponseTypeDef:
        """
        Describes the customizations associated with the provided Amazon Web Services
        account and Amazon Amazon QuickSight namespace in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_account_customization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_account_customization)
        """

    def describe_account_settings(
        self, *, AwsAccountId: str
    ) -> DescribeAccountSettingsResponseTypeDef:
        """
        Describes the settings that were used when your Amazon QuickSight subscription
        was first created in this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_account_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_account_settings)
        """

    def describe_analysis(
        self, *, AwsAccountId: str, AnalysisId: str
    ) -> DescribeAnalysisResponseTypeDef:
        """
        Provides a summary of the metadata for an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_analysis)
        """

    def describe_analysis_permissions(
        self, *, AwsAccountId: str, AnalysisId: str
    ) -> DescribeAnalysisPermissionsResponseTypeDef:
        """
        Provides the read and write permissions for an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_analysis_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_analysis_permissions)
        """

    def describe_dashboard(
        self, *, AwsAccountId: str, DashboardId: str, VersionNumber: int = ..., AliasName: str = ...
    ) -> DescribeDashboardResponseTypeDef:
        """
        Provides a summary for a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_dashboard)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_dashboard)
        """

    def describe_dashboard_permissions(
        self, *, AwsAccountId: str, DashboardId: str
    ) -> DescribeDashboardPermissionsResponseTypeDef:
        """
        Describes read and write permissions for a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_dashboard_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_dashboard_permissions)
        """

    def describe_data_set(
        self, *, AwsAccountId: str, DataSetId: str
    ) -> DescribeDataSetResponseTypeDef:
        """
        Describes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_data_set)
        """

    def describe_data_set_permissions(
        self, *, AwsAccountId: str, DataSetId: str
    ) -> DescribeDataSetPermissionsResponseTypeDef:
        """
        Describes the permissions on a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_data_set_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_data_set_permissions)
        """

    def describe_data_source(
        self, *, AwsAccountId: str, DataSourceId: str
    ) -> DescribeDataSourceResponseTypeDef:
        """
        Describes a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_data_source)
        """

    def describe_data_source_permissions(
        self, *, AwsAccountId: str, DataSourceId: str
    ) -> DescribeDataSourcePermissionsResponseTypeDef:
        """
        Describes the resource permissions for a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_data_source_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_data_source_permissions)
        """

    def describe_folder(self, *, AwsAccountId: str, FolderId: str) -> DescribeFolderResponseTypeDef:
        """
        Describes a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_folder)
        """

    def describe_folder_permissions(
        self, *, AwsAccountId: str, FolderId: str
    ) -> DescribeFolderPermissionsResponseTypeDef:
        """
        Describes permissions for a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_folder_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_folder_permissions)
        """

    def describe_folder_resolved_permissions(
        self, *, AwsAccountId: str, FolderId: str
    ) -> DescribeFolderResolvedPermissionsResponseTypeDef:
        """
        Describes the folder resolved permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_folder_resolved_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_folder_resolved_permissions)
        """

    def describe_group(
        self, *, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DescribeGroupResponseTypeDef:
        """
        Returns an Amazon QuickSight group's description and Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_group)
        """

    def describe_group_membership(
        self, *, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DescribeGroupMembershipResponseTypeDef:
        """
        Use the `DescribeGroupMembership` operation to determine if a user is a member
        of the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_group_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_group_membership)
        """

    def describe_iam_policy_assignment(
        self, *, AwsAccountId: str, AssignmentName: str, Namespace: str
    ) -> DescribeIAMPolicyAssignmentResponseTypeDef:
        """
        Describes an existing IAM policy assignment, as specified by the assignment
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_iam_policy_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_iam_policy_assignment)
        """

    def describe_ingestion(
        self, *, AwsAccountId: str, DataSetId: str, IngestionId: str
    ) -> DescribeIngestionResponseTypeDef:
        """
        Describes a SPICE ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_ingestion)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_ingestion)
        """

    def describe_ip_restriction(self, *, AwsAccountId: str) -> DescribeIpRestrictionResponseTypeDef:
        """
        Provides a summary and status of IP rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_ip_restriction)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_ip_restriction)
        """

    def describe_namespace(
        self, *, AwsAccountId: str, Namespace: str
    ) -> DescribeNamespaceResponseTypeDef:
        """
        Describes the current namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_namespace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_namespace)
        """

    def describe_template(
        self, *, AwsAccountId: str, TemplateId: str, VersionNumber: int = ..., AliasName: str = ...
    ) -> DescribeTemplateResponseTypeDef:
        """
        Describes a template's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_template)
        """

    def describe_template_alias(
        self, *, AwsAccountId: str, TemplateId: str, AliasName: str
    ) -> DescribeTemplateAliasResponseTypeDef:
        """
        Describes the template alias for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_template_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_template_alias)
        """

    def describe_template_permissions(
        self, *, AwsAccountId: str, TemplateId: str
    ) -> DescribeTemplatePermissionsResponseTypeDef:
        """
        Describes read and write permissions on a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_template_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_template_permissions)
        """

    def describe_theme(
        self, *, AwsAccountId: str, ThemeId: str, VersionNumber: int = ..., AliasName: str = ...
    ) -> DescribeThemeResponseTypeDef:
        """
        Describes a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_theme)
        """

    def describe_theme_alias(
        self, *, AwsAccountId: str, ThemeId: str, AliasName: str
    ) -> DescribeThemeAliasResponseTypeDef:
        """
        Describes the alias for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_theme_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_theme_alias)
        """

    def describe_theme_permissions(
        self, *, AwsAccountId: str, ThemeId: str
    ) -> DescribeThemePermissionsResponseTypeDef:
        """
        Describes the read and write permissions for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_theme_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_theme_permissions)
        """

    def describe_user(
        self, *, UserName: str, AwsAccountId: str, Namespace: str
    ) -> DescribeUserResponseTypeDef:
        """
        Returns information about a user, given the user name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.describe_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#describe_user)
        """

    def generate_embed_url_for_anonymous_user(
        self,
        *,
        AwsAccountId: str,
        Namespace: str,
        AuthorizedResourceArns: Sequence[str],
        ExperienceConfiguration: AnonymousUserEmbeddingExperienceConfigurationTypeDef,
        SessionLifetimeInMinutes: int = ...,
        SessionTags: Sequence[SessionTagTypeDef] = ...
    ) -> GenerateEmbedUrlForAnonymousUserResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon QuickSight dashboard
        in your website, without having to register any reader users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.generate_embed_url_for_anonymous_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#generate_embed_url_for_anonymous_user)
        """

    def generate_embed_url_for_registered_user(
        self,
        *,
        AwsAccountId: str,
        UserArn: str,
        ExperienceConfiguration: RegisteredUserEmbeddingExperienceConfigurationTypeDef,
        SessionLifetimeInMinutes: int = ...
    ) -> GenerateEmbedUrlForRegisteredUserResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon QuickSight experience
        in your website.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.generate_embed_url_for_registered_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#generate_embed_url_for_registered_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#generate_presigned_url)
        """

    def get_dashboard_embed_url(
        self,
        *,
        AwsAccountId: str,
        DashboardId: str,
        IdentityType: EmbeddingIdentityTypeType,
        SessionLifetimeInMinutes: int = ...,
        UndoRedoDisabled: bool = ...,
        ResetDisabled: bool = ...,
        StatePersistenceEnabled: bool = ...,
        UserArn: str = ...,
        Namespace: str = ...,
        AdditionalDashboardIds: Sequence[str] = ...
    ) -> GetDashboardEmbedUrlResponseTypeDef:
        """
        Generates a session URL and authorization code that you can use to embed an
        Amazon Amazon QuickSight read-only dashboard in your web server code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_dashboard_embed_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_dashboard_embed_url)
        """

    def get_session_embed_url(
        self,
        *,
        AwsAccountId: str,
        EntryPoint: str = ...,
        SessionLifetimeInMinutes: int = ...,
        UserArn: str = ...
    ) -> GetSessionEmbedUrlResponseTypeDef:
        """
        Generates a session URL and authorization code that you can use to embed the
        Amazon Amazon QuickSight console in your web server code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_session_embed_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_session_embed_url)
        """

    def list_analyses(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAnalysesResponseTypeDef:
        """
        Lists Amazon QuickSight analyses that exist in the specified Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_analyses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_analyses)
        """

    def list_dashboard_versions(
        self, *, AwsAccountId: str, DashboardId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDashboardVersionsResponseTypeDef:
        """
        Lists all the versions of the dashboards in the Amazon QuickSight subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_dashboard_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_dashboard_versions)
        """

    def list_dashboards(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDashboardsResponseTypeDef:
        """
        Lists dashboards in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_dashboards)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_dashboards)
        """

    def list_data_sets(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDataSetsResponseTypeDef:
        """
        Lists all of the datasets belonging to the current Amazon Web Services account
        in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_data_sets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_data_sets)
        """

    def list_data_sources(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists data sources in current Amazon Web Services Region that belong to this
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_data_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_data_sources)
        """

    def list_folder_members(
        self, *, AwsAccountId: str, FolderId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFolderMembersResponseTypeDef:
        """
        List all assets (`DASHBOARD` , `ANALYSIS` , and `DATASET` ) in a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_folder_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_folder_members)
        """

    def list_folders(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFoldersResponseTypeDef:
        """
        Lists all folders in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_folders)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_folders)
        """

    def list_group_memberships(
        self,
        *,
        GroupName: str,
        AwsAccountId: str,
        Namespace: str,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListGroupMembershipsResponseTypeDef:
        """
        Lists member users in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_group_memberships)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_group_memberships)
        """

    def list_groups(
        self, *, AwsAccountId: str, Namespace: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGroupsResponseTypeDef:
        """
        Lists all user groups in Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_groups)
        """

    def list_iam_policy_assignments(
        self,
        *,
        AwsAccountId: str,
        Namespace: str,
        AssignmentStatus: AssignmentStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListIAMPolicyAssignmentsResponseTypeDef:
        """
        Lists IAM policy assignments in the current Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_iam_policy_assignments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_iam_policy_assignments)
        """

    def list_iam_policy_assignments_for_user(
        self,
        *,
        AwsAccountId: str,
        UserName: str,
        Namespace: str,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListIAMPolicyAssignmentsForUserResponseTypeDef:
        """
        Lists all the IAM policy assignments, including the Amazon Resource Names (ARNs)
        for the IAM policies assigned to the specified user and group or groups that the
        user belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_iam_policy_assignments_for_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_iam_policy_assignments_for_user)
        """

    def list_ingestions(
        self, *, DataSetId: str, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListIngestionsResponseTypeDef:
        """
        Lists the history of SPICE ingestions for a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_ingestions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_ingestions)
        """

    def list_namespaces(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists the namespaces for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_namespaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_namespaces)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_tags_for_resource)
        """

    def list_template_aliases(
        self, *, AwsAccountId: str, TemplateId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTemplateAliasesResponseTypeDef:
        """
        Lists all the aliases of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_template_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_template_aliases)
        """

    def list_template_versions(
        self, *, AwsAccountId: str, TemplateId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTemplateVersionsResponseTypeDef:
        """
        Lists all the versions of the templates in the current Amazon QuickSight
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_template_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_template_versions)
        """

    def list_templates(
        self, *, AwsAccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTemplatesResponseTypeDef:
        """
        Lists all the templates in the current Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_templates)
        """

    def list_theme_aliases(
        self, *, AwsAccountId: str, ThemeId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListThemeAliasesResponseTypeDef:
        """
        Lists all the aliases of a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_theme_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_theme_aliases)
        """

    def list_theme_versions(
        self, *, AwsAccountId: str, ThemeId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListThemeVersionsResponseTypeDef:
        """
        Lists all the versions of the themes in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_theme_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_theme_versions)
        """

    def list_themes(
        self,
        *,
        AwsAccountId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Type: ThemeTypeType = ...
    ) -> ListThemesResponseTypeDef:
        """
        Lists all the themes in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_themes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_themes)
        """

    def list_user_groups(
        self,
        *,
        UserName: str,
        AwsAccountId: str,
        Namespace: str,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListUserGroupsResponseTypeDef:
        """
        Lists the Amazon QuickSight groups that an Amazon QuickSight user is a member
        of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_user_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_user_groups)
        """

    def list_users(
        self, *, AwsAccountId: str, Namespace: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListUsersResponseTypeDef:
        """
        Returns a list of all of the Amazon QuickSight users belonging to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.list_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#list_users)
        """

    def register_user(
        self,
        *,
        IdentityType: IdentityTypeType,
        Email: str,
        UserRole: UserRoleType,
        AwsAccountId: str,
        Namespace: str,
        IamArn: str = ...,
        SessionName: str = ...,
        UserName: str = ...,
        CustomPermissionsName: str = ...,
        ExternalLoginFederationProviderType: str = ...,
        CustomFederationProviderUrl: str = ...,
        ExternalLoginId: str = ...
    ) -> RegisterUserResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.register_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#register_user)
        """

    def restore_analysis(
        self, *, AwsAccountId: str, AnalysisId: str
    ) -> RestoreAnalysisResponseTypeDef:
        """
        Restores an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.restore_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#restore_analysis)
        """

    def search_analyses(
        self,
        *,
        AwsAccountId: str,
        Filters: Sequence[AnalysisSearchFilterTypeDef],
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> SearchAnalysesResponseTypeDef:
        """
        Searches for analyses that belong to the user specified in the filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.search_analyses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#search_analyses)
        """

    def search_dashboards(
        self,
        *,
        AwsAccountId: str,
        Filters: Sequence[DashboardSearchFilterTypeDef],
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> SearchDashboardsResponseTypeDef:
        """
        Searches for dashboards that belong to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.search_dashboards)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#search_dashboards)
        """

    def search_folders(
        self,
        *,
        AwsAccountId: str,
        Filters: Sequence[FolderSearchFilterTypeDef],
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> SearchFoldersResponseTypeDef:
        """
        Searches the subfolders in a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.search_folders)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#search_folders)
        """

    def search_groups(
        self,
        *,
        AwsAccountId: str,
        Namespace: str,
        Filters: Sequence[GroupSearchFilterTypeDef],
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> SearchGroupsResponseTypeDef:
        """
        Use the `SearchGroups` operation to search groups in a specified Amazon
        QuickSight namespace using the supplied filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.search_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#search_groups)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> TagResourceResponseTypeDef:
        """
        Assigns one or more tags (key-value pairs) to the specified Amazon QuickSight
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> UntagResourceResponseTypeDef:
        """
        Removes a tag or tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#untag_resource)
        """

    def update_account_customization(
        self,
        *,
        AwsAccountId: str,
        AccountCustomization: AccountCustomizationTypeDef,
        Namespace: str = ...
    ) -> UpdateAccountCustomizationResponseTypeDef:
        """
        Updates Amazon QuickSight customizations the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_account_customization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_account_customization)
        """

    def update_account_settings(
        self, *, AwsAccountId: str, DefaultNamespace: str, NotificationEmail: str = ...
    ) -> UpdateAccountSettingsResponseTypeDef:
        """
        Updates the Amazon QuickSight settings in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_account_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_account_settings)
        """

    def update_analysis(
        self,
        *,
        AwsAccountId: str,
        AnalysisId: str,
        Name: str,
        SourceEntity: AnalysisSourceEntityTypeDef,
        Parameters: ParametersTypeDef = ...,
        ThemeArn: str = ...
    ) -> UpdateAnalysisResponseTypeDef:
        """
        Updates an analysis in Amazon QuickSight See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateAnalysis).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_analysis)
        """

    def update_analysis_permissions(
        self,
        *,
        AwsAccountId: str,
        AnalysisId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateAnalysisPermissionsResponseTypeDef:
        """
        Updates the read and write permissions for an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_analysis_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_analysis_permissions)
        """

    def update_dashboard(
        self,
        *,
        AwsAccountId: str,
        DashboardId: str,
        Name: str,
        SourceEntity: DashboardSourceEntityTypeDef,
        Parameters: ParametersTypeDef = ...,
        VersionDescription: str = ...,
        DashboardPublishOptions: DashboardPublishOptionsTypeDef = ...,
        ThemeArn: str = ...
    ) -> UpdateDashboardResponseTypeDef:
        """
        Updates a dashboard in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_dashboard)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_dashboard)
        """

    def update_dashboard_permissions(
        self,
        *,
        AwsAccountId: str,
        DashboardId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...,
        GrantLinkPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokeLinkPermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateDashboardPermissionsResponseTypeDef:
        """
        Updates read and write permissions on a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_dashboard_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_dashboard_permissions)
        """

    def update_dashboard_published_version(
        self, *, AwsAccountId: str, DashboardId: str, VersionNumber: int
    ) -> UpdateDashboardPublishedVersionResponseTypeDef:
        """
        Updates the published version of a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_dashboard_published_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_dashboard_published_version)
        """

    def update_data_set(
        self,
        *,
        AwsAccountId: str,
        DataSetId: str,
        Name: str,
        PhysicalTableMap: Mapping[str, PhysicalTableTypeDef],
        ImportMode: DataSetImportModeType,
        LogicalTableMap: Mapping[str, LogicalTableTypeDef] = ...,
        ColumnGroups: Sequence[ColumnGroupTypeDef] = ...,
        FieldFolders: Mapping[str, FieldFolderTypeDef] = ...,
        RowLevelPermissionDataSet: RowLevelPermissionDataSetTypeDef = ...,
        RowLevelPermissionTagConfiguration: RowLevelPermissionTagConfigurationTypeDef = ...,
        ColumnLevelPermissionRules: Sequence[ColumnLevelPermissionRuleTypeDef] = ...,
        DataSetUsageConfiguration: DataSetUsageConfigurationTypeDef = ...
    ) -> UpdateDataSetResponseTypeDef:
        """
        Updates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_data_set)
        """

    def update_data_set_permissions(
        self,
        *,
        AwsAccountId: str,
        DataSetId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateDataSetPermissionsResponseTypeDef:
        """
        Updates the permissions on a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_data_set_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_data_set_permissions)
        """

    def update_data_source(
        self,
        *,
        AwsAccountId: str,
        DataSourceId: str,
        Name: str,
        DataSourceParameters: DataSourceParametersTypeDef = ...,
        Credentials: DataSourceCredentialsTypeDef = ...,
        VpcConnectionProperties: VpcConnectionPropertiesTypeDef = ...,
        SslProperties: SslPropertiesTypeDef = ...
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_data_source)
        """

    def update_data_source_permissions(
        self,
        *,
        AwsAccountId: str,
        DataSourceId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateDataSourcePermissionsResponseTypeDef:
        """
        Updates the permissions to a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_data_source_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_data_source_permissions)
        """

    def update_folder(
        self, *, AwsAccountId: str, FolderId: str, Name: str
    ) -> UpdateFolderResponseTypeDef:
        """
        Updates the name of a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_folder)
        """

    def update_folder_permissions(
        self,
        *,
        AwsAccountId: str,
        FolderId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateFolderPermissionsResponseTypeDef:
        """
        Updates permissions of a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_folder_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_folder_permissions)
        """

    def update_group(
        self, *, GroupName: str, AwsAccountId: str, Namespace: str, Description: str = ...
    ) -> UpdateGroupResponseTypeDef:
        """
        Changes a group description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_group)
        """

    def update_iam_policy_assignment(
        self,
        *,
        AwsAccountId: str,
        AssignmentName: str,
        Namespace: str,
        AssignmentStatus: AssignmentStatusType = ...,
        PolicyArn: str = ...,
        Identities: Mapping[str, Sequence[str]] = ...
    ) -> UpdateIAMPolicyAssignmentResponseTypeDef:
        """
        Updates an existing IAM policy assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_iam_policy_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_iam_policy_assignment)
        """

    def update_ip_restriction(
        self,
        *,
        AwsAccountId: str,
        IpRestrictionRuleMap: Mapping[str, str] = ...,
        Enabled: bool = ...
    ) -> UpdateIpRestrictionResponseTypeDef:
        """
        Updates the content and status of IP rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_ip_restriction)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_ip_restriction)
        """

    def update_public_sharing_settings(
        self, *, AwsAccountId: str, PublicSharingEnabled: bool = ...
    ) -> UpdatePublicSharingSettingsResponseTypeDef:
        """
        Use the UpdatePublicSharingSettings operation to enable or disable the public
        sharing settings of an Amazon QuickSight dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_public_sharing_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_public_sharing_settings)
        """

    def update_template(
        self,
        *,
        AwsAccountId: str,
        TemplateId: str,
        SourceEntity: TemplateSourceEntityTypeDef,
        VersionDescription: str = ...,
        Name: str = ...
    ) -> UpdateTemplateResponseTypeDef:
        """
        Updates a template from an existing Amazon QuickSight analysis or another
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_template)
        """

    def update_template_alias(
        self, *, AwsAccountId: str, TemplateId: str, AliasName: str, TemplateVersionNumber: int
    ) -> UpdateTemplateAliasResponseTypeDef:
        """
        Updates the template alias of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_template_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_template_alias)
        """

    def update_template_permissions(
        self,
        *,
        AwsAccountId: str,
        TemplateId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateTemplatePermissionsResponseTypeDef:
        """
        Updates the resource permissions for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_template_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_template_permissions)
        """

    def update_theme(
        self,
        *,
        AwsAccountId: str,
        ThemeId: str,
        BaseThemeId: str,
        Name: str = ...,
        VersionDescription: str = ...,
        Configuration: ThemeConfigurationTypeDef = ...
    ) -> UpdateThemeResponseTypeDef:
        """
        Updates a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_theme)
        """

    def update_theme_alias(
        self, *, AwsAccountId: str, ThemeId: str, AliasName: str, ThemeVersionNumber: int
    ) -> UpdateThemeAliasResponseTypeDef:
        """
        Updates an alias of a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_theme_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_theme_alias)
        """

    def update_theme_permissions(
        self,
        *,
        AwsAccountId: str,
        ThemeId: str,
        GrantPermissions: Sequence[ResourcePermissionTypeDef] = ...,
        RevokePermissions: Sequence[ResourcePermissionTypeDef] = ...
    ) -> UpdateThemePermissionsResponseTypeDef:
        """
        Updates the resource permissions for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_theme_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_theme_permissions)
        """

    def update_user(
        self,
        *,
        UserName: str,
        AwsAccountId: str,
        Namespace: str,
        Email: str,
        Role: UserRoleType,
        CustomPermissionsName: str = ...,
        UnapplyCustomPermissions: bool = ...,
        ExternalLoginFederationProviderType: str = ...,
        CustomFederationProviderUrl: str = ...,
        ExternalLoginId: str = ...
    ) -> UpdateUserResponseTypeDef:
        """
        Updates an Amazon QuickSight user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.update_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_analyses"]) -> ListAnalysesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dashboard_versions"]
    ) -> ListDashboardVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_dashboards"]) -> ListDashboardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_sets"]) -> ListDataSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ingestions"]) -> ListIngestionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_namespaces"]) -> ListNamespacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_template_aliases"]
    ) -> ListTemplateAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_template_versions"]
    ) -> ListTemplateVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_templates"]) -> ListTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_theme_versions"]
    ) -> ListThemeVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_themes"]) -> ListThemesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_analyses"]) -> SearchAnalysesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_dashboards"]
    ) -> SearchDashboardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/client/#get_paginator)
        """
