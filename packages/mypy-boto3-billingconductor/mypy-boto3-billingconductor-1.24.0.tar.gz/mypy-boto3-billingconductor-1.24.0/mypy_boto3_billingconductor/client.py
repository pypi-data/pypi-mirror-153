"""
Type annotations for billingconductor service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_billingconductor.client import BillingConductorClient

    session = Session()
    client: BillingConductorClient = session.client("billingconductor")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import BillingGroupStatusType, PricingRuleScopeType, PricingRuleTypeType
from .paginator import (
    ListAccountAssociationsPaginator,
    ListBillingGroupCostReportsPaginator,
    ListBillingGroupsPaginator,
    ListCustomLineItemsPaginator,
    ListPricingPlansAssociatedWithPricingRulePaginator,
    ListPricingPlansPaginator,
    ListPricingRulesAssociatedToPricingPlanPaginator,
    ListPricingRulesPaginator,
    ListResourcesAssociatedToCustomLineItemPaginator,
)
from .type_defs import (
    AccountGroupingTypeDef,
    AssociateAccountsOutputTypeDef,
    AssociatePricingRulesOutputTypeDef,
    BatchAssociateResourcesToCustomLineItemOutputTypeDef,
    BatchDisassociateResourcesFromCustomLineItemOutputTypeDef,
    ComputationPreferenceTypeDef,
    CreateBillingGroupOutputTypeDef,
    CreateCustomLineItemOutputTypeDef,
    CreatePricingPlanOutputTypeDef,
    CreatePricingRuleOutputTypeDef,
    CustomLineItemBillingPeriodRangeTypeDef,
    CustomLineItemChargeDetailsTypeDef,
    DeleteBillingGroupOutputTypeDef,
    DeleteCustomLineItemOutputTypeDef,
    DeletePricingPlanOutputTypeDef,
    DeletePricingRuleOutputTypeDef,
    DisassociateAccountsOutputTypeDef,
    DisassociatePricingRulesOutputTypeDef,
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
    ListTagsForResourceResponseTypeDef,
    UpdateBillingGroupOutputTypeDef,
    UpdateCustomLineItemChargeDetailsTypeDef,
    UpdateCustomLineItemOutputTypeDef,
    UpdatePricingPlanOutputTypeDef,
    UpdatePricingRuleOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("BillingConductorClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BillingConductorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BillingConductorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#exceptions)
        """

    def associate_accounts(
        self, *, Arn: str, AccountIds: Sequence[str]
    ) -> AssociateAccountsOutputTypeDef:
        """
        Connects an array of account IDs in a consolidated billing family to a
        predefined billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.associate_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#associate_accounts)
        """

    def associate_pricing_rules(
        self, *, Arn: str, PricingRuleArns: Sequence[str]
    ) -> AssociatePricingRulesOutputTypeDef:
        """
        Connects an array of `PricingRuleArns` to a defined `PricingPlan`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.associate_pricing_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#associate_pricing_rules)
        """

    def batch_associate_resources_to_custom_line_item(
        self,
        *,
        TargetArn: str,
        ResourceArns: Sequence[str],
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...
    ) -> BatchAssociateResourcesToCustomLineItemOutputTypeDef:
        """
        Associates a batch of resources to a percentage custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.batch_associate_resources_to_custom_line_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#batch_associate_resources_to_custom_line_item)
        """

    def batch_disassociate_resources_from_custom_line_item(
        self,
        *,
        TargetArn: str,
        ResourceArns: Sequence[str],
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...
    ) -> BatchDisassociateResourcesFromCustomLineItemOutputTypeDef:
        """
        Disassociates a batch of resources from a percentage custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.batch_disassociate_resources_from_custom_line_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#batch_disassociate_resources_from_custom_line_item)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#can_paginate)
        """

    def create_billing_group(
        self,
        *,
        Name: str,
        AccountGrouping: AccountGroupingTypeDef,
        ComputationPreference: ComputationPreferenceTypeDef,
        ClientToken: str = ...,
        PrimaryAccountId: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateBillingGroupOutputTypeDef:
        """
        Creates a billing group that resembles a consolidated billing family that Amazon
        Web Services charges, based off of the predefined pricing plan computation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_billing_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#create_billing_group)
        """

    def create_custom_line_item(
        self,
        *,
        Name: str,
        Description: str,
        BillingGroupArn: str,
        ChargeDetails: CustomLineItemChargeDetailsTypeDef,
        ClientToken: str = ...,
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateCustomLineItemOutputTypeDef:
        """
        Creates a custom line item that can be used to create a one-time fixed charge
        that can be applied to a single billing group for the current or previous
        billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_custom_line_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#create_custom_line_item)
        """

    def create_pricing_plan(
        self,
        *,
        Name: str,
        ClientToken: str = ...,
        Description: str = ...,
        PricingRuleArns: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreatePricingPlanOutputTypeDef:
        """
        Creates a pricing plan that is used for computing Amazon Web Services charges
        for billing groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_pricing_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#create_pricing_plan)
        """

    def create_pricing_rule(
        self,
        *,
        Name: str,
        Scope: PricingRuleScopeType,
        Type: PricingRuleTypeType,
        ModifierPercentage: float,
        ClientToken: str = ...,
        Description: str = ...,
        Service: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreatePricingRuleOutputTypeDef:
        """
        Creates a pricing rule can be associated to a pricing plan, or a set of pricing
        plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_pricing_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#create_pricing_rule)
        """

    def delete_billing_group(self, *, Arn: str) -> DeleteBillingGroupOutputTypeDef:
        """
        Deletes a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_billing_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#delete_billing_group)
        """

    def delete_custom_line_item(
        self, *, Arn: str, BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...
    ) -> DeleteCustomLineItemOutputTypeDef:
        """
        Deletes the custom line item identified by the given ARN in the current, or
        previous billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_custom_line_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#delete_custom_line_item)
        """

    def delete_pricing_plan(self, *, Arn: str) -> DeletePricingPlanOutputTypeDef:
        """
        Deletes a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_pricing_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#delete_pricing_plan)
        """

    def delete_pricing_rule(self, *, Arn: str) -> DeletePricingRuleOutputTypeDef:
        """
        Deletes the pricing rule identified by the input Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_pricing_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#delete_pricing_rule)
        """

    def disassociate_accounts(
        self, *, Arn: str, AccountIds: Sequence[str]
    ) -> DisassociateAccountsOutputTypeDef:
        """
        Removes the specified list of account IDs from the given billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.disassociate_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#disassociate_accounts)
        """

    def disassociate_pricing_rules(
        self, *, Arn: str, PricingRuleArns: Sequence[str]
    ) -> DisassociatePricingRulesOutputTypeDef:
        """
        Disassociates a list of pricing rules from a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.disassociate_pricing_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#disassociate_pricing_rules)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#generate_presigned_url)
        """

    def list_account_associations(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListAccountAssociationsFilterTypeDef = ...,
        NextToken: str = ...
    ) -> ListAccountAssociationsOutputTypeDef:
        """
        * **Amazon Web Services Billing Conductor is in beta release and is subject to
        change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_account_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_account_associations)
        """

    def list_billing_group_cost_reports(
        self,
        *,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListBillingGroupCostReportsFilterTypeDef = ...
    ) -> ListBillingGroupCostReportsOutputTypeDef:
        """
        A paginated call to retrieve a summary report of actual Amazon Web Services
        charges and the calculated Amazon Web Services charges based on the associated
        pricing plan of a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_billing_group_cost_reports)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_billing_group_cost_reports)
        """

    def list_billing_groups(
        self,
        *,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListBillingGroupsFilterTypeDef = ...
    ) -> ListBillingGroupsOutputTypeDef:
        """
        A paginated call to retrieve a list of billing groups for the given billing
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_billing_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_billing_groups)
        """

    def list_custom_line_items(
        self,
        *,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListCustomLineItemsFilterTypeDef = ...
    ) -> ListCustomLineItemsOutputTypeDef:
        """
        A paginated call to get a list of all custom line items (FFLIs) for the given
        billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_custom_line_items)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_custom_line_items)
        """

    def list_pricing_plans(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListPricingPlansFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPricingPlansOutputTypeDef:
        """
        A paginated call to get pricing plans for the given billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_plans)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_pricing_plans)
        """

    def list_pricing_plans_associated_with_pricing_rule(
        self,
        *,
        PricingRuleArn: str,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPricingPlansAssociatedWithPricingRuleOutputTypeDef:
        """
        A list of the pricing plans associated with a pricing rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_plans_associated_with_pricing_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_pricing_plans_associated_with_pricing_rule)
        """

    def list_pricing_rules(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListPricingRulesFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPricingRulesOutputTypeDef:
        """
        Describes a pricing rule that can be associated to a pricing plan, or set of
        pricing plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_pricing_rules)
        """

    def list_pricing_rules_associated_to_pricing_plan(
        self,
        *,
        PricingPlanArn: str,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPricingRulesAssociatedToPricingPlanOutputTypeDef:
        """
        Lists the pricing rules associated with a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_rules_associated_to_pricing_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_pricing_rules_associated_to_pricing_plan)
        """

    def list_resources_associated_to_custom_line_item(
        self,
        *,
        Arn: str,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListResourcesAssociatedToCustomLineItemFilterTypeDef = ...
    ) -> ListResourcesAssociatedToCustomLineItemOutputTypeDef:
        """
        List the resources associated to a custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_resources_associated_to_custom_line_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_resources_associated_to_custom_line_item)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        A list the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#untag_resource)
        """

    def update_billing_group(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Status: BillingGroupStatusType = ...,
        ComputationPreference: ComputationPreferenceTypeDef = ...,
        Description: str = ...
    ) -> UpdateBillingGroupOutputTypeDef:
        """
        This updates an existing billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_billing_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#update_billing_group)
        """

    def update_custom_line_item(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Description: str = ...,
        ChargeDetails: UpdateCustomLineItemChargeDetailsTypeDef = ...,
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...
    ) -> UpdateCustomLineItemOutputTypeDef:
        """
        Update an existing custom line item in the current or previous billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_custom_line_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#update_custom_line_item)
        """

    def update_pricing_plan(
        self, *, Arn: str, Name: str = ..., Description: str = ...
    ) -> UpdatePricingPlanOutputTypeDef:
        """
        This updates an existing pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_pricing_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#update_pricing_plan)
        """

    def update_pricing_rule(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Description: str = ...,
        Type: PricingRuleTypeType = ...,
        ModifierPercentage: float = ...
    ) -> UpdatePricingRuleOutputTypeDef:
        """
        Updates an existing pricing rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_pricing_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#update_pricing_rule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_associations"]
    ) -> ListAccountAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_group_cost_reports"]
    ) -> ListBillingGroupCostReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_groups"]
    ) -> ListBillingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_line_items"]
    ) -> ListCustomLineItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_plans"]
    ) -> ListPricingPlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_plans_associated_with_pricing_rule"]
    ) -> ListPricingPlansAssociatedWithPricingRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_rules"]
    ) -> ListPricingRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_rules_associated_to_pricing_plan"]
    ) -> ListPricingRulesAssociatedToPricingPlanPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resources_associated_to_custom_line_item"]
    ) -> ListResourcesAssociatedToCustomLineItemPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/client/#get_paginator)
        """
