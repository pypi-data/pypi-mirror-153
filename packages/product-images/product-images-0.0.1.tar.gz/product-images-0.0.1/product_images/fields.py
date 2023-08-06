
from django import forms
from django.utils.translation import ugettext_lazy as _

from product_images.widgets import ImagesFormFieldWidget
from product_images.forms import ImagesForm


class ImagesFormField(forms.Field):

    form = None
    widget = ImagesFormFieldWidget

    def init_form(self, *args, **kwargs):
        self.form = ImagesForm(*args, **kwargs)
        self.widget.form = self.form

    def clean(self, *args, **kwargs):
        if not self.form.is_valid():
            raise forms.ValidationError(_('Form is invalid.'))

        return self.form.cleaned_data

    def commit(self, *args, **kwargs):
        return self.form.commit(*args, **kwargs)
