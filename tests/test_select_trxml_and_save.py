"""unit tests to select values from xml dir or mxml"""
import os
import shutil
import tempfile
import filecmp
from unittest import TestCase
from xml_miner.miner import TRXMLMiner
from xml_miner.selectors import TRXMLSelectors
from xml_miner.data_utils import DataLoader

class TrxmlMinerTestCases(TestCase):
    """unit tests for select from trxml and save to csv files"""
    def setUp(self):
        self.trxmls_dir = 'tests/resource/trxmls'
        self.mtrxml_file = 'tests/resource/simple.mtrxml'
        self.gold_name_file = 'tests/resource/gold/trxml_name.tsv'
        self.gold_name_address_file = 'tests/resource/gold/trxml_name_address.tsv'
        self.gold_exp_file = 'tests/resource/gold/trxml_exp.tsv'
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """remove the temp dir when test finished"""
        shutil.rmtree(self.test_dir)

    def test_trxml_select_from_folder(self):
        """select all values from all trxmls from a given directory"""
        eval_filename = os.path.join(self.test_dir, 'from_dir.csv')
        trxml_miner = TRXMLMiner("name.0.name")
        trxml_miner.mine_and_save(self.trxmls_dir, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_name_file,
            shallow=False))

    def test_trxml_select_from_mxml(self):
        """select all values from all xmls from a given mtrxml file"""
        eval_filename = os.path.join(self.test_dir, 'from_mxml.csv')
        trxml_miner = TRXMLMiner("name.0.name")
        trxml_miner.mine_and_save(self.mtrxml_file, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_name_file,
            shallow=False))

    def test_multi_selectors_singleton(self):
        """select all values from all xmls from a given mtrxml file"""
        eval_filename = os.path.join(self.test_dir, 'from_mxml.csv')
        trxml_miner = TRXMLMiner("name.0.name,address.0.address")
        trxml_miner.mine_and_save(self.mtrxml_file, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_name_address_file,
            shallow=False))


    def test_multi_selectors_multi_items(self):
        """select all values from all xmls from a given mtrxml file"""
        eval_filename = os.path.join(self.test_dir, 'from_mxml.csv')
        trxml_miner = TRXMLMiner("experienceitem.*.experience,experienceitem.*.experienceorgplace")
        trxml_miner.mine_and_save(self.mtrxml_file, eval_filename)
        self.assertTrue(filecmp.cmp(
            eval_filename,
            self.gold_exp_file,
            shallow=False))
