import shlex
import sqlite3
import budget.database as database
from datetime import datetime

class Commands:
	def __init__(self, db=None):
		if db:
			self.db = db
		else:
			self.db = database.Database()  
		self.commandMethod = {
				"add":self.addExecutor,
				"remove":self.removeExecutor,
				"delete":self.deleteExecutor,
				"modify":self.modifyExecutor,
				"show":self.showExecutor,
				"total":self.totalExecutor,
				"status":self.statusExecutor,
				"search":self.searchExecutor,
				"report":self.reportExecutor
			}
   
	def commandParser(self,command):
		return shlex.split(command)
	
	def addExecutor(self,commandList):
		category, amount= commandList[0], commandList[2]
		
		print("adding...")
		sql = f"""
			INSERT INTO {category} (amount)
			VALUES (?)
			"""
		params = (amount,)
		sql2 = f"""
			INSERT INTO {category} (amount,label)
			VALUES (?,?)
			"""
		params2 = (amount,commandList[3],)
		try:
			# label = commandList[3]
			if self.db.run(sql2,params2):
					return [True, f"{amount} added for {commandList[3]} successfully to {category}"]
		except Exception:
			try:
				if self.db.run(sql,params):
					return [True, f"{amount} added successfully to {category}"]
			except Exception as e:
				return [False, f"An error occured! {e}"]
		finally:
			if category != "allowance":
				foriegn_key_sql = f"""
					UPDATE {category}
					SET allowance_id = (
						SELECT id 
						FROM allowance 
						WHERE SUBSTR({category}.created_at, 1, 10) = allowance.record_date
						LIMIT 1
					)
					WHERE EXISTS (
						SELECT 1
						FROM allowance 
						WHERE SUBSTR({category}.created_at, 1, 10) = allowance.record_date
					);
				"""
				self.db.run(foriegn_key_sql)
	
	def removeExecutor(self,commandList):
		category, amount = commandList[0], commandList[2]
		negative_amount = -float(amount)
		print("removing...")
		sql = f"""
			INSERT INTO {category} (amount)
			VALUES (?)
			"""
		params = (negative_amount,)
		sql2 = f"""
			INSERT INTO {category} (amount,label)
			VALUES (?,?)
			"""
		params2 = (negative_amount,commandList[3])
		try:
			# label = commandList[3]
			if self.db.run(sql2,params2):
				return [True, f"{amount} removed for {commandList[3]} successfully from {category}"]
		except Exception:
			try:
				if self.db.run(sql,params):
					return [True, f"{amount} removed successfully from {category}"]
			except Exception as e:
				return [False, f"An error occured! {e}"]
		finally:
			if category != "allowance":
				foriegn_key_sql = f"""
					UPDATE {category}
					SET allowance_id = (
						SELECT id 
						FROM allowance 
						WHERE SUBSTR({category}.created_at, 1, 10) = allowance.record_date
						LIMIT 1
					)
					WHERE EXISTS (
						SELECT 1
						FROM allowance 
						WHERE SUBSTR({category}.created_at, 1, 10) = allowance.record_date
					);
				"""
				self.db.run(foriegn_key_sql)

	def deleteExecutor(self,commandList):
		category, id = commandList[0], commandList[2]
		print("deleting...")
		sql = f"""
			DELETE FROM {category} 
			WHERE id = (?)
			"""
		params = (id,)
		try:
			if self.db.run(sql,params):
				return [True, f"ID {id} deleted successfully in {category}"]
			else:
				return [False, f"ID {id} not found in {category}"]
				pass
		except Exception as e:
			return [False, f"An error occured! {e}"]
   
	def modifyExecutor(self,commandList):
		category, id, amount, label = commandList[0], commandList[2], commandList[3], commandList[4]
		print("modifying...")
		sql = f"""
			UPDATE {category}
			SET amount = ?
			WHERE id = ?
			"""
		params = (amount,id,)
		sql2 = f"""
			UPDATE {category}
			SET amount = ?,label = ?
			WHERE id = ?
			"""
		params2 = (amount,label,id,)
		try:
			if self.db.run(sql2,params2):
				return [True, f"ID {id} updated successfully to {amount} for {label} in {category}"]
			else:
				return [False, "ID not found"]
				
		except sqlite3.OperationalError:
			try:
				if self.db.run(sql,params):
					return [True, f"ID {id} updated successfully to {amount} in {category}"]
				else:
					return [False, "ID not found"]
			except Exception as e:
				return [False, f"An error occured! {e}"]
    
	def showExecutor(self,commandList):
		category = commandList[0]
		print("showing...")
		sql = f"""
			SELECT * FROM {category}
			"""
		try:
			records = self.db.query(sql)
			for record in records:
				if len(records) == 0:
					return [False, f"No {category} found"]
				# If the record is not None, it means there are record for that date, so we can consider the status as the calculated value
				else:
					for record in records:
						print(record)
					return [True, f"End of records in {category}"]
		except Exception as e:
			return [False, f"An error occured! {e}"]
   
	def totalExecutor(self,commandList):
		category, date = commandList[0], commandList[2]
		print("totaling...")
		sql = f"""
			SELECT SUM(amount) FROM {category}
			"""
		sql2 = f"""
			SELECT SUM(amount) FROM {category}
			WHERE SUBSTR (created_at, 1, LENGTH(?)) = (?)
			"""
		sql3 = f"""
			SELECT SUM(amount) FROM {category}
			WHERE SUBSTR (record_date, 1, LENGTH(?)) = (?)
			"""
		try:
			if date == "":
				records = self.db.query(sql)
				for record in records:
					if len(records) == 0:
						return [False, f"No {category} found for {date}"]
					# If the record is not None, it means there are record for that date, so we can consider the status as the calculated value
					else:
						return [True, f"Total {category}: {record[0]}"]
			else:
				try:
					if commandList[0] != "allowance":
						records = self.db.query(sql2, (date,date,))
						for record in records:
							if len(records) == 0:
								return [False, f"No {category} found for {date}"]
							# If the record is not None, it means there are record for that date, so we can consider the status as the calculated value
							else:
								return [True, f"Total {category} for {date}: {record[0]}"]
					else:
						records = self.db.query(sql3, (date,date,))
						for record in records:
							if len(records) == 0:
								return [False, f"No {category} found for {date}"]
							# If the record is not None, it means there are record for that date, so we can consider the status as the calculated value
							else:
								return [True, f"Total {category} for {date}: {record[0]}"]
				except Exception as e:
					return [False, e]
		except Exception as e:
					return [False, e]
	
 	# The status is calculated by summing the total allowance and income for the specified date, and then subtracting the total expenses and savings for that date. If there are no record for that date, the status is considered to be 0.
	
	def statusExecutor(self, date= datetime.now().strftime("%Y-%m-%d")):
		print("calculating...")
		# The COALESCE function is used to return 0 instead of NULL when there are no record for that date, ensuring that the status calculation is accurate even when there are no records.
		sql = f"""
			SELECT ((SELECT SUM(amount) FROM allowance WHERE SUBSTR (record_date, 1, LENGTH(?)) = (?))+
			(SELECT COALESCE(SUM(amount), 0)  FROM income WHERE SUBSTR (created_at, 1, LENGTH(?)) = (?)))-
			((SELECT COALESCE(SUM(amount), 0)  FROM expenses WHERE SUBSTR (created_at, 1, LENGTH(?)) = (?))+
			(SELECT COALESCE(SUM(amount), 0)  FROM savings WHERE SUBSTR (created_at, 1, LENGTH(?)) = (?))) As status
			"""
		try:
			# The query returns None if there are no record for that date, so we can consider the status as 0 in that case
			records = self.db.query(sql, (date, date, date, date, date, date, date, date, ))
			for record in records:
				# If the record is None, it means there are no record for that date, so we can consider the status as 0
				if len(records) < 1 or str(record[0]) == "None":
					return [False, f"No record found for {date}"]
				elif date == "":
					return [True, f"Status: {record[0]}"]
				# If the record is not None, it means there are record for that date, so we can consider the status as the calculated value
				else:
					return [True, f"Status for {date}: {record[0]}"]
		# If there is an error in the query execution, we can print the error message and return False
		except Exception as e:
			return [False, f"Error: {e}"]		

	def searchExecutor(self, commandList):
		category, label = commandList[0], commandList[2]
		print("searching...")
		sql = f"""
			SELECT * FROM {category}
			WHERE label LIKE (?)
			"""
		try:
			records = self.db.query(sql, (f"%{label}%",))
			index = 0
			for record in records:
				if len(records) == 0:
					return [False, f"No {category} found for {label}"]
				# If the record is not None, it means there are record for that date, so we can consider the status as the calculated value
				else:
					print  (f"Search '{label}': {record[0]}")
					index += 1	 
				return [True, f"{index} records found in {category}"]
		except Exception as e:
			return [False, f"An error occured! {e}"]
   
	def reportExecutor(self, date = datetime.now().strftime("%Y-%m-%d")):
		allowance_cmd = ["allowance", "total", date]
		expenses_cmd = ["expenses", "total", date]
		income_cmd = ["income", "total", date]
		savings_cmd = ["savings", "total", date]
  
		# Validating each cmd
		# cmd = [allowance_cmd,expenses_cmd,income_cmd,savings_cmd]
		# for c in cmd:
		# 	if (self.validator.is_validated(c, self.statusExecutor)):
		# 		continue
		# 	else:
		# 		return [False, f"An error occured"]
  
		# print (self.totalExecutor(allowance_cmd)[0])
		if (self.totalExecutor(allowance_cmd)[0]):

			return [True, f"""\n---Report---\n{self.totalExecutor(allowance_cmd)[1]}\n{self.totalExecutor(expenses_cmd)[1]}\n{self.totalExecutor(income_cmd)[1]}\n{self.totalExecutor(savings_cmd)[1]}\n\n---Total---\n{self.statusExecutor(date)[1]}"""]
		else:
			return [False, f"No records found for {date}"]
			
  
	def executeCommand(self, commandList):
		print("Executing Command...")
		if commandList[0] in ["status","report"]:
			return self.commandMethod[commandList[0]](commandList[1])[1]
		else:
			return self.commandMethod[commandList[1]](commandList)[1]
			
   
	"""
	def historyExecutor(commandList):
	
	def previousExecutor(commandList):
	
	def nextExecutor(commandList):
	"""