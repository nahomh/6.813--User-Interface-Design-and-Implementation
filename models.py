from datetime import datetime

class User(object):
    def __init__(self):
        self.records = []       #List[Record]
    
    all = {0:User(),1:User(),2:User()}
    all[0].time = datetime.now()
    all[0].location = (40.77377,-73.983307)
    
    all[1].time = datetime.now()
    all[1].location = (35.685361,139.753368)
    all1newDebt = Debt()
    all1newDebt.lender = 0
    all1newDebt.amount = 100.00
    all[1].debts.append(all1newDebt)

    all[2].time = datetime.now()
    all[2].location = (35.685361,139.753368)
    all2newDebt = Debt()
    all2newDebt.lender = 1
    all2newDebt.amount = 50.00
    all[2].debts.append(all2newDebt)
    all3newDebt = Debt()
    all3newDebt.lender = 1
    all3newDebt.amount = 40.50
    all[2].debts.append(all3newDebt)
    all4newDebt = Debt()
    all4newDebt.borrower = 0
    all4newDebt.amount = 10.15
    all[2].debts.append(all4newDebt)
    all5newDebt = Debt()
    all5newDebt.borrower = 1
    all5newDebt.amount = 10.55
    all[2].debts.append(all5newDebt)

class Record(object):
    def __init__(self):
        self.time = None        #Long
        self.location = None    #(Number, Number)
        self.debts = []         #List[Debt]
        
class Debt(object):
    def __init__(self):
        self.lender = None      #User
        self.borrower = None    #User
        self.amount = 0         #Number
