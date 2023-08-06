.. image:: https://jenkins.logilab.org/job/cubicweb-jsonschema/badge/icon
  :target: https://jenkins.logilab.org/job/cubicweb-jsonschema/

===================
cubicweb-jsonschema
===================

`cubicweb-jsonschema`_ provides mappings from CubicWeb entities to `JSON Schema`_
documents as well as an HTTP API based on the `JSON Hyper-Schema`_
specification.

.. _`cubicweb-jsonschema`: \
    https://www.cubicweb.org/project/cubicweb-jsonschema
.. _`JSON Schema`: http://json-schema.org/
.. _`JSON Hyper-Schema`: \
    http://json-schema.org/latest/json-schema-hypermedia.html

Documentation is available at https://cubicweb-jsonschema.readthedocs.io/

Testing
-------

Tests can be run using:

::

    python -m unittest discover -s test

from top-level directory after having installed test dependencies from file
``test-requirements.txt``.

Some tests make use of the ajv_ program (more specifically `ajv-cli`_) to
validate JSON Schema response against meta schema. This can be installed using
`npm` and should be in ``$PATH`` when running tests. If not available
validation would not occur.

.. _ajv: http://epoberezkin.github.io/ajv/
.. _`ajv-cli`: https://github.com/jessedc/ajv-cli
