from datetime import datetime

class User(object):
	def __init__(self,name="",email=""):
		self.records = []						#List[Record]
		self.name = name						#String
		self.email = email						#String

class Record(object):
	def __init__(self,longitude,latitude,amount,debt=[],time=datetime.now()):
		self.time = time						#Long
		self.location = (longitude,latitude)	#(Number, Number)
		self.debts = debt						#List[Debt]
		self.amount = amount					#Number

class Debt(object):
	def __init__(self,amount,lender=None,borrower=None):
		self.lender = lender					#User
		self.borrower = borrower				#User
		self.amount = amount					#Number

users = {0:User("Haoyi Li","haoyi@li.com"),1:User("Nahom Workie","nahom@workie.com"),2:User("Akira Monri","akira@monri.com")}
users[0].records.append(Record(1.296383,103.848953,25.25))

users[1].records.append(Record(42.361778,-71.090426,30.20,[Debt(100.00,users[0])]))

users[2].records.append(Record(35.685361,139.753368,10.50,[Debt(50.00,users[1]),Debt(40.50,users[1]),Debt(10.15,None,users[0]),Debt(10.55,None,users[1])]))
