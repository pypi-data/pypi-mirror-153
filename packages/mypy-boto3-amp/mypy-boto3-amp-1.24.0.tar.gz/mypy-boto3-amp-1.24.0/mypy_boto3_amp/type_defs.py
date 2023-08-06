"""
Type annotations for amp service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amp/type_defs/)

Usage::

    ```python
    from mypy_boto3_amp.type_defs import AlertManagerDefinitionStatusTypeDef

    data: AlertManagerDefinitionStatusTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlertManagerDefinitionStatusCodeType,
    RuleGroupsNamespaceStatusCodeType,
    WorkspaceStatusCodeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AlertManagerDefinitionStatusTypeDef",
    "CreateAlertManagerDefinitionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateRuleGroupsNamespaceRequestRequestTypeDef",
    "RuleGroupsNamespaceStatusTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "WorkspaceStatusTypeDef",
    "DeleteAlertManagerDefinitionRequestRequestTypeDef",
    "DeleteRuleGroupsNamespaceRequestRequestTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "PaginatorConfigTypeDef",
    "ListRuleGroupsNamespacesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "PutAlertManagerDefinitionRequestRequestTypeDef",
    "PutRuleGroupsNamespaceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateWorkspaceAliasRequestRequestTypeDef",
    "AlertManagerDefinitionDescriptionTypeDef",
    "CreateAlertManagerDefinitionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutAlertManagerDefinitionResponseTypeDef",
    "CreateRuleGroupsNamespaceResponseTypeDef",
    "PutRuleGroupsNamespaceResponseTypeDef",
    "RuleGroupsNamespaceDescriptionTypeDef",
    "RuleGroupsNamespaceSummaryTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceSummaryTypeDef",
    "DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    "DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    "ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    "DescribeAlertManagerDefinitionResponseTypeDef",
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    "ListRuleGroupsNamespacesResponseTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "ListWorkspacesResponseTypeDef",
)

_RequiredAlertManagerDefinitionStatusTypeDef = TypedDict(
    "_RequiredAlertManagerDefinitionStatusTypeDef",
    {
        "statusCode": AlertManagerDefinitionStatusCodeType,
    },
)
_OptionalAlertManagerDefinitionStatusTypeDef = TypedDict(
    "_OptionalAlertManagerDefinitionStatusTypeDef",
    {
        "statusReason": str,
    },
    total=False,
)


class AlertManagerDefinitionStatusTypeDef(
    _RequiredAlertManagerDefinitionStatusTypeDef, _OptionalAlertManagerDefinitionStatusTypeDef
):
    pass


_RequiredCreateAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAlertManagerDefinitionRequestRequestTypeDef",
    {
        "data": Union[str, bytes, IO[Any], StreamingBody],
        "workspaceId": str,
    },
)
_OptionalCreateAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAlertManagerDefinitionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateAlertManagerDefinitionRequestRequestTypeDef(
    _RequiredCreateAlertManagerDefinitionRequestRequestTypeDef,
    _OptionalCreateAlertManagerDefinitionRequestRequestTypeDef,
):
    pass


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

_RequiredCreateRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "data": Union[str, bytes, IO[Any], StreamingBody],
        "name": str,
        "workspaceId": str,
    },
)
_OptionalCreateRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateRuleGroupsNamespaceRequestRequestTypeDef(
    _RequiredCreateRuleGroupsNamespaceRequestRequestTypeDef,
    _OptionalCreateRuleGroupsNamespaceRequestRequestTypeDef,
):
    pass


_RequiredRuleGroupsNamespaceStatusTypeDef = TypedDict(
    "_RequiredRuleGroupsNamespaceStatusTypeDef",
    {
        "statusCode": RuleGroupsNamespaceStatusCodeType,
    },
)
_OptionalRuleGroupsNamespaceStatusTypeDef = TypedDict(
    "_OptionalRuleGroupsNamespaceStatusTypeDef",
    {
        "statusReason": str,
    },
    total=False,
)


class RuleGroupsNamespaceStatusTypeDef(
    _RequiredRuleGroupsNamespaceStatusTypeDef, _OptionalRuleGroupsNamespaceStatusTypeDef
):
    pass


CreateWorkspaceRequestRequestTypeDef = TypedDict(
    "CreateWorkspaceRequestRequestTypeDef",
    {
        "alias": str,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

WorkspaceStatusTypeDef = TypedDict(
    "WorkspaceStatusTypeDef",
    {
        "statusCode": WorkspaceStatusCodeType,
    },
)

_RequiredDeleteAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalDeleteAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAlertManagerDefinitionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAlertManagerDefinitionRequestRequestTypeDef(
    _RequiredDeleteAlertManagerDefinitionRequestRequestTypeDef,
    _OptionalDeleteAlertManagerDefinitionRequestRequestTypeDef,
):
    pass


_RequiredDeleteRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "name": str,
        "workspaceId": str,
    },
)
_OptionalDeleteRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteRuleGroupsNamespaceRequestRequestTypeDef(
    _RequiredDeleteRuleGroupsNamespaceRequestRequestTypeDef,
    _OptionalDeleteRuleGroupsNamespaceRequestRequestTypeDef,
):
    pass


_RequiredDeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalDeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteWorkspaceRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteWorkspaceRequestRequestTypeDef(
    _RequiredDeleteWorkspaceRequestRequestTypeDef, _OptionalDeleteWorkspaceRequestRequestTypeDef
):
    pass


DescribeAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "name": str,
        "workspaceId": str,
    },
)

DescribeWorkspaceRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
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

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListRuleGroupsNamespacesRequestRequestTypeDef = TypedDict(
    "_RequiredListRuleGroupsNamespacesRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListRuleGroupsNamespacesRequestRequestTypeDef = TypedDict(
    "_OptionalListRuleGroupsNamespacesRequestRequestTypeDef",
    {
        "maxResults": int,
        "name": str,
        "nextToken": str,
    },
    total=False,
)


class ListRuleGroupsNamespacesRequestRequestTypeDef(
    _RequiredListRuleGroupsNamespacesRequestRequestTypeDef,
    _OptionalListRuleGroupsNamespacesRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "alias": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredPutAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredPutAlertManagerDefinitionRequestRequestTypeDef",
    {
        "data": Union[str, bytes, IO[Any], StreamingBody],
        "workspaceId": str,
    },
)
_OptionalPutAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalPutAlertManagerDefinitionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class PutAlertManagerDefinitionRequestRequestTypeDef(
    _RequiredPutAlertManagerDefinitionRequestRequestTypeDef,
    _OptionalPutAlertManagerDefinitionRequestRequestTypeDef,
):
    pass


_RequiredPutRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredPutRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "data": Union[str, bytes, IO[Any], StreamingBody],
        "name": str,
        "workspaceId": str,
    },
)
_OptionalPutRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalPutRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class PutRuleGroupsNamespaceRequestRequestTypeDef(
    _RequiredPutRuleGroupsNamespaceRequestRequestTypeDef,
    _OptionalPutRuleGroupsNamespaceRequestRequestTypeDef,
):
    pass


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

_RequiredUpdateWorkspaceAliasRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkspaceAliasRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalUpdateWorkspaceAliasRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkspaceAliasRequestRequestTypeDef",
    {
        "alias": str,
        "clientToken": str,
    },
    total=False,
)


class UpdateWorkspaceAliasRequestRequestTypeDef(
    _RequiredUpdateWorkspaceAliasRequestRequestTypeDef,
    _OptionalUpdateWorkspaceAliasRequestRequestTypeDef,
):
    pass


AlertManagerDefinitionDescriptionTypeDef = TypedDict(
    "AlertManagerDefinitionDescriptionTypeDef",
    {
        "createdAt": datetime,
        "data": bytes,
        "modifiedAt": datetime,
        "status": AlertManagerDefinitionStatusTypeDef,
    },
)

CreateAlertManagerDefinitionResponseTypeDef = TypedDict(
    "CreateAlertManagerDefinitionResponseTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
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

PutAlertManagerDefinitionResponseTypeDef = TypedDict(
    "PutAlertManagerDefinitionResponseTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "CreateRuleGroupsNamespaceResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "PutRuleGroupsNamespaceResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRuleGroupsNamespaceDescriptionTypeDef = TypedDict(
    "_RequiredRuleGroupsNamespaceDescriptionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "data": bytes,
        "modifiedAt": datetime,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
    },
)
_OptionalRuleGroupsNamespaceDescriptionTypeDef = TypedDict(
    "_OptionalRuleGroupsNamespaceDescriptionTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)


class RuleGroupsNamespaceDescriptionTypeDef(
    _RequiredRuleGroupsNamespaceDescriptionTypeDef, _OptionalRuleGroupsNamespaceDescriptionTypeDef
):
    pass


_RequiredRuleGroupsNamespaceSummaryTypeDef = TypedDict(
    "_RequiredRuleGroupsNamespaceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
    },
)
_OptionalRuleGroupsNamespaceSummaryTypeDef = TypedDict(
    "_OptionalRuleGroupsNamespaceSummaryTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)


class RuleGroupsNamespaceSummaryTypeDef(
    _RequiredRuleGroupsNamespaceSummaryTypeDef, _OptionalRuleGroupsNamespaceSummaryTypeDef
):
    pass


CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "arn": str,
        "status": WorkspaceStatusTypeDef,
        "tags": Dict[str, str],
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredWorkspaceDescriptionTypeDef = TypedDict(
    "_RequiredWorkspaceDescriptionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "status": WorkspaceStatusTypeDef,
        "workspaceId": str,
    },
)
_OptionalWorkspaceDescriptionTypeDef = TypedDict(
    "_OptionalWorkspaceDescriptionTypeDef",
    {
        "alias": str,
        "prometheusEndpoint": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class WorkspaceDescriptionTypeDef(
    _RequiredWorkspaceDescriptionTypeDef, _OptionalWorkspaceDescriptionTypeDef
):
    pass


_RequiredWorkspaceSummaryTypeDef = TypedDict(
    "_RequiredWorkspaceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "status": WorkspaceStatusTypeDef,
        "workspaceId": str,
    },
)
_OptionalWorkspaceSummaryTypeDef = TypedDict(
    "_OptionalWorkspaceSummaryTypeDef",
    {
        "alias": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class WorkspaceSummaryTypeDef(_RequiredWorkspaceSummaryTypeDef, _OptionalWorkspaceSummaryTypeDef):
    pass


_RequiredDescribeWorkspaceRequestWorkspaceActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalDescribeWorkspaceRequestWorkspaceActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef(
    _RequiredDescribeWorkspaceRequestWorkspaceActiveWaitTypeDef,
    _OptionalDescribeWorkspaceRequestWorkspaceActiveWaitTypeDef,
):
    pass


_RequiredDescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalDescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef(
    _RequiredDescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef,
    _OptionalDescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef,
):
    pass


_RequiredListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef = TypedDict(
    "_RequiredListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef = TypedDict(
    "_OptionalListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    {
        "name": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef(
    _RequiredListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef,
    _OptionalListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef,
):
    pass


ListWorkspacesRequestListWorkspacesPaginateTypeDef = TypedDict(
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    {
        "alias": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAlertManagerDefinitionResponseTypeDef = TypedDict(
    "DescribeAlertManagerDefinitionResponseTypeDef",
    {
        "alertManagerDefinition": AlertManagerDefinitionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    {
        "ruleGroupsNamespace": RuleGroupsNamespaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRuleGroupsNamespacesResponseTypeDef = TypedDict(
    "ListRuleGroupsNamespacesResponseTypeDef",
    {
        "nextToken": str,
        "ruleGroupsNamespaces": List[RuleGroupsNamespaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceResponseTypeDef = TypedDict(
    "DescribeWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "nextToken": str,
        "workspaces": List[WorkspaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
