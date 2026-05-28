from datetime import datetime
import re

class Validator:
    
    def __init__(self):
        self.mainCommands=("allowance","expenses","income","savings")
        self.typeCommands=("add","remove","delete","modify","show","total","search")
        self.actionCommands = ("status", "report")
        pass       
    
    """This method checks if the first two elements of the command list are valid commands (category and action). It returns True if the command is valid, and False with an error message if it is not."""
    def is_command(self, commandList):
        if commandList[0] in self.mainCommands:
            if (len(commandList) > 1 and commandList[1] in self.typeCommands):
                return [True, "Command Verified"]
            elif (len(commandList) < 2):
                return [False, "Incomplete command! Please provide an action for the category. Type 'help' to view valid commands."]
            elif (len(commandList) > 1 and commandList[1] not in self.typeCommands):
                return [False, "Invalid action! Please provide a valid action for the category. Type 'help' to view valid commands."]
        elif commandList[0] in self.actionCommands:
            return [True, "Command Verified"]
        return [False, "Unknown command! Type 'help' to view valid commands"]
    
    """This class will contain methods to validate user input and commands before they are executed."""
    def no_negative_values(self, commandList):
        # Check if any command in the list is a negative number
        for num in commandList:
            try:
                if float(num) < 0:
                    return [False, "Negative values are not allowed! Please enter a positive number."]
            except ValueError:
                continue
        return [True, "All values are valid."]
    
    """This method checks if an allowance record exists for the given date before allowing the user to add or remove any other category. If the command is a status or report command, it will return True since those commands do not require an allowance record."""
    def allowance_exists(self, commandList, statusExecutor):
        if commandList[0] in ["status","report"]:
            return [True, "Allowance record exists."]
        # Implement logic to check if an allowance record exists for the given date
        if commandList[0] != "allowance" and commandList[1] in ["add","remove"]:
            # Check if an allowance record exists for the specified date
            if statusExecutor(date=datetime.now().strftime("%Y-%m-%d"))[0]:
                return [True, "Allowance record exists."]
            # Implement logic to check if the allowance record does not exists
            else:
                return [False, "No allowance record found for today's date! Please record an allowance before adding any other category."]
        return [True, "Allowance check passed."]
    
    """This method checks if the command list has the required number of elements for a valid command."""
    def is_complete(self, commandList):
        # user only typed 1 thing (usually just the action)
        if len(commandList) < 2:
            # Only "report" and "status" are allowed to stand alone
            if commandList[0] in ["report", "status"]:
                return [True, "Command is complete."]
            # Any other command needs more details (category, amount, etc.)
            else:
                return [False, "Incomplete command! Only report and status commands can be executed with just an action. Please provide at least a category, action, and amount for other commands."]
        # user typed 2 things
        elif len(commandList) < 3:
            # Again, "report" and "status" are still valid even if extra argument is present
            if commandList[0] in ["report", "status"]:
                return [True, "Command is complete."]
            # "total" and "show" only need category + action
            elif commandList[1] in ["total", "show"]:
                return [True, "Command is complete."]
            # Other commands still need more info
            else:
                return [False, "Incomplete command! Total and Show actions require at least a category and action. Please provide at least a category, action, and amount for other commands."]
        # user typed 3 things
        elif len(commandList) < 4:
            # These commands are considered complete at this stage (even though some may optionally take more arguments like labels)
            if commandList[1] in ["total", "search", "add", "remove", "delete"]:
                return [True, "Command is complete."]
            # Anything else still lacks required arguments
            else:
                return [False, "Incomplete command! Search, Add, Remove, and Delete require a category, action, amount (except for search), and label (optional except for search). Please provide all required elements for the command."]
        # user typed 4 things
        elif len(commandList) < 5:
            # These commands are valid with up to 4 arguments
            if commandList[1] in ["modify", "add", "remove", "delete"]:
                return [True, "Command is complete."]
            # Other commands shouldn't reach this length without being invalid
            else:
                return [False, "Invalid structure! Modify action requires a category, action, ID, amount, and label(optional). Please provide all required elements for the command."]
        # user typed 5 things
        elif len(commandList) < 6:
            # Only "modify" is allowed to have this many arguments
            if commandList[1] in ["modify"]:
                return [True, "Command is complete."]
            # Anything else has too many arguments for its type
            else:
                return [False, "Too many command! Only Modify action requires a maximum of 5 elements. Please provide all required elements for the command."]
        # command has 6 or more elements → definitely too much
        else:
            return [False, "Command has too many arguments"]
        
    """This method checks if the command list is empty, which would indicate that the user did not enter any command."""
    def is_empty(self, commandList): 
        # Check if the command list is empty
        if len(commandList) == 0:
            return [False, "Empty command! Please enter a valid command."]
        return [True, "Command is not empty."]
    
    """This method checks if the label provided in the command list is valid (not empty and does not contain special characters)."""
    def valid_label(self, commandList):
        if commandList[0] in ["status","report"]:
            return [True, "Label is valid."]
        # Check if the action in the command list is valid for label validation
        if commandList[1] not in ["search", "add", "remove", "modify"] or commandList[0] not in ["expenses", "income"]:
            return [True, "Label is valid."]
        try:
            if commandList[1] == "search":
                label = commandList[2].strip()
                label = commandList[2].strip()
            elif commandList[1] in ["add", "remove"]:
                label = commandList[3].strip()
            elif commandList[1] in ["modify"]:
                label = commandList[4].strip()
        # If the label is not provided in the command list, it will raise an IndexError, which we can catch to return True since the label is optional for some actions
        except IndexError:
            return [True, "Label is valid."]
        # Check if the label is not alphanumeric and does not contain only underscores
        label = label.replace(" ", "_")
        for char in label:
            if not (char.isalnum() or char == "_"):
                return [False, "Invalid label! Labels must be alphanumeric. Please enter a valid label without special characters."]
        return [True, "Label is valid."]
    
    """This method checks if the date provided in the command list is valid and in the correct format (YYYY-MM-DD or YYYY-MM or YYYY)."""
    def valid_date(self, commandList):
        date_str = ""
        try:
            # Check if the action in the command list is valid for date validation
            if commandList[0] not in ["report", "status"] and commandList[1] not in ["total"]:
                return [True, "Date is valid."]
            else:
                if commandList[1] in ["total"]:
                    date_str = commandList[2].strip()
                elif commandList[0] in ["report", "status"]:
                    date_str = commandList[1].strip()
        except IndexError:        
                # If the date is not provided in the command list, it will raise an IndexError, which we can catch to return True since the date is optional for some actions
                return [True, "Date is valid."]
        # Try to parse the date string in different formats (YYYY-MM-DD, YYYY-MM, YYYY) and return True if any of them is valid. If all formats are invalid, print an error message and return False.
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return [True, "Date is valid."]
        except ValueError:
            try:
                datetime.strptime(date_str, "%Y-%m")
                return [True, "Date is valid."]
            except ValueError:
                try:
                    datetime.strptime(date_str, "%Y")
                    return [True, "Date is valid."]
                except ValueError:
                    return [False, "Invalid date format! Please enter a date in the format YYYY-MM-DD, YYYY-MM, or YYYY."]

    """This method checks if the amount provided in the command list is a valid number and not negative."""
    def valid_amount(self, commandList):
        if commandList[0] in ["status","report"]:
            return [True, "Amount validated"]
        # Check if the action in the command list is valid for amount validation
        if commandList[1] not in ["add", "remove", "modify"]:
            return [True, "Amount validated"]
        try:
            # Assigns amount based on the action type in the command list
            if commandList[1] in ["add", "remove"]:
                amount = commandList[2]
            elif commandList[1] in ["modify"]:
                amount = commandList[3]
        except IndexError:
            return [False, "Amount not provided"]
        
        # Try to convert the amount to a float and check if it is negative. If it is negative, print an error message and return False. If it is not a valid number, catch the ValueError and print an error message. If it is valid and not negative, return True.
        try:
            if not re.fullmatch(r"^[0-9]+(\.[0-9]+)?$", amount):
                raise ValueError
            amount = float(amount)
        except ValueError:
            return [False, "Invalid amount format! Please enter a numeric amount."]
        return [True, "Amount is valid."]
    
    """This method checks if the id provided in the command list is a valid number and not negative or float."""
    def valid_id(self, commandList):
        if commandList[0] in ["status","report"]:
            return [True, "ID is valid."]
        # Check if the action in the command list is valid for id validation
        if commandList[1] not in ["delete", "modify"]:
            return [True, "ID is valid."]
        # Assigns id based on the action type in the command list
        if commandList[1] in ["delete", "modify"]:
            id = commandList[2]
        
        # Try to convert the id to an integer and check if it is negative. If it is negative, print an error message and return False. If it is not a valid number, catch the ValueError and print an error message. If it is valid and not negative, return True.
        try:
            if not re.fullmatch(r"^[1-9]?$", id):
                raise ValueError
            id = int(id)
        except ValueError:
            return [False, "Invalid id format! Please enter a numeric id."]
        return [True, "ID is valid."]
    
    """This method checks all available validation method"""
    def is_validated(self, commandList, statusExecutor):
        print("Validating Command...")

        if not self.is_empty(commandList)[0]:
            return [False, self.is_empty(commandList)[1]]

        if not self.is_command(commandList)[0]:
            return [False, self.is_command(commandList)[1]]

        if not self.is_complete(commandList)[0]:
            return [False, self.is_complete(commandList)[1]]

        if not self.no_negative_values(commandList)[0]:
            return [False, self.no_negative_values(commandList)[1]]

        if not self.valid_id(commandList)[0]:
            return [False, self.valid_id(commandList)[1]]

        if not self.valid_amount(commandList)[0]:
            return [False, self.valid_amount(commandList)[1]]

        if not self.valid_label(commandList)[0]:
            return [False, self.valid_label(commandList)[1]]

        if not self.valid_date(commandList)[0]:
            return [False, self.valid_date(commandList)[1]]

        if not self.allowance_exists(commandList, statusExecutor)[0]:
            return [False, self.allowance_exists(commandList, statusExecutor)[1]]

        return [True, "Validation passed"]