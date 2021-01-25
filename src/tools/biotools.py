import pprint
import requests

# This is a wrapper written to handle requests for the bio.tools API
# https://biotools.readthedocs.io/en/latest/api_reference.html

# URL of the API
URL = "https://bio.tools/api/tool/"
KEY = ""

# Set the payload of the GET request
payload = {'name':'group', 'format':'xml'}


class RequestBuilder(object):
    def __init__(self, URL, KEY = None):
        self.url = URL

        if KEY:
            self.key = KEY

class BTRequestBuilder(RequestBuilder):
    def __init__(self):
        RequestBuilder.__init__(self, URL)

        self.payload = {'format':'json'}

    def AddFilters(self, filters):
        """ Adds filters to the tools requested, these are kept between requests
        inputs:     dictionary  : filters  :    A dictionary containing each filter for the API requests
        outputs:    void
        """

        for k in filters.keys():
            self.payload[k] = filters[k]

    def Request(self, filters = None, name = None, toolID = None, operations = None, short = False, fields = None):
        """ Sends a HTML GET request to the BTRequestBuilder's URL.
        inputs:     dictionary  :   filters     : Optional; add addtiional filters to the search
                    string      :   name        : Optional; specify the tool's name
                    string      :   operations  : Optiona; specify which EDAM operations are executed by the tool
        outputs:    dictionary  : The JSON response of the GET request
        """

        payload = self.payload

        if filters:
            for k in filters.keys():
                payload[k] = filters[k]

        if name:
            payload['name']=name

        if toolID:
            payload['biotoolsID'] = toolID

        if operations:
            payload['operation']=operations

        ans = requests.get(url=self.url, params=payload)
        if payload['format'] == "json":
            ans=ans.json()
        elif payload['format'] == "xml":
            ans = ans.content
            return ans

        # Compactify the return list
        if short or fields:
            ans["list"] = [self.shorten(t, fields) for t in ans["list"]]

        return ans

    def RequestAll(self, filters = None, name = None, operations = None):
        """ Sends a HTML GET request to the BTRequestBuilder's URL.
        inputs:     dictionary  :   filters     : Optional; add addtiional filters to the search
                    string      :   name        : Optional; specify the tool's name
                    string      :   operations  : Optiona; specify which EDAM operations are executed by the tool
        outputs:    dictionary  : The JSON response of the GET request
        """
        ret = None

        # Copy the payload so that it can be savely extended
        payload = self.payload

        if filters:
            for k in filters.keys():
                payload[k] = filters[k]

        if name:
            payload['name']=name

        if operations:
            payload['operation']=operations

        page = "?page=1"

        lst = []

        while page:
            # Perform the requests
            ret = requests.get(url=self.url + page, params=payload).json()

            # Update the page URL
            page = ret["next"]

            # Add each found tool to the end of the list
            lst.extend(ret["list"])

        return {'count': len(lst), 'list':lst}

    def shorten(self, tool, fields = None):
        """ Remove fields from the tool answer to limited data
        """

        if not fields:
            return {
                'name': tool["name"],
                'biotoolsID': tool["biotoolsID"],
                'homepage': tool["homepage"],
                'version': tool["version"],
                'toolType': tool["toolType"]
            }

        outp = {}

        for f in fields:
            outp[f] = tool[f]

        return outp
