from dataclasses import dataclass
from PySide6.QtCore import QAbstractTableModel, Qt

@dataclass
class Comic:
    author: str
    base_mode: int
    id: int
    name: str
    tags: list[str]
    ref_id: int | None

class ComicTableModel(QAbstractTableModel):
    def __init__(self, comics):
        super().__init__()
        self.comics = comics

    def rowCount(self, parent):
        return len(self.comics)

    def columnCount(self, parent):
        return 6

    def data(self, index, role):
        if role == Qt.DisplayRole:
            comic = self.comics[index.row()] # get comic object by index

            column = index.column() # get which column is calling

            content = [
                "Manga" if comic.base_mode == 1 else "Webtoon", # 0 - manga or webtoon
                comic.name,                                     # 1- title
                comic.author,                                   # 2 - author
                ", ".join(comic.tags) if comic.tags else "",    # 3 - tags (list to string)
                comic.id,                                       # 4 - comic id
                comic.ref_id,                                   # 5 - reference id (episode id)
            ]
            return content[column]

        if role == Qt.ToolTipRole: # tooltip popup for long content
            comic = self.comics[index.row()]
    
            if index.column() == 1:
                return comic.name
            if index.column() == 3:
                return ", ".join(comic.tags) if comic.tags else "N/A"
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = [
                    "Type",
                    "Title",
                    "Author",
                    "Tags",
                    "Comic ID",
                    "Reference ID",
                ]
                return headers[section]

            if orientation == Qt.Vertical:
                return section + 1 # return index + 1

        return None
    