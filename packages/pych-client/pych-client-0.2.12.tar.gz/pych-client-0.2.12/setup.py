# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pych_client']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.0']

extras_require = \
{'orjson': ['orjson>=3.6.6,<4.0.0']}

entry_points = \
{'console_scripts': ['pych-client = pych_client.cli:main']}

setup_kwargs = {
    'name': 'pych-client',
    'version': '0.2.12',
    'description': 'A ClickHouse client for Python, with a command-line interface.',
    'long_description': '# pych-client\n\n[![Coverage][coverage-badge]][coverage-url]\n[![Tests Status][tests-workflow-badge]][tests-workflow-url]\n[![PyPI][pypi-badge]][pypi-url]\n\npych-client is a [ClickHouse][clickhouse] client for Python built on top of [httpx](https://github.com/encode/httpx/).\nIt targets the HTTP interface and offers the following features:\n\n- Sync (`ClickHouseClient`) and async (`AsyncClickHouseClient`) clients.\n- Streaming requests and responses.\n- Load credentials from environment variables, or from a configuration file.\n\n## Installation\n\n```bash\n# Default Python JSON parser:\npip install pych-client\n# Faster orjson parser:\npip install pych-client[orjson]\n```\n\n## Usage\n\n```python\nfrom pych_client import AsyncClickHouseClient, ClickHouseClient\n\n# See "Credential provider chain" for more information on credential specification.\ncredentials = dict(\n    base_url="http://localhost:8123",\n    database="default",\n    username="default",\n    password=""\n)\n\n# The client can be used directly, or as a context manager.\n# The context manager will ensure that the HTTP client resources\n# are properly cleaned-up on exit.\nwith ClickHouseClient(**credentials) as client:\n    # `.bytes()` and `.text()` return the raw response content from the database.\n    # `.json()` sets the format to `JSONEachRow` and parse the response content.\n    client.bytes("SELECT arrayJoin([1, 2, 3]) AS a")\n    # b\'1\\n2\\n3\\n\'\n    client.text("SELECT arrayJoin([1, 2, 3]) AS a")\n    # \'1\\n2\\n3\\n\'\n    client.json("SELECT arrayJoin([1, 2, 3]) AS a")\n    # [{\'a\': 1}, {\'a\': 2}, {\'a\': 3}]\n\n    # `.iter_bytes()`, `.iter_text()` and `.iter_json()` return the response content\n    # as it is received from the database, without buffering the entire response.\n    # `.iter_text()` iterates on the line of the response.\n    list(client.iter_bytes("SELECT arrayJoin([1, 2, 3]) AS a"))\n    # [b\'1\\n2\\n3\\n\', b\'\']\n    list(client.iter_text("SELECT arrayJoin([1, 2, 3]) AS a"))\n    # [\'1\\n\', \'2\\n\', \'3\\n\']\n    list(client.iter_json("SELECT arrayJoin([1, 2, 3]) AS a"))\n    # [{\'a\': 1}, {\'a\': 2}, {\'a\': 3}]\n\n    # In addition to the query, the following arguments can be set:\n    # - `params`: a mapping of query parameters to their values.\n    # - `data`: a bytes, string or an interator of bytes to send in the request body.\n    # - `settings`: ClickHouse settings (e.g. `{"default_format": "JSONEachRow"`).\n    params = {"table": "test_pych"}\n    client.text(\'\'\'\n        CREATE TABLE {table:Identifier} (a Int64, b Int64)\n        ENGINE MergeTree() ORDER BY (a, b)\n    \'\'\', params)\n    client.text("INSERT INTO {table:Identifier} VALUES", params, "(1, 2)")\n    client.text("INSERT INTO {table:Identifier} VALUES", params, [b"(3, 4)", b"(5, 6)"])\n    client.json("SELECT * FROM {table:Identifier} ORDER BY a", params)\n    # [{\'a\': \'1\', \'b\': \'2\'}, {\'a\': \'3\', \'b\': \'4\'}, {\'a\': \'5\', \'b\': \'6\'}]\n\n# `AsyncClickHouseClient` offers the same methods:\nasync with AsyncClickHouseClient(**credentials) as client:\n    # Example usage for `.json()` and `.iter_json()`:\n    await client.json("SELECT arrayJoin([1, 2, 3]) AS a")\n    # [{\'a\': 1}, {\'a\': 2}, {\'a\': 3}]\n    async for row in client.iter_json("SELECT arrayJoin([1, 2, 3]) AS a"):\n        ...\n```\n\n### Command-line interface\n\n```bash\npych-client --help\n```\n\n### Credential provider chain\n\nThe client looks for credentials in a way similar to the [AWS SDK][aws-sdk]:\n\n1. If one of `base_url`, `database`, `username` or `password` is specified, these values will be used.\n2. If none of the previous values are specified, and one of `PYCH_BASE_URL`, `PYCH_DATABASE`, `PYCH_USERNAME`\n   or `PYCH_PASSWORD` environment variables are present, these values will be used.\n3. If none of the previous values are specified, and the file `~/.config/pych-client/credentials.json` exists, the\n   fields `base_url`, `database` and `username` and `password` will be used.\n4. If none of the previous values are specified, the values `http://localhost:8213`, `default` and `default`\n   will be used.\n\n[aws-sdk]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html\n\n[clickhouse]: https://clickhouse.com\n\n[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/pych-client?logo=codecov&logoColor=white\n\n[coverage-url]: https://codecov.io/gh/dioptra-io/pych-client\n\n[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/Tests?logo=github&label=tests\n\n[tests-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/tests.yml\n\n[pypi-badge]: https://img.shields.io/pypi/v/pych-client?logo=pypi&logoColor=white\n\n[pypi-url]: https://pypi.org/project/pych-client/\n',
    'author': 'Maxime Mouchet',
    'author_email': 'maxime.mouchet@lip6.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dioptra-io/pych-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
