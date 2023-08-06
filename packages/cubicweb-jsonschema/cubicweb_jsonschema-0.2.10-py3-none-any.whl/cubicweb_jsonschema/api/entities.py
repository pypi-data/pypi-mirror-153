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

"""cubicweb-jsonschema Pyramid views for the JSON API of entities."""

from pyramid import httpexceptions
from pyramid.renderers import render
from pyramid.traversal import (
    find_resource,
    find_root,
)
from pyramid.view import view_config

from cubicweb import (
    neg_role,
    ValidationError,
)
from ..resources import (
    EntityResource,
    ETypeResource,
    RelatedEntitiesResource,
    RelatedEntityResource,
    RelationshipResource,
    RootResource,
)
from . import (
    describedby,
    entity_from_context,
    json_config,
    json_problem,
    jsonschema_adapter,
    LOG,
)


@view_config(
    route_name='cubicweb-jsonschema.entities',
    context=RootResource,
    request_method='GET',
    decorator=[describedby],
)
def get_root(context, request):
    """Site root, no data."""
    response = httpexceptions.HTTPNoContent()
    response.allow = ['GET']
    return response


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=ETypeResource,
    request_method='GET',
    decorator=[describedby],
)
def get_entities(context, request):
    """Render multiple entities in JSON format."""
    adapter = jsonschema_adapter(request.cw_request, etype=context.etype)
    vreg = request.registry['cubicweb.registry']
    if vreg.schema[context.etype].has_perm(request.cw_cnx, 'add'):
        request.response.allow = ['GET', 'POST']
    else:
        request.response.allow = ['GET']
    return adapter.serialize(context.rset.entities())


def allow_for_entity(entity):
    """Return a list of HTTP verbs that are Allow-ed for `entity`.
    """
    perm2verb = [
        ('read', 'GET'),
        ('update', 'PUT'),
        ('delete', 'DELETE'),
    ]
    return [v for p, v in perm2verb if entity.cw_has_perm(p)]


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=EntityResource,
    request_method='GET',
    decorator=[entity_from_context, describedby],
)
def get_entity(context, request):
    """Render a single entity in JSON format."""
    entity = context.entity
    request.response.allow = allow_for_entity(entity)
    return entity.cw_adapt_to('IJSONSchema').serialize()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=ETypeResource,
    request_method='POST',
)
def create_entity(context, request):
    """Create a new entity from JSON data."""
    # TODO In case of validation errors, it'd be better to give a JSON Schema
    # entry as a "pointer", would require selection context to be an
    # ETypeSchemaResource.
    adapter = jsonschema_adapter(request.cw_request, etype=context.etype)
    instance = request.json_body
    entity = adapter.create_entity(instance)
    request.cw_cnx.commit()
    LOG.info('created %s', entity)

    value = entity.cw_adapt_to('IJSONSchema').serialize()
    entity_resource = context[entity.eid]
    location = request.resource_url(entity_resource)
    raise httpexceptions.HTTPCreated(
        location=location,
        content_type='application/json; charset=UTF-8',
        body=render('json', value),
    )


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=EntityResource,
    request_method='PUT',
    decorator=[entity_from_context],
)
def update_entity(context, request):
    """Update an entity from JSON data."""
    entity = context.entity
    instance = request.json_body
    adapted = entity.cw_adapt_to('IJSONSchema')
    adapted.edit_entity(instance)
    request.cw_cnx.commit()
    LOG.info('edited attributes "%s" of %s', ', '.join(instance), entity)
    value = adapted.serialize()
    raise httpexceptions.HTTPOk(
        location=request.resource_url(context),
        content_type='application/json; charset=UTF-8',
        body=render('json', value),
    )


@view_config(
    route_name='delete_entity',
    context=EntityResource,
    request_method='DELETE',
    decorator=[entity_from_context],
)
def delete_entity(context, request):
    """Delete an entity."""
    entity = context.entity
    entity.cw_delete()
    request.cw_cnx.commit()
    LOG.info('deleted %s', entity)
    raise httpexceptions.HTTPNoContent()


def allow_for_entity_relation(entity, rtype, role):
    eschema = entity.e_schema
    rdef = eschema.rdef(rtype, role)
    perm2verb = [
        ('read', 'GET'),
        ('add', 'POST'),
    ]
    if role == 'subject':
        kwargs = {'fromeid': entity.eid}
    else:
        kwargs = {'toeid': entity.eid}
    return [v for p, v in perm2verb
            if rdef.has_perm(entity._cw, p, **kwargs)]


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=RelatedEntitiesResource,
    request_method='GET',
    decorator=[describedby],
)
def get_related_entities(context, request):
    """Return a JSON document of entities target of a relationships."""
    vreg = request.registry['cubicweb.registry']
    mapper = vreg['mappers'].select(
        'jsonschema.collection', request.cw_request,
        rtype=context.rtype, role=context.role,
    )
    entity = context.__parent__.rset.one()
    request.response.allow = allow_for_entity_relation(
        entity, context.rtype, context.role)
    return mapper.serialize(context.rset.entities())


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=RelatedEntitiesResource,
    request_method='POST',
)
def post_related_entities(context, request):
    """Insert relationships between entity bound to context and targets from
    request's JSON body.
    """
    try:
        targets_eid = [int(x) for x in request.json_body]
    except ValueError:
        raise httpexceptions.HTTPBadRequest('invalid target identifier(s)')
    entity = context.__parent__.rset.one()
    rtype = context.rtype
    if context.role != 'subject':
        raise httpexceptions.HTTPNotFound(
            'relation {}-subject not found on {}'.format(
                rtype, entity.cw_etype)
        )
    # TODO: move this to an IJSONSchema adapter
    entity.cw_set(**{rtype: targets_eid})
    request.cw_cnx.commit()
    return httpexceptions.HTTPNoContent()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=RelatedEntityResource,
    request_method='GET',
    decorator=[describedby],
)
def get_related_entity(context, request):
    """Return a JSON document of an entity target of a relationship."""
    entity = context.entity
    adapted = jsonschema_adapter(request.cw_cnx, entity=entity,
                                 rtype=context.rtype,
                                 role=neg_role(context.role))
    request.response.allow = allow_for_entity(entity)
    return adapted.serialize()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=RelatedEntityResource,
    request_method='PUT',
)
def update_related_entity(context, request):
    """Update a related entity from JSON data."""
    instance = request.json_body
    entity = context.entity
    adapted = jsonschema_adapter(request.cw_cnx, entity=entity,
                                 rtype=context.rtype,
                                 role=neg_role(context.role))
    adapted.edit_entity(instance)
    request.cw_cnx.commit()
    LOG.info('edited attributes "%s" of %s', ', '.join(instance), entity)
    value = adapted.serialize()
    raise httpexceptions.HTTPOk(
        location=request.resource_url(context),
        content_type='application/json; charset=UTF-8',
        body=render('json', value),
    )


@view_config(
    route_name='delete_entity',
    context=RelatedEntityResource,
    request_method='DELETE',
)
def delete_relation(context, request):
    """Delete a relationship."""
    assert context.role == 'subject', 'can only delete subject relation'
    subj = context.__parent__.__parent__.rset.one()
    obj = context.entity
    request.cw_cnx.execute(
        'DELETE S {rtype} O WHERE S eid %(s)s, O eid %(o)s'.format(
            rtype=context.rtype),
        {'s': subj.eid, 'o': obj.eid})
    request.cw_cnx.commit()
    LOG.info('deleted <%s %s %s>', subj, context.rtype, obj)
    raise httpexceptions.HTTPNoContent()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=RelationshipResource,
    request_method='POST',
    decorator=[entity_from_context],
)
def create_related_entity(context, request):
    """Create an entity with a relation set."""
    rtype, role, target_type = context.rtype, context.role, context.target_type
    adapter = jsonschema_adapter(
        request.cw_request, etype=target_type, rtype=rtype, role=neg_role(role))
    instance = request.json_body
    target = context.entity
    related = adapter.create_entity(instance, target)
    request.cw_cnx.commit()
    LOG.info('created %s target of %s-%s for %s',
             related, rtype, role, context.entity)
    related_adapted = jsonschema_adapter(
        request.cw_request, entity=related, rtype=rtype, role=neg_role(role))
    value = related_adapted.serialize()
    root_resource = find_root(context)
    entity_resource = find_resource(root_resource,
                                    (related.cw_etype, related.eid))
    location = request.resource_url(entity_resource)
    raise httpexceptions.HTTPCreated(
        location=location,
        content_type='application/json; charset=UTF-8',
        body=render('json', value),
    )


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=ValidationError,
)
def validation_failed(exc, request):
    """Exception view for ValidationError on JSON request."""
    LOG.info('%s encountered during processing of %s', exc, request)
    _ = request.cw_request._
    request.cw_cnx.rollback()
    exc.translate(_)
    invalid_params = []
    detail = []
    for rolename, value in exc.errors.items():
        if rolename:
            invalid_params.append({'name': rolename, 'reason': value})
        else:
            detail.append(value)
    kwargs = {}
    if detail:
        kwargs['detail'] = '\n'.join(detail)
    if invalid_params:
        kwargs['invalid-params'] = invalid_params
    return json_problem(status=422, **kwargs)


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=Exception,
)
def generic_error(exc, request):
    """Generic exception handler for exception (usually during "edition"
    operations).

    It will return a jsonapi-formatted error response from exception found in
    context.
    """
    # Because this handler is wired on the "Exception" context, any error will
    # be catched, including the standard pyramid return exceptions.
    # In this case, just return it
    if isinstance(exc, httpexceptions.HTTPException):
        return exc
    if request.cw_cnx is not None:
        request.cw_cnx.rollback()
    LOG.exception('exception occurred while processing %s', request)
    kwargs = {}
    detail = str(exc)
    if detail:
        kwargs['detail'] = detail
    return json_problem(status=500, **kwargs)


def includeme(config):
    config.include('cubicweb.pyramid.predicates')
    config.include('..predicates')
    config.add_route('delete_entity', '/jsonschema/{etype}/*traverse',
                     factory=ETypeResource.from_match('etype'),
                     request_method='DELETE',
                     match_is_etype='etype')
    config.add_route(
        'cubicweb-jsonschema.entities',
        '/jsonschema/*traverse',
        factory=RootResource,
        strict_accept='application/json',
    )
    config.scan(__name__)
