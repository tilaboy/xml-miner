"""XML Selectors class"""
from typing import List
from .selector_utils import selector_attribute, SELECTOR_TYPE
from .xml_selector import XMLSelector


class XMLSelectors():
    '''
    XMLSelectors:
    - array of XMLSelector class
    - method to select values from xml object
    '''

    def __init__(self, selectors: List[str]):
        self.selector_string = ",".join(selectors)
        self.selectors = [
            XMLSelector(selector_string)
            for selector_string in selectors
        ]
        self.multiple_selector = len(selectors) > 1

        self.selector_type = selector_attribute(self.selectors,
                                                'selector_type')
        if self.selector_type != SELECTOR_TYPE['XML']:
            raise ValueError("""expect xml selector.
                             For trxml, please use trxml-miner""")

    @classmethod
    def from_selector_string(cls, selector_string: str):
        '''construct xml selector from input string'''
        selectors = selector_string.split(",")
        return cls(selectors)

    def select_xml_fields(self, xml_tree):
        '''select all values matches the selector'''
        return {
            selector.text: selector.select_all_values(xml_tree)
            for selector in self.selectors
        }

    def __iter__(self):
        for selector in self.selectors:
            yield selector

    def __str__(self):
        return self.selector_string
