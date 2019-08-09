"""unit tests to select values from xml files or strings"""
import os
from unittest import TestCase
from unittest import TestResult
from xml_miner.selectors.selector_utils import valid_field_name, selector_attribute
from xml_miner.selectors.selector_utils import SELECTOR_TYPE, TRXML_SELECTOR_TYPE
from xml_miner.selectors import TRXMLSelectors, XMLSelectors

class XMLUtilsTestCases(TestCase):
    """unit tests to select values from xml files or strings"""

    def test_field_name_validation(self):
        self.assertEqual(valid_field_name('foo'), True)
        self.assertEqual(valid_field_name('foo.bar'), True)
        self.assertEqual(valid_field_name('foo.0.bar'), True)
        self.assertEqual(valid_field_name('foo.*.bar'), True)
        try:
            valid_field_name('*')
            raise ValueError("should not reach here")
        except Exception as err:
            self.assertTrue(err.__str__()=="tag_name '*' needs at least one alphabet char")

    def test_selector_type_attribute(self):
        selectors = XMLSelectors.from_selector_string('foo,bar')
        self.assertEqual(
            selector_attribute(selectors.selectors, 'selector_type'),
            SELECTOR_TYPE['XML']
        )

        try:
            selectors = XMLSelectors.from_selector_string('foo.0.foo,bar.0.bar')
            raise ValueError("should not reach here")
        except Exception as err:
            self.assertTrue(err.__str__().startswith('expect xml selector'))


        selectors = TRXMLSelectors.from_selector_string('foo.0.foo,bar.0.bar')
        self.assertEqual(
            selector_attribute(selectors.selectors, 'selector_type'),
            SELECTOR_TYPE['TRXML']
        )

    def test_trxml_selector_type_attribute(self):
        selectors = TRXMLSelectors.from_selector_string('foo.0.foo,bar.0.bar')
        self.assertEqual(
            selector_attribute(selectors.selectors, 'trxml_selector_type'),
            TRXML_SELECTOR_TYPE['SINGLETON']
        )

        selectors = TRXMLSelectors.from_selector_string('foo.*.foo,foo.*.bar')
        self.assertEqual(
            selector_attribute(selectors.selectors, 'trxml_selector_type'),
            TRXML_SELECTOR_TYPE['MULTIPLE']
        )

        try:
            selectors = TRXMLSelectors.from_selector_string('foo.0.foo,foo.*.bar')
            raise ValueError("should not reach here")
        except Exception as err:
            self.assertTrue(err.__str__().startswith("selector 'foo.*.bar'"))


    def test_same_itemgroup(self):
        selectors = TRXMLSelectors.from_selector_string('foo.*.foo,foo.*.bar')
        self.assertEqual(
            selector_attribute(selectors.selectors, 'same_itemgroup'),
            'foo'
        )

        try:
            selectors = TRXMLSelectors.from_selector_string('foo.*.foo,bar.*.bar')
            raise ValueError("should not reach here")
        except Exception as err:
            self.assertTrue(err.__str__().startswith("selector 'bar.*.bar'"))
