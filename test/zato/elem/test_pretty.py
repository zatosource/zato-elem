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

# Zato
from zato.elem._common import Elem

# ################################################################################################################################

class Pretty(TestCase):
    """ Tests how .pretty method works.
    """
    def setUp(self):
        self.maxDiff = None

        self.doc = Elem(attrs_ordered=True)
        self.doc.ns_map += {'a':'example.com/1', 'b':'example.com/2'}
        self.doc.b_a = 'zzz'
        self.doc.b_a.b.a_c.d.a_e.f = '123'
        self.doc.b_a.b.a_c.d.a_e.f.g[0] = '000'
        self.doc.b_a.b.a_c.d.a_e.f.g[1] = '111'
        self.doc.b_a.b.a_c.d.a_e.f.g[2] = '222'
        self.doc.b_a.b.a_c.d.a_e = 'zzz'
        self.doc.b_a.b.a_c._a = 'zxc'
        self.doc.b_a.b.a_c._b = 'qwe'
        self.doc.b_a.b.a_c.d.a_e.f.g[2]._attr1 = '1234'
        self.doc.b_a.b.a_c.d.a_e.f.g[2]._attr2 = '5678'
        self.doc.b_a.b.a_c.d.a_e.f.g.a_h # No content
        self.doc.b_a.b.a_c.d.a_e.f.g.h.b_i = '123'
        self.doc.b_a.b.a_c.d.a_e.f.g.h.b_i.a_j = 999 # Not a string and it should not be changed to one

# ################################################################################################################################

    def test_pretty_defaults(self):

        expected = b"""
b:a zzz
  b
    a:c
      #a zxc
      #b qwe
      d
        a:e zzz
          f 123
            g[0] 000
            g[1] 111
            g[2] 222
              #attr1 1234
              #attr2 5678
              a:h
              h
                b:i 123
                  a:j 999"""

        self.assertEquals(expected, self.doc.pretty())

# ################################################################################################################################

    def test_pretty_max_chars(self):

        expected = b"""
b:a z (+2)
  b
    a:c
      #a z (+2)
      #b q (+2)
      d
        a:e z (+2)
          f 1 (+2)
            g[0] 0 (+2)
            g[1] 1 (+2)
            g[2] 2 (+2)
              #attr1 1 (+3)
              #attr2 5 (+3)
              a:h
              h
                b:i 1 (+2)
                  a:j 999"""

        self.assertEquals(expected, self.doc.pretty(max_chars=1))

# ################################################################################################################################

    def test_pretty_emphasize_with(self):

        expected = b"""
-b:a zzz
  -b
    -a:c
      #a zxc
      #b qwe
      -d
        -a:e zzz
          -f 123
            -g[0] 000
            -g[1] 111
            -g[2] 222
              #attr1 1234
              #attr2 5678
              -a:h
              -h
                -b:i 123
                  -a:j 999"""

        self.assertEquals(expected, self.doc.pretty(emphasize_with='-'))

# ################################################################################################################################

    def test_pretty_indent(self):

        expected = b"""
b:a zzz
    b
        a:c
            #a zxc
            #b qwe
            d
                a:e zzz
                    f 123
                        g[0] 000
                        g[1] 111
                        g[2] 222
                            #attr1 1234
                            #attr2 5678
                            a:h
                            h
                                b:i 123
                                    a:j 999"""

        self.assertEquals(expected, self.doc.pretty(indent=4))

# ################################################################################################################################

    def test_pretty_indent_with(self):

        expected = b"""
b:a zzz
~~b
~~~~a:c
~~~~~~#a zxc
~~~~~~#b qwe
~~~~~~d
~~~~~~~~a:e zzz
~~~~~~~~~~f 123
~~~~~~~~~~~~g[0] 000
~~~~~~~~~~~~g[1] 111
~~~~~~~~~~~~g[2] 222
~~~~~~~~~~~~~~#attr1 1234
~~~~~~~~~~~~~~#attr2 5678
~~~~~~~~~~~~~~a:h
~~~~~~~~~~~~~~h
~~~~~~~~~~~~~~~~b:i 123
~~~~~~~~~~~~~~~~~~a:j 999"""

        self.assertEquals(expected, self.doc.pretty(indent_with='~'))

# ################################################################################################################################

    def test_pretty_indent_level(self):

        expected = b"""
        b:a zzz
          b
            a:c
              #a zxc
              #b qwe
              d
                a:e zzz
                  f 123
                    g[0] 000
                    g[1] 111
                    g[2] 222
                      #attr1 1234
                      #attr2 5678
                      a:h
                      h
                        b:i 123
                          a:j 999"""

        self.assertEquals(expected, self.doc.pretty(level=4))

# ################################################################################################################################
