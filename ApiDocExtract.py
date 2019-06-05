import sys
from Scripts.ApiCrawler import get_urls, scrape_class_url
from Model.ApiLibrary import ApiLibrary
from Model.ApiPackage import ApiPackage
from Model.ApiClass import class_name_from_url
import random
"""
This module scrapes API class and method information from an API library and stores the info in csv file
The first argument should be the library url. Specifically, the package index page of the library. The second 
argument should be the name of the output file containing all of the scraped information

Created by Chris Crabtree 6/5/2019
"""
# Get url from arguments
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    print("Usage: "+str(sys.argv[0])+" [url of library]")

# Initialize library
library = ApiLibrary()
library.set_library_name(url)
print("Starting scrape of library: " + str(library.name))

# Get urls for each package in library
package_urls = get_urls(url, "packages")


i = 0
# Loop through package urls and scrape classes in each package
for package_url in package_urls:
    if i == 2:
        break

    # Intitialize package
    package = ApiPackage()
    package.set_package_name(package_url)
    print("\tScraping package: "+str(package.name))

    # Get urls for each class in the package
    class_urls = get_urls(package_url, "classes")

    # Loop through class urls scrape info from each class
    if class_urls is not None:
        for class_url in class_urls:
            print("\t\tScraping class: "+str(class_name_from_url(class_url)))
            new_class = scrape_class_url(class_url)
            package.classes.append(new_class)
        library.packages.append(package)

    # Report classes scraped and give sample
    print("\tNumber of classes in "+str(package.name)+": "+ str(len(package.classes)))
    if len(package.classes) > 0:
        index = random.randint(0,len(package.classes)-1)
        print("\tSample from scrapes(index "+str(index)+"):")
        print(package.classes[index].string())

    print()
    i += 1

# for package in library:
#     for api_class in package:
#         print(api_class.string())

