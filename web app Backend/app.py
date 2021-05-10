import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from flask_mail import Mail
from views.s3 import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object('settings')
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

"""
# -- ---------------------------------------------------------------------------------
# -- Set allowed extensions to allow only upload excel files
# -- ---------------------------------------------------------------------------------
"""
ALLOWED_EXTENSIONS = set(['jpg','png','wmv ', 'm4v','3gp', 'mp4' ])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method in ('POST'):
        print(f"*** Inside the template")
    return render_template('main.html')


# ------------------------------------------------------------------------------------------
@app.route('/upload_files_to_s3', methods=['GET', 'POST'])
def upload_files_to_s3():
    if request.method == 'POST':

        # No file selected
        if 'file' not in request.files:
            flash(f' *** No files Selected', 'danger')

        file_to_upload = request.files['file']
        content_type = request.mimetype

        # if empty files
        if file_to_upload.filename == '':
            flash(f' *** No files Selected', 'danger')

        # file uploaded and check
        if file_to_upload and allowed_file(file_to_upload.filename):


            file_name = secure_filename(file_to_upload.filename)

            print(f" *** The file name to upload is {file_name}")
            print(f" *** The file full path  is {file_to_upload}")

            bucket_name = "vdatabacket"

            s3_upload_files(file_to_upload, bucket_name, file_name,content_type )
            flash(f'Success - {file_to_upload} Is uploaded to {bucket_name}', 'success')

        else:
            flash(f'Allowed file type are jpg, png , wmv , m4v , 3gp , mp4 .Please upload proper formats...', 'danger')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)