Dropland
========

Set of frameworks and utilities for building a backend with SQLAlchemy, Redis caching and scheduler support


How to build
------------

- Create a Python virtual environment.

    ``pyenv local 3.9.0``

    ``pip install --upgrade pip``

    ``pip install setuptools``


- Install the project

    ``pip install -e .[extras] --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple``


Extras may be in: `postgresql`, `mysql`, `sqlite`, `redis`, `sqla` | `gino`, `fastapi`, `scheduler`, `test`


- Start the docker environment for development

    ``docker-compose up -d``


- Run tests

    ``python -m pytest``


- Stop the docker environment

    ``docker-compose down``


- Uninstall the project

    ``pip uninstall dropland -y``
