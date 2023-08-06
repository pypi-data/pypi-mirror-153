"""cubicweb-jsonschema application package

JSON Schema for CubicWeb
"""

VIEW_ROLE = 'view'
CREATION_ROLE = 'creation'
EDITION_ROLE = 'edition'

JSONSCHEMA_MEDIA_TYPE = 'application/schema+json'


def orm_rtype(rtype, role):
    if role == 'object':
        return 'reverse_' + rtype
    return rtype
