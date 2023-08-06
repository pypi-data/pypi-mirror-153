"""
Type annotations for eks service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/type_defs/)

Usage::

    ```python
    from mypy_boto3_eks.type_defs import AddonIssueTypeDef

    data: AddonIssueTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AddonIssueCodeType,
    AddonStatusType,
    AMITypesType,
    CapacityTypesType,
    ClusterStatusType,
    ConnectorConfigProviderType,
    ErrorCodeType,
    FargateProfileStatusType,
    IpFamilyType,
    LogTypeType,
    NodegroupIssueCodeType,
    NodegroupStatusType,
    ResolveConflictsType,
    TaintEffectType,
    UpdateParamTypeType,
    UpdateStatusType,
    UpdateTypeType,
    configStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AddonIssueTypeDef",
    "CompatibilityTypeDef",
    "ResponseMetadataTypeDef",
    "OidcIdentityProviderConfigRequestTypeDef",
    "AutoScalingGroupTypeDef",
    "CertificateTypeDef",
    "ConnectorConfigResponseTypeDef",
    "KubernetesNetworkConfigResponseTypeDef",
    "VpcConfigResponseTypeDef",
    "ConnectorConfigRequestTypeDef",
    "CreateAddonRequestRequestTypeDef",
    "KubernetesNetworkConfigRequestTypeDef",
    "VpcConfigRequestTypeDef",
    "FargateProfileSelectorTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "NodegroupScalingConfigTypeDef",
    "NodegroupUpdateConfigTypeDef",
    "RemoteAccessConfigTypeDef",
    "TaintTypeDef",
    "DeleteAddonRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteFargateProfileRequestRequestTypeDef",
    "DeleteNodegroupRequestRequestTypeDef",
    "DeregisterClusterRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAddonRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAddonVersionsRequestRequestTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeFargateProfileRequestRequestTypeDef",
    "IdentityProviderConfigTypeDef",
    "DescribeNodegroupRequestRequestTypeDef",
    "DescribeUpdateRequestRequestTypeDef",
    "ProviderTypeDef",
    "ErrorDetailTypeDef",
    "OidcIdentityProviderConfigTypeDef",
    "OIDCTypeDef",
    "IssueTypeDef",
    "ListAddonsRequestRequestTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListFargateProfilesRequestRequestTypeDef",
    "ListIdentityProviderConfigsRequestRequestTypeDef",
    "ListNodegroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListUpdatesRequestRequestTypeDef",
    "LogSetupTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAddonRequestRequestTypeDef",
    "UpdateClusterVersionRequestRequestTypeDef",
    "UpdateLabelsPayloadTypeDef",
    "UpdateParamTypeDef",
    "AddonHealthTypeDef",
    "AddonVersionInfoTypeDef",
    "ListAddonsResponseTypeDef",
    "ListClustersResponseTypeDef",
    "ListFargateProfilesResponseTypeDef",
    "ListNodegroupsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUpdatesResponseTypeDef",
    "AssociateIdentityProviderConfigRequestRequestTypeDef",
    "NodegroupResourcesTypeDef",
    "RegisterClusterRequestRequestTypeDef",
    "CreateFargateProfileRequestRequestTypeDef",
    "FargateProfileTypeDef",
    "UpdateNodegroupVersionRequestRequestTypeDef",
    "CreateNodegroupRequestRequestTypeDef",
    "UpdateTaintsPayloadTypeDef",
    "DescribeAddonRequestAddonActiveWaitTypeDef",
    "DescribeAddonRequestAddonDeletedWaitTypeDef",
    "DescribeClusterRequestClusterActiveWaitTypeDef",
    "DescribeClusterRequestClusterDeletedWaitTypeDef",
    "DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef",
    "DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef",
    "DescribeNodegroupRequestNodegroupActiveWaitTypeDef",
    "DescribeNodegroupRequestNodegroupDeletedWaitTypeDef",
    "DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef",
    "ListAddonsRequestListAddonsPaginateTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListFargateProfilesRequestListFargateProfilesPaginateTypeDef",
    "ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef",
    "ListNodegroupsRequestListNodegroupsPaginateTypeDef",
    "ListUpdatesRequestListUpdatesPaginateTypeDef",
    "DescribeIdentityProviderConfigRequestRequestTypeDef",
    "DisassociateIdentityProviderConfigRequestRequestTypeDef",
    "ListIdentityProviderConfigsResponseTypeDef",
    "EncryptionConfigTypeDef",
    "IdentityProviderConfigResponseTypeDef",
    "IdentityTypeDef",
    "NodegroupHealthTypeDef",
    "LoggingTypeDef",
    "UpdateTypeDef",
    "AddonTypeDef",
    "AddonInfoTypeDef",
    "CreateFargateProfileResponseTypeDef",
    "DeleteFargateProfileResponseTypeDef",
    "DescribeFargateProfileResponseTypeDef",
    "UpdateNodegroupConfigRequestRequestTypeDef",
    "AssociateEncryptionConfigRequestRequestTypeDef",
    "DescribeIdentityProviderConfigResponseTypeDef",
    "NodegroupTypeDef",
    "ClusterTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "UpdateClusterConfigRequestRequestTypeDef",
    "AssociateEncryptionConfigResponseTypeDef",
    "AssociateIdentityProviderConfigResponseTypeDef",
    "DescribeUpdateResponseTypeDef",
    "DisassociateIdentityProviderConfigResponseTypeDef",
    "UpdateAddonResponseTypeDef",
    "UpdateClusterConfigResponseTypeDef",
    "UpdateClusterVersionResponseTypeDef",
    "UpdateNodegroupConfigResponseTypeDef",
    "UpdateNodegroupVersionResponseTypeDef",
    "CreateAddonResponseTypeDef",
    "DeleteAddonResponseTypeDef",
    "DescribeAddonResponseTypeDef",
    "DescribeAddonVersionsResponseTypeDef",
    "CreateNodegroupResponseTypeDef",
    "DeleteNodegroupResponseTypeDef",
    "DescribeNodegroupResponseTypeDef",
    "CreateClusterResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeregisterClusterResponseTypeDef",
    "DescribeClusterResponseTypeDef",
    "RegisterClusterResponseTypeDef",
)

AddonIssueTypeDef = TypedDict(
    "AddonIssueTypeDef",
    {
        "code": AddonIssueCodeType,
        "message": str,
        "resourceIds": List[str],
    },
    total=False,
)

CompatibilityTypeDef = TypedDict(
    "CompatibilityTypeDef",
    {
        "clusterVersion": str,
        "platformVersions": List[str],
        "defaultVersion": bool,
    },
    total=False,
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

_RequiredOidcIdentityProviderConfigRequestTypeDef = TypedDict(
    "_RequiredOidcIdentityProviderConfigRequestTypeDef",
    {
        "identityProviderConfigName": str,
        "issuerUrl": str,
        "clientId": str,
    },
)
_OptionalOidcIdentityProviderConfigRequestTypeDef = TypedDict(
    "_OptionalOidcIdentityProviderConfigRequestTypeDef",
    {
        "usernameClaim": str,
        "usernamePrefix": str,
        "groupsClaim": str,
        "groupsPrefix": str,
        "requiredClaims": Mapping[str, str],
    },
    total=False,
)


class OidcIdentityProviderConfigRequestTypeDef(
    _RequiredOidcIdentityProviderConfigRequestTypeDef,
    _OptionalOidcIdentityProviderConfigRequestTypeDef,
):
    pass


AutoScalingGroupTypeDef = TypedDict(
    "AutoScalingGroupTypeDef",
    {
        "name": str,
    },
    total=False,
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "data": str,
    },
    total=False,
)

ConnectorConfigResponseTypeDef = TypedDict(
    "ConnectorConfigResponseTypeDef",
    {
        "activationId": str,
        "activationCode": str,
        "activationExpiry": datetime,
        "provider": str,
        "roleArn": str,
    },
    total=False,
)

KubernetesNetworkConfigResponseTypeDef = TypedDict(
    "KubernetesNetworkConfigResponseTypeDef",
    {
        "serviceIpv4Cidr": str,
        "serviceIpv6Cidr": str,
        "ipFamily": IpFamilyType,
    },
    total=False,
)

VpcConfigResponseTypeDef = TypedDict(
    "VpcConfigResponseTypeDef",
    {
        "subnetIds": List[str],
        "securityGroupIds": List[str],
        "clusterSecurityGroupId": str,
        "vpcId": str,
        "endpointPublicAccess": bool,
        "endpointPrivateAccess": bool,
        "publicAccessCidrs": List[str],
    },
    total=False,
)

ConnectorConfigRequestTypeDef = TypedDict(
    "ConnectorConfigRequestTypeDef",
    {
        "roleArn": str,
        "provider": ConnectorConfigProviderType,
    },
)

_RequiredCreateAddonRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
    },
)
_OptionalCreateAddonRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAddonRequestRequestTypeDef",
    {
        "addonVersion": str,
        "serviceAccountRoleArn": str,
        "resolveConflicts": ResolveConflictsType,
        "clientRequestToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAddonRequestRequestTypeDef(
    _RequiredCreateAddonRequestRequestTypeDef, _OptionalCreateAddonRequestRequestTypeDef
):
    pass


KubernetesNetworkConfigRequestTypeDef = TypedDict(
    "KubernetesNetworkConfigRequestTypeDef",
    {
        "serviceIpv4Cidr": str,
        "ipFamily": IpFamilyType,
    },
    total=False,
)

VpcConfigRequestTypeDef = TypedDict(
    "VpcConfigRequestTypeDef",
    {
        "subnetIds": Sequence[str],
        "securityGroupIds": Sequence[str],
        "endpointPublicAccess": bool,
        "endpointPrivateAccess": bool,
        "publicAccessCidrs": Sequence[str],
    },
    total=False,
)

FargateProfileSelectorTypeDef = TypedDict(
    "FargateProfileSelectorTypeDef",
    {
        "namespace": str,
        "labels": Mapping[str, str],
    },
    total=False,
)

LaunchTemplateSpecificationTypeDef = TypedDict(
    "LaunchTemplateSpecificationTypeDef",
    {
        "name": str,
        "version": str,
        "id": str,
    },
    total=False,
)

NodegroupScalingConfigTypeDef = TypedDict(
    "NodegroupScalingConfigTypeDef",
    {
        "minSize": int,
        "maxSize": int,
        "desiredSize": int,
    },
    total=False,
)

NodegroupUpdateConfigTypeDef = TypedDict(
    "NodegroupUpdateConfigTypeDef",
    {
        "maxUnavailable": int,
        "maxUnavailablePercentage": int,
    },
    total=False,
)

RemoteAccessConfigTypeDef = TypedDict(
    "RemoteAccessConfigTypeDef",
    {
        "ec2SshKey": str,
        "sourceSecurityGroups": Sequence[str],
    },
    total=False,
)

TaintTypeDef = TypedDict(
    "TaintTypeDef",
    {
        "key": str,
        "value": str,
        "effect": TaintEffectType,
    },
    total=False,
)

_RequiredDeleteAddonRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
    },
)
_OptionalDeleteAddonRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAddonRequestRequestTypeDef",
    {
        "preserve": bool,
    },
    total=False,
)


class DeleteAddonRequestRequestTypeDef(
    _RequiredDeleteAddonRequestRequestTypeDef, _OptionalDeleteAddonRequestRequestTypeDef
):
    pass


DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "name": str,
    },
)

DeleteFargateProfileRequestRequestTypeDef = TypedDict(
    "DeleteFargateProfileRequestRequestTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
    },
)

DeleteNodegroupRequestRequestTypeDef = TypedDict(
    "DeleteNodegroupRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)

DeregisterClusterRequestRequestTypeDef = TypedDict(
    "DeregisterClusterRequestRequestTypeDef",
    {
        "name": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeAddonRequestRequestTypeDef = TypedDict(
    "DescribeAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
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

DescribeAddonVersionsRequestRequestTypeDef = TypedDict(
    "DescribeAddonVersionsRequestRequestTypeDef",
    {
        "kubernetesVersion": str,
        "maxResults": int,
        "nextToken": str,
        "addonName": str,
    },
    total=False,
)

DescribeClusterRequestRequestTypeDef = TypedDict(
    "DescribeClusterRequestRequestTypeDef",
    {
        "name": str,
    },
)

DescribeFargateProfileRequestRequestTypeDef = TypedDict(
    "DescribeFargateProfileRequestRequestTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
    },
)

IdentityProviderConfigTypeDef = TypedDict(
    "IdentityProviderConfigTypeDef",
    {
        "type": str,
        "name": str,
    },
)

DescribeNodegroupRequestRequestTypeDef = TypedDict(
    "DescribeNodegroupRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)

_RequiredDescribeUpdateRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeUpdateRequestRequestTypeDef",
    {
        "name": str,
        "updateId": str,
    },
)
_OptionalDescribeUpdateRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeUpdateRequestRequestTypeDef",
    {
        "nodegroupName": str,
        "addonName": str,
    },
    total=False,
)


class DescribeUpdateRequestRequestTypeDef(
    _RequiredDescribeUpdateRequestRequestTypeDef, _OptionalDescribeUpdateRequestRequestTypeDef
):
    pass


ProviderTypeDef = TypedDict(
    "ProviderTypeDef",
    {
        "keyArn": str,
    },
    total=False,
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "errorCode": ErrorCodeType,
        "errorMessage": str,
        "resourceIds": List[str],
    },
    total=False,
)

OidcIdentityProviderConfigTypeDef = TypedDict(
    "OidcIdentityProviderConfigTypeDef",
    {
        "identityProviderConfigName": str,
        "identityProviderConfigArn": str,
        "clusterName": str,
        "issuerUrl": str,
        "clientId": str,
        "usernameClaim": str,
        "usernamePrefix": str,
        "groupsClaim": str,
        "groupsPrefix": str,
        "requiredClaims": Dict[str, str],
        "tags": Dict[str, str],
        "status": configStatusType,
    },
    total=False,
)

OIDCTypeDef = TypedDict(
    "OIDCTypeDef",
    {
        "issuer": str,
    },
    total=False,
)

IssueTypeDef = TypedDict(
    "IssueTypeDef",
    {
        "code": NodegroupIssueCodeType,
        "message": str,
        "resourceIds": List[str],
    },
    total=False,
)

_RequiredListAddonsRequestRequestTypeDef = TypedDict(
    "_RequiredListAddonsRequestRequestTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListAddonsRequestRequestTypeDef = TypedDict(
    "_OptionalListAddonsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAddonsRequestRequestTypeDef(
    _RequiredListAddonsRequestRequestTypeDef, _OptionalListAddonsRequestRequestTypeDef
):
    pass


ListClustersRequestRequestTypeDef = TypedDict(
    "ListClustersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "include": Sequence[str],
    },
    total=False,
)

_RequiredListFargateProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredListFargateProfilesRequestRequestTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListFargateProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalListFargateProfilesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListFargateProfilesRequestRequestTypeDef(
    _RequiredListFargateProfilesRequestRequestTypeDef,
    _OptionalListFargateProfilesRequestRequestTypeDef,
):
    pass


_RequiredListIdentityProviderConfigsRequestRequestTypeDef = TypedDict(
    "_RequiredListIdentityProviderConfigsRequestRequestTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListIdentityProviderConfigsRequestRequestTypeDef = TypedDict(
    "_OptionalListIdentityProviderConfigsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListIdentityProviderConfigsRequestRequestTypeDef(
    _RequiredListIdentityProviderConfigsRequestRequestTypeDef,
    _OptionalListIdentityProviderConfigsRequestRequestTypeDef,
):
    pass


_RequiredListNodegroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListNodegroupsRequestRequestTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListNodegroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListNodegroupsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListNodegroupsRequestRequestTypeDef(
    _RequiredListNodegroupsRequestRequestTypeDef, _OptionalListNodegroupsRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredListUpdatesRequestRequestTypeDef = TypedDict(
    "_RequiredListUpdatesRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalListUpdatesRequestRequestTypeDef = TypedDict(
    "_OptionalListUpdatesRequestRequestTypeDef",
    {
        "nodegroupName": str,
        "addonName": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListUpdatesRequestRequestTypeDef(
    _RequiredListUpdatesRequestRequestTypeDef, _OptionalListUpdatesRequestRequestTypeDef
):
    pass


LogSetupTypeDef = TypedDict(
    "LogSetupTypeDef",
    {
        "types": Sequence[LogTypeType],
        "enabled": bool,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAddonRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
    },
)
_OptionalUpdateAddonRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAddonRequestRequestTypeDef",
    {
        "addonVersion": str,
        "serviceAccountRoleArn": str,
        "resolveConflicts": ResolveConflictsType,
        "clientRequestToken": str,
    },
    total=False,
)


class UpdateAddonRequestRequestTypeDef(
    _RequiredUpdateAddonRequestRequestTypeDef, _OptionalUpdateAddonRequestRequestTypeDef
):
    pass


_RequiredUpdateClusterVersionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateClusterVersionRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
    },
)
_OptionalUpdateClusterVersionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateClusterVersionRequestRequestTypeDef",
    {
        "clientRequestToken": str,
    },
    total=False,
)


class UpdateClusterVersionRequestRequestTypeDef(
    _RequiredUpdateClusterVersionRequestRequestTypeDef,
    _OptionalUpdateClusterVersionRequestRequestTypeDef,
):
    pass


UpdateLabelsPayloadTypeDef = TypedDict(
    "UpdateLabelsPayloadTypeDef",
    {
        "addOrUpdateLabels": Mapping[str, str],
        "removeLabels": Sequence[str],
    },
    total=False,
)

UpdateParamTypeDef = TypedDict(
    "UpdateParamTypeDef",
    {
        "type": UpdateParamTypeType,
        "value": str,
    },
    total=False,
)

AddonHealthTypeDef = TypedDict(
    "AddonHealthTypeDef",
    {
        "issues": List[AddonIssueTypeDef],
    },
    total=False,
)

AddonVersionInfoTypeDef = TypedDict(
    "AddonVersionInfoTypeDef",
    {
        "addonVersion": str,
        "architecture": List[str],
        "compatibilities": List[CompatibilityTypeDef],
    },
    total=False,
)

ListAddonsResponseTypeDef = TypedDict(
    "ListAddonsResponseTypeDef",
    {
        "addons": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersResponseTypeDef = TypedDict(
    "ListClustersResponseTypeDef",
    {
        "clusters": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFargateProfilesResponseTypeDef = TypedDict(
    "ListFargateProfilesResponseTypeDef",
    {
        "fargateProfileNames": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNodegroupsResponseTypeDef = TypedDict(
    "ListNodegroupsResponseTypeDef",
    {
        "nodegroups": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUpdatesResponseTypeDef = TypedDict(
    "ListUpdatesResponseTypeDef",
    {
        "updateIds": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssociateIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateIdentityProviderConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "oidc": OidcIdentityProviderConfigRequestTypeDef,
    },
)
_OptionalAssociateIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateIdentityProviderConfigRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
        "clientRequestToken": str,
    },
    total=False,
)


class AssociateIdentityProviderConfigRequestRequestTypeDef(
    _RequiredAssociateIdentityProviderConfigRequestRequestTypeDef,
    _OptionalAssociateIdentityProviderConfigRequestRequestTypeDef,
):
    pass


NodegroupResourcesTypeDef = TypedDict(
    "NodegroupResourcesTypeDef",
    {
        "autoScalingGroups": List[AutoScalingGroupTypeDef],
        "remoteAccessSecurityGroup": str,
    },
    total=False,
)

_RequiredRegisterClusterRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterClusterRequestRequestTypeDef",
    {
        "name": str,
        "connectorConfig": ConnectorConfigRequestTypeDef,
    },
)
_OptionalRegisterClusterRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterClusterRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class RegisterClusterRequestRequestTypeDef(
    _RequiredRegisterClusterRequestRequestTypeDef, _OptionalRegisterClusterRequestRequestTypeDef
):
    pass


_RequiredCreateFargateProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFargateProfileRequestRequestTypeDef",
    {
        "fargateProfileName": str,
        "clusterName": str,
        "podExecutionRoleArn": str,
    },
)
_OptionalCreateFargateProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFargateProfileRequestRequestTypeDef",
    {
        "subnets": Sequence[str],
        "selectors": Sequence[FargateProfileSelectorTypeDef],
        "clientRequestToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateFargateProfileRequestRequestTypeDef(
    _RequiredCreateFargateProfileRequestRequestTypeDef,
    _OptionalCreateFargateProfileRequestRequestTypeDef,
):
    pass


FargateProfileTypeDef = TypedDict(
    "FargateProfileTypeDef",
    {
        "fargateProfileName": str,
        "fargateProfileArn": str,
        "clusterName": str,
        "createdAt": datetime,
        "podExecutionRoleArn": str,
        "subnets": List[str],
        "selectors": List[FargateProfileSelectorTypeDef],
        "status": FargateProfileStatusType,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredUpdateNodegroupVersionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNodegroupVersionRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)
_OptionalUpdateNodegroupVersionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNodegroupVersionRequestRequestTypeDef",
    {
        "version": str,
        "releaseVersion": str,
        "launchTemplate": LaunchTemplateSpecificationTypeDef,
        "force": bool,
        "clientRequestToken": str,
    },
    total=False,
)


class UpdateNodegroupVersionRequestRequestTypeDef(
    _RequiredUpdateNodegroupVersionRequestRequestTypeDef,
    _OptionalUpdateNodegroupVersionRequestRequestTypeDef,
):
    pass


_RequiredCreateNodegroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNodegroupRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
        "subnets": Sequence[str],
        "nodeRole": str,
    },
)
_OptionalCreateNodegroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNodegroupRequestRequestTypeDef",
    {
        "scalingConfig": NodegroupScalingConfigTypeDef,
        "diskSize": int,
        "instanceTypes": Sequence[str],
        "amiType": AMITypesType,
        "remoteAccess": RemoteAccessConfigTypeDef,
        "labels": Mapping[str, str],
        "taints": Sequence[TaintTypeDef],
        "tags": Mapping[str, str],
        "clientRequestToken": str,
        "launchTemplate": LaunchTemplateSpecificationTypeDef,
        "updateConfig": NodegroupUpdateConfigTypeDef,
        "capacityType": CapacityTypesType,
        "version": str,
        "releaseVersion": str,
    },
    total=False,
)


class CreateNodegroupRequestRequestTypeDef(
    _RequiredCreateNodegroupRequestRequestTypeDef, _OptionalCreateNodegroupRequestRequestTypeDef
):
    pass


UpdateTaintsPayloadTypeDef = TypedDict(
    "UpdateTaintsPayloadTypeDef",
    {
        "addOrUpdateTaints": Sequence[TaintTypeDef],
        "removeTaints": Sequence[TaintTypeDef],
    },
    total=False,
)

_RequiredDescribeAddonRequestAddonActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeAddonRequestAddonActiveWaitTypeDef",
    {
        "clusterName": str,
        "addonName": str,
    },
)
_OptionalDescribeAddonRequestAddonActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeAddonRequestAddonActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeAddonRequestAddonActiveWaitTypeDef(
    _RequiredDescribeAddonRequestAddonActiveWaitTypeDef,
    _OptionalDescribeAddonRequestAddonActiveWaitTypeDef,
):
    pass


_RequiredDescribeAddonRequestAddonDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeAddonRequestAddonDeletedWaitTypeDef",
    {
        "clusterName": str,
        "addonName": str,
    },
)
_OptionalDescribeAddonRequestAddonDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeAddonRequestAddonDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeAddonRequestAddonDeletedWaitTypeDef(
    _RequiredDescribeAddonRequestAddonDeletedWaitTypeDef,
    _OptionalDescribeAddonRequestAddonDeletedWaitTypeDef,
):
    pass


_RequiredDescribeClusterRequestClusterActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeClusterRequestClusterActiveWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalDescribeClusterRequestClusterActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeClusterRequestClusterActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeClusterRequestClusterActiveWaitTypeDef(
    _RequiredDescribeClusterRequestClusterActiveWaitTypeDef,
    _OptionalDescribeClusterRequestClusterActiveWaitTypeDef,
):
    pass


_RequiredDescribeClusterRequestClusterDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeClusterRequestClusterDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalDescribeClusterRequestClusterDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeClusterRequestClusterDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeClusterRequestClusterDeletedWaitTypeDef(
    _RequiredDescribeClusterRequestClusterDeletedWaitTypeDef,
    _OptionalDescribeClusterRequestClusterDeletedWaitTypeDef,
):
    pass


_RequiredDescribeFargateProfileRequestFargateProfileActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeFargateProfileRequestFargateProfileActiveWaitTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
    },
)
_OptionalDescribeFargateProfileRequestFargateProfileActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeFargateProfileRequestFargateProfileActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef(
    _RequiredDescribeFargateProfileRequestFargateProfileActiveWaitTypeDef,
    _OptionalDescribeFargateProfileRequestFargateProfileActiveWaitTypeDef,
):
    pass


_RequiredDescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
    },
)
_OptionalDescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef(
    _RequiredDescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef,
    _OptionalDescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef,
):
    pass


_RequiredDescribeNodegroupRequestNodegroupActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeNodegroupRequestNodegroupActiveWaitTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)
_OptionalDescribeNodegroupRequestNodegroupActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeNodegroupRequestNodegroupActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeNodegroupRequestNodegroupActiveWaitTypeDef(
    _RequiredDescribeNodegroupRequestNodegroupActiveWaitTypeDef,
    _OptionalDescribeNodegroupRequestNodegroupActiveWaitTypeDef,
):
    pass


_RequiredDescribeNodegroupRequestNodegroupDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeNodegroupRequestNodegroupDeletedWaitTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)
_OptionalDescribeNodegroupRequestNodegroupDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeNodegroupRequestNodegroupDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeNodegroupRequestNodegroupDeletedWaitTypeDef(
    _RequiredDescribeNodegroupRequestNodegroupDeletedWaitTypeDef,
    _OptionalDescribeNodegroupRequestNodegroupDeletedWaitTypeDef,
):
    pass


DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef = TypedDict(
    "DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef",
    {
        "kubernetesVersion": str,
        "addonName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAddonsRequestListAddonsPaginateTypeDef = TypedDict(
    "_RequiredListAddonsRequestListAddonsPaginateTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListAddonsRequestListAddonsPaginateTypeDef = TypedDict(
    "_OptionalListAddonsRequestListAddonsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAddonsRequestListAddonsPaginateTypeDef(
    _RequiredListAddonsRequestListAddonsPaginateTypeDef,
    _OptionalListAddonsRequestListAddonsPaginateTypeDef,
):
    pass


ListClustersRequestListClustersPaginateTypeDef = TypedDict(
    "ListClustersRequestListClustersPaginateTypeDef",
    {
        "include": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListFargateProfilesRequestListFargateProfilesPaginateTypeDef = TypedDict(
    "_RequiredListFargateProfilesRequestListFargateProfilesPaginateTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListFargateProfilesRequestListFargateProfilesPaginateTypeDef = TypedDict(
    "_OptionalListFargateProfilesRequestListFargateProfilesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFargateProfilesRequestListFargateProfilesPaginateTypeDef(
    _RequiredListFargateProfilesRequestListFargateProfilesPaginateTypeDef,
    _OptionalListFargateProfilesRequestListFargateProfilesPaginateTypeDef,
):
    pass


_RequiredListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef = TypedDict(
    "_RequiredListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef = TypedDict(
    "_OptionalListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef(
    _RequiredListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef,
    _OptionalListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef,
):
    pass


_RequiredListNodegroupsRequestListNodegroupsPaginateTypeDef = TypedDict(
    "_RequiredListNodegroupsRequestListNodegroupsPaginateTypeDef",
    {
        "clusterName": str,
    },
)
_OptionalListNodegroupsRequestListNodegroupsPaginateTypeDef = TypedDict(
    "_OptionalListNodegroupsRequestListNodegroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListNodegroupsRequestListNodegroupsPaginateTypeDef(
    _RequiredListNodegroupsRequestListNodegroupsPaginateTypeDef,
    _OptionalListNodegroupsRequestListNodegroupsPaginateTypeDef,
):
    pass


_RequiredListUpdatesRequestListUpdatesPaginateTypeDef = TypedDict(
    "_RequiredListUpdatesRequestListUpdatesPaginateTypeDef",
    {
        "name": str,
    },
)
_OptionalListUpdatesRequestListUpdatesPaginateTypeDef = TypedDict(
    "_OptionalListUpdatesRequestListUpdatesPaginateTypeDef",
    {
        "nodegroupName": str,
        "addonName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUpdatesRequestListUpdatesPaginateTypeDef(
    _RequiredListUpdatesRequestListUpdatesPaginateTypeDef,
    _OptionalListUpdatesRequestListUpdatesPaginateTypeDef,
):
    pass


DescribeIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "DescribeIdentityProviderConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "identityProviderConfig": IdentityProviderConfigTypeDef,
    },
)

_RequiredDisassociateIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateIdentityProviderConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "identityProviderConfig": IdentityProviderConfigTypeDef,
    },
)
_OptionalDisassociateIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateIdentityProviderConfigRequestRequestTypeDef",
    {
        "clientRequestToken": str,
    },
    total=False,
)


class DisassociateIdentityProviderConfigRequestRequestTypeDef(
    _RequiredDisassociateIdentityProviderConfigRequestRequestTypeDef,
    _OptionalDisassociateIdentityProviderConfigRequestRequestTypeDef,
):
    pass


ListIdentityProviderConfigsResponseTypeDef = TypedDict(
    "ListIdentityProviderConfigsResponseTypeDef",
    {
        "identityProviderConfigs": List[IdentityProviderConfigTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "resources": Sequence[str],
        "provider": ProviderTypeDef,
    },
    total=False,
)

IdentityProviderConfigResponseTypeDef = TypedDict(
    "IdentityProviderConfigResponseTypeDef",
    {
        "oidc": OidcIdentityProviderConfigTypeDef,
    },
    total=False,
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "oidc": OIDCTypeDef,
    },
    total=False,
)

NodegroupHealthTypeDef = TypedDict(
    "NodegroupHealthTypeDef",
    {
        "issues": List[IssueTypeDef],
    },
    total=False,
)

LoggingTypeDef = TypedDict(
    "LoggingTypeDef",
    {
        "clusterLogging": Sequence[LogSetupTypeDef],
    },
    total=False,
)

UpdateTypeDef = TypedDict(
    "UpdateTypeDef",
    {
        "id": str,
        "status": UpdateStatusType,
        "type": UpdateTypeType,
        "params": List[UpdateParamTypeDef],
        "createdAt": datetime,
        "errors": List[ErrorDetailTypeDef],
    },
    total=False,
)

AddonTypeDef = TypedDict(
    "AddonTypeDef",
    {
        "addonName": str,
        "clusterName": str,
        "status": AddonStatusType,
        "addonVersion": str,
        "health": AddonHealthTypeDef,
        "addonArn": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "serviceAccountRoleArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

AddonInfoTypeDef = TypedDict(
    "AddonInfoTypeDef",
    {
        "addonName": str,
        "type": str,
        "addonVersions": List[AddonVersionInfoTypeDef],
    },
    total=False,
)

CreateFargateProfileResponseTypeDef = TypedDict(
    "CreateFargateProfileResponseTypeDef",
    {
        "fargateProfile": FargateProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFargateProfileResponseTypeDef = TypedDict(
    "DeleteFargateProfileResponseTypeDef",
    {
        "fargateProfile": FargateProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFargateProfileResponseTypeDef = TypedDict(
    "DescribeFargateProfileResponseTypeDef",
    {
        "fargateProfile": FargateProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateNodegroupConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNodegroupConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)
_OptionalUpdateNodegroupConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNodegroupConfigRequestRequestTypeDef",
    {
        "labels": UpdateLabelsPayloadTypeDef,
        "taints": UpdateTaintsPayloadTypeDef,
        "scalingConfig": NodegroupScalingConfigTypeDef,
        "updateConfig": NodegroupUpdateConfigTypeDef,
        "clientRequestToken": str,
    },
    total=False,
)


class UpdateNodegroupConfigRequestRequestTypeDef(
    _RequiredUpdateNodegroupConfigRequestRequestTypeDef,
    _OptionalUpdateNodegroupConfigRequestRequestTypeDef,
):
    pass


_RequiredAssociateEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateEncryptionConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "encryptionConfig": Sequence[EncryptionConfigTypeDef],
    },
)
_OptionalAssociateEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateEncryptionConfigRequestRequestTypeDef",
    {
        "clientRequestToken": str,
    },
    total=False,
)


class AssociateEncryptionConfigRequestRequestTypeDef(
    _RequiredAssociateEncryptionConfigRequestRequestTypeDef,
    _OptionalAssociateEncryptionConfigRequestRequestTypeDef,
):
    pass


DescribeIdentityProviderConfigResponseTypeDef = TypedDict(
    "DescribeIdentityProviderConfigResponseTypeDef",
    {
        "identityProviderConfig": IdentityProviderConfigResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NodegroupTypeDef = TypedDict(
    "NodegroupTypeDef",
    {
        "nodegroupName": str,
        "nodegroupArn": str,
        "clusterName": str,
        "version": str,
        "releaseVersion": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": NodegroupStatusType,
        "capacityType": CapacityTypesType,
        "scalingConfig": NodegroupScalingConfigTypeDef,
        "instanceTypes": List[str],
        "subnets": List[str],
        "remoteAccess": RemoteAccessConfigTypeDef,
        "amiType": AMITypesType,
        "nodeRole": str,
        "labels": Dict[str, str],
        "taints": List[TaintTypeDef],
        "resources": NodegroupResourcesTypeDef,
        "diskSize": int,
        "health": NodegroupHealthTypeDef,
        "updateConfig": NodegroupUpdateConfigTypeDef,
        "launchTemplate": LaunchTemplateSpecificationTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "name": str,
        "arn": str,
        "createdAt": datetime,
        "version": str,
        "endpoint": str,
        "roleArn": str,
        "resourcesVpcConfig": VpcConfigResponseTypeDef,
        "kubernetesNetworkConfig": KubernetesNetworkConfigResponseTypeDef,
        "logging": LoggingTypeDef,
        "identity": IdentityTypeDef,
        "status": ClusterStatusType,
        "certificateAuthority": CertificateTypeDef,
        "clientRequestToken": str,
        "platformVersion": str,
        "tags": Dict[str, str],
        "encryptionConfig": List[EncryptionConfigTypeDef],
        "connectorConfig": ConnectorConfigResponseTypeDef,
    },
    total=False,
)

_RequiredCreateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateClusterRequestRequestTypeDef",
    {
        "name": str,
        "roleArn": str,
        "resourcesVpcConfig": VpcConfigRequestTypeDef,
    },
)
_OptionalCreateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateClusterRequestRequestTypeDef",
    {
        "version": str,
        "kubernetesNetworkConfig": KubernetesNetworkConfigRequestTypeDef,
        "logging": LoggingTypeDef,
        "clientRequestToken": str,
        "tags": Mapping[str, str],
        "encryptionConfig": Sequence[EncryptionConfigTypeDef],
    },
    total=False,
)


class CreateClusterRequestRequestTypeDef(
    _RequiredCreateClusterRequestRequestTypeDef, _OptionalCreateClusterRequestRequestTypeDef
):
    pass


_RequiredUpdateClusterConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateClusterConfigRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateClusterConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateClusterConfigRequestRequestTypeDef",
    {
        "resourcesVpcConfig": VpcConfigRequestTypeDef,
        "logging": LoggingTypeDef,
        "clientRequestToken": str,
    },
    total=False,
)


class UpdateClusterConfigRequestRequestTypeDef(
    _RequiredUpdateClusterConfigRequestRequestTypeDef,
    _OptionalUpdateClusterConfigRequestRequestTypeDef,
):
    pass


AssociateEncryptionConfigResponseTypeDef = TypedDict(
    "AssociateEncryptionConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateIdentityProviderConfigResponseTypeDef = TypedDict(
    "AssociateIdentityProviderConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUpdateResponseTypeDef = TypedDict(
    "DescribeUpdateResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateIdentityProviderConfigResponseTypeDef = TypedDict(
    "DisassociateIdentityProviderConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAddonResponseTypeDef = TypedDict(
    "UpdateAddonResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterConfigResponseTypeDef = TypedDict(
    "UpdateClusterConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterVersionResponseTypeDef = TypedDict(
    "UpdateClusterVersionResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNodegroupConfigResponseTypeDef = TypedDict(
    "UpdateNodegroupConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNodegroupVersionResponseTypeDef = TypedDict(
    "UpdateNodegroupVersionResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAddonResponseTypeDef = TypedDict(
    "CreateAddonResponseTypeDef",
    {
        "addon": AddonTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAddonResponseTypeDef = TypedDict(
    "DeleteAddonResponseTypeDef",
    {
        "addon": AddonTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddonResponseTypeDef = TypedDict(
    "DescribeAddonResponseTypeDef",
    {
        "addon": AddonTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddonVersionsResponseTypeDef = TypedDict(
    "DescribeAddonVersionsResponseTypeDef",
    {
        "addons": List[AddonInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNodegroupResponseTypeDef = TypedDict(
    "CreateNodegroupResponseTypeDef",
    {
        "nodegroup": NodegroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteNodegroupResponseTypeDef = TypedDict(
    "DeleteNodegroupResponseTypeDef",
    {
        "nodegroup": NodegroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeNodegroupResponseTypeDef = TypedDict(
    "DescribeNodegroupResponseTypeDef",
    {
        "nodegroup": NodegroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResponseTypeDef = TypedDict(
    "DeleteClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterClusterResponseTypeDef = TypedDict(
    "DeregisterClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterResponseTypeDef = TypedDict(
    "DescribeClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterClusterResponseTypeDef = TypedDict(
    "RegisterClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
