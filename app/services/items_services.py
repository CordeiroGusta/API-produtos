from app.schemas.items_schemas import ItemRequest, ItemUpdate
from app.repositories_local.items_repositories import create_item, update_item

def create_item_service(data: ItemRequest):
    if data.quantity <= 0 or data.value <= 0:
        return None

    if data.name is None or data.name.strip() == '':
        return None

    if len(data.name.strip()) < 3:
        return None

    if data.description is not None:
        description = data.description.strip()

        if len(description) > 25:
            return None
    
    if data.family is None or data.family.strip() == "":
        return None

    return create_item(data)

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

    if data.description is not None:
        description = data.description.strip()

        if len(description) > 25:
            return None

    if data.family is not None:
        if data.family.strip() == "":
            return None

    return update_item(item_id, data)