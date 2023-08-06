"""
Type annotations for sso-admin service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sso_admin.client import SSOAdminClient

    session = Session()
    client: SSOAdminClient = session.client("sso-admin")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import PrincipalTypeType, ProvisioningStatusType, ProvisionTargetTypeType
from .paginator import (
    ListAccountAssignmentCreationStatusPaginator,
    ListAccountAssignmentDeletionStatusPaginator,
    ListAccountAssignmentsPaginator,
    ListAccountsForProvisionedPermissionSetPaginator,
    ListInstancesPaginator,
    ListManagedPoliciesInPermissionSetPaginator,
    ListPermissionSetProvisioningStatusPaginator,
    ListPermissionSetsPaginator,
    ListPermissionSetsProvisionedToAccountPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    CreateAccountAssignmentResponseTypeDef,
    CreatePermissionSetResponseTypeDef,
    DeleteAccountAssignmentResponseTypeDef,
    DescribeAccountAssignmentCreationStatusResponseTypeDef,
    DescribeAccountAssignmentDeletionStatusResponseTypeDef,
    DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef,
    DescribePermissionSetProvisioningStatusResponseTypeDef,
    DescribePermissionSetResponseTypeDef,
    GetInlinePolicyForPermissionSetResponseTypeDef,
    InstanceAccessControlAttributeConfigurationTypeDef,
    ListAccountAssignmentCreationStatusResponseTypeDef,
    ListAccountAssignmentDeletionStatusResponseTypeDef,
    ListAccountAssignmentsResponseTypeDef,
    ListAccountsForProvisionedPermissionSetResponseTypeDef,
    ListInstancesResponseTypeDef,
    ListManagedPoliciesInPermissionSetResponseTypeDef,
    ListPermissionSetProvisioningStatusResponseTypeDef,
    ListPermissionSetsProvisionedToAccountResponseTypeDef,
    ListPermissionSetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OperationStatusFilterTypeDef,
    ProvisionPermissionSetResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SSOAdminClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SSOAdminClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSOAdminClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#exceptions)
        """

    def attach_managed_policy_to_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str, ManagedPolicyArn: str
    ) -> Dict[str, Any]:
        """
        Attaches an IAM managed policy ARN to a permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.attach_managed_policy_to_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#attach_managed_policy_to_permission_set)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#can_paginate)
        """

    def create_account_assignment(
        self,
        *,
        InstanceArn: str,
        TargetId: str,
        TargetType: Literal["AWS_ACCOUNT"],
        PermissionSetArn: str,
        PrincipalType: PrincipalTypeType,
        PrincipalId: str
    ) -> CreateAccountAssignmentResponseTypeDef:
        """
        Assigns access to a principal for a specified Amazon Web Services account using
        a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.create_account_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#create_account_assignment)
        """

    def create_instance_access_control_attribute_configuration(
        self,
        *,
        InstanceArn: str,
        InstanceAccessControlAttributeConfiguration: InstanceAccessControlAttributeConfigurationTypeDef
    ) -> Dict[str, Any]:
        """
        Enables the attributes-based access control (ABAC) feature for the specified
        Amazon Web Services SSO instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.create_instance_access_control_attribute_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#create_instance_access_control_attribute_configuration)
        """

    def create_permission_set(
        self,
        *,
        Name: str,
        InstanceArn: str,
        Description: str = ...,
        SessionDuration: str = ...,
        RelayState: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreatePermissionSetResponseTypeDef:
        """
        Creates a permission set within a specified SSO instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.create_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#create_permission_set)
        """

    def delete_account_assignment(
        self,
        *,
        InstanceArn: str,
        TargetId: str,
        TargetType: Literal["AWS_ACCOUNT"],
        PermissionSetArn: str,
        PrincipalType: PrincipalTypeType,
        PrincipalId: str
    ) -> DeleteAccountAssignmentResponseTypeDef:
        """
        Deletes a principal's access from a specified Amazon Web Services account using
        a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_account_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#delete_account_assignment)
        """

    def delete_inline_policy_from_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Deletes the inline policy from a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_inline_policy_from_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#delete_inline_policy_from_permission_set)
        """

    def delete_instance_access_control_attribute_configuration(
        self, *, InstanceArn: str
    ) -> Dict[str, Any]:
        """
        Disables the attributes-based access control (ABAC) feature for the specified
        Amazon Web Services SSO instance and deletes all of the attribute mappings that
        have been configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_instance_access_control_attribute_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#delete_instance_access_control_attribute_configuration)
        """

    def delete_permission_set(self, *, InstanceArn: str, PermissionSetArn: str) -> Dict[str, Any]:
        """
        Deletes the specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#delete_permission_set)
        """

    def describe_account_assignment_creation_status(
        self, *, InstanceArn: str, AccountAssignmentCreationRequestId: str
    ) -> DescribeAccountAssignmentCreationStatusResponseTypeDef:
        """
        Describes the status of the assignment creation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_account_assignment_creation_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#describe_account_assignment_creation_status)
        """

    def describe_account_assignment_deletion_status(
        self, *, InstanceArn: str, AccountAssignmentDeletionRequestId: str
    ) -> DescribeAccountAssignmentDeletionStatusResponseTypeDef:
        """
        Describes the status of the assignment deletion request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_account_assignment_deletion_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#describe_account_assignment_deletion_status)
        """

    def describe_instance_access_control_attribute_configuration(
        self, *, InstanceArn: str
    ) -> DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef:
        """
        Returns the list of Amazon Web Services SSO identity store attributes that have
        been configured to work with attributes-based access control (ABAC) for the
        specified Amazon Web Services SSO instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_instance_access_control_attribute_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#describe_instance_access_control_attribute_configuration)
        """

    def describe_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> DescribePermissionSetResponseTypeDef:
        """
        Gets the details of the permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#describe_permission_set)
        """

    def describe_permission_set_provisioning_status(
        self, *, InstanceArn: str, ProvisionPermissionSetRequestId: str
    ) -> DescribePermissionSetProvisioningStatusResponseTypeDef:
        """
        Describes the status for the given permission set provisioning request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_permission_set_provisioning_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#describe_permission_set_provisioning_status)
        """

    def detach_managed_policy_from_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str, ManagedPolicyArn: str
    ) -> Dict[str, Any]:
        """
        Detaches the attached IAM managed policy ARN from the specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.detach_managed_policy_from_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#detach_managed_policy_from_permission_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#generate_presigned_url)
        """

    def get_inline_policy_for_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> GetInlinePolicyForPermissionSetResponseTypeDef:
        """
        Obtains the inline policy assigned to the permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_inline_policy_for_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_inline_policy_for_permission_set)
        """

    def list_account_assignment_creation_status(
        self,
        *,
        InstanceArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filter: OperationStatusFilterTypeDef = ...
    ) -> ListAccountAssignmentCreationStatusResponseTypeDef:
        """
        Lists the status of the Amazon Web Services account assignment creation requests
        for a specified SSO instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_account_assignment_creation_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_account_assignment_creation_status)
        """

    def list_account_assignment_deletion_status(
        self,
        *,
        InstanceArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filter: OperationStatusFilterTypeDef = ...
    ) -> ListAccountAssignmentDeletionStatusResponseTypeDef:
        """
        Lists the status of the Amazon Web Services account assignment deletion requests
        for a specified SSO instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_account_assignment_deletion_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_account_assignment_deletion_status)
        """

    def list_account_assignments(
        self,
        *,
        InstanceArn: str,
        AccountId: str,
        PermissionSetArn: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAccountAssignmentsResponseTypeDef:
        """
        Lists the assignee of the specified Amazon Web Services account with the
        specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_account_assignments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_account_assignments)
        """

    def list_accounts_for_provisioned_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        ProvisioningStatus: ProvisioningStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAccountsForProvisionedPermissionSetResponseTypeDef:
        """
        Lists all the Amazon Web Services accounts where the specified permission set is
        provisioned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_accounts_for_provisioned_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_accounts_for_provisioned_permission_set)
        """

    def list_instances(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListInstancesResponseTypeDef:
        """
        Lists the SSO instances that the caller has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_instances)
        """

    def list_managed_policies_in_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListManagedPoliciesInPermissionSetResponseTypeDef:
        """
        Lists the IAM managed policy that is attached to a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_managed_policies_in_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_managed_policies_in_permission_set)
        """

    def list_permission_set_provisioning_status(
        self,
        *,
        InstanceArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filter: OperationStatusFilterTypeDef = ...
    ) -> ListPermissionSetProvisioningStatusResponseTypeDef:
        """
        Lists the status of the permission set provisioning requests for a specified SSO
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_permission_set_provisioning_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_permission_set_provisioning_status)
        """

    def list_permission_sets(
        self, *, InstanceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPermissionSetsResponseTypeDef:
        """
        Lists the  PermissionSet s in an SSO instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_permission_sets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_permission_sets)
        """

    def list_permission_sets_provisioned_to_account(
        self,
        *,
        InstanceArn: str,
        AccountId: str,
        ProvisioningStatus: ProvisioningStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPermissionSetsProvisionedToAccountResponseTypeDef:
        """
        Lists all the permission sets that are provisioned to a specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_permission_sets_provisioned_to_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_permission_sets_provisioned_to_account)
        """

    def list_tags_for_resource(
        self, *, InstanceArn: str, ResourceArn: str, NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are attached to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#list_tags_for_resource)
        """

    def provision_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        TargetType: ProvisionTargetTypeType,
        TargetId: str = ...
    ) -> ProvisionPermissionSetResponseTypeDef:
        """
        The process by which a specified permission set is provisioned to the specified
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.provision_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#provision_permission_set)
        """

    def put_inline_policy_to_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str, InlinePolicy: str
    ) -> Dict[str, Any]:
        """
        Attaches an IAM inline policy to a permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.put_inline_policy_to_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#put_inline_policy_to_permission_set)
        """

    def tag_resource(
        self, *, InstanceArn: str, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a set of tags with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#tag_resource)
        """

    def untag_resource(
        self, *, InstanceArn: str, ResourceArn: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Disassociates a set of tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#untag_resource)
        """

    def update_instance_access_control_attribute_configuration(
        self,
        *,
        InstanceArn: str,
        InstanceAccessControlAttributeConfiguration: InstanceAccessControlAttributeConfigurationTypeDef
    ) -> Dict[str, Any]:
        """
        Updates the Amazon Web Services SSO identity store attributes that you can use
        with the Amazon Web Services SSO instance for attributes-based access control
        (ABAC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.update_instance_access_control_attribute_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#update_instance_access_control_attribute_configuration)
        """

    def update_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        Description: str = ...,
        SessionDuration: str = ...,
        RelayState: str = ...
    ) -> Dict[str, Any]:
        """
        Updates an existing permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.update_permission_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#update_permission_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_assignment_creation_status"]
    ) -> ListAccountAssignmentCreationStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_assignment_deletion_status"]
    ) -> ListAccountAssignmentDeletionStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_assignments"]
    ) -> ListAccountAssignmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accounts_for_provisioned_permission_set"]
    ) -> ListAccountsForProvisionedPermissionSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_policies_in_permission_set"]
    ) -> ListManagedPoliciesInPermissionSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_set_provisioning_status"]
    ) -> ListPermissionSetProvisioningStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_sets"]
    ) -> ListPermissionSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_sets_provisioned_to_account"]
    ) -> ListPermissionSetsProvisionedToAccountPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/client/#get_paginator)
        """
