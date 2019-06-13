import csv
"""
This module writes Api objects (defined in this project only) to a csv file

Created by Chris Crabtree 6/10/2019
"""


def write_class(api_class, csv_writer):
    """
    Formats and writes an ApiClass object to a csv file

    :param api_class: An ApiClass to be written
    :type api_class: ApiClass
    :param csv_writer: Writer object to write formatted info
    :type csv_writer: csv.Writer
    :return:
    """
    row1 = ["", ""]
    name = api_class.name
    if api_class.name is not None:
        name = api_class.name.strip()
    row1.append(name)
    description = api_class.description
    if api_class.description is not None:
        description = api_class.description.strip()
    row1.append(description)
    csv_writer.writerow(row1)

    for method in api_class.methods:
        row_temp = ["","","",method.name,method.description,method.parameters, method.returns]
        csv_writer.writerow(row_temp)

    # Add marker to aid in reading csv
    csv_writer.writerow(["","","","end_of_methods"])



def write_package_info(package, csv_writer):
    """
    Formats and writes ApiPackage object info to a csv file

    :param package: An ApiPackage to be written
    :type package: ApiPackage
    :param csv_writer: Writer object to write formatted info
    :type csv_writer: csv.Writer
    :return:
    """
    row = [""]
    row.append(package.name)
    row.append(package.description)
    row.append(package.number_of_class_urls)
    for bad_read in package.bad_class_reads:
        row.append(bad_read)
    csv_writer.writerow(row)


def write_to_csv(filename, library):
    """
    Formats and writes an ApiLibrary object to a csv file. File path is indicated by the "filename" parameter

    :param library: An ApiClass to be written
    :type library: ApiClass
    :param filename: path to file to save csv file
    :type filename: str
    :return:
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as save_file:
            csv_writer = csv.writer(save_file, dialect="excel")
            row = [str(library.name), str(len(library.packages))]
            csv_writer.writerow(row)
            for package in library.packages:
                write_package_info(package, csv_writer)
                for api_class in package.classes:
                    write_class(api_class, csv_writer)

                # Add markers to aid in reading csv
                csv_writer.writerow(["","","end_of_classes"])
            csv_writer.writerow(["", "end_of_packages"])

    except Exception as e:
        print("Error in opening/writing to "+str(filename))
        print(e)



