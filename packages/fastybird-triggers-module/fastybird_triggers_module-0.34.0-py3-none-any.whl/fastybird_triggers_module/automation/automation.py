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
Triggers module connectors connector worker module
"""

# Python base dependencies
import uuid
from typing import Optional, Union

# Library dependencies
from fastybird_exchange.publisher import Publisher
from fastybird_metadata.routing import RoutingKey
from fastybird_metadata.types import ControlAction, PropertyAction
from kink import inject
from sqlalchemy.orm import close_all_sessions

# Library libs
from fastybird_triggers_module.automation.queue import (
    AutomationQueue,
    ConsumeControlActionMessageQueueItem,
    ConsumeEntityMessageQueueItem,
)
from fastybird_triggers_module.entities.action import (
    ChannelPropertyActionEntity,
    DevicePropertyActionEntity,
)
from fastybird_triggers_module.entities.condition import (
    ChannelPropertyConditionEntity,
    DevicePropertyConditionEntity,
)
from fastybird_triggers_module.exceptions import TerminateAutomatorException
from fastybird_triggers_module.logger import Logger
from fastybird_triggers_module.managers.state import (
    ActionsStatesManager,
    ConditionsStatesManager,
)
from fastybird_triggers_module.repositories.action import ActionsRepository
from fastybird_triggers_module.repositories.condition import ConditionsRepository
from fastybird_triggers_module.repositories.state import (
    ActionsStatesRepository,
    ConditionsStatesRepository,
)
from fastybird_triggers_module.repositories.trigger import (
    TriggerControlsRepository,
    TriggersRepository,
)


@inject(
    bind={
        "publisher": Publisher,
    }
)
class Automator:  # pylint: disable=too-many-instance-attributes
    """
    Triggers automator

    @package        FastyBird:TriggersModule!
    @module         automation/automation

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __stopped: bool = False

    __queue: AutomationQueue

    __triggers_repository: TriggersRepository
    __triggers_control_repository: TriggerControlsRepository
    __actions_repository: ActionsRepository
    __conditions_repository: ConditionsRepository

    __actions_states_repository: ActionsStatesRepository
    __actions_states_manager: ActionsStatesManager
    __conditions_states_repository: ConditionsStatesRepository
    __conditions_states_manager: ConditionsStatesManager

    __publisher: Optional[Publisher] = None

    __logger: Logger

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments
        self,
        queue: AutomationQueue,
        triggers_repository: TriggersRepository,
        triggers_control_repository: TriggerControlsRepository,
        actions_repository: ActionsRepository,
        conditions_repository: ConditionsRepository,
        actions_states_repository: ActionsStatesRepository,
        actions_states_manager: ActionsStatesManager,
        conditions_states_repository: ConditionsStatesRepository,
        conditions_states_manager: ConditionsStatesManager,
        logger: Logger,
        publisher: Optional[Publisher] = None,
    ) -> None:
        self.__queue = queue

        self.__triggers_repository = triggers_repository
        self.__triggers_control_repository = triggers_control_repository
        self.__actions_repository = actions_repository
        self.__conditions_repository = conditions_repository

        self.__actions_states_repository = actions_states_repository
        self.__actions_states_manager = actions_states_manager
        self.__conditions_states_repository = conditions_states_repository
        self.__conditions_states_manager = conditions_states_manager

        self.__publisher = publisher

        self.__logger = logger

    # -----------------------------------------------------------------------------

    def start(self) -> None:
        """Start connector service"""
        self.__stopped = False

    # -----------------------------------------------------------------------------

    def stop(self) -> None:
        """Stop connector service"""
        self.__stopped = True

        self.__logger.info("Stopping...")

    # -----------------------------------------------------------------------------

    def handle(self) -> None:
        """Process connector actions"""
        # All records have to be processed before thread is closed
        if self.__stopped:
            return

        queue_item = self.__queue.get()

        if queue_item is not None:
            try:
                if isinstance(queue_item, ConsumeEntityMessageQueueItem):
                    self.__handle_entity_event(item=queue_item)

                if isinstance(queue_item, ConsumeControlActionMessageQueueItem):
                    self.__handle_control_event(item=queue_item)

            except Exception as ex:  # pylint: disable=broad-except
                self.__logger.error(
                    "An unexpected error occurred during processing queue item",
                    extra={
                        "exception": {
                            "message": str(ex),
                            "code": type(ex).__name__,
                        },
                    },
                )

                raise TerminateAutomatorException("An unexpected error occurred during processing queue item") from ex

    # -----------------------------------------------------------------------------

    def __handle_control_event(  # pylint: disable=too-many-branches,too-many-return-statements,too-many-statements
        self,
        item: ConsumeControlActionMessageQueueItem,
    ) -> None:
        if item.routing_key == RoutingKey.TRIGGER_ACTION and item.data.get("action") == ControlAction.SET.value:
            try:
                trigger_control = self.__triggers_control_repository.get_by_name(
                    trigger_id=uuid.UUID(item.data.get("trigger"), version=4),
                    control_name=str(item.data.get("name")),
                )

            except ValueError:
                return

            if trigger_control is None:
                return

            self.__process_trigger_actions(trigger_id=trigger_control.trigger.id)

    # -----------------------------------------------------------------------------

    def __handle_entity_event(  # pylint: disable=too-many-branches,too-many-return-statements,too-many-statements
        self,
        item: ConsumeEntityMessageQueueItem,
    ) -> None:
        if (
            item.routing_key
            in (
                RoutingKey.DEVICE_PROPERTY_ENTITY_CREATED,
                RoutingKey.DEVICE_PROPERTY_ENTITY_UPDATED,
                RoutingKey.CHANNEL_PROPERTY_ENTITY_CREATED,
                RoutingKey.CHANNEL_PROPERTY_ENTITY_UPDATED,
            )
            and "actual_value" in item.data.keys()
            and item.data.get("actual_value") is not None
        ):
            conditions = self.__conditions_repository.get_all_by_property_identifier(
                property_id=uuid.UUID(item.data.get("id"), version=4),
            )

            for condition in conditions:
                self.__validate_condition_property_item(condition=condition, value=str(item.data.get("actual_value")))

                is_fulfilled = self.__check_conditions(trigger_id=condition.trigger.id)

                if is_fulfilled:
                    trigger = self.__triggers_repository.get_by_id(trigger_id=condition.trigger.id)

                    if trigger is None or not trigger.enabled:
                        return

                    self.__process_trigger_actions(trigger_id=trigger.id)

            actions = self.__actions_repository.get_all_by_property_identifier(
                property_id=uuid.UUID(item.data.get("id"), version=4),
            )

            for action in actions:
                self.__validate_action_property_item(action=action, value=str(item.data.get("actual_value")))

        if item.routing_key in (
            RoutingKey.TRIGGER_ENTITY_CREATED,
            RoutingKey.TRIGGER_ENTITY_UPDATED,
            RoutingKey.TRIGGER_ENTITY_DELETED,
            RoutingKey.TRIGGER_CONTROL_ENTITY_CREATED,
            RoutingKey.TRIGGER_CONTROL_ENTITY_UPDATED,
            RoutingKey.TRIGGER_CONTROL_ENTITY_DELETED,
            RoutingKey.TRIGGER_ACTION_ENTITY_CREATED,
            RoutingKey.TRIGGER_ACTION_ENTITY_UPDATED,
            RoutingKey.TRIGGER_ACTION_ENTITY_DELETED,
            RoutingKey.TRIGGER_NOTIFICATION_ENTITY_CREATED,
            RoutingKey.TRIGGER_NOTIFICATION_ENTITY_UPDATED,
            RoutingKey.TRIGGER_NOTIFICATION_ENTITY_DELETED,
            RoutingKey.TRIGGER_CONDITION_ENTITY_CREATED,
            RoutingKey.TRIGGER_CONDITION_ENTITY_UPDATED,
            RoutingKey.TRIGGER_CONDITION_ENTITY_DELETED,
        ):
            # Clear all session after entity changes
            close_all_sessions()

    # -----------------------------------------------------------------------------

    def __validate_condition_property_item(
        self,
        condition: Union[DevicePropertyConditionEntity, ChannelPropertyConditionEntity],
        value: str,
    ) -> None:
        """Check property against trigger conditions"""
        is_fulfilled = condition.validate(value=value)

        try:
            condition_state = self.__conditions_states_repository.get_by_id(condition_id=condition.id)

        except NotImplementedError:
            return

        try:
            if condition_state is None:
                self.__conditions_states_manager.create(
                    condition=condition,
                    data={
                        "is_fulfilled": is_fulfilled,
                    },
                )

            else:
                self.__conditions_states_manager.update(
                    condition=condition,
                    state=condition_state,
                    data={
                        "is_fulfilled": is_fulfilled,
                    },
                )

        except NotImplementedError:
            return

        self.__logger.debug(
            "Validation result: %s was saved into: %s",
            is_fulfilled,
            condition.id,
        )

    # -----------------------------------------------------------------------------

    def __validate_action_property_item(
        self,
        action: Union[DevicePropertyActionEntity, ChannelPropertyActionEntity],
        value: str,
    ) -> None:
        """Check property against trigger actions"""
        is_triggered = action.validate(value=value)

        try:
            action_state = self.__actions_states_repository.get_by_id(action_id=action.id)

        except NotImplementedError:
            return

        try:
            if action_state is None:
                self.__actions_states_manager.create(
                    action=action,
                    data={
                        "is_triggered": is_triggered,
                    },
                )

            else:
                self.__actions_states_manager.update(
                    action=action,
                    state=action_state,
                    data={
                        "is_triggered": is_triggered,
                    },
                )

        except NotImplementedError:
            return

        self.__logger.debug(
            "Validation result: %s was saved into: %s",
            is_triggered,
            action.id,
        )

    # -----------------------------------------------------------------------------

    def __check_conditions(
        self,
        trigger_id: uuid.UUID,
    ) -> bool:
        conditions_count = 0

        for condition in self.__conditions_repository.get_all_by_trigger(trigger_id=trigger_id):
            if condition.enabled:
                conditions_count = conditions_count + 1

                if not isinstance(condition, (DevicePropertyConditionEntity, ChannelPropertyConditionEntity)):
                    return False

                try:
                    condition_state = self.__conditions_states_repository.get_by_id(condition_id=condition.id)

                except NotImplementedError:
                    return False

                if condition_state is None or not condition_state.is_fulfilled:
                    return False

        return conditions_count > 0

    # -----------------------------------------------------------------------------

    def __process_trigger_actions(
        self,
        trigger_id: uuid.UUID,
    ) -> None:
        if self.__publisher is None:
            return

        for action in self.__actions_repository.get_all_by_trigger(trigger_id=trigger_id):
            if action.enabled is True:
                if isinstance(action, DevicePropertyActionEntity):
                    self.__publisher.publish(
                        source=action.source,
                        routing_key=RoutingKey.DEVICE_PROPERTY_ACTION,
                        data={
                            "action": PropertyAction.SET.value,
                            "device": action.device.__str__(),
                            "property": action.device_property.__str__(),
                            "expected_value": str(action.value),
                        },
                    )

                    self.__logger.debug(
                        "Dispatching trigger action for device property: %s with value: %s",
                        action.device_property.__str__(),
                        str(action.value),
                    )

                elif isinstance(action, ChannelPropertyActionEntity):
                    self.__publisher.publish(
                        source=action.source,
                        routing_key=RoutingKey.CHANNEL_PROPERTY_ACTION,
                        data={
                            "action": PropertyAction.SET.value,
                            "device": action.device.__str__(),
                            "channel": action.channel.__str__(),
                            "property": action.channel_property.__str__(),
                            "expected_value": str(action.value),
                        },
                    )

                    self.__logger.debug(
                        "Dispatching trigger action for channel property: %s with value: %s",
                        action.channel_property.__str__(),
                        str(action.value),
                    )

                else:
                    self.__logger.warning("Trigger has unsupported action type: %s", type(action))
