"""apply selector on input data, and output it to a csv file"""
from typing import List
from os.path import isfile, isdir
import xml.etree.ElementTree as ET
from .data_utils import DataLoader, DataSaver
from .xml import TKXML, TKTRXML
from .selectors import TRXML_SELECTOR_TYPE, TRXMLSelectors, XMLSelectors
from . import LOGGER


class CommonMiner:
    '''
    CommonMiner:

    shared class for both xml and trxml
    '''
    def __init__(self, selectors):
        '''
        params:
            data (xml document_loader): a data generator loop through all xmls
            selectors (XMLSelectors): see xml_selector.py
            output_file (string): the output filename
            with_field_name: add a column to show the field_name of extracted
            value
        output:
            None
        '''
        self.selectors = selectors
        self.selector_string = self.selectors.selector_string
        self._init_counter()

    def _init_counter(self):
        self.num_docs = 0
        self.num_values = 0
        self.value_counter = {selector.text: 0 for selector in self.selectors}

    def _print_summary(self):
        LOGGER.info("found total %s values from %s docss",
                    self.num_values, self.num_docs)
        if len(self.value_counter) > 1:
            for field in self.value_counter:
                LOGGER.info("- found %d %s", self.value_counter[field], field)

    @staticmethod
    def normalize_string(line: str) -> str:
        '''
        normalization selected values:
        - replace \n with '__NEWLINE__'
        - replace \t with 4 space '    '
        '''
        if line:
            line = line.replace('\n', "__NEWLINE__")
            line = line.replace('\t', "    ")
        return line


class XMLMiner(CommonMiner):
    '''
    XMLPorcessor:
    - iterate over the xml files and select values
    - output selected values to a file, and print summary
    '''
    def __init__(self, selectors, with_field_name=False):
        '''
        params:
            selectors (XMLSelectors): see xml_selector.py
            with_field_name: add a column to show the field_name of
            extracted value
        '''
        selector_obj = self.read_selectors(selectors)
        super().__init__(selector_obj)
        self.with_field_name = with_field_name

    def _print_header(self, writer) -> List[str]:
        csv_header = ["filename", "value"]
        if self.with_field_name:
            csv_header.append("field")
        writer.store(csv_header)
        return

    def _print_record(
                      self,
                      writer: DataSaver,
                      filename: str,
                      value: str,
                      field: str) -> List[str]:
        norm_value = self.normalize_string(value)
        if norm_value:
            csv_row = [filename, norm_value]
            if self.with_field_name:
                csv_row.append(field)
            writer.store(csv_row)

            self.num_values += 1
            self.value_counter[field] += 1

    def load_data(self,
                  source: str,
                  query: str = None,
                  as_user: str = None,
                  as_pass: str = None):
        """
        load the data into a data generator

        params:
            - source: data source
            - annotation server parameters: query, as_user, as_pass

        output:
            - yeild xml
        """

        if isdir(source):
            LOGGER.info("reading xml documents in dir %s", source)
            data = DataLoader.load_from_dir(source)
        elif isfile(source):
            LOGGER.info("reading mxml document %s", source)
            data = DataLoader.load_from_mxml(source)
        elif ":" in source:
            host, port = source.split(':')
            LOGGER.info("connecting annotation server: host %s and port %s",
                        host, port)
            data = DataLoader.load_from_as(
                host,
                port,
                query,
                as_user,
                as_pass
                )
        else:
            raise TypeError("could not determine source type, please check")
        return data

    def read_selectors(self, selector: str):
        """
        read selector strings and construct selectors object

        params:
            - selector: input selector strings

        output:
            - selectors: XMLSelectors object
        """

        return XMLSelectors.from_selector_string(selector)

    def mine(self,
             source: str,
             query: str = None,
             as_user: str = None,
             as_pass: str = None):
        """
        iterate the input data (xml obj), apply selector on each xml, and
        yield the selected values

        params:
            - source: data source
            - annotation server parameters: query, as_user, as_pass

        output:
            - iterate over selected fields per doc
        """

        data = self.load_data(source, query, as_user, as_pass)
        for doc in data.data_generator:
            try:
                xml_obj = TKXML.from_string(doc)
                selected = self.selectors.select_xml_fields(xml_obj)
            except ET.ParseError:
                LOGGER.warning("Can not parse, skip file:\n%s", doc)
                continue
            except AttributeError:
                LOGGER.warning("Failed to select, skip file:\n%s", doc)
                continue

            self.num_docs += 1
            yield {'file': xml_obj.filename, 'values': selected}

    def mine_and_save(self,
                      source: str,
                      output_file: str,
                      query: str = None,
                      as_user: str = None,
                      as_pass: str = None):

        """
        iterate the selected values and save/print to ouput

        params:
            - source: data source
            - output_file (string): the output filename
            - annotation server parameters: query, as_user, as_pass

        output file format:
            - no field name: filename value
            - with field name: filename, value, field_name
        """
        writer = DataSaver(output_file)
        self._init_counter()
        self._print_header(writer)
        for selected in self.mine(source, query, as_user, as_pass):
            for field, values in selected['values'].items():
                for value in values:
                    self._print_record(writer,
                                       selected['file'],
                                       value,
                                       field)

        self._print_summary()
        writer.close_stream()


class TRXMLMiner(CommonMiner):
    '''
    TRXMLPorcessor:
    - iterate over the trxml files and select values
    - output selected values to a file, and print summary
    '''

    def __init__(self, selectors, itemgroup=None, fields=None):
        '''
        params:
            selectors (string): input selectors
            itemgroup (string): input ItemGroup
            fields (string): input fields
        '''
        selector_obj = self.read_selectors(selectors, itemgroup, fields)
        super().__init__(selector_obj)

    def _print_header(self, writer) -> List[str]:
        if self.selectors.trxml_selector_type == \
                TRXML_SELECTOR_TYPE['MULTIPLE']:
            field_names = [selector.field_name for selector in self.selectors]
            header = ["filename", self.selectors.shared_itemgroup_name] \
                + field_names
        else:
            field_names = [selector.text for selector in self.selectors]
            header = ["filename"] + field_names
        writer.store(header)

    def _normalize_record_values(self, values) -> List[str]:
        norm_values = []
        for field_name in values:
            norm_value = self.normalize_string(values[field_name])
            norm_values.append(norm_value)
            if norm_value:
                self.num_values += 1
                self.value_counter[field_name] += 1
        return norm_values

    def load_data(self, source):
        """
        load the data into a data generator

        params:
            - source: data source

        output:
            - yeild trxml
        """
        if isdir(source):
            LOGGER.info("reading trxml documents from dir %s", source)
            data = DataLoader.load_from_dir(source)
        elif isfile(source):
            LOGGER.info("reading mtrxml document %s", source)
            data = DataLoader.load_from_mtrxml(source)
        else:
            raise TypeError("could not determine source type, please check")
        return data

    def read_selectors(self,
                       selector: str,
                       itemgroup: str = '',
                       fields: str = ''):
        """
        read selector strings and construct selector object

        params:
            - selector: input selector strings
            - itemgroup: input itemgroup strings
            - fields: input fields strings

        output:
            - selectors: TRXMLSelectors object
        """

        if selector:
            selectors = TRXMLSelectors.from_selector_string(selector)
        elif itemgroup and fields:
            selectors = TRXMLSelectors.from_itemgroup_and_fields(itemgroup,
                                                                 fields)
        else:
            raise RuntimeError('''need to set arguments selectors,
            or itemgroup and fields''')
        return selectors

    def mine(self, source):
        """
        iterate the input data (trxml obj), apply selector on each trxml,
        and output the selected values to a csv file

        params:
            source: data source

        output:
            generate selected values per doc
        """

        data = self.load_data(source)
        for doc in data.data_generator:
            try:
                trxml_obj = TKTRXML.from_string(doc)
                selected = self.selectors.select_trxml_fields(trxml_obj)
            except ET.ParseError:
                LOGGER.warning("Can not parse trxml, skip file:\n%s", doc)
                continue
            except AttributeError:
                LOGGER.warning("Failed to select, skip file:\n%s", doc)
                continue

            self.num_docs += 1
            yield {'file': trxml_obj.filename, 'values': selected}

    def mine_and_save(self, source: str, output_file: str):
        """
        iterate the input data (trxml obj), apply selector on each trxml,
        and output the selected values to a csv file

        params:
            source (string): data source
            output_file (string): the output filename
        """
        self._init_counter()
        writer = DataSaver(output_file)
        self._print_header(writer)

        for selected_values in self.mine(source):

            if self.selectors.trxml_selector_type \
                    == TRXML_SELECTOR_TYPE['MULTIPLE']:
                for item_index in selected_values['values']:
                    norm_values = self._normalize_record_values(
                        selected_values['values'][item_index])
                    writer.store(
                                 [selected_values['file'], item_index]
                                 + norm_values
                                )
            else:
                norm_values = self._normalize_record_values(
                        selected_values['values'])
                writer.store([selected_values['file']] + norm_values)

        self._print_summary()
        writer.close_stream()
