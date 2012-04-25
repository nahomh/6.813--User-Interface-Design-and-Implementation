from datetime import datetime

class User(object):
    def __init__(self):
        self.records = []       #List[Record]
    

class Record(object):
    def __init__(self,longitude,latitude,debt=[],time=datetime.now()):
        self.time = time        #Long
        self.location = (longitude,latitude)    #(Number, Number)
        self.debts = debts         #List[Debt]
        
class Debt(object):
    def __init__(self,amount,lender=None,borrower=None):
        self.lender = lender      #User
        self.borrower = borrower    #User
        self.amount = amount         #Number

all = {0:User(),1:User(),2:User()}
all[0].records.append(Record(40.77377,-73.983307)

all2newRecord = Record()
all2newRecord.time = datetime.now()
all2newRecord.location = (35.685361,139.753368)
all1newDebt = Debt()
all1newDebt.lender = 0
all1newDebt.amount = 100.00
all[1].records.append(all2newRecord)
all[1].records.debts.append(Record(35.685361,139.753368)

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
