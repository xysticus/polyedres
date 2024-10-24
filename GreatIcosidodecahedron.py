from moulinette import aspiro

import cadquery as cq
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane
from cadquery import Color
import random

from progress.bar import Bar

import time

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "GreatIcosidodecahedron"

facteur = 1.6

marge = [0.0]*12 # taille entre la face et le trou

#marge[5] = 0.0
marge[3] = 0.0


epaisseur = [0.0]*12 #épaisseur de l'extrusion
#epaisseur[5] = 0.12
epaisseur[3] = 0.12


largeur = [0.0]*12 #largeur de la face
#largeur[5] = 0.1
largeur[3] = 0.1

trottoir = [0.0]*25 # inutile ?
#trottoir[5] = 0.20
trottoir[3] = 0.20


sphere_int_ry = 0.0
sphere_ext_ry = 0.0 #6.18

trou_perle = 0.0

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

# une face c'est la liste des sommets dans l'ordre et il faut retourner au premmier
les_faces = [ l + [l[0]] for l in les_faces ]

sommets = [(a * facteur, b * facteur, c * facteur) for (a, b, c) in sommets]

print(sommets)
print(les_faces)

def Polyedre():

    premier_tic = time.perf_counter()
   
    le_tout = Workplane()

    bar = Bar('Processing', max=len(les_faces))
    for ixs in les_faces:

        lines = []

        for v1, v2 in zip(ixs, ixs[1:]):
            lines.append(
                Edge.makeLine(Vector(*sommets[v1]), Vector(*sommets[v2]))
            )

        wire = Wire.combine(lines)
        une_face = Face.makeFromWires(*wire)         

        nb_faces = len(ixs) - 1

        if abs(largeur[nb_faces]) > 0:
            if abs(marge[nb_faces]) > 0:
                    dessus = Workplane(une_face).workplane().add(lines).toPending().\
                    offset2D(largeur[nb_faces],"intersection").extrude(epaisseur[nb_faces]).\
                    add(lines).toPending().offset2D(largeur[nb_faces]-marge[nb_faces],"intersection").extrude(epaisseur[nb_faces],combine="cut")
            else:   
                    dessus = Workplane(une_face).faces().workplane().add(une_face)#.wires().toPending().\
                    #offset2D(largeur[nb_faces],"arc").extrude(epaisseur[nb_faces])

            le_tout = le_tout.add(dessus)

        bar.next()

    bar.finish()

    if trou_perle > 0:
        #le_tout = le_tout.union(sphere_ext)
        sphere_ext = cq.Workplane().sphere(sphere_ext_ry).circle(trou_perle).cutThruAll()
        sphere_int = cq.Workplane().sphere(sphere_int_ry).circle(trou_perle).cutThruAll()
        le_tout = le_tout.circle(trou_perle).cutThruAll()   
        le_tout = le_tout.union(sphere_ext).cut(sphere_int)
    else:
        if sphere_int_ry > 0:
            sphere_ext = cq.Workplane().sphere(sphere_ext_ry)
            sphere_int = cq.Workplane().sphere(sphere_int_ry)
            tic = time.perf_counter()
            le_tout = le_tout.union(sphere_ext).cut(sphere_int)
            toc = time.perf_counter()
            print(f"Etape finale en {toc - tic:0.4f} seconds")

    dernier_toc = time.perf_counter()
    print(f"Le tout en {dernier_toc - premier_tic:0.4f} seconds")

    return le_tout

exporters.export(Polyedre(),"./stl/" + nom_polyedre + ".stl",tolerance=0.2)
