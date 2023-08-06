def parse(data, schema):
    pass


schema = {
    'meta': {
        'lazy_functions': ['a', 'b'],
    },

    'type': 'array',
    'items': {
        'type': 'string',
        'format': 'email',
        'validators': email_whitelist_validator,
    }
}

def normalize_schema(schema):
    # converts
    # removes python objects from schema
    # also runs lazy objects specified in meta
    pass


class Widget:
    def __init__(self):
        schema = remove_python_objects(schema)
        pass



class Field:
    schema = schema