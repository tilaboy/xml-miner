'''xml selectors and trxml selectors classes'''

from .xml_selectors import XMLSelectors
from .trxml_selectors import TRXMLSelectors
from .selector_utils import SELECTOR_TYPE, TRXML_SELECTOR_TYPE

__all__ = ['XMLSelectors',
           'TRXMLSelectors',
           'SELECTOR_TYPE',
           'TRXML_SELECTOR_TYPE']
name = 'selectors'
