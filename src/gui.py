import sys

from PySide6.QtCore import QAbstractTableModel, QSize, Qt
from PySide6.QtWidgets import QApplication, QFrame, QHeaderView, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QTableView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.proxy = model

        self.setupUi()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # layout
        layout = QVBoxLayout()

        layout.addWidget(self.create_app_title_label())
        layout.addLayout(self.create_top_bar())
        layout.addLayout(self.create_search_layout())

        view_layout = QHBoxLayout()
        view_layout.addWidget(self.create_table(), stretch=2)
        view_layout.addWidget(self.create_info_panel(), stretch=1)

        layout.addLayout(view_layout)

        main_widget.setLayout(layout)

    def setupUi(self):
        self.setWindowTitle("Webcomic Bookmark Viewer")
        self.setWindowIcon(QIcon("assets/icons/app_icon.ico"))

        DEFAULT_WINDOW_SIZE = QSize(800,600)
        self.resize(DEFAULT_WINDOW_SIZE)
        self.setMinimumSize(DEFAULT_WINDOW_SIZE)
    
    def create_app_title_label(self):
        app_title_label = QLabel("Bookmark Viewer")

        title_font = app_title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(16)

        app_title_label.setFont(title_font)

        return app_title_label

    def create_top_bar(self):
        top_bar_layout = QHBoxLayout()

        self.count_label = QLabel()
        self.update_count_label()
        
        top_bar_layout.addWidget(self.count_label)
        top_bar_layout.addWidget(self.create_unsort_button())

        return top_bar_layout

    def update_count_label(self):
        total_count = len(self.proxy.sourceModel().comics)
        visible_count = self.proxy.rowCount() # visible count after filter
        unread_count = self.proxy.sourceModel().unread_count()
        read_count = total_count - unread_count

        if visible_count != total_count: # filtered
            self.count_label.setText(f"Showing {visible_count} "
                                     f"({read_count} read / {unread_count} unread)")
        else: # unfiltered
            self.count_label.setText(f"Total: {total_count} "
                                     f"({read_count} read / {unread_count} unread)")

    def create_unsort_button(self):
        # button to unsort items
        unsort_button = QPushButton("Unsort")
        unsort_button.clicked.connect(self.on_unsort_clicked)

        return unsort_button

    def on_unsort_clicked(self):
        self.proxy.sort(-1) # unsort
        
    def create_search_layout(self):
        search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.update_filter) # update filter for every text change

        self.proxy.setFilterKeyColumn(1) # title
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) # disable case-sensitivity

        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.create_clear_button())
        
        return search_layout

    def create_clear_button(self):
        # button to clear search bar
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.on_clear_clicked)

        return clear_button
    
    def on_clear_clicked(self):
        self.search_bar.clear() # trigger textChanged -> update_filter

    def update_filter(self, text):
        self.proxy.setFilterFixedString(text)
        self.update_count_label() # show filtered label

    def create_table(self):
        self.table = QTableView()
        self.table.setModel(self.proxy)
        #self.table.resizeColumnsToContents()

        # resize column width for long content
        #self.table.setColumnWidth(1, 200) # title
        #self.table.setColumnWidth(3, 200) # tags

        #self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setSortingEnabled(True) # enable sorting
        self.proxy.sort(-1) # default is unsorted list

        return self.table

    def create_info_panel(self):
        self.table.selectionModel().currentRowChanged.connect(self.on_row_selected)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Sunken)
        #frame.setFixedWidth(300)

        panel_layout = QVBoxLayout()

        self.comic_title_label = QLabel()
        self.comic_title_label.setWordWrap(True)
        self.comic_author_label = QLabel()
        self.comic_tags_label = QLabel()
        self.comic_tags_label.setWordWrap(True)
        self.comic_release_label = QLabel()
        self.comic_type_label = QLabel()
        self.comic_id_label = QLabel()
        self.comic_episode_label = QLabel()
        self.comic_page_label = QLabel()

        panel_layout.addWidget(QLabel("Comic Details"))

        panel_layout.addWidget(self.comic_title_label)
        panel_layout.addWidget(self.comic_author_label)
        panel_layout.addWidget(self.comic_type_label)
        panel_layout.addWidget(self.comic_tags_label)
        panel_layout.addWidget(self.comic_id_label)
        panel_layout.addWidget(self.comic_episode_label)
        panel_layout.addWidget(self.comic_page_label)
        panel_layout.addWidget(self.comic_release_label)

        frame.setLayout(panel_layout)

        return frame
        
    # QModelIndex
    # current = currently selected index / previous = previously selected index
    def on_row_selected(self, current, previous):
        if not current.isValid():
            return

        source_index = self.proxy.mapToSource(current) # getting source index using current proxy index
        comic = self.proxy.sourceModel().comics[source_index.row()]

        self.current_comic = comic
        self.update_info_panel(comic)

    def update_info_panel(self, comic):
        self.comic_title_label.setText("Title: " + comic.name)
        self.comic_author_label.setText("Author: " + (comic.author if comic.author else "unknown"))
        self.comic_tags_label.setText("Tags: " + (", ".join("#" + tag for tag in comic.tags) if comic.tags else "None")) # put hashtag + join
        self.comic_type_label.setText("Type: " + ("Manga" if comic.base_mode == 1 else "Webtoon"))
        self.comic_release_label.setText("Status: " + (comic.release if comic.release else "unknown"))
        self.comic_id_label.setText("Comic ID: " + (str(comic.id) if comic.id else "unknown"))
        self.comic_episode_label.setText("Last Viewed: " + (str(comic.episode_id) if comic.episode_id else "unread"))
        self.comic_page_label.setText("Last Page Number/Position: " + str(comic.page_id if comic.page_id else "no data"))

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