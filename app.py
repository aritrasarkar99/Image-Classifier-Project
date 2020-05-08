from flask import Flask,redirect,request,url_for
from flask import render_template as ren
import os
from werkzeug.utils import secure_filename
import uuid
app = Flask(__name__)


@app.route("/")
def home():
    return ren("index.html")

@app.route("/img-upload", methods=['GET','POST'])
def upload():
    if request.method == 'POST':

        if request.files:

            image = request.files['image']
            id = uuid.uuid1()

            if secure_filename(image.filename):
                filename = image.filename
                ext =  filename.rsplit(".",1)[1]
                filename = id.hex + "." + ext  ######### FileName of uploaded file ############
                basepath = os.path.dirname(__file__)
                file_path = os.path.join(basepath,'templates','uploads',secure_filename(filename))
                image.save(file_path)
                return redirect(request.url)

    return ren("index.html")


if __name__ == '__main__':
     app.run(debug=True)