from enum import Enum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Equipment, Location, Fabric



class ObjectType(str, Enum):
    fabric = Fabric.__name__.lower()
    location = Location.__name__.lower()
    equipment = Equipment.__name__.lower()


async def get_tree(obj, session: AsyncSession):
    parent_chain, children_list  = [], []

    if isinstance(obj, Equipment):
        stmt = (
            select(Equipment)
            .options(
                selectinload(Equipment.locations)
                .selectinload(Location.fabric)
            )
            .where(Equipment.id == obj.id)
        )
        result = await session.execute(stmt)
        obj = result.scalar_one()

        for location in obj.locations:
            parent_chain.append({
                "id": location.id,
                "type": "Location",
                "name": location.name
            })
            if location.fabric:
                parent_chain.append({
                    "id": location.fabric.id,
                    "type": "Fabric",
                    "name": location.fabric.name
                })

    elif isinstance(obj, Location):
        stmt = (
            select(Location)
            .options(
                selectinload(Location.fabric),
                selectinload(Location.equipment)
            )
            .where(Location.id == obj.id)
        )
        result = await session.execute(stmt)
        obj = result.scalar_one()

        if obj.fabric:
            parent_chain.append({
                "id": obj.fabric.id,
                "type": "Fabric",
                "name": obj.fabric.name
            })

        children_list = [{
            "id": eq.id,
            "type": "Equipment",
            "name": eq.name
        } for eq in obj.equipment]

    elif isinstance(obj, Fabric):
        stmt = (
            select(Fabric)
            .options(
                selectinload(Fabric.locations)
                .selectinload(Location.equipment)
            )
            .where(Fabric.id == obj.id)
        )
        result = await session.execute(stmt)
        obj = result.scalar_one()

        for loc in obj.locations:
            children_list.append({
                "id": loc.id,
                "type": "Location",
                "name": loc.name
            })

            for eq in loc.equipment:
                children_list.append({
                    "id": eq.id,
                    "type": "Equipment",
                    "name": eq.name
                })

    return {
        "parent": parent_chain,
        "children": children_list
    }