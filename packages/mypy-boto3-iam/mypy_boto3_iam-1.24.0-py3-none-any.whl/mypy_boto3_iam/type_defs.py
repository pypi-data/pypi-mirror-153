"""
Type annotations for iam service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/type_defs/)

Usage::

    ```python
    from mypy_boto3_iam.type_defs import AccessDetailTypeDef

    data: AccessDetailTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AccessAdvisorUsageGranularityTypeType,
    ContextKeyTypeEnumType,
    DeletionTaskStatusTypeType,
    EntityTypeType,
    PolicyEvaluationDecisionTypeType,
    PolicySourceTypeType,
    PolicyUsageTypeType,
    ReportStateTypeType,
    assignmentStatusTypeType,
    encodingTypeType,
    globalEndpointTokenVersionType,
    jobStatusTypeType,
    policyOwnerEntityTypeType,
    policyScopeTypeType,
    policyTypeType,
    sortKeyTypeType,
    statusTypeType,
    summaryKeyTypeType,
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
    "AccessDetailTypeDef",
    "AccessKeyLastUsedTypeDef",
    "AccessKeyMetadataTypeDef",
    "AccessKeyTypeDef",
    "AddClientIDToOpenIDConnectProviderRequestRequestTypeDef",
    "AddRoleToInstanceProfileRequestInstanceProfileAddRoleTypeDef",
    "AddRoleToInstanceProfileRequestRequestTypeDef",
    "AddUserToGroupRequestGroupAddUserTypeDef",
    "AddUserToGroupRequestRequestTypeDef",
    "AddUserToGroupRequestUserAddGroupTypeDef",
    "AttachGroupPolicyRequestGroupAttachPolicyTypeDef",
    "AttachGroupPolicyRequestPolicyAttachGroupTypeDef",
    "AttachGroupPolicyRequestRequestTypeDef",
    "AttachRolePolicyRequestPolicyAttachRoleTypeDef",
    "AttachRolePolicyRequestRequestTypeDef",
    "AttachRolePolicyRequestRoleAttachPolicyTypeDef",
    "AttachUserPolicyRequestPolicyAttachUserTypeDef",
    "AttachUserPolicyRequestRequestTypeDef",
    "AttachUserPolicyRequestUserAttachPolicyTypeDef",
    "ResponseMetadataTypeDef",
    "AttachedPermissionsBoundaryTypeDef",
    "AttachedPolicyTypeDef",
    "ChangePasswordRequestRequestTypeDef",
    "ChangePasswordRequestServiceResourceChangePasswordTypeDef",
    "ContextEntryTypeDef",
    "CreateAccessKeyRequestRequestTypeDef",
    "CreateAccountAliasRequestRequestTypeDef",
    "CreateAccountAliasRequestServiceResourceCreateAccountAliasTypeDef",
    "CreateGroupRequestGroupCreateTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupRequestServiceResourceCreateGroupTypeDef",
    "GroupTypeDef",
    "TagTypeDef",
    "CreateLoginProfileRequestLoginProfileCreateTypeDef",
    "CreateLoginProfileRequestRequestTypeDef",
    "CreateLoginProfileRequestUserCreateLoginProfileTypeDef",
    "LoginProfileTypeDef",
    "CreatePolicyVersionRequestPolicyCreateVersionTypeDef",
    "CreatePolicyVersionRequestRequestTypeDef",
    "PolicyVersionTypeDef",
    "CreateServiceLinkedRoleRequestRequestTypeDef",
    "CreateServiceSpecificCredentialRequestRequestTypeDef",
    "ServiceSpecificCredentialTypeDef",
    "DeactivateMFADeviceRequestRequestTypeDef",
    "DeleteAccessKeyRequestRequestTypeDef",
    "DeleteAccountAliasRequestRequestTypeDef",
    "DeleteGroupPolicyRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteInstanceProfileRequestRequestTypeDef",
    "DeleteLoginProfileRequestRequestTypeDef",
    "DeleteOpenIDConnectProviderRequestRequestTypeDef",
    "DeletePolicyRequestRequestTypeDef",
    "DeletePolicyVersionRequestRequestTypeDef",
    "DeleteRolePermissionsBoundaryRequestRequestTypeDef",
    "DeleteRolePolicyRequestRequestTypeDef",
    "DeleteRoleRequestRequestTypeDef",
    "DeleteSAMLProviderRequestRequestTypeDef",
    "DeleteSSHPublicKeyRequestRequestTypeDef",
    "DeleteServerCertificateRequestRequestTypeDef",
    "DeleteServiceLinkedRoleRequestRequestTypeDef",
    "DeleteServiceSpecificCredentialRequestRequestTypeDef",
    "DeleteSigningCertificateRequestRequestTypeDef",
    "DeleteUserPermissionsBoundaryRequestRequestTypeDef",
    "DeleteUserPolicyRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteVirtualMFADeviceRequestRequestTypeDef",
    "RoleUsageTypeTypeDef",
    "DetachGroupPolicyRequestGroupDetachPolicyTypeDef",
    "DetachGroupPolicyRequestPolicyDetachGroupTypeDef",
    "DetachGroupPolicyRequestRequestTypeDef",
    "DetachRolePolicyRequestPolicyDetachRoleTypeDef",
    "DetachRolePolicyRequestRequestTypeDef",
    "DetachRolePolicyRequestRoleDetachPolicyTypeDef",
    "DetachUserPolicyRequestPolicyDetachUserTypeDef",
    "DetachUserPolicyRequestRequestTypeDef",
    "DetachUserPolicyRequestUserDetachPolicyTypeDef",
    "EnableMFADeviceRequestMfaDeviceAssociateTypeDef",
    "EnableMFADeviceRequestRequestTypeDef",
    "EnableMFADeviceRequestUserEnableMfaTypeDef",
    "EntityInfoTypeDef",
    "ErrorDetailsTypeDef",
    "OrganizationsDecisionDetailTypeDef",
    "PermissionsBoundaryDecisionDetailTypeDef",
    "GenerateOrganizationsAccessReportRequestRequestTypeDef",
    "GenerateServiceLastAccessedDetailsRequestRequestTypeDef",
    "GetAccessKeyLastUsedRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetAccountAuthorizationDetailsRequestRequestTypeDef",
    "PasswordPolicyTypeDef",
    "GetContextKeysForCustomPolicyRequestRequestTypeDef",
    "GetContextKeysForPrincipalPolicyRequestRequestTypeDef",
    "GetGroupPolicyRequestRequestTypeDef",
    "GetGroupRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetInstanceProfileRequestRequestTypeDef",
    "GetLoginProfileRequestRequestTypeDef",
    "GetOpenIDConnectProviderRequestRequestTypeDef",
    "GetOrganizationsAccessReportRequestRequestTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetPolicyVersionRequestRequestTypeDef",
    "GetRolePolicyRequestRequestTypeDef",
    "GetRoleRequestRequestTypeDef",
    "GetSAMLProviderRequestRequestTypeDef",
    "GetSSHPublicKeyRequestRequestTypeDef",
    "SSHPublicKeyTypeDef",
    "GetServerCertificateRequestRequestTypeDef",
    "GetServiceLastAccessedDetailsRequestRequestTypeDef",
    "GetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef",
    "GetServiceLinkedRoleDeletionStatusRequestRequestTypeDef",
    "GetUserPolicyRequestRequestTypeDef",
    "GetUserRequestRequestTypeDef",
    "PolicyDetailTypeDef",
    "GroupPolicyRequestTypeDef",
    "ListAccessKeysRequestRequestTypeDef",
    "ListAccountAliasesRequestRequestTypeDef",
    "ListAttachedGroupPoliciesRequestRequestTypeDef",
    "ListAttachedRolePoliciesRequestRequestTypeDef",
    "ListAttachedUserPoliciesRequestRequestTypeDef",
    "ListEntitiesForPolicyRequestRequestTypeDef",
    "PolicyGroupTypeDef",
    "PolicyRoleTypeDef",
    "PolicyUserTypeDef",
    "ListGroupPoliciesRequestRequestTypeDef",
    "ListGroupsForUserRequestRequestTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListInstanceProfileTagsRequestRequestTypeDef",
    "ListInstanceProfilesForRoleRequestRequestTypeDef",
    "ListInstanceProfilesRequestRequestTypeDef",
    "ListMFADeviceTagsRequestRequestTypeDef",
    "ListMFADevicesRequestRequestTypeDef",
    "MFADeviceTypeDef",
    "ListOpenIDConnectProviderTagsRequestRequestTypeDef",
    "OpenIDConnectProviderListEntryTypeDef",
    "PolicyGrantingServiceAccessTypeDef",
    "ListPoliciesGrantingServiceAccessRequestRequestTypeDef",
    "ListPoliciesRequestRequestTypeDef",
    "ListPolicyTagsRequestRequestTypeDef",
    "ListPolicyVersionsRequestRequestTypeDef",
    "ListRolePoliciesRequestRequestTypeDef",
    "ListRoleTagsRequestRequestTypeDef",
    "ListRolesRequestRequestTypeDef",
    "ListSAMLProviderTagsRequestRequestTypeDef",
    "SAMLProviderListEntryTypeDef",
    "ListSSHPublicKeysRequestRequestTypeDef",
    "SSHPublicKeyMetadataTypeDef",
    "ListServerCertificateTagsRequestRequestTypeDef",
    "ListServerCertificatesRequestRequestTypeDef",
    "ServerCertificateMetadataTypeDef",
    "ListServiceSpecificCredentialsRequestRequestTypeDef",
    "ServiceSpecificCredentialMetadataTypeDef",
    "ListSigningCertificatesRequestRequestTypeDef",
    "SigningCertificateTypeDef",
    "ListUserPoliciesRequestRequestTypeDef",
    "ListUserTagsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListVirtualMFADevicesRequestRequestTypeDef",
    "PositionTypeDef",
    "PutGroupPolicyRequestGroupCreatePolicyTypeDef",
    "PutGroupPolicyRequestGroupPolicyPutTypeDef",
    "PutGroupPolicyRequestRequestTypeDef",
    "PutRolePermissionsBoundaryRequestRequestTypeDef",
    "PutRolePolicyRequestRequestTypeDef",
    "PutRolePolicyRequestRolePolicyPutTypeDef",
    "PutUserPermissionsBoundaryRequestRequestTypeDef",
    "PutUserPolicyRequestRequestTypeDef",
    "PutUserPolicyRequestUserCreatePolicyTypeDef",
    "PutUserPolicyRequestUserPolicyPutTypeDef",
    "RemoveClientIDFromOpenIDConnectProviderRequestRequestTypeDef",
    "RemoveRoleFromInstanceProfileRequestInstanceProfileRemoveRoleTypeDef",
    "RemoveRoleFromInstanceProfileRequestRequestTypeDef",
    "RemoveUserFromGroupRequestGroupRemoveUserTypeDef",
    "RemoveUserFromGroupRequestRequestTypeDef",
    "RemoveUserFromGroupRequestUserRemoveGroupTypeDef",
    "ResetServiceSpecificCredentialRequestRequestTypeDef",
    "ResyncMFADeviceRequestMfaDeviceResyncTypeDef",
    "ResyncMFADeviceRequestRequestTypeDef",
    "RoleLastUsedTypeDef",
    "RolePolicyRequestTypeDef",
    "TrackedActionLastAccessedTypeDef",
    "ServiceResourceAccessKeyPairRequestTypeDef",
    "ServiceResourceAccessKeyRequestTypeDef",
    "ServiceResourceAssumeRolePolicyRequestTypeDef",
    "ServiceResourceGroupPolicyRequestTypeDef",
    "ServiceResourceGroupRequestTypeDef",
    "ServiceResourceInstanceProfileRequestTypeDef",
    "ServiceResourceLoginProfileRequestTypeDef",
    "ServiceResourceMfaDeviceRequestTypeDef",
    "ServiceResourcePolicyRequestTypeDef",
    "ServiceResourcePolicyVersionRequestTypeDef",
    "ServiceResourceRolePolicyRequestTypeDef",
    "ServiceResourceRoleRequestTypeDef",
    "ServiceResourceSamlProviderRequestTypeDef",
    "ServiceResourceServerCertificateRequestTypeDef",
    "ServiceResourceSigningCertificateRequestTypeDef",
    "ServiceResourceUserPolicyRequestTypeDef",
    "ServiceResourceUserRequestTypeDef",
    "ServiceResourceVirtualMfaDeviceRequestTypeDef",
    "SetDefaultPolicyVersionRequestRequestTypeDef",
    "SetSecurityTokenServicePreferencesRequestRequestTypeDef",
    "UntagInstanceProfileRequestRequestTypeDef",
    "UntagMFADeviceRequestRequestTypeDef",
    "UntagOpenIDConnectProviderRequestRequestTypeDef",
    "UntagPolicyRequestRequestTypeDef",
    "UntagRoleRequestRequestTypeDef",
    "UntagSAMLProviderRequestRequestTypeDef",
    "UntagServerCertificateRequestRequestTypeDef",
    "UntagUserRequestRequestTypeDef",
    "UpdateAccessKeyRequestAccessKeyActivateTypeDef",
    "UpdateAccessKeyRequestAccessKeyDeactivateTypeDef",
    "UpdateAccessKeyRequestAccessKeyPairActivateTypeDef",
    "UpdateAccessKeyRequestAccessKeyPairDeactivateTypeDef",
    "UpdateAccessKeyRequestRequestTypeDef",
    "UpdateAccountPasswordPolicyRequestAccountPasswordPolicyUpdateTypeDef",
    "UpdateAccountPasswordPolicyRequestRequestTypeDef",
    "UpdateAccountPasswordPolicyRequestServiceResourceCreateAccountPasswordPolicyTypeDef",
    "UpdateAssumeRolePolicyRequestAssumeRolePolicyUpdateTypeDef",
    "UpdateAssumeRolePolicyRequestRequestTypeDef",
    "UpdateGroupRequestGroupUpdateTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateLoginProfileRequestLoginProfileUpdateTypeDef",
    "UpdateLoginProfileRequestRequestTypeDef",
    "UpdateOpenIDConnectProviderThumbprintRequestRequestTypeDef",
    "UpdateRoleDescriptionRequestRequestTypeDef",
    "UpdateRoleRequestRequestTypeDef",
    "UpdateSAMLProviderRequestRequestTypeDef",
    "UpdateSAMLProviderRequestSamlProviderUpdateTypeDef",
    "UpdateSSHPublicKeyRequestRequestTypeDef",
    "UpdateServerCertificateRequestRequestTypeDef",
    "UpdateServerCertificateRequestServerCertificateUpdateTypeDef",
    "UpdateServiceSpecificCredentialRequestRequestTypeDef",
    "UpdateSigningCertificateRequestRequestTypeDef",
    "UpdateSigningCertificateRequestSigningCertificateActivateTypeDef",
    "UpdateSigningCertificateRequestSigningCertificateDeactivateTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserRequestUserUpdateTypeDef",
    "UploadSSHPublicKeyRequestRequestTypeDef",
    "UploadSigningCertificateRequestRequestTypeDef",
    "UploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef",
    "UserAccessKeyRequestTypeDef",
    "UserMfaDeviceRequestTypeDef",
    "UserPolicyRequestTypeDef",
    "UserSigningCertificateRequestTypeDef",
    "AttachedPermissionsBoundaryResponseMetadataTypeDef",
    "CreateAccessKeyResponseTypeDef",
    "DeleteServiceLinkedRoleResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GenerateCredentialReportResponseTypeDef",
    "GenerateOrganizationsAccessReportResponseTypeDef",
    "GenerateServiceLastAccessedDetailsResponseTypeDef",
    "GetAccessKeyLastUsedResponseTypeDef",
    "GetAccountSummaryResponseTypeDef",
    "GetContextKeysForPolicyResponseTypeDef",
    "GetCredentialReportResponseTypeDef",
    "GetGroupPolicyResponseTypeDef",
    "GetRolePolicyResponseTypeDef",
    "GetUserPolicyResponseTypeDef",
    "ListAccessKeysResponseTypeDef",
    "ListAccountAliasesResponseTypeDef",
    "ListGroupPoliciesResponseTypeDef",
    "ListRolePoliciesResponseTypeDef",
    "ListUserPoliciesResponseTypeDef",
    "RoleLastUsedResponseMetadataTypeDef",
    "ServerCertificateMetadataResponseMetadataTypeDef",
    "UpdateSAMLProviderResponseTypeDef",
    "ListAttachedGroupPoliciesResponseTypeDef",
    "ListAttachedRolePoliciesResponseTypeDef",
    "ListAttachedUserPoliciesResponseTypeDef",
    "SimulateCustomPolicyRequestRequestTypeDef",
    "SimulatePrincipalPolicyRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "ListGroupsForUserResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "CreateInstanceProfileRequestRequestTypeDef",
    "CreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef",
    "CreateOpenIDConnectProviderRequestRequestTypeDef",
    "CreateOpenIDConnectProviderResponseTypeDef",
    "CreatePolicyRequestRequestTypeDef",
    "CreatePolicyRequestServiceResourceCreatePolicyTypeDef",
    "CreateRoleRequestRequestTypeDef",
    "CreateRoleRequestServiceResourceCreateRoleTypeDef",
    "CreateSAMLProviderRequestRequestTypeDef",
    "CreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef",
    "CreateSAMLProviderResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserRequestServiceResourceCreateUserTypeDef",
    "CreateUserRequestUserCreateTypeDef",
    "CreateVirtualMFADeviceRequestRequestTypeDef",
    "CreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef",
    "GetOpenIDConnectProviderResponseTypeDef",
    "GetSAMLProviderResponseTypeDef",
    "ListInstanceProfileTagsResponseTypeDef",
    "ListMFADeviceTagsResponseTypeDef",
    "ListOpenIDConnectProviderTagsResponseTypeDef",
    "ListPolicyTagsResponseTypeDef",
    "ListRoleTagsResponseTypeDef",
    "ListSAMLProviderTagsResponseTypeDef",
    "ListServerCertificateTagsResponseTypeDef",
    "ListUserTagsResponseTypeDef",
    "PolicyTypeDef",
    "TagInstanceProfileRequestRequestTypeDef",
    "TagMFADeviceRequestRequestTypeDef",
    "TagOpenIDConnectProviderRequestRequestTypeDef",
    "TagPolicyRequestRequestTypeDef",
    "TagRoleRequestRequestTypeDef",
    "TagSAMLProviderRequestRequestTypeDef",
    "TagServerCertificateRequestRequestTypeDef",
    "TagUserRequestRequestTypeDef",
    "UploadServerCertificateRequestRequestTypeDef",
    "UploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef",
    "UserResponseMetadataTypeDef",
    "UserTypeDef",
    "CreateLoginProfileResponseTypeDef",
    "GetLoginProfileResponseTypeDef",
    "CreatePolicyVersionResponseTypeDef",
    "GetPolicyVersionResponseTypeDef",
    "ListPolicyVersionsResponseTypeDef",
    "ManagedPolicyDetailTypeDef",
    "CreateServiceSpecificCredentialResponseTypeDef",
    "ResetServiceSpecificCredentialResponseTypeDef",
    "DeletionTaskFailureReasonTypeTypeDef",
    "EntityDetailsTypeDef",
    "GetOrganizationsAccessReportResponseTypeDef",
    "GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef",
    "GetGroupRequestGetGroupPaginateTypeDef",
    "ListAccessKeysRequestListAccessKeysPaginateTypeDef",
    "ListAccountAliasesRequestListAccountAliasesPaginateTypeDef",
    "ListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef",
    "ListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef",
    "ListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef",
    "ListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef",
    "ListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef",
    "ListGroupsForUserRequestListGroupsForUserPaginateTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef",
    "ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef",
    "ListMFADevicesRequestListMFADevicesPaginateTypeDef",
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    "ListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef",
    "ListRolePoliciesRequestListRolePoliciesPaginateTypeDef",
    "ListRolesRequestListRolesPaginateTypeDef",
    "ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef",
    "ListServerCertificatesRequestListServerCertificatesPaginateTypeDef",
    "ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef",
    "ListUserPoliciesRequestListUserPoliciesPaginateTypeDef",
    "ListUserTagsRequestListUserTagsPaginateTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef",
    "SimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef",
    "SimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef",
    "GetAccountPasswordPolicyResponseTypeDef",
    "GetInstanceProfileRequestInstanceProfileExistsWaitTypeDef",
    "GetPolicyRequestPolicyExistsWaitTypeDef",
    "GetRoleRequestRoleExistsWaitTypeDef",
    "GetUserRequestUserExistsWaitTypeDef",
    "GetSSHPublicKeyResponseTypeDef",
    "UploadSSHPublicKeyResponseTypeDef",
    "GroupDetailTypeDef",
    "UserDetailTypeDef",
    "ListEntitiesForPolicyResponseTypeDef",
    "ListMFADevicesResponseTypeDef",
    "ListOpenIDConnectProvidersResponseTypeDef",
    "ListPoliciesGrantingServiceAccessEntryTypeDef",
    "ListSAMLProvidersResponseTypeDef",
    "ListSSHPublicKeysResponseTypeDef",
    "ListServerCertificatesResponseTypeDef",
    "ServerCertificateTypeDef",
    "UploadServerCertificateResponseTypeDef",
    "ListServiceSpecificCredentialsResponseTypeDef",
    "ListSigningCertificatesResponseTypeDef",
    "UploadSigningCertificateResponseTypeDef",
    "StatementTypeDef",
    "RoleTypeDef",
    "ServiceLastAccessedTypeDef",
    "CreatePolicyResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "ListPoliciesResponseTypeDef",
    "CreateUserResponseTypeDef",
    "GetGroupResponseTypeDef",
    "GetUserResponseTypeDef",
    "ListUsersResponseTypeDef",
    "VirtualMFADeviceTypeDef",
    "GetServiceLinkedRoleDeletionStatusResponseTypeDef",
    "GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef",
    "ListPoliciesGrantingServiceAccessResponseTypeDef",
    "GetServerCertificateResponseTypeDef",
    "ResourceSpecificResultTypeDef",
    "CreateRoleResponseTypeDef",
    "CreateServiceLinkedRoleResponseTypeDef",
    "GetRoleResponseTypeDef",
    "InstanceProfileTypeDef",
    "ListRolesResponseTypeDef",
    "UpdateRoleDescriptionResponseTypeDef",
    "GetServiceLastAccessedDetailsResponseTypeDef",
    "CreateVirtualMFADeviceResponseTypeDef",
    "ListVirtualMFADevicesResponseTypeDef",
    "EvaluationResultTypeDef",
    "CreateInstanceProfileResponseTypeDef",
    "GetInstanceProfileResponseTypeDef",
    "ListInstanceProfilesForRoleResponseTypeDef",
    "ListInstanceProfilesResponseTypeDef",
    "RoleDetailTypeDef",
    "SimulatePolicyResponseTypeDef",
    "GetAccountAuthorizationDetailsResponseTypeDef",
)

_RequiredAccessDetailTypeDef = TypedDict(
    "_RequiredAccessDetailTypeDef",
    {
        "ServiceName": str,
        "ServiceNamespace": str,
    },
)
_OptionalAccessDetailTypeDef = TypedDict(
    "_OptionalAccessDetailTypeDef",
    {
        "Region": str,
        "EntityPath": str,
        "LastAuthenticatedTime": datetime,
        "TotalAuthenticatedEntities": int,
    },
    total=False,
)


class AccessDetailTypeDef(_RequiredAccessDetailTypeDef, _OptionalAccessDetailTypeDef):
    pass


AccessKeyLastUsedTypeDef = TypedDict(
    "AccessKeyLastUsedTypeDef",
    {
        "LastUsedDate": datetime,
        "ServiceName": str,
        "Region": str,
    },
)

AccessKeyMetadataTypeDef = TypedDict(
    "AccessKeyMetadataTypeDef",
    {
        "UserName": str,
        "AccessKeyId": str,
        "Status": statusTypeType,
        "CreateDate": datetime,
    },
    total=False,
)

_RequiredAccessKeyTypeDef = TypedDict(
    "_RequiredAccessKeyTypeDef",
    {
        "UserName": str,
        "AccessKeyId": str,
        "Status": statusTypeType,
        "SecretAccessKey": str,
    },
)
_OptionalAccessKeyTypeDef = TypedDict(
    "_OptionalAccessKeyTypeDef",
    {
        "CreateDate": datetime,
    },
    total=False,
)


class AccessKeyTypeDef(_RequiredAccessKeyTypeDef, _OptionalAccessKeyTypeDef):
    pass


AddClientIDToOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "AddClientIDToOpenIDConnectProviderRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
        "ClientID": str,
    },
)

AddRoleToInstanceProfileRequestInstanceProfileAddRoleTypeDef = TypedDict(
    "AddRoleToInstanceProfileRequestInstanceProfileAddRoleTypeDef",
    {
        "RoleName": str,
    },
)

AddRoleToInstanceProfileRequestRequestTypeDef = TypedDict(
    "AddRoleToInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
        "RoleName": str,
    },
)

AddUserToGroupRequestGroupAddUserTypeDef = TypedDict(
    "AddUserToGroupRequestGroupAddUserTypeDef",
    {
        "UserName": str,
    },
)

AddUserToGroupRequestRequestTypeDef = TypedDict(
    "AddUserToGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "UserName": str,
    },
)

AddUserToGroupRequestUserAddGroupTypeDef = TypedDict(
    "AddUserToGroupRequestUserAddGroupTypeDef",
    {
        "GroupName": str,
    },
)

AttachGroupPolicyRequestGroupAttachPolicyTypeDef = TypedDict(
    "AttachGroupPolicyRequestGroupAttachPolicyTypeDef",
    {
        "PolicyArn": str,
    },
)

AttachGroupPolicyRequestPolicyAttachGroupTypeDef = TypedDict(
    "AttachGroupPolicyRequestPolicyAttachGroupTypeDef",
    {
        "GroupName": str,
    },
)

AttachGroupPolicyRequestRequestTypeDef = TypedDict(
    "AttachGroupPolicyRequestRequestTypeDef",
    {
        "GroupName": str,
        "PolicyArn": str,
    },
)

AttachRolePolicyRequestPolicyAttachRoleTypeDef = TypedDict(
    "AttachRolePolicyRequestPolicyAttachRoleTypeDef",
    {
        "RoleName": str,
    },
)

AttachRolePolicyRequestRequestTypeDef = TypedDict(
    "AttachRolePolicyRequestRequestTypeDef",
    {
        "RoleName": str,
        "PolicyArn": str,
    },
)

AttachRolePolicyRequestRoleAttachPolicyTypeDef = TypedDict(
    "AttachRolePolicyRequestRoleAttachPolicyTypeDef",
    {
        "PolicyArn": str,
    },
)

AttachUserPolicyRequestPolicyAttachUserTypeDef = TypedDict(
    "AttachUserPolicyRequestPolicyAttachUserTypeDef",
    {
        "UserName": str,
    },
)

AttachUserPolicyRequestRequestTypeDef = TypedDict(
    "AttachUserPolicyRequestRequestTypeDef",
    {
        "UserName": str,
        "PolicyArn": str,
    },
)

AttachUserPolicyRequestUserAttachPolicyTypeDef = TypedDict(
    "AttachUserPolicyRequestUserAttachPolicyTypeDef",
    {
        "PolicyArn": str,
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

AttachedPermissionsBoundaryTypeDef = TypedDict(
    "AttachedPermissionsBoundaryTypeDef",
    {
        "PermissionsBoundaryType": Literal["PermissionsBoundaryPolicy"],
        "PermissionsBoundaryArn": str,
    },
    total=False,
)

AttachedPolicyTypeDef = TypedDict(
    "AttachedPolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyArn": str,
    },
    total=False,
)

ChangePasswordRequestRequestTypeDef = TypedDict(
    "ChangePasswordRequestRequestTypeDef",
    {
        "OldPassword": str,
        "NewPassword": str,
    },
)

ChangePasswordRequestServiceResourceChangePasswordTypeDef = TypedDict(
    "ChangePasswordRequestServiceResourceChangePasswordTypeDef",
    {
        "OldPassword": str,
        "NewPassword": str,
    },
)

ContextEntryTypeDef = TypedDict(
    "ContextEntryTypeDef",
    {
        "ContextKeyName": str,
        "ContextKeyValues": Sequence[str],
        "ContextKeyType": ContextKeyTypeEnumType,
    },
    total=False,
)

CreateAccessKeyRequestRequestTypeDef = TypedDict(
    "CreateAccessKeyRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)

CreateAccountAliasRequestRequestTypeDef = TypedDict(
    "CreateAccountAliasRequestRequestTypeDef",
    {
        "AccountAlias": str,
    },
)

CreateAccountAliasRequestServiceResourceCreateAccountAliasTypeDef = TypedDict(
    "CreateAccountAliasRequestServiceResourceCreateAccountAliasTypeDef",
    {
        "AccountAlias": str,
    },
)

CreateGroupRequestGroupCreateTypeDef = TypedDict(
    "CreateGroupRequestGroupCreateTypeDef",
    {
        "Path": str,
    },
    total=False,
)

_RequiredCreateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalCreateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupRequestRequestTypeDef",
    {
        "Path": str,
    },
    total=False,
)


class CreateGroupRequestRequestTypeDef(
    _RequiredCreateGroupRequestRequestTypeDef, _OptionalCreateGroupRequestRequestTypeDef
):
    pass


_RequiredCreateGroupRequestServiceResourceCreateGroupTypeDef = TypedDict(
    "_RequiredCreateGroupRequestServiceResourceCreateGroupTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalCreateGroupRequestServiceResourceCreateGroupTypeDef = TypedDict(
    "_OptionalCreateGroupRequestServiceResourceCreateGroupTypeDef",
    {
        "Path": str,
    },
    total=False,
)


class CreateGroupRequestServiceResourceCreateGroupTypeDef(
    _RequiredCreateGroupRequestServiceResourceCreateGroupTypeDef,
    _OptionalCreateGroupRequestServiceResourceCreateGroupTypeDef,
):
    pass


GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Path": str,
        "GroupName": str,
        "GroupId": str,
        "Arn": str,
        "CreateDate": datetime,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredCreateLoginProfileRequestLoginProfileCreateTypeDef = TypedDict(
    "_RequiredCreateLoginProfileRequestLoginProfileCreateTypeDef",
    {
        "Password": str,
    },
)
_OptionalCreateLoginProfileRequestLoginProfileCreateTypeDef = TypedDict(
    "_OptionalCreateLoginProfileRequestLoginProfileCreateTypeDef",
    {
        "PasswordResetRequired": bool,
    },
    total=False,
)


class CreateLoginProfileRequestLoginProfileCreateTypeDef(
    _RequiredCreateLoginProfileRequestLoginProfileCreateTypeDef,
    _OptionalCreateLoginProfileRequestLoginProfileCreateTypeDef,
):
    pass


_RequiredCreateLoginProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLoginProfileRequestRequestTypeDef",
    {
        "UserName": str,
        "Password": str,
    },
)
_OptionalCreateLoginProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLoginProfileRequestRequestTypeDef",
    {
        "PasswordResetRequired": bool,
    },
    total=False,
)


class CreateLoginProfileRequestRequestTypeDef(
    _RequiredCreateLoginProfileRequestRequestTypeDef,
    _OptionalCreateLoginProfileRequestRequestTypeDef,
):
    pass


_RequiredCreateLoginProfileRequestUserCreateLoginProfileTypeDef = TypedDict(
    "_RequiredCreateLoginProfileRequestUserCreateLoginProfileTypeDef",
    {
        "Password": str,
    },
)
_OptionalCreateLoginProfileRequestUserCreateLoginProfileTypeDef = TypedDict(
    "_OptionalCreateLoginProfileRequestUserCreateLoginProfileTypeDef",
    {
        "PasswordResetRequired": bool,
    },
    total=False,
)


class CreateLoginProfileRequestUserCreateLoginProfileTypeDef(
    _RequiredCreateLoginProfileRequestUserCreateLoginProfileTypeDef,
    _OptionalCreateLoginProfileRequestUserCreateLoginProfileTypeDef,
):
    pass


_RequiredLoginProfileTypeDef = TypedDict(
    "_RequiredLoginProfileTypeDef",
    {
        "UserName": str,
        "CreateDate": datetime,
    },
)
_OptionalLoginProfileTypeDef = TypedDict(
    "_OptionalLoginProfileTypeDef",
    {
        "PasswordResetRequired": bool,
    },
    total=False,
)


class LoginProfileTypeDef(_RequiredLoginProfileTypeDef, _OptionalLoginProfileTypeDef):
    pass


_RequiredCreatePolicyVersionRequestPolicyCreateVersionTypeDef = TypedDict(
    "_RequiredCreatePolicyVersionRequestPolicyCreateVersionTypeDef",
    {
        "PolicyDocument": str,
    },
)
_OptionalCreatePolicyVersionRequestPolicyCreateVersionTypeDef = TypedDict(
    "_OptionalCreatePolicyVersionRequestPolicyCreateVersionTypeDef",
    {
        "SetAsDefault": bool,
    },
    total=False,
)


class CreatePolicyVersionRequestPolicyCreateVersionTypeDef(
    _RequiredCreatePolicyVersionRequestPolicyCreateVersionTypeDef,
    _OptionalCreatePolicyVersionRequestPolicyCreateVersionTypeDef,
):
    pass


_RequiredCreatePolicyVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyVersionRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "PolicyDocument": str,
    },
)
_OptionalCreatePolicyVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyVersionRequestRequestTypeDef",
    {
        "SetAsDefault": bool,
    },
    total=False,
)


class CreatePolicyVersionRequestRequestTypeDef(
    _RequiredCreatePolicyVersionRequestRequestTypeDef,
    _OptionalCreatePolicyVersionRequestRequestTypeDef,
):
    pass


PolicyVersionTypeDef = TypedDict(
    "PolicyVersionTypeDef",
    {
        "Document": str,
        "VersionId": str,
        "IsDefaultVersion": bool,
        "CreateDate": datetime,
    },
    total=False,
)

_RequiredCreateServiceLinkedRoleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceLinkedRoleRequestRequestTypeDef",
    {
        "AWSServiceName": str,
    },
)
_OptionalCreateServiceLinkedRoleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceLinkedRoleRequestRequestTypeDef",
    {
        "Description": str,
        "CustomSuffix": str,
    },
    total=False,
)


class CreateServiceLinkedRoleRequestRequestTypeDef(
    _RequiredCreateServiceLinkedRoleRequestRequestTypeDef,
    _OptionalCreateServiceLinkedRoleRequestRequestTypeDef,
):
    pass


CreateServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "CreateServiceSpecificCredentialRequestRequestTypeDef",
    {
        "UserName": str,
        "ServiceName": str,
    },
)

ServiceSpecificCredentialTypeDef = TypedDict(
    "ServiceSpecificCredentialTypeDef",
    {
        "CreateDate": datetime,
        "ServiceName": str,
        "ServiceUserName": str,
        "ServicePassword": str,
        "ServiceSpecificCredentialId": str,
        "UserName": str,
        "Status": statusTypeType,
    },
)

DeactivateMFADeviceRequestRequestTypeDef = TypedDict(
    "DeactivateMFADeviceRequestRequestTypeDef",
    {
        "UserName": str,
        "SerialNumber": str,
    },
)

_RequiredDeleteAccessKeyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccessKeyRequestRequestTypeDef",
    {
        "AccessKeyId": str,
    },
)
_OptionalDeleteAccessKeyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccessKeyRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class DeleteAccessKeyRequestRequestTypeDef(
    _RequiredDeleteAccessKeyRequestRequestTypeDef, _OptionalDeleteAccessKeyRequestRequestTypeDef
):
    pass


DeleteAccountAliasRequestRequestTypeDef = TypedDict(
    "DeleteAccountAliasRequestRequestTypeDef",
    {
        "AccountAlias": str,
    },
)

DeleteGroupPolicyRequestRequestTypeDef = TypedDict(
    "DeleteGroupPolicyRequestRequestTypeDef",
    {
        "GroupName": str,
        "PolicyName": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)

DeleteInstanceProfileRequestRequestTypeDef = TypedDict(
    "DeleteInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
    },
)

DeleteLoginProfileRequestRequestTypeDef = TypedDict(
    "DeleteLoginProfileRequestRequestTypeDef",
    {
        "UserName": str,
    },
)

DeleteOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "DeleteOpenIDConnectProviderRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
    },
)

DeletePolicyRequestRequestTypeDef = TypedDict(
    "DeletePolicyRequestRequestTypeDef",
    {
        "PolicyArn": str,
    },
)

DeletePolicyVersionRequestRequestTypeDef = TypedDict(
    "DeletePolicyVersionRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "VersionId": str,
    },
)

DeleteRolePermissionsBoundaryRequestRequestTypeDef = TypedDict(
    "DeleteRolePermissionsBoundaryRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)

DeleteRolePolicyRequestRequestTypeDef = TypedDict(
    "DeleteRolePolicyRequestRequestTypeDef",
    {
        "RoleName": str,
        "PolicyName": str,
    },
)

DeleteRoleRequestRequestTypeDef = TypedDict(
    "DeleteRoleRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)

DeleteSAMLProviderRequestRequestTypeDef = TypedDict(
    "DeleteSAMLProviderRequestRequestTypeDef",
    {
        "SAMLProviderArn": str,
    },
)

DeleteSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "DeleteSSHPublicKeyRequestRequestTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
    },
)

DeleteServerCertificateRequestRequestTypeDef = TypedDict(
    "DeleteServerCertificateRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
    },
)

DeleteServiceLinkedRoleRequestRequestTypeDef = TypedDict(
    "DeleteServiceLinkedRoleRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)

_RequiredDeleteServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteServiceSpecificCredentialRequestRequestTypeDef",
    {
        "ServiceSpecificCredentialId": str,
    },
)
_OptionalDeleteServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteServiceSpecificCredentialRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class DeleteServiceSpecificCredentialRequestRequestTypeDef(
    _RequiredDeleteServiceSpecificCredentialRequestRequestTypeDef,
    _OptionalDeleteServiceSpecificCredentialRequestRequestTypeDef,
):
    pass


_RequiredDeleteSigningCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSigningCertificateRequestRequestTypeDef",
    {
        "CertificateId": str,
    },
)
_OptionalDeleteSigningCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSigningCertificateRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class DeleteSigningCertificateRequestRequestTypeDef(
    _RequiredDeleteSigningCertificateRequestRequestTypeDef,
    _OptionalDeleteSigningCertificateRequestRequestTypeDef,
):
    pass


DeleteUserPermissionsBoundaryRequestRequestTypeDef = TypedDict(
    "DeleteUserPermissionsBoundaryRequestRequestTypeDef",
    {
        "UserName": str,
    },
)

DeleteUserPolicyRequestRequestTypeDef = TypedDict(
    "DeleteUserPolicyRequestRequestTypeDef",
    {
        "UserName": str,
        "PolicyName": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
)

DeleteVirtualMFADeviceRequestRequestTypeDef = TypedDict(
    "DeleteVirtualMFADeviceRequestRequestTypeDef",
    {
        "SerialNumber": str,
    },
)

RoleUsageTypeTypeDef = TypedDict(
    "RoleUsageTypeTypeDef",
    {
        "Region": str,
        "Resources": List[str],
    },
    total=False,
)

DetachGroupPolicyRequestGroupDetachPolicyTypeDef = TypedDict(
    "DetachGroupPolicyRequestGroupDetachPolicyTypeDef",
    {
        "PolicyArn": str,
    },
)

DetachGroupPolicyRequestPolicyDetachGroupTypeDef = TypedDict(
    "DetachGroupPolicyRequestPolicyDetachGroupTypeDef",
    {
        "GroupName": str,
    },
)

DetachGroupPolicyRequestRequestTypeDef = TypedDict(
    "DetachGroupPolicyRequestRequestTypeDef",
    {
        "GroupName": str,
        "PolicyArn": str,
    },
)

DetachRolePolicyRequestPolicyDetachRoleTypeDef = TypedDict(
    "DetachRolePolicyRequestPolicyDetachRoleTypeDef",
    {
        "RoleName": str,
    },
)

DetachRolePolicyRequestRequestTypeDef = TypedDict(
    "DetachRolePolicyRequestRequestTypeDef",
    {
        "RoleName": str,
        "PolicyArn": str,
    },
)

DetachRolePolicyRequestRoleDetachPolicyTypeDef = TypedDict(
    "DetachRolePolicyRequestRoleDetachPolicyTypeDef",
    {
        "PolicyArn": str,
    },
)

DetachUserPolicyRequestPolicyDetachUserTypeDef = TypedDict(
    "DetachUserPolicyRequestPolicyDetachUserTypeDef",
    {
        "UserName": str,
    },
)

DetachUserPolicyRequestRequestTypeDef = TypedDict(
    "DetachUserPolicyRequestRequestTypeDef",
    {
        "UserName": str,
        "PolicyArn": str,
    },
)

DetachUserPolicyRequestUserDetachPolicyTypeDef = TypedDict(
    "DetachUserPolicyRequestUserDetachPolicyTypeDef",
    {
        "PolicyArn": str,
    },
)

EnableMFADeviceRequestMfaDeviceAssociateTypeDef = TypedDict(
    "EnableMFADeviceRequestMfaDeviceAssociateTypeDef",
    {
        "AuthenticationCode1": str,
        "AuthenticationCode2": str,
    },
)

EnableMFADeviceRequestRequestTypeDef = TypedDict(
    "EnableMFADeviceRequestRequestTypeDef",
    {
        "UserName": str,
        "SerialNumber": str,
        "AuthenticationCode1": str,
        "AuthenticationCode2": str,
    },
)

EnableMFADeviceRequestUserEnableMfaTypeDef = TypedDict(
    "EnableMFADeviceRequestUserEnableMfaTypeDef",
    {
        "SerialNumber": str,
        "AuthenticationCode1": str,
        "AuthenticationCode2": str,
    },
)

_RequiredEntityInfoTypeDef = TypedDict(
    "_RequiredEntityInfoTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": policyOwnerEntityTypeType,
        "Id": str,
    },
)
_OptionalEntityInfoTypeDef = TypedDict(
    "_OptionalEntityInfoTypeDef",
    {
        "Path": str,
    },
    total=False,
)


class EntityInfoTypeDef(_RequiredEntityInfoTypeDef, _OptionalEntityInfoTypeDef):
    pass


ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "Message": str,
        "Code": str,
    },
)

OrganizationsDecisionDetailTypeDef = TypedDict(
    "OrganizationsDecisionDetailTypeDef",
    {
        "AllowedByOrganizations": bool,
    },
    total=False,
)

PermissionsBoundaryDecisionDetailTypeDef = TypedDict(
    "PermissionsBoundaryDecisionDetailTypeDef",
    {
        "AllowedByPermissionsBoundary": bool,
    },
    total=False,
)

_RequiredGenerateOrganizationsAccessReportRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateOrganizationsAccessReportRequestRequestTypeDef",
    {
        "EntityPath": str,
    },
)
_OptionalGenerateOrganizationsAccessReportRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateOrganizationsAccessReportRequestRequestTypeDef",
    {
        "OrganizationsPolicyId": str,
    },
    total=False,
)


class GenerateOrganizationsAccessReportRequestRequestTypeDef(
    _RequiredGenerateOrganizationsAccessReportRequestRequestTypeDef,
    _OptionalGenerateOrganizationsAccessReportRequestRequestTypeDef,
):
    pass


_RequiredGenerateServiceLastAccessedDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateServiceLastAccessedDetailsRequestRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalGenerateServiceLastAccessedDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateServiceLastAccessedDetailsRequestRequestTypeDef",
    {
        "Granularity": AccessAdvisorUsageGranularityTypeType,
    },
    total=False,
)


class GenerateServiceLastAccessedDetailsRequestRequestTypeDef(
    _RequiredGenerateServiceLastAccessedDetailsRequestRequestTypeDef,
    _OptionalGenerateServiceLastAccessedDetailsRequestRequestTypeDef,
):
    pass


GetAccessKeyLastUsedRequestRequestTypeDef = TypedDict(
    "GetAccessKeyLastUsedRequestRequestTypeDef",
    {
        "AccessKeyId": str,
    },
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

GetAccountAuthorizationDetailsRequestRequestTypeDef = TypedDict(
    "GetAccountAuthorizationDetailsRequestRequestTypeDef",
    {
        "Filter": Sequence[EntityTypeType],
        "MaxItems": int,
        "Marker": str,
    },
    total=False,
)

PasswordPolicyTypeDef = TypedDict(
    "PasswordPolicyTypeDef",
    {
        "MinimumPasswordLength": int,
        "RequireSymbols": bool,
        "RequireNumbers": bool,
        "RequireUppercaseCharacters": bool,
        "RequireLowercaseCharacters": bool,
        "AllowUsersToChangePassword": bool,
        "ExpirePasswords": bool,
        "MaxPasswordAge": int,
        "PasswordReusePrevention": int,
        "HardExpiry": bool,
    },
    total=False,
)

GetContextKeysForCustomPolicyRequestRequestTypeDef = TypedDict(
    "GetContextKeysForCustomPolicyRequestRequestTypeDef",
    {
        "PolicyInputList": Sequence[str],
    },
)

_RequiredGetContextKeysForPrincipalPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetContextKeysForPrincipalPolicyRequestRequestTypeDef",
    {
        "PolicySourceArn": str,
    },
)
_OptionalGetContextKeysForPrincipalPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetContextKeysForPrincipalPolicyRequestRequestTypeDef",
    {
        "PolicyInputList": Sequence[str],
    },
    total=False,
)


class GetContextKeysForPrincipalPolicyRequestRequestTypeDef(
    _RequiredGetContextKeysForPrincipalPolicyRequestRequestTypeDef,
    _OptionalGetContextKeysForPrincipalPolicyRequestRequestTypeDef,
):
    pass


GetGroupPolicyRequestRequestTypeDef = TypedDict(
    "GetGroupPolicyRequestRequestTypeDef",
    {
        "GroupName": str,
        "PolicyName": str,
    },
)

_RequiredGetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredGetGroupRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalGetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalGetGroupRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class GetGroupRequestRequestTypeDef(
    _RequiredGetGroupRequestRequestTypeDef, _OptionalGetGroupRequestRequestTypeDef
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

GetInstanceProfileRequestRequestTypeDef = TypedDict(
    "GetInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
    },
)

GetLoginProfileRequestRequestTypeDef = TypedDict(
    "GetLoginProfileRequestRequestTypeDef",
    {
        "UserName": str,
    },
)

GetOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "GetOpenIDConnectProviderRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
    },
)

_RequiredGetOrganizationsAccessReportRequestRequestTypeDef = TypedDict(
    "_RequiredGetOrganizationsAccessReportRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetOrganizationsAccessReportRequestRequestTypeDef = TypedDict(
    "_OptionalGetOrganizationsAccessReportRequestRequestTypeDef",
    {
        "MaxItems": int,
        "Marker": str,
        "SortKey": sortKeyTypeType,
    },
    total=False,
)


class GetOrganizationsAccessReportRequestRequestTypeDef(
    _RequiredGetOrganizationsAccessReportRequestRequestTypeDef,
    _OptionalGetOrganizationsAccessReportRequestRequestTypeDef,
):
    pass


GetPolicyRequestRequestTypeDef = TypedDict(
    "GetPolicyRequestRequestTypeDef",
    {
        "PolicyArn": str,
    },
)

GetPolicyVersionRequestRequestTypeDef = TypedDict(
    "GetPolicyVersionRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "VersionId": str,
    },
)

GetRolePolicyRequestRequestTypeDef = TypedDict(
    "GetRolePolicyRequestRequestTypeDef",
    {
        "RoleName": str,
        "PolicyName": str,
    },
)

GetRoleRequestRequestTypeDef = TypedDict(
    "GetRoleRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)

GetSAMLProviderRequestRequestTypeDef = TypedDict(
    "GetSAMLProviderRequestRequestTypeDef",
    {
        "SAMLProviderArn": str,
    },
)

GetSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "GetSSHPublicKeyRequestRequestTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
        "Encoding": encodingTypeType,
    },
)

_RequiredSSHPublicKeyTypeDef = TypedDict(
    "_RequiredSSHPublicKeyTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
        "Fingerprint": str,
        "SSHPublicKeyBody": str,
        "Status": statusTypeType,
    },
)
_OptionalSSHPublicKeyTypeDef = TypedDict(
    "_OptionalSSHPublicKeyTypeDef",
    {
        "UploadDate": datetime,
    },
    total=False,
)


class SSHPublicKeyTypeDef(_RequiredSSHPublicKeyTypeDef, _OptionalSSHPublicKeyTypeDef):
    pass


GetServerCertificateRequestRequestTypeDef = TypedDict(
    "GetServerCertificateRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
    },
)

_RequiredGetServiceLastAccessedDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredGetServiceLastAccessedDetailsRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetServiceLastAccessedDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalGetServiceLastAccessedDetailsRequestRequestTypeDef",
    {
        "MaxItems": int,
        "Marker": str,
    },
    total=False,
)


class GetServiceLastAccessedDetailsRequestRequestTypeDef(
    _RequiredGetServiceLastAccessedDetailsRequestRequestTypeDef,
    _OptionalGetServiceLastAccessedDetailsRequestRequestTypeDef,
):
    pass


_RequiredGetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredGetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef",
    {
        "JobId": str,
        "ServiceNamespace": str,
    },
)
_OptionalGetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalGetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef",
    {
        "MaxItems": int,
        "Marker": str,
    },
    total=False,
)


class GetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef(
    _RequiredGetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef,
    _OptionalGetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef,
):
    pass


GetServiceLinkedRoleDeletionStatusRequestRequestTypeDef = TypedDict(
    "GetServiceLinkedRoleDeletionStatusRequestRequestTypeDef",
    {
        "DeletionTaskId": str,
    },
)

GetUserPolicyRequestRequestTypeDef = TypedDict(
    "GetUserPolicyRequestRequestTypeDef",
    {
        "UserName": str,
        "PolicyName": str,
    },
)

GetUserRequestRequestTypeDef = TypedDict(
    "GetUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)

PolicyDetailTypeDef = TypedDict(
    "PolicyDetailTypeDef",
    {
        "PolicyName": str,
        "PolicyDocument": str,
    },
    total=False,
)

GroupPolicyRequestTypeDef = TypedDict(
    "GroupPolicyRequestTypeDef",
    {
        "name": str,
    },
)

ListAccessKeysRequestRequestTypeDef = TypedDict(
    "ListAccessKeysRequestRequestTypeDef",
    {
        "UserName": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListAccountAliasesRequestRequestTypeDef = TypedDict(
    "ListAccountAliasesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredListAttachedGroupPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListAttachedGroupPoliciesRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalListAttachedGroupPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListAttachedGroupPoliciesRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListAttachedGroupPoliciesRequestRequestTypeDef(
    _RequiredListAttachedGroupPoliciesRequestRequestTypeDef,
    _OptionalListAttachedGroupPoliciesRequestRequestTypeDef,
):
    pass


_RequiredListAttachedRolePoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListAttachedRolePoliciesRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListAttachedRolePoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListAttachedRolePoliciesRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListAttachedRolePoliciesRequestRequestTypeDef(
    _RequiredListAttachedRolePoliciesRequestRequestTypeDef,
    _OptionalListAttachedRolePoliciesRequestRequestTypeDef,
):
    pass


_RequiredListAttachedUserPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListAttachedUserPoliciesRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListAttachedUserPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListAttachedUserPoliciesRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListAttachedUserPoliciesRequestRequestTypeDef(
    _RequiredListAttachedUserPoliciesRequestRequestTypeDef,
    _OptionalListAttachedUserPoliciesRequestRequestTypeDef,
):
    pass


_RequiredListEntitiesForPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredListEntitiesForPolicyRequestRequestTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalListEntitiesForPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalListEntitiesForPolicyRequestRequestTypeDef",
    {
        "EntityFilter": EntityTypeType,
        "PathPrefix": str,
        "PolicyUsageFilter": PolicyUsageTypeType,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListEntitiesForPolicyRequestRequestTypeDef(
    _RequiredListEntitiesForPolicyRequestRequestTypeDef,
    _OptionalListEntitiesForPolicyRequestRequestTypeDef,
):
    pass


PolicyGroupTypeDef = TypedDict(
    "PolicyGroupTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
    },
    total=False,
)

PolicyRoleTypeDef = TypedDict(
    "PolicyRoleTypeDef",
    {
        "RoleName": str,
        "RoleId": str,
    },
    total=False,
)

PolicyUserTypeDef = TypedDict(
    "PolicyUserTypeDef",
    {
        "UserName": str,
        "UserId": str,
    },
    total=False,
)

_RequiredListGroupPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupPoliciesRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalListGroupPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupPoliciesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListGroupPoliciesRequestRequestTypeDef(
    _RequiredListGroupPoliciesRequestRequestTypeDef, _OptionalListGroupPoliciesRequestRequestTypeDef
):
    pass


_RequiredListGroupsForUserRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupsForUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListGroupsForUserRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupsForUserRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListGroupsForUserRequestRequestTypeDef(
    _RequiredListGroupsForUserRequestRequestTypeDef, _OptionalListGroupsForUserRequestRequestTypeDef
):
    pass


ListGroupsRequestRequestTypeDef = TypedDict(
    "ListGroupsRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredListInstanceProfileTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListInstanceProfileTagsRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
    },
)
_OptionalListInstanceProfileTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListInstanceProfileTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListInstanceProfileTagsRequestRequestTypeDef(
    _RequiredListInstanceProfileTagsRequestRequestTypeDef,
    _OptionalListInstanceProfileTagsRequestRequestTypeDef,
):
    pass


_RequiredListInstanceProfilesForRoleRequestRequestTypeDef = TypedDict(
    "_RequiredListInstanceProfilesForRoleRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListInstanceProfilesForRoleRequestRequestTypeDef = TypedDict(
    "_OptionalListInstanceProfilesForRoleRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListInstanceProfilesForRoleRequestRequestTypeDef(
    _RequiredListInstanceProfilesForRoleRequestRequestTypeDef,
    _OptionalListInstanceProfilesForRoleRequestRequestTypeDef,
):
    pass


ListInstanceProfilesRequestRequestTypeDef = TypedDict(
    "ListInstanceProfilesRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredListMFADeviceTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListMFADeviceTagsRequestRequestTypeDef",
    {
        "SerialNumber": str,
    },
)
_OptionalListMFADeviceTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListMFADeviceTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListMFADeviceTagsRequestRequestTypeDef(
    _RequiredListMFADeviceTagsRequestRequestTypeDef, _OptionalListMFADeviceTagsRequestRequestTypeDef
):
    pass


ListMFADevicesRequestRequestTypeDef = TypedDict(
    "ListMFADevicesRequestRequestTypeDef",
    {
        "UserName": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

MFADeviceTypeDef = TypedDict(
    "MFADeviceTypeDef",
    {
        "UserName": str,
        "SerialNumber": str,
        "EnableDate": datetime,
    },
)

_RequiredListOpenIDConnectProviderTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListOpenIDConnectProviderTagsRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
    },
)
_OptionalListOpenIDConnectProviderTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListOpenIDConnectProviderTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListOpenIDConnectProviderTagsRequestRequestTypeDef(
    _RequiredListOpenIDConnectProviderTagsRequestRequestTypeDef,
    _OptionalListOpenIDConnectProviderTagsRequestRequestTypeDef,
):
    pass


OpenIDConnectProviderListEntryTypeDef = TypedDict(
    "OpenIDConnectProviderListEntryTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

_RequiredPolicyGrantingServiceAccessTypeDef = TypedDict(
    "_RequiredPolicyGrantingServiceAccessTypeDef",
    {
        "PolicyName": str,
        "PolicyType": policyTypeType,
    },
)
_OptionalPolicyGrantingServiceAccessTypeDef = TypedDict(
    "_OptionalPolicyGrantingServiceAccessTypeDef",
    {
        "PolicyArn": str,
        "EntityType": policyOwnerEntityTypeType,
        "EntityName": str,
    },
    total=False,
)


class PolicyGrantingServiceAccessTypeDef(
    _RequiredPolicyGrantingServiceAccessTypeDef, _OptionalPolicyGrantingServiceAccessTypeDef
):
    pass


_RequiredListPoliciesGrantingServiceAccessRequestRequestTypeDef = TypedDict(
    "_RequiredListPoliciesGrantingServiceAccessRequestRequestTypeDef",
    {
        "Arn": str,
        "ServiceNamespaces": Sequence[str],
    },
)
_OptionalListPoliciesGrantingServiceAccessRequestRequestTypeDef = TypedDict(
    "_OptionalListPoliciesGrantingServiceAccessRequestRequestTypeDef",
    {
        "Marker": str,
    },
    total=False,
)


class ListPoliciesGrantingServiceAccessRequestRequestTypeDef(
    _RequiredListPoliciesGrantingServiceAccessRequestRequestTypeDef,
    _OptionalListPoliciesGrantingServiceAccessRequestRequestTypeDef,
):
    pass


ListPoliciesRequestRequestTypeDef = TypedDict(
    "ListPoliciesRequestRequestTypeDef",
    {
        "Scope": policyScopeTypeType,
        "OnlyAttached": bool,
        "PathPrefix": str,
        "PolicyUsageFilter": PolicyUsageTypeType,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredListPolicyTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListPolicyTagsRequestRequestTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalListPolicyTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListPolicyTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListPolicyTagsRequestRequestTypeDef(
    _RequiredListPolicyTagsRequestRequestTypeDef, _OptionalListPolicyTagsRequestRequestTypeDef
):
    pass


_RequiredListPolicyVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListPolicyVersionsRequestRequestTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalListPolicyVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListPolicyVersionsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListPolicyVersionsRequestRequestTypeDef(
    _RequiredListPolicyVersionsRequestRequestTypeDef,
    _OptionalListPolicyVersionsRequestRequestTypeDef,
):
    pass


_RequiredListRolePoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListRolePoliciesRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListRolePoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListRolePoliciesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListRolePoliciesRequestRequestTypeDef(
    _RequiredListRolePoliciesRequestRequestTypeDef, _OptionalListRolePoliciesRequestRequestTypeDef
):
    pass


_RequiredListRoleTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListRoleTagsRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListRoleTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListRoleTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListRoleTagsRequestRequestTypeDef(
    _RequiredListRoleTagsRequestRequestTypeDef, _OptionalListRoleTagsRequestRequestTypeDef
):
    pass


ListRolesRequestRequestTypeDef = TypedDict(
    "ListRolesRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredListSAMLProviderTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListSAMLProviderTagsRequestRequestTypeDef",
    {
        "SAMLProviderArn": str,
    },
)
_OptionalListSAMLProviderTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListSAMLProviderTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListSAMLProviderTagsRequestRequestTypeDef(
    _RequiredListSAMLProviderTagsRequestRequestTypeDef,
    _OptionalListSAMLProviderTagsRequestRequestTypeDef,
):
    pass


SAMLProviderListEntryTypeDef = TypedDict(
    "SAMLProviderListEntryTypeDef",
    {
        "Arn": str,
        "ValidUntil": datetime,
        "CreateDate": datetime,
    },
    total=False,
)

ListSSHPublicKeysRequestRequestTypeDef = TypedDict(
    "ListSSHPublicKeysRequestRequestTypeDef",
    {
        "UserName": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

SSHPublicKeyMetadataTypeDef = TypedDict(
    "SSHPublicKeyMetadataTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
        "Status": statusTypeType,
        "UploadDate": datetime,
    },
)

_RequiredListServerCertificateTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListServerCertificateTagsRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
    },
)
_OptionalListServerCertificateTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListServerCertificateTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListServerCertificateTagsRequestRequestTypeDef(
    _RequiredListServerCertificateTagsRequestRequestTypeDef,
    _OptionalListServerCertificateTagsRequestRequestTypeDef,
):
    pass


ListServerCertificatesRequestRequestTypeDef = TypedDict(
    "ListServerCertificatesRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredServerCertificateMetadataTypeDef = TypedDict(
    "_RequiredServerCertificateMetadataTypeDef",
    {
        "Path": str,
        "ServerCertificateName": str,
        "ServerCertificateId": str,
        "Arn": str,
    },
)
_OptionalServerCertificateMetadataTypeDef = TypedDict(
    "_OptionalServerCertificateMetadataTypeDef",
    {
        "UploadDate": datetime,
        "Expiration": datetime,
    },
    total=False,
)


class ServerCertificateMetadataTypeDef(
    _RequiredServerCertificateMetadataTypeDef, _OptionalServerCertificateMetadataTypeDef
):
    pass


ListServiceSpecificCredentialsRequestRequestTypeDef = TypedDict(
    "ListServiceSpecificCredentialsRequestRequestTypeDef",
    {
        "UserName": str,
        "ServiceName": str,
    },
    total=False,
)

ServiceSpecificCredentialMetadataTypeDef = TypedDict(
    "ServiceSpecificCredentialMetadataTypeDef",
    {
        "UserName": str,
        "Status": statusTypeType,
        "ServiceUserName": str,
        "CreateDate": datetime,
        "ServiceSpecificCredentialId": str,
        "ServiceName": str,
    },
)

ListSigningCertificatesRequestRequestTypeDef = TypedDict(
    "ListSigningCertificatesRequestRequestTypeDef",
    {
        "UserName": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

_RequiredSigningCertificateTypeDef = TypedDict(
    "_RequiredSigningCertificateTypeDef",
    {
        "UserName": str,
        "CertificateId": str,
        "CertificateBody": str,
        "Status": statusTypeType,
    },
)
_OptionalSigningCertificateTypeDef = TypedDict(
    "_OptionalSigningCertificateTypeDef",
    {
        "UploadDate": datetime,
    },
    total=False,
)


class SigningCertificateTypeDef(
    _RequiredSigningCertificateTypeDef, _OptionalSigningCertificateTypeDef
):
    pass


_RequiredListUserPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListUserPoliciesRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListUserPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListUserPoliciesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListUserPoliciesRequestRequestTypeDef(
    _RequiredListUserPoliciesRequestRequestTypeDef, _OptionalListUserPoliciesRequestRequestTypeDef
):
    pass


_RequiredListUserTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListUserTagsRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListUserTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListUserTagsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListUserTagsRequestRequestTypeDef(
    _RequiredListUserTagsRequestRequestTypeDef, _OptionalListUserTagsRequestRequestTypeDef
):
    pass


ListUsersRequestRequestTypeDef = TypedDict(
    "ListUsersRequestRequestTypeDef",
    {
        "PathPrefix": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListVirtualMFADevicesRequestRequestTypeDef = TypedDict(
    "ListVirtualMFADevicesRequestRequestTypeDef",
    {
        "AssignmentStatus": assignmentStatusTypeType,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

PositionTypeDef = TypedDict(
    "PositionTypeDef",
    {
        "Line": int,
        "Column": int,
    },
    total=False,
)

PutGroupPolicyRequestGroupCreatePolicyTypeDef = TypedDict(
    "PutGroupPolicyRequestGroupCreatePolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyDocument": str,
    },
)

PutGroupPolicyRequestGroupPolicyPutTypeDef = TypedDict(
    "PutGroupPolicyRequestGroupPolicyPutTypeDef",
    {
        "PolicyDocument": str,
    },
)

PutGroupPolicyRequestRequestTypeDef = TypedDict(
    "PutGroupPolicyRequestRequestTypeDef",
    {
        "GroupName": str,
        "PolicyName": str,
        "PolicyDocument": str,
    },
)

PutRolePermissionsBoundaryRequestRequestTypeDef = TypedDict(
    "PutRolePermissionsBoundaryRequestRequestTypeDef",
    {
        "RoleName": str,
        "PermissionsBoundary": str,
    },
)

PutRolePolicyRequestRequestTypeDef = TypedDict(
    "PutRolePolicyRequestRequestTypeDef",
    {
        "RoleName": str,
        "PolicyName": str,
        "PolicyDocument": str,
    },
)

PutRolePolicyRequestRolePolicyPutTypeDef = TypedDict(
    "PutRolePolicyRequestRolePolicyPutTypeDef",
    {
        "PolicyDocument": str,
    },
)

PutUserPermissionsBoundaryRequestRequestTypeDef = TypedDict(
    "PutUserPermissionsBoundaryRequestRequestTypeDef",
    {
        "UserName": str,
        "PermissionsBoundary": str,
    },
)

PutUserPolicyRequestRequestTypeDef = TypedDict(
    "PutUserPolicyRequestRequestTypeDef",
    {
        "UserName": str,
        "PolicyName": str,
        "PolicyDocument": str,
    },
)

PutUserPolicyRequestUserCreatePolicyTypeDef = TypedDict(
    "PutUserPolicyRequestUserCreatePolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyDocument": str,
    },
)

PutUserPolicyRequestUserPolicyPutTypeDef = TypedDict(
    "PutUserPolicyRequestUserPolicyPutTypeDef",
    {
        "PolicyDocument": str,
    },
)

RemoveClientIDFromOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "RemoveClientIDFromOpenIDConnectProviderRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
        "ClientID": str,
    },
)

RemoveRoleFromInstanceProfileRequestInstanceProfileRemoveRoleTypeDef = TypedDict(
    "RemoveRoleFromInstanceProfileRequestInstanceProfileRemoveRoleTypeDef",
    {
        "RoleName": str,
    },
)

RemoveRoleFromInstanceProfileRequestRequestTypeDef = TypedDict(
    "RemoveRoleFromInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
        "RoleName": str,
    },
)

RemoveUserFromGroupRequestGroupRemoveUserTypeDef = TypedDict(
    "RemoveUserFromGroupRequestGroupRemoveUserTypeDef",
    {
        "UserName": str,
    },
)

RemoveUserFromGroupRequestRequestTypeDef = TypedDict(
    "RemoveUserFromGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "UserName": str,
    },
)

RemoveUserFromGroupRequestUserRemoveGroupTypeDef = TypedDict(
    "RemoveUserFromGroupRequestUserRemoveGroupTypeDef",
    {
        "GroupName": str,
    },
)

_RequiredResetServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "_RequiredResetServiceSpecificCredentialRequestRequestTypeDef",
    {
        "ServiceSpecificCredentialId": str,
    },
)
_OptionalResetServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "_OptionalResetServiceSpecificCredentialRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class ResetServiceSpecificCredentialRequestRequestTypeDef(
    _RequiredResetServiceSpecificCredentialRequestRequestTypeDef,
    _OptionalResetServiceSpecificCredentialRequestRequestTypeDef,
):
    pass


ResyncMFADeviceRequestMfaDeviceResyncTypeDef = TypedDict(
    "ResyncMFADeviceRequestMfaDeviceResyncTypeDef",
    {
        "AuthenticationCode1": str,
        "AuthenticationCode2": str,
    },
)

ResyncMFADeviceRequestRequestTypeDef = TypedDict(
    "ResyncMFADeviceRequestRequestTypeDef",
    {
        "UserName": str,
        "SerialNumber": str,
        "AuthenticationCode1": str,
        "AuthenticationCode2": str,
    },
)

RoleLastUsedTypeDef = TypedDict(
    "RoleLastUsedTypeDef",
    {
        "LastUsedDate": datetime,
        "Region": str,
    },
    total=False,
)

RolePolicyRequestTypeDef = TypedDict(
    "RolePolicyRequestTypeDef",
    {
        "name": str,
    },
)

TrackedActionLastAccessedTypeDef = TypedDict(
    "TrackedActionLastAccessedTypeDef",
    {
        "ActionName": str,
        "LastAccessedEntity": str,
        "LastAccessedTime": datetime,
        "LastAccessedRegion": str,
    },
    total=False,
)

ServiceResourceAccessKeyPairRequestTypeDef = TypedDict(
    "ServiceResourceAccessKeyPairRequestTypeDef",
    {
        "user_name": str,
        "id": str,
        "secret": str,
    },
)

ServiceResourceAccessKeyRequestTypeDef = TypedDict(
    "ServiceResourceAccessKeyRequestTypeDef",
    {
        "user_name": str,
        "id": str,
    },
)

ServiceResourceAssumeRolePolicyRequestTypeDef = TypedDict(
    "ServiceResourceAssumeRolePolicyRequestTypeDef",
    {
        "role_name": str,
    },
)

ServiceResourceGroupPolicyRequestTypeDef = TypedDict(
    "ServiceResourceGroupPolicyRequestTypeDef",
    {
        "group_name": str,
        "name": str,
    },
)

ServiceResourceGroupRequestTypeDef = TypedDict(
    "ServiceResourceGroupRequestTypeDef",
    {
        "name": str,
    },
)

ServiceResourceInstanceProfileRequestTypeDef = TypedDict(
    "ServiceResourceInstanceProfileRequestTypeDef",
    {
        "name": str,
    },
)

ServiceResourceLoginProfileRequestTypeDef = TypedDict(
    "ServiceResourceLoginProfileRequestTypeDef",
    {
        "user_name": str,
    },
)

ServiceResourceMfaDeviceRequestTypeDef = TypedDict(
    "ServiceResourceMfaDeviceRequestTypeDef",
    {
        "user_name": str,
        "serial_number": str,
    },
)

ServiceResourcePolicyRequestTypeDef = TypedDict(
    "ServiceResourcePolicyRequestTypeDef",
    {
        "policy_arn": str,
    },
)

ServiceResourcePolicyVersionRequestTypeDef = TypedDict(
    "ServiceResourcePolicyVersionRequestTypeDef",
    {
        "arn": str,
        "version_id": str,
    },
)

ServiceResourceRolePolicyRequestTypeDef = TypedDict(
    "ServiceResourceRolePolicyRequestTypeDef",
    {
        "role_name": str,
        "name": str,
    },
)

ServiceResourceRoleRequestTypeDef = TypedDict(
    "ServiceResourceRoleRequestTypeDef",
    {
        "name": str,
    },
)

ServiceResourceSamlProviderRequestTypeDef = TypedDict(
    "ServiceResourceSamlProviderRequestTypeDef",
    {
        "arn": str,
    },
)

ServiceResourceServerCertificateRequestTypeDef = TypedDict(
    "ServiceResourceServerCertificateRequestTypeDef",
    {
        "name": str,
    },
)

ServiceResourceSigningCertificateRequestTypeDef = TypedDict(
    "ServiceResourceSigningCertificateRequestTypeDef",
    {
        "user_name": str,
        "id": str,
    },
)

ServiceResourceUserPolicyRequestTypeDef = TypedDict(
    "ServiceResourceUserPolicyRequestTypeDef",
    {
        "user_name": str,
        "name": str,
    },
)

ServiceResourceUserRequestTypeDef = TypedDict(
    "ServiceResourceUserRequestTypeDef",
    {
        "name": str,
    },
)

ServiceResourceVirtualMfaDeviceRequestTypeDef = TypedDict(
    "ServiceResourceVirtualMfaDeviceRequestTypeDef",
    {
        "serial_number": str,
    },
)

SetDefaultPolicyVersionRequestRequestTypeDef = TypedDict(
    "SetDefaultPolicyVersionRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "VersionId": str,
    },
)

SetSecurityTokenServicePreferencesRequestRequestTypeDef = TypedDict(
    "SetSecurityTokenServicePreferencesRequestRequestTypeDef",
    {
        "GlobalEndpointTokenVersion": globalEndpointTokenVersionType,
    },
)

UntagInstanceProfileRequestRequestTypeDef = TypedDict(
    "UntagInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
        "TagKeys": Sequence[str],
    },
)

UntagMFADeviceRequestRequestTypeDef = TypedDict(
    "UntagMFADeviceRequestRequestTypeDef",
    {
        "SerialNumber": str,
        "TagKeys": Sequence[str],
    },
)

UntagOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "UntagOpenIDConnectProviderRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
        "TagKeys": Sequence[str],
    },
)

UntagPolicyRequestRequestTypeDef = TypedDict(
    "UntagPolicyRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "TagKeys": Sequence[str],
    },
)

UntagRoleRequestRequestTypeDef = TypedDict(
    "UntagRoleRequestRequestTypeDef",
    {
        "RoleName": str,
        "TagKeys": Sequence[str],
    },
)

UntagSAMLProviderRequestRequestTypeDef = TypedDict(
    "UntagSAMLProviderRequestRequestTypeDef",
    {
        "SAMLProviderArn": str,
        "TagKeys": Sequence[str],
    },
)

UntagServerCertificateRequestRequestTypeDef = TypedDict(
    "UntagServerCertificateRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
        "TagKeys": Sequence[str],
    },
)

UntagUserRequestRequestTypeDef = TypedDict(
    "UntagUserRequestRequestTypeDef",
    {
        "UserName": str,
        "TagKeys": Sequence[str],
    },
)

UpdateAccessKeyRequestAccessKeyActivateTypeDef = TypedDict(
    "UpdateAccessKeyRequestAccessKeyActivateTypeDef",
    {
        "Status": statusTypeType,
    },
    total=False,
)

UpdateAccessKeyRequestAccessKeyDeactivateTypeDef = TypedDict(
    "UpdateAccessKeyRequestAccessKeyDeactivateTypeDef",
    {
        "Status": statusTypeType,
    },
    total=False,
)

UpdateAccessKeyRequestAccessKeyPairActivateTypeDef = TypedDict(
    "UpdateAccessKeyRequestAccessKeyPairActivateTypeDef",
    {
        "Status": statusTypeType,
    },
    total=False,
)

UpdateAccessKeyRequestAccessKeyPairDeactivateTypeDef = TypedDict(
    "UpdateAccessKeyRequestAccessKeyPairDeactivateTypeDef",
    {
        "Status": statusTypeType,
    },
    total=False,
)

_RequiredUpdateAccessKeyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccessKeyRequestRequestTypeDef",
    {
        "AccessKeyId": str,
        "Status": statusTypeType,
    },
)
_OptionalUpdateAccessKeyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccessKeyRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class UpdateAccessKeyRequestRequestTypeDef(
    _RequiredUpdateAccessKeyRequestRequestTypeDef, _OptionalUpdateAccessKeyRequestRequestTypeDef
):
    pass


UpdateAccountPasswordPolicyRequestAccountPasswordPolicyUpdateTypeDef = TypedDict(
    "UpdateAccountPasswordPolicyRequestAccountPasswordPolicyUpdateTypeDef",
    {
        "MinimumPasswordLength": int,
        "RequireSymbols": bool,
        "RequireNumbers": bool,
        "RequireUppercaseCharacters": bool,
        "RequireLowercaseCharacters": bool,
        "AllowUsersToChangePassword": bool,
        "MaxPasswordAge": int,
        "PasswordReusePrevention": int,
        "HardExpiry": bool,
    },
    total=False,
)

UpdateAccountPasswordPolicyRequestRequestTypeDef = TypedDict(
    "UpdateAccountPasswordPolicyRequestRequestTypeDef",
    {
        "MinimumPasswordLength": int,
        "RequireSymbols": bool,
        "RequireNumbers": bool,
        "RequireUppercaseCharacters": bool,
        "RequireLowercaseCharacters": bool,
        "AllowUsersToChangePassword": bool,
        "MaxPasswordAge": int,
        "PasswordReusePrevention": int,
        "HardExpiry": bool,
    },
    total=False,
)

UpdateAccountPasswordPolicyRequestServiceResourceCreateAccountPasswordPolicyTypeDef = TypedDict(
    "UpdateAccountPasswordPolicyRequestServiceResourceCreateAccountPasswordPolicyTypeDef",
    {
        "MinimumPasswordLength": int,
        "RequireSymbols": bool,
        "RequireNumbers": bool,
        "RequireUppercaseCharacters": bool,
        "RequireLowercaseCharacters": bool,
        "AllowUsersToChangePassword": bool,
        "MaxPasswordAge": int,
        "PasswordReusePrevention": int,
        "HardExpiry": bool,
    },
    total=False,
)

UpdateAssumeRolePolicyRequestAssumeRolePolicyUpdateTypeDef = TypedDict(
    "UpdateAssumeRolePolicyRequestAssumeRolePolicyUpdateTypeDef",
    {
        "PolicyDocument": str,
    },
)

UpdateAssumeRolePolicyRequestRequestTypeDef = TypedDict(
    "UpdateAssumeRolePolicyRequestRequestTypeDef",
    {
        "RoleName": str,
        "PolicyDocument": str,
    },
)

UpdateGroupRequestGroupUpdateTypeDef = TypedDict(
    "UpdateGroupRequestGroupUpdateTypeDef",
    {
        "NewPath": str,
        "NewGroupName": str,
    },
    total=False,
)

_RequiredUpdateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalUpdateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGroupRequestRequestTypeDef",
    {
        "NewPath": str,
        "NewGroupName": str,
    },
    total=False,
)


class UpdateGroupRequestRequestTypeDef(
    _RequiredUpdateGroupRequestRequestTypeDef, _OptionalUpdateGroupRequestRequestTypeDef
):
    pass


UpdateLoginProfileRequestLoginProfileUpdateTypeDef = TypedDict(
    "UpdateLoginProfileRequestLoginProfileUpdateTypeDef",
    {
        "Password": str,
        "PasswordResetRequired": bool,
    },
    total=False,
)

_RequiredUpdateLoginProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLoginProfileRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalUpdateLoginProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLoginProfileRequestRequestTypeDef",
    {
        "Password": str,
        "PasswordResetRequired": bool,
    },
    total=False,
)


class UpdateLoginProfileRequestRequestTypeDef(
    _RequiredUpdateLoginProfileRequestRequestTypeDef,
    _OptionalUpdateLoginProfileRequestRequestTypeDef,
):
    pass


UpdateOpenIDConnectProviderThumbprintRequestRequestTypeDef = TypedDict(
    "UpdateOpenIDConnectProviderThumbprintRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
        "ThumbprintList": Sequence[str],
    },
)

UpdateRoleDescriptionRequestRequestTypeDef = TypedDict(
    "UpdateRoleDescriptionRequestRequestTypeDef",
    {
        "RoleName": str,
        "Description": str,
    },
)

_RequiredUpdateRoleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRoleRequestRequestTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalUpdateRoleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRoleRequestRequestTypeDef",
    {
        "Description": str,
        "MaxSessionDuration": int,
    },
    total=False,
)


class UpdateRoleRequestRequestTypeDef(
    _RequiredUpdateRoleRequestRequestTypeDef, _OptionalUpdateRoleRequestRequestTypeDef
):
    pass


UpdateSAMLProviderRequestRequestTypeDef = TypedDict(
    "UpdateSAMLProviderRequestRequestTypeDef",
    {
        "SAMLMetadataDocument": str,
        "SAMLProviderArn": str,
    },
)

UpdateSAMLProviderRequestSamlProviderUpdateTypeDef = TypedDict(
    "UpdateSAMLProviderRequestSamlProviderUpdateTypeDef",
    {
        "SAMLMetadataDocument": str,
    },
)

UpdateSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "UpdateSSHPublicKeyRequestRequestTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
        "Status": statusTypeType,
    },
)

_RequiredUpdateServerCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServerCertificateRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
    },
)
_OptionalUpdateServerCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServerCertificateRequestRequestTypeDef",
    {
        "NewPath": str,
        "NewServerCertificateName": str,
    },
    total=False,
)


class UpdateServerCertificateRequestRequestTypeDef(
    _RequiredUpdateServerCertificateRequestRequestTypeDef,
    _OptionalUpdateServerCertificateRequestRequestTypeDef,
):
    pass


UpdateServerCertificateRequestServerCertificateUpdateTypeDef = TypedDict(
    "UpdateServerCertificateRequestServerCertificateUpdateTypeDef",
    {
        "NewPath": str,
        "NewServerCertificateName": str,
    },
    total=False,
)

_RequiredUpdateServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceSpecificCredentialRequestRequestTypeDef",
    {
        "ServiceSpecificCredentialId": str,
        "Status": statusTypeType,
    },
)
_OptionalUpdateServiceSpecificCredentialRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceSpecificCredentialRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class UpdateServiceSpecificCredentialRequestRequestTypeDef(
    _RequiredUpdateServiceSpecificCredentialRequestRequestTypeDef,
    _OptionalUpdateServiceSpecificCredentialRequestRequestTypeDef,
):
    pass


_RequiredUpdateSigningCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSigningCertificateRequestRequestTypeDef",
    {
        "CertificateId": str,
        "Status": statusTypeType,
    },
)
_OptionalUpdateSigningCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSigningCertificateRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class UpdateSigningCertificateRequestRequestTypeDef(
    _RequiredUpdateSigningCertificateRequestRequestTypeDef,
    _OptionalUpdateSigningCertificateRequestRequestTypeDef,
):
    pass


UpdateSigningCertificateRequestSigningCertificateActivateTypeDef = TypedDict(
    "UpdateSigningCertificateRequestSigningCertificateActivateTypeDef",
    {
        "Status": statusTypeType,
    },
    total=False,
)

UpdateSigningCertificateRequestSigningCertificateDeactivateTypeDef = TypedDict(
    "UpdateSigningCertificateRequestSigningCertificateDeactivateTypeDef",
    {
        "Status": statusTypeType,
    },
    total=False,
)

_RequiredUpdateUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalUpdateUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserRequestRequestTypeDef",
    {
        "NewPath": str,
        "NewUserName": str,
    },
    total=False,
)


class UpdateUserRequestRequestTypeDef(
    _RequiredUpdateUserRequestRequestTypeDef, _OptionalUpdateUserRequestRequestTypeDef
):
    pass


UpdateUserRequestUserUpdateTypeDef = TypedDict(
    "UpdateUserRequestUserUpdateTypeDef",
    {
        "NewPath": str,
        "NewUserName": str,
    },
    total=False,
)

UploadSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "UploadSSHPublicKeyRequestRequestTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyBody": str,
    },
)

_RequiredUploadSigningCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredUploadSigningCertificateRequestRequestTypeDef",
    {
        "CertificateBody": str,
    },
)
_OptionalUploadSigningCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalUploadSigningCertificateRequestRequestTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class UploadSigningCertificateRequestRequestTypeDef(
    _RequiredUploadSigningCertificateRequestRequestTypeDef,
    _OptionalUploadSigningCertificateRequestRequestTypeDef,
):
    pass


_RequiredUploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef = TypedDict(
    "_RequiredUploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef",
    {
        "CertificateBody": str,
    },
)
_OptionalUploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef = TypedDict(
    "_OptionalUploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef",
    {
        "UserName": str,
    },
    total=False,
)


class UploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef(
    _RequiredUploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef,
    _OptionalUploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef,
):
    pass


UserAccessKeyRequestTypeDef = TypedDict(
    "UserAccessKeyRequestTypeDef",
    {
        "id": str,
    },
)

UserMfaDeviceRequestTypeDef = TypedDict(
    "UserMfaDeviceRequestTypeDef",
    {
        "serial_number": str,
    },
)

UserPolicyRequestTypeDef = TypedDict(
    "UserPolicyRequestTypeDef",
    {
        "name": str,
    },
)

UserSigningCertificateRequestTypeDef = TypedDict(
    "UserSigningCertificateRequestTypeDef",
    {
        "id": str,
    },
)

AttachedPermissionsBoundaryResponseMetadataTypeDef = TypedDict(
    "AttachedPermissionsBoundaryResponseMetadataTypeDef",
    {
        "PermissionsBoundaryType": Literal["PermissionsBoundaryPolicy"],
        "PermissionsBoundaryArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessKeyResponseTypeDef = TypedDict(
    "CreateAccessKeyResponseTypeDef",
    {
        "AccessKey": AccessKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceLinkedRoleResponseTypeDef = TypedDict(
    "DeleteServiceLinkedRoleResponseTypeDef",
    {
        "DeletionTaskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateCredentialReportResponseTypeDef = TypedDict(
    "GenerateCredentialReportResponseTypeDef",
    {
        "State": ReportStateTypeType,
        "Description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateOrganizationsAccessReportResponseTypeDef = TypedDict(
    "GenerateOrganizationsAccessReportResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateServiceLastAccessedDetailsResponseTypeDef = TypedDict(
    "GenerateServiceLastAccessedDetailsResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessKeyLastUsedResponseTypeDef = TypedDict(
    "GetAccessKeyLastUsedResponseTypeDef",
    {
        "UserName": str,
        "AccessKeyLastUsed": AccessKeyLastUsedTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountSummaryResponseTypeDef = TypedDict(
    "GetAccountSummaryResponseTypeDef",
    {
        "SummaryMap": Dict[summaryKeyTypeType, int],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContextKeysForPolicyResponseTypeDef = TypedDict(
    "GetContextKeysForPolicyResponseTypeDef",
    {
        "ContextKeyNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCredentialReportResponseTypeDef = TypedDict(
    "GetCredentialReportResponseTypeDef",
    {
        "Content": bytes,
        "ReportFormat": Literal["text/csv"],
        "GeneratedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupPolicyResponseTypeDef = TypedDict(
    "GetGroupPolicyResponseTypeDef",
    {
        "GroupName": str,
        "PolicyName": str,
        "PolicyDocument": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRolePolicyResponseTypeDef = TypedDict(
    "GetRolePolicyResponseTypeDef",
    {
        "RoleName": str,
        "PolicyName": str,
        "PolicyDocument": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserPolicyResponseTypeDef = TypedDict(
    "GetUserPolicyResponseTypeDef",
    {
        "UserName": str,
        "PolicyName": str,
        "PolicyDocument": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessKeysResponseTypeDef = TypedDict(
    "ListAccessKeysResponseTypeDef",
    {
        "AccessKeyMetadata": List[AccessKeyMetadataTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAliasesResponseTypeDef = TypedDict(
    "ListAccountAliasesResponseTypeDef",
    {
        "AccountAliases": List[str],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupPoliciesResponseTypeDef = TypedDict(
    "ListGroupPoliciesResponseTypeDef",
    {
        "PolicyNames": List[str],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRolePoliciesResponseTypeDef = TypedDict(
    "ListRolePoliciesResponseTypeDef",
    {
        "PolicyNames": List[str],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserPoliciesResponseTypeDef = TypedDict(
    "ListUserPoliciesResponseTypeDef",
    {
        "PolicyNames": List[str],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RoleLastUsedResponseMetadataTypeDef = TypedDict(
    "RoleLastUsedResponseMetadataTypeDef",
    {
        "LastUsedDate": datetime,
        "Region": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServerCertificateMetadataResponseMetadataTypeDef = TypedDict(
    "ServerCertificateMetadataResponseMetadataTypeDef",
    {
        "Path": str,
        "ServerCertificateName": str,
        "ServerCertificateId": str,
        "Arn": str,
        "UploadDate": datetime,
        "Expiration": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSAMLProviderResponseTypeDef = TypedDict(
    "UpdateSAMLProviderResponseTypeDef",
    {
        "SAMLProviderArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttachedGroupPoliciesResponseTypeDef = TypedDict(
    "ListAttachedGroupPoliciesResponseTypeDef",
    {
        "AttachedPolicies": List[AttachedPolicyTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttachedRolePoliciesResponseTypeDef = TypedDict(
    "ListAttachedRolePoliciesResponseTypeDef",
    {
        "AttachedPolicies": List[AttachedPolicyTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttachedUserPoliciesResponseTypeDef = TypedDict(
    "ListAttachedUserPoliciesResponseTypeDef",
    {
        "AttachedPolicies": List[AttachedPolicyTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSimulateCustomPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredSimulateCustomPolicyRequestRequestTypeDef",
    {
        "PolicyInputList": Sequence[str],
        "ActionNames": Sequence[str],
    },
)
_OptionalSimulateCustomPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalSimulateCustomPolicyRequestRequestTypeDef",
    {
        "PermissionsBoundaryPolicyInputList": Sequence[str],
        "ResourceArns": Sequence[str],
        "ResourcePolicy": str,
        "ResourceOwner": str,
        "CallerArn": str,
        "ContextEntries": Sequence[ContextEntryTypeDef],
        "ResourceHandlingOption": str,
        "MaxItems": int,
        "Marker": str,
    },
    total=False,
)


class SimulateCustomPolicyRequestRequestTypeDef(
    _RequiredSimulateCustomPolicyRequestRequestTypeDef,
    _OptionalSimulateCustomPolicyRequestRequestTypeDef,
):
    pass


_RequiredSimulatePrincipalPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredSimulatePrincipalPolicyRequestRequestTypeDef",
    {
        "PolicySourceArn": str,
        "ActionNames": Sequence[str],
    },
)
_OptionalSimulatePrincipalPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalSimulatePrincipalPolicyRequestRequestTypeDef",
    {
        "PolicyInputList": Sequence[str],
        "PermissionsBoundaryPolicyInputList": Sequence[str],
        "ResourceArns": Sequence[str],
        "ResourcePolicy": str,
        "ResourceOwner": str,
        "CallerArn": str,
        "ContextEntries": Sequence[ContextEntryTypeDef],
        "ResourceHandlingOption": str,
        "MaxItems": int,
        "Marker": str,
    },
    total=False,
)


class SimulatePrincipalPolicyRequestRequestTypeDef(
    _RequiredSimulatePrincipalPolicyRequestRequestTypeDef,
    _OptionalSimulatePrincipalPolicyRequestRequestTypeDef,
):
    pass


CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsForUserResponseTypeDef = TypedDict(
    "ListGroupsForUserResponseTypeDef",
    {
        "Groups": List[GroupTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "Groups": List[GroupTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateInstanceProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
    },
)
_OptionalCreateInstanceProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInstanceProfileRequestRequestTypeDef",
    {
        "Path": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateInstanceProfileRequestRequestTypeDef(
    _RequiredCreateInstanceProfileRequestRequestTypeDef,
    _OptionalCreateInstanceProfileRequestRequestTypeDef,
):
    pass


_RequiredCreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef = TypedDict(
    "_RequiredCreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef",
    {
        "InstanceProfileName": str,
    },
)
_OptionalCreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef = TypedDict(
    "_OptionalCreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef",
    {
        "Path": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef(
    _RequiredCreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef,
    _OptionalCreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef,
):
    pass


_RequiredCreateOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOpenIDConnectProviderRequestRequestTypeDef",
    {
        "Url": str,
        "ThumbprintList": Sequence[str],
    },
)
_OptionalCreateOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOpenIDConnectProviderRequestRequestTypeDef",
    {
        "ClientIDList": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateOpenIDConnectProviderRequestRequestTypeDef(
    _RequiredCreateOpenIDConnectProviderRequestRequestTypeDef,
    _OptionalCreateOpenIDConnectProviderRequestRequestTypeDef,
):
    pass


CreateOpenIDConnectProviderResponseTypeDef = TypedDict(
    "CreateOpenIDConnectProviderResponseTypeDef",
    {
        "OpenIDConnectProviderArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyRequestRequestTypeDef",
    {
        "PolicyName": str,
        "PolicyDocument": str,
    },
)
_OptionalCreatePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyRequestRequestTypeDef",
    {
        "Path": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePolicyRequestRequestTypeDef(
    _RequiredCreatePolicyRequestRequestTypeDef, _OptionalCreatePolicyRequestRequestTypeDef
):
    pass


_RequiredCreatePolicyRequestServiceResourceCreatePolicyTypeDef = TypedDict(
    "_RequiredCreatePolicyRequestServiceResourceCreatePolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyDocument": str,
    },
)
_OptionalCreatePolicyRequestServiceResourceCreatePolicyTypeDef = TypedDict(
    "_OptionalCreatePolicyRequestServiceResourceCreatePolicyTypeDef",
    {
        "Path": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePolicyRequestServiceResourceCreatePolicyTypeDef(
    _RequiredCreatePolicyRequestServiceResourceCreatePolicyTypeDef,
    _OptionalCreatePolicyRequestServiceResourceCreatePolicyTypeDef,
):
    pass


_RequiredCreateRoleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRoleRequestRequestTypeDef",
    {
        "RoleName": str,
        "AssumeRolePolicyDocument": str,
    },
)
_OptionalCreateRoleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRoleRequestRequestTypeDef",
    {
        "Path": str,
        "Description": str,
        "MaxSessionDuration": int,
        "PermissionsBoundary": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRoleRequestRequestTypeDef(
    _RequiredCreateRoleRequestRequestTypeDef, _OptionalCreateRoleRequestRequestTypeDef
):
    pass


_RequiredCreateRoleRequestServiceResourceCreateRoleTypeDef = TypedDict(
    "_RequiredCreateRoleRequestServiceResourceCreateRoleTypeDef",
    {
        "RoleName": str,
        "AssumeRolePolicyDocument": str,
    },
)
_OptionalCreateRoleRequestServiceResourceCreateRoleTypeDef = TypedDict(
    "_OptionalCreateRoleRequestServiceResourceCreateRoleTypeDef",
    {
        "Path": str,
        "Description": str,
        "MaxSessionDuration": int,
        "PermissionsBoundary": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRoleRequestServiceResourceCreateRoleTypeDef(
    _RequiredCreateRoleRequestServiceResourceCreateRoleTypeDef,
    _OptionalCreateRoleRequestServiceResourceCreateRoleTypeDef,
):
    pass


_RequiredCreateSAMLProviderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSAMLProviderRequestRequestTypeDef",
    {
        "SAMLMetadataDocument": str,
        "Name": str,
    },
)
_OptionalCreateSAMLProviderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSAMLProviderRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSAMLProviderRequestRequestTypeDef(
    _RequiredCreateSAMLProviderRequestRequestTypeDef,
    _OptionalCreateSAMLProviderRequestRequestTypeDef,
):
    pass


_RequiredCreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef = TypedDict(
    "_RequiredCreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef",
    {
        "SAMLMetadataDocument": str,
        "Name": str,
    },
)
_OptionalCreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef = TypedDict(
    "_OptionalCreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef(
    _RequiredCreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef,
    _OptionalCreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef,
):
    pass


CreateSAMLProviderResponseTypeDef = TypedDict(
    "CreateSAMLProviderResponseTypeDef",
    {
        "SAMLProviderArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "Path": str,
        "PermissionsBoundary": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass


_RequiredCreateUserRequestServiceResourceCreateUserTypeDef = TypedDict(
    "_RequiredCreateUserRequestServiceResourceCreateUserTypeDef",
    {
        "UserName": str,
    },
)
_OptionalCreateUserRequestServiceResourceCreateUserTypeDef = TypedDict(
    "_OptionalCreateUserRequestServiceResourceCreateUserTypeDef",
    {
        "Path": str,
        "PermissionsBoundary": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUserRequestServiceResourceCreateUserTypeDef(
    _RequiredCreateUserRequestServiceResourceCreateUserTypeDef,
    _OptionalCreateUserRequestServiceResourceCreateUserTypeDef,
):
    pass


CreateUserRequestUserCreateTypeDef = TypedDict(
    "CreateUserRequestUserCreateTypeDef",
    {
        "Path": str,
        "PermissionsBoundary": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

_RequiredCreateVirtualMFADeviceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVirtualMFADeviceRequestRequestTypeDef",
    {
        "VirtualMFADeviceName": str,
    },
)
_OptionalCreateVirtualMFADeviceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVirtualMFADeviceRequestRequestTypeDef",
    {
        "Path": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateVirtualMFADeviceRequestRequestTypeDef(
    _RequiredCreateVirtualMFADeviceRequestRequestTypeDef,
    _OptionalCreateVirtualMFADeviceRequestRequestTypeDef,
):
    pass


_RequiredCreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef = TypedDict(
    "_RequiredCreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef",
    {
        "VirtualMFADeviceName": str,
    },
)
_OptionalCreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef = TypedDict(
    "_OptionalCreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef",
    {
        "Path": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef(
    _RequiredCreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef,
    _OptionalCreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef,
):
    pass


GetOpenIDConnectProviderResponseTypeDef = TypedDict(
    "GetOpenIDConnectProviderResponseTypeDef",
    {
        "Url": str,
        "ClientIDList": List[str],
        "ThumbprintList": List[str],
        "CreateDate": datetime,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSAMLProviderResponseTypeDef = TypedDict(
    "GetSAMLProviderResponseTypeDef",
    {
        "SAMLMetadataDocument": str,
        "CreateDate": datetime,
        "ValidUntil": datetime,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceProfileTagsResponseTypeDef = TypedDict(
    "ListInstanceProfileTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMFADeviceTagsResponseTypeDef = TypedDict(
    "ListMFADeviceTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOpenIDConnectProviderTagsResponseTypeDef = TypedDict(
    "ListOpenIDConnectProviderTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPolicyTagsResponseTypeDef = TypedDict(
    "ListPolicyTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoleTagsResponseTypeDef = TypedDict(
    "ListRoleTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSAMLProviderTagsResponseTypeDef = TypedDict(
    "ListSAMLProviderTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServerCertificateTagsResponseTypeDef = TypedDict(
    "ListServerCertificateTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserTagsResponseTypeDef = TypedDict(
    "ListUserTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyId": str,
        "Arn": str,
        "Path": str,
        "DefaultVersionId": str,
        "AttachmentCount": int,
        "PermissionsBoundaryUsageCount": int,
        "IsAttachable": bool,
        "Description": str,
        "CreateDate": datetime,
        "UpdateDate": datetime,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

TagInstanceProfileRequestRequestTypeDef = TypedDict(
    "TagInstanceProfileRequestRequestTypeDef",
    {
        "InstanceProfileName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagMFADeviceRequestRequestTypeDef = TypedDict(
    "TagMFADeviceRequestRequestTypeDef",
    {
        "SerialNumber": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagOpenIDConnectProviderRequestRequestTypeDef = TypedDict(
    "TagOpenIDConnectProviderRequestRequestTypeDef",
    {
        "OpenIDConnectProviderArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagPolicyRequestRequestTypeDef = TypedDict(
    "TagPolicyRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagRoleRequestRequestTypeDef = TypedDict(
    "TagRoleRequestRequestTypeDef",
    {
        "RoleName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagSAMLProviderRequestRequestTypeDef = TypedDict(
    "TagSAMLProviderRequestRequestTypeDef",
    {
        "SAMLProviderArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagServerCertificateRequestRequestTypeDef = TypedDict(
    "TagServerCertificateRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagUserRequestRequestTypeDef = TypedDict(
    "TagUserRequestRequestTypeDef",
    {
        "UserName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredUploadServerCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredUploadServerCertificateRequestRequestTypeDef",
    {
        "ServerCertificateName": str,
        "CertificateBody": str,
        "PrivateKey": str,
    },
)
_OptionalUploadServerCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalUploadServerCertificateRequestRequestTypeDef",
    {
        "Path": str,
        "CertificateChain": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class UploadServerCertificateRequestRequestTypeDef(
    _RequiredUploadServerCertificateRequestRequestTypeDef,
    _OptionalUploadServerCertificateRequestRequestTypeDef,
):
    pass


_RequiredUploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef = TypedDict(
    "_RequiredUploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef",
    {
        "ServerCertificateName": str,
        "CertificateBody": str,
        "PrivateKey": str,
    },
)
_OptionalUploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef = TypedDict(
    "_OptionalUploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef",
    {
        "Path": str,
        "CertificateChain": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class UploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef(
    _RequiredUploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef,
    _OptionalUploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef,
):
    pass


UserResponseMetadataTypeDef = TypedDict(
    "UserResponseMetadataTypeDef",
    {
        "Path": str,
        "UserName": str,
        "UserId": str,
        "Arn": str,
        "CreateDate": datetime,
        "PasswordLastUsed": datetime,
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUserTypeDef = TypedDict(
    "_RequiredUserTypeDef",
    {
        "Path": str,
        "UserName": str,
        "UserId": str,
        "Arn": str,
        "CreateDate": datetime,
    },
)
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "PasswordLastUsed": datetime,
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)


class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass


CreateLoginProfileResponseTypeDef = TypedDict(
    "CreateLoginProfileResponseTypeDef",
    {
        "LoginProfile": LoginProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLoginProfileResponseTypeDef = TypedDict(
    "GetLoginProfileResponseTypeDef",
    {
        "LoginProfile": LoginProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePolicyVersionResponseTypeDef = TypedDict(
    "CreatePolicyVersionResponseTypeDef",
    {
        "PolicyVersion": PolicyVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPolicyVersionResponseTypeDef = TypedDict(
    "GetPolicyVersionResponseTypeDef",
    {
        "PolicyVersion": PolicyVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPolicyVersionsResponseTypeDef = TypedDict(
    "ListPolicyVersionsResponseTypeDef",
    {
        "Versions": List[PolicyVersionTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ManagedPolicyDetailTypeDef = TypedDict(
    "ManagedPolicyDetailTypeDef",
    {
        "PolicyName": str,
        "PolicyId": str,
        "Arn": str,
        "Path": str,
        "DefaultVersionId": str,
        "AttachmentCount": int,
        "PermissionsBoundaryUsageCount": int,
        "IsAttachable": bool,
        "Description": str,
        "CreateDate": datetime,
        "UpdateDate": datetime,
        "PolicyVersionList": List[PolicyVersionTypeDef],
    },
    total=False,
)

CreateServiceSpecificCredentialResponseTypeDef = TypedDict(
    "CreateServiceSpecificCredentialResponseTypeDef",
    {
        "ServiceSpecificCredential": ServiceSpecificCredentialTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResetServiceSpecificCredentialResponseTypeDef = TypedDict(
    "ResetServiceSpecificCredentialResponseTypeDef",
    {
        "ServiceSpecificCredential": ServiceSpecificCredentialTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletionTaskFailureReasonTypeTypeDef = TypedDict(
    "DeletionTaskFailureReasonTypeTypeDef",
    {
        "Reason": str,
        "RoleUsageList": List[RoleUsageTypeTypeDef],
    },
    total=False,
)

_RequiredEntityDetailsTypeDef = TypedDict(
    "_RequiredEntityDetailsTypeDef",
    {
        "EntityInfo": EntityInfoTypeDef,
    },
)
_OptionalEntityDetailsTypeDef = TypedDict(
    "_OptionalEntityDetailsTypeDef",
    {
        "LastAuthenticated": datetime,
    },
    total=False,
)


class EntityDetailsTypeDef(_RequiredEntityDetailsTypeDef, _OptionalEntityDetailsTypeDef):
    pass


GetOrganizationsAccessReportResponseTypeDef = TypedDict(
    "GetOrganizationsAccessReportResponseTypeDef",
    {
        "JobStatus": jobStatusTypeType,
        "JobCreationDate": datetime,
        "JobCompletionDate": datetime,
        "NumberOfServicesAccessible": int,
        "NumberOfServicesNotAccessed": int,
        "AccessDetails": List[AccessDetailTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ErrorDetails": ErrorDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef = TypedDict(
    "GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef",
    {
        "Filter": Sequence[EntityTypeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetGroupRequestGetGroupPaginateTypeDef = TypedDict(
    "_RequiredGetGroupRequestGetGroupPaginateTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalGetGroupRequestGetGroupPaginateTypeDef = TypedDict(
    "_OptionalGetGroupRequestGetGroupPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetGroupRequestGetGroupPaginateTypeDef(
    _RequiredGetGroupRequestGetGroupPaginateTypeDef, _OptionalGetGroupRequestGetGroupPaginateTypeDef
):
    pass


ListAccessKeysRequestListAccessKeysPaginateTypeDef = TypedDict(
    "ListAccessKeysRequestListAccessKeysPaginateTypeDef",
    {
        "UserName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAccountAliasesRequestListAccountAliasesPaginateTypeDef = TypedDict(
    "ListAccountAliasesRequestListAccountAliasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef(
    _RequiredListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef,
    _OptionalListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef,
):
    pass


_RequiredListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef = TypedDict(
    "_RequiredListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef = TypedDict(
    "_OptionalListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef(
    _RequiredListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef,
    _OptionalListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef,
):
    pass


_RequiredListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef(
    _RequiredListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef,
    _OptionalListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef,
):
    pass


_RequiredListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef = TypedDict(
    "_RequiredListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef = TypedDict(
    "_OptionalListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef",
    {
        "EntityFilter": EntityTypeType,
        "PathPrefix": str,
        "PolicyUsageFilter": PolicyUsageTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef(
    _RequiredListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef,
    _OptionalListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef,
):
    pass


_RequiredListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef(
    _RequiredListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef,
    _OptionalListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef,
):
    pass


_RequiredListGroupsForUserRequestListGroupsForUserPaginateTypeDef = TypedDict(
    "_RequiredListGroupsForUserRequestListGroupsForUserPaginateTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListGroupsForUserRequestListGroupsForUserPaginateTypeDef = TypedDict(
    "_OptionalListGroupsForUserRequestListGroupsForUserPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGroupsForUserRequestListGroupsForUserPaginateTypeDef(
    _RequiredListGroupsForUserRequestListGroupsForUserPaginateTypeDef,
    _OptionalListGroupsForUserRequestListGroupsForUserPaginateTypeDef,
):
    pass


ListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "ListGroupsRequestListGroupsPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef = TypedDict(
    "_RequiredListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef = TypedDict(
    "_OptionalListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef(
    _RequiredListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef,
    _OptionalListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef,
):
    pass


ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef = TypedDict(
    "ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListMFADevicesRequestListMFADevicesPaginateTypeDef = TypedDict(
    "ListMFADevicesRequestListMFADevicesPaginateTypeDef",
    {
        "UserName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPoliciesRequestListPoliciesPaginateTypeDef = TypedDict(
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    {
        "Scope": policyScopeTypeType,
        "OnlyAttached": bool,
        "PathPrefix": str,
        "PolicyUsageFilter": PolicyUsageTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef = TypedDict(
    "_RequiredListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef = TypedDict(
    "_OptionalListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef(
    _RequiredListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef,
    _OptionalListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef,
):
    pass


_RequiredListRolePoliciesRequestListRolePoliciesPaginateTypeDef = TypedDict(
    "_RequiredListRolePoliciesRequestListRolePoliciesPaginateTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalListRolePoliciesRequestListRolePoliciesPaginateTypeDef = TypedDict(
    "_OptionalListRolePoliciesRequestListRolePoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRolePoliciesRequestListRolePoliciesPaginateTypeDef(
    _RequiredListRolePoliciesRequestListRolePoliciesPaginateTypeDef,
    _OptionalListRolePoliciesRequestListRolePoliciesPaginateTypeDef,
):
    pass


ListRolesRequestListRolesPaginateTypeDef = TypedDict(
    "ListRolesRequestListRolesPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef = TypedDict(
    "ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef",
    {
        "UserName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServerCertificatesRequestListServerCertificatesPaginateTypeDef = TypedDict(
    "ListServerCertificatesRequestListServerCertificatesPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef = TypedDict(
    "ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef",
    {
        "UserName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListUserPoliciesRequestListUserPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListUserPoliciesRequestListUserPoliciesPaginateTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListUserPoliciesRequestListUserPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListUserPoliciesRequestListUserPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUserPoliciesRequestListUserPoliciesPaginateTypeDef(
    _RequiredListUserPoliciesRequestListUserPoliciesPaginateTypeDef,
    _OptionalListUserPoliciesRequestListUserPoliciesPaginateTypeDef,
):
    pass


_RequiredListUserTagsRequestListUserTagsPaginateTypeDef = TypedDict(
    "_RequiredListUserTagsRequestListUserTagsPaginateTypeDef",
    {
        "UserName": str,
    },
)
_OptionalListUserTagsRequestListUserTagsPaginateTypeDef = TypedDict(
    "_OptionalListUserTagsRequestListUserTagsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUserTagsRequestListUserTagsPaginateTypeDef(
    _RequiredListUserTagsRequestListUserTagsPaginateTypeDef,
    _OptionalListUserTagsRequestListUserTagsPaginateTypeDef,
):
    pass


ListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "ListUsersRequestListUsersPaginateTypeDef",
    {
        "PathPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef = TypedDict(
    "ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef",
    {
        "AssignmentStatus": assignmentStatusTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredSimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef = TypedDict(
    "_RequiredSimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef",
    {
        "PolicyInputList": Sequence[str],
        "ActionNames": Sequence[str],
    },
)
_OptionalSimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef = TypedDict(
    "_OptionalSimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef",
    {
        "PermissionsBoundaryPolicyInputList": Sequence[str],
        "ResourceArns": Sequence[str],
        "ResourcePolicy": str,
        "ResourceOwner": str,
        "CallerArn": str,
        "ContextEntries": Sequence[ContextEntryTypeDef],
        "ResourceHandlingOption": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef(
    _RequiredSimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef,
    _OptionalSimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef,
):
    pass


_RequiredSimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef = TypedDict(
    "_RequiredSimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef",
    {
        "PolicySourceArn": str,
        "ActionNames": Sequence[str],
    },
)
_OptionalSimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef = TypedDict(
    "_OptionalSimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef",
    {
        "PolicyInputList": Sequence[str],
        "PermissionsBoundaryPolicyInputList": Sequence[str],
        "ResourceArns": Sequence[str],
        "ResourcePolicy": str,
        "ResourceOwner": str,
        "CallerArn": str,
        "ContextEntries": Sequence[ContextEntryTypeDef],
        "ResourceHandlingOption": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef(
    _RequiredSimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef,
    _OptionalSimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef,
):
    pass


GetAccountPasswordPolicyResponseTypeDef = TypedDict(
    "GetAccountPasswordPolicyResponseTypeDef",
    {
        "PasswordPolicy": PasswordPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetInstanceProfileRequestInstanceProfileExistsWaitTypeDef = TypedDict(
    "_RequiredGetInstanceProfileRequestInstanceProfileExistsWaitTypeDef",
    {
        "InstanceProfileName": str,
    },
)
_OptionalGetInstanceProfileRequestInstanceProfileExistsWaitTypeDef = TypedDict(
    "_OptionalGetInstanceProfileRequestInstanceProfileExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetInstanceProfileRequestInstanceProfileExistsWaitTypeDef(
    _RequiredGetInstanceProfileRequestInstanceProfileExistsWaitTypeDef,
    _OptionalGetInstanceProfileRequestInstanceProfileExistsWaitTypeDef,
):
    pass


_RequiredGetPolicyRequestPolicyExistsWaitTypeDef = TypedDict(
    "_RequiredGetPolicyRequestPolicyExistsWaitTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalGetPolicyRequestPolicyExistsWaitTypeDef = TypedDict(
    "_OptionalGetPolicyRequestPolicyExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetPolicyRequestPolicyExistsWaitTypeDef(
    _RequiredGetPolicyRequestPolicyExistsWaitTypeDef,
    _OptionalGetPolicyRequestPolicyExistsWaitTypeDef,
):
    pass


_RequiredGetRoleRequestRoleExistsWaitTypeDef = TypedDict(
    "_RequiredGetRoleRequestRoleExistsWaitTypeDef",
    {
        "RoleName": str,
    },
)
_OptionalGetRoleRequestRoleExistsWaitTypeDef = TypedDict(
    "_OptionalGetRoleRequestRoleExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetRoleRequestRoleExistsWaitTypeDef(
    _RequiredGetRoleRequestRoleExistsWaitTypeDef, _OptionalGetRoleRequestRoleExistsWaitTypeDef
):
    pass


GetUserRequestUserExistsWaitTypeDef = TypedDict(
    "GetUserRequestUserExistsWaitTypeDef",
    {
        "UserName": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

GetSSHPublicKeyResponseTypeDef = TypedDict(
    "GetSSHPublicKeyResponseTypeDef",
    {
        "SSHPublicKey": SSHPublicKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UploadSSHPublicKeyResponseTypeDef = TypedDict(
    "UploadSSHPublicKeyResponseTypeDef",
    {
        "SSHPublicKey": SSHPublicKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GroupDetailTypeDef = TypedDict(
    "GroupDetailTypeDef",
    {
        "Path": str,
        "GroupName": str,
        "GroupId": str,
        "Arn": str,
        "CreateDate": datetime,
        "GroupPolicyList": List[PolicyDetailTypeDef],
        "AttachedManagedPolicies": List[AttachedPolicyTypeDef],
    },
    total=False,
)

UserDetailTypeDef = TypedDict(
    "UserDetailTypeDef",
    {
        "Path": str,
        "UserName": str,
        "UserId": str,
        "Arn": str,
        "CreateDate": datetime,
        "UserPolicyList": List[PolicyDetailTypeDef],
        "GroupList": List[str],
        "AttachedManagedPolicies": List[AttachedPolicyTypeDef],
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

ListEntitiesForPolicyResponseTypeDef = TypedDict(
    "ListEntitiesForPolicyResponseTypeDef",
    {
        "PolicyGroups": List[PolicyGroupTypeDef],
        "PolicyUsers": List[PolicyUserTypeDef],
        "PolicyRoles": List[PolicyRoleTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMFADevicesResponseTypeDef = TypedDict(
    "ListMFADevicesResponseTypeDef",
    {
        "MFADevices": List[MFADeviceTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOpenIDConnectProvidersResponseTypeDef = TypedDict(
    "ListOpenIDConnectProvidersResponseTypeDef",
    {
        "OpenIDConnectProviderList": List[OpenIDConnectProviderListEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPoliciesGrantingServiceAccessEntryTypeDef = TypedDict(
    "ListPoliciesGrantingServiceAccessEntryTypeDef",
    {
        "ServiceNamespace": str,
        "Policies": List[PolicyGrantingServiceAccessTypeDef],
    },
    total=False,
)

ListSAMLProvidersResponseTypeDef = TypedDict(
    "ListSAMLProvidersResponseTypeDef",
    {
        "SAMLProviderList": List[SAMLProviderListEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSSHPublicKeysResponseTypeDef = TypedDict(
    "ListSSHPublicKeysResponseTypeDef",
    {
        "SSHPublicKeys": List[SSHPublicKeyMetadataTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServerCertificatesResponseTypeDef = TypedDict(
    "ListServerCertificatesResponseTypeDef",
    {
        "ServerCertificateMetadataList": List[ServerCertificateMetadataTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredServerCertificateTypeDef = TypedDict(
    "_RequiredServerCertificateTypeDef",
    {
        "ServerCertificateMetadata": ServerCertificateMetadataTypeDef,
        "CertificateBody": str,
    },
)
_OptionalServerCertificateTypeDef = TypedDict(
    "_OptionalServerCertificateTypeDef",
    {
        "CertificateChain": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)


class ServerCertificateTypeDef(
    _RequiredServerCertificateTypeDef, _OptionalServerCertificateTypeDef
):
    pass


UploadServerCertificateResponseTypeDef = TypedDict(
    "UploadServerCertificateResponseTypeDef",
    {
        "ServerCertificateMetadata": ServerCertificateMetadataTypeDef,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceSpecificCredentialsResponseTypeDef = TypedDict(
    "ListServiceSpecificCredentialsResponseTypeDef",
    {
        "ServiceSpecificCredentials": List[ServiceSpecificCredentialMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSigningCertificatesResponseTypeDef = TypedDict(
    "ListSigningCertificatesResponseTypeDef",
    {
        "Certificates": List[SigningCertificateTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UploadSigningCertificateResponseTypeDef = TypedDict(
    "UploadSigningCertificateResponseTypeDef",
    {
        "Certificate": SigningCertificateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StatementTypeDef = TypedDict(
    "StatementTypeDef",
    {
        "SourcePolicyId": str,
        "SourcePolicyType": PolicySourceTypeType,
        "StartPosition": PositionTypeDef,
        "EndPosition": PositionTypeDef,
    },
    total=False,
)

_RequiredRoleTypeDef = TypedDict(
    "_RequiredRoleTypeDef",
    {
        "Path": str,
        "RoleName": str,
        "RoleId": str,
        "Arn": str,
        "CreateDate": datetime,
    },
)
_OptionalRoleTypeDef = TypedDict(
    "_OptionalRoleTypeDef",
    {
        "AssumeRolePolicyDocument": str,
        "Description": str,
        "MaxSessionDuration": int,
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
        "RoleLastUsed": RoleLastUsedTypeDef,
    },
    total=False,
)


class RoleTypeDef(_RequiredRoleTypeDef, _OptionalRoleTypeDef):
    pass


_RequiredServiceLastAccessedTypeDef = TypedDict(
    "_RequiredServiceLastAccessedTypeDef",
    {
        "ServiceName": str,
        "ServiceNamespace": str,
    },
)
_OptionalServiceLastAccessedTypeDef = TypedDict(
    "_OptionalServiceLastAccessedTypeDef",
    {
        "LastAuthenticated": datetime,
        "LastAuthenticatedEntity": str,
        "LastAuthenticatedRegion": str,
        "TotalAuthenticatedEntities": int,
        "TrackedActionsLastAccessed": List[TrackedActionLastAccessedTypeDef],
    },
    total=False,
)


class ServiceLastAccessedTypeDef(
    _RequiredServiceLastAccessedTypeDef, _OptionalServiceLastAccessedTypeDef
):
    pass


CreatePolicyResponseTypeDef = TypedDict(
    "CreatePolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {
        "Policies": List[PolicyTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupResponseTypeDef = TypedDict(
    "GetGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "Users": List[UserTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserResponseTypeDef = TypedDict(
    "GetUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "Users": List[UserTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredVirtualMFADeviceTypeDef = TypedDict(
    "_RequiredVirtualMFADeviceTypeDef",
    {
        "SerialNumber": str,
    },
)
_OptionalVirtualMFADeviceTypeDef = TypedDict(
    "_OptionalVirtualMFADeviceTypeDef",
    {
        "Base32StringSeed": bytes,
        "QRCodePNG": bytes,
        "User": UserTypeDef,
        "EnableDate": datetime,
        "Tags": List[TagTypeDef],
    },
    total=False,
)


class VirtualMFADeviceTypeDef(_RequiredVirtualMFADeviceTypeDef, _OptionalVirtualMFADeviceTypeDef):
    pass


GetServiceLinkedRoleDeletionStatusResponseTypeDef = TypedDict(
    "GetServiceLinkedRoleDeletionStatusResponseTypeDef",
    {
        "Status": DeletionTaskStatusTypeType,
        "Reason": DeletionTaskFailureReasonTypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef = TypedDict(
    "GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef",
    {
        "JobStatus": jobStatusTypeType,
        "JobCreationDate": datetime,
        "JobCompletionDate": datetime,
        "EntityDetailsList": List[EntityDetailsTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "Error": ErrorDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPoliciesGrantingServiceAccessResponseTypeDef = TypedDict(
    "ListPoliciesGrantingServiceAccessResponseTypeDef",
    {
        "PoliciesGrantingServiceAccess": List[ListPoliciesGrantingServiceAccessEntryTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServerCertificateResponseTypeDef = TypedDict(
    "GetServerCertificateResponseTypeDef",
    {
        "ServerCertificate": ServerCertificateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredResourceSpecificResultTypeDef = TypedDict(
    "_RequiredResourceSpecificResultTypeDef",
    {
        "EvalResourceName": str,
        "EvalResourceDecision": PolicyEvaluationDecisionTypeType,
    },
)
_OptionalResourceSpecificResultTypeDef = TypedDict(
    "_OptionalResourceSpecificResultTypeDef",
    {
        "MatchedStatements": List[StatementTypeDef],
        "MissingContextValues": List[str],
        "EvalDecisionDetails": Dict[str, PolicyEvaluationDecisionTypeType],
        "PermissionsBoundaryDecisionDetail": PermissionsBoundaryDecisionDetailTypeDef,
    },
    total=False,
)


class ResourceSpecificResultTypeDef(
    _RequiredResourceSpecificResultTypeDef, _OptionalResourceSpecificResultTypeDef
):
    pass


CreateRoleResponseTypeDef = TypedDict(
    "CreateRoleResponseTypeDef",
    {
        "Role": RoleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceLinkedRoleResponseTypeDef = TypedDict(
    "CreateServiceLinkedRoleResponseTypeDef",
    {
        "Role": RoleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRoleResponseTypeDef = TypedDict(
    "GetRoleResponseTypeDef",
    {
        "Role": RoleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredInstanceProfileTypeDef = TypedDict(
    "_RequiredInstanceProfileTypeDef",
    {
        "Path": str,
        "InstanceProfileName": str,
        "InstanceProfileId": str,
        "Arn": str,
        "CreateDate": datetime,
        "Roles": List[RoleTypeDef],
    },
)
_OptionalInstanceProfileTypeDef = TypedDict(
    "_OptionalInstanceProfileTypeDef",
    {
        "Tags": List[TagTypeDef],
    },
    total=False,
)


class InstanceProfileTypeDef(_RequiredInstanceProfileTypeDef, _OptionalInstanceProfileTypeDef):
    pass


ListRolesResponseTypeDef = TypedDict(
    "ListRolesResponseTypeDef",
    {
        "Roles": List[RoleTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRoleDescriptionResponseTypeDef = TypedDict(
    "UpdateRoleDescriptionResponseTypeDef",
    {
        "Role": RoleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceLastAccessedDetailsResponseTypeDef = TypedDict(
    "GetServiceLastAccessedDetailsResponseTypeDef",
    {
        "JobStatus": jobStatusTypeType,
        "JobType": AccessAdvisorUsageGranularityTypeType,
        "JobCreationDate": datetime,
        "ServicesLastAccessed": List[ServiceLastAccessedTypeDef],
        "JobCompletionDate": datetime,
        "IsTruncated": bool,
        "Marker": str,
        "Error": ErrorDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVirtualMFADeviceResponseTypeDef = TypedDict(
    "CreateVirtualMFADeviceResponseTypeDef",
    {
        "VirtualMFADevice": VirtualMFADeviceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualMFADevicesResponseTypeDef = TypedDict(
    "ListVirtualMFADevicesResponseTypeDef",
    {
        "VirtualMFADevices": List[VirtualMFADeviceTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredEvaluationResultTypeDef = TypedDict(
    "_RequiredEvaluationResultTypeDef",
    {
        "EvalActionName": str,
        "EvalDecision": PolicyEvaluationDecisionTypeType,
    },
)
_OptionalEvaluationResultTypeDef = TypedDict(
    "_OptionalEvaluationResultTypeDef",
    {
        "EvalResourceName": str,
        "MatchedStatements": List[StatementTypeDef],
        "MissingContextValues": List[str],
        "OrganizationsDecisionDetail": OrganizationsDecisionDetailTypeDef,
        "PermissionsBoundaryDecisionDetail": PermissionsBoundaryDecisionDetailTypeDef,
        "EvalDecisionDetails": Dict[str, PolicyEvaluationDecisionTypeType],
        "ResourceSpecificResults": List[ResourceSpecificResultTypeDef],
    },
    total=False,
)


class EvaluationResultTypeDef(_RequiredEvaluationResultTypeDef, _OptionalEvaluationResultTypeDef):
    pass


CreateInstanceProfileResponseTypeDef = TypedDict(
    "CreateInstanceProfileResponseTypeDef",
    {
        "InstanceProfile": InstanceProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInstanceProfileResponseTypeDef = TypedDict(
    "GetInstanceProfileResponseTypeDef",
    {
        "InstanceProfile": InstanceProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceProfilesForRoleResponseTypeDef = TypedDict(
    "ListInstanceProfilesForRoleResponseTypeDef",
    {
        "InstanceProfiles": List[InstanceProfileTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceProfilesResponseTypeDef = TypedDict(
    "ListInstanceProfilesResponseTypeDef",
    {
        "InstanceProfiles": List[InstanceProfileTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RoleDetailTypeDef = TypedDict(
    "RoleDetailTypeDef",
    {
        "Path": str,
        "RoleName": str,
        "RoleId": str,
        "Arn": str,
        "CreateDate": datetime,
        "AssumeRolePolicyDocument": str,
        "InstanceProfileList": List[InstanceProfileTypeDef],
        "RolePolicyList": List[PolicyDetailTypeDef],
        "AttachedManagedPolicies": List[AttachedPolicyTypeDef],
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
        "RoleLastUsed": RoleLastUsedTypeDef,
    },
    total=False,
)

SimulatePolicyResponseTypeDef = TypedDict(
    "SimulatePolicyResponseTypeDef",
    {
        "EvaluationResults": List[EvaluationResultTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountAuthorizationDetailsResponseTypeDef = TypedDict(
    "GetAccountAuthorizationDetailsResponseTypeDef",
    {
        "UserDetailList": List[UserDetailTypeDef],
        "GroupDetailList": List[GroupDetailTypeDef],
        "RoleDetailList": List[RoleDetailTypeDef],
        "Policies": List[ManagedPolicyDetailTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
