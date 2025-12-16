import hashlib
import sqlite3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ChangePin(QWidget):
    def __init__(self,account_id,account_no,full_name,balance):
        super().__init__()
        self.acc_id=account_id
        self.acc_no=account_no
        self.name=full_name
        self.blc=balance
        self.set_ui()
        self.setObjectName("mainwindow")

    def set_ui(self):
        self.setWindowTitle("Change Pin")
        self.setGeometry(200,200,300,350)

        f=QFormLayout()
        self.lbl=QLabel("Change Your Pin")
        self.lbl.setObjectName('head')
        self.lbl1=QLabel("New Pin:")
        self.txt1=QLineEdit()
        self.txt1.setEchoMode(QLineEdit.Password)
        self.lbl2=QLabel("Confirm Pin:")
        self.txt2=QLineEdit()
        self.txt2.setEchoMode(QLineEdit.Password)
        self.btn1=QPushButton("Change")
        self.btn1.clicked.connect(self.change_pin)
        self.btn2=QPushButton("Cancel")
        self.btn2.clicked.connect(self.go_back)

        g=QGridLayout()
        g.addWidget(self.btn1,0,0)
        g.addWidget(self.btn2,0,1)

        f.addRow(self.lbl)
        f.addRow(self.lbl1)
        f.addRow(self.txt1)
        f.addRow(self.lbl2)
        f.addRow(self.txt2)
        f.addRow(g)

        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl1.setAlignment(Qt.AlignHCenter)
        self.lbl2.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)
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

    def change_pin(self):
        np=self.txt1.text()
        cp=self.txt2.text()

        if not np or not cp:
            QMessageBox.critical(self,"Empty","Required field is empty.")
            return

        if len(np)!=4:
            QMessageBox.critical(self,"Invalid Pin Digits","Pin should be 4 digits.")
            return

        if cp!=np:
            QMessageBox.critical(self,"Unmatched","Pin didn't matched.")
            return

        hashed_np=hashlib.sha256(np.encode()).hexdigest()
        hashed_cp=hashlib.sha256(cp.encode()).hexdigest()

        conn=sqlite3.connect("atm.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM user WHERE account_no=?",(self.acc_no,))
        acc_user=cur.fetchone()

        if acc_user:
            cur.execute("UPDATE user SET new_pin=?,confirm_pin=? WHERE account_no=?",(hashed_np,hashed_cp,self.acc_no))
            conn.commit()
            QMessageBox.information(self, "Success", "Pin changed successfully.")

        else:
            QMessageBox.critical(self, "Not Found", "Given account number is not found.")

        conn.commit()

    def go_back(self):
        from main import MainWindow
        self.m = MainWindow(self.acc_id, self.acc_no, self.name, self.blc)
        self.m.show()
        self.close()

if __name__=="__main__":
    a=QApplication(sys.argv)
    w=ChangePin("")
    w.show()
    sys.exit(a.exec_())