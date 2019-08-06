'''the xml selector script'''
#!/usr/bin/env python
from argparse import ArgumentParser
from os.path import isfile, isdir
from .data_utils import DataLoader
from .selectors import XMLSelectors
from .selector_processor import XMLProcessor
from . import LOGGER

def get_args():
    '''get arguments'''
    parser = ArgumentParser(description='''used defined selector, select field
                        values from xml files.''')

    parser.add_argument('--source', help='''source of the xml files, it could be
                        1. a dir contains xml files
                        2. a mxml file or xml file
                        3. the host:port of a running annotation server''',
                        type=str, required=True)

    parser.add_argument('--selector', help='selector or selector',
                        type=str, required=True)

    parser.add_argument('--output_file', help='outputfile of selected values',
                        type=str, default='STDOUT')

    as_args = parser.add_argument_group('as_args',
                                        'arguments for annotation server')

    as_args.add_argument('--query', help='query to get document sets from AS',
                         type=str, default='')
    as_args.add_argument('--as_user', help='username to the annotationserver',
                         type=str, default='')
    as_args.add_argument('--as_pass', help='password to the annoationserver',
                         type=str, default='')
    parser.add_argument('--with_field_name', help='add a column to show the field',
                        action='store_true')

    return parser.parse_args()

def main():
    '''apply selectors to xml files'''
    args = get_args()

    if isdir(args.source):
        LOGGER.info("reading xml documents in dir %s", args.source)
        data = DataLoader.load_from_dir(args.source)
    elif isfile(args.source):
        LOGGER.info("reading mxml document %s", args.source)
        data = DataLoader.load_from_mxml(args.source)
    elif ":" in args.source:
        host, port = args.source.split(':')
        LOGGER.info("connecting annotation server: host %s and port %s", host, port)
        data = DataLoader.load_from_as(
            host,
            port,
            args.query,
            args.as_user,
            args.as_pass
            )
    else:
        raise TypeError("could not determine source type, please check")

    selectors = XMLSelectors.from_selector_string(args.selector)
    LOGGER.info(
        "select '%s' and write results to '%s'",
        selectors.selector_string,
        args.output_file
    )
    xml_processor = XMLProcessor(
        data,
        selectors,
        args.output_file,
        args.with_field_name
    )
    xml_processor.process()


if __name__ == "__main__":
    main()
