from app import app
from flask import render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from detect import detect
from time import time
import hashlib, os

def is_image(filename):
    ext = filename.split(".")[-1]
    ext = ext.lower()
    if ext == 'jpg' or ext == 'png' or ext == 'jpeg' or ext == 'gif':
        return True
    return False

@app.route('/')
@app.route('/index', methods=["POST", "GET"])

def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(app.config['UPLOAD_FOLDER'] + filename)
        #return redirect(url_for('uploaded_file', filename = filename))
        md5 = hashlib.md5(str(time()).encode('utf-8')).hexdigest() + "." + filename.split(".")[-1]
        detect(app.config['UPLOAD_FOLDER'] + filename, app.config['UPLOAD_FOLDER'] + md5)
        return redirect(url_for('uploaded_file', filename = md5))

    return render_template('index.html', title='Detection Demo', author=app.config['AUTHOR'], menu=app.config['MENU'])

@app.route('/gallery')
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    image_list = []
    for i in files:
        if is_image(i):
            image_list.append(i)
    return render_template('gallery.html', title="Gallery", author=app.config['AUTHOR'], menu=app.config['MENU'], image_list = image_list)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('image.html', title="Detected", author=app.config['AUTHOR'], menu=app.config['MENU'], filename = filename)
@app.route('/capture')
def capture():
    return render_template('capture.html', title="Camera", author=app.config['AUTHOR'], menu=app.config['MENU'])
@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)
@app.route('/static/<filename>')
def download_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)