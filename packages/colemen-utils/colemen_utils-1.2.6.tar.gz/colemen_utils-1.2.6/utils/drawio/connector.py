# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring
# # pylint: disable=line-too-long
# '''
#     Methods for managing connector nodes.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-04-2022 16:21:17
#     `memberOf`: drawio
#     `name`: connector
# '''


# from lxml import etree as _etree
# import utils.string_utils as _csu
# from utils.drawio.nodeBase import NodeBase as _NodeBase
# from utils.drawio.diagram import Diagram as _Diagram
# import utils.drawio.diagram_utils as _dia




# def new_connector(tree:_etree,diagram:_Diagram,source:str,target:str):
#     '''
#         Create a new connector node in the diagram.

#         ----------

#         Arguments
#         -------------------------
#         `tree` {etree}
#             The node tree of the diagram.

#         `diagram` {Diagram}
#             A reference to the Diagram instance that this node belonds to.

#         `source` {str}
#             The id of the node that the connector starts from.

#         `target` {str}
#             The id of the node that the connector points to.

#         Return {Connector}
#         ----------------------
#         An instance of the Connector class.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-04-2022 16:40:21
#         `memberOf`: connector
#         `version`: 1.0
#         `method_name`: new_connector
#         * @xxx [06-04-2022 16:42:20]: documentation for new_connector
#     '''


#     o = _etree.SubElement(diagram.dia_root, 'mxCell')
#     # id = _csu.gen.rand() if id is None else id
#     o.attrib['id'] = _csu.gen.rand()
#     o.attrib['style']="edgeStyle=entityRelationEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
#     o.attrib['edge']="1"
#     o.attrib['parent']="1"
#     o.attrib['source']=source
#     o.attrib['target']=target
    
#     mxgeo = _etree.SubElement(o, 'mxGeometry')
#     mxgeo.attrib['relative'] = "1"
#     mxgeo.attrib['as'] = "geometry"
    
#     return Connector(tree,o,diagram)

# class Connector(_NodeBase):
#     '''
#         This class is used for managing connector arrows in the drawio diagrams.

#         ----------

#         Arguments
#         -------------------------
#         `tree` {etree}
#             The node tree of the diagram.

#         `diagram` {Diagram}
#             A reference to the Diagram instance that this node belonds to.

#         `source` {str}
#             The id of the node that the connector starts from.

#         `target` {str}
#             The id of the node that the connector points to.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-04-2022 16:36:04
#         `memberOf`: connector
#         `version`: 1.0
#         `name`: Connector
#         * @xxx [06-04-2022 16:40:10]: documentation for Connector
#     '''


#     def __init__(self,tree:_etree,element=None,diagram:_Diagram=None):
#         super().__init__(tree,element,diagram)
#         self.settings = {}
#         self.data = {
#             "node_type":"connector",
#             "attributes":{},
#         }
#         self._from_element()

#     def _from_element(self):
#         element = self.element
#         if element is not None:
#             self.data['attributes'] = _dia.attrib_to_dict(element.attrib)
#             return self.data
