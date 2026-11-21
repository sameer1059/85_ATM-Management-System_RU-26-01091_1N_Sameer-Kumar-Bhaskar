# ATM Management System

def load_data():
    pin, balance, transactions = "1234", 10000, []
    try:
        with open("atm.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("PIN:"):
                    pin = line.split(":", 1)[1].strip()
                elif line.startswith("Balance:"):
                    balance = int(float(line.split(":", 1)[1].strip()))
                elif "|" in line:
                    transactions.append(line)
    except Exception:
        pass
    return pin, balance, transactions


def save_data(balance, transactions):
    try:
        with open("atm.txt", "w") as f:
            f.write("PIN: 1234\n")
            f.write(f"Balance: {balance}\n")
            f.write("--- TRANSACTIONS ---\n")
            for t in transactions:
                f.write(f"{t}\n")
    except Exception:
        pass


def check_balance(balance):
    print(f"Current Balance: {balance}")


def deposit_money(balance, transactions):
    try:
        amount = int(float(input("Enter amount to deposit: ")))
        if amount > 0:
            balance += amount
            print(f"Deposit successful. New Balance: {balance}")
            transactions.append(f"Deposit {amount} | Balance: {balance}")
            save_data(balance, transactions)
        else:
            print("Amount must be greater than zero.")
    except ValueError:
        print("Invalid amount. Please enter numbers only.")
    return balance


def withdraw_money(balance, transactions):
    try:
        amount = int(float(input("Enter amount to withdraw: ")))
        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > balance:
            print("Insufficient balance.")
        else:
            balance -= amount
            print(f"Withdrawal successful. New Balance: {balance}")
            transactions.append(f"Withdraw {amount} | Balance: {balance}")
            save_data(balance, transactions)
    except ValueError:
        print("Invalid amount. Please enter numbers only.")
    return balance


def mini_statement(transactions):
    for i, t in enumerate(transactions, 1):
        print(f"{i}. {t}")


def atm_simulator():
    pin, balance, transactions = load_data()

    attempts = 3
    while attempts > 0:
        entered_pin = input("Enter your PIN: ").strip()
        if entered_pin == pin:
            print("Login successful")
            break
        attempts -= 1
        if attempts > 0:
            print(f"Invalid PIN. Attempts left: {attempts}")
        else:
            print("Account locked. Exiting...")
            return

    while True:
        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_balance(balance)
        elif choice == "2":
            balance = deposit_money(balance, transactions)
        elif choice == "3":
            balance = withdraw_money(balance, transactions)
        elif choice == "4":
            mini_statement(transactions)
        elif choice == "5":
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice.")


atm_simulator()
