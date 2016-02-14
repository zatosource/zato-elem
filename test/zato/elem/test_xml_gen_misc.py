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

class XMLGenerationMisc(TestCase):
    """ Miscellaneous XML generation tests.
    """
    def test_gen1(self):

        orig = """
        <ns0:Envelope xmlns:ns0="http://www.w3.org/2003/05/soap-envelope"
        xmlns:rem="http://remoting.example.com" xmlns:wsa="http://www.w3.org/2005/08/addressing">
           <ns0:Header>
              <wsa:Action ns0:mustUnderstand="1" ns0:type="2">urn:hl7-org:v3:MCCI_IN000002UV01</wsa:Action>
              <wsa:MessageID>uuid:123</wsa:MessageID>
              <wsa:ReplyTo>
                 <wsa:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa:Address>
              </wsa:ReplyTo>
           </ns0:Header>
           <ns0:Body>
              <rem:usrOrgRoleLogin>
                 <arg0 rem:keep_alive="true">
                    <user>my-user</user>
                    <pwd>my-password</pwd>
                    <role>my-role</role>
                    <org>my-org</org>
                    <rem:access rem:type="0">
                       no
                       <access>000</access>
                    </rem:access>
                    <rem:access rem:type="1">
                       yes
                       <access>111</access>
                    </rem:access>
                 </arg0>
              </rem:usrOrgRoleLogin>
           </ns0:Body>
        </ns0:Envelope>
        """
        doc = xml()
        doc.ns_map += default_ns.s12, default_ns.wsa, {'rem':'http://remoting.example.com'}

        header = doc.s12_Envelope.s12_Header
        header.wsa_Action = 'urn:hl7-org:v3:MCCI_IN000002UV01'
        header.wsa_Action._s12_mustUnderstand = '1'
        header.wsa_Action._s12_type = '2'
        header.wsa_MessageID = 'uuid:123'
        header.wsa_ReplyTo.wsa_Address = 'http://www.w3.org/2005/08/addressing/anonymous'

        arg0 = doc.s12_Envelope.s12_Body.rem_usrOrgRoleLogin.arg0
        arg0.user = 'my-user'
        arg0._rem_keep_alive = 'true'
        arg0.pwd = 'my-password'
        arg0.role = 'my-role'
        arg0.org = 'my-org'

        arg0.rem_access[0] = 'no'
        arg0.rem_access[0]._rem_type = '0'
        arg0.rem_access[0].access = '000'

        arg0.rem_access[1] = 'yes'
        arg0.rem_access[1]._rem_type = '1'
        arg0.rem_access[1].access = '111'

        compare_xml(orig, doc.to_xml())

    def test_gen_getitem1(self):
        orig = """
        <a>
          <b>
            <c>ddd</c>
          </b>
        </a>
        """
        doc1 = xml()
        doc1.a.b.c = 'ddd'

        doc2 = xml()
        doc2['a']['b']['c'] = 'ddd'

        doc3 = xml()
        doc3.a['b']['c'] = 'ddd'

        doc4 = xml()
        doc4.a.b['c'] = 'ddd'

        doc5 = xml()
        doc5['a'].b['c'] = 'ddd'

        doc6 = xml()
        doc6['a'].b.c = 'ddd'

        doc7 = xml()
        doc7['a']['b'].c = 'ddd'

        compare_xml(orig, doc1.to_xml())
        compare_xml(orig, doc2.to_xml())
        compare_xml(orig, doc3.to_xml())
        compare_xml(orig, doc4.to_xml())
        compare_xml(orig, doc5.to_xml())
        compare_xml(orig, doc6.to_xml())
        compare_xml(orig, doc7.to_xml())

    def test_gen_getitem2(self):
        orig = """
        <a xmlns="example.com">
          <b xmlns="example.com/2">
            <c>ddd</c>
          </b>
        </a>
        """
        doc1 = xml()
        doc1.a.ns = 'example.com'
        doc1.a.b.ns = 'example.com/2'
        doc1.a.b.c = 'ddd'

        doc2 = xml()
        doc2['a'].ns = 'example.com'
        doc2.a['b'].ns = 'example.com/2'
        doc2.a.b['c'] = 'ddd'

        doc3 = xml()
        doc3['a'].ns = 'example.com'
        doc3['a']['b'].ns = 'example.com/2'
        doc3['a'].b['c'] = 'ddd'

        compare_xml(orig, doc1.to_xml())
        compare_xml(orig, doc2.to_xml())
        compare_xml(orig, doc3.to_xml())

    def test_gen_getitem3(self):
        orig = """
        <a xmlns:ns0="example.com">
          <b xmlns="example.com/2">
            <ns0:c>ddd</ns0:c>
          </b>
        </a>
        """
        doc1 = xml()
        doc1.ns_map += {'ns0':'example.com'}
        doc1.a.b.ns = 'example.com/2'
        doc1.a.b.ns0_c = 'ddd'

        doc2 = xml()
        doc2.ns_map += {'ns0':'example.com'}
        doc2['a'].b.ns = 'example.com/2'
        doc2['a']['b'].ns0_c = 'ddd'

        doc3 = xml()
        doc3.ns_map += {'ns0':'example.com'}
        doc3['a'].b.ns = 'example.com/2'
        doc3['a']['b']['ns0_c'] = 'ddd'

        doc4 = xml()
        doc4.ns_map += {'ns0':'example.com'}
        doc4['a'].b.ns = 'example.com/2'
        doc4['a'].b['ns0_c'] = 'ddd'

        doc5 = xml()
        doc5['a'].ns_map += {'ns0':'example.com'}
        doc5['a'].b.ns = 'example.com/2'
        doc5['a'].b['ns0_c'] = 'ddd'

        doc6 = xml()
        doc6['a'].ns_map += {'ns0':'example.com'}
        doc6['a']['b'].ns = 'example.com/2'
        doc6['a'].b['ns0_c'] = 'ddd'

        compare_xml(orig, doc1.to_xml())
        compare_xml(orig, doc2.to_xml())
        compare_xml(orig, doc3.to_xml())
        compare_xml(orig, doc4.to_xml())
        compare_xml(orig, doc5.to_xml())
        compare_xml(orig, doc6.to_xml())

    def test_gen_attr1(self):
        orig = """
        <a aa="1">
          <b bb="2" bbb="22">
            <c cc="3" ccc="33">ddd</c>
          </b>
        </a>
        """
        doc = xml()
        doc.a._aa = '1'
        doc.a.b._bb = '2'
        doc.a.b._bbb = '22'
        doc.a.b.c._cc = '3'
        doc.a.b.c._ccc = '33'
        doc.a.b.c = 'ddd'

        compare_xml(orig, doc.to_xml())

    def test_gen_attr2(self):
        orig = """
        <a aa="1" xmlns="example.com">
          <b bb="2" bbb="22" xmlns="example.com/2">
            <c cc="3" ccc="33">ddd</c>
          </b>
        </a>
        """
        doc1 = xml()
        doc1.ns = 'example.com'
        doc1.a._aa = '1'
        doc1.a.b.ns = 'example.com/2'
        doc1.a.b._bb = '2'
        doc1.a.b._bbb = '22'
        doc1.a.b.c._cc = '3'
        doc1.a.b.c._ccc = '33'
        doc1.a.b.c = 'ddd'

        doc2 = xml()
        doc2.a.ns = 'example.com'
        doc2.a._aa = '1'
        doc2.a.b.ns = 'example.com/2'
        doc2.a.b._bb = '2'
        doc2.a.b._bbb = '22'
        doc2.a.b.c._cc = '3'
        doc2.a.b.c._ccc = '33'
        doc2.a.b.c = 'ddd'

        compare_xml(orig, doc1.to_xml())
        compare_xml(orig, doc2.to_xml())

    def test_gen_attr3(self):
        orig = """
            <a xmlns:ns0="example.com" a="a" aa="aa" ns0:a="ns0a" ns0:aa="ns0aa">
              <b xmlns="example.com/2" a="a" aa="aa" ns0:a="ns0a" ns0:aa="ns0aa" b="b" bb="bb" ns0:b="ns0b" ns0:bb="ns0bb">
                <ns0:c xmlns:ns1="example.com/foo" c="c" cc="cc" ns0:c="ns0c" ns0:cc="ns0cc" ns1:c="ns1c">ddd</ns0:c>
              </b>
            </a>
            """

        doc = xml()
        doc.ns_map += {'ns0':'example.com'}

        doc.a._a = 'a'
        doc.a._aa = 'aa'
        doc.a._ns0_a = 'ns0a'
        doc.a._ns0_aa = 'ns0aa'

        doc.a.b.ns = 'example.com/2'
        doc.a.b._a = 'a'
        doc.a.b._aa = 'aa'
        doc.a.b._ns0_a = 'ns0a'
        doc.a.b._ns0_aa = 'ns0aa'
        doc.a.b._b = 'b'
        doc.a.b._bb = 'bb'
        doc.a.b._ns0_b = 'ns0b'
        doc.a.b._ns0_bb = 'ns0bb'

        doc.a.b.ns0_c.ns_map += {'ns1':'example.com/foo'}
        doc.a.b.ns0_c._c = 'c'
        doc.a.b.ns0_c._cc = 'cc'
        doc.a.b.ns0_c._ns0_c = 'ns0c'
        doc.a.b.ns0_c._ns0_cc = 'ns0cc'
        doc.a.b.ns0_c._ns1_c = 'ns1c'
        doc.a.b.ns0_c = 'ddd'

        compare_xml(orig, doc.to_xml())
