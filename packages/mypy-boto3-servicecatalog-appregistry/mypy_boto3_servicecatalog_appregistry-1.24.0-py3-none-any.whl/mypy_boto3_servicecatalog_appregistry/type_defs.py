"""
Type annotations for servicecatalog-appregistry service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/type_defs/)

Usage::

    ```python
    from mypy_boto3_servicecatalog_appregistry.type_defs import ApplicationSummaryTypeDef

    data: ApplicationSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import ResourceGroupStateType, SyncActionType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApplicationSummaryTypeDef",
    "ApplicationTypeDef",
    "AssociateAttributeGroupRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateResourceRequestRequestTypeDef",
    "AttributeGroupSummaryTypeDef",
    "AttributeGroupTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateAttributeGroupRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteAttributeGroupRequestRequestTypeDef",
    "DisassociateAttributeGroupRequestRequestTypeDef",
    "DisassociateResourceRequestRequestTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetAssociatedResourceRequestRequestTypeDef",
    "GetAttributeGroupRequestRequestTypeDef",
    "ResourceGroupTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListAssociatedAttributeGroupsRequestRequestTypeDef",
    "ListAssociatedResourcesRequestRequestTypeDef",
    "ResourceInfoTypeDef",
    "ListAttributeGroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "SyncResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateAttributeGroupRequestRequestTypeDef",
    "AssociateAttributeGroupResponseTypeDef",
    "AssociateResourceResponseTypeDef",
    "CreateApplicationResponseTypeDef",
    "DeleteApplicationResponseTypeDef",
    "DisassociateAttributeGroupResponseTypeDef",
    "DisassociateResourceResponseTypeDef",
    "GetAttributeGroupResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListAssociatedAttributeGroupsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SyncResourceResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "DeleteAttributeGroupResponseTypeDef",
    "ListAttributeGroupsResponseTypeDef",
    "CreateAttributeGroupResponseTypeDef",
    "UpdateAttributeGroupResponseTypeDef",
    "IntegrationsTypeDef",
    "ResourceIntegrationsTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
    "ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    "ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef",
    "ListAssociatedResourcesResponseTypeDef",
    "GetApplicationResponseTypeDef",
    "ResourceTypeDef",
    "GetAssociatedResourceResponseTypeDef",
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

AssociateAttributeGroupRequestRequestTypeDef = TypedDict(
    "AssociateAttributeGroupRequestRequestTypeDef",
    {
        "application": str,
        "attributeGroup": str,
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

AssociateResourceRequestRequestTypeDef = TypedDict(
    "AssociateResourceRequestRequestTypeDef",
    {
        "application": str,
        "resourceType": Literal["CFN_STACK"],
        "resource": str,
    },
)

AttributeGroupSummaryTypeDef = TypedDict(
    "AttributeGroupSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

AttributeGroupTypeDef = TypedDict(
    "AttributeGroupTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "name": str,
        "clientToken": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


_RequiredCreateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAttributeGroupRequestRequestTypeDef",
    {
        "name": str,
        "attributes": str,
        "clientToken": str,
    },
)
_OptionalCreateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAttributeGroupRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAttributeGroupRequestRequestTypeDef(
    _RequiredCreateAttributeGroupRequestRequestTypeDef,
    _OptionalCreateAttributeGroupRequestRequestTypeDef,
):
    pass


DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)

DeleteAttributeGroupRequestRequestTypeDef = TypedDict(
    "DeleteAttributeGroupRequestRequestTypeDef",
    {
        "attributeGroup": str,
    },
)

DisassociateAttributeGroupRequestRequestTypeDef = TypedDict(
    "DisassociateAttributeGroupRequestRequestTypeDef",
    {
        "application": str,
        "attributeGroup": str,
    },
)

DisassociateResourceRequestRequestTypeDef = TypedDict(
    "DisassociateResourceRequestRequestTypeDef",
    {
        "application": str,
        "resourceType": Literal["CFN_STACK"],
        "resource": str,
    },
)

GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)

GetAssociatedResourceRequestRequestTypeDef = TypedDict(
    "GetAssociatedResourceRequestRequestTypeDef",
    {
        "application": str,
        "resourceType": Literal["CFN_STACK"],
        "resource": str,
    },
)

GetAttributeGroupRequestRequestTypeDef = TypedDict(
    "GetAttributeGroupRequestRequestTypeDef",
    {
        "attributeGroup": str,
    },
)

ResourceGroupTypeDef = TypedDict(
    "ResourceGroupTypeDef",
    {
        "state": ResourceGroupStateType,
        "arn": str,
        "errorMessage": str,
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

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListAssociatedAttributeGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedAttributeGroupsRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalListAssociatedAttributeGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedAttributeGroupsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedAttributeGroupsRequestRequestTypeDef(
    _RequiredListAssociatedAttributeGroupsRequestRequestTypeDef,
    _OptionalListAssociatedAttributeGroupsRequestRequestTypeDef,
):
    pass


_RequiredListAssociatedResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedResourcesRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalListAssociatedResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedResourcesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedResourcesRequestRequestTypeDef(
    _RequiredListAssociatedResourcesRequestRequestTypeDef,
    _OptionalListAssociatedResourcesRequestRequestTypeDef,
):
    pass


ResourceInfoTypeDef = TypedDict(
    "ResourceInfoTypeDef",
    {
        "name": str,
        "arn": str,
    },
    total=False,
)

ListAttributeGroupsRequestRequestTypeDef = TypedDict(
    "ListAttributeGroupsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

SyncResourceRequestRequestTypeDef = TypedDict(
    "SyncResourceRequestRequestTypeDef",
    {
        "resourceType": Literal["CFN_STACK"],
        "resource": str,
    },
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

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


_RequiredUpdateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAttributeGroupRequestRequestTypeDef",
    {
        "attributeGroup": str,
    },
)
_OptionalUpdateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAttributeGroupRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "attributes": str,
    },
    total=False,
)


class UpdateAttributeGroupRequestRequestTypeDef(
    _RequiredUpdateAttributeGroupRequestRequestTypeDef,
    _OptionalUpdateAttributeGroupRequestRequestTypeDef,
):
    pass


AssociateAttributeGroupResponseTypeDef = TypedDict(
    "AssociateAttributeGroupResponseTypeDef",
    {
        "applicationArn": str,
        "attributeGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateResourceResponseTypeDef = TypedDict(
    "AssociateResourceResponseTypeDef",
    {
        "applicationArn": str,
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApplicationResponseTypeDef = TypedDict(
    "DeleteApplicationResponseTypeDef",
    {
        "application": ApplicationSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateAttributeGroupResponseTypeDef = TypedDict(
    "DisassociateAttributeGroupResponseTypeDef",
    {
        "applicationArn": str,
        "attributeGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateResourceResponseTypeDef = TypedDict(
    "DisassociateResourceResponseTypeDef",
    {
        "applicationArn": str,
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAttributeGroupResponseTypeDef = TypedDict(
    "GetAttributeGroupResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "attributes": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "applications": List[ApplicationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedAttributeGroupsResponseTypeDef = TypedDict(
    "ListAssociatedAttributeGroupsResponseTypeDef",
    {
        "attributeGroups": List[str],
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

SyncResourceResponseTypeDef = TypedDict(
    "SyncResourceResponseTypeDef",
    {
        "applicationArn": str,
        "resourceArn": str,
        "actionTaken": SyncActionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAttributeGroupResponseTypeDef = TypedDict(
    "DeleteAttributeGroupResponseTypeDef",
    {
        "attributeGroup": AttributeGroupSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttributeGroupsResponseTypeDef = TypedDict(
    "ListAttributeGroupsResponseTypeDef",
    {
        "attributeGroups": List[AttributeGroupSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAttributeGroupResponseTypeDef = TypedDict(
    "CreateAttributeGroupResponseTypeDef",
    {
        "attributeGroup": AttributeGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAttributeGroupResponseTypeDef = TypedDict(
    "UpdateAttributeGroupResponseTypeDef",
    {
        "attributeGroup": AttributeGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IntegrationsTypeDef = TypedDict(
    "IntegrationsTypeDef",
    {
        "resourceGroup": ResourceGroupTypeDef,
    },
    total=False,
)

ResourceIntegrationsTypeDef = TypedDict(
    "ResourceIntegrationsTypeDef",
    {
        "resourceGroup": ResourceGroupTypeDef,
    },
    total=False,
)

ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef = (
    TypedDict(
        "_RequiredListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
        {
            "application": str,
        },
    )
)
_OptionalListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef = (
    TypedDict(
        "_OptionalListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
        {
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)


class ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef(
    _RequiredListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef,
    _OptionalListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef,
):
    pass


_RequiredListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    {
        "application": str,
    },
)
_OptionalListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef(
    _RequiredListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef,
    _OptionalListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef,
):
    pass


ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef = TypedDict(
    "ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAssociatedResourcesResponseTypeDef = TypedDict(
    "ListAssociatedResourcesResponseTypeDef",
    {
        "resources": List[ResourceInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "associatedResourceCount": int,
        "tags": Dict[str, str],
        "integrations": IntegrationsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "name": str,
        "arn": str,
        "associationTime": datetime,
        "integrations": ResourceIntegrationsTypeDef,
    },
    total=False,
)

GetAssociatedResourceResponseTypeDef = TypedDict(
    "GetAssociatedResourceResponseTypeDef",
    {
        "resource": ResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
