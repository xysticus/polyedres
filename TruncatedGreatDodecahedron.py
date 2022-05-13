from moulinette import aspiro

import cadquery as cq
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane

from progress.bar import Bar

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "TruncatedGreatDodecahedron"

facteur = 1.4

marge = [0.0]*12
marge[10] = 0.4
marge[5] = 0.4

epaisseur = [0.0]*12
epaisseur[10] = 1
epaisseur[5] = 1

largeur = [0.0]*12
largeur[10] = 1
largeur[5] = 1

sphere_int_ry = 0
sphere_ext_ry = 0

trou_perle = 0

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

# une face c'est la liste des sommets dans l'ordre et il faut retourner au premmier
les_faces = [ l + [l[0]] for l in les_faces ]

sommets = [(a * facteur, b * facteur, c * facteur) for (a, b, c) in sommets]

print(sommets)
print(les_faces)

def Polyedre():

    le_tout = Workplane()

    for ixs in les_faces:

        lines = []

        for v1, v2 in zip(ixs, ixs[1:]):
            lines.append(
                Edge.makeLine(Vector(*sommets[v1]), Vector(*sommets[v2]))
            )

        wire = Wire.combine(lines)
        une_face = Face.makeFromWires(*wire)

        nb_faces = len(ixs) - 1

        if largeur[nb_faces] > 0:
            if marge[nb_faces] > 0:
                    dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
                    offset2D(largeur[nb_faces],"arc").extrude(epaisseur[nb_faces]).faces().end().workplane().\
                    add(une_face).wires().toPending().offset2D(largeur[nb_faces]-marge[nb_faces],"arc").extrude(epaisseur[nb_faces],combine="cut")
            else:   
                    dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
                    offset2D(largeur[nb_faces],"arc").extrude(epaisseur[nb_faces])

            le_tout = le_tout.add(dessus)

    return le_tout

exporters.export(Polyedre(),"./stl/" + nom_polyedre + ".stl",tolerance=0.2)
