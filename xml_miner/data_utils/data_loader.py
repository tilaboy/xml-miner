"""A module to load input xml/trxml from different source"""
from os import listdir
from os.path import join, isfile
from .asclient import ASClient
from .. import LOGGER


def load_from_file(input_dir, files):
    """
    load document from a list files read from a directory

    params:
        input_dir (string): directory contains all files
        files (list): a list files

    output:
        xml string: a iterator object to generate xml string
    """

    for filename in sorted(files):
        filepath = join(input_dir, filename)
        if not isfile(filepath):
            LOGGER.warning("Warning: %s is not a file, skip", filepath)
        else:
            with open(filepath, 'rt') as file:
                yield file.read()


def load_from_string(xml_string, header_line):
    """
    load document string, the string might contain multiple xml files

    params:
        xml_string (string): input xml strings

    output:
        xml string: a iterator object to generate xml string
    """
    xml_lines = []
    for line in xml_string.splitlines():
        if line.startswith(header_line):
            if xml_lines:
                xml = "\n".join(xml_lines)
                yield xml
            xml_lines = [line]
        elif line.startswith('<?xml'):
            pass
        else:
            xml_lines.append(line)
    xml = "\n".join(xml_lines)
    yield xml


class DataLoader:
    """
    DataLoader:
    - load data from different resources
    - generate xml input for downstream tasks
    """

    XML_HEADER = '<begin '
    TRXML_HEADER = '<TextractorResult '

    def __init__(self, data_generator=None):
        self.data_generator = data_generator

    @classmethod
    def load_from_dir(cls, input_dir):
        """
        create the document loader object from dir

        params:
            input_dir (string): director contains xml files

        output:
            DataLoader object: a iterator object to generate xml string
        """
        files = listdir(input_dir)
        if not files:
            raise RuntimeError('''no file found here, please check the
                               dir contains XML''')
        return cls(data_generator=load_from_file(input_dir, files))

    @classmethod
    def load_from_mxml(cls, input_mxml):
        """
        create the document loader object from mxml

        params:
            mxml (string): a mxml files

        output:
            DataLoader object: a iterator object to generate xml string
        """
        with open(input_mxml, 'rt') as file:
            xml_string = file.read()
        return cls(data_generator=load_from_string(xml_string, cls.XML_HEADER))

    @classmethod
    def load_from_mtrxml(cls, input_mxml):
        """
        create the document loader object from mxml

        params:
            mxml (string): a mxml files

        output:
            DataLoader object: a iterator object to generate xml string
        """
        with open(input_mxml, 'rt') as file:
            xml_string = file.read()
        return cls(data_generator=load_from_string(xml_string,
                                                   cls.TRXML_HEADER))

    @classmethod
    def load_from_as(cls, host, port, query, as_user='', as_pass=''):
        """
        create the document loader object from AnnotationServer

        params:
            host (string): hostname of the annotationserver
            port (int): port of the AnnotationServer
            query (string): query to select documents
            as_user: AnnotationServer username
            as_pass: AnnotationServer password

        output:
            DataLoader object: a iterator object to generate xml string
        """
        as_client = ASClient(host, port, as_user, as_pass)
        return cls(data_generator=as_client.get_docs(query))
