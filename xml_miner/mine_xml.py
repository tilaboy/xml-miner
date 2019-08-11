'''the xml selector script'''

from argparse import ArgumentParser
from .miner import XMLMiner
from . import LOGGER


def get_args():
    '''get arguments'''
    parser = ArgumentParser(description='''used defined selector, select field
                        values from xml files.''')

    parser.add_argument('--source', help='''source of the xml files,
                        it could be:
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
    parser.add_argument('--with_field_name',
                        help='add a column to show the field',
                        action='store_true')

    return parser.parse_args()


def main():
    '''apply selectors to xml files'''
    args = get_args()
    xml_miner = XMLMiner(args.selectors, args.with_field_name)
    LOGGER.info(
        "select '%s' and write results to '%s'",
        xml_miner.selectors.selector_string,
        args.output_file
    )
    xml_miner.mine_and_save(args.source,
                            args.output_file,
                            args.query,
                            args.as_user,
                            args.as_pass)


if __name__ == "__main__":
    main()
