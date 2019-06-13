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

def process_args():
    if len(sys.argv) < 3:
        print("Usage: "+str(sys.argv[0])+" [url of library] [filename to save to]" )
        sys.exit()

    url = sys.argv[1]
    filename = sys.argv[2]
    verbose = False
    append = False
    for arg in sys.argv:
        if arg == "-v":
            verbose = True
        if arg == "-a":
            append = True

    return url, filename, verbose, append


def error_check(library):
    error_flag = 0
    for package in library.packages:
        if len(package.bad_class_reads) > 0:
            error_flag = 1
            print("Error in package " + str(package.name))
            for bad_read in package.bad_class_reads:
                print("\tDid not read url properly: "+ str(bad_read))

    if error_flag:
        print("Error occured in network. Consider re-running program")
    else:
        print("All clear")


def main():
    (url, filename, verbose, append) = process_args()

    # Initialize library
    library = ApiLibrary()
    library.set_library_name(url)
    print("Starting scrape of library: " + str(library.name))

    # Get urls for each package in library
    package_urls = get_urls(url, "packages")
    total_packages = len(package_urls)
    print("Number of packages: "+str(total_packages))

    # Number of processes to utilize
    max_workers = 10
    if total_packages < max_workers:
        max_workers = total_packages

    # Execute processes
    packages_completed = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(package_urls)):
            process_id = i+1
            future = executor.submit(my_process, process_id, package_urls[i], verbose, library.name, total_packages)
            future.add_done_callback(functools.partial(add_to_library, library))

    print("Final package count: "+str(len(library.packages)))

    # Check for bad url reads
    print("Checking results...")
    error_check(library)

    print("Saving library to " + filename)
    write_to_csv(filename, library)


if __name__ == "__main__":
    freeze_support()
    main()
