from datetime import datetime

class User(object):
    def __init__(self):
        self.records = []       #List[Record]
    

class Record(object):
    def __init__(self,longitude,latitude,debt=[],time=datetime.now()):
        self.time = time        #Long
        self.location = (longitude,latitude)    #(Number, Number)
        self.debts = debt         #List[Debt]
        
class Debt(object):
    def __init__(self,amount,lender=None,borrower=None):
        self.lender = lender      #User
        self.borrower = borrower    #User
        self.amount = amount         #Number

users = {0:User(),1:User(),2:User()}
users[0].records.append(Record(40.77377,-73.983307))

users[1].records.append(Record(35.685361,139.753368,[Debt(100.00,0)]))

users[2].records.append(Record(35.685361,139.753368,[Debt(50.00,1),Debt(40.50,1),Debt(10.15,None,0),Debt(10.55,None,1)]))
