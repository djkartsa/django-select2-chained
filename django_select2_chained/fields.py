"""Contains all the Django fields for select2-chained."""
import copy
import logging

from django_select2.fields import NO_ERR_RESP, AutoModelSelect2Field

from .widgets import ChainedAutoSelect2Widget

__all__ = (
    'ChainedAutoModelSelect2FieldMixin',
    'ChainedAutoModelSelect2Field',
    'RequestSpecificAutoModelSelect2Field',
    'ChainedRequestSpecificAutoModelSelect2Field'
)

logger = logging.getLogger(__name__)


class RequestSpecificAutoModelSelect2Field(AutoModelSelect2Field):
    """
    An AutoHeavy field whose queryset is determined from the current request parameter.

    This is done by using get_queryset method instead of the class-level queryset property.
    Allows using the same AutoHeavy field instance between multiple requests and having request-specific data.
    """

    def get_queryset(self, request):
        """
        Method that determines the queryset from the current request.

        Must be implemented.
        """
        raise NotImplementedError("get_queryset() must be implemented.")

    def get_results(self, request, term, page, context):
        """
        See :py:meth:`.views.Select2View.get_results`.

        This implementation takes care of detecting if more results are available.
        """
        if not hasattr(self, 'search_fields') or not self.search_fields:
            raise ValueError('search_fields is required.')

        # Add request parameter to get_queryset.
        qs = self.get_queryset(request)
        if qs is not None:
            qs = copy.deepcopy(qs)
            params = self.prepare_qs_params(request, term, self.search_fields)

            if self.max_results:
                min_ = (page - 1) * self.max_results
                max_ = min_ + self.max_results + 1  # Fetch one extra row to check if there are more rows.
                res = list(qs.filter(*params['or'], **params['and'])[min_:max_])
                has_more = len(res) == (max_ - min_)
                if has_more:
                    res = res[:-1]
            else:
                res = list(qs.filter(*params['or'], **params['and']))
                has_more = False

            res = [(getattr(obj, self.to_field_name), self.label_from_instance(obj), self.extra_data_from_instance(obj))
                   for obj in res]
        else:
            res = []
            has_more = False
        return NO_ERR_RESP, has_more, res


class ChainedAutoModelSelect2FieldMixin(object):
    """
    A mixin for subclasses of AutoModelSelect2Field that adds chaining functionality.

    The attached field gets filtered by another field in the form, specified by the chain_field attribute.
    The selected option in the chain_field limits the queryset in the current field.
    """

    def __init__(self, *args, **kwargs):
        """
        Init method.

        :param chain_field: related field name
        :param model_field: real foreign key field name in the model
        :param allow_empty: if true, displays all options when related field is empty
        """
        self.chain_field = kwargs.pop('chain_field', None)
        self.model_field = kwargs.pop('model_field', self.chain_field)
        self.allow_empty = kwargs.pop('allow_empty', None)
        select2_options = kwargs.pop('select2_options', None)
        widget = kwargs.get('widget', None)
        if not widget:
            widget = ChainedAutoSelect2Widget(chain_field=self.chain_field, model_field=self.model_field,
                                              select2_options=select2_options)
            kwargs.update({
                'widget': widget
            })
        self.chain_field = self.chain_field or widget.chain_field
        self.model_field = self.model_field or widget.model_field
        if not self.chain_field or not self.model_field:
            raise NotImplementedError(u"Chain field and model field must be specified.")
        super(ChainedAutoModelSelect2FieldMixin, self).__init__(*args, **kwargs)

    def prepare_qs_params(self, request, search_term, search_fields):
        """Prepare queryset parameters for filtering."""
        params = super(ChainedAutoModelSelect2FieldMixin, self).prepare_qs_params(request, search_term, search_fields)
        chain_field_id = request.GET.get(self.chain_field, None)
        if chain_field_id:
            params['and'].update({self.model_field: chain_field_id})
        elif not self.allow_empty:
            params['and'].update({'pk__isnull': True})
        return params


class ChainedAutoModelSelect2Field(ChainedAutoModelSelect2FieldMixin, AutoModelSelect2Field):
    """An :py:class:`AutoModelSelect2Field` with chaining functionality."""

    pass


class ChainedRequestSpecificAutoModelSelect2Field(ChainedAutoModelSelect2FieldMixin,
                                                  RequestSpecificAutoModelSelect2Field):
    """A :py:class:`RequestSpecificAutoModelSelect2Field` with chaining functionality."""

    pass
