import json

def order_data(data, relations):
    ordered_data = []
    for relation in relations:
        if relation.element.name in data:
            ordered_data.append([relation.element.name, data[relation.element.name]])
    return ordered_data

def decode_json(json_data):
    return json.loads(json_data)

def encode_data(data):
    return json.dumps(data)