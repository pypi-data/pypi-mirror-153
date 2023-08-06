#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Triggers module subscriber module
"""

# Python base dependencies
import datetime
from typing import Dict, Optional, Type

# Library dependencies
from fastybird_exchange.publisher import Publisher
from fastybird_metadata.routing import RoutingKey
from kink import inject
from sqlalchemy import event
from sqlalchemy.orm import Session as OrmSession

# Library libs
from fastybird_triggers_module.entities.action import (
    ActionEntity,
    ChannelPropertyActionEntity,
    DevicePropertyActionEntity,
)
from fastybird_triggers_module.entities.base import (
    Base,
    EntityCreatedMixin,
    EntityUpdatedMixin,
)
from fastybird_triggers_module.entities.condition import (
    ChannelPropertyConditionEntity,
    ConditionEntity,
    DateConditionEntity,
    DevicePropertyConditionEntity,
    TimeConditionEntity,
)
from fastybird_triggers_module.entities.notification import (
    EmailNotificationEntity,
    SmsNotificationEntity,
)
from fastybird_triggers_module.entities.trigger import (
    AutomaticTriggerEntity,
    ManualTriggerEntity,
    TriggerControlEntity,
    TriggerEntity,
)
from fastybird_triggers_module.repositories.state import (
    ActionsStatesRepository,
    ConditionsStatesRepository,
)


class EntityCreatedSubscriber:  # pylint: disable=too-few-public-methods
    """
    New entity creation subscriber

    @package        FastyBird:TriggersModule!
    @module         subscriber

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    def __init__(self) -> None:
        event.listen(
            Base, "before_insert", lambda mapper, connection, target: self.before_insert(target), propagate=True
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def before_insert(target: Base) -> None:
        """Before entity inserted update timestamp"""
        if isinstance(target, EntityCreatedMixin):
            target.created_at = datetime.datetime.now()


class EntityUpdatedSubscriber:  # pylint: disable=too-few-public-methods
    """
    Existing entity update subscriber

    @package        FastyBird:TriggersModule!
    @module         subscriber

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    def __init__(self) -> None:
        event.listen(
            Base, "before_update", lambda mapper, connection, target: self.before_update(target), propagate=True
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def before_update(target: Base) -> None:
        """Before entity updated update timestamp"""
        if isinstance(target, EntityUpdatedMixin):
            target.updated_at = datetime.datetime.now()


@inject(
    bind={
        "publisher": Publisher,
    }
)
class EntitiesSubscriber:  # pylint: disable=too-few-public-methods
    """
    Data exchanges utils

    @package        FastyBird:TriggersModule!
    @module         subscriber

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    CREATED_ENTITIES_ROUTING_KEYS_MAPPING: Dict[Type[Base], RoutingKey] = {
        ManualTriggerEntity: RoutingKey.TRIGGER_ENTITY_CREATED,
        AutomaticTriggerEntity: RoutingKey.TRIGGER_ENTITY_CREATED,
        TriggerControlEntity: RoutingKey.TRIGGER_CONTROL_ENTITY_CREATED,
        DevicePropertyActionEntity: RoutingKey.TRIGGER_ACTION_ENTITY_CREATED,
        ChannelPropertyActionEntity: RoutingKey.TRIGGER_ACTION_ENTITY_CREATED,
        DevicePropertyConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_CREATED,
        ChannelPropertyConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_CREATED,
        TimeConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_CREATED,
        DateConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_CREATED,
        SmsNotificationEntity: RoutingKey.TRIGGER_NOTIFICATION_ENTITY_CREATED,
        EmailNotificationEntity: RoutingKey.TRIGGER_NOTIFICATION_ENTITY_CREATED,
    }

    UPDATED_ENTITIES_ROUTING_KEYS_MAPPING: Dict[Type[Base], RoutingKey] = {
        ManualTriggerEntity: RoutingKey.TRIGGER_ENTITY_UPDATED,
        AutomaticTriggerEntity: RoutingKey.TRIGGER_ENTITY_UPDATED,
        TriggerControlEntity: RoutingKey.TRIGGER_CONTROL_ENTITY_UPDATED,
        DevicePropertyActionEntity: RoutingKey.TRIGGER_ACTION_ENTITY_UPDATED,
        ChannelPropertyActionEntity: RoutingKey.TRIGGER_ACTION_ENTITY_UPDATED,
        DevicePropertyConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_UPDATED,
        ChannelPropertyConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_UPDATED,
        TimeConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_UPDATED,
        DateConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_UPDATED,
        SmsNotificationEntity: RoutingKey.TRIGGER_NOTIFICATION_ENTITY_UPDATED,
        EmailNotificationEntity: RoutingKey.TRIGGER_NOTIFICATION_ENTITY_UPDATED,
    }

    DELETED_ENTITIES_ROUTING_KEYS_MAPPING: Dict[Type[Base], RoutingKey] = {
        ManualTriggerEntity: RoutingKey.TRIGGER_ENTITY_DELETED,
        AutomaticTriggerEntity: RoutingKey.TRIGGER_ENTITY_DELETED,
        TriggerControlEntity: RoutingKey.TRIGGER_CONTROL_ENTITY_DELETED,
        DevicePropertyActionEntity: RoutingKey.TRIGGER_ACTION_ENTITY_DELETED,
        ChannelPropertyActionEntity: RoutingKey.TRIGGER_ACTION_ENTITY_DELETED,
        DevicePropertyConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_DELETED,
        ChannelPropertyConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_DELETED,
        TimeConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_DELETED,
        DateConditionEntity: RoutingKey.TRIGGER_CONDITION_ENTITY_DELETED,
        SmsNotificationEntity: RoutingKey.TRIGGER_NOTIFICATION_ENTITY_DELETED,
        EmailNotificationEntity: RoutingKey.TRIGGER_NOTIFICATION_ENTITY_DELETED,
    }

    __publisher: Optional[Publisher]

    __action_state_repository: ActionsStatesRepository
    __condition_state_repository: ConditionsStatesRepository

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        session: OrmSession,
        action_state_repository: ActionsStatesRepository,
        condition_state_repository: ConditionsStatesRepository,
        publisher: Optional[Publisher] = None,
    ) -> None:
        self.__publisher = publisher

        self.__action_state_repository = action_state_repository
        self.__condition_state_repository = condition_state_repository

        event.listen(session, "after_flush", lambda active_session, transaction: self.after_flush(active_session))

    # -----------------------------------------------------------------------------

    def after_flush(self, session: OrmSession) -> None:
        """Event"""
        if self.__publisher is None:
            return

        for entity in session.new:
            routing_key = self.__get_entity_created_routing_key(entity=type(entity))

            if routing_key is not None:
                exchange_data = {**entity.to_dict(), **self.__get_entity_extended_data(entity=entity)}

                self.__publisher.publish(
                    source=entity.source,
                    routing_key=routing_key,
                    data=exchange_data,
                )

        for entity in session.dirty:
            if not session.is_modified(entity, include_collections=False):
                continue

            routing_key = self.__get_entity_updated_routing_key(entity=type(entity))

            if routing_key is not None:
                exchange_data = {**entity.to_dict(), **self.__get_entity_extended_data(entity=entity)}

                self.__publisher.publish(
                    source=entity.source,
                    routing_key=routing_key,
                    data=exchange_data,
                )

        for entity in session.deleted:
            routing_key = self.__get_entity_deleted_routing_key(entity=type(entity))

            if routing_key is not None:
                self.__publisher.publish(
                    source=entity.source,
                    routing_key=routing_key,
                    data={**entity.to_dict(), **self.__get_entity_extended_data(entity=entity)},
                )

    # -----------------------------------------------------------------------------

    def __get_entity_created_routing_key(self, entity: Type[Base]) -> Optional[RoutingKey]:
        """Get routing key for created entity"""
        for classname, routing_key in self.CREATED_ENTITIES_ROUTING_KEYS_MAPPING.items():
            if issubclass(entity, classname):
                return routing_key

        return None

    # -----------------------------------------------------------------------------

    def __get_entity_updated_routing_key(self, entity: Type[Base]) -> Optional[RoutingKey]:
        """Get routing key for updated entity"""
        for classname, routing_key in self.UPDATED_ENTITIES_ROUTING_KEYS_MAPPING.items():
            if issubclass(entity, classname):
                return routing_key

        return None

    # -----------------------------------------------------------------------------

    def __get_entity_deleted_routing_key(self, entity: Type[Base]) -> Optional[RoutingKey]:
        """Get routing key for deleted entity"""
        for classname, routing_key in self.DELETED_ENTITIES_ROUTING_KEYS_MAPPING.items():
            if issubclass(entity, classname):
                return routing_key

        return None

    # -----------------------------------------------------------------------------

    def __get_entity_extended_data(  # pylint: disable=too-many-return-statements,too-many-branches
        self,
        entity: Base,
    ) -> Dict:
        if isinstance(entity, ActionEntity):
            try:
                action_state = self.__action_state_repository.get_by_id(action_id=entity.id)

            except NotImplementedError:
                return {}

            if action_state is None:
                return {}

            return {
                "is_triggered": action_state.is_triggered,
            }

        if isinstance(entity, ConditionEntity):
            try:
                condition_state = self.__condition_state_repository.get_by_id(condition_id=entity.id)

            except NotImplementedError:
                return {}

            if condition_state is None:
                return {}

            return {
                "is_fulfilled": condition_state.is_fulfilled,
            }

        if isinstance(entity, TriggerEntity):
            is_triggered: bool = True

            try:
                for action in entity.actions:
                    action_state = self.__action_state_repository.get_by_id(action_id=action.id)

                    if action_state is None or action_state.is_triggered is False:
                        is_triggered = False

            except NotImplementedError:
                is_triggered = False

            if isinstance(entity, AutomaticTriggerEntity):
                is_fulfilled = True

                try:
                    for condition in entity.conditions:
                        condition_state = self.__condition_state_repository.get_by_id(condition_id=condition.id)

                        if condition_state is None or condition_state.is_fulfilled is False:
                            is_fulfilled = False

                except NotImplementedError:
                    is_fulfilled = False

                return {
                    "is_triggered": is_triggered,
                    "is_fulfilled": is_fulfilled,
                }

            return {
                "is_triggered": is_triggered,
            }

        return {}
