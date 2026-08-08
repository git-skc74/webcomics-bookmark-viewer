import json

from .models import Comic

def load_comics():
    with open("data/data.mvpref", "r", encoding='utf-8') as file:
        data = json.load(file)

    recent_list = data["recent"]        # list of comic dataset
    bookmark_dict = data["bookmark"]    # page number/position
    bookmark2_dict = data["bookmark2"]  # last viewed episode IDs

    comics = []

    for item in recent_list:
        comic = Comic(
            author=item.get("author"),
            base_mode=item.get("baseMode"),
            id=item.get("id"),
            name=item.get("name"),
            tags=item.get("tags"),
            release=item.get("release"),
            episode_id=None,
            page_id=None,
        )
        comics.append(comic)

    for item in comics: # find and save ref_id from bookmark2
        key = f"{item.base_mode}.{item.id}"
        ref = bookmark2_dict.get(key)
        item.episode_id = ref 

    count = 0
    for item in comics:
        key = f"{item.base_mode}.{item.episode_id}"
        ref = bookmark_dict.get(key)
        if ref:
            count += 1
        item.page_id = ref

    print(count)

    return comics