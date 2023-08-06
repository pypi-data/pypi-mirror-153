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

"""cubicweb-jsonschema views tests"""


from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_jsonschema.views import (
    jsonschema_section,
)


class JSONSchemaRelationTagsTC(CubicWebTC):

    def test__init(self):
        tagdefs = jsonschema_section._tagdefs
        for tagged, expected_section in (
            # meta rtype
            (('Book', 'eid', 'Int', 'subject'), 'hidden'),
            # ignored rtypes
            (('Book', 'created_by', 'CWUser', 'subject'), 'hidden'),
            # attribute
            (('Book', 'title', 'String', 'subject'), 'inlined'),
            # inlined relation, role-cardinality '1' or '+'
            (('CWUser', 'in_group', 'CWGroup', 'subject'), 'inlined'),
            # inlined relation, composite
            (('CWUser', 'use_email', 'EmailAddress', 'object'), 'inlined'),
            # plain relation
            (('Book', 'topics', 'Topic', 'subject'), 'related'),
            (('Book', 'topics', 'Topic', 'object'), 'related'),
            # computed relation
            (('Author', 'publications', 'Book', 'object'), 'related'),
        ):
            with self.subTest(tagged=tagged):
                self.assertEqual(tagdefs[tagged], expected_section)

    def fake_entity(self, cnx, etype):
        return self.vreg['etypes'].etype_class(etype)(cnx)

    def rtag(self, cnx, entity):
        return self.vreg['uicfg'].select('jsonschema', cnx, entity=entity)

    def test_relations_by_section_password(self):
        """upassword for CWUser is listed for "add" action, not for "read"."""
        with self.admin_access.cnx() as cnx:
            entity = self.fake_entity(cnx, 'CWUser')
            rsection = self.rtag(cnx, entity)
            for rtype, _, _ in rsection.relations_by_section(
                    entity, 'inlined', 'read'):
                if rtype == u'upassword':
                    self.fail('"upassword" unexpectedly found')
            add_rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'inlined', 'add')]
            self.assertIn(u'upassword', add_rtypes)

    def test_relations_by_section_ignored(self):
        """meta rtypes are not listed."""
        with self.admin_access.cnx() as cnx:
            entity = self.fake_entity(cnx, 'Book')
            rsection = self.rtag(cnx, entity)
            read_rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'inlined', 'read')]
            self.assertNotIn('eid', read_rtypes)
            add_rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'related', 'add')]
            self.assertNotIn('custom_workflow', add_rtypes)

    def test_relations_by_section_inlined(self):
        with self.admin_access.cnx() as cnx:
            entity = self.fake_entity(cnx, 'Book')
            rsection = self.rtag(cnx, entity)
            rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'inlined', 'read')]
            self.assertCountEqual(['title', 'publication_date'], rtypes)

    def test_relations_by_section_related(self):
        with self.admin_access.cnx() as cnx:
            entity = self.fake_entity(cnx, 'Book')
            rsection = self.rtag(cnx, entity)
            rtypes = [rtype for rtype, _, _ in rsection.relations_by_section(
                entity, 'related', 'read')]
            self.assertCountEqual(['author', 'publications', 'topics'],
                                  rtypes)

    def test_relations_by_section_inlined_permissions(self):
        with self.admin_access.cnx() as cnx:
            cnx.create_entity('Book', title=u't')
            self.create_user(cnx, u'bob')
            cnx.commit()
        with self.new_access(u'bob').cnx() as cnx:
            entity = cnx.find('Book').one()
            rsection = self.rtag(cnx, entity)
            read_rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'inlined', 'read')]
            self.assertCountEqual(['title', 'publication_date'], read_rtypes)
            update_rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'inlined', 'update')]
            self.assertCountEqual([], update_rtypes)

    def test_relations_by_section_related_permissions(self):
        with self.admin_access.cnx() as cnx:
            author = cnx.create_entity('Author', name=u'a')
            cnx.create_entity('Book', title=u't', author=author)
            self.create_user(cnx, u'bob')
            cnx.commit()
        with self.new_access(u'bob').cnx() as cnx:
            entity = cnx.find('Book').one()
            rsection = self.rtag(cnx, entity)
            update_rtypes = [
                rtype for rtype, _, _ in rsection.relations_by_section(
                    entity, 'related', 'add')]
            self.assertCountEqual(['topics'],
                                  update_rtypes)


if __name__ == '__main__':
    import unittest
    unittest.main()
