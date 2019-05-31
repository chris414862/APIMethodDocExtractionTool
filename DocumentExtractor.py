from bs4 import BeautifulSoup
from apiClass import apiClass
from apiMethod import apiMethod

with open("Account     Android Developers.htm", "rb") as html_doc:
    soup = BeautifulSoup(html_doc, 'html.parser')


def fillDescription(object, textTag):
    #object description
    for string in textTag.strings:
        object.description += string

    #check for more descriptions in the next tags
    for tag in textTag.next_siblings:
        if tag.name == "p":
            for string in tag.strings:
                object.description += string

        #check for lists or bulletpoints
        if tag.name == "ul":
            list = tag
            for string in list.find("li").strings:
                object.description += string

            for listElement in list.find("li").next_siblings:
                for string in listElement.strings:
                    object.description += string


#Find heading for class
classNameTag = soup.find("devsite-heading", "api-title")

#Fill out class info
newApiClass = apiClass(classNameTag.string)
textTag =soup.find("table","jd-inheritance-table").parent.find_next_sibling("p")
fillDescription(newApiClass, textTag)


#Find the heading for the methods
thing =soup.find(id="public-methods_1")

#Start iterating through the siblings of the heading that have a "div" tag (the methods after the heading)
thing =thing.find_next_sibling("div")
while thing != None:

    #The method name
    methodName = str(thing.find("h3").contents[0])
    newMethod = apiMethod(methodName)

    #Method description
    textTag =thing.find("p")
    fillDescription(newMethod,textTag)

    #Add method to class
    newApiClass.methods.append(newMethod)
    thing = thing.find_next_sibling("div")

print(newApiClass.string())
