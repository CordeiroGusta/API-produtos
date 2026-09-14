def valid_item_payload():
    return {
        "name": "Redragon - K686",
        "description": "Teclado Gamer",
        "family": "Periféricos",
        "value": 289.99,
        "quantity": 55
    }


def invalid_quantity():
    payload = valid_item_payload()
    payload['quantity'] = 0

    return payload

def string_quantity():
    payload = valid_item_payload()
    payload['quantity'] = 'a'

    return payload

def invalid_value():
    payload = valid_item_payload()
    payload['value'] = 0

    return payload

def string_value():
    payload = valid_item_payload()
    payload['value'] = ''

    return payload

def empty_name():
    payload = valid_item_payload()
    payload['name'] = ''

    return payload

def shorert_name():
    payload = valid_item_payload()
    payload['name'] = 'AB'

    return payload

def greater_name():
    payload = valid_item_payload()
    payload['name'] = 'a' * 31

    return payload

def greater_description():
    payload = valid_item_payload()
    payload['description'] = 'a' * 61

    return payload

def empty_family():
    payload = valid_item_payload()
    payload['family'] = ''

    return payload

def greater_family_name():
    payload = valid_item_payload()
    payload['family'] = 'a' * 21