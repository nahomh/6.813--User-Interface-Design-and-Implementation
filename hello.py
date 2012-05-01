from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from models import *
from datetime import *
app = Flask(__name__)
app.debug = True

myUserId = 2
urecords={}

@app.route('/')
def root_route():
	return record_route()


@app.route('/transfer')
def transfer_route():
	return render_template("transfer.html", my_ex_types=users[myUserId].ex_types, today=datetime.now())

	
	
@app.route('/debts')
def debts_route():

	my_records=[]
	urecords={}
	debt_records = []		
	for r in users[myUserId].records:
		for d in r.debts:
			debt_records.append(d)	
	for debt in debt_records:
		if debt.lender == myUserId:
				if  debt.borrower in urecords.keys():
					urecords[debt.borrower].append(debt)
				else:
					urecords[debt.borrower]=[debt]
		else:
				if  debt.lender in urecords.keys():
					urecords[debt.lender].append(debt)
				else:
					urecords[debt.lender]=[debt]
	print debt_records
	print "Break" 
	print urecords
	return render_template("debts.html", debt_records = debt_records, urecords=urecords, myUserId=myUserId)

@app.route('/record/')
@app.route('/record/<id>')
def record_route(id=None):
    record = Record() if id == None else records[int(id)]
    return render_template("records.html", record = record)

@app.route('/record_callback/<id>')	
def record_callback(id):
    record = records[int(id)]
    record.location = (request.args["lat"], request.args["lng"])
    record.amount = float(request.args["amount"])
    record.ex_type = request.args["type"]
    record.time = date(int(request.args["year"]), int(request.args["month"]), int(request.args["day"]))
    print "CALLBACK"
    print request.args
    users[myUserId].records += [record]
    
    return redirect("/record/"+id)
    
@app.route('/analytics')
def analytics_route():
    records = users[myUserId].records
    return render_template("analytics.html", records=records)

@app.route('/invdebt')
@app.route('/invdebt/<id>')
def debt_records_route(id=None):
	us_rec=[]
	debt_records = []	
	for r in users[myUserId].records:
		for d in r.debts:
				debt_records.append(d)								
	for i in debt_records:
		if i in us_rec:
			break
		else:
			if i.lender ==myUserId or i.borrower == myUserId:
				us_rec.append(i)

		
	return render_template("invdebt.html",urec = us_rec, debt_records=debt_records, myUserId=myUserId)

@app.route('/addDebts/')
@app.route('/addDebts/<id>')
def add_debts_oute(id=None):
    debt = Debt() if id == None else debts[int(id)]
    return render_template("addDebts.html", debt=debt)	
	

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
