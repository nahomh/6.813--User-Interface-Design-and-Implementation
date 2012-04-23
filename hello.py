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
def record():
    return render_template("analytics.html")


if __name__ == '__main__':
    app.run()
