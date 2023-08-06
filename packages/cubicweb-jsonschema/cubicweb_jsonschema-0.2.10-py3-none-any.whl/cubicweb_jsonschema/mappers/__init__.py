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
"""Appobjects for mapping Yams schema definitions to JSON Schema documents."""

from collections import OrderedDict
from functools import partial

import iso8601
from six import text_type, string_types

import jsl

from logilab.common.decorators import cachedproperty, classproperty
from logilab.common.registry import Predicate, objectify_predicate, yes

from yams import BadSchemaDefinition, ValidationError
from yams.constraints import StaticVocabularyConstraint
from cubicweb import Binary, neg_role, _
from cubicweb.appobject import AppObject
from cubicweb.predicates import (
    ExpectedValuePredicate,
    PartialPredicateMixIn,
    match_kwargs,
)

from cubicweb_jsonschema import (
    CREATION_ROLE,
    EDITION_ROLE,
    VIEW_ROLE,
    orm_rtype,
)
from cubicweb_jsonschema.views import jsonschema_section


def _etype_from_context(kwargs):
    etype = kwargs.get('etype')
    if etype is None:
        entity = kwargs.get('entity')
        if entity is not None:
            etype = entity.cw_etype
    return etype


@objectify_predicate
def yams_final_rtype(cls, cnx, rtype, role, **kwargs):
    """Predicate that returns 1 when the supplied `rtype` is not final."""
    etype = _etype_from_context(kwargs)
    if etype is None:
        return 0
    rdef = cnx.vreg.schema[etype].rdef(rtype, role=role, takefirst=True)
    if rdef.final:
        return 1
    return 0


@objectify_predicate
def yams_component_target(cls, cnx, rtype, role, target_types=None, **kwargs):
    """Predicate that returns 1 when the target entity types are component of
    the relation defined by `rtype` and `role` (i.e. the relation has
    composite set to `role`).
    """
    etype = _etype_from_context(kwargs)
    if etype is None:
        return 0
    component = None
    eschema = cnx.vreg.schema[etype]
    if target_types is None:
        rschema = cnx.vreg.schema[rtype]
        target_types = tuple(t.type for t in rschema.targets(etype, role=role))
    for target_type in target_types:
        rdef = eschema.rdef(rtype, role=role, targettype=target_type)
        _component = rdef.composite == role
        if component is None:
            component = _component
        elif not component == _component:
            cls.warning('component inconsistency accross target types')
            return 0
    return component


class yams_match(Predicate):
    """Predicate that returns a positive value when the supplied relation
    match parameters given as predicate argument.

    The more __call__ arguments match __init__'s ones, the higher the score
    is.
    """

    def __init__(self, etype=None, rtype=None, role=None, target_types=()):
        self.etype = etype
        self.rtype = rtype
        self.role = role
        if isinstance(target_types, string_types):
            target_types = {target_types}
        elif not isinstance(target_types, (set, frozenset)):
            target_types = frozenset(target_types)
        self.target_types = target_types

    def __call__(self, cls, cnx, rtype, role, **kwargs):
        etype = _etype_from_context(kwargs)
        score = 0
        for key in ('etype', 'rtype', 'role'):
            expected = getattr(self, key, None)
            if expected is not None:
                if locals()[key] != expected:
                    return 0
                score += 1
        target_types = kwargs.get('target_types', frozenset())
        assert isinstance(target_types, (set, frozenset)), \
            'yams_match must be called with a set as "target_types" argument'
        if self.target_types:
            if not target_types.issubset(self.target_types):
                return 0
            score += 1
        return score


class partial_yams_match(PartialPredicateMixIn, ExpectedValuePredicate):
    """Return non-zero if selected class's attributes `etype`, `rtype`, `role`
    and/or `target_types` match with keyword arguments from context.
    """

    match_attributes = ('etype', 'rtype', 'role', 'target_types')

    def __init__(self, *expected, **kwargs):
        super(partial_yams_match, self).__init__((), **kwargs)

    def complete(self, cls):
        self.expected = {}
        for name in self.match_attributes:
            if hasattr(cls, name):
                self.expected[name] = set([getattr(cls, name)])

    def _values_set(self, cls, req, **kwargs):
        values = {}
        for name in self.match_attributes:
            if name in kwargs:
                values[name] = kwargs[name]
        return values


def base_fields(etype):
    fields = OrderedDict()
    fields['__etype__'] = jsl.fields.StringField(
        required=True, enum=[etype], default=etype)
    fields['__eid__'] = jsl.fields.StringField(required=True)
    return fields


def default_options(_cw, etype):
    """Return an Options class for a jsl.Document named `etype`."""
    attrs = {
        'definition_id': etype,
        'title': _cw._(etype),
        'schema_uri': 'http://json-schema.org/draft-06/schema#',
    }
    return type('Options', (object,), attrs)


class JSONSchemaMapper(AppObject):
    """Base class for mappers between Yams schema definitions and JSON Schema
    documents.
    """
    __registry__ = 'mappers'


class ETypeMapper(JSONSchemaMapper):
    """A mapper to build JSL document for an entity type."""
    __regid__ = 'jsonschema.entity'
    __select__ = match_kwargs('etype')

    # Should "base" fields __etype__/__eid__ be included in main schema
    # document?
    include_base_fields = False

    @property
    def etype(self):
        return self.cw_extra_kwargs['etype']

    @property
    def entity(self):
        """Entity bound to this mapper, None for ETypeMapper."""
        return None

    def jsl_document(self, schema_role=None):
        """Return a jsl.Document for bound entity type with fields relations
        registered to appear in the document (through `jsonschema_section`).
        """
        attrs = OrderedDict()
        if self.include_base_fields:
            attrs.update(base_fields(self.etype))
        for mapper in self._object_mappers():
            attrs[mapper.name] = mapper.jsl_field(schema_role)
        for rtype, role, target_types in self.relations(schema_role):
            if target_types is None:
                target_types = self._rtype_target_types(rtype, role)
            assert isinstance(target_types, set), target_types
            mapper = self._relation_mapper(rtype, role, target_types)
            attrs[rtype] = mapper.jsl_field(schema_role)
        attrs['Options'] = default_options(self._cw, self.etype)
        return type(str(self.etype), (jsl.Document, ), attrs)

    def values(self, instance):
        """Return a dict with deserialized data from `instance` suitable for
        insertion in CubicWeb database.
        """
        entity = self.entity
        values = {}
        # Deserialize "jsonschema.object" mappers first.
        for mapper in self._object_mappers():
            values.update(mapper.values(entity, instance))
        # Then Yams relations.
        if entity is None:
            schema_role = CREATION_ROLE
        else:
            schema_role = EDITION_ROLE
        for rtype, role, target_types in self.relations(schema_role):
            mapper = self._relation_mapper(rtype, role, target_types)
            values.update(mapper.values(entity, instance))
        if instance:
            # All properties in "instance" should have been consumed at this
            # point.
            eid = entity.eid if entity is not None else None
            msg = _('unexpected properties: {}').format(', '.join(instance))
            raise ValidationError(eid, {None: msg})
        return values

    def relations(self, schema_role):
        """Yield relation information tuple (rtype, role, targettypes)
        for given schema role in the context of bound entity type.
        """
        try:
            permission = {
                VIEW_ROLE: 'read',
                CREATION_ROLE: 'add',
                EDITION_ROLE: 'update',
            }[schema_role]
        except KeyError:
            raise ValueError('unhandled schema role "{0}" in {1}'.format(
                schema_role, self))
        entity = self.entity
        if entity is None:
            entity = self._cw.vreg['etypes'].etype_class(self.etype)(self._cw)
        rsection = self._cw.vreg['uicfg'].select(
            'jsonschema', self._cw, entity=entity)
        return rsection.relations_by_section(entity, 'inlined', permission)

    def _object_mappers(self):
        """Yield 'jsonschema.object' mapper instance selectable for entity
        bound to this mapper.
        """
        if 'jsonschema.object' not in self._cw.vreg['mappers']:
            return
        for mappercls in self._cw.vreg['mappers']['jsonschema.object']:
            if mappercls.__select__(mappercls, self._cw, etype=self.etype) > 0:
                yield mappercls(self._cw)

    def _rtype_target_types(self, rtype, role):
        rschema = self._cw.vreg.schema[rtype]
        return {t.type for t in rschema.targets(self.etype, role)}

    def _relation_mapper(self, rtype, role, target_types=None):
        return self._cw.vreg['mappers'].select(
            'jsonschema.relation', self._cw,
            etype=self.etype, rtype=rtype, role=role, target_types=target_types)


class TargetETypeMapper(ETypeMapper):
    """Specialized version of :class:`ETypeMapper` selectable for an entity
    type as target of (`rtype`, `role`) relation.
    """
    __select__ = match_kwargs('etype', 'rtype', 'role')

    @property
    def rtype(self):
        return self.cw_extra_kwargs['rtype']

    @property
    def role(self):
        return self.cw_extra_kwargs['role']

    def relations(self, schema_role):
        relations = super(TargetETypeMapper, self).relations(schema_role)
        for rtype, role, target_types in relations:
            if (rtype, role) == (self.rtype, self.role):
                continue
            yield rtype, role, target_types


class EntityMapper(ETypeMapper):
    """Specialized version of :class:`ETypeMapper` for a live entity."""

    __select__ = match_kwargs('entity')

    @property
    def entity(self):
        """Live entity from selection context."""
        return self.cw_extra_kwargs['entity']

    @property
    def etype(self):
        return self.entity.cw_etype

    def _relation_mapper(self, rtype, role, target_types=None):
        return self._cw.vreg['mappers'].select(
            'jsonschema.relation', self._cw,
            entity=self.entity, rtype=rtype,
            role=role, target_types=target_types)

    def serialize(self):
        """Return the serialized value entity bound to this mapper."""
        entity = self.entity
        entity.complete()
        data = {}
        for mapper in self._object_mappers():
            data[mapper.name] = mapper.serialize(entity)
        for rtype, role, target_types in self.relations(VIEW_ROLE):
            relation_mapper = self._relation_mapper(rtype, role, target_types)
            value = relation_mapper.serialize(entity)
            if value is None:
                continue
            data[relation_mapper.orm_rtype] = value
        return data


class TargetEntityMapper(EntityMapper, TargetETypeMapper):
    """Specialized version of :class:`TargetETypeMapper` and
    :class:`EntityMapper` selectable for an *entity* as target of (`rtype`,
    `role`) relation.
    """
    __select__ = match_kwargs('entity', 'rtype', 'role')


class EntityCollectionMapper(JSONSchemaMapper):
    """Mapper for a collection of entities."""
    __regid__ = 'jsonschema.collection'
    __select__ = match_kwargs('etype')

    @property
    def etype(self):
        return self.cw_extra_kwargs['etype']

    @property
    def title(self):
        """Title of the collection, plural form of entity type."""
        return self._cw._('{}_plural').format(self.etype)

    def jsl_field(self, schema_role, **kwargs):
        """Return a JSON schema dict to model a collection of entities."""
        item_mapper = self._cw.vreg['mappers'].select(
            'jsonschema.item', self._cw)
        item_field = item_mapper.jsl_field(schema_role, **kwargs)
        return jsl.fields.ArrayField(title=self.title, items=item_field)

    def serialize(self, entities):
        """Return a list of collection item representing each entity in
        `entities`.
        """
        mapper = self._cw.vreg['mappers'].select(
            'jsonschema.item', self._cw)
        return [mapper.serialize(entity) for entity in entities]


class RelatedCollectionMapper(EntityCollectionMapper):
    """Mapper for a collection of entities through a relation."""
    __select__ = match_kwargs('rtype', 'role')

    @property
    def title(self):
        """Title of the collection, name of the relation."""
        rtype = self.cw_extra_kwargs['rtype']
        role = self.cw_extra_kwargs['role']
        return self._cw._(rtype if role == 'subject' else rtype + '-object')


class CollectionItemMapper(JSONSchemaMapper):
    """Mapper for an item of a collection."""
    __regid__ = 'jsonschema.item'
    __select__ = yes()

    def jsl_field(self, schema_role, **kwargs):
        """Return a jsl.fields.DictField with item description."""
        if schema_role == CREATION_ROLE:
            return jsl.fields.StringField(**kwargs)
        return jsl.fields.DictField(
            properties={
                'type': jsl.fields.StringField(),
                'id': jsl.fields.StringField(),
                'title': jsl.fields.StringField(),
            },
            **kwargs
        )

    @staticmethod
    def serialize(entity):
        """Return a dictionary with entity represented as a collection item."""
        return {
            'type': entity.cw_etype.lower(),
            'id': text_type(entity.eid),
            'title': entity.dc_title(),
        }


class BaseRelationMapper(JSONSchemaMapper):
    """Base abstract class to fill the gap between a yams relation and it's json
    schema mapping.

    They should be selected depending on the relation (`etype`, `rtype`, `role`
    and optionaly `target_types`). You may then get a Jsl field from them by
    calling the `jsl_field` method.
    """
    __regid__ = 'jsonschema.relation'
    __select__ = match_kwargs('rtype', 'role')
    __abstract__ = True

    @property
    def jsl_field_class(self):
        """The jsl.fields.BaseField child class to be returned by the factory.
        """
        raise NotImplementedError

    @property
    def etype(self):
        """The entity type bound to this mapper."""
        return _etype_from_context(self.cw_extra_kwargs)

    def __init__(self, _cw, **kwargs):
        #: relation type name
        self.rtype = kwargs.pop('rtype')
        #: role of `etype` in relation
        self.role = kwargs.pop('role')
        #: possible target types of the relation (empty for attribute relations)
        self.target_types = []
        rschema = _cw.vreg.schema[self.rtype]
        target_types = kwargs.pop('target_types', None)
        for target_eschema in sorted(rschema.targets(role=self.role)):
            if target_eschema.final:
                continue
            target_type = target_eschema.type
            if target_types is not None and target_type not in target_types:
                continue
            self.target_types.append(target_type)

        super(BaseRelationMapper, self).__init__(_cw, **kwargs)

    def __repr__(self):
        return ('<{0.__class__.__name__} etype={0.etype} rtype={0.rtype} '
                'role={0.role} target_types={0.target_types}>'.format(self))

    @cachedproperty
    def description(self):
        ntargets = len(self.target_types)
        if ntargets > 1:
            return None
        elif ntargets == 1:
            targettype = self.target_types[0]
        else:
            targettype = None
        eschema = self._cw.vreg.schema[self.etype]
        rdef = eschema.rdef(self.rtype, role=self.role,
                            targettype=targettype)
        if rdef.description:
            return self._cw._(rdef.description)

    @cachedproperty
    def title(self):
        if self.role == 'object':
            return self._cw._(self.rtype + '_object')
        return self._cw._(self.rtype)

    @cachedproperty
    def orm_rtype(self):
        return orm_rtype(self.rtype, self.role)

    def jsl_field(self, schema_role, **kwargs):
        """Return a JSL field built from `jsl_field_class`."""
        if 'title' not in kwargs:
            kwargs['title'] = self.title
        if 'description' not in kwargs and self.description is not None:
            kwargs['description'] = self.description
        kwargs.pop('module', None)
        return self.jsl_field_class(**kwargs)

    def values(self, entity, instance):
        """Return a dictionary holding deserialized value for this field,
        given the input entity (None on creation) and `instance` (JSON values
        as dictionary).

        If present, the field matching mapped `rtype` is removed from
        `instance` after processing.
        """
        raise NotImplementedError()

    def serialize(self, entity):
        """Return the serialized value for this field."""
        raise NotImplementedError()

    @staticmethod
    def _type(json_value):
        """Return properly typed value for use within a cubicweb's entity from
        given JSON value.

        Nothing to do by default.
        """
        return json_value


class AttributeMapper(BaseRelationMapper):
    """Base abstract class to map attribute relation."""
    __abstract__ = True
    __select__ = yams_final_rtype() & match_kwargs('etype')

    #: JSON Schema "format" keyword for semantic validation.
    format = None

    @property
    def attr(self):
        """Relation definition for bound attribute."""
        return self._cw.vreg.schema[self.etype].rdef(self.rtype)

    def add_constraint(self, cstr, jsl_attrs):
        serializer = self._cw.vreg['mappers'].select_or_none(
            'jsonschema.constraint', self._cw.vreg, self._cw._,
            self.etype, self.rtype, cstr, jsl_attrs)
        if serializer is not None:
            new_attrs = serializer.todict()
            if new_attrs:
                jsl_attrs.update(new_attrs)
        elif not isinstance(cstr, StaticVocabularyConstraint):
            self.warning('JSL: ignored %s on %s', cstr.type(), self.attr)

    def jsl_field(self, schema_role, **kwargs):
        kwargs.setdefault('format', self.format)
        if hasattr(self, 'title') and self.title:
            kwargs['title'] = self.title
        if schema_role in (CREATION_ROLE, EDITION_ROLE):
            if 'required' not in kwargs and self.attr.cardinality[0] == '1':
                kwargs['required'] = True
            if 'default' not in kwargs and self.attr.default is not None:
                kwargs['default'] = self.attr.default
            vocabulary_constraint = next(
                (cstr for cstr in self.attr.constraints
                 if isinstance(cstr, StaticVocabularyConstraint)), None)
            if vocabulary_constraint:
                # In presence of a vocabulary constraint, we wrap the field
                # into a oneOf field with a single-value 'enum', ignoring
                # other constraints.
                fields = []
                field_factory = super(AttributeMapper, self).jsl_field
                for v in sorted(vocabulary_constraint.vocabulary()):
                    kw = {'enum': [v], 'title': self._cw._(v)}
                    fields.append(field_factory(schema_role, **kw))
                return jsl.fields.OneOfField(fields, **kwargs)
            for constraint in self.attr.constraints:
                self.add_constraint(constraint, kwargs)
        return super(AttributeMapper, self).jsl_field(schema_role, **kwargs)

    def values(self, entity, instance):
        """Return a dictionary holding deserialized value for mapped attribute.

        If mapped attribute is absent from `instance` and `entity` is not
        None, the default value for attribute is returned as value of the
        dictionnary.
        """
        try:
            value = instance.pop(self.rtype)
        except KeyError:
            if entity is None:
                return {}
            rschema = entity.e_schema.rdef(self.rtype, self.role)
            value = rschema.default
        else:
            value = self._type(value)
            if entity is not None and getattr(entity, self.orm_rtype) == value:
                # Do not trigger update, if the value has not changed.
                # This is useful for PUT requests for which all fields should
                # be present even if they are not changed. By skipping
                # unchanged value, we avoid possible security check that would
                # be meaningless since the value is not changed.
                return {}
        return {self.orm_rtype: value}

    def serialize(self, entity):
        value = getattr(entity, self.orm_rtype)
        if value is not None:
            return self._value(value)

    @staticmethod
    def _value(value):
        """Return the serializable value from attribute `value`."""
        return value


class ChoiceStringField(jsl.fields.StringField):
    """A string field with choices described in a oneOf array with items made
    of {'enum': [<choice value>], 'title': <choice title>} objects.
    """

    def __init__(self, choices, **kwargs):
        super(ChoiceStringField, self).__init__(**kwargs)
        self.choices = choices

    def get_definitions_and_schema(self, **kwargs):
        definitions, schema = super(
            ChoiceStringField, self).get_definitions_and_schema(**kwargs)
        schema['oneOf'] = [{'enum': [value], 'title': title}
                           for value, title in self.choices]
        return definitions, schema


class StringMapper(AttributeMapper):
    """Attribute mapper for Yams' String type."""
    __select__ = yams_match(target_types='String')
    jsl_field_class = jsl.fields.StringField
    _type = text_type


class FloatMapper(AttributeMapper):
    """Attribute mapper for Yams' Float type."""
    __select__ = yams_match(target_types='Float')
    jsl_field_class = jsl.fields.NumberField


class IntMapper(AttributeMapper):
    """Attribute mapper for Yams' Int type."""
    __select__ = yams_match(target_types='Int')
    jsl_field_class = jsl.fields.IntField


class BooleanMapper(AttributeMapper):
    """Attribute mapper for Yams' Boolean type."""
    __select__ = yams_match(target_types='Boolean')
    jsl_field_class = jsl.fields.BooleanField


class PasswordMapper(AttributeMapper):
    """Attribute mapper for Yams' Password type."""
    __select__ = yams_match(target_types='Password')
    jsl_field_class = jsl.fields.StringField
    #:
    format = 'password'

    def jsl_field(self, schema_role, **kwargs):
        if schema_role == EDITION_ROLE:
            kwargs.setdefault('required', False)
        return super(PasswordMapper, self).jsl_field(schema_role, **kwargs)

    def values(self, entity, instance):
        password_changed = self.orm_rtype in instance
        values = super(PasswordMapper, self).values(entity, instance)
        if entity is not None and not password_changed:
            # We don't want the Password value to be reset if it has not
            # changed.
            del values[self.orm_rtype]
        return values

    def serialize(self, entity):
        return None

    @staticmethod
    def _type(json_value):
        """Return an encoded string suitable for Password type."""
        return json_value.encode('utf-8')


class DateMapper(StringMapper):
    """Attribute mapper for Yams' Date type."""
    __select__ = yams_match(target_types=('Date'))
    #:
    format = 'date'

    @staticmethod
    def _type(value):
        """Return a datetime object parsed from ISO8601 `value` string."""
        return iso8601.parse_date(value)


class DatetimeMapper(DateMapper):
    """Attribute mapper for Yams' (TZ)Datetime type."""
    __select__ = yams_match(target_types=('Datetime', 'TZDatetime'))
    #:
    format = 'date-time'


class BytesMapper(StringMapper):
    """Attribute mapper for Yams' Bytes type."""
    __select__ = yams_match(target_types='Bytes')

    @staticmethod
    def _type(value):
        """Return a Binary containing `value`."""
        return Binary(value.encode('utf-8'))

    @staticmethod
    def _value(value):
        """Return a unicode string from Binary `value`."""
        return value.getvalue().decode('utf-8')


class CompoundMapper(JSONSchemaMapper):
    """Mapper for a "compound" field gathering Yams relations into a
    dedicated JSON "object" to be inserted in "definitions" key of the JSON
    Schema document.

    The compound "object" will appear in the main JSON Schema document's
    properties under the `name` class attribute (defaults to class name).
    """
    __regid__ = 'jsonschema.object'
    __abstract__ = True
    __select__ = partial_yams_match()

    #: entity type holding this compound field.
    etype = None
    #: sequence of relations gathered in this compound field
    relations = ()
    #: title of the field
    title = None

    # sequence of 'relation/role' computed from 'relations'
    _relations = ()

    @classproperty
    def name(cls):
        """name of the property to be inserted in the main JSON Schema
        document (defaults to class name).
        """
        return text_type(cls.__name__)

    @classmethod
    def __registered__(cls, reg):
        if not cls.relations:
            raise ValueError(
                '{} is missing a "relations" class attribute'.format(cls))
        # Compute relation/role pairs from relations
        relations = []
        for relinfo in cls.relations:
            try:
                rtype, role = relinfo
            except ValueError:
                rtype = relinfo
                role = 'subject'
            relations.append((rtype, role))
        cls._relations = tuple(relations)
        # Check for name or relation duplication
        for obj in reg[cls.__regid__]:
            if obj == cls:
                continue
            if obj.etype == cls.etype:
                if obj.name == cls.name:
                    # Make sure 'name' is unique amongst objects with
                    # 'jsonschema.object' regid.
                    raise ValueError('a class with name "{}" is already '
                                     'registered'.format(cls.name))
                # Prevent duplicate mapping of the same etype/rtype.
                common_rtypes = set(obj._relations) & set(cls._relations)
                if common_rtypes:
                    raise ValueError(
                        'duplicate relation mapping for "{}": {}'.format(
                            cls.etype,
                            ', '.join('-'.join(rel) for rel in common_rtypes),
                        )
                    )
        # Hide relations mapped to this document from etype JSON Schema.
        for rtype, role in cls._relations:
            if role == 'object':
                jsonschema_section.tag_object_of(
                    ('*', rtype, cls.etype), 'hidden')
            else:
                jsonschema_section.tag_subject_of(
                    (cls.etype, rtype, '*'), 'hidden')
        return super(CompoundMapper, cls).__registered__(reg)

    @property
    def jsl_field_class(self):
        return partial(jsl.fields.DocumentField, as_ref=True,
                       title=self._cw._(self.title))

    def jsl_field(self, schema_role):
        attrs = {}
        for rtype, role in self._relations:
            rschema = self._cw.vreg.schema[rtype]
            target_types = {
                t.type for t in rschema.targets(self.etype, role)}
            mapper = self._cw.vreg['mappers'].select(
                'jsonschema.relation', self._cw,
                etype=self.etype, rtype=rtype, role=role,
                target_types=target_types,
            )
            attrs[mapper.orm_rtype] = mapper.jsl_field(schema_role)
        attrs['Options'] = default_options(self._cw, self.title)
        doc = type(str(self.title), (jsl.Document, ), attrs)
        return self.jsl_field_class(doc)

    def values(self, entity, instance):
        assert entity is None or entity.cw_etype == self.etype, \
            'cannot get "values" for {} with {}'.format(entity, self)
        try:
            values = instance.pop(self.name)
        except KeyError:
            if entity is None:
                return {}
            # Continue with an empty "value" that would get filled by compound
            # relation mappers with default or None values.
            values = {}
        for rtype, role in self._relations:
            mapper = self._relation_mapper(rtype, role)
            values.update(
                mapper.values(entity, values))
        return values

    def serialize(self, entity):
        assert entity.cw_etype == self.etype, \
            'cannot serialize {} with {}'.format(entity, self)
        data = {}
        for rtype, role in self._relations:
            mapper = self._relation_mapper(rtype, role)
            value = mapper.serialize(entity)
            if value is not None:
                data[mapper.orm_rtype] = value
        return data

    def _relation_mapper(self, rtype, role='subject'):
        vreg = self._cw.vreg
        rschema = vreg.schema[rtype]
        target_types = {t.type for t in rschema.targets(self.etype, role)}
        return vreg['mappers'].select(
            'jsonschema.relation', self._cw, etype=self.etype,
            rtype=rtype, role=role, target_types=target_types,
        )


class _RelationMapper(BaseRelationMapper):
    """Abstract class for true relation (as opposed to attribute) mapper.
    """
    __abstract__ = True
    __select__ = ~yams_final_rtype()
    jsl_field_class = jsl.fields.ArrayField

    def jsl_field(self, schema_role, **kwargs):
        if 'items' not in kwargs:
            targets = list(self.jsl_field_targets(schema_role))
            cardinalities = set([])
            rschema = self._cw.vreg.schema[self.rtype]
            for target_type in self.target_types:
                rdef = rschema.role_rdef(
                    self.etype, target_type, self.role)
                cardinalities.add(rdef.role_cardinality(self.role))
            if len(targets) > 1:
                kwargs['items'] = jsl.fields.OneOfField(targets)
            else:
                kwargs['items'] = targets[0]
            if schema_role in (CREATION_ROLE, EDITION_ROLE):
                cardinality = cardinalities.pop()
                if cardinalities:
                    raise BadSchemaDefinition(
                        'inconsistent cardinalities within {0} relation '
                        'definitions'.format(self.rtype))
                if cardinality != '*':
                    if 'required' not in kwargs and cardinality in '1+':
                        kwargs['required'] = True
                    if 'min_items' not in kwargs:
                        kwargs['min_items'] = 0 if cardinality in '?' else 1
                    if 'max_items' not in kwargs and cardinality in '?1':
                        kwargs['max_items'] = 1
        return super(_RelationMapper, self).jsl_field(schema_role, **kwargs)

    def jsl_field_targets(self, schema_role):
        """Return an iterator on jsl field objects to put in the 'items' key."""
        raise NotImplementedError()


class InlinedRelationMapper(_RelationMapper):
    """Map relation as 'inlined', i.e. the target of the relation is
    created/edited along with its original entity.
    """
    __select__ = (_RelationMapper.__select__
                  & yams_component_target()
                  & (match_kwargs('etype') | match_kwargs('entity')))

    def jsl_field_targets(self, schema_role):
        for target_type in self.target_types:
            mapper = self._cw.vreg['mappers'].select(
                'jsonschema.entity', self._cw, etype=target_type,
                rtype=self.rtype, role=neg_role(self.role),
                target_types={self.etype},
            )
            target_document = mapper.jsl_document(schema_role)
            yield jsl.fields.DocumentField(target_document, as_ref=True)

    def values(self, entity, instance):
        # Would require knownledge of the target type from "instance",
        # but the generated JSON schema does not expose this yet.
        assert len(self.target_types) == 1, \
            'cannot handle multiple target types yet: {}'.format(
                self.target_types)
        target_type = self.target_types[0]
        try:
            values = instance.pop(self.rtype)
        except KeyError:
            if entity is None:
                return {}
            values = []
        if not isinstance(values, list):
            # TODO: rather jsonschema.validate()
            raise ValidationError(entity,
                                  {self.rtype: _('value should be an array')})
        if entity is not None:
            # if entity already exists, delete entities related through
            # this mapped relation
            for linked_entity in getattr(entity, self.orm_rtype):
                if linked_entity.cw_etype in self.target_types:
                    linked_entity.cw_delete()
        target_mapper = self._cw.vreg['mappers'].select(
            'jsonschema.entity', self._cw, etype=target_type,
            rtype=self.rtype, role=neg_role(self.role),
            target_types={self.etype},
        )
        result = []
        for subinstance in values:
            subvalues = target_mapper.values(subinstance)
            result.append(self._cw.create_entity(target_type, **subvalues))
        return {self.orm_rtype: result}

    def serialize(self, entity):
        rset = entity.related(
            self.rtype, self.role, targettypes=tuple(self.target_types))
        if not rset:
            return None

        def serialize(entity):
            mapper = self._cw.vreg['mappers'].select(
                'jsonschema.entity', self._cw, entity=entity,
                rtype=self.rtype, role=neg_role(self.role),
                target_types={self.etype},
            )
            return mapper.serialize()

        return [serialize(related) for related in rset.entities()]


class ETypeRelationMapper(_RelationMapper):
    """Map relation as 'generic', i.e. the target of the relation may be
    selected in preexisting possible targets.
    """
    __select__ = (_RelationMapper.__select__
                  & ~yams_component_target()
                  & match_kwargs('etype'))

    def relation_targets(self, schema_role):
        entity = self._cw.vreg['etypes'].etype_class(self.etype)(self._cw)
        potential_targets = []
        for target_type in self.target_types:
            potential_targets.extend(entity.unrelated(
                self.rtype, target_type, self.role).entities())
        return potential_targets

    def jsl_field_targets(self, schema_role):
        choices = []
        for target in self.relation_targets(schema_role):
            choices.append((text_type(target.eid), target.dc_title()))
        yield ChoiceStringField(choices, type='string')

    def values(self, entity, instance):
        """
        Handling of reverse dependant entities creation is done by returning
        keys starting by __post_create. These keys contain a dictionary:
        {
            type: entity type used for creating the new entity
            values: a dictionary for attributes passed to this new entity
            relation: name of the relation added pointing to the main entity
        }
        These keys can also contain a list of such dictionaries.
        """
        try:
            values = instance.pop(self.rtype)
        except KeyError:
            return {}
        if entity is not None:
            entity.cw_set(**{self.orm_rtype: None})
        return {self.orm_rtype: [int(x) for x in values]}

    def serialize(self, entity):
        rset = entity.related(
            self.rtype, self.role, targettypes=tuple(self.target_types))
        if not rset:
            return None
        return [text_type(x.eid) for x in rset.entities()]


class EntityRelationMapper(ETypeRelationMapper):
    """Map relation using existing relations target when role is view,
    fallback to ETypeMapper otherwise to display all possible relation
    targets.
    """
    __select__ = (_RelationMapper.__select__
                  & ~yams_component_target()
                  & match_kwargs('entity'))

    def relation_targets(self, schema_role):
        entity = self.cw_extra_kwargs['entity']
        if schema_role == VIEW_ROLE:
            return entity.related(
                self.rtype, self.role,
                targettypes=tuple(self.target_types)).entities()
        if schema_role == CREATION_ROLE:
            assert len(self.target_types) == 1, \
                'cannot handle multiple target types in {} for {}'.format(
                    self, schema_role)
            targettype = self.target_types[0]
            return entity.unrelated(
                self.rtype, targettype, role=self.role,
            ).entities()
        return super(EntityRelationMapper, self).relation_targets(schema_role)
