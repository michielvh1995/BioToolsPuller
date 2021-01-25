from pprint import pprint

def Rename(dt):
    goal = {}
    goal["name"] = dt["name"]
    goal["inputs"] = inputs(dt["ingredients"])
    goal["outputs"] = outputs(dt["results"])
    goal["description"] = "The recipe for " + dt["name"]
    goal["id"] = dt["name"]

    return goal

def outputs(outputlist):
    outputs = []

    for e,i in enumerate(outputlist):
        it = {"name" : i["name"],
              "type" : "resource" if i["name"] in baseResources else i["name"],
              "label": "output" + str(e+1),
              "amount": i["amount"]}
        outputs.append(it)

    return outputs


def inputs(inputlist):
    inputs = []

    for e,i in enumerate(inputlist):
        it = {"name" : i["name"],
              "type" : "resource" if i["name"] in baseResources else i["name"],
              "label": "input" + str(e+1),
              "amount": i["amount"]}

        inputs.append(it)

    return inputs

baseResources = [
    "iron-ore", "copper-ore", "coal", "stone", "wood",
    "heavy-oil", "crude-oil", "light-oil", "water", "petroleum-gas"
    ]
