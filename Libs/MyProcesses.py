import grequests
import threading
from Model.ApiPackage import ApiPackage
from Libs.ApiCrawler import get_urls, scrape_class_url
from Model.ApiClass import class_name_from_url, ApiClass
from Libs.DocumentExtractor import get_documentation
import pickle
import sys

def my_thread(*args):
    sys.setrecursionlimit(25000)

    thread_id = args[0]
    package_url = args[1]
    package = ApiPackage()
    package.set_package_name(package_url)
    print("thread_id: "+str(thread_id)+"\npackage_url: "+str(package_url)+"\n\t"+str(thread_id) +
          ": Scraping package: "+str(package.name))

    # Get urls for each class in the package
    class_urls = get_urls(package_url, "classes", )
    if class_urls is None:
        print("\tNo classes in package: "+package.name)
        return package

    unsent_requests = (grequests.get(class_url) for class_url in class_urls)
    results = grequests.map(unsent_requests)
    package.number_of_results = len(results)
    # Loop through class urls scrape info from each class
    if results is not None:
        for result in results:
            try:
                result.raise_for_status()
            except:
                print("Bad url read for class: "+class_name_from_url(result.url))
                package.bad_class_reads.append(result.url)
            try:
                print("\t\t"+str(thread_id+1)+": package: "+str(package.name)+": Scraping class: "
                                                                             + str(class_name_from_url(result.url)))
            except:
                print("Unknown error in package: "+str(package.name))
                continue
            new_class = get_documentation(result.content)
            package.classes.append(new_class)
    print("\t"+str(package.name)+" results:")
    for api_class in package.classes:
        print("\t\t" + str(thread_id + 1) + ": package: "+str(package.name)+"class: " + api_class.name
              + " number of methods: " + str( len(api_class.methods)))

    ret = ""
    for api_class in package.classes:
        ret += api_class.string()
    return ret

def add_to_library(library2, res):
    print(res.result())
    # res2 = pickle.load(res.result())
    # print(res.result())
    #result = res.result()
    #library2.packages.append(result)
    # print("result test: package name is "+str(result.name))

