from PyQt5 import QtCore, QtGui, QtWidgets
from untitled import Ui_Dialog
from packages import uData
import asyncio

class MainWindow(Ui_Dialog):

    def setupUi(self, Dialog):
        super(MainWindow, self).setupUi(Dialog)
        self.label_3.setText(str(uData.update.page_number))
        self.pushButton.clicked.connect(self.btn_clicked)
        self.pushButton_2.clicked.connect(self.btn_clicked_2)
        print("initialized!")

    def btn_clicked(self):
        url = self.textEdit.toPlainText()
        #option
        text = self.checkBox.isChecked()
        title = self.checkBox_2.isChecked()
        dept = self.checkBox_3.isChecked()
        writer = self.checkBox_4.isChecked()
        date = self.checkBox_5.isChecked()
        views = self.checkBox_6.isChecked()

        post01 = uData.init(url, text=text, title=title, dept=dept, writer=writer, date=date, views=views)
        self.textBrowser.setText(post01.contents)

    def btn_clicked_2(self):
        check: uData.update.Refreash = uData.refreash()
        if check is not None:
            self.label_3.setText(str(check.page_number))
            self.textEdit.setText(check.url)
            self.btn_clicked()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())