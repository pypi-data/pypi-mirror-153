"""
Type annotations for events service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_events.client import EventBridgeClient

    session = Session()
    client: EventBridgeClient = session.client("events")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ApiDestinationHttpMethodType,
    ArchiveStateType,
    ConnectionAuthorizationTypeType,
    ConnectionStateType,
    ReplayStateType,
    RuleStateType,
)
from .paginator import (
    ListRuleNamesByTargetPaginator,
    ListRulesPaginator,
    ListTargetsByRulePaginator,
)
from .type_defs import (
    CancelReplayResponseTypeDef,
    ConditionTypeDef,
    CreateApiDestinationResponseTypeDef,
    CreateArchiveResponseTypeDef,
    CreateConnectionAuthRequestParametersTypeDef,
    CreateConnectionResponseTypeDef,
    CreateEndpointResponseTypeDef,
    CreateEventBusResponseTypeDef,
    CreatePartnerEventSourceResponseTypeDef,
    DeauthorizeConnectionResponseTypeDef,
    DeleteConnectionResponseTypeDef,
    DescribeApiDestinationResponseTypeDef,
    DescribeArchiveResponseTypeDef,
    DescribeConnectionResponseTypeDef,
    DescribeEndpointResponseTypeDef,
    DescribeEventBusResponseTypeDef,
    DescribeEventSourceResponseTypeDef,
    DescribePartnerEventSourceResponseTypeDef,
    DescribeReplayResponseTypeDef,
    DescribeRuleResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EndpointEventBusTypeDef,
    ListApiDestinationsResponseTypeDef,
    ListArchivesResponseTypeDef,
    ListConnectionsResponseTypeDef,
    ListEndpointsResponseTypeDef,
    ListEventBusesResponseTypeDef,
    ListEventSourcesResponseTypeDef,
    ListPartnerEventSourceAccountsResponseTypeDef,
    ListPartnerEventSourcesResponseTypeDef,
    ListReplaysResponseTypeDef,
    ListRuleNamesByTargetResponseTypeDef,
    ListRulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsByRuleResponseTypeDef,
    PutEventsRequestEntryTypeDef,
    PutEventsResponseTypeDef,
    PutPartnerEventsRequestEntryTypeDef,
    PutPartnerEventsResponseTypeDef,
    PutRuleResponseTypeDef,
    PutTargetsResponseTypeDef,
    RemoveTargetsResponseTypeDef,
    ReplayDestinationTypeDef,
    ReplicationConfigTypeDef,
    RoutingConfigTypeDef,
    StartReplayResponseTypeDef,
    TagTypeDef,
    TargetTypeDef,
    TestEventPatternResponseTypeDef,
    UpdateApiDestinationResponseTypeDef,
    UpdateArchiveResponseTypeDef,
    UpdateConnectionAuthRequestParametersTypeDef,
    UpdateConnectionResponseTypeDef,
    UpdateEndpointResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("EventBridgeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    IllegalStatusException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidEventPatternException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ManagedRuleException: Type[BotocoreClientError]
    OperationDisabledException: Type[BotocoreClientError]
    PolicyLengthExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class EventBridgeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EventBridgeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#exceptions)
        """

    def activate_event_source(self, *, Name: str) -> EmptyResponseMetadataTypeDef:
        """
        Activates a partner event source that has been deactivated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.activate_event_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#activate_event_source)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#can_paginate)
        """

    def cancel_replay(self, *, ReplayName: str) -> CancelReplayResponseTypeDef:
        """
        Cancels the specified replay.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.cancel_replay)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#cancel_replay)
        """

    def create_api_destination(
        self,
        *,
        Name: str,
        ConnectionArn: str,
        InvocationEndpoint: str,
        HttpMethod: ApiDestinationHttpMethodType,
        Description: str = ...,
        InvocationRateLimitPerSecond: int = ...
    ) -> CreateApiDestinationResponseTypeDef:
        """
        Creates an API destination, which is an HTTP invocation endpoint configured as a
        target for events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.create_api_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_api_destination)
        """

    def create_archive(
        self,
        *,
        ArchiveName: str,
        EventSourceArn: str,
        Description: str = ...,
        EventPattern: str = ...,
        RetentionDays: int = ...
    ) -> CreateArchiveResponseTypeDef:
        """
        Creates an archive of events with the specified settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.create_archive)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_archive)
        """

    def create_connection(
        self,
        *,
        Name: str,
        AuthorizationType: ConnectionAuthorizationTypeType,
        AuthParameters: CreateConnectionAuthRequestParametersTypeDef,
        Description: str = ...
    ) -> CreateConnectionResponseTypeDef:
        """
        Creates a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.create_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_connection)
        """

    def create_endpoint(
        self,
        *,
        Name: str,
        RoutingConfig: RoutingConfigTypeDef,
        EventBuses: Sequence[EndpointEventBusTypeDef],
        Description: str = ...,
        ReplicationConfig: ReplicationConfigTypeDef = ...,
        RoleArn: str = ...
    ) -> CreateEndpointResponseTypeDef:
        """
        Creates a global endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.create_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_endpoint)
        """

    def create_event_bus(
        self, *, Name: str, EventSourceName: str = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> CreateEventBusResponseTypeDef:
        """
        Creates a new event bus within your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.create_event_bus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_event_bus)
        """

    def create_partner_event_source(
        self, *, Name: str, Account: str
    ) -> CreatePartnerEventSourceResponseTypeDef:
        """
        Called by an SaaS partner to create a partner event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.create_partner_event_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#create_partner_event_source)
        """

    def deactivate_event_source(self, *, Name: str) -> EmptyResponseMetadataTypeDef:
        """
        You can use this operation to temporarily stop receiving events from the
        specified partner event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.deactivate_event_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#deactivate_event_source)
        """

    def deauthorize_connection(self, *, Name: str) -> DeauthorizeConnectionResponseTypeDef:
        """
        Removes all authorization parameters from the connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.deauthorize_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#deauthorize_connection)
        """

    def delete_api_destination(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the specified API destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_api_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_api_destination)
        """

    def delete_archive(self, *, ArchiveName: str) -> Dict[str, Any]:
        """
        Deletes the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_archive)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_archive)
        """

    def delete_connection(self, *, Name: str) -> DeleteConnectionResponseTypeDef:
        """
        Deletes a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_connection)
        """

    def delete_endpoint(self, *, Name: str) -> Dict[str, Any]:
        """
        Delete an existing global endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_endpoint)
        """

    def delete_event_bus(self, *, Name: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified custom event bus or partner event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_event_bus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_event_bus)
        """

    def delete_partner_event_source(
        self, *, Name: str, Account: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is used by SaaS partners to delete a partner event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_partner_event_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_partner_event_source)
        """

    def delete_rule(
        self, *, Name: str, EventBusName: str = ..., Force: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.delete_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#delete_rule)
        """

    def describe_api_destination(self, *, Name: str) -> DescribeApiDestinationResponseTypeDef:
        """
        Retrieves details about an API destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_api_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_api_destination)
        """

    def describe_archive(self, *, ArchiveName: str) -> DescribeArchiveResponseTypeDef:
        """
        Retrieves details about an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_archive)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_archive)
        """

    def describe_connection(self, *, Name: str) -> DescribeConnectionResponseTypeDef:
        """
        Retrieves details about a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_connection)
        """

    def describe_endpoint(
        self, *, Name: str, HomeRegion: str = ...
    ) -> DescribeEndpointResponseTypeDef:
        """
        Get the information about an existing global endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_endpoint)
        """

    def describe_event_bus(self, *, Name: str = ...) -> DescribeEventBusResponseTypeDef:
        """
        Displays details about an event bus in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_event_bus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_event_bus)
        """

    def describe_event_source(self, *, Name: str) -> DescribeEventSourceResponseTypeDef:
        """
        This operation lists details about a partner event source that is shared with
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_event_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_event_source)
        """

    def describe_partner_event_source(
        self, *, Name: str
    ) -> DescribePartnerEventSourceResponseTypeDef:
        """
        An SaaS partner can use this operation to list details about a partner event
        source that they have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_partner_event_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_partner_event_source)
        """

    def describe_replay(self, *, ReplayName: str) -> DescribeReplayResponseTypeDef:
        """
        Retrieves details about a replay.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_replay)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_replay)
        """

    def describe_rule(self, *, Name: str, EventBusName: str = ...) -> DescribeRuleResponseTypeDef:
        """
        Describes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.describe_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#describe_rule)
        """

    def disable_rule(self, *, Name: str, EventBusName: str = ...) -> EmptyResponseMetadataTypeDef:
        """
        Disables the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.disable_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#disable_rule)
        """

    def enable_rule(self, *, Name: str, EventBusName: str = ...) -> EmptyResponseMetadataTypeDef:
        """
        Enables the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.enable_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#enable_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#generate_presigned_url)
        """

    def list_api_destinations(
        self,
        *,
        NamePrefix: str = ...,
        ConnectionArn: str = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> ListApiDestinationsResponseTypeDef:
        """
        Retrieves a list of API destination in the account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_api_destinations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_api_destinations)
        """

    def list_archives(
        self,
        *,
        NamePrefix: str = ...,
        EventSourceArn: str = ...,
        State: ArchiveStateType = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> ListArchivesResponseTypeDef:
        """
        Lists your archives.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_archives)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_archives)
        """

    def list_connections(
        self,
        *,
        NamePrefix: str = ...,
        ConnectionState: ConnectionStateType = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> ListConnectionsResponseTypeDef:
        """
        Retrieves a list of connections from the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_connections)
        """

    def list_endpoints(
        self,
        *,
        NamePrefix: str = ...,
        HomeRegion: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListEndpointsResponseTypeDef:
        """
        List the global endpoints associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_endpoints)
        """

    def list_event_buses(
        self, *, NamePrefix: str = ..., NextToken: str = ..., Limit: int = ...
    ) -> ListEventBusesResponseTypeDef:
        """
        Lists all the event buses in your account, including the default event bus,
        custom event buses, and partner event buses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_event_buses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_event_buses)
        """

    def list_event_sources(
        self, *, NamePrefix: str = ..., NextToken: str = ..., Limit: int = ...
    ) -> ListEventSourcesResponseTypeDef:
        """
        You can use this to see all the partner event sources that have been shared with
        your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_event_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_event_sources)
        """

    def list_partner_event_source_accounts(
        self, *, EventSourceName: str, NextToken: str = ..., Limit: int = ...
    ) -> ListPartnerEventSourceAccountsResponseTypeDef:
        """
        An SaaS partner can use this operation to display the Amazon Web Services
        account ID that a particular partner event source name is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_partner_event_source_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_partner_event_source_accounts)
        """

    def list_partner_event_sources(
        self, *, NamePrefix: str, NextToken: str = ..., Limit: int = ...
    ) -> ListPartnerEventSourcesResponseTypeDef:
        """
        An SaaS partner can use this operation to list all the partner event source
        names that they have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_partner_event_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_partner_event_sources)
        """

    def list_replays(
        self,
        *,
        NamePrefix: str = ...,
        State: ReplayStateType = ...,
        EventSourceArn: str = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> ListReplaysResponseTypeDef:
        """
        Lists your replays.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_replays)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_replays)
        """

    def list_rule_names_by_target(
        self, *, TargetArn: str, EventBusName: str = ..., NextToken: str = ..., Limit: int = ...
    ) -> ListRuleNamesByTargetResponseTypeDef:
        """
        Lists the rules for the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_rule_names_by_target)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_rule_names_by_target)
        """

    def list_rules(
        self,
        *,
        NamePrefix: str = ...,
        EventBusName: str = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> ListRulesResponseTypeDef:
        """
        Lists your Amazon EventBridge rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_rules)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with an EventBridge resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_tags_for_resource)
        """

    def list_targets_by_rule(
        self, *, Rule: str, EventBusName: str = ..., NextToken: str = ..., Limit: int = ...
    ) -> ListTargetsByRuleResponseTypeDef:
        """
        Lists the targets assigned to the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.list_targets_by_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#list_targets_by_rule)
        """

    def put_events(
        self, *, Entries: Sequence[PutEventsRequestEntryTypeDef], EndpointId: str = ...
    ) -> PutEventsResponseTypeDef:
        """
        Sends custom events to Amazon EventBridge so that they can be matched to rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.put_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_events)
        """

    def put_partner_events(
        self, *, Entries: Sequence[PutPartnerEventsRequestEntryTypeDef]
    ) -> PutPartnerEventsResponseTypeDef:
        """
        This is used by SaaS partners to write events to a customer's partner event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.put_partner_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_partner_events)
        """

    def put_permission(
        self,
        *,
        EventBusName: str = ...,
        Action: str = ...,
        Principal: str = ...,
        StatementId: str = ...,
        Condition: ConditionTypeDef = ...,
        Policy: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Running `PutPermission` permits the specified Amazon Web Services account or
        Amazon Web Services organization to put events to the specified *event bus*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.put_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_permission)
        """

    def put_rule(
        self,
        *,
        Name: str,
        ScheduleExpression: str = ...,
        EventPattern: str = ...,
        State: RuleStateType = ...,
        Description: str = ...,
        RoleArn: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        EventBusName: str = ...
    ) -> PutRuleResponseTypeDef:
        """
        Creates or updates the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.put_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_rule)
        """

    def put_targets(
        self, *, Rule: str, Targets: Sequence[TargetTypeDef], EventBusName: str = ...
    ) -> PutTargetsResponseTypeDef:
        """
        Adds the specified targets to the specified rule, or updates the targets if they
        are already associated with the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.put_targets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#put_targets)
        """

    def remove_permission(
        self, *, StatementId: str = ..., RemoveAllPermissions: bool = ..., EventBusName: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes the permission of another Amazon Web Services account to be able to put
        events to the specified event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.remove_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#remove_permission)
        """

    def remove_targets(
        self, *, Rule: str, Ids: Sequence[str], EventBusName: str = ..., Force: bool = ...
    ) -> RemoveTargetsResponseTypeDef:
        """
        Removes the specified targets from the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.remove_targets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#remove_targets)
        """

    def start_replay(
        self,
        *,
        ReplayName: str,
        EventSourceArn: str,
        EventStartTime: Union[datetime, str],
        EventEndTime: Union[datetime, str],
        Destination: ReplayDestinationTypeDef,
        Description: str = ...
    ) -> StartReplayResponseTypeDef:
        """
        Starts the specified replay.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.start_replay)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#start_replay)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified EventBridge
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#tag_resource)
        """

    def test_event_pattern(
        self, *, EventPattern: str, Event: str
    ) -> TestEventPatternResponseTypeDef:
        """
        Tests whether the specified event pattern matches the provided event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.test_event_pattern)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#test_event_pattern)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified EventBridge resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#untag_resource)
        """

    def update_api_destination(
        self,
        *,
        Name: str,
        Description: str = ...,
        ConnectionArn: str = ...,
        InvocationEndpoint: str = ...,
        HttpMethod: ApiDestinationHttpMethodType = ...,
        InvocationRateLimitPerSecond: int = ...
    ) -> UpdateApiDestinationResponseTypeDef:
        """
        Updates an API destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.update_api_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_api_destination)
        """

    def update_archive(
        self,
        *,
        ArchiveName: str,
        Description: str = ...,
        EventPattern: str = ...,
        RetentionDays: int = ...
    ) -> UpdateArchiveResponseTypeDef:
        """
        Updates the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.update_archive)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_archive)
        """

    def update_connection(
        self,
        *,
        Name: str,
        Description: str = ...,
        AuthorizationType: ConnectionAuthorizationTypeType = ...,
        AuthParameters: UpdateConnectionAuthRequestParametersTypeDef = ...
    ) -> UpdateConnectionResponseTypeDef:
        """
        Updates settings for a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.update_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_connection)
        """

    def update_endpoint(
        self,
        *,
        Name: str,
        Description: str = ...,
        RoutingConfig: RoutingConfigTypeDef = ...,
        ReplicationConfig: ReplicationConfigTypeDef = ...,
        EventBuses: Sequence[EndpointEventBusTypeDef] = ...,
        RoleArn: str = ...
    ) -> UpdateEndpointResponseTypeDef:
        """
        Update an existing endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.update_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#update_endpoint)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rule_names_by_target"]
    ) -> ListRuleNamesByTargetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_by_rule"]
    ) -> ListTargetsByRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/client/#get_paginator)
        """
