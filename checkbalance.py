import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class CheckBalance(QWidget):
    def __init__(self,account_id,account_no,full_name,balance):
        super().__init__()
        self.acc_id=account_id
        self.acc_no=account_no
        self.name=full_name
        self.blc=balance
        self.set_ui()
        self.setObjectName("mainwindow")

    def set_ui(self):
        self.setWindowTitle("Check Balance")
        self.setGeometry(200,200,300,350)

        f=QFormLayout()
        self.lbl=QLabel("Your Balance")
        self.lbl.setObjectName("head")
        self.lbl1=QLabel("Account No:")
        self.lbl1.setObjectName("attribute")
        self.lbl2=QLabel(self.acc_no)
        self.lbl2.setObjectName("showdata")
        self.lbl3=QLabel("Full name:")
        self.lbl3.setObjectName("attribute")
        self.lbl4=QLabel(self.name)
        self.lbl4.setObjectName("showdata")
        self.lbl5=QLabel("Balance:")
        self.lbl5.setObjectName("attribute")
        self.lbl6=QLabel(str(self.blc))
        self.lbl6.setObjectName("showdata")
        self.btn=QPushButton("Back")
        self.btn.clicked.connect(self.go_back)

        self.lbl.setAlignment(Qt.AlignHCenter)

        f.addRow(self.lbl)
        f.addRow(self.lbl1,self.lbl2)
        f.addRow(self.lbl3,self.lbl4)
        f.addRow(self.lbl5,self.lbl6)
        f.addRow(self.btn)

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
        
        QLabel#attribute{
        font-family:Times New Roman;
        font-size:16px;
        font-weight:bold;
        margin-bottom:5px;
        }
        
        QLabel#showdata{
        font-family:Times New Roman;
        font-size:14px;
        margin-bottom:5px;
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

    def go_back(self):
        from main import MainWindow
        self.m=MainWindow(self.acc_id,self.acc_no,self.name,self.blc)
        self.m.show()
        self.close()

if __name__=="__main__":
    a=QApplication(sys.argv)
    w=CheckBalance()
    w.show()
    sys.exit(a.exec_())

