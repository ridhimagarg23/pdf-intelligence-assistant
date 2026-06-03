from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions


def extract_document(pdf_path):

    pipeline_options = PdfPipelineOptions()

    # Temporary: disable OCR for Streamlit deployment
    pipeline_options.do_ocr = False

    converter = DocumentConverter(
        pipeline_options=pipeline_options
    )

    result = converter.convert(pdf_path)

    return result.document.export_to_markdown()