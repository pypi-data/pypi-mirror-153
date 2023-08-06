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
Triggers module action entities module
"""

# Python base dependencies
import uuid
from abc import abstractmethod
from typing import Dict, Optional, Union

# Library dependencies
from fastybird_metadata.triggers_module import ActionType
from fastybird_metadata.types import ButtonPayload, SwitchPayload
from sqlalchemy import BINARY, BOOLEAN, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

# Library libs
import fastybird_triggers_module.entities  # pylint: disable=unused-import
from fastybird_triggers_module.entities.base import (
    Base,
    EntityCreatedMixin,
    EntityUpdatedMixin,
)
from fastybird_triggers_module.exceptions import InvalidStateException


class ActionEntity(EntityCreatedMixin, EntityUpdatedMixin, Base):
    """
    Action entity

    @package        FastyBird:TriggersModule!
    @module         entities/action

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __tablename__: str = "fb_triggers_module_actions"

    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_charset": "utf8mb4",
        "mysql_comment": "Trigger actions",
    }

    col_type: str = Column(VARCHAR(40), name="action_type", nullable=False)  # type: ignore[assignment]

    col_action_id: bytes = Column(  # type: ignore[assignment]
        BINARY(16), primary_key=True, name="action_id", default=uuid.uuid4
    )
    col_enabled: bool = Column(BOOLEAN, name="action_enabled", nullable=False, default=True)  # type: ignore[assignment]

    trigger_id: Optional[bytes] = Column(  # type: ignore[assignment]  # pylint: disable=unused-private-member
        BINARY(16),
        ForeignKey("fb_triggers_module_triggers.trigger_id", ondelete="CASCADE"),
        name="trigger_id",
        nullable=False,
    )

    trigger: "entities.trigger.TriggerEntity" = relationship(  # type: ignore[name-defined]
        "entities.trigger.TriggerEntity",
        back_populates="actions",
    )

    col_value: Optional[str] = Column(  # type: ignore[assignment]
        VARCHAR(100), name="action_value", nullable=False, default=True
    )
    col_device: Optional[bytes] = Column(BINARY(16), name="action_device", nullable=True)  # type: ignore[assignment]
    col_device_property: Optional[bytes] = Column(  # type: ignore[assignment]
        BINARY(16), name="action_device_property", nullable=True
    )
    col_channel: Optional[bytes] = Column(BINARY(16), name="action_channel", nullable=True)  # type: ignore[assignment]
    col_channel_property: Optional[bytes] = Column(  # type: ignore[assignment]
        BINARY(16), name="action_channel_property", nullable=True
    )

    __mapper_args__ = {
        "polymorphic_identity": "action",
        "polymorphic_on": col_type,
    }

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        trigger: "entities.trigger.TriggerEntity",  # type: ignore[name-defined]
        action_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__()

        self.col_action_id = action_id.bytes if action_id is not None else uuid.uuid4().bytes

        self.trigger = trigger

    # -----------------------------------------------------------------------------

    @property
    @abstractmethod
    def type(self) -> ActionType:
        """Trigger action type"""

    # -----------------------------------------------------------------------------

    @property
    def id(self) -> uuid.UUID:  # pylint: disable=invalid-name
        """Action unique identifier"""
        return uuid.UUID(bytes=self.col_action_id)

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Action enabled status"""
        return self.col_enabled

    # -----------------------------------------------------------------------------

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        """Action enabled setter"""
        self.col_enabled = enabled

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "id": self.id.__str__(),
                "type": self.type.value,
                "enabled": self.enabled,
                "trigger": self.trigger.id.__str__(),
                "owner": self.trigger.owner,
            },
        }


class DevicePropertyActionEntity(ActionEntity):
    """
    Device property action entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "device-property"}

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments
        self,
        device: uuid.UUID,
        device_property: uuid.UUID,
        value: str,
        trigger: "entities.trigger.TriggerEntity",  # type: ignore[name-defined]
        action_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__(trigger, action_id)

        self.col_device = device.bytes
        self.col_device_property = device_property.bytes
        self.col_value = value

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> ActionType:
        """Action type"""
        return ActionType.DEVICE_PROPERTY

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Action device database identifier"""
        if self.col_device is None:
            raise InvalidStateException("Device identifier is missing on action instance")

        return uuid.UUID(bytes=self.col_device)

    # -----------------------------------------------------------------------------

    @property
    def value(self) -> Union[str, ButtonPayload, SwitchPayload]:
        """Action value"""
        if self.col_value is None:
            raise InvalidStateException("Action value is missing on action instance")

        if ButtonPayload.has_value(self.col_value):
            return ButtonPayload(self.col_value)

        if SwitchPayload.has_value(self.col_value):
            return SwitchPayload(self.col_value)

        return self.col_value

    # -----------------------------------------------------------------------------

    @value.setter
    def value(self, value: str) -> None:
        """Action value setter"""
        self.col_value = value

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Action property database identifier"""
        if self.col_device_property is None:
            raise InvalidStateException("Property identifier is missing on action instance")

        return uuid.UUID(bytes=self.col_device_property)

    # -----------------------------------------------------------------------------

    def validate(self, value: str) -> bool:
        """Validate provided value with action"""
        return str(self.value) == value

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "device": self.device.__str__(),
                "property": self.device_property.__str__(),
                "value": str(self.value),
            },
        }


class ChannelPropertyActionEntity(ActionEntity):
    """
    Channel property action entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "channel-property"}

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments
        self,
        device: uuid.UUID,
        channel: uuid.UUID,
        channel_property: uuid.UUID,
        value: str,
        trigger: "entities.trigger.TriggerEntity",  # type: ignore[name-defined]
        action_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__(trigger, action_id)

        self.col_device = device.bytes
        self.col_channel = channel.bytes
        self.col_channel_property = channel_property.bytes
        self.col_value = value

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> ActionType:
        """Action type"""
        return ActionType.CHANNEL_PROPERTY

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Action device database identifier"""
        if self.col_device is None:
            raise InvalidStateException("Device identifier is missing on action instance")

        return uuid.UUID(bytes=self.col_device)

    # -----------------------------------------------------------------------------

    @property
    def value(self) -> Union[str, ButtonPayload, SwitchPayload]:
        """Action value"""
        if self.col_value is None:
            raise InvalidStateException("Action value is missing on action instance")

        if ButtonPayload.has_value(self.col_value):
            return ButtonPayload(self.col_value)

        if SwitchPayload.has_value(self.col_value):
            return SwitchPayload(self.col_value)

        return self.col_value

    # -----------------------------------------------------------------------------

    @value.setter
    def value(self, value: str) -> None:
        """Action value setter"""
        self.col_value = value

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Action channel database identifier"""
        if self.col_channel is None:
            raise InvalidStateException("Channel identifier is missing on action instance")

        return uuid.UUID(bytes=self.col_channel)

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Action property database identifier"""
        if self.col_channel_property is None:
            raise InvalidStateException("Property identifier is missing on action instance")

        return uuid.UUID(bytes=self.col_channel_property)

    # -----------------------------------------------------------------------------

    def validate(self, value: str) -> bool:
        """Validate provided value with action"""
        return str(self.value) == value

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "device": self.device.__str__(),
                "channel": self.channel.__str__(),
                "property": self.channel_property.__str__(),
                "value": str(self.value),
            },
        }
