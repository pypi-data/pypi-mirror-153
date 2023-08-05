from django.conf import settings
from django.utils.functional import cached_property
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from firebase_admin import firestore

from bitsoframework.middleware import get_user, _active
from bitsoframework.utils import lists
from bitsoframework.utils.booleans import to_boolean


def firestore_batch_enabled(auto_commit=True):
    def decorator(func=None):
        def wrapper(*args, **kwargs):
            middleware = FirestoreBatchMiddleware(func, auto_commit)

            return middleware(*args, **kwargs)

        return wrapper

    return decorator


class FirestoreBatchMiddleware(object):

    def __init__(self, get_response, auto_commit=True):
        FirestoreChangeSynchronizer.batch_enabled = True

        self.get_response = get_response
        self.auto_commit = auto_commit

    def __call__(self, *args, **kwargs):
        response = self.get_response(*args, **kwargs)

        if self.auto_commit:
            FirestoreBatchMiddleware.batch_manager().commit()

        return response

    @classmethod
    def batch_manager(cls):
        if not hasattr(_active, "firestore_batch_manager"):
            _active.firestore_batch_manager = FirestoreBatchManager()

        return _active.firestore_batch_manager


class FirestoreBatch(object):
    _batch = None

    @cached_property
    def store(self):
        return firestore.client()

    @property
    def batch(self):
        if not self._batch:
            self._batch = self.store.batch()
        return self._batch

    def __init__(self):
        self.sets = {}

    def set(self, path, data, merge=False):

        self.sets[path] = {
            "data": data,
            "merge": merge
        }

    def commit(self):

        total = len(self.sets.keys())

        print("Committing %i transactions in firestore" % (total,))

        for path, item in self.sets.items():
            self.batch.set(self.store.document(path), item.get("data"), merge=item.get("merge"))

        self.batch.commit()


class FirestoreBatchManager(object):
    _batch = None

    @property
    def batch(self):
        if not self._batch:
            self._batch = FirestoreBatch()
        return self._batch

    def commit(self):
        if self._batch:
            self._batch.commit()
            self._batch = None


def log_change(collection, *args, **kwargs):
    handler = FirestoreChangeSynchronizer(collection=collection)
    handler.log(*args, **kwargs)
    return handler


class FirestoreChangeSynchronizer(object):

    def __init__(self, collection, enabled=None, debug=None, batch_enabled=None, batch_manager=None,
                 snapshot_enabled=None, audit_enabled=None):
        self.collection = collection
        self.transactions = []

        self._enabled = enabled
        self._snapshot_enabled = snapshot_enabled
        self.debug = to_boolean(debug, getattr(settings, 'BITSO_FIRESTORE_SYNC_DEBUG', True))
        self.batch_enabled = to_boolean(batch_enabled, getattr(settings, 'BITSO_FIRESTORE_SYNC_BATCH', False))
        self.batch_manager = batch_manager or (FirestoreBatchMiddleware.batch_manager() if self.batch_enabled else None)
        self.audit_enabled = to_boolean(audit_enabled, getattr(settings, 'BITSO_FIRESTORE_SYNC_AUDIT', False))

    @property
    def enabled(self):
        return to_boolean(self._enabled, getattr(settings, 'BITSO_FIRESTORE_SYNC_ENABLED', True))

    @property
    def snapshot_enabled(self):
        return to_boolean(self._enabled, getattr(settings, 'BITSO_FIRESTORE_SYNC_SNAPSHOT', True))

    @cached_property
    def store(self):
        return firestore.client()

    def get_path(self, record=None, record_id=None):
        values = [str(value) for value in (lists.as_list(self.collection) + [record_id or record.id])]
        path = "/".join(values)
        if self.debug:
            print("Firestore path: " + path)
        return path

    def get(self, record=None, record_id=None):
        path = self.get_path(record, record_id)
        return self.store.document(path)

    def log(self, record, record_id=None, modified_by=None, is_delete=False, **kwargs):
        if not self.enabled:
            return

        record_id = record_id or record.id

        if not modified_by:
            user = get_user()
            if user:
                modified_by = user.id

        data = {
            "id": record_id,
            "modified_by": modified_by
        }

        if isinstance(record, ActivatorModel):
            data.update({
                'status': record.status
            })

        if isinstance(record, TimeStampedModel):
            data.update({
                'modified': record.modified
            })

        data.update(kwargs)

        if is_delete:
            data["deleted"] = True

        if self.batch_enabled:

            if self.audit_enabled:
                self.batch_manager.batch.set(self.get_path(record, record_id), data, merge=True)

            if self.snapshot_enabled:
                self.batch_manager.batch.set(self.get_path(record_id="snapshot"), data)

        else:

            if self.audit_enabled:
                self.store.document(self.get_path(record, record_id)).set(data, merge=True)

            if self.snapshot_enabled:
                self.store.document(self.get_path(record_id="snapshot")).set(data)
