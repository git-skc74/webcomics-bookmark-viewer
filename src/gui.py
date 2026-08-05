import sys

from PySide6.QtCore import QAbstractTableModel, QSize, Qt
from PySide6.QtWidgets import QApplication, QHeaderView, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTableView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.proxy = model

        self.setupUi()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        text = QLabel("Bookmark Viewer")


        total_count = len(model.sourceModel().comics)
        unread_count = self.proxy.sourceModel().unread_count()
        read_count = total_count - unread_count
        
        ui_layout = QHBoxLayout()

        # total count, read count / unread count.
        count = QLabel(f"Total: {total_count} ({read_count} read / {unread_count} unread)")

        # button to unsort items
        unsort_button = QPushButton("Unsort")
        unsort_button.clicked.connect(self.set_unsort_button)


        ui_layout.addWidget(count)
        #ui_layout.addWidget(unread_label)
        ui_layout.addWidget(unsort_button)

        self.table = QTableView()
        self.table.setModel(model)
        self.table.resizeColumnsToContents()

        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setSortingEnabled(True)

        layout.addWidget(text)
        layout.addLayout(ui_layout)
        layout.addWidget(self.table)

        main_widget.setLayout(layout)

    def setupUi(self):
        self.setWindowTitle("Webcomic Bookmark Viewer")
        self.resize(QSize(800,600))
        self.setMinimumSize(800,600)

        #self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()

        window_size = self.geometry()

        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2

        self.move(x, y)

    def set_unsort_button(self):
        self.proxy.sort(-1) # unsort

    #def set_text_box(self):
    #self.line_edit = QLineEdit(self)
    #self.line_edit.setPlaceholderText("Enter text here")
    #self.line_edit.returnPressed.connect(self.text_changed) 
    
    def text_changed(self):
        text = self.line_edit.text()
        print(text)

    def setSortButton(self):
        button = QPushButton("Sort by title")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(button)

    def cell_clicked(self, row, column):
        print(row, column)