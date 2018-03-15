from jsonschema import validate, ValidationError

schema = {
    "oneOf": [
        {"$ref": "#/definitions/singleObject"}, # plain object
    ],
    "definitions": {
        "singleObject": {
            'type':'object',
            'required': ['image'],
            'properties':{
                'name':{
                    'type':'string',
                    'description':'image (name/distribution/architecture)'
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