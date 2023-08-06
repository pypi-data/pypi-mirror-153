# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ecs_tasks_ops', 'ecs_tasks_ops_qt5']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.1,<6.0.0',
 'boto3>=1.15.13,<2.0.0',
 'click>=7,<9',
 'moto[ec2,ecs]>=3.0.3,<4.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['ecs-tasks-ops = ecs_tasks_ops.__main__:main',
                     'ecs-tasks-ops-qt5 = ecs_tasks_ops_qt5.__main__:main']}

setup_kwargs = {
    'name': 'ecs-tasks-ops',
    'version': '0.5.0',
    'description': 'Ecs Tasks Ops',
    'long_description': 'ECS Tasks Ops\n=============\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/ecs-tasks-ops.svg\n   :target: https://pypi.org/project/ecs-tasks-ops/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/ecs-tasks-ops\n   :target: https://pypi.org/project/ecs-tasks-ops\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/ecs-tasks-ops\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/ecs-tasks-ops/latest.svg?label=Read%20the%20Docs\n   :target: https://ecs-tasks-ops.readthedocs.io/\n   :alt: Read the documentation at https://ecs-tasks-ops.readthedocs.io/\n.. |Tests| image:: https://github.com/ppalazon/ecs-tasks-ops/workflows/Tests/badge.svg\n   :target: https://github.com/ppalazon/ecs-tasks-ops/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/ppalazon/ecs-tasks-ops/branch/main/graph/badge.svg?token=zaz1KPR73Q\n   :target: https://codecov.io/gh/ppalazon/ecs-tasks-ops\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Application GUI to manage ECS resources\n* Use your home aws credentials from ~/.aws/credentials\n* Get information and attributes for each task, service or instance container\n* Connect through SSH to container instances or docker container\n* Show logs for each docker container\n* Show ECS events for a service\n* Force restart for a service\n\nRequirements\n------------\n\n* Python 3.10\n* `boto3 <https://pypi.org/project/boto3/>`_\n* `click <https://pypi.org/project/click/>`_\n* `tabulate <https://pypi.org/project/tabulate/>`_\n* `PyQt5 <https://pypi.org/project/PyQt5/>`_\n* `moto <https://pypi.org/project/moto/>`_\n* uxrvt\n\n\nInstallation\n------------\n\nYou can install *Ecs Tasks Ops* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install ecs-tasks-ops\n\n\nConfiguration\n-------------\n\nAWS Access\n^^^^^^^^^^\n\nThis application uses your aws credentials to connect to your ECS, so you need to configure your credentials.\n\nSet up credentials (in e.g. ``~/.aws/credentials``)\n\n.. code:: ini\n\n   [default]\n   aws_access_key_id = YOUR_KEY\n   aws_secret_access_key = YOUR_SECRET\n\nThen, you set up a default region (in e.g. ``~/.aws/config``)\n\n.. code:: ini\n\n   [default]\n   region=us-east-1\n\nYou can read more about it in `boto3 <https://pypi.org/project/boto3/>`_\n\n``ssh`` over ``ssm``\n^^^^^^^^^^^^^^^^^^^^\n\nIf you want to access to containers instances or docker container through ``ssh``, you must configurate ``ssm`` in your EC2 machines.\nThat\'s because ``ecs-tasks-ops`` use its instance id as machine identifier on ``ssh`` command. For example, ``ssh i-0123456789ABCDE``.\nI use `ssh-over-ssm <https://github.com/elpy1/ssh-over-ssm>`_ tool to configure ``ssh`` over ``ssm`` to connect to instances.\n\nPredefined Commands\n^^^^^^^^^^^^^^^^^^^\n\nYou can set multiples predefined commands to execute on docker containers. You can set them in a configuration file called ``ecs-tasks-ops.json``.\nThis file can be located on ``~``, ``~/.config/ecs-tasks-ops``, ``/etc/ecs-tasks-ops``, or any directory configured in the enviromental variable\n``ECS_TASKS_OPS_CONF``\n\nSample configuration\n\n.. code-block:: json\n\n   {\n      "commands": [\n         "/bin/sh",\n         "/bin/bash",\n         "mongo admin -u root -p $(pass mongo/root)"\n      ]\n   }\n\nGUI Usage\n---------\n\nYou can open the ``qt5`` application, using the following command\n\n.. code:: console\n\n   ecs-tasks-ops-qt5\n\nCLI Usage\n---------\n\nYou can open the command line with ``ecs-tasks-ops`` command. This is the help menu:\n\n.. code::\n\n   Usage: ecs-tasks-ops [OPTIONS] COMMAND [ARGS]...\n\n      Ecs Tasks Ops.\n\n   Options:\n      -x, --debug / --no-debug\n      -j, --output-json\n      --version                 Show the version and exit.\n      --help                    Show this message and exit.\n\n   Commands:\n      clusters             Clusters information.\n      container-instances  Container instances defined in a cluster.\n      containers           Get docker containers defined in a cluster.\n      services             Services defined in a cluster.\n      tasks                Set tasks defined in a cluster.\n\nBy default, the output format is in a table, but you can get original ``json`` format with ``-j`` option.\nYou can filter json output with `jq <https://stedolan.github.io/jq/>`_ tool:\n\n.. code:: console\n\n   $ ecs-tasks-ops -j clusters | jq "."\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Ecs Tasks Ops* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/ppalazon/ecs-tasks-ops/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n',
    'author': 'Pablo Palazon',
    'author_email': 'ppalazon@antara.ws',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ppalazon/ecs-tasks-ops',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
