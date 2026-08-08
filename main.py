import sys

from src.parser import load_comics
from src.models import ComicTableModel
from src.gui import MainWindow

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

def main():
    print("Hello from webcomics-bookmark-viewer!")

    # app for gui
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10)) # font and size

    # call parser
    comics = load_comics()
    #print(len(comics))
    model = ComicTableModel(comics) # get model using comics list data

    #print(dir(model)) # test

    # proxy model - for sorting
    proxy = QSortFilterProxyModel() # setup proxy
    proxy.setSourceModel(model) # connect model to proxy

    # create main window
    window = MainWindow(proxy)
    window.show()

    sys.exit(app.exec()) # exit when return exitcode

if __name__ == "__main__":
    main()
