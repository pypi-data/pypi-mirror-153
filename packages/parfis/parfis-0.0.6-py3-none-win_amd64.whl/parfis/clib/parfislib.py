import sys
import os
from ctypes import *
from importlib import reload

# import .datastruct as ds
from .datastruct import PyCfgData, PySimDataClass, Vec3DBase, Type
# import datastruct as ds

class Parfis:

    lib = None
    libPath = None

    currPath = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    
    @staticmethod
    def load_lib(mode='Release', stateType='double'):
        """ Loads speciffic library version in memory. This is needed
        only once per script life. By loading with different parameters
        the dynamic library get unloaded and different version is loaded.

        Args:
            mode (str): Available modes:

                - 'Release' - load release version
                - 'Debug' - load debug version
                - 'Copy' - load debug version if python is in debug mode, otherwise load release version

            stateType (str): Available state types:

                - 'double' - load library with state type double
                - 'float' - load library with state type float
        """

        linuxRelease32Lib = os.path.join(Parfis.currPath, "libparfis32.so")
        linuxDebug32Lib = os.path.join(Parfis.currPath, "libparfis32d.so")
        winRelease32Lib = os.path.join(Parfis.currPath, "parfis32.dll")
        winDebug32Lib = os.path.join(Parfis.currPath, "parfis32d.dll")
        linuxRelease64Lib = os.path.join(Parfis.currPath, "libparfis64.so")
        linuxDebug64Lib = os.path.join(Parfis.currPath, "libparfis64d.so")
        winRelease64Lib = os.path.join(Parfis.currPath, "parfis64.dll")
        winDebug64Lib = os.path.join(Parfis.currPath, "parfis64d.dll")

        pathBackup = os.environ['PATH'].split(os.pathsep)

        releaseLib = ""
        debugLib = ""
        if sys.platform == "linux":
            if stateType == "double":
                releaseLib = linuxRelease64Lib
                debugLib = linuxDebug64Lib
            elif stateType == "float":
                releaseLib = linuxRelease32Lib
                debugLib = linuxDebug32Lib
        elif sys.platform == "win32":
            if stateType == "double":
                releaseLib = winRelease64Lib
                debugLib = winDebug64Lib
            elif stateType == "float":
                releaseLib = winRelease32Lib
                debugLib = winDebug32Lib

        if not os.path.isfile(releaseLib) and not os.path.isfile(debugLib):
            print("Library file not found!")
            sys.exit(1)

        loadRelease = True
        if mode == 'Copy':
            gettrace = getattr(sys, 'gettrace', None)
            if gettrace() and os.path.isfile(debugLib):
                loadRelease == False
        elif mode == 'Debug':
            loadRelease = False

        if loadRelease and not os.path.isfile(releaseLib):
            print(f"Requested Release lib: {releaseLib} wasn't found falling back to Debug lib")
            loadRelease = False
        if not loadRelease and not os.path.isfile(debugLib):
            print(f"Requested Debug lib: {debugLib} wasn't found falling back to Release lib")
            loadRelease = True

        if loadRelease:
            libPath = releaseLib
        else:
            libPath = debugLib

        # needed when the lib is linked with non-system-available dependencies
        os.environ['PATH'] = os.pathsep.join(
            pathBackup + [os.path.dirname(libPath)])

        # If you want to load different lib version
        if Parfis.lib != None and Parfis.libPath != libPath:
            Parfis.unload_lib()
            # PySimData = reload(PySimData)
        elif Parfis.lib != None:
            # If it is the same lib - do nothing
            return

        Parfis.lib = cdll.LoadLibrary(libPath)
        Parfis.libPath = libPath

        if stateType == 'float':
            Type.state_t = c_float
        elif stateType == 'double':
            Type.state_t = c_double

        print(f"Successfully loaded lib file: {libPath[len(Parfis.currPath)+1:]}")

        Parfis.lib.info.argtypes = None
        Parfis.lib.info.restype = c_char_p

        Parfis.lib.newParfis.argtypes = [c_char_p]
        Parfis.lib.newParfis.restype = c_uint32

        Parfis.lib.deleteParfis.argtypes = [c_uint32]
        Parfis.lib.deleteParfis.restype = c_int

        Parfis.lib.deleteAll.argtypes = None
        Parfis.lib.deleteAll.restype = c_int

        Parfis.lib.setPyCfgData.argtypes = [c_uint32]
        Parfis.lib.setPyCfgData.restype = c_int

        Parfis.lib.getPyCfgData.argtypes = [c_uint32]
        Parfis.lib.getPyCfgData.restype = POINTER(PyCfgData)

        Parfis.lib.setPySimData.argtypes = [c_uint32]
        Parfis.lib.setPySimData.restype = c_int

        Parfis.lib.getPySimData.argtypes = [c_uint32]
        Parfis.lib.getPySimData.restype = POINTER(PySimDataClass())

        Parfis.lib.setConfig.argtypes = [c_uint32, c_char_p]
        Parfis.lib.setConfig.restype = c_int

        Parfis.lib.loadCfgData.argtypes = [c_uint32]
        Parfis.lib.loadCfgData.restype = c_int
        
        Parfis.lib.loadSimData.argtypes = [c_uint32]
        Parfis.lib.loadSimData.restype = c_int

        Parfis.lib.runCommandChain.argtypes = [c_uint32, c_char_p]
        Parfis.lib.runCommandChain.restype = c_int

    @staticmethod
    def unload_lib():
        print(f"Unload lib: {Parfis.libPath[len(Parfis.currPath)+1:]}")
        if sys.platform == "linux":
            dlclose_func = cdll.LoadLibrary('').dlclose
            dlclose_func.argtypes = [c_void_p]
            handle = Parfis.lib._handle
            del Parfis.lib
            dlclose_func(handle)
        elif sys.platform == "win32":
            from ctypes import wintypes
            handle = Parfis.lib._handle
            del Parfis.lib
            kernel32 = WinDLL('kernel32', use_last_error=True)
            kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
            kernel32.FreeLibrary(handle)
        else:
            raise NotImplementedError("Unknown platform.")

    @staticmethod
    def info() -> str:
        return Parfis.lib.info().decode()
    
    @staticmethod
    def newParfis(cfgStr: str  = "") -> int:
        return Parfis.lib.newParfis(cfgStr.encode())

    @staticmethod
    def deleteParfis(id: int) -> int:
        return Parfis.lib.deleteParfis(id)

    @staticmethod
    def deleteAll() -> int:
        return Parfis.lib.deleteAll()

    @staticmethod
    def getPyCfgData(id: int) -> PyCfgData:
        return Parfis.lib.getPyCfgData(id)[0]

    @staticmethod
    def setPyCfgData(id: int) -> int:
        return Parfis.lib.setPyCfgData(id)

    @staticmethod
    def getPySimData(id: int) -> PySimDataClass():
        return Parfis.lib.getPySimData(id)[0]

    @staticmethod
    def setPySimData(id: int) -> int:
        return Parfis.lib.setPySimData(id)

    @staticmethod
    def loadCfgData(id: int) -> int:
        return Parfis.lib.loadCfgData(id)

    @staticmethod
    def setConfig(id: int, kvStr: str) -> int:
        return Parfis.lib.setConfig(id, kvStr.encode())

    @staticmethod
    def loadSimData(id: int) -> int:
        return Parfis.lib.loadSimData(id)

    @staticmethod
    def runCommandChain(id: int, cmdStr: str) -> int:
        return Parfis.lib.runCommandChain(id, cmdStr.encode())

    
def getAbsoluteCellId(cellCount: Vec3DBase, node: Vec3DBase) -> int:
    return cellCount.z * (cellCount.y * node.x + node.y) + node.z


if __name__ == "__main__":

    Parfis.load_lib("Copy")
    print(Parfis.info())