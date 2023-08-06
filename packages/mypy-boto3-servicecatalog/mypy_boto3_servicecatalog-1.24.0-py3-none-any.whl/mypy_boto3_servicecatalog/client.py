"""
Type annotations for servicecatalog service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_servicecatalog.client import ServiceCatalogClient

    session = Session()
    client: ServiceCatalogClient = session.client("servicecatalog")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    DescribePortfolioShareTypeType,
    OrganizationNodeTypeType,
    PortfolioShareTypeType,
    ProductTypeType,
    ProductViewFilterByType,
    ProductViewSortByType,
    PropertyKeyType,
    ProvisioningArtifactGuidanceType,
    ServiceActionDefinitionKeyType,
    SortOrderType,
)
from .paginator import (
    ListAcceptedPortfolioSharesPaginator,
    ListConstraintsForPortfolioPaginator,
    ListLaunchPathsPaginator,
    ListOrganizationPortfolioAccessPaginator,
    ListPortfoliosForProductPaginator,
    ListPortfoliosPaginator,
    ListPrincipalsForPortfolioPaginator,
    ListProvisionedProductPlansPaginator,
    ListProvisioningArtifactsForServiceActionPaginator,
    ListRecordHistoryPaginator,
    ListResourcesForTagOptionPaginator,
    ListServiceActionsForProvisioningArtifactPaginator,
    ListServiceActionsPaginator,
    ListTagOptionsPaginator,
    ScanProvisionedProductsPaginator,
    SearchProductsAsAdminPaginator,
)
from .type_defs import (
    AccessLevelFilterTypeDef,
    BatchAssociateServiceActionWithProvisioningArtifactOutputTypeDef,
    BatchDisassociateServiceActionFromProvisioningArtifactOutputTypeDef,
    CopyProductOutputTypeDef,
    CreateConstraintOutputTypeDef,
    CreatePortfolioOutputTypeDef,
    CreatePortfolioShareOutputTypeDef,
    CreateProductOutputTypeDef,
    CreateProvisionedProductPlanOutputTypeDef,
    CreateProvisioningArtifactOutputTypeDef,
    CreateServiceActionOutputTypeDef,
    CreateTagOptionOutputTypeDef,
    DeletePortfolioShareOutputTypeDef,
    DescribeConstraintOutputTypeDef,
    DescribeCopyProductStatusOutputTypeDef,
    DescribePortfolioOutputTypeDef,
    DescribePortfolioSharesOutputTypeDef,
    DescribePortfolioShareStatusOutputTypeDef,
    DescribeProductAsAdminOutputTypeDef,
    DescribeProductOutputTypeDef,
    DescribeProductViewOutputTypeDef,
    DescribeProvisionedProductOutputTypeDef,
    DescribeProvisionedProductPlanOutputTypeDef,
    DescribeProvisioningArtifactOutputTypeDef,
    DescribeProvisioningParametersOutputTypeDef,
    DescribeRecordOutputTypeDef,
    DescribeServiceActionExecutionParametersOutputTypeDef,
    DescribeServiceActionOutputTypeDef,
    DescribeTagOptionOutputTypeDef,
    ExecuteProvisionedProductPlanOutputTypeDef,
    ExecuteProvisionedProductServiceActionOutputTypeDef,
    GetAWSOrganizationsAccessStatusOutputTypeDef,
    GetProvisionedProductOutputsOutputTypeDef,
    ImportAsProvisionedProductOutputTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListBudgetsForResourceOutputTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListProvisioningArtifactsOutputTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListRecordHistorySearchFilterTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsOutputTypeDef,
    ListStackInstancesForProvisionedProductOutputTypeDef,
    ListTagOptionsFiltersTypeDef,
    ListTagOptionsOutputTypeDef,
    OrganizationNodeTypeDef,
    ProvisioningArtifactPropertiesTypeDef,
    ProvisioningParameterTypeDef,
    ProvisioningPreferencesTypeDef,
    ProvisionProductOutputTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminOutputTypeDef,
    SearchProductsOutputTypeDef,
    SearchProvisionedProductsOutputTypeDef,
    ServiceActionAssociationTypeDef,
    TagTypeDef,
    TerminateProvisionedProductOutputTypeDef,
    UpdateConstraintOutputTypeDef,
    UpdatePortfolioOutputTypeDef,
    UpdatePortfolioShareOutputTypeDef,
    UpdateProductOutputTypeDef,
    UpdateProvisionedProductOutputTypeDef,
    UpdateProvisionedProductPropertiesOutputTypeDef,
    UpdateProvisioningArtifactOutputTypeDef,
    UpdateProvisioningParameterTypeDef,
    UpdateProvisioningPreferencesTypeDef,
    UpdateServiceActionOutputTypeDef,
    UpdateTagOptionOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ServiceCatalogClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DuplicateResourceException: Type[BotocoreClientError]
    InvalidParametersException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OperationNotSupportedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagOptionNotMigratedException: Type[BotocoreClientError]


class ServiceCatalogClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServiceCatalogClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#exceptions)
        """

    def accept_portfolio_share(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        PortfolioShareType: PortfolioShareTypeType = ...
    ) -> Dict[str, Any]:
        """
        Accepts an offer to share the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.accept_portfolio_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#accept_portfolio_share)
        """

    def associate_budget_with_resource(self, *, BudgetName: str, ResourceId: str) -> Dict[str, Any]:
        """
        Associates the specified budget with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.associate_budget_with_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_budget_with_resource)
        """

    def associate_principal_with_portfolio(
        self,
        *,
        PortfolioId: str,
        PrincipalARN: str,
        PrincipalType: Literal["IAM"],
        AcceptLanguage: str = ...
    ) -> Dict[str, Any]:
        """
        Associates the specified principal ARN with the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.associate_principal_with_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_principal_with_portfolio)
        """

    def associate_product_with_portfolio(
        self,
        *,
        ProductId: str,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        SourcePortfolioId: str = ...
    ) -> Dict[str, Any]:
        """
        Associates the specified product with the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.associate_product_with_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_product_with_portfolio)
        """

    def associate_service_action_with_provisioning_artifact(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        ServiceActionId: str,
        AcceptLanguage: str = ...
    ) -> Dict[str, Any]:
        """
        Associates a self-service action with a provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.associate_service_action_with_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_service_action_with_provisioning_artifact)
        """

    def associate_tag_option_with_resource(
        self, *, ResourceId: str, TagOptionId: str
    ) -> Dict[str, Any]:
        """
        Associate the specified TagOption with the specified portfolio or product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.associate_tag_option_with_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_tag_option_with_resource)
        """

    def batch_associate_service_action_with_provisioning_artifact(
        self,
        *,
        ServiceActionAssociations: Sequence[ServiceActionAssociationTypeDef],
        AcceptLanguage: str = ...
    ) -> BatchAssociateServiceActionWithProvisioningArtifactOutputTypeDef:
        """
        Associates multiple self-service actions with provisioning artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.batch_associate_service_action_with_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#batch_associate_service_action_with_provisioning_artifact)
        """

    def batch_disassociate_service_action_from_provisioning_artifact(
        self,
        *,
        ServiceActionAssociations: Sequence[ServiceActionAssociationTypeDef],
        AcceptLanguage: str = ...
    ) -> BatchDisassociateServiceActionFromProvisioningArtifactOutputTypeDef:
        """
        Disassociates a batch of self-service actions from the specified provisioning
        artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.batch_disassociate_service_action_from_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#batch_disassociate_service_action_from_provisioning_artifact)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#can_paginate)
        """

    def copy_product(
        self,
        *,
        SourceProductArn: str,
        IdempotencyToken: str,
        AcceptLanguage: str = ...,
        TargetProductId: str = ...,
        TargetProductName: str = ...,
        SourceProvisioningArtifactIdentifiers: Sequence[Mapping[Literal["Id"], str]] = ...,
        CopyOptions: Sequence[Literal["CopyTags"]] = ...
    ) -> CopyProductOutputTypeDef:
        """
        Copies the specified source product to the specified target product or a new
        product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.copy_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#copy_product)
        """

    def create_constraint(
        self,
        *,
        PortfolioId: str,
        ProductId: str,
        Parameters: str,
        Type: str,
        IdempotencyToken: str,
        AcceptLanguage: str = ...,
        Description: str = ...
    ) -> CreateConstraintOutputTypeDef:
        """
        Creates a constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_constraint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_constraint)
        """

    def create_portfolio(
        self,
        *,
        DisplayName: str,
        ProviderName: str,
        IdempotencyToken: str,
        AcceptLanguage: str = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreatePortfolioOutputTypeDef:
        """
        Creates a portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_portfolio)
        """

    def create_portfolio_share(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        AccountId: str = ...,
        OrganizationNode: OrganizationNodeTypeDef = ...,
        ShareTagOptions: bool = ...
    ) -> CreatePortfolioShareOutputTypeDef:
        """
        Shares the specified portfolio with the specified account or organization node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_portfolio_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_portfolio_share)
        """

    def create_product(
        self,
        *,
        Name: str,
        Owner: str,
        ProductType: ProductTypeType,
        ProvisioningArtifactParameters: ProvisioningArtifactPropertiesTypeDef,
        IdempotencyToken: str,
        AcceptLanguage: str = ...,
        Description: str = ...,
        Distributor: str = ...,
        SupportDescription: str = ...,
        SupportEmail: str = ...,
        SupportUrl: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateProductOutputTypeDef:
        """
        Creates a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_product)
        """

    def create_provisioned_product_plan(
        self,
        *,
        PlanName: str,
        PlanType: Literal["CLOUDFORMATION"],
        ProductId: str,
        ProvisionedProductName: str,
        ProvisioningArtifactId: str,
        IdempotencyToken: str,
        AcceptLanguage: str = ...,
        NotificationArns: Sequence[str] = ...,
        PathId: str = ...,
        ProvisioningParameters: Sequence[UpdateProvisioningParameterTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateProvisionedProductPlanOutputTypeDef:
        """
        Creates a plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_provisioned_product_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_provisioned_product_plan)
        """

    def create_provisioning_artifact(
        self,
        *,
        ProductId: str,
        Parameters: ProvisioningArtifactPropertiesTypeDef,
        IdempotencyToken: str,
        AcceptLanguage: str = ...
    ) -> CreateProvisioningArtifactOutputTypeDef:
        """
        Creates a provisioning artifact (also known as a version) for the specified
        product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_provisioning_artifact)
        """

    def create_service_action(
        self,
        *,
        Name: str,
        DefinitionType: Literal["SSM_AUTOMATION"],
        Definition: Mapping[ServiceActionDefinitionKeyType, str],
        IdempotencyToken: str,
        Description: str = ...,
        AcceptLanguage: str = ...
    ) -> CreateServiceActionOutputTypeDef:
        """
        Creates a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_service_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_service_action)
        """

    def create_tag_option(self, *, Key: str, Value: str) -> CreateTagOptionOutputTypeDef:
        """
        Creates a TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_tag_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_tag_option)
        """

    def delete_constraint(self, *, Id: str, AcceptLanguage: str = ...) -> Dict[str, Any]:
        """
        Deletes the specified constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_constraint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_constraint)
        """

    def delete_portfolio(self, *, Id: str, AcceptLanguage: str = ...) -> Dict[str, Any]:
        """
        Deletes the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_portfolio)
        """

    def delete_portfolio_share(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        AccountId: str = ...,
        OrganizationNode: OrganizationNodeTypeDef = ...
    ) -> DeletePortfolioShareOutputTypeDef:
        """
        Stops sharing the specified portfolio with the specified account or organization
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_portfolio_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_portfolio_share)
        """

    def delete_product(self, *, Id: str, AcceptLanguage: str = ...) -> Dict[str, Any]:
        """
        Deletes the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_product)
        """

    def delete_provisioned_product_plan(
        self, *, PlanId: str, AcceptLanguage: str = ..., IgnoreErrors: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes the specified plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_provisioned_product_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_provisioned_product_plan)
        """

    def delete_provisioning_artifact(
        self, *, ProductId: str, ProvisioningArtifactId: str, AcceptLanguage: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes the specified provisioning artifact (also known as a version) for the
        specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_provisioning_artifact)
        """

    def delete_service_action(self, *, Id: str, AcceptLanguage: str = ...) -> Dict[str, Any]:
        """
        Deletes a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_service_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_service_action)
        """

    def delete_tag_option(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_tag_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_tag_option)
        """

    def describe_constraint(
        self, *, Id: str, AcceptLanguage: str = ...
    ) -> DescribeConstraintOutputTypeDef:
        """
        Gets information about the specified constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_constraint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_constraint)
        """

    def describe_copy_product_status(
        self, *, CopyProductToken: str, AcceptLanguage: str = ...
    ) -> DescribeCopyProductStatusOutputTypeDef:
        """
        Gets the status of the specified copy product operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_copy_product_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_copy_product_status)
        """

    def describe_portfolio(
        self, *, Id: str, AcceptLanguage: str = ...
    ) -> DescribePortfolioOutputTypeDef:
        """
        Gets information about the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_portfolio)
        """

    def describe_portfolio_share_status(
        self, *, PortfolioShareToken: str
    ) -> DescribePortfolioShareStatusOutputTypeDef:
        """
        Gets the status of the specified portfolio share operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_portfolio_share_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_portfolio_share_status)
        """

    def describe_portfolio_shares(
        self,
        *,
        PortfolioId: str,
        Type: DescribePortfolioShareTypeType,
        PageToken: str = ...,
        PageSize: int = ...
    ) -> DescribePortfolioSharesOutputTypeDef:
        """
        Returns a summary of each of the portfolio shares that were created for the
        specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_portfolio_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_portfolio_shares)
        """

    def describe_product(
        self, *, AcceptLanguage: str = ..., Id: str = ..., Name: str = ...
    ) -> DescribeProductOutputTypeDef:
        """
        Gets information about the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_product)
        """

    def describe_product_as_admin(
        self,
        *,
        AcceptLanguage: str = ...,
        Id: str = ...,
        Name: str = ...,
        SourcePortfolioId: str = ...
    ) -> DescribeProductAsAdminOutputTypeDef:
        """
        Gets information about the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_product_as_admin)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_product_as_admin)
        """

    def describe_product_view(
        self, *, Id: str, AcceptLanguage: str = ...
    ) -> DescribeProductViewOutputTypeDef:
        """
        Gets information about the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_product_view)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_product_view)
        """

    def describe_provisioned_product(
        self, *, AcceptLanguage: str = ..., Id: str = ..., Name: str = ...
    ) -> DescribeProvisionedProductOutputTypeDef:
        """
        Gets information about the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_provisioned_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioned_product)
        """

    def describe_provisioned_product_plan(
        self, *, PlanId: str, AcceptLanguage: str = ..., PageSize: int = ..., PageToken: str = ...
    ) -> DescribeProvisionedProductPlanOutputTypeDef:
        """
        Gets information about the resource changes for the specified plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_provisioned_product_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioned_product_plan)
        """

    def describe_provisioning_artifact(
        self,
        *,
        AcceptLanguage: str = ...,
        ProvisioningArtifactId: str = ...,
        ProductId: str = ...,
        ProvisioningArtifactName: str = ...,
        ProductName: str = ...,
        Verbose: bool = ...
    ) -> DescribeProvisioningArtifactOutputTypeDef:
        """
        Gets information about the specified provisioning artifact (also known as a
        version) for the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioning_artifact)
        """

    def describe_provisioning_parameters(
        self,
        *,
        AcceptLanguage: str = ...,
        ProductId: str = ...,
        ProductName: str = ...,
        ProvisioningArtifactId: str = ...,
        ProvisioningArtifactName: str = ...,
        PathId: str = ...,
        PathName: str = ...
    ) -> DescribeProvisioningParametersOutputTypeDef:
        """
        Gets information about the configuration required to provision the specified
        product using the specified provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_provisioning_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioning_parameters)
        """

    def describe_record(
        self, *, Id: str, AcceptLanguage: str = ..., PageToken: str = ..., PageSize: int = ...
    ) -> DescribeRecordOutputTypeDef:
        """
        Gets information about the specified request operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_record)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_record)
        """

    def describe_service_action(
        self, *, Id: str, AcceptLanguage: str = ...
    ) -> DescribeServiceActionOutputTypeDef:
        """
        Describes a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_service_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_service_action)
        """

    def describe_service_action_execution_parameters(
        self, *, ProvisionedProductId: str, ServiceActionId: str, AcceptLanguage: str = ...
    ) -> DescribeServiceActionExecutionParametersOutputTypeDef:
        """
        Finds the default parameters for a specific self-service action on a specific
        provisioned product and returns a map of the results to the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_service_action_execution_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_service_action_execution_parameters)
        """

    def describe_tag_option(self, *, Id: str) -> DescribeTagOptionOutputTypeDef:
        """
        Gets information about the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_tag_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_tag_option)
        """

    def disable_aws_organizations_access(self) -> Dict[str, Any]:
        """
        Disable portfolio sharing through AWS Organizations feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.disable_aws_organizations_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disable_aws_organizations_access)
        """

    def disassociate_budget_from_resource(
        self, *, BudgetName: str, ResourceId: str
    ) -> Dict[str, Any]:
        """
        Disassociates the specified budget from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.disassociate_budget_from_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_budget_from_resource)
        """

    def disassociate_principal_from_portfolio(
        self, *, PortfolioId: str, PrincipalARN: str, AcceptLanguage: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociates a previously associated principal ARN from a specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.disassociate_principal_from_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_principal_from_portfolio)
        """

    def disassociate_product_from_portfolio(
        self, *, ProductId: str, PortfolioId: str, AcceptLanguage: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociates the specified product from the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.disassociate_product_from_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_product_from_portfolio)
        """

    def disassociate_service_action_from_provisioning_artifact(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        ServiceActionId: str,
        AcceptLanguage: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociates the specified self-service action association from the specified
        provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.disassociate_service_action_from_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_service_action_from_provisioning_artifact)
        """

    def disassociate_tag_option_from_resource(
        self, *, ResourceId: str, TagOptionId: str
    ) -> Dict[str, Any]:
        """
        Disassociates the specified TagOption from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.disassociate_tag_option_from_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_tag_option_from_resource)
        """

    def enable_aws_organizations_access(self) -> Dict[str, Any]:
        """
        Enable portfolio sharing feature through AWS Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.enable_aws_organizations_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#enable_aws_organizations_access)
        """

    def execute_provisioned_product_plan(
        self, *, PlanId: str, IdempotencyToken: str, AcceptLanguage: str = ...
    ) -> ExecuteProvisionedProductPlanOutputTypeDef:
        """
        Provisions or modifies a product based on the resource changes for the specified
        plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.execute_provisioned_product_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#execute_provisioned_product_plan)
        """

    def execute_provisioned_product_service_action(
        self,
        *,
        ProvisionedProductId: str,
        ServiceActionId: str,
        ExecuteToken: str,
        AcceptLanguage: str = ...,
        Parameters: Mapping[str, Sequence[str]] = ...
    ) -> ExecuteProvisionedProductServiceActionOutputTypeDef:
        """
        Executes a self-service action against a provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.execute_provisioned_product_service_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#execute_provisioned_product_service_action)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#generate_presigned_url)
        """

    def get_aws_organizations_access_status(self) -> GetAWSOrganizationsAccessStatusOutputTypeDef:
        """
        Get the Access Status for AWS Organization portfolio share feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_aws_organizations_access_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_aws_organizations_access_status)
        """

    def get_provisioned_product_outputs(
        self,
        *,
        AcceptLanguage: str = ...,
        ProvisionedProductId: str = ...,
        ProvisionedProductName: str = ...,
        OutputKeys: Sequence[str] = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> GetProvisionedProductOutputsOutputTypeDef:
        """
        This API takes either a `ProvisonedProductId` or a `ProvisionedProductName` ,
        along with a list of one or more output keys, and responds with the key/value
        pairs of those outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_provisioned_product_outputs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_provisioned_product_outputs)
        """

    def import_as_provisioned_product(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        ProvisionedProductName: str,
        PhysicalId: str,
        IdempotencyToken: str,
        AcceptLanguage: str = ...
    ) -> ImportAsProvisionedProductOutputTypeDef:
        """
        Requests the import of a resource as a Service Catalog provisioned product that
        is associated to a Service Catalog product and provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.import_as_provisioned_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#import_as_provisioned_product)
        """

    def list_accepted_portfolio_shares(
        self,
        *,
        AcceptLanguage: str = ...,
        PageToken: str = ...,
        PageSize: int = ...,
        PortfolioShareType: PortfolioShareTypeType = ...
    ) -> ListAcceptedPortfolioSharesOutputTypeDef:
        """
        Lists all imported portfolios for which account-to-account shares were accepted
        by this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_accepted_portfolio_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_accepted_portfolio_shares)
        """

    def list_budgets_for_resource(
        self,
        *,
        ResourceId: str,
        AcceptLanguage: str = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListBudgetsForResourceOutputTypeDef:
        """
        Lists all the budgets associated to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_budgets_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_budgets_for_resource)
        """

    def list_constraints_for_portfolio(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        ProductId: str = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListConstraintsForPortfolioOutputTypeDef:
        """
        Lists the constraints for the specified portfolio and product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_constraints_for_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_constraints_for_portfolio)
        """

    def list_launch_paths(
        self,
        *,
        ProductId: str,
        AcceptLanguage: str = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListLaunchPathsOutputTypeDef:
        """
        Lists the paths to the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_launch_paths)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_launch_paths)
        """

    def list_organization_portfolio_access(
        self,
        *,
        PortfolioId: str,
        OrganizationNodeType: OrganizationNodeTypeType,
        AcceptLanguage: str = ...,
        PageToken: str = ...,
        PageSize: int = ...
    ) -> ListOrganizationPortfolioAccessOutputTypeDef:
        """
        Lists the organization nodes that have access to the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_organization_portfolio_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_organization_portfolio_access)
        """

    def list_portfolio_access(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        OrganizationParentId: str = ...,
        PageToken: str = ...,
        PageSize: int = ...
    ) -> ListPortfolioAccessOutputTypeDef:
        """
        Lists the account IDs that have access to the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_portfolio_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_portfolio_access)
        """

    def list_portfolios(
        self, *, AcceptLanguage: str = ..., PageToken: str = ..., PageSize: int = ...
    ) -> ListPortfoliosOutputTypeDef:
        """
        Lists all portfolios in the catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_portfolios)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_portfolios)
        """

    def list_portfolios_for_product(
        self,
        *,
        ProductId: str,
        AcceptLanguage: str = ...,
        PageToken: str = ...,
        PageSize: int = ...
    ) -> ListPortfoliosForProductOutputTypeDef:
        """
        Lists all portfolios that the specified product is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_portfolios_for_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_portfolios_for_product)
        """

    def list_principals_for_portfolio(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListPrincipalsForPortfolioOutputTypeDef:
        """
        Lists all principal ARNs associated with the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_principals_for_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_principals_for_portfolio)
        """

    def list_provisioned_product_plans(
        self,
        *,
        AcceptLanguage: str = ...,
        ProvisionProductId: str = ...,
        PageSize: int = ...,
        PageToken: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...
    ) -> ListProvisionedProductPlansOutputTypeDef:
        """
        Lists the plans for the specified provisioned product or all plans to which the
        user has access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_provisioned_product_plans)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_provisioned_product_plans)
        """

    def list_provisioning_artifacts(
        self, *, ProductId: str, AcceptLanguage: str = ...
    ) -> ListProvisioningArtifactsOutputTypeDef:
        """
        Lists all provisioning artifacts (also known as versions) for the specified
        product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_provisioning_artifacts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_provisioning_artifacts)
        """

    def list_provisioning_artifacts_for_service_action(
        self,
        *,
        ServiceActionId: str,
        PageSize: int = ...,
        PageToken: str = ...,
        AcceptLanguage: str = ...
    ) -> ListProvisioningArtifactsForServiceActionOutputTypeDef:
        """
        Lists all provisioning artifacts (also known as versions) for the specified
        self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_provisioning_artifacts_for_service_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_provisioning_artifacts_for_service_action)
        """

    def list_record_history(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...,
        SearchFilter: ListRecordHistorySearchFilterTypeDef = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListRecordHistoryOutputTypeDef:
        """
        Lists the specified requests or all performed requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_record_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_record_history)
        """

    def list_resources_for_tag_option(
        self,
        *,
        TagOptionId: str,
        ResourceType: str = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListResourcesForTagOptionOutputTypeDef:
        """
        Lists the resources associated with the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_resources_for_tag_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_resources_for_tag_option)
        """

    def list_service_actions(
        self, *, AcceptLanguage: str = ..., PageSize: int = ..., PageToken: str = ...
    ) -> ListServiceActionsOutputTypeDef:
        """
        Lists all self-service actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_service_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_service_actions)
        """

    def list_service_actions_for_provisioning_artifact(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        PageSize: int = ...,
        PageToken: str = ...,
        AcceptLanguage: str = ...
    ) -> ListServiceActionsForProvisioningArtifactOutputTypeDef:
        """
        Returns a paginated list of self-service actions associated with the specified
        Product ID and Provisioning Artifact ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_service_actions_for_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_service_actions_for_provisioning_artifact)
        """

    def list_stack_instances_for_provisioned_product(
        self,
        *,
        ProvisionedProductId: str,
        AcceptLanguage: str = ...,
        PageToken: str = ...,
        PageSize: int = ...
    ) -> ListStackInstancesForProvisionedProductOutputTypeDef:
        """
        Returns summary information about stack instances that are associated with the
        specified `CFN_STACKSET` type provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_stack_instances_for_provisioned_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_stack_instances_for_provisioned_product)
        """

    def list_tag_options(
        self,
        *,
        Filters: ListTagOptionsFiltersTypeDef = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ListTagOptionsOutputTypeDef:
        """
        Lists the specified TagOptions or all TagOptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.list_tag_options)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_tag_options)
        """

    def provision_product(
        self,
        *,
        ProvisionedProductName: str,
        ProvisionToken: str,
        AcceptLanguage: str = ...,
        ProductId: str = ...,
        ProductName: str = ...,
        ProvisioningArtifactId: str = ...,
        ProvisioningArtifactName: str = ...,
        PathId: str = ...,
        PathName: str = ...,
        ProvisioningParameters: Sequence[ProvisioningParameterTypeDef] = ...,
        ProvisioningPreferences: ProvisioningPreferencesTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        NotificationArns: Sequence[str] = ...
    ) -> ProvisionProductOutputTypeDef:
        """
        Provisions the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.provision_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#provision_product)
        """

    def reject_portfolio_share(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        PortfolioShareType: PortfolioShareTypeType = ...
    ) -> Dict[str, Any]:
        """
        Rejects an offer to share the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.reject_portfolio_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#reject_portfolio_share)
        """

    def scan_provisioned_products(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> ScanProvisionedProductsOutputTypeDef:
        """
        Lists the provisioned products that are available (not terminated).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.scan_provisioned_products)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#scan_provisioned_products)
        """

    def search_products(
        self,
        *,
        AcceptLanguage: str = ...,
        Filters: Mapping[ProductViewFilterByType, Sequence[str]] = ...,
        PageSize: int = ...,
        SortBy: ProductViewSortByType = ...,
        SortOrder: SortOrderType = ...,
        PageToken: str = ...
    ) -> SearchProductsOutputTypeDef:
        """
        Gets information about the products to which the caller has access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.search_products)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#search_products)
        """

    def search_products_as_admin(
        self,
        *,
        AcceptLanguage: str = ...,
        PortfolioId: str = ...,
        Filters: Mapping[ProductViewFilterByType, Sequence[str]] = ...,
        SortBy: ProductViewSortByType = ...,
        SortOrder: SortOrderType = ...,
        PageToken: str = ...,
        PageSize: int = ...,
        ProductSource: Literal["ACCOUNT"] = ...
    ) -> SearchProductsAsAdminOutputTypeDef:
        """
        Gets information about the products for the specified portfolio or all products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.search_products_as_admin)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#search_products_as_admin)
        """

    def search_provisioned_products(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: AccessLevelFilterTypeDef = ...,
        Filters: Mapping[Literal["SearchQuery"], Sequence[str]] = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...,
        PageSize: int = ...,
        PageToken: str = ...
    ) -> SearchProvisionedProductsOutputTypeDef:
        """
        Gets information about the provisioned products that meet the specified
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.search_provisioned_products)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#search_provisioned_products)
        """

    def terminate_provisioned_product(
        self,
        *,
        TerminateToken: str,
        ProvisionedProductName: str = ...,
        ProvisionedProductId: str = ...,
        IgnoreErrors: bool = ...,
        AcceptLanguage: str = ...,
        RetainPhysicalResources: bool = ...
    ) -> TerminateProvisionedProductOutputTypeDef:
        """
        Terminates the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.terminate_provisioned_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#terminate_provisioned_product)
        """

    def update_constraint(
        self, *, Id: str, AcceptLanguage: str = ..., Description: str = ..., Parameters: str = ...
    ) -> UpdateConstraintOutputTypeDef:
        """
        Updates the specified constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_constraint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_constraint)
        """

    def update_portfolio(
        self,
        *,
        Id: str,
        AcceptLanguage: str = ...,
        DisplayName: str = ...,
        Description: str = ...,
        ProviderName: str = ...,
        AddTags: Sequence[TagTypeDef] = ...,
        RemoveTags: Sequence[str] = ...
    ) -> UpdatePortfolioOutputTypeDef:
        """
        Updates the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_portfolio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_portfolio)
        """

    def update_portfolio_share(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        AccountId: str = ...,
        OrganizationNode: OrganizationNodeTypeDef = ...,
        ShareTagOptions: bool = ...
    ) -> UpdatePortfolioShareOutputTypeDef:
        """
        Updates the specified portfolio share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_portfolio_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_portfolio_share)
        """

    def update_product(
        self,
        *,
        Id: str,
        AcceptLanguage: str = ...,
        Name: str = ...,
        Owner: str = ...,
        Description: str = ...,
        Distributor: str = ...,
        SupportDescription: str = ...,
        SupportEmail: str = ...,
        SupportUrl: str = ...,
        AddTags: Sequence[TagTypeDef] = ...,
        RemoveTags: Sequence[str] = ...
    ) -> UpdateProductOutputTypeDef:
        """
        Updates the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_product)
        """

    def update_provisioned_product(
        self,
        *,
        UpdateToken: str,
        AcceptLanguage: str = ...,
        ProvisionedProductName: str = ...,
        ProvisionedProductId: str = ...,
        ProductId: str = ...,
        ProductName: str = ...,
        ProvisioningArtifactId: str = ...,
        ProvisioningArtifactName: str = ...,
        PathId: str = ...,
        PathName: str = ...,
        ProvisioningParameters: Sequence[UpdateProvisioningParameterTypeDef] = ...,
        ProvisioningPreferences: UpdateProvisioningPreferencesTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> UpdateProvisionedProductOutputTypeDef:
        """
        Requests updates to the configuration of the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_provisioned_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_provisioned_product)
        """

    def update_provisioned_product_properties(
        self,
        *,
        ProvisionedProductId: str,
        ProvisionedProductProperties: Mapping[PropertyKeyType, str],
        IdempotencyToken: str,
        AcceptLanguage: str = ...
    ) -> UpdateProvisionedProductPropertiesOutputTypeDef:
        """
        Requests updates to the properties of the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_provisioned_product_properties)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_provisioned_product_properties)
        """

    def update_provisioning_artifact(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        AcceptLanguage: str = ...,
        Name: str = ...,
        Description: str = ...,
        Active: bool = ...,
        Guidance: ProvisioningArtifactGuidanceType = ...
    ) -> UpdateProvisioningArtifactOutputTypeDef:
        """
        Updates the specified provisioning artifact (also known as a version) for the
        specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_provisioning_artifact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_provisioning_artifact)
        """

    def update_service_action(
        self,
        *,
        Id: str,
        Name: str = ...,
        Definition: Mapping[ServiceActionDefinitionKeyType, str] = ...,
        Description: str = ...,
        AcceptLanguage: str = ...
    ) -> UpdateServiceActionOutputTypeDef:
        """
        Updates a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_service_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_service_action)
        """

    def update_tag_option(
        self, *, Id: str, Value: str = ..., Active: bool = ...
    ) -> UpdateTagOptionOutputTypeDef:
        """
        Updates the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_tag_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_tag_option)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accepted_portfolio_shares"]
    ) -> ListAcceptedPortfolioSharesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_constraints_for_portfolio"]
    ) -> ListConstraintsForPortfolioPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_launch_paths"]
    ) -> ListLaunchPathsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_portfolio_access"]
    ) -> ListOrganizationPortfolioAccessPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_portfolios"]) -> ListPortfoliosPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_portfolios_for_product"]
    ) -> ListPortfoliosForProductPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principals_for_portfolio"]
    ) -> ListPrincipalsForPortfolioPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_product_plans"]
    ) -> ListProvisionedProductPlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioning_artifacts_for_service_action"]
    ) -> ListProvisioningArtifactsForServiceActionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_record_history"]
    ) -> ListRecordHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resources_for_tag_option"]
    ) -> ListResourcesForTagOptionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_actions"]
    ) -> ListServiceActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_actions_for_provisioning_artifact"]
    ) -> ListServiceActionsForProvisioningArtifactPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tag_options"]) -> ListTagOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["scan_provisioned_products"]
    ) -> ScanProvisionedProductsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_products_as_admin"]
    ) -> SearchProductsAsAdminPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """
