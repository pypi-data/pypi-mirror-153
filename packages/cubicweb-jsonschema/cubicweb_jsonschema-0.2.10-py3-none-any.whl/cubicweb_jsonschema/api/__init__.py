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

"""cubicweb-jsonschema Pyramid views for the JSON API."""

import datetime
from functools import wraps
import logging

from cubicweb import NoResultError

from pyramid import httpexceptions
from pyramid.renderers import JSON, render
from pyramid.view import view_config

from .. import JSONSCHEMA_MEDIA_TYPE


LOG = logging.getLogger(__name__)


def json_config(**settings):
    """Wraps view_config for JSON rendering."""
    settings.setdefault('accept', 'application/json')
    settings.setdefault('renderer', 'json')
    return view_config(**settings)


def link_header(value, rel, **params):
    base = '<{value}>; rel="{rel}"'.format(value=value, rel=rel,)
    extra = '; '.join('{}="{}"'.format(name, value)
                      for name, value in params.items())
    return '; '.join([base, extra])


def describedby(func):
    """View decorator adding a rel="describedby" Link header pointing to
    resource's JSON Schema URI.
    """
    @wraps(func)
    def wrapper(context, request):
        response = func(context, request)
        response.headers['Link'] = link_header(
            request.resource_path(context, 'schema'),
            'describedby', type=JSONSCHEMA_MEDIA_TYPE,
        )
        return response

    return wrapper


def describes(func):
    """View decorator adding a rel="describes" Link header pointing to
    resource's JSON view URI.
    """
    @wraps(func)
    def wrapper(context, request):
        response = func(context, request)
        response.headers['Link'] = link_header(
            request.resource_path(context),
            'describes', type='application/json'
        )
        return response

    return wrapper


def entity_from_context(func):
    """View decorator binding a CubicWeb `entity` to the `context`.

    May raise HTTPNotFound if no entity can be found.
    Will walk through parents of the `context` until an `EntityResource` gets
    found before fetching the `entity`.
    """
    @wraps(func)
    def wrapper(context, request):
        entity_context = context
        while True:
            try:
                rset = entity_context.rset
            except AttributeError:
                try:
                    entity_context = entity_context.__parent__
                except AttributeError:
                    raise httpexceptions.HTTPNotFound()
            else:
                break
        try:
            entity = rset.one()  # May raise HTTPNotFound.
        except NoResultError:
            raise httpexceptions.HTTPNotFound()
        context.entity = entity
        return func(context, request)

    return wrapper


def jsonschema_adapter(cnx, **context):
    return cnx.vreg['adapters'].select('IJSONSchema', cnx, **context)


def json_problem(type=None, title=None, status=400, detail=None,
                 instance=None, **problem):
    """Return a response application/problem+json following RFC 7807"""
    Error = httpexceptions.status_map[status]
    if type in (None, 'about:blank') and title is None:
        # When type 'about:blank' (default), title SHOULD be the same as the
        # recommended HTTP status phrase for that code, although it MAY be
        # localized
        title = Error.title
    for key, value in (
        ('type', type),
        ('title', title),
        ('status', status),
        ('detail', detail),
        ('instance', instance),
    ):
        if value is not None:
            problem[key] = value
    return Error(
        body=render('json', problem),
        headers={'Content-Type': 'application/problem+json; charset=UTF-8'})


def includeme(config):
    json_renderer = JSON()

    def datetime_isoformat(obj, request):
        return obj.replace(microsecond=0).isoformat()

    def date_isoformat(obj, request):
        return obj.isoformat()

    json_renderer.add_adapter(datetime.datetime, datetime_isoformat)
    json_renderer.add_adapter(datetime.date, date_isoformat)
    config.add_renderer('json', json_renderer)
    config.include('.entities')
    config.include('.schema')
    config.scan(__name__)
