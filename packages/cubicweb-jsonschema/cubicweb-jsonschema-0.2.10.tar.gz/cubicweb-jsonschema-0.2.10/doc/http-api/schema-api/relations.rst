Relationships schema
--------------------

.. note:: Features described here are experimental

There are special routing patterns that makes it possible to manipulate
relationships. Namely on an entity type, we can get the schema of a relation
with:

.. code-block:: python

    >>> url = '/book/relationships/author/schema?role=view'
    >>> resp = client.get_schema(url)
    >>> print(resp)
    Response: 200 OK
    Content-Type: application/json
    {
       "$schema": "http://json-schema.org/draft-06/schema#",
       "title" : "Author",
       "type" : "object",
       "properties" : {
          "name" : {
             "type" : "string",
             "title" : "name"
          }
       },
       "additionalProperties": false
    }

The routing also works the other way around (though this might go away in
future implementation):

.. code-block:: python

    >>> url = '/author/relationships/author/schema?role=creation'
    >>> resp = client.get_schema(url)
    >>> print(resp)
    Response: 200 OK
    Content-Type: application/json
    {
       "$schema": "http://json-schema.org/draft-06/schema#",
       "title" : "Book",
       "type" : "object",
       "properties" : {
          "publication_date": {
              "title": "publication_date",
              "type": "string",
              "format": "date"
          },
          "title" : {
             "type" : "string",
             "title" : "title"
          }
       },
       "required" : [
          "title"
       ],
       "additionalProperties" : false
    }
