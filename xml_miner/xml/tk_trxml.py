"""
TRXML class: render field or strings to trxml class, and select using xpath
"""
from .base_xml import XML


class TKTRXML(XML):
    """
    TRXML:
    - render field or strings to trxml class
    - and select using xpath
    """

    def __init__(self, top_level_obj=None):
        super().__init__(top_level_obj)
        self.working_entity_tag = 'DocumentStructure'

    @property
    def working_entity(self):
        '''the xml element to apply searching'''
        return self.top_level_obj.find(self.working_entity_tag)

    @property
    def xml_entity(self):
        '''the xml part of the tree'''
        return self.top_level_obj.find('Document')

    @property
    def filename(self):
        '''
        filename of the oringal file

        normally stored as an attribute of the top level tag'''

        default_filename = '__UNKNOWN__'
        try:
            filename = self.xml_entity.get('filename', default_filename)
        except AttributeError:
            filename = default_filename
        return filename
