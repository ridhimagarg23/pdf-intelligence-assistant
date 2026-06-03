from docling.document_converter import DocumentConverter


def extract_document(pdf_path):

    converter = DocumentConverter()

    result = converter.convert(pdf_path)

    return result.document.export_to_markdown()