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
from zato.elem import default_ns
from zato.elem._common import top_level, ns_prefix_max_len

# ################################################################################################################################

class Defaults(TestCase):
    """ Test default values.
    """
    def test_constants(self):
        self.assertEquals(top_level, '_zato_toplevel')
        self.assertEquals(ns_prefix_max_len, 11)

    def test_default_ns(self):
        expected = {
            'decr': {'decr':'http://www.w3.org/2002/07/decrypt#'},
            'dsig': {'dsig':'http://www.w3.org/2000/09/xmldsig#'},
            'fo': {'fo':'http://www.w3.org/1999/XSL/Format'},
            'hl7': {'hl7':'urn:hl7-org:v3'},
            'html': {'html':'http://www.w3.org/1999/xhtml'},
            's11': {'s11':'http://schemas.xmlsoap.org/soap/envelope/'},
            's12': {'s12':'http://www.w3.org/2003/05/soap-envelope'},
            'wsa': {'wsa':'http://www.w3.org/2005/08/addressing'},
            'wsdl11': {'wsdl11':'http://schemas.xmlsoap.org/wsdl/'},
            'wsdl20': {'wsdl20':'http://www.w3.org/ns/wsdl'},
            'xenc': {'xenc':'http://www.w3.org/2001/04/xmlenc#'},
            'xi': {'xi':'http://www.w3.org/2001/XInclude'},
            'xkms': {'xkms':'http://www.w3.org/2002/03/xkms#'},
            'xml': {'xml':'http://www.w3.org/XML/1998/namespace'},
            'xop': {'xop':'http://www.w3.org/2004/08/xop/include'},
            'xs': {'xs':'http://www.w3.org/2001/XMLSchema'},
            'xsl': {'xsl': 'http://www.w3.org/1999/XSL/Transform'},
            'zato': {'zato':'https://zato.io/ns/20130518'},
        }

        given = {}

        for name in dir(default_ns):
            value = getattr(default_ns, name)
            if isinstance(value, dict):
                given[name] = value

        self.assertDictEqual(given, expected)
