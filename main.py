import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

#For Main Window
class MainWindow(QWidget):
    def __init__(self,account_id,account_no,full_name):
        super().__init__()
        self.acc_id=account_id
        self.acc_no=account_no
        self.show_name=full_name
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("ATM System")
        self.setGeometry(200,200,400,450)

        v=QVBoxLayout()
        self.lbl=QLabel(f"Welcome: {self.show_name}")
        self.lbl.setObjectName("head")
        self.lbl2=QLabel("Select Your Services:")
        self.lbl2.setObjectName("service")

        g=QGridLayout()
        self.btn1=QPushButton("1. Withdraw")
        self.btn1.clicked.connect(self.open_withdraw)
        self.btn2=QPushButton("2. Deposit")
        self.btn2.clicked.connect(self.open_deposit)
        self.btn3=QPushButton("3. Check Balance")
        self.btn4=QPushButton("4. Transfer")
        self.btn5=QPushButton("5. Change Pin")
        self.btn6=QPushButton("6. Exit")

        g.addWidget(self.btn1,0,0)
        g.addWidget(self.btn2,0,1)
        g.addWidget(self.btn3,1,0)
        g.addWidget(self.btn4,1,1)
        g.addWidget(self.btn5,2,0)
        g.addWidget(self.btn6,2,1)

        g.setColumnStretch(0,1)
        g.setColumnStretch(1,1)

        v.addSpacing(10)
        v.addWidget(self.lbl)
        v.addSpacing(3)
        v.addWidget(self.lbl2)
        v.addSpacing(5)
        v.addLayout(g)
        v.addStretch()
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl2.setAlignment(Qt.AlignCenter)

        self.setStyleSheet('''
        QLabel#head{
        font-family:Times New Roman;
        font-size:22px;
        font-weight:bold;
        margin-top:10px;
        }
        
        QLabel#service{
        font-family:Times New Roman;
        font-size:16px;
        font-weight:bold;
        margin-bottom:12px;
        }
        
        QPushButton{
        margin:4px;
        padding:7px;
        background-color:#c1e4f0;
        font-family:Times New Roman;
        font-size:14px;
        border-radius:5px;
        }
        
        QPushButton:hover{
        background-color:#9edef4;
        font-weight:bold;
        }
        ''')

        self.setLayout(v)


    def open_deposit(self):
        from deposit import Deposit
        self.d=Deposit(self.acc_id,self.acc_no,self.show_name)
        self.d.show()
        self.close()

    def open_withdraw(self):
        from withdraw import Withdraw
        self.wd=Withdraw(self.acc_id,self.acc_no,self.show_name)
        self.wd.show()
        self.close()
