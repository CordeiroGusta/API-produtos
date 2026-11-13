from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.items_schemas import (
    ItemRequest, 
    ItemResponse, 
    ItemUpdate,
    ItemCreatedResponse,
    ItemUpdatedResponse,
    MessageResponse)
from app.database.db_connection import get_db
from app.services import items_services


router = APIRouter(
    prefix='/api/v1/items',
    tags=['items']
)

# LIST ALL ITEMS
@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[ItemResponse]
)
def list_items(db: Session = Depends(get_db)):
    items = items_services.list_items_service(db)
    return items

# LIST A ITEM BY ID
@router.get(
    '/{item_id}',
    status_code=status.HTTP_200_OK,
    response_model=ItemResponse
)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = items_services.list_items_id_service(item_id, db)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O item não foi encontrado'
        )

    return item

# CREATE ITEM
@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ItemCreatedResponse
)
def create_item(data: ItemRequest, db: Session = Depends(get_db)):
    item = items_services.create_item_service(db, data)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='O item não foi criado'
        )

    return {
        'message': 'Item criado com sucesso',
        'item_id': item.id
    }

# UPDATE ITEM
@router.patch(
    '/{item_id}',
    status_code=status.HTTP_200_OK,
    response_model=ItemUpdatedResponse
)
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    item = items_services.update_item_service(db, item_id, data)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O item não foi encontrado'
        )

    return {
        'message': 'Item atualizado com sucesso',
        'item': item
    }

# DELETE ITEM
@router.delete(
    '/{item_id}',
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = items_services.delete_item_service(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O item não foi encontrado'
        )

    return {
        'message': 'Item deletado com sucesso'
    }