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

# Zato
from zato.elem._common import cmp as _common_cmp

# ################################################################################################################################

class Common(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_cmp(self):
        self.assertEquals(_common_cmp(1, 0), 1)
        self.assertEquals(_common_cmp(0, 1), -1)
        self.assertEquals(_common_cmp(1, 1), 0)
        self.assertEquals(_common_cmp(0, 0), 0)
