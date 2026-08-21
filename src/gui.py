import sys
import urllib.parse
import webbrowser

from PySide6.QtCore import QAbstractTableModel, QSize, Qt
from PySide6.QtWidgets import QAbstractItemView, QApplication, QFrame, QHeaderView, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QTableView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.proxy = model
        self.current_comic = None

        self.setupUi()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # layout
        layout = QVBoxLayout()

        layout.addWidget(self.create_app_title_label())
        layout.addLayout(self.create_top_bar())
        layout.addLayout(self.create_search_layout())

        view_layout = QHBoxLayout()
        view_layout.addWidget(self.create_table(), stretch=3)
        view_layout.addWidget(self.create_info_panel(), stretch=2)

        layout.addLayout(view_layout)

        main_widget.setLayout(layout)

        # default screen when nothing selected
        self.show_default_panel()

    def setupUi(self):
        self.setWindowTitle("Webcomic Bookmark Viewer")
        self.setWindowIcon(QIcon("assets/icons/app_icon.ico"))

        DEFAULT_WINDOW_SIZE = QSize(800,600)
        self.resize(DEFAULT_WINDOW_SIZE)
        self.setMinimumSize(DEFAULT_WINDOW_SIZE)

        self.setStyleSheet(self.load_stylesheet("assets/styles/main.qss"))

    def load_stylesheet(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
    def create_app_title_label(self):
        app_title_label = QLabel("Bookmark Viewer")

        app_title_font = app_title_label.font()
        app_title_font.setBold(True)
        app_title_font.setPointSize(16)

        app_title_label.setFont(app_title_font)

        return app_title_label

    def create_top_bar(self):
        top_bar_layout = QHBoxLayout()

        self.count_label = QLabel()
        self.update_count_label()
        
        top_bar_layout.addWidget(self.count_label)
        #top_bar_layout.addWidget(self.create_filter())
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

    #def create_filter(self):
        
          
    def create_search_layout(self):
        search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setObjectName("searchBar")

        self.create_search_actions()

        self.search_bar.textChanged.connect(self.update_filter) # update filter for every text change

        self.proxy.setFilterKeyColumn(1) # title
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) # disable case-sensitivity

        search_layout.addWidget(self.search_bar)
        #search_layout.addWidget(self.create_clear_button())
        
        return search_layout

    def create_search_actions(self):
        # search action
        search_action = QAction(
            QIcon("assets/icons/search.svg"),
            "", # no text
            self.search_bar,
        )

        self.search_bar.addAction(
            search_action,
            QLineEdit.ActionPosition.LeadingPosition # leading position in search bar
        )

        # clear action
        clear_action = QAction(
            QIcon("assets/icons/clear.svg"),
            "", # no text
            self.search_bar
        )

        # trigger textChanged -> update_filter
        clear_action.triggered.connect(self.search_bar.clear) # clear search bar

        self.search_bar.addAction(
            clear_action,
            QLineEdit.ActionPosition.TrailingPosition # trailing position in search bar
        )

    def update_filter(self, text):
        self.table.clearSelection()
        self.table.selectionModel().clearCurrentIndex()

        self.proxy.setFilterFixedString(text)
        self.update_count_label() # show filtered label

        self.current_comic = None
        self.show_default_panel()

    def create_unsort_button(self):
        # button to unsort items
        unsort_button = QPushButton("Unsort")
        unsort_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        unsort_button.clicked.connect(self.on_unsort_clicked)

        return unsort_button

    def on_unsort_clicked(self):
        self.proxy.sort(-1) # unsort

    def create_table(self):
        self.table = QTableView()
        self.table.setModel(self.proxy)

        # block vertical resizing
        vertical_header = self.table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.Fixed)

        # select row instead of content
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # block multiple selection
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        # hide all except for title and author
        self.table.hideColumn(0)  # type
        self.table.hideColumn(3)  # tag
        self.table.hideColumn(4)  # release
        self.table.hideColumn(5)  # comic_id
        self.table.hideColumn(6)  # episode_id
        self.table.hideColumn(7)  # page_id

        #self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setSortingEnabled(True) # enable sorting
        self.proxy.sort(-1) # default is unsorted list

        return self.table

    def create_info_panel(self):
        self.table.selectionModel().currentRowChanged.connect(self.on_row_selected)

        frame = QFrame()
        frame.setObjectName("detailsFrame")

        panel_layout = QVBoxLayout()

        # placeholder cover for detail panel
        cover_label = QLabel("No Cover")
        cover_label.setObjectName("coverLabel")
        cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info_labels = { # Dictionary {key:value}, accessed through key
            "title": QLabel(),
            "author": QLabel(),
            "type": QLabel(),
            "tags": QLabel(),
            "comic_id": QLabel(),
            "episode_id": QLabel(),
            "page_id": QLabel(),
            "release": QLabel(),
        }

        comic_title_font = self.info_labels["title"].font()
        comic_title_font.setPointSize(12)
        comic_title_font.setBold(True)
        self.info_labels["title"].setFont(comic_title_font)

        self.info_labels["title"].setWordWrap(True)
        self.info_labels["tags"].setWordWrap(True)

        panel_layout.addWidget(cover_label)

        for label in self.info_labels.values():
            panel_layout.addWidget(label)

        panel_layout.addWidget(self.create_search_online_button())

        frame.setLayout(panel_layout)

        return frame

    def show_default_panel(self):
        self.info_labels["title"].setText("Select a comic to view details")
        for key, label in self.info_labels.items():
            if key != "title":
                label.setText("")
        
        self.search_online_button.setEnabled(False)
  
    # QModelIndex
    # current = currently selected index / previous = previously selected index
    def on_row_selected(self, current, previous):
        if not current.isValid():
            self.current_comic = None
            self.show_default_panel()
            return

        source_index = self.proxy.mapToSource(current) # getting source index using current proxy index
        comic = self.proxy.sourceModel().comics[source_index.row()]

        self.current_comic = comic
        self.update_info_panel(comic)

    def _format(self, value, fallback="unknown"):
        return str(value) if value else fallback

    def update_info_panel(self, comic):
        self.info_labels["title"].setText(comic.name)
        self.info_labels["author"].setText("Author\n" + self._format(comic.author))
        self.info_labels["tags"].setText("Tags: " + self._format(", ".join(f"#{tag}" for tag in comic.tags), "None")) # put hashtag + join
        self.info_labels["type"].setText("Type: " + ("Manga" if comic.base_mode == 1 else "Webtoon"))
        self.info_labels["comic_id"].setText("Comic ID: " + self._format(comic.id))
        self.info_labels["episode_id"].setText("Last Episode ID: " + self._format(comic.episode_id, "unread"))
        self.info_labels["page_id"].setText("Viewer Position: " + self._format(comic.page_id, "no data"))
        self.info_labels["release"].setText("Status: " + self._format(comic.release))

        self.search_online_button.setEnabled(True)

    def create_search_online_button(self):
        self.search_online_button = QPushButton("Search Comic Online")
        self.search_online_button.setObjectName("searchOnlineButton")
        self.search_online_button.setIcon(QIcon("assets/icons/search_online.svg"))
        self.search_online_button.clicked.connect(self.on_search_online_clicked)
        self.search_online_button.setEnabled(False) # initially disabled - no comic selected

        return self.search_online_button
    
    def on_search_online_clicked(self):
        if self.current_comic is None: # no comic selected
            return
        
        query = urllib.parse.quote(self.current_comic.name)
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()

        window_size = self.geometry()

        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2

        self.move(x, y)

    def cell_clicked(self, row, column):
        print(row, column)