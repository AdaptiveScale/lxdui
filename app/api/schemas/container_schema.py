from jsonschema import validate, ValidationError

schema = {
    "oneOf": [
        {"$ref": "#/definitions/singleObject"}, # plain object
        {
            "type": "array", # array of plain objects
            "items": {"$ref": "#/definitions/singleObject"}
        }
    ],
    "definitions": {
        "singleObject": {
            'type':'object',
            'required': ['name', 'image'],
            'properties':{
                'name':{
                    'type':'string',
                    'description':'Container name'
                },
                'image':{
                    'type':'string',
                    'description':'Image alias or hash'
                },                
                'type':{
                    'type':'string',
                    'description':'Type of instance'
                },
                'newName': {
                    'type': 'string',
                    'description': 'New Container name'
                },
                'stateful':{
                    'type':'boolean',
                    'description':'Stateful container'
                },
                'profiles':{
                    'type':'array',
                    'items':[
                        {'type':'string'}
                    ]
                },
                'network': {
                    'type': 'array',
                    'items': [
                        {'type': 'string'}
                    ]
                },
                'cpu': {
                    'type': 'object',
                    'description': 'CPU Limitation',
                    'required':['percentage','hardLimitation'],
                    'properties':{
                        'percentage':{
                            'type':'integer',
                            'description':'Set CPU Limitations',
                            'minimum':1,
                            'maximum':100
                        },
                        'hardLimitation':{
                            'type':'boolean',
                            'description':'Set as hard limitation (soft limitation presumed on false)'
                        }
                    }
                },
                'memory':{
                    'type': 'object',
                    'description': 'Memory limitation',
                    'required': ['sizeInMB', 'hardLimitation'],
                    'properties': {
                        'sizeInMB': {
                            'type': 'integer',
                            'description': 'Set memory limitation',
                            'minimum': 32
                        },
                        'hardLimitation':{
                            'type':'boolean',
                            'description':'Set as hard limitation (soft limitation presumed on false)'
                        }
                    }
                },
                'autostart':{
                    'type':'boolean',
                    'description':'autostart instance'
                },
                'description': {
                    'type': 'string',
                    'description': 'Description instance'
                }
            }
        }
    }
}

copyMoveSchema = {
    "oneOf": [
        {"$ref": "#/definitions/singleObject"}, # plain object
    ],
    "definitions": {
        "singleObject": {
            'type':'object',
            'required': ['newContainer'],
            'properties':{
                'newContainer':{
                    'type':'string',
                    'description':'newContainer (name)'
                }
            }
        }
    }
}

exportSchema = {
    "oneOf": [
        {"$ref": "#/definitions/singleObject"}, # plain object
    ],
    "definitions": {
        "singleObject": {
            'type':'object',
            'required': ['imageAlias'],
            'properties':{
                'imageAlias':{
                    'type':'string',
                    'description':'image (alias)'
                }
            }
        }
    }
}

def doValidateImageExport(input):
    try:
        validate(input, exportSchema)
        return None
    except ValidationError as e:
        return e

def doValidateCloneMove(input):
    try:
        validate(input, copyMoveSchema)
        return None
    except ValidationError as e:
        return e

def doValidate(input):
    try:
        validate(input, schema)
        return None
    except ValidationError as e:
        return e