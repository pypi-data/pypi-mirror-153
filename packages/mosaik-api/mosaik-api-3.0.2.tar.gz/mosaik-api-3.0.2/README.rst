Mosaik API for Python
=====================

This is an implementation of the mosaik API for simulators written in Python.
It hides all the messaging and networking related stuff and provides a simple
base class that you can implement.


Installation
------------

Just use `pip <https://pip.pypa.io>`_ to install it:

.. sourcecode:: bash

    $ pip install mosaik-api


Documentation
-------------

Please refer to `mosaik’s documentation`__ of the API.

__ http://mosaik.readthedocs.org/en/latest/mosaik-api/high-level.html


Example Simulator
-----------------

This distribution contains an example simulator in the ``example_sim`` package.

It can be started via the ``pyexamplesim`` command; ``pyexamplesim --help``
shows you how to use it.

It can also be run in-process by importing and calling
``example_sim.mosaik.main()``.


Example MAS
-----------

This distribution contains an example "multi-agent system" that uses the
asyncronous remote calls to mosaik (``get_progress()``,
``get_related_entities()``, ``get_data()``, ``set_data()``).

It can be started via the ``pyexamplemas`` command; ``pyexamplemas --help``
shows you how to use it.

It can also be run in-process by importing and calling
``example_mas.mosaik.main()``.


Development setup
-----------------

To setup a devleopment environment, create a virtualenv and install the
packages from ``requirements.txt``:

.. code-block:: bash

   $ mkvirtualenv --python=/usr/bin/python3 mosaik-api-python
   (mosaik-api-python)$ pip install -r requirements.txt

To run the tests for the Python version you are currently using, execute
``py.test``. You should also add the test coverage check:

.. code-block:: bash

   (mosaik-api-python)$ py.test --cov=example_mas --cov=example_sim --cov=mosaik_api

To run the tests for all supported Python versions, run ``tox``:

.. code-block:: bash

   (mosaik-api-python)$ tox

Mosaik's `documentation
<https://mosaik.readthedocs.org/en/latest/dev/setup.html>`_ contains more
details.
