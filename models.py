from datetime import *

records = {}
debts = {}
users = {}
class User(object):
    def __init__(self,name="",email="", password="password"):
        self.ID = len(users)
        users[self.ID] = self
        self.tempRecord = Record()
        self.records = []						#List[Record]
        self.name = name						#String
        self.email = email						#String
        self.password = password                #String
        self.ex_types = {0:"Cash",1:"Bank",2:"Credit Card"}		#Dictionary

    def recordCenter(self):
        print "MOOO I AM A COW"
        total = (0, 0)
        for record in self.records:
            lat, long = record.location
            oldLat, oldLong = total
            total = (lat + oldLat, long + oldLong)
            print total
        return (total[0] / len(self.records), total[1] / len(self.records))
    
    def recordStdDev(self):
        center = self.recordCenter()
        total = 0
        for record in self.records:
            lat, long = record.location
            oldLat, oldLong = center
            total += ((lat + oldLat) ** 2 + (long - oldLong) ** 2)
        return (total / len(self.records)) ** 0.5    

    def is_active(self): return True
    def is_authenticated(self): return True
    def is_anonymous(self): return False
    def get_id(self): return self.ID
class Record(object):
    def __init__(self,latitude=0.0,longitude=0.0,amount=0.00,debt=[],ex_type=0,transfer_to=None,time=date.today()):
        idnum = len(records)
        self.ID = idnum								#Int
        self.time = time							#date
        self.location = (latitude,longitude)		#(Number, Number)
        self.debts = debt							#List[Debt]
        self.amount = amount						#Number
        self.ex_type = ex_type						#Int
        self.transfer_to = transfer_to				#Int/None
        records[idnum] = self
        

class Debt(object):
    def __init__(self,amount=0.00,lender=None,borrower=None):
        idnum = len(debts)
        self.ID = idnum					#Int
        self.lender = lender				#User
        self.borrower = borrower			#User
        self.amount = amount				#Number
        debts[idnum] = self

User("Haoyi Li","haoyi@li.com")
User("Nahom Workie","nahom@workie.com")
User("Akira Monri","akira@monri.com")
print users
users[0].records.append(Record(1.296383,103.848953,25.25))

users[1].records.append(Record(42.361778,-71.090426,30.20,[Debt(100.00,users[0],users[1])]))

users[2].records.append(Record(42.359926,-71.095831,10.50,[Debt(50.00,users[1],users[2]),Debt(40.50,users[1],users[2]),Debt(10.15,users[2],users[0]),Debt(10.55,users[2],users[1])]))
users[2].records.append(Record(42.358956,-71.09416,17.00,[],0,1))
users[2].records.append(Record(42.362793,-71.090748,9.00,[],0,1))
users[2].records.append(Record(42.362904,-71.099696,47.00,[],0,1))
