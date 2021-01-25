
class WorkflowCreator(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.tools = []
        self.steps = {}
        self.inputs= {}

    def CopyTool(self, tool):
        """ Takes a tool and copy it to its minimal requirements to be accapted.
        TODO: This makes the tool impossible to run in a workflow as the tool still requires knowledge about its parameters.
        """
        tt = {}
        tt["uuid"] = None
        tt["label"] = None
        tt["position"] = None
        tt["annotation"] = None

        tt["id"] = tool["id"]
        tt["tool_id"] = tool["tool_id"]
        tt["content_id"] = tool["content_id"]
        tt["tool_version"] = tool["tool_version"]
        tt["name"] = tool["name"]

        tt["input_connections"] = tool["input_connections"]
        tt["outputs"] = tool["outputs"]

        tt["type"] = tool["type"]
        tt["workflow_outputs"] = tool["workflow_outputs"]

        return tt

    def DefineTool(self, tool, outputs):
        """ Convert a tool to the format of a workflow
        """

        lid = len(self.tools)

        tt = {}

        tt["uuid"] = None
        tt["label"] = None
        tt["position"] = None
        tt["annotation"] = None

        tt["id"]            = lid
        tt["tool_id"]       = tool["id"]
        tt["content_id"]    = tool["id"]
        tt["tool_version"]  = tool["version"]
        tt["name"]          = tool["name"]

        #tt["input_connections"]
        tt["outputs"]       = outputs
        tt["type"]          = tool["model_class"].lower()
        tt["workflow_outputs"] = []
        #tt["post_job_actions"] = {}

        #tt["uuid"]  = ""

        #tt["inputs"]


        return tt

    def ConnectTool(self, tid, inputs, input_steps = None):
        """ Creates a new instance of one of the earlier added tools and add it to the workflow's steps list
        inputs: int   : tid          : the tool id/index of the tool in the list of available tools for this workflow
            dictionary: inputs       : a dictionary of additional information needed as inputs for this tool
            dictionary: input_steps  : a list of IDs of tools THAT ARE ALREADY ADDED to this workflow! Can be inputs as well
        outputs:    dictionary       : the updated dictionary of the workflow tool
        """

        # Get the id of the step
        stepId = len(self.steps)

        tool = self.tools[tid].copy()
        tool["id"] = stepId
        tool["tool_inputs"] = inputs

        if input_steps:
            ins = {}
            for k in input_steps.keys():
                ins["input"+str(k)] = input_steps[k]

            tool["input_steps"] = ins

        self.steps[stepId] = tool



def testDefineTool(tool):
    test = WorkflowCreator("Test", "0.0")
    tt = test.DefineTool(tool, [{u'name': u'out_file1', u'type': u'tabular'}])

    wid = gi.workflows.get_workflows()[0]["id"]
    wf = gi.workflows.export_workflow_dict(workflow_id=wid)

    # Quick and dirty copy these fields
    tt["id"] = 3
    tt["input_connections"] = wf["steps"]["3"]["input_connections"]

    return tt

def testCopyTool(tool):
    test = WorkflowCreator("Test", "0.0")
    tt = test.CopyTool(tool)

    return tt



wid = gi.workflows.get_workflows()[0]["id"]
wf = gi.workflows.export_workflow_dict(workflow_id=wid)

tt = testDefineTool(group1)

wf["steps"]["3"] = tt
wf["name"] = "Testorine"

print("")
print("")
print("")
print("ret")


ret = gi.workflows.import_workflow_dict(workflow_dict=wf)
#gi.workflows.delete_workflow(workflow_id=ret["id"])
pprint(ret)


exit()

tt = test.CopyTool(group1)

wf["steps"]["3"] = tt

wf["name"] = "Test 2"

ret = gi.workflows.import_workflow_dict(workflow_dict=wf)
gi.workflows.delete_workflow(workflow_id=ret["id"])

exit()


tid = test.AddTool({"name":"test"})["tid"]
test.ConnectTool(tid,
        {"test": "Nee" },
        {"1": {
            "source_step": 0,
            "step_output": "output"}
        })
# pprint(vars(test))




# We need a way to get the output names etc of the tools












exit()

def DeleteHistory(gi, name = None, id = None):
    """ Deletes a history object
    """
    resL = []
    if not id:
        if name:
            histL = gi.histories.get_histories(name=name)
            for hist in histL:
                id = hist["id"]
                resL.append(gi.histories.delete_history(history_id = id))
    else:
        resL.append(gi.histories.delete_history(history_id = id))
    return resL

def UpdateHistory(gi, name = None, id = None, Payload = None):
    """ Updates a history object
    """
    if not id:
        if name:
            hist = gi.histories.get_histories(name = name)
            id = hist["id"]
    return gi.histories.delete_history(history_id = id)



def CreateWorkflow(gi, name):
    print ("nah mate")

#nh = gi.histories.create_history(name="BioBlendTest")
#print ("Created BioBlendTest")

#gi.histories.update_history(history_id=nh["id"], name="New Bioblend Name")

#nh.update(name = "New Bioblend Name")

#pprint(gi.histories.get_histories())
#DeleteHistory(gi, id = nh["id"])
# DeleteHistory(gi, name="New Bioblend Name")


# Workflow parts!
#flows = gi.workflows.get_workflows()
#wfd= gi.workflows.export_workflow_dict(workflow_id=flows[0]['id'])

# gi._make_url()
#pprint(gi.workflows.import_workflow_dict(wfd))
#flows=gi.workflows.get_workflows(name="Updated")
#gi.workflows.update_workflow(workflow_id=flows[1]['id'], name= "Updated")
#pprint(gi.workflows.delete_workflow(workflow_id=flows[0]['id']))

flows = gi.workflows.get_workflows()

work = gi.workflows.export_workflow_dict(workflow_id=flows[0]['id'])


#tool = (gi.tools.get_tools(tool_id=work["steps"]["4"]["tool_id"])[0])

#m = (re.match(r'\d\.\d\.(\d)', tool["version"]))
#print m.group(1)

#print(re.match(r'n\.n\.(n)',tool["version"]))
#exit()

work["version"] = 1
tools = work["steps"]

def FindToolUpdate(gi,tool=None, name = None):
    """
    Executes the following steps:
        1. Find what tools have a similar name
        2. Find the one with the highest version number
        3. Return that one
    """
    if name == None:
        name = tool["name"]
    return gi.tools.get_tools(name = name)


maxL = 0
maxNm = ""
maxId = 0
for i in range(len(tools)):
    sims = gi.tools.get_tools(name = tools[str(i)]["name"])
    if len(sims) > maxL:
        maxL    = len(sims)
        maxNm   = tools[str(i)]["name"]
        maxId = i

print(maxNm, maxL)

li = FindToolUpdate(gi, name=maxNm)
li2 = []

for i in li:
    if i["description"] == gi.tools.get_tools(tool_id=tools[str(maxId)]["tool_id"])[0]["description"]:
        li2.append(i)

pprint("li2")


max = 0
t = None
for i in li2:
    m = (re.match(r'\d\.\d\.(\d)', i["version"]))
    if m:
        if m.group(0) > max:
            max = m.group(0)
            t = i

pprint(t)





exit()
