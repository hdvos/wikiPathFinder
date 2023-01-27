import random
from attr import asdict
import wikipediaapi
from multiprocessing.pool import ThreadPool
from sklearn.metrics.pairwise import cosine_distances
from functions.wikiPageCache import wikiPageCache
from functions.pageData import pageData
from functions.nlpPreprocessing import preprocess
from tqdm import tqdm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import time
from pprint import pprint


class WikiPageFinder(object):
    def __init__(self, name: str, language: str = 'en'):
        self.engine = wikipediaapi.Wikipedia(language)
        self.pagename = name
        self.page_text = None
        self.page_links = None
        self.page = None

    def download_page(self, cache: dict, preprocess_text=True) -> None:
        """Download a wikipedia page or retrieve it from cache.

        :param cache: cache where the pages are stored that were downloaded before.
        :type cache: dict
        :return: void
        :rtype: None
        """
        assert self.pagename, "Page name is not set"

        if self.pagename in cache.cache.keys():
            page = cache.cache[self.pagename].data
            cache.update(self.pagename)
        else:
            newPage = self.engine.page(self.pagename)

            if not newPage.exists():
                print(f"!!! '{self.pagename}' Cannot be found (anymore)!")
                return None

            text = newPage.text
            if preprocess_text:
                text = preprocess(text)

            page = pageData(self.pagename, text,
                            list(newPage.links.keys()))

            cache.add(page)

        # print((page.text))
        self.page = page

    def get_text(self) -> str:
        """Get the text of the wikipedia article

        :return: text of the wikipedia page.
        :rtype: str
        """
        try:
            return self.page.text
        except Exception as e:
            print(e)
            print(dir(self))
            # input()

    def get_links(self) -> list:
        """Returns a list of strings containing the names of the articles that the current article links to.

        :return: a list of strings containing the names of the articles that the current article links to.
        :rtype: list
        """
        return self.page.links

    def get_child_pages(self, cache: dict, multithread: bool = False, maxdownload=150) -> list:
        """retrieve all the pages the current page links to

        :param PAGECACHE: cache whith pages that were downloaded before.
        :type PAGECACHE: dict
        :param multithread: whether or not to use multithreading for downloading. (Does currently not work yet.), defaults to False
        :type multithread: bool, optional
        :return: list of child pages.
        :rtype: list
        """
        links = self.get_links()
        child_pages = []
        links_sample = random.sample(links, min(len(links), maxdownload))

        if multithread:
            print("Download multithread")
            myPool = ThreadPool(5)
            child_pages = myPool.map(lambda x: WikiPageFinder(
                x).download_page(cache), links_sample)
        else:
            print(f"Download pages ({maxdownload}/{len(links)}).")
            for link in tqdm(links_sample):

                myPage = WikiPageFinder(link)
                myPage.download_page(cache)
                if myPage:
                    child_pages.append(myPage)
                else:
                    print(f"{link} does not exist")

        return child_pages

    def build_vectorizer(self, child_pages: list) -> TfidfVectorizer:
        """a fitted vectorizer that is fitted on all the child pages.

        :param child_pages: list of child pages.
        :type child_pages: list
        :return: A fitted vectorizer.
        :rtype: TfidfVectorizer
        """
        texts = [child.get_text() for child in child_pages]
        
        # remove none values from texts
        texts = [text for text in texts if text]

        vectorizer = TfidfVectorizer()
        vectorizer.fit(texts)
        return vectorizer

    def get_nearest_neighbour(self, other: object, vectorizer: TfidfVectorizer) -> np.array:
        """Gets a sorted list ordered from most similar to least similar to the other page.

        :param other: other page that all pages are compared to
        :type other: object
        :param vectorizer: a fitted tf-idf vectorizer.
        :type vectorizer: TfidfVectorizer
        :return: An ordered list of wikipedia pages.
        :rtype: np.array
        """
        other_text = other.get_text()
        other_vector = vectorizer.transform([other_text])

        child_vectors = vectorizer.transform(
            [page.get_text() for page in self.child_pages if page.get_text()])
        # print(child_vectors.shape)
        distances = cosine_distances(other_vector, child_vectors)[0]

        closest_pages_i = np.argsort(distances)
        closest_pages = np.array(self.child_pages)[closest_pages_i]

        return closest_pages

    def get_closest_pages(self, endPage: object, cache: dict, method: str = 'tfidf') -> np.array:
        """Gets a sorted list ordered from most similar to least similar to the other page.

        :param endPage: the page you want to work towards.
        :type endPage: object
        :param PAGECACHE: cache whith pages that were downloaded before.
        :type PAGECACHE: dict
        :param cache_json_file: the file to which the pagecache will be saved
        :type cache_json_file: str
        :param method: the method that is used to compare the poages. Currently only tf-idf is implemented, defaults to 'tfidf'
        :type method: str, optional
        :return: An ordered list of wikipedia pages.
        :rtype: np.array
        """
        child_pages = self.get_child_pages(cache)

        self.child_pages = [
            page for page in child_pages if hasattr(page, 'page')]

        vectorizer = self.build_vectorizer(self.child_pages)
        closest_pages = self.get_nearest_neighbour(endPage, vectorizer)
        return closest_pages
