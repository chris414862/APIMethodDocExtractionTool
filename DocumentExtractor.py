from bs4 import BeautifulSoup
import re

with open("Account     Android Developers.htm", "rb") as html_doc:
    soup = BeautifulSoup(html_doc, 'html.parser')


#print(soup.prettify())

for thing in soup.find_all("div", id="jd-content"):
    i=0
    print("("+str(i)+") "+str(thing.prettify()))
    #if re.search(r"Public methods")
    #print("\t\t"+str(thing.parent.parent['id']))
    print("\n\n\n")

    #for item in thing.parent.contents:
     #   print("("+str(i)+") "+str(item))
     #   i+=1