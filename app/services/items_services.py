from sqlalchemy.orm import Session
from app.models.items_models import ItemModel
from app.schemas.items_schemas import ItemRequest, ItemUpdate
from app.repositories import items_repositories

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

def update_item_service(db: Session, item_id: int, data: ItemUpdate) -> ItemModel:
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

    return items_repositories.update_item(db, item_id, data)

def list_items_service(db: Session) -> list[ItemModel]:
    return items_repositories.list_items(db)

def list_items_id_service(db: Session, id_item: int) -> ItemModel | None:
    item = items_repositories.list_item_by_id(id_item, db)
    return item

def delete_item_service(db: Session, id_item: int):
    item = items_repositories.delete_item(db, id_item)
    if item == True:
        return True

    return None