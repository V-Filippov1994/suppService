from typing import List, Literal, Dict

from pydantic import BaseModel


class FabricCreate(BaseModel):
    name: str


class FabricRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    name: str
    fabric_id: int


class LocationRead(BaseModel):
    id: int
    name: str
    fabric: FabricRead


class EquipmentCreate(BaseModel):
    name: str
    location_ids: List[int]


class EquipmentRead(BaseModel):
    id: int
    name: str
    location_ids: List[int]


class LocationEquipmentCreate(BaseModel):
    location_id: int
    fabric_id: int


class TreeNode(BaseModel):
    id: int
    name: str
    type: Literal["Fabric", "Location", "Equipment"]


class TreeResponse(BaseModel):
    object: Dict[str, object]
    tree: Dict[str, List[TreeNode]]

