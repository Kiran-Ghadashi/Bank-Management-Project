import json
import random
import string
import hashlib
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        try:
            if Path(cls.database).exists():
                with open(cls.database) as fs:
                    cls.data = json.loads(fs.read())
            else:
                cls.data = []
        except Exception as err:
            print(f"An error occurred while loading data: {err}")
            cls.data = []

    @classmethod
    def __update(cls):
        try:
            with open(cls.database, 'w') as fs:
                fs.write(json.dumps(cls.data, indent=2))
        except Exception as err:
            print(f"An error occurred while saving data: {err}")

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)

    @staticmethod
    def __hash_pin(pin):
        return hashlib.sha256(str(pin).encode()).hexdigest()

    def __find_user(self, accnumber, pin):
        hashed = Bank.__hash_pin(pin)
        userdata = [i for i in Bank.data if i["AccountNo"] == accnumber and i["Pin"] == hashed]
        return userdata

    def create_account(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        email = input("Enter your email: ")
        pin = input("Enter a 4-digit PIN: ")

        if age < 18:
            print("Sorry, you must be 18 or older to create an account.")
            return
        if not pin.isdigit() or len(pin) != 4:
            print("Sorry, PIN must be exactly 4 digits.")
            return

        info = {
            "Name": name,
            "Age": age,
            "Email": email,
            "Pin": Bank.__hash_pin(pin),
            "AccountNo": Bank.__accountgenerate(),
            "Balance": 0
        }

        Bank.data.append(info)
        Bank.__update()

        print("\nAccount created successfully!")
        print(f"  Name       : {info['Name']}")
        print(f"  Age        : {info['Age']}")
        print(f"  Email      : {info['Email']}")
        print(f"  Account No : {info['AccountNo']}")
        print("Please note down your account number.")

    def deposit_money(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        userdata = self.__find_user(accnumber, pin)

        if not userdata:
            print("Sorry, no account found with the given account number and PIN.")
            return

        try:
            amount = int(input("How much do you want to deposit: "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        if amount <= 0:
            print("Deposit amount must be greater than 0.")
        elif amount > 10000:
            print("Sorry, maximum deposit per transaction is ₹10,000.")
        else:
            userdata[0]["Balance"] += amount
            Bank.__update()
            print(f"₹{amount} deposited successfully. New balance: ₹{userdata[0]['Balance']}")

    def withdraw_money(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        userdata = self.__find_user(accnumber, pin)

        if not userdata:
            print("Sorry, no account found with the given account number and PIN.")
            return

        try:
            amount = int(input("How much do you want to withdraw: "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
        elif userdata[0]["Balance"] < amount:
            print(f"Insufficient balance. Your current balance is ₹{userdata[0]['Balance']}.")
        else:
            userdata[0]["Balance"] -= amount
            Bank.__update()
            print(f"₹{amount} withdrawn successfully. New balance: ₹{userdata[0]['Balance']}")

    def show_details(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        userdata = self.__find_user(accnumber, pin)

        if not userdata:
            print("Sorry, no account found with the given account number and PIN.")
            return

        print("\nYour account details:")
        print(f"  Name       : {userdata[0]['Name']}")
        print(f"  Age        : {userdata[0]['Age']}")
        print(f"  Email      : {userdata[0]['Email']}")
        print(f"  Account No : {userdata[0]['AccountNo']}")
        print(f"  Balance    : ₹{userdata[0]['Balance']}")

    def update_details(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        userdata = self.__find_user(accnumber, pin)

        if not userdata:
            print("Sorry, no account found with the given account number and PIN.")
            return

        print("\nLeave a field blank to keep it unchanged.")
        print("Note: Age, Account Number, and Balance cannot be changed.\n")

        new_name = input(f"New name (current: {userdata[0]['Name']}): ").strip()
        new_email = input(f"New email (current: {userdata[0]['Email']}): ").strip()
        new_pin = input("New 4-digit PIN (or press Enter to skip): ").strip()

        if new_name:
            userdata[0]["Name"] = new_name
        if new_email:
            userdata[0]["Email"] = new_email
        if new_pin:
            if not new_pin.isdigit() or len(new_pin) != 4:
                print("Invalid PIN. Must be exactly 4 digits. PIN not updated.")
            else:
                userdata[0]["Pin"] = Bank.__hash_pin(new_pin)

        Bank.__update()
        print("Details updated successfully.")

    def delete_account(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        userdata = self.__find_user(accnumber, pin)

        if not userdata:
            print("Sorry, no account found with the given account number and PIN.")
            return

        check = input("Are you sure you want to delete your account? (y/n): ").strip().lower()
        if check != 'y':
            print("Account deletion cancelled.")
        else:
            Bank.data.remove(userdata[0])
            Bank.__update()
            print("Account deleted successfully.")


# ── Main Program ──

Bank.load_data()
user = Bank()

while True:
    print("\n========== BANK MENU ==========")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Show Account Details")
    print("5. Update Details")
    print("6. Delete Account")
    print("7. Exit")
    print("================================")

    choice = input("Enter your choice (1-7): ").strip()

    if choice == '1':
        user.create_account()
    elif choice == '2':
        user.deposit_money()
    elif choice == '3':
        user.withdraw_money()
    elif choice == '4':
        user.show_details()
    elif choice == '5':
        user.update_details()
    elif choice == '6':
        user.delete_account()
    elif choice == '7':
        print("Thank you for using our banking system. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")