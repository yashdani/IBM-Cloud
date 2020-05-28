"""Cloud Foundry test"""
from flask import Flask, current_app, render_template, request, redirect, url_for
import os, json, requests, xmltodict
import ibm_db

import connect

app = Flask(__name__)

base_url = "https://s3.us-south.cloud-object-storage.appdomain.cloud/yashdani-bucket/"

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

# default
@app.route('/', methods=["GET"])
def hello_world():
	# return 'Hello World! I am running on port ' + str(port)
	return render_template('index.html', result={})

@app.route('/room', methods=["GET"])
def list_files():
	# sending get request and saving the response as response object
	data = requests.get(base_url)
	xpars = xmltodict.parse(data.text)
	st = ''
	for item in xpars["ListBucketResult"]['Contents']:
		st = st + 'name : ' + item["Key"]
		st = st + 'size : ' + item["Size"]
		st = st + '\n\n'

	return render_template('list_files.html', result=xpars["ListBucketResult"]['Contents'])

@app.route('/search_room', methods=["GET"])
def search_room():
	ret = [];
	return render_template('room_search.html', result=ret)

# search by name function
@app.route('/search_room', methods=["POST"])
def search_by_room():
	room = request.form["room"]

	sql = "SELECT * FROM quiz1people WHERE points = ?"
	stmt = ibm_db.prepare(connect.connection, sql)

	ibm_db.bind_param(stmt, 1, room)
	result = ibm_db.execute(stmt)

	result_dict = ibm_db.fetch_assoc(stmt)
	print(result_dict)

	return render_template('room_search.html', result=result_dict)

@app.route('/update', methods=["GET"])
def update_by_room():
	ret = [];
	return render_template('update.html', result=ret)

@app.route('/update', methods=["POST"])
def update():
	room = request.form["room"]
	keywords = request.form["keywords"]

	sql = "UPDATE quiz1people SET name = ? WHERE points = ?"
	stmt = ibm_db.prepare(connect.connection, sql)
	ibm_db.bind_param(stmt, 1, keywords)
	ibm_db.bind_param(stmt, 2, room)

	result = ibm_db.execute(stmt)
	return redirect(url_for("just_hello"))

@app.route('/list', methods=["GET"])
def just_hello():

	sql = "SELECT * FROM quiz1people;"
	stmt = ibm_db.prepare(connect.connection, sql)

	result = ibm_db.execute(stmt)
	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)

	while result_dict is not False:
		print(json.dumps(result_dict))
		ret.append(result_dict)
		result_dict = ibm_db.fetch_assoc(stmt)
	obj = {}
	obj['list'] = ret
	return json.dumps(ret)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
