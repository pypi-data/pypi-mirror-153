"""
Type annotations for servicecatalog service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_servicecatalog.client import ServiceCatalogClient
    from mypy_boto3_servicecatalog.paginator import (
        ListAcceptedPortfolioSharesPaginator,
        ListConstraintsForPortfolioPaginator,
        ListLaunchPathsPaginator,
        ListOrganizationPortfolioAccessPaginator,
        ListPortfoliosPaginator,
        ListPortfoliosForProductPaginator,
        ListPrincipalsForPortfolioPaginator,
        ListProvisionedProductPlansPaginator,
        ListProvisioningArtifactsForServiceActionPaginator,
        ListRecordHistoryPaginator,
        ListResourcesForTagOptionPaginator,
        ListServiceActionsPaginator,
        ListServiceActionsForProvisioningArtifactPaginator,
        ListTagOptionsPaginator,
        ScanProvisionedProductsPaginator,
        SearchProductsAsAdminPaginator,
    )

    session = Session()
    client: ServiceCatalogClient = session.client("servicecatalog")

    list_accepted_portfolio_shares_paginator: ListAcceptedPortfolioSharesPaginator = client.get_paginator("list_accepted_portfolio_shares")
    list_constraints_for_portfolio_paginator: ListConstraintsForPortfolioPaginator = client.get_paginator("list_constraints_for_portfolio")
    list_launch_paths_paginator: ListLaunchPathsPaginator = client.get_paginator("list_launch_paths")
    list_organization_portfolio_access_paginator: ListOrganizationPortfolioAccessPaginator = client.get_paginator("list_organization_portfolio_access")
    list_portfolios_paginator: ListPortfoliosPaginator = client.get_paginator("list_portfolios")
    list_portfolios_for_product_paginator: ListPortfoliosForProductPaginator = client.get_paginator("list_portfolios_for_product")
    list_principals_for_portfolio_paginator: ListPrincipalsForPortfolioPaginator = client.get_paginator("list_principals_for_portfolio")
    list_provisioned_product_plans_paginator: ListProvisionedProductPlansPaginator = client.get_paginator("list_provisioned_product_plans")
    list_provisioning_artifacts_for_service_action_paginator: ListProvisioningArtifactsForServiceActionPaginator = client.get_paginator("list_provisioning_artifacts_for_service_action")
    list_record_history_paginator: ListRecordHistoryPaginator = client.get_paginator("list_record_history")
    list_resources_for_tag_option_paginator: ListResourcesForTagOptionPaginator = client.get_paginator("list_resources_for_tag_option")
    list_service_actions_paginator: ListServiceActionsPaginator = client.get_paginator("list_service_actions")
    list_service_actions_for_provisioning_artifact_paginator: ListServiceActionsForProvisioningArtifactPaginator = client.get_paginator("list_service_actions_for_provisioning_artifact")
    list_tag_options_paginator: ListTagOptionsPaginator = client.get_paginator("list_tag_options")
    scan_provisioned_products_paginator: ScanProvisionedProductsPaginator = client.get_paginator("scan_provisioned_products")
    search_products_as_admin_paginator: SearchProductsAsAdminPaginator = client.get_paginator("search_products_as_admin")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    OrganizationNodeTypeType,
    PortfolioShareTypeType,
    ProductViewFilterByType,
    ProductViewSortByType,
    SortOrderType,
)
from .type_defs import (
    AccessLevelFilterTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListRecordHistorySearchFilterTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsOutputTypeDef,
    ListTagOptionsFiltersTypeDef,
    ListTagOptionsOutputTypeDef,
    PaginatorConfigTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAcceptedPortfolioSharesPaginator",
    "ListConstraintsForPortfolioPaginator",
    "ListLaunchPathsPaginator",
    "ListOrganizationPortfolioAccessPaginator",
    "ListPortfoliosPaginator",
    "ListPortfoliosForProductPaginator",
    "ListPrincipalsForPortfolioPaginator",
    "ListProvisionedProductPlansPaginator",
    "ListProvisioningArtifactsForServiceActionPaginator",
    "ListRecordHistoryPaginator",
    "ListResourcesForTagOptionPaginator",
    "ListServiceActionsPaginator",
    "ListServiceActionsForProvisioningArtifactPaginator",
    "ListTagOptionsPaginator",
    "ScanProvisionedProductsPaginator",
    "SearchProductsAsAdminPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAcceptedPortfolioSharesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        PortfolioShareType: PortfolioShareTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAcceptedPortfolioSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
        """


class ListConstraintsForPortfolioPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
    """

    def paginate(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        ProductId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListConstraintsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
        """


class ListLaunchPathsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListLaunchPaths)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listlaunchpathspaginator)
    """

    def paginate(
        self,
        *,
        ProductId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLaunchPathsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListLaunchPaths.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listlaunchpathspaginator)
        """


class ListOrganizationPortfolioAccessPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
    """

    def paginate(
        self,
        *,
        PortfolioId: str,
        OrganizationNodeType: OrganizationNodeTypeType,
        AcceptLanguage: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationPortfolioAccessOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
        """


class ListPortfoliosPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliospaginator)
    """

    def paginate(
        self, *, AcceptLanguage: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPortfoliosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliospaginator)
        """


class ListPortfoliosForProductPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfoliosForProduct)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliosforproductpaginator)
    """

    def paginate(
        self,
        *,
        ProductId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPortfoliosForProductOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfoliosForProduct.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliosforproductpaginator)
        """


class ListPrincipalsForPortfolioPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
    """

    def paginate(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPrincipalsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
        """


class ListProvisionedProductPlansPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisionedProductPlans)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisionedproductplanspaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        ProvisionProductId: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisionedProductPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisionedProductPlans.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisionedproductplanspaginator)
        """


class ListProvisioningArtifactsForServiceActionPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
    """

    def paginate(
        self,
        *,
        ServiceActionId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisioningArtifactsForServiceActionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
        """


class ListRecordHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListRecordHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listrecordhistorypaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...,
        SearchFilter: ListRecordHistorySearchFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecordHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListRecordHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listrecordhistorypaginator)
        """


class ListResourcesForTagOptionPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListResourcesForTagOption)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
    """

    def paginate(
        self,
        *,
        TagOptionId: str,
        ResourceType: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourcesForTagOptionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListResourcesForTagOption.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
        """


class ListServiceActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionspaginator)
    """

    def paginate(
        self, *, AcceptLanguage: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionspaginator)
        """


class ListServiceActionsForProvisioningArtifactPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
    """

    def paginate(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceActionsForProvisioningArtifactOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
        """


class ListTagOptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListTagOptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listtagoptionspaginator)
    """

    def paginate(
        self,
        *,
        Filters: ListTagOptionsFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListTagOptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listtagoptionspaginator)
        """


class ScanProvisionedProductsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ScanProvisionedProducts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#scanprovisionedproductspaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ScanProvisionedProductsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ScanProvisionedProducts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#scanprovisionedproductspaginator)
        """


class SearchProductsAsAdminPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.SearchProductsAsAdmin)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#searchproductsasadminpaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        PortfolioId: str = ...,
        Filters: Mapping[ProductViewFilterByType, Sequence[str]] = ...,
        SortBy: ProductViewSortByType = ...,
        SortOrder: SortOrderType = ...,
        ProductSource: Literal["ACCOUNT"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchProductsAsAdminOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.SearchProductsAsAdmin.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#searchproductsasadminpaginator)
        """
