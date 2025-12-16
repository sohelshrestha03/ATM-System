import sqlite3
import sys
import hashlib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ForgetPin(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.setObjectName("mainwindow")

    def set_ui(self):
        self.setWindowTitle("Forget Pin")
        self.setGeometry(200, 200, 300, 350)

        form = QFormLayout()
        self.lbl = QLabel("Change Your Pin")
        self.lbl.setObjectName("head")

        self.lbl3 = QLabel("Enter Account Number: ")
        self.txt3 = QLineEdit()
        self.txt3.setPlaceholderText("Enter account Number")

        self.lbl1 = QLabel("Enter new pin:")
        self.txt1 = QLineEdit()
        self.txt1.setEchoMode(QLineEdit.Password)

        self.lbl2 = QLabel("Enter confirm pin:")
        self.txt2 = QLineEdit()
        self.txt2.setEchoMode(QLineEdit.Password)

        self.btn = QPushButton("Reset PIN")
        self.btn.clicked.connect(self.reset_pin)
        self.linklbl=QLabel("<a href='login.py' style='text-decoration:none;margin-top:9px;'>Back</a>")
        self.linklbl.setOpenExternalLinks(False)
        self.linklbl.linkActivated.connect(self.go_back)

        form.addRow(self.lbl)
        form.addRow(self.lbl3)
        form.addRow(self.txt3)
        form.addRow(self.lbl1)
        form.addRow(self.txt1)
        form.addRow(self.lbl2)
        form.addRow(self.txt2)
        form.addRow(self.btn)
        form.addRow(self.linklbl)

        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl3.setAlignment(Qt.AlignHCenter)
        self.txt3.setAlignment(Qt.AlignHCenter)
        self.lbl1.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)
        self.lbl2.setAlignment(Qt.AlignHCenter)
        self.txt2.setAlignment(Qt.AlignHCenter)
        self.linklbl.setAlignment(Qt.AlignHCenter)

        self.setStyleSheet('''
         QWidget#mainwindow{
         background-color:#c1c1e1;
         }
        
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
        background-color:#2948c4;
        padding:4px;
        border-radius:5px;
        }

        QPushButton:hover{
        background-color:#5e7bef;
        color:white;
        fon-weight:bold;
        }

        ''')

        self.setLayout(form)

    def reset_pin(self):
        a = self.txt3.text().strip()
        b = self.txt1.text()
        c = self.txt2.text()

        if not a or not b or not c:
            QMessageBox.critical(self, "Empty", "Required Field is empty.")
            return

        if len(b) != 4:
            QMessageBox.critical(self, "Invalid digits", "Pin digits should be 4.")
            return

        if c != b:
            QMessageBox.critical(self, "Unmatched", "Password didn't match.")
            return

        hashed_np = hashlib.sha256(b.encode()).hexdigest()
        hashed_cp = hashlib.sha256(c.encode()).hexdigest()

        conn = sqlite3.connect("atm.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE account_no=?", (a,))
        acc_no = cur.fetchone()

        if acc_no:
            cur.execute("UPDATE user SET new_pin=?,confirm_pin=? WHERE account_no=?", (hashed_np, hashed_cp, a))
            conn.commit()
            QMessageBox.information(self, "Success", "Pin changed successfully.")

        else:
            QMessageBox.critical(self, "Not Found", "Given account number is not found.")

        conn.close()

    def go_back(self):
        from login import Login
        self.login=Login()
        self.login.show()
        self.close()


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = ForgetPin()
    w.show()
    sys.exit(a.exec_())