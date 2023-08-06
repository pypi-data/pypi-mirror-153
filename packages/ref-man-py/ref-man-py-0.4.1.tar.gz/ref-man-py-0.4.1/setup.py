# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ref_man_py']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'common_pyutil>=0.8.0,<0.9.0',
 'flask>=1.1.2,<2.0.0',
 'lxml>=4.6.4,<5.0.0',
 'psutil>=5.8.0,<6.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['ref_man = ref_man_py.__main__:main',
                     'test = pytest:main']}

setup_kwargs = {
    'name': 'ref-man-py',
    'version': '0.4.1',
    'description': 'Ref Man Python Module',
    'long_description': "* ref-man-py\n\n  Python Module for ~ref-man~ (See https://github.com/akshaybadola/ref-man).\n\n  Network requests and xml parsing can be annoying in emacs, so ref-man uses a\n  separate python process for efficient (and sometimes parallel) fetching of\n  network requests.\n\n* Features\n\n** Persistent Service with Flask\n   - Can easily integrate with other applications\n\n** HTTP integration with Semantic Scholar API (https://www.semanticscholar.org/product/api)\n   - Fetch with multiple IDs like arxiv, ACL etc.\n   - Local files based cache to avoid redundant requests\n   - Fetches all metadata in one go (Will change soon as Semantic Scholar is\n     updating its API)\n\n** Experimental (and undocumented) Semantic Scholar Search API\n   - Mostly gleaned through analyzing network requests. Helpful for searching\n     articles.\n\n** HTTP integration with DBLP and ArXiv\n   - Supports multiple parallel requests for batch updates\n\n** Fetch PDF from a given URL\n   - Easier to fetch using python than with Emacs's callbacks\n\n** Option for proxying requests\n   - Particularly useful for PDFs if you're tunneling to your institution from\n     home or some other location and the article you want is with institutional\n     (IP based) access only.\n\n* Roadmap\n\n\n** More Tests\n   Always\n\n** Change to new Semantic Scholar API\n   Semantic Scholar is changing its API. See https://www.semanticscholar.org/product/api\n   we should migrate to new ~graph/v1/paper~ API.\n\n** Integrate ~common_pyutil.net.Get~\n   It has support for progress tracking. Helpful when network is slow and when\n   downloading large files.\n\n** ASGI server\n   With websockets for better Async integration.\n\n** Integrate more services\n   There're semi-working/broken functions for CrossRef and some other services in\n   ~ref-man~. They can be exported to python perhaps.\n\n* Wishlist\n\n** Serve Org files on the fly as html\n   Will help in integrating a larger userbase. Perhaps also with a py-to-lisp\n   (hy like maybe) interface so that elementary scripting on the org backend can\n   be done.\n\n** Ultimately integrate ~pndconf~ also\n   A document preparation toolchain (See https://github.com/akshaybadola/pndconf),\n   which is integrated with ~ref-man~.\n",
    'author': 'Akshay',
    'author_email': 'akshay.badola.cs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/akshaybadola/ref-man-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
