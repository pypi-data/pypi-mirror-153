Relationships
-------------

.. code-block:: python

    >>> _ = client.login()

Create an entity of type ``Book``.

.. code-block:: python

    >>> r = client.post_json('/book/', {'title': 'The Old Man and the Sea'},
    ...                      headers={'Accept': 'application/json'})
    >>> print(r.status)
    201 Created
    >>> entity_url = r.location

We can manipulate relationships an entity is the subject of through the
``<entity location>/<relation type>`` route. So for instance, to manipulate
``topics`` of the ``Book`` entity we just created:

.. code-block:: python

    >>> topics_route = entity_url + '/topics'
    >>> r = client.get(topics_route,
    ...                headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    Allow: GET, POST
    []

Since our book has no topic yet, we get an empty array.

In order to add a `topics` relationship to our book, we first need to fetch
available ``Topic`` entities:

.. code-block:: python

    >>> r = client.get('/topic/',
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    [
      {
        "type": "topic",
        "id": "...",
        "title": "sword fish"
      },
      {
        "type": "topic",
        "id": "...",
        "title": "gardening"
      },
      {
        "type": "topic",
        "id": "...",
        "title": "fishing"
      }
    ]
    >>> topics = r.json

We can create relationships with the ``Book`` entity by POST-ing to the
relationship route:

.. code-block:: python

    >>> relevant_topics = [t['id'] for t in topics if t['title'] != 'gardening']
    >>> r = client.post_json(topics_route, relevant_topics,
    ...                      headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 204 No Content

.. note:: We get a "Not Content" response because the request was successfully
    processed but the server does not send back the content of the *related*
    collection.

Now we have topics related to our book:

.. code-block:: python

    >>> r = client.get(topics_route,
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    [
      {
        "type": "topic",
        "id": "...",
        "title": "sword fish"
      },
      {
        "type": "topic",
        "id": "...",
        "title": "fishing"
      }
    ]
    >>> book_topics = r.json

Individual related resources (as opposed to the *collection* of related
resources) can also be manipulated through ``<entity location>/<relation
type>/<target id>`` route.

.. code-block:: python

    >>> first_topic_uri = '/'.join([topics_route, book_topics[0]['id']])
    >>> r = client.get(first_topic_uri,
    ...                headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 200 OK
    Allow: GET, PUT, DELETE
    Content-Type: application/json
    {
      "name": "sword fish"
    }

Following what's advertized by the ``Allow`` header, we can modify the related
resource:

.. code-block:: python

    >>> r = client.put_json(first_topic_uri, {"name": "big sword fish"},
    ...                     headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/book/.../topics/.../
    {
      "name": "big sword fish"
    }

.. note:: Maybe the ``Location`` should be be the canonical location of the
    resource of (i.e. ``https://localhost:80/topic/...``)?

We can issue a ``DELETE`` request on that resource; this will actually delete
the relationship between the book and the topic:

.. code-block:: python

    >>> r = client.delete(first_topic_uri)
    >>> print(r)
    Response: 204 No Content

Depending on the data model, deleting a relation may also delete the related
resource (typically if the relation is *composite* on subject here). Though,
here this is not the case for ``topics`` relationship so our `big sword fish`
topic still exists:

.. code-block:: python

    >>> r = client.get('/topic/',
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    [
      {
        "type": "topic",
        "id": "...",
        "title": "big sword fish"
      },
      {
        "type": "topic",
        "id": "...",
        "title": "gardening"
      },
      {
        "type": "topic",
        "id": "...",
        "title": "fishing"
      }
    ]
