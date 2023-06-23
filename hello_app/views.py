import os
import tempfile
from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfFileReader
from docx import Document


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_summary(pdf_path):
    # Load the PDF file
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        num_pages = pdf.getNumPages()

        # Extract text from each page
        text = ''
        for page_num in range(num_pages):
            page = pdf.getPage(page_num)
            text += page.extract_text()

        # Generate summary (you can replace this with your own summarization logic)
        summary = text[:500]  # Example: Take the first 500 characters as a summary

    return summary


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file is selected for upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'})

    file = request.files['file']

    # Check if a file is uploaded
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    # Save the uploaded file to a temporary location
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    # Show "file uploaded successfully" message
    message = 'File uploaded successfully'

    # Process the uploaded file
    message = 'File is being processed...'
    summary = generate_summary(temp_path)

    # Create a Word document with the summary
    doc = Document()
    doc.add_paragraph(summary)
    doc_path = os.path.join(temp_dir, 'summary.docx')
    doc.save(doc_path)

    # Remove the temporary directory
    os.remove(temp_path)
    os.rmdir(temp_dir)

    # Provide the summary document as a download
    return jsonify({'summary': summary, 'doc_url': doc_path})


if __name__ == '__main__':
    app.run(debug=True)
