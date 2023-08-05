import lxml.etree as x_xml
import numpy as np
import collections
__author__ = 'Jaime Undurraga'


def xml_file_to_dict(file_name=''):
    fxml = x_xml.parse(file_name)
    xml_root = fxml.getroot()
    return get_nodes(xml_root)


def xml_string_to_dict(string_content=''):
    xml_root = x_xml.fromstring(string_content)
    return get_nodes(xml_root)


def get_nodes(in_node=[]):
    c = in_node.getchildren()
    out = {}
    if len(c) > 0:
        # check that names are not repeated
        _children_tags = []
        for i in range(len(c)):
            _children_tags.append(c[i].tag)
        repeated = [x for x, y in list(collections.Counter(_children_tags).items()) if y > 1]

        list_out = []
        for i in range(len(c)):
            _node = get_nodes(c[i])
            if c[i].tag in repeated:
                list_out.append(_node[c[i].tag])
                out.update({c[i].tag: list_out})
            else:
                out.update(_node)
        return {in_node.tag: out}

    else:
        if isinstance(in_node.text, str):
            try:
                out = {in_node.tag: float(in_node.text)}
            except ValueError:
                try:
                    out = {in_node.tag: np.array(in_node.text.split(' '), dtype=float)}
                except ValueError:
                    out = {in_node.tag: in_node.text}
            return out
        else:
            return {in_node.tag: ''}
