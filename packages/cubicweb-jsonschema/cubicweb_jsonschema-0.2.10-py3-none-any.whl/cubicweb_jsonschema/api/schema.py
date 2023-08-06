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

"""cubicweb-jsonschema Pyramid views for JSON Schema endpoints."""

from pyramid import httpexceptions
from pyramid.view import view_config

from cubicweb import neg_role
from cubicweb.web.views import uicfg

from .. import (
    CREATION_ROLE,
    EDITION_ROLE,
    JSONSCHEMA_MEDIA_TYPE,
    VIEW_ROLE,
    resources,
)
from . import (
    describes,
)


def jsonschema_config(**settings):
    for name, value in [
        ('name', 'schema'),
        ('route_name', 'cubicweb-jsonschema.schema'),
        ('accept', JSONSCHEMA_MEDIA_TYPE),
        ('renderer', 'json'),
        ('request_method', 'GET'),
    ]:
        settings.setdefault(name, value)
    return view_config(**settings)


def links_sortkey(link):
    """key function for sorting a list of link description object."""
    return link['href'], link['rel']


@jsonschema_config(
    context=resources.RootResource,
    decorator=[describes],
)
def application_schema(context, request):
    """Schema view for the application."""
    vreg = request.registry['cubicweb.registry']

    def links():
        for eschema in vreg.schema.entities():
            if uicfg.indexview_etype_section.get(eschema) != 'application':
                continue
            etype = eschema.type
            etype_resource = context[etype]
            title = etype + '_plural'
            link = vreg['links'].select(
                'collection', request.cw_request, title=title)
            yield link.description_object(request, etype_resource)

    return {
        'title': request.cw_cnx.property_value('ui.site-title'),
        'type': "null",
        'links': sorted(links(), key=links_sortkey),
    }


@jsonschema_config(
    context=resources.ETypeResource,
    request_param='role',
)
def etype_role_schema(context, request):
    """Schema view for an entity type with specified role."""
    req = request.cw_request
    adapted = req.vreg['adapters'].select('IJSONSchema', req,
                                          etype=context.etype)
    role = request.params['role'].lower()
    if role == VIEW_ROLE:
        return adapted.view_schema(ordered=True)
    elif role == CREATION_ROLE:
        return adapted.creation_schema(ordered=True)
    else:
        raise httpexceptions.HTTPBadRequest(
            'invalid role: {0}'.format(role))


@jsonschema_config(
    context=resources.ETypeResource,
    decorator=[describes],
)
def etype_schema(context, request):
    """Schema view for an entity type returning the complete hyper schema.
    """
    req = request.cw_request
    vreg = request.registry['cubicweb.registry']
    collection_mapper = vreg['mappers'].select(
        'jsonschema.collection', req, etype=context.etype)
    schema = collection_mapper.jsl_field(VIEW_ROLE).get_schema(ordered=True)
    # Insert "rel": "item" link with "items" of the collection array with an
    # "anchor" pointing at the main instance (i.e. the collection).
    item_link = vreg['links'].select('collection-item', req, anchor=u'#')
    schema['items']['links'] = [item_link.description_object(request, context)]
    schema['links'] = sorted([
        link.description_object(request, context)
        for link in vreg['links'].possible_objects(req, etype=context.etype,
                                                   rset=context.rset)
    ], key=links_sortkey)
    return schema


@jsonschema_config(
    context=resources.EntityResource,
    request_param='role',
)
def entity_role_schema(context, request):
    """Schema view for a live entity with specified role."""
    entity = context.rset.one()  # May raise HTTPNotFound.
    adapted = entity.cw_adapt_to('IJSONSchema')
    role = request.params['role'].lower()
    if role == VIEW_ROLE:
        return adapted.view_schema(ordered=True)
    elif role == EDITION_ROLE:
        return adapted.edition_schema(ordered=True)
    else:
        raise httpexceptions.HTTPBadRequest(
            'invalid role: {0}'.format(role))


@jsonschema_config(
    context=resources.EntityResource,
    decorator=[describes],
)
def entity_schema(context, request):
    """Schema view for a live entity returning the complete hyper schema.
    """
    req = request.cw_request
    entity = context.rset.one()  # May raise HTTPNotFound.
    adapted = entity.cw_adapt_to('IJSONSchema')
    schema = adapted.view_schema(ordered=True)
    vreg = request.registry['cubicweb.registry']
    linksreg = vreg['links']
    links = [
        link.description_object(request, context)
        for link in linksreg.possible_objects(req, entity=entity)
    ]
    for rtype, role, __ in adapted.relations():
        if role != 'subject':
            continue
        links.append(
            linksreg.select(
                'entity.related', req,
                entity=entity, rtype=rtype, role=role,
            ).description_object(request, context)
        )
    schema['links'] = sorted(links, key=links_sortkey)
    return schema


@jsonschema_config(
    context=resources.RelatedEntitiesResource,
    decorator=[describes],
)
def related_entities_schema(context, request):
    """Schema view for the collection of targets of a relation.
    """
    req = request.cw_request
    rtype, role = context.rtype, context.role
    vreg = request.registry['cubicweb.registry']
    collection_mapper = vreg['mappers'].select(
        'jsonschema.collection', req, rtype=rtype, role=role)
    schema = collection_mapper.jsl_field(VIEW_ROLE).get_schema(ordered=True)
    # Insert "rel": "item" link with "items" of the collection array with an
    # "anchor" pointing at the main instance (i.e. the collection).
    item_link = vreg['links'].select('collection-item',
                                     req, anchor=u'#')
    schema['items']['links'] = [item_link.description_object(request, context)]
    relatedcollection_link = vreg['links'].select(
        'related-collection', req, title=collection_mapper.title)
    schema['links'] = [
        relatedcollection_link.description_object(request, context),
    ]
    return schema


@jsonschema_config(
    context=resources.RelatedEntitiesResource,
    request_param='role',
)
def related_entities_role_schema(context, request):
    """Schema view for targets of a relation with specified 'role'."""
    req = request.cw_request
    vreg = request.registry['cubicweb.registry']
    entity = context.__parent__.rset.one()
    mapper = vreg['mappers'].select('jsonschema.relation', req, entity=entity,
                                    rtype=context.rtype, role=context.role)
    schema_role = request.params['role'].lower()
    if schema_role not in (VIEW_ROLE, CREATION_ROLE):
        raise httpexceptions.HTTPBadRequest(
            'invalid role: {0}'.format(schema_role))
    return mapper.jsl_field(schema_role).get_schema(ordered=True)


@jsonschema_config(
    context=resources.RelatedEntityResource,
    decorator=[describes],
)
def related_entity_schema(context, request):
    """Schema view for a target entity of a relation."""
    req = request.cw_request
    entity = context.entity
    vreg = request.registry['cubicweb.registry']
    mapper = vreg['mappers'].select(
        'jsonschema.entity', req, entity=entity,
        rtype=context.__parent__.rtype, role=context.__parent__.role,
    )
    schema = mapper.jsl_document(VIEW_ROLE).get_schema(ordered=True)
    linksreg = vreg['links']
    links = [
        link.description_object(request, context)
        for link in linksreg.possible_objects(req, entity=entity)
    ]
    schema['links'] = sorted(links, key=links_sortkey)
    return schema


@jsonschema_config(
    context=resources.RelatedEntityResource,
    request_param='role',
)
def related_entity_role_schema(context, request):
    """Schema view for a target entity of a relation with specified 'role'."""
    req = request.cw_request
    entity = context.entity
    vreg = request.registry['cubicweb.registry']
    mapper = vreg['mappers'].select(
        'jsonschema.entity', req, entity=entity,
        rtype=context.__parent__.rtype, role=context.__parent__.role,
    )
    schema_role = request.params['role'].lower()
    if schema_role not in (VIEW_ROLE, EDITION_ROLE):
        raise httpexceptions.HTTPBadRequest(
            'invalid role: {0}'.format(schema_role))
    return mapper.jsl_document(schema_role).get_schema(ordered=True)


@jsonschema_config(
    context=resources.RelationshipResource,
    request_param='role',
)
def relationship_schema(context, request):
    rtype, role, target_type = context.rtype, context.role, context.target_type
    adapter = request.cw_request.vreg['adapters'].select(
        'IJSONSchema', request.cw_request,
        etype=target_type, rtype=rtype, role=neg_role(role))
    schema_role = request.params['role'].lower()
    if schema_role == CREATION_ROLE:
        return adapter.creation_schema(ordered=True)
    elif schema_role == VIEW_ROLE:
        return adapter.view_schema(ordered=True)
    raise httpexceptions.HTTPBadRequest(
        'invalid or missing schema role')


def includeme(config):
    config.include('..predicates')
    config.add_route(
        'cubicweb-jsonschema.schema',
        '*traverse',
        factory=resources.RootResource,
        strict_accept=JSONSCHEMA_MEDIA_TYPE,
    )
    config.scan(__name__)
