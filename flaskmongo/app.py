from flask import Flask, json, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_json import JsonRequest, JsonError, JsonTestResponse
from flask_wtf import FlaskForm
from flask_json import jsonify
from json import dumps
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='template')
app.debug = True
app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://localhost:27017/users"

bootstrap = Bootstrap(app)
mongo = PyMongo(app)

@app.route ("/")
def main():
    return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('login.html')

@app.route("/signup", methods=['POST','GET'])
def signup():
	_json = request.form
	_name = _json['name']
	_email = _json['email']
	_password = _json['password']
	if _name and _email and _password and request.method == "POST":
		conn = mongo.db.users
		_hashed_password = generate_password_hash(_password)
		conn.insert_one({'name':_name,'email':_email,'password':_hashed_password})

		return render_template('board.html')
			 
	else:
		return not_found()	

@app.route("/core")
def core():
	return render_template('board.html')

@app.errorhandler(404)
def not_found(error=None):
 	massage = {
 	'status' : 404,
 	'massage' : 'Not_Found' + request.url
 	}

 	resp = jsonify(massage)

 	resp.status_code = 404

 	return resp

if __name__ == "__main__":
	app.run()

