import budget.user as user
import budget.help as help
import budget.utils as utils
import budget.commands as commands
import budget.config as config
from datetime import datetime

class Main:
	def __init__(self):
		self.user = user.User()
		self.help = help.Help()
		self.tools = utils.Utils()
		self.cmds = commands.Commands()
		self.config = config.Config()
		self.command = ""
	def startupPage(self):
		self.tools.cls()
		self.cmds = None  # Reset commands when returning to startup page
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
			print("Invalid option. Please enter a number.")
			input("Press ENTER to continue...")
			self.startupPage()
			return
		
		match option:
			case 1:
				self.user.login(self.startupPage, self.homePage)
			case 2:
				self.user.register(self.startupPage, self.homePage)
			case 3:
				self.tools.end()
			case _:
				print("Invalid option")
				input("Press ENTER to continue...")
				self.startupPage()
	def homePage(self):
		if not self.user.get_current_user():
			print("No user logged in. Redirecting to login...")
			input("Press ENTER to continue...")
			self.startupPage()
			return
		
		# Get user info for display
		user_info = self.user.get_user_info()
		if user_info:
			firstname, lastname = user_info
			welcome_msg = f"{firstname} {lastname}"
		else:
			welcome_msg = self.user.get_current_user()
		
		self.tools.cls()
		print(f"--- Home (Welcome {welcome_msg}) ---")
		
		# Initialize commands with user's database
		self.cmds = commands.Commands(self.user.get_user_db())
		
		while True:
			command = str(input("\n~~~ ").strip().lower())
			self.command = command
			
			if self.command == "quit":
				self.user.logout()
				self.tools.end()
				break
			elif self.command == "logout":
				self.user.logout()
				print("Logged out. Returning to startup...")
				input("Press ENTER to continue...")
				self.startupPage()
				break
			elif self.command == "help":
				self.help.helpMessage()
			elif self.command == "help detailed":
				self.help.detailedHelp()
			elif self.command.split(" ")[0] == "status":
				if len(self.command.split(" ")) > 1:
					self.cmds.statusExecutor(date=self.command.split(" ")[1])
				else:
					self.cmds.statusExecutor()
			elif self.command.split(" ")[0] == "report":
				if len(self.command.split(" ")) > 1:
					self.cmds.reportExecutor(date=self.command.split(" ")[1])
				else:
					self.cmds.reportExecutor()
			else:
				if self.cmds:
					self.cmds.executeCommand(command)
				else:
					print("Command system not initialized. Please logout and login again.")

# Start the application
def main():
	app = Main()
	app.startupPage()