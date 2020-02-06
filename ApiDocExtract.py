from Libs.MyProcesses import my_process, add_to_library
from Libs.ApiCrawler import get_urls, scrape_class_url
from Libs.MyWriter import write_to_csv
from Model.ApiLibrary import ApiLibrary
from Model.ApiClass import class_name_from_url
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

    url = sys.argv  [1]

    verbose = False
    append = False
    api_level = -1
    workers = 10
    for i,arg in enumerate(sys.argv):
        if arg == "-v":
            verbose = True
        if arg == "-a":
            append = True

        # Specify up to what api level should be scraped. Argument should be of the form "-24" for up to api level 24
        if len(arg) > 1 and arg[0] == "-" and arg[1:].isdigit():
            try:
                api_level = int(arg[1:])
            except:
                print("Fourth argument is optional but should be an integer if included")
                sys.exit()
        if arg == "-w":
            if len(sys.argv) < i+1:
                print("There should be an integer after -w")
                sys.exit()
            else:
                try:
                    workers = int(sys.argv[i+1])
                except:
                    print("There should be an integer after -w")
                    sys.exit()

    return url, verbose, append, api_level, workers


def error_check(library, api_level=-1):
    print("Total bad url requests: ", end="")
    bad_url_count = 0
    for package in library.packages:
        bad_url_count += len(package.bad_class_reads)
    print(bad_url_count)

    for package in library.packages:
        if len(package.bad_class_reads) > 0:
            print("Error in package " + str(package.name))

        urls_to_remove_from_bad_list = []
        for bad_url in package.bad_class_reads:
            print("\tDid not read url properly: " + str(bad_url))
            print("\tAttempting to resolve...")
            try:
                fixed_class = scrape_class_url(bad_url,api_level)
                if fixed_class == -1:
                    print("\t\t"+str(bad_url)+" was out of api range")
                    urls_to_remove_from_bad_list.append(bad_url)
                    continue
                elif fixed_class == None or fixed_class == -2:
                    raise
                else:
                    already_in = [api_class for api_class in package.classes if api_class.name == fixed_class.name]
                    if already_in is not None:
                        try:
                            package.classes.remove(already_in)
                        except:
                            pass
                    package.classes.append(fixed_class)
                    urls_to_remove_from_bad_list.append(bad_url)
                    #package.bad_class_reads.remove(bad_url)
                    print("\t\tResolved problem with",str(fixed_class.name))

            except Exception as e:
                print("\t\tCould not resolve problem with",str(bad_url))
                print("\t\t"+str(e))
                print("\t\tConsider re-running program")

        package.bad_class_reads = [url for url in package.bad_class_reads if url not in urls_to_remove_from_bad_list]
    print("Finished checking results")


    #     if len(package.bad_class_reads) > 0:
    #         error_flag = 1
    #         print("Error in package " + str(package.name))
    #         for bad_read in package.bad_class_reads:
    #
    #
    # if error_flag:
    #     print("Error occured in network. Consider re-running program")
    # else:
    #     print("All clear")


def main():
    (url, verbose, append, api_level, workers) = process_args()
    print(api_level)
    # Initialize library
    library = ApiLibrary()
    library.set_library_name(url)
    print("Starting scrape of library: " + str(library.name))

    # Get urls for each package in library
    package_urls = get_urls(url, "packages")
    for p in package_urls:
        print(p)
    total_packages = len(package_urls)

    # ##### Delete later
    # package_urls = ["https://developer.android.com/reference/android/app/admin/package-summary", "https://developer.android.com/reference/android/app/assist/package-summary"]
    # total_packages = len(package_urls)
    # print("Number of packages: "+str(total_packages))

    # Number of processes to utilize
    max_workers = workers
    if total_packages < max_workers:
        max_workers = total_packages

    # Execute processes
    packages_completed = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0,  len(package_urls)):
            process_id = i+1
            future = executor.submit(my_process, process_id, package_urls[i], verbose, library.name
                                     , total_packages, api_level)
            future.add_done_callback(functools.partial(add_to_library, library))

    print("Final package count: "+str(len(library.packages)))

    # Check for bad url reads
    print("Checking results...")
    error_check(library, api_level)

    print("Saving library files to " + library.name+"/")
    write_to_csv(library)


if __name__ == "__main__":
    freeze_support()
    main()
