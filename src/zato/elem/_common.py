# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# stdlib
from collections import OrderedDict
from itertools import count

# six
from six import integer_types, iteritems, PY3, string_types as basestring

# ujson
from ujson import dumps

# zato-elem
from zato.elem._serial import DictSerializer, no_value

# cmp function as found in https://bitbucket.org/gutworth/six/pull-requests/36/add-cmp-function-removed-in-py3/diff
if PY3: # pragma: no cover
    def cmp(a, b):
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0

else: # pragma: no cover
    cmp = cmp

# ################################################################################################################################

top_level = '_zato_toplevel'
ns_prefix_max_len = 11 # It's 10 characters + 1 for slice syntax

class default_ns:
    decr =   {'decr':'http://www.w3.org/2002/07/decrypt#'}
    dsig =   {'dsig':'http://www.w3.org/2000/09/xmldsig#'}
    fo =     {'fo':'http://www.w3.org/1999/XSL/Format'}
    hl7 =    {'hl7':'urn:hl7-org:v3'}
    html =   {'html':'http://www.w3.org/1999/xhtml'}
    s11 =    {'s11':'http://schemas.xmlsoap.org/soap/envelope/'}
    s12 =    {'s12':'http://www.w3.org/2003/05/soap-envelope'}
    wsa =    {'wsa':'http://www.w3.org/2005/08/addressing'}
    wsdl11 = {'wsdl11':'http://schemas.xmlsoap.org/wsdl/'}
    wsdl20 = {'wsdl20':'http://www.w3.org/ns/wsdl'}
    xenc =   {'xenc':'http://www.w3.org/2001/04/xmlenc#'}
    xi =     {'xi':'http://www.w3.org/2001/XInclude'}
    xkms =   {'xkms':'http://www.w3.org/2002/03/xkms#'}
    xml =    {'xml':'http://www.w3.org/XML/1998/namespace'}
    xop =    {'xop':'http://www.w3.org/2004/08/xop/include'}
    xs =     {'xs':'http://www.w3.org/2001/XMLSchema'}
    xsl =    {'xsl': 'http://www.w3.org/1999/XSL/Transform'}
    zato =   {'zato':'https://zato.io/ns/20130518'}

# ################################################################################################################################

class NSMap(dict):

    def __iadd__(self, *other):
        for maybe_dict in other:
            if isinstance(maybe_dict, dict):
                self.update(maybe_dict)
            else:
                for dict_ in maybe_dict:
                    self.update(dict_)
        return self

# ################################################################################################################################

class NSInfo(object):
    """ Contains information about namespaces a given element or attribute is aware of and uses.
    """
    # For namespaces without initial prefixes.
    ns_counter = count(0)

# ################################################################################################################################

    def __init__(self, value=None, map=None):
        self.prefix = None
        self.value = value
        self.map = map or NSMap()
        self._map_inverted = {v:k for k, v in iteritems(self.map)} if self.map else {}

        # Default NS is one that was set by a user explicitely
        self.is_default = False

# ################################################################################################################################

    def __str__(self):
        return '<{} at {} prefix:`{}` value:`{}` is_def:`{}` map:`{}`>'.format(
            self.__class__.__name__, hex(id(self)), self.prefix or '', self.value, int(self.is_default), self.map)

    def __nonzero__(self):
        return self.value is not None

    def __bool__(self):
        return NSInfo.__nonzero__(self)

# ################################################################################################################################

    def set_default_ns(self, value):
        self.set_ns(value, True)

    def set_ns(self, value, is_default=False):
        if isinstance(value, dict):
            value = list(value.values())[0]
        if value in self._map_inverted:
            self.prefix = self._map_inverted[value]
            self.value = value
        else:
            if value is not None:
                self.value = value
                self.prefix = '_ns{}'.format(next(self.ns_counter))

        self._map_inverted[self.value] = None
        self.is_default = is_default

# ################################################################################################################################

def get_ns(name, ns_map, parent, is_elem=True):
    """ Returns namespace prefix, namespace itself of an element or attribute + info if it's a default one.
    """
    # TODO: The following block is a hot-spot

    # Don't look up anything if it doesn't seem to have a NS prefix
    sep_idx = name.find('_', 0, ns_prefix_max_len)
    if sep_idx:
        prefix = name[:sep_idx]
        if prefix in ns_map:
            return prefix, ns_map[prefix], False

    # Speed up access
    _top_level = top_level

    # Could be a default one for an element but not for an attribute - attributes don't inherit namespaces from parents.
    if is_elem:
        if parent.ns.is_default and parent.ns.value is not None:
            return parent.ns.prefix, parent.ns.value, True
        else:
            while parent is not None and parent._zato_elem_name != _top_level:
                if parent.ns.is_default and parent.ns.value is not None:
                    return parent.ns.prefix, parent.ns.value, True

                parent = parent._zato_parent

    # No NS at all
    return None, None, False

# ################################################################################################################################

def get_ns_name(name, ns_map):
    """ Returns prefix + name of an element or atribute.
    """
    # Don't look up anything if it doesn't seem to have a NS prefix
    sep_idx = name.find('_', 0, ns_prefix_max_len)
    if sep_idx:
        prefix = name[:sep_idx]
        if prefix in ns_map:
            name_no_ns = name[sep_idx+1:]
            name = '{}:{}'.format(prefix, name_no_ns)
            return name_no_ns, name

    # No NS at all
    return name, name

# ################################################################################################################################

class Attr(object):
    def __init__(self, name, value=None, ns_map=None, parent=None):
        self.orig_name = name
        self.name = name[1:] # [1:] to chop off the attribute indicator
        self.name_no_ns = get_ns_name(self.name, ns_map)[0]
        self.full_name = '{}{}'.format(name[0], self.name_no_ns)
        self._zato_value = value
        self.ns_prefix, self.ns, _ = get_ns(self.name, ns_map, parent, False)

    def __repr__(self):
        return '<{} at {} name:`{}` value:`{}`>'.format(
            self.__class__.__name__, hex(id(self)), self.name, self._zato_value if self._zato_value != no_value else None)

    def __cmp__(self, other):
        return cmp('{}{}'.format(self.ns, self.name), '{}{}'.format(other.ns, other.name))

    def __lt__(self, other):
        return Attr.__cmp__(self, other)

# ################################################################################################################################

class Elem(object):

    # Used by the .path attribute
    _zato_path_prefix = ''
    _zato_path_sep = '.'
    _zato_attr_prefix = '@#$.'
    _zato_attr_prefix_setattr = '_' + _zato_attr_prefix # _ is first because it will be most commonly used

# ################################################################################################################################

    def __init__(self, name=top_level, value=no_value, parent=None, attrs_ordered=False, incl_empty_text=False):
        self._zato_elem_name = name
        self._zato_value = value
        self._zato_parent = parent
        self._zato_ns_info = NSInfo()
        self._zato_children = []
        self._zato_children_names = set()
        self._zato_list_children = {}
        self._zato_attrs_ordered = attrs_ordered
        self._zato_incl_empty_text = incl_empty_text
        self._zato_attrs = OrderedDict() if attrs_ordered else {}
        self._zato_full_name_value = None
        self._zato_top_level_name = top_level

# ################################################################################################################################

    def __repr__(self):
        return '<{} at {} {}{}>'.format(
            self.__class__.__name__, hex(id(self)), self.path,
            ' `{}`'.format(self._zato_value) if self._zato_value and self._zato_value != no_value else '')

    __str__ = __repr__

    def __contains__(self, elem):
        """ Returns information if 'elem' is a child of self. Takes elem's namespace prefix, if any, into account.
        """
        return (elem if isinstance(elem, basestring) else elem._zato_elem_name) in self._zato_children_names

# ################################################################################################################################

    def __getitem__(self, label):
        """ Returns either an individual list element by its idx, an element by name, or attribute by its name.
        """
        # Elements
        if isinstance(label, integer_types):
            return self._get_elem_by_idx(label)

        else:
            if label[0] in self._zato_attr_prefix:
                return self._get_attr_by_name(label)

            existing_child = self.get_child(label)
            return existing_child if existing_child is not None else self._new_elem(label, self)

# ################################################################################################################################

    def __setitem__(self, label, value):
        """ Sets either a value of an individual list element or that of an attribute.
        """
        elem = self.__getitem__(label)._zato_value = value
        return elem

# ################################################################################################################################

    def __delitem__(self, value):
        pass

# ################################################################################################################################

    def __len__(self):
        return len(self._zato_children)

# ################################################################################################################################

    def __length_hint__(self):
        return len(self._zato_children)

# ################################################################################################################################

    def __nonzero__(self):
        return self._zato_value == no_value

# ################################################################################################################################

    def __bool__(self):
        return Elem.__nonzero__(self)

# ################################################################################################################################

    def __getattr__(self, name):
        """ Invoked when an attribute of a Python instance cannot be found.
        Dynamically creates a new element in the tree of elements.
        """
        if name[0] in self._zato_attr_prefix_setattr:
            return self._get_attr_by_name(name)
        else:
            return self._new_elem(name, self)

# ################################################################################################################################

    def __setattr__(self, name, value):
        """ Called on attribute access, i.e. foo.bar.baz.
        If the name starts with _zato or ns it is understood to be an internal attribute and is returned as is.
        If the value is not an already existing element/attribute, a new one is created unless it already exists.
        """
        if not name.startswith('_zato'):
            if name in ('ns', 'ns_map'):
                object.__setattr__(self, name, value)
                return

            elif not isinstance(value, Elem):
                existing_child = self.get_child(name)
                if existing_child is not None:
                    existing_child._zato_value = value
                    return
                else:
                    if name[0] in self._zato_attr_prefix_setattr:
                        return self._get_attr_by_name(name, value)
                    else:
                        self._new_elem(name, self, value)
                        return
            else:
                print(3333, name, value)

        object.__setattr__(self, name, value)

# ################################################################################################################################

    def get_child(self, name):
        # TODO: This could be sped up by using a dict to keep children names in addition to self._zato_children,
        # in that manner there would be no iteration here
        for child in self._zato_children:
            if child._zato_elem_name == name:
                return child

    def has_list_child(self, child):
        # TODO: Same or similar speed up as in get_child
        if self._zato_list_children:
            for children in self._zato_list_children.values():
                for _child in children:
                    if child._full_zato_name == _child._full_zato_name:
                        return True

# ################################################################################################################################

    @property
    def ns(self):
        return self._zato_ns_info

    @ns.setter
    def ns(self, value):
        self._zato_ns_info.set_default_ns(value)

# ################################################################################################################################

    @property
    def ns_map(self):
        return self._zato_ns_info.map

    @ns_map.setter
    def ns_map(self, value):
        self._zato_ns_info.map.update(value)

# ################################################################################################################################

    @property
    def path(self):
        """ Returns a full path to the element down from the root. Includes indexes, if any.
        Takes format-specific information into account, such as XML namespaces
        and separators different for XML or JSON and other formats.
        """
        out = []
        if self._zato_elem_name != top_level:
            out.append(self._full_zato_name)

        for parent in self.yield_ancestors(self):
            out.append(parent._full_zato_name)

        return '{}{}'.format(self._zato_path_prefix, self._zato_path_sep.join(reversed(out)))

# ################################################################################################################################

    @property
    def attrs(self):
        """ All attributes of the element.
        """
        return self._zato_attrs.values()

# ################################################################################################################################

    @property
    def _full_zato_name(self):
        """ Full name of an element, including its namespace and index in parent's list (if any).
        """
        if not self._zato_full_name_value:
            idx = self._get_list_idx()
            idx = '[{}]'.format(idx) if idx is not None else ''
            self._zato_full_name_value = '{}{}'.format(get_ns_name(self._zato_elem_name, self.ns_map)[1], idx)

        return self._zato_full_name_value

    @property
    def _no_ns_zato_name(self):
        """ Name of the element without its namespace prefix, if any.
        """
        # Don't look up anything if it doesn't seem to have a NS prefix
        if '_' in self._zato_elem_name[:ns_prefix_max_len]:
            sep_idx = self._zato_elem_name.find('_', 0, ns_prefix_max_len)
            if sep_idx:
                prefix = self._zato_elem_name[:sep_idx]
                if prefix in self.ns_map:
                    return self._zato_elem_name[sep_idx+1:]

        return self._zato_elem_name

# ################################################################################################################################

    def _get_value_max_chars(self, orig_value, max_chars):
        if isinstance(orig_value, basestring):
            value = orig_value[:max_chars]
            if len(value) < len(orig_value):
                return '{} (+{})'.format(value, len(orig_value) - max_chars)
            else:
                return value
        else:
            return orig_value

    def pretty(self, max_chars=20, emphasize_with='', indent=2, indent_with=' ', level=0):
        """ Returns a pretty representation of the tree of elements.
        @max_chars - how many characters of string values to return
        @emphasize_with - vertical separator to emphasize indentation with
        @indent - how much space to add on each level
        @indent_with - horizontal indentation character
        @level - level of indentation to start with, defaults to -1 to account for the internal top level element
        """
        if self._zato_elem_name != top_level:
            out = '{}{}{}'.format(indent_with * level * indent, emphasize_with, self._full_zato_name)
        else:
            out = ''

        if self._zato_value != no_value:
            out += ' {}'.format(self._get_value_max_chars(self._zato_value, max_chars))

        # Display attributes before elements ..
        for attr in self.attrs:
            out += '\n{}#{} {}'.format(
                indent_with * (level+1) * indent, attr.name, self._get_value_max_chars(attr._zato_value, max_chars))

        for child in self._zato_children:
            out += '\n' + child.pretty(
                max_chars, emphasize_with, indent, indent_with, level+1 if self._zato_elem_name != top_level else level
                ).decode('utf-8')

        return out.encode('utf-8')

# ################################################################################################################################

    def _get_list_idx(self):
        """ Returns idx in self parent's _zato_list_children as long as this is a list element at all.
        """
        if self._zato_parent._zato_list_children:
            values = self._zato_parent._zato_list_children.values()
            for children in values:
                if self in children:
                    return children.index(self)

# ################################################################################################################################

    def yield_ancestors(self, start):
        parent = start._zato_parent
        while parent and parent._zato_elem_name != top_level:
            yield parent
            parent = parent._zato_parent

# ################################################################################################################################

    def _set_ns(self, name):
        """ Adds namespace information to an element or attribute + extracts actual name
        of element/attribute without namespace prefix (if any).
        """
        self.ns_map = self._zato_parent.ns_map

        name, ns, is_default = get_ns(name, self.ns_map, self._zato_parent)
        if is_default:
            self.ns.set_default_ns(ns)
        else:
            self.ns.set_ns(ns)

# ################################################################################################################################

    def _new_elem(self, name, parent, value=no_value):
        """ Creates a new element, sets its namespace and makes the parent aware of it.
        """
        elem = self.__class__(
            name, value=value, parent=parent, attrs_ordered=parent._zato_attrs_ordered,
            incl_empty_text=self._zato_incl_empty_text)
        elem._set_ns(name)
        elem._zato_elem_name = name
        setattr(parent, elem._zato_elem_name, elem)
        parent._zato_children.append(elem)
        parent._zato_children_names.add(name)

        return elem

# ################################################################################################################################

    def _validate_get_item_idx(self, list_child, idx, len_list_child):
        """ Raises IndexError if an element under idx cannot be added to list_child.
        This will be the case if:
        * the list is empty and idx is not 0
        * the list is not empty and idx would not point to the intent of creating a new element
        """

        # If there are no elements, the only accepted index is 0
        # If there is at least one elment, the index must not be greater than len_list_child
        # because otherwhise it would mean adding an element past the boundaries of the list.
        if (not list_child and idx > 0) or idx > len_list_child:

            if idx - len_list_child == 1:
                missing = '[{}] is'.format(len_list_child)
            else:
                missing = '[{}-{}] are'.format(len_list_child, idx-1)

            # self.path will end with an index so we must strip it off for the purpose of error reporting.
            path = self.path
            path = path[:path.rfind('[')]

            raise IndexError('Cannot access idx {}, {}{} missing'.format(idx, path, missing))

# ################################################################################################################################

    def _get_elem_by_idx(self, idx):
        """ Returns an element by its index in parent's list of elements of that name
        If idx is within boundaries of already existing elements, the element the idx is pointing to is returned.
        If idx is len(child_elements) + 1, a new element is added.
        Otherwise, IndexError is raised.
        """
        # All children of our parent with the same name as ours, i.e. our siblings.
        list_child = self._zato_parent._zato_list_children.setdefault(self._zato_elem_name, [])
        len_list_child = len(list_child)

        # Raises IndexError if invalid idx
        self._validate_get_item_idx(list_child, idx, len_list_child)

        # At that point we know that we either append a new element or modify an existing one.

        # New element
        if idx == len_list_child:
            elem = self._new_elem(self._zato_elem_name, self._zato_parent)
            list_child.append(elem)

            if idx == 0:
                for child in self._zato_parent._zato_children:
                    if child._full_zato_name == self._full_zato_name:
                        self._zato_parent._zato_children.remove(child)

            return elem

        # Update existing element
        else:
            return list_child[idx]

# ################################################################################################################################

    def _get_attr_by_name(self, name, value=None):
        return self._zato_attrs.setdefault(name, Attr(name, value, ns_map=self.ns_map, parent=self))

# ################################################################################################################################

    def append(self, value):
        self.__setitem__(len(self._zato_parent._zato_list_children.setdefault(self._zato_elem_name, [])), value)

# ################################################################################################################################

    def insert(self, value):
        pass

# ################################################################################################################################

    def update(self, values):
        pass

# ################################################################################################################################

    def extend(self, value):
        pass

# ################################################################################################################################

    def index(self, value):
        pass

# ################################################################################################################################

    def get(self, name, default):
        pass

# ################################################################################################################################

    def pop(self, name, default):
        pass

# ################################################################################################################################

    def keys(self, name, default):
        pass

# ################################################################################################################################

    def values(self, name, default):
        pass

# ################################################################################################################################

    def items(self, name, default):
        pass

# ################################################################################################################################

    def iterkeys(self, name, default):
        pass

# ################################################################################################################################

    def itervalues(self, name, default):
        pass

# ################################################################################################################################

    def iteritems(self, name, default):
        pass

# ################################################################################################################################

    def clear(self, name, default):
        pass

# ################################################################################################################################

    def has_key(self, name, default):
        pass

# ################################################################################################################################

    def fromkeys(self, name, default):
        pass

# ################################################################################################################################

    def get_parent(self, name, default):
        pass

# ################################################################################################################################

    def get_children(self, name, default):
        pass

# ################################################################################################################################

    def walk_tree(self, on_value, on_attr, on_non_list_child, on_list_child, include_ns=None, opaque=None):
        """ Goes through all nodes in the internal tree and invokes callback functions on each of them.
        May be used recursivelly if needed - context is kept in the 'out' callback data.
        """
        # We want for both top-level elements to behave as they were the _zato_top_level_name one
        # because it's a natural way to think of them, i.e. doc.walk_tree() and doc.a.walk_tree() should both anchor at .a
        if self._zato_elem_name != self._zato_top_level_name:
            opaque = on_value(self._zato_value, self, opaque)

        for attr in self.attrs:
            opaque = on_attr(attr.name if include_ns else attr.name_no_ns, attr._zato_value, attr, self, opaque)

        for child in self._zato_children:
            if self.has_list_child(child):
                continue

            on_non_list_child(
                child._zato_elem_name if include_ns else child._no_ns_zato_name, child, opaque)

        for children in self._zato_list_children.values():
            for idx, child in enumerate(children):
                on_list_child(
                    idx, child._zato_elem_name if include_ns else child._no_ns_zato_name, child, opaque)

# ################################################################################################################################

    def to_dict(self, text_key='text', attr_prefix='#', include_ns=False, serializer=DictSerializer):
        """ Returns a dict representation of a given root node, including its attributes and any children.
            The root may not necessarily be a top-level element, any node in the tree can be serialized to dict.
        """
        return serializer(self, text_key, include_ns, attr_prefix, self._zato_incl_empty_text, {}).serialize()

# ################################################################################################################################

    def to_json(self, text_key='text', include_ns=False, dumps_func=dumps):
        """ Dumps a tree of nodes to JSON.
        """
        return dumps_func(self.to_dict(text_key, include_ns))
