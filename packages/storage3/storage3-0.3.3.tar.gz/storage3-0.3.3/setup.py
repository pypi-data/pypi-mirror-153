# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage3', 'storage3._async', 'storage3._sync']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19,<0.22', 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'storage3',
    'version': '0.3.3',
    'description': 'Supabase Storage client for Python.',
    'long_description': '# Storage-py\n\nPython Client library to interact with Supabase Storage.\n\n\n\n## How to use\n\nAs it takes some effort to get the headers. We suggest that you use the storage functionality through the main [Supabase Python Client](https://github.com/supabase-community/supabase-py)\n\n\n```python3\nfrom storage3 import create_client\n\nurl = "https://<your_supabase_id>.supabase.co/storage/v1"\nkey = "<your api key>"\nheaders = {"apiKey": key, "Authorization": f"Bearer {key}"}\n\n# pass in is_async=True to create an async client\nstorage_client = create_client(url, headers, is_async=False)\n\nstorage_client.list_buckets()\n```\n',
    'author': 'Joel Lee',
    'author_email': 'joel@joellee.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://supabase-community.github.io/storage-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
