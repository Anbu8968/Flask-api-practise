import json
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.ext.declarative import declarative_base


engine=create_engine('postgresql://ubuntu:iphone21@localhost:5432/postgres')

Base= declarative_base()
app=Flask(__name__)
Session = sessionmaker(bind=engine)
session=Session()

class Orders(Base):
    __tablename__="orders"
    product_id=Column(Integer,primary_key=True)
    market_place=Column(String,nullable=False)
    quantity=Column(Integer,nullable=False)

class Products(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True)
    product_name=Column(String,nullable=False)
    price=Column(Integer,nullable=False)
    Quantity=Column(Integer,nullable=False)

class Login(Base):
    __tablename__="login"
    username=Column(String,primary_key=True)
    password=Column(String,nullable=False)


# @app.route("/login",methods=["POST"])
# def login():
#     data=request.json
#     username=data["username"]
#     password=data["password"]
#     if username=="Anbu" and  password=="12345":
#         return "Welcome da Sambu Mavanaeee !"
#     else:
#         return "Savu da setha payalaee"



@app.route("/adduser",methods=["POST"])
def add_user():
    data=request.json
    username=data["username"]
    password=data["password"]
    insert_query=Login(username=username,password=password)
    session.add(insert_query)
    session.commit()
    return "Added User Succesfully"

@app.route("/order",methods=["POST"])
def place_order():
    data=request.json
    product_id=data["product_id"]
    market_place=data["market_place"]
    quantity=data["quantity"]
    insert_query=Orders(product_id=product_id,market_place=market_place,quantity=quantity)
    session.add(insert_query)
    session.commit()
    return "Order placed da Sambu Mavanae"


@app.route("/addproduct",methods=["POST"])
def addproduct():
    data=request.json
    id=data["id"]
    product_name=data["product_name"]
    price=data["price"]
    Quantity=data["Quantity"]
    insert_query=Products(id=id,product_name=product_name,price=price,Quantity=Quantity)
    session.add(insert_query)
    session.commit()
    return "Products Added da Sambu Mavanae"

@app.route("/listproducts",methods=["GET"])
def listproducts():
    result=session.query(Products).all()
    l=[]
    for i in result:
        d={
            "ID":i.id,
            "product_name":i.product_name,
            "price":i.price,
            "Quantity":i.Quantity
        }
        l.append(d)
    return jsonify(l)


@app.route("/market",methods=["GET"])
def market():
    data=request.json
    m_place=data["market_place"]
    result=session.query(Orders).all()
    l=[]
    for i in result:
        if i.market_place == m_place:
                d={
                    "ID":i.product_id,
                    "quantity":i.quantity
                }
                l.append(d)
    # print(l)
    return jsonify(l)


@app.route("/orderiddetails",methods=["GET"])
def orderiddetails():
    data=request.json
    id=data["id"]
    result=session.query(Products).all()
    l=[]
    for i in result:
        if i.id == id:
            d={
                "Product Name":i.product_name,
                "Price":i.price
            }
            l.append(d)
    if len(l) == 0:
        return "dei wrong id da !"
    else:
        return jsonify(l)

@app.route("/pr/or/de",methods=["GET"])
def pod():
    data=request.json
    p_name=data["product_name"]
    result=session.query(Products).all()
    l=[]
    id=0
    for i in result:
        if i.product_name == p_name:
            id=i.id
    if id!=0:
        result1=session.query(Orders).all()
        for j in result1:
            if j.product_id==id:
                d={
                    "MArket place":j.market_place,
                    "Quantity":j.quantity
                }
                l.append(d)
        return jsonify(l)
    else:
        return "Poda dei poi vera vela iruntha paaru"

@app.route("/userlogin",methods=["Get"])
def userlogin():
    data=request.json
    username=data["username"]
    password=data["password"]
    result2=session.query(Login).all()
    # print(result)
    # a=[username, password]
    l=[]
    for j in result2:
        d={
            "username":j.username,
            "password":j.password
        }
        l.append(d)
        if j.username==username and j.password==password:
            return "Welcome da Sambu Mavanaeee"
        else:
            return "veliya poda ayogiya rascal "
    return jsonify(l)






if __name__ == "__main__":
    app.run(debug=True)