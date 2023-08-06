"""
Type annotations for health service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_health.client import HealthClient

    session = Session()
    client: HealthClient = session.client("health")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAffectedAccountsForOrganizationPaginator,
    DescribeAffectedEntitiesForOrganizationPaginator,
    DescribeAffectedEntitiesPaginator,
    DescribeEventAggregatesPaginator,
    DescribeEventsForOrganizationPaginator,
    DescribeEventsPaginator,
    DescribeEventTypesPaginator,
)
from .type_defs import (
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEntityAggregatesResponseTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventDetailsForOrganizationResponseTypeDef,
    DescribeEventDetailsResponseTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesResponseTypeDef,
    DescribeHealthServiceStatusForOrganizationResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EntityFilterTypeDef,
    EventAccountFilterTypeDef,
    EventFilterTypeDef,
    EventTypeFilterTypeDef,
    OrganizationEventFilterTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("HealthClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidPaginationToken: Type[BotocoreClientError]
    UnsupportedLocale: Type[BotocoreClientError]


class HealthClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#can_paginate)
        """

    def describe_affected_accounts_for_organization(
        self, *, eventArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> DescribeAffectedAccountsForOrganizationResponseTypeDef:
        """
        Returns a list of accounts in the organization from Organizations that are
        affected by the provided event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_affected_accounts_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_affected_accounts_for_organization)
        """

    def describe_affected_entities(
        self,
        *,
        filter: EntityFilterTypeDef,
        locale: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeAffectedEntitiesResponseTypeDef:
        """
        Returns a list of entities that have been affected by the specified events,
        based on the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_affected_entities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_affected_entities)
        """

    def describe_affected_entities_for_organization(
        self,
        *,
        organizationEntityFilters: Sequence[EventAccountFilterTypeDef],
        locale: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeAffectedEntitiesForOrganizationResponseTypeDef:
        """
        Returns a list of entities that have been affected by one or more events for one
        or more accounts in your organization in Organizations, based on the filter
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_affected_entities_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_affected_entities_for_organization)
        """

    def describe_entity_aggregates(
        self, *, eventArns: Sequence[str] = ...
    ) -> DescribeEntityAggregatesResponseTypeDef:
        """
        Returns the number of entities that are affected by each of the specified
        events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_entity_aggregates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_entity_aggregates)
        """

    def describe_event_aggregates(
        self,
        *,
        aggregateField: Literal["eventTypeCategory"],
        filter: EventFilterTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeEventAggregatesResponseTypeDef:
        """
        Returns the number of events of each event type (issue, scheduled change, and
        account notification).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_event_aggregates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_aggregates)
        """

    def describe_event_details(
        self, *, eventArns: Sequence[str], locale: str = ...
    ) -> DescribeEventDetailsResponseTypeDef:
        """
        Returns detailed information about one or more specified events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_event_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_details)
        """

    def describe_event_details_for_organization(
        self,
        *,
        organizationEventDetailFilters: Sequence[EventAccountFilterTypeDef],
        locale: str = ...
    ) -> DescribeEventDetailsForOrganizationResponseTypeDef:
        """
        Returns detailed information about one or more specified events for one or more
        Amazon Web Services accounts in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_event_details_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_details_for_organization)
        """

    def describe_event_types(
        self,
        *,
        filter: EventTypeFilterTypeDef = ...,
        locale: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeEventTypesResponseTypeDef:
        """
        Returns the event types that meet the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_event_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_types)
        """

    def describe_events(
        self,
        *,
        filter: EventFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        locale: str = ...
    ) -> DescribeEventsResponseTypeDef:
        """
        Returns information about events that meet the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_events)
        """

    def describe_events_for_organization(
        self,
        *,
        filter: OrganizationEventFilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        locale: str = ...
    ) -> DescribeEventsForOrganizationResponseTypeDef:
        """
        Returns information about events across your organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_events_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_events_for_organization)
        """

    def describe_health_service_status_for_organization(
        self,
    ) -> DescribeHealthServiceStatusForOrganizationResponseTypeDef:
        """
        This operation provides status information on enabling or disabling Health to
        work with your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.describe_health_service_status_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_health_service_status_for_organization)
        """

    def disable_health_service_access_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Disables Health from working with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.disable_health_service_access_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#disable_health_service_access_for_organization)
        """

    def enable_health_service_access_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Enables Health to work with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.enable_health_service_access_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#enable_health_service_access_for_organization)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#generate_presigned_url)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_affected_accounts_for_organization"]
    ) -> DescribeAffectedAccountsForOrganizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_affected_entities"]
    ) -> DescribeAffectedEntitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_affected_entities_for_organization"]
    ) -> DescribeAffectedEntitiesForOrganizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_aggregates"]
    ) -> DescribeEventAggregatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_types"]
    ) -> DescribeEventTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_events_for_organization"]
    ) -> DescribeEventsForOrganizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """
