import user
import help
import utils
import commands

class Main:
	def __init__(self):
		self.user = user.User()
		self.help = help.Help()
		self.tools = utils.Utils()
		self.cmds = None
		self.command = ""
	def startupPage(self):
		self.tools.cls()
		print("=" * self.tools.terminal_width)
		print(self.tools.center("Budget CLI"))
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
			else:
				if self.cmds:
					self.cmds.executeCommand(command)
				else:
					print("Command system not initialized. Please logout and login again.")
# Start the application
if __name__ == "__main__":
	m = Main()
	m.startupPage()