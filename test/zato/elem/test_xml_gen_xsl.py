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

class XMLGenerationXSL(TestCase):
    """ Generate and compare documents found at http://www.w3.org/TR/2006/REC-xsl11-20061205/
    """
    def test_gen1(self):
        orig = """
        <fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
           <fo:layout-master-set>
              <fo:simple-page-master master-name="all-pages">
                 <fo:region-body region-name="xsl-region-body" margin="0.75in" writing-mode="tb-rl"/>
                 <fo:region-before region-name="xsl-region-before" extent="0.75in"/>
              </fo:simple-page-master>
              <fo:page-sequence-master master-name="default-sequence">
                 <fo:repeatable-page-master-reference master-reference="all-pages"/>
              </fo:page-sequence-master>
           </fo:layout-master-set>
           <fo:page-sequence master-name="default-sequence">
              <fo:flow flow-name="xsl-region-body">
                 <fo:block>[Content in a language which allows either horizontal or vertical formatting]</fo:block>
              </fo:flow>
           </fo:page-sequence>
        </fo:root>
        """
        doc = xml()
        doc.ns = default_ns.fo

        simple_page_master = doc.root['layout-master-set']['simple-page-master']
        simple_page_master['#master-name'] = 'all-pages'

        simple_page_master['region-body']['#region-name'] = 'xsl-region-body'
        simple_page_master['region-body']['#margin'] = '0.75in'
        simple_page_master['region-body']['#writing-mode'] = 'tb-rl'

        simple_page_master['region-before']['#region-name'] = 'xsl-region-before'
        simple_page_master['region-before']['#extent'] = '0.75in'

        page_sequence_master = doc.root['layout-master-set']['page-sequence-master']
        page_sequence_master['#master-name'] = 'default-sequence'
        page_sequence_master['repeatable-page-master-reference']['#master-reference'] = 'all-pages'

        page_sequence = doc.root['page-sequence']
        page_sequence['#master-name'] = 'default-sequence'
        page_sequence.flow['#flow-name'] = 'xsl-region-body'
        page_sequence.flow.block = '[Content in a language which allows either horizontal or vertical formatting]'

        compare_xml(orig, doc.to_xml())

    def test_gen2(self):
        orig = """
        <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">

        <xsl:template match="chapter">
          <fo:block break-before="page">
            <xsl:apply-templates/>
          </fo:block>
        </xsl:template>

        <xsl:template match="chapter/title">
          <fo:block text-align="center" space-after="8pt" space-before="16pt" space-after.precedence="3">
            <xsl:apply-templates/>
          </fo:block>
        </xsl:template>
        
        <xsl:template match="section">
          <xsl:apply-templates/>
        </xsl:template>

        <xsl:template match="section/title">
          <fo:block text-align="center" space-after="6pt" space-before="12pt" space-before.precedence="0"
              space-after.precedence="3">
            <xsl:apply-templates/>
          </fo:block>
        </xsl:template>

        <xsl:template match="paragraph[1]" priority="1">
          <fo:block text-indent="0pc" space-after="7pt" space-before.minimum="6pt" space-before.optimum="8pt"
              space-before.maximum="10pt">
            <xsl:apply-templates/>
          </fo:block>
        </xsl:template>

        <xsl:template match="paragraph">
          <fo:block text-indent="2pc" space-after="7pt" space-before.minimum="6pt" space-before.optimum="8pt"
              space-before.maximum="10pt">
            <xsl:apply-templates/>
          </fo:block>
        </xsl:template>

        </xsl:stylesheet>
        """
        doc = xml()
        doc.ns_map += default_ns.xsl, default_ns.fo

        t0 = doc.xsl_stylesheet.xsl_template[0]
        t0._match = 'chapter'
        t0.fo_block['#break-before'] = 'page'
        t0.fo_block['xsl_apply-templates'] = ''

        t1 = doc.xsl_stylesheet.xsl_template[1]
        t1._match = 'chapter/title'
        t1.fo_block['#text-align'] = 'center'
        t1.fo_block['#space-after'] = '8pt'
        t1.fo_block['#space-before'] = '16pt'
        t1.fo_block['#space-after.precedence'] = '3'
        t1.fo_block['xsl_apply-templates'] = ''

        t2 = doc.xsl_stylesheet.xsl_template[2]
        t2._match = 'section'
        t2['xsl_apply-templates'] = ''

        t3 = doc.xsl_stylesheet.xsl_template[3]
        t3._match = 'section/title'
        t3.fo_block['#text-align'] = 'center'
        t3.fo_block['#space-after'] = '6pt'
        t3.fo_block['#space-before'] = '12pt'
        t3.fo_block['#space-before.precedence'] = '0'
        t3.fo_block['#space-after.precedence'] = '3'
        t3.fo_block['xsl_apply-templates'] = ''

        t4 = doc.xsl_stylesheet.xsl_template[4]
        t4._match = 'paragraph[1]'
        t4._priority = '1'
        t4.fo_block['#text-indent'] = '0pc'
        t4.fo_block['#space-after'] = '7pt'
        t4.fo_block['#space-before.minimum'] = '6pt'
        t4.fo_block['#space-before.optimum'] = '8pt'
        t4.fo_block['#space-before.maximum'] = '10pt'
        t4.fo_block['xsl_apply-templates'] = ''

        t5 = doc.xsl_stylesheet.xsl_template[5]
        t5._match = 'paragraph'
        t5.fo_block['#text-indent'] = '2pc'
        t5.fo_block['#space-after'] = '7pt'
        t5.fo_block['#space-before.minimum'] = '6pt'
        t5.fo_block['#space-before.optimum'] = '8pt'
        t5.fo_block['#space-before.maximum'] = '10pt'
        t5.fo_block['xsl_apply-templates'] = ''

        compare_xml(orig, doc.to_xml())
