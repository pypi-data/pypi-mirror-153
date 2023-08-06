
import json

from django import forms
from django.urls import reverse_lazy

from product_images.utils import refresh_logo
from product_images.models import ProductImage


class ImagesForm(forms.ModelForm):

    images = forms.ModelMultipleChoiceField(
        ProductImage.objects.none(), required=False)

    def __init__(
            self,
            data=None,
            files=None,
            instance=None,
            initial=None,
            **kwargs):

        self._images = instance.images.all() if instance else []

        initial = {'images': [i.id for i in self._images or []]}

        super().__init__(
            data=data,
            files=files,
            instance=instance,
            initial=initial,
            **kwargs)

        if self.is_bound:
            self.fields['images'].queryset = ProductImage.objects.all()

    @property
    def serialized_images(self):
        return json.dumps([
            {'id': i.id, 'url': i.get_preview_url()} for i in self._images
        ])

    @property
    def upload_url(self):
        return reverse_lazy('product-images:upload')

    def commit(self, instance):

        instance.images.all().update(product=None)

        ordering = {
            img_id: i for i, img_id in enumerate(self.data.getlist('images'))
        }

        for img in self.cleaned_data.get('images') or []:
            img.product = instance
            img.order = ordering[str(img.id)]
            img.save(update_fields=['product', 'order'])

        refresh_logo(instance)

        return instance

    class Media:
        css = {
            'all': [
                'file-manager/file-manager.css',
                'dropzone/dropzone.min.css'
            ]
        }
        js = [
            'dropzone/dropzone.min.js',
            'file-manager/file-manager.js',
        ]

    class Meta:
        model = ProductImage
        fields = ['images']


class UploadImageForm(forms.Form):

    url = forms.URLField(required=False)
    file = forms.ImageField(required=False)
