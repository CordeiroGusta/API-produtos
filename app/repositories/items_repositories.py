from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.items_schemas import ItemRequest, ItemUpdate
from app.models.items_models import ItemModel

def create_item(db: Session, data: ItemRequest) -> ItemModel:
    item = ItemModel(
        name=data.name,
        description=data.description,
        family=data.family,
        value=data.value,
        quantity=data.quantity
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_items(db: Session) -> list[ItemModel]:
    items = db.scalars(select(ItemModel)).all()
    return items

def list_item_by_id(db: Session, item_id: int) -> ItemModel | None:
    item = db.scalar(select(ItemModel).where(ItemModel.id == item_id))
    return item 

def update_item(db: Session, item_id: int, data: ItemUpdate) -> ItemModel:
    item = db.get(ItemModel, item_id)

    if item is None:
        return None

    updated_fields = data.model_dump(exclude_unset=True)

    for field, value in updated_fields.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item

def delete_item(db: Session, item_id: int) -> bool | None:
    item = db.get(ItemModel, item_id)

    if item is None:
        return None

    db.delete(item)
    db.commit()
    return True