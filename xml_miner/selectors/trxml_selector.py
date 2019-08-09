'''selector class for trxml'''

from .xml_selector import XMLSelector


class TRXMLSelector(XMLSelector):
    '''
    trxml selector:

    - subclass of XMLSelector

    - method to select values from trxml
    '''

    def __init__(self, selector: str):
        super().__init__(selector)
        self.itemgroup_name, self.item_index, self.field_name = \
            self.parse_trxml_selector()
        self.xpath = self._trxml_selector_to_xpath()

    def parse_trxml_selector(self):
        '''
        converting the trxml selector to (itemgroup, index, field):

        params:

        - selector: string

        output:

        - itemgroup, index, field

        conversion rules:
        ::

            - ig.index.field    ->    (ig, index, field)
            - ig.*.field        ->    (ig, *, field)
            - ig.field          ->    (ig, *, field)
        '''

        if "." in self.text:
            tags = self.text.split(".")
            itemgroup = tags[0]
            if len(tags) == 2:
                field = tags[1]
                index = "*"
            elif len(tags) == 3:
                field = tags[2]
                index = tags[1]
            else:
                raise ValueError("unable to parse the trxml selector")
        else:
            raise ValueError('''trxml selector should be in the form of
                             \n\t- itemgroup.field
                             \n\t- itemgroup.*.field
                             \n\t- itemgroup.0.field''')
        return itemgroup, index, field

    def _itemgroup_xpath(self) -> str:
        """convert the itemgroup name to the xpath"""
        return f"ItemGroup[@key='{self.itemgroup_name}']"

    def _field_xpath(self) -> str:
        """convert the field name to the xpath"""
        return f"Field[@key='{self.field_name}']/Value"

    def _item_xpath(self) -> str:
        """convert the item with index to the xpath"""
        return f"/Item[@index='{self.item_index}']/"

    def _trxml_selector_to_xpath(self) -> str:
        """convert a full trxml selector to the xpath"""
        return self._itemgroup_xpath() + self._item_xpath() \
            + self._field_xpath()

    def select_field_with_xpath(self, xml_tree):
        '''select the field using the selector xpath'''
        return xml_tree.working_entity.find(self.xpath)

    def select_value_with_xpath(self, xml_tree) -> str:
        '''
        get the value of the field where the selector matches
        '''
        element = self.select_field_with_xpath(xml_tree)
        value = element.text if element is not None else ''
        return value

    def field_value_from_item(self, item) -> str:
        '''
        given an item and a field_name, get the value of that field
        '''
        try:
            field = item.find(self._field_xpath())
            field_value = field.text
        except AttributeError:
            field_value = ''
        return field_value

    def __str__(self):
        return self.text
