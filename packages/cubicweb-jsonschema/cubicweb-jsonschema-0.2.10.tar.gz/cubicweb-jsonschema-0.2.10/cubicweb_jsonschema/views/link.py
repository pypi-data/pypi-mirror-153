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

"""cubicweb-jsonschema hyper schema "link" components.

See http://json-schema.org/draft-06/links for the JSON schema of these
objects.
"""


from cubicweb.appobject import AppObject
from cubicweb.predicates import has_permission, match_kwargs

from .. import VIEW_ROLE, CREATION_ROLE, EDITION_ROLE


class Link(AppObject):
    """Abstract hyper schema link."""
    __registry__ = 'links'

    def description_object(self, request, resource):
        """Return the link description object as a dict."""
        raise NotImplementedError()


class CollectionLink(Link):
    """Link for a collection."""
    __regid__ = 'collection'
    __select__ = match_kwargs('title')
    rel = 'collection'

    @property
    def title(self):
        return self.cw_extra_kwargs['title']

    def description_object(self, request, resource):
        return {
            u'href': request.resource_path(resource),
            u'rel': self.rel,
            u'targetSchema': {
                u'$ref': request.resource_path(resource, 'schema'),
            },
            u'submissionSchema': {
                u'$ref': request.resource_path(resource, 'schema',
                                               query={'role': CREATION_ROLE}),
            },
            u'title': self.title,
        }


class CollectionItemLink(Link):
    """Link for a collection item."""
    __regid__ = 'collection-item'
    __select__ = match_kwargs('anchor')
    rel = 'item'

    def description_object(self, request, resource):
        href = request.resource_path(resource) + '{id}'
        return {
            u'href': href,
            u'rel': self.rel,
            u'anchor': self.cw_extra_kwargs['anchor'],
        }


class ETypeLink(CollectionLink):
    """Link for a collection of entities of the same type."""
    __regid__ = 'collection.etype'
    __select__ = match_kwargs('etype')
    rel = 'self'

    @property
    def title(self):
        etype = self.cw_extra_kwargs['etype']
        return self._cw.__(etype + '_plural')


class EntityLink(Link):
    """Abstract hyper schema link suitable for entity JSON schema."""
    __abstract__ = True
    __select__ = match_kwargs('entity')

    @property
    def entity(self):
        return self.cw_extra_kwargs['entity']


class EntitySelfLink(EntityLink):
    """Link for an entity as rel="self"."""
    __regid__ = 'entity.self'
    __select__ = EntityLink.__select__ & has_permission('read')

    def description_object(self, request, resource):
        entity = self.entity
        title = self._cw._('{0} #{1}').format(
            self._cw.__(entity.cw_etype), entity.eid)
        return {
            u'href': request.resource_path(resource),
            u'rel': u'self',
            u'title': title,
            u'submissionSchema': {
                u'$ref': request.resource_path(
                    resource, 'schema', query={'role': EDITION_ROLE}),
            },
            u'targetSchema': {
                u'$ref': request.resource_path(
                    resource, 'schema', query={'role': VIEW_ROLE}),
            },
        }


class EntityParentLink(EntityLink):
    """Link to the parent resource of an entity (i.e. the entity type)."""
    __regid__ = 'entity.type'
    rel = u'up'

    def description_object(self, request, resource):
        return {
            u'href': request.resource_path(resource.__parent__),
            u'rel': self.rel,
            u'title': self._cw.__('{0}_plural').format(self.entity.cw_etype),
            u'targetSchema': {
                u'$ref': request.resource_path(
                    resource.__parent__, 'schema'),
            },
        }


class EntityCollectionLink(EntityParentLink):
    """Link for an entity as item of a collection."""
    __regid__ = 'entity.collection'
    rel = u'collection'


class EntityRelatedLink(EntityLink):
    """Link to (`rtype`, `role`) relation from `entity` as `role`.
    """
    __regid__ = 'entity.related'
    __select__ = match_kwargs('entity', 'rtype', 'role')

    def description_object(self, request, resource):
        assert resource.__class__.__name__ == 'EntityResource'  # XXX debug
        rtype = self.cw_extra_kwargs['rtype']
        role = self.cw_extra_kwargs['role']
        collection_mapper = self._cw.vreg['mappers'].select(
            'jsonschema.collection', self._cw, rtype=rtype, role=role)
        title = collection_mapper.title
        return {
            u'href': request.resource_path(resource[rtype]),
            u'rel': u'related',
            u'title': title,
        }


class RelatedCollectionLink(CollectionLink):
    """rel="self" link for collection of related entities."""
    __regid__ = 'related-collection'
    rel = 'self'

    def description_object(self, request, resource):
        ldo = super(RelatedCollectionLink, self).description_object(
            request, resource)
        ldo['targetSchema']['$ref'] = request.resource_path(
            resource, 'schema', query={'role': VIEW_ROLE})
        return ldo
