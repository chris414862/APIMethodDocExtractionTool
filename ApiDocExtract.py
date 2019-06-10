import sys
from Libs.MyProcesses import my_thread, add_to_library
from Libs.ApiCrawler import get_urls
from Model.ApiLibrary import ApiLibrary
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool, freeze_support
from concurrent import futures
import functools
import sys


"""
This module scrapes API class and method information from an API library and stores the info in csv file
The first argument should be the library url. Specifically, the package index page of the library. The second 
argument should be the name of the output file containing all of the scraped information

Created by Chris Crabtree 6/5/2019
"""

# Get url from arguments
def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Usage: "+str(sys.argv[0])+" [url of library]")

    sys.setrecursionlimit(25000)
    # Initialize library
    library = ApiLibrary()
    library.set_library_name(url)
    print("Starting scrape of library: " + str(library.name))

    # Get urls for each package in library
    thread_lock = threading.Lock()
    package_urls = get_urls(url, "packages")

    print("Number of packages: "+str(len(package_urls)))
    max_workers = 1
    # with Pool(processes=max_workers) as p:
    #     args_list = list()
    #     for i in range(0, 10):
    #         args_list.append((i,package_urls[i]))
    #     future = p.starmap(my_thread, args_list)

    futures2 = list()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:

        for i in range(0,1):
            future = executor.submit(my_thread, i, package_urls[i])
            #futures2.append(future)
            #print(future)
            future.add_done_callback(functools.partial(add_to_library, library))

    print("Final package count: "+str(len(library.packages)))
    # for future in futures2:
    #     try:
    #         future.result()
    #     except futures.process.BrokenProcessPool as e:
    #         print('could not start new tasks: {}'.format(e))
    #     #print(future)


if __name__ == "__main__":
    freeze_support()
    main()
