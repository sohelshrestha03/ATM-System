import sqlite3
import sys
import hashlib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("Login Account")
        self.setGeometry(200,200,400,400)

        l=QFormLayout()
        self.lbl=QLabel("Welcome To ATM Service")
        self.lbl.setObjectName("head")

        self.lbl1=QLabel("Account Number")

        self.txt1=QLineEdit(self)

        self.lbl2=QLabel("Pin")

        self.txt2=QLineEdit(self)
        self.txt2.setEchoMode(QLineEdit.Password)

        self.btn=QPushButton("OK")
        self.btn.clicked.connect(self.log_acc)
        self.forget_pin=QLabel("<a href='changepin.py' style='text-decoration:none;margin-top:10px;'>Forget Pin</a>")
        self.forget_pin.setOpenExternalLinks(False)
        self.forget_pin.linkActivated.connect(self.forgot_pin)

        self.register_acc=QLabel("<a href='register.py' style='text-decoration:none;margin-top:10px;'>Register Account</a>")
        self.register_acc.setOpenExternalLinks(False)
        self.register_acc.linkActivated.connect(self.go_register)


        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl1.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)
        self.lbl2.setAlignment(Qt.AlignHCenter)
        self.txt2.setAlignment(Qt.AlignHCenter)
        self.forget_pin.setAlignment(Qt.AlignHCenter)
        self.register_acc.setAlignment(Qt.AlignHCenter)

        l.addRow(self.lbl)
        l.addRow(self.lbl1)
        l.addRow(self.txt1)
        l.addRow(self.lbl2)
        l.addRow(self.txt2)
        l.addRow(self.btn)
        l.addRow(self.forget_pin)
        l.addRow(self.register_acc)

        self.setStyleSheet('''
        QLabel#head{
        font-family:Times New Roman;
        font-size:22px;
        font-weight:bold;
        margin-top:10px;
        margin-bottom:10px;
        }
        
        QLabel{
        font-family:Times New Roman;
        font-size:14px;
        font-weight:bold;
        margin-bottom:7px;
        }
        
        QLineEdit{
        font-family:Times New Roman;
        font-size:14px;
        margin-bottom:7px;
        }
        
        QPushButton{
        font-family:Times New Roman;
        padding:5px;
        background-color:#cef4fb;
        border-radius:5px;
        }
        
        QPushButton:hover{
        background-color:#a9f2ff;
        color:white;
        font-weight:bold;
        }
        
        
        ''')

        self.setLayout(l)

    def log_acc(self):
        a=self.txt1.text().strip()
        p=self.txt2.text()

        if not a or not p:
            QMessageBox.critical(self,"Empty","Required field is empty.")
            return

        hashed_pin=hashlib.sha256(p.encode()).hexdigest()

        conn=sqlite3.connect("atm.db")
        cur=conn.cursor()
        cur.execute('SELECT account_id,account_no,full_name,balance FROM user WHERE account_no=? AND confirm_pin=?', (a, hashed_pin))
        acc_holder=cur.fetchone()
        conn.close()

        if acc_holder:
            account_id,account_no,full_name,balance=acc_holder
            balance=float(balance)
            from main import MainWindow
            self.main_app=MainWindow(account_id,account_no,full_name,balance)
            self.main_app.show()
            self.close()

        else:
            QMessageBox.critical(self,"Not Found","Given account number and pin is not found.")

    def forgot_pin(self):
        from forgetpin import ForgetPin
        self.chg=ForgetPin()
        self.chg.show()
        self.close()

    def go_register(self):
        from register import Register
        self.reg=Register()
        self.reg.show()
        self.close()

if __name__=="__main__":
    a=QApplication(sys.argv)
    w=Login()
    w.show()
    sys.exit(a.exec_())

