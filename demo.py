
    def designComboBox(self):
        # Design the Combo box
        for i in range (len(self.unit_label.unitTable)): #Unit Combo box  
            self.homePage.unitItemCB.addItems([str(self.unit_label.unitTable[i][1])])                  
        for i in range (len(self.supplier_label.supplierTable)): #Supplier Combo box
            self.homePage.supplierItemCB.addItems([str(self.supplier_label.supplierTable[i][1])])     
            self.homePage.SMSupplier.addItems([str(self.supplier_label.supplierTable[i][1])])
            self.homePage.LISupplier.addItems([str(self.supplier_label.supplierTable[i][1])])
        for i in range (len(self.role_label.roleTable)):
            self.homePage.User_RoleCB.addItems([str(self.role_label.roleTable[i][1])])


class confirmBEWindow(QMainWindow):
    closed = pyqtSignal()
    def __init__(self, BEId: int):
        super(confirmBEWindow, self).__init__()    
        self.confirmBEWindow = ui.ui_confirmBE.Ui_MainWindow()
        self.confirmBEWindow.setupUi(self) 
        self.BE_label = classTask.BE()
        self.BE_Detail_label = classTask.BE_Detail()
        self.user_label = classTask.Users()
        self.supplier_label = classTask.Supplier()
        self.item_label = classTask.Item()
        self.customer_label = classTask.Customer()
        self.BEId = BEId
        self.completer_user_list = []

        #Design the element
        requesterId = db.execute("SELECT UserId from BE WHERE Id = ?", BEId).fetchone()[0]
        requesterName = db.execute("SELECT Name FROM Users WHERE Id = ?", int(requesterId)).fetchone()[0]
        createDate = db.execute("SELECT CreateDate FROM BE WHERE Id = ?", BEId).fetchone()[0]

        self.confirmBEWindow.Requester.setText(f"{requesterId} - {requesterName}")
        self.confirmBEWindow.creationDate.setText(f"{createDate}")
        current_datetime = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm:ss")
        self.confirmBEWindow.duedate.setText(f"{current_datetime}")
        self.confirmBEWindow.BEId.setText(f"{BEId}")

        #Design the recommended box
        for i in range (len(self.user_label.userTable)):
            self.completer_user_list.append(f"{self.user_label.userTable[i][0]} - {self.user_label.userTable[i][1]}")
        self.completer_user = QCompleter(self.completer_user_list, self)
        self.completer_user.setCaseSensitivity(Qt.CaseInsensitive)
        self.confirmBEWindow.staff.setCompleter(self.completer_user)

        #Design table
        for i in range(len(self.BE_Detail_label.BE_DetailTable)):
            if self.BE_Detail_label.BE_DetailTable[i][0] == self.BEId:
                rowPosition = self.confirmBEWindow.ItemTable.rowCount()
                self.confirmBEWindow.ItemTable.insertRow(rowPosition)
                self.confirmBEWindow.ItemTable.setItem(rowPosition, 0, QTableWidgetItem(str(self.BE_Detail_label.BE_DetailTable[i][1])))
                name = db.execute("SELECT Name FROM Item WHERE Id = ?", self.BE_Detail_label.BE_DetailTable[i][1]).fetchone()[0]
                self.confirmBEWindow.ItemTable.setItem(rowPosition, 1, QTableWidgetItem(str(name)))
                self.confirmBEWindow.ItemTable.setItem(rowPosition, 2, QTableWidgetItem(str(self.BE_Detail_label.BE_DetailTable[i][2])))
        
        # interact with button
        self.confirmBEWindow.confirmButton.clicked.connect(self.confirmBE)
    
    def confirmBE(self):
        # Check condition  
        notiDisplay = ""
        check = True
        # 1. Staff must have in staff list with form Id - name
        # 1.1. Check if it has " - "
        if not " - " in self.confirmBEWindow.staff.text():
            notiDisplay += "Staff information is invalid.\n"
            check = False
        else:
            staffId, staffName = str(self.confirmBEWindow.staff.text()).split(" - ")
            # 1.2. Does the ID exist?
            check_exist = False
            for i in range (len(self.user_label.userTable)):
                if int(staffId) == self.user_label.userTable[i][0]:
                    check_exist = True
                    break
            if check_exist == False:
                notiDisplay += "Staff information is invalid.\n"
                check = False
            else:
                # 1.3. ID and Name are been one person in staff list?
                staffID_test = db.execute("SELECT Id FROM Users WHERE Name = ?", staffName).fetchone()[0]
                if int(staffId) != staffID_test:
                    notiDisplay += "Staff information is invalid.\n"
                    check = False
        # 2. Check realAmount
        # 2.1. All row of realAmount col must be filled 
        check_filled = True
        for i in range (self.confirmBEWindow.ItemTable.rowCount()):
            if self.confirmBEWindow.ItemTable.item(i, 3) is None:
                check_filled = False
                break
        if check_filled == False:
                notiDisplay += "All row off \"Real Amount\" column must be filled.\n"
                check = False
        else:
            check_filled = True
            for i in range (self.confirmBEWindow.ItemTable.rowCount()):
                if self.confirmBEWindow.ItemTable.item(i, 3).text() == "":
                    check_filled = False
                    break
            if check_filled == False:
                notiDisplay += "All row off \"Real Amount\" column must be filled.\n"
                check = False
            else: 
                # 2.2. The value must a number
                check_number = True
                for i in range (self.confirmBEWindow.ItemTable.rowCount()):
                    text = str(self.confirmBEWindow.ItemTable.item(i, 3).text())
                    if not text.isdigit():
                        check_number = False
                        break
                if check_number == False:
                    notiDisplay += "The value of real amount must be a number.\n"
                    check = False
                else:
                    # 2.3. The number must be greater than 0
                    check_number = True
                    for i in range (self.confirmBEWindow.ItemTable.rowCount()):
                        text = int(self.confirmBEWindow.ItemTable.item(i, 3).text())
                        if text < 0:
                            check_number = False
                            break
                    if check_number == False:
                        notiDisplay += "The value of real amount must be greater than 0.\n"
                        check= False
        # 3. Check invoice total
        # 2.1. invoice total must be filled 
        if self.confirmBEWindow.invoiceTotal.text() == "":
            notiDisplay += "The invoice total must be filled.\n"
            check = False
        else: 
            # 2.2. The invoice total must a number
            text = str(self.confirmBEWindow.invoiceTotal.text())
            if not text.isdigit():
                notiDisplay += "The value of invoice total must be a number.\n"
                check = False
            else:
                try:
                    text = int(self.confirmBEWindow.invoiceTotal.text())
                except ValueError:
                    text = "0"
                if text < 0:
                    notiDisplay += "The value of invoice total must be greater than 0.\n"
                    check= False
        homeTask = home()
        if check == True:
            itemId_tList = []
            for i in range(self.confirmBEWindow.ItemTable.rowCount()):
                itemId_tdict= {"ItemId": int(self.confirmBEWindow.ItemTable.item(i,0).text()), "RealAmount": int(self.confirmBEWindow.ItemTable.item(i,3).text())}
                itemId_tList.append(itemId_tdict)
            self.BE_label.confirmBuyingEntry(self.BEId, self.confirmBEWindow.invoiceTotal.text(), itemId_tList)
            notiDisplay += "Confirmed successfully!"
            homeTask.noti(notiDisplay)
        else: homeTask.noti(notiDisplay)
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()
        
class editItem(QMainWindow):
    closed = pyqtSignal()
    def __init__(self, itemId: int):
        super(editItem, self).__init__()    
        self.editItem = ui.ui_editItem.Ui_MainWindow()
        self.editItem.setupUi(self) 
        self.itemId = itemId
        itemName = db.execute("SELECT Name FROM Item WHERE Id = ?", itemId).fetchone()[0]
        itemPrice = db.execute("SELECT Price FROM Item WHERE Id = ?", itemId).fetchone()[0]
        itemStatus = int(db.execute("SELECT Status FROM Item WHERE Id = ?", itemId).fetchone()[0])
        self.editItem.EditItemName.setText(f"{itemName}")
        self.editItem.EditItemPrice.setText(f"{itemPrice}")
        if itemStatus == 1:
            self.editItem.EditItemStatus.setCurrentText("Available")
        else: self.editItem.EditItemStatus.setCurrentText("Not available")
        self.editItem.EditItemChange.clicked.connect(self.changeIteminfo)

    def changeIteminfo(self):
        homeTask = home()
        try:
            db.execute("UPDATE Item SET Name = ? WHERE Id = ?", (str(self.editItem.EditItemName.text()), self.itemId))
            db.execute(f"UPDATE Item SET Price = {int(self.editItem.EditItemPrice.text())} WHERE Id = {self.itemId}")
            if self.editItem.EditItemStatus.currentText() == "Available":
                db.execute(f"UPDATE Item SET Status = 1 WHERE Id = {self.itemId}")
            else: db.execute(f"UPDATE Item SET Status = 0 WHERE Id = {self.itemId}")
            db.commit()
            self.close()
            homeTask.noti('Item updated successfully!')
            homeTask.item_label.update_db()
        except ValueError:
            homeTask.noti("Value Error!")
        
    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()
  
class EditStaff(QMainWindow):
    def __init__(self, userId: int):
        super(EditStaff, self).__init__()
        self.editStaff = ui.ui_EditUser.Ui_MainWindow()
        self.editStaff.setupUi(self)
        self.userId = userId 
        self.user_label = classTask.Users()
        self.role_label = classTask.Role()

        # Design the Combo box
        for i in range (len(self.role_label.roleTable)): 
            self.editStaff.ESRole.addItem(str(self.role_label.roleTable[i][1]))

        self.editStaff.ESName.setText(db.execute("SELECT Name FROM Users WHERE Id = ?", self.userId).fetchone()[0])
        self.editStaff.ESPhone.setText(str(db.execute("SELECT Phone FROM Users WHERE Id = ?", self.userId).fetchone()[0]))
        self.editStaff.ESAddress.setText(db.execute("SELECT Address FROM Users WHERE Id = ?", self.userId).fetchone()[0])
        self.editStaff.ESEmail.setText(db.execute("SELECT Email FROM Users WHERE Id = ?", self.userId).fetchone()[0])
        esrole = db.execute("SELECT RoleName FROM Role JOIN Users ON Role.Id = Users.RoleId WHERE Users.RoleId = ?", self.userId).fetchone()[0]
        self.editStaff.ESRole.setCurrentText(esrole)
        if self.user_label.userTable[i][8] == True: 
            self.editStaff.ESStatus.setCurrentText("Available")
        else: self.editStaff.ESStatus.setCurrentText("Not available")
        self.editStaff.ESUsername.setText(db.execute("SELECT Username FROM Users WHERE Id = ?", self.userId).fetchone()[0])
        self.editStaff.ESPassword.setText(db.execute("SELECT Password FROM Users WHERE Id = ?", self.userId).fetchone()[0])
    
        self.editStaff.ESButton.clicked.connect(self.changeInfo)

    def changeInfo(self):
        homeTask = home()
        try:
            db.execute("UPDATE Users SET Name = ? WHERE Id = ?", self.editStaff.ESName.text(), self.userId)
            db.execute("UPDATE Users SET Phone = ? WHERE Id = ?", int(self.editStaff.ESPhone.text()),self.userId)
            db.execute("UPDATE Users SET Address = ? WHERE Id = ?", self.editStaff.ESAddress.text(), self.userId)
            db.execute("UPDATE Users SET Email = ? WHERE Id = ?", self.editStaff.ESEmail.text(),self.userId)
            role_new = int(db.execute("SELECT Id FROM Role WHERE RoleName = ?",self.editStaff.ESRole.currentText()).fetchone()[0])
            db.execute("UPDATE Users SET RoleId = ? WHERE Id = ?", role_new, self.userId)
            db.execute("UPDATE Users SET Username = ? WHERE Id = ?", self.editStaff.ESUsername.text(), self.userId)
            db.execute("UPDATE Users SET Password = ? WHERE Id = ?", self.editStaff.ESPassword.text(), self.userId)
            if self.editStaff.ESStatus.currentText() == "Available":
                db.execute("UPDATE Users SET Status = 1 WHERE Id = ?", self.userId)
            else: db.execute("UPDATE Users SET Status = 0 WHERE Id = ?", self.userId)
            db.commit()
            homeTask =home()
            homeTask.format_list_staff()
            homeTask.noti("Update the user information sucessfully")
            self.close()
        except ValueError:
            homeTask.noti("Vale Error!")
        except Exception as e:
            homeTask.noti(f"Error: {e}")

class ChangePassword(QMainWindow):
    def __init__(self, loginUserId):
        super(ChangePassword, self).__init__()
        self.changePassword = ui.ui_changePassword.Ui_MainWindow()
        self.changePassword.setupUi(self)
        self.changePassword.pushButton.clicked.connect(self.update)
        self.user_label = classTask.Users()
        self.loginUserId = loginUserId
    
    def update(self):
        #Check condition
        check = True
        displayTest = ""
        homeTask = home()
        if self.changePassword.lineEdit.text() == "" or self.changePassword.lineEdit_2.text() == "":
            check = False
            displayTest += "You must fill all the information.\n"
        elif self.changePassword.lineEdit.text() != self.changePassword.lineEdit_2.text():
            check = False
            displayTest += "Your re-input password is not as password.\n"
        if check == False:
            displayTest += "Please re-input."
            homeTask.noti("displayTest")
        else: 
            try:
                db.execute("UPDATE Users SET Password = ? WHERE Id = ?", (self.changePassword.lineEdit.text(), self.loginUserId))
                db.commit()
                self.user_label.update_db()
                homeTask.noti("Update password successfully!")
            except ValueError:
                homeTask.noti("Value error!")
            except Exception:
                homeTask.noti("Something wrong. Please re-input!")
