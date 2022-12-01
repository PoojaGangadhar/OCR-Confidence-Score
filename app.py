import os

from flask import Flask, render_template, request
from extractionApplication import ocr_ext, confidenceScore
from pdftoimage import conversionToImage

UPLOAD_FOLDER = '/static/uploads/'
EXTENSIONS_ALLOWED = {'png', 'jpg', 'jpeg', 'pdf'}

appExt = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
FILES_UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
appExt.config['UPLOAD_FOLDER'] = FILES_UPLOAD_FOLDER


def files_ext(filename):
    print(filename)
    """  file = filename.rsplit('.', 1)[1]
    print(file)"""
    if filename.rsplit('.', 1)[1] == "pdf":
        conversionToImage(filename)
        print("PDF To Image Conversion completed")
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_ALLOWED
    else:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_ALLOWED


@appExt.route('/')
def home_page():
    # return "Invoice Data Extraction"
    # return render_template("fileupload.html")
    return render_template("index.html")


@appExt.route('/upload', methods=['GET', 'POST'])
def pageUpload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('fileupload.html', msg='No file selected')
        file = request.files['file']

        if file.filename == '':
            return render_template('fileupload.html', msg='No file selected')

        if file and files_ext(file.filename):
            textExtracted = ocr_ext(file)
            TextObtained = confidenceScore(file)
            """ return render_template('fileupload.html', msg='Successfully Processed', textExtracted=textExtracted,
                                   img_src=UPLOAD_FOLDER + file.filename)"""
            return render_template('fileupload.html', msg='Successfully Processed', textExtracted=textExtracted, confidence=TextObtained,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('fileupload.html')


if __name__ == '__main__':
    appExt.run()
