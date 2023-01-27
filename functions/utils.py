import os


def show_route(route: list):
    """shows the route

    :param route: list countaining he names of the pages that were visited.
    :type route: list
    """
    maxlen = max([len(name) for name in route])
    print("Route:")
    for i, page in enumerate(route, start=1):
        print(
            f"{i:.<3} {page:.<50} en.wikipedia.org/wiki/{page.replace(' ', '_')}")
