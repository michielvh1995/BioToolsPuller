import requests

class Requester:
  def __init__(self, URL = "https://bio.tools/api/tool/"):
      """ Inputs: URL : string : The URL at which location the bio.tools API is located
                                 By default this is the current URL
      """
      self.URL = URL

  def FilterFields(self, data, fields):
    """ Reduce the data to specific fields
    """
    r = []
    for d in data:
      ret = {}
      
      # Filter the fields
      for i in fields:
        ret[i] = d[i]
      
      # Append it to the list again
      r.append(ret)

    return r

  def Request(self, payload, page = "?page=1"):
    """ Request the tools given a dictionary of constraints
    Returns:
        a dictionary with keys: count, previous, list, next
    """
    
    # Request the data
    ans = requests.get(url = self.URL + page, params=payload)

    # Extract the data in the given format
    if payload['format'] == "json":
       ans = ans.json()
        
    elif payload['format'] == "xml":
       ans = ans.content
       return ans

    return ans

  def RequestAll(self, payload, fields = None):
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
       ret = self.Request(payload, page)

       # Update the page URL
       page = ret["next"]

       # Add each found tool to the end of the list
       lst.extend(ret["list"])

    return {'count': len(lst), 'list': lst}


