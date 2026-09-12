from app.schemas.items_schemas import ItemRequest, ItemUpdate

_items: list[dict] = []
_next_id = 1

def list_itens_all() -> list[dict]:
    return _items

#Lista o item pelo seu id
def list_item_id(item_id: int) -> dict | None:
    for item in _items:
        if item['id'] == item_id:
            return item 
    
    return None

def create_item(data: ItemRequest) -> bool:
    global _next_id

    item = {
        'id': _next_id,
        'name': data.name,
        'description': data.description,
        'family': data.family,
        'value': data.value,
        'quantity': data.quantity
    }
    _items.append(item)
    _next_id += 1

    return True

def update_item(item_id: int, updated_item: ItemUpdate) -> bool | None:
    for index, item in enumerate(_items):
        if item['id'] == item_id: 
            updated_item = updated_item.model_dump(exclude_unset=True)
            item.update(updated_item)
            return True 
    return None

def delete_item(item_id: int) -> bool | None:
    for index, item in enumerate(_items):
        if item['id'] == item_id:
            del _items[index]
            return True
    return None 