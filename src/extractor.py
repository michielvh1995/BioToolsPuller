
def ExtractIO(toolF, iotype = "input"):
    """ Extract the inputs from the function array of a bio.tools tool.
    outputs: [dict] : the inputs arranged in a list of {name, type, label} dicts
    """
    ins = []
    for i, e in enumerate(toolF[iotype]):
       ins.append({
           'name' : iotype + str(i),
           'label': iotype + str(i),
           'type' : e["data"]["uri"]
           })
    return ins

def ExtractInputs(toolF):
    return ExtractIO(toolF)

def ExtractOutputs(toolF):
    return ExtractIO(toolF, "output")

def ExtractOperations(toolF):
    """ Extract the operations from the function array of a bio.tools dictionary
    """
    return [o["uri"] for o in toolF["operation"]]

def functionToIO(tool):
     """ This function extracts the input, output and operation fields from the 'function' field of a bio.tool tool and puts it along with the other fields into an output dictionary.
     """
     outp = {}

     # Copy each field to the new dictionary, with the exception of the 'function' field
     for f in tool.keys():
       if f == "function":
          continue

       outp[f] = tool[f]

     # Extract the IO and operations fields
     outp["inputs"]  = ExtractOutputs(tool["function"][0])
     outp["outputs"] = ExtractInputs (tool["function"][0])
     outp["operations"] = ExtractOperations(tool["function"][0])
  
     return outp

def RenameFields(tool):
    """ This function changes the field names to something more usable for my GA
    """
    # The old fields and their new names
    oldNewPairs = {
              "biotoolsID" : "id",
              "toolType":"type",
            }

    # Now rename the fields
    for pk in oldNewPairs.keys():
        tool[oldNewPairs[pk]] = tool.pop(pk)

    # We turn the version number from a list to a value:
    if len(tool["version"]) > 0:
        tool["version"] = tool["version"][0]
    else:
        tool["version"] = "n/a"

    # We also have to turn the type of tool into just "tool", due to programmatic constraints
    tool["type"] = "tool"

    # And finally we extract the IO fields from the tool:
    return functionToIO(tool)
