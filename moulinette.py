from bs4 import BeautifulSoup  
import re

def aspiro(chemin):
    with open(chemin) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        if soup.find(class_="Constants",attrs="value"):
            constantes = soup.find(class_="Constants",attrs="value")['value'].split(',')
            constantes = [chaine.strip() for chaine in constantes]
        else:
            constantes = []

        sommets = soup.find(class_="Vertices",attrs="value")['value'].split(',')
        sommets = [s.split() for s in sommets]

        faces = soup.find(class_="Faces",attrs="value")['value'].split(',')
        faces = [list(map(int,f.split()[:-1])) for f in faces]

        constantepositive = re.compile("C(\d+)")
        constantenegative = re.compile("-C(\d+)")

        def evalue(chaine):
            matchmoins = constantenegative.match(chaine)
            matchplus = constantepositive.match(chaine)
            if matchmoins: return -float(constantes[int(matchmoins.group(1))])
            elif matchplus: return float(constantes[int(matchplus.group(1))])
            else: return(float(chaine))

        def evaluesommet(point):
            return list(map(evalue,point))

        sommets = list(map(evaluesommet,sommets)) 

        return (sommets, faces)

if __name__ == "__main__":

    racine = "./dmccooey.com/polyhedra/"
    test = "LsnubCube"

    (sommets, faces) = aspiro(racine + test + ".html")

    print(sommets)
    print(faces)
       