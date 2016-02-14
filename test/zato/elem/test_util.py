# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2016 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# stdlib
from unittest import TestCase

# Bunch
from bunch import Bunch

# six
from six import PY2

# Zato
from zato.elem._util import bunchify

# ################################################################################################################################

class Util(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_bunchify(self):

        if PY2:
            a = {'a1':'a1', 'a2':'a2', 'a3': {'a33':'a33', 'a44':{'a444':'a444'}}}
            b = [1, 2, 3, 4, {'5':'5'}]
            c = (11, 22, 33, 44, {'55':'55'})
            d = 1
            e = str('e')

            result = bunchify(a)
            self.assertIsInstance(result, Bunch)
            self.assertDictEqual(a, result.toDict())

            result = bunchify(b)
            self.assertIsInstance(result, list)
            self.assertListEqual(b, result)

            result = bunchify(c)
            self.assertIsInstance(result, tuple)
            self.assertTupleEqual(c, result)

            result = bunchify(d)
            self.assertIsInstance(result, int)
            self.assertEqual(d, result)

            result = bunchify(e)
            self.assertIsInstance(result, str)
            self.assertEqual(e, result)
