from flask import Flask
from flask import render_template
from models import *
app = Flask(__name__)
app.debug = True

@app.route('/analytics')
def analytics():
	return render_template("analytics.html")

@app.route('/transfer')
def transfer():
	return render_template("transfer.html")

@app.route('/debts')
def debts():
	return render_template("debts.html")

@app.route('/record')
def record():
	return render_template("records.html")
	
@app.route('/analytics')
def analytics():
	return render_template("analytics.html")

@app.route("/data-test")
def datatest():
	output = ""
	output += "Number of Users: " + str(len(users)) + "<br><br>"
	for i in range(len(users)):
		output += "<b>User ID: " + str(i) + "</b><br>"
		output += "Number of Records: " + str(len(users[i].records)) + "<br>"
		for r in users[i].records:
			output += "Record Time: " + str(r.time) + "<br>"
			output += "Record Location: " +str(r.location) + "<br>"
			output += "Number of Debts: " + str(len(r.debts)) + "<br>"

	
	return output

if __name__ == '__main__':
	app.run()
