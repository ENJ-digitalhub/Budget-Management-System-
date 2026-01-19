import sqlite3
from database import Database  

class Commands:
    @staticmethod
    def commandParser(command):
        return command.split(" ")
        pass
    @staticmethod
    def isValid(commandList):
        while len(commandList) != 5:
            commandList.append("")
        mainCommands=("allowance","expenses","income","savings")
        typeCommands={"add":Commands.addExecutor,\
                                "remove":Commands.removeExecutor,\
                                "modify":Commands.modifyExecutor, \
                                "show":Commands.showExecutor,\
                                "total":Commands.totalExecutor}
        if commandList[0] in mainCommands and \
        commandList[1] in typeCommands.keys():
            print("Valid Command")
            typeCommands[commandList[1]](commandList)
        else:
            print("Invalid Command")
        pass
    @staticmethod
    def addExecutor(commandList):
        print("adding...")
        sql = f"""
            INSERT INTO {commandList[0]} (amount)
            VALUES (?)
            """
        params = (commandList[2],)
        sql2 = f"""
            INSERT INTO {commandList[0]} (amount, label)
            VALUES (?, ?)
            """
        params2 = (commandList[2], commandList[3])
        try:
            Database.run(sql2, params2)
        except sqlite3.OperationalError:
            try:
                Database.run(sql, params)
            except Exception as e:
                print(e)
    @staticmethod
    def removeExecutor(commandList):
        print("removing...")
        sql = f"""
            DELETE FROM {commandList[0]} 
            WHERE id = (?)
            """
        params = (commandList[2],)
        try:
            int(commandList[2])
            Database.run(sql,params)
        except Exception as e:
            print(e)
    @staticmethod
    def modifyExecutor(commandList):
        print("modifying...")
        sql = f"""
            UPDATE {commandList[0]}
            SET amount = ?, label = ?
            WHERE id = ?
            """
        params = (commandList[3],commandList[4],commandList[2],)
        try:
            int(commandList[2])
            Database.run(sql, params)
        except Exception as e:
            print(e)
    @staticmethod
    def showExecutor(commandList):
        print("showing...")
        sql = f"""
            SELECT * FROM {commandList[0]}
            """
        try:
            records = Database.query(sql)
            for record in records:
                print(record)
            if len(records) == 0:
                print("(No records found...)")
        except Exception as e:
            print(e)
    """@staticmethod
    def statusExecutor(commandList):
    @staticmethod
    def historyExecutor(commandList):
    @staticmethod
    def previousExecutor(commandList):
    @staticmethod
    def nextExecutor(commandList):
    @staticmethod"""
    def totalExecutor(commandList):
        print("totaling...")
        sql = f"""
            SELECT SUM(amount) FROM {commandList[0]}
            """
        try:
            records = Database.query(sql)
            for record in records:
                print(record)
        except Exception as e:
            print(e)
    """@staticmethod
    def searchExecutor(commandList):"""
    @staticmethod
    def executeCommand(command):
        Commands.isValid(Commands.commandParser(command))