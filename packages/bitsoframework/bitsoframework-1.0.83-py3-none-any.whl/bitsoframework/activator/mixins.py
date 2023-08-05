import datetime

from django_extensions.db.models import ActivatorModel, TimeStampedModel
from rest_framework.decorators import action
from rest_framework.response import Response

from bitsoframework.serializers import ListIDSerializer
from bitsoframework.utils.models import set_attrs


class ActivateModelMixin(object):

    def get_serializer_class(self):
        if self.action == 'activate':
            return ListIDSerializer

        return super(ActivateModelMixin, self).get_serializer_class()

    @action(detail=False, methods=["POST"])
    def activate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        records = self.get_queryset().filter(id__in=serializer.data.get("ids"))

        data = {
            "status": ActivatorModel.ACTIVE_STATUS,
            "activate_date": datetime.datetime.now()
        }

        if issubclass(records.model, TimeStampedModel):
            data["modified"] = datetime.datetime.now()

        # TODO: find a way to trigger signals on queryset natively...

        for record in records:
            set_attrs(record, data)
            record.save(update_fields=data.keys())

        # records.update(**data)

        # for record in records:
        #    post_save.send(record.__class__, instance=record, created=False)

        return Response("OK")


class DeactivateModelMixin(object):

    def get_serializer_class(self):
        if self.action == 'deactivate':
            return ListIDSerializer

        return super(DeactivateModelMixin, self).get_serializer_class()

    @action(detail=False, methods=["POST"])
    def deactivate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        records = self.get_queryset().filter(id__in=serializer.data.get("ids"))

        data = {
            "status": ActivatorModel.INACTIVE_STATUS,
            "deactivate_date": datetime.datetime.now()
        }

        if issubclass(records.model, TimeStampedModel):
            data["modified"] = datetime.datetime.now()

        # TODO: find a way to trigger signals on queryset natively...
        for record in records:
            set_attrs(record, data)
            record.save(update_fields=data.keys())

        # records.update(**data)
        # for record in records:
        #    post_save.send(records.model, instance=record, created=False)

        return Response("OK")


class ActiveModelMixin(object):

    @action(detail=False)
    def active(self, request, *args, **kwargs):
        """
        List active queryset.
        """
        queryset = self.filter_queryset(self.get_queryset().filter(status=ActivatorModel.ACTIVE_STATUS))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InactiveModelMixin(object):

    @action(detail=False)
    def inactive(self, request, *args, **kwargs):
        """
        List inactive queryset.
        """
        queryset = self.filter_queryset(self.get_queryset().filter(status=ActivatorModel.INACTIVE_STATUS))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActivatorModelMixin(ActivateModelMixin,
                          DeactivateModelMixin,
                          ActiveModelMixin,
                          InactiveModelMixin):
    pass
