import re
import requests
import json

# Pretty printing
from pprint import pprint

# Biotools and galaxy
from tools.biotools import BTRequestBuilder

# ========================================================================= #
# =============================== Constants =============================== #
# ========================================================================= #


# The bio.tools API
URL = "https://bio.tools/api/tool/"

def Shorten(data, fields):
    """ Reduce the data to specific fields
    """
    r = []
    for d in data:
      ret = {}
      
      # Filter the fields
      for i in fields:
        ret[i] = data[i]
      
      # Append it to the list again
      r.append(ret)

    return r

def Request(payload, page = "?page=1"):
    """ Request the tools given a dictionary of constraints
    Returns:
        a dictionary with keys: count, previous, list, next
    """
    
    # Request the data
    ans = requests.get(url=URL+page, params=payload)

    # Extract the data in the given format
    if payload['format'] == "json":
       ans = ans.json()
        
    elif payload['format'] == "xml":
       ans = ans.content
       return ans

    return ans

def RequestAll(payload, fields = None):
    """ Get the tooldata from all pages
    Returns:
        a tuple dictionary with keys "count" and "list"
    """
    page = "?page=1"

    lst = []
    
    # Force the format to be JSON
    payload["format"] = "json"

    while page:
       # Perform the requests
       ret = Request(payload, page)

       # Update the page URL
       page = ret["next"]

       # Add each found tool to the end of the list
       lst.extend(ret["list"])

    return {'count': len(lst), 'list': lst}


# Set the payload to be requested
payload = {
          'format': 'json',
          'collectionID' : 'emboss',
        }


# count, previous, list, next
print(len(Request(payload)["list"]))

print(len(RequestAll(payload)["list"]))

# Now that we have the toolset, we export it as a json!
# And after that we can turn it into a .cpp file

