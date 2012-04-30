from datetime import datetime

records = {}
debts = {}

class User(object):
	def __init__(self,idnum,name="",email=""):
		self.ID = idnum
		self.records = []						#List[Record]
		self.name = name						#String
		self.email = email						#String
		self.ex_types = {0:"Cash",1:"Bank",2:"Credit Card"}		#Dictionary


class Record(object):
	def __init__(self,latitude=0.0,longitude=0.0,amount=0.00,debt=[],ex_type=0,transfer_to=None,time=datetime.now()):
		idnum = len(records)
		self.ID = idnum								#Int
		self.time = time							#Datetime
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

users = {0:User(0,"Haoyi Li","haoyi@li.com"),1:User(1,"Nahom Workie","nahom@workie.com"),2:User(2,"Akira Monri","akira@monri.com")}
users[0].records.append(Record(1.296383,103.848953,25.25))

users[1].records.append(Record(42.361778,-71.090426,30.20,[Debt(100.00,users[0])]))

users[2].records.append(Record(35.685361,139.753368,10.50,[Debt(50.00,users[1]),Debt(40.50,users[1]),Debt(10.15,None,users[0]),Debt(10.55,None,users[1])]))
users[2].records.append(Record(1.296383,103.848953,40.00,[],0,1))
