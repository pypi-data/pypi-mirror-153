"""
Type annotations for workspaces-web service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/type_defs/)

Usage::

    ```python
    from mypy_boto3_workspaces_web.type_defs import AssociateBrowserSettingsRequestRequestTypeDef

    data: AssociateBrowserSettingsRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import EnabledTypeType, IdentityProviderTypeType, PortalStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateBrowserSettingsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateNetworkSettingsRequestRequestTypeDef",
    "AssociateTrustStoreRequestRequestTypeDef",
    "AssociateUserSettingsRequestRequestTypeDef",
    "BrowserSettingsSummaryTypeDef",
    "BrowserSettingsTypeDef",
    "CertificateSummaryTypeDef",
    "CertificateTypeDef",
    "TagTypeDef",
    "CreateIdentityProviderRequestRequestTypeDef",
    "DeleteBrowserSettingsRequestRequestTypeDef",
    "DeleteIdentityProviderRequestRequestTypeDef",
    "DeleteNetworkSettingsRequestRequestTypeDef",
    "DeletePortalRequestRequestTypeDef",
    "DeleteTrustStoreRequestRequestTypeDef",
    "DeleteUserSettingsRequestRequestTypeDef",
    "DisassociateBrowserSettingsRequestRequestTypeDef",
    "DisassociateNetworkSettingsRequestRequestTypeDef",
    "DisassociateTrustStoreRequestRequestTypeDef",
    "DisassociateUserSettingsRequestRequestTypeDef",
    "GetBrowserSettingsRequestRequestTypeDef",
    "GetIdentityProviderRequestRequestTypeDef",
    "IdentityProviderTypeDef",
    "GetNetworkSettingsRequestRequestTypeDef",
    "NetworkSettingsTypeDef",
    "GetPortalRequestRequestTypeDef",
    "PortalTypeDef",
    "GetPortalServiceProviderMetadataRequestRequestTypeDef",
    "GetTrustStoreCertificateRequestRequestTypeDef",
    "GetTrustStoreRequestRequestTypeDef",
    "TrustStoreTypeDef",
    "GetUserSettingsRequestRequestTypeDef",
    "UserSettingsTypeDef",
    "IdentityProviderSummaryTypeDef",
    "ListBrowserSettingsRequestRequestTypeDef",
    "ListIdentityProvidersRequestRequestTypeDef",
    "ListNetworkSettingsRequestRequestTypeDef",
    "NetworkSettingsSummaryTypeDef",
    "ListPortalsRequestRequestTypeDef",
    "PortalSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTrustStoreCertificatesRequestRequestTypeDef",
    "ListTrustStoresRequestRequestTypeDef",
    "TrustStoreSummaryTypeDef",
    "ListUserSettingsRequestRequestTypeDef",
    "UserSettingsSummaryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBrowserSettingsRequestRequestTypeDef",
    "UpdateIdentityProviderRequestRequestTypeDef",
    "UpdateNetworkSettingsRequestRequestTypeDef",
    "UpdatePortalRequestRequestTypeDef",
    "UpdateTrustStoreRequestRequestTypeDef",
    "UpdateUserSettingsRequestRequestTypeDef",
    "AssociateBrowserSettingsResponseTypeDef",
    "AssociateNetworkSettingsResponseTypeDef",
    "AssociateTrustStoreResponseTypeDef",
    "AssociateUserSettingsResponseTypeDef",
    "CreateBrowserSettingsResponseTypeDef",
    "CreateIdentityProviderResponseTypeDef",
    "CreateNetworkSettingsResponseTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateTrustStoreResponseTypeDef",
    "CreateUserSettingsResponseTypeDef",
    "GetPortalServiceProviderMetadataResponseTypeDef",
    "UpdateTrustStoreResponseTypeDef",
    "ListBrowserSettingsResponseTypeDef",
    "GetBrowserSettingsResponseTypeDef",
    "UpdateBrowserSettingsResponseTypeDef",
    "ListTrustStoreCertificatesResponseTypeDef",
    "GetTrustStoreCertificateResponseTypeDef",
    "CreateBrowserSettingsRequestRequestTypeDef",
    "CreateNetworkSettingsRequestRequestTypeDef",
    "CreatePortalRequestRequestTypeDef",
    "CreateTrustStoreRequestRequestTypeDef",
    "CreateUserSettingsRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "GetIdentityProviderResponseTypeDef",
    "UpdateIdentityProviderResponseTypeDef",
    "GetNetworkSettingsResponseTypeDef",
    "UpdateNetworkSettingsResponseTypeDef",
    "GetPortalResponseTypeDef",
    "UpdatePortalResponseTypeDef",
    "GetTrustStoreResponseTypeDef",
    "GetUserSettingsResponseTypeDef",
    "UpdateUserSettingsResponseTypeDef",
    "ListIdentityProvidersResponseTypeDef",
    "ListNetworkSettingsResponseTypeDef",
    "ListPortalsResponseTypeDef",
    "ListTrustStoresResponseTypeDef",
    "ListUserSettingsResponseTypeDef",
)

AssociateBrowserSettingsRequestRequestTypeDef = TypedDict(
    "AssociateBrowserSettingsRequestRequestTypeDef",
    {
        "browserSettingsArn": str,
        "portalArn": str,
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

AssociateNetworkSettingsRequestRequestTypeDef = TypedDict(
    "AssociateNetworkSettingsRequestRequestTypeDef",
    {
        "networkSettingsArn": str,
        "portalArn": str,
    },
)

AssociateTrustStoreRequestRequestTypeDef = TypedDict(
    "AssociateTrustStoreRequestRequestTypeDef",
    {
        "portalArn": str,
        "trustStoreArn": str,
    },
)

AssociateUserSettingsRequestRequestTypeDef = TypedDict(
    "AssociateUserSettingsRequestRequestTypeDef",
    {
        "portalArn": str,
        "userSettingsArn": str,
    },
)

BrowserSettingsSummaryTypeDef = TypedDict(
    "BrowserSettingsSummaryTypeDef",
    {
        "browserSettingsArn": str,
    },
    total=False,
)

_RequiredBrowserSettingsTypeDef = TypedDict(
    "_RequiredBrowserSettingsTypeDef",
    {
        "browserSettingsArn": str,
    },
)
_OptionalBrowserSettingsTypeDef = TypedDict(
    "_OptionalBrowserSettingsTypeDef",
    {
        "associatedPortalArns": List[str],
        "browserPolicy": str,
    },
    total=False,
)


class BrowserSettingsTypeDef(_RequiredBrowserSettingsTypeDef, _OptionalBrowserSettingsTypeDef):
    pass


CertificateSummaryTypeDef = TypedDict(
    "CertificateSummaryTypeDef",
    {
        "issuer": str,
        "notValidAfter": datetime,
        "notValidBefore": datetime,
        "subject": str,
        "thumbprint": str,
    },
    total=False,
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "body": bytes,
        "issuer": str,
        "notValidAfter": datetime,
        "notValidBefore": datetime,
        "subject": str,
        "thumbprint": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredCreateIdentityProviderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIdentityProviderRequestRequestTypeDef",
    {
        "identityProviderDetails": Mapping[str, str],
        "identityProviderName": str,
        "identityProviderType": IdentityProviderTypeType,
        "portalArn": str,
    },
)
_OptionalCreateIdentityProviderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIdentityProviderRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateIdentityProviderRequestRequestTypeDef(
    _RequiredCreateIdentityProviderRequestRequestTypeDef,
    _OptionalCreateIdentityProviderRequestRequestTypeDef,
):
    pass


DeleteBrowserSettingsRequestRequestTypeDef = TypedDict(
    "DeleteBrowserSettingsRequestRequestTypeDef",
    {
        "browserSettingsArn": str,
    },
)

DeleteIdentityProviderRequestRequestTypeDef = TypedDict(
    "DeleteIdentityProviderRequestRequestTypeDef",
    {
        "identityProviderArn": str,
    },
)

DeleteNetworkSettingsRequestRequestTypeDef = TypedDict(
    "DeleteNetworkSettingsRequestRequestTypeDef",
    {
        "networkSettingsArn": str,
    },
)

DeletePortalRequestRequestTypeDef = TypedDict(
    "DeletePortalRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

DeleteTrustStoreRequestRequestTypeDef = TypedDict(
    "DeleteTrustStoreRequestRequestTypeDef",
    {
        "trustStoreArn": str,
    },
)

DeleteUserSettingsRequestRequestTypeDef = TypedDict(
    "DeleteUserSettingsRequestRequestTypeDef",
    {
        "userSettingsArn": str,
    },
)

DisassociateBrowserSettingsRequestRequestTypeDef = TypedDict(
    "DisassociateBrowserSettingsRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

DisassociateNetworkSettingsRequestRequestTypeDef = TypedDict(
    "DisassociateNetworkSettingsRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

DisassociateTrustStoreRequestRequestTypeDef = TypedDict(
    "DisassociateTrustStoreRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

DisassociateUserSettingsRequestRequestTypeDef = TypedDict(
    "DisassociateUserSettingsRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

GetBrowserSettingsRequestRequestTypeDef = TypedDict(
    "GetBrowserSettingsRequestRequestTypeDef",
    {
        "browserSettingsArn": str,
    },
)

GetIdentityProviderRequestRequestTypeDef = TypedDict(
    "GetIdentityProviderRequestRequestTypeDef",
    {
        "identityProviderArn": str,
    },
)

_RequiredIdentityProviderTypeDef = TypedDict(
    "_RequiredIdentityProviderTypeDef",
    {
        "identityProviderArn": str,
    },
)
_OptionalIdentityProviderTypeDef = TypedDict(
    "_OptionalIdentityProviderTypeDef",
    {
        "identityProviderDetails": Dict[str, str],
        "identityProviderName": str,
        "identityProviderType": IdentityProviderTypeType,
    },
    total=False,
)


class IdentityProviderTypeDef(_RequiredIdentityProviderTypeDef, _OptionalIdentityProviderTypeDef):
    pass


GetNetworkSettingsRequestRequestTypeDef = TypedDict(
    "GetNetworkSettingsRequestRequestTypeDef",
    {
        "networkSettingsArn": str,
    },
)

_RequiredNetworkSettingsTypeDef = TypedDict(
    "_RequiredNetworkSettingsTypeDef",
    {
        "networkSettingsArn": str,
    },
)
_OptionalNetworkSettingsTypeDef = TypedDict(
    "_OptionalNetworkSettingsTypeDef",
    {
        "associatedPortalArns": List[str],
        "securityGroupIds": List[str],
        "subnetIds": List[str],
        "vpcId": str,
    },
    total=False,
)


class NetworkSettingsTypeDef(_RequiredNetworkSettingsTypeDef, _OptionalNetworkSettingsTypeDef):
    pass


GetPortalRequestRequestTypeDef = TypedDict(
    "GetPortalRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

PortalTypeDef = TypedDict(
    "PortalTypeDef",
    {
        "browserSettingsArn": str,
        "browserType": Literal["Chrome"],
        "creationDate": datetime,
        "displayName": str,
        "networkSettingsArn": str,
        "portalArn": str,
        "portalEndpoint": str,
        "portalStatus": PortalStatusType,
        "rendererType": Literal["AppStream"],
        "statusReason": str,
        "trustStoreArn": str,
        "userSettingsArn": str,
    },
    total=False,
)

GetPortalServiceProviderMetadataRequestRequestTypeDef = TypedDict(
    "GetPortalServiceProviderMetadataRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)

GetTrustStoreCertificateRequestRequestTypeDef = TypedDict(
    "GetTrustStoreCertificateRequestRequestTypeDef",
    {
        "thumbprint": str,
        "trustStoreArn": str,
    },
)

GetTrustStoreRequestRequestTypeDef = TypedDict(
    "GetTrustStoreRequestRequestTypeDef",
    {
        "trustStoreArn": str,
    },
)

TrustStoreTypeDef = TypedDict(
    "TrustStoreTypeDef",
    {
        "associatedPortalArns": List[str],
        "trustStoreArn": str,
    },
    total=False,
)

GetUserSettingsRequestRequestTypeDef = TypedDict(
    "GetUserSettingsRequestRequestTypeDef",
    {
        "userSettingsArn": str,
    },
)

_RequiredUserSettingsTypeDef = TypedDict(
    "_RequiredUserSettingsTypeDef",
    {
        "userSettingsArn": str,
    },
)
_OptionalUserSettingsTypeDef = TypedDict(
    "_OptionalUserSettingsTypeDef",
    {
        "associatedPortalArns": List[str],
        "copyAllowed": EnabledTypeType,
        "disconnectTimeoutInMinutes": int,
        "downloadAllowed": EnabledTypeType,
        "idleDisconnectTimeoutInMinutes": int,
        "pasteAllowed": EnabledTypeType,
        "printAllowed": EnabledTypeType,
        "uploadAllowed": EnabledTypeType,
    },
    total=False,
)


class UserSettingsTypeDef(_RequiredUserSettingsTypeDef, _OptionalUserSettingsTypeDef):
    pass


IdentityProviderSummaryTypeDef = TypedDict(
    "IdentityProviderSummaryTypeDef",
    {
        "identityProviderArn": str,
        "identityProviderName": str,
        "identityProviderType": IdentityProviderTypeType,
    },
    total=False,
)

ListBrowserSettingsRequestRequestTypeDef = TypedDict(
    "ListBrowserSettingsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListIdentityProvidersRequestRequestTypeDef = TypedDict(
    "_RequiredListIdentityProvidersRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)
_OptionalListIdentityProvidersRequestRequestTypeDef = TypedDict(
    "_OptionalListIdentityProvidersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListIdentityProvidersRequestRequestTypeDef(
    _RequiredListIdentityProvidersRequestRequestTypeDef,
    _OptionalListIdentityProvidersRequestRequestTypeDef,
):
    pass


ListNetworkSettingsRequestRequestTypeDef = TypedDict(
    "ListNetworkSettingsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

NetworkSettingsSummaryTypeDef = TypedDict(
    "NetworkSettingsSummaryTypeDef",
    {
        "networkSettingsArn": str,
        "vpcId": str,
    },
    total=False,
)

ListPortalsRequestRequestTypeDef = TypedDict(
    "ListPortalsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

PortalSummaryTypeDef = TypedDict(
    "PortalSummaryTypeDef",
    {
        "browserSettingsArn": str,
        "browserType": Literal["Chrome"],
        "creationDate": datetime,
        "displayName": str,
        "networkSettingsArn": str,
        "portalArn": str,
        "portalEndpoint": str,
        "portalStatus": PortalStatusType,
        "rendererType": Literal["AppStream"],
        "trustStoreArn": str,
        "userSettingsArn": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredListTrustStoreCertificatesRequestRequestTypeDef = TypedDict(
    "_RequiredListTrustStoreCertificatesRequestRequestTypeDef",
    {
        "trustStoreArn": str,
    },
)
_OptionalListTrustStoreCertificatesRequestRequestTypeDef = TypedDict(
    "_OptionalListTrustStoreCertificatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTrustStoreCertificatesRequestRequestTypeDef(
    _RequiredListTrustStoreCertificatesRequestRequestTypeDef,
    _OptionalListTrustStoreCertificatesRequestRequestTypeDef,
):
    pass


ListTrustStoresRequestRequestTypeDef = TypedDict(
    "ListTrustStoresRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

TrustStoreSummaryTypeDef = TypedDict(
    "TrustStoreSummaryTypeDef",
    {
        "trustStoreArn": str,
    },
    total=False,
)

ListUserSettingsRequestRequestTypeDef = TypedDict(
    "ListUserSettingsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

UserSettingsSummaryTypeDef = TypedDict(
    "UserSettingsSummaryTypeDef",
    {
        "copyAllowed": EnabledTypeType,
        "disconnectTimeoutInMinutes": int,
        "downloadAllowed": EnabledTypeType,
        "idleDisconnectTimeoutInMinutes": int,
        "pasteAllowed": EnabledTypeType,
        "printAllowed": EnabledTypeType,
        "uploadAllowed": EnabledTypeType,
        "userSettingsArn": str,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateBrowserSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBrowserSettingsRequestRequestTypeDef",
    {
        "browserSettingsArn": str,
    },
)
_OptionalUpdateBrowserSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBrowserSettingsRequestRequestTypeDef",
    {
        "browserPolicy": str,
        "clientToken": str,
    },
    total=False,
)


class UpdateBrowserSettingsRequestRequestTypeDef(
    _RequiredUpdateBrowserSettingsRequestRequestTypeDef,
    _OptionalUpdateBrowserSettingsRequestRequestTypeDef,
):
    pass


_RequiredUpdateIdentityProviderRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIdentityProviderRequestRequestTypeDef",
    {
        "identityProviderArn": str,
    },
)
_OptionalUpdateIdentityProviderRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIdentityProviderRequestRequestTypeDef",
    {
        "clientToken": str,
        "identityProviderDetails": Mapping[str, str],
        "identityProviderName": str,
        "identityProviderType": IdentityProviderTypeType,
    },
    total=False,
)


class UpdateIdentityProviderRequestRequestTypeDef(
    _RequiredUpdateIdentityProviderRequestRequestTypeDef,
    _OptionalUpdateIdentityProviderRequestRequestTypeDef,
):
    pass


_RequiredUpdateNetworkSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNetworkSettingsRequestRequestTypeDef",
    {
        "networkSettingsArn": str,
    },
)
_OptionalUpdateNetworkSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNetworkSettingsRequestRequestTypeDef",
    {
        "clientToken": str,
        "securityGroupIds": Sequence[str],
        "subnetIds": Sequence[str],
        "vpcId": str,
    },
    total=False,
)


class UpdateNetworkSettingsRequestRequestTypeDef(
    _RequiredUpdateNetworkSettingsRequestRequestTypeDef,
    _OptionalUpdateNetworkSettingsRequestRequestTypeDef,
):
    pass


_RequiredUpdatePortalRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePortalRequestRequestTypeDef",
    {
        "portalArn": str,
    },
)
_OptionalUpdatePortalRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePortalRequestRequestTypeDef",
    {
        "displayName": str,
    },
    total=False,
)


class UpdatePortalRequestRequestTypeDef(
    _RequiredUpdatePortalRequestRequestTypeDef, _OptionalUpdatePortalRequestRequestTypeDef
):
    pass


_RequiredUpdateTrustStoreRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrustStoreRequestRequestTypeDef",
    {
        "trustStoreArn": str,
    },
)
_OptionalUpdateTrustStoreRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrustStoreRequestRequestTypeDef",
    {
        "certificatesToAdd": Sequence[Union[str, bytes, IO[Any], StreamingBody]],
        "certificatesToDelete": Sequence[str],
        "clientToken": str,
    },
    total=False,
)


class UpdateTrustStoreRequestRequestTypeDef(
    _RequiredUpdateTrustStoreRequestRequestTypeDef, _OptionalUpdateTrustStoreRequestRequestTypeDef
):
    pass


_RequiredUpdateUserSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserSettingsRequestRequestTypeDef",
    {
        "userSettingsArn": str,
    },
)
_OptionalUpdateUserSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserSettingsRequestRequestTypeDef",
    {
        "clientToken": str,
        "copyAllowed": EnabledTypeType,
        "disconnectTimeoutInMinutes": int,
        "downloadAllowed": EnabledTypeType,
        "idleDisconnectTimeoutInMinutes": int,
        "pasteAllowed": EnabledTypeType,
        "printAllowed": EnabledTypeType,
        "uploadAllowed": EnabledTypeType,
    },
    total=False,
)


class UpdateUserSettingsRequestRequestTypeDef(
    _RequiredUpdateUserSettingsRequestRequestTypeDef,
    _OptionalUpdateUserSettingsRequestRequestTypeDef,
):
    pass


AssociateBrowserSettingsResponseTypeDef = TypedDict(
    "AssociateBrowserSettingsResponseTypeDef",
    {
        "browserSettingsArn": str,
        "portalArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateNetworkSettingsResponseTypeDef = TypedDict(
    "AssociateNetworkSettingsResponseTypeDef",
    {
        "networkSettingsArn": str,
        "portalArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateTrustStoreResponseTypeDef = TypedDict(
    "AssociateTrustStoreResponseTypeDef",
    {
        "portalArn": str,
        "trustStoreArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateUserSettingsResponseTypeDef = TypedDict(
    "AssociateUserSettingsResponseTypeDef",
    {
        "portalArn": str,
        "userSettingsArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBrowserSettingsResponseTypeDef = TypedDict(
    "CreateBrowserSettingsResponseTypeDef",
    {
        "browserSettingsArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIdentityProviderResponseTypeDef = TypedDict(
    "CreateIdentityProviderResponseTypeDef",
    {
        "identityProviderArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNetworkSettingsResponseTypeDef = TypedDict(
    "CreateNetworkSettingsResponseTypeDef",
    {
        "networkSettingsArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePortalResponseTypeDef = TypedDict(
    "CreatePortalResponseTypeDef",
    {
        "portalArn": str,
        "portalEndpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrustStoreResponseTypeDef = TypedDict(
    "CreateTrustStoreResponseTypeDef",
    {
        "trustStoreArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserSettingsResponseTypeDef = TypedDict(
    "CreateUserSettingsResponseTypeDef",
    {
        "userSettingsArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPortalServiceProviderMetadataResponseTypeDef = TypedDict(
    "GetPortalServiceProviderMetadataResponseTypeDef",
    {
        "portalArn": str,
        "serviceProviderSamlMetadata": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTrustStoreResponseTypeDef = TypedDict(
    "UpdateTrustStoreResponseTypeDef",
    {
        "trustStoreArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBrowserSettingsResponseTypeDef = TypedDict(
    "ListBrowserSettingsResponseTypeDef",
    {
        "browserSettings": List[BrowserSettingsSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBrowserSettingsResponseTypeDef = TypedDict(
    "GetBrowserSettingsResponseTypeDef",
    {
        "browserSettings": BrowserSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBrowserSettingsResponseTypeDef = TypedDict(
    "UpdateBrowserSettingsResponseTypeDef",
    {
        "browserSettings": BrowserSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrustStoreCertificatesResponseTypeDef = TypedDict(
    "ListTrustStoreCertificatesResponseTypeDef",
    {
        "certificateList": List[CertificateSummaryTypeDef],
        "nextToken": str,
        "trustStoreArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrustStoreCertificateResponseTypeDef = TypedDict(
    "GetTrustStoreCertificateResponseTypeDef",
    {
        "certificate": CertificateTypeDef,
        "trustStoreArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateBrowserSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBrowserSettingsRequestRequestTypeDef",
    {
        "browserPolicy": str,
    },
)
_OptionalCreateBrowserSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBrowserSettingsRequestRequestTypeDef",
    {
        "additionalEncryptionContext": Mapping[str, str],
        "clientToken": str,
        "customerManagedKey": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateBrowserSettingsRequestRequestTypeDef(
    _RequiredCreateBrowserSettingsRequestRequestTypeDef,
    _OptionalCreateBrowserSettingsRequestRequestTypeDef,
):
    pass


_RequiredCreateNetworkSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkSettingsRequestRequestTypeDef",
    {
        "securityGroupIds": Sequence[str],
        "subnetIds": Sequence[str],
        "vpcId": str,
    },
)
_OptionalCreateNetworkSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkSettingsRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateNetworkSettingsRequestRequestTypeDef(
    _RequiredCreateNetworkSettingsRequestRequestTypeDef,
    _OptionalCreateNetworkSettingsRequestRequestTypeDef,
):
    pass


CreatePortalRequestRequestTypeDef = TypedDict(
    "CreatePortalRequestRequestTypeDef",
    {
        "additionalEncryptionContext": Mapping[str, str],
        "clientToken": str,
        "customerManagedKey": str,
        "displayName": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

_RequiredCreateTrustStoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrustStoreRequestRequestTypeDef",
    {
        "certificateList": Sequence[Union[str, bytes, IO[Any], StreamingBody]],
    },
)
_OptionalCreateTrustStoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrustStoreRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateTrustStoreRequestRequestTypeDef(
    _RequiredCreateTrustStoreRequestRequestTypeDef, _OptionalCreateTrustStoreRequestRequestTypeDef
):
    pass


_RequiredCreateUserSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserSettingsRequestRequestTypeDef",
    {
        "copyAllowed": EnabledTypeType,
        "downloadAllowed": EnabledTypeType,
        "pasteAllowed": EnabledTypeType,
        "printAllowed": EnabledTypeType,
        "uploadAllowed": EnabledTypeType,
    },
)
_OptionalCreateUserSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserSettingsRequestRequestTypeDef",
    {
        "clientToken": str,
        "disconnectTimeoutInMinutes": int,
        "idleDisconnectTimeoutInMinutes": int,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUserSettingsRequestRequestTypeDef(
    _RequiredCreateUserSettingsRequestRequestTypeDef,
    _OptionalCreateUserSettingsRequestRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredTagResourceRequestRequestTypeDef = TypedDict(
    "_RequiredTagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)
_OptionalTagResourceRequestRequestTypeDef = TypedDict(
    "_OptionalTagResourceRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class TagResourceRequestRequestTypeDef(
    _RequiredTagResourceRequestRequestTypeDef, _OptionalTagResourceRequestRequestTypeDef
):
    pass


GetIdentityProviderResponseTypeDef = TypedDict(
    "GetIdentityProviderResponseTypeDef",
    {
        "identityProvider": IdentityProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIdentityProviderResponseTypeDef = TypedDict(
    "UpdateIdentityProviderResponseTypeDef",
    {
        "identityProvider": IdentityProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNetworkSettingsResponseTypeDef = TypedDict(
    "GetNetworkSettingsResponseTypeDef",
    {
        "networkSettings": NetworkSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNetworkSettingsResponseTypeDef = TypedDict(
    "UpdateNetworkSettingsResponseTypeDef",
    {
        "networkSettings": NetworkSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPortalResponseTypeDef = TypedDict(
    "GetPortalResponseTypeDef",
    {
        "portal": PortalTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePortalResponseTypeDef = TypedDict(
    "UpdatePortalResponseTypeDef",
    {
        "portal": PortalTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrustStoreResponseTypeDef = TypedDict(
    "GetTrustStoreResponseTypeDef",
    {
        "trustStore": TrustStoreTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserSettingsResponseTypeDef = TypedDict(
    "GetUserSettingsResponseTypeDef",
    {
        "userSettings": UserSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserSettingsResponseTypeDef = TypedDict(
    "UpdateUserSettingsResponseTypeDef",
    {
        "userSettings": UserSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIdentityProvidersResponseTypeDef = TypedDict(
    "ListIdentityProvidersResponseTypeDef",
    {
        "identityProviders": List[IdentityProviderSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNetworkSettingsResponseTypeDef = TypedDict(
    "ListNetworkSettingsResponseTypeDef",
    {
        "networkSettings": List[NetworkSettingsSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPortalsResponseTypeDef = TypedDict(
    "ListPortalsResponseTypeDef",
    {
        "nextToken": str,
        "portals": List[PortalSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrustStoresResponseTypeDef = TypedDict(
    "ListTrustStoresResponseTypeDef",
    {
        "nextToken": str,
        "trustStores": List[TrustStoreSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserSettingsResponseTypeDef = TypedDict(
    "ListUserSettingsResponseTypeDef",
    {
        "nextToken": str,
        "userSettings": List[UserSettingsSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
