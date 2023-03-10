""" Manages the cache for the wiki pages.
    :raises NotImplementedError: prune cache is not implemented yet.
    :return: The cache as a dict object."""
import json
# import pageData
from functions.pageData import pageData
from dataclasses import asdict, dataclass
from datetime import datetime
import time
import os


@dataclass
class cacheItem:
    """A cache item is a dataclass that contains the page data and the admin data.
    """    
    data: dataclass
    admin: dataclass


@dataclass
class cacheDataAdmin:
    """Admin data for the cache item.
    Last used and times used.
    """
    lastUsed: datetime
    timesUsed: int


class cacheIndex():
    """ The cache index is a dict that contains the name of the page as key and the filename of the page as value.
    """

    def __init__(self, cache_folder: str = "cache") -> None:
        """Initializes the cache index.

        :param cache_folder: the folder where the cache will be stored, defaults to "cache"
        :type cache_folder: str, optional
        """        
        self.filename = f"{cache_folder}/cacheIndex.json"
        self.cache = {}
        self.cache_folder = cache_folder

    def load(self) -> dict:
        """Loads cache file if it exists

        :param cache_json_file: the filename where the cache is stored.
        :type cache_json_file: str
        :return: The cache as a dict object.
        :rtype: dict
        """
        try:
            with open(self.filename, 'rt', encoding="utf-8") as f:
                self.cache = json.load(f)
                print(f"Loaded cache: {len(self.cache.keys())}")

        except FileNotFoundError as e:
            print(f"could not find {self.filename}. Creating a new cache ...")
            self.cache = {}

            if not os.path.exists(self.cache_folder):
                os.mkdir(self.cache_folder)
            else:
                raise Exception(f"Cache folder {self.cache_folder} already exists!")

    def save(self):
        """Store the cache to a json file.

        :param cache_json_file: file where the cache will be stored.
        :type cache_json_file: _type_
        :param pagecache: the dict object containing the cache
        :type pagecache: dict
        """
        print(f"Savecache: {len(self.cache.keys())}")

        with open(self.filename, 'wt', encoding="utf-8") as f:
            json.dump(self.cache, f)


    def index_page(self, page: pageData):
        """Adds a page to the cache index if it is not in there, else it updates.

        :param page: The page to be added to the cache.
        :type page: pageData
        """        
        
        if page.name in list(self.cache.keys()):
            print(f"Updating {page.name} ...")
            self.update(page.name)
        else:
            if not os.path.exists(f"{self.cache_folder}/items"):
                os.mkdir(f"{self.cache_folder}/items")

            item_filename = f"{self.cache_folder}/items/{page.name}.json"
            self.cache[page.name] = item_filename
            self.save_item(page, item_filename)

    def create_item_filename(self, pagename: str) -> str:
        """Creates the filename for the cache item.

        :param pagename: The name of the page.
        :type pagename: str
        :return: The filename for the cache item.
        :rtype: str
        """        
        return f"{self.cache_folder}/{pagename}.json"

    def save_item(self, page: pageData, item_filename: str = None, times_used: int = 1):
        """ Saves a page to the cache.

        :param page: The pageobject of the page to be saved.
        :type page: pageData
        :param item_filename: The file where the page must be stored, defaults to None
        :type item_filename: str, optional
        :param times_used: how often the cache object was accessed, defaults to 1
        :type times_used: int, optional
        """        
        # if '/' in item_filename:
        #     # TODO: more graceful solution
        #     return
        try:
            item = {
                    "data": asdict(page),
                    "admin": {
                        "lastUsed": time.time(),
                        "timesUsed": times_used,
                    }
                }
            with open(item_filename, 'wt', encoding="utf-8") as f:
                json.dump(item, f)
        except FileNotFoundError as e:
            print(f"Could not find {item_filename}, file not created")
            self.cache.pop(page.name)
            return

        assert os.path.exists(item_filename), f"Could not find {item_filename}, file not created"

    def load_item(self, item_filename: str ) -> cacheItem:
        """Loads a page from the cache.

        :param item_filename: The filename of the page to be loaded.
        :type item_filename: str
        :return: The page as a pageData object.
        :rtype: cacheItem
        """        
        with open(item_filename, 'rt', encoding="utf-8") as f:
            item = json.load(f)

            item = cacheItem(
                data=pageData(
                    name=item["data"]["name"],
                    text=item["data"]["text"],
                    links=item["data"]["links"],
                ),
                admin=cacheDataAdmin(
                    lastUsed=item["admin"]["lastUsed"],
                    timesUsed=item["admin"]["timesUsed"],
                )
            )
            return item

    def update_item(self, pagename: str):
        raise DeprecationWarning("This method is deprecated, use update instead")
        item_filename = self.cache[pagename]
        item = self.load_item(item_filename)
        item.admin.lastUsed = time.time()
        item.admin.timesUsed += 1
        self.save_item(item.data, item_filename, item.admin.timesUsed)

        return item

    def get_page(self, pagename: str) -> dict:
        """Gets a page from the cache.

        :param pagename: The name of the page to be loaded.
        :type pagename: str
        :return: The page as a dict object.  TODO: check if this is correct. Is it a dict?
        :rtype: dict
        """        


        # print(f"Getting page {pagename} ...")
        item_filename = self.cache[pagename]
        item = self.load_item(item_filename)
        item.admin.lastUsed = time.time()
        item.admin.timesUsed += 1
        self.save_item(item.data, item_filename, item.admin.timesUsed)
        return item.data

