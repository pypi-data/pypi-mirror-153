import simplejson
from django_extensions.db.models import ActivatorModel
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from django_filters import utils as df_utils

from bitsoframework.media import settings
from bitsoframework.media.serializers import *
from bitsoframework.media.utils import is_image, get_files, download


class MediaServiceMixin(object):
    """
    shared functionality for services to create and destroy media objects
    """

    avoid_duplicates = settings.AVOID_DUPLICATES

    def import_media(self, record, origin_url, origin_id=None, category=None, **kwargs):

        file = download(origin_url)

        return self.create_media(record, file=file, origin_url=origin_url, origin_id=origin_id, category=category,
                                 **kwargs)

    def create_media(self, record, file=None, category=None, **kwargs):
        """
        @param record: parent record that the media belongs to

        @param file: file that is being attached as a document/image

        @param category: multiple types of files can be uploaded to a record and
                         when this happens we need to pass in the file category
        """
        type = kwargs.pop("type", None)

        if not type and file:
            if is_image(file):
                type = "image"

        if not type:
            type = "document"

        service_class = registry.get_service(type)
        service = service_class(parent=record)

        if file and self.avoid_duplicates:
            checksum = settings.CHECKSUM_CALCULATOR(file)
            media = service.filter(checksum=checksum, status=ActivatorModel.ACTIVE_STATUS).first()
            if media:
                return media
            else:
                kwargs["checksum"] = checksum

        media = service.create(category=category, file=file, **kwargs)

        return media

    def update_media(self, record, media_id, media_type, **kwargs):
        """
        Update media information such as name or description for the given
        media object within the given record.

        Note that updating media's file is not supported. This can only be done
        by deleting the existing file and adding a new media record instead.
        """

        service = record.media_service_from_type(media_type)

        media = service.filter(id=media_id).get()

        return service.update(media, **kwargs)

    def destroy_media(self, record, media_id, media_type):

        service = record.media_service_from_type(media_type)

        service.delete(id__in=[media_id])


class MediaViewMixin(object):
    list_media_serializer_class = MediaSerializer
    create_media_response_serializer_class = MediaSerializer
    media_service_class = MediaServiceMixin
    """
    shared functionality for views to interact with media objects
    """

    @action(detail=True, url_path="media")
    def list_media(self, request, pk):

        return self.list_media_by_type(request, pk, None)

    @action(detail=True, url_path="media/(?P<media_type>[-\w]+)")
    def list_media_by_type(self, request, pk, media_type):
        """
        Retrieve all media documents attached to the underlying record.

        @param media_type: the type of media (image|document)
        """

        instance = self.get_object()

        media_types = [media_type] if media_type else registry.media_types

        media = []

        for media_type in media_types:

            queryset = instance.media_service_from_type(media_type).all()

            filterset_class = registry.get_filterset(media_type)
            filterset = filterset_class(queryset=queryset, request=request, data=request.query_params)

            if not filterset.is_valid():
                raise df_utils.translate_validation(filterset.errors)

            queryset = filterset.filter_queryset(queryset)

            for item in queryset:
                media.append(item)

        serializer = self.list_media_serializer_class(instance=media, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["delete"], url_path="media/destroy/(?P<media_id>[\d+]+)/(?P<media_type>[-\w]+)")
    def destroy_media(self, request, pk, media_id, media_type):
        """
        Destroys an existing media entry within the given object, permanently 
        deleting all of its metadata and attached files - including thumbnails 
        for images.
        
        @param media_id: the media's primary key
        
        @param media_type: the type of media (image|document)
        """

        instance = self.get_object()

        service = self.media_service_class()

        service.destroy_media(instance, media_id, media_type)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["put"], url_path="media/create",
            parser_classes=(FormParser, MultiPartParser, FileUploadParser))
    def create_media(self, request, pk, *args, **kwargs):
        """
        Attach a new media content to the bounding record.
                    
        @param metadata: An array of objects (JSON), each object containing name
            of the document being uploaded. Note that while sending multiple files,
            both file and metadata should match size and order.
        """

        record = self.get_object()

        service = self.media_service_class()

        documents = MediaViewMixin._create_media(request, service, record)

        serializer = self.create_media_response_serializer_class(instance=documents, many=True)

        return Response(serializer.data, status=201)

    @classmethod
    def _create_media(cls, request, service, record, **kwargs):

        metadata = simplejson.loads(request.data.get("metadata")) if "metadata" in request.data else None
        data = simplejson.loads(request.data.get("data")) if "data" in request.data else None

        documents = list()

        files = get_files(request)

        i = 0
        for file in files:

            params = {
                **kwargs
            }

            if metadata:
                params.update(metadata[i])

            documents.append(service.create_media(record, file=file, **params))

            i += 1

        if data:

            for item in data:
                serializer_class = registry.get_serializer(item.get("type"))
                serializer = serializer_class(data=item)
                serializer.is_valid(raise_exception=True)

                documents.append(service.create_media(record, **serializer.validated_data))

        return documents

    @action(detail=True, methods=["patch"], url_path="media/update/(?P<media_id>[\d+]+)/(?P<media_type>[-\w]+)")
    def update_media(self, request, pk, media_id, media_type, *args, **kwargs):
        """
        Update data for an existing media record. Notice that updating the
        file itself is not supported.
        """

        record = self.get_object()

        service = self.media_service_class()

        serializer_class = registry.get_serializer(media_type)

        files = get_files(request)

        params = {}

        # attach file being updated
        if len(files) == 1:
            params["file"] = files[0]

        data = simplejson.loads(request.data.get("metadata")) if "metadata" in request.data else request.data

        if data:
            serializer = serializer_class(data=data, partial=True)
            serializer.is_valid(raise_exception=True)

            params.update(serializer.validated_data)

        params.update(kwargs)

        media = service.update_media(record, media_id, media_type, **params)

        serializer = serializer_class(instance=media)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaModelMixin(object):
    """
    shared functionality for models that manage bitso media objects.
    """

    def media_service_from_type(self, media_type):
        """
        Look up for a media service based on its type
        
        @param media_type: the type of media service
        
        @return service for the given media type (either ImageService or DocumentService)
        """
        from bitsoframework.media.settings import registry

        service_class = registry.get_service(media_type)

        return service_class(parent=self)

    def get_media(self, media_type=None, **kwargs):
        result = []

        if media_type:
            for record in self.media_service_from_type(media_type).filter(**kwargs):
                result.append(record)
        else:

            from bitsoframework.media.settings import registry

            for media_type in registry.media_types:

                for record in self.media_service_from_type(media_type).filter(**kwargs):
                    result.append(record)

        return result

    @property
    def media(self):
        """
        Encapsulate all media documents and images. If there are different categories
        of documents this method will need to be overridden.
        """

        return self.get_media()

    def copy(self, **kwargs):
        """
        Copies all underlying documents under new instances/paths in the remote server.
        :param kwargs:
        :return:
        """

        new_model = super(MediaModelMixin, self).copy(**kwargs)

        for document in self.media:
            document.copy(parent_id=new_model.id)

        return new_model
