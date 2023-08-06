# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hebikani']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'ascii-magic>=1.6,<2.0',
 'colorama>=0.4.4,<0.5.0',
 'playsound>=1.3.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'romkan>=0.2.1,<0.3.0']

extras_require = \
{':sys_platform == "darwin"': ['pyobjc>=8.5,<9.0'],
 ':sys_platform == "linux"': ['PyGObject>=3.42.1,<4.0.0']}

entry_points = \
{'console_scripts': ['hebikani = hebikani.hebikani:main']}

setup_kwargs = {
    'name': 'hebikani',
    'version': '1.2.1',
    'description': 'WaniKani command line interface',
    'long_description': '.. image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/ajite/c90a126b4e926b94c07a36ac78e9a9ad/raw/hebikani_coverage.json\n\t:target: https://github.com/ajite/hebikani\n\t:alt: Coverage\n\n.. image:: https://readthedocs.org/projects/hebikani/badge/?version=latest\n\t:target: https://hebikani.readthedocs.io/en/latest/?badge=latest\n\t:alt: Documentation Status\n\nHebiKani\n============\n\n**This program is not an official WaniKani client. Use at your own risk.**\n\nA command line interface to do your WaniKani lessons and reviews.\n\n.. figure:: docs/source/_static/demo.gif\n   :alt: CLI demo gif\n\nINSTALL\n-------\n\n.. code-block:: bash\n\n    pip install hebikani\n\nIf you are missing libraries check the  `documentation <https://hebikani.readthedocs.io/en/latest/install.html>`_\n\nRUN\n---\n\nCheck the help:\n\n.. code-block:: bash\n\n    hebikani --help\n\nTo display your review summary:\n\n.. code-block:: bash\n\n    hebikani summary\n\nTo start a review session:\n\n.. code-block:: bash\n\n    hebikani reviews\n\nTo start a review session in hard mode with audio and a limited number of reviews:\n\n.. code-block:: bash\n\n    hebikani reviews --hard --autoplay --limit 10\n\nDEVELOPMENT\n-----------\nThis project uses `Poetry <https://python-poetry.org/docs/>`_.\n\n.. code-block:: bash\n\n    poetry install\n\nTEST\n----\n\nRun the test:\n\n.. code-block:: bash\n\n    poetry run pytest\n',
    'author': 'Augustin',
    'author_email': 'ajitekun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajite/hebikani',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
