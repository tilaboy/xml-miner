"""unit tests to select values from xml files or strings"""
import os
from unittest import TestCase
from unittest import TestResult
from xml_miner.xml import TKXML
from xml_miner.selectors import XMLSelectors

class XmlTestCases(TestCase):
    """unit tests to select values from xml files or strings"""
    def setUp(self):
        self.test_file = 'tests/resource/xmls/test_02.xml'
        self.xml_obj = TKXML.from_file(self.test_file)

    def test_filename(self):
        self.assertEqual(self.xml_obj.filename, 'test02.pdf.txtorin',
            'check the filename from xml file "filename"')


    def test_working_entity(self):
        self.assertEqual(self.xml_obj.working_entity.tag, 'begin',
            'check the working level of tags')


    def test_select_first_jobtitle(self):
        selector = XMLSelectors.from_selector_string('jobtitle')
        self.assertEqual(
            selector.select_xml_fields(self.xml_obj),
            {'jobtitle':['java developer']},
            f'select the first jobtitle from file: {self.test_file}'
        )

    def test_select_whole_item(self):
        selector = XMLSelectors.from_selector_string('item')
        self.assertEqual(
            selector.select_xml_fields(self.xml_obj),
            {'item':[
                '2010-2012  New York, US, java developer',
                '''May 1997-Sept 1997: NEW ZEALAND WHEELS (New Zealand)
   Job Description: Toolmaker, making of die cast tooling (lathes, mills, spark eroders etc.)
   reason for leaving: company went into receivership'''
            ]},
            f'select items from file: {self.test_file}'
        )

    def test_select_org_place(self):
        selector = XMLSelectors.from_selector_string('experienceorgplace,experienceorg,experienceplace')
        self.assertEqual(
            selector.select_xml_fields(self.xml_obj),
            {
                'experienceorgplace':['NEW ZEALAND WHEELS (New Zealand)'],
                'experienceorg':['NEW ZEALAND WHEELS'],
                'experienceplace':['New Zealand']
            },
            f'select org and place from file: {self.test_file}'
        )
