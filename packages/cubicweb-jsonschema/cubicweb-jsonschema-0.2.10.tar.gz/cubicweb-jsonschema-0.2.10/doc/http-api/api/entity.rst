Single entity resource
----------------------

To create an entity of type ``Author``, we `POST` on ``/author`` endpoint:

.. code-block:: python

    >>> _ = client.login()
    >>> resp = client.post_json('/author/',
    ...                         {'name': 'Ernest Hemingway'},
    ...                         headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/author/.../
    {
        "name": "Ernest Hemingway"
    }

Keep the resource location for further usage:

    >>> url = resp.location[len('https://localhost:80'):]

In case of invalid input data, we get a meaningful error message following
`rfc-7807 <https://tools.ietf.org/html/rfc7807>`_.

.. code-block:: python

    >>> resp = client.post_json('/author/', {}, status=422,
    ...                         headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 422 Unprocessable Entity
    Content-Type: application/problem+json; charset=UTF-8
    {
        "status": 422,
        "title": "Unprocessable Entity",
        "invalid-params": [{
            "reason": "required attribute",
            "name": "name-subject"
        }]
    }

To update an entity, we need to ``PUT`` the resource:

.. code-block:: python

    >>> resp = client.put_json(url, {'name': 'Ernest Miller Hemingway'},
    ...                        headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json; charset=UTF-8
    Location: https://localhost:80/author/.../
    {
        "name": "Ernest Miller Hemingway"
    }

Finally we can delete an entity:

.. code-block:: python

    >>> resp = client.delete(url)
    >>> print(resp)
    Response: 204 No Content

    >>> resp = client.get('/author/',
    ...                   headers={'accept': 'application/json'})
    >>> print(resp)
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    []
