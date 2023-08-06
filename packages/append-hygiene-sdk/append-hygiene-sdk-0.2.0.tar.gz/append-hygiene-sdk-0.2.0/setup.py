# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['append_hygiene_sdk', 'append_hygiene_sdk.logs']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.20.0,<0.21.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'append-hygiene-sdk',
    'version': '0.2.0',
    'description': 'Append Hygiene SDK provides a library of classes for working with On-Demand API in your Python code.',
    'long_description': '# Append Hygiene SDK\n\nAppend Hygiene SDK provides a library of classes for working with On-Demand API in your Python code.\n\n## Requirements\n\n* Python 3.6+\n* Must be logged into the private VPN.\n\n## Installation\n\n```bash\npip install append-hygiene-sdk \n```\n\n## Environment Variables\n\n- `ONDEMAND_URL`: On-Demand Base URL.\n\n## Examples\n\n### Hygiene\n\n```python\nimport time\n\nfrom dotenv import load_dotenv\n\nfrom append_hygiene_sdk import Hygiene\n\nload_dotenv()\n\n# Step 1: Create the Hygiene object\nmy_hygiene = Hygiene()\n\n# Step 2: Add your custom payload to the Hygiene object and execute the hygiene push\nmy_hygiene.push_hygiene(\n    payload={\n        "filepath": "s3://bucket-name/folder1/folder2/file1.csv",\n        "result_path": "s3://bucket-name/folder1/folder2/",\n        "verification": False,\n        "has_header": True,\n        "email_column_number": 1,\n        "omit_suppressions": False,\n        "ignore_duplicates": False,\n        "suppression_types": [\n            "trap",\n            "high_complainer",\n            "low_complainer"\n        ],\n        "on_success_uri": "mailto:[EMAIL]?subject=[SUCCESS SUBJECT LINE]",\n        "on_error_uri": "mailto:[EMAIL]?subject=[FAILED SUBJECT LINE]",\n        "callback_context": "{\\"clientID\\": \\"123\\"}"\n    }\n)\n\n# Step 3: Wait for the hygiene to complete\nwhile my_hygiene.hygiene_status(my_hygiene.hygiene_id):\n    time.sleep(10)\n    print("Waiting for Hygiene to complete...")\n```\n\n### Append\n\n```python\nimport time\n\nfrom dotenv import load_dotenv\n\nfrom append_hygiene_sdk import Append\n\nload_dotenv()\n\n# Step 1: Create the Append object\nmy_append = Append()\n\n# Step 2: Add your custom payload to the Append object and execute the Append push\nmy_append.push_append(\n    payload={\n        "filepath": "s3://bucket-name/folder1/folder2/file1.csv",\n        "has_header": True,\n        "identifier_columns": {\n            "first_name": 1,\n            "last_name": 2,\n            "address": 4,\n            "zip5": 8\n        },\n        "individual_match": True,\n        "household_match": False,\n        "append_fields": [\n            "email"\n        ],\n        "hygiene_and_verification": False,\n        "verification": False,\n        "results_per_row": 1,\n        "prioritize_individual_email": True,\n        "additional_append_fields": {},\n        "hide_results": False,\n        "unique_emails": True,\n        "suppression_types": [\n            "bad_domain",\n            "bad_extension",\n            "bad_word",\n            "catch_all",\n            "unsub",\n            "trap",\n            "high_complainer",\n            "low_complainer",\n            "bad_format",\n            "invalid",\n            "unknown",\n            "unpreferred_domain"\n        ],\n        "apply_address_correction": False,\n        "ac_with_history": False,\n        "append_ac_columns": False,\n        "raw_email": False,\n        "result_path": "s3://bucket-name/folder1/folder2/",\n        "on_success_uri": "mailto:[EMAIL]?subject=[SUCCESS SUBJECT LINE]",\n        "on_error_uri": "mailto:[EMAIL]?subject=[FAILED SUBJECT LINE]",\n        "callback_context": "{\\"clientID\\": \\"123\\"}"\n    }\n)\n\n# Step 3: Wait for the Append to complete\nwhile my_append.append_status(my_append.append_id):\n    time.sleep(10)\n    print("Waiting for Hygiene to complete...")\n\n```\n\n## CHANGELOG\n\n### [0.2.0] - 2020-06-01\n\n- Added `Append` object to the SDK.\n- Added `push_append` method to the Append class.\n- Added `append_status` method to the Append class.\n- Updated `README.md` to include the Append SDK.\n\n### [0.1.1] - 2020-06-01\n\n- Updated pypi description\n\n### [0.1.0] - 2020-05-31\n\n- Added `Hygiene` object to the SDK.\n- Added `push_hygiene` method to Hygiene class.\n- Added `hygiene_status` method to Hygiene class.\n- Updated `README.md`',
    'author': 'TheBridgeDan',
    'author_email': '97176881+TheBridgeDan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oneaudience/data-team-append-hygiene-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
