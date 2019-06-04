import sys
from ApiCrawler import get_api_package_urls, get_api_class_urls, scrape_class_url
import random

#Start with urls
url = sys.argv[1]

package_urls = get_api_package_urls(url)
i = 0

library = []
for package_url in package_urls:
    if i == 2:
        break
    class_urls = get_api_class_urls(package_url)
    print("Scraping package: "+str(package_url))
    package = []
    for class_url in class_urls:
        print("\tScraping class: "+str(class_url))
        package.append(scrape_class_url(class_url))
    library.append(package)
    print()
    print("Sample from scrapes:")
    print(package[random.randint(0,len(package))].string())
    i+=1


