# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# ################################################################################################################################

no_value = 'ZATO_NO_VALUE'

# ################################################################################################################################

class Serializer(object):
    """ Base class for subclasses serializing internal elem tree to output formats.
    """
    def __init__(self, orig_top_level=None, text_key='text', include_ns=False, attr_prefix='#', incl_empty_text=False, out=None):
        self.orig_top_level = orig_top_level
        self.text_key = text_key
        self.include_ns = include_ns
        self.attr_prefix = attr_prefix
        self.incl_empty_text = incl_empty_text
        self.out = out

    def serialize(self):
        self.orig_top_level.walk_tree(
            self.on_value, self.on_attr, self.on_non_list_child, self.on_list_child, self.include_ns, self.out)

        return self.out

    def on_value(self, value, elem, out): # pragma: no cover
        raise NotImplementedError('Must be overridden in subclasses')

    def on_attr(self, name, value, attr, elem, out): # pragma: no cover
        raise NotImplementedError('Must be overridden in subclasses')

    def on_non_list_child(self, name, elem, out): # pragma: no cover
        raise NotImplementedError('Must be overridden in subclasses')

    def on_list_child(self, idx, name, elem, out): # pragma: no cover
        raise NotImplementedError('Must be overridden in subclasses')

# ################################################################################################################################

class DictSerializer(Serializer):
    """ Serializes to a Python dict.
    """
    def _set_value(self, elem, out):
        has_children = elem._zato_children
        has_attrs = elem._zato_attrs

        name = elem._zato_elem_name if self.include_ns else elem._no_ns_zato_name

        if not (has_children or has_attrs):
            out[name] = elem._zato_value if elem._zato_value != no_value else None
        else:
            out[name] = {}
            out = out[name]
            if elem._zato_value != no_value or elem._zato_incl_empty_text:
                out[self.text_key] = elem._zato_value

        return out

    def on_value(self, value, elem, out):
        return self._set_value(elem, out)

    def on_attr(self, name, value, attr, elem, out):
        out['%s%s' % (self.attr_prefix, name if self.include_ns else attr.name_no_ns)] = value
        return out

    def on_non_list_child(self, name, elem, out):

        out = self._set_value(elem, out)
        has_children = elem._zato_children
        has_attrs = elem._zato_attrs

        if has_attrs:
            for attr in elem._zato_attrs.values():
                out['%s%s' % (self.attr_prefix, attr.name if self.include_ns else attr.name_no_ns)] = attr._zato_value

        if has_children:

            for child in elem._zato_children:
                if elem.has_list_child(child):
                    continue

                out_child = {}
                child.walk_tree(
                    self.on_value, self.on_attr, self.on_non_list_child, self.on_list_child, self.include_ns,
                    out_child)
                out.update(out_child)

            for children in elem._zato_list_children.values():
                for idx, child in enumerate(children):
                    self.on_list_child(
                        idx, child._zato_elem_name if self.include_ns else child._no_ns_zato_name, child, out)

        return out

    def on_list_child(self, idx, name, elem, out):

        # TODO: Consider changing it to a call to elem.walk_tree rather than elem.to_dict
        # to save on the number of serializer instances created = to increase performance.
        value = elem.to_dict(self.text_key, self.attr_prefix, self.include_ns)[name]

        if name in out:
            # We append an element to an already existing list so idx must equal to the len of an already existing list.
            if idx != len(out[name]):
                raise ValueError('Unexpected input (append), idx:`{}`, name:`{}`, elem:`{}`, out:`{}`'.format(
                    idx, name, elem, out))

            out[name].append(value)
        else:
            # We add a new list so idx must be equal to zero since the list did not exist before.
            if idx != 0:
                raise ValueError('Unexpected input (first), idx:`{}`, name:`{}`, elem:`{}`, out:`{}`'.format(
                    idx, name, elem, out))

            out[name] = [value]

# ################################################################################################################################
