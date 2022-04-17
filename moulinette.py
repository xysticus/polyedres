from multiprocessing.sharedctypes import Value
from bs4 import BeautifulSoup as bellesoupe 


with open("//wsl.localhost/Ubuntu/home/alex/polyhedra/dmccooey.com/polyhedra/Dodecahedron.html") as fp:
    soup = bellesoupe(fp, 'html.parser')

    constantes = soup.find(class_="Constants",attrs="value")['value'].split()

    print (constantes)
