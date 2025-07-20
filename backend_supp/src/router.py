import logging
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import Equipment, Location, Fabric
from .orm import FabricORM, LocationORM, EquipmentORM
from .schemas import (
    EquipmentRead, EquipmentCreate, FabricCreate, FabricRead, LocationRead, LocationCreate, TreeResponse, TreeNode
)
from .utils import equipment_to_read, ObjectType, get_tree

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.post("/fabrics/", response_model=FabricRead)
async def create_fabric(fabric: FabricCreate, session: AsyncSession = Depends(get_async_session)):
    orm = FabricORM(session)
    return await orm.create_fabric(fabric)


@router.post("/locations/", response_model=LocationRead)
async def create_location(location: LocationCreate, session: AsyncSession = Depends(get_async_session)):
    orm = LocationORM(session)
    return await orm.create_location(location)



@router.post("/equipment/", response_model=EquipmentRead)
async def create_equipment(equipment: EquipmentCreate, session: AsyncSession = Depends(get_async_session)):
    service = EquipmentORM(session)
    new_equipment = await service.create(equipment)
    await session.refresh(new_equipment, attribute_names=["locations"])
    return equipment_to_read(new_equipment)


@router.get("/tree/{object_type}/{object_id}", response_model=TreeResponse)
async def get_tree_view(
    object_type: ObjectType,
    object_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    obj = None
    if object_type == ObjectType.fabric:
        obj = await session.get(Fabric, object_id)
    elif object_type == ObjectType.location:
        obj = await session.get(Location, object_id)
    elif object_type == ObjectType.equipment:
        obj = await session.get(Equipment, object_id)

    if not obj:
        raise HTTPException(404, "Object not found")

    tree_raw = await get_tree(obj, session)

    return TreeResponse(
        object={"id": obj.id, "type": object_type.value.capitalize()},
        tree={
            "parent": [TreeNode(**node) for node in tree_raw["parent"]],
            "children": [TreeNode(**node) for node in tree_raw["children"]],
        }
    )
