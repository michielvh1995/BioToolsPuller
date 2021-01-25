import re

class Field:
    def __init__(self, name, depth = 0):
        self.name = name
        self.children = []
        self.depth = depth
        self.attributes = []

    def AddFields(self, child):
        """ Adds a a child to this field
        The field parameter can either be a string or another field
        """
        child.depth = self.depth+2
        self.children.append(child)

    def AddAttribute(self, attr, xml_attribs):
        """ Appends the list of attributes to be printed in the main tag
        inputs  :   Attribute : attr        :  The attribute object to be added to the field
        """
        if xml_attribs:
            self.attributes.append(attr)
        else:
            f = Field(attr.name)
            f.AddFields(TextField(attr.value))
            self.children.append(f)

    def Export(self, depth = 0):
        """ Turns the Field and all its children into strings
        """
        exp = []

        # Create the <name> tag
        h = " " * self.depth + "<"+self.name

        # Add attributes to said tag
        for att in self.attributes:
            h += att.Export()
        h += ">\n"

        exp.append(h)

        # Export each of the children of the field
        for c in self.children:
            cl = c.Export()
            for l in cl:
                exp.append(l)

        # Close the tag
        exp.append(" " * self.depth + "</" + self.name + ">\n")

        return exp

class Attribute(Field):
    """ Special type of Field that can be used for adding attributes to the header tag
    """
    def __init__(self, name, value = ""):
        Field.__init__(self, name)
        if value:
            self.value = value
        else:
            self.value = " "

    def Export(self):
        return " " + self.name + "=" + '"' + self.value + '"'

class TextField(Field):
    """ Special type of Field that can exclusively be used to add strings inside the attribute tags
    """
    def __init__(self, name):
        Field.__init__(self, name)

    def Export(self):
        return " " * self.depth + self.name + "\n"


class XMLGenerator(object):
    def __init__(self):
        """ This class is used to generate XML data to export tool so that they can be imported into a galaxy.
        The support format is the one retrieved from bio.tools.
        This object should be used in conjunction with the biotools class from biotools.py
        """
        self.root = None

    def addBTDIO(self, dict, name, xml_attribs = True):
        """ Adds IO fields to the dictionary
        inputs  : dictionary : dict     :   The source dictionary
                : string     : name     :   Either "input" or "output" for the fields
                :boolean     : xml_attribs   : Whether or not attributes are added

        outputs: void
        """
        iofields = Field(name = name+"s", depth = 2)
        for f in dict["function"]:
            # we're now on function level, so....

            ins = []
            for inf in f[name]:
                i = Field(name = "param")
                i.AddAttribute(Attribute("name", name+str(len(ins)+1)), xml_attribs)

                if len(inf["format"]):
                    i.AddAttribute(Attribute("format", inf["format"][0]["term"]), xml_attribs)

                if "data" in inf.keys():
                    i.AddAttribute(Attribute("type", "data"), xml_attribs)
                    i.AddAttribute(Attribute("label",inf["data"]["term"]), xml_attribs)
                ins.append(i)

            for i in ins:
                iofields.AddFields(i)

        self.root.AddFields(iofields)


    def FromBTDict(self, tool, xml_attribs = True):
        """ Extracts all necessary fields from a bio.tools tool dictionary and inserts them into the dictionary
        inputs  :   dictionary  : tool          :
                    boolean     : xml_attribs   : Whether or not attributes are added
        outputs:    void
        """
        print(tool["biotoolsID"])

        # To ensure the tool has a version value
        version = "n/a"
        if tool["version"]:
            version = str(tool["version"][0])

        # Generate the root node
        self.root = Field(name="tool")
        self.root.AddAttribute(Attribute("id", tool["biotoolsID"]), xml_attribs)
        self.root.AddAttribute(Attribute("version", version), xml_attribs)
        self.root.AddAttribute(Attribute("name", tool["name"]), xml_attribs)

        # Add the fields
        self.root.AddFields(self.generateTextField("description", re.sub(u"(\u2018|\u2019)", "'", tool["description"])))
        self.root.AddFields(self.generateTextField("command", "TODO"))
        if len(tool["link"]):
            self.root.AddFields(self.generateTextField("help", tool["link"][0]["url"]))

        # Extract and add input and output fields
        self.addBTDIO(tool, name="input", xml_attribs=xml_attribs)
        self.addBTDIO(tool, name="output", xml_attribs=xml_attribs)






        #inputs = Field(name="inputs", depth = 2)
        #for i in tool["function"]:

    def generateTextField(self, name, value, depth = 2):
        """ Creates a Field with name
        """
        desc = Field(name = name, depth = depth)
        desc.AddFields(TextField(name = value))
        return desc


    def AddDictionary(self, dict):

        self.root = Field(name="tool")

        #self.root.AddAttribute(Attribute("id", dict["id"]))
        #self.root.AddAttribute(Attribute("version", version))
        #self.root.AddAttribute(Attribute("name", tool["name"]))

        self.root.AddFields(self.generateTextField("description", re.sub(u"(\u2018|\u2019)", "'", dict["description"])))
        self.root.AddFields(self.generateTextField("command", "TODO"))

        if "help" in dict.keys():
            self.root.AddFields(self.generateTextField("help", dict["help"]))


        outputs = Field(name = "outputs", depth = 2)

        if len(dict["outputs"]):
            for f in dict["outputs"]["param"]:
                i = Field(name = "param")
                outputs.AddFields(i)

        self.root.AddFields(outputs)

        inputs = Field(name = "inputs", depth = 2)

        if len(dict["inputs"]):
            for f in dict["inputs"]["param"]:
                i = Field(name = "param")
                inputs.AddFields(i)

        self.root.AddFields(inputs)


    def Export(self, file = None, mode = 'w' ):
        with open(file, mode) as fil:
            for s in self.root.Export():
                fil.write(s)
            fil.write("\n")






"""
test = XMLGenerator()
test.dict["id"] = "test"
test.dict["name"] = "testorine"
test.dict["version"] = "0.0.1"


desc = Field("description")
val = TextField("Dit is een test")
desc.AddFields(val)

for i in desc.Export(desc):
    print i

test.children.append(desc)
test.Export("./testes.xml")
"""
