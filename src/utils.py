import os
import platform

class Utils:
    isConfirm=False
    @staticmethod
    def center(string,width):
        padding = int((width-len(string))/2)
        return " "*padding+string+" "*padding
    @staticmethod
    def cls():
        try:
            if platform.system().lower().startswith("win"):
                os.system("cls")
            else:
                print("\033[H\033[2J", end="")
        except Exception:
            for _ in range(50):
                print()
    @staticmethod
    def exit():
        Utils.cls()
        print("Closing Program...")
    @staticmethod
    def confirm(object):
        Utils.cls()
        confirm = str(input("Confirm \""+object+"\" (y/n)? "))
        if confirm.lower() == "y":
            Utils.cls()
            print("Confirmed...")
            Utils.isConfirm = True
        elif confirm.lower() == "n":
            Utils.cls()
            print("...")
        else:
            cls
            print("Invaild Input...")
            Utils.confirm(object)
        pass
    @staticmethod
    def encrypt(pin: str) -> str:
        if len(pin) != 4:
            raise ValueError("PIN must be 4 digits")

        d1 = int(pin[0])
        d2 = int(pin[1])
        d3 = int(pin[2])
        d4 = int(pin[3])

        d1, d3 = d3, d1
        d2, d4 = d4, d2

        d1 = (d1 + 7) % 10
        d2 = (d2 + 7) % 10
        d3 = (d3 + 7) % 10
        d4 = (d4 + 7) % 10

        encryptedPin = (d1 * 1000) + (d2 * 100) + (d3 * 10) + d4

        return f"{encryptedPin:04d}"
    @staticmethod
    def decrypt(e_pin: str) -> str:
        if len(e_pin) != 4:
            raise ValueError("Encrypted PIN must be 4 digits")

        d1 = int(e_pin[0])
        d2 = int(e_pin[1])
        d3 = int(e_pin[2])
        d4 = int(e_pin[3])

        d1, d3 = d3, d1
        d2, d4 = d4, d2

        d1 = (d1 + 3) % 10
        d2 = (d2 + 3) % 10
        d3 = (d3 + 3) % 10
        d4 = (d4 + 3) % 10

        decrypted_pin = (d1 * 1000) + (d2 * 100) + (d3 * 10) + d4

        return f"{decrypted_pin:04d}"
