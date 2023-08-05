from bitsoframework.utils import lists


def get_delta_fields(detail_serializer, search_serializer):
    detail_fields = list(detail_serializer().fields.keys())
    search_fields = list(search_serializer().fields.keys())

    if detail_fields == search_fields:
        return ['id', ]

    delta_fields = lists.remove_all(lists.copy(detail_fields), search_fields)

    return delta_fields
