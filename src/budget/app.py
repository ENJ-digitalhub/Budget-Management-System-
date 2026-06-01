import budget.user as user
import budget.help as help
import budget.utils as utils
import budget.commands as cmd
import budget.validator as check
import budget.config as config
import shlex
from datetime import datetime

class Main:
	def __init__(self):
		self.user = user.User()
		self.help = help.Help()
		self.tools = utils.Utils()
		self.cmd = cmd.Commands()
		self.check = check.Validator()
		self.config = config.Config()
		self.command = ""
		self.logout = False
		self.quit = False

	def startupPage(self):
		input("Press ENTER to continue...")
		self.tools.cls()
		self.cmd = None  # Reset cmd when returning to startup page
		#print("\n")
		print("=" * self.tools.terminal_width)
		#print("\n")
		name = self.config.get("application.name")
		version = self.config.get("version")
		title = f"{name} | v{version}"
		print(self.tools.center(title, self.tools.terminal_width))
		date_time ="Date: " + datetime.now().strftime("%Y-%m-%d")+" \t Time: " + datetime.now().strftime("%H:%M:%S") 
		#print("\n")
		print(self.tools.center(date_time,self.tools.terminal_width))
		#print("\n")
		print("=" * self.tools.terminal_width)
		
		print("1. Login")
		print("2. Register")
		print("3. Exit")
		
		try:
			option = int(input("Option: "))
		except ValueError:
			return [False, "Invalid option. Please enter a number."]
		
		match option:
			case 1:
				login = self.user.login()
				if login[0]:
					print(login[1])
					self.homePage()
					return True
				else:
					print(login[1])
					return True
			case 2:
				register = self.user.register()
				if register[0]:
					print(register[1])
					login = self.user.login()
					if login[0]:
						print(login[1])
						self.homePage()
						return True
					else:
						print(login[1])
						return True
				else:
					print(register[1])
					return True
			case 3:
				self.quit = self.tools.end()
				print (self.tools.end()[1])
			case _:
				return [False, "Invalid option"]
    
	def homePage(self):
		self.logout = False
		input("Press ENTER to continue...")
		if not self.user.get_current_user():
			login = self.user.login()
			if login[0]:
				print(login[1])
				self.homePage()
				return True
			else:
				print(login[1])
				return True


		# Get user info for display
		user_info = self.user.get_user_info()
		if user_info:
			firstname, lastname = user_info
			welcome_msg = f"{firstname} {lastname}"
		else:
			welcome_msg = self.user.get_current_user()
		
		self.tools.cls()
		print(f"--- Home (Welcome {welcome_msg}) ---")
		
		# Initialize cmd with user's database
		self.cmd = cmd.Commands(self.user.get_user_db())
		
		while not self.logout:
			command = str(input("\n~~~ ").strip().lower())
			self.command = command
			
			if self.command == "quit":
				self.logout = self.user.logout()[0]
				self.quit = self.tools.end()[0]
				print (self.user.logout()[1])
				print (self.tools.end()[1])

			elif self.command == "logout":
				self.logout = self.user.logout()[0]
				print (self.user.logout()[1])
				self.startupPage()

			elif self.command == "help":
				self.help.helpMessage()

			elif self.command == "help detailed":
				self.help.detailedHelp()

			else:
				commandList = self.cmd.commandParser(self.command)
				if(self.check.is_validated(commandList, self.cmd.statusExecutor)[0]):
     				# Pad the command list to ensure it has at least 5 elements
					commandList = commandList + [""] * (5 - len(commandList))  
					result = self.cmd.executeCommand(commandList)
					print(result)

				else:
					error = self.check.is_validated(commandList, self.cmd.statusExecutor)[1]
					print(error)

# Start the application
def main():
	app = Main()
	while not app.quit:
		app.startupPage()