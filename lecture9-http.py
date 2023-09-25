"""
This script covers the urllib standard module and requests module for communicating with http.

Written by Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""
print("--- Welcome to Lecture 9's HTTP example/follow-along code ---")
print("--- Check the code for some of the printed stuff below to make sense ---\n")

# First, we import the urllib.request and requests module
import urllib.request
import requests
# and json, we'll need it later
import json

def urllib_print_response(u, conv_json=False, limit_read = None):
    """ Helper function to print what we get back from a urllib request"""
    print("u.url ->\t", u.url)
    print("u.status ->\t", u.status)
    print("u.reason ->\t", u.reason)
    print("u.getheaders() ->\t", u.getheaders())
    if conv_json:
        # as u is a file-like object, we can have the json module load it like it would
        # a file, returning a dictionarty
        data = json.load(u)
        print("json.load(u) ->\t", data)
    else:
        print("u.read() ->\t", u.read(limit_read))
    print("\n")

def requests_print_response(u, limit_read = None):
    """ Helper function to print what we get back from a requests request"""
    print("u.url ->\t", u.url)
    print("u.status_code ->\t", u.status_code)
    print("u.reason ->\t", u.reason)
    print("u.headers ->\t", u.headers)
    try:
        print("u.json() ->\t", u.json())
    except requests.JSONDecodeError:
        print("u.text ->\t", u.text[:limit_read])
    print("\n")


# For the most part, urlopen is sufficient of a callback to open an URL
# The urlopen open a file-like object, and we can use `with` if we really want to

# So let's open a regular website!
with urllib.request.urlopen("https://semver.org/") as res:
    urllib_print_response(res, limit_read=100)

# Let's open an URL that returns an API for weather
url = "https://api.weather.gov/gridpoints/OKX/65,67/forecast"
res = urllib.request.urlopen(url)
# As the response is in JSON, we can also convert the
# file-like response to a json
urllib_print_response(res, conv_json=True)

# Let's open a GET request but with added added to the URL
url = "https://opentdb.com/api.php"
data = {'amount': 10}
url = url + '?' + urllib.parse.urlencode(data)
res = urllib.request.urlopen(url)
urllib_print_response(res, conv_json=True)

# Let's do a POST request
url = "https://reqres.in/api/users"
data = {'name': 'morpheus', 'job': 'leader'}
header = {'User-Agent' : 'Mozilla/5.0'}         # due to it rejecting otherwise
data = urllib.parse.urlencode(data).encode()    # we encode the url into bytes
url = urllib.request.Request(url, data, header) # we make a request object
res = urllib.request.urlopen(url)
urllib_print_response(res, conv_json=True)

### Now let's do all of that again, but with the requests library
# So let's open a regular website!
res = requests.get("https://semver.org/")
requests_print_response(res, limit_read=100)

# Let's open an URL that returns an API for weather
url = "https://api.weather.gov/gridpoints/OKX/65,67/forecast"
res = requests.get(url)
requests_print_response(res)

# Let's open a GET request but with added added to the URL
url = "https://opentdb.com/api.php"
data = {'amount': 10}
res = requests.get(url, data)
requests_print_response(res)

# Let's do a POST request
url = "https://reqres.in/api/users"
data = {'name': 'morpheus', 'job': 'leader'}
header = {'User-Agent' : 'Mozilla/5.0'}         # due to it rejecting otherwise
res = requests.post(url, data, headers=header)
requests_print_response(res)

print("\n--- end ---")
# end
