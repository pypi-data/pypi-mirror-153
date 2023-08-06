# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qapi_sdk', 'qapi_sdk.logs']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.23.10,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0',
 'smart-open>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'qapi-sdk',
    'version': '0.3.3',
    'description': 'QAPI SDK provides a library of classes for working with Query API in your Python code.',
    'long_description': '# QAPI SDK\n\nQAPI SDK provides a library of classes for working with Query API in your Python code.\n\n## Requirements\n\n* Python 3.6+\n* Must be logged into the private VPN.\n\n## Installation\n\n```bash\npip install qapi-sdk \n```\n\n## Environment Variables\n\n- `QAPI_URL`: QAPI Base URL.\n- `EMAIL`: Your Email\n\n  *Optional*: If you choose to add your AWS credentials, you can use the `read_columns` method to read in the\n  headers of your CSV file automatically.\n- `AWS_ACCESS_KEY_ID`: AWS Access Key ID\n- `AWS_SECRET_ACCESS_KEY`: AWS Secret Access Key\n- `AWS_DEFAULT_REGION`: AWS Default Region\n\n## Examples\n\n### Query\n\n- `FEED ID`: The table must exist in Athena.\n- `QUERY ID`: The query id is used as an identifier for the query. Query id must be unique. Once you have retrieved your\n  data from S3 it is advised to delete the query.\n- `SQL`: The SQL query to be executed.\n\n```python\nimport time\n\nfrom dotenv import load_dotenv\n\nfrom qapi_sdk import Query\n\nload_dotenv()\n\n# Step 1: Assign your FEED ID, QUERY ID, and SQL QUERY\nfeed_id = "[FEED/TABLE NAME]"\nquery_id = "[QUERY NAME]"\nquery = f"SELECT * FROM {feed_id}"\n\n# Step 2: Create a Query object\nmy_query = Query(\n    feed_id=feed_id,\n    query_id=query_id\n)\n\n# Step 3: Execute the query push\nmy_query.push_query(sql=query)\n\n# Step 4: Wait for the query to complete\nwhile my_query.query_status():\n    print("Waiting for query to complete...")\n    time.sleep(10)\n\n# Step 5 (Optional): Delete the query\nmy_query.delete_query()\n```\n\n### Feed\n\n- `FEED ID`: The table name you want to create in Athena.\n- `PUSH ID`: The push id is used as an identifier for the query. Push id must be unique.\n- `COLUMNS`: The name of the columns that will be pushed to Athena.\n\n```python\nimport time\n\nfrom dotenv import load_dotenv\n\nfrom qapi_sdk import Feed\n\nload_dotenv()\n\n# Step 1: Assign your FEED ID, PUSH ID, and COLUMNS\nfeed_id = "[FEED/TABLE NAME]"\npush_id = "[PUSH ID/PUSH NAME]"\n\n# Step 1A: You can manually assign the columns\ncolumns = [\n    {\n        "name": "email",\n        "type": "string"\n    },\n    {\n        "name": "md5email",\n        "type": "string"\n    },\n    {\n        "name": "firstname",\n        "type": "string"\n    }\n]\n\n# Step 1B (Optional): If you added AWS credentials, you can use the `read_columns` method to read \n# in the headers of your CSV file automatically.\ncolumns = my_feed.read_columns(\n    data_bucket="[DATA BUCKET]",\n    data_key_dir="path/to/your/data/",\n    delimiter=","\n)\n\n# Step 2: Create a Feed object\nmy_feed = Feed(feed_id=feed_id, push_id=push_id)\n\n# Step 3: Define where to grab the data and format of the data.Then push the data to Athena.\nmy_feed.push_feed(\n    pull_path_bucket="[DATA BUCKET]",\n    pull_path_key="path/to/your/data/",\n    columns=columns,\n    separator=","\n)\n\n# Step 4: Wait for the push to complete\nwhile my_feed.push_status():\n    print("Waiting for push to complete...")\n    time.sleep(10)\n\n# Step 5 (Optional): Delete the push\nmy_feed.delete_push()\n\n# Step 6 (Optional): Delete the feed\nmy_feed.delete_feed()\n```\n\n## Redshift\n\n- `FEED ID`: You must use an existing feed.\n- `QUERY ID`: The query id is used as an identifier for the query. Query id must be unique. Once you have retrieved your\n  data from S3 it is advised to delete the query.\n- `SQL`: The SQL query to be executed.\n- If you query an Athena table from Redshift, you must append the Athena schema to the table name.\n    - For example: `SELECT * FROM [query_api].[TABLE NAME]`\n- If you use a `LIMIT` clause, you must wrap the query in a `SELECT * FROM ()` clause.\n    - For example: `SELECT * FROM (SELECT * FROM [TABLE NAME] LIMIT 100)`\n\n```python\nimport time\n\nfrom dotenv import load_dotenv\n\nfrom qapi_sdk import Redshift\n\nload_dotenv()\n\n# Step 1: Assign your FEED ID, QUERY ID, and SQL QUERY\nfeed_id = "[EXISTING FEED ID]"\nquery_id = "[QUERY NAME]"\nquery = "SELECT * FROM (SELECT * FROM [SCHEMA].[TABLE NAME] LIMIT 10)"\n\n# Step 2: Create a Redshift object\nmy_query = Redshift(\n    feed_id=feed_id,\n    query_id=query_id\n)\n\n# Step 3: Execute the query push\nmy_query.push_query(sql=query)\n\n# Step 4: Wait for the query to complete\nwhile my_query.query_status():\n    print("Waiting for query to complete...")\n    time.sleep(10)\n\n# Step 5 (Optional): Delete the query\nmy_query.delete_query()\n\n```\n\n## CHANGELOG\n\n### [0.3.3] - 2020-06-01\n\n- Updated package to include Python 3.6+\n\n### [0.3.2] - 2020-05-30\n\n- Updated `README.md`\n\n### [0.3.0] - 2020-05-30\n\n- Added `Redshift` object to the SDK.\n- Added `delete_query` method to Redshift class.\n- Added `query_status` method to Redshift class.\n- Added `push_query` method to Redshift class.\n- Updated `README.md`\n\n### [0.2.1] - 2020-05-30\n\n- Added `homepage` and `repository` links to the `pyproject.toml` file.\n\n### [0.2.0] - 2020-05-29\n\n- Added `FEED` object to the SDK.\n- Added `read_columns` method to Feed class.\n- Added `delete_push` method to Feed class.\n- Added `delete_feed` method to Feed class.\n- Added `push_status` method to Feed class.\n- Added `push_feed` method to Feed class.\n- Updated `README.md`\n\n### [0.1.4] - 2022-05-29\n\n- Added `QUERY` object to the SDK.\n- Added `delete_query` method to Query class.\n- Added `query_status` method to Query class.\n- Added `push_query` method to Query class.\n- Added the `CHANGELOG` section.\n- Updated `README.md`\n',
    'author': 'TheBridgeDan',
    'author_email': '97176881+TheBridgeDan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oneaudience/data-team-qapi-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
