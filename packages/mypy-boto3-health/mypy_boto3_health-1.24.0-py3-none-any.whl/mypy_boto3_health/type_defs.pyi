"""
Type annotations for health service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/type_defs/)

Usage::

    ```python
    from mypy_boto3_health.type_defs import AffectedEntityTypeDef

    data: AffectedEntityTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    entityStatusCodeType,
    eventScopeCodeType,
    eventStatusCodeType,
    eventTypeCategoryType,
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
    "AffectedEntityTypeDef",
    "DateTimeRangeTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAffectedAccountsForOrganizationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "EventAccountFilterTypeDef",
    "OrganizationAffectedEntitiesErrorItemTypeDef",
    "DescribeEntityAggregatesRequestRequestTypeDef",
    "EntityAggregateTypeDef",
    "EventAggregateTypeDef",
    "OrganizationEventDetailsErrorItemTypeDef",
    "DescribeEventDetailsRequestRequestTypeDef",
    "EventDetailsErrorItemTypeDef",
    "EventTypeFilterTypeDef",
    "EventTypeTypeDef",
    "OrganizationEventTypeDef",
    "EventTypeDef",
    "EventDescriptionTypeDef",
    "EntityFilterTypeDef",
    "EventFilterTypeDef",
    "OrganizationEventFilterTypeDef",
    "DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef",
    "DescribeAffectedAccountsForOrganizationResponseTypeDef",
    "DescribeAffectedEntitiesResponseTypeDef",
    "DescribeHealthServiceStatusForOrganizationResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef",
    "DescribeAffectedEntitiesForOrganizationRequestRequestTypeDef",
    "DescribeEventDetailsForOrganizationRequestRequestTypeDef",
    "DescribeAffectedEntitiesForOrganizationResponseTypeDef",
    "DescribeEntityAggregatesResponseTypeDef",
    "DescribeEventAggregatesResponseTypeDef",
    "DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef",
    "DescribeEventTypesRequestRequestTypeDef",
    "DescribeEventTypesResponseTypeDef",
    "DescribeEventsForOrganizationResponseTypeDef",
    "DescribeEventsResponseTypeDef",
    "EventDetailsTypeDef",
    "OrganizationEventDetailsTypeDef",
    "DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef",
    "DescribeAffectedEntitiesRequestRequestTypeDef",
    "DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef",
    "DescribeEventAggregatesRequestRequestTypeDef",
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef",
    "DescribeEventsForOrganizationRequestRequestTypeDef",
    "DescribeEventDetailsResponseTypeDef",
    "DescribeEventDetailsForOrganizationResponseTypeDef",
)

AffectedEntityTypeDef = TypedDict(
    "AffectedEntityTypeDef",
    {
        "entityArn": str,
        "eventArn": str,
        "entityValue": str,
        "entityUrl": str,
        "awsAccountId": str,
        "lastUpdatedTime": datetime,
        "statusCode": entityStatusCodeType,
        "tags": Dict[str, str],
    },
    total=False,
)

DateTimeRangeTypeDef = TypedDict(
    "DateTimeRangeTypeDef",
    {
        "from": Union[datetime, str],
        "to": Union[datetime, str],
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

_RequiredDescribeAffectedAccountsForOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAffectedAccountsForOrganizationRequestRequestTypeDef",
    {
        "eventArn": str,
    },
)
_OptionalDescribeAffectedAccountsForOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAffectedAccountsForOrganizationRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class DescribeAffectedAccountsForOrganizationRequestRequestTypeDef(
    _RequiredDescribeAffectedAccountsForOrganizationRequestRequestTypeDef,
    _OptionalDescribeAffectedAccountsForOrganizationRequestRequestTypeDef,
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

_RequiredEventAccountFilterTypeDef = TypedDict(
    "_RequiredEventAccountFilterTypeDef",
    {
        "eventArn": str,
    },
)
_OptionalEventAccountFilterTypeDef = TypedDict(
    "_OptionalEventAccountFilterTypeDef",
    {
        "awsAccountId": str,
    },
    total=False,
)

class EventAccountFilterTypeDef(
    _RequiredEventAccountFilterTypeDef, _OptionalEventAccountFilterTypeDef
):
    pass

OrganizationAffectedEntitiesErrorItemTypeDef = TypedDict(
    "OrganizationAffectedEntitiesErrorItemTypeDef",
    {
        "awsAccountId": str,
        "eventArn": str,
        "errorName": str,
        "errorMessage": str,
    },
    total=False,
)

DescribeEntityAggregatesRequestRequestTypeDef = TypedDict(
    "DescribeEntityAggregatesRequestRequestTypeDef",
    {
        "eventArns": Sequence[str],
    },
    total=False,
)

EntityAggregateTypeDef = TypedDict(
    "EntityAggregateTypeDef",
    {
        "eventArn": str,
        "count": int,
    },
    total=False,
)

EventAggregateTypeDef = TypedDict(
    "EventAggregateTypeDef",
    {
        "aggregateValue": str,
        "count": int,
    },
    total=False,
)

OrganizationEventDetailsErrorItemTypeDef = TypedDict(
    "OrganizationEventDetailsErrorItemTypeDef",
    {
        "awsAccountId": str,
        "eventArn": str,
        "errorName": str,
        "errorMessage": str,
    },
    total=False,
)

_RequiredDescribeEventDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEventDetailsRequestRequestTypeDef",
    {
        "eventArns": Sequence[str],
    },
)
_OptionalDescribeEventDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEventDetailsRequestRequestTypeDef",
    {
        "locale": str,
    },
    total=False,
)

class DescribeEventDetailsRequestRequestTypeDef(
    _RequiredDescribeEventDetailsRequestRequestTypeDef,
    _OptionalDescribeEventDetailsRequestRequestTypeDef,
):
    pass

EventDetailsErrorItemTypeDef = TypedDict(
    "EventDetailsErrorItemTypeDef",
    {
        "eventArn": str,
        "errorName": str,
        "errorMessage": str,
    },
    total=False,
)

EventTypeFilterTypeDef = TypedDict(
    "EventTypeFilterTypeDef",
    {
        "eventTypeCodes": Sequence[str],
        "services": Sequence[str],
        "eventTypeCategories": Sequence[eventTypeCategoryType],
    },
    total=False,
)

EventTypeTypeDef = TypedDict(
    "EventTypeTypeDef",
    {
        "service": str,
        "code": str,
        "category": eventTypeCategoryType,
    },
    total=False,
)

OrganizationEventTypeDef = TypedDict(
    "OrganizationEventTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": eventTypeCategoryType,
        "eventScopeCode": eventScopeCodeType,
        "region": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": eventStatusCodeType,
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": eventTypeCategoryType,
        "region": str,
        "availabilityZone": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": eventStatusCodeType,
        "eventScopeCode": eventScopeCodeType,
    },
    total=False,
)

EventDescriptionTypeDef = TypedDict(
    "EventDescriptionTypeDef",
    {
        "latestDescription": str,
    },
    total=False,
)

_RequiredEntityFilterTypeDef = TypedDict(
    "_RequiredEntityFilterTypeDef",
    {
        "eventArns": Sequence[str],
    },
)
_OptionalEntityFilterTypeDef = TypedDict(
    "_OptionalEntityFilterTypeDef",
    {
        "entityArns": Sequence[str],
        "entityValues": Sequence[str],
        "lastUpdatedTimes": Sequence[DateTimeRangeTypeDef],
        "tags": Sequence[Mapping[str, str]],
        "statusCodes": Sequence[entityStatusCodeType],
    },
    total=False,
)

class EntityFilterTypeDef(_RequiredEntityFilterTypeDef, _OptionalEntityFilterTypeDef):
    pass

EventFilterTypeDef = TypedDict(
    "EventFilterTypeDef",
    {
        "eventArns": Sequence[str],
        "eventTypeCodes": Sequence[str],
        "services": Sequence[str],
        "regions": Sequence[str],
        "availabilityZones": Sequence[str],
        "startTimes": Sequence[DateTimeRangeTypeDef],
        "endTimes": Sequence[DateTimeRangeTypeDef],
        "lastUpdatedTimes": Sequence[DateTimeRangeTypeDef],
        "entityArns": Sequence[str],
        "entityValues": Sequence[str],
        "eventTypeCategories": Sequence[eventTypeCategoryType],
        "tags": Sequence[Mapping[str, str]],
        "eventStatusCodes": Sequence[eventStatusCodeType],
    },
    total=False,
)

OrganizationEventFilterTypeDef = TypedDict(
    "OrganizationEventFilterTypeDef",
    {
        "eventTypeCodes": Sequence[str],
        "awsAccountIds": Sequence[str],
        "services": Sequence[str],
        "regions": Sequence[str],
        "startTime": DateTimeRangeTypeDef,
        "endTime": DateTimeRangeTypeDef,
        "lastUpdatedTime": DateTimeRangeTypeDef,
        "entityArns": Sequence[str],
        "entityValues": Sequence[str],
        "eventTypeCategories": Sequence[eventTypeCategoryType],
        "eventStatusCodes": Sequence[eventStatusCodeType],
    },
    total=False,
)

_RequiredDescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef = TypedDict(
    "_RequiredDescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef",
    {
        "eventArn": str,
    },
)
_OptionalDescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef = TypedDict(
    "_OptionalDescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef(
    _RequiredDescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef,
    _OptionalDescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef,
):
    pass

DescribeAffectedAccountsForOrganizationResponseTypeDef = TypedDict(
    "DescribeAffectedAccountsForOrganizationResponseTypeDef",
    {
        "affectedAccounts": List[str],
        "eventScopeCode": eventScopeCodeType,
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAffectedEntitiesResponseTypeDef = TypedDict(
    "DescribeAffectedEntitiesResponseTypeDef",
    {
        "entities": List[AffectedEntityTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHealthServiceStatusForOrganizationResponseTypeDef = TypedDict(
    "DescribeHealthServiceStatusForOrganizationResponseTypeDef",
    {
        "healthServiceAccessStatusForOrganization": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef = TypedDict(
    "_RequiredDescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef",
    {
        "organizationEntityFilters": Sequence[EventAccountFilterTypeDef],
    },
)
_OptionalDescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef = TypedDict(
    "_OptionalDescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef",
    {
        "locale": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef(
    _RequiredDescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef,
    _OptionalDescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef,
):
    pass

_RequiredDescribeAffectedEntitiesForOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAffectedEntitiesForOrganizationRequestRequestTypeDef",
    {
        "organizationEntityFilters": Sequence[EventAccountFilterTypeDef],
    },
)
_OptionalDescribeAffectedEntitiesForOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAffectedEntitiesForOrganizationRequestRequestTypeDef",
    {
        "locale": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class DescribeAffectedEntitiesForOrganizationRequestRequestTypeDef(
    _RequiredDescribeAffectedEntitiesForOrganizationRequestRequestTypeDef,
    _OptionalDescribeAffectedEntitiesForOrganizationRequestRequestTypeDef,
):
    pass

_RequiredDescribeEventDetailsForOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEventDetailsForOrganizationRequestRequestTypeDef",
    {
        "organizationEventDetailFilters": Sequence[EventAccountFilterTypeDef],
    },
)
_OptionalDescribeEventDetailsForOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEventDetailsForOrganizationRequestRequestTypeDef",
    {
        "locale": str,
    },
    total=False,
)

class DescribeEventDetailsForOrganizationRequestRequestTypeDef(
    _RequiredDescribeEventDetailsForOrganizationRequestRequestTypeDef,
    _OptionalDescribeEventDetailsForOrganizationRequestRequestTypeDef,
):
    pass

DescribeAffectedEntitiesForOrganizationResponseTypeDef = TypedDict(
    "DescribeAffectedEntitiesForOrganizationResponseTypeDef",
    {
        "entities": List[AffectedEntityTypeDef],
        "failedSet": List[OrganizationAffectedEntitiesErrorItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEntityAggregatesResponseTypeDef = TypedDict(
    "DescribeEntityAggregatesResponseTypeDef",
    {
        "entityAggregates": List[EntityAggregateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventAggregatesResponseTypeDef = TypedDict(
    "DescribeEventAggregatesResponseTypeDef",
    {
        "eventAggregates": List[EventAggregateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef = TypedDict(
    "DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef",
    {
        "filter": EventTypeFilterTypeDef,
        "locale": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventTypesRequestRequestTypeDef = TypedDict(
    "DescribeEventTypesRequestRequestTypeDef",
    {
        "filter": EventTypeFilterTypeDef,
        "locale": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

DescribeEventTypesResponseTypeDef = TypedDict(
    "DescribeEventTypesResponseTypeDef",
    {
        "eventTypes": List[EventTypeTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventsForOrganizationResponseTypeDef = TypedDict(
    "DescribeEventsForOrganizationResponseTypeDef",
    {
        "events": List[OrganizationEventTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef",
    {
        "events": List[EventTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventDetailsTypeDef = TypedDict(
    "EventDetailsTypeDef",
    {
        "event": EventTypeDef,
        "eventDescription": EventDescriptionTypeDef,
        "eventMetadata": Dict[str, str],
    },
    total=False,
)

OrganizationEventDetailsTypeDef = TypedDict(
    "OrganizationEventDetailsTypeDef",
    {
        "awsAccountId": str,
        "event": EventTypeDef,
        "eventDescription": EventDescriptionTypeDef,
        "eventMetadata": Dict[str, str],
    },
    total=False,
)

_RequiredDescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef = TypedDict(
    "_RequiredDescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef",
    {
        "filter": EntityFilterTypeDef,
    },
)
_OptionalDescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef = TypedDict(
    "_OptionalDescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef",
    {
        "locale": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef(
    _RequiredDescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef,
    _OptionalDescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef,
):
    pass

_RequiredDescribeAffectedEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAffectedEntitiesRequestRequestTypeDef",
    {
        "filter": EntityFilterTypeDef,
    },
)
_OptionalDescribeAffectedEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAffectedEntitiesRequestRequestTypeDef",
    {
        "locale": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class DescribeAffectedEntitiesRequestRequestTypeDef(
    _RequiredDescribeAffectedEntitiesRequestRequestTypeDef,
    _OptionalDescribeAffectedEntitiesRequestRequestTypeDef,
):
    pass

_RequiredDescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef = TypedDict(
    "_RequiredDescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef",
    {
        "aggregateField": Literal["eventTypeCategory"],
    },
)
_OptionalDescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef = TypedDict(
    "_OptionalDescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef",
    {
        "filter": EventFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef(
    _RequiredDescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef,
    _OptionalDescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef,
):
    pass

_RequiredDescribeEventAggregatesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEventAggregatesRequestRequestTypeDef",
    {
        "aggregateField": Literal["eventTypeCategory"],
    },
)
_OptionalDescribeEventAggregatesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEventAggregatesRequestRequestTypeDef",
    {
        "filter": EventFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class DescribeEventAggregatesRequestRequestTypeDef(
    _RequiredDescribeEventAggregatesRequestRequestTypeDef,
    _OptionalDescribeEventAggregatesRequestRequestTypeDef,
):
    pass

DescribeEventsRequestDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    {
        "filter": EventFilterTypeDef,
        "locale": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventsRequestRequestTypeDef = TypedDict(
    "DescribeEventsRequestRequestTypeDef",
    {
        "filter": EventFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
        "locale": str,
    },
    total=False,
)

DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef = TypedDict(
    "DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef",
    {
        "filter": OrganizationEventFilterTypeDef,
        "locale": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventsForOrganizationRequestRequestTypeDef = TypedDict(
    "DescribeEventsForOrganizationRequestRequestTypeDef",
    {
        "filter": OrganizationEventFilterTypeDef,
        "nextToken": str,
        "maxResults": int,
        "locale": str,
    },
    total=False,
)

DescribeEventDetailsResponseTypeDef = TypedDict(
    "DescribeEventDetailsResponseTypeDef",
    {
        "successfulSet": List[EventDetailsTypeDef],
        "failedSet": List[EventDetailsErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventDetailsForOrganizationResponseTypeDef = TypedDict(
    "DescribeEventDetailsForOrganizationResponseTypeDef",
    {
        "successfulSet": List[OrganizationEventDetailsTypeDef],
        "failedSet": List[OrganizationEventDetailsErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
