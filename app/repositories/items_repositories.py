from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.items_schemas import ItemRequest
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