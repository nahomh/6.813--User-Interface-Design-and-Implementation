class User(object):
    def __init__(self):
        self.records = []       #List[Record]
        
    
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