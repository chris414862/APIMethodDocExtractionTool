from bs4 import BeautifulSoup
from bs4 import Tag
from Model.ApiClass import ApiClass
from Model.ApiMethod import ApiMethod
import requests
import re
"""
This module contains methods that execute the logic to scrape method and class info from html documents

Created by Chris Crabtree 6/5/2019
"""


def scrape_class_info(contents_container_tag, soup, api_level, is_verbose=False):
    '''
    Scrape class description from contents_container_tag and return a ApiClass object with a populated description
    field.

    :param contents_container_tag: html "div" tag that contains whole class document (i.e. everything but scroll
    tables on the side)
    :type contents_container_tag: Tag
    :return: ApiClass with scraped description field
    :rtype ApiClass
    '''
    # Find heading for class
    class_name_tag = contents_container_tag.find("h1", "api-title")

    # Create new api class
    new_api_class = ApiClass(class_name_tag.string)
    # print(new_api_class.name)
    # Check if its a later api level
    if api_level >= 0:
        if is_later_api_level(soup, api_level, new_api_class.name, is_verbose=is_verbose):
            return -1

    # Find name for class (for some reason there is a blank "p" html tag so I skip it)
    blank_tag = class_name_tag.find_next_sibling("p")

    if blank_tag is None:
        return new_api_class
    first_class_description_tag = blank_tag.find_next_sibling("p")
    if first_class_description_tag is None:
        return new_api_class

    # Attach the class descriptions to the class
    new_api_class.attach_descriptions(first_class_description_tag)
    new_api_class.description += "\n"

    # # Check for more descriptions in the next tags
    # for tag in first_class_description_tag.next_siblings:
    #     if isinstance(tag, Tag) and tag.strings is not None:
    #         if tag.string is not None:
    #             if re.search(r"Summary[ \n]?", tag.string):
    #                 break
    #         new_api_class.attach_descriptions(tag)
    #         new_api_class.description += "\n"

    return new_api_class


def scrape_params_and_rets(api_method, container_tag):
    '''
    Scrapes the description in container_tag and fills either the parameter or return fields of
    api_method depending on the heading inside container_tag

    :param api_method: method to populate with info
    :type api_method: ApiMethod
    :param container_tag: html "table" tag containing either a parameter list or return values
    :type container_tag: Tag
    '''
    # Find tag that holds heading for either Parameters or Returns
    type_tag = container_tag.find("th")
    if type_tag is not None:

        # Find the first row in the table of container_tag (the first row contains the title)
        first_child_of_tag = container_tag.find("tr")
        if first_child_of_tag is not None:

            # Loop through second row until last row in table and attach each description to corresponding field
            for row_tag in first_child_of_tag.find_next_siblings("tr"):
                if isinstance(row_tag, Tag):
                    if type_tag.string == "Parameters":
                        api_method.attach_parameters(row_tag)

                    if type_tag.string == "Returns":
                        api_method.attach_returns(row_tag)


def scrape_method_info(container_tag):
    '''
    Scrapes the description for a method, it's return value, and it's parameters from the from the container_tag
    and returns an ApiMethod object containing the scraped info

    :param container_tag: "div" Tag containing the info for a method
    :type container_tag: Tag
    :return ApiMethod with scraped fields
    :rtype ApiMethod
    '''
    if container_tag is None:
        return None

    # Get method name and create method
    method_name_tag = container_tag.find("h3")
    if method_name_tag is None:
        return None
    method_name = str(method_name_tag.contents[0])
    new_method = ApiMethod(method_name)

    # Populate method description
    container_tag = container_tag.find("p")
    new_method.attach_descriptions(container_tag)

    # Check for more descriptions in the next tags
    for tag in container_tag.next_siblings:
        if tag.name == "p":
            new_method.attach_descriptions(tag)

        # Check if description is inside a bullet point list
        if tag.name == "ul":
            for bullet_point in tag.find_all("li"):
                new_method.attach_descriptions(bullet_point)
                new_method.description += "\n"

        # Assign parameters and return values
        if tag.name == "table" and "class" in tag.attrs and tag["class"] == ["responsive"]:
            scrape_params_and_rets(new_method, tag)

    return new_method


def is_later_api_level(html_doc, api_level, class_name, is_verbose):
    """
    Checks if the html document is from a later api than api_level

    :param html_doc: html text (un-parsed) to find api level from
    :type html_doc: string
    :param api_level: api level after which to return true
    :type api_level: int
    :return Boolean indicating whether this html is from a later api than api_level
    :rtype boolean
    """
    # Search for correct tag
    api_info_block = html_doc.find("div", id="api-info-block")
    # If not there then return False to scrape anyway
    if api_info_block is None:
        if is_verbose:
            print(class_name, "had no api-level info\nCould not find api_info_block")
        return False
    api_level_block = api_info_block.find("div", {"class": "api-level"})
    if api_level_block is None:
        if is_verbose:
            print(class_name, "had no api-level info\nCould not find api_level_block")
        return False
    api_href = api_level_block.find("a")
    if api_href is None:
        if is_verbose:
            print(class_name, "had no api-level info\nCould not find api_info_block")
        return False

    # Get string for tag

    api_string = api_href.string
    if api_href is None:
        if is_verbose:
            print(class_name, "had no api-level info\napi_string was none")
        return False

    # Get api level in tag
    doc_api_level = None
    if api_string is not None:
        for token in api_string.split():
            if token.isdigit():
                try:
                    doc_api_level = int(token)
                except:
                    if is_verbose:
                        print("Error when determining api level: ", token)
                        print("tag searched:", api_string)
                        print("class name:", class_name)
                    return False
    else:
        if is_verbose:
            print("Error when determining api level")
            print("tag searched:", api_level_block)
            print("class name:", class_name)
        return False

    if doc_api_level is None:
        if is_verbose:
            print(class_name, "had no api-level info")
        return False
    # doc is earlier than api level cutoff
    elif doc_api_level <= api_level:
        return False
    # doc is later than api level cutoff
    else:
        return True



def get_documentation(html_doc, api_level=-1, is_verbose=False):
    '''
    Returns an apiClass object that containg the documentation for that class and it's methods

    :param html_doc: html text (un-parsed) to exctract documentation from
    :type html_doc: string
    :return: (ApiClass) ApiClass object that contains deocumentation for the class
    '''
    if html_doc is None:
        print("get_documentation did not receive html_doc")
        return -2

    #Soupify html document
    soup = BeautifulSoup(html_doc, 'lxml')

    # Find heading for class
    class_name_divider = soup.find("div", id="jd-content")
    # print("UUUU")
    # Fill out class info
    new_api_class = scrape_class_info(class_name_divider, soup, api_level, is_verbose=is_verbose)
    # print("FFFF")
    # Check if its a later api level
    if new_api_class == -1:
        return -1

    # Find the heading for the methods
    methods_heading_tag = None
    for iter_tag in soup.find_all("h2", "api-section"):
        if iter_tag.string == "Public methods":
            methods_heading_tag = iter_tag
            break
    if methods_heading_tag == None:
        return new_api_class

    # Find first tag that contains method info
    method_tag = methods_heading_tag.find_next_sibling("div")

    # Start iterating through the siblings of the heading that have a "div" tag (the methods after the heading)
    while methods_heading_tag != None:
        # Get new method
        new_method = scrape_method_info(method_tag)

        # Add method to class
        if new_method == None:
            break
        new_api_class.methods.append(new_method)
        method_tag = method_tag.find_next_sibling("div")

    return new_api_class

def get_package_descrip(package_url):
    result = requests.get(package_url)
    soup = BeautifulSoup(result.content, 'lxml')
    outer_tag = soup.find("div", {"class": "nocontent"})
    if outer_tag is None:
        return ""
    descrip = ""
    for sibling in outer_tag.next_siblings:
        if sibling.name == "div" or sibling.name == "h2":
            break
        if isinstance(sibling, Tag) and sibling.strings is not None:
            for string in sibling.strings:
                if not re.search(r"^\s*$", string):
                    descrip += string+" "

    return descrip

