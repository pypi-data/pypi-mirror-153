import PyPDF2
import textract
from django.core.files import File


def get_text(file_path, language="eng", preferences=["textract", "pypdf"], include_all=False):
    """
    Extract text for all pages of the given PDF document
    """
    if isinstance(file_path, File):
        f = file_path.open('rb')
        file_path = f.name
    elif isinstance(file_path, str, ):
        f = open(file_path, 'rb')
    else:
        f = file_path

    text = None

    result = []

    for preference in preferences:

        if preference == "textract":

            text = textract.process(file_path, method='tesseract', language=language).decode("UTF-8")

        elif preference == "pypdf":

            pdf = PyPDF2.PdfFileReader(f)

            num_pages = pdf.numPages
            count = 0
            text = ""

            while count < num_pages:
                page = pdf.getPage(count)
                count += 1
                text += page.extractText()

        if text:
            if include_all:
                result.append(text)

            else:
                return text

    return result if include_all else None
