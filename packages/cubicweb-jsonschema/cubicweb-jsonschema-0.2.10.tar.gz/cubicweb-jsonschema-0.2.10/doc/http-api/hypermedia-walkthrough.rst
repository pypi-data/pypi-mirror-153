.. _hypermedia-walkthrough:

Hypermedia walkthrough
~~~~~~~~~~~~~~~~~~~~~~

This page goes through possible navigation steps from the point of view of an
hypermedia-aware client talking to a cubicweb-jsonschema server.

Site root
+++++++++

We start our navigation from the root URL of the application with a `GET`
request:

.. code-block:: python

    >>> r = client.get('/', headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 204 No Content
    Allow: GET
    Link: </schema>; rel="describedby"; type="application/schema+json"

The application root does not contain any data, hence the ``204 No Content``
response status. Notice the ``Link`` with a ``rel="describedby"`` which is the
canonical way of indicating the JSON Schema location of a resource (here the
root resource). So let's fetch it at ``/schema``:

.. code-block:: python

    >>> r = client.get('/schema',
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    Link: </>; rel="describes"; type="application/json"
    {
       "title": "test app",
       "type": "null",
       "links" : [
          {
             "rel" : "collection",
             "href" : "/author/",
             "targetSchema" : {
                "$ref" : "/author/schema"
             },
             "submissionSchema" : {
                "$ref" : "/author/schema?role=creation"
             },
             "title" : "Author_plural"
          },
          {
             "rel" : "collection",
             "href" : "/book/",
             "targetSchema" : {
                "$ref" : "/book/schema"
             },
             "submissionSchema" : {
                "$ref" : "/book/schema?role=creation"
             },
             "title" : "Book_plural"
          }
       ]
    }
    >>> application_schema = r.json

Collections links
+++++++++++++++++

From the application schema, the client can follow one of the
`rel="collection"` links, for instance the one with ``href="/book/"``:

.. code-block:: python

    >>> books_link = application_schema['links'][1]

and try a HEAD request on URI specified by ``href``:

.. note:: For now, we need to pass the ``Accept`` header in HEAD request, this
    is a temporary limitation because handling of this verb is not implemented
    and falls back to a GET request.

.. code-block:: python

    >>> print(client.head(books_link['href'],
    ...                   headers={'accept': 'application/json'}))
    Response: 200 OK
    Allow: GET
    Link: </book/schema>; rel="describedby"; type="application/schema+json"

which means that we're only able to GET a resource at ``/book/`` endpoint.

Would the client be logged-in:

.. code-block:: python

    >>> _ = client.login()

we'd now get:

.. code-block:: python

    >>> print(client.head(books_link['href'],
    ...                   headers={'accept': 'application/json'}))
    Response: 200 OK
    Allow: GET, POST
    Link: </book/schema>; rel="describedby"; type="application/schema+json"

now we can post at this endpoint and we must, for that, follow the ``schema``
referenced in the link, so let's fetch it first:

.. code-block:: python

    >>> r = client.get(books_link['submissionSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    {
       "$schema": "http://json-schema.org/draft-06/schema#",
       "type" : "object",
       "title" : "Book",
       "properties" : {
          "title" : {
             "type" : "string",
             "title" : "title"
          },
          "publication_date": {
              "format": "date",
              "type": "string",
              "title": "publication_date"
          }
       },
       "required" : [
          "title"
       ],
       "additionalProperties" : false
    }

and then perform a ``POST`` request with a payload matching the above schema:

.. code-block:: python

    >>> r = client.post_json(books_link['href'],
    ...                      {'title': 'The Old Man and the Sea'},
    ...                      headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/book/.../
    {
        "title": "The Old Man and the Sea"
    }

The response of this ``POST`` request contains a ``Location`` header. This is
the primary information a client should follow to navigate to the new
ressource.

Now if the client wants to move on to the *collection* of books, it should
follow the ``href`` URL with a GET in HTTP

.. code-block:: python

    >>> r = client.get(books_link['href'],
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </book/schema>; rel="describedby"; type="application/schema+json"
    [
        {
            "type": "book",
            "id": "...",
            "title": "The Old Man and the Sea"
        }
    ]
    >>> books = r.json

and expect something matching the ``targetSchema`` entry of the link (which
indicates the schema of the domain of the relation):

.. code-block:: python

    >>> r = client.get(books_link['targetSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    Link: </book/>; rel="describes"; type="application/json"
    {
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type" : "string"
          },
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          }
        },
        "links": [
          {
            "href": "/book/{id}",
            "rel": "item",
            "anchor": "#"
          }
        ]
      },
      "type": "array",
      "title": "Book_plural",
      "links": [
        {
          "title": "Book_plural",
          "targetSchema": {
            "$ref": "/book/schema"
          },
          "href": "/book/",
          "rel": "self",
          "submissionSchema": {
            "$ref": "/book/schema?role=creation"
          }
        }
      ]
    }
    >>> books_schema = r.json

From collection to items
++++++++++++++++++++++++

The schema above has a `rel="item"` link nested into the ``items`` property.
This can be used to manipulate an item of the collection (notice the ``"auchor":
"#"`` property of the link, indicating that the subject of the link is
actually the collection ``#`` and not the item). Each item can be fetched by
expanding the `templated`_ ``href`` of the link with an item of the collection
as context (here it's ``id`` property). For that we use the uritemplate_
Python package.

.. _templated: http://tools.ietf.org/html/rfc6570
.. _uritemplate: https://pypi.python.org/pypi/uritemplate

.. code-block:: python

    >>> from uritemplate import URITemplate
    >>> item_link = books_schema['items']['links'][0]
    >>> item_uritemplate = URITemplate(item_link['href'])
    >>> item_uri = item_uritemplate.expand(books[0])
    >>> item_response = client.get(item_uri,
    ...                            headers={'accept': 'application/json'})
    >>> print(item_response)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, PUT, DELETE
    Link: </book/.../schema>; rel="describedby"; type="application/schema+json"
    Content-Type: application/json
    {
        "title": "The Old Man and the Sea"
    }

Typically the client would also retrieve the JSON Schema of this resource
advertized by the ``Link`` header in previous response:

.. code-block:: python

    >>> item_schema_uri = item_response.headers['Link'].split('; ')[0][1:-1]
    >>> r = client.get(item_schema_uri,
    ...                headers={'accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "title": "Book",
        "type": "object",
        "properties": {
            "publication_date": {
                "format": "date",
                "type": "string",
                "title": "publication_date"
            },
            "title": {
                "type": "string",
                "title": "title"
            }
        },
        "additionalProperties": false,
        "links": [
            {
                "href": "/book/",
                "rel": "collection",
                "title": "Book_plural",
                "targetSchema": {
                  "$ref": "/book/schema"
                }
            },
            {
                "href": "/book/",
                "rel": "up",
                "title": "Book_plural",
                "targetSchema": {
                  "$ref": "/book/schema"
                }
            },
            {
                "href": "/book/.../",
                "rel": "self",
                "title": "Book #...",
                "targetSchema": {
                  "$ref": "/book/.../schema?role=view"
                },
                "submissionSchema": {
                  "$ref": "/book/.../schema?role=edition"
                }
            },
            {
                "href": "/book/.../author/",
                "rel": "related",
                "title": "author"
            },
            {
                "rel": "related",
                "href": "/book/.../topics/",
                "title": "topics"
            }
        ]
    }


Entity resource
+++++++++++++++

Now if we stay on this resource and retrieve its complete hyper schema which
is targetted by the ``rel="describedby"`` Link header in the resource
response.

.. code-block:: python

    >>> item_schema_uri = item_response.headers['Link'].split('; ')[0][1:-1]
    >>> r = client.get(item_schema_uri,
    ...                headers={'accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </book/.../>; rel="describes"; type="application/json"
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "title": "Book",
      "type": "object",
      "properties": {
        "publication_date": {
          "format": "date",
          "type": "string",
          "title": "publication_date"
        },
        "title": {
          "type": "string",
          "title": "title"
        }
      },
      "additionalProperties": false,
      "links": [
        {
          "targetSchema": {
            "$ref": "/book/schema"
          },
          "href": "/book/",
          "rel": "collection",
          "title": "Book_plural"
        },
        {
          "targetSchema": {
            "$ref": "/book/schema"
          },
          "href": "/book/",
          "rel": "up",
          "title": "Book_plural"
        },
        {
          "title": "Book #...",
          "targetSchema": {
            "$ref": "/book/.../schema?role=view"
          },
          "href": "/book/.../",
          "rel": "self",
          "submissionSchema": {
            "$ref": "/book/.../schema?role=edition"
          }
        },
        {
          "href": "/book/.../author/",
          "rel": "related",
          "title": "author"
        },
        {
          "href": "/book/.../topics/",
          "rel": "related",
          "title": "topics"
        }
      ]
    }
    >>> book_schema = r.json

We get a new ``rel="self"`` link which can be used to manipulate the resource.
For instance, as we have seen that we are allowed to perform a PUT request on
the resource, we can update it by following the ``submissionSchema`` property
of the link. So let's fetch the schema first:

.. code-block:: python

    >>> r = client.get(book_schema['links'][2]['submissionSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "title": "Book",
      "type": "object",
      "properties": {
        "publication_date": {
          "format": "date",
          "type": "string",
          "title": "publication_date"
        },
        "title": {
          "type": "string",
          "title": "title"
        }
      },
      "required": [
        "title"
      ],
      "additionalProperties": false
    }

and then we perform the ``PUT``:

.. code-block:: python

    >>> r = client.put_json(book_schema['links'][2]['href'],
    ...                     {'title': 'The Old Man and the Sea',
    ...                      'publication_date': '1952-08-25'},
    ...                     headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/book/.../
    {
        "title": "The Old Man and the Sea",
        "publication_date": "1952-08-25"
    }

Entity relationships
++++++++++++++++++++

Another kind of interesting links are ``rel="related"`` links which advertized
relationships between the current resource and related ones.

.. code-block:: python

    >>> topics_link = book_schema['links'][-1]
    >>> r = client.get(topics_link['href'],
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    Link: </book/.../topics/schema>; rel="describedby"; type="application/schema+json"
    []

No data yet here, let's follow the ``rel="describedby"`` Link to see what can
be done there.

.. _topics_relation_hyperschema:

.. code-block:: python

    >>> topics_schema_uri = r.headers['Link'].split('; ')[0][1:-1]
    >>> r = client.get(topics_schema_uri,
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r) # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </book/.../topics/>; rel="describes"; type="application/json"
    {
      "title": "topics",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string"
          },
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          }
        },
        "links": [
          {
            "href": "/book/.../topics/{id}",
            "anchor": "#",
            "rel": "item"
          }
        ]
      },
      "links": [
        {
          "title": "topics",
          "rel": "self",
          "href": "/book/.../topics/",
          "targetSchema": {
            "$ref": "/book/.../topics/schema?role=view"
          },
          "submissionSchema": {
            "$ref": "/book/.../topics/schema?role=creation"
          }
        }
      ]
    }
    >>> topics_schema = r.json

So in order to add a topic relation, we need to POST at URL specified in
``rel="self"`` link of this schema. Payload should also conform to the
``submissionSchema`` of the link, let's retrieve it first:

.. code-block:: python

    >>> r = client.get(topics_schema['links'][0]['submissionSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    {
      "title": "topics",
      "type": "array",
      "items": {
        "type": "string",
        "oneOf": [
          {
            "enum": [
              "..."
            ],
            "title": "sword fish"
          },
          {
            "enum": [
              "..."
            ],
            "title": "gardening"
          },
          {
            "enum": [
              "..."
            ],
            "title": "fishing"
          }
        ]
      }
    }
    >>> possible_topics = r.json['items']['oneOf']

We can create relationships with the ``Book`` entity by POST-ing to the
relationship route:

.. code-block:: python

    >>> fishing_topic = [t['enum'][0] for t in possible_topics
    ...                  if t['title'] == 'fishing']
    >>> r = client.post_json(topics_link['href'], fishing_topic,
    ...                      headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 204 No Content

Now if we retrieve back the relation URL:

.. code-block:: python

    >>> r = client.get(topics_link['href'],
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    Link: </book/.../topics/schema>; rel="describedby"; type="application/schema+json"
    [
      {
        "type": "topic",
        "id": "...",
        "title": "fishing"
      }
    ]
    >>> topics = r.json

we have an item in the ``topics`` collection.

If we now come back to the `/book/.../topics/schema
<topics_relation_hyperschema_>`_ response we got earlier, we can now use the
``rel="item"`` link to fetch an item of the collection given the `URI template
<templated_>`_ ``/book/.../topics/{id}`` and the above response.

.. code-block:: python

    >>> from uritemplate import URITemplate
    >>> item_link = topics_schema['items']['links'][0]
    >>> item_uritemplate = URITemplate(item_link['href'])
    >>> item_uri = item_uritemplate.expand(topics[0])
    >>> item_response = client.get(item_uri,
    ...                            headers={'accept': 'application/json'})
    >>> print(item_response)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, PUT, DELETE
    Link: </book/.../topics/.../schema>; rel="describedby"; type="application/schema+json"
    Content-Type: application/json
    {
      "name": "fishing"
    }

along with its JSON Schema as advertized by the ``rel="describedby"`` `Link`
header:

.. code-block:: python

    >>> related_topic_schema_uri = item_response.headers['Link'].split('; ')[0][1:-1]
    >>> r = client.get(related_topic_schema_uri,
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </book/.../topics/.../>; rel="describes"; type="application/json"
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "title": "Topic",
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "title": "name"
        }
      },
      "additionalProperties": false,
      "links": [
        {
          "href": "/book/.../topics/",
          "rel": "collection",
          "title": "Topic_plural",
          "targetSchema": {
            "$ref": "/book/.../topics/schema"
          }
        },
        {
          "href": "/book/.../topics/",
          "rel": "up",
          "title": "Topic_plural",
          "targetSchema": {
            "$ref": "/book/.../topics/schema"
          }
        },
        {
          "href": "/book/.../topics/.../",
          "rel": "self",
          "title": "Topic #...",
          "targetSchema": {
            "$ref": "/book/.../topics/.../schema?role=view"
          },
          "submissionSchema": {
            "$ref": "/book/.../topics/.../schema?role=edition"
          }
        }
      ]
    }
    >>> fishing_topic_schema = r.json

Notice the ``rel="self"`` link which can (as for any resource) be used to
manipulate the related entity. In particular, should we want to update the
related topic, we'd need to conform the the ``submissionSchema``:

.. code-block:: python

    >>> r = client.get(fishing_topic_schema['links'][-1]['submissionSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "title": "Topic",
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "title": "name"
        }
      },
      "required": [
        "name"
      ],
      "additionalProperties": false
    }

So let's update the "fishing" topic and change it's name:

.. code-block:: python

    >>> r = client.put_json(item_uri, {'name': 'fish hunting'},
    ...                     headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/book/.../topics/.../
    {
      "name": "fish hunting"
    }

Let's now fetch back the relation schema:

.. code-block:: python

    >>> r = client.get(topics_schema['links'][0]['targetSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    {
      "title": "topics",
      "type": "array",
      "items": {
        "type": "string",
        "oneOf": [
          {
            "enum": [
              "..."
            ],
            "title": "fish hunting"
          }
        ]
      }
    }

we notice that the ``items`` of the array contains a ``oneOf`` constraint
which lists schemas for existing relations.

Another request on *topics* link's ``submissionSchema``:

.. code-block:: python

    >>> r = client.get(topics_schema['links'][0]['submissionSchema']['$ref'],
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    {
      "title": "topics",
      "type": "array",
      "items": {
        "type": "string",
        "oneOf": [
          {
            "enum": [
              "..."
            ],
            "title": "sword fish"
          },
          {
            "enum": [
              "..."
            ],
            "title": "gardening"
          }
        ]
      }
    }

We can see that only *unrelated* targets are listed in the ``oneOf`` property
of ``submissionSchema``.
