"""
Created on Mon Sep 2 13:00:47 2021

@author: sprite
"""

import hashlib
from PyQt5.uic.uiparser import QtCore
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QMainWindow, QRadioButton, QMenuBar, QMenu, QDialog
import sys
from Blockchain_func import *
import os
import checksumdir
import requests
import base64
import hashlib


class SecondUi(QMainWindow):
    def __init__(self, parent=None):
        super(SecondUi, self).__init__(parent)


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()    

    def init_ui(self):
        #UI objects
        main_window = uic.loadUi('UserInterface_Alpha.ui', self)

        #Hide QRImg
        self.lblQRImg.setHidden(True)
        #Hide txtUsername till login is required
        self.txtUsername.setHidden(True)
        #Hide txtPassword till login is required
        self.txtPassword.setHidden(True)
        #Hide txtUrl till login is required
        self.txtUrl.setHidden(True)
        #Hide lblUrl till login is required
        self.lblUrl.setHidden(True)
        #Hide btnCheck till login is required
        self.btnCheck.setHidden(True)
        #Hide lblUser till login is required
        self.lblUser.setHidden(True)
        #Hide lblPass till login is required
        self.lblPass.setHidden(True)
        #Hide btn_Run till login is confirmed
        self.btn_Run.setHidden(True)

        #Login menu button actions
        self.actionLogin_2.triggered.connect(lambda: self.loginShow(main_window))

        #CheckDetails on userBlockchain action 
        self.button_checkDetails = self.findChild(QtWidgets.QPushButton, 'btnCheck')
        self.button_checkDetails.clicked.connect(lambda: self.checkDetails(main_window))

        #Browse button actions
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.clicked.connect(lambda: self.getfile(main_window))
        self.show()

        #Add program button
        self.button_run = self.findChild(QtWidgets.QPushButton, 'btn_Run')
        self.button_run.clicked.connect(lambda: self.sendHash(main_window))

        #Search program button
        self.button_search = self.findChild(QtWidgets.QPushButton, 'btn_Search')
        self.button_search.clicked.connect(lambda : self.searchHash(main_window))


        #Close program action
        self.button_close = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button_close.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def getfile(self, main_window):
        #Will open a folder browser
        if main_window.radFolder.isChecked(): 
            print("File browser")  
            dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'OpenFile')
            #dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'F:\\')
            print(dir)
            if dir:
                print( "setting directory: " + dir )
                main_window.plainTextEdit_5.setPlainText(dir)
                file_source = main_window.plainTextEdit_5.toPlainText()
                hash = checksumdir.dirhash(dir, hashfunc="sha256")
                print(hash)
                main_window.plainTextEdit_4.setPlainText(hash)

        #Will open a file browser
        if main_window.radFile.isChecked():        
            print("Folder browser")
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                            None,
                            "QFileDialog.getOpenFileName()",
                            "",
                            "All Files (*);;Python Files (*.py)",
                            options=options)
            if self.fileName:
                print( "setting file name: " + self.fileName )
                main_window.plainTextEdit_5.setPlainText(self.fileName)
                file_source = main_window.plainTextEdit_5.toPlainText()
                name, extension = os.path.splitext(file_source)
                
                with open(file_source, "rb") as f:
                    bytes = f.read()
                    hashcode = hashlib.sha256(bytes).hexdigest()
                    main_window.plainTextEdit_4.setPlainText(hashcode)
                
                print(name)
                print(extension)
    
    def sendHash(self, main_window):
        
        hashcode = main_window.plainTextEdit_4.toPlainText()
        print(hashcode)
        url = main_window.txtUrl.toPlainText()
        print(url)
        payload = {'hashcode': hashcode, 'url': url}
        print(payload)
        r = requests.post("http://0.0.0.0:5000/hashValidate", params=payload)
        #print(r.text)
        #print(r.json())
        data = r.json()
        imgRaw = data['QR']
        print(imgRaw)
        
        with open("imageToSave.png", "wb") as imgFile:
            imgFile.write(base64.b64decode(imgRaw))
        pixmap = QtGui.QPixmap('imageToSave.png')
        main_window.lblQRImg.setPixmap(pixmap)
        main_window.lblQRImg.setScaledContents(True)
        #self.resize(370,370)
        main_window.lblQRImg.setHidden(False)
        pass
    
    def searchHash(self, main_window):
        hashcode = main_window.plainTextEdit_4.toPlainText()
        payload = {'hashcode': hashcode}
        print(payload)
        r = requests.post("http://0.0.0.0:5000/search_chain", params=payload)
        data = r.json()
        print(data)
        imgRaw = data['message']
        print(imgRaw)
        
        if data['message'] == 'Does not exist':
            main_window.lblResult.setText('<html><head/><body><p align="center"><span style=" font-size:12pt;">Not found</span></p></body></html>')
        else:
            with open("imageToSave.png", "wb") as imgFile:
                imgFile.write(base64.b64decode(imgRaw))
            pixmap = QtGui.QPixmap('imageToSave.png')
            main_window.lblQRImg.setPixmap(pixmap)
            main_window.lblQRImg.setScaledContents(True)
            #self.resize(370,370)
            main_window.lblQRImg.setHidden(False)
            main_window.lblResult.setText('<html><head/><body><p align="center"><span style=" font-size:12pt;">Found</span></p></body></html>')

        pass
    
    def loginShow(self, main_window):
        #Show txtUsername till login is required
        self.txtUsername.setHidden(False)
        #Show txtPassword till login is required
        self.txtPassword.setHidden(False)
        #Show btnCheck till login is required
        self.btnCheck.setHidden(False)
        #Show lblUser till login is required
        self.lblUser.setHidden(False)
        #Show lblPass till login is required
        self.lblPass.setHidden(False)
        
        pass

    def hash(self, data):
        data = data.encode('utf8')
        return str(hashlib.sha256(data).hexdigest())


    def checkDetails(self, main_window):
        #print("CheckDetails function active")
        
        username = self.txtUsername.toPlainText()
        password = self.txtPassword.text()
        print(self.hash(password))

        #Post request to userBlockchain
        payload = {'username': username, 'password': self.hash(password)}
        print(payload)
        r = requests.post("http://0.0.0.0:6000/search_chain", params=payload)
        data = r.json()
        print(data)

        #Show Url textbox and label
        if data['message'] == 'Valid':
            #print("Valid")
            self.txtUrl.setHidden(False)
            self.lblUrl.setHidden(False)
            self.btn_Run.setHidden(False)

        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())