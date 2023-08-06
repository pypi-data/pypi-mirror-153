Application schema
------------------

The application schema consists of hyper schema links with top-level entity
types in the application.

.. code-block:: python

    >>> resp = client.get_schema('/schema')
    >>> print(resp)
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
