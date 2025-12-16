import sqlite3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Transfer(QWidget):
    def __init__(self,account_id,account_no,full_name,balance):
        super().__init__()
        self.acc_id=account_id
        self.acc_no=account_no
        self.name=full_name
        self.blc=balance
        self.set_ui()
        self.setObjectName("mainwindow")

    def set_ui(self):
        self.setWindowTitle("Money Transfer")
        self.setGeometry(200,200,300,350)

        f=QFormLayout()
        self.lbl=QLabel("Transfer Your Balance")
        self.lbl.setObjectName('head')

        self.lbl1=QLabel("From Account:")
        self.lbl1.setObjectName("lblacc")
        self.lbl2=QLabel(self.acc_no)
        self.lbl2.setObjectName("acc")

        self.lbl3=QLabel("To Account:")
        self.txt1=QLineEdit()

        self.lbl4=QLabel("Enter Amount:")
        self.txt2=QDoubleSpinBox()
        self.txt2.setMaximum(999999999)

        self.btn1=QPushButton("Transfer")
        self.btn1.clicked.connect(self.transfer_money)
        self.btn2=QPushButton("Cancel")
        self.btn2.clicked.connect(self.go_back)

        g=QGridLayout()
        g.addWidget(self.btn1,0,0)
        g.addWidget(self.btn2,0,1)

        f.addRow(self.lbl)
        f.addRow(self.lbl1,self.lbl2)
        f.addRow(self.lbl3)
        f.addRow(self.txt1)
        f.addRow(self.lbl4)
        f.addRow(self.txt2)
        f.addRow(g)

        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl3.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)
        self.lbl4.setAlignment(Qt.AlignHCenter)
        self.txt2.setAlignment(Qt.AlignHCenter)

        self.setStyleSheet('''
        QWidget#mainwindow{
         background-color:#c1c1e1;
        }
        
        QLabel#head{
        font-family:Times New Roman;
        font-weight:bold;
        font-size:22px;
        margin-top:10px;
        margin-bottom:12px;
        }
        
        QLabel#lblacc{
        font-family:Times New Roman;
        font-weight:bold;
        font-size:16px;
        margin-bottom:10px;
        }
        
        QLabel#acc{
        font-family:Times New Roman;
        font-size:14px;
        margin-bottom:10px;
        }
        
        QLabel{
        font-family:Times New Roman;
        font-weight:bold;
        font-size:16px;
        margin-bottom:10px;
        }
        
        QLineEdit{
        font-family:Times New Roman;
        font-size:14px;
        margin-bottom:10px;
        }
        
         QPushButton{
         font-family:Times New Roman;
         font-size:14px;
         padding:5px;
         background-color:#c1e4f0;
         border-radius:5px;
        }
        
        QPushButton:hover{
          background-color:#9edef4;
          font-weight:bold;
        }
        ''')

        self.setLayout(f)

    def transfer_money(self):
        another_account=self.txt1.text().strip()
        amt=self.txt2.value()

        if not another_account or not amt:
            QMessageBox.critical(self,"Empty","Required field is empty.")
            return

        if another_account==self.acc_no:
            QMessageBox.critical(self,"Error","You cannot transfer money into your own account.")
            return

        if amt>self.blc:
            QMessageBox.warning(self,"Insufficient Balance","You don't have enough balance for transfer.")
            return

        conn=sqlite3.connect("atm.db")
        cur=conn.cursor()
        cur.execute('SELECT account_no,balance FROM user WHERE account_no=?',(another_account,))
        reciever=cur.fetchone()

        if not reciever:
            QMessageBox.critical(self,"Not Found","receiver account not found.")
            conn.close()
            return

        reciever_no,reciever_blc=reciever

        sender_blc=self.blc-amt
        to_reciever_blc=reciever_blc+amt

        cur.execute("UPDATE user SET balance=? WHERE account_no=?",(sender_blc,self.acc_no))
        cur.execute("UPDATE user SET balance=? WHERE account_no=?",(to_reciever_blc,reciever_no))

        cur.execute("INSERT INTO transactions(account_no,type,amount,user_id)VALUES(?,?,?,?)",(self.acc_no, f"Transfer to:-{self.name}", amt, self.acc_id))
        conn.commit()
        conn.close()

        self.blc=sender_blc

        QMessageBox.information(self,"Success",f"Rs.{amt} transferred successfully.")
        self.clear_data()

    def clear_data(self):
        self.txt1.clear()
        self.txt2.clear()

    def go_back(self):
        from main import MainWindow
        self.m=MainWindow(self.acc_id, self.acc_no, self.name, self.blc)
        self.m.show()
        self.close()

if __name__=="__main__":
    a=QApplication(sys.argv)
    w=Transfer("")
    w.show()
    sys.exit(a.exec_())

