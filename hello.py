from flask import Flask
from flask import render_template
from models import *
app = Flask(__name__)
app.debug = True

myUserId = 2

@app.route('/transfer')
def transfer_route():
	return render_template("transfer.html")

@app.route('/debts')
def debts_route():

	my_records=[]
	output="<ul data-role="listview" data-filter="true" id="listarea">"
	for r in users[myUserId].records:
		for d in r.debts:
			if d.lender != None:
				my_records.append(["Debt ID: " + str(d.ID,
					"Lender: " + d.lender.name,
					"Amount: $" + "%.2f" % d.amount,
					"lender"])
				
			else:
				my_records.append(["Debt ID: " + str(d.ID),
					"Borrower: " + d.borrower.name,
					"Amount: $" + "%.2f" % d.amount,
					"borrower"])

    return render_template("debts.html", my_records = my_records)

@app.route('/record/')
@app.route('/record/<id>')
def record_route(id=None):
    record = Record() if id == None else records[int(id)]
    return render_template("records.html", record = record)
	
@app.route('/analytics')
def analytics_route():
	return render_template("analytics.html")


@app.route("/data-test")
def datatest_route():
	output = "<html><head><title>Data Test</title></head><body>"
	output += "Number of Users: " + str(len(users)) + "<br><br>"
	for i in range(len(users)):
		output += "<b>User ID: " + str(i) + "</b><br>"
		output += "<b>User Name: " + users[i].name + " / " + users[i].email + "</b><br>"
		output += "&emsp;Number of Records: " + str(len(users[i].records)) + "<br>"
		for r in users[i].records:
			output += "&emsp;&emsp;Record ID: " + str(r.ID) + "<br>"
			output += "&emsp;&emsp;Record Time: " + str(r.time) + "<br>"
			output += "&emsp;&emsp;Record Location: " +str(r.location) + "<br>"
			output += "&emsp;&emsp;<img src=\"https://maps.googleapis.com/maps/api/staticmap?center=" + str(r.location[0]) + "," + str(r.location[1]) + "&zoom=14&size=400x100&sensor=false\"><br>"
			output += "&emsp;&emsp;Amount: $" + "%.2f" % r.amount +"<br>"
			output += "&emsp;&emsp;Number of Debts: " + str(len(r.debts)) + "<br>"
			if len(r.debts) > 0:
				output += "&emsp;&emsp;<b>Debt Record</b><br>"
			for d in r.debts:
				if d.lender != None:
					output += "&emsp;&emsp;&emsp;Debt ID: " + str(d.ID) + "<br>"
					output += "&emsp;&emsp;&emsp;Lender: " + d.lender.name + "<br>"
				else:
					output += "&emsp;&emsp;&emsp;Debt ID: " + str(d.ID) + "<br>"
					output += "&emsp;&emsp;&emsp;Borrower: " + d.borrower.name + "<br>"
				output += "&emsp;&emsp;&emsp;Amount: $" + "%.2f" % d.amount + "<br>"
			output += "<br>"
	
	for rc in range(len(records)):
		output += "Record ID: " + str(records[rc].ID) + "<br>"
	
	for db in range(len(debts)):
		output += "Debt ID: " + str(debts[db].ID) + "<br>"
	output += "</body></html>"

	return output

if __name__ == '__main__':
	app.run()
