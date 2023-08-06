# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    Methods for managing connector nodes.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 16:21:17
    `memberOf`: drawio
    `name`: connector
'''


from typing import TypeVar as _TypeVar
from typing import Iterable as _Iterable
from lxml import etree as _etree


import utils.file_utils as _f
import utils.dict_utils as _obj
import utils.string_utils as _csu
from utils.drawio.nodeBase import NodeBase as _NodeBase
# from utils.drawio.diagram import Diagram as Diagram
import utils.drawio.diagram_utils as _dia




# _diagram_type = _TypeVar('_diagram_type', bound=Diagram)

class Onode(_NodeBase):
    def __init__(self,tree,element=None,diagram=None):
        super().__init__(tree,element,diagram)
        self.settings = {}
        self.tree = tree
        self.element = element
        self.data = {
            "node_type":"onode",
            "lxml":"",
            "xml":"",
            "coords":{
                "x":None,
                "y":None,
                "tlc":[],
                "trc":[],
                "brc":[],
                "blc":[],
            },
            "attributes":{},
            "mxcell":{
                "attributes":{},
                "style":{},
                "vertex":None,
                "parent":None,
            },
            "mxgeometry":{
                "x":None,
                "y":None,
                "width":None,
                "height":None,
                "as":None,
            },
        }
        self._from_element()

    def _from_element(self):
        element = self.element
        if element is not None:
            self.data['attributes'] = _dia.attrib_to_dict(element.attrib)
            if 'tags' in self.data['attributes']:
                self.data['attributes']['tags'] = self.data['attributes']['tags'].split(",")

            # @Mstep [] parse the mxcell attributes
            mxcell = element.xpath('mxCell')
            if len(mxcell) > 0:
                self.data['mxcell']['attributes'] = _dia.attrib_to_dict(mxcell[0].attrib)
                # style = _dia.style_to_dict(self.data['mxcell']['attributes']['style'])
                # print(f"style:{style}")

                # @Mstep [] retrieve and parse the mxGeometry attributes.
                mxgeometry = mxcell[0].xpath('mxGeometry')
                self.data['mxgeometry'] = _dia.attrib_to_dict(mxgeometry[0].attrib)

                self.data['mxcell']['attributes']['style'] = _dia.style_to_dict(self.data['mxcell']['attributes']['style'])


            return self.data

    def has_tag(self,value):
        '''
            Check if this object node contains a matching tag in the tags attribute.

            ----------

            Arguments
            -------------------------
            `value` {string|list}
                The tag to search for.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 10:56:33
            `memberOf`: onode
            `version`: 1.0
            `method_name`: has_tag
            # @xxx [05-27-2022 10:59:21]: documentation for has_tag
        '''

        if isinstance(value,(str)):
            value = [value]
        for v in value:
            if 'tags' in self.data['attributes']:
                if v in self.data['attributes']['tags']:
                    return True
            return False

    def set_tag(self,tag=None):
        '''
            Adds a new tag to the tags attribute of the object node.

            ----------

            Arguments
            -------------------------
            `tag` {string|None}
                The new tag to add.
                if None, all tags will be removed.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 10:59:30
            `memberOf`: onode
            `version`: 1.0
            `method_name`: set_tag
        '''

        if tag is None:
            self.data['attributes']['tags'] = []
            return
            
        if 'tags' in self.data['attributes']:
            if isinstance(self.data['attributes']['tags'],(str)):
                self.data['attributes']['tags'] = self.data['attributes']['tags'].split(",")

        if 'tags' not in self.data['attributes']:
            self.data['attributes']['tags'] = []

        self.data['attributes']['tags'].append(tag)
        self.element.attrib['tags'] = ','.join(self.data['attributes']['tags'])

    def remove_tag(self,tag):
        '''
            Remove a tag from the object node's tags attribute

            ----------

            Arguments
            -------------------------
            `tag` {string}
                The tag to remove.

            Return {bool}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 11:01:49
            `memberOf`: onode
            `version`: 1.0
            `method_name`: remove_tag
        '''

        new_tags = []
        if 'tags' in self.data['attributes']:
            for t in self.data['attributes']['tags']:
                if t != tag:
                    new_tags.append(t)
        self.data['attributes']['tags'] = new_tags
        self.element.attrib['tags'] = ','.join(new_tags)

class Mxcell(_NodeBase):
    def __init__(self,tree,element=None,diagram=None):
        super().__init__(tree,element,diagram)
        self.settings = {}
        self.tree = tree
        self.element = element
        self.data = {
            "node_type":"mxcell",
            "lxml":"",
            "xml":"",
            "coords":{
                "x":None,
                "y":None,
                "tlc":[],
                "trc":[],
                "brc":[],
                "blc":[],
            },
            "attributes":{},
        }
        self._from_element()
        # self.set_defaults()



    def _from_element(self):
        element = self.element
        if element is not None:

            # @Mstep [] parse the mxcell attributes
            # mxcell = element.xpath('mxCell')
            self.data['attributes'] = _dia.attrib_to_dict(element.attrib)

            if 'style' in self.data['attributes']:
                self.data['attributes']['style'] = _dia.style_to_dict(self.data['attributes']['style'])

            # @Mstep [] retrieve and parse the mxGeometry attributes.
            mxgeometry = element.xpath('mxGeometry')
            if len(mxgeometry) > 0:
                self.data['mxgeometry'] = _dia.attrib_to_dict(mxgeometry[0].attrib)



            return self.data

class Connector(_NodeBase):
    '''
        This class is used for managing connector arrows in the drawio diagrams.

        ----------

        Arguments
        -------------------------
        `tree` {etree}
            The node tree of the diagram.

        `diagram` {Diagram}
            A reference to the Diagram instance that this node belonds to.

        `source` {str}
            The id of the node that the connector starts from.

        `target` {str}
            The id of the node that the connector points to.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 16:36:04
        `memberOf`: connector
        `version`: 1.0
        `name`: Connector
        * @xxx [06-04-2022 16:40:10]: documentation for Connector
    '''


    def __init__(self,tree:_etree,element=None,diagram:Diagram=None):
        super().__init__(tree,element,diagram)
        self.settings = {}
        self.data = {
            "node_type":"connector",
            "attributes":{},
        }
        self._from_element()

    def _from_element(self):
        element = self.element
        if element is not None:
            self.data['attributes'] = _dia.attrib_to_dict(element.attrib)
            return self.data


class Diagram:
    '''
        Manages a drawio diagram.
        The diagrams contains the nodes and appear as tabs in the drawing.

        ----------

        Arguments
        -------------------------
        `tree` {etree}
            The drawing xml tree.
        `element` {element}
            The etree element that will be added to the drawing.
            The new_diagram method generates this automatically.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 16:47:17
        `memberOf`: diagram
        `version`: 1.0
        `method_name`: Diagram
        * @xxx [06-04-2022 16:49:56]: documentation for Diagram
    '''


    def __init__(self,tree:_etree,element=None):
        self.settings = {}
        self.tree = tree
        self.element = element
        self.dia_root = None
        self.data = {
            "attributes":{},
            "connectors":[],
            "mxcells":[],
            "onodes":[],
            "children":[],
        }

        self._from_element()
        # self.set_defaults()

    def _from_element(self):
        element = self.element
        if element is not None:
            root_list:_Iterable = _dia.get_diagram_root_node(element)
            if len(root_list) > 0:
                dia_root = root_list[0]
                self.dia_root = dia_root
            self.data['attributes'] = _dia.attrib_to_dict(element.attrib)
            # self.data['connectors'] = _dia.get_connectors(element)
            children = _dia.get_children(self.dia_root)
            # print(f"children: {children}")
            for c in children:
                if c.tag == "mxCell":
                    if 'source' in c.attrib:
                        con = Connector(self.tree,c,self)
                        self.data['connectors'].append(con)
                        # self.data['connectors']
                        # print(f"connector Found: {c}")
                    else:
                        self.data['mxcells'].append(Mxcell(self.tree,c,self))
                        # print(f"mxcell found: {c}")

                if c.tag == "object":
                    O = Onode(self.tree,c,self)
                    self.data['onodes'].append(O)
                    # print(f"object found: {c}")
                # self.data['children']['id'] = c.attrib['id']

            return self.data

    def show_grid(self,value:bool):
        if value is True:
            self.element.attrib['grid'] = "1"
        if value is False:
            self.element.attrib['grid'] = "0"

    def grid_size(self,value:int):
        if value < 1:
            value = 10
        self.element.attrib['gridSize'] = str(value)

    def list_node_labels(self):
        '''
            Print the labels of every node in this diagram.

            ----------


            Return {None}
            ----------------------
            returns nothing.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:45:59
            `memberOf`: diagram
            `version`: 1.0
            `method_name`: list_node_labels
        '''
        x:Onode
        for x in self.data['onodes']:
            label = x.get_label(None)
            if label is not None:
                print(label)

        x:Mxcell
        for x in self.data['mxcells']:
            label = x.get_label(None)
            if label is not None:
                print(label)

        x:Connector
        for x in self.data['connectors']:
            label = x.get_label(None)
            if label is not None:
                print(label)

    def add_mxcell(self,id=None,parent=None)->Mxcell:
        cell = new_mxcell(self.tree,self,id,parent)
        self.data['mxcells'].append(cell)
        return cell

    def add_onode(self,id=None)->Onode:
        cell = new_onode(self.tree,self,id)
        self.data['onodes'].append(cell)
        return cell

    def add_connector(self,source,target)->Connector:
        cell = new_connector(self.tree,self,source,target)
        self.data['connectors'].append(cell)
        return cell

    def get_nodes_by_tag(self,tag)->_Iterable[Onode]:
        '''
            Get all nodes that contain the tag provided.

            ----------

            Arguments
            -------------------------
            `tag` {str|list}
                The tag or list of tags to search for.


            Return {list}
            ----------------------
            A list of onodes that contain the tag.
            Only object nodes support the tags attribute, so this will not include mxcells or connectors.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 13:36:21
            `memberOf`: diagram
            `version`: 1.0
            `method_name`: get_nodes_by_tag
        '''

        nodes = []
        c:Onode
        for c in self.data['onodes']:
            if c.has_tag(tag):
                nodes.append(c)
        return nodes


    def set_name(self,name:str):
        '''
            Set this diagrams name.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The new name to assign.

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 13:38:58
            `memberOf`: diagram
            `version`: 1.0
            `method_name`: set_name
        '''

        self.data['attributes']['name'] = name
        self.element.attrib['name'] = name

    def get_name(self,test_value=None,default_val=False):
        '''
            Get the name attribute of the diagram.

            ----------

            Arguments
            -------------------------
            [`test_value`=None] {str}
                If provided, the name value must match this in order to return positively.

            [`default_val`=''] {any}
                The value to return of the name does not exist or does not match the test_value.


            Return {any}
            ----------------------
            If no test_value is provided the name value is returned.
            If a test_value is provided and the name value matches, the name is returned.

            If the name attribute does not exist or does not match the test_value,
            the default_val is returned.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 11:55:25
            `memberOf`: nodeBase
            `version`: 1.0
            `method_name`: get_name
        '''

        if 'name' in self.data['attributes']:
            if test_value is not None:
                if self.data['attributes']['name'] == test_value:
                    return self.data['attributes']['name']
            else:
                return self.data['attributes']['name']
        return default_val


    def has_name(self,name=None):
        if 'name' in self.data['attributes']:
            if name is not None:
                if self.data['attributes']['name'] == name:
                    return True
            return True
        return False


class Drawing(_NodeBase):
    '''
        Used to manage drawio drawings and their diagrams.

        ----------

        Arguments
        -------------------------
        `tree` {etree}
            A reference to the lxml etree

        [`element`=None] {_etree.element}
            The drawing element of the xml file.
            This is automatically generated by the new_drawing methods.

            When a drawing is read, this class will automatically parse the drawing nodes.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 10:47:56
        `memberOf`: drawing
        `version`: 1.0
        `name`: Drawing
        * @xxx [06-05-2022 10:48:35]: documentation for Drawing
    '''


    def __init__(self,tree,element=None):
        super().__init__(tree,element)
        self.settings = {}
        self.tree = tree
        self.element = element
        self.dia_root = None
        self.data = {
            "file":{
                "file_path":None,
            },
            "diagrams":[],
        }

        _get_diagrams(self)

    def new_diagram(self,name):
        '''
            Create a new diagram in the drawing.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the diagram, this is shown on tabs in draw.io

            Return {Diagram}
            ----------------------
            An instance of the Diagram class.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:34:35
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: new_diagram
        '''

        dia = new_diagram(self.tree,name)
        self.data['diagrams'].append(dia)
        return dia

    def save(self,path=None):
        '''
            Save this drawing

            You should use set_file_path to set the default file_path for the drawing.

            ----------

            Arguments
            -------------------------
            [`path`=None] {str}
                Where to save this drawing, if not provided the default path will be used.

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                    arg_description

            Return {bool}
            ----------------------
            If no path is provided and there is no default path, it will return False.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:38:44
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: save
        '''


        # self.to_element()
        if path is None:
            if 'file_path' in self.data['file']:
                if self.data['file']['file_path'] is not None:
                    path = self.data['file']
            if path is None:
                return False
        _f.write(path,_etree.tostring(self.tree).decode("utf-8"))
        return True

    def list_diagrams(self):
        '''
            list all diagrams that belong to this drawing.

            ----------

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:40:32
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: list_diagrams
        '''


        for d in self.data['diagrams']:
            if d.has_name():
                print(d.data['attributes']['name'])

    def get_diagram(self,name:str) -> Diagram:
        '''
            Get a diagram by its name.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the diagram to return.

            Return {Diagram}
            ----------------------
            The Diagram class instance with a matching name.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:41:56
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: get_diagram
        '''
        diagram:_diagram_type
        for diagram in self.data['diagrams']:
            if diagram.get_name(name):
                return diagram
        return None

    def set_file_path(self,value):
        '''
            Set the file_path for this drawing.

            ----------

            Arguments
            -------------------------
            `value` {str}
                The file_path to where this drawing will be saved.

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:30:13
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: set_file_path
        '''

        self.data['file']['file_path'] = value

    def get_file_path(self,test_value=None,default_val=None):
        '''
            Get the file_path attribute of the drawing.

            ----------

            Arguments
            -------------------------
            [`test_value`=None] {str}
                If provided, the file_path value must match this in order to return positively.

            [`default_val`=''] {any}
                The value to return of the file_path does not exist or does not match the test_value.


            Return {any}
            ----------------------
            If no test_value is provided the file_path value is returned.
            If a test_value is provided and the file_path value matches, the file_path is returned.

            If the file_path attribute does not exist or does not match the test_value,
            the default_val is returned.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 11:55:25
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: get_file_path
        '''

        if 'file_path' in self.data['file']:
            if test_value is not None:
                if self.data['file']['file_path'] == test_value:
                    return self.data['file']['file_path']
            else:
                return self.data['file']['file_path']
        return default_val



def new_drawing(**kwargs):
    '''
        Creates a new draw.io drawing.

        ----------

        Keyword Arguments
        -------------------------
        [`file_path`=None] {string}
            The path to where the drawing should be saved.

        Return {Drawing}
        ----------------------
        An instance of the Drawing class

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:22:38
        `memberOf`: drawing
        `version`: 1.0
        `method_name`: new_drawing
    '''

    file_path = _obj.get_kwarg(['file_path','path'],None,(str),**kwargs)

    mxfile = _etree.Element("mxfile")
    mxfile.attrib['host'] = "Electron"
    mxfile.attrib['modified'] = "2022-05-26T18:37:31.077Z"
    mxfile.attrib['agent'] = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/14.9.6 Chrome/89.0.4389.128 Electron/12.0.16 Safari/537.36"
    mxfile.attrib['etag'] = "AdGKFnLcEHsRAx8fGjjM"
    mxfile.attrib['compressed'] = "false"
    mxfile.attrib['version'] = "14.9.6"
    mxfile.attrib['type'] = "device"
    dwg = Drawing(mxfile)
    if file_path is not None:
        dwg.set_file_path(file_path)
    return dwg

def read(file_path):
    '''
        Read an existing draw.io diagram.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The file_path to the diagram.

        Return {Drawing}
        ----------------------
        An instance of the Drawing class

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:31:54
        `memberOf`: drawing
        `version`: 1.0
        `method_name`: read
    '''

    
    xml = _f.read.readr(file_path)
    # tree = _etree.parse(xml)
    tree = _etree.fromstring(xml)
    drawing = Drawing(tree)
    drawing.data['file'] = _f.get_data(file_path)
    return drawing


def _get_diagrams(drawing):
    '''
        Parses the drawing to find all diagrams that it contains.
        This is used internally when reading a draw.io file.

        ----------

        Return {list}
        ----------------------
        A list of diagram instances, if no diagrams are found, the list is empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:35:48
        `memberOf`: drawing
        `version`: 1.0
        `method_name`: get_diagrams
    '''

    result = []
    diagrams = drawing.tree.xpath("//diagram['@name']")
    if len(diagrams) > 0:
        d:Diagram
        for d in diagrams:
            result.append(Diagram(drawing.tree,d))
    drawing.data['diagrams'] = result
    return result

def new_diagram(drawing:Drawing,name:str)->Diagram:
    '''
        Create a new diagram in the drawing.

        ----------

        Arguments
        -------------------------
        `drawing` {Drawing}
            A reference to the drawing that this diagram will belong to.
        `name` {str}
            The name of the diagram, this is shown on the tabs in draw.io

        Return {Diagram}
        ----------------------
        An instance of the Diagram class

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:42:40
        `memberOf`: diagram
        `version`: 1.0
        `method_name`: new_diagram
    '''

    diagram = _etree.SubElement(drawing, 'diagram')
    # diagram = _etree.Element("diagram")

    diagram.attrib['id'] = _csu.gen.rand(20)
    diagram.attrib['name'] = name

    mxgm_data = {
        "dx":"1074",
        "dy":"954",
        "grid":"1",
        "gridSize":"10",
        "guides":"1",
        "tooltips":"1",
        "connect":"1",
        "arrows":"1",
        "fold":"1",
        "page":"1",
        "pageScale":"1",
        "pageWidth":"1700",
        "pageHeight":"1100",
        "math":"0",
        "shadow":"0",
    }

    mxGraphModel = _etree.SubElement(diagram, 'mxGraphModel')
    for k,v in mxgm_data.items():
        mxGraphModel.attrib[k] = v

    # @Mstep [] create the root node for the diagram
    root = _etree.SubElement(mxGraphModel, 'root')


    d = Diagram(drawing,diagram)

    # @Mstep [] add the two default nodes to the diagram.
    d.add_mxcell("0")
    d.add_mxcell("1","0")

    # @Mstep [RETURN] return the diagram instance.
    return d

def new_onode(tree,diagram,id:str=None,**kwargs):
    '''
        Creates a new element for an object node.

        ----------

        Keyword Arguments
        -------------------------
        [`x`=0] {int|str}
            The initial x coordinate of the node
        [`y`=0] {int|str}
            The initial y coordinate of the node
        [`w`=120] {int|str}
            The initial width of the node
        [`h`=60] {int|str}
            The initial height of the node

        Arguments
        -------------------------
        `tree` {object}
            A reference to the lxml tree object.
        `diagram` {object}
            A reference to the Diagram instance this node is added to.
        [`id`=None] {string}
            The optional id of the node, if not provided, a random one is generated.

        Return {Onode}
        ----------------------
        An Onode instance.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 11:13:10
        `memberOf`: onode
        `version`: 1.0
        `method_name`: new_onode
    '''

    x = _obj.get_kwarg(['x'],"0",(int,str),**kwargs)
    y = _obj.get_kwarg(['y'],"0",(int,str),**kwargs)
    width = _obj.get_kwarg(['width','w'],"120",(int,str),**kwargs)
    height = _obj.get_kwarg(['height','h'],"60",(int,str),**kwargs)

    o = _etree.SubElement(diagram.dia_root, 'object')
    id = _csu.gen.rand() if id is None else id
    o.attrib['id'] = id

    mxCell = _etree.SubElement(o, 'mxCell')
    # mxCell.attrib['style']="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=10;fillColor=#76608a;strokeColor=#432D57;fontColor=#ffffff;"
    mxCell.attrib['style']="rounded=0;whiteSpace=wrap;html=1;"
    mxCell.attrib['vertex']="1"
    mxCell.attrib['parent']="1"

    mxGeo = _etree.SubElement(mxCell, 'mxGeometry')
    mxGeo.attrib['x']=str(x)
    mxGeo.attrib['y']=str(y)
    mxGeo.attrib['width']=str(width)
    mxGeo.attrib['height']=str(height)
    mxGeo.attrib['as']="geometry"

    return Onode(tree,o,diagram)

def new_mxcell(tree,diagram,id:str=None,parent=None):
    '''
        Create a new mxcell node in the diagram.

        ----------

        Arguments
        -------------------------
        `arg_name` {etree}
            A reference to the etree xml

        `diagram` {Diagram}
            A reference to the Diagram instance this node belongs to.
        [`id`=None] {str}
            The node id, if not provided a random one is generated.

        [`parent`=None] {type}
            ???


        Return {Mxcell}
        ----------------------
        An instance of the Mxcell Class

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 10:51:06
        `memberOf`: mcxell
        `version`: 1.0
        `method_name`: new_mxcell
        * @TODO []: documentation for new_mxcell
    '''


    mxCell = _etree.SubElement(diagram.dia_root, 'mxCell')
    id = _csu.gen.rand() if id is None else id
    mxCell.attrib["id"] = id
    if parent is not None:
        mxCell.attrib["parent"] = parent

    return Mxcell(tree,mxCell,diagram)

def new_connector(tree:_etree,diagram:Diagram,source:str,target:str):
    '''
        Create a new connector node in the diagram.

        ----------

        Arguments
        -------------------------
        `tree` {etree}
            The node tree of the diagram.

        `diagram` {Diagram}
            A reference to the Diagram instance that this node belonds to.

        `source` {str}
            The id of the node that the connector starts from.

        `target` {str}
            The id of the node that the connector points to.

        Return {Connector}
        ----------------------
        An instance of the Connector class.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 16:40:21
        `memberOf`: connector
        `version`: 1.0
        `method_name`: new_connector
        * @xxx [06-04-2022 16:42:20]: documentation for new_connector
    '''


    o = _etree.SubElement(diagram.dia_root, 'mxCell')
    # id = _csu.gen.rand() if id is None else id
    o.attrib['id'] = _csu.gen.rand()
    o.attrib['style']="edgeStyle=entityRelationEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
    o.attrib['edge']="1"
    o.attrib['parent']="1"
    o.attrib['source']=source
    o.attrib['target']=target
    
    mxgeo = _etree.SubElement(o, 'mxGeometry')
    mxgeo.attrib['relative'] = "1"
    mxgeo.attrib['as'] = "geometry"
    
    return Connector(tree,o,diagram)



