# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resql', 'resql.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'resql',
    'version': '0.1.0',
    'description': 'A beginner friendly database',
    'long_description': '# <p align="center"> resql: Built for Beginners </p>\n\n## Quick Examples\n<br>\n\nimports\n\n```\npip install resql\n```\n\n\n\n```python\nimport resql\n\ndatabase = resql.PyDatabase("mydb.db")\n# default is in :memory:\n```\n\n<br>\n\n## .create_table(name)\n\ncreates a database table.\n\n```python\ndatabase.create_table("newtable")\n# {\'status\': \'success\', \'table\': \'newtable\'}\n```\n\n<br>\n\n\n## .insert(key, value, [table])\n\ninsert into given table.\n\n```python\ndatabase.insert("key","value")\n# {\'status\': \'success\'}\n```\n\n<br>\n\n\n## .all([table])\n\nfind data from given table.\n\n```py\ndatabase.all()\n# [(\'key\',\'value\')]\n```\n\n<br>\n\n## .find(key, [table]) or .get(key, [table])\n\nfind data from given table.\n\n```py\ndatabase.find("key")\n# value\n```\n\n<br>\n\n## .wipe([table])\n\nwipe complete table.\n\n\n```py\ndatabase.wipe()\n# {\'status\': \'success\'}\n```\n\n<br>\n\n## .run(sql)\n\ndirectly run sql query.\n\n```py\ndatabase.run("SELECT * FROM table")\n# cursor\n```\n\n<br>\n\n## .delete(key, [table])\n\ndelete key from table.\n\n```py\ndatabase.delete("key")\n# value\n```\n\n\n\n\n',
    'author': 'ResetXD',
    'author_email': 'resetwastakenwastaken@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
