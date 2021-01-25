import re

# Pretty printing
from pprint import pprint

# Import:
# Biotools and galaxy
from tools.biotools import BTRequestBuilder
from tools.galaxyHandler import GalaxyWorkflowCaller, GalaxyToolCaller

# Import the converter for the Factorio dataset
from tools.factorioToGalaxy import Rename

# ========================================================================= #
# =============================== Constants =============================== #
# ========================================================================= #

# The api_key and the address of my local galaxy
local = 'http://localhost:8080/'
api_key = '6e67819172924ccc612431446dba2222'

# Our caller object for galaxy workflows
gwc = GalaxyWorkflowCaller() #url = local, key = api_key)
gtc = GalaxyToolCaller()

# The tool used to retrieve bio.tools data
biotools = BTRequestBuilder()
biotools.AddFilters({'format':'json'})

#embos = biotools.Request(name ="emboss")

# ========================================================================= #
# =========================== Defining functions=========================== #
# ========================================================================= #


# TODO: Bekijk EMBOSS
# en de imagemagic voorbeeld van de APE website!
# Idealiter heb je een collectie met veel vergelijkbare, kleine operaties
#

import json

# Load the base-game recipes
recipes = {}
with open("../data/factorioVanilla.json",'r') as fVf:
    data = json.load(fVf)
    for k in data["recipes"].keys():
        recipes[k] = Rename(data["recipes"][k])
        recipes[k]["type"] = "tool"

# Load my set of alternative recipes
altRecipes = {}
with open("../data/factorioExtend.json",'r') as fVf:
    data = json.load(fVf)
    altRecipes = data["recipes"]
    for k in data["recipes"].keys():
        recipes[k] = altRecipes[k]
        recipes[k]["type"] = "tool"

items = {}
# Create a dictionary with all items and a list of their recipes.
# These are the original item recipes
for i in recipes.keys():
    if not i in items.keys():
        items[recipes[i]["outputs"][0]["name"]] = [recipes[i]["name"]]
    else:
        items[recipes[i]["outputs"][0]["name"]].append([recipes[i]["name"]])

# Add my extended set of recipes
# These recipes can be used as alternatives for the original one, if one breaks
for i in altRecipes.keys():
    if not i in items.keys():
        items[altRecipes[i]["outputs"][0]["name"]] = [altRecipes[i]["name"]]
    else:
        items[altRecipes[i]["outputs"][0]["name"]].append([altRecipes[i]["name"]])

# ========================================================================= #
# ========================== Generate the graphs ========================== #
# ========================================================================= #

def solveInputs(graph, recipe, parent):
    """ Adds all inputs of a recipe of a certain name
    inputs  :   string : parent : the index of the parent of the graph
    """

    if "inputs" in recipes[recipe].keys():

        for e in recipes[recipe]["inputs"]:
            p = 0
            if e["type"] == "resource":
                p = graph.AddVertex(tool = {"id":e["name"], "name": e["name"], "type" : "resource"})
            else:
                p = graph.AddVertex(recipes[e["name"]])
                solveInputs(graph, e["name"], p)

            graph.AddConnection(p, parent)

def GenerateGraph(item):
    """ Sets the goal of the graph and solves for all prerequisites
    """
    g = Graph()
    i = recipes[item]
    o = {"type" : "output", "id":"output","name":"output"}
    q = g.AddVertex(o)
    p = g.AddVertex(i)
    g.AddConnection(p,q)
    solveInputs(g, item, p)

    return g

def findItem(item):
    print([x for x in recipes.keys() if item in x])

tools = []
for k in recipes.keys():
    tools.append(recipes[k])


# ========================================================================= #
# ================================= Trees ================================= #
# ========================================================================= #

from workflows.graph import Graph
from workflows.tree import tree

from genetics import geneticTree

def GenResource(name):
    return {
        "id"    : name,
        "name"  : name,
        "type"  : "resource",
        "outputs": [{
            "name"  : name
        }]
    }


def TreeInputs(node):
    """
    """
    if "inputs" in node.tool.keys():
        for e in node.tool["inputs"]:
            if e["type"] == "resource":
                node.AddChild(tree.Node(tool = GenResource(e["name"])))
            else:
                ind = node.AddChild(tree.Node(recipes[e["name"]]))
                TreeInputs(node.children[ind])


def GenerateTree(item):
    """ Sets the root of the tree to the item and adds each item as a child
    """
    i = recipes[item]
    t = tree.Node(i)
    TreeInputs(t)
    return t

def GraphTreeInputs(g, tree, parent):

    # Loop over each children and add them to the graph
    for e in tree.children:
        p = g.AddVertex(e.tool)
        g.AddConnection(p, parent)
        GraphTreeInputs(g, e, p)



def GraphFromTree(tree):
    """ Turn a tree into a graph
    """
    g = Graph()

    # Set the output node
    o = {"type" : "output", "id":"output","name":"output"}
    q = g.AddVertex(o)

    # Add the root node
    p = g.AddVertex(tree.tool)
    g.AddConnection(p,q)

    # Do recursion
    GraphTreeInputs(g, tree, p)
    return g

def GraphFromNDE(tree):
    """ Decode an ND encoded tree into a graph
    """
    g = Graph()

    tree = tree.tree

    # Set the output node
    o = {"type" : "output", "id":"output","name":"output"}
    q = g.AddVertex(o)

    # Add the root node

    nl = []

    for n, d in tree:
        # Add all vertices
        nl.append((g.AddVertex(n.tool),d))

        # Now determine the connections
        if len(nl) == 1:
            g.AddConnection(nl[0][0],q)

        for i in range(len(nl)-1,-1,-1):
            if nl[i][1] == d - 1:
                g.AddConnection(nl[-1][0], nl[i][0])
                break
            elif nl[i][1] < d-1:
                raise Exception("Deze node heeft geen fucking parent!?")

    return g

from genetics import ndeGame, ndeTree, operators


# Create the goal NDETree
goal = GenerateTree("fast-inserter")
g = GraphFromTree(goal)
g.visualize("goal.pdf")
g = ndeTree.NDETree.FromTree(goal)


# Create the reference
reference = GenerateTree("inserter-alt")
ref = GraphFromTree(reference)
ref.visualize("reference.pdf")
ref = ndeTree.NDETree.FromTree(reference)

mock = [n.tool for n in g]


testG = ndeGame.NDEGame(
        n           =100,
        target      = g,
        toolset     = mock,
        heur        = lambda x,y: 1,
        mutation    = operators.EPO,
        selection   = operators.Tournament,
        crossover   = operators.ECO,
        mChance     = 0.1,
        xChance     = 0.1
    )

testG.GeneratePopulation()
best = testG.Play()
print(best)

















#mock = [{"id":"a","type": "tool"},{"id":"b","type": "tool"},{"id":"c","type": "tool"},{"id":"d","type": "tool"}]
# test = ndeTree.NDETree.GenerateRandom(mock, count = 10, mdepth=6)

def Compare(tree1, tree2):
    if not len(tree1) == len(tree2):
        print("lengtes")
        return False

    for i in range(len(tree1)):
        if not tree1[i] in tree2:
            return False

    return True


test = ndeTree.ECO(g, g)

g = GraphFromNDE(test)
g.visualize("que.pdf")

exit()
















#
