'''the trxml selector script'''

from argparse import ArgumentParser
from .miner import TRXMLMiner
from . import LOGGER


def get_args():
    '''get arguments'''
    parser = ArgumentParser(description='''used defined selector, select field
                            values from trxml files.''')

    parser.add_argument('--source', help='''source of the trxml files, it is
                        1) a dir contains trxml files or 2) a mtrxml file''',
                        type=str, required=True)

    parser.add_argument('--output_file', help='outputfile of selected values',
                        type=str, default='STDOUT')

    parser.add_argument('--selector', help='''selector or selectors, selectors
                        are comma separated selector, both singleton selector,
                        e.g. 'name.0.name,address.0.address',
                        or multi-item selectors:
                        'skill.*.skill,skill.*.skill_type' ''',
                        type=str, default=None)

    parser.add_argument('--itemgroup',
                        help='itemgroup, for multi field selection',
                        type=str, default=None)

    parser.add_argument('--fields', help='fields, comma separated',
                        type=str, default=None)

    return parser.parse_args()


def main():
    '''apply selectors to trxml files'''
    args = get_args()
    trxml_miner = TRXMLMiner(args.selector, args.itemgroup, args.fields)
    LOGGER.info(
        "select '%s' and write results to '%s'",
        trxml_miner.selectors.selector_string,
        args.output_file
    )
    trxml_miner.mine_and_save(args.source, args.output_file)


if __name__ == "__main__":
    main()
