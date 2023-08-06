# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['combine', 'combine.checks', 'combine.files', 'combine.jinja']

package_data = \
{'': ['*'], 'combine': ['base_content/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pygments>=2.6.1,<3.0.0',
 'barrel>=0.3.0,<0.4.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'click>7.1.2',
 'cls-client>=1.2.0,<2.0.0',
 'honcho>=1.1.0,<2.0.0',
 'jinja2>2.11.2',
 'markdown>=3.2.2,<4.0.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'watchdog>=2.1.6,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

entry_points = \
{'console_scripts': ['combine = combine.cli:cli']}

setup_kwargs = {
    'name': 'combine',
    'version': '2.8.0',
    'description': 'A straightforward static site builder.',
    'long_description': '# Combine\n\n**Build a straightforward marketing or documentation website with the power of [Jinja](http://jinja.pocoo.org/).\nNo fancy JavaScript here &mdash; this is just like the good old days.**\n\nPut your site into the "content" directory and Combine will:\n\n- Render files using Jinja\n- Create pretty URLs ("file-system routing")\n- Inject variables\n- Run custom build steps (like building Tailwind)\n\nMost sites follow a simple pattern.\n\nCreate a `base.template.html`:\n\n```html+jinja\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>My site</title>\n</head>\n<body>\n    {% block content %}{% endblock %}\n</body>\n</html>\n```\n\nAnd use it (ex. `pricing.html`):\n\n```html+jinja\n{% extends "base.template.html" %}\n\n{% block content %}\n<div class="pricing">\n    <div class="flex">\n        ...\n    </div>\n</div>\n{% endblock %}\n```\n\nIn the end, you get a static HTML site that can be deployed almost anywhere.\n',
    'author': 'Dropseed',
    'author_email': 'python@dropseed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://combine.dropseed.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
