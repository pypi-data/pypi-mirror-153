# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring
# # pylint: disable=line-too-long
# '''
#     Methods for managing default drawio nodes.

#     Most nodes in drawio are represented by mxCell tags, unless they have meta data, then they are wrapped
#     in an object tag.

#     Connectors are mxcell tags with source and target attributes, we use a connector class just to make 
#     the process a little easier.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-04-2022 15:45:00
#     `memberOf`: drawio
#     `name`: mxcell
# '''


# from lxml import etree as _etree
# import utils.string_utils as _csu

# # import json
# # import objectUtils as obj
# from utils.drawio.nodeBase import NodeBase as _NodeBase
# import utils.drawio.diagram_utils as _dia
# # from io import StringIO, BytesIO


# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring

# class Mxcell(_NodeBase):
#     def __init__(self,tree,element=None,diagram=None):
#         super().__init__(tree,element,diagram)
#         self.settings = {}
#         self.tree = tree
#         self.element = element
#         self.data = {
#             "node_type":"mxcell",
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
#         }
#         self._from_element()
#         # self.set_defaults()



#     def _from_element(self):
#         element = self.element
#         if element is not None:

#             # @Mstep [] parse the mxcell attributes
#             # mxcell = element.xpath('mxCell')
#             self.data['attributes'] = _dia.attrib_to_dict(element.attrib)

#             if 'style' in self.data['attributes']:
#                 self.data['attributes']['style'] = _dia.style_to_dict(self.data['attributes']['style'])

#             # @Mstep [] retrieve and parse the mxGeometry attributes.
#             mxgeometry = element.xpath('mxGeometry')
#             if len(mxgeometry) > 0:
#                 self.data['mxgeometry'] = _dia.attrib_to_dict(mxgeometry[0].attrib)



#             return self.data

#     # def set_coords(self,x=None,y=None,w=None,h=None):
#     #     if self.data['coords']['x'] is None:
#     #         self.coords()

#     #     if x is None:
#     #         x = self.data['mxgeometry']['x']
#     #     if y is None:
#     #         y = self.data['mxgeometry']['y']
#     #     if w is None:
#     #         w = self.data['mxgeometry']['width']
#     #     if h is None:
#     #         h = self.data['mxgeometry']['height']

#     #     self.data['coords']['x'] = x
#     #     self.data['coords']['y'] = y
#     #     self.data['coords']['width'] = w
#     #     self.data['coords']['height'] = h

#     #     self.data['mxgeometry']['x'] = self.data['coords']['x']
#     #     self.data['mxgeometry']['y'] = self.data['coords']['y']
#     #     self.data['mxgeometry']['width'] = self.data['coords']['width']
#     #     self.data['mxgeometry']['height'] = self.data['coords']['height']
#     #     mxCell = self.element.xpath('mxCell')
#     #     mxGeo = mxCell[0].xpath('mxGeometry')
#     #     for k,v in self.data['mxgeometry'].items():
#     #         mxGeo[0].attrib[k] = str(v)

#     # def coords(self):
#     #     x = self.data['mxgeometry']['x']
#     #     y = self.data['mxgeometry']['y']
#     #     width = self.data['mxgeometry']['width']
#     #     height = self.data['mxgeometry']['height']

#     #     self.data['coords']['x'] = x
#     #     self.data['coords']['y'] = y
#     #     self.data['coords']['tlc'] = [x,y]
#     #     self.data['coords']['trc'] = [x + width,y]
#     #     self.data['coords']['brc'] = [x + width,y + height]
#     #     self.data['coords']['blc'] = [x,y + height]

#     #     return self.data['coords']


# def new_mxcell(tree,diagram,id:str=None,parent=None):
#     '''
#         Create a new mxcell node in the diagram.

#         ----------

#         Arguments
#         -------------------------
#         `arg_name` {etree}
#             A reference to the etree xml

#         `diagram` {Diagram}
#             A reference to the Diagram instance this node belongs to.
#         [`id`=None] {str}
#             The node id, if not provided a random one is generated.

#         [`parent`=None] {type}
#             ???


#         Return {Mxcell}
#         ----------------------
#         An instance of the Mxcell Class

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-05-2022 10:51:06
#         `memberOf`: mcxell
#         `version`: 1.0
#         `method_name`: new_mxcell
#         * @TODO []: documentation for new_mxcell
#     '''


#     mxCell = _etree.SubElement(diagram.dia_root, 'mxCell')
#     id = _csu.gen.rand() if id is None else id
#     mxCell.attrib["id"] = id
#     if parent is not None:
#         mxCell.attrib["parent"] = parent

#     return Mxcell(tree,mxCell,diagram)



