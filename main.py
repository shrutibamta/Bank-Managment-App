import json
import random
import string 
from pathlib import Path

# Decorator
def syncDatabase(func) :
    def wrapper(cls, *args, **kwargs) :
        cls._Bank__loadDatabase()
        result = func(cls, *args, **kwargs)
        cls._Bank__updateDatabase()
        return result
    return wrapper

class Bank:
    database = "data.json"
    data = []           # dummy data storage

    # try : 
    #     if Path(database).exists() :
    #         with open(database) as f :
    #             data = json.load(f.read())
    #     else :
    #         print("Database not found...")

    # except Exception as err :
    #     print(f"An exception occured as {err}")

    @classmethod
    def __loadDatabase(cls):
        """Load existing data from JSON file."""
        if Path(cls.database).exists():
            with open(cls.database, 'r') as f:
                try:
                    cls.data = json.load(f)
                except json.JSONDecodeError:
                    cls.data = []  # empty or invalid file
        else:
            cls.data = []

 
    @classmethod
    def __updateDatabase(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __generateAccountNumber(cls):
        alpha = random.choices(string.ascii_letters, k = 3)
        num = random.choices(string.digits, k = 3)
        spchar = random.choices("!@#$%^&*", k = 1)
        id = alpha + num + spchar
        random.shuffle(id)          # this returns an list or object
        return "".join(id)


    def createAccount(self):
        Bank.__loadDatabase()
        info = {
            "name" : input("Enter your name : "),
            "age" : int(input("Enter your age : ")),
            "email" : input("Enter your email : "),
            "pin" : int(input("Set your 4 digit pin : ")),
            "account_number" : Bank.__generateAccountNumber(),
            "balance" : 0
        }

        if info['age'] < 18 or len(str(info['pin'])) != 4 :
            print("Sorry, account cannot be created...")

        else :
            print("Account created successfully...")
            for i in info :
                print(f"{i} : {info[i]}")

            print("Please save your account number for future reference...")
            Bank.data.append(info)
            Bank.__updateDatabase()

    @classmethod
    @syncDatabase
    def depositeMoney(cls) :
        accNo = input("Enter your account number : ")
        pin = int(input("Enter your 4 digit pin : "))          

        userdata = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]

        if userdata == False :
            print("Invalid account number or pin...")

        else :
            amount = float(input("Enter amount to be deposited : ")) 
            if amount > 10000 or amount <= 0 :
                print("Sorry, the amount should be less than 10000 and greater than 0...")

            else :
                userdata[0]['balance'] += amount
                print(f"Amount of {amount} deposited successfully...")
                print(f"Updated balance is {userdata[0]['balance']}")

    @classmethod
    @syncDatabase
    def withdrawMoney(cls) :
        accNo = input("Enter your account number : ")
        pin = int(input("Enter your 4 digit pin : "))

        userdata = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]

        if userdata == False :
            print("Invalid account number or pin...")

        else :
            amount = float(input("Enter amount to be withdrawn : "))

            if amount > userdata[0]['balance'] or amount <= 0 :
                print("Insufficient balance or invalid amount...")

            else :
                userdata[0]['balance'] -= amount
                print(f"Amount of {amount} withdrawn successfully...")
                print(f"Updated balance is {userdata[0]['balance']}")

    @classmethod
    @syncDatabase
    def showDetails(cls) :
        accNo = input("Enter you account number : ")
        pin = int(input("Enter your 4 digit pin : "))

        userdata = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]

        if userdata == False :
            print("Invalid account number or pin...")

        else :
            print("Account details are as follows : ")

            for i in userdata[0] :
                print(f"{i} : {userdata[0][i]}")


    @classmethod
    @syncDatabase
    def updateDetails(cls) :
        accNo = input("Enter your account number : ")
        pin = int(input("Enter your 4 digit pin : "))

        userdata = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]

        if userdata == False :
            print("Invalid account number or pin...")

        else : 
            print("You cannot change your account number, age and balance...")

            print('Fill the details for change or leave it empty for no change...')

            newData = {
                'name': input("Enter your new name or press enter to skip :"),
                'email': input("Enter your new email or press enter to skip : "),
                'pin' : input("Enter your new 4 digit pin or press enter to skip : ")
            }

            if newData['name'] == '' :
                newData['name'] = userdata[0]['name']

            if newData['email'] == '' :
                newData['email'] = userdata[0]['email']

            if newData['pin'] == '' :
                newData['pin'] = userdata[0]['pin']

            newData['age'] = userdata[0]['age']
            newData['account_number'] = userdata[0]['account_number']
            newData['balance'] = userdata[0]['balance']

            if type(newData['pin']) == str :
                newData['pin'] = int(newData['pin'])
            
            for i in newData :
                if newData[i] == userdata[0][i] :
                    continue
                else :
                    userdata[0][i] = newData[i]

            print("Details updated successfully...")

    @classmethod
    @syncDatabase
    def deleteAccount(cls) :
        accNo = input("Enter your account number : ")
        pin = int(input("Enter your 4 digit pin : "))

        userdata = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]

        if userdata == False :
            print("Invalid account number or pin...")
        
        else :
            index = cls.data.index(userdata[0])
            cls.data.pop(index)
            print("Account deleted successfully...")
            

user = Bank()

print("Prss 1 for CREATING an account : ")
print("Press 2 for DEPOSITING money : ")
print("Press 3 for WITHDRAWING money : ")
print("Press 4 for DETAILS of account : ")
print("Press 5 for UPDATING the deatils : ")
print("Press 6 for DELETING the account : ")

choice = int(input("Enter your choice : "))

if choice == 1 :
    user.createAccount()

if choice == 2 :
    user.depositeMoney()

if choice == 3 :
    user.withdrawMoney()

if choice == 4 :
    user.showDetails()

if choice == 5 :
    user.updateDetails()

if choice == 6 :
    user.deleteAccount()