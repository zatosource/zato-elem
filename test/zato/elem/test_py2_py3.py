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
from zato.elem._common import NSInfo

# ################################################################################################################################

class Py2Py3(TestCase):
    """ Tests related to the fact that we support both Python 2 and 3.
    """
    def test_ns_info_bool(self):
        info1 = NSInfo()
        self.assertFalse(info1)
        self.assertFalse(info1.__nonzero__())
        self.assertFalse(info1.__bool__())

        info2 = NSInfo('zxc')
        self.assertTrue(info2)
        self.assertTrue(info2.__nonzero__())
        self.assertTrue(info2.__bool__())
