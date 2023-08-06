# pylint: disable=W0622
"""cubicweb-jsonschema application packaging information"""


modname = 'cubicweb_jsonschema'
distname = 'cubicweb-jsonschema'

numversion = (0, 2, 10)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'JSON Schema for CubicWeb'
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.26.19, < 3.38.0',
    'six': '>= 1.12.0',
    'iso8601': None,
    'jsl': None,
    'pyramid': '>= 1.10.0',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
