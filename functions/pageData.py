from dataclasses import dataclass


@dataclass
class pageData:
    """A DataClass to keep data about a wikipedia page together.
    """
    name: str
    text: str
    links: list
