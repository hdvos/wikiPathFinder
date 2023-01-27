""" Manages the cache for the wiki pages.
    :raises NotImplementedError: prune cache is not implemented yet.
    :return: The cache as a dict object."""
import json
# import pageData
from functions.pageData import pageData
from dataclasses import asdict, dataclass
from datetime import datetime
import time

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


class wikiPageCache(object):
    def __init__(self, filename) -> None:
        self.filename = filename
        self.cache = {}

    def load(self) -> dict:
        """Loads cache file if it exists

        :param cache_json_file: the filename where the cache is stored.
        :type cache_json_file: str
        :return: The cache as a dict object.
        :rtype: dict
        """
        try:
            with open(self.filename, 'rt', encoding="utf-8") as f:
                pageJson = json.load(f)
                pagecache = {}
                for key, value in pageJson.items():
                    data = value["data"]
                    pagedata = pageData(
                        name=data["name"],
                        text=data["text"],
                        links=data["links"],
                    )

                    admin = value["admin"]
                    admindata = cacheDataAdmin(
                        lastUsed=admin["lastUsed"],
                        timesUsed=admin["timesUsed"],
                    )

                    cacheitem = cacheItem(
                        data=pagedata,
                        admin=admindata,
                    )
                    self.cache[key] = cacheitem

        except FileNotFoundError as e:
            print(f"could not find {self.filename}. Creating a new cache ...")
            self.cache = {}

    def save(self):
        """Store the cache to a json file.

        :param cache_json_file: file where the cache will be stored.
        :type cache_json_file: _type_
        :param pagecache: the dict object containing the cache
        :type pagecache: dict
        """
        print(f"Savecache: {len(self.cache.keys())}")

        pagecache_serialized = []
        pagecache_serialized = {key: asdict(value)
                                for key, value in self.cache.items()}


        with open(self.filename, 'wt', encoding='utf-8') as out:
            json.dump(pagecache_serialized, out)

    def add(self, data):
        self.cache[data.name] = cacheItem(
            data=data,
            admin=cacheDataAdmin(
                lastUsed=int(time.time()),
                timesUsed=1
            )
        )

    def update(self, pagename):
        self.cache[pagename].admin.lastUsed = time.time()
        self.cache[pagename].admin.timesUsed += 1

    def prune_cache(self, keep: float = .50, criterium: str = 'timesUsed'):
        raise NotImplementedError("Prune Cache is not implemented yet")
