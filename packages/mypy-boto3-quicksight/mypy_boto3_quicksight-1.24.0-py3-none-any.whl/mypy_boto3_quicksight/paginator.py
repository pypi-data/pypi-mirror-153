"""
Type annotations for quicksight service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_quicksight.client import QuickSightClient
    from mypy_boto3_quicksight.paginator import (
        ListAnalysesPaginator,
        ListDashboardVersionsPaginator,
        ListDashboardsPaginator,
        ListDataSetsPaginator,
        ListDataSourcesPaginator,
        ListIngestionsPaginator,
        ListNamespacesPaginator,
        ListTemplateAliasesPaginator,
        ListTemplateVersionsPaginator,
        ListTemplatesPaginator,
        ListThemeVersionsPaginator,
        ListThemesPaginator,
        SearchAnalysesPaginator,
        SearchDashboardsPaginator,
    )

    session = Session()
    client: QuickSightClient = session.client("quicksight")

    list_analyses_paginator: ListAnalysesPaginator = client.get_paginator("list_analyses")
    list_dashboard_versions_paginator: ListDashboardVersionsPaginator = client.get_paginator("list_dashboard_versions")
    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_template_aliases_paginator: ListTemplateAliasesPaginator = client.get_paginator("list_template_aliases")
    list_template_versions_paginator: ListTemplateVersionsPaginator = client.get_paginator("list_template_versions")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    list_theme_versions_paginator: ListThemeVersionsPaginator = client.get_paginator("list_theme_versions")
    list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    search_analyses_paginator: SearchAnalysesPaginator = client.get_paginator("search_analyses")
    search_dashboards_paginator: SearchDashboardsPaginator = client.get_paginator("search_dashboards")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ThemeTypeType
from .type_defs import (
    AnalysisSearchFilterTypeDef,
    DashboardSearchFilterTypeDef,
    ListAnalysesResponseTypeDef,
    ListDashboardsResponseTypeDef,
    ListDashboardVersionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListIngestionsResponseTypeDef,
    ListNamespacesResponseTypeDef,
    ListTemplateAliasesResponseTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsResponseTypeDef,
    ListThemesResponseTypeDef,
    ListThemeVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
    SearchAnalysesResponseTypeDef,
    SearchDashboardsResponseTypeDef,
)

__all__ = (
    "ListAnalysesPaginator",
    "ListDashboardVersionsPaginator",
    "ListDashboardsPaginator",
    "ListDataSetsPaginator",
    "ListDataSourcesPaginator",
    "ListIngestionsPaginator",
    "ListNamespacesPaginator",
    "ListTemplateAliasesPaginator",
    "ListTemplateVersionsPaginator",
    "ListTemplatesPaginator",
    "ListThemeVersionsPaginator",
    "ListThemesPaginator",
    "SearchAnalysesPaginator",
    "SearchDashboardsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAnalysesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListAnalyses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listanalysespaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListAnalyses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listanalysespaginator)
        """


class ListDashboardVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDashboardVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdashboardversionspaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, DashboardId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDashboardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDashboardVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdashboardversionspaginator)
        """


class ListDashboardsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDashboards)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdashboardspaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDashboards.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdashboardspaginator)
        """


class ListDataSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDataSets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDataSets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdatasetspaginator)
        """


class ListDataSourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDataSources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdatasourcespaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListDataSources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listdatasourcespaginator)
        """


class ListIngestionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListIngestions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listingestionspaginator)
    """

    def paginate(
        self, *, DataSetId: str, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIngestionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListIngestions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listingestionspaginator)
        """


class ListNamespacesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListNamespaces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listnamespacespaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListNamespaces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listnamespacespaginator)
        """


class ListTemplateAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListTemplateAliases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listtemplatealiasespaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, TemplateId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTemplateAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListTemplateAliases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listtemplatealiasespaginator)
        """


class ListTemplateVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListTemplateVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listtemplateversionspaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, TemplateId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListTemplateVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listtemplateversionspaginator)
        """


class ListTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listtemplatespaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listtemplatespaginator)
        """


class ListThemeVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListThemeVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listthemeversionspaginator)
    """

    def paginate(
        self, *, AwsAccountId: str, ThemeId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThemeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListThemeVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listthemeversionspaginator)
        """


class ListThemesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListThemes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listthemespaginator)
    """

    def paginate(
        self,
        *,
        AwsAccountId: str,
        Type: ThemeTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.ListThemes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#listthemespaginator)
        """


class SearchAnalysesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.SearchAnalyses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#searchanalysespaginator)
    """

    def paginate(
        self,
        *,
        AwsAccountId: str,
        Filters: Sequence[AnalysisSearchFilterTypeDef],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.SearchAnalyses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#searchanalysespaginator)
        """


class SearchDashboardsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.SearchDashboards)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#searchdashboardspaginator)
    """

    def paginate(
        self,
        *,
        AwsAccountId: str,
        Filters: Sequence[DashboardSearchFilterTypeDef],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Paginator.SearchDashboards.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/paginators/#searchdashboardspaginator)
        """
