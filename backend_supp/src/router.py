import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import Equipment, Location, Fabric
from .orm import FabricORM, LocationORM, EquipmentORM
from .schemas import (
    EquipmentRead, EquipmentCreate, FabricCreate, FabricRead, LocationRead, LocationCreate, TreeResponse, TreeNode
)
from .utils import ObjectType, get_tree

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.post("/fabrics/", response_model=FabricRead)
async def create_fabric(fabric: FabricCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = select(exists().where(Fabric.name == fabric.name))
    result = await session.execute(stmt)
    is_fabric_exist = result.scalar()

    if is_fabric_exist:
        raise HTTPException(status_code=400, detail={'error': 'Фабрика с таким названием уже существует'})

    orm = FabricORM(session)
    return await orm.create_fabric(fabric)


@router.post("/locations/", response_model=LocationRead)
async def create_location(location: LocationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = select(exists().where(Location.name == location.name))
    result = await session.execute(stmt)
    is_location_exist = result.scalar()

    if is_location_exist:
        raise HTTPException(status_code=400, detail={'error': 'Участок с таким названием уже существует'})

    orm = LocationORM(session)
    return await orm.create_location(location)


@router.post("/equipment/", response_model=EquipmentRead)
async def create_equipment(equipment: EquipmentCreate, session: AsyncSession = Depends(get_async_session)):
    service = EquipmentORM(session)
    new_equipment = await service.create(equipment)
    await session.refresh(new_equipment, attribute_names=["locations"])
    return new_equipment


@router.get("/fabrics-all/", response_model=List[FabricRead])
async def get_fabrics(session: AsyncSession = Depends(get_async_session)):
    orm = FabricORM(session)
    return await orm.get_objects_all(Fabric)


@router.get("/locations-all/", response_model=List[LocationRead])
async def get_locations(session: AsyncSession = Depends(get_async_session)):
    orm = LocationORM(session)
    return await orm.get_objects_all(Location)


@router.get("/equipments-all/", response_model=List[EquipmentRead])
async def get_equipments(session: AsyncSession = Depends(get_async_session)):
    orm = EquipmentORM(session)
    return await orm.get_objects_all(Equipment)


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
