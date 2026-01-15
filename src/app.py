from user import User
from utils import Utils as tools 

class Main:
    def startupPage():
        tools.cls()
        tools.center("Budget CLI",60)
        option = int(input("1.Login\n2.Register\n3.Exit\nOption: "))
        match option:
            case 1:
                User.login(Main.startupPage, Main.homePage)
            case 2:
                User.register(Main.startupPage, Main.homePage)
            case 3:
                tools.exit()
            case _:
                print("No match\nPress ENTER to continue...")
                input()
                startupPage()
        pass
    def homePage():
        tools.cls()
        print("--- Home ---")
        command = ""
        while True:
            command = str(input("~~~ ").strip().lower())
            if command == "quit":
                tools.exit()
                break
        pass
Main.homePage()