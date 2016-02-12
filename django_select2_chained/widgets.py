"""Contains all the Django widgets for select2-chained."""

import logging

from django.utils.safestring import mark_safe
from django_select2.util import JSFunctionInContext
from django_select2.widgets import AutoHeavySelect2Widget

__all__ = (
    'PrepopulatedSelect2Widget', 'ChainedAutoSelect2Widget'
)

logger = logging.getLogger(__name__)


class PrepopulatedSelect2Widget(AutoHeavySelect2Widget):
    """
    A prepopulated :py:class:`django_select2.widgets.AutoHeavySelect2Widget`.

    It allows sending empty search queries to the server.
    """

    def __init__(self, **kwargs):
        """
        Init method.

        :keyword select2_options: A dictionary containing select2 options.
        """
        if not isinstance(kwargs.get('select2_options'), dict):
            kwargs['select2_options'] = {}

        kwargs['select2_options'].update({
            # This will allow select2 to send empty search to server.
            'minimumInputLength': 0,
            # This is needed, otherwise search field will be hidden by select2.
            'minimumResultsForSearch': 0,
        })
        super(PrepopulatedSelect2Widget, self).__init__(**kwargs)


class ChainedAutoSelect2Widget(PrepopulatedSelect2Widget):
    """A :py:class:`PrepopulatedSelect2Widget` to be used with chained fields."""

    def __init__(self, *args, **kwargs):
        """
        Init method.

        :keyword chain_field: Name of the field in the form.
        :keyword model_field: Name of the field in the model.
        """
        self.chain_field = kwargs.pop('chain_field', None)
        self.model_field = kwargs.pop('model_field', None)
        super(ChainedAutoSelect2Widget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        """Render the widget."""
        if not self.chain_field or not self.model_field:
            raise NotImplementedError(u"Chain field and model field must be specified.")
        if len(name.split('-')) > 1:  # formset
            chain_field = '-'.join(name.split('-')[:-1] + [self.chain_field])
        else:
            chain_field = self.chain_field

        data_div = '<div class="field-chained-select-data" style="display: none" data-chained-field="%s" ' \
                   'data-value="%s" data-id="%s"></div>' \
                   % (chain_field, value, attrs['id'])
        output = super(ChainedAutoSelect2Widget, self).render(name, value, attrs, choices)
        output += data_div
        return mark_safe(output)

    class Media:
        js = ['/static/js/select2_chained.js']

    def init_options(self):
        """Initialize widget options."""
        self.options['ajax']['data'] = JSFunctionInContext('django_select2_chained.extra_url_params')
        self.options['chain_field'] = self.chain_field
