import grequests
from Model.ApiPackage import ApiPackage
from Libs.ApiCrawler import get_urls
from Model.ApiClass import class_name_from_url
from Libs.DocumentExtractor import get_documentation
from Libs.MySerializer import serialize_package, unserialize_package
"""
This module defines the child processes for ApiDocExtract and their return values. Each process is responsible for 
scraping one Api package from a url specified by an argument. Separate processes are used to speed up execution. 
Processes are used instead of threads because the CPython interpreter is limited by a GIL (Global Interpreter Lock) that
prevents more than one thread from executing at one time. In this module, execution speed is further enhanced by using
"grequests" module instead of the standard "requests" module. "requests" blocks during each one of it's http requests,
not allowing for any additional http request to be sent until a response is received. "grequests" allows for multiple 
requests to be sent at one time.   

Created by Chris Crabtree 6/10/2019
"""


def my_process(*args):
    """
    Scrapes class urls from a package url, then scrapes all relevant documentation from each class url.

    :param args: List of arguments sent from main function
    :type args: list
    :return: Serialized version of ApiPackage object with scraped fields
    :rtype: str
    """
    # Get arguments
    process_id = args[0]
    package_url = args[1]
    verbose = args[2]
    library_name = args[3]
    max_packages = args[4]

    package = ApiPackage()
    package.set_package_name(package_url, library_name)
    if verbose:
        print("process_id: "+str(process_id)+"\npackage_url: "+str(package_url)+"\n\t"+str(process_id) +
              ": Scraping package: " + str(package.name))
    else:
        print(str(process_id) + ": Scraping package: " + str(package.name))

    # Get urls for each class in the package
    class_urls = get_urls(package_url, "classes", )

    if class_urls is None:
        if verbose:
            print("\tNo classes in package: "+package.name)
        package.number_of_class_urls = 0
        return serialize_package(package)

    # Send http request with "grequests"
    unsent_requests = (grequests.get(class_url) for class_url in class_urls)
    results = grequests.map(unsent_requests)
    package.number_of_class_urls = len(class_urls)

    # Loop through class urls and scrape info from each class
    if results is not None:
        for result in results:
            # Check for errors
            try:
                result.raise_for_status()
            except:
                print("Bad url read for class: "+class_name_from_url(result.url))
                if result.url not in package.bad_class_reads:
                    package.bad_class_reads.append(result.url)
                continue
            try:
                if verbose:
                    print("\t\t"+str(process_id)+": package: "+str(package.name)+": Scraping class: "
                                                                             + str(class_name_from_url(result.url)))
            except:
                print("Unknown error in package: "+str(package.name)+"\nresult from grequests:"+str(result))
                if result.url not in package.bad_class_reads:
                    package.bad_class_reads.append(result.url)
                continue

            # Scrape documentation from class url
            try:
                new_class = get_documentation(result.content)
                package.classes.append(new_class)
            except Exception as e:
                print("Exception in parsing of "+str(class_name_from_url(result.url)))
                if result.url not in package.bad_class_reads:
                    package.bad_class_reads.append(result.url)
                print(e)


    # Print results
    if verbose:
        print("\t"+str(package.name)+" results:")
        for api_class in package.classes:
            print("\t\t" + str(process_id) + ": package: "+str(package.name)+" class: " + api_class.name
                  + " number of methods: " + str( len(api_class.methods)))
    elif process_id == max_packages:
        print("Cleaning up packages. May take a moment...")

    return serialize_package(package)


def add_to_library(library, res):
    """
    This method is called each time an instantiation of my_process is completed. It returns an ApiLibrary object that
    has been unserialized.

    :param library: An ApiLibrary oject to fill with the return value from res
    :param res: A Future object that contains the result of a completed process (an ApiPackage object)
    :type res: concurrent.futures.Future
    :return: An ApiLibrary object with fields filled from unserialization
    :rtype: ApiLibrary
    """
    unserialized = unserialize_package(res.result())
    if unserialized is not None:
        library.packages.append(unserialized)
        #print(unserialized.string())



