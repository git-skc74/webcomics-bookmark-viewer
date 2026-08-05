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

        # layout
        layout = QVBoxLayout()

        layout.addWidget(self.set_title_label())
        layout.addLayout(self.set_top_bar())
        layout.addWidget(self.set_search_bar())
        layout.addWidget(self.set_table())

        main_widget.setLayout(layout)

    def setupUi(self):
        self.setWindowTitle("Webcomic Bookmark Viewer")
        self.resize(QSize(800,600))
        self.setMinimumSize(800,600)

        #self.center_on_screen()
    
    def set_title_label(self):
        title_label = QLabel("Bookmark Viewer")

        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(16)

        title_label.setFont(title_font)

        return title_label

    def set_top_bar(self):
        top_bar_layout = QHBoxLayout()

        self.count_label = QLabel()
        self.update_count_label()
        
        top_bar_layout.addWidget(self.count_label)
        top_bar_layout.addWidget(self.set_unsort_button())

        return top_bar_layout

    def update_count_label(self):
        total_count = len(self.proxy.sourceModel().comics)
        visible_count = self.proxy.rowCount() # visible count after filter
        unread_count = self.proxy.sourceModel().unread_count()
        read_count = total_count - unread_count

        if visible_count != total_count: # filtered
            self.count_label.setText(f"Showing {visible_count} ({read_count} read / {unread_count} unread)")
        else: # unfiltered
            self.count_label.setText(f"Total: {total_count} ({read_count} read / {unread_count} unread)")
        
    def set_search_bar(self):
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.textChanged.connect(self.update_filter)

        self.proxy.setFilterKeyColumn(1) # title
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) # disable case-sensitivity
        
        return search_bar
    
    def update_filter(self, text):
        self.proxy.setFilterFixedString(text)
        self.update_count_label() # show filtered label

    def set_table(self):
        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.resizeColumnsToContents()
        
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(3, 200)

        self.table.setSortingEnabled(True)
        self.proxy.sort(-1) # default is unsorted list

        return self.table

    def set_unsort_button(self):
        # button to unsort items
        unsort_button = QPushButton("Unsort")
        unsort_button.clicked.connect(self.on_unsort_clicked)

        return unsort_button

    def on_unsort_clicked(self):
        self.proxy.sort(-1) # unsort

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()

        window_size = self.geometry()

        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2

        self.move(x, y)

    #def set_text_box(self):
    #self.line_edit = QLineEdit(self)
    #self.line_edit.setPlaceholderText("Enter text here")
    #self.line_edit.returnPressed.connect(self.text_changed) 
    
    def text_changed(self):
        text = self.line_edit.text()
        print(text)

    def cell_clicked(self, row, column):
        print(row, column)