import pytest

from app.repositories_local import items_repositories
from app.schemas.items_schemas import ItemRequest, ItemUpdate
from tests.payloads import items_payloads


@pytest.fixture(autouse=True)
def reset_repository():
    items_repositories._items.clear()
    items_repositories._next_id = 1

    yield

    items_repositories._items.clear()
    items_repositories._next_id = 1


def make_item_request(payload=None):
    payload = payload or items_payloads.valid_item_payload()
    return ItemRequest(**payload)


def test_list_items_all_empty():
    result = items_repositories.list_items_all()

    assert result == []


def test_create_item():
    data = make_item_request()

    result = items_repositories.create_item(data)

    assert result == 1
    assert items_repositories._items == [
        {
            "id": 1,
            "name": data.name,
            "description": data.description,
            "family": data.family,
            "value": data.value,
            "quantity": data.quantity,
        }
    ]


def test_create_multiple_items_generates_sequential_ids():
    first_data = make_item_request()

    second_payload = items_payloads.valid_item_payload()
    second_payload["name"] = "Mouse Redragon"
    second_data = make_item_request(second_payload)

    first_id = items_repositories.create_item(first_data)
    second_id = items_repositories.create_item(second_data)

    assert first_id == 1
    assert second_id == 2
    assert len(items_repositories._items) == 2
    assert items_repositories._items[0]["id"] == 1
    assert items_repositories._items[1]["id"] == 2


def test_list_items_all_returns_created_items():
    first_data = make_item_request()

    second_payload = items_payloads.valid_item_payload()
    second_payload["name"] = "Mouse Redragon"
    second_data = make_item_request(second_payload)

    items_repositories.create_item(first_data)
    items_repositories.create_item(second_data)

    result = items_repositories.list_items_all()

    assert len(result) == 2
    assert result[0]["name"] == first_data.name
    assert result[1]["name"] == second_data.name


def test_list_item_id_returns_item_when_it_exists():
    data = make_item_request()

    item_id = items_repositories.create_item(data)

    result = items_repositories.list_item_id(item_id)

    assert result == {
        "id": item_id,
        "name": data.name,
        "description": data.description,
        "family": data.family,
        "value": data.value,
        "quantity": data.quantity,
    }


def test_list_item_id_returns_none_when_item_does_not_exist():
    result = items_repositories.list_item_id(900)

    assert result is None


def test_update_item_quantity():
    data = make_item_request()
    item_id = items_repositories.create_item(data)

    update_data = ItemUpdate(quantity=10)

    result = items_repositories.update_item(
        item_id,
        update_data
    )

    assert result is not None
    assert result["id"] == item_id
    assert result["quantity"] == 10
    assert result["name"] == data.name
    assert result["value"] == data.value


def test_update_item_multiple_fields():
    data = make_item_request()
    item_id = items_repositories.create_item(data)

    update_data = ItemUpdate(
        name="Teclado Atualizado",
        family="Gaming",
        value=350.0,
        quantity=20,
    )

    result = items_repositories.update_item(
        item_id,
        update_data
    )

    assert result is not None
    assert result["id"] == item_id
    assert result["name"] == "Teclado Atualizado"
    assert result["family"] == "Gaming"
    assert result["value"] == 350.0
    assert result["quantity"] == 20
    assert result["description"] == data.description


def test_update_item_only_changes_fields_sent():
    data = make_item_request()
    item_id = items_repositories.create_item(data)

    update_data = ItemUpdate(quantity=10)

    result = items_repositories.update_item(
        item_id,
        update_data
    )

    assert result["quantity"] == 10
    assert result["name"] == data.name
    assert result["description"] == data.description
    assert result["family"] == data.family
    assert result["value"] == data.value


def test_update_item_with_empty_update_does_not_change_item():
    data = make_item_request()
    item_id = items_repositories.create_item(data)

    update_data = ItemUpdate()

    result = items_repositories.update_item(
        item_id,
        update_data
    )

    assert result == {
        "id": item_id,
        "name": data.name,
        "description": data.description,
        "family": data.family,
        "value": data.value,
        "quantity": data.quantity,
    }


def test_update_item_returns_none_when_item_does_not_exist():
    update_data = ItemUpdate(quantity=10)

    result = items_repositories.update_item(
        900,
        update_data
    )

    assert result is None


def test_delete_item():
    data = make_item_request()
    item_id = items_repositories.create_item(data)

    result = items_repositories.delete_item(item_id)

    assert result is True
    assert items_repositories._items == []


def test_delete_item_returns_none_when_item_does_not_exist():
    result = items_repositories.delete_item(900)

    assert result is None


def test_deleted_item_is_no_longer_found():
    data = make_item_request()
    item_id = items_repositories.create_item(data)

    items_repositories.delete_item(item_id)

    result = items_repositories.list_item_id(item_id)

    assert result is None


def test_id_is_not_reused_after_deletion():
    first_data = make_item_request()
    first_id = items_repositories.create_item(first_data)

    items_repositories.delete_item(first_id)

    second_data = make_item_request()
    second_id = items_repositories.create_item(second_data)

    assert first_id == 1
    assert second_id == 2
    assert items_repositories._items[0]["id"] == 2