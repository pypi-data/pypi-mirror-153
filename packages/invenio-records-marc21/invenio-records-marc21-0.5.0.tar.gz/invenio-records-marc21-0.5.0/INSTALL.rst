Installation
============

Invenio-Records-Marc21 is on PyPI so all you need is:

.. code-block:: console

   $ pip install invenio-records-marc21


Choose a version of elasticsearch and a DB, if you want to test the module.
The installation [options] supported for the Marc21 module:

  ``docs``
      for documentation building dependencies;
  ``elasticsearch7``
      to use elasticsearch version 7 backend;    
  ``postgresql``
      to use PostgreSQL database backend;
  ``tests``
      for test dependencies.

An example installation:

.. code-block:: console
    
   pip install -e .[all,elasticsearch7,postgresql]

