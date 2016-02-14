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

class XMLGenerationNS(TestCase):
    """ Generate and compare documents found at http://www.w3.org/TR/2009/REC-xml-names-20091208/
    """
    def test_gen1(self):
        orig = """
        <x xmlns:edi='http://ecommerce.example.org/schema'>
        </x>
        """
        doc = xml()
        doc.ns_map += {'edi':'http://ecommerce.example.org/schema'}
        doc.x = ''

        compare_xml(orig, doc.to_xml())

    def test_gen2(self):
        orig = """
        <edi:price xmlns:edi='http://ecommerce.example.org/schema' units='Euro'>32.18</edi:price>
        """
        doc = xml()
        doc.ns_map += {'edi':'http://ecommerce.example.org/schema'}
        doc.edi_price = '32.18'
        doc.edi_price._units = 'Euro'

        compare_xml(orig, doc.to_xml())

    def test_gen3(self):
        orig = """
        <html:html xmlns:html="http://www.w3.org/1999/xhtml">
           <html:head>
              <html:title>Frobnostication</html:title>
           </html:head>
           <html:body>
              <html:p>
                 Moved to
                 <html:a href="http://frob.example.com">here.</html:a>
              </html:p>
           </html:body>
        </html:html>
        """
        doc = xml()
        doc.ns = default_ns.html

        html = doc.html
        html.head.title = 'Frobnostication'
        html.body.p = 'Moved to'
        html.body.p.a = 'here.'
        html.body.p.a._href = 'http://frob.example.com'

        compare_xml(orig, doc.to_xml())

    def test_gen4(self):
        orig = """
        <root>
          <bk:book xmlns:bk='urn:loc.gov:books' xmlns:isbn='urn:ISBN:0-395-36341-6'>
            <bk:title>Cheaper by the Dozen</bk:title>
            <isbn:number>1568491379</isbn:number>
          </bk:book>
        </root>
        """
        doc = xml()
        doc.ns_map += {'bk':'urn:loc.gov:books', 'isbn':'urn:ISBN:0-395-36341-6'}

        doc.root.bk_book.bk_title = 'Cheaper by the Dozen'
        doc.root.bk_book.isbn_number = '1568491379'

        compare_xml(orig, doc.to_xml())

    def test_gen5(self):
        orig = """
        <book xmlns='urn:loc.gov:books' xmlns:isbn='urn:ISBN:0-395-36341-6'>
            <title>Cheaper by the Dozen</title>
            <isbn:number>1568491379</isbn:number>
            <notes>
              <p xmlns='http://www.w3.org/1999/xhtml'>
              </p>
            </notes>
        </book>
        """
        doc = xml()
        doc.ns = 'urn:loc.gov:books'
        doc.ns_map += {'isbn':'urn:ISBN:0-395-36341-6'}, default_ns.html

        doc.book.title = 'Cheaper by the Dozen'
        doc.book.isbn_number = '1568491379'
        doc.book.notes.html_p = ''

        compare_xml(orig, doc.to_xml())

    def test_gen6(self):
        orig = """
        <Beers>
          <table xmlns='http://www.w3.org/1999/xhtml'>
           <th><td>Name</td><td>Origin</td><td>Description</td></th>
           <tr>
             <td><brandName xmlns="">Huntsman</brandName></td>
             <td><origin xmlns="">Bath, UK</origin></td>
             <td>
               <details xmlns=""><class>Bitter</class><hop>Fuggles</hop>
                 <pro>Wonderful hop, light alcohol, good summer beer</pro>
                 <con>Fragile; excessive variance pub to pub</con>
                 </details>
                </td>
              </tr>
            </table>
          </Beers>
        """
        doc = xml()

        table = doc.Beers.table
        table.ns = default_ns.html

        table.th.td[0] = 'Name'
        table.th.td[1] = 'Origin'
        table.th.td[2] = 'Description'

        table.tr.td[0].brandName.ns = ''
        table.tr.td[0].brandName = 'Huntsman'

        table.tr.td[1].origin.ns = ''
        table.tr.td[1].origin = 'Bath, UK'

        table.tr.td[2].details.ns = ''
        table.tr.td[2].details['class'] = 'Bitter'
        table.tr.td[2].details.hop = 'Fuggles'
        table.tr.td[2].details.pro = 'Wonderful hop, light alcohol, good summer beer'
        table.tr.td[2].details.con = 'Fragile; excessive variance pub to pub'

        compare_xml(orig, doc.to_xml())

    def test_gen7(self):
        orig = """
        <x xmlns:n1="example.com" xmlns="example.com">
          <good a="1" b="2" />
          <good a="1" n1:a="2" />
        </x>
        """
        doc = xml()
        doc.ns = 'example.com'
        doc.ns_map += {'n1':'example.com'}

        doc.x.good[0]._a = '1'
        doc.x.good[0]._b = '2'

        doc.x.good[1]._a = '1'
        doc.x.good[1]._n1_a = '2'

        compare_xml(orig, doc.to_xml())

    def test_gen_default_ns_elem(self):
        orig = """
        <root xmlns="example.com">
          <x:a xmlns:x="example.com/x">
            <b>123</b>
          </x:a>
        </root>
        """
        doc = xml()
        doc.root.ns = 'example.com'
        doc.root.ns_map += {'x':'example.com/x'}
        doc.root.x_a.b = '123'

        compare_xml(orig, doc.to_xml())

    def test_gen_default_ns_attr(self):
        orig = """
        <root xmlns="example.com">
          <x:a xmlns:x="example.com/x">
            <b foo="bar">123</b>
          </x:a>
        </root>
        """
        doc = xml()
        doc.root.ns = 'example.com'
        doc.root.ns_map += {'x':'example.com/x'}
        doc.root.x_a.b = '123'
        doc.root.x_a.b._foo = 'bar'

        compare_xml(orig, doc.to_xml())

    def test_gen_set_already_existing_ns(self):
        orig = """
            <root xmlns="example.com">
              <x:a xmlns:x="example.com/x">
                <b>123</b>
              </x:a>
            </root>
            """
        doc = xml()
        doc.root.ns = 'example.com'
        doc.root.ns_map += {'x':'example.com/x'}
        doc.root.x_a.b = '123'
        doc.root.x_a.ns = 'example.com/x' # Set explicitely and expected to reuse prefix defined in doc.root.ns_map

        compare_xml(orig, doc.to_xml())
