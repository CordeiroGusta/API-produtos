from sqlalchemy.orm import Session
from app.repositories import items_repositories
from app.models.items_models import ItemModel
from app.schemas.items_schemas import ItemRequest, ItemUpdate
from app.repositories_local.items_repositories import create_item, update_item, list_items_all, list_item_id, delete_item

def create_item_service(db: Session, data: ItemRequest) -> ItemModel:
    if data.quantity <= 0 or data.value <= 0:
        return None

    if data.name is None or data.name.strip() == '':
        return None

    if len(data.name.strip()) < 3:
        return None

    if len(data.name.strip()) > 30:
            return None

    if data.description is not None:
        description = data.description.strip()

        if len(description) > 60:
            return None
    
    if data.family is None or data.family.strip() == "":
        return None

    if len(data.family.strip()) > 20:
        return None 

    return items_repositories.create_item(db, data)

def update_item_service(item_id: int, data: ItemUpdate):
    if data.quantity is not None:
        if data.quantity <= 0:
            return None

    if data.value is not None:
        if data.value <= 0:
            return None

    if data.name is not None:
        if data.name.strip() == '':
            return None

        if len(data.name.strip()) < 3:
            return None

        if len(data.name.strip()) > 30:
            return None

    if data.description is not None:
        description = data.description.strip()

        if len(description) > 60:
            return None

    if data.family is not None:
        if data.family.strip() == "":
            return None

        if len(data.family.strip()) > 20:
            return None 

    return update_item(item_id, data)

def list_items_service(db: Session) -> list[ItemModel]:
    return items_repositories.list_items(db)

def list_items_id_service(id_item: int):
    item = list_item_id(id_item)
    return item

def delete_item_service(id_item: int):
    item = delete_item(id_item)
    if item == True:
        return True

    return None