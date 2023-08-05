from django.db.models.signals import post_save
from rest_framework import exceptions, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings

from bitsoframework.serializers import ListIDSerializer


class CreateBulkModelMixin(object):
    """
    Create model instances in bulk.
    """

    send_create_signals = True

    @action(detail=False, methods=["POST"], url_path="bulk_create")
    def create_bulk(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = self.perform_create_bulk(serializer)
        if isinstance(self, ActionSerializerView):
            serializer = self.get_serializer_for("list", instances, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create_bulk(self, serializer):
        instances = serializer.save()

        if self.send_create_signals:
            for instance in instances:
                post_save.send(instance.__class__, instance=instance, created=True)

        return instances

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateBulkModelMixin(object):
    """
    Update model instances in bulk.
    """

    send_update_signals = True

    @action(detail=False, methods=["PATCH"], url_path="bulk_update")
    def update_bulk(self, request, *args, **kwargs):
        instances = self.get_update_instances(request.data)

        serializer = self.get_serializer(
            instances, data=request.data, partial=True, many=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update_bulk(serializer)

        return Response(serializer.data)

    def perform_update_bulk(self, serializer):
        instances = serializer.save()

        if self.send_update_signals:
            for instance in instances:
                post_save.send(instance.__class__, instance=instance, created=False)

        return instances

    def get_update_ids(self, data, field="id", unique=True):

        if isinstance(data, list):
            id_list = [int(x[field]) for x in data]

            if unique and len(id_list) != len(set(id_list)):
                raise ValidationError("Multiple updates to a single {} found".format(field))

            return id_list

        return [data[field]]

    def get_update_instances(self, data, field="id"):

        pks = self.get_update_ids(data, field=field)

        instances = list(self.get_queryset().filter(id__in=pks))

        result = []
        for pk in pks:
            for instance in instances:
                if pk == getattr(instance, field):
                    result.append(instance)
                    break

        return result


class DestroyBulkModelMixin(object):
    """
    Destroy model instances in bulk.
    """

    @action(detail=False, methods=["DELETE"], url_path="bulk_destroy")
    def destroy_bulk(self, request, *args, **kwargs):
        serializer = ListIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_destroy_bulk(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy_bulk(self, serializer):
        instances = self.get_queryset().filter(id__in=serializer.validated_data.get("ids"))
        instances.delete()


class MethodSerializerView(object):
    """
    Utility class for get different serializer class by http method.
    For example:
    method_serializer_classes = {
        ("GET", ): MyModelListViewSerializer,
        ("PUT", "PATCH"): MyModelCreateUpdateSerializer
    }
    """
    http_method_serializer_classes = None

    def get_serializer_class(self):
        assert self.http_method_serializer_classes is not None, (
                "Expected view %s should contain http_method_serializer_classes "
                "to get right serializer class." %
                (self.__class__.__name__,)
        )
        for methods, serializer_cls in self.http_method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)


class ActionSerializerView(object):
    """
    Utility class for get different serializer class by action name.
    For example:
    action_serializer_classes = {
        ("create", ): MyModelListViewSerializer,
        ("retrieve", "update"): MyModelCreateUpdateSerializer
    }
    """
    action_serializer_classes = None

    def get_serializer_for(self, action, *args, **kwargs):

        kwargs['context'] = self.get_serializer_context()

        return self.get_serializer_class_for(action)(*args, **kwargs)

    def get_serializer_class_for(self, action):
        if self.action_serializer_classes:
            for actions, serializer_cls in self.action_serializer_classes.items():
                if action in actions:
                    return serializer_cls

        return super(ActionSerializerView, self).get_serializer_class()

    def get_serializer_class(self):
        return self.get_serializer_class_for(self.action)


class SmartQuerysetView(object):

    def get_queryset(self):

        queryset = super(SmartQuerysetView, self).get_queryset()

        serializer_class = self.get_serializer_class()

        if hasattr(serializer_class, "Meta"):

            if hasattr(serializer_class.Meta, "select_related"):
                queryset = queryset.select_related(*serializer_class.Meta.select_related)

            if hasattr(serializer_class.Meta, "prefetch_related"):
                queryset = queryset.prefetch_related(*serializer_class.Meta.prefetch_related)

            if hasattr(serializer_class.Meta, "select_only"):
                queryset = queryset.only(*serializer_class.Meta.select_only)

            elif hasattr(serializer_class.Meta, "fields") and isinstance(serializer_class.Meta.fields, (list, tuple)):
                queryset = queryset.only(*serializer_class.Meta.fields)

        return queryset


class AbstractViewSet(ActionSerializerView,
                      SmartQuerysetView,
                      viewsets.GenericViewSet):
    """
    Base abstract viewset for convenience
    """
    pass
