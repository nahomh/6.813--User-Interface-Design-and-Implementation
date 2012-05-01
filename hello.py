from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from models import *
from datetime import *
app = Flask(__name__)
app.debug = True

myUserId = 2
my_records=[]
urecords={}
@app.context_processor
def utility_processor():
	def two_decimal(amount):
		s = "%.2f" % float(amount)
		return s
	return dict(two_decimal=two_decimal)

@app.route('/')
def root_route():
	return record_route()


@app.route('/transfer/')
@app.route('/transfer/<id>')
def transfer_route(id=None):
	record = Record() if id == None else records[int(id)]
	return render_template("transfer.html", my_ex_types=users[myUserId].ex_types, record=record,is_new=(id==None))

	
@app.route('/transfer_callback/<id>', methods=['POST','GET'])
def transfer_callback(id):
	if request.method=='POST':
		record = records[int(id)]
		record.amount = float(request.form['amount'])
		record.ex_type = int(request.form['from'])
		record.transfer_to = int(request.form['to'])
		the_date = datetime(int(request.form['year']),int(request.form['month']),int(request.form['day']))
		record.time = the_date
		if request.form["isNew"]=="1": users[myUserId].records += [record]
		return redirect('/transfer/'+id)
	else:
		return redirect('/transfer/')

	
@app.route('/debts')
def debts_route():

	for r in users[myUserId].records:
		for d in r.debts:
			if d.lender != None:
				my_records.append(["Debt ID: " + str(d.ID),
					 d.lender.name,
					"$" + "%.2f" % d.amount,
					"lender"])
				
			else:
				my_records.append(["Debt ID: " + str(d.ID),
					d.borrower.name,
					"$" + "%.2f" % d.amount,
					"borrower"])
					
	for record in my_records:
		print record
		if record[1] in urecords.keys():
			urecords[record[1]].append(record)
		else:
			urecords[record[1]]=[record]
	
	return render_template("debts.html", my_records = my_records, urecords=urecords)

def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item): 
      return item
      
@app.route('/debt_callback/<recordid>/<debtid>')	
def debts_callback(recordid, debtid):
    record = records[int(recordid)]
    debt = debts[int(debtid)]
    lender, borrower = (users[myUserId], find(lambda u: u.name == request.args["other"], users.values()))
    if request.args["type"] == "Owe": 
        lender, borrower = borrower, lender
    debt.lender = lender
    debt.borrower = borrower
    debt.amount = float(request.args["amount"])
    record.debts += [debt]

    return redirect("/record/"+recordid)
    
@app.route('/record/')
@app.route('/record/<id>')
def record_route(id=None):
    return render_template("records.html", record = users[myUserId].tempRecord)

@app.route('/record_callback/<id>', methods=['POST']) 	
def record_callback(id):
    print "OMG"
    print request.form
    print request.args
    record = users[myUserId].tempRecord
    users[myUserId].tempRecord.location = (request.args["lat"], request.args["lng"])
    users[myUserId].tempRecord.amount = float(request.args["amount"])
    users[myUserId].tempRecord.ex_type = request.args["type"]
    users[myUserId].tempRecord.time = datetime(int(request.args["year"]), int(request.args["month"]), int(request.args["day"]))
    print "OK"  
    return "Ok"

@app.route('/record_commit/<id>')
def record_commit(id):    
    users[myUserId].records += [users[myUserId].tempRecord]
    users[myUserId].tempRecord = Record()
    return redirect("/record/"+id)

@app.route('/analytics')
def analytics_route():
	records = users[myUserId].records
	records.sort(key=lambda rec:rec.time)
	return render_template("analytics.html", records=records)

@app.route('/invdebt')
@app.route('/invdebt/<id>')
def debt_records_route(id=None):
	us_rec=[]
	for i in my_records:
		if i in us_rec:
			break
		else:
			if i[1]==id:
				print i[1]
				us_rec.append(i)
		
	return render_template("invdebt.html",urec = us_rec, my_records=my_records)

@app.route('/addDebts/<recordId>')
@app.route('/addDebts/<recordId>/<id>')
def add_debts_route(recordId, id=None):
    debt = Debt() if id == None else debts[int(id)]
    return render_template("addDebts.html", debt=debt, recordId=recordId)	
	

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
				if d.lender != users[myUserId]:
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
