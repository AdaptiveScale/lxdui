from jsonschema import validate, ValidationError

schema = {
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
            'properties':{
                'percentage':{
                    'type':'integer',
                    'description':'Set CPU Limitations'
                },
                'hardLimitation':{
                    'type':'boolean',
                    'description':'Set as hard limitation'
                }
            },
        }
    }
}

def doValidate(input):
    try:
        validate(input, schema)
        return None
    except ValidationError as e:
        return e