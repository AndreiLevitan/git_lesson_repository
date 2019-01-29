from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog
import sys
import shutil


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.editor = QtWidgets.QTextEdit(self.centralwidget)
        self.editor.setGeometry(QtCore.QRect(20, 40, 771, 521))
        self.editor.setObjectName("editor")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(430, 10, 351, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_new_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.create_new_btn.setObjectName("create_new_btn")
        self.horizontalLayout.addWidget(self.create_new_btn)
        self.load_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.load_btn.setObjectName("load_btn")
        self.horizontalLayout.addWidget(self.load_btn)
        self.save_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout.addWidget(self.save_btn)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.create_new_btn.setText(_translate("MainWindow", "Создать новый"))
        self.load_btn.setText(_translate("MainWindow", "Загрузить..."))
        self.save_btn.setText(_translate("MainWindow", "Сохранить..."))


class TextEditor(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_btn.clicked.connect(self.load_form)
        self.save_btn.clicked.connect(self.save_form)
        self.create_new_btn.clicked.connect(self.create_form)
        self.file_path = ''

    def get_case(self):
        case = self.editor.toPlainText()
        return case

    def load_form(self):

        self.file_path = QFileDialog.getOpenFileName(self, 'Выбрать файл')[0]
        with open(self.file_path, mode='r') as file:
            self.editor.setText(file.read())

    def save_form(self):
        if self.file_path:
            self.save_path = QFileDialog.getSaveFileName(self, 'Сохранить файл', 'untitled.txt', "text (*.txt)")[0]
            shutil.copy(self.file_path, self.save_path + '.txt')
            with open(self.save_path, mode='r', encoding='utf-8') as file:
                file.write(self.get_case())

    def create_form(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())
