import json

from src.biotools import Requester 
import src.extractor as Extractor

# ========================================================================= #
# =============================== Constants =============================== #
# ========================================================================= #

# Set the payload to be requested
payload = {
          'format': 'json',
          'collectionID' : 'fasta',
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
fasta = req.RequestAll(payload)["list"]
fasta = req.FilterFields(fasta, fields)

# Now we have to unpack the data to our format and mold it into a dictionary
fasta = { 'fasta' : 
           { e["id"] : Extractor.RenameFields(e) for e in fasta }
        }

print("Retrieved ", len(fasta["fasta"]), " tools")

with open("fasta.json", "w+") as fil:
   json.dump(fasta, fil, sort_keys=True, indent=4)

