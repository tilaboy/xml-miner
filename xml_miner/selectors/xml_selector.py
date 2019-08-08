'''XML selector'''
from typing import List
from .selector_utils import valid_field_name


class XMLSelector:
    '''
    XMLSelector:
    - select all values of nodes matches selector
    '''

    def __init__(self, selector: str):
        valid_field_name(selector)
        self.text = selector

    def select_all_fields(self, xml_tree):
        '''select all fields match selectors'''
        return xml_tree.working_entity.iter(self.text)

    def select_all_values(self, xml_tree) -> List[str]:
        '''select all values match selectors'''
        return [
                "".join(element.itertext())
                for element in self.select_all_fields(xml_tree)
               ]

    def __str__(self):
        return self.text
