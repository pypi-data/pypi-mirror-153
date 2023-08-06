Data model mappers between Yams and JSON Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: cubicweb_jsonschema.mappers

Module :mod:`cubicweb_jsonschema.mappers` provides appobjects that
aims at mapping Yams model definitions to JSON Schema ones.

These appobjects live in the ``mappers`` registry and are selectable with
context information in Yams/CubicWeb semantics:

* `etype` or `entity`: entity type or entity,
* `rtype`: relation type,
* `role`: role of `etype`/`entity` in `rtype` relation,
* `target_types`: target entity types of `rtype` relation with
  `etype`/`entity` as `role`.

The main predicate for these appobjects is :class:`yams_match`.

Mappers for relations
+++++++++++++++++++++

.. autoclass:: BaseRelationMapper
   :members: etype, rtype, role, target_types

   .. autoattribute:: __regid__

   To control JSON Schema generation through JSL:

   .. autoattribute:: jsl_field_class
      :annotation: to be implemented in concrete classes
   .. automethod:: jsl_field

   Methods to control serialization and deserialization from/to JSON Schema
   values:

   .. automethod:: serialize
   .. automethod:: values
   .. automethod:: _type

.. autoclass:: InlinedRelationMapper
   :members: jsl_field_class

.. autoclass:: ETypeRelationMapper
   :members:

.. autoclass:: EntityRelationMapper
   :members:

Final types mappers
+++++++++++++++++++

Based on relation mappers, :class:`AttributeMapper` is the base class for
mapping Yams final relation type (i.e. *attributes*).

.. autoclass:: AttributeMapper
   :members: format, attr, _type, _value

   .. autoattribute:: __regid__

All standard Yams final types have a default mapper:

.. autoclass:: StringMapper
   :members: jsl_field_class, _type
.. autoclass:: BytesMapper
   :members: jsl_field_class, _type, _value
.. autoclass:: FloatMapper
   :members: jsl_field_class
.. autoclass:: IntMapper
   :members: jsl_field_class
.. autoclass:: BooleanMapper
   :members: jsl_field_class
.. autoclass:: DateMapper
   :members: jsl_field_class, format
.. autoclass:: DatetimeMapper
   :members: jsl_field_class, format
.. autoclass:: PasswordMapper
   :members: jsl_field_class, format, _type

There are several ways to override default attribute mappers.

*   One define a custom `JSON Schema format`_ through the ``format`` class
    attribute:

    .. code-block:: python

        class EmailMapper(StringMapper):
            __select__ = yams_match(etype='EmailAddress',
                                    rtype='address', role='subject')
            format = 'email'

    and get the following schema for the ``address`` property of
    ``EmailAddress`` entity type:

    .. code-block:: json

        {
          "title": "EmailAddress",
          "type": "object",
          "properties": {
            "address": {
              "format": "email",
              "title": "address",
              "type": "string"
            },
            "alias": {
              "title": "alias",
              "type": "string"
            }
          }
        }


    .. _`JSON Schema format`: \
        http://json-schema.org/latest/json-schema-validation.html#rfc.section.8

*   Another possibility is to override `_type` and/or `_value` methods of an
    attribute mapper to control serialization and deserialization:

    .. code-block:: python

        class Base64BytesMapper(BytesMapper):
            """A mapper for Bytes attribute encoded in base64."""
            __select__ = yams_match(etype='File',
                                    rtype='data', role='subject',
                                    target_types='Bytes')

            @staticmethod
            def _type(value):
                return Binary(b64decode(value))

            @staticmethod
            def _value(value):
                return b64encode(value.getvalue()).decode('ascii')


Compound mappers
++++++++++++++++

:class:`CompoundMapper` can be used to define a JSON Schema sub-document
gathering a set of relations of a given entity type.

For example, consider the following Yams entity type definition:

.. code-block:: python

    class Photo(EntityType):
        longitude = Float()
        latitude = Float()
        taken_at = Datetime()

the following class defines a "geo" property to be inserted in the JSON Schema
document for "Photo" entity type:

.. code-block:: python

    class geo(CompoundMapper):
        etype = 'Photo'
        relations = ('longitude', 'latitude')
        title = _('Geographic Coordinates')

thus leading to the following JSON Schema:

.. code-block:: json

    {
      "type": "object",
      "title": "Photo",
      "properties": {
        "geo": {
          "$ref": "#/definitions/Geographic Coordinates"
        },
        "take_at": {
          "type": "string",
          "format": "date-time"
        }
      },
      "definitions": {
        "Geographic Coordinates": {
          "type": "object",
          "title": "Geographic Coordinates",
          "properties": {
            "longitude": {
              "type": "float"
            },
            "latitude": {
              "type": "float"
            }
          }
        }
      }
    }

.. autoclass:: CompoundMapper
   :members:

   .. autoattribute:: __regid__

Mappers for entity types and entities
+++++++++++++++++++++++++++++++++++++

.. autoclass:: ETypeMapper
   :members:

   .. autoattribute:: __regid__

.. autoclass:: TargetETypeMapper
   :members:

   .. autoattribute:: __regid__

.. autoclass:: EntityMapper
   :members:

   .. autoattribute:: __regid__

Mappers for entities as colletions and items
++++++++++++++++++++++++++++++++++++++++++++

The following mapper classes are used to represent entities as `collections` and
`items` of a collection. These are selected for entity types collection as
well as for targets of relation.

.. autoclass:: EntityCollectionMapper
   :members:

   .. autoattribute:: __regid__

.. autoclass:: RelatedCollectionMapper
   :members:

   .. autoattribute:: __regid__

.. autoclass:: CollectionItemMapper
   :members:

   .. autoattribute:: __regid__

Predicates
++++++++++

.. autoclass:: yams_match
.. autoclass:: yams_final_rtype
.. autoclass:: yams_component_target
