from jsonschema import validate, ValidationError

schema = {
    'type': 'object',
    'required': ['name', 'config', 'devices'],
    'properties': {
        'name': {
            'type': 'string',
            'description': 'Profile name'
        },
        'description': {
            'type': 'string',
            'description': 'Profile description'
        },
        'devices': {
            'type': 'object',
            'description': 'Configuration devices',
            'properties': {
                'none': {
                    'type': 'string',
                    'description': 'Inheritance blocker'
                },
                'nic': {
                    'type': 'object',
                    'description': 'Network interface',
                    'properties': {
                        'physical': {
                            'type': 'object',
                            'required': ['nictype', 'parent'],
                            'description': 'Straight physical device passthrough from the host. The targeted device will vanish from the host and appear in the container',
                            'properties': {
                                'nictype': {
                                    'type': 'string',
                                    'description': 'The device type, one of "bridged", "macvlan", "p2p", "physical", or "sriov"'
                                },
                                'parent': {
                                    'type': 'string',
                                    'description': 'The name of the host device or bridge'
                                }
                            }
                        },
                        'bridged': {
                            'type': 'object',
                            'required': ['nictype', 'parent'],
                            'description': 'Uses an existing bridge on the host and creates a virtual device pair to connect the host bridge to the container',
                            'properties': {
                                'nictype': {
                                    'type': 'string',
                                    'description': 'The device type, one of "bridged", "macvlan", "p2p", "physical", or "sriov"'
                                },
                                'parent': {
                                    'type': 'string',
                                    'description': 'The name of the host device or bridge'
                                }
                            }
                        },
                        'macvlan': {
                            'type': 'object',
                            'required': ['nictype', 'parent'],
                            'description': 'Sets up a new network device based on an existing one but using a different MAC address.',
                            'properties': {
                                'nictype': {
                                    'type': 'string',
                                    'description': 'The device type, one of "bridged", "macvlan", "p2p", "physical", or "sriov"'
                                },
                                'parent': {
                                    'type': 'string',
                                    'description': 'The name of the host device or bridge'
                                }
                            }
                        },
                        'p2p': {
                            'type': 'object',
                            'required': ['nictype'],
                            'description': 'Creates a virtual device pair, putting one side in the container and leaving the other side on the host.',
                            'properties': {
                                'nictype': {
                                    'type': 'string',
                                    'description': 'The device type, one of "bridged", "macvlan", "p2p", "physical", or "sriov"'
                                }
                            }
                        },
                        'sriov': {
                            'type': 'object',
                            'required': ['nictype', 'parent'],
                            'description': 'Passes a virtual function of an SR-IOV enabled physical network device into the container.',
                            'properties': {
                                'nictype': {
                                    'type': 'string',
                                    'description': 'The device type, one of "bridged", "macvlan", "p2p", "physical", or "sriov"'
                                },
                                'parent': {
                                    'type': 'string',
                                    'description': 'The name of the host device or bridge'
                                }
                            }
                        },
                    }
                },
                'disk': {
                    'type': 'object',
                    'required': ['path', 'source'],
                    'properties': {
                        'path': {
                            'type': 'string',
                            'description': 'Path inside the container where the disk will be mounted'
                        },
                        'source': {
                            'type': 'string',
                            'description': 'Path on the host, either to a file/directory or to a block device'
                        }
                    }
                }
            }
        },
        'config': {
            'type': 'object'
        },
        'used_by': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        'new_name': {
            'type': 'string',
            'description': 'The new name to set to the profile.'
        }
    }
}

renameSchema = {
    'type': 'object',
    'required': ['new_name'],
    'properties': {
        'new_name': {
            'type': 'string',
            'description': 'The new name to set to the profile'
        }
    }
}


def doValidate(data):
    try:
        validate(data, schema)
        return None
    except ValidationError as e:
        return e


def doValidateRename(data):
    try:
        validate(data, renameSchema)
        return None
    except ValidationError as e:
        return e
