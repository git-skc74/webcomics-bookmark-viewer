import json

def debug_bookmark():
    with open("data/data.mvpref", "r", encoding="utf-8") as file:
        data = json.load(file)

    recent_list = data["recent"] # comic data
    bookmark_dict = data["bookmark"] # contain last viewed episode data
    bookmark2_dict = data["bookmark2"] # expected to have page data

    print("=== Bookmark Debug ===")
    print(f"recent:    {len(recent_list)}")
    print(f"bookmark:  {len(bookmark_dict)}")
    print(f"bookmark2: {len(bookmark2_dict)}")

    # comic keys in recent
    recent_keys = {
        f"{item.get('baseMode')}.{item.get('id')}"
        for item in recent_list
    }

    # --------------------------------------------------
    # 1. recent ∩ bookmark2
    # --------------------------------------------------

    recent_bookmark2 = recent_keys & bookmark2_dict.keys()

    print()
    print("recent ∩ bookmark2:", len(recent_bookmark2))

    # --------------------------------------------------
    # 2. let bookmark2's values to be ref_id
    # --------------------------------------------------

    ref_keys = set()

    print()
    print("=== bookmark2 -> ref_id ===")

    for key in recent_bookmark2:
        ref_id = bookmark2_dict[key]

        # baseMode from key (manga = 1, webtoon = 2)
        base_mode = key.split(".", 1)[0]

        ref_key = f"{base_mode}.{ref_id}" # new ref_id for bookmark
        ref_keys.add(ref_key)

    print("ref_id count:", len(ref_keys))

    # --------------------------------------------------
    # 3. check if ref_id exists as bookmark's key
    # --------------------------------------------------

    matched = ref_keys & bookmark_dict.keys()

    print()
    print("ref_id ∩ bookmark:", len(matched))

    # --------------------------------------------------
    # 4. actual results
    # --------------------------------------------------

    print()
    print("=== MATCHED ===")

    count = 0

    for key in recent_bookmark2:
        ref_id = bookmark2_dict[key]
        base_mode = key.split(".", 1)[0]
        ref_key = f"{base_mode}.{ref_id}"

        if ref_key in bookmark_dict:
            print(
                f"manga={key} | "
                f"ref_id={ref_key} | "
                f"position={bookmark_dict[ref_key]}"
            )

            count += 1

            if count >= 30:
                break

    # --------------------------------------------------
    # 5. not matched results
    # --------------------------------------------------

    print()
    print("=== NOT MATCHED (first 30) ===")

    count = 0

    for key in recent_bookmark2:
        ref_id = bookmark2_dict[key]
        base_mode = key.split(".", 1)[0]
        ref_key = f"{base_mode}.{ref_id}"

        if ref_key not in bookmark_dict:
            print(
                f"manga={key} | "
                f"ref_id={ref_key}"
            )

            count += 1

            if count >= 30:
                break


if __name__ == "__main__":
    debug_bookmark()