"""
Type annotations for codestar-notifications service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codestar_notifications.client import CodeStarNotificationsClient
    from mypy_boto3_codestar_notifications.paginator import (
        ListEventTypesPaginator,
        ListNotificationRulesPaginator,
        ListTargetsPaginator,
    )

    session = Session()
    client: CodeStarNotificationsClient = session.client("codestar-notifications")

    list_event_types_paginator: ListEventTypesPaginator = client.get_paginator("list_event_types")
    list_notification_rules_paginator: ListNotificationRulesPaginator = client.get_paginator("list_notification_rules")
    list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListEventTypesFilterTypeDef,
    ListEventTypesResultTypeDef,
    ListNotificationRulesFilterTypeDef,
    ListNotificationRulesResultTypeDef,
    ListTargetsFilterTypeDef,
    ListTargetsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListEventTypesPaginator", "ListNotificationRulesPaginator", "ListTargetsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEventTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Paginator.ListEventTypes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listeventtypespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ListEventTypesFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEventTypesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Paginator.ListEventTypes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listeventtypespaginator)
        """


class ListNotificationRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Paginator.ListNotificationRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listnotificationrulespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ListNotificationRulesFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNotificationRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Paginator.ListNotificationRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listnotificationrulespaginator)
        """


class ListTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Paginator.ListTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listtargetspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ListTargetsFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Paginator.ListTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_notifications/paginators/#listtargetspaginator)
        """
