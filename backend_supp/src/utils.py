from enum import Enum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Equipment, Location, Fabric
from .schemas import EquipmentRead



class ObjectType(str, Enum):
    fabric = Fabric.__name__.lower()
    location = Location.__name__.lower()
    equipment = Equipment.__name__.lower()


def equipment_to_read(equipment: Equipment) -> EquipmentRead:
    return EquipmentRead(
        id=equipment.id,
        name=equipment.name,
        location_ids=[loc.id for loc in equipment.locations]
    )


async def get_tree(obj, session: AsyncSession):
    visited = set()
    result = {"parent": [], "children": []}

    if isinstance(obj, Equipment):
        await session.refresh(obj, ["locations"])

    elif isinstance(obj, Location):
        await session.refresh(obj, ["fabric"])

    async def recurse_parent(current):
        nonlocal visited
        if isinstance(current, Equipment):
            stmt = (
                select(Location)
                .where(Location.id.in_([loc.id for loc in current.locations]))
                .options(selectinload(Location.fabric))
            )
            locations = (await session.execute(stmt)).scalars().all()

            for loc in locations:
                if loc.id not in visited:
                    visited.add(loc.id)
                    result["parent"].append({"id": loc.id, "name": loc.name, "type": Location.__name__})
                    await recurse_parent(loc)

        elif isinstance(current, Location):
            if current.fabric and current.fabric.id not in visited:
                visited.add(current.fabric.id)
                result["parent"].append({"id": current.fabric.id, "name": current.fabric.name, "type": Fabric.__name__})

    async def recurse_children(current):
        nonlocal visited
        if isinstance(current, Fabric):
            stmt = (
                select(Location)
                .where(Location.fabric_id == current.id)
                .options(selectinload(Location.equipment))
            )
            locations = (await session.execute(stmt)).scalars().all()

            for loc in locations:
                if loc.id not in visited:
                    visited.add(loc.id)
                    result["children"].append({"id": loc.id, "name": loc.name, "type": Location.__name__})
                    await recurse_children(loc)

        elif isinstance(current, Location):
            stmt = (
                select(Equipment)
                .join(Location.equipment)
                .where(Location.id == current.id)
            )
            equipments = (await session.execute(stmt)).scalars().all()

            for eq in equipments:
                if eq.id not in visited:
                    visited.add(eq.id)
                    result["children"].append({"id": eq.id, "name": eq.name, "type": Equipment.__name__})

    await recurse_parent(obj)
    await recurse_children(obj)
    return result