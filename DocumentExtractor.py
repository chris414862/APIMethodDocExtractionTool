from bs4 import BeautifulSoup
import re

with open("BackupManager     Android Developers.htm", "rb") as html_doc:
    soup = BeautifulSoup(html_doc, 'html.parser')

i=0

thing =soup.find(id="public-methods_1")
thing =thing.find_next_sibling("div")
while thing != None:
    print("(" + str(i) + ") " + str(thing.find("h3").contents[0]))
    textTag =thing.find("p")
    for string in textTag.strings:
        print(string, end="")
    for tag in textTag.next_siblings:
        if tag.name == "p":
            for string in tag.strings:
                print(string, end="")
        if tag.name == "ul":
            list = tag
            for string in list.find("li").strings:
                print(string, end="")
            for listElement in list.find("li").next_siblings:
                for string in listElement.strings:
                    print(string, end="")
    print()
    thing = thing.find_next_sibling("div")
    i += 1
