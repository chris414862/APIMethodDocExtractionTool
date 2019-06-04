import requests
from bs4 import BeautifulSoup
from DocumentExtractor import get_documentation

#Start with urls
url = "https://developer.android.com/reference/packages"
base_url = "https://developer.android.com"

#Query server at url
result = requests.get(url)

if result.status_code != 200:
    print("Error: request to "+str(url)+" was not successful")

#Soupify html from result
soup = BeautifulSoup(result.content, "html.parser")
#print(soup.prettify())
#Find table of packages
table_of_packages = soup.find("h1", text="Package Index").parent
#print(table_of_packages.prettify())

i=0
api_classes = []
#Loop through table to get the url for each package
for href in table_of_packages.find_all("a"):
    if i == 2:
        break
    if href.string == "API classes":
        continue
    print("Getting Package:")
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
    #j=1
    for row in table_of_classes.find_all("tr"):
        #if j == 4:
        #    break
        href = row.find("a")
        if href == None:
            continue
        new_url = str(base_url)+(href.attrs["href"])
        print("\tGetting class:")
        print("\t"+str(new_url))
        class_html = requests.get(new_url)
        class_api_doc = get_documentation(class_html.content)
        #print(class_api_doc.string())
        api_classes.append(class_api_doc)
        #j+=1
    #print()
    i+=1

for api_class in api_classes:
    print(api_class.string())
    print("++++++++++")