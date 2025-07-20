from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Fabric, Location, Equipment
from .schemas import FabricCreate, LocationCreate, EquipmentCreate


class BaseORM:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit_obj(self, new_obj: object) -> object:
        try:
            await self.session.commit()
            await self.session.refresh(new_obj)
        except Exception as e:
            await self.session.rollback()
            raise e


class FabricORM(BaseORM):
    async def create_fabric(self, fabric_data: FabricCreate) -> Fabric:
        new_fabric = Fabric(name=fabric_data.name)
        self.session.add(new_fabric)
        await self.commit_obj(new_fabric)
        return new_fabric


class LocationORM(BaseORM):
    async def create_location(self, location_data: LocationCreate) -> Location:
        new_location = Location(name=location_data.name, fabric_id=location_data.fabric_id)
        self.session.add(new_location)
        await self.commit_obj(new_location)
        return new_location


class EquipmentORM(BaseORM):
    async def create(self, data: EquipmentCreate) -> Equipment:
        stmt = select(Location).where(Location.id.in_(data.location_ids))
        result = await self.session.execute(stmt)
        locations = result.scalars().all()
        new_equipment = Equipment(name=data.name, locations=list(locations))
        self.session.add(new_equipment)
        await self.commit_obj(new_equipment)
        return new_equipment