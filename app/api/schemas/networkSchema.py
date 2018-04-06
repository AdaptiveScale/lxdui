from jsonschema import validate, ValidationError

schema = {
    "oneOf": [
        {"$ref": "#/definitions/singleObject"}, # plain object
    ],
    "definitions": {
        "singleObject": {
            'type':'object',
            'required': ['IPv4_ENABLED', 'IPv4_AUTO', 'IPv4_ADDR', 'IPv4_NETMASK', 'IPv4_DHCP_START', 'IPv4_DHCP_END'],
            'properties':{
                'IPv4_ENABLED':{
                    'type':'boolean',
                    'description':'Enbale or disable the IPv4'
                },
                'IPv4_AUTO':{
                    'type':'boolean',
                    'description':'Enable auto configuration'
                },
                'IPv4_ADDR':{
                    'type':'string',
                    'description':'Set IPv4 Address for your bridge network'
                },
                'IPv4_NETMASK':{
                    'type':'string',
                    'description':'Set IPv4 Netmask for your bridge'
                },
                'IPv4_DHCP_START':{
                    'type':'string',
                    'description':'Set the starting IP for your DHCP'
                },
                'IPv4_DHCP_END':{
                    'type':'string',
                    'description':'Set the ending IP for your DHCP'
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