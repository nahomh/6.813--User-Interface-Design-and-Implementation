from flask import Flask
from flask import render_template
from stuff import *
app = Flask(__name__)
app.debug = True


class Data:
    x = "1"
    
@app.route('/')
def hello_world():
    Data.x = Data.x + "1"
    return Data.x 
    #return render_template("traxx.html")

if __name__ == '__main__':
    app.run()