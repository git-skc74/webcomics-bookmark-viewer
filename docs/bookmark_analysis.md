# Bookmark Data Structure Analysis
The original JSON bookmark file contains three major collections:

#### `recent`  
Contains metadata such as title, comic ID, and `baseMode` (used to determine the comic's type: `Manga = 1, Webtoon = 2`)

#### `bookmark`  
Contains the page number/position within an episode, depending on the comic's type. It can be referenced using `baseMode.episode_id`.

#### `bookmark2`  
Contains the last viewed episode, which can be referenced using `baseMode.comic_id`.

## Initial (Incorrect) Hypothesis

I initially assumed `bookmark` was an outdated bookmark structure that has already been migrated to `bookmark2`.  

This assumption was based on two observations:
- None of the comic IDs in `recent` matched any reference ID in `bookmark`, whereas every reference ID in `bookmark2` matched a comic ID in `recent`.
- The values in `bookmark` looked like they could be page numbers.

I suspected `bookmark` might contain page numbers, so I tried searching for IDs from `bookmark` directly against `recent`. None of the IDs I tried matched, which led me to conclude — incorrectly — that `bookmark` was simply an obsolete, unused structure.

## What I Discovered

While builing the GUI's detail panel, I needed to revisit the original JSON structure. The first thing I checked was the length of each collection. Here's the result from my own bookmark file:

```
recent:    1137
bookmark:  4652
bookmark2: 704
```

`bookmark` is almost 4x longer than `recent` and 6x longer than `bookmark2`. It suggested it wasn't just a legacy/unused data — it likely held something more granular, like page-level information.

To test this, I wrote a small debugging script. Instead of matching `bookmark`'s keys directly against `recent`'s comic IDs, I combined the `baseMode` from `recent` with the **episode ID** from `bookmark2`, and searched for that combined key in `bookmark`.  Results:

```
=== bookmark2 -> ref_id ===
ref_id count: 704

ref_id ∩ bookmark: 454
```

Out of 704 episode IDs derived from `bookmark2`, 454 had a matching entry in `bookmark`.

In other words: of 1,137 comics, 704 have a recorded episode ID, and 454 of those also have a recorded page number.

## Conclusion

The `bookmark` object does not store page numbers keyed by comic ID — it stores page numbers keyed by **episode ID**, which can be accessed via `baseMode.episode_id`.  

Episode IDs themselves live in `bookmark2` and are only resolvable via `baseMode.comic_id`.

This means the correct lookup chain is:

```
recent (comic_id) -> bookmark2 (episode_id) -> bookmark (page number)
```

Not:  
```
recent (comic_id) -> bookmark
```

## Known Data Limitations
   Some titles in `recent` were already truncated (ending in "...")
   by the original app before being saved to the bookmark file.
   Since the original service is discontinued, these titles cannot
   be recovered in full.