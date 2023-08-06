# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-jsonschema Yams to jsl  unit tests."""

from six import text_type

from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_jsonschema.views.y2jsl import y2j_etype


class CWYams2JsonTC(CubicWebTC):

    def rtype(self, etype, rtype):
        return self.vreg.schema[etype].rdef(rtype)

    def test_auto_attributes(self):
        with self.admin_access.cnx() as cnx:

            @y2j_etype(self.vreg, cnx)
            class CWUser(object):
                pass

        j_schema = CWUser.get_schema(ordered=True)
        j_props = j_schema['properties']
        # Check attribute list
        self.assertEqual(['__etype__', '__eid__', 'login', 'upassword',
                          'firstname', 'surname', 'last_login_time'],
                         list(j_props))
        self.assertEqual(['__etype__', '__eid__', 'login', 'upassword'],
                         j_schema['required'])
        # Check type and description
        login = self.rtype('CWUser', 'login')
        self.assertEqual(login.description,
                         j_props['login'].get('description'))
        self.assertEqual('string', j_props['login'].get('type'))
        # Check format
        self.assertEqual('string', j_props['last_login_time'].get('type'))
        self.assertEqual('date-time', j_props['last_login_time'].get('format'))
        # Check simple constraint
        firstname = self.rtype('CWUser', 'firstname')
        self.assertEqual(firstname.constraint_by_type('SizeConstraint').max,
                         j_props['firstname'].get('maxLength'))

    def test_auto_relations(self):
        with self.admin_access.cnx() as cnx:

            @y2j_etype(self.vreg, cnx)
            class Workflow(object):
                __filter_in__ = ('name', 'description')

            @y2j_etype(self.vreg, cnx)
            class State(object):
                pass

            userworkflow_eid = cnx.execute(
                'Any X WHERE X workflow_of ET, ET name "CWUser"')[0][0]

        j_schema = State.get_schema(ordered=True)
        state_props = j_schema['properties']

        self.assertEqual(['__etype__', '__eid__', 'name', 'description',
                          'state_of'], list(state_props))
        expected_items = {
            'type': 'string',
            'oneOf': [{'enum': [text_type(userworkflow_eid)],
                       'title': u'default user workflow'}],
        }
        self.assertEqual(state_props['state_of']['items'],
                         expected_items)
        self.assertEqual(state_props['state_of']['minItems'], 1)
        self.assertEqual(state_props['state_of']['maxItems'], 1)

    def test_reverse_relation(self):
        with self.admin_access.cnx() as cnx:

            @y2j_etype(self.vreg, cnx)
            class CWUser(object):
                pass

            @y2j_etype(self.vreg, cnx)
            class CWGroup(object):
                __filter_in__ = ('reverse_in_group', )

            users = [(user.eid, user.dc_title())
                     for user in cnx.find('CWUser').entities()]

        j_schema = CWGroup.get_schema(ordered=True)
        properties = j_schema['properties']
        self.assertIn('in_group', properties)
        expected_items = {
            'type': 'string',
            'oneOf': [
                {'enum': [text_type(eid)], 'title': title}
                for eid, title in users],
        }
        self.assertEqual(properties['in_group']['items'],
                         expected_items)

    def test_custom_attribute(self):
        with self.admin_access.cnx() as cnx:

            @y2j_etype(self.vreg, cnx)
            class CWUser(object):
                upassword = {'min_length': 7}

        j_schema = CWUser.get_schema(ordered=True)
        j_props = j_schema['properties']
        self.assertIn('minLength', j_props['upassword'])
        self.assertEqual(7, j_props['upassword']['minLength'])

    def test_custom_relation(self):
        with self.admin_access.cnx() as cnx:

            @y2j_etype(self.vreg, cnx)
            class CWGroup(object):
                pass

            @y2j_etype(self.vreg, cnx)
            class CWUser(object):
                in_group = {'min_items': 1}

        j_schema = CWUser.get_schema(ordered=True)
        user_props = j_schema['properties']
        self.assertIn('in_group', user_props)
        self.assertEqual(1, user_props['in_group']['minItems'])


if __name__ == '__main__':
    import unittest
    unittest.main()
