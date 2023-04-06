import json
from datetime import datetime
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,String,Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base

from flask import Blueprint,render_template,request,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
# from flask.ext.login import UserMixin
# from flask_login import UserMixin
# from yourapp import login_manager

# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo


engine=create_engine("postgresql://ubuntu:iphone21@localhost:5432/fb")

Base=declarative_base()
app=Flask(__name__)
Session=sessionmaker(bind=engine)
session=Session()

class User(Base):
    __tablename__="users"
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,primary_key=True)
    password=Column(String,nullable=False)
    phone_no=Column(String,nullable=False)
class Posts(Base):
    __tablename__="posts"
    # id = Column(Integer, primary_key=True)
    by = Column(String,primary_key=True)
    link = Column(String,nullable=False)
    desc = Column(String,nullable=False)
    date = Column(DateTime, default=datetime.now())


@app.route("/newUser",methods=["POST","GET"])
def newUser():
    data=request.json
    result=session.query(User).all()
    a=0
    name=data["name"]
    email=data["email"]
    password=data["password"]
    phone_no=data["phone_no"]
    a=0
    for i in result:
        if i.email==email:
            a+=1
            # return "Email already Exists"
    if a==0:
        insert_query=User(name=name,email=email,password=generate_password_hash(password),phone_no=phone_no)
        session.add(insert_query)
        session.commit()
        return "Successfully Added User"
    else:
        return "User Already exists"

@app.route("/login", methods=["GET", "POST"])
# @user_loader
def login():
    data=request.json
    email=data["email"]
    password=data["password"]
    result=session.query(User).all()
    for i in result:
        if i.email==email and check_password_hash(i.password,password):
            # login_user(i.email)
            return "Welcome"
            break
    else:
        return "user not found"

@app.route("/logout",methods=["GET", "POST"])
# @login_required
def logout():
    # logout_user()
    return "ThankYou for logging out"


@app.route("/user/changePassword",methods=["GET", "POST"])
def userPassUpdate():
    data=request.json
    email=data["email"]
    old_password=data["old_password"]
    new_password=data["new_password"]
    result=session.query(User).filter(User.email==email,check_password_hash(User.password==old_password)).first()
    if result:
        result.password=generate_password_hash(new_password)
        session.commit()
        return "Changed password successfully"
    else:
        return "wrong password"

@app.route("/userUpdate",methods=["GET", "POST"])
def userUpdate():
    data=request.json
    email=data["email"]
    new_email=data["new_email"]
    name=data["name"]
    new_name=data["new_name"]
    phone_no=data["phone_no"]
    new_phone_no=data["new_phone_no"]
    result=session.query(User).filter(User.email==email,User.phone_no==phone_no,User.name==name).first()
    result.name=new_name
    result.phone_no=new_phone_no
    result.email=new_email
    session.commit()
    return "Updated successfully"





@app.route("/user/delete",methods=["DELETE", "POST"])
def userDelete():
    data=request.json
    email=data["email"]
    password=data["password"]
    result=session.query(User).filter(User.email==email,User.password==password).first()
    if result:
        session.delete(result)
        session.commit()
        return "Deleted User"
    else:
        return "email or password Wrong"

@app.route("/searchName",methods=["GET", "POST"])
def search():
    data=request.json
    search=data["name"]
    result=session.query(User.name).filter(User.name.contains(search)).all()
    users=[]
    for i in result:
        d={
            "username":i.name
        }
        users.append(d)
    if len(users)==0:
        return "No users found"
    else:
        return jsonify(users)


@app.route("/createPost", methods=["POST"])
def createPost():
    data=request.json
    link=data["link"]
    desc=data["desc"]
    email=data["email"]
    data = Posts(by=email, link=link, desc=desc)
    session.add(data)
    session.commit()
    return "Successfully created post"





if __name__=="__main__":
    app.run(debug=True)