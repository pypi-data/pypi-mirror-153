import os
from tempfile import mkdtemp

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.test import TestCase

from bitsoframework.media.settings import Image
from .models import MyProduct


class ImageServiceTestCase(TestCase):
    def setUp(self):
        image_field = Image()._meta.get_field_by_name('file')[0]

        self.product = MyProduct.objects.create(name="Macbook Pro 15\"")

        image_field.storage = FileSystemStorage(location=mkdtemp(), base_url="/")

    def test_crud(self):
        """Make sure images are attached, retrieved and deleted"""

        f = File(open(settings.BASE_DIR + "/bitsoframework/tmp/Photo-1.jpg"))

        photo = self.product.images.save(name="Photo 1", file=f)
        photo_path = photo.file.file.name

        self.assertTrue(os.path.exists(photo_path), "Photo does not exist on local path")
        self.assertEqual(photo.width, 350.0, "Photo 1's width does not match")
        self.assertEqual(photo.height, 277.0, "Photo 1's height does not match")

        self.product = MyProduct.objects.get(id=self.product.id)

        self.assertEqual(self.product.images.filter().count(), 1, "Photo 1 is not created")

        photo = self.product.images.filter()[0]

        self.assertEqual(photo.width, 350.0, "Photo 1's width does not match")
        self.assertEqual(photo.height, 277.0, "Photo 1's height does not match")

        photo.file = File(open(settings.BASE_DIR + "/bitsoframework/tmp/Photo-2.jpg"))
        photo.save()

        self.assertTrue(os.path.exists(photo_path), "Photo should exist on same local path")
        self.assertEqual(self.product.images.filter().count(), 1, "Photo should be updated...")

        self.assertEqual(photo.width, 275.0, "Photo 2's width does not match")
        self.assertEqual(photo.height, 183.0, "Photo 2's height does not match")

        photo.delete()

        self.assertFalse(os.path.exists(photo_path), "Photo should not exist on local path")
        self.assertEqual(self.product.images.filter().count(), 0, "Photo should be deleted...")
