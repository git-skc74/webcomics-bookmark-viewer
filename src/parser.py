import json

from .models import Comic

def load_comics():
    with open("data/data.mvpref", "r", encoding='utf-8') as file:
        data = json.load(file)

    recent_list = data["recent"] # list of comic dataset
    bookmark_dict = data["bookmark"] # old bookmark list - migrated
    bookmark2_dict = data["bookmark2"] # new bookmark list

    comics = []

    for item in recent_list:
        comic = Comic(
            author=item.get("author"),
            base_mode=item.get("baseMode"),
            id=item.get("id"),
            name=item.get("name"),
            tags=item.get("tags"),
            ref_id=None,
        )
        comics.append(comic)

    for item in comics: # find and save ref_id from bookmark and bookmark2
        key = f"{item.base_mode}.{item.id}"
        ref = bookmark_dict.get(key)
        if ref is None:
            ref = bookmark2_dict.get(key)
        item.ref_id = ref

    return comics