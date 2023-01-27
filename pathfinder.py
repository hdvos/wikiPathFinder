from functions.wikiPageFinder import WikiPageFinder
from functions.wikiPageCache import wikiPageCache
from functions.utils import show_route


cache_json_file = "pagecache.json"

START = "Love"
END = "Apple"

START = START.replace('_', ' ')
END = END.replace('_', ' ')

MAXDOWNLOAD = 150

CACHE = wikiPageCache(cache_json_file)
CACHE.load()


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
