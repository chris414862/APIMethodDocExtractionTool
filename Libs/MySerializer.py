from Model.ApiPackage import ApiPackage
from Model.ApiClass import ApiClass
from Model.ApiMethod import ApiMethod
import re
"""
This module serializes and unserializes Api objects (defined in this project only) in order to facilitate inter-process
communication. Serialization is a process that converts a data structure to a format that can be stored in a file or 
transported across a network. Serialization is necessary for this project because for some reason both the serializer
used with the ProcessPoolExecutor module and the standard python serializer, pickle, are not able to serialize objects. 
Serialization is necessary when conducting inter-process communication (e.g. when sending parameters or return values 
to other processes). 

Created by Chris Crabtree 6/10/2019 
"""


def serialize_method(method):
    """
    Turns the information in an ApiMethod object into a string to be sent through a pipe during multiprocessing.

    :param api_class: An ApiMethod to be serialized
    :type api_class: ApiMethod
    :return: A string containing all the information of the ApiMethod
    :rtype: str
    """
    ret = ""
    if method is None:
        return ret

    # Add "!1*" as a delimiter between method info to facilitate unserialization
    ret = str(method.name) + "!1*" + str(method.description) + "!1*" + str(method.parameters)
    ret += "!1*" + str(method.returns)
    return str(ret)


def serialize_class(api_class):
    """
    Turns the information in an ApiClass object into a string to be sent through a pipe during multiprocessing.

    :param api_class: An ApiClass to be serialized
    :type api_class: ApiClass
    :return: A string containing all the information of the ApiClass
    :rtype: str
    """

    if api_class is None:
        return ""

    # Add "!2*" as a delimiter to facilitate unserialization
    line1 = str(api_class.name) + "!2*"
    line2 = str(api_class.description) + "!2*"

    method_strings = ""
    if len(api_class.methods) > 0:
        method_strings += serialize_method(api_class.methods[0])

        # Add "&*-" as a delimiter between methods to facilitate unserialization
        for i in range(1,len(api_class.methods)):
            method_strings += "&*-" + serialize_method(api_class.methods[i])

    return str(line1)+str(line2)+str(method_strings)


def serialize_package(package):
    """
    Turns the information in an ApiPackage object into a string to be sent through a pipe during multiprocessing.

    :param package: An ApiPackage to be serialized
    :type package: ApiPackage
    :return: A string containing all the information of the ApiPackage
    :rtype: str
    """
    if package is None:
        return ""
    line1 = str(package.name)+"~~"+str(package.number_of_class_urls)+"~~"+str(len(package.classes))+"!3*"
    line2 = ""
    if len(package.bad_class_reads) > 0:
        line2 = package.bad_class_reads[0]
        for i in range(1,len(package.bad_class_reads)):
            line2 += "~~" + str(package.bad_class_reads[i])
    line2 += "!3*"
    line3 = ""
    if package.description is not None and package.description != "":
        line3 += package.description
    line3 += "!3*"
    class_strings = ""
    if len(package.classes) > 0:
        class_strings = serialize_class(package.classes[0])
        for i in range(1, len(package.classes)):
            class_strings += "$%^"+ serialize_class(package.classes[i])

    return str(line1)+str(line2)+str(line3)+str(class_strings)


def unserialize_method(method_string):
    """
    Turns a formatted string into an ApiMethod object

    :param method_string: String containing info for ApiMethod object
    :type method_string: str
    :return: ApiMethod object with completed fields
    :rtype: ApiMethod
    """
    if method_string is None:
        return None
    if method_string == "":
        return None
    ret_method = ApiMethod()
    lines = method_string.split("!1*")
    ret_method.name = lines[0]
    ret_method.description = lines[1]
    ret_method.parameters = lines[2]
    ret_method.returns = lines[3]
    return ret_method


def unserialize_class(api_class_string):
    """
    Turns a formatted string into an ApiClass object

    :param api_class_string: String containing info for ApiClass object
    :type api_class_string: str
    :return: ApiClass object with completed fields
    :rtype: ApiClass
    """
    if api_class_string is None:
        return None
    if api_class_string == "":
        return None
    ret_class = ApiClass()
    lines = api_class_string.split("!2*")
    ret_class.name = str(lines[0])
    ret_class.description = str(lines[1])

    method_strings = lines[2].split("&*-")
    for method_string in method_strings:
        unserialized = unserialize_method(method_string)
        if unserialized is not None:
            ret_class.methods.append(unserialized)

    return ret_class


def unserialize_package(package_str):
    """
    Turns a formatted string into an ApiPackage object. Basically reversing the actions taken in serialize_package()

    :param package_string: String containing info for ApiClass object
    :type api_class_string: str
    :return: ApiClass object with completed fields
    :rtype: ApiClass
    """
    if package_str is None:
        return None
    if package_str == "":
        return None
    ret_package = ApiPackage()

    lines = package_str.split("!3*")

    # line 1: package name ~~ number of class urls ~~ num classes
    package_info = lines[0].split("~~")
    ret_package.name = str(package_info[0])
    ret_package.number_of_class_urls = int(package_info[1])
    num_classes = int(package_info[2])

    # line 2: bad_class_read 1 ~~ bad_class_read 2 ~~ ........
    for bad_class_read in lines[1].split("~~"):
        if not re.search(r"^\s*$", bad_class_read):
            ret_package.bad_class_reads.append(bad_class_read)

    # line 3 package description
    ret_package.description = lines[2]

    api_classes_strings = lines[3].split("$%^")
    for api_class_string in api_classes_strings:
        unserialized = unserialize_class(api_class_string)
        if unserialized is not None:
            ret_package.classes.append(unserialized)
            #print(unserialized.string())

    return ret_package

