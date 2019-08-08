'''the trxml selector script'''

from os.path import isfile, isdir
from argparse import ArgumentParser
from .data_utils import DataLoader
from .selectors import TRXMLSelectors
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


def _load_data(args):
    if isdir(args.source):
        LOGGER.info("reading trxml documents from dir %s", args.source)
        data = DataLoader.load_from_dir(args.source)
    elif isfile(args.source):
        LOGGER.info("reading mtrxml document %s", args.source)
        data = DataLoader.load_from_mtrxml(args.source)
    else:
        raise TypeError("could not determine source type, please check")
    return data


def _read_selectors(args):
    if args.selector:
        selectors = TRXMLSelectors.from_selector_string(args.selector)
    elif args.itemgroup and args.fields:
        selectors = TRXMLSelectors.from_itemgroup_and_fields(args.itemgroup,
                                                             args.fields)
    else:
        raise RuntimeError('''need to set arguments selectors,
        or itemgroup and fields''')
    return selectors


def main():
    '''apply selectors to trxml files'''
    args = get_args()
    data = _load_data(args)
    selectors = _read_selectors(args)
    LOGGER.info(
        "select '%s' and write results to '%s'",
        selectors.selector_string,
        args.output_file
    )
    trxml_miner = TRXMLMiner(selectors)
    trxml_miner.mine(data, args.output_file)


if __name__ == "__main__":
    main()
