# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cofactr',
 'cofactr.kb',
 'cofactr.kb.entity',
 'cofactr.schema',
 'cofactr.schema.flagship',
 'cofactr.schema.logistics']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'cofactr',
    'version': '5.0.0',
    'description': 'Client library for accessing Cofactr data.',
    'long_description': '# Cofactr\n\nPython client library for accessing Cofactr.\n\n## Example\n\n```python\nfrom typing import List\nfrom cofactr.graph import GraphAPI\n\n# Flagship is the default schema.\nfrom cofactr.schema.flagship.part import Part\n\ngraph = GraphAPI()\n\npart_res = graph.get_product(id="IM60640MOX6H")\npart: Part = part_res["data"]\n\nparts_res = graph.get_products(query="esp32")\nparts: List[Part] = parts_res["data"]\n```\n',
    'author': 'Noah Trueblood',
    'author_email': 'noah@cofactr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cofactr/cofactr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
