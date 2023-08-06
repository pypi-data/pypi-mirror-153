"""
Type annotations for workmail service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmail/type_defs/)

Usage::

    ```python
    from mypy_boto3_workmail.type_defs import AccessControlRuleTypeDef

    data: AccessControlRuleTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AccessControlRuleEffectType,
    DnsRecordVerificationStatusType,
    EntityStateType,
    FolderNameType,
    MailboxExportJobStateType,
    MemberTypeType,
    MobileDeviceAccessRuleEffectType,
    PermissionTypeType,
    ResourceTypeType,
    RetentionActionType,
    UserRoleType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessControlRuleTypeDef",
    "AssociateDelegateToResourceRequestRequestTypeDef",
    "AssociateMemberToGroupRequestRequestTypeDef",
    "BookingOptionsTypeDef",
    "CancelMailboxExportJobRequestRequestTypeDef",
    "CreateAliasRequestRequestTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateMobileDeviceAccessRuleRequestRequestTypeDef",
    "DomainTypeDef",
    "CreateResourceRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DelegateTypeDef",
    "DeleteAccessControlRuleRequestRequestTypeDef",
    "DeleteAliasRequestRequestTypeDef",
    "DeleteEmailMonitoringConfigurationRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteMailboxPermissionsRequestRequestTypeDef",
    "DeleteMobileDeviceAccessOverrideRequestRequestTypeDef",
    "DeleteMobileDeviceAccessRuleRequestRequestTypeDef",
    "DeleteOrganizationRequestRequestTypeDef",
    "DeleteResourceRequestRequestTypeDef",
    "DeleteRetentionPolicyRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeregisterFromWorkMailRequestRequestTypeDef",
    "DeregisterMailDomainRequestRequestTypeDef",
    "DescribeEmailMonitoringConfigurationRequestRequestTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeInboundDmarcSettingsRequestRequestTypeDef",
    "DescribeMailboxExportJobRequestRequestTypeDef",
    "DescribeOrganizationRequestRequestTypeDef",
    "DescribeResourceRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DisassociateDelegateFromResourceRequestRequestTypeDef",
    "DisassociateMemberFromGroupRequestRequestTypeDef",
    "DnsRecordTypeDef",
    "FolderConfigurationTypeDef",
    "GetAccessControlEffectRequestRequestTypeDef",
    "GetDefaultRetentionPolicyRequestRequestTypeDef",
    "GetMailDomainRequestRequestTypeDef",
    "GetMailboxDetailsRequestRequestTypeDef",
    "GetMobileDeviceAccessEffectRequestRequestTypeDef",
    "MobileDeviceAccessMatchedRuleTypeDef",
    "GetMobileDeviceAccessOverrideRequestRequestTypeDef",
    "GroupTypeDef",
    "ListAccessControlRulesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListGroupMembersRequestRequestTypeDef",
    "MemberTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListMailDomainsRequestRequestTypeDef",
    "MailDomainSummaryTypeDef",
    "ListMailboxExportJobsRequestRequestTypeDef",
    "MailboxExportJobTypeDef",
    "ListMailboxPermissionsRequestRequestTypeDef",
    "PermissionTypeDef",
    "ListMobileDeviceAccessOverridesRequestRequestTypeDef",
    "MobileDeviceAccessOverrideTypeDef",
    "ListMobileDeviceAccessRulesRequestRequestTypeDef",
    "MobileDeviceAccessRuleTypeDef",
    "ListOrganizationsRequestRequestTypeDef",
    "OrganizationSummaryTypeDef",
    "ListResourceDelegatesRequestRequestTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ResourceTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ListUsersRequestRequestTypeDef",
    "UserTypeDef",
    "PutAccessControlRuleRequestRequestTypeDef",
    "PutEmailMonitoringConfigurationRequestRequestTypeDef",
    "PutInboundDmarcSettingsRequestRequestTypeDef",
    "PutMailboxPermissionsRequestRequestTypeDef",
    "PutMobileDeviceAccessOverrideRequestRequestTypeDef",
    "RegisterMailDomainRequestRequestTypeDef",
    "RegisterToWorkMailRequestRequestTypeDef",
    "ResetPasswordRequestRequestTypeDef",
    "StartMailboxExportJobRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDefaultMailDomainRequestRequestTypeDef",
    "UpdateMailboxQuotaRequestRequestTypeDef",
    "UpdateMobileDeviceAccessRuleRequestRequestTypeDef",
    "UpdatePrimaryEmailAddressRequestRequestTypeDef",
    "UpdateResourceRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateMobileDeviceAccessRuleResponseTypeDef",
    "CreateOrganizationResponseTypeDef",
    "CreateResourceResponseTypeDef",
    "CreateUserResponseTypeDef",
    "DeleteOrganizationResponseTypeDef",
    "DescribeEmailMonitoringConfigurationResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeInboundDmarcSettingsResponseTypeDef",
    "DescribeMailboxExportJobResponseTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DescribeResourceResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "GetAccessControlEffectResponseTypeDef",
    "GetMailboxDetailsResponseTypeDef",
    "GetMobileDeviceAccessOverrideResponseTypeDef",
    "ListAccessControlRulesResponseTypeDef",
    "ListAliasesResponseTypeDef",
    "StartMailboxExportJobResponseTypeDef",
    "CreateOrganizationRequestRequestTypeDef",
    "ListResourceDelegatesResponseTypeDef",
    "GetMailDomainResponseTypeDef",
    "GetDefaultRetentionPolicyResponseTypeDef",
    "PutRetentionPolicyRequestRequestTypeDef",
    "GetMobileDeviceAccessEffectResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListGroupMembersRequestListGroupMembersPaginateTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef",
    "ListOrganizationsRequestListOrganizationsPaginateTypeDef",
    "ListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef",
    "ListResourcesRequestListResourcesPaginateTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListGroupMembersResponseTypeDef",
    "ListMailDomainsResponseTypeDef",
    "ListMailboxExportJobsResponseTypeDef",
    "ListMailboxPermissionsResponseTypeDef",
    "ListMobileDeviceAccessOverridesResponseTypeDef",
    "ListMobileDeviceAccessRulesResponseTypeDef",
    "ListOrganizationsResponseTypeDef",
    "ListResourcesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
)

AccessControlRuleTypeDef = TypedDict(
    "AccessControlRuleTypeDef",
    {
        "Name": str,
        "Effect": AccessControlRuleEffectType,
        "Description": str,
        "IpRanges": List[str],
        "NotIpRanges": List[str],
        "Actions": List[str],
        "NotActions": List[str],
        "UserIds": List[str],
        "NotUserIds": List[str],
        "DateCreated": datetime,
        "DateModified": datetime,
    },
    total=False,
)

AssociateDelegateToResourceRequestRequestTypeDef = TypedDict(
    "AssociateDelegateToResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
        "EntityId": str,
    },
)

AssociateMemberToGroupRequestRequestTypeDef = TypedDict(
    "AssociateMemberToGroupRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "GroupId": str,
        "MemberId": str,
    },
)

BookingOptionsTypeDef = TypedDict(
    "BookingOptionsTypeDef",
    {
        "AutoAcceptRequests": bool,
        "AutoDeclineRecurringRequests": bool,
        "AutoDeclineConflictingRequests": bool,
    },
    total=False,
)

CancelMailboxExportJobRequestRequestTypeDef = TypedDict(
    "CancelMailboxExportJobRequestRequestTypeDef",
    {
        "ClientToken": str,
        "JobId": str,
        "OrganizationId": str,
    },
)

CreateAliasRequestRequestTypeDef = TypedDict(
    "CreateAliasRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
        "Alias": str,
    },
)

CreateGroupRequestRequestTypeDef = TypedDict(
    "CreateGroupRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
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

_RequiredCreateMobileDeviceAccessRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMobileDeviceAccessRuleRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
        "Effect": MobileDeviceAccessRuleEffectType,
    },
)
_OptionalCreateMobileDeviceAccessRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMobileDeviceAccessRuleRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "DeviceTypes": Sequence[str],
        "NotDeviceTypes": Sequence[str],
        "DeviceModels": Sequence[str],
        "NotDeviceModels": Sequence[str],
        "DeviceOperatingSystems": Sequence[str],
        "NotDeviceOperatingSystems": Sequence[str],
        "DeviceUserAgents": Sequence[str],
        "NotDeviceUserAgents": Sequence[str],
    },
    total=False,
)


class CreateMobileDeviceAccessRuleRequestRequestTypeDef(
    _RequiredCreateMobileDeviceAccessRuleRequestRequestTypeDef,
    _OptionalCreateMobileDeviceAccessRuleRequestRequestTypeDef,
):
    pass


DomainTypeDef = TypedDict(
    "DomainTypeDef",
    {
        "DomainName": str,
        "HostedZoneId": str,
    },
    total=False,
)

CreateResourceRequestRequestTypeDef = TypedDict(
    "CreateResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
        "Type": ResourceTypeType,
    },
)

CreateUserRequestRequestTypeDef = TypedDict(
    "CreateUserRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
        "DisplayName": str,
        "Password": str,
    },
)

DelegateTypeDef = TypedDict(
    "DelegateTypeDef",
    {
        "Id": str,
        "Type": MemberTypeType,
    },
)

DeleteAccessControlRuleRequestRequestTypeDef = TypedDict(
    "DeleteAccessControlRuleRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
    },
)

DeleteAliasRequestRequestTypeDef = TypedDict(
    "DeleteAliasRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
        "Alias": str,
    },
)

DeleteEmailMonitoringConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteEmailMonitoringConfigurationRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "GroupId": str,
    },
)

DeleteMailboxPermissionsRequestRequestTypeDef = TypedDict(
    "DeleteMailboxPermissionsRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
        "GranteeId": str,
    },
)

DeleteMobileDeviceAccessOverrideRequestRequestTypeDef = TypedDict(
    "DeleteMobileDeviceAccessOverrideRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
        "DeviceId": str,
    },
)

DeleteMobileDeviceAccessRuleRequestRequestTypeDef = TypedDict(
    "DeleteMobileDeviceAccessRuleRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "MobileDeviceAccessRuleId": str,
    },
)

_RequiredDeleteOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteOrganizationRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "DeleteDirectory": bool,
    },
)
_OptionalDeleteOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteOrganizationRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class DeleteOrganizationRequestRequestTypeDef(
    _RequiredDeleteOrganizationRequestRequestTypeDef,
    _OptionalDeleteOrganizationRequestRequestTypeDef,
):
    pass


DeleteResourceRequestRequestTypeDef = TypedDict(
    "DeleteResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
    },
)

DeleteRetentionPolicyRequestRequestTypeDef = TypedDict(
    "DeleteRetentionPolicyRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Id": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
    },
)

DeregisterFromWorkMailRequestRequestTypeDef = TypedDict(
    "DeregisterFromWorkMailRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
    },
)

DeregisterMailDomainRequestRequestTypeDef = TypedDict(
    "DeregisterMailDomainRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "DomainName": str,
    },
)

DescribeEmailMonitoringConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeEmailMonitoringConfigurationRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)

DescribeGroupRequestRequestTypeDef = TypedDict(
    "DescribeGroupRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "GroupId": str,
    },
)

DescribeInboundDmarcSettingsRequestRequestTypeDef = TypedDict(
    "DescribeInboundDmarcSettingsRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)

DescribeMailboxExportJobRequestRequestTypeDef = TypedDict(
    "DescribeMailboxExportJobRequestRequestTypeDef",
    {
        "JobId": str,
        "OrganizationId": str,
    },
)

DescribeOrganizationRequestRequestTypeDef = TypedDict(
    "DescribeOrganizationRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)

DescribeResourceRequestRequestTypeDef = TypedDict(
    "DescribeResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
    },
)

DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
    },
)

DisassociateDelegateFromResourceRequestRequestTypeDef = TypedDict(
    "DisassociateDelegateFromResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
        "EntityId": str,
    },
)

DisassociateMemberFromGroupRequestRequestTypeDef = TypedDict(
    "DisassociateMemberFromGroupRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "GroupId": str,
        "MemberId": str,
    },
)

DnsRecordTypeDef = TypedDict(
    "DnsRecordTypeDef",
    {
        "Type": str,
        "Hostname": str,
        "Value": str,
    },
    total=False,
)

_RequiredFolderConfigurationTypeDef = TypedDict(
    "_RequiredFolderConfigurationTypeDef",
    {
        "Name": FolderNameType,
        "Action": RetentionActionType,
    },
)
_OptionalFolderConfigurationTypeDef = TypedDict(
    "_OptionalFolderConfigurationTypeDef",
    {
        "Period": int,
    },
    total=False,
)


class FolderConfigurationTypeDef(
    _RequiredFolderConfigurationTypeDef, _OptionalFolderConfigurationTypeDef
):
    pass


GetAccessControlEffectRequestRequestTypeDef = TypedDict(
    "GetAccessControlEffectRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "IpAddress": str,
        "Action": str,
        "UserId": str,
    },
)

GetDefaultRetentionPolicyRequestRequestTypeDef = TypedDict(
    "GetDefaultRetentionPolicyRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)

GetMailDomainRequestRequestTypeDef = TypedDict(
    "GetMailDomainRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "DomainName": str,
    },
)

GetMailboxDetailsRequestRequestTypeDef = TypedDict(
    "GetMailboxDetailsRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
    },
)

_RequiredGetMobileDeviceAccessEffectRequestRequestTypeDef = TypedDict(
    "_RequiredGetMobileDeviceAccessEffectRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalGetMobileDeviceAccessEffectRequestRequestTypeDef = TypedDict(
    "_OptionalGetMobileDeviceAccessEffectRequestRequestTypeDef",
    {
        "DeviceType": str,
        "DeviceModel": str,
        "DeviceOperatingSystem": str,
        "DeviceUserAgent": str,
    },
    total=False,
)


class GetMobileDeviceAccessEffectRequestRequestTypeDef(
    _RequiredGetMobileDeviceAccessEffectRequestRequestTypeDef,
    _OptionalGetMobileDeviceAccessEffectRequestRequestTypeDef,
):
    pass


MobileDeviceAccessMatchedRuleTypeDef = TypedDict(
    "MobileDeviceAccessMatchedRuleTypeDef",
    {
        "MobileDeviceAccessRuleId": str,
        "Name": str,
    },
    total=False,
)

GetMobileDeviceAccessOverrideRequestRequestTypeDef = TypedDict(
    "GetMobileDeviceAccessOverrideRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
        "DeviceId": str,
    },
)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Id": str,
        "Email": str,
        "Name": str,
        "State": EntityStateType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

ListAccessControlRulesRequestRequestTypeDef = TypedDict(
    "ListAccessControlRulesRequestRequestTypeDef",
    {
        "OrganizationId": str,
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

_RequiredListAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListAliasesRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
    },
)
_OptionalListAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListAliasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAliasesRequestRequestTypeDef(
    _RequiredListAliasesRequestRequestTypeDef, _OptionalListAliasesRequestRequestTypeDef
):
    pass


_RequiredListGroupMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupMembersRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "GroupId": str,
    },
)
_OptionalListGroupMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupMembersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListGroupMembersRequestRequestTypeDef(
    _RequiredListGroupMembersRequestRequestTypeDef, _OptionalListGroupMembersRequestRequestTypeDef
):
    pass


MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "Id": str,
        "Name": str,
        "Type": MemberTypeType,
        "State": EntityStateType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

_RequiredListGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupsRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListGroupsRequestRequestTypeDef(
    _RequiredListGroupsRequestRequestTypeDef, _OptionalListGroupsRequestRequestTypeDef
):
    pass


_RequiredListMailDomainsRequestRequestTypeDef = TypedDict(
    "_RequiredListMailDomainsRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListMailDomainsRequestRequestTypeDef = TypedDict(
    "_OptionalListMailDomainsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListMailDomainsRequestRequestTypeDef(
    _RequiredListMailDomainsRequestRequestTypeDef, _OptionalListMailDomainsRequestRequestTypeDef
):
    pass


MailDomainSummaryTypeDef = TypedDict(
    "MailDomainSummaryTypeDef",
    {
        "DomainName": str,
        "DefaultDomain": bool,
    },
    total=False,
)

_RequiredListMailboxExportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListMailboxExportJobsRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListMailboxExportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListMailboxExportJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListMailboxExportJobsRequestRequestTypeDef(
    _RequiredListMailboxExportJobsRequestRequestTypeDef,
    _OptionalListMailboxExportJobsRequestRequestTypeDef,
):
    pass


MailboxExportJobTypeDef = TypedDict(
    "MailboxExportJobTypeDef",
    {
        "JobId": str,
        "EntityId": str,
        "Description": str,
        "S3BucketName": str,
        "S3Path": str,
        "EstimatedProgress": int,
        "State": MailboxExportJobStateType,
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

_RequiredListMailboxPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredListMailboxPermissionsRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
    },
)
_OptionalListMailboxPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalListMailboxPermissionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListMailboxPermissionsRequestRequestTypeDef(
    _RequiredListMailboxPermissionsRequestRequestTypeDef,
    _OptionalListMailboxPermissionsRequestRequestTypeDef,
):
    pass


PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "GranteeId": str,
        "GranteeType": MemberTypeType,
        "PermissionValues": List[PermissionTypeType],
    },
)

_RequiredListMobileDeviceAccessOverridesRequestRequestTypeDef = TypedDict(
    "_RequiredListMobileDeviceAccessOverridesRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListMobileDeviceAccessOverridesRequestRequestTypeDef = TypedDict(
    "_OptionalListMobileDeviceAccessOverridesRequestRequestTypeDef",
    {
        "UserId": str,
        "DeviceId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListMobileDeviceAccessOverridesRequestRequestTypeDef(
    _RequiredListMobileDeviceAccessOverridesRequestRequestTypeDef,
    _OptionalListMobileDeviceAccessOverridesRequestRequestTypeDef,
):
    pass


MobileDeviceAccessOverrideTypeDef = TypedDict(
    "MobileDeviceAccessOverrideTypeDef",
    {
        "UserId": str,
        "DeviceId": str,
        "Effect": MobileDeviceAccessRuleEffectType,
        "Description": str,
        "DateCreated": datetime,
        "DateModified": datetime,
    },
    total=False,
)

ListMobileDeviceAccessRulesRequestRequestTypeDef = TypedDict(
    "ListMobileDeviceAccessRulesRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)

MobileDeviceAccessRuleTypeDef = TypedDict(
    "MobileDeviceAccessRuleTypeDef",
    {
        "MobileDeviceAccessRuleId": str,
        "Name": str,
        "Description": str,
        "Effect": MobileDeviceAccessRuleEffectType,
        "DeviceTypes": List[str],
        "NotDeviceTypes": List[str],
        "DeviceModels": List[str],
        "NotDeviceModels": List[str],
        "DeviceOperatingSystems": List[str],
        "NotDeviceOperatingSystems": List[str],
        "DeviceUserAgents": List[str],
        "NotDeviceUserAgents": List[str],
        "DateCreated": datetime,
        "DateModified": datetime,
    },
    total=False,
)

ListOrganizationsRequestRequestTypeDef = TypedDict(
    "ListOrganizationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

OrganizationSummaryTypeDef = TypedDict(
    "OrganizationSummaryTypeDef",
    {
        "OrganizationId": str,
        "Alias": str,
        "DefaultMailDomain": str,
        "ErrorMessage": str,
        "State": str,
    },
    total=False,
)

_RequiredListResourceDelegatesRequestRequestTypeDef = TypedDict(
    "_RequiredListResourceDelegatesRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
    },
)
_OptionalListResourceDelegatesRequestRequestTypeDef = TypedDict(
    "_OptionalListResourceDelegatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListResourceDelegatesRequestRequestTypeDef(
    _RequiredListResourceDelegatesRequestRequestTypeDef,
    _OptionalListResourceDelegatesRequestRequestTypeDef,
):
    pass


_RequiredListResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListResourcesRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListResourcesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListResourcesRequestRequestTypeDef(
    _RequiredListResourcesRequestRequestTypeDef, _OptionalListResourcesRequestRequestTypeDef
):
    pass


ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Id": str,
        "Email": str,
        "Name": str,
        "Type": ResourceTypeType,
        "State": EntityStateType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass


UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Id": str,
        "Email": str,
        "Name": str,
        "DisplayName": str,
        "State": EntityStateType,
        "UserRole": UserRoleType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

_RequiredPutAccessControlRuleRequestRequestTypeDef = TypedDict(
    "_RequiredPutAccessControlRuleRequestRequestTypeDef",
    {
        "Name": str,
        "Effect": AccessControlRuleEffectType,
        "Description": str,
        "OrganizationId": str,
    },
)
_OptionalPutAccessControlRuleRequestRequestTypeDef = TypedDict(
    "_OptionalPutAccessControlRuleRequestRequestTypeDef",
    {
        "IpRanges": Sequence[str],
        "NotIpRanges": Sequence[str],
        "Actions": Sequence[str],
        "NotActions": Sequence[str],
        "UserIds": Sequence[str],
        "NotUserIds": Sequence[str],
    },
    total=False,
)


class PutAccessControlRuleRequestRequestTypeDef(
    _RequiredPutAccessControlRuleRequestRequestTypeDef,
    _OptionalPutAccessControlRuleRequestRequestTypeDef,
):
    pass


PutEmailMonitoringConfigurationRequestRequestTypeDef = TypedDict(
    "PutEmailMonitoringConfigurationRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "RoleArn": str,
        "LogGroupArn": str,
    },
)

PutInboundDmarcSettingsRequestRequestTypeDef = TypedDict(
    "PutInboundDmarcSettingsRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Enforced": bool,
    },
)

PutMailboxPermissionsRequestRequestTypeDef = TypedDict(
    "PutMailboxPermissionsRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
        "GranteeId": str,
        "PermissionValues": Sequence[PermissionTypeType],
    },
)

_RequiredPutMobileDeviceAccessOverrideRequestRequestTypeDef = TypedDict(
    "_RequiredPutMobileDeviceAccessOverrideRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
        "DeviceId": str,
        "Effect": MobileDeviceAccessRuleEffectType,
    },
)
_OptionalPutMobileDeviceAccessOverrideRequestRequestTypeDef = TypedDict(
    "_OptionalPutMobileDeviceAccessOverrideRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class PutMobileDeviceAccessOverrideRequestRequestTypeDef(
    _RequiredPutMobileDeviceAccessOverrideRequestRequestTypeDef,
    _OptionalPutMobileDeviceAccessOverrideRequestRequestTypeDef,
):
    pass


_RequiredRegisterMailDomainRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterMailDomainRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "DomainName": str,
    },
)
_OptionalRegisterMailDomainRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterMailDomainRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class RegisterMailDomainRequestRequestTypeDef(
    _RequiredRegisterMailDomainRequestRequestTypeDef,
    _OptionalRegisterMailDomainRequestRequestTypeDef,
):
    pass


RegisterToWorkMailRequestRequestTypeDef = TypedDict(
    "RegisterToWorkMailRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
        "Email": str,
    },
)

ResetPasswordRequestRequestTypeDef = TypedDict(
    "ResetPasswordRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
        "Password": str,
    },
)

_RequiredStartMailboxExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartMailboxExportJobRequestRequestTypeDef",
    {
        "ClientToken": str,
        "OrganizationId": str,
        "EntityId": str,
        "RoleArn": str,
        "KmsKeyArn": str,
        "S3BucketName": str,
        "S3Prefix": str,
    },
)
_OptionalStartMailboxExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartMailboxExportJobRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class StartMailboxExportJobRequestRequestTypeDef(
    _RequiredStartMailboxExportJobRequestRequestTypeDef,
    _OptionalStartMailboxExportJobRequestRequestTypeDef,
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateDefaultMailDomainRequestRequestTypeDef = TypedDict(
    "UpdateDefaultMailDomainRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "DomainName": str,
    },
)

UpdateMailboxQuotaRequestRequestTypeDef = TypedDict(
    "UpdateMailboxQuotaRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "UserId": str,
        "MailboxQuota": int,
    },
)

_RequiredUpdateMobileDeviceAccessRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMobileDeviceAccessRuleRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "MobileDeviceAccessRuleId": str,
        "Name": str,
        "Effect": MobileDeviceAccessRuleEffectType,
    },
)
_OptionalUpdateMobileDeviceAccessRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMobileDeviceAccessRuleRequestRequestTypeDef",
    {
        "Description": str,
        "DeviceTypes": Sequence[str],
        "NotDeviceTypes": Sequence[str],
        "DeviceModels": Sequence[str],
        "NotDeviceModels": Sequence[str],
        "DeviceOperatingSystems": Sequence[str],
        "NotDeviceOperatingSystems": Sequence[str],
        "DeviceUserAgents": Sequence[str],
        "NotDeviceUserAgents": Sequence[str],
    },
    total=False,
)


class UpdateMobileDeviceAccessRuleRequestRequestTypeDef(
    _RequiredUpdateMobileDeviceAccessRuleRequestRequestTypeDef,
    _OptionalUpdateMobileDeviceAccessRuleRequestRequestTypeDef,
):
    pass


UpdatePrimaryEmailAddressRequestRequestTypeDef = TypedDict(
    "UpdatePrimaryEmailAddressRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
        "Email": str,
    },
)

_RequiredUpdateResourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResourceRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
    },
)
_OptionalUpdateResourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResourceRequestRequestTypeDef",
    {
        "Name": str,
        "BookingOptions": BookingOptionsTypeDef,
    },
    total=False,
)


class UpdateResourceRequestRequestTypeDef(
    _RequiredUpdateResourceRequestRequestTypeDef, _OptionalUpdateResourceRequestRequestTypeDef
):
    pass


CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "GroupId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMobileDeviceAccessRuleResponseTypeDef = TypedDict(
    "CreateMobileDeviceAccessRuleResponseTypeDef",
    {
        "MobileDeviceAccessRuleId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOrganizationResponseTypeDef = TypedDict(
    "CreateOrganizationResponseTypeDef",
    {
        "OrganizationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourceResponseTypeDef = TypedDict(
    "CreateResourceResponseTypeDef",
    {
        "ResourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "UserId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteOrganizationResponseTypeDef = TypedDict(
    "DeleteOrganizationResponseTypeDef",
    {
        "OrganizationId": str,
        "State": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEmailMonitoringConfigurationResponseTypeDef = TypedDict(
    "DescribeEmailMonitoringConfigurationResponseTypeDef",
    {
        "RoleArn": str,
        "LogGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {
        "GroupId": str,
        "Name": str,
        "Email": str,
        "State": EntityStateType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInboundDmarcSettingsResponseTypeDef = TypedDict(
    "DescribeInboundDmarcSettingsResponseTypeDef",
    {
        "Enforced": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMailboxExportJobResponseTypeDef = TypedDict(
    "DescribeMailboxExportJobResponseTypeDef",
    {
        "EntityId": str,
        "Description": str,
        "RoleArn": str,
        "KmsKeyArn": str,
        "S3BucketName": str,
        "S3Prefix": str,
        "S3Path": str,
        "EstimatedProgress": int,
        "State": MailboxExportJobStateType,
        "ErrorInfo": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationResponseTypeDef = TypedDict(
    "DescribeOrganizationResponseTypeDef",
    {
        "OrganizationId": str,
        "Alias": str,
        "State": str,
        "DirectoryId": str,
        "DirectoryType": str,
        "DefaultMailDomain": str,
        "CompletedDate": datetime,
        "ErrorMessage": str,
        "ARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResourceResponseTypeDef = TypedDict(
    "DescribeResourceResponseTypeDef",
    {
        "ResourceId": str,
        "Email": str,
        "Name": str,
        "Type": ResourceTypeType,
        "BookingOptions": BookingOptionsTypeDef,
        "State": EntityStateType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "UserId": str,
        "Name": str,
        "Email": str,
        "DisplayName": str,
        "State": EntityStateType,
        "UserRole": UserRoleType,
        "EnabledDate": datetime,
        "DisabledDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessControlEffectResponseTypeDef = TypedDict(
    "GetAccessControlEffectResponseTypeDef",
    {
        "Effect": AccessControlRuleEffectType,
        "MatchedRules": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMailboxDetailsResponseTypeDef = TypedDict(
    "GetMailboxDetailsResponseTypeDef",
    {
        "MailboxQuota": int,
        "MailboxSize": float,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMobileDeviceAccessOverrideResponseTypeDef = TypedDict(
    "GetMobileDeviceAccessOverrideResponseTypeDef",
    {
        "UserId": str,
        "DeviceId": str,
        "Effect": MobileDeviceAccessRuleEffectType,
        "Description": str,
        "DateCreated": datetime,
        "DateModified": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessControlRulesResponseTypeDef = TypedDict(
    "ListAccessControlRulesResponseTypeDef",
    {
        "Rules": List[AccessControlRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef",
    {
        "Aliases": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMailboxExportJobResponseTypeDef = TypedDict(
    "StartMailboxExportJobResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOrganizationRequestRequestTypeDef",
    {
        "Alias": str,
    },
)
_OptionalCreateOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOrganizationRequestRequestTypeDef",
    {
        "DirectoryId": str,
        "ClientToken": str,
        "Domains": Sequence[DomainTypeDef],
        "KmsKeyArn": str,
        "EnableInteroperability": bool,
    },
    total=False,
)


class CreateOrganizationRequestRequestTypeDef(
    _RequiredCreateOrganizationRequestRequestTypeDef,
    _OptionalCreateOrganizationRequestRequestTypeDef,
):
    pass


ListResourceDelegatesResponseTypeDef = TypedDict(
    "ListResourceDelegatesResponseTypeDef",
    {
        "Delegates": List[DelegateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMailDomainResponseTypeDef = TypedDict(
    "GetMailDomainResponseTypeDef",
    {
        "Records": List[DnsRecordTypeDef],
        "IsTestDomain": bool,
        "IsDefault": bool,
        "OwnershipVerificationStatus": DnsRecordVerificationStatusType,
        "DkimVerificationStatus": DnsRecordVerificationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDefaultRetentionPolicyResponseTypeDef = TypedDict(
    "GetDefaultRetentionPolicyResponseTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "FolderConfigurations": List[FolderConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutRetentionPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutRetentionPolicyRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Name": str,
        "FolderConfigurations": Sequence[FolderConfigurationTypeDef],
    },
)
_OptionalPutRetentionPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutRetentionPolicyRequestRequestTypeDef",
    {
        "Id": str,
        "Description": str,
    },
    total=False,
)


class PutRetentionPolicyRequestRequestTypeDef(
    _RequiredPutRetentionPolicyRequestRequestTypeDef,
    _OptionalPutRetentionPolicyRequestRequestTypeDef,
):
    pass


GetMobileDeviceAccessEffectResponseTypeDef = TypedDict(
    "GetMobileDeviceAccessEffectResponseTypeDef",
    {
        "Effect": MobileDeviceAccessRuleEffectType,
        "MatchedRules": List[MobileDeviceAccessMatchedRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "Groups": List[GroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "_RequiredListAliasesRequestListAliasesPaginateTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
    },
)
_OptionalListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "_OptionalListAliasesRequestListAliasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAliasesRequestListAliasesPaginateTypeDef(
    _RequiredListAliasesRequestListAliasesPaginateTypeDef,
    _OptionalListAliasesRequestListAliasesPaginateTypeDef,
):
    pass


_RequiredListGroupMembersRequestListGroupMembersPaginateTypeDef = TypedDict(
    "_RequiredListGroupMembersRequestListGroupMembersPaginateTypeDef",
    {
        "OrganizationId": str,
        "GroupId": str,
    },
)
_OptionalListGroupMembersRequestListGroupMembersPaginateTypeDef = TypedDict(
    "_OptionalListGroupMembersRequestListGroupMembersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGroupMembersRequestListGroupMembersPaginateTypeDef(
    _RequiredListGroupMembersRequestListGroupMembersPaginateTypeDef,
    _OptionalListGroupMembersRequestListGroupMembersPaginateTypeDef,
):
    pass


_RequiredListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "_RequiredListGroupsRequestListGroupsPaginateTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "_OptionalListGroupsRequestListGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGroupsRequestListGroupsPaginateTypeDef(
    _RequiredListGroupsRequestListGroupsPaginateTypeDef,
    _OptionalListGroupsRequestListGroupsPaginateTypeDef,
):
    pass


_RequiredListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef = TypedDict(
    "_RequiredListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef",
    {
        "OrganizationId": str,
        "EntityId": str,
    },
)
_OptionalListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef = TypedDict(
    "_OptionalListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef(
    _RequiredListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef,
    _OptionalListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef,
):
    pass


ListOrganizationsRequestListOrganizationsPaginateTypeDef = TypedDict(
    "ListOrganizationsRequestListOrganizationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef = TypedDict(
    "_RequiredListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef",
    {
        "OrganizationId": str,
        "ResourceId": str,
    },
)
_OptionalListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef = TypedDict(
    "_OptionalListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef(
    _RequiredListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef,
    _OptionalListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef,
):
    pass


_RequiredListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "_RequiredListResourcesRequestListResourcesPaginateTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "_OptionalListResourcesRequestListResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListResourcesRequestListResourcesPaginateTypeDef(
    _RequiredListResourcesRequestListResourcesPaginateTypeDef,
    _OptionalListResourcesRequestListResourcesPaginateTypeDef,
):
    pass


_RequiredListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_RequiredListUsersRequestListUsersPaginateTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_OptionalListUsersRequestListUsersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUsersRequestListUsersPaginateTypeDef(
    _RequiredListUsersRequestListUsersPaginateTypeDef,
    _OptionalListUsersRequestListUsersPaginateTypeDef,
):
    pass


ListGroupMembersResponseTypeDef = TypedDict(
    "ListGroupMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMailDomainsResponseTypeDef = TypedDict(
    "ListMailDomainsResponseTypeDef",
    {
        "MailDomains": List[MailDomainSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMailboxExportJobsResponseTypeDef = TypedDict(
    "ListMailboxExportJobsResponseTypeDef",
    {
        "Jobs": List[MailboxExportJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMailboxPermissionsResponseTypeDef = TypedDict(
    "ListMailboxPermissionsResponseTypeDef",
    {
        "Permissions": List[PermissionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMobileDeviceAccessOverridesResponseTypeDef = TypedDict(
    "ListMobileDeviceAccessOverridesResponseTypeDef",
    {
        "Overrides": List[MobileDeviceAccessOverrideTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMobileDeviceAccessRulesResponseTypeDef = TypedDict(
    "ListMobileDeviceAccessRulesResponseTypeDef",
    {
        "Rules": List[MobileDeviceAccessRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOrganizationsResponseTypeDef = TypedDict(
    "ListOrganizationsResponseTypeDef",
    {
        "OrganizationSummaries": List[OrganizationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesResponseTypeDef = TypedDict(
    "ListResourcesResponseTypeDef",
    {
        "Resources": List[ResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "Users": List[UserTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
