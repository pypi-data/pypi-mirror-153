import os
import shutil
import sys
import tempfile

from django.core.files.base import File

from bitsoframework.media.services import MediaService
from bitsoframework.media.settings import (PREVIEW_ENABLED, PREVIEW_HEIGHT,
                                           PREVIEW_WIDTH, Document, Image)
from bitsoframework.utils import files


class DocumentService(MediaService):
    """
    Service used to manage the lifecycle of the Document model.
    """

    model_class = Document

    def filter(self, **kwargs):
        queryset = super(DocumentService, self).filter(**kwargs)

        if PREVIEW_ENABLED:
            queryset = queryset.select_related("preview")

        return queryset

    def create(self, file=None, category=None, generate_preview=PREVIEW_ENABLED, **kwargs):

        document = super(DocumentService, self).create(file=file, category=category, **kwargs)

        if generate_preview and not kwargs.get("preview"):
            self.create_preview(document, file)

        return document

    def create_preview(self, document, file):
        from preview_generator.manager import PreviewManager

        preview_file_path = None
        temp_source_path = None

        try:
            temp_dir = tempfile.gettempdir()

            try:
                temp_source_path = document.file.path
            except:
                temp_source_path = tempfile.mktemp(files.get_extension(file.name))

                with open(temp_source_path, 'wb') as outfile:
                    document.file.open(mode='rb')
                    shutil.copyfileobj(document.file, outfile)

            preview_manager = PreviewManager(temp_dir, create_folder=True)

            preview_file_path = preview_manager.get_jpeg_preview(temp_source_path,
                                                                 width=PREVIEW_WIDTH,
                                                                 height=PREVIEW_HEIGHT)

            if preview_file_path:
                preview_file = File(file=None, name=preview_file_path)
                preview_file.open(mode='rb')

                preview = Image(file=preview_file)
                # temporarily store preview_source until one-to-one is loaded after save
                preview.preview_source = document
                preview.save()

                document.preview = preview
                document.old_file = document.file  # avoid re-uploading the file
                document.save()

        except Exception as e:
            import traceback
            print("Could not generate preview for file: " + str(file) + " due " + str(e))
            print(traceback.format_exception(None,  # <- type(e) by docs, but ignored
                                             e, e.__traceback__),
                  file=sys.stderr, flush=True)
        finally:
            if preview_file_path:
                os.remove(preview_file_path)
