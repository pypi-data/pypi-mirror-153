"""
Type annotations for sso-admin service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/type_defs/)

Usage::

    ```python
    from mypy_boto3_sso_admin.type_defs import AccessControlAttributeValueTypeDef

    data: AccessControlAttributeValueTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    InstanceAccessControlAttributeConfigurationStatusType,
    PrincipalTypeType,
    ProvisioningStatusType,
    ProvisionTargetTypeType,
    StatusValuesType,
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
    "AccessControlAttributeValueTypeDef",
    "AccountAssignmentOperationStatusMetadataTypeDef",
    "AccountAssignmentOperationStatusTypeDef",
    "AccountAssignmentTypeDef",
    "AttachManagedPolicyToPermissionSetRequestRequestTypeDef",
    "AttachedManagedPolicyTypeDef",
    "CreateAccountAssignmentRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "PermissionSetTypeDef",
    "DeleteAccountAssignmentRequestRequestTypeDef",
    "DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef",
    "DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DeletePermissionSetRequestRequestTypeDef",
    "DescribeAccountAssignmentCreationStatusRequestRequestTypeDef",
    "DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DescribePermissionSetProvisioningStatusRequestRequestTypeDef",
    "PermissionSetProvisioningStatusTypeDef",
    "DescribePermissionSetRequestRequestTypeDef",
    "DetachManagedPolicyFromPermissionSetRequestRequestTypeDef",
    "GetInlinePolicyForPermissionSetRequestRequestTypeDef",
    "InstanceMetadataTypeDef",
    "OperationStatusFilterTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccountAssignmentsRequestRequestTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestRequestTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListManagedPoliciesInPermissionSetRequestRequestTypeDef",
    "PermissionSetProvisioningStatusMetadataTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestRequestTypeDef",
    "ListPermissionSetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ProvisionPermissionSetRequestRequestTypeDef",
    "PutInlinePolicyToPermissionSetRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePermissionSetRequestRequestTypeDef",
    "AccessControlAttributeTypeDef",
    "CreateAccountAssignmentResponseTypeDef",
    "DeleteAccountAssignmentResponseTypeDef",
    "DescribeAccountAssignmentCreationStatusResponseTypeDef",
    "DescribeAccountAssignmentDeletionStatusResponseTypeDef",
    "GetInlinePolicyForPermissionSetResponseTypeDef",
    "ListAccountAssignmentCreationStatusResponseTypeDef",
    "ListAccountAssignmentDeletionStatusResponseTypeDef",
    "ListAccountAssignmentsResponseTypeDef",
    "ListAccountsForProvisionedPermissionSetResponseTypeDef",
    "ListManagedPoliciesInPermissionSetResponseTypeDef",
    "ListPermissionSetsProvisionedToAccountResponseTypeDef",
    "ListPermissionSetsResponseTypeDef",
    "CreatePermissionSetRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreatePermissionSetResponseTypeDef",
    "DescribePermissionSetResponseTypeDef",
    "DescribePermissionSetProvisioningStatusResponseTypeDef",
    "ProvisionPermissionSetResponseTypeDef",
    "ListInstancesResponseTypeDef",
    "ListAccountAssignmentCreationStatusRequestRequestTypeDef",
    "ListAccountAssignmentDeletionStatusRequestRequestTypeDef",
    "ListPermissionSetProvisioningStatusRequestRequestTypeDef",
    "ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef",
    "ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef",
    "ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef",
    "ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef",
    "ListPermissionSetsRequestListPermissionSetsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListPermissionSetProvisioningStatusResponseTypeDef",
    "InstanceAccessControlAttributeConfigurationTypeDef",
    "CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef",
    "UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
)

AccessControlAttributeValueTypeDef = TypedDict(
    "AccessControlAttributeValueTypeDef",
    {
        "Source": Sequence[str],
    },
)

AccountAssignmentOperationStatusMetadataTypeDef = TypedDict(
    "AccountAssignmentOperationStatusMetadataTypeDef",
    {
        "Status": StatusValuesType,
        "RequestId": str,
        "CreatedDate": datetime,
    },
    total=False,
)

AccountAssignmentOperationStatusTypeDef = TypedDict(
    "AccountAssignmentOperationStatusTypeDef",
    {
        "Status": StatusValuesType,
        "RequestId": str,
        "FailureReason": str,
        "TargetId": str,
        "TargetType": Literal["AWS_ACCOUNT"],
        "PermissionSetArn": str,
        "PrincipalType": PrincipalTypeType,
        "PrincipalId": str,
        "CreatedDate": datetime,
    },
    total=False,
)

AccountAssignmentTypeDef = TypedDict(
    "AccountAssignmentTypeDef",
    {
        "AccountId": str,
        "PermissionSetArn": str,
        "PrincipalType": PrincipalTypeType,
        "PrincipalId": str,
    },
    total=False,
)

AttachManagedPolicyToPermissionSetRequestRequestTypeDef = TypedDict(
    "AttachManagedPolicyToPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "ManagedPolicyArn": str,
    },
)

AttachedManagedPolicyTypeDef = TypedDict(
    "AttachedManagedPolicyTypeDef",
    {
        "Name": str,
        "Arn": str,
    },
    total=False,
)

CreateAccountAssignmentRequestRequestTypeDef = TypedDict(
    "CreateAccountAssignmentRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "TargetId": str,
        "TargetType": Literal["AWS_ACCOUNT"],
        "PermissionSetArn": str,
        "PrincipalType": PrincipalTypeType,
        "PrincipalId": str,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

PermissionSetTypeDef = TypedDict(
    "PermissionSetTypeDef",
    {
        "Name": str,
        "PermissionSetArn": str,
        "Description": str,
        "CreatedDate": datetime,
        "SessionDuration": str,
        "RelayState": str,
    },
    total=False,
)

DeleteAccountAssignmentRequestRequestTypeDef = TypedDict(
    "DeleteAccountAssignmentRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "TargetId": str,
        "TargetType": Literal["AWS_ACCOUNT"],
        "PermissionSetArn": str,
        "PrincipalType": PrincipalTypeType,
        "PrincipalId": str,
    },
)

DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef = TypedDict(
    "DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)

DeletePermissionSetRequestRequestTypeDef = TypedDict(
    "DeletePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DescribeAccountAssignmentCreationStatusRequestRequestTypeDef = TypedDict(
    "DescribeAccountAssignmentCreationStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "AccountAssignmentCreationRequestId": str,
    },
)

DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef = TypedDict(
    "DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "AccountAssignmentDeletionRequestId": str,
    },
)

DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)

DescribePermissionSetProvisioningStatusRequestRequestTypeDef = TypedDict(
    "DescribePermissionSetProvisioningStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ProvisionPermissionSetRequestId": str,
    },
)

PermissionSetProvisioningStatusTypeDef = TypedDict(
    "PermissionSetProvisioningStatusTypeDef",
    {
        "Status": StatusValuesType,
        "RequestId": str,
        "AccountId": str,
        "PermissionSetArn": str,
        "FailureReason": str,
        "CreatedDate": datetime,
    },
    total=False,
)

DescribePermissionSetRequestRequestTypeDef = TypedDict(
    "DescribePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DetachManagedPolicyFromPermissionSetRequestRequestTypeDef = TypedDict(
    "DetachManagedPolicyFromPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "ManagedPolicyArn": str,
    },
)

GetInlinePolicyForPermissionSetRequestRequestTypeDef = TypedDict(
    "GetInlinePolicyForPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

InstanceMetadataTypeDef = TypedDict(
    "InstanceMetadataTypeDef",
    {
        "InstanceArn": str,
        "IdentityStoreId": str,
    },
    total=False,
)

OperationStatusFilterTypeDef = TypedDict(
    "OperationStatusFilterTypeDef",
    {
        "Status": StatusValuesType,
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

_RequiredListAccountAssignmentsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountAssignmentsRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "AccountId": str,
        "PermissionSetArn": str,
    },
)
_OptionalListAccountAssignmentsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountAssignmentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAccountAssignmentsRequestRequestTypeDef(
    _RequiredListAccountAssignmentsRequestRequestTypeDef,
    _OptionalListAccountAssignmentsRequestRequestTypeDef,
):
    pass


_RequiredListAccountsForProvisionedPermissionSetRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountsForProvisionedPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)
_OptionalListAccountsForProvisionedPermissionSetRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountsForProvisionedPermissionSetRequestRequestTypeDef",
    {
        "ProvisioningStatus": ProvisioningStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAccountsForProvisionedPermissionSetRequestRequestTypeDef(
    _RequiredListAccountsForProvisionedPermissionSetRequestRequestTypeDef,
    _OptionalListAccountsForProvisionedPermissionSetRequestRequestTypeDef,
):
    pass


ListInstancesRequestRequestTypeDef = TypedDict(
    "ListInstancesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListManagedPoliciesInPermissionSetRequestRequestTypeDef = TypedDict(
    "_RequiredListManagedPoliciesInPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)
_OptionalListManagedPoliciesInPermissionSetRequestRequestTypeDef = TypedDict(
    "_OptionalListManagedPoliciesInPermissionSetRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListManagedPoliciesInPermissionSetRequestRequestTypeDef(
    _RequiredListManagedPoliciesInPermissionSetRequestRequestTypeDef,
    _OptionalListManagedPoliciesInPermissionSetRequestRequestTypeDef,
):
    pass


PermissionSetProvisioningStatusMetadataTypeDef = TypedDict(
    "PermissionSetProvisioningStatusMetadataTypeDef",
    {
        "Status": StatusValuesType,
        "RequestId": str,
        "CreatedDate": datetime,
    },
    total=False,
)

_RequiredListPermissionSetsProvisionedToAccountRequestRequestTypeDef = TypedDict(
    "_RequiredListPermissionSetsProvisionedToAccountRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "AccountId": str,
    },
)
_OptionalListPermissionSetsProvisionedToAccountRequestRequestTypeDef = TypedDict(
    "_OptionalListPermissionSetsProvisionedToAccountRequestRequestTypeDef",
    {
        "ProvisioningStatus": ProvisioningStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListPermissionSetsProvisionedToAccountRequestRequestTypeDef(
    _RequiredListPermissionSetsProvisionedToAccountRequestRequestTypeDef,
    _OptionalListPermissionSetsProvisionedToAccountRequestRequestTypeDef,
):
    pass


_RequiredListPermissionSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListPermissionSetsRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListPermissionSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListPermissionSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPermissionSetsRequestRequestTypeDef(
    _RequiredListPermissionSetsRequestRequestTypeDef,
    _OptionalListPermissionSetsRequestRequestTypeDef,
):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
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


_RequiredProvisionPermissionSetRequestRequestTypeDef = TypedDict(
    "_RequiredProvisionPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "TargetType": ProvisionTargetTypeType,
    },
)
_OptionalProvisionPermissionSetRequestRequestTypeDef = TypedDict(
    "_OptionalProvisionPermissionSetRequestRequestTypeDef",
    {
        "TargetId": str,
    },
    total=False,
)


class ProvisionPermissionSetRequestRequestTypeDef(
    _RequiredProvisionPermissionSetRequestRequestTypeDef,
    _OptionalProvisionPermissionSetRequestRequestTypeDef,
):
    pass


PutInlinePolicyToPermissionSetRequestRequestTypeDef = TypedDict(
    "PutInlinePolicyToPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "InlinePolicy": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdatePermissionSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)
_OptionalUpdatePermissionSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePermissionSetRequestRequestTypeDef",
    {
        "Description": str,
        "SessionDuration": str,
        "RelayState": str,
    },
    total=False,
)


class UpdatePermissionSetRequestRequestTypeDef(
    _RequiredUpdatePermissionSetRequestRequestTypeDef,
    _OptionalUpdatePermissionSetRequestRequestTypeDef,
):
    pass


AccessControlAttributeTypeDef = TypedDict(
    "AccessControlAttributeTypeDef",
    {
        "Key": str,
        "Value": AccessControlAttributeValueTypeDef,
    },
)

CreateAccountAssignmentResponseTypeDef = TypedDict(
    "CreateAccountAssignmentResponseTypeDef",
    {
        "AccountAssignmentCreationStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountAssignmentResponseTypeDef = TypedDict(
    "DeleteAccountAssignmentResponseTypeDef",
    {
        "AccountAssignmentDeletionStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountAssignmentCreationStatusResponseTypeDef = TypedDict(
    "DescribeAccountAssignmentCreationStatusResponseTypeDef",
    {
        "AccountAssignmentCreationStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountAssignmentDeletionStatusResponseTypeDef = TypedDict(
    "DescribeAccountAssignmentDeletionStatusResponseTypeDef",
    {
        "AccountAssignmentDeletionStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInlinePolicyForPermissionSetResponseTypeDef = TypedDict(
    "GetInlinePolicyForPermissionSetResponseTypeDef",
    {
        "InlinePolicy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentCreationStatusResponseTypeDef = TypedDict(
    "ListAccountAssignmentCreationStatusResponseTypeDef",
    {
        "AccountAssignmentsCreationStatus": List[AccountAssignmentOperationStatusMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentDeletionStatusResponseTypeDef = TypedDict(
    "ListAccountAssignmentDeletionStatusResponseTypeDef",
    {
        "AccountAssignmentsDeletionStatus": List[AccountAssignmentOperationStatusMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentsResponseTypeDef = TypedDict(
    "ListAccountAssignmentsResponseTypeDef",
    {
        "AccountAssignments": List[AccountAssignmentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountsForProvisionedPermissionSetResponseTypeDef = TypedDict(
    "ListAccountsForProvisionedPermissionSetResponseTypeDef",
    {
        "AccountIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListManagedPoliciesInPermissionSetResponseTypeDef = TypedDict(
    "ListManagedPoliciesInPermissionSetResponseTypeDef",
    {
        "AttachedManagedPolicies": List[AttachedManagedPolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPermissionSetsProvisionedToAccountResponseTypeDef = TypedDict(
    "ListPermissionSetsProvisionedToAccountResponseTypeDef",
    {
        "NextToken": str,
        "PermissionSets": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPermissionSetsResponseTypeDef = TypedDict(
    "ListPermissionSetsResponseTypeDef",
    {
        "PermissionSets": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePermissionSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePermissionSetRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceArn": str,
    },
)
_OptionalCreatePermissionSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePermissionSetRequestRequestTypeDef",
    {
        "Description": str,
        "SessionDuration": str,
        "RelayState": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePermissionSetRequestRequestTypeDef(
    _RequiredCreatePermissionSetRequestRequestTypeDef,
    _OptionalCreatePermissionSetRequestRequestTypeDef,
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
        "InstanceArn": str,
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreatePermissionSetResponseTypeDef = TypedDict(
    "CreatePermissionSetResponseTypeDef",
    {
        "PermissionSet": PermissionSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePermissionSetResponseTypeDef = TypedDict(
    "DescribePermissionSetResponseTypeDef",
    {
        "PermissionSet": PermissionSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePermissionSetProvisioningStatusResponseTypeDef = TypedDict(
    "DescribePermissionSetProvisioningStatusResponseTypeDef",
    {
        "PermissionSetProvisioningStatus": PermissionSetProvisioningStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProvisionPermissionSetResponseTypeDef = TypedDict(
    "ProvisionPermissionSetResponseTypeDef",
    {
        "PermissionSetProvisioningStatus": PermissionSetProvisioningStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstancesResponseTypeDef = TypedDict(
    "ListInstancesResponseTypeDef",
    {
        "Instances": List[InstanceMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAccountAssignmentCreationStatusRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountAssignmentCreationStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListAccountAssignmentCreationStatusRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountAssignmentCreationStatusRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filter": OperationStatusFilterTypeDef,
    },
    total=False,
)


class ListAccountAssignmentCreationStatusRequestRequestTypeDef(
    _RequiredListAccountAssignmentCreationStatusRequestRequestTypeDef,
    _OptionalListAccountAssignmentCreationStatusRequestRequestTypeDef,
):
    pass


_RequiredListAccountAssignmentDeletionStatusRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountAssignmentDeletionStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListAccountAssignmentDeletionStatusRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountAssignmentDeletionStatusRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filter": OperationStatusFilterTypeDef,
    },
    total=False,
)


class ListAccountAssignmentDeletionStatusRequestRequestTypeDef(
    _RequiredListAccountAssignmentDeletionStatusRequestRequestTypeDef,
    _OptionalListAccountAssignmentDeletionStatusRequestRequestTypeDef,
):
    pass


_RequiredListPermissionSetProvisioningStatusRequestRequestTypeDef = TypedDict(
    "_RequiredListPermissionSetProvisioningStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListPermissionSetProvisioningStatusRequestRequestTypeDef = TypedDict(
    "_OptionalListPermissionSetProvisioningStatusRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filter": OperationStatusFilterTypeDef,
    },
    total=False,
)


class ListPermissionSetProvisioningStatusRequestRequestTypeDef(
    _RequiredListPermissionSetProvisioningStatusRequestRequestTypeDef,
    _OptionalListPermissionSetProvisioningStatusRequestRequestTypeDef,
):
    pass


_RequiredListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef = TypedDict(
    "_RequiredListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef = TypedDict(
    "_OptionalListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef",
    {
        "Filter": OperationStatusFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef(
    _RequiredListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef,
    _OptionalListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef,
):
    pass


_RequiredListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef = TypedDict(
    "_RequiredListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef = TypedDict(
    "_OptionalListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef",
    {
        "Filter": OperationStatusFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef(
    _RequiredListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef,
    _OptionalListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef,
):
    pass


_RequiredListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef = TypedDict(
    "_RequiredListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef",
    {
        "InstanceArn": str,
        "AccountId": str,
        "PermissionSetArn": str,
    },
)
_OptionalListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef = TypedDict(
    "_OptionalListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef(
    _RequiredListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef,
    _OptionalListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef,
):
    pass


_RequiredListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef = TypedDict(
    "_RequiredListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)
_OptionalListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef = TypedDict(
    "_OptionalListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef",
    {
        "ProvisioningStatus": ProvisioningStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef(
    _RequiredListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef,
    _OptionalListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef,
):
    pass


ListInstancesRequestListInstancesPaginateTypeDef = TypedDict(
    "ListInstancesRequestListInstancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef = TypedDict(
    "_RequiredListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)
_OptionalListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef = TypedDict(
    "_OptionalListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef(
    _RequiredListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef,
    _OptionalListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef,
):
    pass


_RequiredListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef = TypedDict(
    "_RequiredListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef = TypedDict(
    "_OptionalListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef",
    {
        "Filter": OperationStatusFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef(
    _RequiredListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef,
    _OptionalListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef,
):
    pass


_RequiredListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef = TypedDict(
    "_RequiredListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef",
    {
        "InstanceArn": str,
        "AccountId": str,
    },
)
_OptionalListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef = TypedDict(
    "_OptionalListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef",
    {
        "ProvisioningStatus": ProvisioningStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef(
    _RequiredListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef,
    _OptionalListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef,
):
    pass


_RequiredListPermissionSetsRequestListPermissionSetsPaginateTypeDef = TypedDict(
    "_RequiredListPermissionSetsRequestListPermissionSetsPaginateTypeDef",
    {
        "InstanceArn": str,
    },
)
_OptionalListPermissionSetsRequestListPermissionSetsPaginateTypeDef = TypedDict(
    "_OptionalListPermissionSetsRequestListPermissionSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPermissionSetsRequestListPermissionSetsPaginateTypeDef(
    _RequiredListPermissionSetsRequestListPermissionSetsPaginateTypeDef,
    _OptionalListPermissionSetsRequestListPermissionSetsPaginateTypeDef,
):
    pass


_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
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


ListPermissionSetProvisioningStatusResponseTypeDef = TypedDict(
    "ListPermissionSetProvisioningStatusResponseTypeDef",
    {
        "PermissionSetsProvisioningStatus": List[PermissionSetProvisioningStatusMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceAccessControlAttributeConfigurationTypeDef = TypedDict(
    "InstanceAccessControlAttributeConfigurationTypeDef",
    {
        "AccessControlAttributes": Sequence[AccessControlAttributeTypeDef],
    },
)

CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "InstanceAccessControlAttributeConfiguration": InstanceAccessControlAttributeConfigurationTypeDef,
    },
)

DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef = TypedDict(
    "DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef",
    {
        "Status": InstanceAccessControlAttributeConfigurationStatusType,
        "StatusReason": str,
        "InstanceAccessControlAttributeConfiguration": InstanceAccessControlAttributeConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "InstanceAccessControlAttributeConfiguration": InstanceAccessControlAttributeConfigurationTypeDef,
    },
)
