from flask import Flask, request, jsonify
from docx import Document
import PyPDF2
import os
import tempfile

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text_content = []
    for paragraph in doc.paragraphs:
        text_content.append(paragraph.text)
    return '\n'.join(text_content)

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_content = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content.append(page.extract_text())
    return '\n'.join(text_content)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def gen():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith('.docx'):
        try:
            text_content = extract_text_from_docx(file)
            return jsonify({'text_content': text_content})
        except Exception as e:
            return jsonify({'error': f'Error processing the DOCX file: {str(e)}'})
    elif file and file.filename.endswith('.pdf'):
        try:
            # Save the PDF file to a temporary location
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            file.save(temp_pdf.name)
            text_content = extract_text_from_pdf(temp_pdf.name)
            os.remove(temp_pdf.name)  # Clean up the temporary PDF file
            return jsonify({'text_content': text_content})
        except Exception as e:
            return jsonify({'error': f'Error processing the PDF file: {str(e)}'})
    else:
        return jsonify({'error': 'Invalid file format. Please upload a DOCX or PDF file'})

if __name__ == '__main__':
    app.run(port=5000)
