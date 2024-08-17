# File Conversion API

## Overview
This is a Flask-based API for converting files between different formats. The supported conversions include:
- DOCX to PDF
- DOCX to HTML
- PDF to HTML
- HTML to PDF
- HTML to DOCX

## Prerequisites
- Docker
- Docker Compose

## Setup

### Using Docker
1. **Build the Docker image:**
    ```sh
    docker build -t file-conversion-api .
    ```

2. **Run the Docker container:**
    ```sh
    docker run -p 5000:5000 file-conversion-api
    ```

### Without Docker
1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    flask run
    ```

## API Endpoints

### Convert File
- **URL:** `/api/convert`
- **Method:** `POST`
- **Parameters:**
  - `file` (formData, required): The file to be converted.
  - `conversion_type` (formData, required): The type of conversion (e.g., `docx-to-pdf`, `docx-to-html`, `pdf-to-html`, `html-to-pdf`, `html-to-docx`).

- **Responses:**
  - `200 OK`: File converted successfully.
  - `400 Bad Request`: Invalid conversion type or file extension.

### Example Request
```sh
curl -X POST http://localhost:5000/api/convert \
  -F "file=@/path/to/your/file.docx" \
  -F "conversion_type=docx-to-pdf"