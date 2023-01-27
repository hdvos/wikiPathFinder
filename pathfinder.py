from functions.wikiPageFinder import WikiPageFinder
from functions.wikiPageCache import wikiPageCache
from functions.utils import show_route
import argparse

# Default values
cache_json_file = "pagecache.json"
START = "Love"
END = "Apple"
START = START.replace('_', ' ')
END = END.replace('_', ' ')
MAXDOWNLOAD = 150
CACHE = wikiPageCache(cache_json_file)
CACHE.load()

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", help="The start page", default=START, type=str)
parser.add_argument("-e", "--end", help="The end page", default=END, type=str)
parser.add_argument("-c", "--cache", help="The cache file", default=cache_json_file, type=str)
parser.add_argument("-m", "--max", help="The maximum number of pages to download", default=MAXDOWNLOAD, type=int)
args = parser.parse_args()

# Set the values
START = args.start
END = args.end
MAXDOWNLOAD = args.max
cache_json_file = args.cache
MAXDOWNLOAD = args.max

def main():
    """Main function

    :raises RuntimeError: When no path can be found
    """
    # Retrieve the end page.
    end_page = WikiPageFinder(END)
    end_page.download_page(CACHE)

    # Retrieve the start page.
    current_page = WikiPageFinder(START)
    current_page.download_page(CACHE)

    CACHE.save()

    # The route is a list of pages that will be used to get from the start to the end page.
    route = [current_page.pagename]

    # While the end page is not in the links of the current page, keep searching.
    while not end_page.pagename in current_page.get_links():
        closest_pages = current_page.get_closest_pages(
            end_page, CACHE)

        i = 0
        current_page = closest_pages[i]
        i += 1
        while current_page.pagename in route:
            try:
                current_page = closest_pages[i]
                i += 1
            except IndexError:
                raise RuntimeError("All possibilities exhausted")

        current_page.download_page(CACHE)
        print(f"\n\nCurrent page: {current_page.pagename}")
        route.append(current_page.pagename)
        CACHE.save()

    route.append(end_page.pagename)

    show_route(route)


if __name__ == "__main__":
    main()
