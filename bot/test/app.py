from flask import Flask, render_template, request,flash, redirect, jsonify
import jwt
import config
from functools import wraps


app = Flask(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.get_json())
        data  = request.get_json()
        token = data["token"]
        print("token")
        
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        
        try:
            data = jwt.decode(token, config.secret_key)
        except: 
            return jsonify({"message" : "Token is missing or invalid"}), 403
        
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
    return jsonify({"message": "Hi this is login page"})

@app.route("/authenticate", method=["POST"])
def authenticate():
    data = request.get_json()
    print(data)
    return jsonify({"message": "Hi this the authenticate route"})



@app.route("/test", methods=["POST"])
@token_required
def test():
    return "Success",200

if __name__=="__main__":
    app.run(debug=True, port="5001")
    