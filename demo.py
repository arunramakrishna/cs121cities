import os
from app import app
import sys
import pickle
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def display_text(filename, imagetype):
    if imagetype == "landmark":
        return "Still in development: your LANDMARK prediction"
    elif imagetype == "skyline":
        return "Still in development: your SKYLINE prediction"
    else:
        return "Still in development: your prediction"

	# learn_inf = load_learner('')
	# pred = learn_inf.predict('uploads/' + filename)[0]
	# return pred

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        if "imagetype" not in request.values:
            flash("no image type selected")
            return redirect(request.url)

        imagetype = request.form["imagetype"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed below')
        predict = display_text(file.filename, imagetype)
        return render_template('upload.html', filename=filename, prediction = predict)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)