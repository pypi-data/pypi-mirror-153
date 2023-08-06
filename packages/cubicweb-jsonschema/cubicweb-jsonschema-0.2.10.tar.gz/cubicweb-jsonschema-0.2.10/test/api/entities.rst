Collection resources (entities)
-------------------------------

.. code-block:: python

    >>> resp = client.get('/author/',
    ...                   headers={'accept': 'application/json'})
    >>> print(resp)
    Response: 200 OK
    Allow: GET
    Content-Type: application/json
    []


Now if we login, we get an additional ``Allow: POST`` header, meaning the
server would accept the creation of entity of type ``Author`` at the
``/author`` endpoint:

.. code-block:: python

    >>> _ = client.login()
    >>> resp = client.get('/author/',
    ...                   headers={'accept': 'application/json'})
    >>> print(resp)
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    []

So let's add some ``Author`` entities:

.. code-block:: python

    >>> resp = client.post_json('/author/', {'name': 'Victor Hugo'},
    ...                         headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/author/.../
    {
        "name": "Victor Hugo"
    }
    >>> resp = client.post_json('/author/', {'name': 'Ernest Hemingway'},
    ...                         headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/author/.../
    {
        "name": "Ernest Hemingway"
    }

Now we have something in the author collection:

.. code-block:: python

    >>> resp = client.get('/author/',
    ...                   headers={'accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    [
        {
            "type": "author",
            "id": "...",
            "title": "Ernest Hemingway"
        },
        {
            "type": "author",
            "id": "...",
            "title": "Victor Hugo"
        }
    ]
