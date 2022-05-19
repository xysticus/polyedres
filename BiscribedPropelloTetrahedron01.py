from moulinette import aspiro

from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane

from progress.bar import Bar

import time

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "BiscribedPropelloTetrahedron"
sortie = "./stl/" + nom_polyedre + "BisProp01.stl"
pluspetit = "./stl/" + nom_polyedre + "BisProp01bin.stl"

facteur_d_echelle = 1

epaisseur = [0.0]*12
epaisseur[4] = .25
epaisseur[3] = .25

epaisseur_arriere = [0.0]*12
epaisseur_arriere[4] = 0
epaisseur_arriere[3] = 0

trou_face = [0.0]*12
trou_face[4] = 0.1
trou_face[3] = 0.1

offset_face = [0.0]*12
offset_face[4] = .08
offset_face[3] = .07

trou_perle = 0

chanfrein = 0
arrondi = 0

finesse = 0.1

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

# une face c'est la liste des sommets dans l'ordre et il faut retourner au premmier
les_faces = [ l + [l[0]] for l in les_faces ]

sommets = [(a * facteur_d_echelle, b * facteur_d_echelle, c * facteur_d_echelle) for (a, b, c) in sommets]

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

        if offset_face[nb_faces] > 0:
            dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
            offset2D(offset_face[nb_faces],"arc").extrude(epaisseur[nb_faces]) .workplane().\
            add(une_face).wires().toPending().offset2D(offset_face[nb_faces]-trou_face[nb_faces],"arc").\
            extrude(epaisseur[nb_faces],combine="cut")

            if epaisseur_arriere[nb_faces]:
                dessous = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
                offset2D(offset_face[nb_faces],"arc").extrude(-epaisseur_arriere[nb_faces]).workplane().\
                add(une_face).wires().toPending().offset2D(offset_face[nb_faces]-trou_face[nb_faces],"arc").\
                extrude(-epaisseur_arriere[nb_faces],combine="cut")


                piece = Workplane().add(dessus).union(dessous)
            else:
                piece = Workplane().add(dessus)

            if chanfrein:
                piece = Workplane().add(piece).edges().chamfer(chanfrein)
            elif arrondi:
                piece = Workplane().add(piece).edges().fillet(arrondi)

        le_tout = le_tout.union(piece)

        bar.next()

    bar.finish()

    dernier_toc = time.perf_counter()
    print(f"Le tout en {dernier_toc - premier_tic:0.4f} seconds")

    return le_tout.combine()

design = Polyedre()

exporters.export(design, sortie, angularTolerance=finesse)
print("On a écrit le fichier", sortie)

import pymeshlab
print("On fait travailler meshlab")

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
