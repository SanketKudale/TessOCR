from flask import Flask, request, redirect, url_for, flash
from flask_restful import Api, Resource
import json
import os
import sys
import tess

app = Flask(__name__)
app.secret_key = 'Digidocs'

UPLOAD_FOLDER = './uploads/'  # Set to your desired folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # save the file
        nameSplit = file.filename.split(".")

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "temp." + nameSplit[1]))

        return tess.Tess().scanImage()

    return 'Invalid file format!'


class HelloWorld(Resource):
    @staticmethod
    def get():
        return {"response": "Hello World"}


class Tessy(Resource):
    @staticmethod
    def post():
        return upload_file()


api = Api(app)

api.add_resource(HelloWorld, "/test")
api.add_resource(Tessy, "/ocr")

if __name__ == "__main__":
    app.run(debug=True)
