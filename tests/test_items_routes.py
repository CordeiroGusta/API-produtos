from tests.payloads import items_payloads


BASE_URL = "/api/v1/items"


def test_api_status(client):
    response = client.get("/api/v1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Olá, se você esta lendo isso, a API esta funcionando!"
    }


def test_list_items(client):
    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_item(client):
    payload = items_payloads.valid_item_payload()

    created_response = client.post(
        f"{BASE_URL}/",
        json=payload
    )

    assert created_response.status_code == 201

    item_id = created_response.json()["item_id"]

    get_response = client.get(f"{BASE_URL}/{item_id}")

    assert get_response.status_code == 200

    item = get_response.json()

    assert item == {
        "id": item_id,
        **payload
    }


def test_get_unexistent_item(client):
    response = client.get(f"{BASE_URL}/900")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "O item não foi encontrado"
    }


def test_create_and_list_items(client):
    payload_1 = items_payloads.valid_item_payload()
    payload_2 = items_payloads.valid_item_payload()
    payload_2["name"] = "Mouse Redragon"

    client.post(f"{BASE_URL}/", json=payload_1)
    client.post(f"{BASE_URL}/", json=payload_2)

    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == payload_1["name"]
    assert response.json()[1]["name"] == payload_2["name"]


def test_create_and_update_item(client):
    payload = items_payloads.valid_item_payload()

    created_response = client.post(
        f"{BASE_URL}/",
        json=payload
    )

    assert created_response.status_code == 201

    item_id = created_response.json()["item_id"]

    update_payload = {"quantity": 10}

    update_response = client.patch(
        f"{BASE_URL}/{item_id}",
        json=update_payload
    )

    assert update_response.status_code == 200

    updated_item = update_response.json()["item"]

    assert updated_item["id"] == item_id
    assert updated_item["quantity"] == 10
    assert updated_item["name"] == payload["name"]
    assert updated_item["value"] == payload["value"]


def test_update_multiple_fields(client):
    payload = items_payloads.valid_item_payload()

    created_response = client.post(
        f"{BASE_URL}/",
        json=payload
    )

    item_id = created_response.json()["item_id"]

    update_payload = {
        "name": "Teclado Atualizado",
        "value": 300.0,
        "family": "Gaming"
    }

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json=update_payload
    )

    assert response.status_code == 200

    updated_item = response.json()["item"]

    assert updated_item["name"] == update_payload["name"]
    assert updated_item["value"] == update_payload["value"]
    assert updated_item["family"] == update_payload["family"]
    assert updated_item["description"] == payload["description"]
    assert updated_item["quantity"] == payload["quantity"]


def test_update_unexistent_item(client):
    response = client.patch(
        f"{BASE_URL}/900",
        json={"quantity": 10}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "O item não foi encontrado"
    }


def test_delete_item(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    delete_response = client.delete(f"{BASE_URL}/{item_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Item deletado com sucesso"
    }


def test_deleted_item_cannot_be_found(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    client.delete(f"{BASE_URL}/{item_id}")

    response = client.get(f"{BASE_URL}/{item_id}")

    assert response.status_code == 404


def test_delete_unexistent_item(client):
    response = client.delete(f"{BASE_URL}/900")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "O item não foi encontrado"
    }


def test_create_invalid_quantity(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.invalid_quantity()
    )

    assert response.status_code == 400


def test_create_invalid_value(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.invalid_value()
    )

    assert response.status_code == 400


def test_create_empty_name(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.empty_name()
    )

    assert response.status_code == 400


def test_create_short_name(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.shorter_name()
    )

    assert response.status_code == 400


def test_create_long_name(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.greater_name()
    )

    assert response.status_code == 400


def test_create_long_description(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.greater_description()
    )

    assert response.status_code == 400


def test_create_empty_family(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.empty_family()
    )

    assert response.status_code == 400


def test_create_long_family(client):
    response = client.post(
        "/api/v1/items/",
        json=items_payloads.greater_family_name()
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.json())

    assert response.status_code == 400


def test_create_string_quantity(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.string_quantity()
    )

    assert response.status_code == 422


def test_create_string_value(client):
    response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.string_value()
    )

    assert response.status_code == 422


def test_update_invalid_quantity(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"quantity": 0}
    )

    assert response.status_code == 404


def test_update_invalid_value(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"value": 0}
    )

    assert response.status_code == 404


def test_update_empty_name(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"name": ""}
    )

    assert response.status_code == 404


def test_update_short_name(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"name": "AB"}
    )

    assert response.status_code == 404


def test_update_long_description(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"description": "a" * 61}
    )

    assert response.status_code == 404


def test_update_empty_family(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"family": ""}
    )

    assert response.status_code == 404


def test_update_invalid_quantity_type(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"quantity": "a"}
    )

    assert response.status_code == 422


def test_update_invalid_value_type(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={"value": "a"}
    )

    assert response.status_code == 422


def test_id_in_create_body_is_ignored(client):
    payload = items_payloads.valid_item_payload()
    payload["id"] = 900

    response = client.post(
        f"{BASE_URL}/",
        json=payload
    )

    assert response.status_code == 201
    assert response.json()["item_id"] == 1


def test_id_in_update_body_is_ignored(client):
    created_response = client.post(
        f"{BASE_URL}/",
        json=items_payloads.valid_item_payload()
    )

    item_id = created_response.json()["item_id"]

    response = client.patch(
        f"{BASE_URL}/{item_id}",
        json={
            "id": 900,
            "quantity": 20
        }
    )

    assert response.status_code == 200
    assert response.json()["item"]["id"] == item_id
    assert response.json()["item"]["quantity"] == 20