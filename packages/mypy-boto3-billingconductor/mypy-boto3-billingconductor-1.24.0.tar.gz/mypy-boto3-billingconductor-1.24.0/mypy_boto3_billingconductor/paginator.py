"""
Type annotations for billingconductor service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_billingconductor.client import BillingConductorClient
    from mypy_boto3_billingconductor.paginator import (
        ListAccountAssociationsPaginator,
        ListBillingGroupCostReportsPaginator,
        ListBillingGroupsPaginator,
        ListCustomLineItemsPaginator,
        ListPricingPlansPaginator,
        ListPricingPlansAssociatedWithPricingRulePaginator,
        ListPricingRulesPaginator,
        ListPricingRulesAssociatedToPricingPlanPaginator,
        ListResourcesAssociatedToCustomLineItemPaginator,
    )

    session = Session()
    client: BillingConductorClient = session.client("billingconductor")

    list_account_associations_paginator: ListAccountAssociationsPaginator = client.get_paginator("list_account_associations")
    list_billing_group_cost_reports_paginator: ListBillingGroupCostReportsPaginator = client.get_paginator("list_billing_group_cost_reports")
    list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
    list_custom_line_items_paginator: ListCustomLineItemsPaginator = client.get_paginator("list_custom_line_items")
    list_pricing_plans_paginator: ListPricingPlansPaginator = client.get_paginator("list_pricing_plans")
    list_pricing_plans_associated_with_pricing_rule_paginator: ListPricingPlansAssociatedWithPricingRulePaginator = client.get_paginator("list_pricing_plans_associated_with_pricing_rule")
    list_pricing_rules_paginator: ListPricingRulesPaginator = client.get_paginator("list_pricing_rules")
    list_pricing_rules_associated_to_pricing_plan_paginator: ListPricingRulesAssociatedToPricingPlanPaginator = client.get_paginator("list_pricing_rules_associated_to_pricing_plan")
    list_resources_associated_to_custom_line_item_paginator: ListResourcesAssociatedToCustomLineItemPaginator = client.get_paginator("list_resources_associated_to_custom_line_item")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAccountAssociationsFilterTypeDef,
    ListAccountAssociationsOutputTypeDef,
    ListBillingGroupCostReportsFilterTypeDef,
    ListBillingGroupCostReportsOutputTypeDef,
    ListBillingGroupsFilterTypeDef,
    ListBillingGroupsOutputTypeDef,
    ListCustomLineItemsFilterTypeDef,
    ListCustomLineItemsOutputTypeDef,
    ListPricingPlansAssociatedWithPricingRuleOutputTypeDef,
    ListPricingPlansFilterTypeDef,
    ListPricingPlansOutputTypeDef,
    ListPricingRulesAssociatedToPricingPlanOutputTypeDef,
    ListPricingRulesFilterTypeDef,
    ListPricingRulesOutputTypeDef,
    ListResourcesAssociatedToCustomLineItemFilterTypeDef,
    ListResourcesAssociatedToCustomLineItemOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAccountAssociationsPaginator",
    "ListBillingGroupCostReportsPaginator",
    "ListBillingGroupsPaginator",
    "ListCustomLineItemsPaginator",
    "ListPricingPlansPaginator",
    "ListPricingPlansAssociatedWithPricingRulePaginator",
    "ListPricingRulesPaginator",
    "ListPricingRulesAssociatedToPricingPlanPaginator",
    "ListResourcesAssociatedToCustomLineItemPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListAccountAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listaccountassociationspaginator)
    """

    def paginate(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListAccountAssociationsFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListAccountAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listaccountassociationspaginator)
        """


class ListBillingGroupCostReportsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroupCostReports)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupcostreportspaginator)
    """

    def paginate(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListBillingGroupCostReportsFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBillingGroupCostReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroupCostReports.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupcostreportspaginator)
        """


class ListBillingGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupspaginator)
    """

    def paginate(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListBillingGroupsFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBillingGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupspaginator)
        """


class ListCustomLineItemsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListCustomLineItems)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listcustomlineitemspaginator)
    """

    def paginate(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListCustomLineItemsFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListCustomLineItems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listcustomlineitemspaginator)
        """


class ListPricingPlansPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlans)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplanspaginator)
    """

    def paginate(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListPricingPlansFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPricingPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlans.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplanspaginator)
        """


class ListPricingPlansAssociatedWithPricingRulePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
    """

    def paginate(
        self,
        *,
        PricingRuleArn: str,
        BillingPeriod: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPricingPlansAssociatedWithPricingRuleOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
        """


class ListPricingRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulespaginator)
    """

    def paginate(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListPricingRulesFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPricingRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulespaginator)
        """


class ListPricingRulesAssociatedToPricingPlanPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
    """

    def paginate(
        self,
        *,
        PricingPlanArn: str,
        BillingPeriod: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPricingRulesAssociatedToPricingPlanOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
        """


class ListResourcesAssociatedToCustomLineItemPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
    """

    def paginate(
        self,
        *,
        Arn: str,
        BillingPeriod: str = ...,
        Filters: ListResourcesAssociatedToCustomLineItemFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourcesAssociatedToCustomLineItemOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
        """
