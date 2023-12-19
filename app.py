from flask import Flask, request, jsonify
from docx import Document

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text_content = []
    for paragraph in doc.paragraphs:
        text_content.append(paragraph.text)
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
            return jsonify({'error': f'Error processing the file: {str(e)}'})
    else:
        return jsonify({'error': 'Invalid file format. Please upload a DOCX file'})

if __name__ == '__main__':
    app.run(port=5000)
