# File: frontend/views/file_upload.py

from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os

file_upload_bp = Blueprint('file_upload', __name__)

UPLOAD_FOLDER = 'path/to/upload/folder'  # Update this path as needed
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('file_upload.upload_file'))
    return render_template('upload.html')  # Ensure you have an upload.html template for rendering