ECS Tasks Ops
=============

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/ecs-tasks-ops.svg
   :target: https://pypi.org/project/ecs-tasks-ops/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/ecs-tasks-ops
   :target: https://pypi.org/project/ecs-tasks-ops
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/ecs-tasks-ops
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/ecs-tasks-ops/latest.svg?label=Read%20the%20Docs
   :target: https://ecs-tasks-ops.readthedocs.io/
   :alt: Read the documentation at https://ecs-tasks-ops.readthedocs.io/
.. |Tests| image:: https://github.com/ppalazon/ecs-tasks-ops/workflows/Tests/badge.svg
   :target: https://github.com/ppalazon/ecs-tasks-ops/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/ppalazon/ecs-tasks-ops/branch/main/graph/badge.svg?token=zaz1KPR73Q
   :target: https://codecov.io/gh/ppalazon/ecs-tasks-ops
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* Application GUI to manage ECS resources
* Use your home aws credentials from ~/.aws/credentials
* Get information and attributes for each task, service or instance container
* Connect through SSH to container instances or docker container
* Show logs for each docker container
* Show ECS events for a service
* Force restart for a service

Requirements
------------

* Python 3.10
* `boto3 <https://pypi.org/project/boto3/>`_
* `click <https://pypi.org/project/click/>`_
* `tabulate <https://pypi.org/project/tabulate/>`_
* `PyQt5 <https://pypi.org/project/PyQt5/>`_
* `moto <https://pypi.org/project/moto/>`_
* uxrvt


Installation
------------

You can install *Ecs Tasks Ops* via pip_ from PyPI_:

.. code:: console

   $ pip install ecs-tasks-ops


Configuration
-------------

AWS Access
^^^^^^^^^^

This application uses your aws credentials to connect to your ECS, so you need to configure your credentials.

Set up credentials (in e.g. ``~/.aws/credentials``)

.. code:: ini

   [default]
   aws_access_key_id = YOUR_KEY
   aws_secret_access_key = YOUR_SECRET

Then, you set up a default region (in e.g. ``~/.aws/config``)

.. code:: ini

   [default]
   region=us-east-1

You can read more about it in `boto3 <https://pypi.org/project/boto3/>`_

``ssh`` over ``ssm``
^^^^^^^^^^^^^^^^^^^^

If you want to access to containers instances or docker container through ``ssh``, you must configurate ``ssm`` in your EC2 machines.
That's because ``ecs-tasks-ops`` use its instance id as machine identifier on ``ssh`` command. For example, ``ssh i-0123456789ABCDE``.
I use `ssh-over-ssm <https://github.com/elpy1/ssh-over-ssm>`_ tool to configure ``ssh`` over ``ssm`` to connect to instances.

Predefined Commands
^^^^^^^^^^^^^^^^^^^

You can set multiples predefined commands to execute on docker containers. You can set them in a configuration file called ``ecs-tasks-ops.json``.
This file can be located on ``~``, ``~/.config/ecs-tasks-ops``, ``/etc/ecs-tasks-ops``, or any directory configured in the enviromental variable
``ECS_TASKS_OPS_CONF``

Sample configuration

.. code-block:: json

   {
      "commands": [
         "/bin/sh",
         "/bin/bash",
         "mongo admin -u root -p $(pass mongo/root)"
      ]
   }

GUI Usage
---------

You can open the ``qt5`` application, using the following command

.. code:: console

   ecs-tasks-ops-qt5

CLI Usage
---------

You can open the command line with ``ecs-tasks-ops`` command. This is the help menu:

.. code::

   Usage: ecs-tasks-ops [OPTIONS] COMMAND [ARGS]...

      Ecs Tasks Ops.

   Options:
      -x, --debug / --no-debug
      -j, --output-json
      --version                 Show the version and exit.
      --help                    Show this message and exit.

   Commands:
      clusters             Clusters information.
      container-instances  Container instances defined in a cluster.
      containers           Get docker containers defined in a cluster.
      services             Services defined in a cluster.
      tasks                Set tasks defined in a cluster.

By default, the output format is in a table, but you can get original ``json`` format with ``-j`` option.
You can filter json output with `jq <https://stedolan.github.io/jq/>`_ tool:

.. code:: console

   $ ecs-tasks-ops -j clusters | jq "."

Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT_ license,
*Ecs Tasks Ops* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.


.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/ppalazon/ecs-tasks-ops/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
