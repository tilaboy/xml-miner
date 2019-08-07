"""apply selector on input data, and output it to a csv file"""
from typing import List
import xml.etree.ElementTree as ET
from .data_utils import DataSaver
from .xml import TKXML, TKTRXML
from .selectors import TRXML_SELECTOR_TYPE
from . import LOGGER

def _normalize_string(line: str) -> str:
    '''
    normalization selected values:
    - replace \n with __NEWLINE__
    '''
    if line:
        line = line.replace('\n', "__NEWLINE__")
        line = line.replace('\t', "    ")
    return line


class CommonMiner:
    '''
    CommonMiner:

    shared class for both xml and trxml
    '''
    def __init__(self, data, selectors, output_file):
        '''
        params:
            data (xml document_loader): a data generator loop through all xmls
            selectors (XMLSelectors): see xml_selector.py
            output_file (string): the output filename
            with_field_name: add a column to show the field_name of extracted value
        output:
            None
        '''
        self.data = data
        self.selectors = selectors
        self.selector_string = selectors.selector_string
        self.writer = DataSaver(output_file)
        self._init_counter()

    def _init_counter(self):
        self.num_docs = 0
        self.num_values = 0
        self.value_counter = {selector.text:0 for selector in self.selectors}

    def _print_summary(self):
        LOGGER.info("found total %s values from %s docss", self.num_values, self.num_docs)
        if len(self.value_counter) > 1:
            for field in self.value_counter:
                LOGGER.info("- found %d %s", self.value_counter[field], field)


class XMLMiner(CommonMiner):
    '''
    XMLPorcessor:
    - iterate over the xml files and select values
    - output selected values to a file, and print summary
    '''
    def __init__(self, data, selectors, output_file, with_field_name=False):
        '''
        params:
            data (xml document_loader): a data generator loop through all xmls
            selectors (XMLSelectors): see xml_selector.py
            output_file (string): the output filename
            with_field_name: add a column to show the field_name of extracted value
        output:
            None
        '''
        super().__init__(data, selectors, output_file)
        self.with_field_name = with_field_name

    def _print_header(self) -> List[str]:
        csv_header = ["filename", "value"]
        if self.with_field_name:
            csv_header.append("field")
        self.writer.store(csv_header)
        return

    def _print_record(self, filename: str, value: str, field: str) -> List[str]:
        norm_value = _normalize_string(value)
        if norm_value:
            csv_row = [filename, norm_value]
            if self.with_field_name:
                csv_row.append(field)
            self.writer.store(csv_row)

            self.num_values += 1
            self.value_counter[field] += 1



    def mine(self):
        """
        iterate the input data (xml obj), apply selector on each xml, and save
        the selected values to the output file

        output file format:
        - no field name: filename value
        - with field name: filename, value, field_name
        """
        self._init_counter()
        self._print_header()

        for doc in self.data.data_generator:
            try:
                xml_obj = TKXML.from_string(doc)
            except ET.ParseError:
                LOGGER.warning("WARNING: could not parse, skip file:\n%s", doc)
                continue

            self.num_docs += 1

            for field, values in self.selectors.select_xml_fields(xml_obj).items():
                for value in values:
                    self._print_record(xml_obj.filename, value, field)

        self._print_summary()
        self.writer.close_stream()


class TRXMLMiner(CommonMiner):
    '''
    TRXMLPorcessor:
    - iterate over the trxml files and select values
    - output selected values to a file, and print summary
    '''

    def _print_header(self) -> List[str]:
        if self.selectors.trxml_selector_type == TRXML_SELECTOR_TYPE['MULTIPLE']:
            field_names = [selector.field_name for selector in self.selectors]
            header = ["filename", self.selectors.shared_itemgroup_name] + field_names
        else:
            field_names = [selector.text for selector in self.selectors]
            header = ["filename"] + field_names
        self.writer.store(header)

    def _normalize_record_values(self, values) -> List[str]:
        norm_values = []
        for field_name in values:
            norm_value = _normalize_string(values[field_name])
            norm_values.append(norm_value)
            if norm_value:
                self.num_values += 1
                self.value_counter[field_name] += 1
        return norm_values

    def mine(self):
        """
        iterate the input data (trxml obj), apply selector on each trxml, and output
        the selected values to a csv file

        params:
            data (trxml document_loader): contains a data generator loop
            through all input data
            selectors(TRXMLSectors): see trxml_selector.py
            output_file (string): the output filename
        """
        self._init_counter()
        self._print_header()

        for doc in self.data.data_generator:
            try:
                trxml_obj = TKTRXML.from_string(doc)
            except ET.ParseError:
                LOGGER.warning("WARNING: could not parse trxml, skip file:\n%s", doc)
                continue

            self.num_docs += 1
            selected_values = self.selectors.select_trxml_fields(trxml_obj)

            if self.selectors.trxml_selector_type == TRXML_SELECTOR_TYPE['MULTIPLE']:
                for item_index in selected_values:
                    norm_values = self._normalize_record_values(selected_values[item_index])
                    self.writer.store([trxml_obj.filename, item_index] + norm_values)
            else:
                norm_values = self._normalize_record_values(selected_values)
                self.writer.store([trxml_obj.filename] + norm_values)

        self._print_summary()
        self.writer.close_stream()
