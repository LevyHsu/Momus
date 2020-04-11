#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, make_response, jsonify, url_for, session, flash
import random
import string
import os
import json
import image_processing
from PIL import Image
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './templates/usr_temp_files'
app = Flask(__name__,
    template_folder='./templates',  
    static_folder='./templates',
    static_url_path='', 
    )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Generate a random string of letters and digits
def generate_key(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

# Error page with reason
@app.route('/error')
def error():
    error_trace = request.args['error_trace']  
    error_trace = session['error_trace']       
    return render_template("error.html", reason=json.loads(error_trace))

# Index
@app.route('/')
def index():
    return render_template("index.html")

# Handle file upload
@app.route('/uploads', methods = ['POST'])
def upload_img():
    
    # Random file name, also the sessionkey.
    this_sessionkey = generate_key(8)
    file = request.files["file"]
    filename = secure_filename(file.filename)

    print("-------------------------------")
    print("New File upload: " + filename)
    
    filename = this_sessionkey + os.path.splitext(filename)[1] 
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename);

    # if not image file
    if (os.path.splitext(filepath)[1] != ".png" and os.path.splitext(filepath)[1] != ".jpg" and os.path.splitext(filepath)[1] != ".PNG" and os.path.splitext(filepath)[1] != ".JPG" and os.path.splitext(filepath)[1] != ".jpeg" and os.path.splitext(filepath)[1] != ".JPEG"): 
        error_trace = json.dumps("Unsupported file type")
        session['error_trace'] = error_trace
        return redirect(url_for('.error', error_trace=error_trace))
    
    else:
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        print("Saved Image Size: " + str(file_size/1000000) + "MB")
        # File > 20MB
        if (file_size>20480000):
            os.remove(filepath)
            print("File > 20MB, Dropped")    
            error_trace = json.dumps("File greater than 20MB")
            session['error_trace'] = error_trace
            return redirect(url_for('.error', error_trace=error_trace))
        # File > 2MB
        elif (file_size>2048000):
            print("File > 2MB, Compressed")    
            large_image_processing(filepath)

        session_key = json.dumps(filename)
        session['session_key'] = session_key
        return redirect(url_for('.submission', session_key=session_key))

    error_trace = json.dumps("Unknow Error code: U01")
    session['error_trace'] = error_trace
    return redirect(url_for('.error', error_trace=error_trace))

# Render submission page
@app.route('/submission')
def submission():
    session_key = request.args['session_key']  
    session_key = session['session_key']
    return render_template("submission.html",code=json.loads(session_key),user_image = "usr_temp_files/"+session_key.replace('"', ""))

# Handle target_similarity submission form submission.html
@app.route('/pack', methods = ['POST'])
def pack_to_queue():
    # if no file was given
    if (request.form['file_name']!="" and request.form['target_similarity']!=""):
        name_temp = momus_img_processing(request.form['target_similarity'],"templates/" + request.form['file_name'])[10:]
        print ("Success :" + name_temp)
        print("-------------------------------")
        output_name = json.dumps(name_temp)
        session['output_name'] = output_name
        return redirect(url_for('.download_file', output_name=output_name))
    
    error_trace = json.dumps("Unknow Error code: P01")
    session['error_trace'] = error_trace
    return redirect(url_for('.error', error_trace=error_trace))        

# Download page
@app.route('/downloads')
def download_file():
    output_name = request.args['output_name']  
    output_name = session['output_name']
    return render_template("downloads.html",user_image=json.loads(output_name))

# Image_processing
def momus_img_processing(level,path):
    # 0 for online mode
    user_image = image_processing.usr_img(path,0)
    
    if (level == "high"):
        for i in range(10):
            user_image.keypoint_obscure(1)
    
    if (level == "mid"):
        for i in range(15):
            user_image.keypoint_obscure(1)
            user_image.keypoint_white_black_salt(1)
            user_image.Random_Shape_Draw(20,15)
    
    if (level == "low"):
        for i in range(20):
            user_image.keypoint_obscure(1)
            user_image.keypoint_white_black_salt(1)
            user_image.Random_Shape_Draw(40,25)
    
    if (level == "superlow"):
        for i in range(25):
            user_image.keypoint_obscure(2)
            user_image.keypoint_white_black_salt(2)
            user_image.Random_Shape_Draw(50,25)
    
    user_image.Random_Crop(random.randint(5,10))
    output_name = user_image.output_flask()
    return output_name

# Resize image if too big. For PNG, remove alpha channel.
def large_image_processing(filepath):
    factor = 0.8
    image = Image.open(filepath)
    
    if(os.path.splitext(filepath)[1] ==".png" or os.path.splitext(filepath)[1] ==".PNG"):
       image.putalpha(255)
    
    if (image.width > 6144 or image.height > 6144):
        if (image.height > image.width):
            factor = 6144 / image.height
        else:
            factor = 6144 / image.width
    new_image = image.resize((int(image.width * factor), int(image.height * factor)))
    new_image.save(filepath,quality=80,optimize=True)

if __name__ == '__main__':
    app.secret_key = generate_key(20)
    app.run(host= '0.0.0.0',port=5000)
'''
Reference:
https://link.springer.com/content/pdf/10.1186/1687-417X-2013-8.pdf
https://docs.opencv.org/3.4/d2/d29/classcv_1_1KeyPoint.html
https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
https://pysimplegui.readthedocs.io/en/latest/
https://isotope11.com/blog/storing-surf-sift-orb-keypoints-using-opencv-in-python
https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
https://docs.opencv.org/master/d4/d5d/group__features2d__draw.html
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV.py
https://pythonise.com/categories/javascript/upload-progress-bar-xmlhttprequest
https://blog.csdn.net/Likianta/article/details/89363973
https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
'''
