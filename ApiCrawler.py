import requests
from bs4 import BeautifulSoup
from DocumentExtractor import get_documentation
import re

def get_api_package_urls(library_url):
    base_url = re.sub(r"(.*\.com).*", r"\1", library_url)
    #Query server at url
    result = requests.get(library_url)

    if result.status_code != 200:
        print("Error: request to " + str(library_url) + " was not successful")
        return None

    #Soupify html from result
    soup = BeautifulSoup(result.content, "html.parser")

    #Find table of packages
    table_of_packages = soup.find("h1", text="Package Index").find_next_sibling("table")

    package_urls = []

    #Loop through table to get the url for each package
    for row_tag in table_of_packages.find_all("tr"):
        first_column_tag = row_tag.find("td")
        if first_column_tag is None:
            continue

        href = first_column_tag.find("a")
        if href is None:
            continue

        new_package_url =str(base_url)+str(href.attrs["href"])
        package_urls.append(new_package_url)

    return package_urls


def get_api_class_urls(package_url):
    base_url = re.sub(r"(.*\.com).*", r"\1",package_url)
    #Make new query to server at new url
    result = requests.get(package_url)

    if result.status_code != 200:
        print("Error: request to "+str(package_url)+" was not successful")
        return None

    #Soupify html doc from response
    soup = BeautifulSoup(result.content, "html.parser")

    #Locate class list table and error check
    tag = soup.find("div",itemtype="http://developers.google.com/ReferenceObject")
    if tag == None:
        return None
    tag = tag.find("h2", string="Classes")
    if tag == None:
        return None
    table_of_classes = tag.find_next_sibling("table")
    if table_of_classes == None:
        return None

    class_urls = []

    #Get class urls
    for row in table_of_classes.find_all("tr"):
        href = row.find("a")
        if href == None:
            continue
        new_url = str(base_url)+(href.attrs["href"])
        class_urls.append(new_url)

    return class_urls

def scrape_class_url(class_url):
    result = requests.get(class_url)
    if result.status_code != 200:
        print("Error: request to "+str(class_url)+" was not successful")
        return None
    return get_documentation(result.content)
