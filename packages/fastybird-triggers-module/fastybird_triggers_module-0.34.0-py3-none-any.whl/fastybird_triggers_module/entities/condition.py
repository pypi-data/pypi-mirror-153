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
Triggers module condition entities module
"""

# Python base dependencies
import datetime
import uuid
from abc import abstractmethod
from typing import Dict, List, Optional, Union

# Library dependencies
from fastybird_metadata.triggers_module import ConditionOperator, ConditionType
from fastybird_metadata.types import ButtonPayload, SwitchPayload
from sqlalchemy import BINARY, BOOLEAN, DATE, TEXT, TIME, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

# Library libs
import fastybird_triggers_module.entities  # pylint: disable=unused-import
from fastybird_triggers_module.entities.base import (
    Base,
    EntityCreatedMixin,
    EntityUpdatedMixin,
)
from fastybird_triggers_module.exceptions import InvalidStateException


class ConditionEntity(EntityCreatedMixin, EntityUpdatedMixin, Base):
    """
    Condition entity

    @package        FastyBird:TriggersModule!
    @module         entities/condition

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __tablename__: str = "fb_triggers_module_conditions"

    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_charset": "utf8mb4",
        "mysql_comment": "Trigger conditions",
    }

    col_type: str = Column(VARCHAR(40), name="condition_type", nullable=False)  # type: ignore[assignment]

    col_condition_id: bytes = Column(  # type: ignore[assignment]
        BINARY(16), primary_key=True, name="condition_id", default=uuid.uuid4
    )
    col_enabled: bool = Column(  # type: ignore[assignment]
        BOOLEAN, name="condition_enabled", nullable=False, default=True
    )

    trigger_id: Optional[bytes] = Column(  # type: ignore[assignment]  # pylint: disable=unused-private-member
        BINARY(16),
        ForeignKey("fb_triggers_module_triggers.trigger_id", ondelete="CASCADE"),
        name="trigger_id",
        nullable=False,
    )

    trigger: "entities.trigger.AutomaticTriggerEntity" = relationship(  # type: ignore[name-defined]
        "entities.trigger.AutomaticTriggerEntity",
        back_populates="conditions",
    )

    col_device: Optional[bytes] = Column(BINARY(16), name="condition_device", nullable=True)  # type: ignore[assignment]
    col_device_property: Optional[bytes] = Column(  # type: ignore[assignment]
        BINARY(16), name="condition_device_property", nullable=True
    )
    col_channel: Optional[bytes] = Column(  # type: ignore[assignment]
        BINARY(16), name="condition_channel", nullable=True
    )
    col_channel_property: Optional[bytes] = Column(  # type: ignore[assignment]
        BINARY(16), name="condition_channel_property", nullable=True
    )
    col_operator: Optional[str] = Column(  # type: ignore[assignment]
        VARCHAR(15), name="condition_operator", nullable=True
    )
    col_operand: Optional[str] = Column(  # type: ignore[assignment]
        VARCHAR(20), name="condition_operand", nullable=True
    )
    col_date: Optional[datetime.date] = Column(DATE, name="condition_date", nullable=True)  # type: ignore[assignment]
    col_time: Optional[datetime.time] = Column(TIME, name="condition_time", nullable=True)  # type: ignore[assignment]
    col_days: Optional[str] = Column(TEXT, name="condition_days", nullable=True)  # type: ignore[assignment]

    __mapper_args__ = {
        "polymorphic_identity": "condition",
        "polymorphic_on": col_type,
    }

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        trigger: "entities.trigger.AutomaticTriggerEntity",  # type: ignore[name-defined]
        condition_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__()

        self.col_condition_id = condition_id.bytes if condition_id is not None else uuid.uuid4().bytes

        self.trigger = trigger

    # -----------------------------------------------------------------------------

    @property
    @abstractmethod
    def type(self) -> ConditionType:
        """Trigger condition type"""

    # -----------------------------------------------------------------------------

    @property
    def id(self) -> uuid.UUID:  # pylint: disable=invalid-name
        """Condition unique identifier"""
        return uuid.UUID(bytes=self.col_condition_id)

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Condition enabled status"""
        return self.col_enabled

    # -----------------------------------------------------------------------------

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        """Condition enabled setter"""
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


class DevicePropertyConditionEntity(ConditionEntity):
    """
    Device property condition entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "device-property"}

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments
        self,
        device: uuid.UUID,
        condition_property: uuid.UUID,
        operator: ConditionOperator,
        operand: str,
        trigger: "entities.trigger.AutomaticTriggerEntity",  # type: ignore[name-defined]
        condition_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__(trigger, condition_id)

        self.col_device = device.bytes
        self.col_device_property = condition_property.bytes
        self.col_operator = operator.value
        self.col_operand = operand

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> ConditionType:
        """Condition type"""
        return ConditionType.DEVICE_PROPERTY

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Condition device database identifier"""
        if self.col_device is None:
            raise InvalidStateException("Device identifier is missing on condition instance")

        return uuid.UUID(bytes=self.col_device)

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Condition property database identifier"""
        if self.col_device_property is None:
            raise InvalidStateException("Property identifier is missing on condition instance")

        return uuid.UUID(bytes=self.col_device_property)

    # -----------------------------------------------------------------------------

    @property
    def operator(self) -> ConditionOperator:
        """Condition operator"""
        if self.col_operator is None:
            raise InvalidStateException("Condition operator is missing on condition instance")

        return ConditionOperator(self.col_operator)

    # -----------------------------------------------------------------------------

    @operator.setter
    def operator(self, operator: ConditionOperator) -> None:
        """Condition operator setter"""
        self.col_operator = operator.value

    # -----------------------------------------------------------------------------

    @property
    def operand(self) -> Union[str, ButtonPayload, SwitchPayload]:
        """Condition operand"""
        if self.col_operand is None:
            raise InvalidStateException("Condition operand is missing on condition instance")

        if ButtonPayload.has_value(self.col_operand):
            return ButtonPayload(self.col_operand)

        if SwitchPayload.has_value(self.col_operand):
            return SwitchPayload(self.col_operand)

        return self.col_operand

    # -----------------------------------------------------------------------------

    @operand.setter
    def operand(self, operand: str) -> None:
        """Condition operand setter"""
        self.col_operand = operand

    # -----------------------------------------------------------------------------

    def validate(self, value: str) -> bool:
        """Validate provided value with condition"""
        if self.operator == ConditionOperator.EQUAL:
            return str(self.operand) == value

        if self.operator == ConditionOperator.ABOVE:
            return float(str(self.operand)) < float(value)

        if self.operator == ConditionOperator.BELOW:
            return float(str(self.operand)) > float(value)

        return False

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "device": self.device.__str__(),
                "property": self.device_property.__str__(),
                "operator": self.operator.value,
                "operand": str(self.operand),
            },
        }


class ChannelPropertyConditionEntity(ConditionEntity):
    """
    Channel property condition entity

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
        condition_property: uuid.UUID,
        operator: ConditionOperator,
        operand: str,
        trigger: "entities.trigger.AutomaticTriggerEntity",  # type: ignore[name-defined]
        condition_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__(trigger, condition_id)

        self.col_device = device.bytes
        self.col_channel = channel.bytes
        self.col_channel_property = condition_property.bytes
        self.col_operator = operator.value
        self.col_operand = operand

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> ConditionType:
        """Condition type"""
        return ConditionType.CHANNEL_PROPERTY

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Condition device database identifier"""
        if self.col_device is None:
            raise InvalidStateException("Device identifier is missing on condition instance")

        return uuid.UUID(bytes=self.col_device)

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Condition channel database identifier"""
        if self.col_channel is None:
            raise InvalidStateException("Channel identifier is missing on condition instance")

        return uuid.UUID(bytes=self.col_channel)

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Condition property database identifier"""
        if self.col_channel_property is None:
            raise InvalidStateException("Property identifier is missing on condition instance")

        return uuid.UUID(bytes=self.col_channel_property)

    # -----------------------------------------------------------------------------

    @property
    def operator(self) -> ConditionOperator:
        """Condition operator"""
        if self.col_operator is None:
            raise InvalidStateException("Condition operator is missing on condition instance")

        return ConditionOperator(self.col_operator)

    # -----------------------------------------------------------------------------

    @operator.setter
    def operator(self, operator: ConditionOperator) -> None:
        """Condition operator setter"""
        self.col_operator = operator.value

    # -----------------------------------------------------------------------------

    @property
    def operand(self) -> Union[str, ButtonPayload, SwitchPayload]:
        """Condition operand"""
        if self.col_operand is None:
            raise InvalidStateException("Condition operand is missing on condition instance")

        if ButtonPayload.has_value(self.col_operand):
            return ButtonPayload(self.col_operand)

        if SwitchPayload.has_value(self.col_operand):
            return SwitchPayload(self.col_operand)

        return self.col_operand

    # -----------------------------------------------------------------------------

    @operand.setter
    def operand(self, operand: str) -> None:
        """Condition operand setter"""
        self.col_operand = operand

    # -----------------------------------------------------------------------------

    def validate(self, value: str) -> bool:
        """Validate provided value with condition"""
        if self.operator == ConditionOperator.EQUAL:
            return str(self.operand) == value

        if self.operator == ConditionOperator.ABOVE:
            return float(str(self.operand)) < float(value)

        if self.operator == ConditionOperator.BELOW:
            return float(str(self.operand)) > float(value)

        return False

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "device": self.device.__str__(),
                "channel": self.channel.__str__(),
                "property": self.channel_property.__str__(),
                "operator": self.operator.value,
                "operand": str(self.operand),
            },
        }


class DateConditionEntity(ConditionEntity):
    """
    Date condition entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "date"}

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        date: datetime.datetime,
        trigger: "entities.trigger.AutomaticTriggerEntity",  # type: ignore[name-defined]
        condition_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__(trigger, condition_id)

        self.col_date = date.date()

    # -----------------------------------------------------------------------------

    @property
    @abstractmethod
    def type(self) -> ConditionType:
        """Trigger condition type"""
        return ConditionType.DATE

    # -----------------------------------------------------------------------------

    @property
    def date(self) -> datetime.date:
        """Condition date"""
        if self.col_date is None:
            raise InvalidStateException("Date is missing on condition instance")

        return self.col_date

    # -----------------------------------------------------------------------------

    @date.setter
    def date(self, date: datetime.datetime) -> None:
        """Condition date setter"""
        self.col_date = date.date()

    # -----------------------------------------------------------------------------

    def validate(self, value: datetime.datetime) -> bool:
        """Validate provided value with condition"""
        return self.date == value.date()

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "date": self.date.strftime(r"%Y-%m-%dT%H:%M:%S+00:00"),
            },
        }


class TimeConditionEntity(ConditionEntity):
    """
    Date condition entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "time"}

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        time: datetime.datetime,
        days: List[int],
        trigger: "entities.trigger.AutomaticTriggerEntity",  # type: ignore[name-defined]
        condition_id: Optional[uuid.UUID] = None,
    ) -> None:
        super().__init__(trigger, condition_id)

        self.col_time = time.time()
        self.col_days = ",".join([str(day) for day in days])

    # -----------------------------------------------------------------------------

    @property
    @abstractmethod
    def type(self) -> ConditionType:
        """Trigger condition type"""
        return ConditionType.TIME

    # -----------------------------------------------------------------------------

    @property
    def time(self) -> datetime.time:
        """Condition time"""
        if self.col_time is None:
            raise InvalidStateException("Time is missing on condition instance")

        return self.col_time

    # -----------------------------------------------------------------------------

    @time.setter
    def time(self, time: datetime.datetime) -> None:
        """Condition time setter"""
        self.col_time = time.time()

    # -----------------------------------------------------------------------------

    @property
    def days(self) -> List[int]:
        """Condition days"""
        if self.col_days is None:
            raise InvalidStateException("Days are missing on condition instance")

        return [int(day) for day in self.col_days.split(",")]

    # -----------------------------------------------------------------------------

    @days.setter
    def days(self, days: List[int]) -> None:
        """Condition days setter"""
        self.col_days = ",".join([str(day) for day in days])

    # -----------------------------------------------------------------------------

    def validate(self, time: datetime.datetime) -> bool:
        """Validate provided value with condition"""
        if time.isoweekday() not in self.days:
            return False

        return time.strftime("%H:%M:%S") == self.__format_time()

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, List[int], None]]:  # type: ignore[override]
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "time": f"1970-01-01\\T{self.__format_time()}+00:00",
                "days": self.days,
            },
        }

    # -----------------------------------------------------------------------------

    def __format_time(self) -> str:
        return f"{self.time.hour:02d}:{self.time.minute:02d}:{self.time.second:02d}"
