# Imports the required Packages
from flask import Flask , render_template ,  request , Response, redirect, url_for, abort, jsonify
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from config import cred
from PIL import Image
from connect import *
from healper import *
from utils import *
import io

app = Flask(__name__ , template_folder='templates')
app.secret_key = cred["secret_key"]

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=["GET"])
def register():
    return render_template('/register.html')


@app.route('/second_register', methods=["GET", "POST"])
def second_register():
    return render_template("/secondreg.html")

@app.route('/third_register_validation', methods=["POST"])
def third_reg_val():
    print(request.files)
    if "image" not in request.files:
        return jsonify({"error": "No file found"}), 404

    imagefile = request.files["image"]

    image_bytes = imagefile.read()

    image = Image.open(io.BytesIO(image_bytes))

    image_array = face_recognition.load_image_file(io.BytesIO(image_bytes))

    face_encodings = face_recognition.face_encodings(image_array)

    if len(face_encodings) == 0:
        return jsonify({ "status": "error", "description" : "No face found"}), 200
    if len(face_encodings) > 1:
        return jsonify({"status" : "error", "Description" : "More than 1 face found"}), 200

    face_encoding = face_encodings[0]
    encoded_list = face_encoding.tolist() 

    return jsonify({"status": "success", "encoding": encoded_list}), 200

@app.route("/last_login", methods = ["POST"])
def last_login():

    if "image" not in request.files:
        return jsonify({"error": "No file found"}), 404
    
    email = request.form.get("email")

    imagefile = request.files["image"]

    image_bytes = imagefile.read()

    image = Image.open(io.BytesIO(image_bytes))

    image_array = face_recognition.load_image_file(io.BytesIO(image_bytes))

    face_encodings = face_recognition.face_encodings(image_array)

    if len(face_encodings) == 0:
        return jsonify({ "status": "error", "description" : "No face found"}), 200
    if len(face_encodings) > 1:
        return jsonify({"status" : "error", "Description" : "More than 1 face found"}), 200

    face_encoding = face_encodings[0]

    faceidblob = get_faceid(email)
    faceid = blobToList(faceidblob[0])

    result = face_recognition.compare_faces([faceid], face_encoding)

    if(result[0] == True):
        return jsonify({"status" : "success"})
    return jsonify({"status" : "fail"})


@app.route('/third_register/<email>', methods = ["GET", "POST"])
async def third_reg(email):
    otp = await generate_otp()
    flag = await store_otp(email, otp)
    body = f"Your OTP is - {otp}"
    await send_email(email, body)
    return render_template("/thirdreg.html", email=email)

@app.route("/last_reg", methods=["POST"])
def last_reg():
    # print(request.get_json())
    data = request.get_json()
    email = data["Email"]
    name = data["name"]
    password = data["password"]
    education = data["education"]
    face_id = listToBlob(data["face_embbeding"])
    dob = data["dob"]
    profesion = "student"
    success = add_profile(name, email, password, face_id, education, profesion, dob)
    if(success):
        return jsonify({"status" : "success"}), 200
    return jsonify({"status" : "Failed"}), 200
    

@app.route("/otp_varification", methods = ["POST"])
def otp_registration():
    data = request.get_json()
    if not data:
        return jsonify({"result" : False, "description" : "Some thing went wrong"})
    print(data)
    Enterd_otp = data["OTP"]
    email = data["EMAIL"]
    result = validate_otp(email, Enterd_otp)
    return jsonify({"result" : result["status"], "description" : result["description"]})


@app.route('/profile/<email>', methods = ["POST", "GET"])
def profile(email):
    info = get_profile(email)
    label = ["Accno", "Name", "dob", "Education", "Profession"]
    return render_template('/home.html', info=info, label = label)

@app.route('/login_validation' , methods = ["POST", "GET"])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email, password)
    actual_password = get_password(email)
    print(actual_password)
    if actual_password == None:
        return jsonify({"description" : "No User Found !"})
    if password == actual_password[0]:
        return redirect(url_for("second_login", email=email))
    else:
        return jsonify({"description" : "Wrong Password"})

@app.route('/second/<email>' , methods = ["GET"])
async def second_login(email):
    if(True):
        otp = await generate_otp()
        flag = await store_otp(email, otp)
        body = f"Your OTP is - {otp}"
        await send_email(email, body)
        return render_template("secondlogin.html", email=email)
    else:
        return abort(400, "Something Went Wrong")

@app.route('/third' , methods = ["POST", "GET"])
def third_login():
    return render_template("thirdlogin.html")



def login_time(name):
    with open('Users_login_time.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dtstring}')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
