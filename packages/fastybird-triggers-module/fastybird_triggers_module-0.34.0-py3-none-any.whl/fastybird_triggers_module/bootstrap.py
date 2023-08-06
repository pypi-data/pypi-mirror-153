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
Triggers module DI container
"""

# pylint: disable=no-value-for-parameter

# Python base dependencies
import logging

# Library dependencies
from fastybird_exchange.consumer import Consumer
from kink import di
from sqlalchemy.orm import Session as OrmSession

# Library libs
from fastybird_triggers_module.automation.automation import Automator
from fastybird_triggers_module.automation.consumer import AutomationConsumer
from fastybird_triggers_module.automation.queue import AutomationQueue
from fastybird_triggers_module.logger import Logger
from fastybird_triggers_module.managers.action import ActionsManager
from fastybird_triggers_module.managers.condition import ConditionsManager
from fastybird_triggers_module.managers.notification import NotificationsManager
from fastybird_triggers_module.managers.state import (
    ActionsStatesManager,
    ConditionsStatesManager,
)
from fastybird_triggers_module.managers.trigger import (
    TriggerControlsManager,
    TriggersManager,
)
from fastybird_triggers_module.repositories.action import ActionsRepository
from fastybird_triggers_module.repositories.condition import ConditionsRepository
from fastybird_triggers_module.repositories.notification import NotificationsRepository
from fastybird_triggers_module.repositories.state import (
    ActionsStatesRepository,
    ConditionsStatesRepository,
)
from fastybird_triggers_module.repositories.trigger import (
    TriggerControlsRepository,
    TriggersRepository,
)
from fastybird_triggers_module.subscriber import (
    EntitiesSubscriber,
    EntityCreatedSubscriber,
)


def register_services(
    logger: logging.Logger = logging.getLogger("dummy"),
) -> None:
    """Register triggers module services"""
    if OrmSession not in di:
        logger.error("SQLAlchemy database session is not registered in container!")

        return

    di[Logger] = Logger(logger=logger)
    di["fb-triggers-module_logger"] = di[Logger]

    # Entities repositories

    di[TriggersRepository] = TriggersRepository(session=di[OrmSession])
    di["fb-triggers-module_trigger-repository"] = di[TriggersRepository]
    di[TriggerControlsRepository] = TriggerControlsRepository(session=di[OrmSession])
    di["fb-triggers-module_trigger-control-repository"] = di[TriggerControlsRepository]
    di[ActionsRepository] = ActionsRepository(session=di[OrmSession])
    di["fb-triggers-module_action-repository"] = di[ActionsRepository]
    di[ConditionsRepository] = ConditionsRepository(session=di[OrmSession])
    di["fb-triggers-module_condition-repository"] = di[ConditionsRepository]
    di[NotificationsRepository] = NotificationsRepository(session=di[OrmSession])
    di["fb-triggers-module_notification-repository"] = di[NotificationsRepository]

    # States repositories

    di[ActionsStatesRepository] = ActionsStatesRepository()
    di["fb-triggers-module_actions-states-repository"] = di[ActionsStatesRepository]
    di[ConditionsStatesRepository] = ConditionsStatesRepository()
    di["fb-triggers-module_conditions-states-repository"] = di[ConditionsStatesRepository]

    # Entities managers

    di[TriggersManager] = TriggersManager(session=di[OrmSession])
    di["fb-triggers-module_triggers-manager"] = di[TriggersManager]
    di[TriggerControlsManager] = TriggerControlsManager(session=di[OrmSession])
    di["fb-triggers-module_trigger-controls-manager"] = di[TriggerControlsManager]
    di[ActionsManager] = ActionsManager(session=di[OrmSession])
    di["fb-triggers-module_actions-manager"] = di[ActionsManager]
    di[ConditionsManager] = ConditionsManager(session=di[OrmSession])
    di["fb-triggers-module_conditions-manager"] = di[ConditionsManager]
    di[NotificationsManager] = NotificationsManager(session=di[OrmSession])
    di["fb-triggers-module_notifications-manager"] = di[NotificationsManager]

    # States managers

    di[ActionsStatesManager] = ActionsStatesManager()
    di["fb-triggers-module_actions-states-manager"] = di[ActionsStatesManager]
    di[ConditionsStatesManager] = ConditionsStatesManager()
    di["fb-triggers-module_conditions-states-manager"] = di[ConditionsStatesManager]

    # Entities subscribers

    di[EntitiesSubscriber] = EntitiesSubscriber(
        action_state_repository=di[ActionsStatesRepository],
        condition_state_repository=di[ConditionsStatesRepository],
        session=di[OrmSession],
    )
    di["fb-triggers-module_entities-subscriber"] = di[EntitiesSubscriber]
    di[EntityCreatedSubscriber] = EntityCreatedSubscriber()
    di["fb-triggers-module_entity-created-subscriber"] = di[EntityCreatedSubscriber]

    # Module automator

    di[AutomationQueue] = AutomationQueue(logger=di[Logger])
    di["fb-triggers-module_automator-queue"] = di[AutomationQueue]
    di[AutomationConsumer] = AutomationConsumer(queue=di[AutomationQueue], logger=di[Logger])
    di["fb-triggers-module_automator-consumer"] = di[AutomationConsumer]

    di[Automator] = Automator(
        queue=di[AutomationQueue],
        triggers_repository=di[TriggersRepository],
        triggers_control_repository=di[TriggerControlsRepository],
        actions_repository=di[ActionsRepository],
        actions_states_manager=di[ActionsStatesRepository],
        actions_states_repository=di[ActionsStatesRepository],
        conditions_repository=di[ConditionsRepository],
        conditions_states_repository=di[ConditionsStatesRepository],
        conditions_states_manager=di[ConditionsStatesManager],
        logger=di[Logger],
    )
    di["fb-triggers-module_automator-handler"] = di[Automator]

    # Check for presence of exchange consumer proxy
    if Consumer in di:
        # Register automator exchange consumer into consumer proxy
        di[Consumer].register_consumer(di[AutomationConsumer])
