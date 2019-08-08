"""TRXML class: render fild or strings to xml class, and select values"""
from .base_xml import XML


class TKXML(XML):
    '''
    TKXML class:
        xml tree object generated from
        - xml file
        - xml string
    '''

    def __init__(self, top_level_obj=None):
        super().__init__(top_level_obj)
        self.filename = self.top_level_obj.attrib.get('filename',
                                                      "__UNKNOWN__")

    @property
    def working_entity(self):
        '''the xml element to apply searching'''
        return self.top_level_obj
