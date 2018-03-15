from jsonschema import validate, ValidationError

schema = {
    "oneOf": [
        {"$ref": "#/definitions/singleObject"}, # plain object
    ],
    "definitions": {
        "singleObject": {
            'type':'object',
            'required': ['username', 'password'],
            'properties':{
                'username':{
                    'type':'string',
                    'description':'username (username)'
                },
                'password': {
                    'type': 'string',
                    'description': 'password (password)'
                }
            }
        }
    }
}

def doValidate(input):
    try:
        validate(input, schema)
        return None
    except ValidationError as e:
        return e