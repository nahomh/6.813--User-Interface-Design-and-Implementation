from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True





@app.route('/analytics')
def analytics():
    print "analytics"
    return render_template("analytics.html")

@app.route('/transfer')
def transfer():
    print "transfer"
    return render_template("transfer.html")
 

 
@app.route('/debts')
def debts():
    print "debts"
    return render_template("debts.html")
    


@app.route('/record')
def record():
    print "record"
    return render_template("records.html")


if __name__ == '__main__':
    app.run()
