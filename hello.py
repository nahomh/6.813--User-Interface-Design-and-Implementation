from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import itertools
from models import *
from datetime import *
from flasklogin import *
from  collections import defaultdict 
import math
import itertools
app = Flask(__name__)
app.debug = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(userid):
    return users[userid] if userid in users.keys() else None

    
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return "Logged Out Lolz"
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    global users
    email = request.form["email"] if "email" in request.form else None
    password = request.form["password"] if "password" in request.form else None
    matchedusers = [u for u in users.values() if (u.email == email and u.password == password)]
    
    if len(matchedusers)> 0:
        login_user(matchedusers[0])
        return redirect("/")
        
    if "name" in request.form:
        login_user(User(request.form["name"], email, password))
        
        return redirect("/")
        
    anyusers = [u for u in users.values() if u.email == email]
    if email and len(anyusers) == 0:
        return render_template("login.html", email=email, password=password, registering=True)
            
    return render_template("login.html")
    
@app.context_processor
def utility_processor():    
    def two_decimal(amount):
        x=math.fabs(amount)
        s = "%.2f" % float(x)
        return s
    return dict(two_decimal=two_decimal, zip=zip, len=len)

@app.route('/')
@login_required
def root_route():
    return record_route()


@app.route('/transfer/')
@app.route('/transfer/<id>')
@login_required
def transfer_route(id=None):
    record = Record() if id == None else records[int(id)]
    return render_template("transfer.html", my_ex_types=current_user.ex_types, record=record,is_new=(id==None))
    
@app.route('/transfer_callback/<id>', methods=['POST','GET'])
@login_required
def transfer_callback(id):
    if request.method=='POST':
        record = records[int(id)]
        record.amount = float(request.form['amount'])
        record.ex_type = int(request.form['from'])
        record.transfer_to = int(request.form['to'])
        the_date = date(int(request.form['year']),int(request.form['month']),int(request.form['day']))
        record.time = the_date
        if request.form["isNew"]=="1": current_user.records += [record]
        return redirect('/transfer/'+id)
    else:
        return redirect('/transfer/')

    
@app.route('/debts')
@login_required
def debts_route():
    full_debts = defaultdict(float) #dict with default value
        
    for d in debts.values():
        if d.lender!=None and d.borrower!=None:
            if d.lender.ID==current_user.ID: full_debts[d.borrower] += d.amount
            elif d.borrower.ID==current_user.ID: full_debts[d.lender] -=d.amount
    
    return render_template("debts.html", full_debts=full_debts, myUserId=current_user.ID)


def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item): 
      return item
      
@app.route('/debt_callback/<recordid>/<debtid>', methods=['POST','GET'])	
@app.route('/debt_callback/<recordid>/<debtid>/<backToRecord>', methods=['POST','GET'])	
@login_required
def debts_callback(recordid, debtid, backToRecord = False):
    record = records[int(recordid)]
    debt = debts[int(debtid)]
    lender, borrower = (current_user, find(lambda u: u.name == request.form["other"], users.values()))
    if request.form["type"] == "Owe": 
        lender, borrower = borrower, lender
    debt.lender = lender
    debt.borrower = borrower
    debt.amount = float(request.form["amount"])
    record.debts += [debt]
    
    if backToRecord: return ""
    else: return ""
    
@app.route('/record/')
@app.route('/record/<id>')
@login_required
def record_route(id=None):

    return render_template("records.html", 
                           record = current_user.tempRecord if id==None else records[int(id)], 
                           my_accounts=current_user.ex_types,
                           newRecord = id == None)

@app.route('/record_callback/<id>', methods=['POST']) 	
@login_required
def record_callback(id):
    
    record = current_user.tempRecord
    current_user.tempRecord.location = (request.args["lat"], request.args["lng"])
    current_user.tempRecord.amount = float(request.args["amount"])
    current_user.tempRecord.ex_type = int(request.args["type"])
    current_user.tempRecord.time = date(int(request.args["year"]), int(request.args["month"]), int(request.args["day"]))
    return "Ok"

@app.route('/record_commit/<id>')
@login_required
def record_commit(id):    

    current_user.records.append(current_user.tempRecord)
    current_user.tempRecord = Record()
    return redirect("/analytics/list")

@app.route('/analytics')
@app.route('/analytics/<analytics_type>')

@app.route('/analytics/<analytics_type>/<year>/<month>/<day>')
def analytics_route(analytics_type = "list", year=None,month=None,day=None):

    exType = 0
    try: 
        exType = int(request.args.get("account"))
    except Exception: pass    
    user = current_user

    records = user.records
    
    records.sort(key=lambda rec:rec.time)
    
    if (analytics_type == "list"):


        if(year==None or month==None or day==None):
            return render_template("list.html", groupedRecords=itertools.groupby(records, lambda x: x.time), ex_types=current_user.ex_types, viewAccount=exType, user=user)
        else:
            itered = itertools.groupby(records, lambda x:x.time)
            limitDate = date(int(year),int(month),int(day))
            limited = []
            for k, g in itered:
                if k == limitDate:
                    for r in g:
                        limited += [r]
            regrouped = itertools.groupby(limited, lambda x:x.time)
            return render_template("list.html", groupedRecords=regrouped, ex_types=current_user.ex_types, viewAccount=exType, user=user)

    elif(analytics_type == "map"):
        return render_template("map.html", records=records, ex_types=current_user.ex_types, viewAccount=exType, user=user)

    elif(analytics_type == "chart"):
        import json
        from flask import Markup
        chartDataR = []
        chartDataR += [['Date','Amount']]
        chartDataD = {}
        today = date.today()

        import sys
        try:
            offset = int(request.args.get("offset"))
        except Exception:
            offset = 0
        try:
            wkoffset = int(request.args.get("hioffset"))
        except Exception:
            wkoffset=0
        try:
            viewer = int(request.args.get("view"))
        except Exception:
            viewer = 0

        fromDate = None
        if viewer == 0:
            for x in range(0+offset,7+offset):
                newDay = today - timedelta(x,0,0,0,0,0,wkoffset)
                chartDataD[newDay] = 0
            fromDate = newDay
        else:
            import calendar
            for x in range(1,calendar.monthrange(today.year-wkoffset,today.month-offset)[1]+1,1):
                newDay = date(today.year-wkoffset,today.month-offset,x)
                chartDataD[newDay] = 0
                if fromDate==None: fromDate = newDay

        itered = itertools.groupby(records,lambda x:x.time)
        for k,g in itered:
            if k in chartDataD.keys():
                totalAmount = 0
                for r in g:
                    if r.ex_type==exType:
                        totalAmount += r.amount
                chartDataD[k] += totalAmount
        
        for d in sorted(chartDataD.iterkeys()):
           chartDataR += [[str(d.month)+"/"+str(d.day),chartDataD[d]]]
        chartData = json.dumps(chartDataR)

        return render_template("chart.html", records=records, ex_types=current_user.ex_types, viewAccount=exType, chartData=Markup(chartData), user=user,analytics_type=analytics_type, wkoff=wkoffset, off=offset, viewer=viewer, fromDate=fromDate)

@app.route('/chartToList/<fyear>/<fmonth>/<fday>/<row>')
def chartToList_route(fyear=None,fmonth=None,fday=None,row=None):
    if(fyear==None or fmonth==None or fday==None or row==None):
        return redirect('/analytics/chart')
    
    fromDay = date(int(fyear),int(fmonth),int(fday))
    limitDate = fromDay + timedelta(int(row))
    return redirect('/analytics/list/'+str(limitDate.year)+'/'+str(limitDate.month)+'/'+str(limitDate.day))


@app.route('/invdebt')
@app.route('/invdebt/<person_id>')
@login_required
def debt_inv_route(person_id=None):
    
    debt_records = {}    # Dict[Debt:Record]
    for r in records.values():
        for d in r.debts:
            if d.lender.ID==int(person_id) and d.borrower==current_user:
                debt_records[d] = r
            elif d.borrower.ID==int(person_id) and d.lender==current_user:
                debt_records[d] = r
    return render_template("invdebt.html",user=users[int(person_id)], debt_records=debt_records, myUserId=current_user.ID)

@app.route('/recdebt')
@app.route('/recdebt/<record_id>')
@login_required
def record_debt_route(record_id=None):    
    debt_records = {}	# List[(Debt,Record)]
    r = records[int(record_id)]
    for d in r.debts:
        debt_records[d] = r
        
    return render_template("invdebt.html",debt_records=debt_records, myUserId=current_user.ID)
    
@app.route('/addDebts/<recordId>')
@app.route('/addDebts/<recordId>/<id>')
@login_required
def add_debts_route(recordId, id=None):
    debt = Debt() if id == None else debts[int(id)]
    user_list=[]
    for i in users.keys():
        user_list.append(users[i].name)

    if id==None:
        backToRecords=True
    else:
        backToRecords=False

    return render_template("addDebts.html", debt=debt, recordId=recordId, user=current_user, user_list=user_list, backToRecords=backToRecords)	


if __name__ == '__main__':
    app.run()
