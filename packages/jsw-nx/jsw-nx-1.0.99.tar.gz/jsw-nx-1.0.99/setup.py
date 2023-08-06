# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsw_nx', 'jsw_nx.base', 'jsw_nx.classes', 'jsw_nx.packages', 'jsw_nx.rubify']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'psutil>=5.9.0,<6.0.0', 'ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'jsw-nx',
    'version': '1.0.99',
    'description': 'Next toolkit for python.',
    'long_description': '# jsw-nx\n> Next toolkit for python.\n\n## installation\n```shell\npip install jsw-nx -U\n```\n\n## usage\n```python\nimport jsw_nx as nx\n\n## common methods\nnx.includes([1,2,3], 2) # => True\nnx.includes([1,2,3], 5) # => False\n```\n\n## next core methods\n- base/every\n- base/filter\n- base/find\n- base/find_index\n- base/flatten\n- base/foreach\n- base/forin\n- base/get\n- base/includes\n- base/index\n- base/map\n- base/reduce\n- base/set\n- base/some\n- base/type\n\n## ruby style\n- rubify/times\n- rubify/to_a\n- rubify/to_b\n- rubify/to_f\n- rubify/to_i\n- rubify/to_n\n- rubify/to_s\n\n## next packages\n- days\n- deep_each\n- filesize\n- is_process_alive\n- md5\n- param\n- parse_cookie\n- qs\n- replace_dict_all\n- sample\n- [tmpl](https://js.work/posts/34ef06b7870ec)\n- uniq\n- urljoin\n\n## next classes\n+ configuration\n  - set\n  - get \n  - sets\n  - gets\n  - save\n  - update\n+ date\n  - format \n  - now \n  - create\n+ fileutils\n  - mkdir_p\n  - cd\n  - pwd\n  - ls\n  - mv\n  - rmdir\n  - touch\n  - cp_r\n  - isfile\n  - isdir\n  - rm\n  - exists\n  - gbk_to_utf8\n+ tar\n  - gz\n  - xz\n+ [JSON](https://js.work/posts/3dc24683e53c4)\n  - parse\n  - stringify',
    'author': 'feizheng',
    'author_email': '1290657123@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://js.work',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
