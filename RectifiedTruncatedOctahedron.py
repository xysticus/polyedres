import cadquery as cq
from moulinette import aspiro
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "RectifiedTruncatedOctahedron"

marge = [0.0]*25
marge[6] = 0.4
marge[4] = 0.4
marge[3] = 0.4

epaisseur = [0.0]*25
epaisseur[6] = 0.08
epaisseur[4] = 0.08
epaisseur[3] = 0.08

largeur = [0.0]*25
largeur[6] = 1.6
largeur[4] = 1.6
largeur[3] = 1.6

sphere_ext_ry = 0.0
sphere_int_ry = 1.0

trou_perle = 0

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

# une face c'est la liste des sommets dans l'ordre et il faut retourner au premmier
les_faces = [ l + [l[0]] for l in les_faces ]

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

            le_tout = le_tout.union(dessus)

        if trou_perle > 0:
            sphere_ext = cq.Workplane().sphere(sphere_ext_ry).circle(trou_perle).cutThruAll()
            sphere_int = cq.Workplane().sphere(sphere_int_ry).circle(trou_perle).cutThruAll()
            le_tout = le_tout.circle(trou_perle).cutThruAll()   
            le_tout = le_tout.union(sphere_ext).cut(sphere_int)
        else:
            if sphere_ext_ry > 0:
                sphere_ext = cq.Workplane().sphere(sphere_ext_ry)
                le_tout = le_tout.union(sphere_ext)

    return le_tout

exporters.export(Polyedre(),"./stl/" + nom_polyedre + ".stl",tolerance=0.2)