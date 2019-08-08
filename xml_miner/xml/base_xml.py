"""XML class: render xml file or xml strings to xml tree object"""
import xml.etree.ElementTree as ET


class XML:
    '''
    XML:
        general xml class, xml tree object can be generated from
        - xml file
        - xml string
    '''

    def __init__(self, top_level_obj=None):
        self.top_level_obj = top_level_obj
        self.top_level_tag = self.top_level_obj.tag

    @classmethod
    def from_file(cls, xml_file: str):
        """
        create xml object from filename

        params:
            xml_file (string): xml file

        output:
            xml object: ElementTree object
        """
        tree = ET.parse(xml_file)
        return cls(top_level_obj=tree.getroot())

    @classmethod
    def from_string(cls, xml_string: str):
        """
        create xml object from xml_string

        params:
            xml_string (string): xml string

        output:
            xml object: ElementTree object
        """

        tree = ET.ElementTree(ET.fromstring(xml_string))
        return cls(top_level_obj=tree.getroot())

    @staticmethod
    def text_from_element(element):
        '''the text value of an xml element'''
        if element is not None:
            value = element.text
        else:
            value = ''
        return value

    def __str__(self):
        return ET.tostring(self.top_level_obj, encoding="UTF-8",
                           short_empty_elements=False).decode().strip()
