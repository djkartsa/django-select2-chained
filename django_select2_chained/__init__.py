"""
Chainable fields for Django-Select2_.

.. _Django-Select2: https://github.com/applegrew/django-select2

Widgets
-------

**Available widgets:**

- :py:class:`.ChainedAutoSelect2Widget`,
- :py:class:`.PrepopulatedSelect2Widget`

Fields
------

**Available fields and mixins:**

- :py:class:`.ChainedAutoModelSelect2FieldMixin`,
- :py:class:`.ChainedAutoModelSelect2Field`,
- :py:class:`.RequestSpecificAutoModelSelect2Field`,
- :py:class:`.ChainedRequestSpecificAutoModelSelect2Field`

"""

import logging

from .fields import (
    ChainedAutoModelSelect2FieldMixin,
    ChainedAutoModelSelect2Field,
    RequestSpecificAutoModelSelect2Field,
    ChainedRequestSpecificAutoModelSelect2Field
)
from .widgets import ChainedAutoSelect2Widget, PrepopulatedSelect2Widget

__all__ = ('ChainedAutoModelSelect2FieldMixin', 'ChainedAutoModelSelect2Field',
           'RequestSpecificAutoModelSelect2Field', 'ChainedRequestSpecificAutoModelSelect2Field',
           'ChainedAutoSelect2Widget', 'PrepopulatedSelect2Widget')

logger = logging.getLogger(__name__)

__version__ = u"0.1"
