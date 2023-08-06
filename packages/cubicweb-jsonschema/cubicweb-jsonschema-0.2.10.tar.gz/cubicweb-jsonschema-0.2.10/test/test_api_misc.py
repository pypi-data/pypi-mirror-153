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

"""cubicweb-jsonschema unit tests for Pyramid JSON API."""

import base64
from datetime import date
from unittest import skip

import jsonschema
from mock import patch

from cubicweb import Binary, ValidationError
from cubicweb.pyramid.test import PyramidCWTest

from cubicweb_jsonschema import VIEW_ROLE
from cubicweb_jsonschema.entities.ijsonschema import (
    jsonschema_adapter,
)


class BaseTC(PyramidCWTest):

    settings = {
        'cubicweb.bwcompat': False,
        'pyramid.debug_notfound': True,
        'cubicweb.auth.authtkt.session.secret': 'x',
        'cubicweb.auth.authtkt.persistent.secret': 'x',
        'cubicweb.session.secret': 'x',
    }

    def includeme(self, config):
        config.include('cubicweb_jsonschema.api')


class EntitiesTC(BaseTC):

    @skip('todo')
    def test_post_json_file_upload(self):
        data = {
            'login': u'bob',
            'upassword': u'bob',
            'picture': [{
                u'data': u'data:text/xml;name=test;base64,{}'.format(
                    base64.b64encode('hello')),
            }],
        }
        self.login()
        resp = self.webapp.post_json('/cwuser/', data, status=201,
                                     headers={'Accept': 'application/json'})
        with self.admin_access.cnx() as cnx:
            entity = cnx.find('CWUser', login=u'bob').one()
            self.assertTrue(entity.picture)
            photo = entity.picture[0]
            self.assertEqual(photo.read(), 'hello')
        self.assertEqual(
            resp.location, 'https://localhost:80/CWUser/%d' % entity.eid)

    @skip('todo')
    def test_post_json_file_upload_badrequest(self):
        self.login()
        for rtype, value in [
            ('unknown', [{'data': u'who cares?'}]),
            ('picture', [{'data': u'badprefix:blah blah'}]),
            ('picture', {'data': u'not in a list'}),
        ]:
            data = {rtype: value}
            with self.subTest(**data):
                data[u'login'] = u'bob'
                data[u'upassword'] = u'bob'
                # Rely on "status=400" for test assertion.
                self.webapp.post_json('/CWUser/', data, status=400,
                                      headers={'Accept': 'application/json'})

    def test_get_related(self):
        with self.admin_access.cnx() as cnx:
            book = cnx.create_entity('Book', title=u'title')
            author = cnx.create_entity('Author', name=u'bob',
                                       reverse_author=book)
            jschema = self.vreg['adapters'].select(
                'IJSONSchema', cnx, entity=author,
                rtype='author', role='object').view_schema()
            cnx.commit()
        url = '/book/%s/author' % book.eid
        res = self.webapp.get(url, headers={'accept': 'application/json'})
        related = res.json
        expected = [{
            'type': u'author',
            'id': str(author.eid),
            'title': u'bob',
        }]
        with self.admin_access.cnx() as cnx:
            collection_mapper = cnx.vreg['mappers'].select(
                'jsonschema.collection', cnx, etype='Author')
            jschema = collection_mapper.jsl_field(VIEW_ROLE).get_schema()
        jsonschema.validate(related, jschema)
        self.assertEqual(related, expected)

    def test_post_related_bad_identifier(self):
        with self.admin_access.cnx() as cnx:
            book = cnx.create_entity('Book', title=u'title')
            cnx.commit()
        self.login()
        url = '/book/%s/author' % book.eid
        res = self.webapp.post_json(url, ['a'], status=400,
                                    headers={'accept': 'application/json'})
        self.assertIn('invalid target identifier(s)', res.json['message'])

    def test_post_related_bad_role(self):
        with self.admin_access.cnx() as cnx:
            author = cnx.create_entity('Author', name=u'bob')
            cnx.commit()
        self.login()
        url = '/author/%s/author' % author.eid
        res = self.webapp.post_json(url, [], status=404,
                                    headers={'accept': 'application/json'})
        self.assertIn('relation author-subject not found on Author',
                      res.json['message'])

    def test_post_related_entity_notfound(self):
        self.login()
        url = '/book/999/author'
        self.webapp.post_json(url, [], status=404,
                              headers={'accept': 'application/json'})

    def test_post_related_bad_target(self):
        with self.admin_access.cnx() as cnx:
            book = cnx.create_entity('Book', title=u'title')
            cnx.commit()
            cwuser_eid = cnx.find('CWUser', login=u'admin')[0][0]
        self.login()
        url = '/book/%s/author' % book.eid
        # TODO: status should be 4xx
        self.webapp.post_json(url, [str(cwuser_eid)], status=500,
                              headers={'accept': 'application/json'})

    def test_put_with_incomplete_data(self):
        """A PUT request *replaces* entity attributes, so if fields are
        missing from JSON request body, respective attributes are reset.
        """
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity('Photo', data=Binary(b'plop'),
                                       flash=True,
                                       exposure_time=1.23)
            cnx.create_entity('Thumbnail', data=Binary(b'plip'),
                              reverse_thumbnail=entity)
            cnx.commit()
        self.login()
        url = '/photo/{}/'.format(entity.eid)
        self.webapp.put_json(url, {'data': 'plip', 'media_type': u'jpeg'},
                             headers={'Accept': 'application/json'})
        with self.admin_access.cnx() as cnx:
            entity = cnx.entity_from_eid(entity.eid)
            self.assertEqual(entity.data.getvalue(), b'plip')
            self.assertEqual(entity.media_type, u'jpeg')
            # 'thumbnail' absent from request body, we should get ().
            self.assertEqual(entity.thumbnail, ())
            self.assertFalse(cnx.find('Thumbnail'))
            # 'flash' has a default value, we should get this back.
            self.assertEqual(entity.flash, False)
            # 'exposure_time' absent from request body, we should get None.
            self.assertIsNone(entity.exposure_time)

    def test_get_related_sort(self):
        """Sort by modification_date ascending and descending"""
        with self.admin_access.cnx() as cnx:
            author = cnx.create_entity(
                'Author', name=u'bob')
            book1 = cnx.create_entity(
                'Book', title=u'1',
                publication_date=date(1976, 3, 1),
                author=author,
            )
            book2 = cnx.create_entity(
                'Book', title=u'1',
                publication_date=date(1977, 3, 1),
                author=author,
            )
            cnx.commit()

        ascending = [book1.title, book2.title]
        descending = ascending[::-1]
        for sort, expected in [
            ('publication_date', ascending),
            ('-publication_date', descending),
        ]:
            with self.subTest(sort=sort):
                url = ('/author/%s/publications?sort=%s'
                       % (author.eid, sort))
                res = self.webapp.get(
                    url, headers={'accept': 'application/json'})
                entities = res.json
                self.assertEqual(len(entities), 2)
                ids = [d['title'] for d in entities]
                self.assertEqual(ids, expected)

    def test_add_related(self):
        """POST on /<etype>/<eid>/relationships/<rtype> with primary entity as
        subject of <rtype>.
        """
        with self.admin_access.repo_cnx() as cnx:
            book = cnx.create_entity('Book', title=u'tmp')
            cnx.commit()
        url = '/book/%d/relationships/author' % book.eid
        data = {
            'name': u'bob',
        }
        self.login()
        res = self.webapp.post_json(url, data, status=201,
                                    headers={'accept': 'application/json'})
        entity = res.json
        with self.admin_access.cnx() as cnx:
            author_eid = cnx.find('Author').one().eid
            jschema = jsonschema_adapter(
                cnx, etype='Author').view_schema()
        self.assertEqual(
            res.location,
            'https://localhost:80/author/{}/'.format(author_eid))
        jsonschema.validate(entity, jschema)
        self.assertEqual(entity['name'], u'bob')
        with self.admin_access.cnx() as cnx:
            rset = cnx.execute(
                'Any A WHERE B author A, B eid %(b)s, A name "bob"',
                {'b': book.eid})
        self.assertTrue(rset)

    def test_add_related_object(self):
        """POST on /<etype>/<eid>/relationships/<rtype> with primary entity as
        object of <rtype>.
        """
        with self.admin_access.repo_cnx() as cnx:
            author = cnx.create_entity('Author', name=u'bob')
            cnx.commit()
        url = '/author/%s/relationships/author' % author.eid
        data = {
            'title': u'introducing cubicweb-jsonschema',
        }
        self.login()
        res = self.webapp.post_json(url, data, status=201,
                                    headers={'accept': 'application/json'})
        entity = res.json
        with self.admin_access.cnx() as cnx:
            book_eid = cnx.find('Book').one().eid
            jschema = jsonschema_adapter(
                cnx, etype='Book').view_schema()
        self.assertEqual(
            res.location,
            'https://localhost:80/book/{}/'.format(book_eid))
        jsonschema.validate(entity, jschema)
        self.assertEqual(entity['title'], u'introducing cubicweb-jsonschema')
        with self.admin_access.cnx() as cnx:
            rset = cnx.execute(
                'Any X WHERE X author A, A eid %(a)s,'
                ' X title "introducing cubicweb-jsonschema"',
                {'a': author.eid})
        self.assertTrue(rset)

    def test_validationerror_additionalproperties(self):
        data = {
            u'name': u'bob',
            u'born': u'1986',
        }
        self.login()
        res = self.webapp.post_json('/author/', data, status=422,
                                    headers={'Accept': 'application/json'})
        self.assertEqual(res.content_type, 'application/problem+json')
        self.assertEqual(res.json_body, {
            u'status': 422,
            u'title': u'Unprocessable Entity',
            u'detail': u'unexpected properties: born',
        })

    def test_validationerror_nosource(self):
        """Test validation_failed view with no specific source entry."""
        with self.admin_access.cnx() as cnx:
            gid = cnx.find('CWGroup', name=u'users')[0][0]
        data = {
            'login': u'bob',
            'upassword': u'pass',
            'in_group': [str(gid)],
        }
        with patch('cubicweb.req.RequestSessionBase.create_entity',
                   side_effect=ValidationError(None, {None: u'unmapped'})):
            self.login()
            res = self.webapp.post_json('/cwuser/', data, status=422,
                                        headers={'Accept': 'application/json'})
            self.assertEqual(res.content_type, 'application/problem+json')
            self.assertEqual(res.json_body, {
                u'status': 422,
                u'title': u'Unprocessable Entity',
                u'detail': u'unmapped',
            })

    def test_validationerror_integrityerror(self):
        with self.admin_access.cnx() as cnx:
            gid = cnx.find('CWGroup', name=u'users')[0][0]
            self.create_user(cnx, u'bob')
            cnx.commit()
        data = {
            'login': 'bob',
            'upassword': 'pass',
            'in_group': [str(gid)],
        }
        self.login()
        res = self.webapp.post_json('/cwuser/', data, status=422,
                                    headers={'Accept': 'application/json'})
        self.assertEqual(res.content_type, 'application/problem+json')
        self.assertEqual(res.json_body, {
            u'status': 422,
            u'title': u'Unprocessable Entity',
            u'detail': u'some relations violate a unicity constraint',
            u'invalid-params': [
                {u'name': u'login',
                 u'reason': u'login is part of violated unicity constraint'}],
        })

    def test_exception(self):
        with self.admin_access.cnx() as cnx:
            gid = cnx.find('CWGroup', name=u'users')[0][0]
        data = {
            'login': 'bob',
            'upassword': 'pass',
            'in_group': [str(gid)],
        }
        self.login()
        error = ValueError("invalid literal for int() with base 10: 'foo'")
        with patch('cubicweb.req.RequestSessionBase.create_entity',
                   side_effect=error):
            res = self.webapp.post_json('/cwuser/', data, status=500,
                                        headers={'Accept': 'application/json'})
            self.assertEqual(res.content_type, 'application/problem+json')
            self.assertEqual(res.json_body, {
                u'status': 500,
                u'title': u'Internal Server Error',
                u'detail': u"invalid literal for int() with base 10: 'foo'",
            })

    def test_exception_no_detail(self):
        data = {'title': 'thing'}
        self.login()

        with patch('cubicweb.req.RequestSessionBase.create_entity',
                   side_effect=NotImplementedError()):
            res = self.webapp.post_json('/book/', data, status=500,
                                        headers={'Accept': 'application/json'})
            self.assertEqual(res.content_type, 'application/problem+json')
            self.assertEqual(res.json_body, {
                u'status': 500,
                u'title': u'Internal Server Error',
            })


if __name__ == '__main__':
    import unittest
    unittest.main()
