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
Triggers module trigger entities module
"""

# Python base dependencies
import uuid
from abc import abstractmethod
from typing import Dict, List, Optional, Union

# Library dependencies
from fastybird_metadata.triggers_module import TriggerType
from sqlalchemy import (
    BINARY,
    BOOLEAN,
    JSON,
    TEXT,
    VARCHAR,
    Column,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

# Library libs
from fastybird_triggers_module.entities.action import ActionEntity
from fastybird_triggers_module.entities.base import (
    Base,
    EntityCreatedMixin,
    EntityUpdatedMixin,
)
from fastybird_triggers_module.entities.condition import ConditionEntity
from fastybird_triggers_module.entities.notification import NotificationEntity


class TriggerEntity(EntityCreatedMixin, EntityUpdatedMixin, Base):
    """
    Trigger entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __tablename__: str = "fb_triggers_module_triggers"

    __table_args__ = (
        Index("trigger_name_idx", "trigger_name"),
        Index("trigger_enabled_idx", "trigger_enabled"),
        {
            "mysql_engine": "InnoDB",
            "mysql_collate": "utf8mb4_general_ci",
            "mysql_charset": "utf8mb4",
            "mysql_comment": "Triggers",
        },
    )

    col_type: str = Column(VARCHAR(40), name="trigger_type", nullable=False)  # type: ignore[assignment]

    col_trigger_id: bytes = Column(  # type: ignore[assignment]
        BINARY(16), primary_key=True, name="trigger_id", default=uuid.uuid4
    )
    col_name: str = Column(VARCHAR(255), name="trigger_name", nullable=False)  # type: ignore[assignment]
    col_comment: Optional[str] = Column(  # type: ignore[assignment]
        TEXT, name="trigger_comment", nullable=True, default=None
    )
    col_enabled: bool = Column(
        BOOLEAN, name="trigger_enabled", nullable=False, default=True  # type: ignore[assignment]
    )

    col_owner: Optional[str] = Column(  # type: ignore[assignment]
        VARCHAR(50), name="owner", nullable=True, default=None
    )

    col_params: Optional[Dict] = Column(JSON, name="params", nullable=True)  # type: ignore[assignment]

    actions: List[ActionEntity] = relationship(  # type: ignore[assignment]
        ActionEntity,
        back_populates="trigger",
        cascade="delete, delete-orphan",
    )
    notifications: List[NotificationEntity] = relationship(  # type: ignore[assignment]
        NotificationEntity,
        back_populates="trigger",
        cascade="delete, delete-orphan",
    )
    controls: List["TriggerControlEntity"] = relationship(  # type: ignore[assignment]
        "TriggerControlEntity",
        back_populates="trigger",
        cascade="delete, delete-orphan",
    )

    __mapper_args__ = {
        "polymorphic_identity": "trigger",
        "polymorphic_on": col_type,
    }

    # -----------------------------------------------------------------------------

    def __init__(self, name: str, trigger_id: Optional[uuid.UUID] = None) -> None:
        super().__init__()

        self.col_trigger_id = trigger_id.bytes if trigger_id is not None else uuid.uuid4().bytes

        self.col_name = name

    # -----------------------------------------------------------------------------

    @property
    @abstractmethod
    def type(self) -> TriggerType:
        """Trigger type"""

    # -----------------------------------------------------------------------------

    @property
    def id(self) -> uuid.UUID:  # pylint: disable=invalid-name
        """Trigger unique identifier"""
        return uuid.UUID(bytes=self.col_trigger_id)

    # -----------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Trigger name"""
        return self.col_name

    # -----------------------------------------------------------------------------

    @name.setter
    def name(self, name: str) -> None:
        """Trigger name setter"""
        self.col_name = name

    # -----------------------------------------------------------------------------

    @property
    def comment(self) -> Optional[str]:
        """Trigger comment"""
        return self.col_comment

    # -----------------------------------------------------------------------------

    @comment.setter
    def comment(self, comment: Optional[str]) -> None:
        """Trigger comment setter"""
        self.col_comment = comment

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Trigger enabled status"""
        return self.col_enabled

    # -----------------------------------------------------------------------------

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        """Trigger enabled setter"""
        self.col_enabled = enabled

    # -----------------------------------------------------------------------------

    @property
    def owner(self) -> Optional[str]:
        """Trigger owner identifier"""
        return self.col_owner

    # -----------------------------------------------------------------------------

    @owner.setter
    def owner(self, owner: Optional[str]) -> None:
        """Trigger owner identifier setter"""
        self.col_owner = owner

    # -----------------------------------------------------------------------------

    @property
    def params(self) -> Dict:
        """Trigger params"""
        return self.col_params if self.col_params is not None else {}

    # -----------------------------------------------------------------------------

    @params.setter
    def params(self, params: Optional[Dict]) -> None:
        """Trigger params"""
        self.col_params = params

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, bool, None]]:
        """Transform entity to dictionary"""
        return {
            "id": self.id.__str__(),
            "type": self.type.value,
            "name": self.name,
            "comment": self.comment,
            "enabled": self.enabled,
            "owner": self.owner,
        }


class AutomaticTriggerEntity(TriggerEntity):
    """
    Automatic trigger entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "automatic"}

    conditions: List[ConditionEntity] = relationship(  # type: ignore[assignment]
        ConditionEntity,
        back_populates="trigger",
        cascade="delete, delete-orphan",
    )

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> TriggerType:
        """Trigger type"""
        return TriggerType.AUTOMATIC


class ManualTriggerEntity(TriggerEntity):
    """
    Manual trigger entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": "manual"}

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> TriggerType:
        """Trigger type"""
        return TriggerType.MANUAL


class TriggerControlEntity(EntityCreatedMixin, EntityUpdatedMixin, Base):
    """
    Trigger control entity

    @package        FastyBird:TriggersModule!
    @module         entities/trigger

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __tablename__: str = "fb_triggers_module_triggers_controls"

    __table_args__ = (
        Index("control_name_idx", "control_name"),
        UniqueConstraint("control_name", "trigger_id", name="control_name_unique"),
        {
            "mysql_engine": "InnoDB",
            "mysql_collate": "utf8mb4_general_ci",
            "mysql_charset": "utf8mb4",
            "mysql_comment": "Triggers controls",
        },
    )

    col_control_id: bytes = Column(  # type: ignore[assignment]
        BINARY(16), primary_key=True, name="control_id", default=uuid.uuid4
    )
    col_name: str = Column(VARCHAR(100), name="control_name", nullable=False)  # type: ignore[assignment]

    col_trigger_id: bytes = Column(  # type: ignore[assignment]  # pylint: disable=unused-private-member
        BINARY(16),
        ForeignKey("fb_triggers_module_triggers.trigger_id", ondelete="CASCADE"),
        name="trigger_id",
        nullable=False,
    )

    trigger: TriggerEntity = relationship(TriggerEntity, back_populates="controls")  # type: ignore[assignment]

    # -----------------------------------------------------------------------------

    def __init__(self, name: str, trigger: TriggerEntity, control_id: Optional[uuid.UUID] = None) -> None:
        super().__init__()

        self.col_control_id = control_id.bytes if control_id is not None else uuid.uuid4().bytes

        self.col_name = name

        self.trigger = trigger

    # -----------------------------------------------------------------------------

    @property
    def id(self) -> uuid.UUID:  # pylint: disable=invalid-name
        """Control unique identifier"""
        return uuid.UUID(bytes=self.col_control_id)

    # -----------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Control name"""
        return self.col_name

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "id": self.id.__str__(),
                "name": self.name,
                "trigger": self.trigger.id.__str__(),
                "owner": self.trigger.owner,
            },
        }
