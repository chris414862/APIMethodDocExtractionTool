import requests
from bs4 import BeautifulSoup

#Start with urls
url = "https://developer.android.com/reference/android/support/packages"
base_url = "https://developer.android.com"

#Query server at url
result = requests.get("https://developer.android.com/reference/android/support/packages")

if result.status_code != 200:
    print("Error: request to "+str(url)+" was not successful")

#Soupify html from result
soup = BeautifulSoup(result.content, "html.parser")

#Find table of packages
table_of_packages = soup.find("div", id="doc-api-level").find_next_sibling("table")

#Loop through table to get the url for each class
for href in table_of_packages.find_all("a"):
    print("Getting class")
    print(str(base_url)+str(href.attrs["href"]+"\n"))

    #Make new query to server at new url
    url = str(base_url)+str(href.attrs["href"])
    result = requests.get(url)

    if result.status_code != 200:
        print("Error: request to "+str(url)+" was not successful")
        continue

    #Soupify html doc from response
    soup = BeautifulSoup(result.content, "html.parser")

    #Locate class list table and error check
    tag = soup.find("div",itemtype="http://developers.google.com/ReferenceObject")
    if tag == None:
        continue
    tag = tag.find("h2", string="Classes")
    if tag == None:
        continue
    table_of_classes = tag.find_next_sibling("table")
    if table_of_classes == None:
        continue

    #Get html doc for each class then get documentation with DocumentExtractor
    #TODO: finish this section
    for row in table_of_classes.find_all("tr"):
        href = row.find("a")
        if href == None:
            continue
        print(str(base_url)+(href.attrs["href"]))
    print()