# Append Hygiene SDK

Append Hygiene SDK provides a library of classes for working with On-Demand API in your Python code.

## Requirements

* Python 3.6+
* Must be logged into the private VPN.

## Installation

```bash
pip install append-hygiene-sdk 
```

## Environment Variables

- `ONDEMAND_URL`: On-Demand Base URL.

## Examples

### Hygiene

```python
import time

from dotenv import load_dotenv

from append_hygiene_sdk import Hygiene

load_dotenv()

# Step 1: Create the Hygiene object
my_hygiene = Hygiene()

# Step 2: Add your custom payload to the Hygiene object and execute the hygiene push
my_hygiene.push_hygiene(
    payload={
        "filepath": "s3://bucket-name/folder1/folder2/file1.csv",
        "result_path": "s3://bucket-name/folder1/folder2/",
        "verification": False,
        "has_header": True,
        "email_column_number": 1,
        "omit_suppressions": False,
        "ignore_duplicates": False,
        "suppression_types": [
            "trap",
            "high_complainer",
            "low_complainer"
        ],
        "on_success_uri": "mailto:[EMAIL]?subject=[SUCCESS SUBJECT LINE]",
        "on_error_uri": "mailto:[EMAIL]?subject=[FAILED SUBJECT LINE]",
        "callback_context": "{\"clientID\": \"123\"}"
    }
)

# Step 3: Wait for the hygiene to complete
while my_hygiene.hygiene_status(my_hygiene.hygiene_id):
    time.sleep(10)
    print("Waiting for Hygiene to complete...")
```

### Append

```python
import time

from dotenv import load_dotenv

from append_hygiene_sdk import Append

load_dotenv()

# Step 1: Create the Append object
my_append = Append()

# Step 2: Add your custom payload to the Append object and execute the Append push
my_append.push_append(
    payload={
        "filepath": "s3://bucket-name/folder1/folder2/file1.csv",
        "has_header": True,
        "identifier_columns": {
            "first_name": 1,
            "last_name": 2,
            "address": 4,
            "zip5": 8
        },
        "individual_match": True,
        "household_match": False,
        "append_fields": [
            "email"
        ],
        "hygiene_and_verification": False,
        "verification": False,
        "results_per_row": 1,
        "prioritize_individual_email": True,
        "additional_append_fields": {},
        "hide_results": False,
        "unique_emails": True,
        "suppression_types": [
            "bad_domain",
            "bad_extension",
            "bad_word",
            "catch_all",
            "unsub",
            "trap",
            "high_complainer",
            "low_complainer",
            "bad_format",
            "invalid",
            "unknown",
            "unpreferred_domain"
        ],
        "apply_address_correction": False,
        "ac_with_history": False,
        "append_ac_columns": False,
        "raw_email": False,
        "result_path": "s3://bucket-name/folder1/folder2/",
        "on_success_uri": "mailto:[EMAIL]?subject=[SUCCESS SUBJECT LINE]",
        "on_error_uri": "mailto:[EMAIL]?subject=[FAILED SUBJECT LINE]",
        "callback_context": "{\"clientID\": \"123\"}"
    }
)

# Step 3: Wait for the Append to complete
while my_append.append_status(my_append.append_id):
    time.sleep(10)
    print("Waiting for Hygiene to complete...")

```

## CHANGELOG

### [0.2.1] - 2020-06-01

- Updated package to include Python 3.6+

### [0.2.0] - 2020-06-01

- Added `Append` object to the SDK.
- Added `push_append` method to the Append class.
- Added `append_status` method to the Append class.
- Updated `README.md` to include the Append SDK.

### [0.1.1] - 2020-06-01

- Updated pypi description

### [0.1.0] - 2020-05-31

- Added `Hygiene` object to the SDK.
- Added `push_hygiene` method to Hygiene class.
- Added `hygiene_status` method to Hygiene class.
- Updated `README.md`