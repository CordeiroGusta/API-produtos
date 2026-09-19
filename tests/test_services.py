import pytest
from unittest.mock import Mock

from app.schemas.items_schemas import ItemRequest, ItemUpdate
from app.services import items_services
from tests.payloads import items_payloads


def make_item_request(payload=None):
    payload = payload or items_payloads.valid_item_payload()
    return ItemRequest(**payload)

def test_create_item_service_success(monkeypatch):
    data = make_item_request()
    expected_item = {"id": 1, **items_payloads.valid_item_payload()}
    repository_mock = Mock(return_value=expected_item)

    monkeypatch.setattr(items_services, "create_item", repository_mock)

    result = items_services.create_item_service(data)

    assert result == expected_item
    repository_mock.assert_called_once_with(data)

@pytest.mark.parametrize(
    "payload_factory",
    [
        items_payloads.invalid_quantity,
        items_payloads.invalid_value,
        items_payloads.empty_name,
        items_payloads.shorter_name,
        items_payloads.greater_name,
        items_payloads.greater_description,
        items_payloads.empty_family,
        items_payloads.greater_family_name,
    ],
    ids=[
        "quantity_invalida",
        "value_invalido",
        "nome_vazio",
        "nome_curto",
        "nome_longo",
        "descricao_longa",
        "familia_vazia",
        "familia_longa",
    ],
)
def test_create_item_service_invalid_data(monkeypatch, payload_factory):
    data = make_item_request(payload_factory())
    repository_mock = Mock()

    monkeypatch.setattr(items_services, "create_item", repository_mock)

    result = items_services.create_item_service(data)

    assert result is None
    repository_mock.assert_not_called()

@pytest.mark.parametrize(
    "field, value",
    [
        ("name", "   "),
        ("family", "   "),
    ],
    ids=["nome_apenas_espacos", "familia_apenas_espacos"],
)
def test_create_item_service_whitespace_only(monkeypatch, field, value):
    payload = items_payloads.valid_item_payload()
    payload[field] = value
    data = ItemRequest(**payload)
    repository_mock = Mock()

    monkeypatch.setattr(items_services, "create_item", repository_mock)

    result = items_services.create_item_service(data)

    assert result is None
    repository_mock.assert_not_called()

def test_update_item_service_success(monkeypatch):
    item_id = 1
    data = ItemUpdate(quantity=10)
    expected_item = {"id": item_id, "quantity": 10}
    repository_mock = Mock(return_value=expected_item)

    monkeypatch.setattr(items_services, "update_item", repository_mock)

    result = items_services.update_item_service(item_id, data)

    assert result == expected_item
    repository_mock.assert_called_once_with(item_id, data)


@pytest.mark.parametrize(
    "field, value",
    [
        ("quantity", 0),
        ("value", 0),
        ("name", ""),
        ("name", "   "),
        ("name", "AB"),
        ("name", "a" * 31),
        ("description", "a" * 61),
        ("family", ""),
        ("family", "   "),
        ("family", "a" * 21),
    ],
    ids=[
        "quantity_invalida",
        "value_invalido",
        "nome_vazio",
        "nome_apenas_espacos",
        "nome_curto",
        "nome_longo",
        "descricao_longa",
        "familia_vazia",
        "familia_apenas_espacos",
        "familia_longa",
    ],
)
def test_update_item_service_invalid_data(monkeypatch, field, value):
    data = ItemUpdate(**{field: value})
    repository_mock = Mock()

    monkeypatch.setattr(items_services, "update_item", repository_mock)

    result = items_services.update_item_service(1, data)

    assert result is None
    repository_mock.assert_not_called()

def test_update_item_service_accepts_empty_update(monkeypatch):
    data = ItemUpdate()
    expected_result = {"id": 1}
    repository_mock = Mock(return_value=expected_result)

    monkeypatch.setattr(items_services, "update_item", repository_mock)

    result = items_services.update_item_service(1, data)

    assert result == expected_result
    repository_mock.assert_called_once_with(1, data)

def test_list_items_service(monkeypatch):
    expected_items = [{"id": 1, "name": "Teclado"}]
    repository_mock = Mock(return_value=expected_items)

    monkeypatch.setattr(items_services, "list_items_all", repository_mock)

    result = items_services.list_items_service()

    assert result == expected_items
    repository_mock.assert_called_once_with()

def test_list_items_service_empty_result(monkeypatch):
    repository_mock = Mock(return_value=[])

    monkeypatch.setattr(items_services, "list_items_all", repository_mock)

    result = items_services.list_items_service()

    assert result == []
    repository_mock.assert_called_once_with()

def test_list_items_id_service_found(monkeypatch):
    expected_item = {"id": 1, "name": "Teclado"}
    repository_mock = Mock(return_value=expected_item)

    monkeypatch.setattr(items_services, "list_item_id", repository_mock)

    result = items_services.list_items_id_service(1)

    assert result == expected_item
    repository_mock.assert_called_once_with(1)

def test_list_items_id_service_not_found(monkeypatch):
    repository_mock = Mock(return_value=None)

    monkeypatch.setattr(items_services, "list_item_id", repository_mock)

    result = items_services.list_items_id_service(900)

    assert result is None
    repository_mock.assert_called_once_with(900)

def test_delete_item_service_success(monkeypatch):
    repository_mock = Mock(return_value=True)

    monkeypatch.setattr(items_services, "delete_item", repository_mock)

    result = items_services.delete_item_service(1)

    assert result is True
    repository_mock.assert_called_once_with(1)

def test_delete_item_service_not_found(monkeypatch):
    repository_mock = Mock(return_value=False)

    monkeypatch.setattr(items_services, "delete_item", repository_mock)

    result = items_services.delete_item_service(900)

    assert result is None
    repository_mock.assert_called_once_with(900)