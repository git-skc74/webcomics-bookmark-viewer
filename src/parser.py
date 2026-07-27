import json
from pprint import pprint
from models import Comic

with open("data/data.mvpref", "r", encoding='utf-8') as file:
    data = json.load(file)

recent_list = data["recent"]
bookmark_dict = data["bookmark"]
bookmark2_dict = data["bookmark2"]

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

for item in comics:
    key = f"{item.base_mode}.{item.id}"
    ref = bookmark_dict.get(key)
    if ref is None:
        ref = bookmark2_dict.get(key)
    item.ref_id = ref


# test code
pprint(comics[:5])

none_count = sum(1 for c in comics if c.ref_id is None)
print(f"{none_count} / {len(comics)}")