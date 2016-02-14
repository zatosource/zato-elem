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

class XMLGenerationXInclude(TestCase):
    """ Generate and compare documents found at http://www.w3.org/TR/2006/REC-xinclude-20061115/
    """
    def test_gen1(self):
        orig = """
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xi="http://www.w3.org/2001/XInclude"
            targetNamespace="http://www.w3.org/2001/XInclude" finalDefault="extension">

          <xs:element name="include" type="xi:includeType" />

          <xs:complexType name="includeType" mixed="true">
            <xs:choice minOccurs='0' maxOccurs='unbounded' >
              <xs:element ref='xi:fallback' />
              <xs:any namespace='##other' processContents='lax' />
              <xs:any namespace='##local' processContents='lax' />
            </xs:choice>
            <xs:attribute name="href" use="optional" type="xs:anyURI"/>
            <xs:attribute name="parse" use="optional" default="xml" type="xi:parseType" />
            <xs:attribute name="xpointer" use="optional" type="xs:string"/>
            <xs:attribute name="encoding" use="optional" type="xs:string"/>
            <xs:attribute name="accept" use="optional" type="xs:string"/>
            <xs:attribute name="accept-language" use="optional" type="xs:string"/>
            <xs:anyAttribute namespace="##other" processContents="lax"/>
          </xs:complexType>

          <xs:simpleType name="parseType">
            <xs:restriction base="xs:token">
              <xs:enumeration value="xml"/>
              <xs:enumeration value="text"/>
            </xs:restriction>
          </xs:simpleType>

          <xs:element name="fallback" type="xi:fallbackType" />

        </xs:schema>
        """
        doc = xml()
        doc.ns_map += default_ns.xs, default_ns.xi

        doc.xs_schema._targetNamespace = 'http://www.w3.org/2001/XInclude'
        doc.xs_schema._finalDefault = 'extension'

        doc.xs_schema.xs_element._name = 'include'
        doc.xs_schema.xs_element._type = 'xi:includeType'

        complex_type = doc.xs_schema.xs_complexType
        complex_type._name = 'includeType'
        complex_type._mixed = 'true'

        complex_type.xs_choice._minOccurs = '0'
        complex_type.xs_choice._maxOccurs = 'unbounded'
        complex_type.xs_choice.xs_element._ref = 'xi:fallback'
        complex_type.xs_choice.xs_any[0]._namespace = '##other'
        complex_type.xs_choice.xs_any[0]._processContents = 'lax'
        complex_type.xs_choice.xs_any[1]._namespace = '##local'
        complex_type.xs_choice.xs_any[1]._processContents = 'lax'

        attr0 = complex_type.xs_attribute[0]
        attr0._name = 'href'
        attr0._use = 'optional'
        attr0._type = 'xs:anyURI'

        attr1 = complex_type.xs_attribute[1]
        attr1._name = 'parse'
        attr1._use = 'optional'
        attr1._default = 'xml'
        attr1._type = 'xi:parseType'

        attr2 = complex_type.xs_attribute[2]
        attr2._name = 'xpointer'
        attr2._use = 'optional'
        attr2._type = 'xs:string'

        attr3 = complex_type.xs_attribute[3]
        attr3._name = 'encoding'
        attr3._use = 'optional'
        attr3._type = 'xs:string'

        attr4 = complex_type.xs_attribute[4]
        attr4._name = 'accept'
        attr4._use = 'optional'
        attr4._type = 'xs:string'

        attr5 = complex_type.xs_attribute[5]
        attr5._name = 'accept-language'
        attr5._use = 'optional'
        attr5._type = 'xs:string'

        complex_type.xs_anyAttribute._namespace = '##other'
        complex_type.xs_anyAttribute._processContents = 'lax'

        simple_type = doc.xs_schema.xs_simpleType
        simple_type._name = 'parseType'
        simple_type.xs_restriction._base = 'xs:token'
        simple_type.xs_restriction.xs_enumeration[0]._value = 'xml'
        simple_type.xs_restriction.xs_enumeration[1]._value = 'text'

        # TODO: This won't work until .addsibling is added
        # doc.xs_schema.xs_element._name = 'fallback'
        # doc.xs_schema.xs_element._type = 'xi:fallbackType'
        # compare_xml(orig, doc.to_xml())

        # TODO: for flake8
        todo = orig
        todo = compare_xml
        todo = todo
