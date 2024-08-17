import logging
import subprocess

import mammoth
from docx2pdf import convert
from pyhtml2pdf import converter
from selenium.common import InvalidArgumentException
from spire.pdf import *

from converter.constants.path import get_folder_save_file


def convert_docx_to_html(docx_file):
    save_folder = get_folder_save_file()
    docx_file.save(save_folder + '/input.docx')
    with open(save_folder + '/input.docx', 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

        style = """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """
        html = f"<html><head>{style}</head><body>{html}</body></html>"

        with open(save_folder + '/output.html', 'w', encoding='utf-8') as f:
            f.write(html)
    return save_folder + '/output.html'


def convert_pdf_to_html(pdf_file):
    save_folder = get_folder_save_file()
    pdf_file.save(save_folder + '/input.pdf')
    doc = PdfDocument()
    doc.LoadFromFile(save_folder + '/input.pdf')
    convert_options = doc.ConvertOptions
    convert_options.is_embed_font = True
    convert_options.is_embed_image = True
    convert_options.is_embed_css = True
    doc.SaveToFile(save_folder + '/output.html', FileFormat.HTML)
    doc.Dispose()
    return save_folder + '/output.html'


def convert_docx_to_pdf(docx_file):
    save_folder = get_folder_save_file()
    input_path = save_folder + '/input.docx'
    output_path = save_folder + '/input.pdf'
    docx_file.save(input_path)

    try:
        if os.name == 'nt':
            convert(input_path, output_path)
        else:
            subprocess.run(['libreoffice', '--convert-to', 'pdf', input_path, '--outdir', save_folder], check=True,
                           capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting DOCX to PDF: {e}")
        raise RuntimeError(f"Failed to convert DOCX to PDF: {e}")

    return output_path


def convert_html_to_pdf(html_file):
    save_folder = get_folder_save_file()
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    input_file_path = os.path.join(save_folder, 'input.html')
    html_file.save(input_file_path)

    input_file_url = f'file://{input_file_path}'

    output_file_path = os.path.join(save_folder, 'output.pdf')

    try:
        converter.convert(input_file_url, output_file_path)
    except InvalidArgumentException as e:
        print(f"Lỗi InvalidArgumentException: {e}")
        raise
    except Exception as e:
        print(f"Lỗi khác khi chuyển đổi HTML sang PDF: {e}")
        raise

    return output_file_path


def convert_html_to_docx(html_file):
    save_folder = get_folder_save_file()
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    input_html_file_path = os.path.join(save_folder, 'input.html')
    html_file.save(input_html_file_path)

    output_pdf_file_path = os.path.join(save_folder, 'output.pdf')

    output_docx_file_path = os.path.join(save_folder, 'output.docx')

    input_file_url = f'file://{input_html_file_path}'

    try:
        converter.convert(input_file_url, output_pdf_file_path)
    except InvalidArgumentException as e:
        print(f"Lỗi InvalidArgumentException: {e}")
        raise
    except Exception as e:
        print(f"Lỗi khác khi chuyển đổi HTML sang PDF: {e}")
        raise

    try:
        doc = PdfDocument()
        doc.LoadFromFile(output_pdf_file_path)
        doc.SaveToFile(output_docx_file_path, FileFormat.DOCX)
        doc.Dispose()
    except Exception as e:
        print(f"Lỗi khi chuyển đổi PDF sang DOCX: {e}")
        raise

    return output_docx_file_path


def convert_pdf_to_docx(pdf_file):
    save_folder = get_folder_save_file()
    pdf_file.save(save_folder + '/input.pdf')
    doc = PdfDocument()
    doc.LoadFromFile(save_folder + '/input.pdf')
    doc.SaveToFile(save_folder + '/output.docx', FileFormat.DOCX)
    doc.Dispose()
    return save_folder + '/output.docx'
