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
from zato.elem import compare_xml, default_ns, xml

# ################################################################################################################################

class XMLGenerationXML(TestCase):
    """ Generate and compare documents found at http://www.w3.org/TR/2008/REC-xml-20081126/
    """
    def test_gen1(self):
        orig = """
        <greeting>Hello, world!</greeting> 
        """

        doc = xml()
        doc.greeting = 'Hello, world!'

        compare_xml(orig, doc.to_xml())

    def test_gen2(self):
        orig = """
        <root>
          <p xml:lang="en">The quick brown fox jumps over the lazy dog.</p>
          <p xml:lang="en-GB">What colour is it?</p>
          <p xml:lang="en-US">What color is it?</p>
          <sp who="Faust" desc='leise' xml:lang="de">
            <l>Habe nun, ach! Philosophie,</l>
            <l>Juristerei, und Medizin</l>
            <l>und leider auch Theologie</l>
            <l>durchaus studiert mit heißem Bemüh'n.</l>
            </sp>
        </root>
        """

        doc = xml()
        doc.ns_map += default_ns.xml

        root = doc.root

        root.p[0]._xml_lang = 'en'
        root.p[0] = 'The quick brown fox jumps over the lazy dog.'

        root.p[1]._xml_lang = 'en-GB'
        root.p[1] = 'What colour is it?'

        root.p[2]._xml_lang = 'en-US'
        root.p[2] = 'What color is it?'

        sp = root.sp
        sp._who = 'Faust'
        sp._desc = 'leise'
        sp._xml_lang = 'de'

        sp.l[0] = 'Habe nun, ach! Philosophie,'
        sp.l[1] = 'Juristerei, und Medizin'
        sp.l[2] = 'und leider auch Theologie'
        sp.l[3] = 'durchaus studiert mit heißem Bemüh\'n.'

        compare_xml(orig, doc.to_xml())
