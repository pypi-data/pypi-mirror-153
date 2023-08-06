# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring
# # pylint: disable=line-too-long
# '''
#     Methods for managing drawio nodes that are wrapped in an object tag.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-04-2022 15:45:00
#     `memberOf`: drawio
#     `name`: onode
# '''

# from lxml import etree as _etree
# import utils.string_utils as _csu
# import utils.dict_utils as _obj
# from utils.drawio.nodeBase import NodeBase as _NodeBase
# import utils.drawio.diagram_utils as _dia

# def new_onode(tree,diagram,id:str=None,**kwargs):
#     '''
#         Creates a new element for an object node.

#         ----------

#         Keyword Arguments
#         -------------------------
#         [`x`=0] {int|str}
#             The initial x coordinate of the node
#         [`y`=0] {int|str}
#             The initial y coordinate of the node
#         [`w`=120] {int|str}
#             The initial width of the node
#         [`h`=60] {int|str}
#             The initial height of the node

#         Arguments
#         -------------------------
#         `tree` {object}
#             A reference to the lxml tree object.
#         `diagram` {object}
#             A reference to the Diagram instance this node is added to.
#         [`id`=None] {string}
#             The optional id of the node, if not provided, a random one is generated.

#         Return {Onode}
#         ----------------------
#         An Onode instance.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 05-27-2022 11:13:10
#         `memberOf`: onode
#         `version`: 1.0
#         `method_name`: new_onode
#     '''

#     x = _obj.get_kwarg(['x'],"0",(int,str),**kwargs)
#     y = _obj.get_kwarg(['y'],"0",(int,str),**kwargs)
#     width = _obj.get_kwarg(['width','w'],"120",(int,str),**kwargs)
#     height = _obj.get_kwarg(['height','h'],"60",(int,str),**kwargs)

#     o = _etree.SubElement(diagram.dia_root, 'object')
#     id = _csu.gen.rand() if id is None else id
#     o.attrib['id'] = id

#     mxCell = _etree.SubElement(o, 'mxCell')
#     # mxCell.attrib['style']="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=10;fillColor=#76608a;strokeColor=#432D57;fontColor=#ffffff;"
#     mxCell.attrib['style']="rounded=0;whiteSpace=wrap;html=1;"
#     mxCell.attrib['vertex']="1"
#     mxCell.attrib['parent']="1"

#     mxGeo = _etree.SubElement(mxCell, 'mxGeometry')
#     mxGeo.attrib['x']=str(x)
#     mxGeo.attrib['y']=str(y)
#     mxGeo.attrib['width']=str(width)
#     mxGeo.attrib['height']=str(height)
#     mxGeo.attrib['as']="geometry"

#     return Onode(tree,o,diagram)

# class Onode(_NodeBase):
#     def __init__(self,tree,element=None,diagram=None):
#         super().__init__(tree,element,diagram)
#         self.settings = {}
#         self.tree = tree
#         self.element = element
#         self.data = {
#             "node_type":"onode",
#             "lxml":"",
#             "xml":"",
#             "coords":{
#                 "x":None,
#                 "y":None,
#                 "tlc":[],
#                 "trc":[],
#                 "brc":[],
#                 "blc":[],
#             },
#             "attributes":{},
#             "mxcell":{
#                 "attributes":{},
#                 "style":{},
#                 "vertex":None,
#                 "parent":None,
#             },
#             "mxgeometry":{
#                 "x":None,
#                 "y":None,
#                 "width":None,
#                 "height":None,
#                 "as":None,
#             },
#         }
#         self._from_element()

#     def _from_element(self):
#         element = self.element
#         if element is not None:
#             self.data['attributes'] = _dia.attrib_to_dict(element.attrib)
#             if 'tags' in self.data['attributes']:
#                 self.data['attributes']['tags'] = self.data['attributes']['tags'].split(",")

#             # @Mstep [] parse the mxcell attributes
#             mxcell = element.xpath('mxCell')
#             if len(mxcell) > 0:
#                 self.data['mxcell']['attributes'] = _dia.attrib_to_dict(mxcell[0].attrib)
#                 # style = _dia.style_to_dict(self.data['mxcell']['attributes']['style'])
#                 # print(f"style:{style}")

#                 # @Mstep [] retrieve and parse the mxGeometry attributes.
#                 mxgeometry = mxcell[0].xpath('mxGeometry')
#                 self.data['mxgeometry'] = _dia.attrib_to_dict(mxgeometry[0].attrib)

#                 self.data['mxcell']['attributes']['style'] = _dia.style_to_dict(self.data['mxcell']['attributes']['style'])


#             return self.data

#     def has_tag(self,value):
#         '''
#             Check if this object node contains a matching tag in the tags attribute.

#             ----------

#             Arguments
#             -------------------------
#             `value` {string|list}
#                 The tag to search for.

#             Return {bool}
#             ----------------------
#             True upon success, false otherwise.

#             Meta
#             ----------
#             `author`: Colemen Atwood
#             `created`: 05-27-2022 10:56:33
#             `memberOf`: onode
#             `version`: 1.0
#             `method_name`: has_tag
#             # @xxx [05-27-2022 10:59:21]: documentation for has_tag
#         '''

#         if isinstance(value,(str)):
#             value = [value]
#         for v in value:
#             if 'tags' in self.data['attributes']:
#                 if v in self.data['attributes']['tags']:
#                     return True
#             return False

#     def set_tag(self,tag=None):
#         '''
#             Adds a new tag to the tags attribute of the object node.

#             ----------

#             Arguments
#             -------------------------
#             `tag` {string|None}
#                 The new tag to add.
#                 if None, all tags will be removed.

#             Meta
#             ----------
#             `author`: Colemen Atwood
#             `created`: 05-27-2022 10:59:30
#             `memberOf`: onode
#             `version`: 1.0
#             `method_name`: set_tag
#         '''

#         if tag is None:
#             self.data['attributes']['tags'] = []
#             return
            
#         if 'tags' in self.data['attributes']:
#             if isinstance(self.data['attributes']['tags'],(str)):
#                 self.data['attributes']['tags'] = self.data['attributes']['tags'].split(",")

#         if 'tags' not in self.data['attributes']:
#             self.data['attributes']['tags'] = []

#         self.data['attributes']['tags'].append(tag)
#         self.element.attrib['tags'] = ','.join(self.data['attributes']['tags'])

#     def remove_tag(self,tag):
#         '''
#             Remove a tag from the object node's tags attribute

#             ----------

#             Arguments
#             -------------------------
#             `tag` {string}
#                 The tag to remove.

#             Return {bool}
#             ----------------------
#             return_description

#             Meta
#             ----------
#             `author`: Colemen Atwood
#             `created`: 05-27-2022 11:01:49
#             `memberOf`: onode
#             `version`: 1.0
#             `method_name`: remove_tag
#         '''

#         new_tags = []
#         if 'tags' in self.data['attributes']:
#             for t in self.data['attributes']['tags']:
#                 if t != tag:
#                     new_tags.append(t)
#         self.data['attributes']['tags'] = new_tags
#         self.element.attrib['tags'] = ','.join(new_tags)
