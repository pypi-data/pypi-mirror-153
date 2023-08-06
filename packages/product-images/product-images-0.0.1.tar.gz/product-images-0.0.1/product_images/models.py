
from PIL import Image
from watermarks.utils import insert_watermark

from os.path import basename
from urllib.request import urlretrieve

from django.db import models
from django.core.files import File
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail


class ProductImage(models.Model):

    product = models.ForeignKey(
        'products.Product',
        verbose_name=_("Product"),
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    file = models.ImageField(
        verbose_name=_("File"),
        upload_to='product_images',
        max_length=255)

    order = models.PositiveIntegerField(_('Ordering'))

    def __str__(self):
        return str(self.product)

    def get_preview_url(self):
        try:
            return get_thumbnail(self.file.file, '100').url
        except IOError:
            pass

        return ''

    @classmethod
    def create_from_url(cls, url):

        result = urlretrieve(url)

        return cls.objects.create(
            file=File(open(result[0], 'rb'), name=basename(url)))

    def compress(self):

        max_size = 2000, 2000

        try:
            img = Image.open(self.file.path)
            img.thumbnail(max_size, Image.ANTIALIAS)
            img.save(self.file.path, quality=70)
        except Exception as e:
            print(e)

    class Meta:
        db_table = 'products_productimage'
        ordering = ['order']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class LogoField(models.ImageField):

    def __init__(
            self,
            verbose_name=_('Logo'),
            upload_to='logos',
            blank=True,
            null=True,
            max_length=255,
            editable=False,
            *args, **kwargs):

        super(LogoField, self).__init__(
            verbose_name=verbose_name,
            upload_to=upload_to,
            blank=blank,
            null=null,
            max_length=max_length,
            editable=editable,
            *args, **kwargs)


def add_product_image_watermark(sender, instance, created, **kwargs):

    if not created:
        return

    instance.compress()

    try:
        insert_watermark('product', instance.file.path)
    except Exception as e:
        pass


post_save.connect(add_product_image_watermark, sender=ProductImage)
