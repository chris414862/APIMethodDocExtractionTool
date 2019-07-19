import csv
import os
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

    for method in sorted(api_class.methods, key=lambda method: method.name):
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


def write_to_csv_for_numpy(library):
    try:
        dir_name = library.name
        filename = dir_name+".csv"
        # package_descrip_dir = dir_name+"/package_descriptions"
        # class_descrip_dir =dir_name + "/class_descriptions"
        # methods_dir =dir_name + "/methods"
        # errors_dir =dir_name + "/errors"
        #
        try:
            os.mkdir(dir_name)
        except:
            pass
        # try:
        #     os.mkdir(dir_name+"/package_descriptions")
        # except:
        #     pass
        # try:
        #     os.mkdir(dir_name + "/class_descriptions")
        # except:
        #     pass
        # try:
        #     os.mkdir(dir_name + "/methods")
        # except:
        #     pass
        # try:
        #     os.mkdir(dir_name + "/errors")
        # except:
        #     pass


        package_descrip_filename = dir_name+"/package_descriptions_" +filename
        with open(package_descrip_filename, 'w', newline='', encoding='utf-8') as f_package_descrip:
            try:
                class_descrip_filename = dir_name +"/class_descriptions_"+ filename
                with open(class_descrip_filename, 'w', newline='', encoding='utf-8') as f_class_descrip:
                    try:
                        with open(dir_name+"/"+filename, 'w', newline='', encoding='utf-8') as f_methods:
                            f_error = open(dir_name+"/errors_"+filename, 'w',newline="",encoding='utf-8')

                            # Open csv writers
                            package_writer = csv.writer(f_package_descrip, dialect="excel")
                            method_writer = csv.writer(f_methods, dialect="excel")
                            class_writer = csv.writer(f_class_descrip, dialect="excel")
                            error_writer = csv.writer(f_error, dialect="excel")

                            for package in library.packages:
                                # Assemble rows for package descriptions and errors
                                row_package = [library.name,package.name, len(package.classes)
                                              ,package.description.strip()]


                                row_errors = [library.name, package.name]
                                row_errors.extend([bad_read for bad_read in package.bad_class_reads])

                                # Write to package file and error file
                                package_writer.writerow(row_package)
                                if len(row_errors) > 2:
                                    error_writer.writerow(row_errors)

                                # Loop through clases
                                for api_class in package.classes:
                                    # Assemble rows for class descriptions
                                    row_class = [library.name,package.name, api_class.name, len(api_class.methods)
                                                , api_class.description.strip()]

                                    # Write to class file
                                    class_writer.writerow(row_class)
                                    for method in api_class.methods:
                                        # Assemble rows for class descriptions
                                        row_method = [library.name, package.name, api_class.name, method.name
                                                      ,method.description.strip(), method.parameters.strip()
                                                      , method.returns.strip()]

                                        # Write to method file
                                        method_writer.writerow(row_method)


                            f_error.close()
                    except Exception as e:
                        print("Error in opening/writing to " + str(package_descrip_filename))
                        raise

            except Exception as e:
                print("Error in opening/writing to " + str(package_descrip_filename))
                raise
            # csv_writer = csv.writer(save_file, dialect="excel")

            # row = [str(library.name), str(len(library.packages))]
            # csv_writer.writerow(row)
            # for package in library.packages:
            #     write_package_info_for_numpy(package, csv_writer)
            #     for api_class in package.classes:
            #         write_class(api_class, csv_writer)
            #
            #     # Add markers to aid in reading csv
            #     csv_writer.writerow(["", "", "end_of_classes"])
            # csv_writer.writerow(["", "end_of_packages"])

    except Exception as e:
        print("Error in opening/writing to " + str(filename))
        raise


def write_to_csv(library, heirarchical=False):
    """
    Formats and writes an ApiLibrary object to a csv file. File path is indicated by the "filename" parameter

    :param library: An ApiClass to be written
    :type library: ApiClass
    :param filename: path to file to save csv file
    :type filename: str
    :return:
    """
    if heirarchical:
        dir_name = library.name
        filename = dir_name + ".csv"
        try:
            os.mkdir(dir_name)
        except:
            pass
        try:
            with open(dir_name+"/"+filename, 'w', newline='', encoding='utf-8') as save_file:
                csv_writer = csv.writer(save_file, dialect="excel")
                row = [str(library.name), str(len(library.packages))]
                csv_writer.writerow(row)
                for package in sorted(library.packages, key=lambda package: package.name):
                    write_package_info(package, csv_writer)
                    for api_class in sorted(package.classes, key=lambda api_class : api_class.name):
                        write_class(api_class, csv_writer)

                    # Add markers to aid in reading csv
                    csv_writer.writerow(["","","end_of_classes"])
                csv_writer.writerow(["", "end_of_packages"])

        except Exception as e:
            print("Error in opening/writing to "+str(filename))
            print(e)

    else:
        write_to_csv_for_numpy(library)


