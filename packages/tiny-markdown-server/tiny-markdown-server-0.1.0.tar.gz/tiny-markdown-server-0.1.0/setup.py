# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_markdown_server']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.7,<4.0.0']

entry_points = \
{'console_scripts': ['tiny-markdown-server = '
                     'tiny_markdown_server.tiny_markdown_server:main']}

setup_kwargs = {
    'name': 'tiny-markdown-server',
    'version': '0.1.0',
    'description': 'Python based Tiny Markdown Server, which transforms Markdown files to webpages and shows it in a browser with auto-reload.',
    'long_description': 'Tiny Markdown Server\n====================\n\n Introduction\n--------------\n\nThis is a start of a very simple markdown web-server. The server must be started in the folder where your markdown files are located. You point the URL to the markdown-file, which will be converted on the fly.\n\n\nTODO\n----\n\n- CSS as an argument parameter to customize the html.',
    'author': 'David Tillemans',
    'author_email': 'davidtillemans@cryptable.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cryptable/tiny-markdown-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
