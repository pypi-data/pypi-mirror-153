# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''
from django.forms import CharField
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from django import forms

class EmailLookupWidget(forms.TextInput):
    class Media:
        js = ('https://unpkg.com/@yaireo/tagify',
              'https://unpkg.com/@yaireo/tagify/dist/tagify.polyfills.min.js',
              static('/tagify/tagify.widget.js'))
        css = {"all": ('https://unpkg.com/@yaireo/tagify/dist/tagify.css',)}

    #def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["type"] = self.input_type
        if 'class' not in context["widget"]["attrs"] :
            context["widget"]["attrs"]['class']=''
        context["widget"]["attrs"]['class'] += ' djtagify'
        return context

    # def value_from_datadict(self, data, files, name):
    #     # eg. 'members': ['|229|4688|190|']
    #     # backward compatibility ['1,3,4']
    #     ids = data.get(name, '')
    #     if "," in ids:
    #         return [val for val in ids.split(',') if val]
    #
    #     return super(EmailLookupWidget, self).value_from_datadict(
    #         data, files, name)


class EmailLookup(CharField):
    widget = EmailLookupWidget

    def __init__(self, url, *args, **kwargs):
        self.url = url
        return super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['data-href'] = self.url
        return attrs
    # def clean(self, value):
    #     if not value and self.required:
    #         raise ValidationError(self.error_messages['required'])
    #     if not value:
    #         return None
    #     return value  # a list of primary keys from widget value_from_datadict


