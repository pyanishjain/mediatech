from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from time import sleep
import time
import os
import pandas
import re
from googlesearch import search 
import threading
from PyQt5.QtWidgets import QFileDialog

chrome_path="D:\drivers\chromedriver.exe"
chrome_options = Options()
B_name=[]
Address_name=[]
reg = re.compile('\d{6}')
PINCODE=[]
Web_link=[]
mbl_num=[]
browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 743)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 151, 71))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(470, 20, 141, 91))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 70, 131, 81))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(480, 80, 141, 71))
        self.label_4.setObjectName("label_4")
        self.Result = QtWidgets.QPushButton(self.centralwidget)
        self.Result.setGeometry(QtCore.QRect(330, 150, 191, 71))
        self.Result.setObjectName("Result")
        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(482, 160, 191, 71))
        self.Save.setObjectName("Save")
        self.mobile = QtWidgets.QLineEdit(self.centralwidget)
        self.mobile.setGeometry(QtCore.QRect(230, 50, 113, 22))
        self.mobile.setObjectName("mobile")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(640, 50, 113, 22))
        self.password.setObjectName("password")
        self.keyword = QtWidgets.QLineEdit(self.centralwidget)
        self.keyword.setGeometry(QtCore.QRect(230, 100, 113, 22))
        self.keyword.setObjectName("keyword")
        self.location = QtWidgets.QLineEdit(self.centralwidget)
        self.location.setGeometry(QtCore.QRect(650, 110, 113, 22))
        self.location.setObjectName("location")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 290, 941, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(180)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionsave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "IndiaMart Mobile number"))
        self.label_2.setText(_translate("MainWindow", "IndiaMart Password"))
        self.label_3.setText(_translate("MainWindow", "Keyword"))
        self.label_4.setText(_translate("MainWindow", "Location"))
        self.Result.setText(_translate("MainWindow", "Get Result"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Business Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Address"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Pincode"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Mobile Number"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Website"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionsave.setText(_translate("MainWindow", "save"))
        self.Result.setText(_translate("MainWindow", "Execute"))
        

        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    valueChanged = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.valueChanged.connect(self.on_value_changed)
        self.Result.clicked.connect(self.on_clicked)
        self.Save.clicked.connect(self.export)

    @QtCore.pyqtSlot()
    def on_clicked(self):
        threading.Thread(target=self.hello, daemon=True).start()
        
    @QtCore.pyqtSlot(list)
    def on_value_changed(self, value):
#         self.textEdit.append("Business Name: {}".format(value[0]))
#         self.textEdit.append("Address: {}".format(value[1]))
#         self.textEdit.append("Pincode: {}".format(value[2]))
#         self.textEdit.append("Phone Number: {}".format(value[3]))
#         self.textEdit.append("Website: {}".format(value[4]))
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)
        # Add text to the row
        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(value[0]))
        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(value[1]))
        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(value[2]))
        self.tableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(value[3]))
        self.tableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(value[4]))

    
    
    def open_indiamart(self):
        query = "List of" +" "+  self.keyword +" " + "in"+" "+  self.location +" " +"indiamart"
        print(query)
        for url in search(query, tld="com", num=1, stop=1, pause=2):
            browser.get(url)
            browser.maximize_window()
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             sleep(10)

    def login_indiamart(self):
        login = browser.find_elements_by_xpath('//*[@id="lshead"]')[0]
        sleep(4)
        login.click()
        sleep(4)    
        input_box = browser.find_element_by_xpath('//*[@id="mobile"]')
        input_box.send_keys(self.your_num)
        input_box.send_keys(Keys.ENTER)
        sleep(10)
        
    def fetch_indiamart(self):
        sleep(8)
        try:

            button = browser.find_elements_by_xpath('//span[text()=" Show More Results "]')
            button[0].click()
            sleep(7)
            password = browser.find_elements_by_xpath('//*[@id="passwordbtn1"]')[1]
            password.click()
            sleep(4)
            input_box = browser.find_element_by_xpath('//*[@id="usr_pass"]')
            input_box.send_keys(self.pwd)
            input_box.send_keys(Keys.ENTER)
            sleep(5)

            while True:
                sleep(6)
                try:
                    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Show More Results "]'))).click()
                    sleep(12)
                except TimeoutException:
                    break

        except:
            pass
    
    def extract_indiamart(self):
        
    
        Busi_name= browser.find_elements_by_class_name("lcname")
        for c in range(len(Busi_name)):
#             
            sleep(1)
            try:
                Business_name = browser.find_elements_by_class_name("lcname")[c]
                pata=Business_name.get_attribute("innerHTML")


            except:
                Business_name = None
            if Business_name is not None:
                B_name.append(pata)
            else:
                B_name.append(None)
            sleep(1)
            try:
                web = browser.find_elements_by_class_name("r-cl")[c].find_elements_by_tag_name('a')[0]
                webji=web.get_attribute("href")
                Web_link.append(webji)



            except:
                web = browser.find_elements_by_class_name("lcname")[c]
                webji=web.get_attribute("href")
                Web_link.append(webji)



            sleep(1)    
            try:
                sleep(1)
                address =browser.find_elements_by_class_name("to-txt")[c]
                location=address.get_attribute("innerHTML")
            except:
                address=None
            if address is not None:
                Address_name.append(location)
                try:

                    pin_code=reg.findall(location)[0]
                    PINCODE.append(pin_code)
                except:
                    PINCODE.append(None)
            else:
                Address_name.append(None)
                PINCODE.append(None)
            sleep(1)
            try:

                Moobile_num =browser.find_elements_by_class_name("pns_h")[c]
                Phone_num=Moobile_num.get_attribute("innerHTML")

            except:
                Moobile_num=None
            if Moobile_num is not None:

                mbl_num.append(Phone_num)
            else:
                mbl_num.append(None)
            df = pandas.DataFrame({'Business Name':B_name,'Address':Address_name,'Pincode':PINCODE,'Phone Number':mbl_num,'Website':Web_link})
            row=df.iloc[c].T
            new_row=[row[0],row[1],row[2],row[3],row[4]]
#             self.table()
            self.valueChanged.emit(new_row)
#             self.table()
#             print(row[0])
#             print(row[1])
#             print(row[2])
#             print(row[3])
#             print(row[4])
#             print("--------------------------------------------------")
            
#             numRows = self.tableWidget.rowCount()
#             self.tableWidget.insertRow(numRows)
#             # Add text to the row
#             self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(row[0]))
#             self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(row[1]))
#             self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(row[2]))
#             self.tableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(row[3]))
#             self.tableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(row[4]))
        self.new_df=df
        
        
#     def table(self):
        
#         numRows = self.tableWidget.rowCount()
#         self.tableWidget.insertRow(numRows)
#         # Add text to the row
#         self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(self.row[0]))
#         self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(self.row[1]))
#         self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(self.row[2]))
#         self.tableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(self.row[3]))
#         self.tableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(self.row[4]))
        


    
    def hello(self):
        self.your_num=self.mobile.text()
        self.pwd=self.password.text()
        self.keyword=self.keyword.text()
        self.location=self.location.text()
        print("Thank you")
        print("Work in progress")
        print(self.your_num)
        print(self.pwd)
        print(self.keyword)
        print(self.location)
        self.open_indiamart()
#         self.login_indiamart()
#         self.fetch_indiamart()
        print("Half work completed")
        self.extract_indiamart()
    
    def export(self):
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self, 'Select an awesome directory')
        print(foo_dir)
        print(self.new_df)
        file_path=foo_dir+'/dataji.csv'
        print(file_path)
        self.new_df.to_csv(file_path, index=False)
        
if __name__ == "__main__":
    import sys
#     self.your_num=input("Mobile")
#     self.pwd=input("password")
#     self.keyword=input("keyword")
#     self.location=input("location")

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())