from dataclasses import dataclass


@dataclass
class JobItem:
    urls: list[str]
    folder: str
    refid: str
    params: dict[str, str] = None

    def __post_init__(self):
        if not self.params:
            self.params = {}
