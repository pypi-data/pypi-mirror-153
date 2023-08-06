"""
Type annotations for organizations service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_organizations/type_defs/)

Usage::

    ```python
    from mypy_boto3_organizations.type_defs import AcceptHandshakeRequestRequestTypeDef

    data: AcceptHandshakeRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    AccountJoinedMethodType,
    AccountStatusType,
    ActionTypeType,
    ChildTypeType,
    CreateAccountFailureReasonType,
    CreateAccountStateType,
    EffectivePolicyTypeType,
    HandshakePartyTypeType,
    HandshakeResourceTypeType,
    HandshakeStateType,
    IAMUserAccessToBillingType,
    OrganizationFeatureSetType,
    ParentTypeType,
    PolicyTypeStatusType,
    PolicyTypeType,
    TargetTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptHandshakeRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AccountTypeDef",
    "AttachPolicyRequestRequestTypeDef",
    "CancelHandshakeRequestRequestTypeDef",
    "ChildTypeDef",
    "CloseAccountRequestRequestTypeDef",
    "TagTypeDef",
    "CreateAccountStatusTypeDef",
    "CreateOrganizationRequestRequestTypeDef",
    "OrganizationalUnitTypeDef",
    "DeclineHandshakeRequestRequestTypeDef",
    "DelegatedAdministratorTypeDef",
    "DelegatedServiceTypeDef",
    "DeleteOrganizationalUnitRequestRequestTypeDef",
    "DeletePolicyRequestRequestTypeDef",
    "DeregisterDelegatedAdministratorRequestRequestTypeDef",
    "DescribeAccountRequestRequestTypeDef",
    "DescribeCreateAccountStatusRequestRequestTypeDef",
    "DescribeEffectivePolicyRequestRequestTypeDef",
    "EffectivePolicyTypeDef",
    "DescribeHandshakeRequestRequestTypeDef",
    "DescribeOrganizationalUnitRequestRequestTypeDef",
    "DescribePolicyRequestRequestTypeDef",
    "DetachPolicyRequestRequestTypeDef",
    "DisableAWSServiceAccessRequestRequestTypeDef",
    "DisablePolicyTypeRequestRequestTypeDef",
    "EnableAWSServiceAccessRequestRequestTypeDef",
    "EnablePolicyTypeRequestRequestTypeDef",
    "EnabledServicePrincipalTypeDef",
    "HandshakeFilterTypeDef",
    "HandshakePartyTypeDef",
    "HandshakeResourceTypeDef",
    "PaginatorConfigTypeDef",
    "ListAWSServiceAccessForOrganizationRequestRequestTypeDef",
    "ListAccountsForParentRequestRequestTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "ListChildrenRequestRequestTypeDef",
    "ListCreateAccountStatusRequestRequestTypeDef",
    "ListDelegatedAdministratorsRequestRequestTypeDef",
    "ListDelegatedServicesForAccountRequestRequestTypeDef",
    "ListOrganizationalUnitsForParentRequestRequestTypeDef",
    "ListParentsRequestRequestTypeDef",
    "ParentTypeDef",
    "ListPoliciesForTargetRequestRequestTypeDef",
    "PolicySummaryTypeDef",
    "ListPoliciesRequestRequestTypeDef",
    "ListRootsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTargetsForPolicyRequestRequestTypeDef",
    "PolicyTargetSummaryTypeDef",
    "MoveAccountRequestRequestTypeDef",
    "PolicyTypeSummaryTypeDef",
    "RegisterDelegatedAdministratorRequestRequestTypeDef",
    "RemoveAccountFromOrganizationRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateOrganizationalUnitRequestRequestTypeDef",
    "UpdatePolicyRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "DescribeAccountResponseTypeDef",
    "ListAccountsForParentResponseTypeDef",
    "ListAccountsResponseTypeDef",
    "ListChildrenResponseTypeDef",
    "CreateAccountRequestRequestTypeDef",
    "CreateGovCloudAccountRequestRequestTypeDef",
    "CreateOrganizationalUnitRequestRequestTypeDef",
    "CreatePolicyRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateGovCloudAccountResponseTypeDef",
    "DescribeCreateAccountStatusResponseTypeDef",
    "ListCreateAccountStatusResponseTypeDef",
    "CreateOrganizationalUnitResponseTypeDef",
    "DescribeOrganizationalUnitResponseTypeDef",
    "ListOrganizationalUnitsForParentResponseTypeDef",
    "UpdateOrganizationalUnitResponseTypeDef",
    "ListDelegatedAdministratorsResponseTypeDef",
    "ListDelegatedServicesForAccountResponseTypeDef",
    "DescribeEffectivePolicyResponseTypeDef",
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    "ListHandshakesForAccountRequestRequestTypeDef",
    "ListHandshakesForOrganizationRequestRequestTypeDef",
    "HandshakeTypeDef",
    "InviteAccountToOrganizationRequestRequestTypeDef",
    "ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef",
    "ListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    "ListAccountsRequestListAccountsPaginateTypeDef",
    "ListChildrenRequestListChildrenPaginateTypeDef",
    "ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef",
    "ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef",
    "ListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    "ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef",
    "ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef",
    "ListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    "ListParentsRequestListParentsPaginateTypeDef",
    "ListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    "ListRootsRequestListRootsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    "ListParentsResponseTypeDef",
    "ListPoliciesForTargetResponseTypeDef",
    "ListPoliciesResponseTypeDef",
    "PolicyTypeDef",
    "ListTargetsForPolicyResponseTypeDef",
    "OrganizationTypeDef",
    "RootTypeDef",
    "AcceptHandshakeResponseTypeDef",
    "CancelHandshakeResponseTypeDef",
    "DeclineHandshakeResponseTypeDef",
    "DescribeHandshakeResponseTypeDef",
    "EnableAllFeaturesResponseTypeDef",
    "InviteAccountToOrganizationResponseTypeDef",
    "ListHandshakesForAccountResponseTypeDef",
    "ListHandshakesForOrganizationResponseTypeDef",
    "CreatePolicyResponseTypeDef",
    "DescribePolicyResponseTypeDef",
    "UpdatePolicyResponseTypeDef",
    "CreateOrganizationResponseTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DisablePolicyTypeResponseTypeDef",
    "EnablePolicyTypeResponseTypeDef",
    "ListRootsResponseTypeDef",
)

AcceptHandshakeRequestRequestTypeDef = TypedDict(
    "AcceptHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
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

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Email": str,
        "Name": str,
        "Status": AccountStatusType,
        "JoinedMethod": AccountJoinedMethodType,
        "JoinedTimestamp": datetime,
    },
    total=False,
)

AttachPolicyRequestRequestTypeDef = TypedDict(
    "AttachPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
        "TargetId": str,
    },
)

CancelHandshakeRequestRequestTypeDef = TypedDict(
    "CancelHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

ChildTypeDef = TypedDict(
    "ChildTypeDef",
    {
        "Id": str,
        "Type": ChildTypeType,
    },
    total=False,
)

CloseAccountRequestRequestTypeDef = TypedDict(
    "CloseAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CreateAccountStatusTypeDef = TypedDict(
    "CreateAccountStatusTypeDef",
    {
        "Id": str,
        "AccountName": str,
        "State": CreateAccountStateType,
        "RequestedTimestamp": datetime,
        "CompletedTimestamp": datetime,
        "AccountId": str,
        "GovCloudAccountId": str,
        "FailureReason": CreateAccountFailureReasonType,
    },
    total=False,
)

CreateOrganizationRequestRequestTypeDef = TypedDict(
    "CreateOrganizationRequestRequestTypeDef",
    {
        "FeatureSet": OrganizationFeatureSetType,
    },
    total=False,
)

OrganizationalUnitTypeDef = TypedDict(
    "OrganizationalUnitTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

DeclineHandshakeRequestRequestTypeDef = TypedDict(
    "DeclineHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

DelegatedAdministratorTypeDef = TypedDict(
    "DelegatedAdministratorTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Email": str,
        "Name": str,
        "Status": AccountStatusType,
        "JoinedMethod": AccountJoinedMethodType,
        "JoinedTimestamp": datetime,
        "DelegationEnabledDate": datetime,
    },
    total=False,
)

DelegatedServiceTypeDef = TypedDict(
    "DelegatedServiceTypeDef",
    {
        "ServicePrincipal": str,
        "DelegationEnabledDate": datetime,
    },
    total=False,
)

DeleteOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "DeleteOrganizationalUnitRequestRequestTypeDef",
    {
        "OrganizationalUnitId": str,
    },
)

DeletePolicyRequestRequestTypeDef = TypedDict(
    "DeletePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

DeregisterDelegatedAdministratorRequestRequestTypeDef = TypedDict(
    "DeregisterDelegatedAdministratorRequestRequestTypeDef",
    {
        "AccountId": str,
        "ServicePrincipal": str,
    },
)

DescribeAccountRequestRequestTypeDef = TypedDict(
    "DescribeAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

DescribeCreateAccountStatusRequestRequestTypeDef = TypedDict(
    "DescribeCreateAccountStatusRequestRequestTypeDef",
    {
        "CreateAccountRequestId": str,
    },
)

_RequiredDescribeEffectivePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEffectivePolicyRequestRequestTypeDef",
    {
        "PolicyType": EffectivePolicyTypeType,
    },
)
_OptionalDescribeEffectivePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEffectivePolicyRequestRequestTypeDef",
    {
        "TargetId": str,
    },
    total=False,
)


class DescribeEffectivePolicyRequestRequestTypeDef(
    _RequiredDescribeEffectivePolicyRequestRequestTypeDef,
    _OptionalDescribeEffectivePolicyRequestRequestTypeDef,
):
    pass


EffectivePolicyTypeDef = TypedDict(
    "EffectivePolicyTypeDef",
    {
        "PolicyContent": str,
        "LastUpdatedTimestamp": datetime,
        "TargetId": str,
        "PolicyType": EffectivePolicyTypeType,
    },
    total=False,
)

DescribeHandshakeRequestRequestTypeDef = TypedDict(
    "DescribeHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

DescribeOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "DescribeOrganizationalUnitRequestRequestTypeDef",
    {
        "OrganizationalUnitId": str,
    },
)

DescribePolicyRequestRequestTypeDef = TypedDict(
    "DescribePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

DetachPolicyRequestRequestTypeDef = TypedDict(
    "DetachPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
        "TargetId": str,
    },
)

DisableAWSServiceAccessRequestRequestTypeDef = TypedDict(
    "DisableAWSServiceAccessRequestRequestTypeDef",
    {
        "ServicePrincipal": str,
    },
)

DisablePolicyTypeRequestRequestTypeDef = TypedDict(
    "DisablePolicyTypeRequestRequestTypeDef",
    {
        "RootId": str,
        "PolicyType": PolicyTypeType,
    },
)

EnableAWSServiceAccessRequestRequestTypeDef = TypedDict(
    "EnableAWSServiceAccessRequestRequestTypeDef",
    {
        "ServicePrincipal": str,
    },
)

EnablePolicyTypeRequestRequestTypeDef = TypedDict(
    "EnablePolicyTypeRequestRequestTypeDef",
    {
        "RootId": str,
        "PolicyType": PolicyTypeType,
    },
)

EnabledServicePrincipalTypeDef = TypedDict(
    "EnabledServicePrincipalTypeDef",
    {
        "ServicePrincipal": str,
        "DateEnabled": datetime,
    },
    total=False,
)

HandshakeFilterTypeDef = TypedDict(
    "HandshakeFilterTypeDef",
    {
        "ActionType": ActionTypeType,
        "ParentHandshakeId": str,
    },
    total=False,
)

HandshakePartyTypeDef = TypedDict(
    "HandshakePartyTypeDef",
    {
        "Id": str,
        "Type": HandshakePartyTypeType,
    },
)

HandshakeResourceTypeDef = TypedDict(
    "HandshakeResourceTypeDef",
    {
        "Value": str,
        "Type": HandshakeResourceTypeType,
        "Resources": List[Dict[str, Any]],
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

ListAWSServiceAccessForOrganizationRequestRequestTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListAccountsForParentRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountsForParentRequestRequestTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListAccountsForParentRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountsForParentRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAccountsForParentRequestRequestTypeDef(
    _RequiredListAccountsForParentRequestRequestTypeDef,
    _OptionalListAccountsForParentRequestRequestTypeDef,
):
    pass


ListAccountsRequestRequestTypeDef = TypedDict(
    "ListAccountsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListChildrenRequestRequestTypeDef = TypedDict(
    "_RequiredListChildrenRequestRequestTypeDef",
    {
        "ParentId": str,
        "ChildType": ChildTypeType,
    },
)
_OptionalListChildrenRequestRequestTypeDef = TypedDict(
    "_OptionalListChildrenRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListChildrenRequestRequestTypeDef(
    _RequiredListChildrenRequestRequestTypeDef, _OptionalListChildrenRequestRequestTypeDef
):
    pass


ListCreateAccountStatusRequestRequestTypeDef = TypedDict(
    "ListCreateAccountStatusRequestRequestTypeDef",
    {
        "States": Sequence[CreateAccountStateType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDelegatedAdministratorsRequestRequestTypeDef = TypedDict(
    "ListDelegatedAdministratorsRequestRequestTypeDef",
    {
        "ServicePrincipal": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListDelegatedServicesForAccountRequestRequestTypeDef = TypedDict(
    "_RequiredListDelegatedServicesForAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListDelegatedServicesForAccountRequestRequestTypeDef = TypedDict(
    "_OptionalListDelegatedServicesForAccountRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDelegatedServicesForAccountRequestRequestTypeDef(
    _RequiredListDelegatedServicesForAccountRequestRequestTypeDef,
    _OptionalListDelegatedServicesForAccountRequestRequestTypeDef,
):
    pass


_RequiredListOrganizationalUnitsForParentRequestRequestTypeDef = TypedDict(
    "_RequiredListOrganizationalUnitsForParentRequestRequestTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListOrganizationalUnitsForParentRequestRequestTypeDef = TypedDict(
    "_OptionalListOrganizationalUnitsForParentRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListOrganizationalUnitsForParentRequestRequestTypeDef(
    _RequiredListOrganizationalUnitsForParentRequestRequestTypeDef,
    _OptionalListOrganizationalUnitsForParentRequestRequestTypeDef,
):
    pass


_RequiredListParentsRequestRequestTypeDef = TypedDict(
    "_RequiredListParentsRequestRequestTypeDef",
    {
        "ChildId": str,
    },
)
_OptionalListParentsRequestRequestTypeDef = TypedDict(
    "_OptionalListParentsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListParentsRequestRequestTypeDef(
    _RequiredListParentsRequestRequestTypeDef, _OptionalListParentsRequestRequestTypeDef
):
    pass


ParentTypeDef = TypedDict(
    "ParentTypeDef",
    {
        "Id": str,
        "Type": ParentTypeType,
    },
    total=False,
)

_RequiredListPoliciesForTargetRequestRequestTypeDef = TypedDict(
    "_RequiredListPoliciesForTargetRequestRequestTypeDef",
    {
        "TargetId": str,
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesForTargetRequestRequestTypeDef = TypedDict(
    "_OptionalListPoliciesForTargetRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPoliciesForTargetRequestRequestTypeDef(
    _RequiredListPoliciesForTargetRequestRequestTypeDef,
    _OptionalListPoliciesForTargetRequestRequestTypeDef,
):
    pass


PolicySummaryTypeDef = TypedDict(
    "PolicySummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "Type": PolicyTypeType,
        "AwsManaged": bool,
    },
    total=False,
)

_RequiredListPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListPoliciesRequestRequestTypeDef",
    {
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListPoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPoliciesRequestRequestTypeDef(
    _RequiredListPoliciesRequestRequestTypeDef, _OptionalListPoliciesRequestRequestTypeDef
):
    pass


ListRootsRequestRequestTypeDef = TypedDict(
    "ListRootsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


_RequiredListTargetsForPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredListTargetsForPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalListTargetsForPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalListTargetsForPolicyRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTargetsForPolicyRequestRequestTypeDef(
    _RequiredListTargetsForPolicyRequestRequestTypeDef,
    _OptionalListTargetsForPolicyRequestRequestTypeDef,
):
    pass


PolicyTargetSummaryTypeDef = TypedDict(
    "PolicyTargetSummaryTypeDef",
    {
        "TargetId": str,
        "Arn": str,
        "Name": str,
        "Type": TargetTypeType,
    },
    total=False,
)

MoveAccountRequestRequestTypeDef = TypedDict(
    "MoveAccountRequestRequestTypeDef",
    {
        "AccountId": str,
        "SourceParentId": str,
        "DestinationParentId": str,
    },
)

PolicyTypeSummaryTypeDef = TypedDict(
    "PolicyTypeSummaryTypeDef",
    {
        "Type": PolicyTypeType,
        "Status": PolicyTypeStatusType,
    },
    total=False,
)

RegisterDelegatedAdministratorRequestRequestTypeDef = TypedDict(
    "RegisterDelegatedAdministratorRequestRequestTypeDef",
    {
        "AccountId": str,
        "ServicePrincipal": str,
    },
)

RemoveAccountFromOrganizationRequestRequestTypeDef = TypedDict(
    "RemoveAccountFromOrganizationRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOrganizationalUnitRequestRequestTypeDef",
    {
        "OrganizationalUnitId": str,
    },
)
_OptionalUpdateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOrganizationalUnitRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateOrganizationalUnitRequestRequestTypeDef(
    _RequiredUpdateOrganizationalUnitRequestRequestTypeDef,
    _OptionalUpdateOrganizationalUnitRequestRequestTypeDef,
):
    pass


_RequiredUpdatePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalUpdatePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePolicyRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Content": str,
    },
    total=False,
)


class UpdatePolicyRequestRequestTypeDef(
    _RequiredUpdatePolicyRequestRequestTypeDef, _OptionalUpdatePolicyRequestRequestTypeDef
):
    pass


EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountResponseTypeDef = TypedDict(
    "DescribeAccountResponseTypeDef",
    {
        "Account": AccountTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountsForParentResponseTypeDef = TypedDict(
    "ListAccountsForParentResponseTypeDef",
    {
        "Accounts": List[AccountTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef",
    {
        "Accounts": List[AccountTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChildrenResponseTypeDef = TypedDict(
    "ListChildrenResponseTypeDef",
    {
        "Children": List[ChildTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAccountRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccountRequestRequestTypeDef",
    {
        "Email": str,
        "AccountName": str,
    },
)
_OptionalCreateAccountRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccountRequestRequestTypeDef",
    {
        "RoleName": str,
        "IamUserAccessToBilling": IAMUserAccessToBillingType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAccountRequestRequestTypeDef(
    _RequiredCreateAccountRequestRequestTypeDef, _OptionalCreateAccountRequestRequestTypeDef
):
    pass


_RequiredCreateGovCloudAccountRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGovCloudAccountRequestRequestTypeDef",
    {
        "Email": str,
        "AccountName": str,
    },
)
_OptionalCreateGovCloudAccountRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGovCloudAccountRequestRequestTypeDef",
    {
        "RoleName": str,
        "IamUserAccessToBilling": IAMUserAccessToBillingType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGovCloudAccountRequestRequestTypeDef(
    _RequiredCreateGovCloudAccountRequestRequestTypeDef,
    _OptionalCreateGovCloudAccountRequestRequestTypeDef,
):
    pass


_RequiredCreateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOrganizationalUnitRequestRequestTypeDef",
    {
        "ParentId": str,
        "Name": str,
    },
)
_OptionalCreateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOrganizationalUnitRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateOrganizationalUnitRequestRequestTypeDef(
    _RequiredCreateOrganizationalUnitRequestRequestTypeDef,
    _OptionalCreateOrganizationalUnitRequestRequestTypeDef,
):
    pass


_RequiredCreatePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyRequestRequestTypeDef",
    {
        "Content": str,
        "Description": str,
        "Name": str,
        "Type": PolicyTypeType,
    },
)
_OptionalCreatePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePolicyRequestRequestTypeDef(
    _RequiredCreatePolicyRequestRequestTypeDef, _OptionalCreatePolicyRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateAccountResponseTypeDef = TypedDict(
    "CreateAccountResponseTypeDef",
    {
        "CreateAccountStatus": CreateAccountStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGovCloudAccountResponseTypeDef = TypedDict(
    "CreateGovCloudAccountResponseTypeDef",
    {
        "CreateAccountStatus": CreateAccountStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCreateAccountStatusResponseTypeDef = TypedDict(
    "DescribeCreateAccountStatusResponseTypeDef",
    {
        "CreateAccountStatus": CreateAccountStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCreateAccountStatusResponseTypeDef = TypedDict(
    "ListCreateAccountStatusResponseTypeDef",
    {
        "CreateAccountStatuses": List[CreateAccountStatusTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOrganizationalUnitResponseTypeDef = TypedDict(
    "CreateOrganizationalUnitResponseTypeDef",
    {
        "OrganizationalUnit": OrganizationalUnitTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationalUnitResponseTypeDef = TypedDict(
    "DescribeOrganizationalUnitResponseTypeDef",
    {
        "OrganizationalUnit": OrganizationalUnitTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOrganizationalUnitsForParentResponseTypeDef = TypedDict(
    "ListOrganizationalUnitsForParentResponseTypeDef",
    {
        "OrganizationalUnits": List[OrganizationalUnitTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateOrganizationalUnitResponseTypeDef = TypedDict(
    "UpdateOrganizationalUnitResponseTypeDef",
    {
        "OrganizationalUnit": OrganizationalUnitTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDelegatedAdministratorsResponseTypeDef = TypedDict(
    "ListDelegatedAdministratorsResponseTypeDef",
    {
        "DelegatedAdministrators": List[DelegatedAdministratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDelegatedServicesForAccountResponseTypeDef = TypedDict(
    "ListDelegatedServicesForAccountResponseTypeDef",
    {
        "DelegatedServices": List[DelegatedServiceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEffectivePolicyResponseTypeDef = TypedDict(
    "DescribeEffectivePolicyResponseTypeDef",
    {
        "EffectivePolicy": EffectivePolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAWSServiceAccessForOrganizationResponseTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    {
        "EnabledServicePrincipals": List[EnabledServicePrincipalTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHandshakesForAccountRequestRequestTypeDef = TypedDict(
    "ListHandshakesForAccountRequestRequestTypeDef",
    {
        "Filter": HandshakeFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListHandshakesForOrganizationRequestRequestTypeDef = TypedDict(
    "ListHandshakesForOrganizationRequestRequestTypeDef",
    {
        "Filter": HandshakeFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

HandshakeTypeDef = TypedDict(
    "HandshakeTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Parties": List[HandshakePartyTypeDef],
        "State": HandshakeStateType,
        "RequestedTimestamp": datetime,
        "ExpirationTimestamp": datetime,
        "Action": ActionTypeType,
        "Resources": List["HandshakeResourceTypeDef"],
    },
    total=False,
)

_RequiredInviteAccountToOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredInviteAccountToOrganizationRequestRequestTypeDef",
    {
        "Target": HandshakePartyTypeDef,
    },
)
_OptionalInviteAccountToOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalInviteAccountToOrganizationRequestRequestTypeDef",
    {
        "Notes": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class InviteAccountToOrganizationRequestRequestTypeDef(
    _RequiredInviteAccountToOrganizationRequestRequestTypeDef,
    _OptionalInviteAccountToOrganizationRequestRequestTypeDef,
):
    pass


ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAccountsForParentRequestListAccountsForParentPaginateTypeDef = TypedDict(
    "_RequiredListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListAccountsForParentRequestListAccountsForParentPaginateTypeDef = TypedDict(
    "_OptionalListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccountsForParentRequestListAccountsForParentPaginateTypeDef(
    _RequiredListAccountsForParentRequestListAccountsForParentPaginateTypeDef,
    _OptionalListAccountsForParentRequestListAccountsForParentPaginateTypeDef,
):
    pass


ListAccountsRequestListAccountsPaginateTypeDef = TypedDict(
    "ListAccountsRequestListAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListChildrenRequestListChildrenPaginateTypeDef = TypedDict(
    "_RequiredListChildrenRequestListChildrenPaginateTypeDef",
    {
        "ParentId": str,
        "ChildType": ChildTypeType,
    },
)
_OptionalListChildrenRequestListChildrenPaginateTypeDef = TypedDict(
    "_OptionalListChildrenRequestListChildrenPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListChildrenRequestListChildrenPaginateTypeDef(
    _RequiredListChildrenRequestListChildrenPaginateTypeDef,
    _OptionalListChildrenRequestListChildrenPaginateTypeDef,
):
    pass


ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef = TypedDict(
    "ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef",
    {
        "States": Sequence[CreateAccountStateType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef = TypedDict(
    "ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef",
    {
        "ServicePrincipal": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef = TypedDict(
    "_RequiredListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef = TypedDict(
    "_OptionalListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef(
    _RequiredListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef,
    _OptionalListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef,
):
    pass


ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef = TypedDict(
    "ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef",
    {
        "Filter": HandshakeFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef = TypedDict(
    "ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef",
    {
        "Filter": HandshakeFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef = TypedDict(
    "_RequiredListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef = TypedDict(
    "_OptionalListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef(
    _RequiredListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef,
    _OptionalListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef,
):
    pass


_RequiredListParentsRequestListParentsPaginateTypeDef = TypedDict(
    "_RequiredListParentsRequestListParentsPaginateTypeDef",
    {
        "ChildId": str,
    },
)
_OptionalListParentsRequestListParentsPaginateTypeDef = TypedDict(
    "_OptionalListParentsRequestListParentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListParentsRequestListParentsPaginateTypeDef(
    _RequiredListParentsRequestListParentsPaginateTypeDef,
    _OptionalListParentsRequestListParentsPaginateTypeDef,
):
    pass


_RequiredListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef = TypedDict(
    "_RequiredListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    {
        "TargetId": str,
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef = TypedDict(
    "_OptionalListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef(
    _RequiredListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef,
    _OptionalListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef,
):
    pass


_RequiredListPoliciesRequestListPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListPoliciesRequestListPoliciesPaginateTypeDef",
    {
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesRequestListPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListPoliciesRequestListPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPoliciesRequestListPoliciesPaginateTypeDef(
    _RequiredListPoliciesRequestListPoliciesPaginateTypeDef,
    _OptionalListPoliciesRequestListPoliciesPaginateTypeDef,
):
    pass


ListRootsRequestListRootsPaginateTypeDef = TypedDict(
    "ListRootsRequestListRootsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef = TypedDict(
    "_RequiredListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef = TypedDict(
    "_OptionalListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef(
    _RequiredListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef,
    _OptionalListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef,
):
    pass


ListParentsResponseTypeDef = TypedDict(
    "ListParentsResponseTypeDef",
    {
        "Parents": List[ParentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPoliciesForTargetResponseTypeDef = TypedDict(
    "ListPoliciesForTargetResponseTypeDef",
    {
        "Policies": List[PolicySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {
        "Policies": List[PolicySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "PolicySummary": PolicySummaryTypeDef,
        "Content": str,
    },
    total=False,
)

ListTargetsForPolicyResponseTypeDef = TypedDict(
    "ListTargetsForPolicyResponseTypeDef",
    {
        "Targets": List[PolicyTargetSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OrganizationTypeDef = TypedDict(
    "OrganizationTypeDef",
    {
        "Id": str,
        "Arn": str,
        "FeatureSet": OrganizationFeatureSetType,
        "MasterAccountArn": str,
        "MasterAccountId": str,
        "MasterAccountEmail": str,
        "AvailablePolicyTypes": List[PolicyTypeSummaryTypeDef],
    },
    total=False,
)

RootTypeDef = TypedDict(
    "RootTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "PolicyTypes": List[PolicyTypeSummaryTypeDef],
    },
    total=False,
)

AcceptHandshakeResponseTypeDef = TypedDict(
    "AcceptHandshakeResponseTypeDef",
    {
        "Handshake": HandshakeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelHandshakeResponseTypeDef = TypedDict(
    "CancelHandshakeResponseTypeDef",
    {
        "Handshake": HandshakeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeclineHandshakeResponseTypeDef = TypedDict(
    "DeclineHandshakeResponseTypeDef",
    {
        "Handshake": HandshakeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHandshakeResponseTypeDef = TypedDict(
    "DescribeHandshakeResponseTypeDef",
    {
        "Handshake": HandshakeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableAllFeaturesResponseTypeDef = TypedDict(
    "EnableAllFeaturesResponseTypeDef",
    {
        "Handshake": HandshakeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InviteAccountToOrganizationResponseTypeDef = TypedDict(
    "InviteAccountToOrganizationResponseTypeDef",
    {
        "Handshake": HandshakeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHandshakesForAccountResponseTypeDef = TypedDict(
    "ListHandshakesForAccountResponseTypeDef",
    {
        "Handshakes": List[HandshakeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHandshakesForOrganizationResponseTypeDef = TypedDict(
    "ListHandshakesForOrganizationResponseTypeDef",
    {
        "Handshakes": List[HandshakeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePolicyResponseTypeDef = TypedDict(
    "CreatePolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePolicyResponseTypeDef = TypedDict(
    "DescribePolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePolicyResponseTypeDef = TypedDict(
    "UpdatePolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOrganizationResponseTypeDef = TypedDict(
    "CreateOrganizationResponseTypeDef",
    {
        "Organization": OrganizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationResponseTypeDef = TypedDict(
    "DescribeOrganizationResponseTypeDef",
    {
        "Organization": OrganizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisablePolicyTypeResponseTypeDef = TypedDict(
    "DisablePolicyTypeResponseTypeDef",
    {
        "Root": RootTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnablePolicyTypeResponseTypeDef = TypedDict(
    "EnablePolicyTypeResponseTypeDef",
    {
        "Root": RootTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRootsResponseTypeDef = TypedDict(
    "ListRootsResponseTypeDef",
    {
        "Roots": List[RootTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
