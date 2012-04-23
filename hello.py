from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True





@app.route('/analytics')
def hello_world():
    return render_template("analytics.html")

@app.route('/transfer')
def hello_world():
    return render_template("transfer.html")
    
@app.route('/debts')
def hello_world():
    return render_template("debts.html")
    
@app.route('/record')
def hello_world():
    return render_template("records.html")


if __name__ == '__main__':
    app.run()
