# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# lxml
from lxml.etree import cleanup_namespaces, Element, SubElement, tostring

# Zato
from zato.elem._common import Elem, no_value, top_level

# ################################################################################################################################

class xml(Elem):
    """ A base class for working with XML.
    """
    # How to separate path elements in element's __repr__ representation.
    _zato_path_prefix = _zato_path_sep = '/'

    def _child_to_xml(self, xml_elem, child):
        """ Serializes an individual child, list or not, to XML. Recursively calls
        serialization for descendant elements.
        """
        if child._zato_ns_info:
            xml_child = SubElement(xml_elem, '{%s}%s' % (child._zato_ns_info.value, child._no_ns_zato_name))
        else:
            xml_child = SubElement(xml_elem, child._no_ns_zato_name)

        xml_child.text = child._zato_value if child._zato_value != no_value else None

        # Don't recurse if there is nothing else to add for that child
        if child.attrs or child._zato_children:
            self._root_to_xml(child, xml_child)

    def _root_to_xml(self, root, xml_elem):
        """ Recursively serializes a node and all of its descendants to XML, including attributes.
        Includes namespaces in output, both explicit and default ones.
        """
        # Serialize attributes
        for attr in root.attrs:
            xml_elem.set(attr.name_no_ns if not attr.ns else '{%s}%s' % (attr.ns, attr.name_no_ns), attr._zato_value)

        # All children, including list ones
        for child in root._zato_children:
            self._child_to_xml(xml_elem, child)

        return xml_elem

    def root_to_xml(self, root, to_string, cleanup_ns, **kwargs):
        """ Serializes root node to XML. Check to_xml's docstring for details.
        """
        # Prepare the top-level lxml element upfront
        if root._zato_ns_info:
            xml_elem = Element('{%s}%s' % (root._zato_ns_info.value, root._no_ns_zato_name))
        else:
            xml_elem = Element(root._no_ns_zato_name)

        # Root may have some text in addition to attributes and children
        xml_elem.text = root._zato_value if root._zato_value != no_value else None

        # xml_root is an lxml element
        xml_root = self._root_to_xml(root, xml_elem)

        # Useful to offer it as a parameter
        if cleanup_ns:
            cleanup_namespaces(xml_root, root._zato_ns_info.map or {})

        # Serialize by default but not always so users can customize the resulting document if need be
        if to_string:
            return tostring(xml_root, **kwargs)
        else:
            return xml_root

    def to_xml(self, to_string=True, cleanup_ns=True, **kwargs):
        """ Returns an XML representation of self. Either as lxml Element or string,
        depending on value of to_string. If cleanup_ns is True, unused namespaces will be cleaned up.
        Any keyword arguments are passed directly to lxml.etree.tostring used for string serialization.
        """
        # There must be exactly one root element. However, we raise exception only if we're serializing
        # top-level element and not if, for instance, a user selected one of middle nodes in the tree for serialization.
        if self._zato_elem_name == top_level:
            if len(self._zato_children) > 1:
                raise ValueError('Multiple roots found: `{}`'.format(self._zato_children))

            elif not self._zato_children:
                raise ValueError('No root node found')

            # We know there is exactly one child and it must be our root
            root = self._zato_children[0]

        # A node somewhere in the tree, other than top-level, is to be serialized
        else:
            root = self

        return self.root_to_xml(root, to_string, cleanup_ns, **kwargs)

# ################################################################################################################################
