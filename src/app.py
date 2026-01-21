import user
import help
import utils
import commands

class Main:
    def __init__(self):
        self.user=user.User()
        self.help=help.Help()
        self.tools=utils.Utils()
        self.cmds=commands.Commands()
        self.command = ""
    def startupPage(self):
        self.tools.cls()
        self.tools.center("Budget CLI",60)
        option = int(input("1.Login\n2.Register\n3.end\nOption: "))
        match option:
            case 1:
                self.user.login(self.startupPage,self.homePage)
            case 2:
                self.user.register(self.startupPage,self.homePage)
            case 3:
                self.tools.end()
            case _:
                print("No match\nPress ENTER to continue...")
                input()
                self.startupPage()
        pass
    def homePage(self):
        self.tools.cls()
        print("--- Home ---")
        while True:
            command = str(input("\n~~~ ").strip().lower())
            if command == "quit":
                self.tools.end()
                break
            elif command == "help":
                self.help.helpMessage()
            else:
                self.cmds.executeCommand(command)
m=Main()
m.homePage()