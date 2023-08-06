# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    Utility methods for the rest of the module..

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 15:45:00
    `memberOf`: drawio
    `name`: diagram_utils
'''

from typing import TypeVar as _TypeVar
from typing import Iterable as _Iterable
# from typing import TYPE_CHECKING
from lxml import etree as _etree
# import utils.drawio as _diagram_module
# _Diagram = _diagram_module.Diagram

_element_type = _TypeVar('_element_type', bound=_etree.Element)



def get_by_attribute(tree,values,attribute,element=None):
    if isinstance(values,(list)) is False:
        values = [values]
    elements = []
    for v in values:
        r = []
        if element is None:
            r = tree.xpath(f"//*[contains(@{attribute},'{v}')]")
        if element is not None:
            r = tree.xpath(f"//{element}[contains(@{attribute},'{v}')]")
        if len(r) > 0:
            elements = elements + r
    return elements

def get_by_label(tree,labels,element=None):
    if isinstance(labels,(list)) is False:
        labels = [labels]
    elements = []
    for l in labels:
        r = []
        if element is None:
            r = tree.xpath(f"//*[contains(@label,'{l}')]")
            # r = tree.xpath(f"//attribute::*[contains(., '{t}')]")
        if element is not None:
            r = tree.xpath(f"//{element}[contains(@label,'{l}')]")
        if len(r) > 0:
            elements = elements + r
    return elements

def get_diagrams(tree):
    import utils.drawio.diagram as _diagram_module
    _Diagram = _diagram_module.Diagram
    result = []
    diagrams = tree.xpath("//diagram['@name']")
    if len(diagrams) > 0:
        for d in diagrams:
            result.append(_Diagram(tree,d))
    return result

def get_connectors(element):
    return element.xpath("mxCell[@target]")

def get_children(element:_element_type)->_Iterable[_element_type]:
    '''
        Get all direct children of the element provided.

        ----------

        Arguments
        -------------------------
        `element` {any}
            The parent element to search within.

        Return {list}
        ----------------------
        A list of children elements

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 13:15:21
        `memberOf`: diagramUtils
        `version`: 1.0
        `method_name`: get_children
    '''


    if isinstance(element,(list)):
        element = element[0]
    children = element.xpath("*")
    return children

def get_diagram_root_node(element:_element_type)->_element_type:
    '''
        Retrieves the diagrams literal "root" element

        ----------

        Arguments
        -------------------------
        `element` {any}
            The diagram element to search within.

        Return {any}
        ----------------------
        The root element if it is found, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 13:17:44
        `memberOf`: diagramUtils
        `version`: 1.0
        `method_name`: get_diagram_root_node
    '''

    root = False
    mx_graph_model = element.xpath('mxGraphModel')
    if len(mx_graph_model) > 0:
        root = mx_graph_model[0].xpath('root')
    return root

def get_nodes(element):
    return element.xpath("mxCell")

def attrib_to_dict(attrib)->dict:
    '''
        Convert a nodes attributes to a dictionary.

        ----------

        Arguments
        -------------------------
        `attrib` {dict}
            The lxml attribute dictionary.

        Return {dict}
        ----------------------
        The attribute dictionary.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 13:27:45
        `memberOf`: diagramUtils
        `version`: 1.0
        `method_name`: attrib_to_dict
    '''

    
    data = {}
    for k,v in attrib.items():
        data[k] = v
    return data

def style_to_dict(style):
    data = {}
    if isinstance(style,(str)):
        styleList = style.split(";")
        for x in styleList:
            s = x.split("=")
            if len(s) > 1:
                # print(f"s: {s}")
                data[s[0]] = s[1]
    return data