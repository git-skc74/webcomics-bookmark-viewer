import sys

from PySide6.QtCore import QAbstractTableModel, QSize, Qt
from PySide6.QtWidgets import QApplication, QHeaderView, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTableView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.setupUi()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        text = QLabel("Bookmark Viewer")
        count = QLabel(f"Total: {len(model.comics)}")
        #button = QPushButton("Button")

        table = QTableView()
        table.setModel(model)
        table.resizeColumnsToContents()

        table.setColumnWidth(1, 200)
        table.setColumnWidth(3, 200)
        #table.setTextElideMode(Qt.ElideRight)


        layout.addWidget(text)
        #layout.addWidget(button)
        layout.addWidget(count)
        layout.addWidget(table)

        main_widget.setLayout(layout)

    def setupUi(self):
        self.setWindowTitle("Webcomic Bookmark Viewer")
        self.resize(QSize(400,300))
        self.setMinimumSize(400,300)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()

        window_size = self.geometry()

        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2

        self.move(x, y)

    def the_button_was_clicked(self):
        print("Clicked!")

    #def set_text_box(self):
    #self.line_edit = QLineEdit(self)
    #self.line_edit.setPlaceholderText("Enter text here")
    #self.line_edit.returnPressed.connect(self.text_changed) 
    
    def text_changed(self):
        text = self.line_edit.text()
        print(text)

    def setButton(self):
        button = QPushButton("PUSH")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(button)

    def cell_clicked(self, row, column):
        print(row, column)