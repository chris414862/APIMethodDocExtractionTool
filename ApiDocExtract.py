from Libs.MyProcesses import my_process, add_to_library
from Libs.ApiCrawler import get_urls
from Libs.MyWriter import write_to_csv
from Model.ApiLibrary import ApiLibrary
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support
import functools
import sys
"""
This module scrapes API class and method information from an API library and stores the info in csv file
The first argument should be the library url. Specifically, the package index page of the library. The second 
argument should be the name of the output file containing all of the scraped information

Created by Chris Crabtree 6/5/2019
"""


def main():
    if len(sys.argv) > 2:
        url = sys.argv[1]
    else:
        print("Usage: "+str(sys.argv[0])+" [url of library] [filename to save to]" )
        sys.exit()

    # Initialize library
    library = ApiLibrary()
    library.set_library_name(url)
    print("Starting scrape of library: " + str(library.name))

    # Get urls for each package in library
    package_urls = get_urls(url, "packages")
    print("Number of packages: "+str(len(package_urls)))

    # Number of processes to utilize
    max_workers = 15

    # Execute processes
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(package_urls)):
            process_id = i+1
            verbose = 0
            future = executor.submit(my_process, process_id, package_urls[i], verbose)
            future.add_done_callback(functools.partial(add_to_library, library))

    print("Final package count: "+str(len(library.packages)))
    print("Saving library to " + sys.argv[2])
    write_to_csv(sys.argv[2], library)


if __name__ == "__main__":
    freeze_support()
    main()
