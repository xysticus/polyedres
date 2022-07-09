from moulinette import aspiro

from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane

from progress.bar import Bar

import time
import os

import pymeshlab

import winsound

import colorama
from colorama import Fore

# Entrée

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "BiscribedPropelloTetrahedron"

#
# Aspiration des coordonnées
#

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

# une face c'est la liste des sommets dans l'ordre et il faut retourner au premmier
les_faces = [ l + [l[0]] for l in les_faces ]

print(f"{len(sommets)} sommets")
print(f"{len(les_faces)} faces")

def Polyedre():

    print()
    print("On calcule", sortie)

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
            dessus = Workplane(une_face).workplane().add(une_face).wires().toPending().\
            offset2D(offset_face[nb_faces],"arc").twistExtrude(epaisseur[nb_faces],twist)
            if trou_face[nb_faces]:
                dessus = dessus.workplane().add(une_face).wires().toPending().\
                    offset2D(offset_face[nb_faces]-trou_face[nb_faces],"arc").\
                    twistExtrude(epaisseur[nb_faces], twist, combine="cut")
            if epaisseur_arriere[nb_faces]:
                dessous = Workplane(une_face).workplane().add(une_face).workplane().add(une_face).wires().toPending().\
                offset2D(offset_face[nb_faces],"arc").twistExtrude(-epaisseur_arriere[nb_faces],twist)
                
                if trou_face[nb_faces]:
                    dessous = dessous.workplane().add(une_face).wires().toPending().\
                    offset2D(offset_face[nb_faces]-trou_face[nb_faces],"arc").\
                    twistExtrude(-epaisseur_arriere[nb_faces], twist, combine="cut")

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

#
# Meshlab en action
#

def compression():
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(sortie)

    geo_dict = ms.get_geometric_measures()
    mesh_volume = geo_dict['mesh_volume']

    topo_dict = ms.get_topological_measures()
    nb_compo = topo_dict['connected_components_number']
    faces_number = topo_dict['faces_number']

    print(f"Volume: {Fore.BLUE}{mesh_volume}{Fore.RESET}")
    print(f"Composants: {Fore.GREEN}{nb_compo}{Fore.RESET}")
    print(f"Faces: {Fore.RED}{faces_number:,}{Fore.RESET} sur un max d'un million de faces".replace(',',' '))

    if pluspetit:
        ms.save_current_mesh(pluspetit, save_face_color=False)
        print(f"Taile du fichier en mode bin :{os.path.getsize(pluspetit)//1024:,}Ko sur un max de 50 000".replace(',',' '))

    if propre:
        ms.print_status()
        ms.generate_splitting_by_connected_components(delete_source_mesh=True)
        ms.set_current_mesh(1)
        ms.save_current_mesh(propre, save_face_color=False)


def dessine():
    design = Polyedre()

    exporters.export(design, sortie, angularTolerance=finesse)
    print("On a écrit le fichier", sortie)

    winsound.Beep(440, 500)

    compression()

twist = 18

# premier calcul

sortie = "./stl/" + nom_polyedre + "BisProp11.stl"
pluspetit = "./stl/" + nom_polyedre + "BisProp11bin.stl"
propre = None

facteur_d_echelle = 1

eloigne = 0

sommets = [(a * facteur_d_echelle, b * facteur_d_echelle, c * facteur_d_echelle) for (a, b, c) in sommets]

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

dessine()

# deuxième calcul

sortie = "./stl/" + nom_polyedre + "BisProp12.stl"
pluspetit = "./stl/" + nom_polyedre + "BisProp12bin.stl"
propre = "./stl/" + nom_polyedre + "BisProp12propre.stl"

epaisseur = [0.0]*12
epaisseur[4] = .4
epaisseur[3] = .4

epaisseur_arriere = [0.0]*12
epaisseur_arriere[4] = 0
epaisseur_arriere[3] = 0

trou_face = [0.0]*12
trou_face[4] = 0.12
trou_face[3] = 0.12

offset_face = [0.0]*12
offset_face[4] = .08
offset_face[3] = .065

dessine()

# troisième calcul

sortie = "./stl/" + nom_polyedre + "BisProp13.stl"
pluspetit = "./stl/" + nom_polyedre + "BisProp13bin.stl"
propre = "./stl/" + nom_polyedre + "BisProp13propre.stl"

epaisseur = [0.0]*12
epaisseur[4] = .4
epaisseur[3] = .4

epaisseur_arriere = [0.0]*12
epaisseur_arriere[4] = 0
epaisseur_arriere[3] = 0

trou_face = [0.0]*12
trou_face[4] = 0
trou_face[3] = 0

offset_face = [0.0]*12
offset_face[4] = .08
offset_face[3] = .08

dessine()
