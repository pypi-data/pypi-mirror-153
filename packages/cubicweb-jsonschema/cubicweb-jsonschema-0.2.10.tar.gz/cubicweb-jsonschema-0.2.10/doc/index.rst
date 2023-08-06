.. cubicweb-jsonschema documentation master file, created by
   sphinx-quickstart on Thu Mar 23 12:15:30 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cubicweb-jsonschema's documentation!
===============================================

`cubicweb-jsonschema`_ provides mappings from CubicWeb entities to `JSON Schema`_
documents as well as an HTTP API based on the `JSON Hyper-Schema`_
specification.

.. _`cubicweb-jsonschema`: \
    https://www.cubicweb.org/project/cubicweb-jsonschema
.. _`JSON Schema`: http://json-schema.org/
.. _`JSON Hyper-Schema`: \
    http://json-schema.org/latest/json-schema-hypermedia.html


.. include:: contributing.rst


HTTP API
--------

This part of the documentation describes the HTTP API provided by
cubicweb-jsonschema. Start reading the :ref:`hypermedia-walkthrough`.

.. toctree::
   :maxdepth: 1

   http-api/hypermedia-walkthrough
   http-api/schema-api/index
   http-api/api/index

.. note:: In Python code examples of pages in this section, ``client`` is a
    thin wrapper of `webtest.app.TestApp`_.

.. _`webtest.app.TestApp`: \
    http://docs.pylonsproject.org/projects/webtest/en/latest/api.html#webtest.app.TestApp


Developer interface
-------------------

This part of the documentation describes the developer interface (API) of
cubicweb-jsonschema.

.. toctree::
   :maxdepth: 1

   dev/mappers


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
