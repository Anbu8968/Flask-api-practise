from flask import Flask,jsonify,request,session
# from tensorflow import keras
# import tensorflow as tf
# import numpy as np
# from tensorflow.keras.utils import load_img
# from tensorflow.keras.utils import img_to_array

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,String,Integer,Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_mail import Mail,Message


import jwt
# from datetime import datetime,timedelta
import datetime
from functools import wraps


engine=create_engine('postgresql://ubuntu:iphone21@localhost:5432/postgres')

Base= declarative_base()
# app=Flask(__name__)
Session = sessionmaker(bind=engine)
session=Session()




class Users(Base):
    __tablename__="users"
    email=Column(String,nullable=False,primary_key=True)
    password=Column(String,nullable=False)
    username=Column(String,nullable=False)
    phone_number=Column(String,nullable=False)
    verified=Column(Integer,nullable=False)



class Friends(Base):
    __tablename__="friends"
    id=Column(Integer,primary_key=True)
    email_id=Column(String,nullable=False)
    request_send=Column(String,nullable=False)
    request_recieved=Column(String,nullable=False)
    friends=Column(String,nullable=False)

app=Flask(__name__)
app.config["SECRET_KEY"]="2ff6d8d552d24a90977b6591647bb561"
ALGORITHM="HS256"



mail=Mail(app)


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"]="anbu2872001@gmail.com"
app.config["MAIL_PASSWORD"]="enter password"
# app.config["MAIL_USE_TLS"]="True"
app.config["MAIL_USE_SSL"]=False

mail=Mail(app)




# load_model=keras.models.load_model("potatoes.h5")
# class_names=['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']


# def token_required(func):
#     @wraps(func)
#     def decorated(*args,**kwargs):
#         data=request.json
#         token=data["token"]
#         if not token:
#             return jsonify({"Alert":"Token is missing"}),401
#         try:
#             data=jwt.decode(token,app.config["SECRET_KEY"],algorithms=[ALGORITHM])
#             # return data
#         except:
#             return jsonify({"message":"Invalid token"}),403
#         return func(*args,**kwargs)
#     return decorated




def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token=request.args.get('token')
        # token=data["token"]
        if not token:
            return jsonify({"Alert":"Token is missing"}),401
        try:
            data=jwt.decode(token,app.config["SECRET_KEY"],algorithms=[ALGORITHM])
            # return data
        except:
            return jsonify({"message":"Invalid token"}),403
        return func(*args,**kwargs)
    return decorated
















@app.route("/",methods=["GET"])
def home():
    return "Welcome"

# @app.route("/predict",methods=["GET","POST"])
# def predict():
#     img=load_img("/home/divum/STUDY/POTATO_EXPERIMENT/POTATO/Potato___Late_blight/0acdc2b2-0dde-4073-8542-6fca275ab974___RS_LB 4857.JPG")
#     x=img_to_array(img)
#     x=np.expand_dims(x,axis=0)
#     predicted_class=class_names[np.argmax(load_model.predict(x))]
#     # print(predicted_class)
#     return {"predicted_class":predicted_class}


# @app.route('/login',methods=["GET"])
# def login():


@app.route("/newUser",methods=["POST"])
def newUser():
    data=request.get_json()
    email=data.get("email")
    username=data.get("username")
    phone_number=data.get("phone_number")
    password=str(data.get("password"))
    result=session.query(Users).all()
    a=0
    for i in result:
        if i.email==email:
            a+=1
    if a==0:
        insert_query=Users(email=email,password=generate_password_hash(password),username=username,phone_number=phone_number,verified=0)
        session.add(insert_query)
        session.commit()
        email=data["email"]
        token=jwt.encode({'username':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=120)},app.config["SECRET_KEY"])
        msg=Message(subject="link",sender="Anbu",recipients=[email])
        msg.body=str("http://127.0.0.1:5000/validate?token="+str(token))
        mail.send(msg)
        return "Registered Successfully verify mail id"
    else:
        return "Users Email Already exists"
      

    #   return {"email":email,"username":username,"phone_number":phone_number,"password":password}

@app.route("/validate",methods=["POST","GET"])
@token_required
def validate():
    token=request.args.get('token')
    payload=jwt.decode(token,app.config["SECRET_KEY"],algorithms=ALGORITHM)
    email=payload.get("email")
    print(email)
    result=session.query(Users).filter(Users.email==email).first()
    result.verified=1
    session.commit()
    return "email verified successfully"
    # for i in result:
    #     if i.email==email:
    #         i.verified=1
    #         session.commit()
    #         return "verified"
    #         break
    # session.add()
    # session.commit()


@app.route("/login",methods=["GET"])
def login():
    data=request.json
    email=data['email']
    password=str(data["password"])
    result=session.query(Users).filter(Users.email==email).first()
    # print(result.email,result.verified)
    # print(email)
    if result.email==email and check_password_hash(result.password,password):
        if result.verified==1:
            session["logged_in"]=True
            token=jwt.encode({'username':data["username"],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=120)},app.config["SECRET_KEY"])
            # print(token)
            payload=jwt.decode(token,app.config["SECRET_KEY"],algorithms=ALGORITHM)
            username=payload.get("username")

            return jsonify({"token":token,"username":username})
                # break
        else:
            token=jwt.encode({'email':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=120)},app.config["SECRET_KEY"])
            msg=Message(subject="link",sender="Anbu",recipients=[email])
            msg.body=str("http://127.0.0.1:5000/validate?token="+str(token))
            mail.send(msg)
            return "mail sended"
        
    else:
        return "User not found"

@app.route('/logout',methods=["GET"])
@token_required
def logout():
    return "Logout Successfully "




@app.route("/changepassword",methods=["POST","GET"])
@token_required
def changepassword():
    data=request.json
    email=data["email"]
    old_password=data["old_password"]
    new_password=data["new_password"]
    result=session.query(Users).filter(Users.email==email,check_password_hash(Users.password==old_password)).first()
    if result:
        result.password=generate_password_hash(new_password)
        session.commit()
        return "Password changed Successfully"
    else:
        return "wrong password"




@app.route('/userDelete',methods=["DELETE"])
@token_required
def delete():
    data=request.json
    email=data['email']
    password=data['password']
    result=session.query(Users).filter(Users.email==email).first()
    if result:
        c_p=check_password_hash(result.password,password)
        if c_p==True:
            session.delete(result)
            session.commit()
            return "User Deleted"
        else:
            return "Wrong password"
    else:
        return "User already Deleted the account"


@app.route('/userUpdate',methods=["POST"])
@token_required
def update():
    data=request.json
    username=data["username"]
    email=data["email"]
    phone_number=data["phone_number"]
    result=session.query(Users).filter(Users.email==email)
    if result:
        result.username=username
        result.phone_number=phone_number
        session.commit()
        return "updated Success"
    else:
        return "user invalid"


# @app.route("/verify",methods=["POST"])
# def verify():
#     data=request.json
#     email=data["email"]
#     token=jwt.encode({'username':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=60)},app.config["SECRET_KEY"])
#     msg=Message(subject="link",sender="Anbu",recipients=[email])
#     msg.body=str("http://127.0.0.1:5000/validate?token="+str(token))
#     mail.send(msg)
#     return "mail sended"




 

@app.route("/forgotPassword",methods=["GET"])
def forgotPasswod():
    data=request.json
    email=data['email']
    result=session.query(Users).filter(Users.email==email,Users.verified==1).first()
    # print(result.email)
    if result!=None:
        token=jwt.encode({'email':data["email"],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=120)},app.config["SECRET_KEY"])
        msg=Message(subject="link",sender="Anbu",recipients=[email])
        msg.body=str("http://127.0.0.1:5000/newPassword?token="+str(token))
        mail.send(msg)
        return "reset mail sended"
    else:
        return "Invalid email"


@app.route("/newPassword",methods=["POST"])
@token_required
def newPassword():
    data=request.json
    token=request.args.get('token')
    # print("hi",token)
    new_pass=data["new_pass"]
    confirm_pass=data["confirm_pass"]
    payload=jwt.decode(token,app.config["SECRET_KEY"],algorithms=ALGORITHM)
    email=payload.get('email')
    result=session.query(Users).filter(Users.email==email)
    if result:
        if new_pass==confirm_pass:
            result.password=generate_password_hash(new_pass)
            session.commit()
            return "password updated"
        else:
            return "password mismatch"
    else:
        return "email invalid"






# @app.route('/requestSend',methods=["POST"])
# def requestSend():
#     data=request.json
#     sender=data["sender"]
#     reciever=data["reciever"]
#     result=Friends(email_id=sender,request_send=reciever,request_recieved="0",friends="0")
#     result1=Friends(email_id=reciever,request_recieved=sender,request_send="0",friends="0")
#     result2=session.query(Friends).all()
#     c=0
#     l=[]
#     check_request=session.query(Friends).all()
#     d=0
#     for check in check_request:
#         if check.email_id==sender and check.request_send==reciever:
#             print(check.email_id)
#             d+=1
#     # print(d)
#     if d==0:
#         for f in result2:
#             if f.friends==reciever:
#                 c+=1

#         # print(c,"c")
#         if c==0:
#             session.add(result1)
#             session.add(result)
#             session.commit()
#             return "request sended"
#         else:
#             return "Already Friends"
#     else:
#         return "request already sended"
#     # return "hi"


# @app.route("/listRequest",methods=["GET"])
# def listRequest():
#     data=request.json
#     email=data["email"]
#     result=session.query(Friends).filter(Friends.email_id==email)
#     l=[]
#     for i in result:
#         if i.request_recieved!="0":
#             l.append(i.request_recieved)
#     # for i in result:
#     #     if i.email_id==email:
#     #         x={i:i.request_recieved}
#     #         l.append(x)
#     # return jsonify(l)
#     if len(l)==0:
#         return "no request found"
#     else:
#         return jsonify(l)



# @app.route("/acceptRequest",methods=["POST"])
# def acceptRequest():
#     data=request.json
#     current_user=data["current_user"]
#     requested_email=data["requested_email"]
#     result=session.query(Friends).all()
#     # print(requested_email)
#     # print(result.email_id)

#     # if c!=1:
#     for i in result:
#         if i.email_id==current_user and i.friends=="0" and i.request_recieved=="0":
#             i.request_recieved="0"
#             i.friends=requested_email
#             session.commit()
#     result1=session.query(Friends).all()
#     for j in result1:
#         if j.email_id==requested_email and j.friends=="0" and j.request_send=="0":
#             j.request_send="0"
#             j.friends=current_user
#             session.commit()
#     return "accepted"
    # else:
    #     return "already friends"



# @app.route("/friends",methods=['GET'])
# def friends():
#     l=[]
#     data=request.json
#     current_user=data["current_user"]
#     result=session.query(Friends).filter(Friends.email_id==current_user)
#     for i in result:
#         if i.email_id==current_user:
#             l.append(i.friends)
#     # print(l)
#     return jsonify(l)











if __name__=='__main__':
    app.run(debug=True)
