# Banking Application - Assignment 3

## What is this?

This is a simple banking app. You can use it with a window (GUI) or in the command line (CLI). You can make accounts, log in, put in or take out money, send money, top up your phone, and see your history. The app saves your data in a file.

## What can you do?

- Make a personal or business account (the app gives you a username and password)
- Log in safely
- Deposit and withdraw money
- Send money to other accounts
- Delete your account
- See your transaction history
- Top up your mobile phone
- The app handles errors and saves your data

## Files in this project

```
banking_app/
│── DorjiWangchuk_02240250_A3.py         # Main app
│── DorjiWangchuk_02240250_A3_test.py    # Tests
│── accounts.txt                         # Where your data is saved
│── README.md                            # This file
```

## How to use

### What you need

- Python 3.6 or newer
- tkinter (comes with Python)

### Start the app

**To use the window (GUI):**
```bash
python DorjiWangchuk_02240250_A3.py
```

**To use the command line:**
```bash
python DorjiWangchuk_02240250_A3.py --cli
```

**To run the tests:**
```bash
python DorjiWangchuk_02240250_A3_test.py
```

## How it works

### In the window (GUI)

1. Click "New Account" to make an account
2. Log in with your account number and password
3. Pick what you want to do
4. Fill in the info and click "Do Action"

### In the command line (CLI)

1. Follow the menu to make or log in to an account
2. After logging in, you can:
    - Deposit or withdraw money
    - Send money
    - Top up your phone
    - See your history
    - Delete your account

## About the tests

The tests check:
- Making accounts
- Deposits, withdrawals, and transfers
- Mobile top-up
- Error handling

To run all tests:
```bash
python -m unittest DorjiWangchuk_02240250_A3_test.py
```

## Notes

- The app uses classes and objects
- It has custom error messages
- Data is saved in `accounts.txt`
- The window uses tkinter
- Tests use unittest


