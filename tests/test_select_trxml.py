"""unit tests to select values from xml files or strings"""
import os
from unittest import TestCase
from xml_miner.xml import TKTRXML
from xml_miner.selectors import TRXMLSelectors

class TrxmlTestCases(TestCase):
    """unit tests to select values from xml files or strings"""
    def setUp(self):
        self.test_file = 'tests/resource/trxmls/foo3.pdf.trxml'
        with open(self.test_file, 'r') as file:
            self.xml_string = file.read()

        self.expected_name = 'Foo3 Bar3'
        self.expected_jobtitle = [
            'Global Communications officer',
            'Manager, Organisational Identity and Brand Management',
            'Senior Consultant'
        ]


    def test_filename(self):
        """test: select filename from xml"""
        trxml_obj = TKTRXML.from_file(self.test_file)
        self.assertEqual(
            trxml_obj.filename,
            't/test-cvs/foo3.pdf',
            "from file: check filename"
        )


    def test_working_entity(self):
        trxml_obj = TKTRXML.from_file(self.test_file)
        self.assertEqual(trxml_obj.working_entity.tag, 'DocumentStructure',
            'check the working level of tags')


    def test_select_single_value(self):
        trxml_obj = TKTRXML.from_file(self.test_file)
        selectors = TRXMLSelectors(['name.0.name'])
        self.assertEqual(
            selectors.select_trxml_fields(trxml_obj)['name.0.name'],
            self.expected_name,
            "from file: simple one name"
        )

        selectors = TRXMLSelectors(['experienceitem.1.experience'])
        self.assertEqual(
            selectors.select_trxml_fields(trxml_obj)['experienceitem.1.experience'],
            self.expected_jobtitle[1],
            "from file: select second value of experience"
        )
