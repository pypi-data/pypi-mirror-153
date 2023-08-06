# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.delta_lake', 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['delta-spark==1.2.1']

setup_kwargs = {
    'name': 'python-prakashravip1',
    'version': '1.0.4',
    'description': 'Common Python Utility and Client Tools',
    'long_description': '# ravi-python-clients\n\nAssortment of python client for personal or business use\n\n## Current Facilities\n\n1) Logger with unique identifier per session\n\n## Windows Installation\n\n```commandline\npy -m venv venv\nsource venv\\Scripts\\activate\npy -m pip install python-prakashravip1\n```\n\n## Linux/ Mac Installation\n\n```bash\npython -m venv venv\nsource venv/bin/activate\npip install python-prakashravip1\n```\n\n## Example\n\n### Delta Lake Write client\n\n1) Create/Delete Delta Lake Database\n```python\nfrom src.delta_lake.delta_lake_spark import create_database, delete_database\n\nDB_NAME = "food_db"\n\ncreate_database(DB_NAME)\ndelete_database(DB_NAME)\n```\n\n2) Create Delta Lake Table\n```python\nfrom src.delta_lake.delta_lake_spark import create_database, create_table_with_schema\n\nDB_NAME = "food_db"\nTABLE_NAME = "indian_food"\n\ncreate_database(DB_NAME)\ncreate_table_with_schema(db=DB_NAME, table=TABLE_NAME,\n     schema=[("food_type", "STRING"), ("name", "STRING"), ("price", "FLOAT")],\n     partition_cols=["food_type"])\n```\n\n### Logging\n\n```python\nfrom utils.logger import logger\n\nlogger.info("test info log")\n```\n\n```python\nfrom utils.trace_logger import get_trace_logger\n\ntest_trace_id = "1234"\nlogger = get_trace_logger(test_trace_id)\nlogger.info(f"test info log with trace_id. {test_trace_id}")        \n```\n',
    'author': 'ravipnsit',
    'author_email': 'prakashravip1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ravip18596/ravi-python-clients',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
