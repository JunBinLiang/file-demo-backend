import os
# import magic
import urllib.request
from flask import Flask, flash, request, redirect, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = 'C:\\Users\\leyal\\PycharmProjects\\File-Handling\\venv\\Upload-files'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    print('Uploading')

    if request.method == 'POST':
        # check if the post request has the file part
        # print('json', request.form.to_dict())
        # print(request.files)
        # print(request.files['files[]'])
        # handle uppy file
        if 'files[]' in request.files:
            file = request.files['files[]']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {'message': 'Created', 'code': 'SUCCESS'}
            return make_response(jsonify(data), 201)

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('File successfully uploaded')
            data = {'message': 'Created', 'code': 'SUCCESS'}
            return make_response(jsonify(data), 201)
        else:
            print('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()
