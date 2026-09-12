from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int 
    name: str 
    description: str 
    family: str 
    value: float 
    quantity: int 

class ItemRequest(BaseModel):
    name: str
    description: str | None = None
    family: str
    value: float
    quantity: int

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    family: str | None = None
    value: float | None = None
    quantity: int | None = None