from bs4 import BeautifulSoup
from bs4 import Tag
from ApiClass import ApiClass
from ApiMethod import ApiMethod
import re


def get_class_info(text_tag):
    # Find heading for class
    class_name_tag = text_tag.find("h1", "api-title")

    # Fill out class info
    new_api_class = ApiClass(class_name_tag.string)
    text_tag = class_name_tag.find_next_sibling("p").find_next_sibling("p")

    # Class description
    if text_tag is None:
        return new_api_class

    new_api_class.attach_descriptions(text_tag)
    new_api_class.description += "\n"

    # Check for more descriptions in the next tags
    for tag in text_tag.next_siblings:
        if isinstance(tag, Tag) and tag.strings is not None:
            if tag.string is not None:
                if re.search(r"Summary[ \n]?", tag.string):
                    break
            new_api_class.attach_descriptions(tag)
            new_api_class.description += "\n"

    return new_api_class


def assign_params_and_rets(new_method, tag):
    type_tag = tag.find("th")
    if type_tag is not None:
        child_of_tag = tag.find("tr")
        if child_of_tag is not None:
            for row_tag in child_of_tag.find_next_siblings("tr"):
                if isinstance(row_tag, Tag):
                    if type_tag.string == "Parameters":
                        new_method.attach_parameters(row_tag)

                    if type_tag.string == "Returns":
                        new_method.attach_returns(row_tag)


def get_method_info(text_tag):
    if text_tag is None:
        return None

    # Get method name and create method
    method_name_tag = text_tag.find("h3")
    if method_name_tag is None:
        return None
    method_name = str(method_name_tag.contents[0])
    new_method = ApiMethod(method_name)

    # Method description
    text_tag = text_tag.find("p")
    # print("_____\n"+str(text_tag.prettify())+"\n______")
    new_method.attach_descriptions(text_tag)

    # Check for more descriptions in the next tags
    for tag in text_tag.next_siblings:
        if tag.name == "p":
            new_method.attach_descriptions(tag)

        if tag.name == "ul":
            add_newline = 1
            for bullet_point in tag.find_all("li"):
                new_method.attach_descriptions(bullet_point)
                new_method.description += "\n"

        # Assign parameters and return values
        if tag.name == "table" and tag["class"] == ["responsive"]:
            assign_params_and_rets(new_method, tag)

    return new_method


def get_documentation(html_doc):
    '''
    Returns an apiClass object that containg the documentation for that class and it's methods

    Parameters:
    html_doc (string): html text (un-parsed) to exctract documentation from

    Returns:
    new_api_class (ApiClass): ApiClass object that contains deocumentation for the class
    '''

    soup = BeautifulSoup(html_doc, 'lxml')

    # Find heading for class
    class_name_divider = soup.find("div", id="jd-content")

    # Fill out class info
    new_api_class = get_class_info(class_name_divider)

    # Find the heading for the methods
    thing = None
    for heading_tag in soup.find_all("h2", "api-section"):
        if heading_tag.string == "Public methods":
            thing = heading_tag
            break
    if thing == None:
        return new_api_class
    # Start iterating through the siblings of the heading that have a "div" tag (the methods after the heading)
    thing = thing.find_next_sibling("div")

    while thing != None:
        # Get new method
        new_method = get_method_info(thing)

        # Add method to class
        if new_method == None:
            break
        new_api_class.methods.append(new_method)
        thing = thing.find_next_sibling("div")

    return new_api_class
