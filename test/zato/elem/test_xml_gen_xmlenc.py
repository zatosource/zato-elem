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

class XMLGenerationXMLEnc(TestCase):
    """ Generate and compare various documents found at http://www.w3.org/TR/2002/REC-xmlenc-core-20021210/
    """
    def test_gen1(self):
        orig = """
        <EncryptedData xmlns='http://www.w3.org/2001/04/xmlenc#' Type='http://www.w3.org/2001/04/xmlenc#Element'>
            <EncryptionMethod Algorithm='http://www.w3.org/2001/04/xmlenc#tripledes-cbc'/>
            <ds:KeyInfo xmlns:ds='http://www.w3.org/2000/09/xmldsig#'>
                <ds:KeyName>John Smith</ds:KeyName>
            </ds:KeyInfo>
            <CipherData>
                <CipherValue>ABCDEF</CipherValue>
            </CipherData>
        </EncryptedData>
        """

        # Main structure + NS
        doc = xml()
        doc.ns = default_ns.xenc
        doc.ns_map += default_ns.dsig

        # Top-level
        data = doc.EncryptedData
        data._Type = 'http://www.w3.org/2001/04/xmlenc#Element'

        # Children
        data.EncryptionMethod._Algorithm = 'http://www.w3.org/2001/04/xmlenc#tripledes-cbc'
        data.dsig_KeyInfo.dsig_KeyName = 'John Smith'
        data.CipherData.CipherValue = 'ABCDEF'

        # Compare
        compare_xml(orig, doc.to_xml())

    def test_gen2(self):
        orig = """
        <?xml version='1.0'?>
         <PaymentInfo xmlns='http://example.org/paymentv2'>
           <Name>John Smith</Name>
           <CreditCard Limit='5,000' Currency='USD'>
             <Number>4019 2445 0277 5567</Number>
             <Issuer>Example Bank</Issuer>
             <Expiration>04/02</Expiration>
           </CreditCard>
         </PaymentInfo>
        """
        doc = xml()
        doc.ns = 'http://example.org/paymentv2'

        info = doc.PaymentInfo
        info.Name = 'John Smith'
        info.CreditCard._Limit = '5,000'
        info.CreditCard._Currency = 'USD'
        info.CreditCard.Number = '4019 2445 0277 5567'
        info.CreditCard.Issuer = 'Example Bank'
        info.CreditCard.Expiration = '04/02'

        # Compare
        compare_xml(orig, doc.to_xml())

    def test_gen3(self):
        orig = """
          <?xml version='1.0'?> 
          <PaymentInfo xmlns='http://example.org/paymentv2'>
            <Name>John Smith</Name>
            <CreditCard Limit='5,000' Currency='USD'>
              <EncryptedData xmlns='http://www.w3.org/2001/04/xmlenc#'
               Type='http://www.w3.org/2001/04/xmlenc#Content'>
                <CipherData>
                  <CipherValue>A23B45C56</CipherValue>
                </CipherData>
              </EncryptedData>
            </CreditCard>
          </PaymentInfo>
        """

        doc = xml()
        doc.ns = 'http://example.org/paymentv2'

        info = doc.PaymentInfo
        info.Name = 'John Smith'
        info.CreditCard._Limit = '5,000'
        info.CreditCard._Currency = 'USD'

        enc_data = info.CreditCard.EncryptedData
        enc_data.ns = default_ns.xenc
        enc_data._Type = 'http://www.w3.org/2001/04/xmlenc#Content'
        enc_data.CipherData.CipherValue = 'A23B45C56'

        # Compare
        compare_xml(orig, doc.to_xml())

    def test_gen4(self):
        orig = """
          <CipherReference URI="http://www.example.com/CipherValues.xml">
          <Transforms xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
            <ds:Transform 
             Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116">
                <ds:XPath xmlns:rep="http://www.example.org/repository">
                  self::text()[parent::rep:CipherValue[@Id="example1"]]
                </ds:XPath>
            </ds:Transform>
            <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#base64"/>
          </Transforms>
        </CipherReference>
  """

        doc = xml()
        doc.ns_map += default_ns.dsig
        doc.ns_map += {'rep':'http://www.example.org/repository'}

        cipher_ref = doc.CipherReference
        cipher_ref._URI = 'http://www.example.com/CipherValues.xml'

        transform = cipher_ref.Transforms.dsig_Transform[0]
        transform._Algorithm = 'http://www.w3.org/TR/1999/REC-xpath-19991116'
        transform.dsig_XPath = 'self::text()[parent::rep:CipherValue[@Id="example1"]]'

        cipher_ref.Transforms.dsig_Transform[1]._Algorithm = 'http://www.w3.org/2000/09/xmldsig#base64'

        # Compare
        compare_xml(orig, doc.to_xml())

    def test_gen5(self):
        orig = """
        <ReferenceList xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
            <DataReference URI="#invoice34">
                <ds:Transforms>
                    <ds:Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116">
                        <ds:XPath xmlns:xenc="http://www.w3.org/2001/04/xmlenc#">
                            self::xenc:EncryptedData[@Id="example1"]
                        </ds:XPath>
                    </ds:Transform>
                </ds:Transforms>
            </DataReference>
        </ReferenceList>
        """

        doc = xml()
        doc.ns_map += default_ns.dsig, default_ns.xenc

        doc.ReferenceList.DataReference._URI = '#invoice34'
        transforms = doc.ReferenceList.DataReference.dsig_Transforms
        transforms.dsig_Transform._Algorithm = 'http://www.w3.org/TR/1999/REC-xpath-19991116'
        transforms.dsig_Transform.dsig_XPath = 'self::xenc:EncryptedData[@Id="example1"]'

        # Compare
        compare_xml(orig, doc.to_xml())

    def test_gen6(self):
        orig = """
        <root>
          <element name='EncryptedKey' type='xenc:EncryptedKeyType'/>
          <complexType name='EncryptedKeyType'>
            <complexContent>
              <extension base='xenc:EncryptedType'>
                <sequence>
                  <element ref='xenc:ReferenceList' minOccurs='0'/>
                  <element name='CarriedKeyName' type='string' minOccurs='0'/>
                </sequence>
                <attribute name='Recipient' type='string' use='optional'/>
              </extension>
            </complexContent>
          </complexType>
        </root>
          """

        doc = xml()
        doc.root.element._name = 'EncryptedKey'
        doc.root.element._type = 'xenc:EncryptedKeyType'
        doc.root.complexType._name = 'EncryptedKeyType'

        ext = doc.root.complexType.complexContent.extension
        ext._base = 'xenc:EncryptedType'

        ext.sequence.element[0]._ref = 'xenc:ReferenceList'
        ext.sequence.element[0]._minOccurs = '0'

        ext.sequence.element[1]._name = 'CarriedKeyName'
        ext.sequence.element[1]._type = 'string'
        ext.sequence.element[1]._minOccurs = '0'

        ext.attribute._name='Recipient'
        ext.attribute._type='string'
        ext.attribute._use='optional'

        # Compare
        compare_xml(orig, doc.to_xml())
