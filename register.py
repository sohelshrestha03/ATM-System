import sqlite3
import sys
import hashlib
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("Register Account")
        self.setGeometry(200,200,400,500)

        form=QFormLayout()
        self.lbl=QLabel("Register Your Account")
        self.lbl.setObjectName("heading")

        self.lbl1=QLabel("Enter Account Number:")
        self.txt1=QLineEdit()
        self.txt1.setPlaceholderText("Account Number")

        self.name_lbl=QLabel("Enter Full Name:")
        self.name_txt=QLineEdit()
        self.name_txt.setPlaceholderText("Full Name")

        self.phone_lbl=QLabel("Enter Phone Number:")
        self.phone_txt=QLineEdit()
        self.phone_txt.setPlaceholderText("Phone Number")

        self.email_lbl=QLabel("Enter Email:")
        self.email_txt=QLineEdit()
        self.email_txt.setPlaceholderText("Email")


        self.lbl2=QLabel("Enter New Pin:")
        self.txt2=QLineEdit()
        self.txt2.setEchoMode(QLineEdit.Password)
        self.txt2.setPlaceholderText("New Pin")

        self.lbl3=QLabel("Enter Confirm Pin:")
        self.txt3=QLineEdit()
        self.txt3.setEchoMode(QLineEdit.Password)
        self.txt3.setPlaceholderText("Confirm Password")

        self.lbl4=QLabel("Enter your balance: ")
        self.txt4=QDoubleSpinBox()
        self.txt4.setMaximum(999999999)

        self.btn=QPushButton("Done")
        self.btn.clicked.connect(self.register_account)

        self.log_lbl=QLabel("<a href='login.py' style='text-decoration:none;margin-top:10px';>Back</a>")
        self.log_lbl.setOpenExternalLinks(False)
        self.log_lbl.linkActivated.connect(self.open_login)

        form.addRow(self.lbl)
        form.addRow(self.lbl1,self.txt1)
        form.addRow(self.name_lbl,self.name_txt)
        form.addRow(self.phone_lbl,self.phone_txt)
        form.addRow(self.email_lbl,self.email_txt)
        form.addRow(self.lbl2,self.txt2)
        form.addRow(self.lbl3,self.txt3)
        form.addRow(self.lbl4,self.txt4)
        form.addRow(self.btn)
        form.addRow(self.log_lbl)


        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl1.setAlignment(Qt.AlignHCenter)
        self.lbl2.setAlignment(Qt.AlignHCenter)
        self.lbl3.setAlignment(Qt.AlignHCenter)
        self.lbl4.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)
        self.txt2.setAlignment(Qt.AlignHCenter)
        self.txt3.setAlignment(Qt.AlignHCenter)
        self.txt4.setAlignment(Qt.AlignHCenter)
        self.log_lbl.setAlignment(Qt.AlignHCenter)
        self.name_txt.setAlignment(Qt.AlignHCenter)
        self.name_lbl.setAlignment(Qt.AlignHCenter)
        self.phone_lbl.setAlignment(Qt.AlignHCenter)
        self.phone_txt.setAlignment(Qt.AlignHCenter)
        self.email_txt.setAlignment(Qt.AlignHCenter)
        self.email_lbl.setAlignment(Qt.AlignHCenter)



        self.setStyleSheet('''
        QLabel#heading{
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
        background-color:#6df37a;
        border-radius:5px;
        }
        
        QPushButton:hover{
        background-color:#2df240;
        color:white;
        font-weight:bold;
        }
        ''')

        self.setLayout(form)

    def register_account(self):
        acc=self.txt1.text().strip()
        name=self.name_txt.text().strip()
        phone=self.phone_txt.text().strip()
        email=self.email_txt.text().strip()
        np=self.txt2.text()
        cp=self.txt3.text()
        balance=self.txt4.value()

        hashed_np=hashlib.sha256(np.encode()).hexdigest()
        hashed_cp=hashlib.sha256(cp.encode()).hexdigest()

        if not acc or not name or not phone or not email or not np or not cp or not balance:
            QMessageBox.critical(self,"Empty","Required field is empty.")
            return

        if len(acc)!=16:
            QMessageBox.critical(self,"Digits Invalid","Account number should be 16 digits.")
            return

        if len(phone)!=10:
            QMessageBox.critical(self,"Invalid number","Phone number should be 10 digits.")
            return

        if not phone.isdigit():
            QMessageBox.critical(self,"Invalid number format","Phone number should be digits.")
            return

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            self.display_error("Invalid email format.")
            return


        if len(np)!=4:
            QMessageBox.critical(self,"Digits Invalid","Pin should be 4 digits.")
            return

        if np!=cp:
            QMessageBox.critical(self,"Unmatch","Password didn't match.")
            return

        if balance<=0:
            QMessageBox.critical(self,"Insufficient Balance","Balance should be more than Rs.O.")
            return

        if balance<1000:
            QMessageBox.critical(self,"Not valid amount","Balance should be Rs.1000 or more than Rs.1000.")
            return

        conn=sqlite3.connect("atm.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM user WHERE account_no=?",(acc,))

        if cur.fetchone():
            QMessageBox.warning(self,"Account Exist","This account number is already registered.")
            conn.close()
            return

        cur.execute('''INSERT INTO user(account_no,full_name,phone_no,email,new_pin,confirm_pin,balance) VALUES(?,?,?,?,?,?,?)'''
                    ,(acc,name,phone,email,hashed_np,hashed_cp,balance))
        conn.commit()
        conn.close()

        QMessageBox.information(self,"Success","Your account has been created successfully.")
        self.clear_box()

    def clear_box(self):
        self.txt1.clear()
        self.name_lbl.clear()
        self.phone_lbl.clear()
        self.email_lbl.clear()
        self.txt2.clear()
        self.txt3.clear()
        self.txt4.setValue(0)

    def open_login(self):
        from login import Login
        self.l=Login()
        self.l.show()
        self.close()


if __name__=="__main__":
    a=QApplication(sys.argv)
    w=Register()
    w.show()
    sys.exit(a.exec_())