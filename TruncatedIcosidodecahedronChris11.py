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
sortie = "./stl/" + nom_polyedre + "Chris11.stl"
pluspetit = "./stl/" + nom_polyedre + "Chris11bin.stl"


facteur = 2 #1.8

marge = [0.0]*12
marge[10] = 1.4
marge[6] = 1.3
marge[4] = 1

epaisseur = [0.0]*12
epaisseur[10] = 0.5
epaisseur[6] = .3
epaisseur[4] = .3

epaisseur_arriere = [0.0]*12
epaisseur_arriere[10] = 0
epaisseur_arriere[6] = 0
epaisseur_arriere[4] = 0


largeur = [0.0]*12
largeur[10] = 0
largeur[6] = 2.9
largeur[4] = 2.7

sphere_int_ry = 0 # 7.3
sphere_ext_ry = 0 #7.64 #6.18

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
            dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
            offset2D(largeur[nb_faces],"arc").twistExtrude(epaisseur[nb_faces],18).workplane().\
            add(une_face).wires().toPending().offset2D(largeur[nb_faces]-marge[nb_faces],"arc").\
            twistExtrude(epaisseur[nb_faces],-20,combine="cut")

            if epaisseur_arriere[nb_faces]:
                dessous = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
                offset2D(largeur[nb_faces],"arc").extrude(-epaisseur_arriere[nb_faces])

                piece = Workplane().add(dessus).union(dessous).edges().chamfer(0.05)
                le_tout = le_tout.union(piece)
            else:
                piece = Workplane().add(dessus).edges().chamfer(0.05)
                le_tout = le_tout.union(piece)

        bar.next()

    bar.finish()

    dernier_toc = time.perf_counter()
    print(f"Le tout en {dernier_toc - premier_tic:0.4f} seconds")

    return le_tout.combine()

design = Polyedre()

print("On écrit le fichier", sortie)
exporters.export(design, sortie, angularTolerance=0.2)

import pymeshlab
print("On fait travailler mechlab")

ms = pymeshlab.MeshSet()
ms.load_new_mesh(sortie)

geo_dict = ms.get_geometric_measures()
mesh_volume = geo_dict['mesh_volume']
print(geo_dict)

topo_dict = ms.get_topological_measures()
nb_compo = topo_dict['connected_components_number']
faces_number = topo_dict['faces_number']
print(topo_dict)

if pluspetit:
    ms.save_current_mesh(pluspetit, save_face_color=False)

print(f"Volume: {mesh_volume}")
print(f"Composants: {nb_compo}")
print(f"Faces: {faces_number:,} sur un max d'un million de faces".replace(',',' '))

import os
print(f"Taile du fichier :{os.path.getsize(pluspetit)//1024:,}Ko sur un max de 50 000".replace(',',' '))

ms.show_polyscope()
