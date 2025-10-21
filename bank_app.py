import streamlit as st
import json
import random
import string
from pathlib import Path


# -------------------------
# DECORATOR FOR DB SYNC
# -------------------------
def syncDatabase(func):
    def wrapper(cls, *args, **kwargs):
        cls._Bank__loadDatabase()
        result = func(cls, *args, **kwargs)
        cls._Bank__updateDatabase()
        return result
    return wrapper


# -------------------------
# BANK CLASS
# -------------------------
class Bank:
    database = "data.json"
    data = []

    @classmethod
    def __loadDatabase(cls):
        """Load data from JSON file."""
        if Path(cls.database).exists():
            try:
                with open(cls.database, 'r') as f:
                    cls.data = json.load(f)
            except json.JSONDecodeError:
                cls.data = []
        else:
            cls.data = []

    @classmethod
    def __updateDatabase(cls):
        """Save data back to JSON."""
        with open(cls.database, 'w') as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def __generateAccountNumber(cls):
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choice("!@#$%^&*")
        all_chars = alpha + num + [spchar]
        random.shuffle(all_chars)
        return "".join(all_chars)

    # -------------------------
    # ACCOUNT CREATION
    # -------------------------
    @classmethod
    def createAccount(cls, name, age, email, pin):
        cls.__loadDatabase()
        if age < 18 or len(str(pin)) != 4:
            return "❌ Account cannot be created (age < 18 or invalid PIN)."

        account_number = cls.__generateAccountNumber()
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": account_number,
            "balance": 0.0
        }
        cls.data.append(info)
        cls.__updateDatabase()
        return f"✅ Account created successfully!\nYour Account Number: {account_number}"

    # -------------------------
    # DEPOSIT MONEY
    # -------------------------
    @classmethod
    @syncDatabase
    def depositMoney(cls, accNo, pin, amount):
        user = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]
        if not user:
            return "❌ Invalid account number or PIN."
        if amount <= 0 or amount > 10000:
            return "❌ Amount should be between 0 and 10000."
        user[0]['balance'] += amount
        return f"💰 Deposited {amount}. Updated balance: {user[0]['balance']}"

    # -------------------------
    # WITHDRAW MONEY
    # -------------------------
    @classmethod
    @syncDatabase
    def withdrawMoney(cls, accNo, pin, amount):
        user = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]
        if not user:
            return "❌ Invalid account number or PIN."
        if amount <= 0 or amount > user[0]['balance']:
            return "❌ Invalid amount or insufficient balance."
        user[0]['balance'] -= amount
        return f"🏧 Withdrawn {amount}. Remaining balance: {user[0]['balance']}"

    # -------------------------
    # SHOW DETAILS
    # -------------------------
    @classmethod
    def showDetails(cls, accNo, pin):
        cls.__loadDatabase()
        user = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]
        if not user:
            return None
        return user[0]

    # -------------------------
    # UPDATE DETAILS
    # -------------------------
    @classmethod
    @syncDatabase
    def updateDetails(cls, accNo, pin, new_name, new_email, new_pin):
        user = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]
        if not user:
            return "❌ Invalid account number or PIN."
        user = user[0]
        if new_name:
            user['name'] = new_name
        if new_email:
            user['email'] = new_email
        if new_pin:
            user['pin'] = int(new_pin)
        return "✅ Details updated successfully."

    # -------------------------
    # DELETE ACCOUNT
    # -------------------------
    @classmethod
    @syncDatabase
    def deleteAccount(cls, accNo, pin):
        user = [i for i in cls.data if i['account_number'] == accNo and i['pin'] == pin]
        if not user:
            return "❌ Invalid account number or PIN."
        cls.data.remove(user[0])
        return "🗑️ Account deleted successfully."


# -------------------------
# STREAMLIT UI
# -------------------------
st.title("🏦 Bank Management System")

menu = st.sidebar.radio(
    "Select Action",
    ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
)

# CREATE ACCOUNT
if menu == "Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=1, max_value=100)
    email = st.text_input("Enter Email")
    pin = st.text_input("Set 4-digit PIN", type="password")
    if st.button("Create Account"):
        if name and email and pin:
            st.success(Bank.createAccount(name, age, email, int(pin)))
        else:
            st.warning("Please fill all fields.")

# DEPOSIT
elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    accNo = st.text_input("Enter Account Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=0.0)
    if st.button("Deposit"):
        st.info(Bank.depositMoney(accNo, int(pin), amount))

# WITHDRAW
elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    accNo = st.text_input("Enter Account Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=0.0)
    if st.button("Withdraw"):
        st.info(Bank.withdrawMoney(accNo, int(pin), amount))

# SHOW DETAILS
elif menu == "Show Details":
    st.subheader("Show Account Details")
    accNo = st.text_input("Enter Account Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")
    if st.button("Show"):
        details = Bank.showDetails(accNo, int(pin))
        if details:
            st.json(details)
        else:
            st.error("❌ Invalid credentials.")

# UPDATE DETAILS
elif menu == "Update Details":
    st.subheader("Update Account Details")
    accNo = st.text_input("Enter Account Number")
    pin = st.text_input("Enter Current 4-digit PIN", type="password")
    new_name = st.text_input("Enter New Name (optional)")
    new_email = st.text_input("Enter New Email (optional)")
    new_pin = st.text_input("Enter New 4-digit PIN (optional)", type="password")
    if st.button("Update"):
        st.success(Bank.updateDetails(accNo, int(pin), new_name, new_email, new_pin))

# DELETE ACCOUNT
elif menu == "Delete Account":
    st.subheader("Delete Account")
    accNo = st.text_input("Enter Account Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")
    if st.button("Delete"):
        st.warning(Bank.deleteAccount(accNo, int(pin)))
