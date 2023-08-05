# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flagsmith', 'flagsmith.utils']

package_data = \
{'': ['*']}

install_requires = \
['flagsmith-flag-engine>=1.5.1,<2.0.0',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'flagsmith',
    'version': '3.0.0a2',
    'description': 'Flagsmith Python SDK',
    'long_description': '<img width="100%" src="https://github.com/Flagsmith/flagsmith/raw/main/static-files/hero.png"/>\n\n# Flagsmith Python SDK\n\n> Flagsmith allows you to manage feature flags and remote config across multiple projects, environments and organisations.\n\nThe SDK for Python applications for [https://www.flagsmith.com/](https://www.flagsmith.com/).\n\n## Adding to your project\n\nFor full documentation visit [https://docs.flagsmith.com/clients/python/](https://docs.flagsmith.com/clients/python/)\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](https://gist.github.com/kyle-ssg/c36a03aebe492e45cbd3eefb21cb0486) for details on our code of conduct, and the process for submitting pull requests\n\n## Getting Help\n\nIf you encounter a bug or feature request we would like to hear about it. Before you submit an issue please search existing issues in order to prevent duplicates.\n\n## Get in touch\n\nIf you have any questions about our projects you can email <a href="mailto:support@flagsmith.com">support@flagsmith.com</a>.\n\n## Useful links\n\n[Website](https://www.flagsmith.com/)\n\n[Documentation](https://docs.flagsmith.com/)\n',
    'author': 'Flagsmith',
    'author_email': 'support@flagsmith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
