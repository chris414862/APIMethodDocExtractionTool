import requests
from bs4 import BeautifulSoup
from Libs.DocumentExtractor import get_documentation
import re
"""
This module contains methods to scrape different types of information from websites

Created by Chris Crabtree 6/5/2019
"""


def get_urls(orig_url, type_to_get="packages"):
    """
    Returns a list of urls. This method does the networking work for both get_api_package_urls and get_api_class_urls.

    :param orig_url: url of page to get other urls from
    :type orig_url: str
    :param type_to_get: string that indicates what type of html document will be scraping
    :type type_to_get: str
    :return: list of urls
    :rtype list
    """
    base_url = re.sub(r"(.*\.com).*", r"\1", orig_url)
    # Query server at url
    repeat_count = 3
    while repeat_count > 0:
        result = requests.get(orig_url)
        if result.status_code != 200:
            if repeat_count > 0:
                repeat_count -= 1
                continue
            else:
                print("Error: request to " + str(orig_url) + " was not successful(from get_urls)")
                return None
        else:
            break


    # Soupify html from result
    soup = BeautifulSoup(result.content, "html.parser")

    if type_to_get == "packages":
        return get_api_package_urls(soup, base_url)
    elif type_to_get == "classes":
        return get_api_class_urls(soup, base_url)


def get_api_package_urls(soup, base_url):
    """


    :param soup: parsed html document
    :type BeautifulSoup
    :param base_url: url to attach url parts in soup to
    :return: list of package urls
    :rtype list
    """
    # Find table of packages
    table_of_packages = soup.find("h1", text="Package Index").find_next_sibling("table")

    package_urls = []

    # Loop through table to get the url for each package
    for row_tag in table_of_packages.find_all("tr"):
        first_column_tag = row_tag.find("td")
        if first_column_tag is None:
            continue

        href = first_column_tag.find("a")
        if href is None:
            continue

        new_package_url = str(base_url) + str(href.attrs["href"])
        package_urls.append(new_package_url)

    return package_urls


def get_api_class_urls(soup, base_url):
    """
    Returns list of class urls contained in soup(parsed html document). Attributes in soup only contain part of a url.
    This part must be attached to a base url which is sent in as a parameter

    :param soup: parsed html document
    :type soup: BeautifulSoup
    :param base_url: url to attach url parts in soup to
    :return: list of class urls
    :rtype list
    """
    # Locate class list table and error check
    tag = soup.find("div",itemtype="http://developers.google.com/ReferenceObject")
    if tag == None:
        return None
    tag = tag.find("h2", string="Classes")
    if tag == None:
        return None
    table_of_classes = tag.find_next_sibling("table")
    if table_of_classes is None:
        return None

    class_urls = []

    # Get class urls
    for row in table_of_classes.find_all("tr"):
        href = row.find("a")
        if href == None:
            continue
        new_url = str(base_url)+(href.attrs["href"])
        class_urls.append(new_url)

    return class_urls


def scrape_class_url(class_url, api_level=-1):
    """
    Scrapes the class_url for class and method descriptions/info then returns a fully populated ApiClass object

    :param class_url: url of class to scrape
    :type class_url: str
    :return: ApiClass object with fully populated fields, including all methods
    :rtype ApiClass
    """

    # Query server at url
    repeat_count = 5
    while repeat_count > 0:
        result = requests.get(class_url, timeout=5)
        if result.status_code != 200:
            print('\tCould not read url.')
            if repeat_count > 0:
                print("\tAttempting again")
                repeat_count -= 1
                continue
            else:
                print("Error: request to " + str(class_url) + " was not successful(from get_urls)")
                return None
        else:
            break


    doc = get_documentation(result.content, api_level)
    if doc != -1:
        return doc
    else:
        return -1
