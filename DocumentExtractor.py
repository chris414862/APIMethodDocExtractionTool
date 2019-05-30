from bs4 import BeautifulSoup

with open("Account     Android Developers.htm", "rb") as html_doc:
    soup = BeautifulSoup(html_doc, 'html.parser')


#print(soup.prettify())
for thing in soup.find_all(class_="api-name", id="describeContents()"):
    i=0
    print(thing.parent.contents[7])
    #for item in thing.parent.contents:
     #   print("("+str(i)+") "+str(item))
     #   i+=1