import cadquery as cq
from moulinette import aspiro
from cadquery import exporters
from cadquery import Edge
from cadquery import Wire
from cadquery import Face
from cadquery import Shell
from cadquery import Solid
from cadquery import Vector

racine = "./dmccooey.com/polyhedra/"
test = "ExpandedJoinedHexpropelloDodecahedron"

(sommets, les_faces) = aspiro(racine + test + ".html")

les_faces = [ l + [l[0]] for l in les_faces ]

print(sommets)
print(les_faces)

def Polyedre(s=1):
   
    faces = []
    for ixs in les_faces:
        lines = []
        for v1, v2 in zip(ixs, ixs[1:]):
            lines.append(
                Edge.makeLine(Vector(*sommets[v1]), Vector(*sommets[v2]))
            )
        wire = Wire.combine(lines)
        faces.append(Face.makeFromWires(*wire))
   
    shell = Shell.makeShell(faces)
    solid = Solid.makeSolid(shell)
    return solid

exporters.export(Polyedre(),"./stl/" + test + ".stl")
