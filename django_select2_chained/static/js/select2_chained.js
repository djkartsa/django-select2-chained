/*jslint indent: 4, maxlen: 120 */
/*global $: false, window, document, jQuery, django, navigator */

// TODO: get rid of this hack when Django 1.6
if ($.fn.jquery === '1.4.2') {
    $.noConflict(true);
}

if (!window['django_select2_chained']) {
    var django_select2_chained = {
        extra_url_params: function (term, page, context) {
            var field_id = jQuery(this).data('field_id'),
                res = {
                    'term': term,
                    'page': page,
                    'context': context
                };
            if (field_id) {
                res['field_id'] = field_id;
            }
            var $el = $(this),
                chained_field = $el.data('select2').opts.chain_field,
                $select_box = $('#' + $el.attr('id')),
                prefix = $el.attr('id').substring(0, $el.attr('id').lastIndexOf("-")+1);

            var $chained_field = $('#' + ((prefix) ? prefix : 'id_') + chained_field);
            res[chained_field] = $chained_field.val();
            return res;
        },
        add_select2_chaining_handlers: function() {
            $('div.field-chained-select-data').each(function () {
                var chained_field = this.getAttribute('data-chained-field'),
                    $el = $(this),
                    //$select_box = $el.siblings('select').eq(0),
                    $select_box = $("#" + $el.attr('data-id')),
                    // Handle the case where the field is from an inline template being added.
                    $chained_field = $('#id_' + chained_field.replace('__prefix__', $select_box.attr('id').split('-')[1])),
                    is_tabular = this.parentNode.tagName.toLowerCase() === 'td',
                    $field_set = $el.closest(is_tabular ? 'tr' : 'fieldset'),
                    $object_block = is_tabular ? $field_set : $field_set.parent(),
                    is_template = !$object_block.is(':visible') && $object_block.hasClass('empty-form');

                // If we have a template, don't do anything - we need to reuse the data.
                if (is_template) {
                    return;
                }

                var field_name = $select_box.attr('name');
                var field_name_tokens = field_name.split('-');
                var real_field_name = field_name.split('-')[field_name_tokens.length - 1];

                // Compatibility with add-another.
                var $chained_add_another = $select_box.prev('#add_id_' + field_name + '.add-another');
                var default_add_another_url;
                if ($chained_add_another.length > 0) {
                    default_add_another_url = $chained_add_another.attr("href");

                }

                var handler_already_attached = false;
                var select_box_name = $select_box.attr('id').split('-')[2];
                var data = $._data($chained_field.get(0), 'events');
                if (data && data.change) {
                    var changelist = data.change;
                    for (var item in changelist) {
                        if (changelist.hasOwnProperty(item) && changelist[item].hasOwnProperty('namespace')) {
                            var changeNamespace = changelist[item].namespace;
                            if (changeNamespace && changeNamespace == select_box_name) {
                                handler_already_attached = true;
                                break;
                            }
                        }
                    }
                }
                $chained_field.off('change.' + select_box_name);
                $chained_field.on('change.' + select_box_name, function () {
                    if ($select_box.select2) {
                        if ($select_box != null && $select_box.data() != null && $select_box.data().select2 != null) {
                            // add-another button related to chained field
                            var add_another_url = $(this).select2("data")[real_field_name + '_add_another_url'];
                            if ($chained_add_another.length > 0) {
                                if (!!add_another_url) {
                                    $chained_add_another.attr('href', add_another_url);
                                    $chained_add_another.show();
                                }
                                else if (!!default_add_another_url) {
                                    $chained_add_another.attr('href', default_add_another_url);
                                    $chained_add_another.show();
                                }
                                else {
                                    $chained_add_another.hide();
                                    $chained_add_another.attr('href', "#");
                                }
                            }
                            $select_box.select2('data', null);
                        }
                        else if (!this.value && $chained_add_another.length > 0) {
                            if (!!default_add_another_url) {
                                $chained_add_another.attr('href', default_add_another_url);
                                $chained_add_another.show();
                            }
                            else
                                $chained_add_another.hide();
                        }
                    }
                });
                if (!handler_already_attached)
                    $chained_field.change();
            });
        }
    };

    $(function () {
        // Add all current chained selects
        django_select2_chained.add_select2_chaining_handlers();
    });
}