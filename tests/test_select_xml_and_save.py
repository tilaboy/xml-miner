"""unit tests to select values from xml dir or mxml"""
import os
import shutil
import tempfile
import filecmp
from unittest import TestCase
from xml_miner.miner import XMLMiner
from xml_miner.selectors import XMLSelectors
from xml_miner.data_utils import DataLoader

class XmlTestCases(TestCase):
    """unit tests for select from xml and save to csv files"""
    def setUp(self):
        self.xmls_dir = 'tests/resource/xmls'
        self.mxml_file = 'tests/resource/simple.mxml'
        self.gold_name_file = 'tests/resource/gold/xml_name.tsv'
        self.gold_name_address_file = 'tests/resource/gold/xml_name_address.tsv'
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """remove the temp dir when test finished"""
        shutil.rmtree(self.test_dir)

    def test_xml_select_from_folder(self):
        """select all values from all xmls from a given director"""
        data_generator = DataLoader.load_from_dir(self.xmls_dir)
        eval_filename = os.path.join(self.test_dir, 'from_dir.csv')
        selectors = XMLSelectors(["name"])
        xml_miner = XMLMiner(selectors)
        xml_miner.mine(data_generator, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_name_file,
            shallow=False))


    def test_xml_select_from_mxml(self):
        """select all values from all xmls from a given mxml file"""
        data_generator = DataLoader.load_from_mxml(self.mxml_file)
        eval_filename = os.path.join(self.test_dir, 'from_mxml.csv')
        selectors = XMLSelectors(["name"])
        xml_miner = XMLMiner(selectors)
        xml_miner.mine(data_generator, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_name_file,
            shallow=False))


    def test_xml_multi_select_from_mxml(self):
        """select multiple fields from all xmls from a given mxml file"""
        data_generator = DataLoader.load_from_mxml(self.mxml_file)
        eval_filename = os.path.join(self.test_dir, 'from_mxml.csv')
        selectors = XMLSelectors(["name", "address"])
        xml_miner = XMLMiner(selectors, with_field_name=True)
        xml_miner.mine(data_generator, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_name_address_file,
            shallow=False))
