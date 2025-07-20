from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import BaseModel, BaseM2M


class Fabric(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    locations: Mapped[list["Location"]] = relationship(
        "Location",
        back_populates="fabric",
        cascade="all, delete-orphan"
    )


class Location(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    fabric_id: Mapped[int] = mapped_column(
        ForeignKey("fabric.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    fabric: Mapped[Fabric] = relationship(
        "Fabric",
        back_populates="locations",
        lazy="joined"
    )

    equipment: Mapped[list["Equipment"]] = relationship(
        "Equipment",
        back_populates="locations",
        secondary="locationequipment",
    )


class Equipment(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    locations: Mapped[list["Location"]] = relationship(
        "Location",
        back_populates="equipment",
        secondary="locationequipment",
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

