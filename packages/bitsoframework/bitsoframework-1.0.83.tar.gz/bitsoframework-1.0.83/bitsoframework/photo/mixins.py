from django.db.models import SET_NULL, ForeignKey, Model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response

from bitsoframework.media.image.serializers import ImageSerializer
from bitsoframework.media.image.services import ImageService
from bitsoframework.media.serializers import MediaMetadataSerializer
from bitsoframework.media.settings import Image
from bitsoframework.media.utils import is_image


class PhotoModelMixin(Model):
    photo = ForeignKey(Image, null=True, blank="true", on_delete=SET_NULL)

    class Meta:
        abstract = True


class AbstractPhotoViewMixin(object):
    delete_existing_photo = True

    def get_photo_for(self, request, instance):

        serializer = ImageSerializer(instance=instance.photo)

        return Response(serializer.data)

    def create_photo_for(self, request, instance):
        """
        Attach a new photo to the underlying record.
        """

        file = None

        for item in request.data.values():

            if not hasattr(item, "file"):
                continue

            file = item

        if file is None:
            raise ValidationError("A single image file should be uploaded")

        if not is_image(file):
            raise ValidationError("The uploaded file is not a valid image")

        metadata = simplejson.loads(request.data.get("metadata")) if "metadata" in request.data else {}

        serializer = MediaMetadataSerializer(data=metadata)
        serializer.is_valid(raise_exception=True)

        service = ImageService()

        params = {}

        if serializer.validated_data:
            params.update(serializer.validated_data)

        if instance.photo and self.delete_existing_photo:
            instance.photo.delete()

        photo = service.create(file=file, **params)

        instance.photo = photo
        instance.save()

        serializer = ImageSerializer(photo)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_photo_for(self, request, instance):

        service = ImageService()

        serializer = ImageSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if instance.photo:
            service.update(instance.photo, **serializer.validated_data)

        serializer = ImageSerializer(instance.photo)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def remove_photo_for(self, request, instance):

        if instance.photo:
            photo = instance.photo

            instance.photo = None
            instance.save()

            photo.delete()

        return Response(status=status.HTTP_200_OK)


class PhotoViewMixin(AbstractPhotoViewMixin):
    @action(detail=False, methods=["get"], url_path="photo")
    def get_photo(self, request):
        """
        Attach a new photo to the underlying record.
        """

        instance = self.get_photo_owner()

        return self.get_photo_for(request, instance)

    @action(detail=False, methods=["put"], url_path="photo/create",
            parser_classes=(FormParser, MultiPartParser, FileUploadParser))
    def create_photo(self, request):
        """
        Attach a new photo to the underlying record.
        """

        instance = self.get_photo_owner()

        return self.create_photo_for(request, instance)

    @action(detail=False, methods=["patch"], url_path="photo/update")
    def update_photo(self, request):
        """
        Update data for an existing photo record. Notice that updating the
        file itself is not supported.
        """

        instance = self.get_photo_owner()

        return self.update_photo_for(request, instance)

    @action(detail=False, methods=["delete"], url_path="photo/destroy")
    def remove_photo(self, request):
        """
        Remove the currently attached photo to the underlying record.
        """

        instance = self.get_photo_owner()

        return self.remove_photo_for(request, instance)


class MyPhotoViewMixin(PhotoViewMixin):

    def get_photo_owner(self):
        return self.request.user


class PhotoDetailViewMixin(AbstractPhotoViewMixin):
    @action(detail=True, methods=["get"], url_path="photo")
    def get_photo(self, request, pk):
        """
        Attach a new photo to the underlying record.
        """

        instance = self.get_object()

        return self.get_photo_for(request, instance)

    @action(detail=True, methods=["put"], url_path="photo/create",
            parser_classes=(FormParser, MultiPartParser, FileUploadParser))
    def create_photo(self, request, pk):
        """
        Attach a new photo to the underlying record.
        """

        instance = self.get_object()

        return self.create_photo_for(request, instance)

    @action(detail=True, methods=["patch"], url_path="photo/update")
    def update_photo(self, request, pk):
        """
        Update data for an existing photo record. Notice that updating the
        file itself is not supported.
        """

        instance = self.get_object()

        return self.update_photo_for(request, instance)

    @action(detail=True, methods=["delete"], url_path="photo/destroy")
    def remove_photo(self, request, pk):
        """
        Remove the currently attached photo to the underlying record.
        """

        instance = self.get_object()

        return self.remove_photo_for(request, instance)
