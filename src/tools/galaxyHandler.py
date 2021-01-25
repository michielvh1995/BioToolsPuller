import bioblend.galaxy

# These are a set of wrappers to contain the bioblend API handler for galaxy workflows
# Reference list:
# Bioblend & Galaxy API tuturials
# https://github.com/nsoranzo/bioblend-tutorial/
# https://galaxyproject.github.io/training-material/topics/dev/tutorials/bioblend-api/slides.html#18
#
# Official Galaxy Github:
# https://github.com/galaxyproject/galaxy
#   API code
# https://github.com/galaxyproject/galaxy/blob/dev/lib/galaxy/webapps/galaxy/api/
#
# Official Bioblend Galaxy Github:
# https://github.com/galaxyproject/bioblend/blob/master/bioblend/galaxy

# The Galaxy API caller
d_server = 'https://usegalaxy.org/'  # Default usgalaxy server and key
d_api_key = 'f9ee4df0088fb7794be2d3b3f42c8512'

#server = 'http://localhost:8080/'
#api_key = '6e67819172924ccc612431446dba2222'

class GalaxyCaller(object):
    def __init__(self, url =d_server, key = d_api_key):
        self.gi = bioblend.galaxy.GalaxyInstance(url=url, key=key)


class GalaxyWorkflowCaller(GalaxyCaller):
    def __init__(self, url =d_server, key = d_api_key):
        GalaxyCaller.__init__(self)


    def GetWorkflowsByName(self, name= None):
        """ Get all workflows with a given name
        """

        if name:
            return self.gi.workflows.get_workflows(name=name)
        return self.gi.workflows.get_workflows()


    def GetWorkflowTools(self, id):
        """ Get all steps of a specified workflow
        """
        return self.gi.workflows.export_workflow_dict(workflow_id=id)["steps"]

    def ExportWorkflow(self, id):
        """ Get the entire workflow as a dictionary.
        This dictionary can be used to import the entire workflow into a galaxy.
        """
        return self.gi.workflows.export_workflow_dict(workflow_id=id)

    def ImportWorkfow(self, dict):
        """ Imports a workflow dictionary to the galaxy.
        """
        return self.gi.workflows.import_workflow_dict(dict)



class GalaxyToolCaller(GalaxyCaller):
    def __init__(self, url =d_server, key = d_api_key):
        GalaxyCaller.__init__(self)

    def GetToolInfo(self, name = None, toolId = None):
        """ Get information regarding a tool.
        """

        if not toolId and name:
            res = self.gi.tools.get_tools(name = name)
            if len(res) == 1:
                toolId = res[0]["id"]
            elif len(res) == 0:
                return "ERROR; no tools found"
            else:
                return res

        if toolId:
            return self.gi.tools.show_tool(toolId)


    def InstallWorkflowTools(self, dict):
        """ Install all toolshed repositories needed to run this workflow.
        """
        tools = dict["steps"]
