from sqlalchemy.orm import Session
from app.schemas.items_schemas import ItemRequest
from app.models.items_models import ItemModel

def create_item(db: Session, data: ItemRequest):
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