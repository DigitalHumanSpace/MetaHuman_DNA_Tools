"""
This example demonstrates Maya UI Window for simple and non-programmatic creation the scene with the creating functional rig.
- usage in command line:
    - call without arguments:
        - will not start with error message: "DNAViewer needs to be run with Maya2022"
    NOTE: Script cannot be called with Python or mayapy, it' must be called in Maya Script Editor.
- usage in Maya:
    1. copy whole content of this file to Maya Script Editor
    2. change value of ROOT_DIR to absolute path of dna_calibration, e.g. `c:/dna_calibration` in Windows or `/home/user/dna_calibration`. Important:
    Use `/` (forward slash), because Maya uses forward slashes in path.

    Expected: Maya will show UI.

NOTE: If running on Linux, please make sure to append the LD_LIBRARY_PATH with absolute path to the lib/linux directory before running the example:
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<path-to-lib-linux-dir>
"""


from importlib import reload
from os import environ
from os import path as ospath
from sys import path as syspath
from sys import platform
import traceback


try:
    # if you use Maya, use absolute path
    scriptPath = "E:\Projects\MetaHuman_DNA_Tools\examples\dna_viewer_run_in_maya.py"
    ROOT_DIR = ospath.abspath(f"{ospath.dirname(ospath.abspath(scriptPath))}/..").replace("\\", "/")
    print(f"ROOT_DIR is {ROOT_DIR}")
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
    if ROOT_DIR not in syspath:
        syspath.insert(0, ROOT_DIR)
    if LIB_DIR not in syspath:
        syspath.insert(0, LIB_DIR)  

    print("syspath begin:" + "="*50)    
    for pth in syspath:
        print(pth)    
    print("syspath end:" + "="*50)    

    # this example is intended to be used in Maya

    import dna_viewer
    reload(dna_viewer)
    from dna_viewer import show_dna_viewer_window
    show_dna_viewer_window(ROOT_DIR)
except Exception as e:
    traceback.print_exc()