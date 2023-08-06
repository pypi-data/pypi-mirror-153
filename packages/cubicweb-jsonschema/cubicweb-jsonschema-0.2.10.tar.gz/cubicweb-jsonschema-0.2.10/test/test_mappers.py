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

import base64
from datetime import datetime
import unittest

import jsl
import jsonschema
from pytz import UTC

from cubicweb import (
    Binary,
    Unauthorized,
    _,
)
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_jsonschema import CREATION_ROLE, EDITION_ROLE, VIEW_ROLE
from cubicweb_jsonschema.mappers import (
    CompoundMapper,
    yams_match
)


class CollectionMapperTC(CubicWebTC):

    def test_jsl_field_view(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.collection', cnx, etype='Book')
            field = mapper.jsl_field(VIEW_ROLE)
        j_schema = field.get_schema()
        expected = {
            'type': 'array',
            'title': 'Book_plural',
            'items': {
                'properties': {
                    'type': {'type': 'string'},
                    'id': {'type': 'string'},
                    'title': {'type': 'string'},
                },
                'type': 'object',
            },
        }
        self.assertEqual(j_schema, expected)

    def test_jsl_field_creation(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.collection', cnx, etype='Book')
            field = mapper.jsl_field(CREATION_ROLE)
        j_schema = field.get_schema()
        expected = {
            'type': 'array',
            'title': 'Book_plural',
            'items': {'type': 'string'},
        }
        self.assertEqual(j_schema, expected)


class RelationMapperTC(CubicWebTC):

    def test_target_types(self):
        with self.admin_access.client_cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='CWEType', rtype='add_permission', role='subject',
                target_types={'CWGroup', 'RQLExpression'})
            self.assertCountEqual(mapper.target_types, [
                                  'CWGroup', 'RQLExpression'])

            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='CWEType', rtype='add_permission', role='subject',
                target_types={'CWGroup'})
            self.assertEqual(mapper.target_types, ['CWGroup'])

    def test_multiple_target_types_inlined(self):
        with self.admin_access.client_cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='CWUser', rtype='use_email', role='subject',
                target_types={'EmailAddress', 'EmailAlias'})
            field = mapper.jsl_field(CREATION_ROLE)
            self.assertIsInstance(field, jsl.fields.ArrayField)
            self.assertIsInstance(field.items, jsl.fields.OneOfField)
            self.assertEqual(len(field.items.fields), 2)

    def test_attribute_have_no_target_types(self):
        with self.admin_access.client_cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='CWUser', rtype='login', role='subject',
                target_types={'String'})
            self.assertCountEqual(mapper.target_types, [])

    def test_password_field_not_required_on_update(self):
        with self.admin_access.client_cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='CWUser', rtype='upassword', role='subject',
                target_types={'Password'})
            self.assertTrue(mapper.jsl_field(CREATION_ROLE).required)
            self.assertFalse(mapper.jsl_field(EDITION_ROLE).required)

    def test_inlined_relation_select_on_entity(self):
        with self.admin_access.client_cnx() as cnx:
            user = cnx.find('CWUser', login=u'admin').one()
            mapper = cnx.vreg['mappers'].select_or_none(
                'jsonschema.relation', cnx,
                entity=user, rtype='use_email', role='subject',
                target_types={'EmailAddress'})
            self.assertIsNotNone(mapper)

    def test_vocabulary(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='Photo', rtype='media_type', role='subject',
                target_types={'String'})
            field = mapper.jsl_field(CREATION_ROLE)
            expected = {
                'oneOf': [
                    {'enum': ['jpeg'], 'title': 'jpeg', 'type': 'string'},
                    {'enum': ['png'], 'title': 'png', 'type': 'string'},
                ],
                'default': 'png',
                'title': 'media_type',
            }
            self.assertEqual(field.get_schema(), expected)
            adapter = self.vreg['adapters'].select(
                'IJSONSchema', cnx, etype='Photo')
            # Make sure 'required' constraint is present in the main schema.
            schema = adapter.creation_schema()
            self.assertIn('media_type', schema['required'])

    def test_required_generic_relation(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='CWUser')
            schema = mapper.jsl_document(CREATION_ROLE).get_schema()
            self.assertIn('in_group', schema['required'])


class InlinedRelationMapperTC(CubicWebTC):

    def test_schema(self):
        with self.admin_access.client_cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='CWUser', rtype='use_email', role='subject',
                target_types={'EmailAddress'},
            )
            field = mapper.jsl_field(CREATION_ROLE)
            schema = field.get_schema()
            expected = {
                'title': 'use_email',
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/EmailAddress',
                },
                'description': "user's email account",
                'definitions': {
                    'EmailAddress': {
                        'title': 'EmailAddress',
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': {
                            'address': {
                                'format': 'email',
                                'maxLength': 128,
                                'title': 'address',
                                'type': 'string',
                            },
                            'alias': {
                                'maxLength': 56,
                                'title': 'alias',
                                'type': 'string',
                            },
                        },
                        'required': ['address'],
                    },
                },
            }
        self.maxDiff = None
        self.assertEqual(schema, expected)


class AttributeMappersTC(CubicWebTC):

    def test_bytes_serialize(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity('Photo', data=Binary(b'plop'))
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, etype='Photo',
                rtype='data', role='subject', target_types={'Bytes'})
            self.assertEqual(mapper.__class__.__name__,
                             'BytesMapper')
            self.assertEqual(mapper.serialize(entity), u'plop')

    def test_bytes_value(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, etype='Photo',
                rtype='data', role='subject', target_types={'Bytes'})
            self.assertEqual(mapper.__class__.__name__,
                             'BytesMapper')
            values = mapper.values(None, {'data': u'plop'})
            self.assertEqual(len(values), 1)
            bin_value = values['data']
            self.assertIsInstance(bin_value, Binary)
            self.assertEqual(bin_value.getvalue(), b'plop')

    def test_date_value(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, etype='CWUser',
                rtype='last_login_time', role='subject',
                target_types={'TZDatetime'})
            instance = {'last_login_time': '2007-01-25T12:00:00Z'}
            values = mapper.values(None, instance)
            expected = {
                'last_login_time': datetime(2007, 1, 25, 12, 0, tzinfo=UTC),
            }
            self.assertEqual(values, expected)

    def test_password_values(self):
        with self.admin_access.cnx() as cnx:
            users = cnx.find('CWGroup', name=u'users').one()
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, etype='CWUser',
                rtype='upassword', role='subject', target_types={'Password'},
            )
            instance = {
                'upassword': u'bob',
            }
            values = mapper.values(None, instance)
            self.assertEqual(values, {'upassword': b'bob'})

            # Make sure we can create an entity with these "values".
            user = cnx.create_entity(
                'CWUser', login=u'bob', in_group=users, **values)
            cnx.commit()
            self.assertEqual(user.upassword, b'bob')

            # Now check update.
            instance = {
                'upassword': u'bobby',
            }
            values = mapper.values(user, instance)
            self.assertEqual(values, {'upassword': b'bobby'})
            # We cannot apparently read the password after entity creation, so
            # just make sure update does not raise a validation error.
            try:
                user.cw_set(**values)
                cnx.commit()
            except Exception as exc:
                self.fail(str(exc))

    def test_select_custom_mapper_over_default_one(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='Thumbnail', rtype='data', role='subject',
                target_types={'Bytes'})
            self.assertEqual(mapper.__class__.__name__, 'ThumbnailDataMapper')
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx,
                etype='Photo', rtype='data', role='subject',
                target_types={'Bytes'})
            self.assertEqual(mapper.__class__.__name__, 'BytesMapper')

    def test_custom_mapper_for_bytes(self):
        with self.admin_access.cnx() as cnx:
            thumbnail = cnx.create_entity('Thumbnail', data=Binary(b'plip'))
            photo = cnx.create_entity('Photo', data=Binary(b'plop'),
                                      thumbnail=thumbnail)
            cnx.commit()
            adapter = photo.cw_adapt_to('IJSONSchema')
            instance = adapter.serialize()
            expected = {
                'data': u'plop',
                'exif_data': {
                    'flash': False,
                },
                'media_type': 'png',
                'thumbnail': [
                    {'data': base64.b64encode(b'plip').decode('ascii')},
                ],
            }
            self.assertEqual(instance, expected)

    def test_custom_format(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, etype='EmailAddress',
                rtype='address', role='subject', target_types={'String'})
            schema = mapper.jsl_field(VIEW_ROLE).get_schema()
            expected = {
                'type': 'string',
                'title': 'address',
                'format': 'email',
            }
            self.assertEqual(schema, expected)

    def test_unchanged_value_not_updated(self):
        with self.admin_access.cnx() as cnx:
            self.create_user(cnx, u'bob')
            cnx.commit()
        with self.new_access(u'bob').cnx() as cnx:
            entity = cnx.create_entity('Topic', name=u'top')
            cnx.commit()
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, entity=entity,
                rtype='name', role='subject', target_types={'String'})
            # By permission, we can change the attribute.
            values = mapper.values(entity, {'name': 'tip'})
            self.assertEqual(values, {'name': 'tip'})
            entity.cw_set(**values)
            cnx.commit()
            cnx.create_entity('Book', title=u'ti', topics=entity)
            cnx.commit()
            # Value change, we get something returned.
            values = mapper.values(entity, {'name': 'top'})
            self.assertEqual(values, {'name': 'top'})
            # By permission, we can't change the attribute.
            with self.assertRaises(Unauthorized):
                entity.cw_set(**values)
                cnx.commit()
            cnx.rollback()
            # But passing the actual value of attribute should not trigger
            # entity update.
            values = mapper.values(entity, {'name': 'tip'})
            self.assertEqual(values, {})


class CompoundMapperTC(CubicWebTC):

    def mapper_by_name(self, name):
        for obj in self.vreg['mappers']['jsonschema.object']:
            if obj.name == name:
                return obj
        raise ValueError(name)

    def test_no_relations_attribute(self):
        class bad_compound(CompoundMapper):
            etype = 'Photo'

        expected_regexp = 'is missing a "relations" class attribute'
        with self.assertRaisesRegex(ValueError, expected_regexp):
            bad_compound.__registered__(self.vreg['mappers'])

    def test_no_duplicate_relation_mapping(self):
        """A CompoundMapper with the same relation 'flash' is defined in
        test/data/mappers.py, thus this one is a duplicate and should fail.
        """
        class bad_compound(CompoundMapper):
            etype = 'Photo'
            relations = ('flash', )

        expected_regexp = 'duplicate relation mapping for "Photo": flash'
        with self.assertRaisesRegex(ValueError, expected_regexp):
            bad_compound.__registered__(self.vreg['mappers'])

    def test_no_duplicate_subject_relation_mapping(self):
        """A CompoundMapper with the same relation 'flash' is defined in
        test/data/mappers.py, thus this one is a duplicate and should fail.
        """
        class bad_compound(CompoundMapper):
            etype = 'Photo'
            relations = (
                ('flash', 'subject'),
            )

        expected_regexp = 'duplicate relation mapping for "Photo": flash-subject'  # noqa: E501
        with self.assertRaisesRegex(ValueError, expected_regexp):
            bad_compound.__registered__(self.vreg['mappers'])

    def test_no_duplicate_object_relation_mapping(self):
        class good_compound(CompoundMapper):
            etype = 'Book'
            relations = (
                'author',
                ('author', 'object'),
            )

        try:
            good_compound.__registered__(self.vreg['mappers'])
        except ValueError as e:
            self.fail("unexpected {}".format(e))

    def test_mapped_attributes_hidden(self):
        """Make sure attributes mapped to CompoundMapper are in "hidden" uicfg
        section.
        """
        with self.admin_access.cnx() as cnx:
            entity = cnx.vreg['etypes'].etype_class('Photo')(cnx)
            rsection = cnx.vreg['uicfg'].select(
                'jsonschema', cnx, entity=entity)
            for action in ('read', 'add'):
                with self.subTest(action=action):
                    hidden = list(rsection.relations_by_section(
                        entity, 'hidden', action))
                    self.assertIn(('exposure_time', 'subject', set(['Float'])),
                                  hidden)
                    self.assertIn(('flash', 'subject', set(['Boolean'])),
                                  hidden)

    def test_schema(self):
        with self.admin_access.cnx() as cnx:
            mapper = self.mapper_by_name('exif_data')(cnx)
            doc = mapper.jsl_field(VIEW_ROLE)
            schema = doc.get_schema()
            expected = {
                '$ref': '#/definitions/EXIF data',
                'definitions': {
                    u'EXIF data': {
                        'title': u'EXIF data',
                        'type': 'object',
                        'properties': {
                            'exposure_time': {
                                'title': u'exposure_time',
                                'type': 'number',
                            },
                            'flash': {
                                'title': u'flash',
                                'type': 'boolean',
                            },
                            'maker_note': {
                                'title': u'maker_note',
                                'type': 'string',
                            },
                        },
                        'additionalProperties': False,
                    },
                },
            }
            self.maxDiff = None
            self.assertEqual(schema, expected)
            doc = mapper.jsl_field(CREATION_ROLE)
            schema = doc.get_schema()
            expected['definitions']['EXIF data']['required'] = ['flash']
            expected['definitions']['EXIF data'][
                'properties']['flash']['default'] = False
            self.assertEqual(schema, expected)

    def test_serialize(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity(
                'Photo', data=Binary(b'plop'),
                exposure_time=1.23, flash=False)
            mapper = self.mapper_by_name('exif_data')(cnx)
            data = mapper.serialize(entity)
            expected = {
                'exposure_time': 1.23,
                'flash': False,
            }
            self.assertEqual(data, expected)
            entity.cw_set(exposure_time=None)
            del expected['exposure_time']
            data = mapper.serialize(entity)
            self.assertEqual(data, expected)

    def test_values(self):
        with self.admin_access.cnx() as cnx:
            instance = {
                'data': 'plop',
                'exif_data': {
                    'flash': True,
                    'exposure_time': 0.87,
                    'maker_note': 'secret thing',
                }
            }
            mapper = self.mapper_by_name('exif_data')(cnx)
            values = mapper.values(None, instance.copy())
            self.assertEqual(values, instance['exif_data'])
            self.assertIsInstance(values['maker_note'], Binary)
            self.assertEqual(values['maker_note'].getvalue(),
                             b'secret thing')
            # Now make sure we can actually create an entity from "values".
            # We need to add 'data' property to "values" as the latter comes
            # from the compound mapper which does not manage the former.
            assert 'data' not in values
            values['data'] = Binary(b'plop')
            try:
                cnx.create_entity('Photo', **values)
            except Exception as e:
                self.fail(str(e))

    def test_etype_schema(self):
        with self.admin_access.cnx() as cnx:
            adapter = cnx.vreg['adapters'].select(
                'IJSONSchema', cnx, etype='Photo')
            view_schema = adapter.view_schema()
            self._check_schema(view_schema)
            creation_schema = adapter.creation_schema()
            self._check_schema(creation_schema, True)

    def test_entity_schema(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity('Photo', data=Binary(b'plop'))
            adapter = entity.cw_adapt_to('IJSONSchema')
            view_schema = adapter.view_schema()
            self._check_schema(view_schema)
            edition_schema = adapter.edition_schema()
            self._check_schema(edition_schema, True)

    def _check_schema(self, schema, edition_role=False):
        self.assertIn('exif_data', schema['properties'])
        self.maxDiff = None
        expected = {
            'title': u'EXIF data',
            'type': 'object',
            'properties': {
                'exposure_time': {
                    'title': u'exposure_time',
                    'type': 'number',
                },
                'flash': {
                    'title': u'flash',
                    'type': 'boolean',
                },
                'maker_note': {
                    'title': u'maker_note',
                    'type': 'string',
                },
            },
            'additionalProperties': False,
        }
        if edition_role:
            expected['required'] = ['flash']
            expected['properties']['flash']['default'] = False
        self.assertEqual(schema['definitions']['EXIF data'], expected)

    def test_entity_serialize(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity(
                'Photo', data=Binary(b'plop'),
                exposure_time=1.23, flash=False)
            adapter = entity.cw_adapt_to('IJSONSchema')
            schema = adapter.view_schema()
            self._check_schema(schema)
            instance = adapter.serialize()
            try:
                jsonschema.validate(instance, schema)
            except jsonschema.ValidationError as exc:
                self.fail(str(exc))

    def test_entity_create(self):
        with self.admin_access.cnx() as cnx:
            adapter = cnx.vreg['adapters'].select(
                'IJSONSchema', cnx, etype='Photo')
            self._check_insert(cnx, adapter.create_entity)

    def test_entity_create_no_compound_data(self):
        with self.admin_access.cnx() as cnx:
            adapter = cnx.vreg['adapters'].select(
                'IJSONSchema', cnx, etype='Photo')
            instance = {
                'data': u'plip',
                'media_type': 'jpeg',
            }
            adapter.create_entity(instance)
            cnx.commit()
            entity = cnx.find('Photo').one()
            self.assertEqual(entity.data.getvalue(), b'plip')
            self.assertEqual(entity.flash, False)  # default value

    def test_entity_update(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity(
                'Photo', data=Binary(b'plop'))
            cnx.commit()
            adapter = entity.cw_adapt_to('IJSONSchema')
            self._check_insert(cnx, adapter.edit_entity)

    def _check_insert(self, cnx, insert_function):
        instance = {
            'data': 'plip',
            'media_type': 'jpeg',
            'exif_data': {
                'flash': True,
                'exposure_time': 0.9,
            },
        }
        insert_function(instance)
        cnx.commit()
        entity = cnx.find('Photo').one()
        self.assertEqual(entity.flash, True)
        self.assertEqual(entity.exposure_time, 0.9)
        self.assertEqual(entity.media_type, u'jpeg')

    def test_nonfinal_relation_schema(self):

        class bin_data(CompoundMapper):
            etype = 'Photo'
            relations = ('data', 'thumbnail')
            title = _('Photo data')

        expected_schema = {
            '$ref': '#/definitions/Photo data',
            'definitions': {
                'Photo data': {
                    'title': 'Photo data',
                    'type': 'object',
                    'properties': {
                        'data': {
                            'title': 'data',
                            'type': 'string',
                        },
                        'thumbnail': {
                            'items': {
                                '$ref': '#/definitions/Thumbnail',
                            },
                            'title': 'thumbnail',
                            'type': 'array',
                        },
                    },
                    'additionalProperties': False,
                },
                'Thumbnail': {
                    'title': 'Thumbnail',
                    'type': 'object',
                    'properties': {
                        'data': {
                            'title': 'data',
                            'type': 'string',
                        },
                    },
                    'additionalProperties': False,
                },
            },
        }

        with self.temporary_appobjects(bin_data):
            with self.admin_access.cnx() as cnx:
                mapper = self.mapper_by_name('bin_data')(cnx)
                schema = mapper.jsl_field(VIEW_ROLE).get_schema()
                self.assertEqual(schema, expected_schema)

    def test_nonfinal_relation_values(self):

        class bin_data(CompoundMapper):
            etype = 'Photo'
            relations = ('data', 'thumbnail')
            title = _('Photo data')

        with self.temporary_appobjects(bin_data):
            with self.admin_access.cnx() as cnx:
                mapper = self.mapper_by_name('bin_data')(cnx)
                instance = {
                    'bin_data': {
                        'data': 'plip',
                        'thumbnail': [
                            {
                                'data': 'plop',
                            },
                        ],
                    },
                }
                values = mapper.values(None, instance)
                self.assertCountEqual(list(values), ['data', 'thumbnail'])
                # A Thumbnail entity should have been created.
                thumbnail = cnx.find('Thumbnail').one()
                self.assertEqual(values['thumbnail'], [thumbnail])

    def test_object_relation(self):

        class my_compound(CompoundMapper):
            name = 'My Compound'
            title = 'My Title'
            etype = 'Author'
            relations = (
                ('author', 'object'),
            )

        expected_schema = {
            "$schema": "http://json-schema.org/draft-06/schema#",
            "type": "object",
            "title": u"Author",
            "additionalProperties": False,
            "properties": {
                "name": {"title": u"name", "type": "string"},
                "My Compound": {
                    "$ref": "#/definitions/My Title",
                },
            },
            "definitions": {
                "My Title": {
                    "type": "object",
                    "title": u"My Title",
                    "additionalProperties": False,
                    "properties": {
                        "reverse_author": {
                            "title": u"author_object",
                            "items": {
                                "oneOf": [],
                                "type": "string",
                            },
                            "type": "array",
                        },
                    },
                },
            },
        }

        with self.temporary_appobjects(my_compound):
            with self.admin_access.cnx() as cnx:
                author = cnx.create_entity(
                    'Author', name=u'author')
                cnx.create_entity(
                    'Book', author=author, title=u'title')

                adapter = author.cw_adapt_to('IJSONSchema')
                schema = adapter.view_schema()
                self.assertEqual(expected_schema, schema)


class EntityMapperTC(CubicWebTC):

    def test__object_mappers(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='Photo')
            self.assertEqual([f.name for f in mapper._object_mappers()],
                             ['exif_data'])

    def test_etypemapper_relations(self):
        expected_rtypes = ['login', 'firstname', 'surname',
                           'last_login_time', 'in_group', 'use_email',
                           'picture']
        with self.admin_access.cnx() as cnx:
            user = cnx.find('CWUser', login=u'admin').one()
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, entity=user)
            rtypes = [rtype
                      for rtype, _, _ in mapper.relations(VIEW_ROLE)]
            self.assertCountEqual(expected_rtypes, rtypes)
            self.create_user(cnx, u'bob')
            cnx.commit()
        with self.new_access(u'bob').cnx() as cnx:
            user = cnx.find('CWUser', login=u'admin').one()
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, entity=user)
            rtypes = [rtype
                      for rtype, _, _ in mapper.relations(VIEW_ROLE)]
            self.assertCountEqual(expected_rtypes, rtypes)

    def test_etypemapper_relations_accounts_for_uicfg(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='CWUser')
            fields = dict(
                (rtype, targets)
                for rtype, _, targets in mapper.relations(VIEW_ROLE))
            # EmailAlias no in, per jsonschema_section.
            self.assertEqual(fields['use_email'], {'EmailAddress'})

    def test_targetetypemapper_relations_and_schema(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='Thumbnail',
                rtype='thumbnail', role='object',
            )
            self._check_thumbnail_relations_and_schema(mapper)

    def test_targetentitymapper_relations_and_schema(self):
        with self.admin_access.cnx() as cnx:
            thumbnail = cnx.create_entity('Thumbnail', data=Binary(b'plip'))
            cnx.create_entity('Photo', data=Binary(b'plop'),
                              thumbnail=thumbnail)
            cnx.commit()
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, entity=thumbnail,
                rtype='thumbnail', role='object',
            )
            self._check_thumbnail_relations_and_schema(mapper)

    def _check_thumbnail_relations_and_schema(self, mapper):
        relations = [(rtype, role)
                     for rtype, role, _ in mapper.relations('view')]
        self.assertEqual([('data', 'subject')], relations)
        relations = [(rtype, role)
                     for rtype, role, _ in mapper.relations('creation')]
        self.assertEqual([('data', 'subject')], relations)
        schema = mapper.jsl_document(VIEW_ROLE).get_schema()
        expected = {
            '$schema': 'http://json-schema.org/draft-06/schema#',
            'title': 'Thumbnail',
            'type': 'object',
            'properties': {
                'data': {
                    'title': 'data',
                    'type': 'string',
                },
            },
            'additionalProperties': False,
        }
        self.assertEqual(schema, expected)

    def test_relation_targets(self):
        with self.admin_access.cnx() as cnx:
            dinosaurs = cnx.create_entity('Topic', name=u'Dinosaurs')
            monsters = cnx.create_entity('Topic', name=u'Monsters')
            programming = cnx.create_entity('Topic', name=u'Programming')
            book = cnx.create_entity('Book', title=u'Creatures', topics=[
                                     dinosaurs, monsters])

            mapper = cnx.vreg['mappers'].select(
                'jsonschema.relation', cnx, entity=book,
                rtype='topics', role='subject',
                target_types={'Topic'})

            # Only related entities appear in view schema
            view_targets = [
                target.eid for target in mapper.relation_targets(VIEW_ROLE)]
            self.assertIn(dinosaurs.eid, view_targets)
            self.assertIn(monsters.eid, view_targets)
            self.assertNotIn(programming.eid, view_targets)

            # All entities that could be related appear in edition schema
            targets = [
                target.eid for target in mapper.relation_targets(EDITION_ROLE)]
            self.assertIn(dinosaurs.eid, targets)
            self.assertIn(monsters.eid, targets)
            self.assertIn(programming.eid, targets)

            # Only unrelated entities appear in creation schema
            targets = [
                target.eid for target in mapper.relation_targets(CREATION_ROLE)]
            self.assertNotIn(dinosaurs.eid, targets)
            self.assertNotIn(monsters.eid, targets)
            self.assertIn(programming.eid, targets)

    def test_schema(self):
        expected = {
            '$schema': 'http://json-schema.org/draft-06/schema#',
            'title': 'Photo',
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'data': {
                    'title': 'data',
                    'type': 'string',
                },
                'exif_data': {
                    '$ref': '#/definitions/EXIF data',
                },
                'media_type': {
                    'title': 'media_type',
                    'type': 'string',
                },
                'thumbnail': {
                    'items': {
                        '$ref': '#/definitions/Thumbnail',
                    },
                    'title': 'thumbnail',
                    'type': 'array',
                },
            },
            'definitions': {
                'EXIF data': {
                    'additionalProperties': False,
                    'properties': {
                        'exposure_time': {
                            'title': 'exposure_time',
                            'type': 'number',
                        },
                        'flash': {
                            'title': 'flash',
                            'type': 'boolean',
                        },
                        'maker_note': {
                            'title': 'maker_note',
                            'type': 'string',
                        },
                    },
                    'title': 'EXIF data',
                    'type': 'object',
                },
                'Thumbnail': {
                    'additionalProperties': False,
                    'properties': {
                        'data': {
                            'title': 'data',
                            'type': 'string',
                        },
                    },
                    'title': 'Thumbnail',
                    'type': 'object',
                },
            },
        }
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='Photo')
            view_schema = mapper.jsl_document('view').get_schema()
            self.assertEqual(view_schema, expected)
            creation_schema = mapper.jsl_document('creation').get_schema()

            # Update expected schema to insert constraints.
            expected['required'] = ['data', 'media_type']
            expected['definitions'][
                'EXIF data']['properties']['flash']['default'] = False
            expected['definitions']['EXIF data']['required'] = ['flash']
            expected['properties']['media_type']['default'] = 'png'
            del expected['properties']['media_type']['type']
            expected['properties']['media_type']['oneOf'] = [
                {'enum': ['jpeg'], 'title': 'jpeg', 'type': 'string'},
                {'enum': ['png'], 'title': 'png', 'type': 'string'},
            ]
            expected['properties']['thumbnail']['maxItems'] = 1
            expected['properties']['thumbnail']['minItems'] = 0
            expected['definitions']['Thumbnail']['required'] = ['data']
            self.assertEqual(creation_schema, expected)

    def test_values_creation(self):
        with self.admin_access.cnx() as cnx:
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, etype='Photo')
            instance = {'data': 'plip'}
            values = mapper.values(instance)
            self.assertEqual(list(values), ['data'])
            self.assertEqual(values['data'].getvalue(), b'plip')
            instance = {
                'data': 'plip',
                'thumbnail': [
                    {
                        'data': 'plop',
                    },
                ],
            }
            values = mapper.values(instance)
            self.assertCountEqual(list(values), ['data', 'thumbnail'])
            self.assertEqual(values['data'].getvalue(), b'plip')
            thumbnail, = values['thumbnail']
            self.assertEqual(thumbnail.cw_etype, 'Thumbnail')
            # Custom "base64" mapper for Thumbnail's data attribute.
            self.assertEqual(thumbnail.data.getvalue(),
                             base64.b64decode(b'plop'))

    def test_values_update(self):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity('Photo', data=Binary(b'plop'),
                                       flash=True,
                                       exposure_time=1.23)
            cnx.create_entity('Thumbnail', data=Binary(b'plip'),
                              reverse_thumbnail=entity)
            cnx.commit()
            mapper = cnx.vreg['mappers'].select(
                'jsonschema.entity', cnx, entity=entity)
            instance = {'data': 'plip', 'media_type': u'jpeg'}
            values = mapper.values(instance.copy())
            # All subject relations should appear in "values"
            subjrels = [rschema.type
                        for rschema in entity.e_schema.subject_relations()
                        if not rschema.meta]
            self.assertCountEqual(list(values), subjrels)
            self.assertEqual(values['data'].getvalue(), b'plip')
            self.assertEqual(values['media_type'], u'jpeg')
            # These are absent from instance, so should be reset to None.
            self.assertIsNone(values['exposure_time'])
            self.assertIsNone(values['maker_note'])
            self.assertEqual(values['thumbnail'], [])
            # "flash" has a default value.
            self.assertEqual(values['flash'], False)
            # inlined-related entities should have been dropped.
            self.assertFalse(cnx.find('Thumbnail'))


class PredicatesTC(CubicWebTC):

    def test_yams_match_base(self):
        predicate = yams_match(etype='etype', rtype='rtype', role='role')

        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='role',
                                   target_types={'CWGroup'}),
                         3)
        self.assertEqual(predicate(None, None,
                                   etype='notetype', rtype='rtype', role='role',
                                   target_types={'CWGroup'}),
                         0)
        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='notrtype', role='role',
                                   target_types={'CWGroup'}),
                         0)
        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='notrole',
                                   target_types={'CWGroup'}),
                         0)

    def test_yams_match_entity(self):
        predicate = yams_match(etype='CWUser')
        with self.admin_access.client_cnx() as cnx:
            bob = cnx.create_entity('CWUser', upassword=u'123', login=u'bob')
            self.assertEqual(predicate(None, None,
                                       entity=bob, rtype='rtype', role='role',
                                       target_types=set([])),
                             1)
        predicate = yams_match(etype='CWUser', rtype='upassword',
                               role='subject', target_types='Bytes')
        with self.admin_access.client_cnx() as cnx:
            bob = cnx.create_entity('CWUser', upassword=u'123', login=u'bob')
            self.assertEqual(predicate(None, None,
                                       entity=bob, rtype='upassword',
                                       role='subject', target_types={'Bytes'}),
                             4)

    def test_yams_match_target_types(self):
        predicate = yams_match(target_types='String')

        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='role',
                                   target_types={'CWGroup'}),
                         0)
        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='role',
                                   target_types={'String'}),
                         1)
        predicate = yams_match(target_types={'CWUser', 'CWGroup'})
        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='role',
                                   target_types={'CWUser', 'CWGroup'}),
                         1)
        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='role',
                                   target_types={'CWUser'}),
                         1)

    def test_yams_match_all(self):
        predicate = yams_match(etype='Photo', rtype='data', role='subject',
                               target_types='Bytes')

        self.assertEqual(predicate(None, None,
                                   etype='etype', rtype='rtype', role='role',
                                   target_types={'CWGroup'}),
                         0)
        self.assertEqual(predicate(None, None,
                                   etype='Thumbnail', rtype='data',
                                   role='subject', target_types={'Bytes'}),
                         0)
        self.assertEqual(predicate(None, None,
                                   etype='Photo', rtype='data', role='subject',
                                   target_types={'Bytes'}),
                         4)


if __name__ == '__main__':
    unittest.main()
