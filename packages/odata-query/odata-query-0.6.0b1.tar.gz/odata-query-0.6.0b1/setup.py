# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odata_query',
 'odata_query.django',
 'odata_query.sql',
 'odata_query.sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'sly>=0.4,<0.5']

extras_require = \
{'dev': ['bump2version>=1.0,<2.0'],
 'django': ['django>=2.2'],
 'docs': ['sphinx>=4.5,<5.0', 'sphinx-rtd-theme>=1.0,<2.0'],
 'linting': ['black>=22.1,<23.0',
             'flake8>=3.8,<4.0',
             'isort>=5.7,<6.0',
             'mypy>=0.931,<0.932',
             'types-python-dateutil>=2.8.1,<3.0.0',
             'vulture>=2.3,<3.0'],
 'sqlalchemy': ['sqlalchemy>=1.4,<2.0'],
 'testing': ['pytest>=6.2,<8.0', 'pytest-cov']}

setup_kwargs = {
    'name': 'odata-query',
    'version': '0.6.0b1',
    'description': 'An OData query parser and transpiler.',
    'long_description': 'OData-Query\n===========\n\n.. image:: https://sonarcloud.io/api/project_badges/measure?project=gorillaco_odata-query&metric=alert_status&token=cb35257e036d950788a0f628af7062929318482b\n    :alt: Quality Gate Status\n    :target: https://sonarcloud.io/dashboard?id=gorillaco_odata-query\n\n.. image:: https://sonarcloud.io/api/project_badges/measure?project=gorillaco_odata-query&metric=coverage&token=cb35257e036d950788a0f628af7062929318482b\n    :alt: Coverage\n    :target: https://sonarcloud.io/dashboard?id=gorillaco_odata-query\n\n.. image:: https://readthedocs.org/projects/odata-query/badge/?version=latest\n    :alt: Documentation Status\n    :target: https://odata-query.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code style: black\n    :target: https://github.com/psf/black\n\n\n``odata-query`` is a library that parses `OData v4`_ filter strings, and can\nconvert them to other forms such as `Django Queries`_, `SQLAlchemy Queries`_,\nor just plain SQL.\n\n\nInstallation\n------------\n\n``odata-query`` is available on pypi, so can be installed with the package manager\nof your choice:\n\n.. code-block:: bash\n\n    pip install odata-query\n    # OR\n    poetry add odata-query\n    # OR\n    pipenv install odata-query\n\n\nThe package defines the following optional ``extra``\'s:\n\n* ``django``: If you want to pin a compatible Django version.\n* ``sqlalchemy``: If you want to pin a compatible SQLAlchemy version.\n\n\nThe following ``extra``\'s relate to the development of this library:\n\n- ``linting``: The linting and code style tools.\n- ``testing``: Packages for running the tests.\n- ``docs``: For building the project documentation.\n\n\nYou can install ``extra``\'s by adding them between square brackets during\ninstallation:\n\n.. code-block:: bash\n\n    pip install odata-query[sqlalchemy]\n\n\nQuickstart\n----------\n\nThe most common use case is probably parsing an OData query string, and applying\nit to a query your ORM understands. For this purpose there is an all-in-one function:\n``apply_odata_query``.\n\nExample for Django:\n\n.. code-block:: python\n\n    from odata_query.django import apply_odata_query\n\n    orm_query = MyModel.objects  # This can be a Manager or a QuerySet.\n    odata_query = "name eq \'test\'"  # This will usually come from a query string parameter.\n\n    query = apply_odata_query(orm_query, odata_query)\n    results = query.all()\n\n\nExample for SQLAlchemy:\n\n.. code-block:: python\n\n    from odata_query.sqlalchemy import apply_odata_query\n\n    orm_query = select(MyModel)  # This is any form of Query or Selectable.\n    odata_query = "name eq \'test\'"  # This will usually come from a query string parameter.\n\n    query = apply_odata_query(orm_query, odata_query)\n    results = session.execute(query).scalars().all()\n\n.. splitinclude-1\n\nAdvanced Usage\n--------------\n\nNot all use cases are as simple as that. Luckily, ``odata-query`` is modular\nand extendable. See the `documentation`_ for advanced usage or extending the\nlibrary for other cases.\n\n.. splitinclude-2\n\nContact\n-------\n\nGot any questions or ideas? We\'d love to hear from you. Check out our\n`contributing guidelines`_ for ways to offer feedback and\ncontribute.\n\n\nLicense\n-------\n\nCopyright © `Gorillini NV`_.\nAll rights reserved.\n\nLicensed under the MIT License.\n\n\n.. _odata v4: https://www.odata.org/\n.. _django queries: https://docs.djangoproject.com/en/3.2/topics/db/queries/\n.. _sqlalchemy queries: https://docs.sqlalchemy.org/en/14/orm/loading_objects.html\n.. _documentation: https://odata-query.readthedocs.io/en/latest\n.. _Gorillini NV: https://gorilla.co/\n.. _contributing guidelines: ./CONTRIBUTING.rst\n',
    'author': 'Oliver Hofkens',
    'author_email': 'oliver@gorilla.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
