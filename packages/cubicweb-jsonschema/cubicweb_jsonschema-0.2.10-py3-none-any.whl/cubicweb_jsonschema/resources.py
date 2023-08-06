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

"""cubicweb-jsonschema Pyramid "entities" resources definitions."""

from functools import wraps

from six import text_type

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound

from rql import nodes, TypeResolverException


def parent(init_method):
    """Decorator for resource class's __init__ method to bind the __parent__
    attribute to instance.
    """
    @wraps(init_method)
    def wrapper(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        init_method(self, *args, **kwargs)
        self.__parent__ = parent

    return wrapper


def find_relationship(schema, etype, rtype):
    """Return (`rtype`, `role`) if `etype` has a relationship `rtype` else
    raise a ValueError.
    """
    eschema = schema[etype]
    for relinfo in eschema.relation_definitions():
        rschema, __, role = relinfo
        if rschema.final or rschema.meta:
            continue
        if rschema.type == rtype:
            return relinfo
    raise ValueError(rtype)


class RootResource(object):
    """Root resources for entities."""
    __parent__ = None
    __name__ = ''

    def __init__(self, request):
        self.request = request

    def __getitem__(self, value):
        try:
            return ETypeResource(self.request, value, self)
        except KeyError:
            raise KeyError(value)


class ETypeResource(object):
    """A resource class for an entity type."""

    @classmethod
    def from_match(cls, matchname):
        def factory(request):
            return cls(request, request.matchdict[matchname])
        return factory

    def __init__(self, request, etype, parent=None):
        vreg = request.registry['cubicweb.registry']
        self.request = request
        self.etype = vreg.case_insensitive_etypes[etype.lower()]
        self.cls = vreg['etypes'].etype_class(self.etype)
        if parent is None:
            parent = RootResource(request)
        self.__parent__ = parent
        self.__name__ = self.etype.lower()

    def __getitem__(self, value):
        if value == 'relationships':
            return _RelationshipProxyResource(self.request, self.etype)
        for attrname in ('eid', self.cls.cw_rest_attr_info()[0]):
            resource = EntityResource(self.request, self.cls,
                                      attrname, value, self)
            try:
                rset = resource.rset
            except HTTPNotFound:
                continue
            if rset.rowcount:
                return resource
        raise KeyError(value)

    @reify
    def rset(self):
        rql = self.cls.fetch_rql(self.request.cw_cnx.user)
        rset = self.request.cw_request.execute(rql)
        return rset


class _RelationshipProxyResource(object):
    """A "proxy" resource allowing to pass through the "relationships" segment
    of path during traversal.
    """

    @parent
    def __init__(self, request, etype=None, **kwargs):
        self.request = request
        self.etype = etype

    def __getitem__(self, value):
        vreg = self.request.registry['cubicweb.registry']
        schema = vreg.schema
        if self.etype:
            etype = self.etype
        elif hasattr(self, '__parent__'):
            etype = self.__parent__.entity.cw_etype
        else:
            raise AssertionError('neither etype nor __parent__ got specified')
        try:
            relinfo = find_relationship(schema, etype, value)
        except ValueError:
            raise KeyError(value)
        else:
            parent = getattr(self, '__parent__', None)
            return RelationshipResource(self.request, *relinfo, parent=parent)


class RelationshipResource(object):
    """A resource to manipulate a relationship `rtype` with __parent__ as
    `role`.

    This can be used for both "schema" and "entities" resources.
    """

    @parent
    def __init__(self, request, rschema, target_schemas, role, **kwargs):
        self.request = request
        self.rtype = rschema.type
        self.target_schemas = target_schemas
        self.role = role

    @property
    def target_type(self):
        """Target entity type of relationship."""
        if len(self.target_schemas) > 1:
            target = self.request.params.get('target_type')
            if target and target in {s.type for s in self.target_schemas}:
                return target
            raise NotImplementedError()
        return self.target_schemas[0].type


class EntityResource(object):
    """A resource class for an entity. It provide method to retrieve an entity
    by eid.
    """

    def __init__(self, request, cls, attrname, name, parent):
        self.request = request
        self.cls = cls
        self.attrname = attrname
        self.__name__ = name
        self.__parent__ = parent

    def __getitem__(self, value):
        # Make sure parent class has no __getitem__ as we do not call it here.
        # If it happens, we'll need to call it here.
        assert not hasattr(super(EntityResource, self), '__getitem__')
        etype = self.cls.cw_etype
        if value == 'relationships':
            return _RelationshipProxyResource(self.request, etype, parent=self)
        vreg = self.request.registry['cubicweb.registry']
        schema = vreg.schema
        try:
            rschema, __, role = find_relationship(schema, etype, value)
        except ValueError:
            raise KeyError(value)
        else:
            return RelatedEntitiesResource(
                self.request, rschema.type, role, parent=self)

    @reify
    def rset(self):
        req = self.request.cw_request
        if self.cls is None:
            return req.execute('Any X WHERE X eid %(x)s',
                               {'x': int(self.__name__)})
        st = self.cls.fetch_rqlst(self.request.cw_cnx.user, ordermethod=None)
        st.add_constant_restriction(st.get_variable('X'), self.attrname,
                                    'x', 'Substitute')
        if self.attrname == 'eid':
            try:
                rset = req.execute(st.as_string(), {'x': int(self.__name__)})
            except (ValueError, TypeResolverException):
                # conflicting eid/type
                raise HTTPNotFound()
        else:
            rset = req.execute(st.as_string(), {'x': text_type(self.__name__)})
        return rset


class RelatedEntitiesResource(object):
    """A resource wrapping entities related to the entity bound to
    `entity_resource` through `rtype`/`role`.
    """

    @parent
    def __init__(self, request, rtype, role, **kwargs):
        self.request = request
        self.rtype = rtype
        self.role = role
        self.__name__ = rtype

    @reify
    def rset(self):
        # May raise HTTPNotFound, this is probably fine (isn't it?)
        entity = self.__parent__.rset.one()
        vreg = self.request.registry['cubicweb.registry']
        # XXX Until https://www.cubicweb.org/ticket/12306543 gets done.
        rql = entity.cw_related_rql(self.rtype, role=self.role)
        args = {'x': entity.eid}
        select = vreg.parse(entity._cw, rql, args).children[0]
        sortterms = self.request.params.get('sort')
        if sortterms:
            select.remove_sort_terms()
            mainvar = select.get_variable('X')
            for term in sortterms.split(','):
                if term.startswith('-'):
                    asc = False
                    term = term[1:]
                else:
                    asc = True
                mdvar = select.make_variable()
                rel = nodes.make_relation(mainvar, term,
                                          (mdvar,), nodes.VariableRef)
                select.add_restriction(rel)
                select.add_sort_var(mdvar, asc=asc)
        rql = select.as_string()
        return entity._cw.execute(rql, args)

    def __getitem__(self, value):
        if self.role != 'subject':
            # We only handle subject-relation in traversal.
            raise KeyError(value)
        entity = self.__parent__.rset.one()
        rset = self.request.cw_cnx.execute(
            'Any O WHERE O eid %(o)s, S {rtype} O, S eid %(s)s'.format(
                rtype=self.rtype),
            {'o': value, 's': entity.eid})
        if not rset:
            raise KeyError(value)
        return RelatedEntityResource(
            self.request, rset.one(), rtype=self.rtype, role=self.role,
            parent=self)


class RelatedEntityResource(object):
    """A resource an entity related to another one."""

    def __init__(self, request, entity, rtype, role, parent):
        self.request = request
        self.entity = entity
        self.rtype = rtype
        self.role = role
        self.__parent__ = parent
        self.__name__ = text_type(entity.eid)
