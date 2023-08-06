# copyright 2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-jsonschema unit tests for Pyramid JSON Schema API."""

from __future__ import print_function

import doctest
from functools import partial
from glob import glob
import json
from os import path
import subprocess
import tempfile
import warnings

import jsonschema
from six import PY2

from cubicweb.pyramid.test import PyramidCWTest
from cubicweb_jsonschema import testing


def testcase_cls(test):
    """Return a unittest TestCase subclass to run `test` doctest."""
    # build class name from doctest's filename (slugify, camelcase)
    basename, __ = path.splitext(path.basename(test.filename))
    clsname = ''.join([w.capitalize() for w in basename.split('-')])

    class ApiBaseTC(PyramidCWTest):
        """Base class of API (doc)tests."""

        settings = {
            'cubicweb.bwcompat': False,
            'cubicweb.auth.authtkt.session.secret': 'x',
            'cubicweb.auth.authtkt.persistent.secret': 'x',
            'cubicweb.session.secret': 'x',
        }

        def includeme(self, config):
            config.include('cubicweb_jsonschema.api')

        def logout(self):
            # XXX /logout route is not implemented without bwcompat so reset
            # cookies by hand...
            self.webapp.reset()

        def setup_database(self):
            with self.admin_access.cnx() as cnx:
                for topic_name in (u'fishing', u'gardening', u'sword fish'):
                    cnx.create_entity('Topic', name=topic_name)
                cnx.commit()

    return type(clsname, (ApiBaseTC, ), {})


def load_tests(loader, tests, ignore):

    here = path.dirname(__file__)
    hyperschema = path.join(here, 'data', 'hyper-schema-draft-06.json')
    validationschema = path.join(here, 'data', 'schema-draft-06.json')
    try:
        has_ajv = subprocess.call(['ajv', 'help'], stdout=subprocess.PIPE) == 0
    except OSError:
        warnings.warn('"ajv" is not available, no validation of JSON Schema '
                      'will be performed')
        has_ajv = False

    if PY2:
        temporary_file = tempfile.NamedTemporaryFile
    else:
        temporary_file = partial(tempfile.NamedTemporaryFile,
                                 mode='w', encoding='utf-8')

    def validate_schema(schema):
        """Validate `schema` against validation and hyper meta-schema.

        Rely on ajv validator if available and use python-jsonschema only for
        hyper schema validation since draft-06 is not supported and $ref are
        not apparently resolved (meaning that hyper-schema reference to
        validation schema is not used).
        """
        with open(hyperschema) as f:
            try:
                jsonschema.validate(schema, json.load(f))
            except jsonschema.RefResolutionError as exc:
                warnings.warn(
                    'validation with python-jsonschema failed ({})'.format(
                        str(exc)),
                    RuntimeWarning,
                )
        if not has_ajv:
            return
        with temporary_file(suffix='.json') as schemafile:
            json.dump(schema, schemafile, indent=2)
            schemafile.seek(0)
            for metaschema in (validationschema, hyperschema):
                cmd = ['ajv', 'validate', '-s', metaschema, '-d',
                       schemafile.name]
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                if proc.returncode != 0:
                    raise AssertionError(
                        '\n'.join([
                            'error validating instance:',
                            json.dumps(schema, indent=2),
                            'against: {}'.format(metaschema),
                            stderr.decode(errors='replace'),
                        ])
                    )

    def get_schema(app, url, status=200, **kwargs):
        """Helper function to get a JSON schema from `url`."""
        response = app.get(url, status=status,
                           headers={'accept': 'application/schema+json'},
                           **kwargs)
        if status != 200:
            return None
        schema = response.json
        validate_schema(schema)
        return response

    def setUp(test):
        tccls = testcase_cls(test)
        testing.setUp(test, tccls, ['webapp', 'login'])
        client = test.globs['client'] = test.globs.pop('webapp')
        client.get_schema = partial(get_schema, client)
        client.login = partial(test.globs.pop('login'))

    def docfilesuite(fpath):
        return doctest.DocFileSuite(
            fpath,
            setUp=setUp,
            tearDown=testing.tearDown,
            module_relative=False,
            checker=testing.WebTestReponseOutputChecker(),
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
        )

    for fpath in glob(path.join(here, 'schema-api', '*.rst')):
        tests.addTests(docfilesuite(fpath))
    for fpath in glob(path.join(here, 'api', '*.rst')):
        tests.addTests(docfilesuite(fpath))
    tests.addTests(
        docfilesuite(path.join(here, 'hypermedia-walkthrough.rst')))

    return tests


if __name__ == '__main__':
    import unittest
    unittest.main()
