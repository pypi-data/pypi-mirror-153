"""
Type annotations for billingconductor service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/type_defs/)

Usage::

    ```python
    from mypy_boto3_billingconductor.type_defs import AccountAssociationsListElementTypeDef

    data: AccountAssociationsListElementTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AssociateResourceErrorReasonType,
    BillingGroupStatusType,
    CurrencyCodeType,
    CustomLineItemRelationshipType,
    CustomLineItemTypeType,
    PricingRuleScopeType,
    PricingRuleTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountAssociationsListElementTypeDef",
    "AccountGroupingTypeDef",
    "AssociateAccountsInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociatePricingRulesInputRequestTypeDef",
    "AssociateResourceErrorTypeDef",
    "CustomLineItemBillingPeriodRangeTypeDef",
    "BillingGroupCostReportElementTypeDef",
    "ComputationPreferenceTypeDef",
    "CreatePricingPlanInputRequestTypeDef",
    "CreatePricingRuleInputRequestTypeDef",
    "CustomLineItemFlatChargeDetailsTypeDef",
    "CustomLineItemPercentageChargeDetailsTypeDef",
    "DeleteBillingGroupInputRequestTypeDef",
    "DeletePricingPlanInputRequestTypeDef",
    "DeletePricingRuleInputRequestTypeDef",
    "DisassociateAccountsInputRequestTypeDef",
    "DisassociatePricingRulesInputRequestTypeDef",
    "ListAccountAssociationsFilterTypeDef",
    "PaginatorConfigTypeDef",
    "ListBillingGroupCostReportsFilterTypeDef",
    "ListBillingGroupsFilterTypeDef",
    "ListCustomLineItemFlatChargeDetailsTypeDef",
    "ListCustomLineItemPercentageChargeDetailsTypeDef",
    "ListCustomLineItemsFilterTypeDef",
    "ListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef",
    "ListPricingPlansFilterTypeDef",
    "PricingPlanListElementTypeDef",
    "ListPricingRulesAssociatedToPricingPlanInputRequestTypeDef",
    "ListPricingRulesFilterTypeDef",
    "PricingRuleListElementTypeDef",
    "ListResourcesAssociatedToCustomLineItemFilterTypeDef",
    "ListResourcesAssociatedToCustomLineItemResponseElementTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCustomLineItemFlatChargeDetailsTypeDef",
    "UpdateCustomLineItemPercentageChargeDetailsTypeDef",
    "UpdatePricingPlanInputRequestTypeDef",
    "UpdatePricingRuleInputRequestTypeDef",
    "AssociateAccountsOutputTypeDef",
    "AssociatePricingRulesOutputTypeDef",
    "CreateBillingGroupOutputTypeDef",
    "CreateCustomLineItemOutputTypeDef",
    "CreatePricingPlanOutputTypeDef",
    "CreatePricingRuleOutputTypeDef",
    "DeleteBillingGroupOutputTypeDef",
    "DeleteCustomLineItemOutputTypeDef",
    "DeletePricingPlanOutputTypeDef",
    "DeletePricingRuleOutputTypeDef",
    "DisassociateAccountsOutputTypeDef",
    "DisassociatePricingRulesOutputTypeDef",
    "ListAccountAssociationsOutputTypeDef",
    "ListPricingPlansAssociatedWithPricingRuleOutputTypeDef",
    "ListPricingRulesAssociatedToPricingPlanOutputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateBillingGroupOutputTypeDef",
    "UpdatePricingPlanOutputTypeDef",
    "UpdatePricingRuleOutputTypeDef",
    "AssociateResourceResponseElementTypeDef",
    "DisassociateResourceResponseElementTypeDef",
    "BatchAssociateResourcesToCustomLineItemInputRequestTypeDef",
    "BatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef",
    "DeleteCustomLineItemInputRequestTypeDef",
    "ListBillingGroupCostReportsOutputTypeDef",
    "BillingGroupListElementTypeDef",
    "CreateBillingGroupInputRequestTypeDef",
    "UpdateBillingGroupInputRequestTypeDef",
    "CustomLineItemChargeDetailsTypeDef",
    "ListAccountAssociationsInputRequestTypeDef",
    "ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef",
    "ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef",
    "ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef",
    "ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef",
    "ListBillingGroupCostReportsInputRequestTypeDef",
    "ListBillingGroupsInputListBillingGroupsPaginateTypeDef",
    "ListBillingGroupsInputRequestTypeDef",
    "ListCustomLineItemChargeDetailsTypeDef",
    "ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef",
    "ListCustomLineItemsInputRequestTypeDef",
    "ListPricingPlansInputListPricingPlansPaginateTypeDef",
    "ListPricingPlansInputRequestTypeDef",
    "ListPricingPlansOutputTypeDef",
    "ListPricingRulesInputListPricingRulesPaginateTypeDef",
    "ListPricingRulesInputRequestTypeDef",
    "ListPricingRulesOutputTypeDef",
    "ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef",
    "ListResourcesAssociatedToCustomLineItemInputRequestTypeDef",
    "ListResourcesAssociatedToCustomLineItemOutputTypeDef",
    "UpdateCustomLineItemChargeDetailsTypeDef",
    "BatchAssociateResourcesToCustomLineItemOutputTypeDef",
    "BatchDisassociateResourcesFromCustomLineItemOutputTypeDef",
    "ListBillingGroupsOutputTypeDef",
    "CreateCustomLineItemInputRequestTypeDef",
    "CustomLineItemListElementTypeDef",
    "UpdateCustomLineItemOutputTypeDef",
    "UpdateCustomLineItemInputRequestTypeDef",
    "ListCustomLineItemsOutputTypeDef",
)

AccountAssociationsListElementTypeDef = TypedDict(
    "AccountAssociationsListElementTypeDef",
    {
        "AccountId": str,
        "BillingGroupArn": str,
        "AccountName": str,
        "AccountEmail": str,
    },
    total=False,
)

AccountGroupingTypeDef = TypedDict(
    "AccountGroupingTypeDef",
    {
        "LinkedAccountIds": Sequence[str],
    },
)

AssociateAccountsInputRequestTypeDef = TypedDict(
    "AssociateAccountsInputRequestTypeDef",
    {
        "Arn": str,
        "AccountIds": Sequence[str],
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

AssociatePricingRulesInputRequestTypeDef = TypedDict(
    "AssociatePricingRulesInputRequestTypeDef",
    {
        "Arn": str,
        "PricingRuleArns": Sequence[str],
    },
)

AssociateResourceErrorTypeDef = TypedDict(
    "AssociateResourceErrorTypeDef",
    {
        "Message": str,
        "Reason": AssociateResourceErrorReasonType,
    },
    total=False,
)

CustomLineItemBillingPeriodRangeTypeDef = TypedDict(
    "CustomLineItemBillingPeriodRangeTypeDef",
    {
        "InclusiveStartBillingPeriod": str,
        "ExclusiveEndBillingPeriod": str,
    },
)

BillingGroupCostReportElementTypeDef = TypedDict(
    "BillingGroupCostReportElementTypeDef",
    {
        "Arn": str,
        "AWSCost": str,
        "ProformaCost": str,
        "Margin": str,
        "MarginPercentage": str,
        "Currency": str,
    },
    total=False,
)

ComputationPreferenceTypeDef = TypedDict(
    "ComputationPreferenceTypeDef",
    {
        "PricingPlanArn": str,
    },
)

_RequiredCreatePricingPlanInputRequestTypeDef = TypedDict(
    "_RequiredCreatePricingPlanInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreatePricingPlanInputRequestTypeDef = TypedDict(
    "_OptionalCreatePricingPlanInputRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "PricingRuleArns": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreatePricingPlanInputRequestTypeDef(
    _RequiredCreatePricingPlanInputRequestTypeDef, _OptionalCreatePricingPlanInputRequestTypeDef
):
    pass


_RequiredCreatePricingRuleInputRequestTypeDef = TypedDict(
    "_RequiredCreatePricingRuleInputRequestTypeDef",
    {
        "Name": str,
        "Scope": PricingRuleScopeType,
        "Type": PricingRuleTypeType,
        "ModifierPercentage": float,
    },
)
_OptionalCreatePricingRuleInputRequestTypeDef = TypedDict(
    "_OptionalCreatePricingRuleInputRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Service": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreatePricingRuleInputRequestTypeDef(
    _RequiredCreatePricingRuleInputRequestTypeDef, _OptionalCreatePricingRuleInputRequestTypeDef
):
    pass


CustomLineItemFlatChargeDetailsTypeDef = TypedDict(
    "CustomLineItemFlatChargeDetailsTypeDef",
    {
        "ChargeValue": float,
    },
)

_RequiredCustomLineItemPercentageChargeDetailsTypeDef = TypedDict(
    "_RequiredCustomLineItemPercentageChargeDetailsTypeDef",
    {
        "PercentageValue": float,
    },
)
_OptionalCustomLineItemPercentageChargeDetailsTypeDef = TypedDict(
    "_OptionalCustomLineItemPercentageChargeDetailsTypeDef",
    {
        "AssociatedValues": Sequence[str],
    },
    total=False,
)


class CustomLineItemPercentageChargeDetailsTypeDef(
    _RequiredCustomLineItemPercentageChargeDetailsTypeDef,
    _OptionalCustomLineItemPercentageChargeDetailsTypeDef,
):
    pass


DeleteBillingGroupInputRequestTypeDef = TypedDict(
    "DeleteBillingGroupInputRequestTypeDef",
    {
        "Arn": str,
    },
)

DeletePricingPlanInputRequestTypeDef = TypedDict(
    "DeletePricingPlanInputRequestTypeDef",
    {
        "Arn": str,
    },
)

DeletePricingRuleInputRequestTypeDef = TypedDict(
    "DeletePricingRuleInputRequestTypeDef",
    {
        "Arn": str,
    },
)

DisassociateAccountsInputRequestTypeDef = TypedDict(
    "DisassociateAccountsInputRequestTypeDef",
    {
        "Arn": str,
        "AccountIds": Sequence[str],
    },
)

DisassociatePricingRulesInputRequestTypeDef = TypedDict(
    "DisassociatePricingRulesInputRequestTypeDef",
    {
        "Arn": str,
        "PricingRuleArns": Sequence[str],
    },
)

ListAccountAssociationsFilterTypeDef = TypedDict(
    "ListAccountAssociationsFilterTypeDef",
    {
        "Association": str,
        "AccountId": str,
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

ListBillingGroupCostReportsFilterTypeDef = TypedDict(
    "ListBillingGroupCostReportsFilterTypeDef",
    {
        "BillingGroupArns": Sequence[str],
    },
    total=False,
)

ListBillingGroupsFilterTypeDef = TypedDict(
    "ListBillingGroupsFilterTypeDef",
    {
        "Arns": Sequence[str],
        "PricingPlan": str,
    },
    total=False,
)

ListCustomLineItemFlatChargeDetailsTypeDef = TypedDict(
    "ListCustomLineItemFlatChargeDetailsTypeDef",
    {
        "ChargeValue": float,
    },
)

ListCustomLineItemPercentageChargeDetailsTypeDef = TypedDict(
    "ListCustomLineItemPercentageChargeDetailsTypeDef",
    {
        "PercentageValue": float,
    },
)

ListCustomLineItemsFilterTypeDef = TypedDict(
    "ListCustomLineItemsFilterTypeDef",
    {
        "Names": Sequence[str],
        "BillingGroups": Sequence[str],
        "Arns": Sequence[str],
    },
    total=False,
)

_RequiredListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef = TypedDict(
    "_RequiredListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef",
    {
        "PricingRuleArn": str,
    },
)
_OptionalListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef = TypedDict(
    "_OptionalListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef(
    _RequiredListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef,
    _OptionalListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef,
):
    pass


ListPricingPlansFilterTypeDef = TypedDict(
    "ListPricingPlansFilterTypeDef",
    {
        "Arns": Sequence[str],
    },
    total=False,
)

PricingPlanListElementTypeDef = TypedDict(
    "PricingPlanListElementTypeDef",
    {
        "Name": str,
        "Arn": str,
        "Description": str,
        "Size": int,
        "CreationTime": int,
        "LastModifiedTime": int,
    },
    total=False,
)

_RequiredListPricingRulesAssociatedToPricingPlanInputRequestTypeDef = TypedDict(
    "_RequiredListPricingRulesAssociatedToPricingPlanInputRequestTypeDef",
    {
        "PricingPlanArn": str,
    },
)
_OptionalListPricingRulesAssociatedToPricingPlanInputRequestTypeDef = TypedDict(
    "_OptionalListPricingRulesAssociatedToPricingPlanInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListPricingRulesAssociatedToPricingPlanInputRequestTypeDef(
    _RequiredListPricingRulesAssociatedToPricingPlanInputRequestTypeDef,
    _OptionalListPricingRulesAssociatedToPricingPlanInputRequestTypeDef,
):
    pass


ListPricingRulesFilterTypeDef = TypedDict(
    "ListPricingRulesFilterTypeDef",
    {
        "Arns": Sequence[str],
    },
    total=False,
)

PricingRuleListElementTypeDef = TypedDict(
    "PricingRuleListElementTypeDef",
    {
        "Name": str,
        "Arn": str,
        "Description": str,
        "Scope": PricingRuleScopeType,
        "Type": PricingRuleTypeType,
        "ModifierPercentage": float,
        "Service": str,
        "AssociatedPricingPlanCount": int,
        "CreationTime": int,
        "LastModifiedTime": int,
    },
    total=False,
)

ListResourcesAssociatedToCustomLineItemFilterTypeDef = TypedDict(
    "ListResourcesAssociatedToCustomLineItemFilterTypeDef",
    {
        "Relationship": CustomLineItemRelationshipType,
    },
    total=False,
)

ListResourcesAssociatedToCustomLineItemResponseElementTypeDef = TypedDict(
    "ListResourcesAssociatedToCustomLineItemResponseElementTypeDef",
    {
        "Arn": str,
        "Relationship": CustomLineItemRelationshipType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
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

UpdateCustomLineItemFlatChargeDetailsTypeDef = TypedDict(
    "UpdateCustomLineItemFlatChargeDetailsTypeDef",
    {
        "ChargeValue": float,
    },
)

UpdateCustomLineItemPercentageChargeDetailsTypeDef = TypedDict(
    "UpdateCustomLineItemPercentageChargeDetailsTypeDef",
    {
        "PercentageValue": float,
    },
)

_RequiredUpdatePricingPlanInputRequestTypeDef = TypedDict(
    "_RequiredUpdatePricingPlanInputRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalUpdatePricingPlanInputRequestTypeDef = TypedDict(
    "_OptionalUpdatePricingPlanInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)


class UpdatePricingPlanInputRequestTypeDef(
    _RequiredUpdatePricingPlanInputRequestTypeDef, _OptionalUpdatePricingPlanInputRequestTypeDef
):
    pass


_RequiredUpdatePricingRuleInputRequestTypeDef = TypedDict(
    "_RequiredUpdatePricingRuleInputRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalUpdatePricingRuleInputRequestTypeDef = TypedDict(
    "_OptionalUpdatePricingRuleInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Type": PricingRuleTypeType,
        "ModifierPercentage": float,
    },
    total=False,
)


class UpdatePricingRuleInputRequestTypeDef(
    _RequiredUpdatePricingRuleInputRequestTypeDef, _OptionalUpdatePricingRuleInputRequestTypeDef
):
    pass


AssociateAccountsOutputTypeDef = TypedDict(
    "AssociateAccountsOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociatePricingRulesOutputTypeDef = TypedDict(
    "AssociatePricingRulesOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBillingGroupOutputTypeDef = TypedDict(
    "CreateBillingGroupOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomLineItemOutputTypeDef = TypedDict(
    "CreateCustomLineItemOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePricingPlanOutputTypeDef = TypedDict(
    "CreatePricingPlanOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePricingRuleOutputTypeDef = TypedDict(
    "CreatePricingRuleOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBillingGroupOutputTypeDef = TypedDict(
    "DeleteBillingGroupOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCustomLineItemOutputTypeDef = TypedDict(
    "DeleteCustomLineItemOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePricingPlanOutputTypeDef = TypedDict(
    "DeletePricingPlanOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePricingRuleOutputTypeDef = TypedDict(
    "DeletePricingRuleOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateAccountsOutputTypeDef = TypedDict(
    "DisassociateAccountsOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociatePricingRulesOutputTypeDef = TypedDict(
    "DisassociatePricingRulesOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssociationsOutputTypeDef = TypedDict(
    "ListAccountAssociationsOutputTypeDef",
    {
        "LinkedAccounts": List[AccountAssociationsListElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPricingPlansAssociatedWithPricingRuleOutputTypeDef = TypedDict(
    "ListPricingPlansAssociatedWithPricingRuleOutputTypeDef",
    {
        "BillingPeriod": str,
        "PricingRuleArn": str,
        "PricingPlanArns": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPricingRulesAssociatedToPricingPlanOutputTypeDef = TypedDict(
    "ListPricingRulesAssociatedToPricingPlanOutputTypeDef",
    {
        "BillingPeriod": str,
        "PricingPlanArn": str,
        "PricingRuleArns": List[str],
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

UpdateBillingGroupOutputTypeDef = TypedDict(
    "UpdateBillingGroupOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
        "PrimaryAccountId": str,
        "PricingPlanArn": str,
        "Size": int,
        "LastModifiedTime": int,
        "Status": BillingGroupStatusType,
        "StatusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePricingPlanOutputTypeDef = TypedDict(
    "UpdatePricingPlanOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
        "Size": int,
        "LastModifiedTime": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePricingRuleOutputTypeDef = TypedDict(
    "UpdatePricingRuleOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
        "Scope": PricingRuleScopeType,
        "Type": PricingRuleTypeType,
        "ModifierPercentage": float,
        "Service": str,
        "AssociatedPricingPlanCount": int,
        "LastModifiedTime": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateResourceResponseElementTypeDef = TypedDict(
    "AssociateResourceResponseElementTypeDef",
    {
        "Arn": str,
        "Error": AssociateResourceErrorTypeDef,
    },
    total=False,
)

DisassociateResourceResponseElementTypeDef = TypedDict(
    "DisassociateResourceResponseElementTypeDef",
    {
        "Arn": str,
        "Error": AssociateResourceErrorTypeDef,
    },
    total=False,
)

_RequiredBatchAssociateResourcesToCustomLineItemInputRequestTypeDef = TypedDict(
    "_RequiredBatchAssociateResourcesToCustomLineItemInputRequestTypeDef",
    {
        "TargetArn": str,
        "ResourceArns": Sequence[str],
    },
)
_OptionalBatchAssociateResourcesToCustomLineItemInputRequestTypeDef = TypedDict(
    "_OptionalBatchAssociateResourcesToCustomLineItemInputRequestTypeDef",
    {
        "BillingPeriodRange": CustomLineItemBillingPeriodRangeTypeDef,
    },
    total=False,
)


class BatchAssociateResourcesToCustomLineItemInputRequestTypeDef(
    _RequiredBatchAssociateResourcesToCustomLineItemInputRequestTypeDef,
    _OptionalBatchAssociateResourcesToCustomLineItemInputRequestTypeDef,
):
    pass


_RequiredBatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef = TypedDict(
    "_RequiredBatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef",
    {
        "TargetArn": str,
        "ResourceArns": Sequence[str],
    },
)
_OptionalBatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef = TypedDict(
    "_OptionalBatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef",
    {
        "BillingPeriodRange": CustomLineItemBillingPeriodRangeTypeDef,
    },
    total=False,
)


class BatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef(
    _RequiredBatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef,
    _OptionalBatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef,
):
    pass


_RequiredDeleteCustomLineItemInputRequestTypeDef = TypedDict(
    "_RequiredDeleteCustomLineItemInputRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalDeleteCustomLineItemInputRequestTypeDef = TypedDict(
    "_OptionalDeleteCustomLineItemInputRequestTypeDef",
    {
        "BillingPeriodRange": CustomLineItemBillingPeriodRangeTypeDef,
    },
    total=False,
)


class DeleteCustomLineItemInputRequestTypeDef(
    _RequiredDeleteCustomLineItemInputRequestTypeDef,
    _OptionalDeleteCustomLineItemInputRequestTypeDef,
):
    pass


ListBillingGroupCostReportsOutputTypeDef = TypedDict(
    "ListBillingGroupCostReportsOutputTypeDef",
    {
        "BillingGroupCostReports": List[BillingGroupCostReportElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BillingGroupListElementTypeDef = TypedDict(
    "BillingGroupListElementTypeDef",
    {
        "Name": str,
        "Arn": str,
        "Description": str,
        "PrimaryAccountId": str,
        "ComputationPreference": ComputationPreferenceTypeDef,
        "Size": int,
        "CreationTime": int,
        "LastModifiedTime": int,
        "Status": BillingGroupStatusType,
        "StatusReason": str,
    },
    total=False,
)

_RequiredCreateBillingGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateBillingGroupInputRequestTypeDef",
    {
        "Name": str,
        "AccountGrouping": AccountGroupingTypeDef,
        "ComputationPreference": ComputationPreferenceTypeDef,
    },
)
_OptionalCreateBillingGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateBillingGroupInputRequestTypeDef",
    {
        "ClientToken": str,
        "PrimaryAccountId": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateBillingGroupInputRequestTypeDef(
    _RequiredCreateBillingGroupInputRequestTypeDef, _OptionalCreateBillingGroupInputRequestTypeDef
):
    pass


_RequiredUpdateBillingGroupInputRequestTypeDef = TypedDict(
    "_RequiredUpdateBillingGroupInputRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalUpdateBillingGroupInputRequestTypeDef = TypedDict(
    "_OptionalUpdateBillingGroupInputRequestTypeDef",
    {
        "Name": str,
        "Status": BillingGroupStatusType,
        "ComputationPreference": ComputationPreferenceTypeDef,
        "Description": str,
    },
    total=False,
)


class UpdateBillingGroupInputRequestTypeDef(
    _RequiredUpdateBillingGroupInputRequestTypeDef, _OptionalUpdateBillingGroupInputRequestTypeDef
):
    pass


_RequiredCustomLineItemChargeDetailsTypeDef = TypedDict(
    "_RequiredCustomLineItemChargeDetailsTypeDef",
    {
        "Type": CustomLineItemTypeType,
    },
)
_OptionalCustomLineItemChargeDetailsTypeDef = TypedDict(
    "_OptionalCustomLineItemChargeDetailsTypeDef",
    {
        "Flat": CustomLineItemFlatChargeDetailsTypeDef,
        "Percentage": CustomLineItemPercentageChargeDetailsTypeDef,
    },
    total=False,
)


class CustomLineItemChargeDetailsTypeDef(
    _RequiredCustomLineItemChargeDetailsTypeDef, _OptionalCustomLineItemChargeDetailsTypeDef
):
    pass


ListAccountAssociationsInputRequestTypeDef = TypedDict(
    "ListAccountAssociationsInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListAccountAssociationsFilterTypeDef,
        "NextToken": str,
    },
    total=False,
)

ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef = TypedDict(
    "ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListAccountAssociationsFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef = TypedDict(
    "_RequiredListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef",
    {
        "PricingRuleArn": str,
    },
)
_OptionalListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef = TypedDict(
    "_OptionalListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef",
    {
        "BillingPeriod": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef(
    _RequiredListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef,
    _OptionalListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef,
):
    pass


_RequiredListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef = TypedDict(
    "_RequiredListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef",
    {
        "PricingPlanArn": str,
    },
)
_OptionalListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef = TypedDict(
    "_OptionalListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef",
    {
        "BillingPeriod": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef(
    _RequiredListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef,
    _OptionalListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef,
):
    pass


ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef = TypedDict(
    "ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListBillingGroupCostReportsFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListBillingGroupCostReportsInputRequestTypeDef = TypedDict(
    "ListBillingGroupCostReportsInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "MaxResults": int,
        "NextToken": str,
        "Filters": ListBillingGroupCostReportsFilterTypeDef,
    },
    total=False,
)

ListBillingGroupsInputListBillingGroupsPaginateTypeDef = TypedDict(
    "ListBillingGroupsInputListBillingGroupsPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListBillingGroupsFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListBillingGroupsInputRequestTypeDef = TypedDict(
    "ListBillingGroupsInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "MaxResults": int,
        "NextToken": str,
        "Filters": ListBillingGroupsFilterTypeDef,
    },
    total=False,
)

_RequiredListCustomLineItemChargeDetailsTypeDef = TypedDict(
    "_RequiredListCustomLineItemChargeDetailsTypeDef",
    {
        "Type": CustomLineItemTypeType,
    },
)
_OptionalListCustomLineItemChargeDetailsTypeDef = TypedDict(
    "_OptionalListCustomLineItemChargeDetailsTypeDef",
    {
        "Flat": ListCustomLineItemFlatChargeDetailsTypeDef,
        "Percentage": ListCustomLineItemPercentageChargeDetailsTypeDef,
    },
    total=False,
)


class ListCustomLineItemChargeDetailsTypeDef(
    _RequiredListCustomLineItemChargeDetailsTypeDef, _OptionalListCustomLineItemChargeDetailsTypeDef
):
    pass


ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef = TypedDict(
    "ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListCustomLineItemsFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCustomLineItemsInputRequestTypeDef = TypedDict(
    "ListCustomLineItemsInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "MaxResults": int,
        "NextToken": str,
        "Filters": ListCustomLineItemsFilterTypeDef,
    },
    total=False,
)

ListPricingPlansInputListPricingPlansPaginateTypeDef = TypedDict(
    "ListPricingPlansInputListPricingPlansPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListPricingPlansFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPricingPlansInputRequestTypeDef = TypedDict(
    "ListPricingPlansInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListPricingPlansFilterTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListPricingPlansOutputTypeDef = TypedDict(
    "ListPricingPlansOutputTypeDef",
    {
        "BillingPeriod": str,
        "PricingPlans": List[PricingPlanListElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPricingRulesInputListPricingRulesPaginateTypeDef = TypedDict(
    "ListPricingRulesInputListPricingRulesPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListPricingRulesFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPricingRulesInputRequestTypeDef = TypedDict(
    "ListPricingRulesInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListPricingRulesFilterTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListPricingRulesOutputTypeDef = TypedDict(
    "ListPricingRulesOutputTypeDef",
    {
        "BillingPeriod": str,
        "PricingRules": List[PricingRuleListElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef = TypedDict(
    "_RequiredListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef",
    {
        "Arn": str,
    },
)
_OptionalListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef = TypedDict(
    "_OptionalListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef",
    {
        "BillingPeriod": str,
        "Filters": ListResourcesAssociatedToCustomLineItemFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef(
    _RequiredListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef,
    _OptionalListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef,
):
    pass


_RequiredListResourcesAssociatedToCustomLineItemInputRequestTypeDef = TypedDict(
    "_RequiredListResourcesAssociatedToCustomLineItemInputRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalListResourcesAssociatedToCustomLineItemInputRequestTypeDef = TypedDict(
    "_OptionalListResourcesAssociatedToCustomLineItemInputRequestTypeDef",
    {
        "BillingPeriod": str,
        "MaxResults": int,
        "NextToken": str,
        "Filters": ListResourcesAssociatedToCustomLineItemFilterTypeDef,
    },
    total=False,
)


class ListResourcesAssociatedToCustomLineItemInputRequestTypeDef(
    _RequiredListResourcesAssociatedToCustomLineItemInputRequestTypeDef,
    _OptionalListResourcesAssociatedToCustomLineItemInputRequestTypeDef,
):
    pass


ListResourcesAssociatedToCustomLineItemOutputTypeDef = TypedDict(
    "ListResourcesAssociatedToCustomLineItemOutputTypeDef",
    {
        "Arn": str,
        "AssociatedResources": List[ListResourcesAssociatedToCustomLineItemResponseElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomLineItemChargeDetailsTypeDef = TypedDict(
    "UpdateCustomLineItemChargeDetailsTypeDef",
    {
        "Flat": UpdateCustomLineItemFlatChargeDetailsTypeDef,
        "Percentage": UpdateCustomLineItemPercentageChargeDetailsTypeDef,
    },
    total=False,
)

BatchAssociateResourcesToCustomLineItemOutputTypeDef = TypedDict(
    "BatchAssociateResourcesToCustomLineItemOutputTypeDef",
    {
        "SuccessfullyAssociatedResources": List[AssociateResourceResponseElementTypeDef],
        "FailedAssociatedResources": List[AssociateResourceResponseElementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateResourcesFromCustomLineItemOutputTypeDef = TypedDict(
    "BatchDisassociateResourcesFromCustomLineItemOutputTypeDef",
    {
        "SuccessfullyDisassociatedResources": List[DisassociateResourceResponseElementTypeDef],
        "FailedDisassociatedResources": List[DisassociateResourceResponseElementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBillingGroupsOutputTypeDef = TypedDict(
    "ListBillingGroupsOutputTypeDef",
    {
        "BillingGroups": List[BillingGroupListElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateCustomLineItemInputRequestTypeDef = TypedDict(
    "_RequiredCreateCustomLineItemInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "BillingGroupArn": str,
        "ChargeDetails": CustomLineItemChargeDetailsTypeDef,
    },
)
_OptionalCreateCustomLineItemInputRequestTypeDef = TypedDict(
    "_OptionalCreateCustomLineItemInputRequestTypeDef",
    {
        "ClientToken": str,
        "BillingPeriodRange": CustomLineItemBillingPeriodRangeTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateCustomLineItemInputRequestTypeDef(
    _RequiredCreateCustomLineItemInputRequestTypeDef,
    _OptionalCreateCustomLineItemInputRequestTypeDef,
):
    pass


CustomLineItemListElementTypeDef = TypedDict(
    "CustomLineItemListElementTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ChargeDetails": ListCustomLineItemChargeDetailsTypeDef,
        "CurrencyCode": CurrencyCodeType,
        "Description": str,
        "ProductCode": str,
        "BillingGroupArn": str,
        "CreationTime": int,
        "LastModifiedTime": int,
        "AssociationSize": int,
    },
    total=False,
)

UpdateCustomLineItemOutputTypeDef = TypedDict(
    "UpdateCustomLineItemOutputTypeDef",
    {
        "Arn": str,
        "BillingGroupArn": str,
        "Name": str,
        "Description": str,
        "ChargeDetails": ListCustomLineItemChargeDetailsTypeDef,
        "LastModifiedTime": int,
        "AssociationSize": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateCustomLineItemInputRequestTypeDef = TypedDict(
    "_RequiredUpdateCustomLineItemInputRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalUpdateCustomLineItemInputRequestTypeDef = TypedDict(
    "_OptionalUpdateCustomLineItemInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "ChargeDetails": UpdateCustomLineItemChargeDetailsTypeDef,
        "BillingPeriodRange": CustomLineItemBillingPeriodRangeTypeDef,
    },
    total=False,
)


class UpdateCustomLineItemInputRequestTypeDef(
    _RequiredUpdateCustomLineItemInputRequestTypeDef,
    _OptionalUpdateCustomLineItemInputRequestTypeDef,
):
    pass


ListCustomLineItemsOutputTypeDef = TypedDict(
    "ListCustomLineItemsOutputTypeDef",
    {
        "CustomLineItems": List[CustomLineItemListElementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
