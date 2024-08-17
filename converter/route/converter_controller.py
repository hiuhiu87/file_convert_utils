from flasgger import swag_from
from flask import Blueprint, request, send_file

from converter.service.converter_service import convert_docx_to_pdf, convert_docx_to_html, \
    convert_pdf_to_html, convert_html_to_pdf, convert_html_to_docx

converter = Blueprint('converter', __name__)


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@converter.route('/api/convert', methods=['POST'])
@swag_from({
    'tags': ['File Conversion'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'File to be converted'
        },
        {
            'name': 'conversion_type',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Type of conversion (e.g., docx-to-pdf, docx-to-html, pdf-to-html, html-to-pdf, html-to-docx)'
        }
    ],
    'responses': {
        200: {
            'description': 'File converted successfully',
            'schema': {
                'type': 'file'
            }
        },
        400: {
            'description': 'Invalid conversion type or file extension'
        }
    }
})
def convert_file():
    file = request.files['file']
    conversion_type = request.form['conversion_type']

    allowed_extensions = {
        'docx-to-pdf': ['docx'],
        'docx-to-html': ['docx'],
        'pdf-to-html': ['pdf'],
        'html-to-pdf': ['html'],
        'html-to-docx': ['html']
    }

    if conversion_type not in allowed_extensions:
        return {"message": "Invalid conversion type",
                "success": False
                }, 400

    if not allowed_file(file.filename, allowed_extensions[conversion_type]):
        return {"message": "Invalid conversion type",
                "success": False
                }, 400

    if conversion_type == 'docx-to-pdf':
        converted_file = convert_docx_to_pdf(file)
    elif conversion_type == 'docx-to-html':
        converted_file = convert_docx_to_html(file)
    elif conversion_type == 'pdf-to-html':
        converted_file = convert_pdf_to_html(file)
    elif conversion_type == 'html-to-pdf':
        converted_file = convert_html_to_pdf(file)
    elif conversion_type == 'html-to-docx':
        converted_file = convert_html_to_docx(file)
    else:
        return {"message": "Invalid conversion type",
                "success": False
                }, 400

    return send_file(converted_file, as_attachment=True)
