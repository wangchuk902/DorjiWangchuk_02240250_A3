import random
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class BankError(Exception):
    """Base error for banking operations"""
    pass

class NotEnoughMoneyError(BankError):
    """When account doesn't have enough funds"""
    pass

class BadInputError(BankError):
    """For invalid user inputs"""
    pass

class NoAccountError(BankError):
    """When account doesn't exist"""
    pass

class WrongPasswordError(BankError):
    """For incorrect login attempts"""
    pass

class Account:
    """Base account class with core banking features"""
    
    def __init__(self, num, pwd, kind, money=0):
        """Initialize account with number, password, type and balance"""
        self.number = num
        self.password = pwd
        self.type = kind
        self.balance = money
        self.phone_credit = 0
        self.history = []
    
    def add_money(self, amount):
        """Deposit money into account"""
        if amount <= 0:
            raise BadInputError("Amount must be positive")
        self.balance += amount
        self.history.append(f"Added {amount}")
    
    def take_money(self, amount):
        """Withdraw money from account"""
        if amount <= 0:
            raise BadInputError("Amount must be positive")
        if amount > self.balance:
            raise NotEnoughMoneyError("Not enough funds")
        self.balance -= amount
        self.history.append(f"Took {amount}")
    
    def send_money(self, amount, other_account):
        """Transfer to another account"""
        self.take_money(amount)
        other_account.add_money(amount)
        self.history.append(f"Sent {amount} to {other_account.number}")
        other_account.history.append(f"Got {amount} from {self.number}")
    
    def add_phone_credit(self, amount):
        """Top up mobile balance"""
        self.take_money(amount)
        self.phone_credit += amount
        self.history.append(f"Phone +{amount}")

class PersonalAccount(Account):
    """Account for individual customers"""
    def __init__(self, num, pwd, money=0):
        super().__init__(num, pwd, "Personal", money)

class BusinessAccount(Account):
    """Account for business customers"""
    def __init__(self, num, pwd, money=0):
        super().__init__(num, pwd, "Business", money)

class BankManager:
    """Handles all bank operations and data storage"""
    
    DATA_FILE = "bank_data.txt"
    
    def __init__(self):
        self.accounts = {}
        self.load_data()
    
    def load_data(self):
        """Load accounts from file"""
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        num = parts[0]
                        pwd = parts[1]
                        kind = parts[2]
                        money = float(parts[3])
                        phone = float(parts[4])
                        
                        if kind == "Personal":
                            acc = PersonalAccount(num, pwd, money)
                        else:
                            acc = BusinessAccount(num, pwd, money)
                        
                        acc.phone_credit = phone
                        if len(parts) > 5:
                            acc.history = parts[5].split(';')
                        
                        self.accounts[num] = acc
    
    def save_data(self):
        """Save accounts to file"""
        with open(self.DATA_FILE, 'w') as f:
            for acc in self.accounts.values():
                history = ';'.join(acc.history)
                f.write(f"{acc.number}|{acc.password}|{acc.type}|{acc.balance}|{acc.phone_credit}|{history}\n")
    
    def make_account(self, acc_type):
        """Create new account"""
        num = str(random.randint(10000, 99999))
        while num in self.accounts:
            num = str(random.randint(10000, 99999))
        
        pwd = str(random.randint(1000, 9999))
        
        if acc_type == "Personal":
            acc = PersonalAccount(num, pwd)
        else:
            acc = BusinessAccount(num, pwd)
        
        self.accounts[num] = acc
        self.save_data()
        return num, pwd
    
    def login(self, num, pwd):
        """Authenticate user"""
        if num not in self.accounts:
            raise NoAccountError("Account not found")
        if self.accounts[num].password != pwd:
            raise WrongPasswordError("Wrong password")
        return self.accounts[num]
    
    def remove_account(self, num):
        """Delete account"""
        if num in self.accounts:
            del self.accounts[num]
            self.save_data()
        else:
            raise NoAccountError("Account not found")
    
    def handle_choice(self, choice, *args):
        """Process user menu selections"""
        try:
            if choice == '1':  # New account
                acc_type = args[0]
                num, pwd = self.make_account(acc_type)
                return f"New {acc_type} account:\nNumber: {num}\nPassword: {pwd}"
            
            elif choice == '2':  # Login
                num = args[0]
                pwd = args[1]
                acc = self.login(num, pwd)
                return f"Welcome {acc.type} account {num}"
            
            elif choice == '3':  # Deposit
                num = args[0]
                pwd = args[1]
                amount = float(args[2])
                acc = self.login(num, pwd)
                acc.add_money(amount)
                self.save_data()
                return f"Added {amount}. New balance: {acc.balance}"
            
            elif choice == '4':  # Withdraw
                num = args[0]
                pwd = args[1]
                amount = float(args[2])
                acc = self.login(num, pwd)
                acc.take_money(amount)
                self.save_data()
                return f"Withdrew {amount}. New balance: {acc.balance}"
            
            elif choice == '5':  # Transfer
                from_num = args[0]
                pwd = args[1]
                to_num = args[2]
                amount = float(args[3])
                
                from_acc = self.login(from_num, pwd)
                if to_num not in self.accounts:
                    raise NoAccountError("Receiver account not found")
                
                to_acc = self.accounts[to_num]
                from_acc.send_money(amount, to_acc)
                self.save_data()
                return f"Sent {amount} to {to_num}"
            
            elif choice == '6':  # Check balance
                num = args[0]
                pwd = args[1]
                acc = self.login(num, pwd)
                return f"Balance: {acc.balance}\nPhone credit: {acc.phone_credit}"
            
            elif choice == '7':  # Delete account
                num = args[0]
                pwd = args[1]
                self.login(num, pwd)
                self.remove_account(num)
                return f"Account {num} deleted"
            
            elif choice == '8':  # Phone top-up
                num = args[0]
                pwd = args[1]
                amount = float(args[2])
                acc = self.login(num, pwd)
                acc.add_phone_credit(amount)
                self.save_data()
                return f"Added {int(amount)} phone credit. New balance: {int(acc.phone_credit)}"
            
            elif choice == '9':  # History
                num = args[0]
                pwd = args[1]
                acc = self.login(num, pwd)
                return "\n".join(acc.history) if acc.history else "No transactions"
            
            else:
                return "Invalid option"
        
        except ValueError:
            raise BadInputError("Please enter numbers only")

class BankAppGUI:
    """Graphical interface for the banking app"""
    
    def __init__(self, manager):
        self.manager = manager
        self.current_acc = None
        
        self.window = tk.Tk()
        self.window.title("Simple Bank")
        self.setup_ui()
    
    def setup_ui(self):
        """Create all UI elements"""
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack()
        
        # Title
        tk.Label(main_frame, text="Bank App", font=('Arial', 16)).grid(
            row=0, column=0, columnspan=2, pady=10)
        
        # Login section
        self.login_frame = tk.Frame(main_frame)
        self.login_frame.grid(row=1, column=0, columnspan=2)
        
        tk.Label(self.login_frame, text="Account #:").grid(row=0, column=0)
        self.num_entry = tk.Entry(self.login_frame)
        self.num_entry.grid(row=0, column=1)
        
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.pwd_entry = tk.Entry(self.login_frame, show="*")
        self.pwd_entry.grid(row=1, column=1)
        
        tk.Button(self.login_frame, text="Login", command=self.do_login).grid(
            row=2, column=0, columnspan=2, pady=5)
        
        # Account actions
        self.actions_frame = tk.Frame(main_frame)
        
        self.acc_info = tk.Label(self.actions_frame, font=('Arial', 12))
        self.acc_info.pack()
        
        tk.Label(self.actions_frame, text="Choose action:").pack()
        
        self.action_var = tk.StringVar()
        actions = [
            ("3. Deposit", "3"),
            ("4. Withdraw", "4"),
            ("5. Transfer", "5"),
            ("6. View Balance", "6"),
            ("7. Delete Account", "7"),
            ("8. Phone Top-up", "8"),
            ("9. History", "9"),
            ("0. Logout", "0")
        ]
        
        for text, val in actions:
            tk.Radiobutton(self.actions_frame, text=text, 
                          variable=self.action_var, value=val).pack(anchor='w')
        
        # Input fields
        self.input_frame = tk.Frame(self.actions_frame)
        self.input_frame.pack(pady=10)
        
        self.input_labels = []
        self.input_boxes = []
        
        for i in range(3):
            label = tk.Label(self.input_frame, text="")
            label.grid(row=i, column=0, sticky='e')
            entry = tk.Entry(self.input_frame, width=20)
            entry.grid(row=i, column=1, pady=2)
            self.input_labels.append(label)
            self.input_boxes.append(entry)
        
        self.action_var.trace('w', self.update_inputs)
        self.action_var.set("3")
        
        # Output area
        self.output = tk.Text(main_frame, height=10, width=50, state='disabled')
        self.output.grid(row=3, column=0, columnspan=2)
        
        # Action button
        tk.Button(main_frame, text="Do Action", command=self.do_action).grid(
            row=4, column=0, columnspan=2, pady=10)
        
        # New account button
        tk.Button(main_frame, text="New Account", 
                 command=self.make_new_account).grid(
            row=5, column=0, columnspan=2, pady=5)
    
    def update_inputs(self, *args):
        """Show relevant input fields for each action"""
        choice = self.action_var.get()
        
        # Hide all first
        for label, box in zip(self.input_labels, self.input_boxes):
            label.grid_remove()
            box.grid_remove()
            box.delete(0, tk.END)
        
        if choice == '3':  # Deposit
            self.input_labels[0].config(text="Amount:")
            self.input_labels[0].grid()
            self.input_boxes[0].grid()
        
        elif choice == '4':  # Withdraw
            self.input_labels[0].config(text="Amount:")
            self.input_labels[0].grid()
            self.input_boxes[0].grid()
        
        elif choice == '5':  # Transfer
            self.input_labels[0].config(text="To Account:")
            self.input_labels[1].config(text="Amount:")
            self.input_labels[0].grid()
            self.input_boxes[0].grid()
            self.input_labels[1].grid()
            self.input_boxes[1].grid()
        
        elif choice == '8':  # Phone top-up
            self.input_labels[0].config(text="Amount:")
            self.input_labels[0].grid()
            self.input_boxes[0].grid()
    
    def show_message(self, text):
        """Display output"""
        self.output.config(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')
    
    def do_login(self):
        """Handle login attempt"""
        num = self.num_entry.get()
        pwd = self.pwd_entry.get()
        
        try:
            self.current_acc = self.manager.login(num, pwd)
            self.acc_info.config(
                text=f"{self.current_acc.type} Account {num}")
            self.login_frame.grid_remove()
            self.actions_frame.grid(row=1, column=0, columnspan=2)
            self.show_message(f"Welcome! Balance: {self.current_acc.balance}")
        except BankError as e:
            messagebox.showerror("Error", str(e))
    
    def do_action(self):
        """Perform selected banking action"""
        if not self.current_acc:
            return
        
        choice = self.action_var.get()
        
        if choice == '0':  # Logout
            self.current_acc = None
            self.actions_frame.grid_remove()
            self.login_frame.grid()
            self.num_entry.delete(0, tk.END)
            self.pwd_entry.delete(0, tk.END)
            self.show_message("Logged out")
            return
        
        try:
            num = self.current_acc.number
            pwd = self.current_acc.password
            
            if choice == '3':  # Deposit
                amount = self.input_boxes[0].get()
                result = self.manager.handle_choice(choice, num, pwd, amount)
            
            elif choice == '4':  # Withdraw
                amount = self.input_boxes[0].get()
                result = self.manager.handle_choice(choice, num, pwd, amount)
            
            elif choice == '5':  # Transfer
                to_num = self.input_boxes[0].get()
                amount = self.input_boxes[1].get()
                result = self.manager.handle_choice(choice, num, pwd, to_num, amount)
            
            elif choice == '6':  # Balance
                result = self.manager.handle_choice(choice, num, pwd)
            
            elif choice == '7':  # Delete
                result = self.manager.handle_choice(choice, num, pwd)
                if "deleted" in result:
                    self.current_acc = None
                    self.actions_frame.grid_remove()
                    self.login_frame.grid()
                    self.num_entry.delete(0, tk.END)
                    self.pwd_entry.delete(0, tk.END)
            
            elif choice == '8':  # Phone
                amount = self.input_boxes[0].get()
                result = self.manager.handle_choice(choice, num, pwd, amount)
            
            elif choice == '9':  # History
                result = self.manager.handle_choice(choice, num, pwd)
            
            self.show_message(result)
        
        except BankError as e:
            messagebox.showerror("Error", str(e))
    
    def make_new_account(self):
        """Create new account dialog"""
        acc_type = simpledialog.askstring("New Account", 
                                        "Account type (Personal/Business):")
        if acc_type and acc_type.lower() in ['personal', 'business']:
            try:
                result = self.manager.handle_choice('1', acc_type.capitalize())
                messagebox.showinfo("Success", result)
            except BankError as e:
                messagebox.showerror("Error", str(e))
        elif acc_type:
            messagebox.showerror("Error", "Must be Personal or Business")
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

def main():
    """Run the banking application"""
    bank = BankManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Command line interface
        print("Bank App - Command Line")
        while True:
            print("\nMain Menu:")
            print("1. New Account")
            print("2. Login")
            print("0. Exit")
            
            choice = input("Choose: ")
            
            if choice == '0':
                break
            
            try:
                if choice == '1':
                    acc_type = input("Account type (Personal/Business): ")
                    num, pwd = bank.make_account(acc_type)
                    print(f"Created {acc_type} account:\n#: {num}\nPassword: {pwd}")
                
                elif choice == '2':
                    num = input("Account #: ")
                    pwd = input("Password: ")
                    acc = bank.login(num, pwd)
                    print(f"Welcome {acc.type} account {num}")
                    
                    while True:
                        print("\nAccount Menu:")
                        print("3. Deposit")
                        print("4. Withdraw")
                        print("5. Transfer")
                        print("6. Balance")
                        print("7. Delete")
                        print("8. Phone")
                        print("9. History")
                        print("0. Logout")
                        
                        action = input("Choose: ")
                        
                        if action == '0':
                            break
                        
                        try:
                            if action == '3':
                                amount = float(input("Amount: "))
                                acc.add_money(amount)
                                bank.save_data()
                                print(f"Added {amount}. New balance: {acc.balance}")
                            
                            elif action == '4':
                                amount = float(input("Amount: "))
                                acc.take_money(amount)
                                bank.save_data()
                                print(f"Withdrew {amount}. New balance: {acc.balance}")
                            
                            elif action == '5':
                                to_num = input("To account #: ")
                                amount = float(input("Amount: "))
                                if to_num not in bank.accounts:
                                    print("Account not found")
                                    continue
                                acc.send_money(amount, bank.accounts[to_num])
                                bank.save_data()
                                print(f"Sent {amount} to {to_num}")
                            
                            elif action == '6':
                                print(f"Balance: {acc.balance}\nPhone: {acc.phone_credit}")
                            
                            elif action == '7':
                                confirm = input("Delete account? (y/n): ")
                                if confirm.lower() == 'y':
                                    bank.remove_account(num)
                                    print(f"Account {num} deleted")
                                    break
                            
                            elif action == '8':
                                amount = float(input("Amount: "))
                                acc.add_phone_credit(amount)
                                bank.save_data()
                                print(f"Added {amount} phone credit")
                            
                            elif action == '9':
                                print("\n".join(acc.history) if acc.history else "No history")
                            
                            else:
                                print("Invalid choice")
                        
                        except BankError as e:
                            print(f"Error: {str(e)}")
                        except ValueError:
                            print("Please enter numbers only")
                
                else:
                    print("Invalid choice")
            
            except BankError as e:
                print(f"Error: {str(e)}")
    
    else:
        # Graphical interface
        app = BankAppGUI(bank)
        app.run()

if __name__ == "__main__":
    import sys
    main()