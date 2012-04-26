from datetime import datetime

records = {}
debts = {}

class User(object):
	def __init__(self,idnum,name="",email=""):
		self.ID = idnum
		self.records = []				#List[Record]
		self.name = name				#String
		self.email = email				#String
		self.ex_types = {0:"Cash",1:"Bank"}		#Dictionary

class Record(object):
	def __init__(self,longitude=0.0,latitude=0.0,amount=0.00,ex_type=0,debt=[],time=datetime.now()):
		idnum = len(records)
		self.ID = idnum					#Int
		self.time = time				#Long
		self.location = (longitude,latitude)		#(Number, Number)
		self.debts = debt				#List[Debt]
		self.amount = amount				#Number
		self.ex_type = ex_type				#Int
		records[idnum] = self

class Debt(object):
	def __init__(self,amount=0.00,lender=None,borrower=None):
		idnum = len(debts)
		print idnum
		self.ID = idnum					#Int
		self.lender = lender				#User
		self.borrower = borrower			#User
		self.amount = amount				#Number
		debts[idnum] = self
		print len(debts)

users = {0:User(0,"Haoyi Li","haoyi@li.com"),1:User(1,"Nahom Workie","nahom@workie.com"),2:User(2,"Akira Monri","akira@monri.com")}
users[0].records.append(Record(1.296383,103.848953,25.25))

users[1].records.append(Record(42.361778,-71.090426,30.20,[Debt(100.00,users[0])]))

users[2].records.append(Record(35.685361,139.753368,10.50,[Debt(50.00,users[1]),Debt(40.50,users[1]),Debt(10.15,None,users[0]),Debt(10.55,None,users[1])]))
