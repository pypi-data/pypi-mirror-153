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
Triggers module state repositories module
"""

# Python base dependencies
import uuid
from abc import ABC, abstractmethod
from typing import Optional

# Library dependencies
from kink import inject

# Library libs
from fastybird_triggers_module.state.action import IActionState
from fastybird_triggers_module.state.condition import IConditionState


class IActionsStatesRepository(ABC):  # pylint: disable=too-few-public-methods
    """
    State repository for action

    @package        FastyBird:TriggersModule!
    @module         repositories/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def get_by_id(self, action_id: uuid.UUID) -> Optional[IActionState]:
        """Find trigger action state record by provided database identifier"""


class IConditionsStatesRepository(ABC):  # pylint: disable=too-few-public-methods
    """
    State repository for condition

    @package        FastyBird:TriggersModule!
    @module         repositories/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def get_by_id(self, condition_id: uuid.UUID) -> Optional[IConditionState]:
        """Find trigger condition state record by provided database identifier"""


@inject(
    bind={
        "repository": IActionsStatesRepository,
    },
)
class ActionsStatesRepository(ABC):  # pylint: disable=too-few-public-methods
    """
    State repository for action

    @package        FastyBird:TriggersModule!
    @module         repositories/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __repository: Optional[IActionsStatesRepository] = None

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        repository: Optional[IActionsStatesRepository] = None,
    ) -> None:
        self.__repository = repository

    # -----------------------------------------------------------------------------

    def get_by_id(self, action_id: uuid.UUID) -> Optional[IActionState]:
        """Find trigger action state record by provided database identifier"""
        if self.__repository is None:
            raise NotImplementedError("Action states repository is not implemented")

        return self.__repository.get_by_id(action_id=action_id)


@inject(
    bind={
        "repository": IConditionsStatesRepository,
    },
)
class ConditionsStatesRepository(ABC):  # pylint: disable=too-few-public-methods
    """
    State repository for condition

    @package        FastyBird:TriggersModule!
    @module         repositories/state

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __repository: Optional[IConditionsStatesRepository] = None

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        repository: Optional[IConditionsStatesRepository] = None,
    ) -> None:
        self.__repository = repository

    # -----------------------------------------------------------------------------

    def get_by_id(self, condition_id: uuid.UUID) -> Optional[IConditionState]:
        """Find trigger condition state record by provided database identifier"""
        if self.__repository is None:
            raise NotImplementedError("Condition states repository is not implemented")

        return self.__repository.get_by_id(condition_id=condition_id)
