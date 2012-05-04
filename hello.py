from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import itertools
from models import *
from datetime import *
app = Flask(__name__)
app.debug = True

myUserId = 2
urecords={}
@app.context_processor
def utility_processor():    
    def two_decimal(amount):
        s = "%.2f" % float(amount)
        return s
    return dict(two_decimal=two_decimal, zip=zip)

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
    debtsPerPerson={}
    debt_records = []		
    for r in users[myUserId].records:
        for d in r.debts:
            debt_records.append(d)	
			
    for debt in debt_records:
        if debt.lender.ID == myUserId:
                if  debt.borrower.name in debtsPerPerson.keys():
                    debtsPerPerson[debt.borrower.name].append(debt)
                else:
                    debtsPerPerson[debt.borrower.name]=[debt]
        else:
                if  debt.lender.name in debtsPerPerson.keys():
                    debtsPerPerson[debt.lender.name].append(debt)
                else:
                    debtsPerPerson[debt.lender.name]=[debt]

    return render_template("debts.html", debt_records = debt_records, debtsPerPerson=debtsPerPerson, myUserId=myUserId)

def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item): 
      return item
      
@app.route('/debt_callback/<recordid>/<debtid>')	
@app.route('/debt_callback/<recordid>/<debtid>/<backToRecord>')	
def debts_callback(recordid, debtid, backToRecord = False):
    record = records[int(recordid)]
    debt = debts[int(debtid)]
    lender, borrower = (users[myUserId], find(lambda u: u.name == request.args["other"], users.values()))
    if request.args["type"] == "Owe": 
        lender, borrower = borrower, lender
    debt.lender = lender
    debt.borrower = borrower
    debt.amount = float(request.args["amount"])
    record.debts += [debt]
    
    if backToRecord: return redirect("/record/"+recordid)
    else: return redirect("/invdebt/"+str(debt.lender.ID if debt.lender != users[myUserId] else debt.borrower.ID))
    
@app.route('/record/')
@app.route('/record/<id>')
def record_route(id=None):
    return render_template("records.html", record = users[myUserId].tempRecord if id==None else records[int(id)], my_accounts=users[myUserId].ex_types)

@app.route('/record_callback/<id>', methods=['POST']) 	
def record_callback(id):
    
    record = users[myUserId].tempRecord
    users[myUserId].tempRecord.location = (request.args["lat"], request.args["lng"])
    users[myUserId].tempRecord.amount = float(request.args["amount"])
    users[myUserId].tempRecord.ex_type = int(request.args["type"])
    users[myUserId].tempRecord.time = datetime(int(request.args["year"]), int(request.args["month"]), int(request.args["day"]))
    return "Ok"

@app.route('/record_commit/<id>')
def record_commit(id):    

    users[myUserId].records.append(users[myUserId].tempRecord)
    users[myUserId].tempRecord = Record()
    return redirect("/analytics/list")

@app.route('/analytics')
@app.route('/analytics/<analytics_type>')
def analytics_route(analytics_type = "list"):
    exType = 0
    try: 
        exType = int(request.args.get["account"])
    except Exception: pass
        
    
    
    
    user = users[myUserId]
    records = user.records
    
    records.sort(key=lambda rec:rec.time)
    
    if (analytics_type == "list"):
        return render_template("list.html", groupedRecords=itertools.groupby(records, lambda x: x.time), ex_types=users[myUserId].ex_types, viewAccount=exType, user=user)
        
    elif(analytics_type == "map"):
        return render_template("map.html", records=records, ex_types=users[myUserId].ex_types, viewAccount=exType, user=user)
        
    elif(analytics_type == "chart"):
        import json
        from flask import Markup
        chartDataR = []
        chartDataR += [['Date','Amount']]
        for r in records:
            chartDataR += [[str(r.time.year)+'/'+str(r.time.month)+'/'+str(r.time.day),r.amount]]
        chartData = json.dumps(chartDataR)
        print chartData
        return render_template("chart.html", records=records, ex_types=users[myUserId].ex_types, viewAccount=exType, chartData=Markup(chartData), user=user)

@app.route('/invdebt')
@app.route('/invdebt/<id>')
def debt_records_route(id=None):

    deep_rec=[]         # List[Debts]
    debt_records = []	# List[Record]    
    for r in users[myUserId].records:
        for d in r.debts:
                debt_records.append(d)	
				
    for i in debt_records:
		if i.lender.ID ==int(id) or i.borrower.ID ==int(id):
			deep_rec.append(i)
        
    return render_template("invdebt.html",urec = deep_rec, debt_records=debt_records, myUserId=myUserId)


@app.route('/addDebts/<recordId>')
@app.route('/addDebts/<recordId>/<id>')
def add_debts_route(recordId, id=None):
    debt = Debt() if id == None else debts[int(id)]
    user_list=[]
    for i in users.keys():
	    user_list.append(users[i].name)
	
		
    return render_template("addDebts.html", debt=debt, recordId=recordId, user=users[myUserId], user_list=user_list, backToRecord=id==None)	
    


if __name__ == '__main__':
    app.run()
