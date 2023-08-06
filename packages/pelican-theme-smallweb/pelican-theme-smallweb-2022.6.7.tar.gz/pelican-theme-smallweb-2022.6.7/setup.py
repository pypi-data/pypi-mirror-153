# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.themes.smallweb']

package_data = \
{'': ['*'],
 'pelican': ['themes/smallweb/static/css/*',
             'themes/smallweb/templates/*',
             'themes/smallweb/templates/partial/*']}

install_requires = \
['pelican', 'setuptools']

setup_kwargs = {
    'name': 'pelican-theme-smallweb',
    'version': '2022.6.7',
    'description': 'SmallWeb theme for Pelican static site generator',
    'long_description': "# SmallWeb theme for Pelican static site generator\n\nThis is a simple yet modern-looking theme for Pelican blogs. It uses no\nJavaScript, and all HTML/CSS had been crafted by hand - remember [webmasters]?\n\nTheme name is inspired by the idea of [small web] - a simpler old-style web of\npersonal pages that didn't actually disappear but has become a lot less\nvisible as Internet had grown older and larger.\nAuthors would like to thank [Marginalia Search] for keeping the spirit alive!\n\n[webmasters]: https://justinjackson.ca/webmaster/\n[small web]: https://felix.plesoianu.ro/web/in-the-small.html\n[Marginalia Search]: https://search.marginalia.nu/\n\n\n## Installation and usage\n\nThis theme is installable via pip:\n\n```\n$ pip install git+https://github.com/sio/pelican-smallweb/\n```\n\nImport it in your `pelicanconf.py`:\n\n```python\nfrom pelican.themes import smallweb\nTHEME = smallweb.path()\n```\n\n\n## Privacy concerns\n\nThis theme uses *Google Fonts* by default. If you do not want third-parties to\ntrack your visitors, set `ALLOW_GOOGLE_FONTS = False` in your pelicanconf.py\nand (optionally) provide self-hosted version of fonts via `CSS_OVERRIDE` list.\n\nNo other third-party resources are referenced.\n\nNo personally identifiable information is collected.\n",
    'author': 'Vitaly Potyarkin',
    'author_email': 'sio.wtf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
