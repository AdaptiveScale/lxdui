from jsonschema import validate, ValidationError

schema = {
    'type': 'object',
    'required': ['name', 'driver', 'config'],
    'properties': {
        'name': {
            'type': 'string',
            'description': 'Storage pool name'
        },
        'driver': {
            'type': 'string',
            'description': 'Storage pool driver'
        },
        'config': {
            'type': 'object',
            'description': 'Storage pool config'
        }
    }
}


def doValidate(data):
    try:
        validate(data, schema)
        return None
    except ValidationError as e:
        return e
