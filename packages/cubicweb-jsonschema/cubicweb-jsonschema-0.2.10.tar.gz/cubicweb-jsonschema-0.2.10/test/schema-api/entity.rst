Entity schema
-------------

Before examining entity's schema, we need an entity so let's create one of
type ``Author``, by posting data at the ``/author/`` route:

.. code-block:: python

    >>> _ = client.login()
    >>> r = client.post_json('/author/', {'name': 'bob'},
    ...                      headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/author/.../
    {
      "name": "bob"
    }
    >>> entity_url = r.location

On our ``Author`` entity we get the following schema:

.. code-block:: python

    >>> resp = client.get_schema(entity_url + '/schema')
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </author/.../>; rel="describes"; type="application/json"
    {
       "$schema": "http://json-schema.org/draft-06/schema#",
       "title" : "Author",
       "type" : "object",
       "properties" : {
          "name" : {
             "title" : "name",
             "type" : "string"
          }
       },
       "additionalProperties" : false,
       "links" : [
          {
             "rel" : "collection",
             "href" : "/author/",
             "targetSchema" : {
                "$ref" : "/author/schema"
             },
             "title" : "Author_plural"
          },
          {
             "rel" : "up",
             "href" : "/author/",
             "targetSchema" : {
                "$ref" : "/author/schema"
             },
             "title" : "Author_plural"
          },
          {
             "rel" : "self",
             "href" : "/author/.../",
             "targetSchema" : {
                "$ref" : "/author/.../schema?role=view"
             },
             "submissionSchema" : {
                "$ref" : "/author/.../schema?role=edition"
             },
             "title" : "Author #..."
          },
          {
            "href": "/author/.../publications/",
            "rel": "related",
            "title": "publications"
          }
       ]
    }
    >>> author_hyperschema = resp.json


Hyperschema links
+++++++++++++++++

Let's now follow the ``self`` link above which indicates how to interact with
the current resource (entity). For instance, would we need to perform
*edition* of this resource we should send a request to ``self`` link's
``href`` URL with a payload matching the JSON Schema pointed at by ``schema``
property of the link:

.. code-block:: python

    >>> self_link = author_hyperschema['links'][2]
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

On the other hand, ``self`` link's ``targetSchema`` is:

.. code-block:: python

    >>> resp = client.get_schema(self_link['targetSchema']['$ref'])
    >>> print(resp)
    Response: 200 OK
    Content-Type: application/json
    {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "title": "Author",
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "title": "name"
          }
        },
        "additionalProperties": false
    }

which is exactly the same schema as found in the Hyper Schema obtained above.
