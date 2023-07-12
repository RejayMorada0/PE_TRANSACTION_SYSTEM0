
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QLCDNumber, QMessageBox
from PyQt5.QtCore import QTimer, QTime, QPropertyAnimation, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import sys
from datetime import datetime
import time

#for matrix list
from numpy import *

#for scanner
import cv2
import numpy as np
from pyzbar.pyzbar import decode

#CURRENT TIME AND DATE
now = datetime.now()
#DATE
date = now.strftime("%m | %d | %Y")
#DAY IN A WEEK
day = now.strftime("%A")
#lIST KO
list = []
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('design.ui', self)
        self.show()
        self.setWindowTitle("Physical Education System Modernization Software")
        self.setWindowIcon(QtGui.QIcon('green.png'))
        self.pushButton_4.setStyleSheet("background-color: rgb(237, 119, 39);")
           
        #LOGIN BUTTONS
            #login button
        self.pushButton.clicked.connect(self.logins)
            #Exit button
        self.pushButton_13.clicked.connect(self.exit)
            #show password button
        self.pushButton_2.clicked.connect(self.showpass)
            #hide password button
        self.pushButton_3.hide()
        self.pushButton_3.clicked.connect(self.hidepass)
            #Label = "password is required"
        self.label_4.hide()
            #Line Edit enter password
        self.lineEdit.returnPressed.connect(self.logins)

        #HOME PAGE BUTTONS
            #enable password
        self.pushButton_10.clicked.connect(self.enablepass)
            #disabled button
        self.pushButton_11.clicked.connect(self.disabled)
        self.pushButton_11.hide()
            #change password button
        self.pushButton_12.clicked.connect(self.changepass)
        self.pushButton_12.hide()
            #side bar buttons
                #more button
        self.pushButton_5.clicked.connect(self.more)
                #home button
        self.pushButton_4.clicked.connect(self.home)
                #uniform buttons
        self.pushButton_6.clicked.connect(self.uniforms)
                #equipment button
        self.pushButton_7.clicked.connect(self.equipment)
                #facilities button
        self.pushButton_8.clicked.connect(self.facilities)
                #logout button
        self.pushButton_9.clicked.connect(self.logout)
            #labels
        self.label_12.hide()
                #date
        self.label_40.setText(date)
                #day
        self.label_41.setText(day)
            #TIME WITH TIMER
        timer = QTimer(self)
        timer.timeout.connect(self.timedisplay)
        timer.start(1000)
        self.timedisplay()
        

        #ENABLE PASSWORD BUTTONS
            #PASSWORD
        self.pushButton_14.clicked.connect(self.showpassword1)
        self.pushButton_16.clicked.connect(self.hidepassword1)
            #CONFIRM PASSWORD
        self.pushButton_17.clicked.connect(self.hidepassword2)
        self.pushButton_15.clicked.connect(self.showpassword2)
            #CANCEL AND CONFIRM
        self.pushButton_19.clicked.connect(self.cancel)
        self.pushButton_18.clicked.connect(self.confirm)
        self.lineEdit_2.returnPressed.connect(self.confirm)
        self.lineEdit_3.returnPressed.connect(self.confirm)
        self.pushButton_16.hide()
        self.pushButton_17.hide()
        self.label_19.hide()
        self.label_20.hide()
        self.label_24.hide()
        

        #DISABLE PASSWORD BUTTONS
        
        self.pushButton_20.clicked.connect(self.disshowpass)
        self.pushButton_22.clicked.connect(self.dishidepass)
        self.pushButton_21.clicked.connect(self.disconfirm)
        self.lineEdit_4.returnPressed.connect(self.disconfirm)
        self.pushButton_23.clicked.connect(self.discancel)
        self.pushButton_22.hide()
        self.label_28.hide()

        #CHANGE PASSWORD BUTTONS
            #CONFIRM and CANCEL
        self.pushButton_24.clicked.connect(self.confirmchange)
        self.lineEdit_5.returnPressed.connect(self.confirmchange)
        self.lineEdit_6.returnPressed.connect(self.confirmchange)
        self.lineEdit_7.returnPressed.connect(self.confirmchange)
        self.pushButton_25.clicked.connect(self.cancelchange)
            #DEFAULT PASSWORD
        self.pushButton_26.clicked.connect(self.showpc1)
        self.pushButton_29.clicked.connect(self.hidepc1)
            #NEW PASSWORD
        self.pushButton_27.clicked.connect(self.showpc2)
        self.pushButton_30.clicked.connect(self.hidepc2)
            #CONFIRM PASSWORD
        self.pushButton_28.clicked.connect(self.showpc3)
        self.pushButton_31.clicked.connect(self.hidepc3)
            #LABELS
        self.label_36.hide()
        self.label_37.hide()
        self.label_38.hide()
            #PUSHBUTTONS
        self.pushButton_29.hide()
        self.pushButton_30.hide()
        self.pushButton_31.hide()

        #PE UNIFORM - ORDER BUTTONS
            #PRICES
        self.pushButton_35.clicked.connect(self.scancode)
        self.pushButton_32.clicked.connect(self.prices)
            #PENDING
        self.pushButton_34.clicked.connect(self.pending)
            #SUMMARY
        self.pushButton_33.clicked.connect(self.summary)
            #PAY
        self.pushButton_36.clicked.connect(self.pay)
            #PRINT RECEIPT
        self.pushButton_37.clicked.connect(self.printreceipt)
        #list for printing the receipt
        self.receipt = array([["testing", "testing"]])
        #refresh list for printing the receipt
        self.receiptRefresh = array([["testing", "testing"]])


        #UPDATE PRICE BUTTONS
            #UPDATE PRICE
        self.pushButton_43.clicked.connect(self.updateprice)
        #matrix list for our items and price in pe order 
        self.priceKeeper = array([["testing","testing"], ['XS - TSHIRT', '100'],['S - TSHIRT', '100'], 
            ['M - TSHIRT', '100'], ['L - TSHIRT', '100'], ['XL - TSHIRT', '100'],
            [  'XXL - TSHIRT', '100'], ['XS - PANTS', '100'], ['S - PANTS', '100'],
            ['M - PANTS', '100'], ['L - PANTS', '100'], ['XL - PANTS', '100'],
            ['XXL - PANTS', '100'],['NOT AVAIL', '0']])
        #method for displaying the priceKeeper List
        self.tableWidget_4.setRowCount(len(self.priceKeeper) - 1)
        row = 0
        for y in range(1,len(self.priceKeeper)):
            n = 0
            for x in self.priceKeeper[int(y)]:
                if n==0:
                    self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                else :
                    self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                n+=1
            row +=1


            #GO BACK
        self.pushButton_44.clicked.connect(self.goback)

        #PENDING BUTTONS
            #RECEIVED
        self.pushButton_50.clicked.connect(self.receiveduniform)
            #SCAN QRCODE
        self.pushButton_46.clicked.connect(self.scancode)
            #BATCH 1
        self.pushButton_45.clicked.connect(self.batch1)
            #BATCH 2
        self.pushButton_47.clicked.connect(self.batch2)
            #BATCH 3
        self.pushButton_48.clicked.connect(self.batch3)
            #BATCH 4
        self.pushButton_49.clicked.connect(self.batch4)
            #SCAN QRCODE
        self.pushButton_51.clicked.connect(self.backtoordering)
            #REFRESH 
        self.pushButton_52.clicked.connect(self.startNewTable)
        #matrix list for refreshing the preOrder List
        self.refreshList = array([["testing", "testing", "testing", "testing", "testing","testing", "testing"]])
        #different matrix list to transfer per batch the sets in matrix list
        self.preOrderList = array([["testing", "testing", "testing", "testing", "testing","testing", "testing"]])
        self.pendingOrderList = array([["testing", "testing", "testing", "testing", "testing", "testing", "testing"]])
        self.pendingOrderList_1 = array([["testing", "testing", "testing", "testing", "testing","testing", "testing"]])
        self.pendingOrderList_2 = array([["testing", "testing", "testing", "testing", "testing","testing", "testing"]])
        self.pendingOrderList_3 = array([["testing", "testing", "testing", "testing", "testing","testing", "testing"]])



        #EQUIPMENT CATALOG - BORROW
            #BACK TO ORDERING
        self.pushButton_38.clicked.connect(self.scancode)
            #BORROW
        self.pushButton_39.clicked.connect(self.borrow)
            #RETURNED
        self.pushButton_40.clicked.connect(self.returned)
            #SEARCH
        self.pushButton_41.clicked.connect(self.search)
        self.list = array([["testing","testing","testing","testing"]])
        self.list2 = []

        #SEARCH VALIDATOR

        model = QStandardItemModel(len(self.list2), 1)
        filtersearch = QSortFilterProxyModel()
        filtersearch.setSourceModel(model)
        filtersearch.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filtersearch.setFilterKeyColumn(0)
        self.lineEdit_10.textChanged.connect(filtersearch.setFilterRegExp)
        
        

        #FACILITY RESERVATION - RESERVE BUTTON
        self.pushButton_42.clicked.connect(self.schedule)
        #matrix list for our items and status in reserve facility
        self.reserveF = array( [ ["testing", "testing", "testing", "testing", "testing"]])
        
        

    
    
    #LOGIN FUNCTIONS
    def showpass(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit.echoMode()==hide and self.lineEdit.text() is not empty:
            self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_3.show()
            self.pushButton_2.hide()
            self.label_4.hide()

        else:
            print("empty")
            self.label_4.hide()

    def hidepass(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit.echoMode()==shown and self.lineEdit.text() is not empty:
            self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_2.show()
            self.pushButton_3.hide()
            self.label_4.hide()

        else:
            print("empty")
            self.label_4.hide()
    
    def logins(self):
        empty = ''
        a = list[0]

        if self.lineEdit.text()==empty:
            self.label_4.show()

        if self.lineEdit.text()!= a:
            self.label_4.setText("Wrong Password")
            self.label_4.show()     

        else:
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_2.setCurrentIndex(0)
            self.lineEdit.clear()
            self.label_4.hide()
            print(list)
            

    def exit(self):
        self.message()

    #HOME MENUS
    def enablepass(self):
        self.stackedWidget_2.setCurrentIndex(5)
        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.pushButton_8.hide()
        self.pushButton_9.hide()
    def changepass(self):
        self.stackedWidget_2.setCurrentIndex(7)
        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.pushButton_8.hide()
        self.pushButton_9.hide()
    def home(self):
        self.stackedWidget_2.setCurrentIndex(0)
        self.pushButton_4.setStyleSheet("background-color: rgb(237, 119, 39);")
        self.pushButton_6.setStyleSheet("background-color: transparent")
        self.pushButton_7.setStyleSheet("background-color: transparent")
        self.pushButton_8.setStyleSheet("background-color: transparent")
    def uniforms(self):
        self.stackedWidget_2.setCurrentIndex(1)
        self.pushButton_4.setStyleSheet("background-color: transparent")
        self.pushButton_6.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.pushButton_7.setStyleSheet("background-color: transparent")
        self.pushButton_8.setStyleSheet("background-color: transparent")
    def equipment(self):
        self.stackedWidget_2.setCurrentIndex(2)
        self.pushButton_4.setStyleSheet("background-color: transparent")
        self.pushButton_6.setStyleSheet("background-color: transparent")
        self.pushButton_7.setStyleSheet("background-color: rgb(255, 201, 38);")
        self.pushButton_8.setStyleSheet("background-color: transparent")
    def facilities(self):
        self.stackedWidget_2.setCurrentIndex(3)
        self.pushButton_4.setStyleSheet("background-color: transparent")
        self.pushButton_6.setStyleSheet("background-color: transparent")
        self.pushButton_7.setStyleSheet("background-color: transparent")
        self.pushButton_8.setStyleSheet("background-color: rgb(120, 72, 120);")
    def logout(self):
        self.pushButton_4.setStyleSheet("background-color: transparent")
        self.pushButton_6.setStyleSheet("background-color: transparent")
        self.pushButton_7.setStyleSheet("background-color: transparent")
        self.pushButton_8.setStyleSheet("background-color: transparent")
        self.message()

    def timedisplay(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        self.lcdNumber.display(text)
        
    def more(self):
        width = self.frame_2.width()

        if width == 60:
            self.frame_2.setMinimumSize(QtCore.QSize(250, 0))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/back/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton.setIcon(icon)


        else:
            self.frame_2.setMinimumSize(QtCore.QSize(60, 0))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/moreicon/more.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton.setIcon(icon)

    #ENABLE PASSWORD
    def showpassword1(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit_2.echoMode()==hide and self.lineEdit_2.text() is not empty:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_14.hide()
            self.pushButton_16.show()
            

        else:
            print("empty")
        

    def hidepassword1(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit_2.echoMode()==shown and self.lineEdit_2.text() is not empty:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_16.hide()
            self.pushButton_14.show()

        else:
            print("empty")


    def showpassword2(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit_3.echoMode()==hide and self.lineEdit_3.text() is not empty:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_17.show()
            self.pushButton_15.hide()

        else:
            print("empty")


    def hidepassword2(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit_3.echoMode()==shown and self.lineEdit_3.text() is not empty:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_15.show()
            self.pushButton_17.hide()

        else:
            print("empty")
    

    def confirm(self):
        empty = ''
        a = str(self.lineEdit_3.text())
        
        if self.lineEdit_2.text() is not empty and self.lineEdit_3.text()==empty:
            self.label_20.show()
            self.label_19.hide()
            self.label_24.hide()
            
        elif self.lineEdit_2.text()==empty and self.lineEdit_3.text() is not empty:
            self.label_19.show()
            self.label_20.hide()
            self.label_24.hide()

        elif (self.lineEdit_2.text() and self.lineEdit_3.text()) is empty:
            self.label_19.show()
            self.label_20.show()
            self.label_24.hide()

        elif self.lineEdit_2.text() != self.lineEdit_3.text():
            self.label_19.hide()
            self.label_20.hide()
            self.label_24.show()
            

        else:
            self.label_19.hide()
            self.label_20.hide()
            self.label_24.hide()
            self.messagepassword()
            self.stackedWidget.setCurrentIndex(0)
            self.pushButton_12.show()
            self.pushButton_11.show()
            self.label_12.show()
            self.pushButton_10.hide()
            list.append(a)  
            self.textfile()
            self.lineEdit_3.clear()
            self.lineEdit_2.clear()
            self.pushButton_5.show()
            self.pushButton_4.show()
            self.pushButton_6.show()
            self.pushButton_7.show()
            self.pushButton_8.show()
            self.pushButton_9.show()
            print(list)


    def cancel(self):
        self.messagecancel()
        

    #DISABLE FUNCTIONS
    def disabled(self):
        self.stackedWidget_2.setCurrentIndex(6)
        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.pushButton_8.hide()
        self.pushButton_9.hide()

    def disconfirm(self):
        empty = ''
        a = list[0]
        if self.lineEdit_4.text() is empty:
            self.label_28.show()
            
        if self.lineEdit_4.text()!=a:
            self.label_28.show()

        else:
            self.label_28.hide()
            self.messagedisable()
            print(list)

            
    def disshowpass(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit_4.echoMode()==hide and self.lineEdit_4.text() is not empty:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_20.hide()
            self.pushButton_22.show()
            self.label_28.hide()

        else:
            print("empty")
            

    def dishidepass(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit_4.echoMode()==shown and self.lineEdit_4.text() is not empty:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_22.hide()
            self.pushButton_20.show()
            self.label_28.hide()

        else:
            
            print("empty")

    def discancel(self):
        self.messagecancel()
        


    #.TXT FILE
    def textfile(self):
        outfile = open("data.txt", "w")
        a = list[0]

        outfile.write(a)
        outfile.close()

    #CHANGE PASSWORD FUNCTIONS
    def confirmchange(self):
        empty = ''
        a = str(self.lineEdit_5.text()) #default
        b = str(self.lineEdit_6.text()) #new
        c = str(self.lineEdit_7.text()) #confirm
        d = list[0]
        

        if a==empty and b==empty and c==empty:
            self.label_36.show()
            self.label_37.show()
            self.label_38.show()

        elif a!=empty and b!=empty and c==empty:
            self.label_36.hide()
            self.label_37.hide()
            self.label_38.show()
        elif a!=empty and b==empty and c!=empty:
            self.label_36.hide()
            self.label_37.show()
            self.label_38.hide()

        elif a==empty and b!=empty and c!=empty:
            self.label_36.show()
            self.label_37.hide()
            self.label_38.hide()
        elif a!=empty and b==empty and c==empty:
            self.label_36.hide()
            self.label_37.show()
            self.label_38.show()
        
        elif a==empty and b!=empty and c==empty:
            self.label_36.show()
            self.label_37.hide()
            self.label_38.show()

        elif a==empty and b==empty and c!=empty:
            self.label_36.show()
            self.label_37.show()
            self.label_38.hide()

        elif a!=d and b!=c:
            self.label_36.show()
            self.label_37.hide()
            self.label_38.show()
        
        elif a==d and b!=c:
            self.label_36.hide()
            self.label_37.hide()
            self.label_38.show()

        elif a!=d and b==c:
            self.label_36.show()
            self.label_37.hide()
            self.label_38.hide()
        
        
        else:
            self.label_36.hide()
            self.label_37.hide()
            self.label_38.hide()
            self.messagechange()
            self.stackedWidget.setCurrentIndex(0)
            list.pop(0)
            list.append(c)
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
            self.pushButton_5.show()
            self.pushButton_4.show()
            self.pushButton_6.show()
            self.pushButton_7.show()
            self.pushButton_8.show()
            self.pushButton_9.show()
            print(list)


    def cancelchange(self):
        self.messagecancel()
        
        #DEFAULT PASSWORD
    def showpc1(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit_5.echoMode()==hide and self.lineEdit_5.text() is not empty:
            self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_26.hide()
            self.pushButton_29.show()
            self.label_36.hide()

        else:
            print("empty")

    def hidepc1(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit_5.echoMode()==shown and self.lineEdit_5.text() is not empty:
            self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_26.show()
            self.pushButton_29.hide()
            self.label_36.hide()


        else:
            print("empty")
            
        #NEW PASSWORD
    def showpc2(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit_6.echoMode()==hide and self.lineEdit_6.text() is not empty:
            self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_27.hide()
            self.pushButton_30.show()
            self.label_37.hide()

        else:
            print("empty")
    def hidepc2(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit_6.echoMode()==shown and self.lineEdit_6.text() is not empty:
            self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_27.show()
            self.pushButton_30.hide()
            self.label_37.hide()


        else:
            print("empty")
        #CONFIRM PASSWORD
    def showpc3(self):
        hide = QtWidgets.QLineEdit.Password
        empty = ''

        if self.lineEdit_7.echoMode()==hide and self.lineEdit_7.text() is not empty:
            self.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_28.hide()
            self.pushButton_31.show()
            self.label_38.hide()

        else:
            print("empty")
    def hidepc3(self):
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        if self.lineEdit_7.echoMode()==shown and self.lineEdit_7.text() is not empty:
            self.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_28.show()
            self.pushButton_31.hide()
            self.label_38.hide()

        else:
            print("empty")
    
    def message(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("font: 20pt 'Calibri';"
                                            "background-color: rgb(208, 125, 9);\n"
                                            "width: 200px;"
                                        )
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("Quit now?")
        self.msg.setWindowTitle("Logout attempt")
        returnValue = self.msg.exec()

        if returnValue == QtWidgets.QMessageBox.Yes:
            app.exit()

    def messagepassword(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("font: 20pt 'Calibri';"
                                            "background-color: rgb(208, 125, 9);\n"
                                            "width: 200px;"
                                        )
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.setText("Privacy Feature Enabled. You must now login first.")
        self.msg.setWindowTitle("Notification Update")
        self.msg.exec()

    def messagechange(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("font: 20pt 'Calibri';"
                                            "background-color: rgb(81, 238, 244);\n"
                                            "width: 200px;"
                                        )
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.setText("Successfully changed password. You must now login first.")
        self.msg.setWindowTitle("Notification Update")
        self.msg.exec()

    def messagedisenableconfirmed(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("font: 20pt 'Calibri';"
                                            "background-color: rgb(204, 145, 246);\n"
                                            "width: 200px;"
                                        )
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.setText("Successfully Disabled Password Option")
        self.msg.setWindowTitle("Notification Update")
        self.msg.exec()

    def messagedisable(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("font: 20pt 'Calibri';"
                                            "background-color: rgb(204, 145, 246);\n"
                                            "width: 200px;"
                                        )
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("Do you really want to disable privacy feature?")
        self.msg.setWindowTitle("Disable Privacy feature.")
        returnValue = self.msg.exec()

        if returnValue==QtWidgets.QMessageBox.Yes:
            self.messagedisenableconfirmed()
            self.stackedWidget_2.setCurrentIndex(0)
            self.pushButton_12.hide()
            self.pushButton_11.hide()
            self.label_12.hide()
            self.pushButton_10.show()
            list.pop(0)
            self.lineEdit_4.clear()
            print("login")
            self.pushButton_5.show()
            self.pushButton_4.show()
            self.pushButton_6.show()
            self.pushButton_7.show()
            self.pushButton_8.show()
            self.pushButton_9.show()

        elif returnValue==QtWidgets.QMessageBox.Cancel:
            self.stackedWidget_2.setCurrentIndex(6)
            print("quit")

        

    def messagecancel(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet(
           
            "font: 20pt 'Calibri';"
                                            "background-color: rgb(200, 55, 74);\n"
                                            "width: 200px;"
                                        )
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("You will lose your progress. Do you really want to cancel?")
        self.msg.setWindowTitle("Cancel Attempt")
        returnValue = self.msg.exec()

        if returnValue == QtWidgets.QMessageBox.Yes:
            self.stackedWidget_2.setCurrentIndex(0)
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()

            self.pushButton_5.show()
            self.pushButton_4.show()
            self.pushButton_6.show()
            self.pushButton_7.show()
            self.pushButton_8.show()
            self.pushButton_9.show()

        elif returnValue == QtWidgets.QMessageBox.Cancel:
            self.pushButton_5.hide()
            self.pushButton_4.hide()
            self.pushButton_6.hide()
            self.pushButton_7.hide()
            self.pushButton_8.hide()
            self.pushButton_9.hide()    
       
    #PE UNIFORM FUNCTIONS AND TRANSITIONS
    def prices(self):
        self.stackedWidget_2.setCurrentIndex(4)
        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.pushButton_8.hide()
        self.pushButton_9.hide()
    def pending(self):
        self.stackedWidget_2.setCurrentIndex(8)
        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.pushButton_8.hide()
        self.pushButton_9.hide()
    def summary(self):
        stat = "PRE-ORDER"
        stat_2 = "PENDING ORDER"
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        
        msgBox.setText("ARE YOU REALLY SURE TO RESET AND GENERATE ORDER SUMMARY? \
                        EVERY LIST ON THIS TABLE WILL BE TRANSFER IN PENDING ORDER BATCH.")
        msgBox.setStyleSheet(
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            #refresh table
            if len(self.preOrderList) <= 1:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("PRE-ORDER LIST ARE EMPTY.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()
            elif len(self.pendingOrderList) <= 1:
                self.pendingOrderList = self.preOrderList.copy()
                #find using linear search
                for w in range(1,len(self.pendingOrderList)):
                    o = (self.pendingOrderList[w][0])
                    n = (self.pendingOrderList[w][1])
                    m = (self.pendingOrderList[w][2])
                    l = (self.pendingOrderList[w][3])
                    z = (self.pendingOrderList[w][4])
                    y = (self.pendingOrderList[w][5])
                    x = (self.pendingOrderList[w][6])
                    if x == stat :
                        self.pendingOrderList[w] = [str(o), str(n), str(m), str(l),str(z), str(y), str(stat_2)]
                        self.tableWidget_5.clearContents()
                        self.tableWidget_5.setRowCount(len(self.pendingOrderList) - 1)
                        row = 0
                        for y in range(1,len(self.pendingOrderList)):
                            n = 0
                            for x in self.pendingOrderList[int(y)]:
                                if n==0:
                                    self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget_5.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget_5.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget_5.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget_5.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget_5.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
                    
                        #refresh table
                        self.preOrderList = self.refreshList.copy()
                        self.tableWidget.clearContents()
                        self.tableWidget.setRowCount(len(self.preOrderList) - 1)
                        row = 0
                        for y in range(1,len(self.preOrderList)):
                            n = 0
                            for x in self.preOrderList[int(y)]:
                                if n==0:
                                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
            elif len(self.pendingOrderList_1) <= 1:
                self.pendingOrderList_1 = self.preOrderList.copy()
                #find using linear search
                for w in range(1,len(self.pendingOrderList_1)):
                    o = (self.pendingOrderList_1[w][0])
                    n = (self.pendingOrderList_1[w][1])
                    m = (self.pendingOrderList_1[w][2])
                    l = (self.pendingOrderList_1[w][3])
                    z = (self.pendingOrderList_1[w][4])
                    y = (self.pendingOrderList_1[w][5])
                    x = (self.pendingOrderList_1[w][6])
                    if x == stat :
                        self.pendingOrderList_1[w] = [str(o), str(n), str(m), str(l),str(z), str(y), str(stat_2)]
                        self.tableWidget_6.clearContents()
                        self.tableWidget_6.setRowCount(len(self.pendingOrderList_1) - 1)
                        row = 0
                        for y in range(1,len(self.pendingOrderList_1)):
                            n = 0
                            for x in self.pendingOrderList_1[int(y)]:
                                if n==0:
                                    self.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget_6.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget_6.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget_6.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget_6.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget_6.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
                    
                        #refresh table
                        self.preOrderList = self.refreshList.copy()
                        self.tableWidget.clearContents()
                        self.tableWidget.setRowCount(len(self.preOrderList) - 1)
                        row = 0
                        for y in range(1,len(self.preOrderList)):
                            n = 0
                            for x in self.preOrderList[int(y)]:
                                if n==0:
                                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
            elif len(self.pendingOrderList_2) <= 1:
                self.pendingOrderList_2 = self.preOrderList.copy()
                for w in range(1,len(self.pendingOrderList_2)):
                    o = (self.pendingOrderList_2[w][0])
                    n = (self.pendingOrderList_2[w][1])
                    m = (self.pendingOrderList_2[w][2])
                    l = (self.pendingOrderList_2[w][3])
                    z = (self.pendingOrderList_2[w][4])
                    y = (self.pendingOrderList_2[w][5])
                    x = (self.pendingOrderList_2[w][6])
                    if x == stat :
                        self.pendingOrderList_2[w] = [str(o), str(n), str(m), str(l),str(z), str(y), str(stat_2)]
                        self.tableWidget_7.clearContents()
                        self.tableWidget_7.setRowCount(len(self.pendingOrderList_2) - 1)
                        row = 0
                        for y in range(1,len(self.pendingOrderList_2)):
                            n = 0
                            for x in self.pendingOrderList_2[int(y)]:
                                if n==0:
                                    self.tableWidget_7.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget_7.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget_7.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget_7.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget_7.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget_7.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget_7.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget_7.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
                    
                        #refresh table
                        self.preOrderList = self.refreshList.copy()
                        self.tableWidget.clearContents()
                        self.tableWidget.setRowCount(len(self.preOrderList) - 1)
                        row = 0
                        for y in range(1,len(self.preOrderList)):
                            n = 0
                            for x in self.preOrderList[int(y)]:
                                if n==0:
                                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
            elif len(self.pendingOrderList_3) <= 1:
                self.pendingOrderList_3 = self.preOrderList.copy()
                for w in range(1,len(self.pendingOrderList_3)):
                    o = (self.pendingOrderList_3[w][0])
                    n = (self.pendingOrderList_3[w][1])
                    m = (self.pendingOrderList_3[w][2])
                    l = (self.pendingOrderList_3[w][3])
                    z = (self.pendingOrderList_3[w][4])
                    y = (self.pendingOrderList_3[w][5])
                    x = (self.pendingOrderList_3[w][6])
                    if x == stat :
                        self.pendingOrderList_3[w] = [str(o), str(n), str(m), str(l),str(z), str(y), str(stat_2)]
                        self.tableWidget_8.clearContents()
                        self.tableWidget_8.setRowCount(len(self.pendingOrderList_3) - 1)
                        row = 0
                        for y in range(1,len(self.pendingOrderList_3)):
                            n = 0
                            for x in self.pendingOrderList_3[int(y)]:
                                if n==0:
                                    self.tableWidget_8.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget_8.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget_8.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget_8.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget_8.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget_8.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget_8.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
                    
                        #refresh table
                        self.preOrderList = self.refreshList.copy()
                        self.tableWidget.clearContents()
                        self.tableWidget.setRowCount(len(self.preOrderList) - 1)
                        row = 0
                        for y in range(1,len(self.preOrderList)):
                            n = 0
                            for x in self.preOrderList[int(y)]:
                                if n==0:
                                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==1:
                                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==2:
                                    self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==3:
                                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==4:
                                    self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                                elif n==5:
                                    self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
            else:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("MAXIMUM BATCHES HIT, REFRESH YOUR YEARLY BATCHES.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()
        else:
            pass

    def pay(self):
        #preorder details to get to the students
        studentDetail = self.lineEdit_8.text().upper()
        uniCombo = self.comboBox.currentText()
        uniSpin = self.spinBox.value()
        pantsCombo = self.comboBox_2.currentText()
        pantsSpin = self.spinBox_2.value()
        cash = self.spinBox_3.text().upper()
        stat = "PRE-ORDER"

        #find the value of uniCombo & linear search
        if len(studentDetail) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE FILL OUT THE STUDENT DETAILS OR SCAN ID.")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        elif (str(uniCombo) or str(pantsCombo)) == "NOT AVAIL":
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("BOTH NOT AVAIL UNIFORM AND PANTS CAN'T PROCEED.")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        elif (int(uniSpin) or int(pantsSpin)) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("AVAIL ATLEAT ONE, BUT 0 QUANTITY CAN'T PROCEED.")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        else:
            for index in range(1,len(self.priceKeeper)):
                m = (self.priceKeeper[index][0])
                n = (self.priceKeeper[index][1])
                if m == str(uniCombo):
                    break
            a = str(m)
            b = (int(n))

            #find the value of pantsCombo & linear search
            for index2 in range(1,len(self.priceKeeper)):
                q = (self.priceKeeper[index2][0])
                r = (self.priceKeeper[index2][1])
                if q == str(pantsCombo):
                    break
            c = str(q)
            d = (int(r))
        
            z = b * uniSpin
            y = d * pantsSpin


            #total price computation
            tp = str(z+y)
            self.label_61.setText(tp)

            #payment and change computation
            studentCash = self.spinBox_3.value()            
            if (studentCash < int(tp)) :
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("ENTER AMOUNT OF MONEY EXACT OR GREATER THAN TO THE TOTAL PRICE.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("WARNING!!!")
                self.msg.exec_()
   
            else:
                change = studentCash - (int(tp))

                #printing receipt in label
                self.textBrowser_2.setText("RECIEPT: " + "\n" + "STUDENT DETAILS: " +  str(studentDetail) + "\n" + "SIZE - UNIFORM: " + str(a) +
                "\n" + "UNIFORM QNTY: " + str(uniSpin) + "\n" + "SIZE - PANTS: " + str(c) +  "\n" + "PANTS  QNTY: " + str(pantsSpin) 
                +"\n" + "TOTAL PRICE: " + str(tp) + "\n" + "CASH: " + str(studentCash) + "\n" + "CHANGE: " + str(change))
                
               
                # add to list for printing in txt
                self.receipt = append(self.receipt, [["STUDENT DETAILS: ", str(studentDetail)]],0)
                self.receipt = append(self.receipt, [[" SIZE - UNIFORM: ", str(a)]],0) 
                self.receipt = append(self.receipt, [["SIZE - PANTS: ", str(c)]],0) 
                self.receipt = append(self.receipt, [["PANTS  QNTY: ", str(pantsSpin)]],0) 
                self.receipt = append(self.receipt, [["TOTAL PRICE: ", str(tp)]],0) 
                self.receipt = append(self.receipt, [["CASH: ", str(studentCash)]],0)
                self.receipt = append(self.receipt, [["CHANGE: ", str(change)]],0) 


                #storing in table of Pre-Order
                if len(studentDetail) == 0:
                    self.msg = QtWidgets.QMessageBox(self.centralwidget)
                    self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                    self.msg.setText("PLEASE FILL OUT THE STUDENT DETAILS OR SCAN ID.")
                    self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                    self.msg.setWindowTitle("WARNING!!!")
                    self.msg.exec_()
                elif (studentDetail) in (self.preOrderList):
                    self.msg = QtWidgets.QMessageBox(self.centralwidget)
                    self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                    self.msg.setText("PLEASE ENTER A DIFFERENT STUDENT DETAILS OR SCAN ID.")
                    self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                    self.msg.setWindowTitle("WARNING!!!")
                    self.msg.exec_()
                else:
                    #appends the new account to matrix
                    self.preOrderList = append(self.preOrderList, [[studentDetail, uniCombo, uniSpin, pantsCombo, pantsSpin, tp, str(stat)]],0)
                    #refresh table
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(len(self.preOrderList) - 1)
                    row = 0
                    for y in range(1,len(self.preOrderList)):
                        n = 0
                        for x in self.preOrderList[int(y)]:
                            if n==0:
                                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                            elif n==1:
                                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                            elif n==2:
                                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                            elif n==3:
                                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                            elif n==4:
                                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                            elif n==5:
                                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                            else:
                                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                            n+=1
                        row +=1        
                    self.msg = QtWidgets.QMessageBox(self.centralwidget)
                    self.msg.setIcon(QtWidgets.QMessageBox.Information)
                    self.msg.setText("PRE-ORDER SUCCESUL")
                    self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                    self.msg.setWindowTitle("INFORMATION")
                    self.msg.exec_()

    def printreceipt(self):
        if len(self.receipt) <= 1:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("SORRY, RECEIPT IS EMPTY.")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()
        else:
            # Displaying the array
            print('Array:\n', self.receipt)
            file = open("file1.txt", "w+")

            # Saving the 2D array in a text file
            content = str(self.receipt)
            file.write(content)
            file.close()

            # Displaying the contents of the text file
            file = open("file1.txt", "r")
            content = file.read()

            print("\nContent in file1.txt:\n", content)
            file.close()
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("PRINT RECEIPT IS IN THE file1.txt.")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()

            self.receipt = self.receiptRefresh.copy()
            print(self.receiptRefresh)
        pass

    #CHANGE PRICES FUNCTIONS AND TRANSITIONS
    def updateprice(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("DO YOU REALLY WANT TO CHANGE THE PRICE OF THIS ITEM?")
        self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            typeOfOrder = self.comboBox_5.currentText()
            changeThePrice = self.lineEdit_14.text().upper()
            #to avoid error
            if len(changeThePrice) == 0:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("PLEASE ENTER  AMOUNT OF PRICE TO CHANGE.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()
            elif changeThePrice.isalpha():
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("PLEASE ENTER NUMBER TO CHANGE THE PRICE AMOUNT.")
                self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()
            else:
                #find price
                for o in range(1,len(self.priceKeeper)):
                    m = (self.priceKeeper[o][0])
                    if m == str(typeOfOrder):
                        #update the matrix
                        self.priceKeeper[o] = [str(typeOfOrder), str(changeThePrice)]
                        #refresh table
                        self.tableWidget_4.clearContents()
                        self.tableWidget_4.setRowCount(len(self.priceKeeper) - 1)
                        row = 0
                        for y in range(1,len(self.priceKeeper)):
                            n = 0
                            for x in self.priceKeeper[int(y)]:
                                if n==0:
                                    self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                                else:
                                    self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                                n+=1
                            row +=1
                        self.msg = QtWidgets.QMessageBox(self.centralwidget)
                        self.msg.setIcon(QtWidgets.QMessageBox.Information)
                        self.msg.setText("SUCCESSFULLY CHANGE THE PRICE AMOUNT.")
                        self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                        self.msg.setWindowTitle("INFORMATION")
                        self.msg.exec_()
        else:
            pass

    def goback(self):
        self.stackedWidget_2.setCurrentIndex(1)
        self.pushButton_5.show()
        self.pushButton_4.show()
        self.pushButton_6.show()
        self.pushButton_7.show()
        self.pushButton_8.show()
        self.pushButton_9.show()

    #PENDING FUNCTIONS AND TRANSITIONS
    def receiveduniform(self):
        receiverName = self.lineEdit_13.text().upper()
        stat_3 = "RECIEVED ORDER: " + (str(datetime.now()))

        #to avoid error
        if len(receiverName) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE ENTER THE RECEIVER'S NAME.")
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif (receiverName not in self.pendingOrderList) and (receiverName not in self.pendingOrderList_1) and (receiverName not in self.pendingOrderList_2) and (receiverName not in self.pendingOrderList_3):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("STUDENT DETAILS HAVE NO RECORDS ON ORDER OF PE UNIFORM.")
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif receiverName in (self.pendingOrderList):
            #find the name of RECEIVER'S NAME
            for g in range(1,len(self.pendingOrderList)):
                m = (self.pendingOrderList[g][0])
                if m == str(receiverName):
                    z = (self.pendingOrderList[g][0])
                    y = (self.pendingOrderList[g][1])
                    x = (self.pendingOrderList[g][2])
                    w = (self.pendingOrderList[g][3])
                    v = (self.pendingOrderList[g][4])
                    u = (self.pendingOrderList[g][5])
                    s = (self.pendingOrderList[g][6])
          
            #update the matrix
            self.pendingOrderList[g] = [str(z), str(y), str(x), str(w), str(v), str(u), str(stat_3)]
            #refresh table
            self.tableWidget_5.clearContents()
            self.tableWidget_5.setRowCount(len(self.pendingOrderList) -1)
            row = 0
            for y in range(1,len(self.pendingOrderList)):
                n = 0
                for x in self.pendingOrderList[int(y)]:
                    if n==0:
                        self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_5.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_5.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_5.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==5:
                        self.tableWidget_5.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_5.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row+=1
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("SUCCESSFULLY RECEIVED THE ORDER IN BATCH 1.")
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()

        elif receiverName in (self.pendingOrderList_1):
            #find the name of RECEIVER'S NAME
            for g in range(1,len(self.pendingOrderList_1)):
                m = (self.pendingOrderList_1[g][0])
                if m == str(receiverName):
                    z = (self.pendingOrderList_1[g][0])
                    y = (self.pendingOrderList_1[g][1])
                    x = (self.pendingOrderList_1[g][2])
                    w = (self.pendingOrderList_1[g][3])
                    v = (self.pendingOrderList_1[g][4])
                    u = (self.pendingOrderList_1[g][5])
                    s = (self.pendingOrderList_1[g][6])
           
          

            #update the matrix
            self.pendingOrderList_1[g] = [str(z), str(y), str(x), str(w), str(v), str(u), str(stat_3)]
            #refresh table
            self.tableWidget_6.clearContents()
            self.tableWidget_6.setRowCount(len(self.pendingOrderList_1) -1)
            row = 0
            for y in range(1,len(self.pendingOrderList_1)):
                n = 0
                for x in self.pendingOrderList_1[int(y)]:
                    if n==0:
                        self.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_6.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_6.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_6.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==5:
                        self.tableWidget_6.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_6.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row+=1
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("SUCCESSFULLY RECEIVED THE ORDER BATCH 2")
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()
        
        elif receiverName in (self.pendingOrderList_2):
            #find the name of RECEIVER'S NAME
            for g in range(1,len(self.pendingOrderList_2)):
                m = (self.pendingOrderList_2[g][0])
                if m == str(receiverName):
                    z = (self.pendingOrderList_2[g][0])
                    y = (self.pendingOrderList_2[g][1])
                    x = (self.pendingOrderList_2[g][2])
                    w = (self.pendingOrderList_2[g][3])
                    v = (self.pendingOrderList_2[g][4])
                    u = (self.pendingOrderList_2[g][5])
                    s = (self.pendingOrderList_2[g][6])

            #update the matrix
            self.pendingOrderList_2[g] = [str(z), str(y), str(x), str(w), str(v), str(u), str(stat_3)]
            #refresh table
            self.tableWidget_7.clearContents()
            self.tableWidget_7.setRowCount(len(self.pendingOrderList_2) -1)
            row = 0
            for y in range(1,len(self.pendingOrderList_2)):
                n = 0
                for x in self.pendingOrderList_2[int(y)]:
                    if n==0:
                        self.tableWidget_7.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_7.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_7.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_7.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_7.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==5:
                        self.tableWidget_7.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_7.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row+=1
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("SUCCESSFULLY RECEIVED THE ORDER BATCH 3")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()

        elif receiverName in (self.pendingOrderList_3):
            #find the name of RECEIVER'S NAME
            for g in range(1,len(self.pendingOrderList_3)):
                m = (self.pendingOrderList_3[g][0])
                if m == str(receiverName):
                    z = (self.pendingOrderList_3[g][0])
                    y = (self.pendingOrderList_3[g][1])
                    x = (self.pendingOrderList_3[g][2])
                    w = (self.pendingOrderList_3[g][3])
                    v = (self.pendingOrderList_3[g][4])
                    u = (self.pendingOrderList_3[g][5])
                    s = (self.pendingOrderList_3[g][6])
               

            #update the matrix
            self.pendingOrderList_3[g] = [str(z), str(y), str(x), str(w), str(v), str(u), str(stat_3)]
            #refresh table
            self.tableWidget_8.clearContents()
            self.tableWidget_8.setRowCount(len(self.pendingOrderList_3) -1)
            row = 0
            for y in range(1,len(self.pendingOrderList_3)):
                n = 0
                for x in self.pendingOrderList_3[int(y)]:
                    if n==0:
                        self.tableWidget_8.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_8.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_8.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_8.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_8.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==5:
                        self.tableWidget_8.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_8.setItem(row, 6, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row+=1
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("SUCCESSFULLY RECEIVED THE ORDER BATCH 4")
            self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()
        else:
            pass

    def batch1(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("DO YOU WANT TO PRINT PENDING ORDER IN BATCH 1?")
        msgBox.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            if len(self.pendingOrderList) <= 1:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SORRY, BATCH 1 IS EMPTY.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
            else:
                # Displaying the array
                print('Array:\n', self.pendingOrderList)
                file = open("BATCH1.txt", "w+")

                # Saving the 2D array in a text file
                content = str(self.pendingOrderList)
                file.write(content)
                file.close()

                # Displaying the contents of the text file
                file = open("BATCH1.txt", "r")
                content = file.read()

                print("\nContent in BATCH1.txt:\n", content)
                file.close()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("PRINT THIS BATCH IS PROCESSING, BUT FOR NOW CHECK THE FILE NAMED BATCH1.txt.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
        else:
            pass
    def batch2(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("DO YOU WANT TO PRINT PENDING ORDER IN BATCH 2?")
        msgBox.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            if len(self.pendingOrderList_1) <= 1:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SORRY, BATCH 2 IS EMPTY.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
            else:
                # Displaying the array
                print('Array:\n', self.pendingOrderList_1)
                file = open("BATCH2.txt", "w+")

                # Saving the 2D array in a text file
                content = str(self.pendingOrderList_1)
                file.write(content)
                file.close()

                # Displaying the contents of the text file
                file = open("BATCH2.txt", "r")
                content = file.read()

                print("\nContent in BATCH2.txt:\n", content)
                file.close()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("PRINT THIS BATCH IS PROCESSING, BUT FOR NOW CHECK THE FILE NAMED BATCH2.txt.")
                self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
    def batch3(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("DO YOU WANT TO PRINT PENDING ORDER IN BATCH 3?")
        msgBox.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            if len(self.pendingOrderList_2) <= 1:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SORRY, BATCH 3 IS EMPTY.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
            else:
                # Displaying the array
                print('Array:\n', self.pendingOrderList_2)
                file = open("BATCH3.txt", "w+")

                # Saving the 2D array in a text file
                content = str(self.pendingOrderList_2)
                file.write(content)
                file.close()

                # Displaying the contents of the text file
                file = open("BATCH3.txt", "r")
                content = file.read()

                print("\nContent in BATCH3.txt:\n", content)
                file.close()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("PRINT THIS BATCH IS PROCESSING, BUT FOR NOW CHECK THE FILE NAMED BATCH3.txt.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
    def batch4(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("DO YOU WANT TO PRINT PENDING ORDER IN BATCH 4?")
        msgBox.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            if len(self.pendingOrderList_3) <= 1:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SORRY, BATCH 4 IS EMPTY.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
            else:
                # Displaying the array
                print('Array:\n', self.pendingOrderList_3)
                file = open("BATCH4.txt", "w+")

                # Saving the 2D array in a text file
                content = str(self.pendingOrderList_3)
                file.write(content)
                file.close()

                # Displaying the contents of the text file
                file = open("BATCH4.txt", "r")
                content = file.read()

                print("\nContent in BATCH4.txt:\n", content)
                file.close()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("PRINT THIS BATCH IS PROCESSING, BUT FOR NOW CHECK THE FILE NAMED BATCH4.txt.")
                self.msg.setStyleSheet(
                                            "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()

    #refresh yearly batches     
    def startNewTable(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("ARE YOU REALLY SURE TO RESET AND START NEW IN YEARLY TABLE? EVERY LIST ON EVERY BATCHCES IN TABLE WILL BE DELETED.")
        msgBox.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(85, 170, 255);"
                                        )
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            #for self.pendingOrderList
            self.pendingOrderList = self.refreshList.copy()
            self.tableWidget_5.clearContents()
            self.tableWidget_5.setRowCount(len(self.pendingOrderList) - 1)
            row = 0
            for y in range(1,len(self.pendingOrderList)):
                n = 0
                for x in self.pendingOrderList[int(y)]:
                    if n==0:
                        self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_5.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_5.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_5.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_5.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row +=1
            #for self.pendingOrderList_1
            self.pendingOrderList_1 = self.refreshList.copy()
            self.tableWidget_6.clearContents()
            self.tableWidget_6.setRowCount(len(self.pendingOrderList_1) - 1)
            row = 0
            for y in range(1,len(self.pendingOrderList_1)):
                n = 0
                for x in self.pendingOrderList_1[int(y)]:
                    if n==0:
                        self.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_6.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_6.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_6.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_6.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row +=1
            #for self.pendingOrderList_2
            self.pendingOrderList_2 = self.refreshList.copy()
            self.tableWidget_7.clearContents()
            self.tableWidget_7.setRowCount(len(self.pendingOrderList_2) - 1)
            row = 0
            for y in range(1,len(self.pendingOrderList_2)):
                n = 0
                for x in self.pendingOrderList_2[int(y)]:
                    if n==0:
                        self.tableWidget_7.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_7.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_7.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_7.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_7.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_7.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row +=1

            #for self.pendingOrderList_3
            self.pendingOrderList_3 = self.refreshList.copy()
            self.tableWidget_8.clearContents()
            self.tableWidget_8.setRowCount(len(self.pendingOrderList_3) - 1)
            row = 0
            for y in range(1,len(self.pendingOrderList_3)):
                n = 0
                for x in self.pendingOrderList_3[int(y)]:
                    if n==0:
                        self.tableWidget_8.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_8.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_8.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_8.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==4:
                        self.tableWidget_8.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_8.setItem(row, 5, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row +=1
        else:
            pass
          
    
    def backtoordering(self):
        self.stackedWidget_2.setCurrentIndex(1)
        self.pushButton_5.show()
        self.pushButton_4.show()
        self.pushButton_6.show()
        self.pushButton_7.show()
        self.pushButton_8.show()
        self.pushButton_9.show()

    #EQUIPMENT CATALOG - BORROW FUNCTIONS
    def borrow(self):
        a = self.lineEdit_9.text().upper()
        b = self.comboBox_3.currentText()
        c = str(datetime.now().strftime("%H:%M:%S / %y-%m-%d"))
        d = "not yet returned"

        #to avoid error
        if len(a) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE ENTER THE STUDENT DETAILS.")
            self.msg.setStyleSheet(
                                    "font: 20pt 'Calibri';"
                                    "background-color: rgb(32, 33, 36);\n"
                                    "width: 200px;"
                                    "color: rgb(255, 201, 38);"
                                    )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif (a in self.list):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("STUDENT DETAILS HAVE EXISTING BORROW IN RECORD, THIS TRANSACTION CAN'T BE PROCESS.")
            self.msg.setStyleSheet(
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(255, 201, 38);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        else:
            row = 0
            self.list = append(self.list, [[str(a), str(b), str(c), str(d)]],0)
            self.tableWidget_2.clearContents()
            self.tableWidget_2.setRowCount(len(self.list) - 1)
            row = 0
            for y in range(1,len(self.list)):
                n = 0
                for x in self.list[int(y)]:
                    if n==0:
                        self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row +=1

                
    def returned(self):
        a = self.lineEdit_9.text().upper()
        b = self.comboBox_3.currentText()
        c = str(datetime.now().strftime("%H:%M:%S / %y-%m-%d"))
        d = "not yet returned"
        #to avoid error
        if len(a) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE ENTER THE STUDENT DETAILS.")
            self.msg.setStyleSheet(
                                    "font: 20pt 'Calibri';"
                                    "background-color: rgb(32, 33, 36);\n"
                                    "width: 200px;"
                                    "color: rgb(255, 201, 38);"
                                    )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif (a not in self.list):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("STUDENT DETAILS HAVE NO EXISTING BORROW IN RECORD, THIS TRANSACTION CAN'T BE PROCESS.")
            self.msg.setStyleSheet(
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(255, 201, 38);"
                                        )
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        else:
            for w in range(len(self.list)):
                x = (self.list[w][0])
                y = (self.list[w][1])
                z = (self.list[w][2])
                if x == str(a) and y == str(b):
                    #Transfer search items in other table
                    self.list2.append(x + " : " + y + " : " + "time in:" + z + " : " + "time in:" + c)
                    self.textBrowser_3.setText("\n".join(self.list2))
                    print("LIST 2: ", self.list2)
                    #Delete search items in its table
                    self.list = delete(self.list, w, 0)
                    self.tableWidget_2.removeRow(w)
                    self.tableWidget_2.clearContents()
                    self.tableWidget_2.setRowCount(len(self.list) - 1)
                    row = 0
                    for k in range(1,len(self.list)):
                        n = 0
                        for s in self.list[int(k)]:
                            if n==0:
                                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(s)))
                            elif n==1:
                                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(s)))
                            elif n==2:
                                self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(s)))
                            else:
                                self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(s)))
                            n+=1
                        row +=1
                    break

    def search(self):
        print("search")

    #FACILITY RESERVATION - RESERVE FUNCTION
    def schedule(self):
        eventName = self.lineEdit_12.text().upper()
        schoolOrg = self.lineEdit_11.text().upper()
        eventDetails = str(eventName)+ " - " + str(schoolOrg)

        #Seclected Date in Calendar
        dateselected = self.calendarWidget.selectedDate()
        dateInStr = str(dateselected.toPyDate())

        #Seclected time start in TimeEdit
       
        timeStart = self.timeEdit.time().toString()

        #Seclected time end in TimeEdit
        timeEnd = self.timeEdit_2.time().toString()

        #Selected item in ComboBox 
        facility = self.comboBox_4.currentText()

        if (len(eventName) and len(schoolOrg)) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(120, 72, 120);"
                                        )
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE INPUT THE EVENT NAME AND SCHOOL ORGANIZATION THAT WANT FOR RESERVATION.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        elif (eventDetails) in self.reserveF:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(120, 72, 120);"
                                        )
            self.msg.setText("PLEASE INPUT DIFFERENT EVENT NAME AND SCHOOL ORGANIZATION THAT WANT FOR RESERVATION..")
            self.msg.setWindowTitle("WARNING!!!")
            self.msg.exec_()
        else:
            #appends the new account to matrix
            self.reserveF = append(self.reserveF, [[eventDetails, dateInStr, timeStart, timeEnd, facility]],0)
            #reselfresh table
            self.tableWidget_3.clearContents()
            self.tableWidget_3.setRowCount(len(self.reserveF) - 1)
            row = 0
            for y in range(1,len(self.reserveF)):
                n = 0
                for x in self.reserveF[int(y)]:
                    if n==0:
                        self.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==1:
                        self.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==2:
                        self.tableWidget_3.setItem(row, 2, QtWidgets.QTableWidgetItem(str(x)))
                    elif n==3:
                        self.tableWidget_3.setItem(row, 3, QtWidgets.QTableWidgetItem(str(x)))
                    else:
                        self.tableWidget_3.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x)))
                    n+=1
                row +=1
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setStyleSheet(
           
                    "font: 20pt 'Calibri';"
                                            "background-color: rgb(32, 33, 36);\n"
                                            "width: 200px;"
                                            "color: rgb(120, 72, 120);"
                                        )
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("SUCCESSFULY ENLISTED THE EVENT DETAILS OF STUDENT.")
            self.msg.setWindowTitle("WARNING!!!")

    #SCANNER FUNCTION
    def scancode(self):
        def decoder(image):
            gray_img = cv2.cvtColor(image,0)
            barcode = decode(gray_img)

            for obj in barcode:
                points = obj.polygon
                (x,y,w,h) = obj.rect
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 255, 0), 3)

                barcodeData = obj.data.decode("utf-8")
                barcodeType = obj.type
                string = "Data " + str(barcodeData)  + " | Type " + str(barcodeType)

                #setText in lineEdit
                self.lineEdit_3.setText(str(barcodeData))

                cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                print("Barcode: "+barcodeData +" | Type: "+barcodeType)

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            decoder(frame)
            cv2.imshow('Image', frame)
            code = cv2.waitKey(2)
            if code == ord('q'):
                break
            elif code == ord('s'):
                break

import images

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()