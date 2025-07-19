from pydantic import BaseModel


class FabricCreate(BaseModel):
    name: str


class LocationCreate(BaseModel):
    name: str
    fabric_id: int


class Equipment(BaseModel):
    name: str


class LocationEquipmentCreate(BaseModel):
    location_id: int
    fabric_id: int