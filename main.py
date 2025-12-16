import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

#For Main Window
class MainWindow(QWidget):
    def __init__(self,account_id,account_no,full_name,balance):
        super().__init__()
        self.acc_id=account_id
        self.acc_no=account_no
        self.show_name=full_name
        self.blc=balance
        self.set_ui()
        self.show_transaction()
        self.setObjectName("mainwindow")

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
        self.btn3.clicked.connect(self.open_check)
        self.btn4=QPushButton("4. Transfer")
        self.btn4.clicked.connect(self.open_transfer)
        self.btn5=QPushButton("5. Change Pin")
        self.btn5.clicked.connect(self.open_change)
        self.btn6=QPushButton("6. Exit")
        self.btn6.clicked.connect(self.go_exit)

        self.table_head=QLabel("Transaction:")
        self.table_head.setObjectName("uphead")
        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Date","Type","Amount"])
        self.table.setColumnHidden(0,True)
        self.table.horizontalHeader().setStyleSheet('''
                   QHeaderView::section{
                   background-color:#46464b;
                   font-weight:bold;
                   font-family:Times New Roman;
                   color:#e2e2f1;
                   padding:5px;
                   }
               ''')

        self.table.horizontalHeader().setStretchLastSection(True)

        self.del_btn=QPushButton("Delete")
        self.del_btn.setObjectName("remove")
        self.del_btn.clicked.connect(self.delete_transaction)


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
        v.addWidget(self.table_head)
        v.addWidget(self.table)
        v.addWidget(self.del_btn)


        self.setStyleSheet('''
        QWidget#mainwindow{
        background-color:#c1c1e1;
        }
        
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
        
        QLabel#uphead{
        margin-top:5px;
        margin:bottom:5px;
        font-family:Times New Roman;
        font-size:14px;
        font-weight:bold;
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
        
        QPushButton#remove{
        margin:4px;
        padding:7px;
        background-color:#c1e4f0;
        font-family:Times New Roman;
        font-size:14px;
        border-radius:5px;
        }
        
        QPushButton#remove:hover{
        background-color:#9edef4;
        font-weight:bold;
        }
        ''')

        self.setLayout(v)

    def show_transaction(self):
        try:
         conn=sqlite3.connect("atm.db")
         cur=conn.cursor()
         cur.execute("SELECT t.id,t.date,t.type,t.amount FROM transactions t JOIN user u ON t.user_id=u.account_id WHERE u.account_id=? ORDER BY t.date DESC",(self.acc_id,))
         row=cur.fetchall()
         conn.close()

         self.table.setRowCount(0)

         for num,data in enumerate(row):
             self.table.insertRow(num)
             for c,c_data in enumerate(data):
                 self.table.setItem(num,c,QTableWidgetItem(str(c_data)))

        except Exception as e:
            QMessageBox.critical(self,"DB Error",str(e))

    def open_deposit(self):
        from deposit import Deposit
        self.d=Deposit(self.acc_id,self.acc_no,self.show_name,self.blc)
        self.d.show()
        self.close()

    def open_withdraw(self):
        from withdraw import Withdraw
        self.wd=Withdraw(self.acc_id,self.acc_no,self.show_name,self.blc)
        self.wd.show()
        self.close()

    def open_check(self):
        from checkbalance import CheckBalance
        self.cb=CheckBalance(self.acc_id,self.acc_no,self.show_name,self.blc)
        self.cb.show()
        self.close()

    def open_change(self):
        from changepin import ChangePin
        self.chgpin=ChangePin(self.acc_id,self.acc_no,self.show_name,self.blc)
        self.chgpin.show()
        self.close()

    def open_transfer(self):
        from transfer import Transfer
        self.t=Transfer(self.acc_id,self.acc_no,self.show_name,self.blc)
        self.t.show()
        self.close()

    def go_exit(self):
        from login import Login
        self.ln=Login()
        self.ln.show()
        self.close()

    def delete_transaction(self):
        t=self.table.currentRow()

        if t<0:
            QMessageBox.warning(self,"Select","You must select the transaction for deleting it.")
            return

        transaction_sn=self.table.item(t,0).text()

        confirm=QMessageBox.question(self,"Confirmation for delete","Do you want to delete your transactions?",QMessageBox.Yes|QMessageBox.No)

        if confirm==QMessageBox.No:
            return

        conn=sqlite3.connect("atm.db")
        cur=conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id=? and user_id=?",(transaction_sn,self.acc_id))
        conn.commit()
        conn.close()
        self.show_transaction()
