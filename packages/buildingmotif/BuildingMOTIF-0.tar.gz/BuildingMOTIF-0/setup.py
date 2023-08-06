# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buildingmotif', 'buildingmotif.dataclasses', 'buildingmotif.db_connections']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0',
 'nbmake>=1.3.0,<2.0.0',
 'networkx>=2.7.1,<3.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'rdflib>=6.1.1,<7.0.0',
 'types-PyYAML>=6.0.4,<7.0.0']

setup_kwargs = {
    'name': 'buildingmotif',
    'version': '0',
    'description': 'Building Metadata OnTology Interoperability Framework',
    'long_description': '# BuildingMOTIF [![Documentation Status](https://readthedocs.org/projects/buildingmotif/badge/?version=latest)](https://buildingmotif.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/NREL/BuildingMOTIF/branch/main/graph/badge.svg?token=HAFSYH45NX)](https://codecov.io/gh/NREL/BuildingMOTIF) \n\nThe Building Metadata OnTology Interoperability Framework (BuildingMOTIF)...\n\n# Installing\n\nRequirements:\n- Python >= 3.8.0\n- [Poetry](https://python-poetry.org/docs/)\n\nSimply clone and run `poetry install`. Then run `poetry run pre-commit install` to set up pre-commit.\n\n# Developing\nTo test, run \n``` \npoetry run pytest\n```\n\nTo format and lint, run\n```\npoetry run black .\npoetry run isort .\npoetry run pylama\n```\n\nDocumentation can be built locally with the following command, which will make the HTML files in the `docs/build/html` directory.\n\n```\ncd docs\npoetry run make html\n```\n\n# Visualizing\n\n![repo-vis](./diagram.svg)\n',
    'author': 'Hannah Eslinger',
    'author_email': 'hannah.eslinger@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NREL/BuildingMOTIF',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
