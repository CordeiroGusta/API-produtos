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

class ItemCreatedResponse(BaseModel):
    message: str
    item_id: int

class ItemUpdatedResponse(BaseModel):
    message: str
    item: ItemResponse

class MessageResponse(BaseModel):
    message: str