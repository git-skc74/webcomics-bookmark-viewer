from dataclasses import dataclass
from PySide6.QtCore import QAbstractTableModel, QSortFilterProxyModel, Qt

@dataclass
class Comic:
    author: str
    base_mode: int
    id: int
    name: str
    tags: list[str]
    release: str
    episode_id: int | None
    page_id: int | None

class ComicFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        self.search_text = ""
        self.type_filter = "All"
        self.read_filter = "All"

    #def set_search_text


class ComicTableModel(QAbstractTableModel):
    def __init__(self, comics):
        super().__init__()
        self.comics = comics

    def rowCount(self, parent):
        return len(self.comics)

    def columnCount(self, parent):
        return 8

    def unread_count(self):
        unread = sum(comic.episode_id is None for comic in self.comics)
        return unread
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            comic = self.comics[index.row()] # get comic object by index

            column = index.column() # get which column is calling

            content = [
                "Manga" if comic.base_mode == 1 else "Webtoon", # 0 - manga or webtoon
                comic.name,                                     # 1- title
                comic.author,                                   # 2 - author
                ", ".join(comic.tags) if comic.tags else "",    # 3 - tags (list to string)
                comic.release,                                  # 4 - release: ongoing (weekly/biweekly/monthly) or complete
                comic.id,                                       # 5 - comic id
                comic.episode_id,                               # 6 - episode id
                comic.page_id,                                  # 7 - page number/position
            ]
            return content[column]

        if role == Qt.ToolTipRole: # tooltip popup for long content
            comic = self.comics[index.row()]
    
            if index.column() == 1: # title
                return comic.name
            if index.column() == 3: # tags
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
                    "Release",
                    "Comic ID",
                    "Episode ID",
                    "Page Number/Position"
                ]
                return headers[section]

            if orientation == Qt.Vertical:
                return section + 1 # return index + 1

        return None