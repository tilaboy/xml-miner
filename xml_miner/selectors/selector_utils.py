'''utils and constants functions used by the selector and selectors class'''

import re

RE_ALPHA = re.compile(r'\w')
SELECTOR_TYPE = {'XML': 'xml', 'TRXML': 'trxml'}
TRXML_SELECTOR_TYPE = {'SINGLETON': 'singleton', 'MULTIPLE': 'multiple'}


def valid_field_name(tag_name: str = '') -> bool:
    '''
    simple validation function:

    params:
    - tag_name: string

    output:
    - True/False
    '''
    # need to contain at least one alphabet chars
    if RE_ALPHA.search(tag_name) is None:
        raise ValueError(
            f"tag_name '{tag_name}' needs at least one alphabet char")
    return True


def _selector_target_type(selector) -> str:
    if "." in selector.text:
        selector_type = SELECTOR_TYPE['TRXML']
    else:
        selector_type = SELECTOR_TYPE['XML']
    return selector_type


def _selector_singleton_type(selector) -> bool:
    item_index = selector.item_index
    if item_index.isdigit():
        selector_type = TRXML_SELECTOR_TYPE['SINGLETON']
    else:
        selector_type = TRXML_SELECTOR_TYPE['MULTIPLE']
    return selector_type


def _selector_same_itemgroup(selector) -> str:
    return selector.itemgroup_name


def selector_attribute(selectors, attribute_name) -> str:
    '''
    fetch the selector attribute, and check the consistency of all selectors

    params:
    - selectors: a list of selector object
    - attribute_name: name of the attribute

    output:
    attibute_value: string
    '''
    if attribute_name == 'selector_type':
        result = _selector_attribute_checking(selectors, _selector_target_type)
    elif attribute_name == 'trxml_selector_type':
        result = _selector_attribute_checking(selectors,
                                              _selector_singleton_type)
    elif attribute_name == 'same_itemgroup':
        result = _selector_attribute_checking(selectors,
                                              _selector_same_itemgroup)
    else:
        raise ValueError(
            f"selector attribute type '{attribute_name}' unknown"
        )
    return result


def _selector_attribute_checking(selectors, attrib_func):
    first_attrib = None

    for selector in selectors:
        if first_attrib is None:
            first_attrib = attrib_func(selector)
        elif first_attrib != attrib_func(selector):
            raise ValueError(
                f"""selector '{selector.text}' seems has different type than others,
                e.g.,
                - xml v.s. trxml,
                - or singleton V.S. multi-item
                - or different itemgroup for multi-item selectors.

                Please check!
                """
            )
    return first_attrib
