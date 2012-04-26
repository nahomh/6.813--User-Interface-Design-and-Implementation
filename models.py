from datetime import datetime

class User(object):
	def __init__(self,idnum,name="",email=""):
		self.ID = idnum
		self.records = []				#List[Record]
		self.name = name				#String
		self.email = email				#String

class Record(object):
	def __init__(self,idnum,longitude,latitude,amount,debt=[],time=datetime.now()):
		self.ID = idnum					#Int
		self.time = time				#Long
		self.location = (longitude,latitude)		#(Number, Number)
		self.debts = debt				#List[Debt]
		self.amount = amount				#Number

class Debt(object):
	def __init__(self,idnum,amount,lender=None,borrower=None):
		self.ID = idnum					#Int
		self.lender = lender				#User
		self.borrower = borrower			#User
		self.amount = amount				#Number

class Records(object):
	def __init__(self):
		self.records = {}
	
	def addRecord(self,longitude,latitude,amount,debt=[],time=datetime.now()):
		newId = len(self.records)
		newRec = Record(newId,longitude,latitude,amount,debt,time)
		self.records[newId] = newRec
		return newRec

class Debts(object):
	def __init__(self):
		self.debts = {}
	
	def addDebt(self,amount,lender=None,borrower=None):
		newId = len(self.debts)
		newDebt = Debt(newId,amount,lender,borrower)
		self.debts[newId] = newDebt
		return newDebt


records = Records()
debts = Debts()
users = {0:User(0,"Haoyi Li","haoyi@li.com"),1:User(1,"Nahom Workie","nahom@workie.com"),2:User(2,"Akira Monri","akira@monri.com")}
users[0].records.append(records.addRecord(1.296383,103.848953,25.25))

users[1].records.append(records.addRecord(42.361778,-71.090426,30.20,[debts.addDebt(100.00,users[0])]))

users[2].records.append(records.addRecord(35.685361,139.753368,10.50,[debts.addDebt(50.00,users[1]),debts.addDebt(40.50,users[1]),debts.addDebt(10.15,None,users[0]),debts.addDebt(10.55,None,users[1])]))
