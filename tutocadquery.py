import cadquery as cq
from moulinette import aspiro
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Vector
from cadquery import Workplane

racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "TruncatedIcosidodecahedron"
marge = [0.0]*12
marge[10] = 0.0
marge[6] = 0.2
marge[4] = 0
epaisseur = [0.0]*12
epaisseur[10] = 0.3
epaisseur[6] = 0.15
epaisseur[4] = 0.15
largeur = [0.0]*12
largeur[10] = 0
largeur[6] = 2.4
largeur[4] = 2.5
sphere_ext_ry = 4.6
sphere_int_ry = 4.45

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

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

    sphere_ext = cq.Workplane().sphere(sphere_ext_ry)
    sphere_int = cq.Workplane().sphere(sphere_int_ry)
    return le_tout.union(sphere_ext).cut(sphere_int).workplane().circle(.3).cutThruAll()

exporters.export(Polyedre(),"./stl/" + nom_polyedre + ".stl",tolerance=0.8)
