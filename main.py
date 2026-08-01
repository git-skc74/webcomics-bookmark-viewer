from src.parser import load_comics
from src.models import ComicTableModel
from src.gui import MainWindow

import sys
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QApplication

def main():
    print("Hello from webcomics-bookmark-viewer!")

    # app for gui
    app = QApplication(sys.argv)

    # call parser
    comics = load_comics()
    #print(len(comics))
    model = ComicTableModel(comics) # get model using comics list data

    # create main window
    window = MainWindow(model)
    window.show()

    sys.exit(app.exec()) # exit when return exitcode

if __name__ == "__main__":
    main()
