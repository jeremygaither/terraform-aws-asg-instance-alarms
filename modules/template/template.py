#!/usr/bin/env python

import decimal
import hashlib
import json
import sys


# Parse the query.
query = json.load(sys.stdin)

# Build the JSON template.

boolean_keys = [
    'ActionsEnabled',
]
list_keys = [
    'AlarmActions',
    'Dimensions',
    'InsufficientDataActions',
    'OKActions',
]

alarm = {}
for key, value in query.items():

    if key in boolean_keys:
        value = value.lower() in ('1', 'true')
    elif key in list_keys:
        value = json.loads(value)

    if value:
        alarm[key] = value

content = json.dumps(alarm, indent=2, sort_keys=True)
etag = hashlib.md5(content.encode('utf-8')).hexdigest()

# Output the result to Terraform.
json.dump({
    'key': etag,
    'content': content,
    'etag': etag,
}, sys.stdout, indent=2)
sys.stdout.write('\n')
