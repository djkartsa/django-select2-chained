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
logger = logging.getLogger(__name__)

__version__ = u"0.1"

try:
    from django.conf import settings
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Django found.")
    if settings.configured:
        from .widgets import ChainedAutoSelect2Widget, PrepopulatedSelect2Widget
        from .fields import (
            ChainedAutoModelSelect2FieldMixin,
            ChainedAutoModelSelect2Field,
            RequestSpecificAutoModelSelect2Field,
            ChainedRequestSpecificAutoModelSelect2Field
        )

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Django found and fields and widgets loaded.")
except ImportError:
    if logger.isEnabledFor(logging.INFO):
        logger.info("Django not found.")
