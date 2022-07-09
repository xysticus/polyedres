from moulinette import aspiro

import cadquery as cq
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane

from progress.bar import Bar

import time

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "TruncatedIcosidodecahedron"

facteur = 1.4

marge = [0.0]*12
marge[10] = 0.4
marge[6] = 0.4
marge[4] = 0.4

epaisseur = [0.0]*12
epaisseur[10] = 0.3
epaisseur[6] = 0.3
epaisseur[4] = 0.3

largeur = [0.0]*12
largeur[10] = 1.9
largeur[6] = 2.3
largeur[4] = 2.45

sphere_int_ry = 5.8
sphere_ext_ry = 6 #6.18

trou_perle = 0

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

        if largeur[nb_faces] > 0:
            if marge[nb_faces] > 0:
                    dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
                    offset2D(largeur[nb_faces],"arc").extrude(epaisseur[nb_faces]).faces().end().workplane().\
                    add(une_face).wires().toPending().offset2D(largeur[nb_faces]-marge[nb_faces],"arc").extrude(epaisseur[nb_faces],combine="cut")
            else:   
                    dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
                    offset2D(largeur[nb_faces],"arc").extrude(epaisseur[nb_faces])

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

exporters.export(Polyedre(),"./stl/" + nom_polyedre + "Chris01.stl",tolerance=0.2)
