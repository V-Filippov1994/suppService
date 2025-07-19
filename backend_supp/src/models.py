from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import BaseModel, BaseM2M


class Fabric(BaseModel):

    locations: Mapped[list["Location"]] = relationship(
        back_populates="fabric",
        cascade="all, delete-orphan"
    )


class Location(BaseModel):
    fabric_id: Mapped[int] = mapped_column(
        ForeignKey("fabric.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    fabric: Mapped[Fabric] = relationship(
        back_populates="locations",
        lazy="joined"
    )

    equipment: Mapped[list["Equipment"]] = relationship(
        back_populates="locations",
        secondary="location_equipment",
    )


class Equipment(BaseModel):
    locations: Mapped[list["Location"]] = relationship(
        back_populates="equipment",
        secondary="location_equipment",
    )


class LocationEquipment(BaseM2M):
    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

