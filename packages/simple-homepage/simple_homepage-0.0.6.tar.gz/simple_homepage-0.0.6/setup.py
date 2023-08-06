# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_homepage']

package_data = \
{'': ['*'],
 'simple_homepage': ['files/*',
                     'files/template/*',
                     'files/template/static/*',
                     'files/template/static/images/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'PyYAML>=6.0,<7.0', 'oyaml>=1.0,<2.0']

entry_points = \
{'console_scripts': ['homepage = simple_homepage.cli:cli']}

setup_kwargs = {
    'name': 'simple-homepage',
    'version': '0.0.6',
    'description': 'Command line utility that helps you create a simple static homepage for your browser',
    'long_description': '# simple-homepage\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/simple-homepage)](https://img.shields.io/github/v/release/fpgmaas/simple-homepage)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/simple-homepage/merge-to-main)](https://img.shields.io/github/workflow/status/fpgmaas/simple-homepage/merge-to-main)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://fpgmaas.github.io/simple-homepage/)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![License](https://img.shields.io/github/license/fpgmaas/simple-homepage)](https://img.shields.io/github/license/fpgmaas/simple-homepage)\n\n`simple-homepage` is a command line utility that helps you create a simple static homepage for your browser. The documentation can be found [here](https://fpgmaas.github.io/simple-homepage/).\n\n### Light ([Link to demo](https://fpgmaas.github.io/simple-homepage/demo/light/homepage.html))\n\n\n<img src="static/screenshot-light.png" alt="Example light homepage" width="500"/>\n\n### Dark ([Link to demo](https://fpgmaas.github.io/simple-homepage/demo/dark/homepage.html))\n\n<img src="static/screenshot-dark.png" alt="Example dark homepage" width="500"/>\n\n## Quick start\n\nTo get started, first install the package:\n\n```\npip install simple-homepage\n```\n\nThen, navigate to a directory in which you want to create your homepage, and run\n\n```\nhomepage init\n```\n\nor, for the dark version of the homepage:\n\n```\nhomepage init --dark\n```\n\nThen, modify `settings.yaml` to your liking, and run\n\n```\nhomepage build\n```\n\nYour custom homepage is now available under `public/homepage.html`.\n\n## Acknowledgements\n\nInspiration for this project comes from [this](https://www.reddit.com/r/startpages/comments/hca1dj/simple_light_startpage/) post on Reddit by [/u/akauro](https://www.reddit.com/user/akauro/).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Florian Maas',
    'author_email': 'fpgmaas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fpgmaas/simple-homepage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
