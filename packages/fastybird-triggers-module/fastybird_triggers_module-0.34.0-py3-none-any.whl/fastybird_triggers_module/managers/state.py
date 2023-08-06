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
Triggers module device states managers module
"""

# Python base dependencies
from abc import abstractmethod
from typing import Dict, Optional, Union

# Library dependencies
from fastybird_exchange.publisher import Publisher
from fastybird_metadata.routing import RoutingKey
from kink import inject

# Library libs
from fastybird_triggers_module.entities.action import ActionEntity
from fastybird_triggers_module.entities.condition import ConditionEntity
from fastybird_triggers_module.state.action import IActionState
from fastybird_triggers_module.state.condition import IConditionState


class IActionsStatesManager:
    """
    Triggers actions states manager

    @package        FastyBird:TriggersModule!
    @module         managers/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def create(
        self,
        action: ActionEntity,
        data: Dict[str, Union[bool, None]],
    ) -> IActionState:
        """Create new action state record"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def update(
        self,
        action: ActionEntity,
        state: IActionState,
        data: Dict[str, Union[bool, None]],
    ) -> IActionState:
        """Update existing action state record"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def delete(
        self,
        action: ActionEntity,
        state: IActionState,
    ) -> bool:
        """Delete existing action state"""


class IConditionsStatesManager:
    """
    Triggers conditions states manager

    @package        FastyBird:TriggersModule!
    @module         managers/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def create(
        self,
        condition: ConditionEntity,
        data: Dict[str, Union[bool, None]],
    ) -> IConditionState:
        """Create new condition state record"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def update(
        self,
        condition: ConditionEntity,
        state: IConditionState,
        data: Dict[str, Union[bool, None]],
    ) -> IConditionState:
        """Update existing condition state record"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def delete(
        self,
        condition: ConditionEntity,
        state: IConditionState,
    ) -> bool:
        """Delete existing condition state"""


@inject(
    bind={
        "manager": IActionsStatesManager,
        "publisher": Publisher,
    }
)
class ActionsStatesManager:
    """
    Actions states manager

    @package        FastyBird:DevicesModule!
    @module         managers/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __manager: Optional[IActionsStatesManager] = None

    __publisher: Optional[Publisher] = None

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        manager: Optional[IActionsStatesManager] = None,
        publisher: Optional[Publisher] = None,
    ) -> None:
        self.__manager = manager
        self.__publisher = publisher

    # -----------------------------------------------------------------------------

    def create(
        self,
        action: ActionEntity,
        data: Dict[str, Union[bool, None]],
    ) -> IActionState:
        """Create new action state record"""
        if self.__manager is None:
            raise NotImplementedError("Actions states manager is not implemented")

        created_state = self.__manager.create(action=action, data=data)

        self.__publish_entity(
            action=action,
            state=created_state,
        )

        return created_state

    # -----------------------------------------------------------------------------

    def update(
        self,
        action: ActionEntity,
        state: IActionState,
        data: Dict[str, Union[bool, None]],
    ) -> IActionState:
        """Update existing action state record"""
        if self.__manager is None:
            raise NotImplementedError("Action states manager is not implemented")

        updated_state = self.__manager.update(action=action, state=state, data=data)

        self.__publish_entity(
            action=action,
            state=updated_state,
        )

        return updated_state

    # -----------------------------------------------------------------------------

    def delete(
        self,
        action: ActionEntity,
        state: IActionState,
    ) -> bool:
        """Delete existing action state"""
        if self.__manager is None:
            raise NotImplementedError("Action states manager is not implemented")

        result = self.__manager.delete(action=action, state=state)

        if result is True:
            self.__publish_entity(
                action=action,
                state=None,
            )

        return result

    # -----------------------------------------------------------------------------

    def __publish_entity(
        self,
        action: ActionEntity,
        state: Optional[IActionState],
    ) -> None:
        if self.__publisher is None:
            return

        self.__publisher.publish(
            source=action.source,
            routing_key=RoutingKey.TRIGGER_ACTION_ENTITY_UPDATED,
            data={
                **action.to_dict(),
                **{
                    "is_triggered": state.is_triggered if state is not None else False,
                },
            },
        )


@inject(
    bind={
        "manager": IConditionsStatesManager,
        "publisher": Publisher,
    }
)
class ConditionsStatesManager:
    """
    Conditions states manager

    @package        FastyBird:DevicesModule!
    @module         managers/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __manager: Optional[IConditionsStatesManager] = None

    __publisher: Optional[Publisher] = None

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        manager: Optional[IConditionsStatesManager] = None,
        publisher: Optional[Publisher] = None,
    ) -> None:
        self.__manager = manager
        self.__publisher = publisher

    # -----------------------------------------------------------------------------

    def create(
        self,
        condition: ConditionEntity,
        data: Dict[str, Union[bool, None]],
    ) -> IConditionState:
        """Create new condition state record"""
        if self.__manager is None:
            raise NotImplementedError("Conditions states manager is not implemented")

        created_state = self.__manager.create(condition=condition, data=data)

        self.__publish_entity(
            condition=condition,
            state=created_state,
        )

        return created_state

    # -----------------------------------------------------------------------------

    def update(
        self,
        condition: ConditionEntity,
        state: IConditionState,
        data: Dict[str, Union[bool, None]],
    ) -> IConditionState:
        """Update existing condition state record"""
        if self.__manager is None:
            raise NotImplementedError("Condition states manager is not implemented")

        updated_state = self.__manager.update(condition=condition, state=state, data=data)

        self.__publish_entity(
            condition=condition,
            state=updated_state,
        )

        return updated_state

    # -----------------------------------------------------------------------------

    def delete(
        self,
        condition: ConditionEntity,
        state: IConditionState,
    ) -> bool:
        """Delete existing condition state"""
        if self.__manager is None:
            raise NotImplementedError("Condition states manager is not implemented")

        result = self.__manager.delete(condition=condition, state=state)

        if result is True:
            self.__publish_entity(
                condition=condition,
                state=None,
            )

        return result

    # -----------------------------------------------------------------------------

    def __publish_entity(
        self,
        condition: ConditionEntity,
        state: Optional[IConditionState],
    ) -> None:
        if self.__publisher is None:
            return

        self.__publisher.publish(
            source=condition.source,
            routing_key=RoutingKey.TRIGGER_CONDITION_ENTITY_UPDATED,
            data={
                **condition.to_dict(),
                **{
                    "is_fulfilled": state.is_fulfilled if state is not None else False,
                },
            },
        )
