"""
Main interface for amp service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amp import (
        Client,
        ListRuleGroupsNamespacesPaginator,
        ListWorkspacesPaginator,
        PrometheusServiceClient,
        WorkspaceActiveWaiter,
        WorkspaceDeletedWaiter,
    )

    session = Session()
    client: PrometheusServiceClient = session.client("amp")

    workspace_active_waiter: WorkspaceActiveWaiter = client.get_waiter("workspace_active")
    workspace_deleted_waiter: WorkspaceDeletedWaiter = client.get_waiter("workspace_deleted")

    list_rule_groups_namespaces_paginator: ListRuleGroupsNamespacesPaginator = client.get_paginator("list_rule_groups_namespaces")
    list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```
"""
from .client import PrometheusServiceClient
from .paginator import ListRuleGroupsNamespacesPaginator, ListWorkspacesPaginator
from .waiter import WorkspaceActiveWaiter, WorkspaceDeletedWaiter

Client = PrometheusServiceClient


__all__ = (
    "Client",
    "ListRuleGroupsNamespacesPaginator",
    "ListWorkspacesPaginator",
    "PrometheusServiceClient",
    "WorkspaceActiveWaiter",
    "WorkspaceDeletedWaiter",
)
