#-*- coding: utf-8 -*-
import argparse
from os import environ, makedirs
from os import path as ospath
from sys import path as syspath
from sys import platform
import os

# if you use Maya, use absolute path
ROOT_DIR = f"{ospath.dirname(ospath.abspath(__file__))}/../../../..".replace("\\", "/")
OUTPUT_DIR = f"{ROOT_DIR}/output"
ROOT_LIB_DIR = f"{ROOT_DIR}/lib"
if platform == "win32":
    LIB_DIR = f"{ROOT_LIB_DIR}/windows"
elif platform == "linux":
    LIB_DIR = f"{ROOT_LIB_DIR}/linux"
else:
    raise OSError(
        "OS not supported, please compile dependencies and add value to LIB_DIR"
    )

# Add bin directory to maya plugin path
if "MAYA_PLUG_IN_PATH" in environ:
    separator = ":" if platform == "linux" else ";"
    environ["MAYA_PLUG_IN_PATH"] = separator.join([environ["MAYA_PLUG_IN_PATH"], LIB_DIR])
else:
    environ["MAYA_PLUG_IN_PATH"] = LIB_DIR

# Adds directories to path
syspath.insert(0, ROOT_DIR)
syspath.insert(0, LIB_DIR)

import dna
from collections import defaultdict


def createDNA(path):
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Write, dna.FileStream.OpenMode_Binary)
    writer = dna.BinaryStreamWriter(stream)

    writer.setName("rig name")
    writer.setLODCount(4)
    writer.setJointName(0, "spine")
    writer.setJointName(1, "neck")

    writer.setMeshName(0, "head")
    writer.setVertexPositions(0, [[0.0, 0.5, 0.3], [1.0, 3.0, -8.0]])
    writer.setVertexTextureCoordinates(0, [[0.25, 0.55], [1.5, 3.6]])

    writer.write()
    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError("Error saving DNA: {}".format(status.message))


def loadDNA(path):
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
    reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
    reader.read()
    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError("Error loading DNA: {}".format(status.message))
    return reader


def printDNASummary(dnaReader):
    print("Name: {}".format(dnaReader.getName()))
    print("Joint count: {}".format(dnaReader.getJointCount()))
    jointNames = ', '.join(dnaReader.getJointName(i) for i in range(dnaReader.getJointCount()))
    print("Joint names: " + jointNames)

    for meshIdx in range(dnaReader.getMeshCount()):
        # Get vertices one by one
        mesh_name = dnaReader.getMeshName(meshIdx)
        for vtxId in range(dnaReader.getVertexPositionCount(meshIdx)):
            vtx = dnaReader.getVertexPosition(meshIdx, vtxId)
            print("Mesh {} {} - Vertex {} : {}".format(meshIdx, mesh_name, vtxId, vtx))
        # Get all X / Y / Z coordinates
        print(dnaReader.getVertexPositionXs(meshIdx))
        print(dnaReader.getVertexPositionYs(meshIdx))
        print(dnaReader.getVertexPositionZs(meshIdx))

        for tcIdx in range(dnaReader.getVertexTextureCoordinateCount(meshIdx)):
            texCoord = dnaReader.getVertexTextureCoordinate(meshIdx, tcIdx)
            print("Mesh {} {} - Texture coordinate {} : {}".format(meshIdx, mesh_name, tcIdx, texCoord))


def getVertexPositions(dnaReader):
    print("Name: {}".format(dnaReader.getName()))
    print("Joint count: {}".format(dnaReader.getJointCount()))
    # jointNames = ', '.join(dnaReader.getJointName(i) for i in range(dnaReader.getJointCount()))
    # print("Joint names: " + jointNames)

    mesh_vertex_positions = defaultdict(dict)

    for meshIdx in range(dnaReader.getMeshCount()):
        # Get vertices one by one
        mesh_name = dnaReader.getMeshName(meshIdx)
        for vtxId in range(dnaReader.getVertexPositionCount(meshIdx)):
            vtx = dnaReader.getVertexPosition(meshIdx, vtxId)
            mesh_vertex_positions[mesh_name][vtxId] = vtx
            if vtxId == 17071:
                print(vtx)

    return mesh_vertex_positions  

def printVertexPosition(mesh_vertex_positions, mesh_name, vertex_id):
    print("mesh = {} vertex_id={} position={}".format(mesh_name, vertex_id, mesh_vertex_positions[mesh_name][vertex_id]))     

        


def main():
    parser = argparse.ArgumentParser(description="DNA demo")
    parser.add_argument('dna_path',
                        metavar='dna_path',
                        help='Path where to save the DNA file')

    args = parser.parse_args()

    # createDNA(args.dna_path)
    print(args.dna_path)
    dnaReader = loadDNA(args.dna_path)
    # printDNASummary(dnaReader)
    mesh_vertex_positions = getVertexPositions(dnaReader)
    printVertexPosition(mesh_vertex_positions, "head_lod0_mesh", 0)


if __name__ == '__main__':
    main()
