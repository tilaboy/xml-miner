"""TRXML Selectors class"""
from typing import List
from .selector_utils import valid_field_name, selector_attribute
from .selector_utils import SELECTOR_TYPE, TRXML_SELECTOR_TYPE
from .trxml_selector import TRXMLSelector


class TRXMLSelectors():
    '''
    TRXMLSelectors:
    - array of TRXMLSelector class
    - method to select values on trxml doc level or from each items
    '''

    def __init__(self, selectors: List[str], trxml_selector_type=None,
                 shared_itemgroup_name=None):

        self.selector_string = ",".join(selectors)
        self.selectors = [
            TRXMLSelector(selector_string)
            for selector_string in selectors
        ]
        self.multiple_selector = len(selectors) > 1

        self.selector_type = selector_attribute(
            self.selectors,
            'selector_type'
        )
        if self.selector_type != SELECTOR_TYPE['TRXML']:
            raise ValueError(
                """expect trxml selector.
                For xml, please use xml-miner
                """)

        if trxml_selector_type is None:
            self.trxml_selector_type = \
                selector_attribute(self.selectors, 'trxml_selector_type')
        else:
            self.trxml_selector_type = trxml_selector_type

        if self.trxml_selector_type == TRXML_SELECTOR_TYPE['MULTIPLE']:
            if shared_itemgroup_name is None:
                self.shared_itemgroup_name = \
                    selector_attribute(self.selectors, 'same_itemgroup')
            else:
                self.shared_itemgroup_name = shared_itemgroup_name

    @classmethod
    def from_selector_string(cls, selector_string: str):
        '''
        construct the selectors from string

        input:
            - selector string
        '''
        selectors = selector_string.split(",")
        return cls(selectors)

    @classmethod
    def from_itemgroup_and_fields(cls, itemgroup: str, fields: str):
        '''
        construct from itemgroup and fields, only for trxml

        input:
            - ItemGroup, e.g. experienceitem
            - Fields, e.g. jobtitle,startdate,enddate
        '''
        valid_field_name(itemgroup)
        valid_field_name(fields)

        if '.' in fields:
            raise ValueError(
                "'.' NOT allowed in the field name")

        return cls(
            [f"{itemgroup}.*.{field}" for field in fields.split(",")],
            TRXML_SELECTOR_TYPE['MULTIPLE'],
            itemgroup
        )

    def select_trxml_fields(self, trxml):
        '''select values from all fields matching selectors'''
        if self.trxml_selector_type == TRXML_SELECTOR_TYPE['SINGLETON']:
            selected = self._select_singletons(trxml)
        else:
            selected = self._select_multiple_items(trxml)
        return selected

    def _select_multiple_items(self, trxml):
        '''
        select values from multiple items:

        e.g. selectors are "skill.skill,skill.type", the output is a dictionary
        xx = {
            0:{skill:'java',type:'compskill'}
            1:{skill:'leadership',type:'softskill'}
            2:.....
        }
        '''
        if self.trxml_selector_type != TRXML_SELECTOR_TYPE['MULTIPLE']:
            raise ValueError("selector for _select_multiple_items should \
            be multiple value selectors")

        # get the itemgroup
        itemgroup = trxml.working_entity.find(
            f"ItemGroup[@key='{self.shared_itemgroup_name}']")

        try:
            items = itemgroup.findall("Item")
        except AttributeError:
            items = []

        multiple_item_values = {}
        # for each item, get field value and save to item[index][field]:value
        for item in items:
            index = item.get('index')

            multiple_item_values[index] = {}
            for selector in self.selectors:
                field_value = selector.field_value_from_item(item)
                multiple_item_values[index][selector.text] = field_value

        return multiple_item_values

    def _select_singletons(self, trxml):
        '''
        select values from single item:

        e.g. selectors are "firstname.0.firstname,lastname.0.lastname",
        the output is a dictionary
        xx = {
            firstname:'Chao',
            lastname:'Li'}
        }

        '''
        if self.trxml_selector_type != TRXML_SELECTOR_TYPE['SINGLETON']:
            raise ValueError("selectors for select singletons should be \
            single value selectors")
        return {
            selector.text: selector.select_value_with_xpath(trxml)
            for selector in self.selectors
        }

    def __iter__(self):
        for selector in self.selectors:
            yield selector

    def __str__(self):
        return self.selector_string
