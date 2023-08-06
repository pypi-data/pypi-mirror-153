Entity type schema
------------------

On a given entity type we get the following schema:

.. code-block:: python

    >>> resp = client.get_schema('/author/schema')
    >>> print(resp)
    Response: 200 OK
    Content-Type: application/json
    Link: </author/>; rel="describes"; type="application/json"
    {
       "title" : "Author_plural",
       "items" : {
          "properties" : {
             "type" : {
                "type" : "string"
             },
             "id" : {
                "type" : "string"
             },
             "title" : {
                "type" : "string"
             }
          },
          "type" : "object",
          "links": [
             {
                "rel" : "item",
                "href" : "/author/{id}",
                "anchor": "#"
             }
         ]
       },
       "type" : "array",
       "links" : [
          {
             "rel" : "self",
             "href" : "/author/",
             "targetSchema" : {
                "$ref" : "/author/schema"
             },
             "submissionSchema" : {
                "$ref" : "/author/schema?role=creation"
             },
             "title" : "Author_plural"
          }
       ]
    }
    >>> author_etype_hyperschema = resp.json

Hyperschema links
+++++++++++++++++

Let's now follow one the links above, for instance to get the schema that
needs to be respected in order to perform *creation* of an entity:

.. code-block:: python

    >>> self_link = author_etype_hyperschema['links'][0]
    >>> resp = client.get_schema(self_link['submissionSchema']['$ref'])
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
       "required" : [
          "name"
       ],
       "additionalProperties" : false
    }
