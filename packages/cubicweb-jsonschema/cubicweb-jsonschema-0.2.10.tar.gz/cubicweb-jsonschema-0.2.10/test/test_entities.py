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

"""cubicweb-jsonschema entities tests"""

from base64 import b64encode
from copy import deepcopy

from six import text_type

from cubicweb import ValidationError
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_jsonschema.entities.ijsonschema import (
    jsonschema_adapter,
)


class MiscTC(CubicWebTC):
    """Tests for functions and mixins in entities module."""

    def test_document_tree_nested(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='CWUser')
            document = mapper.jsl_document('creation')
            j_schema = document.get_schema()
        self.assertIn(
            'thumbnail', j_schema['definitions']['Photo']['properties'])
        self.assertIn('Thumbnail', j_schema['definitions'])


class IJSONSchemaETypeAdapterTC(CubicWebTC):

    maxDiff = None

    def test_adapter_from_etype_uicfg(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            self.assertIsNotNone(adapter)
            j_schema = adapter.creation_schema()
        user_props = j_schema['properties']
        self.assertIn(u'firstname', user_props)
        self.assertNotIn(u'lastname', user_props)  # per uicfg

    def test_adapter_from_etype_view_schema(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            j_schema = adapter.view_schema()
        self.assertNotIn('EmailAlias', j_schema['definitions'])  # per uicfg
        self.assertNotIn('required', j_schema)
        user_props = j_schema['properties']
        self.assertIn('use_email', user_props)
        self.assertNotIn(u'upassword', user_props)
        emailaddr_def = j_schema['definitions']['EmailAddress']
        self.assertNotIn('use_email', emailaddr_def['properties'])

    def test_relation_in_attributes_section(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            creation_schema = adapter.creation_schema()
            view_schema = adapter.view_schema()
            groups = [(group.eid, group.dc_title())
                      for group in cnx.find('CWGroup').entities()
                      if group.name != u'owners']
        self.assertNotIn('CWGroup', creation_schema['definitions'])
        user_creation_schema = creation_schema['properties']
        expected_items = {
            'type': 'string',
            'oneOf': [{'enum': [text_type(eid)], 'title': title}
                      for eid, title in groups],
        }
        self.assertEqual(user_creation_schema['in_group']['items'],
                         expected_items)
        expected = {
            'type': 'array',
            'items': expected_items,
            'description': u'groups grant permissions to the user',
            'title': u'in_group',
        }
        self.assertEqual(view_schema['properties']['in_group'], expected)

    def test_target_of_relation_in_inlined_autoform_section(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            j_schema = adapter.creation_schema()
        self.assertIn('EmailAddress', j_schema['definitions'])

    def test_target_of_relation_has_a_bytes_attribute(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            j_schema = adapter.creation_schema()
        self.assertIn('Photo', j_schema['definitions'])
        photo_schema = j_schema['definitions']['Photo']
        self.assertEqual(photo_schema['properties']['data']['type'],
                         'string')

    def test_target_of_relation_of_relation_registered(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            j_schema = adapter.creation_schema()
        self.assertIn('Thumbnail', j_schema['definitions'])

    def test_create_entity(self):
        with self.admin_access.cnx() as cnx:
            group = cnx.find('CWGroup', name=u'users').one()
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            instance = {
                u'login': u'bob',
                u'upassword': u'123',
                u'firstname': u'Bob',
                u'in_group': [str(group.eid)],
            }
            user = adapter.create_entity(instance)
            cnx.commit()
            for attrname, value in instance.items():
                self.assertEqual(getattr(user, attrname), value)

    def test_create_entity_default_required(self):
        """Not supplying a required property which schema has a "default" flag
        is allowed.
        """
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='Photo')
            j_schema = adapter.creation_schema()
            self.assertIn('media_type', j_schema['required'])
            instance = {
                'data': u'plop',
            }
            entity = adapter.create_entity(instance)
            cnx.commit()
            self.assertEqual(entity.media_type, u'png')

    def test_create_entity_inlined(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='Photo')
            instance = {
                'data': u'plop',
                'media_type': 'png',
                'thumbnail': [
                    {
                        'data': b64encode(b'plip').decode('ascii'),
                    },
                ],
            }
            expected = deepcopy(instance)
            expected['exif_data'] = {
                'flash': False,
            }
            entity = adapter.create_entity(instance.copy())
            entity.cw_clear_all_caches()
            self.assertEqual(len(entity.thumbnail), 1)
            self.assertEqual(entity.thumbnail[0].data.getvalue(),
                             b'plip')
            serialized = entity.cw_adapt_to('IJSONSchema').serialize()
            self.assertEqual(serialized, expected)

    def test_schema_role_required(self):
        """Depending on schema role, required field should not be set."""
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            creation_schema = adapter.creation_schema()
            view_schema = adapter.view_schema()
        # 'required' only present in 'creation' schema.
        self.assertNotIn('required', view_schema)
        self.assertIn('properties', view_schema)
        self.assertCountEqual(creation_schema['required'],
                              ['login', 'upassword', 'in_group'])


class IJSONSchemaRelationTargetETypeAdapterTC(CubicWebTC):

    def test_creation_set_relation(self):
        with self.admin_access.cnx() as cnx:
            adapter = jsonschema_adapter(
                cnx, etype='CWUser', rtype='in_group', role='subject')
            group = cnx.find('CWGroup', name=u'users').one()
            user = adapter.create_entity(
                {u'login': u'bob', u'upassword': u'bob'}, group)
            cnx.commit()
            self.assertEqual([x.eid for x in user.in_group], [group.eid])
            with self.assertRaises(ValidationError) as cm:
                instance = {
                    u'login': u'bob',
                    u'upassword': u'bob',
                    'in_group': [group.eid],
                }
                adapter.create_entity(instance, group)
                cnx.commit()
            self.assertIn('unexpected properties: in_group', str(cm.exception))


class IJSONSchemaEntityAdapterTC(CubicWebTC):

    def test_adapter_from_entity(self):
        with self.admin_access.cnx() as cnx:
            user = cnx.find('CWUser', login=u'admin').one()
            adapter = user.cw_adapt_to('IJSONSchema')
            self.assertIsNotNone(adapter)
            j_schema = adapter.edition_schema()
        self.assertNotIn(u'lastname', j_schema['properties'])

    def test_edition_schema_role(self):
        with self.admin_access.cnx() as cnx:
            user = cnx.find('CWUser', login=u'admin').one()
            adapter = user.cw_adapt_to('IJSONSchema')
            j_schema = adapter.edition_schema()
            user_props = j_schema['properties']
            self.assertIn('upassword', user_props)
            # in "inlined" jsonschema_section
            self.assertIn('use_email', user_props)
            # per jsonschema_section
            self.assertNotIn('lastname', user_props)

    def test_relations(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity('Book', title=u'bouquin')
            cnx.commit()
            adapter = entity.cw_adapt_to('IJSONSchema')
            relations = list(adapter.relations())
            expected = [
                ('author', 'subject', set(['Author'])),
                ('publications', 'object', set(['Author'])),
                ('topics', 'subject', set(['Topic'])),
            ]
            self.assertCountEqual(relations, expected)

    def test_entity_create(self):
        with self.admin_access.cnx() as cnx:
            users = cnx.find('CWGroup', name=u'users').one()
            adapter = jsonschema_adapter(cnx, etype='CWUser')
            instance = {'login': 'bob', 'upassword': 'sponge',
                        'in_group': [text_type(users.eid)],
                        'use_email': [{'address': 'bob@sponge.com'}]}
            entity = adapter.create_entity(instance)
            self.assertEqual(entity.login, 'bob')
            self.assertEqual(entity.upassword, b'sponge')
            self.assertEqual(len(entity.in_group), 1)
            self.assertEqual(entity.in_group[0].name, 'users')
            self.assertEqual(len(entity.use_email), 1)
            self.assertEqual(entity.use_email[0].address, 'bob@sponge.com')

    def test_entity_update(self):
        with self.admin_access.cnx() as cnx:
            entity = self.create_user(cnx, u'bob', password=u'sponge')
            cnx.commit()
            users = cnx.find('CWGroup', name=u'users').one()
            guests = cnx.find('CWGroup', name=u'guests').one()
            adapter = jsonschema_adapter(cnx, entity=entity)

            instance = {'login': 'bobby',
                        'in_group': [text_type(users.eid)],
                        'use_email': [{'address': 'bob@sponge.com'}]}
            adapter.edit_entity(instance)
            entity.cw_clear_all_caches()
            self.assertEqual(entity.login, 'bobby')
            # ensure password have not been reseted
            with cnx.security_enabled(read=False):
                self.assertTrue(entity.upassword)
            self.assertEqual(len(entity.in_group), 1)
            self.assertEqual(entity.in_group[0].name, 'users')
            self.assertEqual(len(entity.use_email), 1)
            self.assertEqual(entity.use_email[0].address, 'bob@sponge.com')

            instance = {'login': 'bobby',
                        'in_group': [text_type(users.eid),
                                     text_type(guests.eid)],
                        'use_email': [{'address': 'bobby@sponge.com'}]}
            adapter.edit_entity(instance)
            entity.cw_clear_all_caches()
            self.assertEqual(entity.login, 'bobby')
            self.assertEqual(len(entity.in_group), 2)
            self.assertCountEqual([group.name for group in entity.in_group],
                                  ['users', 'guests'])
            self.assertEqual(len(entity.use_email), 1)
            self.assertEqual(entity.use_email[0].address, 'bobby@sponge.com')

            instance = {'login': 'bobby',
                        'in_group': [text_type(users.eid)],
                        'use_email': [{'address': 'bobby@sponge.com'},
                                      {'address': 'bob.sponge@sponge.com'}]}
            adapter.edit_entity(instance)
            entity.cw_clear_all_caches()
            self.assertEqual(len(entity.in_group), 1)
            self.assertEqual(entity.in_group[0].name, 'users')
            self.assertEqual(len(entity.use_email), 2)
            self.assertCountEqual([addr.address for addr in entity.use_email],
                                  ['bobby@sponge.com', 'bob.sponge@sponge.com'])

            instance = {'login': 'bobby',
                        'in_group': [text_type(users.eid)],
                        'use_email': [{'address': 'bob.sponge@sponge.com'}]}
            adapter.edit_entity(instance)
            entity.cw_clear_all_caches()
            self.assertEqual(len(entity.use_email), 1)
            self.assertEqual(
                entity.use_email[0].address, 'bob.sponge@sponge.com')

            entity.cw_set(use_email=cnx.create_entity('EmailAlias'))
            instance = {'login': 'bobby',
                        'in_group': [text_type(users.eid)],
                        'use_email': []}
            adapter.edit_entity(instance)
            entity.cw_clear_all_caches()
            self.assertEqual(len(entity.use_email), 1)
            self.assertEqual(entity.use_email[0].cw_etype, 'EmailAlias')

    def test_serialize(self):
        self.maxDiff = None
        with self.admin_access.cnx() as cnx:
            entity = self.create_user(cnx, u'bob', password=u'sponge',
                                      firstname=u'Bob')
            email = cnx.create_entity('EmailAddress', address=u'bob@sponge.com',
                                      reverse_use_email=entity)
            cnx.commit()
            entity.cw_clear_all_caches()
            email.cw_clear_all_caches()

            groups = entity.related('in_group', 'subject').entities()
            group_ids = [text_type(group.eid) for group in groups]
            expected = {
                u'firstname': u'Bob',
                u'login': u'bob',
                u'in_group': group_ids,
                u'use_email': [{u'address': u'bob@sponge.com'}],
            }
            data = entity.cw_adapt_to('IJSONSchema').serialize()
            self.assertEqual(data, expected)


if __name__ == '__main__':
    import unittest
    unittest.main()
