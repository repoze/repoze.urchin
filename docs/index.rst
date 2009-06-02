Documentation for repoze.urchin
===============================

This package provides WSGI middleware for injecting the markup
required to use Google Analytics into web pages.


.. toctree::
   :maxdepth: 2

Configuring the Middleware
--------------------------

In your :mod:`Paste` configuration file, add a stanza which uses
the middleware provided by this pacakge, and which supplies your
Google Analytics account ID::

  [filter:urchin]
  use = egg:repoze.urchin#middleware
  account = UA-1234567-8

Then add that filter to your pipeline::

  [pipeline:main]
  pipeline =
      ...
      urchin
      <your appname>

See ``example.ini`` for a working example.
 

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
