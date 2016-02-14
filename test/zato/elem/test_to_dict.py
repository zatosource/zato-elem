# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# stdlib
from unittest import TestCase
from uuid import uuid4

# Zato
from zato.elem import bunchify, Elem

# ################################################################################################################################

does_not_exist = uuid4().hex

# ################################################################################################################################

class ToDict(TestCase):
    def setUp(self):
        self.maxDiff = None

# ################################################################################################################################

class Simple(ToDict):
    """ Tests to_dict serialization - most simple documents.
    """
    def xtest_simple_01(self):
        doc = Elem()

        doc.a = 123

        expected = {'a': 123}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': 123}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_02(self):
        doc = Elem()

        doc.a = 123
        doc.a.b = 456

        expected = {'a': {'text':123, 'b':456}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'text':123, 'b':456}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b':456}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_03(self):
        doc = Elem()

        doc.a = 123
        doc.a._b = 456

        expected = {'a': {'#b': 456, u'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_04(self):
        doc = Elem()

        doc.a = 123
        doc.a.b = 456
        doc.a._b = 789

        expected = {'a': {u'text': 123, 'b': 456, '#b': 789}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {u'text': 123, 'b': 456, '#b': 789}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b':456}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_05(self):
        doc = Elem()

        doc.a = 123
        doc.a._b = 789
        doc.a.b = 456

        expected = {'a': {u'text': 123, 'b': 456, '#b': 789}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {u'text': 123, 'b': 456, '#b': 789}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b':456}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_06(self):
        doc = Elem()

        doc.a = 123
        doc.a.b

        expected = {'a': {u'text': 123, 'b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {u'text': 123, 'b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b':None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_07(self):
        doc = Elem()

        doc.a = 123
        doc.a._b

        expected = {'a': {'#b': None, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'#b': None, 'text': 123}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_08(self):
        doc = Elem()

        doc.a = 123
        doc.a.b = 456
        doc.a._b

        expected = {'a': {'#b': None, 'b': 456, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'#b': None, 'b': 456, 'text': 123}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': 456}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_09(self):
        doc = Elem()

        doc.a = 123
        doc.a._b
        doc.a.b = 456

        expected = {'a': {'#b': None, 'b': 456, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'#b': None, 'b': 456, 'text': 123}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': 456}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_10(self):
        doc = Elem()

        doc.a = 123
        doc.a.b
        doc.a._b = 789

        expected = {'a': {'#b': 789, 'b': None, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'#b': 789, 'b': None, 'text': 123}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_11(self):
        doc = Elem()

        doc.a = 123

        expected = {'a': 123}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': 123}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_12(self):
        doc = Elem()

        doc.a

        expected = {'a': None}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': None}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_13(self):
        doc = Elem()

        doc.a
        doc.a.b

        expected = {'a': {'b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_14(self):
        doc = Elem()

        doc.a
        doc.a._b

        expected = {'a': {'#b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'#b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_15(self):
        doc = Elem()

        doc.a.b
        doc.a._b

        expected = {'a': {'b': None, '#b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': None, '#b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_16(self):
        doc = Elem()

        doc.a._b
        doc.a.b

        expected = {'a': {'b': None, '#b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': None, '#b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_17(self):
        doc = Elem()

        doc.a.b
        doc.a

        expected = {'a': {'b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_18(self):
        doc = Elem()

        doc.a.b
        doc.a._b
        doc.a

        expected = {'a': {'b': None, '#b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': None, '#b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_simple_19(self):
        doc = Elem()

        doc.a._b
        doc.a.b
        doc.a

        expected = {'a': {'b': None, '#b': None}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': None, '#b': None}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': None}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class Nested(ToDict):
    """ Tests to_dict serialization - nested elements.
    """
    def xtest_nested_01(self):
        doc = Elem()

        doc.a = 1
        doc.a.b = 2
        doc.a.b.c = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        expected = {'a': {'b': {'c': {'d': {'text': 4, 'e': 5}, 'text': 3}, 'text': 2}, 'text': 1}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': {'c': {'d': {'e': 5, 'text': 4}, 'text': 3}, 'text': 2}, 'text': 1}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': {'c': {'text': 3, 'd': {'e': 5, 'text': 4}}, 'text': 2}}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'c': {'d': {'e': 5, 'text': 4}, 'text': 3}}
        out = doc.a.b.c.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'d': {'text': 4, 'e': 5}}
        out = doc.a.b.c.d.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'e': 5}
        out = doc.a.b.c.d.e.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_nested_basic_02(self):
        doc = Elem()

        doc.a.b.c.d.e = 5
        doc.a.b.c.d = 4
        doc.a.b.c = 3
        doc.a.b = 2
        doc.a = 1

        expected = {'a': {'b': {'c': {'d': {'text': 4, 'e': 5}, 'text': 3}, 'text': 2}, 'text': 1}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': {'c': {'d': {'e': 5, 'text': 4}, 'text': 3}, 'text': 2}, 'text': 1}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': {'c': {'text': 3, 'd': {'e': 5, 'text': 4}}, 'text': 2}}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'c': {'d': {'e': 5, 'text': 4}, 'text': 3}}
        out = doc.a.b.c.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'d': {'text': 4, 'e': 5}}
        out = doc.a.b.c.d.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'e': 5}
        out = doc.a.b.c.d.e.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_nested_basic_03(self):
        doc = Elem()

        doc.a = 1
        doc.a.bb = 2
        doc.a.b.c = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        out = bunchify(doc.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.c.text, 3)
        self.assertEquals(out.a.b.c.d.text, 4)
        self.assertEquals(out.a.b.c.d.e, 5)

        out = bunchify(doc.a.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.c.text, 3)
        self.assertEquals(out.a.b.c.d.text, 4)
        self.assertEquals(out.a.b.c.d.e, 5)

        out = bunchify(doc.a.bb.to_dict())

        self.assertEquals(out.bb, 2)
        expected = {'bb': 2}
        self.assertDictEqual(expected, out)

        out = bunchify(doc.a.b.to_dict())

        self.assertEquals(getattr(out.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.b.c.text, 3)
        self.assertEquals(out.b.c.d.text, 4)
        self.assertEquals(out.b.c.d.e, 5)

        out = bunchify(doc.a.b.c.to_dict())

        self.assertEquals(out.c.text, 3)
        self.assertEquals(out.c.d.text, 4)
        self.assertEquals(out.c.d.e, 5)

        out = bunchify(doc.a.b.c.d.to_dict())

        self.assertEquals(out.d.text, 4)
        self.assertEquals(out.d.e, 5)
        expected = {'d': {'e': 5, 'text': 4}}
        self.assertDictEqual(expected, out)

        out = bunchify(doc.a.b.c.d.e.to_dict())

        self.assertEquals(out.e, 5)
        expected = {'e': 5}
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_nested_basic_04(self):
        doc = Elem()

        doc.a = 1
        doc.a.bb = 2
        doc.a.b.cc = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        out = bunchify(doc.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.cc, 3)
        self.assertEquals(out.a.b.c.d.text, 4)
        self.assertEquals(out.a.b.c.d.e, 5)

        out = bunchify(doc.a.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.cc, 3)
        self.assertEquals(out.a.b.c.d.text, 4)
        self.assertEquals(out.a.b.c.d.e, 5)

# ################################################################################################################################

    def xtest_nested_basic_05(self):
        doc = Elem()

        doc.a = 1
        doc.a.bb = 2
        doc.a.b.cc = 3
        doc.a.b.c.dd = 4
        doc.a.b.c.d.e = 5

        out = bunchify(doc.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.cc, 3)
        self.assertEquals(out.a.b.c.dd, 4)
        self.assertEquals(out.a.b.c.d.e, 5)

        out = bunchify(doc.a.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.cc, 3)
        self.assertEquals(out.a.b.c.dd, 4)
        self.assertEquals(out.a.b.c.d.e, 5)

# ################################################################################################################################

    def xtest_nested_basic_06(self):
        doc = Elem()

        doc.a = 1
        doc.a.bb = 2
        doc.a.b.cc = 3
        doc.a.b.c.dd = 4
        doc.a.b.c.d.e = 5
        doc.a.b.c.d.ee = 6

        out = bunchify(doc.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.cc, 3)
        self.assertEquals(out.a.b.c.dd, 4)
        self.assertEquals(out.a.b.c.d.e, 5)
        self.assertEquals(out.a.b.c.d.ee, 6)

        out = bunchify(doc.a.to_dict())

        self.assertEquals(out.a.text, 1)
        self.assertEquals(getattr(out.a.b, 'text', does_not_exist), does_not_exist)
        self.assertEquals(out.a.bb, 2)
        self.assertEquals(out.a.b.cc, 3)
        self.assertEquals(out.a.b.c.dd, 4)
        self.assertEquals(out.a.b.c.d.e, 5)
        self.assertEquals(out.a.b.c.d.ee, 6)

# ################################################################################################################################

class TextKey(ToDict):
    """ Tests to_dict serialization with custom text elements.
    """
    def xtest_text_key_default(self):
        doc = Elem()

        doc.a = 1
        doc.a.b = 2
        doc.a.b.c = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        expected = {'a': {'b': {'c': {'d': {'text': 4, 'e': 5}, 'text': 3}, 'text': 2}, 'text': 1}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': {'c': {'d': {'e': 5, 'text': 4}, 'text': 3}, 'text': 2}, 'text': 1}}
        out = doc.a.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'b': {'c': {'text': 3, 'd': {'e': 5, 'text': 4}}, 'text': 2}}
        out = doc.a.b.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'c': {'d': {'e': 5, 'text': 4}, 'text': 3}}
        out = doc.a.b.c.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'d': {'text': 4, 'e': 5}}
        out = doc.a.b.c.d.to_dict()
        self.assertDictEqual(expected, out)

        expected = {'e': 5}
        out = doc.a.b.c.d.e.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_text_key_custom_01(self):
        doc = Elem()

        doc.a = 1
        doc.a.b = 2
        doc.a.b.c = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        text_key = 'x'

        expected = {'a': {'b': {'c': {'d': {text_key: 4, 'e': 5}, text_key: 3}, text_key: 2}, text_key: 1}}
        out = doc.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': {'c': {'d': {'e': 5, text_key: 4}, text_key: 3}, text_key: 2}, text_key: 1}}
        out = doc.a.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'b': {'c': {text_key: 3, 'd': {'e': 5, text_key: 4}}, text_key: 2}}
        out = doc.a.b.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'c': {'d': {'e': 5, text_key: 4}, text_key: 3}}
        out = doc.a.b.c.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'d': {text_key: 4, 'e': 5}}
        out = doc.a.b.c.d.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'e': 5}
        out = doc.a.b.c.d.e.to_dict(text_key)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_text_key_custom_02(self):
        doc = Elem()

        doc.a = 1
        doc.a.b = 2
        doc.a.b.c = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        text_key = 'abcdef'

        expected = {'a': {'b': {'c': {'d': {text_key: 4, 'e': 5}, text_key: 3}, text_key: 2}, text_key: 1}}
        out = doc.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': {'c': {'d': {'e': 5, text_key: 4}, text_key: 3}, text_key: 2}, text_key: 1}}
        out = doc.a.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'b': {'c': {text_key: 3, 'd': {'e': 5, text_key: 4}}, text_key: 2}}
        out = doc.a.b.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'c': {'d': {'e': 5, text_key: 4}, text_key: 3}}
        out = doc.a.b.c.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'d': {text_key: 4, 'e': 5}}
        out = doc.a.b.c.d.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'e': 5}
        out = doc.a.b.c.d.e.to_dict(text_key)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_text_key_custom_03(self):
        doc = Elem()

        doc.a = 1
        doc.a.b = 2
        doc.a.b.c = 3
        doc.a.b.c.d = 4
        doc.a.b.c.d.e = 5

        # Integer rather than text
        text_key = 123

        expected = {'a': {'b': {'c': {'d': {text_key: 4, 'e': 5}, text_key: 3}, text_key: 2}, text_key: 1}}
        out = doc.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'a': {'b': {'c': {'d': {'e': 5, text_key: 4}, text_key: 3}, text_key: 2}, text_key: 1}}
        out = doc.a.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'b': {'c': {text_key: 3, 'd': {'e': 5, text_key: 4}}, text_key: 2}}
        out = doc.a.b.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'c': {'d': {'e': 5, text_key: 4}, text_key: 3}}
        out = doc.a.b.c.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'d': {text_key: 4, 'e': 5}}
        out = doc.a.b.c.d.to_dict(text_key)
        self.assertDictEqual(expected, out)

        expected = {'e': 5}
        out = doc.a.b.c.d.e.to_dict(text_key)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class AttrPrefix(ToDict):
    """ Tests to_dict serialization with custom attribute prefixes.
    """
    def xtest_attr_prefix_default(self):
        doc = Elem()

        doc.a = 123
        doc.a._b = 456

        expected = {'a': {'#b': 456, u'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_attr_prefix_custom_len1(self):
        doc = Elem()
        doc.a = 123
        doc.a._b = 456

        expected = {'a': {'%b': 456, u'text': 123}}
        out = doc.to_dict(attr_prefix='%')
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_attr_prefix_custom_long(self):
        doc = Elem()

        doc.a = 123
        doc.a._b = 456

        expected = {'a': {'attr_b': 456, u'text': 123}}
        out = doc.to_dict(attr_prefix='attr_')
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_attr_prefix_none(self):
        doc = Elem()

        doc.a = 123
        doc.a._b = 456

        expected = {'a': {'b': 456, u'text': 123}}
        out = doc.to_dict(attr_prefix='')
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class Namespaces(ToDict):
    """ Tests handling of namespaces during to_dict serialization.
    """
    def xtest_ns_elems_default(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.x_b = 456

        expected = {'a': 123, 'b': 456}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_elems_include_ns_true(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.x_b = 456

        expected = {'a': 123, 'x_b': 456}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_attrs_default_simple(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a._x_b = 456

        expected = {'a': {'#b': 456, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_attrs_include_ns_true_simple(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a._x_b = 456

        expected = {'a': {'#x_b': 456, 'text': 123}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_attrs_default_nested(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a.q._x_b = 456

        expected = {'a': {'q': {'#b': 456}, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_attrs_include_ns_true_nested(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a.q._x_b = 456

        expected = {'a': {'q': {'#x_b': 456}, 'text': 123}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_elems_attrs_default(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a.x_b = 456
        doc.a._x_b = 789

        expected = {'a': {'text': 123, 'b': 456, '#b': 789}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_elems_attrs_ns_true(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a.x_b = 456
        doc.a._x_b = 789

        expected = {'a': {'#x_b': 789, 'text': 123, 'x_b': 456}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_elems_attrs_default_nested(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a.q.x_b = 456
        doc.a.q._x_b = 789

        expected = {'a': {'q': {'b': 456, '#b': 789}, 'text': 123}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_ns_elems_attrs_ns_true_nested(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 123
        doc.a.q.x_b = 456
        doc.a.q._x_b = 789

        expected = {'a': {'q': {'x_b': 456, '#x_b': 789}, 'text': 123}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class ListElements(ToDict):
    """ Tests to_dict serialization - list elements.
    """
    def xtest_direct1(self):
        doc = Elem()

        doc.a[0] = '000'

        expected = {'a':['000']}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_direct2(self):
        doc = Elem()

        doc.a[0] = '000'
        doc.a[1] = '111'

        expected = {'a':['000', '111']}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_direct3(self):
        doc = Elem()

        doc.a[0]

        expected = {'a':[None]}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_direct4(self):
        doc = Elem()

        doc.a[0]
        doc.a[1]

        expected = {'a':[None, None]}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_indirect1(self):
        doc = Elem()

        doc.a.b[0] = '000'

        expected = {'a': {'b': ['000']}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_indirect2(self):
        doc = Elem()

        doc.a.b[0] = '000'
        doc.a.b[1] = '111'

        expected = {'a': {'b': ['000', '111']}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_indirect3(self):
        doc = Elem()

        doc.a.b[0]

        expected = {'a': {'b': [None]}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_indirect4(self):
        doc = Elem()

        doc.a.b[0]
        doc.a.b[1]

        expected = {'a': {'b': [None, None]}}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class ListElementsNS(ToDict):
    """ Tests to_dict serialization - list elements with elements.
    """
    def xtest_direct1(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0] = '000'

        expected = {'ns0_a':['000']}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

    def xtest_direct2(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0] = '000'
        doc.a[0] = '111'

        expected = {'ns0_a':['000'], 'a':['111']}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

    def xtest_direct3(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0]

        expected = {'ns0_a':[None]}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

    def xtest_direct4(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0]
        doc.ns0_a[1]

        expected = {'ns0_a':[None, None]}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_indirect1(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.a.ns0_b[0] = '000'

        expected = {'a': {'ns0_b': ['000']}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

    def xtest_indirect2(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.a.ns0_b[0] = '000'
        doc.a.ns0_b[1] = '111'

        expected = {'a': {'ns0_b': ['000', '111']}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

    def xtest_indirect3(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a.b[0]

        expected = {'ns0_a': {'b': [None]}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

    def xtest_indirect4(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a.b[0]
        doc.ns0_a.b[1]

        expected = {'ns0_a': {'b': [None, None]}}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class TopLevel(ToDict):
    """ Tests to_dict serialization of top-level elements.
    """
    def xtest_top_level_elems_no_ns(self):
        doc = Elem()

        doc.a = 'a'
        doc.b = 'b'

        expected = {'a':'a', 'b':'b'}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_top_level_elems_ns(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc.a = 'a'
        doc.b = 'b'

        doc.x_a = 'a2'
        doc.x_b = 'b2'

        expected = {'a':'a', 'b':'b', 'x_a':'a2', 'x_b':'b2'}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_top_level_attrs_no_ns(self):
        doc = Elem()

        doc._a = 'a'
        doc._b = 'b'

        expected = {'#a':'a', '#b':'b'}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_top_level_attrs_ns(self):
        doc = Elem()
        doc.ns_map += {'x':'example.com/1'}

        doc._a = 'a'
        doc._b = 'b'

        doc._x_a = 'a2'
        doc._x_b = 'b2'

        expected = {'#a':'a', '#b':'b', '#x_a':'a2', '#x_b':'b2'}
        out = doc.to_dict(include_ns=True)
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_top_level_attrs_elems_attrs_no_ns(self):
        doc = Elem()

        doc.a = 'a'
        doc.b = 'b'

        doc._a = 'a2'
        doc._b = 'b2'

        expected = {'a':'a', 'b':'b', '#a':'a2', '#b':'b2'}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_top_level_attrs_elems_attrs_ns(self):

        doc = Elem()

        doc.a = 'a'
        doc.b = 'b'

        doc._a = 'a2'
        doc._b = 'b2'

        doc.x_a = 'a3'
        doc.x_b = 'b3'

        doc._x_a = 'a4'
        doc._x_b = 'b4'

        expected = {'a':'a', 'b':'b', '#a':'a2', '#b':'b2', 'x_a':'a3', 'x_b':'b3', '#x_a':'a4', '#x_b':'b4'}
        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_top_level_list_simple1(self):
        doc = Elem()

        doc.a[0]

        expected = {'a':[None]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_simple2(self):
        doc = Elem()

        doc.a[0]
        doc.a[1]

        expected = {'a':[None, None]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_simple3(self):
        doc = Elem()

        doc.a[0]
        doc.a[1]
        doc.a[2]

        expected = {'a':[None, None, None]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_top_level_list_value1(self):
        doc = Elem()

        doc.a[0] = 'a0'

        expected = {'a':['a0']}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_value2(self):
        doc = Elem()

        doc.a[0] = 'a0'
        doc.a[1] = 'a1'

        expected = {'a':['a0', 'a1']}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_value3(self):
        doc = Elem()

        doc.a[0] = 'a0'
        doc.a[1] = 'a1'
        doc.a[2] = 'a2'

        expected = {'a':['a0', 'a1', 'a2']}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_value4(self):
        doc = Elem()

        doc.a[0]
        doc.a[1] = 'a1'
        doc.a[2] = 'a2'

        expected = {'a':[None, 'a1', 'a2']}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_value5(self):
        doc = Elem()

        doc.a[0] = 'a0'
        doc.a[1]
        doc.a[2] = 'a2'

        expected = {'a':['a0', None, 'a2']}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_value6(self):
        doc = Elem()

        doc.a[0] = 'a0'
        doc.a[1] = 'a1'
        doc.a[2]

        expected = {'a':['a0', 'a1', None]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_top_level_list_nested1(self):
        doc = Elem()

        doc.a[0].b.c.d = 'ddd'
        doc.a[1]
        doc.a[2]

        expected = {'a': [{'b': {'c': {'d': 'ddd'}}}, None, None]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_nested2(self):
        doc = Elem()

        doc.a[0]
        doc.a[1].b.c.d = 'ddd'
        doc.a[2]

        expected = {'a': [None, {'b': {'c': {'d': u'ddd'}}}, None]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_list_nested3(self):
        doc = Elem()

        doc.a[0]
        doc.a[1]
        doc.a[2].b.c.d = 'ddd'

        expected = {'a': [None, None, {'b': {'c': {'d': u'ddd'}}}]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def xtest_top_level_mixed_all_types(self):
        doc = Elem()

        doc.a = 'a-value'
        doc.b[0] = 'b0-value'
        doc.b[1] = 'b1-value'
        doc.b[1].c[0].d = 'd-value'

        expected = {'a': 'a-value', 'b': ['b0-value', {'c': [{'d': 'd-value'}], 'text': 'b1-value'}]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_top_level_nested_twitter1(self):
        """ Based on https://dev.twitter.com/rest/reference/get/mutes/users/ids
        """
        doc = Elem()
        doc.ids = [1228026486, 54931584]
        doc.next_cursor = 0
        doc.next_cursor_str = '0'
        doc.previous_cursor = 0
        doc.previous_cursor_str = '0'

        expected = {
            'ids': [
              1228026486,
              54931584
            ],
            'next_cursor': 0,
            'next_cursor_str': '0',
            'previous_cursor': 0,
            'previous_cursor_str': '0'
        }

        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_top_level_nested_twitter2(self):
        """ Based on https://dev.twitter.com/rest/reference/get/users/profile_banner
        """
        doc = Elem()
        doc.media_id = 553639437322563584
        doc.media_id_string = '553639437322563584'
        doc.size = 998865
        doc.image.w = 2234
        doc.image.h = 1873
        doc.image.image_type = 'image/jpeg'

        expected = {
            'media_id': 553639437322563584,
            'media_id_string': '553639437322563584',
            'size': 998865,
            'image': {
              'w': 2234,
              'h': 1873,
              'image_type': 'image/jpeg'
            }
          }

        out = doc.to_dict()
        self.assertDictEqual(expected, out)

    def xtest_top_level_nested_twitter3(self):
        """ Based on https://dev.twitter.com/rest/reference/get/statuses/show/:id
        """
        doc = Elem()

        doc.coordinates = None
        doc.favorited = False
        doc.truncated = False
        doc.created_at = 'Wed Jun 06 20:07:10 +0000 2012'
        doc.id_str = '210462857140252672'
        doc.entities.urls[0].expanded_url = 'https://dev.twitter.com/terms/display-guidelines'
        doc.entities.urls[0].url = 'https://t.co/Ed4omjYs'
        doc.entities.urls[0].indices = [76, 97]
        doc.entities.urls[0].display_url = 'dev.twitter.com/terms/display-\u2026'
        doc.entities.hashtags[0].text = 'Twitterbird'
        doc.entities.hashtags[0].indices = [19, 31]
        doc.entities.user_mentions = []
        doc.in_reply_to_user_id_str = 2
        doc.contributors = [14927800]
        doc.text = "Along with our new #Twitterbird, we've also updated our Display Guidelines: https://t.co/Ed4omjYs  ^JC"
        doc.retweet_count = 66
        doc.in_reply_to_status_id_str = None
        doc.id = 210462857140252672
        doc.geo = None
        doc.retweeted = True
        doc.possibly_sensitive = False
        doc.in_reply_to_user_id = None
        doc.place = None
        doc.user.profile_sidebar_fill_color = 'DDEEF6'
        doc.user.profile_sidebar_border_color = 'C0DEED'
        doc.user.profile_background_tile = False
        doc.user.name = 'Twitter API'
        doc.user.profile_image_url = 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png'
        doc.user.created_at = 'Wed May 23 06:01:13 +0000 2007'
        doc.user.location = 'San Francisco, CA'
        doc.user.follow_request_sent = False
        doc.user.profile_link_color = '0084B4'
        doc.user.is_translator = False
        doc.user.id_str = '6253282'
        doc.user.entities.url.urls[0].expanded_url = None
        doc.user.entities.url.urls[0].url = 'http://dev.twitter.com'
        doc.user.entities.url.urls[0].indices = [0, 22]
        doc.user.entities.description.urls = []
        doc.user.default_profile = True
        doc.user.contributors_enabled = True
        doc.user.favourites_count = 24
        doc.user.url = 'http://dev.twitter.com'
        doc.user.profile_image_url_https = 'https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png'
        doc.user.utc_offset = -28800
        doc.user.id = 6253282
        doc.user.profile_use_background_image = True
        doc.user.listed_count = 10774
        doc.user.profile_text_color = '333333'
        doc.user.lang = 'en'
        doc.user.followers_count = 1212963
        doc.user.protected = False
        doc.user.notifications = None
        doc.user.profile_background_image_url_https = 'https://si0.twimg.com/images/themes/theme1/bg.png'
        doc.user.profile_background_color = 'C0DEED'
        doc.user.verified = True
        doc.user.geo_enabled = True
        doc.user.time_zone = 'Pacific Time (US & Canada)'
        doc.user.description = 'The Real Twitter API.'
        doc.user.default_profile_image = False
        doc.user.profile_background_image_url = 'http://a0.twimg.com/images/themes/theme1/bg.png'
        doc.user.statuses_count = 3333
        doc.user.friends_count = 31
        doc.user.following = True
        doc.user.show_all_inline_media = False
        doc.user.screen_name = 'twitterapi'
        doc.in_reply_to_screen_name = None
        doc.source = 'web'
        doc.in_reply_to_status_id = None

        expected = {
            'coordinates': None,
            'favorited': False,
            'truncated': False,
            'created_at': 'Wed Jun 06 20:07:10 +0000 2012',
            'id_str': '210462857140252672',

            'entities': {
                'urls': [
                    {'expanded_url': 'https://dev.twitter.com/terms/display-guidelines',
                     'url': 'https://t.co/Ed4omjYs',
                     'indices': [76, 97],
                     'display_url': 'dev.twitter.com/terms/display-\u2026'}
                ],
                'hashtags': [
                    {'text': 'Twitterbird',
                     'indices': [19, 31]}
                ],
                'user_mentions': []
            },
            'in_reply_to_user_id_str': 2,

            'contributors': [
                14927800
                ],
            'text': "Along with our new #Twitterbird, we've also updated our Display Guidelines: https://t.co/Ed4omjYs  ^JC",
            'retweet_count': 66,
            'in_reply_to_status_id_str': None,
            'id': 210462857140252672,
            'geo': None,
            'retweeted': True,
            'possibly_sensitive': False,
            'in_reply_to_user_id': None,
            'place': None,

            'user': {
                'profile_sidebar_fill_color': 'DDEEF6',
                'profile_sidebar_border_color': 'C0DEED',
                'profile_background_tile': False,
                'name': 'Twitter API',
                'profile_image_url': 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
                'created_at': 'Wed May 23 06:01:13 +0000 2007',
                'location': 'San Francisco, CA',
                'follow_request_sent': False,
                'profile_link_color': '0084B4',
                'is_translator': False,
                'id_str': '6253282',
                'entities': {
                    'url': {
                        'urls': [
                            {'expanded_url': None,
                             'url': 'http://dev.twitter.com',
                             'indices': [0, 22]
                            }
                        ]
                    },
                    'description': {'urls': []}
                    },
                'default_profile': True,
                'contributors_enabled': True,
                'favourites_count': 24,
                'url': 'http://dev.twitter.com',
                'profile_image_url_https': 'https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
                'utc_offset': -28800,
                'id': 6253282,
                'profile_use_background_image': True,
                'listed_count': 10774,
                'profile_text_color': '333333',
                'lang': 'en',
                'followers_count': 1212963,
                'protected': False,
                'notifications': None,
                'profile_background_image_url_https': 'https://si0.twimg.com/images/themes/theme1/bg.png',
                'profile_background_color': 'C0DEED',
                'verified': True,
                'geo_enabled': True,
                'time_zone': 'Pacific Time (US & Canada)',
                'description': 'The Real Twitter API.',
                'default_profile_image': False,
                'profile_background_image_url': 'http://a0.twimg.com/images/themes/theme1/bg.png',
                'statuses_count': 3333,
                'friends_count': 31,
                'following': True,
                'show_all_inline_media': False,
                'screen_name': 'twitterapi'
                },
            'in_reply_to_screen_name': None,
            'source': 'web',
            'in_reply_to_status_id': None
        }

        out = doc.to_dict()
        self.assertDictEqual(expected, out)

# ################################################################################################################################

class NestedOrder(ToDict):

    def xtest_nested_order1(self):
        doc = Elem()

        doc.a1.b1 = 'b1'
        doc.a2 = 'a2'

        expected = {'a1': {'b1': 'b1'}, 'a2':'a2'}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_nested_order2(self):
        doc = Elem()

        doc.a1 = 'a1'
        doc.a2 = 'a2'
        doc.a1.b1 = 'b1'

        expected = {'a1': {'b1': 'b1', 'text': 'a1'}, 'a2':'a2'}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_nested_order3(self):
        doc = Elem()

        doc.a2 = 'a2'
        doc.a1 = 'a1'
        doc.a1.b1 = 'b1'

        expected = {'a1': {'b1': 'b1', 'text': 'a1'}, 'a2':'a2'}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

    def xtest_nested_order4(self):
        doc = Elem()

        doc.a1.b1 = 'b1'
        doc.a2 = 'a2'
        doc.a1 = 'a1'

        expected = {'a1': {'b1': 'b1', 'text': 'a1'}, 'a2':'a2'}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

class SubElements(ToDict):
    """ Tests to_dict serialization with mixed content of simple types and other Elem instances.
    """
    def test_sub1(self):
        doc1 = Elem()
        doc2 = Elem()

        doc2.b = 123
        doc1.a = doc2

        expected = {'a': {'b': 123}}
        out = doc1.to_dict()

        self.assertDictEqual(expected, out)
