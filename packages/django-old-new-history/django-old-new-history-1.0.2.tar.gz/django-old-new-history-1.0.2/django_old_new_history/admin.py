from django.utils.text import capfirst
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class DjangoOldNewHistory:
    object_history_template = 'django_old_new_history/object_history.html'

    def construct_change_message(self, request, form, formsets, add=False):
        add_and_delete_message = []
        change_order_list = ""
        table_header = f"Changed field <table border='1' style='border-bottom: 1.3px solid #cccccc;'>" \
                       f"<tbody>" \
                       f"<tr style='background:#f6f6f6;'>" \
                       f"<th>Field</th>" \
                       f"<th>Old value</th>" \
                       f"<th>New value</th>" \
                       f"<th>Comment</th></tr>"
        if form.changed_data:
            change_order_list = table_header
            for field in form.changed_data:
                field_name = capfirst(self.model._meta.get_field(field).verbose_name)
                if form.initial[field] is not None and hasattr(form.fields[field], 'queryset'):
                    try:
                        old_value = form.fields[field].queryset.get(id=form.initial[field])
                    except Exception:
                        old_value = ''
                    else:
                        try:
                            old_value = old_value.__unicode__()
                        except Exception:
                            old_value = str(old_value)
                else:
                    old_value = form.initial[field]
                new_value = form.cleaned_data[field]

                if not field_name:
                    field_name = field

                change_order_list = f'{change_order_list}' \
                                    f'<tr>' \
                                    f'<td>{field_name}</td>' \
                                    f'<td>{old_value}</td>' \
                                    f'<td>{new_value}</td>' \
                                    f'<td></td>' \
                                    f'</tr>'

        if formsets:
            for formset in formsets:
                for added_object in formset.new_objects:
                    add_and_delete_message.append(_('<li>Added %(name)s "%(object)s".</li>')
                                                  % {'name': force_text(added_object._meta.verbose_name),
                                                     'object': force_text(added_object)})
                for changed_object, changed_fields in formset.changed_objects:
                    for form in formset.initial_forms:
                        if form.instance != changed_object:
                            continue
                        if not change_order_list:
                            change_order_list = table_header
                        for field in changed_fields:
                            field_name = capfirst(changed_object._meta.get_field(field).verbose_name)
                            if form.initial[field] is not None and hasattr(form.fields[field], 'queryset'):
                                old_value = form.fields[field].queryset.get(id=form.initial[field]).__unicode__()
                            else:
                                old_value = form.initial[field]
                            new_value = form.cleaned_data[field]
                            if not field_name:
                                field_name = field

                            change_order_list = f'{change_order_list}' \
                                                f'<tr>' \
                                                f'<td>{field_name}</td>' \
                                                f'<td>{old_value}</td>' \
                                                f'<td>{new_value}</td>' \
                                                f'<td>{force_text(changed_object._meta.verbose_name)} ' \
                                                f'"{force_text(changed_object)}".</td>' \
                                                f'</tr>'

                for deleted_object in formset.deleted_objects:
                    add_and_delete_message.append(_('<li>Deleted %(name)s "%(object)s".</li>')
                                                  % {'name': force_text(deleted_object._meta.verbose_name),
                                                     'object': force_text(deleted_object)})
        if change_order_list:
            add_and_delete_message.append(f'<li>{change_order_list}</tbody></table></li>')
        change_message = ' '.join(add_and_delete_message)

        if change_message:
            change_message = format_html(f'<ul>{change_message}</ul>')
            return change_message
        else:
            return 'No fields changed'

