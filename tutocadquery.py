import cadquery as cq
from moulinette import aspiro
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Shell
from cadquery import Solid
from cadquery import Vector
from cadquery import Workplane


racine = "./dmccooey.com/polyhedra/"
nom_polyedre= "TruncatedIcosidodecahedron"
trou1=2.8
trou2=2.4
epaisseur=0.15
largeur1=0.5
largeur=2.2

(sommets, les_faces) = aspiro(racine + nom_polyedre + ".html")

les_faces = [ l + [l[0]] for l in les_faces ]

print(sommets)
print(les_faces)

def Polyedre(s=1):
   
    le_tout = Workplane()

    for ixs in les_faces:

        lines = []

        for v1, v2 in zip(ixs, ixs[1:]):
            lines.append(
                Edge.makeLine(Vector(*sommets[v1]), Vector(*sommets[v2]))
            )

        wire = Wire.combine(lines)
        une_face = Face.makeFromWires(*wire)

        if len(ixs)==11:
            pass
            #dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
            #    offset2D(largeur1,"arc").extrude(epaisseur).faces().end().workplane().circle(trou1).cutThruAll()
        elif len(ixs)==7:
           dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
           offset2D(largeur,"arc").extrude(epaisseur).faces().end().workplane().circle(trou2).cutThruAll()
           le_tout = le_tout.add(dessus)

        elif len(ixs)==5:
           dessus = Workplane(une_face).faces().workplane().add(une_face).wires().toPending().\
           offset2D(largeur,"arc").extrude(epaisseur)
           le_tout = le_tout.add(dessus)

    return le_tout

exporters.export(Polyedre(),"./stl/" + nom_polyedre + ".stl",tolerance=0.5)
