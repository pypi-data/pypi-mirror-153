
from django.core.files import File


def refresh_logo(instance):

    first_image = instance.images.first()

    if first_image:
        file = File(open(first_image.file.path, 'rb'))
        instance.logo.save(first_image.file.name, file)
    else:
        instance.logo.delete()
