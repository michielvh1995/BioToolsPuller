import json

from src.biotools import Requester 
import src.bioToolExtractor as Extractor

# ========================================================================= #
# =============================== Constants =============================== #
# ========================================================================= #

# Set the payload to be requested
payload = {
          'format': 'json',
          'collectionID' : 'emboss',
        }

# Reduce the fields to those which are relevant:
fields = [
        "version",
        "function",
        "description",
        "toolType",
        "biotoolsID",
        "name",
        ]

# Create requester object and get the data
req = Requester()
emboss = req.RequestAll(payload)["list"]
emboss = req.FilterFields(emboss, fields)

# Now we have to unpack the data to our format and mold it into a dictionary
emboss = { e["id"] : Extractor.RenameFields(e) for e in emboss }

with open("emboss.json", "w+") as fil:
   json.dump(emboss, fil, sort_keys=True, indent=4)

