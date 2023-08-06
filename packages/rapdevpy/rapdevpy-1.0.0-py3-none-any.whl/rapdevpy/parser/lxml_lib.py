from pathlib import Path

from lxml import etree
from lxml.etree import HTMLParser

"""Tree"""


def load_tree(file_path: Path):
    parser = get_file_parser(file_path)
    return etree.parse(file_path.as_posix(), parser=parser)


def get_file_parser(file_path: Path) -> HTMLParser:
    suffix = file_path.suffix
    if suffix == ".html":
        parser = etree.HTMLParser(
            encoding="UTF-8",
            remove_blank_text=True,
            remove_comments=True,
            remove_pis=True,
        )
    else:
        parser = None
    return parser


"""Children"""


def get_children(element):
    return list(element)


def get_descendants(element):
    descendants = []
    for child in element.iter():
        descendants.append(child)
    return descendants


"""Element"""


def get_root(tree):
    root = tree.getroot()
    return root


def get_element_attribute(element, attribute):
    return element.get(attribute)


def get_source_file_name(element):
    return element.base


def get_namespace_dict(element):
    return element.nsmap


def get_namespace_prefix(element):
    return element.prefix


def get_sourceline(element):
    return element.sourceline


def get_tag(element):
    prefixed_tag = get_tag_with_namespace(element)
    return prefixed_tag.split("}")[-1]


def get_tags(elements):
    tags = []
    for element in elements:
        tags.append(get_tag(element))
    return tags


def get_namespace(element):
    prefixed_tag = get_tag_with_namespace(element)
    return prefixed_tag.split("}")[0] + "}"


def get_tag_with_namespace(element):
    return element.tag


# def get_tail(element): # haven't found a tail yet!
#     return element.tail


def get_text(element):
    return element.text


def filter_elements_by_tags(elements, tags):
    filtered = []
    for element in elements:
        if get_tag(element) in tags:
            filtered.append(element)
    return filtered


def find_by_xpath(node, xpath, namespace=None):
    """
    Relative path: body
    Absolute path: /body
    """
    return node.find(xpath, namespace)


def find_all_by_xpath(node, xpath, namespace=None):
    return node.findall(xpath, namespace)


"""Booleans"""


def is_element(element):
    return etree.iselement(element)


"""Output and stringify"""


def stringify(element):
    return etree.tostring(element, pretty_print=True)


def tree_to_file(tree, file):
    tree.write(file)
