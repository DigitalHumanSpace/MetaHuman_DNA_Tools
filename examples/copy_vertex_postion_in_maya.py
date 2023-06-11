from maya import cmds
import math

src_mesh_name = "head_lod0_mesh1"
target_mesh_name = "head_lod0_mesh"

def getVertexDistance(position_1, position_2):
    x1,y1,z1 = position_1
    x2,y2,z2 = position_2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

vertex_count = cmds.polyEvaluate(src_mesh_name, vertex=True)
for i in range(vertex_count):
    src_position = cmds.xform("{}.vtx[{}]".format(src_mesh_name, i), q=True, ws=True, t=True)
    target_position = cmds.xform("{}.vtx[{}]".format(target_mesh_name, i), q=True, ws=True, t=True)
    if getVertexDistance(src_position, target_position) > 0.001:
        print("{} {} -> {}".format(i, target_position, src_position))
        cmds.xform("{}.vtx[{}]".format(target_mesh_name, i), t=src_position, ws=True)
print("done")