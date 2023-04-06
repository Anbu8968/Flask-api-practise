from flask import Flask,render_template,request,jsonify
from flask_mail import Mail,Message
from random import *
from functools import wraps
import datetime
import jwt


app=Flask(__name__)
mail=Mail(app)


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"]="anbu2872001@gmail.com"
app.config["MAIL_PASSWORD"]="enter password"
# app.config["MAIL_USE_TLS"]="True"
app.config["MAIL_USE_SSL"]=False

mail=Mail(app)
# otp=randint(0000000,9999999)


app.config["SECRET_KEY"]="2ff6d8d552d24a90977b6591647bb561"
ALGORITHM="HS256"


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


@app.route("/")
def home():
    return "Welcome"

@app.route("/verify",methods=["POST"])
def verify():
    data=request.json
    email=data["email"]
    token=jwt.encode({'username':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=60)},app.config["SECRET_KEY"])
    msg=Message(subject="link",sender="Anbu",recipients=[email])
    msg.body=str("http://127.0.0.1:5000/validate?token="+str(token))
    mail.send(msg)
    return "mail sended"

@app.route("/validate",methods=["POST","GET"])
@token_required
def validate():
    return "verified"

if __name__=="__main__":
    app.run(debug=True)
