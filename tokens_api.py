from flask import Flask,request,jsonify,make_response,render_template,session,flash
import jwt
# from datetime import datetime,timedelta
import datetime
from functools import wraps

app=Flask(__name__)

app.config["SECRET_KEY"]="2ff6d8d552d24a90977b6591647bb561"
ALGORITHM="HS256"


def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        data=request.json
        token=data["token"]
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
    if not session.get("logged_in"):
        return "please login"
    else:
        return "login success"


@app.route("/auth")
@token_required
def auth():
    return "JWT IS VERIFIED WELCOME TO DASHBOARD"


@app.route("/login")
def login():
    data=request.json
    if data["username"] and data["password"]=="12345":
        session["logged_in"]=True
        token=jwt.encode({'username':data["username"],'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=60)},app.config["SECRET_KEY"])
        print(token)
        payload=jwt.decode(token,app.config["SECRET_KEY"],algorithms=ALGORITHM)
        username=payload.get("username")

        return jsonify({"token":token,"username":username})
    else:
        return make_response("unable to verify",403,{'WWW-Authenticate':'Basic realm:"Authentication Failed"' })

@app.route("/logout",methods=["POST"])
def logout():
    pass



if __name__=="__main__":
    app.run(debug=True)