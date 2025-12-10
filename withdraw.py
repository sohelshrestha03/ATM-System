import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Withdraw(QWidget):
    def __init__(self,account_id,account_no,full_name):
        super().__init__()
        self.acc_id=account_id
        self.acc_no=account_no
        self.name=full_name
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("Withdraw Cash")
        self.setGeometry(200,200,300,350)

        f=QFormLayout()
        self.lbl=QLabel("Withdraw Your Money")
        self.lbl.setObjectName("heading")

        self.lbl1=QLabel("Enter Amount For Withdraw:")
        self.txt1=QDoubleSpinBox()
        self.txt1.setMaximum(999999999)
        self.btn1=QPushButton("Withdraw")
        self.btn1.clicked.connect(self.withdraw_cash)
        self.btn2=QPushButton("Cancel")
        self.btn2.clicked.connect(self.cancel_it)

        g=QGridLayout()
        g.addWidget(self.btn1,0,0)
        g.addWidget(self.btn2,0,1)

        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl1.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)

        f.addRow(self.lbl)
        f.addRow(self.lbl1)
        f.addRow(self.txt1)
        f.addRow(g)

        self.setStyleSheet('''
              QLabel#head{
              font-family:Times New Roman;
              font-size:22px;
              font-weight:bold;
              margin-top:10px;
              margin-bottom:12px;
              }

              QLabel{
              font-family:Times New Roman;
              font-size:16px;
              font-weight:bold;
              margin-bottom:12px;
              }

              QLineEdit{
              font-family:Times New Roman;
              font-size:14px;
              margin-bottom:14px;
              }

              QPushButton{
              margin-right:5px;
              margin-left:5px;
              margin-bottom:7px;
              padding:5px;
              font-family:Times New Roman;
              font-size:14px;
              background-color:#c1e4f0;
              border-radius:5px;
              }

              QPushButton:hover{
              background-color:#9edef4;
              font-weight:bold;
              }
              ''')

        self.setLayout(f)

    def withdraw_cash(self):
        amt=self.txt1.value()

        if amt<=0:
            QMessageBox.critical(self, "Insuffient Amount", "Amount should not be less or equal to zero.")
            return

        try:
            conn=sqlite3.connect("atm.db")
            cur=conn.cursor()

            cur.execute("UPDATE user SET balance=balance-? WHERE account_no=?",(amt,self.acc_no))

            if cur.rowcount==0:
                QMessageBox.critical(self, "Not Found", "Account not found.")
                return

            conn.commit()
            conn.close()

            QMessageBox.information(self,"Success",f"Amount Rs.{amt} has been withdrawn from your account.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self,"Database Error",str(e))

    def cancel_it(self):
        from main import MainWindow
        self.m=MainWindow(self.acc_id,self.acc_no,self.name)
        self.m.show()
        self.close()

if __name__=="__main__":
    a=QApplication(sys.argv)
    w=Withdraw("")
    w.show()
    sys.exit(a.exec_())




