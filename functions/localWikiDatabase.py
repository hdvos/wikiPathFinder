from dataclasses import asdict, dataclass

@dataclass
class cacheItem:
    data: dataclass
    admin: dataclass


@dataclass
class cacheDataAdmin:
    """Admin data for the cache
    """
    lastUsed: datetime
    timesUsed: int
