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
from zato.elem._common import Attr

# ################################################################################################################################

class AttrTestCase(TestCase):
    """ Test how attributes are handled.
    """
    def test_cmp(self):
        """ Attributes should be sorted lexicographically.
        """
        ns_map = {'zzz': 'example.com'}

        attr1 = Attr('abc', ns_map=ns_map)
        attr2 = Attr('def', ns_map=ns_map)

        attr3 = Attr('abc', ns_map=ns_map)
        attr4 = Attr('zzz_def', ns_map=ns_map)

        self.assertLess(attr1, attr2)
        self.assertLess(attr3, attr4)
        self.assertLess(attr3, attr2)
        self.assertLess(attr2, attr4)
