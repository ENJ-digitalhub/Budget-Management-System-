import sqlite3
import database  

class Commands:
	def __init__(self, db=None):
		if db:
			self.db = db
		else:
			self.db = database.Database()
		self.command=""
		self.commandList=[]
		self.mainCommands=("allowance","expenses","income","savings")
		self.typeCommands={"add":self.addExecutor,\
								"remove":self.removeExecutor,\
								"modify":self.modifyExecutor,\
								"show":self.showExecutor,\
								"total":self.totalExecutor}
	def commandParser(self,command):
		self.command= command
		return self.command.split(" ")
		pass
	def isValid(self,commandList):
		self.commandList=commandList
		while len(self.commandList) != 5:
			self.commandList.append("")
		if self.commandList[0] in self.mainCommands and \
		self.commandList[1] in self.typeCommands.keys():
			print("Valid Command")
			self.typeCommands[self.commandList[1]](self.commandList)
		else:
			print("Invalid Command")
		pass	
	def addExecutor(self,commandList):
		self.commandList=commandList
		print("adding...")
		sql = f"""
			INSERT INTO {self.commandList[0]} (amount)
			VALUES (?)
			"""
		params = (self.commandList[2],)
		sql2 = f"""
			INSERT INTO {self.commandList[0]} (amount,label)
			VALUES (?,?)
			"""
		params2 = (self.commandList[2],self.commandList[3])
		try:
			self.db.run(sql2,params2)
		except sqlite3.OperationalError:
			try:
				self.db.run(sql,params)
			except Exception as e:
				print(e)
		finally:
			if self.commandList[0] != "allowance":
				foriegn_key_sql = f"""
					UPDATE {self.commandList[0]}
					SET allowance_id = (
						SELECT id 
						FROM allowance 
						WHERE SUBSTR({self.commandList[0]}.created_at, 1, 10) = allowance.record_date
						LIMIT 1
					)
					WHERE EXISTS (
						SELECT 1
						FROM allowance 
						WHERE SUBSTR({self.commandList[0]}.created_at, 1, 10) = allowance.record_date
					);
				"""
				self.db.run(foriegn_key_sql)
			else:
				pass
	def removeExecutor(self,commandList):
		self.commandList=commandList
		print("removing...")
		sql = f"""
			DELETE FROM {self.commandList[0]} 
			WHERE id = (?)
			"""
		params = (self.commandList[2],)
		try:
			int(self.commandList[2])
			self.db.run(sql,params)
		except Exception as e:
			print(e)
	def modifyExecutor(self,commandList):
		self.commandList=commandList
		print("modifying...")
		sql = f"""
			UPDATE {self.commandList[0]}
			SET amount = ?,label = ?
			WHERE id = ?
			"""
		params = (self.commandList[3],self.commandList[4],self.commandList[2],)
		sql2 = f"""
			UPDATE {self.commandList[0]}
			SET amount = ?
			WHERE id = ?
			"""
		params2 = (self.commandList[3],self.commandList[2],)
		try:
			int(self.commandList[2])
			self.db.run(sql,params)
		except sqlite3.OperationalError:
			try:
				int(self.commandList[2])
				self.db.run(sql2,params2)
			except Exception as e:
				print(e)
	def showExecutor(self,commandList):
		self.commandList=commandList
		print("showing...")
		sql = f"""
			SELECT * FROM {self.commandList[0]}
			"""
		try:
			records = self.db.query(sql)
			for record in records:
				print(record)
			if len(records) == 0:
				print("(No records found...)")
		except Exception as e:
			print(e)
	"""
	def statusExecutor(commandList):
	
	def historyExecutor(commandList):
	
	def previousExecutor(commandList):
	
	def nextExecutor(commandList):
	"""
	def totalExecutor(self,commandList):
		self.commandList=commandList
		print("totaling...")
		sql = f"""
			SELECT SUM(amount) FROM {self.commandList[0]}
			"""
		sql2 = f"""
			SELECT SUM(amount) FROM {self.commandList[0]}
			WHERE SUBSTR(created_at, 1, 7) = (?)
			"""
		sql3 = f"""
			SELECT SUM(amount) FROM {self.commandList[0]}
			WHERE SUBSTR(record_date, 1, 7) = (?)
			"""
		try:
			if self.commandList[2]=="":
				records = self.db.query(sql)
				for record in records:
					print(record)
			else:
				try:
					if self.commandList[0] != "allowance":
						records = self.db.query(sql2, (self.commandList[2],))
						for record in records:
							print(record)
					else:
						records = self.db.query(sql3, (self.commandList[2],))
						for record in records:
							print(record)
				except Exception as e:
					print(e)
		except Exception as e:
					print(e)
	"""
	def searchExecutor(commandList):"""
	def executeCommand(self,command):
		self.command=command
		self.isValid(self.commandParser(self.command))