from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        # Handle file uploads and merging
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        if file1 and file2 and file1.filename.endswith('.pdf') and file2.filename.endswith('.pdf'):
            # Save files
            file1_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename))
            file2_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename))
            file1.save(file1_path)
            file2.save(file2_path)
            
            # Create output path
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.pdf')
            
            # Merge PDFs
            try:
                pdf_writer = PdfWriter()
                
                for pdf_path in [file1_path, file2_path]:
                    pdf_reader = PdfReader(pdf_path)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                
                with open(output_path, 'wb') as out_pdf:
                    pdf_writer.write(out_pdf)
                
                # Send merged file to user
                return send_file(output_path, as_attachment=True, download_name='merged.pdf')
            
            except Exception as e:
                return f"Error merging PDFs: {str(e)}", 400
        
        return "Invalid files uploaded", 400
    
    return render_template('merge.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        # Handle file upload and extraction
        pdf_file = request.files['pdf_file']
        page_numbers = request.form.get('page_numbers', '')
        
        if pdf_file and pdf_file.filename.endswith('.pdf') and page_numbers:
            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pdf_file.filename))
            pdf_file.save(file_path)
            
            # Parse page numbers
            pages = parse_page_numbers(page_numbers)
            if not pages:
                return "Invalid page numbers format", 400
            
            # Create output path
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted.pdf')
            
            # Extract pages
            try:
                pdf_reader = PdfReader(file_path)
                pdf_writer = PdfWriter()
                
                for page_num in pages:
                    if 1 <= page_num <= len(pdf_reader.pages):
                        pdf_writer.add_page(pdf_reader.pages[page_num - 1])
                
                with open(output_path, 'wb') as out_pdf:
                    pdf_writer.write(out_pdf)
                
                # Send extracted file to user
                return send_file(output_path, as_attachment=True, download_name='extracted.pdf')
            
            except Exception as e:
                return f"Error extracting pages: {str(e)}", 400
        
        return "Invalid file or page numbers", 400
    
    return render_template('extract.html')

def parse_page_numbers(page_input):
    """Parse a string of page numbers and ranges into a list of integers."""
    pages = set()
    try:
        parts = page_input.split(",")
        for part in parts:
            if "-" in part:
                start, end = map(int, part.split("-"))
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
        return sorted(pages)
    except ValueError:
        return None

if __name__ == '__main__':
    app.run(debug=True)