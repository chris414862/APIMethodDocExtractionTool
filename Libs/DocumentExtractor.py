from bs4 import BeautifulSoup
from bs4 import Tag
from Model.ApiClass import ApiClass
from Model.ApiMethod import ApiMethod
import re
"""
This module contains methods that execute the logic to scrape method and class info from html documents

Created by Chris Crabtree 6/5/2019
"""


def scrape_class_info(contents_container_tag):
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

    # Find name for class (for some reason there is a blank "p" html tag so I skip it)
    blank_tag = class_name_tag.find_next_sibling("p")
    if blank_tag is None:
        return new_api_class
    first_class_description_tag = blank_tag.find_next_sibling("p")
    if first_class_description_tag is None:
        return new_api_class

    #
    new_api_class.attach_descriptions(first_class_description_tag)
    new_api_class.description += "\n"

    # Check for more descriptions in the next tags
    for tag in first_class_description_tag.next_siblings:
        if isinstance(tag, Tag) and tag.strings is not None:
            if tag.string is not None:
                if re.search(r"Summary[ \n]?", tag.string):
                    break
            new_api_class.attach_descriptions(tag)
            new_api_class.description += "\n"

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


def get_documentation(html_doc):
    '''
    Returns an apiClass object that containg the documentation for that class and it's methods

    :param html_doc: html text (un-parsed) to exctract documentation from
    :type html_doc: string
    :return: (ApiClass) ApiClass object that contains deocumentation for the class
    '''
    #Soupify html document
    soup = BeautifulSoup(html_doc, 'lxml')

    # Find heading for class
    class_name_divider = soup.find("div", id="jd-content")

    # Fill out class info
    new_api_class = scrape_class_info(class_name_divider)

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


