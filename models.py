from dataclasses import dataclass

@dataclass
class Comic:
    author: str
    base_mode: int
    id: int
    name: str
    tags: list[str]
    ref_id: int | None