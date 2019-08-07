"""unit tests to select values from xml files or strings"""
import os
from unittest import TestCase
from unittest import TestResult
from xml_miner.selectors import XMLSelectors, TRXMLSelectors
from xml_miner.selectors.trxml_selector import TRXMLSelector
from xml_miner.xml import TKXML, TKTRXML

class SelectorsXMLTestCases(TestCase):
    """unit tests to select values from xml files or strings"""
    def setUp(self):
        self.xml_obj = TKXML.from_file('tests/resource/xmls/test_03.xml')

    def test_select_name(self):
        selectors = XMLSelectors.from_selector_string('name')
        selected = selectors.select_xml_fields(self.xml_obj)
        self.assertEqual(selected, {'name':['first name', \
                        'second name', \
                        'third\n          name', \
                        "fourth 'name'"]})

    def test_select_name_address(self):
        selectors = XMLSelectors.from_selector_string('name,address')
        selected = selectors.select_xml_fields(self.xml_obj)
        self.assertEqual(selected,
                        {'name':['first name', \
                                 'second name', \
                                 'third\n          name', \
                                 "fourth 'name'"],
                         'address':['1021AB Amsterdam', 'The Netherlands']
                        })

    def test_select_nonexist(self):
        selectors = XMLSelectors.from_selector_string('unknown')
        selected = selectors.select_xml_fields(self.xml_obj)
        self.assertEqual(selected, {'unknown':[]})


class SelectorsTRXMLTestCases(TestCase):
    """unit tests to select values from xml files or strings"""
    def setUp(self):
        self.trxml_obj = TKTRXML.from_file(
            'tests/resource/trxmls/foo1.doc.trxml'
        )
        self.expected_name = 'Foo3 Bar3'
        self.expected_jobtitle = [
            'Global Communications officer',
            'Manager, Organisational Identity and Brand Management',
            'Senior Consultant'
        ]

    def test_select_name(self):
        selectors = TRXMLSelectors.from_selector_string('name.0.name')
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected, {'name.0.name': 'Foo1 Bar1, BA.'})


    def test_select_name_address(self):
        selectors = TRXMLSelectors.from_selector_string('name.0.name,address.0.address')
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected,
                        {
                            'name.0.name': 'Foo1 Bar1, BA.',
                            'address.0.address': '11111 Some Street, Calgary, Canada'
                        })

    def test_select_all_jobtitles(self):
        selectors = TRXMLSelectors.from_selector_string('experienceitem.*.experience')
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected,
                        {'0': {'experienceitem.*.experience': 'Supervisor Human Resources'},
                         '1': {'experienceitem.*.experience': 'Consultant Logistics'}}
                        )


    def test_select_multi_items_1(self):
        selectors = TRXMLSelectors.from_selector_string(
            'experienceitem.*.experience,experienceitem.*.experiencedate,experienceitem.*.experienceorgplace'
        )
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected,
                        {'0': {'experienceitem.*.experience': 'Supervisor Human Resources',
                               'experienceitem.*.experiencedate': 'June 2007 - June 2010',
                               'experienceitem.*.experienceorgplace': 'Company ABC, Mississauga, ON'},
                         '1': {'experienceitem.*.experience': 'Consultant Logistics',
                               'experienceitem.*.experiencedate': 'May 2005 - June 2007',
                               'experienceitem.*.experienceorgplace': 'Company DEF, Mississauga, ON'}}
                        )

    def test_select_multi_items_2(self):
        selectors = TRXMLSelectors.from_itemgroup_and_fields(
            'experienceitem', 'experience,experiencedate,experienceorgplace'
        )
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected,
                        {'0': {'experienceitem.*.experience': 'Supervisor Human Resources',
                               'experienceitem.*.experiencedate': 'June 2007 - June 2010',
                               'experienceitem.*.experienceorgplace': 'Company ABC, Mississauga, ON'},
                         '1': {'experienceitem.*.experience': 'Consultant Logistics',
                               'experienceitem.*.experiencedate': 'May 2005 - June 2007',
                               'experienceitem.*.experienceorgplace': 'Company DEF, Mississauga, ON'}}
                        )

    def test_select_nonexist(self):
        selectors = TRXMLSelectors.from_selector_string('unknown.0.unknown')
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected, {'unknown.0.unknown': ''})

    def test_select_not_all_exist(self):
        selectors = TRXMLSelectors.from_selector_string('name.0.name,unknown.0.unknown')
        selected = selectors.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected,
                        {
                            'name.0.name': 'Foo1 Bar1, BA.',
                            'unknown.0.unknown': ''
                        })

    def test_select_not_all_items(self):
        selectors_1 = TRXMLSelectors.from_itemgroup_and_fields(
            'experienceitem', 'experience,experiencedate,experienceorgplace,extra_1'
        )
        selected_1 = selectors_1.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected_1,
                        {'0': {'experienceitem.*.experience': 'Supervisor Human Resources',
                               'experienceitem.*.experiencedate': 'June 2007 - June 2010',
                               'experienceitem.*.experienceorgplace': 'Company ABC, Mississauga, ON',
                               'experienceitem.*.extra_1': 'foo, bar'},
                         '1': {'experienceitem.*.experience': 'Consultant Logistics',
                               'experienceitem.*.experiencedate': 'May 2005 - June 2007',
                               'experienceitem.*.experienceorgplace': 'Company DEF, Mississauga, ON',
                               'experienceitem.*.extra_1': ''}}
                        )



        selectors_2 = TRXMLSelectors.from_itemgroup_and_fields(
            'experienceitem', 'experience,experiencedate,experienceorgplace,extra_3'
        )
        selected_2 = selectors_2.select_trxml_fields(self.trxml_obj)
        self.assertEqual(selected_2,
                        {'0': {'experienceitem.*.experience': 'Supervisor Human Resources',
                               'experienceitem.*.experiencedate': 'June 2007 - June 2010',
                               'experienceitem.*.experienceorgplace': 'Company ABC, Mississauga, ON',
                               'experienceitem.*.extra_3': ''},
                         '1': {'experienceitem.*.experience': 'Consultant Logistics',
                               'experienceitem.*.experiencedate': 'May 2005 - June 2007',
                               'experienceitem.*.experienceorgplace': 'Company DEF, Mississauga, ON',
                               'experienceitem.*.extra_3': ''}}
                        )

class SelectorTRXMLTestCases(TestCase):
    """unit tests to select values from xml files or strings"""
    def test_parse_trxml_selector(self):
        cases = [
            {
                'input':'foo.4.bar',
                'itemgroup':'foo',
                'index': '4',
                'field': 'bar'
            },
            {
                'input':'foo.bar',
                'itemgroup':'foo',
                'index': '*',
                'field': 'bar'
            },
            {
                'input':'foo.*.bar',
                'itemgroup':'foo',
                'index': '*',
                'field': 'bar'
            },
        ]

        for case in cases:
            selector = TRXMLSelector(case['input'])
            itemgroup, index, field = selector.parse_trxml_selector()
            self.assertEqual(itemgroup, case['itemgroup'])
            self.assertEqual(index, case['index'])
            self.assertEqual(field, case['field'])
