import unittest
import os
from DorjiWangchuk_02240250_A3 import BankManager, Account, PersonalAccount, BusinessAccount
from DorjiWangchuk_02240250_A3 import BankError, NotEnoughMoneyError, BadInputError

class TestAccountBasics(unittest.TestCase):
    """Tests for core account functionality"""
    
    def setUp(self):
        """Create test account"""
        self.test_acc = Account("12345", "pass123", "Test", 1000)
    
    def test_deposit_positive(self):
        """Adding money increases balance"""
        self.test_acc.add_money(500)
        self.assertEqual(self.test_acc.balance, 1500)
        self.assertIn("Added 500", self.test_acc.history)
    
    def test_deposit_negative(self):
        """Can't deposit negative amounts"""
        with self.assertRaises(BadInputError):
            self.test_acc.add_money(-100)
    
    def test_withdraw_success(self):
        """Withdrawing available funds"""
        self.test_acc.take_money(200)
        self.assertEqual(self.test_acc.balance, 800)
    
    def test_withdraw_insufficient(self):
        """Can't withdraw more than balance"""
        with self.assertRaises(NotEnoughMoneyError):
            self.test_acc.take_money(2000)

class TestTransferOperations(unittest.TestCase):
    """Tests for money transfers between accounts"""
    
    def setUp(self):
        """Create test accounts"""
        self.acc1 = Account("11111", "pass1", "Test", 1000)
        self.acc2 = Account("22222", "pass2", "Test", 500)
    
    def test_successful_transfer(self):
        """Normal transfer between accounts"""
        self.acc1.send_money(300, self.acc2)
        self.assertEqual(self.acc1.balance, 700)
        self.assertEqual(self.acc2.balance, 800)
    
    def test_transfer_insufficient(self):
        """Can't transfer more than balance"""
        with self.assertRaises(NotEnoughMoneyError):
            self.acc1.send_money(2000, self.acc2)

class TestAccountTypes(unittest.TestCase):
    """Tests for different account types"""
    
    def test_personal_account(self):
        """Personal account initialization"""
        acc = PersonalAccount("33333", "pass3")
        self.assertEqual(acc.type, "Personal")
        self.assertEqual(acc.balance, 0)
    
    def test_business_account(self):
        """Business account initialization"""
        acc = BusinessAccount("44444", "pass4", 2000)
        self.assertEqual(acc.type, "Business")
        self.assertEqual(acc.balance, 2000)

class TestBankManager(unittest.TestCase):
    """Tests for bank management system"""
    
    TEST_FILE = "test_bank_data.txt"
    
    def setUp(self):
        """Set up test environment"""
        # Backup original file name
        self.original_file = BankManager.DATA_FILE
        BankManager.DATA_FILE = self.TEST_FILE
        
        # Create test file
        with open(self.TEST_FILE, 'w') as f:
            f.write("11111|pass1|Personal|1000|0|\n")
            f.write("22222|pass2|Business|5000|0|\n")
        
        self.bank = BankManager()
    
    def tearDown(self):
        """Clean up test environment"""
        BankManager.DATA_FILE = self.original_file
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)
    
    def test_load_accounts(self):
        """Test loading accounts from file"""
        self.assertEqual(len(self.bank.accounts), 2)
        self.assertIn("11111", self.bank.accounts)
        self.assertIn("22222", self.bank.accounts)
    
    def test_create_account(self):
        """Test account creation"""
        num, pwd = self.bank.make_account("Personal")
        self.assertEqual(len(num), 5)
        self.assertEqual(len(pwd), 4)
        self.assertIn(num, self.bank.accounts)
    
    def test_successful_login(self):
        """Test valid login"""
        acc = self.bank.login("11111", "pass1")
        self.assertEqual(acc.number, "11111")
    
    def test_failed_login(self):
        """Test invalid login attempts"""
        with self.assertRaises(BankError):
            self.bank.login("99999", "wrong")  # Wrong account
        with self.assertRaises(BankError):
            self.bank.login("11111", "wrong")  # Wrong password
    
    def test_account_deletion(self):
        """Test removing accounts"""
        self.bank.remove_account("11111")
        self.assertNotIn("11111", self.bank.accounts)

class TestBankOperations(unittest.TestCase):
    """Tests for banking operations through manager"""
    
    def setUp(self):
        """Set up test bank"""
        self.bank = BankManager()
        self.test_num, self.test_pwd = self.bank.make_account("Personal")
        self.bank.accounts[self.test_num].balance = 1000  # Set test balance
    
    def test_deposit_operation(self):
        """Test deposit through bank manager"""
        result = self.bank.handle_choice('3', self.test_num, self.test_pwd, "500")
        self.assertIn("Added 500", result)
        self.assertEqual(self.bank.accounts[self.test_num].balance, 1500)
    
    def test_invalid_deposit(self):
        """Test bad deposit input"""
        with self.assertRaises(BadInputError):
            self.bank.handle_choice('3', self.test_num, self.test_pwd, "not_number")

class TestPhoneTopUp(unittest.TestCase):
    """Tests for mobile credit functionality"""
    
    def setUp(self):
        """Set up test account"""
        self.bank = BankManager()
        self.test_num, self.test_pwd = self.bank.make_account("Personal")
        self.bank.accounts[self.test_num].balance = 1000
    
    def test_top_up_success(self):
        """Test successful phone credit"""
        result = self.bank.handle_choice('8', self.test_num, self.test_pwd, "200")
        self.assertIn("Added 200 phone credit", result)
        self.assertEqual(self.bank.accounts[self.test_num].phone_credit, 200)
        self.assertEqual(self.bank.accounts[self.test_num].balance, 800)
    
    def test_top_up_insufficient(self):
        """Test without enough balance"""
        with self.assertRaises(NotEnoughMoneyError):
            self.bank.handle_choice('8', self.test_num, self.test_pwd, "2000")

if __name__ == '__main__':
    unittest.main()