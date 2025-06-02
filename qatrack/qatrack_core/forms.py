from django import forms
from django.utils.safestring import mark_safe


class MultipleCharField(forms.CharField):
    widget = forms.SelectMultiple

    def to_python(self, value):
        return value


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class BetterFormMixin:
    """A replacement for django-form-utils BetterForm functionality.
    Provides fieldset support for forms, allowing fields to be grouped into named sections.
    """

    fieldsets = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fieldsets = None

    def get_fieldsets(self):
        """Get the fieldsets for this form.
        
        Returns a list of (name, options) tuples where name is a label for the
        fieldset and options is a dictionary with a 'fields' key mapping to the
        list of field names in the fieldset.
        """
        if self._fieldsets is None:
            self._fieldsets = []
            if self.fieldsets:
                for name, options in self.fieldsets:
                    fields = options.get('fields', ())
                    self._fieldsets.append((name, {
                        'fields': [f for f in fields if f in self.fields],
                        'legend': options.get('legend', name.replace('_', ' ').title()),
                        'classes': options.get('classes', ()),
                        'description': options.get('description', ''),
                    }))
            else:
                self._fieldsets = [(None, {'fields': list(self.fields.keys())})]
        return self._fieldsets

    def as_fieldset(self):
        """Render the form as a series of fieldsets."""
        output = []
        for name, options in self.get_fieldsets():
            output.append(self._html_fieldset(name, options))
        return mark_safe('\n'.join(output))

    def _html_fieldset(self, name, options):
        """Return an individual fieldset as HTML."""
        if name:
            legend = options.get('legend', name)
            classes = ' '.join(options.get('classes', []))
            if classes:
                fieldset_tpl = '<fieldset class="%s">' % classes
            else:
                fieldset_tpl = '<fieldset>'
            output = [fieldset_tpl]
            if legend:
                output.append('<legend>%s</legend>' % legend)
        else:
            output = []

        if options.get('description'):
            output.append('<p class="description">%s</p>' % options['description'])

        for field_name in options['fields']:
            output.append(str(self[field_name]))

        if name:
            output.append('</fieldset>')

        return '\n'.join(output)


class BetterModelForm(BetterFormMixin, forms.ModelForm):
    """A ModelForm subclass that includes fieldset support."""
    pass
