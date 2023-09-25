"""
This script covers the JSON standard module

Written by Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""
print("--- Welcome to Lecture 9's JSON example/follow-along code ---")
print("--- Check the code for some of the printed stuff below to make sense ---\n")

# First, we import the json module
import json

# Let's make a data-set.
# This is copied right from Wikipedia: https://en.wikipedia.org/wiki/JSON
data = {
  "first_name": "John",
  "last_name": "Smith",
  "is_alive": True,
  "age": 27,
  "address": {
    "street_address": "21 2nd Street",
    "city": "New York",
    "state": "NY",
    "postal_code": "10021-3100"
  },
  "phone_numbers": [
    {
      "type": "home",
      "number": "212 555-1234"
    },
    {
      "type": "office",
      "number": "646 555-4567"
    }
  ],
  "children": [
    "Catherine",
    "Thomas",
    "Trevor"
  ],
  "spouse": None,
}

# We can convert the dictionary to a JSON string
json_string = json.dumps(data)
print("JSON Dump: ", json_string, end="\n\n")

# We can also save to a file with dump (not dumps)
# This needs a file-like object
with open('test_json.json', 'w') as f:
    # indent is optional, and only for nicely formatting the JSON file. Try it with None
    json.dump(data, f, indent=4)
print("Check your folder for a JSON file!", end="\n\n")

# We can 'load' the JSON string back into a dictionary
print("'Loaded' Json Type and data: ", type(json.loads(json_string)), json.loads(json_string), end="\n\n")

# We can also load data from a JSON file directly
with open('test_json.json', 'r') as f:
    data = json.load(f)
print("JSON file data: ", data, end="\n\n")

print("\n--- end ---")
# end
