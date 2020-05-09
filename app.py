from flask import Flask,redirect,request,url_for
from flask import render_template as ren
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

UPLOAD_PATH = 'uploads'
app.config['UPLOAD_PATH'] = UPLOAD_PATH

@app.route("/")
def home():
    return ren("index.html")

@app.route("/img-upload", methods=['GET','POST'])
def upload():
    
    if request.method == 'POST':

        if request.files:

            image = request.files['image']
            print(image)
            id = uuid.uuid1()

            if secure_filename(image.filename):
                filename = image.filename
                ext =  filename.rsplit(".",1)[1]
                filename = id.hex + "." + ext  ######### FileName of uploaded file ############
                basepath = os.path.dirname(__file__)
                file_path = os.path.join(basepath,'templates','uploads',secure_filename(filename))
                print(file_path)
                image.save(file_path)
                return redirect(request.url)

    return ren("index.html")

@app.route('/upload-new',methods=['GET','POST'])
def upload_file():
     if request.method == 'POST':
        
        if request.files:

            image = request.files['image']
            id = uuid.uuid1()

            if image:

                filename = image.filename
                # ext =  filename.rsplit(".",1)[1]
                # filename = id.hex + "." + ext  ######### FileName of uploaded file ############
                filename = secure_filename(image.filename)

                file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                image.save(file_path)
                return send_from_directory(app.config['UPLOAD_PATH'],
                               filename)

     return ren("index.html")

from flask import send_from_directory
from werkzeug.middleware.shared_data import SharedDataMiddleware

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],
                               filename)


app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_PATH']
})

if __name__ == '__main__':
     app.run(debug=True)