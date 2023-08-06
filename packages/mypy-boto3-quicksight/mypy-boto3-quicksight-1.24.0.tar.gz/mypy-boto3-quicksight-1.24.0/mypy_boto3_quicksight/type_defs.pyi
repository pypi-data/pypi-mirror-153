"""
Type annotations for quicksight service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/type_defs/)

Usage::

    ```python
    from mypy_boto3_quicksight.type_defs import AccountCustomizationTypeDef

    data: AccountCustomizationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AnalysisErrorTypeType,
    AssignmentStatusType,
    ColumnDataTypeType,
    ColumnTagNameType,
    DashboardBehaviorType,
    DashboardErrorTypeType,
    DashboardUIStateType,
    DataSetImportModeType,
    DataSourceErrorInfoTypeType,
    DataSourceTypeType,
    EditionType,
    EmbeddingIdentityTypeType,
    FileFormatType,
    GeoSpatialDataRoleType,
    IdentityTypeType,
    IngestionErrorTypeType,
    IngestionRequestSourceType,
    IngestionRequestTypeType,
    IngestionStatusType,
    IngestionTypeType,
    InputColumnDataTypeType,
    JoinTypeType,
    MemberTypeType,
    NamespaceErrorTypeType,
    NamespaceStatusType,
    ResourceStatusType,
    RowLevelPermissionFormatVersionType,
    RowLevelPermissionPolicyType,
    StatusType,
    TemplateErrorTypeType,
    TextQualifierType,
    ThemeTypeType,
    UserRoleType,
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
    "AccountCustomizationTypeDef",
    "AccountSettingsTypeDef",
    "ActiveIAMPolicyAssignmentTypeDef",
    "AdHocFilteringOptionTypeDef",
    "AmazonElasticsearchParametersTypeDef",
    "AmazonOpenSearchParametersTypeDef",
    "AnalysisErrorTypeDef",
    "AnalysisSearchFilterTypeDef",
    "DataSetReferenceTypeDef",
    "AnalysisSummaryTypeDef",
    "SheetTypeDef",
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    "AthenaParametersTypeDef",
    "AuroraParametersTypeDef",
    "AuroraPostgreSqlParametersTypeDef",
    "AwsIotAnalyticsParametersTypeDef",
    "BorderStyleTypeDef",
    "CalculatedColumnTypeDef",
    "CancelIngestionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CastColumnTypeOperationTypeDef",
    "ColumnDescriptionTypeDef",
    "ColumnGroupColumnSchemaTypeDef",
    "GeoSpatialColumnGroupTypeDef",
    "ColumnLevelPermissionRuleTypeDef",
    "ColumnSchemaTypeDef",
    "TagTypeDef",
    "ResourcePermissionTypeDef",
    "DataSetUsageConfigurationTypeDef",
    "FieldFolderTypeDef",
    "RowLevelPermissionDataSetTypeDef",
    "SslPropertiesTypeDef",
    "VpcConnectionPropertiesTypeDef",
    "CreateFolderMembershipRequestRequestTypeDef",
    "FolderMemberTypeDef",
    "CreateGroupMembershipRequestRequestTypeDef",
    "GroupMemberTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "GroupTypeDef",
    "CreateIAMPolicyAssignmentRequestRequestTypeDef",
    "CreateIngestionRequestRequestTypeDef",
    "CreateTemplateAliasRequestRequestTypeDef",
    "TemplateAliasTypeDef",
    "CreateThemeAliasRequestRequestTypeDef",
    "ThemeAliasTypeDef",
    "InputColumnTypeDef",
    "DashboardErrorTypeDef",
    "ExportToCSVOptionTypeDef",
    "SheetControlsOptionTypeDef",
    "DashboardSearchFilterTypeDef",
    "DashboardSummaryTypeDef",
    "DashboardVersionSummaryTypeDef",
    "DataColorPaletteTypeDef",
    "OutputColumnTypeDef",
    "DataSourceErrorInfoTypeDef",
    "ExasolParametersTypeDef",
    "JiraParametersTypeDef",
    "MariaDbParametersTypeDef",
    "MySqlParametersTypeDef",
    "OracleParametersTypeDef",
    "PostgreSqlParametersTypeDef",
    "PrestoParametersTypeDef",
    "RdsParametersTypeDef",
    "RedshiftParametersTypeDef",
    "ServiceNowParametersTypeDef",
    "SnowflakeParametersTypeDef",
    "SparkParametersTypeDef",
    "SqlServerParametersTypeDef",
    "TeradataParametersTypeDef",
    "TwitterParametersTypeDef",
    "DateTimeParameterTypeDef",
    "DecimalParameterTypeDef",
    "DeleteAccountCustomizationRequestRequestTypeDef",
    "DeleteAnalysisRequestRequestTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteDataSetRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteFolderMembershipRequestRequestTypeDef",
    "DeleteFolderRequestRequestTypeDef",
    "DeleteGroupMembershipRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteTemplateAliasRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteThemeAliasRequestRequestTypeDef",
    "DeleteThemeRequestRequestTypeDef",
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeAccountCustomizationRequestRequestTypeDef",
    "DescribeAccountSettingsRequestRequestTypeDef",
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    "DescribeAnalysisRequestRequestTypeDef",
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    "DescribeDataSetRequestRequestTypeDef",
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    "DescribeDataSourceRequestRequestTypeDef",
    "DescribeFolderPermissionsRequestRequestTypeDef",
    "DescribeFolderRequestRequestTypeDef",
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    "FolderTypeDef",
    "DescribeGroupMembershipRequestRequestTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    "IAMPolicyAssignmentTypeDef",
    "DescribeIngestionRequestRequestTypeDef",
    "DescribeIpRestrictionRequestRequestTypeDef",
    "DescribeNamespaceRequestRequestTypeDef",
    "DescribeTemplateAliasRequestRequestTypeDef",
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    "DescribeTemplateRequestRequestTypeDef",
    "DescribeThemeAliasRequestRequestTypeDef",
    "DescribeThemePermissionsRequestRequestTypeDef",
    "DescribeThemeRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "UserTypeDef",
    "ErrorInfoTypeDef",
    "FilterOperationTypeDef",
    "FolderSearchFilterTypeDef",
    "FolderSummaryTypeDef",
    "SessionTagTypeDef",
    "GetDashboardEmbedUrlRequestRequestTypeDef",
    "GetSessionEmbedUrlRequestRequestTypeDef",
    "GroupSearchFilterTypeDef",
    "GutterStyleTypeDef",
    "IAMPolicyAssignmentSummaryTypeDef",
    "QueueInfoTypeDef",
    "RowInfoTypeDef",
    "IntegerParameterTypeDef",
    "JoinKeyPropertiesTypeDef",
    "PaginatorConfigTypeDef",
    "ListAnalysesRequestRequestTypeDef",
    "ListDashboardVersionsRequestRequestTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListFolderMembersRequestRequestTypeDef",
    "MemberIdArnPairTypeDef",
    "ListFoldersRequestRequestTypeDef",
    "ListGroupMembershipsRequestRequestTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsRequestRequestTypeDef",
    "ListIngestionsRequestRequestTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTemplateAliasesRequestRequestTypeDef",
    "ListTemplateVersionsRequestRequestTypeDef",
    "TemplateVersionSummaryTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "ListThemeAliasesRequestRequestTypeDef",
    "ListThemeVersionsRequestRequestTypeDef",
    "ThemeVersionSummaryTypeDef",
    "ListThemesRequestRequestTypeDef",
    "ThemeSummaryTypeDef",
    "ListUserGroupsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ManifestFileLocationTypeDef",
    "MarginStyleTypeDef",
    "NamespaceErrorTypeDef",
    "StringParameterTypeDef",
    "ProjectOperationTypeDef",
    "RegisterUserRequestRequestTypeDef",
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    "RenameColumnOperationTypeDef",
    "RestoreAnalysisRequestRequestTypeDef",
    "RowLevelPermissionTagRuleTypeDef",
    "UploadSettingsTypeDef",
    "TemplateErrorTypeDef",
    "TemplateSourceTemplateTypeDef",
    "UIColorPaletteTypeDef",
    "ThemeErrorTypeDef",
    "UntagColumnOperationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    "UpdateFolderRequestRequestTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateIAMPolicyAssignmentRequestRequestTypeDef",
    "UpdateIpRestrictionRequestRequestTypeDef",
    "UpdatePublicSharingSettingsRequestRequestTypeDef",
    "UpdateTemplateAliasRequestRequestTypeDef",
    "UpdateThemeAliasRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateAccountCustomizationRequestRequestTypeDef",
    "SearchAnalysesRequestRequestTypeDef",
    "AnalysisSourceTemplateTypeDef",
    "DashboardSourceTemplateTypeDef",
    "TemplateSourceAnalysisTypeDef",
    "AnalysisTypeDef",
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    "TileStyleTypeDef",
    "CreateColumnsOperationTypeDef",
    "CancelIngestionResponseTypeDef",
    "CreateAccountCustomizationResponseTypeDef",
    "CreateAnalysisResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFolderResponseTypeDef",
    "CreateIAMPolicyAssignmentResponseTypeDef",
    "CreateIngestionResponseTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateTemplateResponseTypeDef",
    "CreateThemeResponseTypeDef",
    "DeleteAccountCustomizationResponseTypeDef",
    "DeleteAnalysisResponseTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteDataSetResponseTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteFolderMembershipResponseTypeDef",
    "DeleteFolderResponseTypeDef",
    "DeleteGroupMembershipResponseTypeDef",
    "DeleteGroupResponseTypeDef",
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteTemplateAliasResponseTypeDef",
    "DeleteTemplateResponseTypeDef",
    "DeleteThemeAliasResponseTypeDef",
    "DeleteThemeResponseTypeDef",
    "DeleteUserByPrincipalIdResponseTypeDef",
    "DeleteUserResponseTypeDef",
    "DescribeAccountCustomizationResponseTypeDef",
    "DescribeAccountSettingsResponseTypeDef",
    "DescribeIpRestrictionResponseTypeDef",
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    "GetDashboardEmbedUrlResponseTypeDef",
    "GetSessionEmbedUrlResponseTypeDef",
    "ListAnalysesResponseTypeDef",
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    "RestoreAnalysisResponseTypeDef",
    "SearchAnalysesResponseTypeDef",
    "TagResourceResponseTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateAccountCustomizationResponseTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateAnalysisResponseTypeDef",
    "UpdateDashboardPublishedVersionResponseTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateDataSetPermissionsResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateDataSourcePermissionsResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateFolderResponseTypeDef",
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    "UpdateIpRestrictionResponseTypeDef",
    "UpdatePublicSharingSettingsResponseTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateThemeResponseTypeDef",
    "ColumnTagTypeDef",
    "ColumnGroupSchemaTypeDef",
    "ColumnGroupTypeDef",
    "DataSetSchemaTypeDef",
    "CreateAccountCustomizationRequestRequestTypeDef",
    "CreateNamespaceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateFolderRequestRequestTypeDef",
    "DescribeAnalysisPermissionsResponseTypeDef",
    "DescribeDataSetPermissionsResponseTypeDef",
    "DescribeDataSourcePermissionsResponseTypeDef",
    "DescribeFolderPermissionsResponseTypeDef",
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    "DescribeTemplatePermissionsResponseTypeDef",
    "DescribeThemePermissionsResponseTypeDef",
    "LinkSharingConfigurationTypeDef",
    "UpdateAnalysisPermissionsRequestRequestTypeDef",
    "UpdateAnalysisPermissionsResponseTypeDef",
    "UpdateDashboardPermissionsRequestRequestTypeDef",
    "UpdateDataSetPermissionsRequestRequestTypeDef",
    "UpdateDataSourcePermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsResponseTypeDef",
    "UpdateTemplatePermissionsRequestRequestTypeDef",
    "UpdateTemplatePermissionsResponseTypeDef",
    "UpdateThemePermissionsRequestRequestTypeDef",
    "UpdateThemePermissionsResponseTypeDef",
    "DataSetSummaryTypeDef",
    "CreateFolderMembershipResponseTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "CreateGroupResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ListUserGroupsResponseTypeDef",
    "SearchGroupsResponseTypeDef",
    "UpdateGroupResponseTypeDef",
    "CreateTemplateAliasResponseTypeDef",
    "DescribeTemplateAliasResponseTypeDef",
    "ListTemplateAliasesResponseTypeDef",
    "UpdateTemplateAliasResponseTypeDef",
    "CreateThemeAliasResponseTypeDef",
    "DescribeThemeAliasResponseTypeDef",
    "ListThemeAliasesResponseTypeDef",
    "UpdateThemeAliasResponseTypeDef",
    "CustomSqlTypeDef",
    "RelationalTableTypeDef",
    "DashboardVersionTypeDef",
    "DashboardPublishOptionsTypeDef",
    "SearchDashboardsRequestRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "SearchDashboardsResponseTypeDef",
    "ListDashboardVersionsResponseTypeDef",
    "DescribeFolderResponseTypeDef",
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "ListUsersResponseTypeDef",
    "RegisterUserResponseTypeDef",
    "UpdateUserResponseTypeDef",
    "SearchFoldersRequestRequestTypeDef",
    "ListFoldersResponseTypeDef",
    "SearchFoldersResponseTypeDef",
    "SearchGroupsRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsResponseTypeDef",
    "IngestionTypeDef",
    "JoinInstructionTypeDef",
    "ListAnalysesRequestListAnalysesPaginateTypeDef",
    "ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    "ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    "ListThemesRequestListThemesPaginateTypeDef",
    "SearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    "SearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    "ListFolderMembersResponseTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListThemeVersionsResponseTypeDef",
    "ListThemesResponseTypeDef",
    "S3ParametersTypeDef",
    "TileLayoutStyleTypeDef",
    "NamespaceInfoV2TypeDef",
    "ParametersTypeDef",
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    "RowLevelPermissionTagConfigurationTypeDef",
    "S3SourceTypeDef",
    "AnalysisSourceEntityTypeDef",
    "DashboardSourceEntityTypeDef",
    "TemplateSourceEntityTypeDef",
    "DescribeAnalysisResponseTypeDef",
    "GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    "TagColumnOperationTypeDef",
    "DataSetConfigurationTypeDef",
    "DescribeDashboardPermissionsResponseTypeDef",
    "UpdateDashboardPermissionsResponseTypeDef",
    "ListDataSetsResponseTypeDef",
    "DashboardTypeDef",
    "DescribeIngestionResponseTypeDef",
    "ListIngestionsResponseTypeDef",
    "LogicalTableSourceTypeDef",
    "DataSourceParametersTypeDef",
    "SheetStyleTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "ListNamespacesResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    "PhysicalTableTypeDef",
    "CreateAnalysisRequestRequestTypeDef",
    "UpdateAnalysisRequestRequestTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "TransformOperationTypeDef",
    "TemplateVersionTypeDef",
    "DescribeDashboardResponseTypeDef",
    "CredentialPairTypeDef",
    "DataSourceTypeDef",
    "ThemeConfigurationTypeDef",
    "LogicalTableTypeDef",
    "TemplateTypeDef",
    "DataSourceCredentialsTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "ListDataSourcesResponseTypeDef",
    "CreateThemeRequestRequestTypeDef",
    "ThemeVersionTypeDef",
    "UpdateThemeRequestRequestTypeDef",
    "CreateDataSetRequestRequestTypeDef",
    "DataSetTypeDef",
    "UpdateDataSetRequestRequestTypeDef",
    "DescribeTemplateResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "ThemeTypeDef",
    "DescribeDataSetResponseTypeDef",
    "DescribeThemeResponseTypeDef",
)

AccountCustomizationTypeDef = TypedDict(
    "AccountCustomizationTypeDef",
    {
        "DefaultTheme": str,
        "DefaultEmailCustomizationTemplate": str,
    },
    total=False,
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "AccountName": str,
        "Edition": EditionType,
        "DefaultNamespace": str,
        "NotificationEmail": str,
        "PublicSharingEnabled": bool,
    },
    total=False,
)

ActiveIAMPolicyAssignmentTypeDef = TypedDict(
    "ActiveIAMPolicyAssignmentTypeDef",
    {
        "AssignmentName": str,
        "PolicyArn": str,
    },
    total=False,
)

AdHocFilteringOptionTypeDef = TypedDict(
    "AdHocFilteringOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

AmazonElasticsearchParametersTypeDef = TypedDict(
    "AmazonElasticsearchParametersTypeDef",
    {
        "Domain": str,
    },
)

AmazonOpenSearchParametersTypeDef = TypedDict(
    "AmazonOpenSearchParametersTypeDef",
    {
        "Domain": str,
    },
)

AnalysisErrorTypeDef = TypedDict(
    "AnalysisErrorTypeDef",
    {
        "Type": AnalysisErrorTypeType,
        "Message": str,
    },
    total=False,
)

AnalysisSearchFilterTypeDef = TypedDict(
    "AnalysisSearchFilterTypeDef",
    {
        "Operator": Literal["StringEquals"],
        "Name": Literal["QUICKSIGHT_USER"],
        "Value": str,
    },
    total=False,
)

DataSetReferenceTypeDef = TypedDict(
    "DataSetReferenceTypeDef",
    {
        "DataSetPlaceholder": str,
        "DataSetArn": str,
    },
)

AnalysisSummaryTypeDef = TypedDict(
    "AnalysisSummaryTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "Name": str,
        "Status": ResourceStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

SheetTypeDef = TypedDict(
    "SheetTypeDef",
    {
        "SheetId": str,
        "Name": str,
    },
    total=False,
)

AnonymousUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardId": str,
    },
)

AthenaParametersTypeDef = TypedDict(
    "AthenaParametersTypeDef",
    {
        "WorkGroup": str,
    },
    total=False,
)

AuroraParametersTypeDef = TypedDict(
    "AuroraParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

AuroraPostgreSqlParametersTypeDef = TypedDict(
    "AuroraPostgreSqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

AwsIotAnalyticsParametersTypeDef = TypedDict(
    "AwsIotAnalyticsParametersTypeDef",
    {
        "DataSetName": str,
    },
)

BorderStyleTypeDef = TypedDict(
    "BorderStyleTypeDef",
    {
        "Show": bool,
    },
    total=False,
)

CalculatedColumnTypeDef = TypedDict(
    "CalculatedColumnTypeDef",
    {
        "ColumnName": str,
        "ColumnId": str,
        "Expression": str,
    },
)

CancelIngestionRequestRequestTypeDef = TypedDict(
    "CancelIngestionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "IngestionId": str,
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

_RequiredCastColumnTypeOperationTypeDef = TypedDict(
    "_RequiredCastColumnTypeOperationTypeDef",
    {
        "ColumnName": str,
        "NewColumnType": ColumnDataTypeType,
    },
)
_OptionalCastColumnTypeOperationTypeDef = TypedDict(
    "_OptionalCastColumnTypeOperationTypeDef",
    {
        "Format": str,
    },
    total=False,
)

class CastColumnTypeOperationTypeDef(
    _RequiredCastColumnTypeOperationTypeDef, _OptionalCastColumnTypeOperationTypeDef
):
    pass

ColumnDescriptionTypeDef = TypedDict(
    "ColumnDescriptionTypeDef",
    {
        "Text": str,
    },
    total=False,
)

ColumnGroupColumnSchemaTypeDef = TypedDict(
    "ColumnGroupColumnSchemaTypeDef",
    {
        "Name": str,
    },
    total=False,
)

GeoSpatialColumnGroupTypeDef = TypedDict(
    "GeoSpatialColumnGroupTypeDef",
    {
        "Name": str,
        "CountryCode": Literal["US"],
        "Columns": Sequence[str],
    },
)

ColumnLevelPermissionRuleTypeDef = TypedDict(
    "ColumnLevelPermissionRuleTypeDef",
    {
        "Principals": Sequence[str],
        "ColumnNames": Sequence[str],
    },
    total=False,
)

ColumnSchemaTypeDef = TypedDict(
    "ColumnSchemaTypeDef",
    {
        "Name": str,
        "DataType": str,
        "GeographicRole": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

ResourcePermissionTypeDef = TypedDict(
    "ResourcePermissionTypeDef",
    {
        "Principal": str,
        "Actions": Sequence[str],
    },
)

DataSetUsageConfigurationTypeDef = TypedDict(
    "DataSetUsageConfigurationTypeDef",
    {
        "DisableUseAsDirectQuerySource": bool,
        "DisableUseAsImportedSource": bool,
    },
    total=False,
)

FieldFolderTypeDef = TypedDict(
    "FieldFolderTypeDef",
    {
        "description": str,
        "columns": Sequence[str],
    },
    total=False,
)

_RequiredRowLevelPermissionDataSetTypeDef = TypedDict(
    "_RequiredRowLevelPermissionDataSetTypeDef",
    {
        "Arn": str,
        "PermissionPolicy": RowLevelPermissionPolicyType,
    },
)
_OptionalRowLevelPermissionDataSetTypeDef = TypedDict(
    "_OptionalRowLevelPermissionDataSetTypeDef",
    {
        "Namespace": str,
        "FormatVersion": RowLevelPermissionFormatVersionType,
        "Status": StatusType,
    },
    total=False,
)

class RowLevelPermissionDataSetTypeDef(
    _RequiredRowLevelPermissionDataSetTypeDef, _OptionalRowLevelPermissionDataSetTypeDef
):
    pass

SslPropertiesTypeDef = TypedDict(
    "SslPropertiesTypeDef",
    {
        "DisableSsl": bool,
    },
    total=False,
)

VpcConnectionPropertiesTypeDef = TypedDict(
    "VpcConnectionPropertiesTypeDef",
    {
        "VpcConnectionArn": str,
    },
)

CreateFolderMembershipRequestRequestTypeDef = TypedDict(
    "CreateFolderMembershipRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
)

FolderMemberTypeDef = TypedDict(
    "FolderMemberTypeDef",
    {
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
    total=False,
)

CreateGroupMembershipRequestRequestTypeDef = TypedDict(
    "CreateGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

GroupMemberTypeDef = TypedDict(
    "GroupMemberTypeDef",
    {
        "Arn": str,
        "MemberName": str,
    },
    total=False,
)

_RequiredCreateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalCreateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class CreateGroupRequestRequestTypeDef(
    _RequiredCreateGroupRequestRequestTypeDef, _OptionalCreateGroupRequestRequestTypeDef
):
    pass

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Arn": str,
        "GroupName": str,
        "Description": str,
        "PrincipalId": str,
    },
    total=False,
)

_RequiredCreateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "AssignmentStatus": AssignmentStatusType,
        "Namespace": str,
    },
)
_OptionalCreateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "Identities": Mapping[str, Sequence[str]],
    },
    total=False,
)

class CreateIAMPolicyAssignmentRequestRequestTypeDef(
    _RequiredCreateIAMPolicyAssignmentRequestRequestTypeDef,
    _OptionalCreateIAMPolicyAssignmentRequestRequestTypeDef,
):
    pass

_RequiredCreateIngestionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIngestionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "IngestionId": str,
        "AwsAccountId": str,
    },
)
_OptionalCreateIngestionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIngestionRequestRequestTypeDef",
    {
        "IngestionType": IngestionTypeType,
    },
    total=False,
)

class CreateIngestionRequestRequestTypeDef(
    _RequiredCreateIngestionRequestRequestTypeDef, _OptionalCreateIngestionRequestRequestTypeDef
):
    pass

CreateTemplateAliasRequestRequestTypeDef = TypedDict(
    "CreateTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
        "TemplateVersionNumber": int,
    },
)

TemplateAliasTypeDef = TypedDict(
    "TemplateAliasTypeDef",
    {
        "AliasName": str,
        "Arn": str,
        "TemplateVersionNumber": int,
    },
    total=False,
)

CreateThemeAliasRequestRequestTypeDef = TypedDict(
    "CreateThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
)

ThemeAliasTypeDef = TypedDict(
    "ThemeAliasTypeDef",
    {
        "Arn": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
    total=False,
)

InputColumnTypeDef = TypedDict(
    "InputColumnTypeDef",
    {
        "Name": str,
        "Type": InputColumnDataTypeType,
    },
)

DashboardErrorTypeDef = TypedDict(
    "DashboardErrorTypeDef",
    {
        "Type": DashboardErrorTypeType,
        "Message": str,
    },
    total=False,
)

ExportToCSVOptionTypeDef = TypedDict(
    "ExportToCSVOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

SheetControlsOptionTypeDef = TypedDict(
    "SheetControlsOptionTypeDef",
    {
        "VisibilityState": DashboardUIStateType,
    },
    total=False,
)

_RequiredDashboardSearchFilterTypeDef = TypedDict(
    "_RequiredDashboardSearchFilterTypeDef",
    {
        "Operator": Literal["StringEquals"],
    },
)
_OptionalDashboardSearchFilterTypeDef = TypedDict(
    "_OptionalDashboardSearchFilterTypeDef",
    {
        "Name": Literal["QUICKSIGHT_USER"],
        "Value": str,
    },
    total=False,
)

class DashboardSearchFilterTypeDef(
    _RequiredDashboardSearchFilterTypeDef, _OptionalDashboardSearchFilterTypeDef
):
    pass

DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "Arn": str,
        "DashboardId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PublishedVersionNumber": int,
        "LastPublishedTime": datetime,
    },
    total=False,
)

DashboardVersionSummaryTypeDef = TypedDict(
    "DashboardVersionSummaryTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "VersionNumber": int,
        "Status": ResourceStatusType,
        "SourceEntityArn": str,
        "Description": str,
    },
    total=False,
)

DataColorPaletteTypeDef = TypedDict(
    "DataColorPaletteTypeDef",
    {
        "Colors": Sequence[str],
        "MinMaxGradient": Sequence[str],
        "EmptyFillColor": str,
    },
    total=False,
)

OutputColumnTypeDef = TypedDict(
    "OutputColumnTypeDef",
    {
        "Name": str,
        "Description": str,
        "Type": ColumnDataTypeType,
    },
    total=False,
)

DataSourceErrorInfoTypeDef = TypedDict(
    "DataSourceErrorInfoTypeDef",
    {
        "Type": DataSourceErrorInfoTypeType,
        "Message": str,
    },
    total=False,
)

ExasolParametersTypeDef = TypedDict(
    "ExasolParametersTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)

JiraParametersTypeDef = TypedDict(
    "JiraParametersTypeDef",
    {
        "SiteBaseUrl": str,
    },
)

MariaDbParametersTypeDef = TypedDict(
    "MariaDbParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

MySqlParametersTypeDef = TypedDict(
    "MySqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

OracleParametersTypeDef = TypedDict(
    "OracleParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

PostgreSqlParametersTypeDef = TypedDict(
    "PostgreSqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

PrestoParametersTypeDef = TypedDict(
    "PrestoParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Catalog": str,
    },
)

RdsParametersTypeDef = TypedDict(
    "RdsParametersTypeDef",
    {
        "InstanceId": str,
        "Database": str,
    },
)

_RequiredRedshiftParametersTypeDef = TypedDict(
    "_RequiredRedshiftParametersTypeDef",
    {
        "Database": str,
    },
)
_OptionalRedshiftParametersTypeDef = TypedDict(
    "_OptionalRedshiftParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "ClusterId": str,
    },
    total=False,
)

class RedshiftParametersTypeDef(
    _RequiredRedshiftParametersTypeDef, _OptionalRedshiftParametersTypeDef
):
    pass

ServiceNowParametersTypeDef = TypedDict(
    "ServiceNowParametersTypeDef",
    {
        "SiteBaseUrl": str,
    },
)

SnowflakeParametersTypeDef = TypedDict(
    "SnowflakeParametersTypeDef",
    {
        "Host": str,
        "Database": str,
        "Warehouse": str,
    },
)

SparkParametersTypeDef = TypedDict(
    "SparkParametersTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)

SqlServerParametersTypeDef = TypedDict(
    "SqlServerParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

TeradataParametersTypeDef = TypedDict(
    "TeradataParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

TwitterParametersTypeDef = TypedDict(
    "TwitterParametersTypeDef",
    {
        "Query": str,
        "MaxRows": int,
    },
)

DateTimeParameterTypeDef = TypedDict(
    "DateTimeParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[Union[datetime, str]],
    },
)

DecimalParameterTypeDef = TypedDict(
    "DecimalParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[float],
    },
)

_RequiredDeleteAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalDeleteAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
    },
    total=False,
)

class DeleteAccountCustomizationRequestRequestTypeDef(
    _RequiredDeleteAccountCustomizationRequestRequestTypeDef,
    _OptionalDeleteAccountCustomizationRequestRequestTypeDef,
):
    pass

_RequiredDeleteAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)
_OptionalDeleteAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAnalysisRequestRequestTypeDef",
    {
        "RecoveryWindowInDays": int,
        "ForceDeleteWithoutRecovery": bool,
    },
    total=False,
)

class DeleteAnalysisRequestRequestTypeDef(
    _RequiredDeleteAnalysisRequestRequestTypeDef, _OptionalDeleteAnalysisRequestRequestTypeDef
):
    pass

_RequiredDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDashboardRequestRequestTypeDef",
    {
        "VersionNumber": int,
    },
    total=False,
)

class DeleteDashboardRequestRequestTypeDef(
    _RequiredDeleteDashboardRequestRequestTypeDef, _OptionalDeleteDashboardRequestRequestTypeDef
):
    pass

DeleteDataSetRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DeleteFolderMembershipRequestRequestTypeDef = TypedDict(
    "DeleteFolderMembershipRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
)

DeleteFolderRequestRequestTypeDef = TypedDict(
    "DeleteFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DeleteGroupMembershipRequestRequestTypeDef = TypedDict(
    "DeleteGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)

DeleteNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteTemplateAliasRequestRequestTypeDef = TypedDict(
    "DeleteTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
    },
)

_RequiredDeleteTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalDeleteTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTemplateRequestRequestTypeDef",
    {
        "VersionNumber": int,
    },
    total=False,
)

class DeleteTemplateRequestRequestTypeDef(
    _RequiredDeleteTemplateRequestRequestTypeDef, _OptionalDeleteTemplateRequestRequestTypeDef
):
    pass

DeleteThemeAliasRequestRequestTypeDef = TypedDict(
    "DeleteThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
    },
)

_RequiredDeleteThemeRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalDeleteThemeRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteThemeRequestRequestTypeDef",
    {
        "VersionNumber": int,
    },
    total=False,
)

class DeleteThemeRequestRequestTypeDef(
    _RequiredDeleteThemeRequestRequestTypeDef, _OptionalDeleteThemeRequestRequestTypeDef
):
    pass

DeleteUserByPrincipalIdRequestRequestTypeDef = TypedDict(
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    {
        "PrincipalId": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

_RequiredDescribeAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalDescribeAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
        "Resolved": bool,
    },
    total=False,
)

class DescribeAccountCustomizationRequestRequestTypeDef(
    _RequiredDescribeAccountCustomizationRequestRequestTypeDef,
    _OptionalDescribeAccountCustomizationRequestRequestTypeDef,
):
    pass

DescribeAccountSettingsRequestRequestTypeDef = TypedDict(
    "DescribeAccountSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)

_RequiredDescribeDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalDescribeDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDashboardRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)

class DescribeDashboardRequestRequestTypeDef(
    _RequiredDescribeDashboardRequestRequestTypeDef, _OptionalDescribeDashboardRequestRequestTypeDef
):
    pass

DescribeDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSetRequestRequestTypeDef = TypedDict(
    "DescribeDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DescribeDataSourceRequestRequestTypeDef = TypedDict(
    "DescribeDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DescribeFolderPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeFolderPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DescribeFolderRequestRequestTypeDef = TypedDict(
    "DescribeFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DescribeFolderResolvedPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

FolderTypeDef = TypedDict(
    "FolderTypeDef",
    {
        "FolderId": str,
        "Arn": str,
        "Name": str,
        "FolderType": Literal["SHARED"],
        "FolderPath": List[str],
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

DescribeGroupMembershipRequestRequestTypeDef = TypedDict(
    "DescribeGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeGroupRequestRequestTypeDef = TypedDict(
    "DescribeGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)

IAMPolicyAssignmentTypeDef = TypedDict(
    "IAMPolicyAssignmentTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentId": str,
        "AssignmentName": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": AssignmentStatusType,
    },
    total=False,
)

DescribeIngestionRequestRequestTypeDef = TypedDict(
    "DescribeIngestionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "IngestionId": str,
    },
)

DescribeIpRestrictionRequestRequestTypeDef = TypedDict(
    "DescribeIpRestrictionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeTemplateAliasRequestRequestTypeDef = TypedDict(
    "DescribeTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
    },
)

DescribeTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)

_RequiredDescribeTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalDescribeTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTemplateRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)

class DescribeTemplateRequestRequestTypeDef(
    _RequiredDescribeTemplateRequestRequestTypeDef, _OptionalDescribeTemplateRequestRequestTypeDef
):
    pass

DescribeThemeAliasRequestRequestTypeDef = TypedDict(
    "DescribeThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
    },
)

DescribeThemePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeThemePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)

_RequiredDescribeThemeRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalDescribeThemeRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeThemeRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)

class DescribeThemeRequestRequestTypeDef(
    _RequiredDescribeThemeRequestRequestTypeDef, _OptionalDescribeThemeRequestRequestTypeDef
):
    pass

DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": UserRoleType,
        "IdentityType": IdentityTypeType,
        "Active": bool,
        "PrincipalId": str,
        "CustomPermissionsName": str,
        "ExternalLoginFederationProviderType": str,
        "ExternalLoginFederationProviderUrl": str,
        "ExternalLoginId": str,
    },
    total=False,
)

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "Type": IngestionErrorTypeType,
        "Message": str,
    },
    total=False,
)

FilterOperationTypeDef = TypedDict(
    "FilterOperationTypeDef",
    {
        "ConditionExpression": str,
    },
)

FolderSearchFilterTypeDef = TypedDict(
    "FolderSearchFilterTypeDef",
    {
        "Operator": Literal["StringEquals"],
        "Name": Literal["PARENT_FOLDER_ARN"],
        "Value": str,
    },
    total=False,
)

FolderSummaryTypeDef = TypedDict(
    "FolderSummaryTypeDef",
    {
        "Arn": str,
        "FolderId": str,
        "Name": str,
        "FolderType": Literal["SHARED"],
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

SessionTagTypeDef = TypedDict(
    "SessionTagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredGetDashboardEmbedUrlRequestRequestTypeDef = TypedDict(
    "_RequiredGetDashboardEmbedUrlRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "IdentityType": EmbeddingIdentityTypeType,
    },
)
_OptionalGetDashboardEmbedUrlRequestRequestTypeDef = TypedDict(
    "_OptionalGetDashboardEmbedUrlRequestRequestTypeDef",
    {
        "SessionLifetimeInMinutes": int,
        "UndoRedoDisabled": bool,
        "ResetDisabled": bool,
        "StatePersistenceEnabled": bool,
        "UserArn": str,
        "Namespace": str,
        "AdditionalDashboardIds": Sequence[str],
    },
    total=False,
)

class GetDashboardEmbedUrlRequestRequestTypeDef(
    _RequiredGetDashboardEmbedUrlRequestRequestTypeDef,
    _OptionalGetDashboardEmbedUrlRequestRequestTypeDef,
):
    pass

_RequiredGetSessionEmbedUrlRequestRequestTypeDef = TypedDict(
    "_RequiredGetSessionEmbedUrlRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalGetSessionEmbedUrlRequestRequestTypeDef = TypedDict(
    "_OptionalGetSessionEmbedUrlRequestRequestTypeDef",
    {
        "EntryPoint": str,
        "SessionLifetimeInMinutes": int,
        "UserArn": str,
    },
    total=False,
)

class GetSessionEmbedUrlRequestRequestTypeDef(
    _RequiredGetSessionEmbedUrlRequestRequestTypeDef,
    _OptionalGetSessionEmbedUrlRequestRequestTypeDef,
):
    pass

GroupSearchFilterTypeDef = TypedDict(
    "GroupSearchFilterTypeDef",
    {
        "Operator": Literal["StartsWith"],
        "Name": Literal["GROUP_NAME"],
        "Value": str,
    },
)

GutterStyleTypeDef = TypedDict(
    "GutterStyleTypeDef",
    {
        "Show": bool,
    },
    total=False,
)

IAMPolicyAssignmentSummaryTypeDef = TypedDict(
    "IAMPolicyAssignmentSummaryTypeDef",
    {
        "AssignmentName": str,
        "AssignmentStatus": AssignmentStatusType,
    },
    total=False,
)

QueueInfoTypeDef = TypedDict(
    "QueueInfoTypeDef",
    {
        "WaitingOnIngestion": str,
        "QueuedIngestion": str,
    },
)

RowInfoTypeDef = TypedDict(
    "RowInfoTypeDef",
    {
        "RowsIngested": int,
        "RowsDropped": int,
        "TotalRowsInDataset": int,
    },
    total=False,
)

IntegerParameterTypeDef = TypedDict(
    "IntegerParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[int],
    },
)

JoinKeyPropertiesTypeDef = TypedDict(
    "JoinKeyPropertiesTypeDef",
    {
        "UniqueKey": bool,
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

_RequiredListAnalysesRequestRequestTypeDef = TypedDict(
    "_RequiredListAnalysesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListAnalysesRequestRequestTypeDef = TypedDict(
    "_OptionalListAnalysesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListAnalysesRequestRequestTypeDef(
    _RequiredListAnalysesRequestRequestTypeDef, _OptionalListAnalysesRequestRequestTypeDef
):
    pass

_RequiredListDashboardVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDashboardVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalListDashboardVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDashboardVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListDashboardVersionsRequestRequestTypeDef(
    _RequiredListDashboardVersionsRequestRequestTypeDef,
    _OptionalListDashboardVersionsRequestRequestTypeDef,
):
    pass

_RequiredListDashboardsRequestRequestTypeDef = TypedDict(
    "_RequiredListDashboardsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDashboardsRequestRequestTypeDef = TypedDict(
    "_OptionalListDashboardsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListDashboardsRequestRequestTypeDef(
    _RequiredListDashboardsRequestRequestTypeDef, _OptionalListDashboardsRequestRequestTypeDef
):
    pass

_RequiredListDataSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSetsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListDataSetsRequestRequestTypeDef(
    _RequiredListDataSetsRequestRequestTypeDef, _OptionalListDataSetsRequestRequestTypeDef
):
    pass

_RequiredListDataSourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSourcesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSourcesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListDataSourcesRequestRequestTypeDef(
    _RequiredListDataSourcesRequestRequestTypeDef, _OptionalListDataSourcesRequestRequestTypeDef
):
    pass

_RequiredListFolderMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListFolderMembersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)
_OptionalListFolderMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListFolderMembersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListFolderMembersRequestRequestTypeDef(
    _RequiredListFolderMembersRequestRequestTypeDef, _OptionalListFolderMembersRequestRequestTypeDef
):
    pass

MemberIdArnPairTypeDef = TypedDict(
    "MemberIdArnPairTypeDef",
    {
        "MemberId": str,
        "MemberArn": str,
    },
    total=False,
)

_RequiredListFoldersRequestRequestTypeDef = TypedDict(
    "_RequiredListFoldersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListFoldersRequestRequestTypeDef = TypedDict(
    "_OptionalListFoldersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListFoldersRequestRequestTypeDef(
    _RequiredListFoldersRequestRequestTypeDef, _OptionalListFoldersRequestRequestTypeDef
):
    pass

_RequiredListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupMembershipsRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupMembershipsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListGroupMembershipsRequestRequestTypeDef(
    _RequiredListGroupMembershipsRequestRequestTypeDef,
    _OptionalListGroupMembershipsRequestRequestTypeDef,
):
    pass

_RequiredListGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListGroupsRequestRequestTypeDef(
    _RequiredListGroupsRequestRequestTypeDef, _OptionalListGroupsRequestRequestTypeDef
):
    pass

_RequiredListIAMPolicyAssignmentsForUserRequestRequestTypeDef = TypedDict(
    "_RequiredListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "UserName": str,
        "Namespace": str,
    },
)
_OptionalListIAMPolicyAssignmentsForUserRequestRequestTypeDef = TypedDict(
    "_OptionalListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListIAMPolicyAssignmentsForUserRequestRequestTypeDef(
    _RequiredListIAMPolicyAssignmentsForUserRequestRequestTypeDef,
    _OptionalListIAMPolicyAssignmentsForUserRequestRequestTypeDef,
):
    pass

_RequiredListIAMPolicyAssignmentsRequestRequestTypeDef = TypedDict(
    "_RequiredListIAMPolicyAssignmentsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListIAMPolicyAssignmentsRequestRequestTypeDef = TypedDict(
    "_OptionalListIAMPolicyAssignmentsRequestRequestTypeDef",
    {
        "AssignmentStatus": AssignmentStatusType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListIAMPolicyAssignmentsRequestRequestTypeDef(
    _RequiredListIAMPolicyAssignmentsRequestRequestTypeDef,
    _OptionalListIAMPolicyAssignmentsRequestRequestTypeDef,
):
    pass

_RequiredListIngestionsRequestRequestTypeDef = TypedDict(
    "_RequiredListIngestionsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
    },
)
_OptionalListIngestionsRequestRequestTypeDef = TypedDict(
    "_OptionalListIngestionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListIngestionsRequestRequestTypeDef(
    _RequiredListIngestionsRequestRequestTypeDef, _OptionalListIngestionsRequestRequestTypeDef
):
    pass

_RequiredListNamespacesRequestRequestTypeDef = TypedDict(
    "_RequiredListNamespacesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListNamespacesRequestRequestTypeDef = TypedDict(
    "_OptionalListNamespacesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListNamespacesRequestRequestTypeDef(
    _RequiredListNamespacesRequestRequestTypeDef, _OptionalListNamespacesRequestRequestTypeDef
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListTemplateAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateAliasesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateAliasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListTemplateAliasesRequestRequestTypeDef(
    _RequiredListTemplateAliasesRequestRequestTypeDef,
    _OptionalListTemplateAliasesRequestRequestTypeDef,
):
    pass

_RequiredListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListTemplateVersionsRequestRequestTypeDef(
    _RequiredListTemplateVersionsRequestRequestTypeDef,
    _OptionalListTemplateVersionsRequestRequestTypeDef,
):
    pass

TemplateVersionSummaryTypeDef = TypedDict(
    "TemplateVersionSummaryTypeDef",
    {
        "Arn": str,
        "VersionNumber": int,
        "CreatedTime": datetime,
        "Status": ResourceStatusType,
        "Description": str,
    },
    total=False,
)

_RequiredListTemplatesRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplatesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListTemplatesRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListTemplatesRequestRequestTypeDef(
    _RequiredListTemplatesRequestRequestTypeDef, _OptionalListTemplatesRequestRequestTypeDef
):
    pass

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "Arn": str,
        "TemplateId": str,
        "Name": str,
        "LatestVersionNumber": int,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredListThemeAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListThemeAliasesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalListThemeAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListThemeAliasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListThemeAliasesRequestRequestTypeDef(
    _RequiredListThemeAliasesRequestRequestTypeDef, _OptionalListThemeAliasesRequestRequestTypeDef
):
    pass

_RequiredListThemeVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListThemeVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalListThemeVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListThemeVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListThemeVersionsRequestRequestTypeDef(
    _RequiredListThemeVersionsRequestRequestTypeDef, _OptionalListThemeVersionsRequestRequestTypeDef
):
    pass

ThemeVersionSummaryTypeDef = TypedDict(
    "ThemeVersionSummaryTypeDef",
    {
        "VersionNumber": int,
        "Arn": str,
        "Description": str,
        "CreatedTime": datetime,
        "Status": ResourceStatusType,
    },
    total=False,
)

_RequiredListThemesRequestRequestTypeDef = TypedDict(
    "_RequiredListThemesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListThemesRequestRequestTypeDef = TypedDict(
    "_OptionalListThemesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Type": ThemeTypeType,
    },
    total=False,
)

class ListThemesRequestRequestTypeDef(
    _RequiredListThemesRequestRequestTypeDef, _OptionalListThemesRequestRequestTypeDef
):
    pass

ThemeSummaryTypeDef = TypedDict(
    "ThemeSummaryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ThemeId": str,
        "LatestVersionNumber": int,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredListUserGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListUserGroupsRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListUserGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListUserGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListUserGroupsRequestRequestTypeDef(
    _RequiredListUserGroupsRequestRequestTypeDef, _OptionalListUserGroupsRequestRequestTypeDef
):
    pass

_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass

ManifestFileLocationTypeDef = TypedDict(
    "ManifestFileLocationTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

MarginStyleTypeDef = TypedDict(
    "MarginStyleTypeDef",
    {
        "Show": bool,
    },
    total=False,
)

NamespaceErrorTypeDef = TypedDict(
    "NamespaceErrorTypeDef",
    {
        "Type": NamespaceErrorTypeType,
        "Message": str,
    },
    total=False,
)

StringParameterTypeDef = TypedDict(
    "StringParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

ProjectOperationTypeDef = TypedDict(
    "ProjectOperationTypeDef",
    {
        "ProjectedColumns": Sequence[str],
    },
)

_RequiredRegisterUserRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterUserRequestRequestTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "Email": str,
        "UserRole": UserRoleType,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalRegisterUserRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterUserRequestRequestTypeDef",
    {
        "IamArn": str,
        "SessionName": str,
        "UserName": str,
        "CustomPermissionsName": str,
        "ExternalLoginFederationProviderType": str,
        "CustomFederationProviderUrl": str,
        "ExternalLoginId": str,
    },
    total=False,
)

class RegisterUserRequestRequestTypeDef(
    _RequiredRegisterUserRequestRequestTypeDef, _OptionalRegisterUserRequestRequestTypeDef
):
    pass

RegisteredUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardId": str,
    },
)

RegisteredUserQSearchBarEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    {
        "InitialTopicId": str,
    },
    total=False,
)

RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    {
        "InitialPath": str,
    },
    total=False,
)

RenameColumnOperationTypeDef = TypedDict(
    "RenameColumnOperationTypeDef",
    {
        "ColumnName": str,
        "NewColumnName": str,
    },
)

RestoreAnalysisRequestRequestTypeDef = TypedDict(
    "RestoreAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

_RequiredRowLevelPermissionTagRuleTypeDef = TypedDict(
    "_RequiredRowLevelPermissionTagRuleTypeDef",
    {
        "TagKey": str,
        "ColumnName": str,
    },
)
_OptionalRowLevelPermissionTagRuleTypeDef = TypedDict(
    "_OptionalRowLevelPermissionTagRuleTypeDef",
    {
        "TagMultiValueDelimiter": str,
        "MatchAllValue": str,
    },
    total=False,
)

class RowLevelPermissionTagRuleTypeDef(
    _RequiredRowLevelPermissionTagRuleTypeDef, _OptionalRowLevelPermissionTagRuleTypeDef
):
    pass

UploadSettingsTypeDef = TypedDict(
    "UploadSettingsTypeDef",
    {
        "Format": FileFormatType,
        "StartFromRow": int,
        "ContainsHeader": bool,
        "TextQualifier": TextQualifierType,
        "Delimiter": str,
    },
    total=False,
)

TemplateErrorTypeDef = TypedDict(
    "TemplateErrorTypeDef",
    {
        "Type": TemplateErrorTypeType,
        "Message": str,
    },
    total=False,
)

TemplateSourceTemplateTypeDef = TypedDict(
    "TemplateSourceTemplateTypeDef",
    {
        "Arn": str,
    },
)

UIColorPaletteTypeDef = TypedDict(
    "UIColorPaletteTypeDef",
    {
        "PrimaryForeground": str,
        "PrimaryBackground": str,
        "SecondaryForeground": str,
        "SecondaryBackground": str,
        "Accent": str,
        "AccentForeground": str,
        "Danger": str,
        "DangerForeground": str,
        "Warning": str,
        "WarningForeground": str,
        "Success": str,
        "SuccessForeground": str,
        "Dimension": str,
        "DimensionForeground": str,
        "Measure": str,
        "MeasureForeground": str,
    },
    total=False,
)

ThemeErrorTypeDef = TypedDict(
    "ThemeErrorTypeDef",
    {
        "Type": Literal["INTERNAL_FAILURE"],
        "Message": str,
    },
    total=False,
)

UntagColumnOperationTypeDef = TypedDict(
    "UntagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "TagNames": Sequence[ColumnTagNameType],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccountSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DefaultNamespace": str,
    },
)
_OptionalUpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccountSettingsRequestRequestTypeDef",
    {
        "NotificationEmail": str,
    },
    total=False,
)

class UpdateAccountSettingsRequestRequestTypeDef(
    _RequiredUpdateAccountSettingsRequestRequestTypeDef,
    _OptionalUpdateAccountSettingsRequestRequestTypeDef,
):
    pass

UpdateDashboardPublishedVersionRequestRequestTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "VersionNumber": int,
    },
)

UpdateFolderRequestRequestTypeDef = TypedDict(
    "UpdateFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Name": str,
    },
)

_RequiredUpdateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalUpdateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGroupRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateGroupRequestRequestTypeDef(
    _RequiredUpdateGroupRequestRequestTypeDef, _OptionalUpdateGroupRequestRequestTypeDef
):
    pass

_RequiredUpdateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)
_OptionalUpdateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AssignmentStatus": AssignmentStatusType,
        "PolicyArn": str,
        "Identities": Mapping[str, Sequence[str]],
    },
    total=False,
)

class UpdateIAMPolicyAssignmentRequestRequestTypeDef(
    _RequiredUpdateIAMPolicyAssignmentRequestRequestTypeDef,
    _OptionalUpdateIAMPolicyAssignmentRequestRequestTypeDef,
):
    pass

_RequiredUpdateIpRestrictionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIpRestrictionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalUpdateIpRestrictionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIpRestrictionRequestRequestTypeDef",
    {
        "IpRestrictionRuleMap": Mapping[str, str],
        "Enabled": bool,
    },
    total=False,
)

class UpdateIpRestrictionRequestRequestTypeDef(
    _RequiredUpdateIpRestrictionRequestRequestTypeDef,
    _OptionalUpdateIpRestrictionRequestRequestTypeDef,
):
    pass

_RequiredUpdatePublicSharingSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePublicSharingSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalUpdatePublicSharingSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePublicSharingSettingsRequestRequestTypeDef",
    {
        "PublicSharingEnabled": bool,
    },
    total=False,
)

class UpdatePublicSharingSettingsRequestRequestTypeDef(
    _RequiredUpdatePublicSharingSettingsRequestRequestTypeDef,
    _OptionalUpdatePublicSharingSettingsRequestRequestTypeDef,
):
    pass

UpdateTemplateAliasRequestRequestTypeDef = TypedDict(
    "UpdateTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
        "TemplateVersionNumber": int,
    },
)

UpdateThemeAliasRequestRequestTypeDef = TypedDict(
    "UpdateThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
)

_RequiredUpdateUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "Email": str,
        "Role": UserRoleType,
    },
)
_OptionalUpdateUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserRequestRequestTypeDef",
    {
        "CustomPermissionsName": str,
        "UnapplyCustomPermissions": bool,
        "ExternalLoginFederationProviderType": str,
        "CustomFederationProviderUrl": str,
        "ExternalLoginId": str,
    },
    total=False,
)

class UpdateUserRequestRequestTypeDef(
    _RequiredUpdateUserRequestRequestTypeDef, _OptionalUpdateUserRequestRequestTypeDef
):
    pass

_RequiredUpdateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AccountCustomization": AccountCustomizationTypeDef,
    },
)
_OptionalUpdateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
    },
    total=False,
)

class UpdateAccountCustomizationRequestRequestTypeDef(
    _RequiredUpdateAccountCustomizationRequestRequestTypeDef,
    _OptionalUpdateAccountCustomizationRequestRequestTypeDef,
):
    pass

_RequiredSearchAnalysesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchAnalysesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[AnalysisSearchFilterTypeDef],
    },
)
_OptionalSearchAnalysesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchAnalysesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class SearchAnalysesRequestRequestTypeDef(
    _RequiredSearchAnalysesRequestRequestTypeDef, _OptionalSearchAnalysesRequestRequestTypeDef
):
    pass

AnalysisSourceTemplateTypeDef = TypedDict(
    "AnalysisSourceTemplateTypeDef",
    {
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
        "Arn": str,
    },
)

DashboardSourceTemplateTypeDef = TypedDict(
    "DashboardSourceTemplateTypeDef",
    {
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
        "Arn": str,
    },
)

TemplateSourceAnalysisTypeDef = TypedDict(
    "TemplateSourceAnalysisTypeDef",
    {
        "Arn": str,
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
    },
)

AnalysisTypeDef = TypedDict(
    "AnalysisTypeDef",
    {
        "AnalysisId": str,
        "Arn": str,
        "Name": str,
        "Status": ResourceStatusType,
        "Errors": List[AnalysisErrorTypeDef],
        "DataSetArns": List[str],
        "ThemeArn": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "Sheets": List[SheetTypeDef],
    },
    total=False,
)

AnonymousUserEmbeddingExperienceConfigurationTypeDef = TypedDict(
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    {
        "Dashboard": AnonymousUserDashboardEmbeddingConfigurationTypeDef,
    },
    total=False,
)

TileStyleTypeDef = TypedDict(
    "TileStyleTypeDef",
    {
        "Border": BorderStyleTypeDef,
    },
    total=False,
)

CreateColumnsOperationTypeDef = TypedDict(
    "CreateColumnsOperationTypeDef",
    {
        "Columns": Sequence[CalculatedColumnTypeDef],
    },
)

CancelIngestionResponseTypeDef = TypedDict(
    "CancelIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccountCustomizationResponseTypeDef = TypedDict(
    "CreateAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAnalysisResponseTypeDef = TypedDict(
    "CreateAnalysisResponseTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "CreationStatus": ResourceStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFolderResponseTypeDef = TypedDict(
    "CreateFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "CreateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "AssignmentStatus": AssignmentStatusType,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIngestionResponseTypeDef = TypedDict(
    "CreateIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "IngestionStatus": IngestionStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNamespaceResponseTypeDef = TypedDict(
    "CreateNamespaceResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "CapacityRegion": str,
        "CreationStatus": NamespaceStatusType,
        "IdentityStore": Literal["QUICKSIGHT"],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateResponseTypeDef = TypedDict(
    "CreateTemplateResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "TemplateId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThemeResponseTypeDef = TypedDict(
    "CreateThemeResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "ThemeId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountCustomizationResponseTypeDef = TypedDict(
    "DeleteAccountCustomizationResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAnalysisResponseTypeDef = TypedDict(
    "DeleteAnalysisResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "AnalysisId": str,
        "DeletionTime": datetime,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDashboardResponseTypeDef = TypedDict(
    "DeleteDashboardResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "DashboardId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSetResponseTypeDef = TypedDict(
    "DeleteDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSourceResponseTypeDef = TypedDict(
    "DeleteDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFolderMembershipResponseTypeDef = TypedDict(
    "DeleteFolderMembershipResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFolderResponseTypeDef = TypedDict(
    "DeleteFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGroupMembershipResponseTypeDef = TypedDict(
    "DeleteGroupMembershipResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGroupResponseTypeDef = TypedDict(
    "DeleteGroupResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteNamespaceResponseTypeDef = TypedDict(
    "DeleteNamespaceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateAliasResponseTypeDef = TypedDict(
    "DeleteTemplateAliasResponseTypeDef",
    {
        "Status": int,
        "TemplateId": str,
        "AliasName": str,
        "Arn": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateResponseTypeDef = TypedDict(
    "DeleteTemplateResponseTypeDef",
    {
        "RequestId": str,
        "Arn": str,
        "TemplateId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteThemeAliasResponseTypeDef = TypedDict(
    "DeleteThemeAliasResponseTypeDef",
    {
        "AliasName": str,
        "Arn": str,
        "RequestId": str,
        "Status": int,
        "ThemeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteThemeResponseTypeDef = TypedDict(
    "DeleteThemeResponseTypeDef",
    {
        "Arn": str,
        "RequestId": str,
        "Status": int,
        "ThemeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserByPrincipalIdResponseTypeDef = TypedDict(
    "DeleteUserByPrincipalIdResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserResponseTypeDef = TypedDict(
    "DeleteUserResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountCustomizationResponseTypeDef = TypedDict(
    "DescribeAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountSettingsResponseTypeDef = TypedDict(
    "DescribeAccountSettingsResponseTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIpRestrictionResponseTypeDef = TypedDict(
    "DescribeIpRestrictionResponseTypeDef",
    {
        "AwsAccountId": str,
        "IpRestrictionRuleMap": Dict[str, str],
        "Enabled": bool,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForAnonymousUserResponseTypeDef = TypedDict(
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForRegisteredUserResponseTypeDef = TypedDict(
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDashboardEmbedUrlResponseTypeDef = TypedDict(
    "GetDashboardEmbedUrlResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionEmbedUrlResponseTypeDef = TypedDict(
    "GetSessionEmbedUrlResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnalysesResponseTypeDef = TypedDict(
    "ListAnalysesResponseTypeDef",
    {
        "AnalysisSummaryList": List[AnalysisSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIAMPolicyAssignmentsForUserResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    {
        "ActiveAssignments": List[ActiveIAMPolicyAssignmentTypeDef],
        "RequestId": str,
        "NextToken": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreAnalysisResponseTypeDef = TypedDict(
    "RestoreAnalysisResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "AnalysisId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAnalysesResponseTypeDef = TypedDict(
    "SearchAnalysesResponseTypeDef",
    {
        "AnalysisSummaryList": List[AnalysisSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceResponseTypeDef = TypedDict(
    "TagResourceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceResponseTypeDef = TypedDict(
    "UntagResourceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountCustomizationResponseTypeDef = TypedDict(
    "UpdateAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountSettingsResponseTypeDef = TypedDict(
    "UpdateAccountSettingsResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnalysisResponseTypeDef = TypedDict(
    "UpdateAnalysisResponseTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "UpdateStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPublishedVersionResponseTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardResponseTypeDef = TypedDict(
    "UpdateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetPermissionsResponseTypeDef = TypedDict(
    "UpdateDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourcePermissionsResponseTypeDef = TypedDict(
    "UpdateDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "UpdateStatus": ResourceStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFolderResponseTypeDef = TypedDict(
    "UpdateFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": AssignmentStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIpRestrictionResponseTypeDef = TypedDict(
    "UpdateIpRestrictionResponseTypeDef",
    {
        "AwsAccountId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePublicSharingSettingsResponseTypeDef = TypedDict(
    "UpdatePublicSharingSettingsResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateResponseTypeDef = TypedDict(
    "UpdateTemplateResponseTypeDef",
    {
        "TemplateId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeResponseTypeDef = TypedDict(
    "UpdateThemeResponseTypeDef",
    {
        "ThemeId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ColumnTagTypeDef = TypedDict(
    "ColumnTagTypeDef",
    {
        "ColumnGeographicRole": GeoSpatialDataRoleType,
        "ColumnDescription": ColumnDescriptionTypeDef,
    },
    total=False,
)

ColumnGroupSchemaTypeDef = TypedDict(
    "ColumnGroupSchemaTypeDef",
    {
        "Name": str,
        "ColumnGroupColumnSchemaList": List[ColumnGroupColumnSchemaTypeDef],
    },
    total=False,
)

ColumnGroupTypeDef = TypedDict(
    "ColumnGroupTypeDef",
    {
        "GeoSpatialColumnGroup": GeoSpatialColumnGroupTypeDef,
    },
    total=False,
)

DataSetSchemaTypeDef = TypedDict(
    "DataSetSchemaTypeDef",
    {
        "ColumnSchemaList": List[ColumnSchemaTypeDef],
    },
    total=False,
)

_RequiredCreateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AccountCustomization": AccountCustomizationTypeDef,
    },
)
_OptionalCreateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateAccountCustomizationRequestRequestTypeDef(
    _RequiredCreateAccountCustomizationRequestRequestTypeDef,
    _OptionalCreateAccountCustomizationRequestRequestTypeDef,
):
    pass

_RequiredCreateNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "IdentityStore": Literal["QUICKSIGHT"],
    },
)
_OptionalCreateNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNamespaceRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateNamespaceRequestRequestTypeDef(
    _RequiredCreateNamespaceRequestRequestTypeDef, _OptionalCreateNamespaceRequestRequestTypeDef
):
    pass

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateFolderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)
_OptionalCreateFolderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFolderRequestRequestTypeDef",
    {
        "Name": str,
        "FolderType": Literal["SHARED"],
        "ParentFolderArn": str,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateFolderRequestRequestTypeDef(
    _RequiredCreateFolderRequestRequestTypeDef, _OptionalCreateFolderRequestRequestTypeDef
):
    pass

DescribeAnalysisPermissionsResponseTypeDef = TypedDict(
    "DescribeAnalysisPermissionsResponseTypeDef",
    {
        "AnalysisId": str,
        "AnalysisArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSetPermissionsResponseTypeDef = TypedDict(
    "DescribeDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSourcePermissionsResponseTypeDef = TypedDict(
    "DescribeDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderPermissionsResponseTypeDef = TypedDict(
    "DescribeFolderPermissionsResponseTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderResolvedPermissionsResponseTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTemplatePermissionsResponseTypeDef = TypedDict(
    "DescribeTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemePermissionsResponseTypeDef = TypedDict(
    "DescribeThemePermissionsResponseTypeDef",
    {
        "ThemeId": str,
        "ThemeArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LinkSharingConfigurationTypeDef = TypedDict(
    "LinkSharingConfigurationTypeDef",
    {
        "Permissions": List[ResourcePermissionTypeDef],
    },
    total=False,
)

_RequiredUpdateAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnalysisPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)
_OptionalUpdateAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnalysisPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateAnalysisPermissionsRequestRequestTypeDef(
    _RequiredUpdateAnalysisPermissionsRequestRequestTypeDef,
    _OptionalUpdateAnalysisPermissionsRequestRequestTypeDef,
):
    pass

UpdateAnalysisPermissionsResponseTypeDef = TypedDict(
    "UpdateAnalysisPermissionsResponseTypeDef",
    {
        "AnalysisArn": str,
        "AnalysisId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDashboardPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalUpdateDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDashboardPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
        "GrantLinkPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokeLinkPermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateDashboardPermissionsRequestRequestTypeDef(
    _RequiredUpdateDashboardPermissionsRequestRequestTypeDef,
    _OptionalUpdateDashboardPermissionsRequestRequestTypeDef,
):
    pass

_RequiredUpdateDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSetPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)
_OptionalUpdateDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSetPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateDataSetPermissionsRequestRequestTypeDef(
    _RequiredUpdateDataSetPermissionsRequestRequestTypeDef,
    _OptionalUpdateDataSetPermissionsRequestRequestTypeDef,
):
    pass

_RequiredUpdateDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSourcePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)
_OptionalUpdateDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSourcePermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateDataSourcePermissionsRequestRequestTypeDef(
    _RequiredUpdateDataSourcePermissionsRequestRequestTypeDef,
    _OptionalUpdateDataSourcePermissionsRequestRequestTypeDef,
):
    pass

_RequiredUpdateFolderPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFolderPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)
_OptionalUpdateFolderPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFolderPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateFolderPermissionsRequestRequestTypeDef(
    _RequiredUpdateFolderPermissionsRequestRequestTypeDef,
    _OptionalUpdateFolderPermissionsRequestRequestTypeDef,
):
    pass

UpdateFolderPermissionsResponseTypeDef = TypedDict(
    "UpdateFolderPermissionsResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplatePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalUpdateTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplatePermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateTemplatePermissionsRequestRequestTypeDef(
    _RequiredUpdateTemplatePermissionsRequestRequestTypeDef,
    _OptionalUpdateTemplatePermissionsRequestRequestTypeDef,
):
    pass

UpdateTemplatePermissionsResponseTypeDef = TypedDict(
    "UpdateTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateThemePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThemePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalUpdateThemePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThemePermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)

class UpdateThemePermissionsRequestRequestTypeDef(
    _RequiredUpdateThemePermissionsRequestRequestTypeDef,
    _OptionalUpdateThemePermissionsRequestRequestTypeDef,
):
    pass

UpdateThemePermissionsResponseTypeDef = TypedDict(
    "UpdateThemePermissionsResponseTypeDef",
    {
        "ThemeId": str,
        "ThemeArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataSetSummaryTypeDef = TypedDict(
    "DataSetSummaryTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "ImportMode": DataSetImportModeType,
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfigurationApplied": bool,
        "ColumnLevelPermissionRulesApplied": bool,
    },
    total=False,
)

CreateFolderMembershipResponseTypeDef = TypedDict(
    "CreateFolderMembershipResponseTypeDef",
    {
        "Status": int,
        "FolderMember": FolderMemberTypeDef,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupMembershipResponseTypeDef = TypedDict(
    "CreateGroupMembershipResponseTypeDef",
    {
        "GroupMember": GroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupMembershipResponseTypeDef = TypedDict(
    "DescribeGroupMembershipResponseTypeDef",
    {
        "GroupMember": GroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupMembershipsResponseTypeDef = TypedDict(
    "ListGroupMembershipsResponseTypeDef",
    {
        "GroupMemberList": List[GroupMemberTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserGroupsResponseTypeDef = TypedDict(
    "ListUserGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchGroupsResponseTypeDef = TypedDict(
    "SearchGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGroupResponseTypeDef = TypedDict(
    "UpdateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateAliasResponseTypeDef = TypedDict(
    "CreateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTemplateAliasResponseTypeDef = TypedDict(
    "DescribeTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateAliasesResponseTypeDef = TypedDict(
    "ListTemplateAliasesResponseTypeDef",
    {
        "TemplateAliasList": List[TemplateAliasTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateAliasResponseTypeDef = TypedDict(
    "UpdateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThemeAliasResponseTypeDef = TypedDict(
    "CreateThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemeAliasResponseTypeDef = TypedDict(
    "DescribeThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemeAliasesResponseTypeDef = TypedDict(
    "ListThemeAliasesResponseTypeDef",
    {
        "ThemeAliasList": List[ThemeAliasTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeAliasResponseTypeDef = TypedDict(
    "UpdateThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCustomSqlTypeDef = TypedDict(
    "_RequiredCustomSqlTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "SqlQuery": str,
    },
)
_OptionalCustomSqlTypeDef = TypedDict(
    "_OptionalCustomSqlTypeDef",
    {
        "Columns": Sequence[InputColumnTypeDef],
    },
    total=False,
)

class CustomSqlTypeDef(_RequiredCustomSqlTypeDef, _OptionalCustomSqlTypeDef):
    pass

_RequiredRelationalTableTypeDef = TypedDict(
    "_RequiredRelationalTableTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "InputColumns": Sequence[InputColumnTypeDef],
    },
)
_OptionalRelationalTableTypeDef = TypedDict(
    "_OptionalRelationalTableTypeDef",
    {
        "Catalog": str,
        "Schema": str,
    },
    total=False,
)

class RelationalTableTypeDef(_RequiredRelationalTableTypeDef, _OptionalRelationalTableTypeDef):
    pass

DashboardVersionTypeDef = TypedDict(
    "DashboardVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List[DashboardErrorTypeDef],
        "VersionNumber": int,
        "Status": ResourceStatusType,
        "Arn": str,
        "SourceEntityArn": str,
        "DataSetArns": List[str],
        "Description": str,
        "ThemeArn": str,
        "Sheets": List[SheetTypeDef],
    },
    total=False,
)

DashboardPublishOptionsTypeDef = TypedDict(
    "DashboardPublishOptionsTypeDef",
    {
        "AdHocFilteringOption": AdHocFilteringOptionTypeDef,
        "ExportToCSVOption": ExportToCSVOptionTypeDef,
        "SheetControlsOption": SheetControlsOptionTypeDef,
    },
    total=False,
)

_RequiredSearchDashboardsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchDashboardsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DashboardSearchFilterTypeDef],
    },
)
_OptionalSearchDashboardsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchDashboardsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class SearchDashboardsRequestRequestTypeDef(
    _RequiredSearchDashboardsRequestRequestTypeDef, _OptionalSearchDashboardsRequestRequestTypeDef
):
    pass

ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[DashboardSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchDashboardsResponseTypeDef = TypedDict(
    "SearchDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[DashboardSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDashboardVersionsResponseTypeDef = TypedDict(
    "ListDashboardVersionsResponseTypeDef",
    {
        "DashboardVersionSummaryList": List[DashboardVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderResponseTypeDef = TypedDict(
    "DescribeFolderResponseTypeDef",
    {
        "Status": int,
        "Folder": FolderTypeDef,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    {
        "IAMPolicyAssignment": IAMPolicyAssignmentTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "UserList": List[UserTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterUserResponseTypeDef = TypedDict(
    "RegisterUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "UserInvitationUrl": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSearchFoldersRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFoldersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[FolderSearchFilterTypeDef],
    },
)
_OptionalSearchFoldersRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFoldersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class SearchFoldersRequestRequestTypeDef(
    _RequiredSearchFoldersRequestRequestTypeDef, _OptionalSearchFoldersRequestRequestTypeDef
):
    pass

ListFoldersResponseTypeDef = TypedDict(
    "ListFoldersResponseTypeDef",
    {
        "Status": int,
        "FolderSummaryList": List[FolderSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchFoldersResponseTypeDef = TypedDict(
    "SearchFoldersResponseTypeDef",
    {
        "Status": int,
        "FolderSummaryList": List[FolderSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSearchGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchGroupsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "Filters": Sequence[GroupSearchFilterTypeDef],
    },
)
_OptionalSearchGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class SearchGroupsRequestRequestTypeDef(
    _RequiredSearchGroupsRequestRequestTypeDef, _OptionalSearchGroupsRequestRequestTypeDef
):
    pass

ListIAMPolicyAssignmentsResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsResponseTypeDef",
    {
        "IAMPolicyAssignments": List[IAMPolicyAssignmentSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredIngestionTypeDef = TypedDict(
    "_RequiredIngestionTypeDef",
    {
        "Arn": str,
        "IngestionStatus": IngestionStatusType,
        "CreatedTime": datetime,
    },
)
_OptionalIngestionTypeDef = TypedDict(
    "_OptionalIngestionTypeDef",
    {
        "IngestionId": str,
        "ErrorInfo": ErrorInfoTypeDef,
        "RowInfo": RowInfoTypeDef,
        "QueueInfo": QueueInfoTypeDef,
        "IngestionTimeInSeconds": int,
        "IngestionSizeInBytes": int,
        "RequestSource": IngestionRequestSourceType,
        "RequestType": IngestionRequestTypeType,
    },
    total=False,
)

class IngestionTypeDef(_RequiredIngestionTypeDef, _OptionalIngestionTypeDef):
    pass

_RequiredJoinInstructionTypeDef = TypedDict(
    "_RequiredJoinInstructionTypeDef",
    {
        "LeftOperand": str,
        "RightOperand": str,
        "Type": JoinTypeType,
        "OnClause": str,
    },
)
_OptionalJoinInstructionTypeDef = TypedDict(
    "_OptionalJoinInstructionTypeDef",
    {
        "LeftJoinKeyProperties": JoinKeyPropertiesTypeDef,
        "RightJoinKeyProperties": JoinKeyPropertiesTypeDef,
    },
    total=False,
)

class JoinInstructionTypeDef(_RequiredJoinInstructionTypeDef, _OptionalJoinInstructionTypeDef):
    pass

_RequiredListAnalysesRequestListAnalysesPaginateTypeDef = TypedDict(
    "_RequiredListAnalysesRequestListAnalysesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListAnalysesRequestListAnalysesPaginateTypeDef = TypedDict(
    "_OptionalListAnalysesRequestListAnalysesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAnalysesRequestListAnalysesPaginateTypeDef(
    _RequiredListAnalysesRequestListAnalysesPaginateTypeDef,
    _OptionalListAnalysesRequestListAnalysesPaginateTypeDef,
):
    pass

_RequiredListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef = TypedDict(
    "_RequiredListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef = TypedDict(
    "_OptionalListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef(
    _RequiredListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef,
    _OptionalListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef,
):
    pass

_RequiredListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_RequiredListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_OptionalListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDashboardsRequestListDashboardsPaginateTypeDef(
    _RequiredListDashboardsRequestListDashboardsPaginateTypeDef,
    _OptionalListDashboardsRequestListDashboardsPaginateTypeDef,
):
    pass

_RequiredListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "_RequiredListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "_OptionalListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDataSetsRequestListDataSetsPaginateTypeDef(
    _RequiredListDataSetsRequestListDataSetsPaginateTypeDef,
    _OptionalListDataSetsRequestListDataSetsPaginateTypeDef,
):
    pass

_RequiredListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "_RequiredListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "_OptionalListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDataSourcesRequestListDataSourcesPaginateTypeDef(
    _RequiredListDataSourcesRequestListDataSourcesPaginateTypeDef,
    _OptionalListDataSourcesRequestListDataSourcesPaginateTypeDef,
):
    pass

_RequiredListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "_RequiredListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
    },
)
_OptionalListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "_OptionalListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListIngestionsRequestListIngestionsPaginateTypeDef(
    _RequiredListIngestionsRequestListIngestionsPaginateTypeDef,
    _OptionalListIngestionsRequestListIngestionsPaginateTypeDef,
):
    pass

_RequiredListNamespacesRequestListNamespacesPaginateTypeDef = TypedDict(
    "_RequiredListNamespacesRequestListNamespacesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListNamespacesRequestListNamespacesPaginateTypeDef = TypedDict(
    "_OptionalListNamespacesRequestListNamespacesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListNamespacesRequestListNamespacesPaginateTypeDef(
    _RequiredListNamespacesRequestListNamespacesPaginateTypeDef,
    _OptionalListNamespacesRequestListNamespacesPaginateTypeDef,
):
    pass

_RequiredListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef = TypedDict(
    "_RequiredListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef = TypedDict(
    "_OptionalListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef(
    _RequiredListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef,
    _OptionalListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef,
):
    pass

_RequiredListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef(
    _RequiredListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef,
    _OptionalListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef,
):
    pass

_RequiredListTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "_RequiredListTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "_OptionalListTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTemplatesRequestListTemplatesPaginateTypeDef(
    _RequiredListTemplatesRequestListTemplatesPaginateTypeDef,
    _OptionalListTemplatesRequestListTemplatesPaginateTypeDef,
):
    pass

_RequiredListThemeVersionsRequestListThemeVersionsPaginateTypeDef = TypedDict(
    "_RequiredListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalListThemeVersionsRequestListThemeVersionsPaginateTypeDef = TypedDict(
    "_OptionalListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListThemeVersionsRequestListThemeVersionsPaginateTypeDef(
    _RequiredListThemeVersionsRequestListThemeVersionsPaginateTypeDef,
    _OptionalListThemeVersionsRequestListThemeVersionsPaginateTypeDef,
):
    pass

_RequiredListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "_RequiredListThemesRequestListThemesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "_OptionalListThemesRequestListThemesPaginateTypeDef",
    {
        "Type": ThemeTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListThemesRequestListThemesPaginateTypeDef(
    _RequiredListThemesRequestListThemesPaginateTypeDef,
    _OptionalListThemesRequestListThemesPaginateTypeDef,
):
    pass

_RequiredSearchAnalysesRequestSearchAnalysesPaginateTypeDef = TypedDict(
    "_RequiredSearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[AnalysisSearchFilterTypeDef],
    },
)
_OptionalSearchAnalysesRequestSearchAnalysesPaginateTypeDef = TypedDict(
    "_OptionalSearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchAnalysesRequestSearchAnalysesPaginateTypeDef(
    _RequiredSearchAnalysesRequestSearchAnalysesPaginateTypeDef,
    _OptionalSearchAnalysesRequestSearchAnalysesPaginateTypeDef,
):
    pass

_RequiredSearchDashboardsRequestSearchDashboardsPaginateTypeDef = TypedDict(
    "_RequiredSearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DashboardSearchFilterTypeDef],
    },
)
_OptionalSearchDashboardsRequestSearchDashboardsPaginateTypeDef = TypedDict(
    "_OptionalSearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchDashboardsRequestSearchDashboardsPaginateTypeDef(
    _RequiredSearchDashboardsRequestSearchDashboardsPaginateTypeDef,
    _OptionalSearchDashboardsRequestSearchDashboardsPaginateTypeDef,
):
    pass

ListFolderMembersResponseTypeDef = TypedDict(
    "ListFolderMembersResponseTypeDef",
    {
        "Status": int,
        "FolderMemberList": List[MemberIdArnPairTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateVersionsResponseTypeDef = TypedDict(
    "ListTemplateVersionsResponseTypeDef",
    {
        "TemplateVersionSummaryList": List[TemplateVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "TemplateSummaryList": List[TemplateSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemeVersionsResponseTypeDef = TypedDict(
    "ListThemeVersionsResponseTypeDef",
    {
        "ThemeVersionSummaryList": List[ThemeVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemesResponseTypeDef = TypedDict(
    "ListThemesResponseTypeDef",
    {
        "ThemeSummaryList": List[ThemeSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3ParametersTypeDef = TypedDict(
    "S3ParametersTypeDef",
    {
        "ManifestFileLocation": ManifestFileLocationTypeDef,
    },
)

TileLayoutStyleTypeDef = TypedDict(
    "TileLayoutStyleTypeDef",
    {
        "Gutter": GutterStyleTypeDef,
        "Margin": MarginStyleTypeDef,
    },
    total=False,
)

NamespaceInfoV2TypeDef = TypedDict(
    "NamespaceInfoV2TypeDef",
    {
        "Name": str,
        "Arn": str,
        "CapacityRegion": str,
        "CreationStatus": NamespaceStatusType,
        "IdentityStore": Literal["QUICKSIGHT"],
        "NamespaceError": NamespaceErrorTypeDef,
    },
    total=False,
)

ParametersTypeDef = TypedDict(
    "ParametersTypeDef",
    {
        "StringParameters": Sequence[StringParameterTypeDef],
        "IntegerParameters": Sequence[IntegerParameterTypeDef],
        "DecimalParameters": Sequence[DecimalParameterTypeDef],
        "DateTimeParameters": Sequence[DateTimeParameterTypeDef],
    },
    total=False,
)

RegisteredUserEmbeddingExperienceConfigurationTypeDef = TypedDict(
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    {
        "Dashboard": RegisteredUserDashboardEmbeddingConfigurationTypeDef,
        "QuickSightConsole": RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef,
        "QSearchBar": RegisteredUserQSearchBarEmbeddingConfigurationTypeDef,
    },
    total=False,
)

_RequiredRowLevelPermissionTagConfigurationTypeDef = TypedDict(
    "_RequiredRowLevelPermissionTagConfigurationTypeDef",
    {
        "TagRules": Sequence[RowLevelPermissionTagRuleTypeDef],
    },
)
_OptionalRowLevelPermissionTagConfigurationTypeDef = TypedDict(
    "_OptionalRowLevelPermissionTagConfigurationTypeDef",
    {
        "Status": StatusType,
    },
    total=False,
)

class RowLevelPermissionTagConfigurationTypeDef(
    _RequiredRowLevelPermissionTagConfigurationTypeDef,
    _OptionalRowLevelPermissionTagConfigurationTypeDef,
):
    pass

_RequiredS3SourceTypeDef = TypedDict(
    "_RequiredS3SourceTypeDef",
    {
        "DataSourceArn": str,
        "InputColumns": Sequence[InputColumnTypeDef],
    },
)
_OptionalS3SourceTypeDef = TypedDict(
    "_OptionalS3SourceTypeDef",
    {
        "UploadSettings": UploadSettingsTypeDef,
    },
    total=False,
)

class S3SourceTypeDef(_RequiredS3SourceTypeDef, _OptionalS3SourceTypeDef):
    pass

AnalysisSourceEntityTypeDef = TypedDict(
    "AnalysisSourceEntityTypeDef",
    {
        "SourceTemplate": AnalysisSourceTemplateTypeDef,
    },
    total=False,
)

DashboardSourceEntityTypeDef = TypedDict(
    "DashboardSourceEntityTypeDef",
    {
        "SourceTemplate": DashboardSourceTemplateTypeDef,
    },
    total=False,
)

TemplateSourceEntityTypeDef = TypedDict(
    "TemplateSourceEntityTypeDef",
    {
        "SourceAnalysis": TemplateSourceAnalysisTypeDef,
        "SourceTemplate": TemplateSourceTemplateTypeDef,
    },
    total=False,
)

DescribeAnalysisResponseTypeDef = TypedDict(
    "DescribeAnalysisResponseTypeDef",
    {
        "Analysis": AnalysisTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "AuthorizedResourceArns": Sequence[str],
        "ExperienceConfiguration": AnonymousUserEmbeddingExperienceConfigurationTypeDef,
    },
)
_OptionalGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    {
        "SessionLifetimeInMinutes": int,
        "SessionTags": Sequence[SessionTagTypeDef],
    },
    total=False,
)

class GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef(
    _RequiredGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef,
    _OptionalGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef,
):
    pass

TagColumnOperationTypeDef = TypedDict(
    "TagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "Tags": Sequence[ColumnTagTypeDef],
    },
)

DataSetConfigurationTypeDef = TypedDict(
    "DataSetConfigurationTypeDef",
    {
        "Placeholder": str,
        "DataSetSchema": DataSetSchemaTypeDef,
        "ColumnGroupSchemaList": List[ColumnGroupSchemaTypeDef],
    },
    total=False,
)

DescribeDashboardPermissionsResponseTypeDef = TypedDict(
    "DescribeDashboardPermissionsResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "LinkSharingConfiguration": LinkSharingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPermissionsResponseTypeDef = TypedDict(
    "UpdateDashboardPermissionsResponseTypeDef",
    {
        "DashboardArn": str,
        "DashboardId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "LinkSharingConfiguration": LinkSharingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List[DataSetSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DashboardTypeDef = TypedDict(
    "DashboardTypeDef",
    {
        "DashboardId": str,
        "Arn": str,
        "Name": str,
        "Version": DashboardVersionTypeDef,
        "CreatedTime": datetime,
        "LastPublishedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

DescribeIngestionResponseTypeDef = TypedDict(
    "DescribeIngestionResponseTypeDef",
    {
        "Ingestion": IngestionTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIngestionsResponseTypeDef = TypedDict(
    "ListIngestionsResponseTypeDef",
    {
        "Ingestions": List[IngestionTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LogicalTableSourceTypeDef = TypedDict(
    "LogicalTableSourceTypeDef",
    {
        "JoinInstruction": JoinInstructionTypeDef,
        "PhysicalTableId": str,
        "DataSetArn": str,
    },
    total=False,
)

DataSourceParametersTypeDef = TypedDict(
    "DataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": AmazonElasticsearchParametersTypeDef,
        "AthenaParameters": AthenaParametersTypeDef,
        "AuroraParameters": AuroraParametersTypeDef,
        "AuroraPostgreSqlParameters": AuroraPostgreSqlParametersTypeDef,
        "AwsIotAnalyticsParameters": AwsIotAnalyticsParametersTypeDef,
        "JiraParameters": JiraParametersTypeDef,
        "MariaDbParameters": MariaDbParametersTypeDef,
        "MySqlParameters": MySqlParametersTypeDef,
        "OracleParameters": OracleParametersTypeDef,
        "PostgreSqlParameters": PostgreSqlParametersTypeDef,
        "PrestoParameters": PrestoParametersTypeDef,
        "RdsParameters": RdsParametersTypeDef,
        "RedshiftParameters": RedshiftParametersTypeDef,
        "S3Parameters": S3ParametersTypeDef,
        "ServiceNowParameters": ServiceNowParametersTypeDef,
        "SnowflakeParameters": SnowflakeParametersTypeDef,
        "SparkParameters": SparkParametersTypeDef,
        "SqlServerParameters": SqlServerParametersTypeDef,
        "TeradataParameters": TeradataParametersTypeDef,
        "TwitterParameters": TwitterParametersTypeDef,
        "AmazonOpenSearchParameters": AmazonOpenSearchParametersTypeDef,
        "ExasolParameters": ExasolParametersTypeDef,
    },
    total=False,
)

SheetStyleTypeDef = TypedDict(
    "SheetStyleTypeDef",
    {
        "Tile": TileStyleTypeDef,
        "TileLayout": TileLayoutStyleTypeDef,
    },
    total=False,
)

DescribeNamespaceResponseTypeDef = TypedDict(
    "DescribeNamespaceResponseTypeDef",
    {
        "Namespace": NamespaceInfoV2TypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNamespacesResponseTypeDef = TypedDict(
    "ListNamespacesResponseTypeDef",
    {
        "Namespaces": List[NamespaceInfoV2TypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "UserArn": str,
        "ExperienceConfiguration": RegisteredUserEmbeddingExperienceConfigurationTypeDef,
    },
)
_OptionalGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    {
        "SessionLifetimeInMinutes": int,
    },
    total=False,
)

class GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef(
    _RequiredGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef,
    _OptionalGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef,
):
    pass

PhysicalTableTypeDef = TypedDict(
    "PhysicalTableTypeDef",
    {
        "RelationalTable": RelationalTableTypeDef,
        "CustomSql": CustomSqlTypeDef,
        "S3Source": S3SourceTypeDef,
    },
    total=False,
)

_RequiredCreateAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "Name": str,
        "SourceEntity": AnalysisSourceEntityTypeDef,
    },
)
_OptionalCreateAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAnalysisRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "ThemeArn": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateAnalysisRequestRequestTypeDef(
    _RequiredCreateAnalysisRequestRequestTypeDef, _OptionalCreateAnalysisRequestRequestTypeDef
):
    pass

_RequiredUpdateAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "Name": str,
        "SourceEntity": AnalysisSourceEntityTypeDef,
    },
)
_OptionalUpdateAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnalysisRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "ThemeArn": str,
    },
    total=False,
)

class UpdateAnalysisRequestRequestTypeDef(
    _RequiredUpdateAnalysisRequestRequestTypeDef, _OptionalUpdateAnalysisRequestRequestTypeDef
):
    pass

_RequiredCreateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "Name": str,
        "SourceEntity": DashboardSourceEntityTypeDef,
    },
)
_OptionalCreateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDashboardRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "Tags": Sequence[TagTypeDef],
        "VersionDescription": str,
        "DashboardPublishOptions": DashboardPublishOptionsTypeDef,
        "ThemeArn": str,
    },
    total=False,
)

class CreateDashboardRequestRequestTypeDef(
    _RequiredCreateDashboardRequestRequestTypeDef, _OptionalCreateDashboardRequestRequestTypeDef
):
    pass

_RequiredUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "Name": str,
        "SourceEntity": DashboardSourceEntityTypeDef,
    },
)
_OptionalUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDashboardRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "VersionDescription": str,
        "DashboardPublishOptions": DashboardPublishOptionsTypeDef,
        "ThemeArn": str,
    },
    total=False,
)

class UpdateDashboardRequestRequestTypeDef(
    _RequiredUpdateDashboardRequestRequestTypeDef, _OptionalUpdateDashboardRequestRequestTypeDef
):
    pass

_RequiredCreateTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "SourceEntity": TemplateSourceEntityTypeDef,
    },
)
_OptionalCreateTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTemplateRequestRequestTypeDef",
    {
        "Name": str,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "Tags": Sequence[TagTypeDef],
        "VersionDescription": str,
    },
    total=False,
)

class CreateTemplateRequestRequestTypeDef(
    _RequiredCreateTemplateRequestRequestTypeDef, _OptionalCreateTemplateRequestRequestTypeDef
):
    pass

_RequiredUpdateTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "SourceEntity": TemplateSourceEntityTypeDef,
    },
)
_OptionalUpdateTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplateRequestRequestTypeDef",
    {
        "VersionDescription": str,
        "Name": str,
    },
    total=False,
)

class UpdateTemplateRequestRequestTypeDef(
    _RequiredUpdateTemplateRequestRequestTypeDef, _OptionalUpdateTemplateRequestRequestTypeDef
):
    pass

TransformOperationTypeDef = TypedDict(
    "TransformOperationTypeDef",
    {
        "ProjectOperation": ProjectOperationTypeDef,
        "FilterOperation": FilterOperationTypeDef,
        "CreateColumnsOperation": CreateColumnsOperationTypeDef,
        "RenameColumnOperation": RenameColumnOperationTypeDef,
        "CastColumnTypeOperation": CastColumnTypeOperationTypeDef,
        "TagColumnOperation": TagColumnOperationTypeDef,
        "UntagColumnOperation": UntagColumnOperationTypeDef,
    },
    total=False,
)

TemplateVersionTypeDef = TypedDict(
    "TemplateVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List[TemplateErrorTypeDef],
        "VersionNumber": int,
        "Status": ResourceStatusType,
        "DataSetConfigurations": List[DataSetConfigurationTypeDef],
        "Description": str,
        "SourceEntityArn": str,
        "ThemeArn": str,
        "Sheets": List[SheetTypeDef],
    },
    total=False,
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {
        "Dashboard": DashboardTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCredentialPairTypeDef = TypedDict(
    "_RequiredCredentialPairTypeDef",
    {
        "Username": str,
        "Password": str,
    },
)
_OptionalCredentialPairTypeDef = TypedDict(
    "_OptionalCredentialPairTypeDef",
    {
        "AlternateDataSourceParameters": Sequence[DataSourceParametersTypeDef],
    },
    total=False,
)

class CredentialPairTypeDef(_RequiredCredentialPairTypeDef, _OptionalCredentialPairTypeDef):
    pass

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "Status": ResourceStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "DataSourceParameters": DataSourceParametersTypeDef,
        "AlternateDataSourceParameters": List[DataSourceParametersTypeDef],
        "VpcConnectionProperties": VpcConnectionPropertiesTypeDef,
        "SslProperties": SslPropertiesTypeDef,
        "ErrorInfo": DataSourceErrorInfoTypeDef,
    },
    total=False,
)

ThemeConfigurationTypeDef = TypedDict(
    "ThemeConfigurationTypeDef",
    {
        "DataColorPalette": DataColorPaletteTypeDef,
        "UIColorPalette": UIColorPaletteTypeDef,
        "Sheet": SheetStyleTypeDef,
    },
    total=False,
)

_RequiredLogicalTableTypeDef = TypedDict(
    "_RequiredLogicalTableTypeDef",
    {
        "Alias": str,
        "Source": LogicalTableSourceTypeDef,
    },
)
_OptionalLogicalTableTypeDef = TypedDict(
    "_OptionalLogicalTableTypeDef",
    {
        "DataTransforms": Sequence[TransformOperationTypeDef],
    },
    total=False,
)

class LogicalTableTypeDef(_RequiredLogicalTableTypeDef, _OptionalLogicalTableTypeDef):
    pass

TemplateTypeDef = TypedDict(
    "TemplateTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Version": TemplateVersionTypeDef,
        "TemplateId": str,
        "LastUpdatedTime": datetime,
        "CreatedTime": datetime,
    },
    total=False,
)

DataSourceCredentialsTypeDef = TypedDict(
    "DataSourceCredentialsTypeDef",
    {
        "CredentialPair": CredentialPairTypeDef,
        "CopySourceArn": str,
    },
    total=False,
)

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "DataSources": List[DataSourceTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateThemeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "Name": str,
        "BaseThemeId": str,
        "Configuration": ThemeConfigurationTypeDef,
    },
)
_OptionalCreateThemeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateThemeRequestRequestTypeDef",
    {
        "VersionDescription": str,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateThemeRequestRequestTypeDef(
    _RequiredCreateThemeRequestRequestTypeDef, _OptionalCreateThemeRequestRequestTypeDef
):
    pass

ThemeVersionTypeDef = TypedDict(
    "ThemeVersionTypeDef",
    {
        "VersionNumber": int,
        "Arn": str,
        "Description": str,
        "BaseThemeId": str,
        "CreatedTime": datetime,
        "Configuration": ThemeConfigurationTypeDef,
        "Errors": List[ThemeErrorTypeDef],
        "Status": ResourceStatusType,
    },
    total=False,
)

_RequiredUpdateThemeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "BaseThemeId": str,
    },
)
_OptionalUpdateThemeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThemeRequestRequestTypeDef",
    {
        "Name": str,
        "VersionDescription": str,
        "Configuration": ThemeConfigurationTypeDef,
    },
    total=False,
)

class UpdateThemeRequestRequestTypeDef(
    _RequiredUpdateThemeRequestRequestTypeDef, _OptionalUpdateThemeRequestRequestTypeDef
):
    pass

_RequiredCreateDataSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "Name": str,
        "PhysicalTableMap": Mapping[str, PhysicalTableTypeDef],
        "ImportMode": DataSetImportModeType,
    },
)
_OptionalCreateDataSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSetRequestRequestTypeDef",
    {
        "LogicalTableMap": Mapping[str, LogicalTableTypeDef],
        "ColumnGroups": Sequence[ColumnGroupTypeDef],
        "FieldFolders": Mapping[str, FieldFolderTypeDef],
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfiguration": RowLevelPermissionTagConfigurationTypeDef,
        "ColumnLevelPermissionRules": Sequence[ColumnLevelPermissionRuleTypeDef],
        "Tags": Sequence[TagTypeDef],
        "DataSetUsageConfiguration": DataSetUsageConfigurationTypeDef,
    },
    total=False,
)

class CreateDataSetRequestRequestTypeDef(
    _RequiredCreateDataSetRequestRequestTypeDef, _OptionalCreateDataSetRequestRequestTypeDef
):
    pass

DataSetTypeDef = TypedDict(
    "DataSetTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PhysicalTableMap": Dict[str, PhysicalTableTypeDef],
        "LogicalTableMap": Dict[str, LogicalTableTypeDef],
        "OutputColumns": List[OutputColumnTypeDef],
        "ImportMode": DataSetImportModeType,
        "ConsumedSpiceCapacityInBytes": int,
        "ColumnGroups": List[ColumnGroupTypeDef],
        "FieldFolders": Dict[str, FieldFolderTypeDef],
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfiguration": RowLevelPermissionTagConfigurationTypeDef,
        "ColumnLevelPermissionRules": List[ColumnLevelPermissionRuleTypeDef],
        "DataSetUsageConfiguration": DataSetUsageConfigurationTypeDef,
    },
    total=False,
)

_RequiredUpdateDataSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "Name": str,
        "PhysicalTableMap": Mapping[str, PhysicalTableTypeDef],
        "ImportMode": DataSetImportModeType,
    },
)
_OptionalUpdateDataSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSetRequestRequestTypeDef",
    {
        "LogicalTableMap": Mapping[str, LogicalTableTypeDef],
        "ColumnGroups": Sequence[ColumnGroupTypeDef],
        "FieldFolders": Mapping[str, FieldFolderTypeDef],
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfiguration": RowLevelPermissionTagConfigurationTypeDef,
        "ColumnLevelPermissionRules": Sequence[ColumnLevelPermissionRuleTypeDef],
        "DataSetUsageConfiguration": DataSetUsageConfigurationTypeDef,
    },
    total=False,
)

class UpdateDataSetRequestRequestTypeDef(
    _RequiredUpdateDataSetRequestRequestTypeDef, _OptionalUpdateDataSetRequestRequestTypeDef
):
    pass

DescribeTemplateResponseTypeDef = TypedDict(
    "DescribeTemplateResponseTypeDef",
    {
        "Template": TemplateTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
    },
)
_OptionalCreateDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSourceRequestRequestTypeDef",
    {
        "DataSourceParameters": DataSourceParametersTypeDef,
        "Credentials": DataSourceCredentialsTypeDef,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "VpcConnectionProperties": VpcConnectionPropertiesTypeDef,
        "SslProperties": SslPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDataSourceRequestRequestTypeDef(
    _RequiredCreateDataSourceRequestRequestTypeDef, _OptionalCreateDataSourceRequestRequestTypeDef
):
    pass

_RequiredUpdateDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
    },
)
_OptionalUpdateDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSourceRequestRequestTypeDef",
    {
        "DataSourceParameters": DataSourceParametersTypeDef,
        "Credentials": DataSourceCredentialsTypeDef,
        "VpcConnectionProperties": VpcConnectionPropertiesTypeDef,
        "SslProperties": SslPropertiesTypeDef,
    },
    total=False,
)

class UpdateDataSourceRequestRequestTypeDef(
    _RequiredUpdateDataSourceRequestRequestTypeDef, _OptionalUpdateDataSourceRequestRequestTypeDef
):
    pass

ThemeTypeDef = TypedDict(
    "ThemeTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ThemeId": str,
        "Version": ThemeVersionTypeDef,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "Type": ThemeTypeType,
    },
    total=False,
)

DescribeDataSetResponseTypeDef = TypedDict(
    "DescribeDataSetResponseTypeDef",
    {
        "DataSet": DataSetTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemeResponseTypeDef = TypedDict(
    "DescribeThemeResponseTypeDef",
    {
        "Theme": ThemeTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
