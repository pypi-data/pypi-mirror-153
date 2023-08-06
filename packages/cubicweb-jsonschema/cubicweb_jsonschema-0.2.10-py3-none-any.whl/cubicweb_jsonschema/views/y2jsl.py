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

from collections import OrderedDict

import jsl

from cubicweb.schema import META_RTYPES
from cubicweb.view import Component

from cubicweb_jsonschema import CREATION_ROLE


class Y2JError(Exception):
    pass


def field_names_from_yams(etype):
    """ Yield the names of jsl fields for entity type ``etype``.
    These names are yams attributes and inlined relations.
    """
    for rtype in etype.ordered_relations():
        if rtype.type not in META_RTYPES:
            if etype.is_metadata(rtype.type):
                continue
            if rtype.final or rtype.inlined:
                yield rtype.type, 'subject'


class JslDocumentBuilder(Component):
    """Class that builds a jsl document from a description class.

    Inherit this class and pass an instance to `y2j_etype` to
    customize the jsl field gathering and generation.

    By default, the resulting jsl document will have following fields,
    in this order:

    - `__etype__` and `__eid__`

    - all yams attributes and inlined relations (unless an explicit
      name list is supplied in the `from_yams` attribute of the
      description class)

    - all the jsl fields attributes set on the description class

    The field generation itself is be delegated to the classes which
    `__regid__` is "jsonschema.relation" in the "mappers" register.

    """
    __regid__ = 'jsonschema.map.builder'

    # Should "base" fields be included in main schema document?
    include_base_fields = False

    def __init__(self, *args, **kwargs):
        super(JslDocumentBuilder, self).__init__(*args, **kwargs)
        self.relation_targets = {}

    def base_fields(self, etype):
        fields = OrderedDict()
        fields['__etype__'] = jsl.fields.StringField(
            required=True, enum=[etype], default=etype)
        fields['__eid__'] = jsl.fields.StringField(required=True)
        return fields

    def fields_from_yams(self, etype, filter_in=None, filter_out=None,
                         schema_role=None):
        """Return fields for a Yams `etype` using the `generate_field` method.

        The field list is built using `field_names_from_yams` for yams entity
        type which name is `etype`, unless `filter_in` specifies such a field
        name list.

        If `filter_out` is given, it must be a sequence of names which are
        excluded from the above field name list. Therefore, if a name is both
        in `filter_in` and `filter_out`, an error is raised.
        """
        if filter_in and filter_out:
            both = set(filter_in).intersection(set(filter_out))
            if both:
                msg = self._cw._(
                    'Fields %s are both in __filter_in__ and __filter_out__')
                raise Y2JError(msg % both)
        if filter_in:
            rtype_roles = []
            for value in filter_in:
                try:
                    rtype, role = value
                except ValueError:
                    if value.startswith('reverse_'):
                        rtype, role = value[len('reverse_'):], 'object'
                    else:
                        rtype, role = value, 'subject'
                rtype_roles.append((rtype, role))
        else:
            rtype_roles = field_names_from_yams(self._cw.vreg.schema[etype])
        if filter_out:
            rtype_roles = [rtype_role for rtype_role in rtype_roles
                           if rtype_role[0] not in filter_out]
        return OrderedDict((rtype, self.generate_field(etype, rtype, role,
                                                       schema_role))
                           for rtype, role in rtype_roles)

    def explicit_fields(self, etype, explicit_fields, schema_role=None):
        """Collect attributes from `explicit_fields` mapping.

        Values of `explicit_fields` may either jsl fields or dict instances.
        In the later case, the field is built using a field factory
        which is passed keyword arguments given at the dict value.
        """
        fields = OrderedDict()
        for key, val in explicit_fields.items():
            if isinstance(val, jsl.fields.BaseField):
                fields[key] = val
            elif isinstance(val, dict):
                fields[key] = self.generate_field(
                    etype, key, 'subject', schema_role, **val)
        return fields

    def generate_field(self, etype, rtype, role, schema_role,
                       target_types=None, **kwargs):
        """ Return a jsl field named `rtype` supposed to described a
        yams relation definition of entity type `etype` as `role` in the
        context of schema `schema_role` (in the jsl sense).

        The generation is delegated to a field factory which is called
        with the keyword arguments `kwargs`.
        """
        if target_types is None:
            rschema = self._cw.vreg.schema[rtype]
            target_types = {
                target.type for target in rschema.targets(etype, role)}
        assert isinstance(target_types, set), target_types
        field_factory = self._cw.vreg['mappers'].select_or_none(
            'jsonschema.relation', self._cw,
            etype=etype, rtype=rtype, role=role, target_types=target_types)
        if field_factory is None:
            raise Y2JError(
                'Cannot find a field factory for %s-%s' % (etype, rtype))
        fieldcls = field_factory.jsl_field(schema_role, **kwargs)
        assert (rtype, role) not in self.relation_targets, \
            'field for {0}-{1} already generated'.format(rtype, role)
        self.relation_targets[rtype, role] = field_factory.target_types
        return fieldcls

    def set_default_options(self, etype, options=None):
        """Return an Options class with `definition_id` to the class name of
        `etype`; it `options` is not None and is an `Options` class, it is
        updated and returned.
        """
        if options is None:
            options = type('Options', (object,), {})
        if 'definition_id' not in dir(options):
            options.definition_id = etype
        if 'title' not in dir(options):
            options.title = self._cw._(etype)
        return options

    def document(self, cls, schema_role=None):
        """ Return a Jsl Document class from the description class `cls`.
        This is the entry point of the builder.
        """
        etype = cls.__name__
        newdict = self.base_fields(etype)
        fields = dict((k, getattr(cls, k)) for k in dir(cls))
        # Add explicit fields to `filter_out` to avoid generating them twice.
        filter_out = getattr(cls, '__filter_out__', ()) + tuple(fields)
        yams_fields = self.fields_from_yams(
            etype,
            filter_in=getattr(cls, '__filter_in__', ()),
            filter_out=filter_out,
            schema_role=schema_role,
        )
        newdict.update(yams_fields)
        newdict.update(self.explicit_fields(etype, fields, schema_role))
        options = newdict.get('Options')
        newdict['Options'] = self.set_default_options(etype, options)
        return type(etype, (jsl.Document,), newdict)


def y2j_etype(vreg, cnx, schema_role=CREATION_ROLE):
    """Class decorator that returns a jsl Document subclass.

    This jsl document is built using registered 'jsonschema.map.builder'
    component.
    """
    def decorator(cls):
        builder = vreg['components'].select('jsonschema.map.builder', cnx)
        return builder.document(cls, schema_role)
    return decorator
