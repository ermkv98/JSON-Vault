from cerberus import Validator

get_schema = {
    'link': {'required': True, 'type': 'string'},
    'protected': {'required': False, 'type': 'boolean'},
    'password': {'required': False, 'type': 'string', 'dependencies': 'protected'},
    'content': {'required': False, 'type': 'string'},
    'new_password': {'required': False, 'type': 'string', 'dependencies': 'protected'},
    'old_password': {'required': False, 'type': 'string', 'dependencies': 'protected'}
}

get_validator = Validator(get_schema)


