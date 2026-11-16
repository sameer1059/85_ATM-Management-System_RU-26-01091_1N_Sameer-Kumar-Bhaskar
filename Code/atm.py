# ATM Management System
# Language: Python 3
# Concepts used: Conditions, Loops, Functions, Exceptions, File Handling

FILE_NAME = "atm.txt"
DEFAULT_PIN = "1234"
DEFAULT_BALANCE = 10000
MAX_ATTEMPTS = 3


# ---------- File handling functions ----------

def create_default_file():
    """Create atm.txt with default balance (no transactions)."""
    try:
        with open(FILE_NAME, "w") as f:
            f.write(str(DEFAULT_BALANCE) + "\n")
    except IOError:
        print("Error: Could not create the data file.")


def load_data():
    """Read balance (first line) and transactions (remaining lines) from file."""
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.read().splitlines()
        balance = int(lines[0])
        transactions = lines[1:]          # each line like: "Deposit 5000 | Balance: 15000"
        return balance, transactions
    except FileNotFoundError:
        # file not found -> make a new one with default data
        create_default_file()
        return DEFAULT_BALANCE, []
    except (ValueError, IndexError):
        # file is empty or corrupted -> reset to default
        print("Data file was corrupted. Resetting to default data.")
        create_default_file()
        return DEFAULT_BALANCE, []
    except IOError:
        print("Error: Could not read the data file.")
        return DEFAULT_BALANCE, []


def save_data(balance, transactions):
    """Save balance and all transactions to file."""
    try:
        with open(FILE_NAME, "w") as f:
            f.write(str(balance) + "\n")
            for t in transactions:
                f.write(t + "\n")
    except IOError:
        print("Error: Could not save data to file.")


# ---------- PIN verification ----------

def verify_pin():
    """Allow max 3 attempts. Returns True if login is successful."""
    attempts_left = MAX_ATTEMPTS
    while attempts_left > 0:
        pin = input("Enter PIN: ").strip()
        if pin == DEFAULT_PIN:
            print("Login successful")
            return True
        else:
            attempts_left -= 1
            print("Invalid PIN. Attempts left:", attempts_left)
    print("Account locked. Exiting...")
    return False


# ---------- Banking functions ----------

def check_balance(balance):
    print("Current Balance:", balance)


def get_amount():
    """Ask the user for an amount. Returns an int, or None if invalid."""
    try:
        amount = int(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter numbers only.")
        return None
    if amount <= 0:
        print("Amount must be greater than 0.")
        return None
    return amount


def deposit(balance, transactions):
    amount = get_amount()
    if amount is None:
        return balance
    balance += amount
    transactions.append("Deposit " + str(amount) + " | Balance: " + str(balance))
    save_data(balance, transactions)          # save after every operation
    print("Deposit successful. New Balance:", balance)
    return balance


def withdraw(balance, transactions):
    amount = get_amount()
    if amount is None:
        return balance
    if amount > balance:
        print("Insufficient balance. Current Balance:", balance)
        return balance
    balance -= amount
    transactions.append("Withdraw " + str(amount) + " | Balance: " + str(balance))
    save_data(balance, transactions)          # save after every operation
    print("Withdrawal successful. New Balance:", balance)
    return balance


def mini_statement(transactions):
    """Show the last 5 transactions."""
    print("----- Mini Statement -----")
    if len(transactions) == 0:
        print("No transactions yet.")
        return
    last_five = transactions[-5:]
    count = 1
    for t in last_five:
        print(str(count) + ".", t)
        count += 1


# ---------- Menu ----------

def show_menu():
    print("\n===== ATM MENU =====")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Mini Statement")
    print("5. Exit")


def main():
    print("===== WELCOME TO ATM =====")
    balance, transactions = load_data()

    if not verify_pin():
        return

    while True:
        show_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            check_balance(balance)
        elif choice == 2:
            balance = deposit(balance, transactions)
        elif choice == 3:
            balance = withdraw(balance, transactions)
        elif choice == 4:
            mini_statement(transactions)
        elif choice == 5:
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


main()
