from ctypes import *

class Type():
    """Defines type names similary to the c++ module.
    """
    cellId_t = c_uint32
    stateId_t = c_uint32
    state_t = c_double
    cellPos_t = c_uint16
    nodeFlag_t = c_uint8

class Const():
    noCellId = 0xFFFFFFFF
    noStateId = 0xFFFFFFFF

class Vec3DBase():
    """Base parent class for the Vec3D (resembles template Vec3D).
    Class is inherited from other Vec3D_<type> classes.
    
    """

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def asTuple(self):
        return (self.x, self.y, self.z)

    def asList(self):
        return [self.x, self.y, self.z]

    def __mul__(self, val):
        # Check if it is another Vec3DBase
        if Vec3DBase in [baseClass for baseClass in val.__class__.__bases__]:
            return Vec3DClass(self.type)(self.x*val.x, self.y*val.y, self.z*val.z) 
        # Val is a single value (float or int)
        else:
            return Vec3DClass(self.type)(self.x*val, self.y*val, self.z*val) 

    def __str__(self):
        return f"{{x: {self.x}, y: {self.y}, z: {self.z}}}"

class Vec3D_double(Structure, Vec3DBase):
    _fields_ = [
        ('x', c_double),
        ('y', c_double),
        ('z', c_double)
    ]
    type = c_double

class Vec3D_float(Structure, Vec3DBase):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float)
    ]
    type = c_float

class Vec3D_int(Structure, Vec3DBase):
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('z', c_int)
    ]
    type = c_int

class Vec3D_uint32(Structure, Vec3DBase):
    _fields_ = [
        ('x', c_uint32),
        ('y', c_uint32),
        ('z', c_uint32)
    ]
    type = c_uint32

class Vec3D_uint16(Structure, Vec3DBase):
    _fields_ = [
        ('x', c_uint16),
        ('y', c_uint16),
        ('z', c_uint16)
    ]
    type = c_uint16

def Vec3DClass(cType = c_int):
    if cType == c_float:
        return Vec3D_float
    elif cType == c_double:
            return Vec3D_double
    elif cType == c_int:
        return Vec3D_int
    elif cType == c_uint32:
        return Vec3D_uint32
    elif cType == c_uint16:
        return Vec3D_uint16
    else:
        return None

class State_float(Structure):
    _fields_ = [
        ('next', Type.stateId_t),
        ('prev', Type.stateId_t),
        ('pos', Vec3DClass(c_float)),
        ('vel', Vec3DClass(c_float))
    ]

class State_double(Structure):
    _fields_ = [
        ('next', Type.stateId_t),
        ('prev', Type.stateId_t),
        ('pos', Vec3DClass(c_double)),
        ('vel', Vec3DClass(c_double))
    ]

def StateClass():
    if Type.state_t == c_float:
        return State_float
    elif Type.state_t == c_double:
        return State_double
    else:
        return None

class Cell(Structure):
    _fields_ = [
        ('pos', Vec3DClass(Type.cellPos_t))
    ]

class Specie(Structure):
    _fields_ = [
        ('id', c_uint32),
        ('name', c_char_p),
        ('velInitDist', c_int),
        ('statesPerCell', c_int),
        ('timestepRatio', c_int),
        ('dt', c_double),
        ('idt', c_double),
        ('maxVel', Vec3DClass(c_double)),
        ('velInitDistMin', Vec3DClass(c_double)),
        ('velInitDistMax', Vec3DClass(c_double))
    ]

class PyVecBase:
    def asList(self):
        if self.__class__ == PyVec_char_p:
            return [self.ptr[i].decode() for i in range(self.size)]

class PyVec_char_p(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(c_char_p)),
        ('size', c_size_t)
    ]

class PyVec_State_float(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(State_float)),
        ('size', c_size_t)
    ]

class PyVec_State_double(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(State_double)),
        ('size', c_size_t)
    ]

class PyVec_Cell(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(Cell)),
        ('size', c_size_t)
    ]

class PyVec_uint32(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(c_uint32)),
        ('size', c_size_t)
    ]

class PyVec_uint8(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(c_uint8)),
        ('size', c_size_t)
    ]

class PyVec_uint8(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(c_uint8)),
        ('size', c_size_t)
    ]

class PyVec_Specie(Structure, PyVecBase):
    _fields_ = [
        ('ptr', POINTER(Specie)),
        ('size', c_size_t)
    ]

def PyVecClass(cType = c_char_p):
    if cType == c_char_p:
        return PyVec_char_p
    elif cType == c_uint32:
            return PyVec_uint32
    elif cType == c_uint8:
            return PyVec_uint8
    elif cType == State_float:
        return PyVec_State_float
    elif cType == State_double:
        return PyVec_State_double
    elif cType == Specie:
        return PyVec_Specie
    elif cType == Cell:
        return PyVec_Cell
    else:
        return None

class PyCfgData(Structure):
    """PyCfgData(ctypes.Structure)

    Args:
        geometry: Name of the geometry (ex. 'cylindrical')
        timestep: Timestep in seconds, double
        geometrySize: Pointer to Vec3D_double, size of geometry in meters
        cellCount: Pointer to Vec3D_int, number of cells
    """
    _fields_ = [
        ('geometry', c_char_p),
        ('timestep', c_double),
        ('geometrySize', POINTER(Vec3DClass(c_double))),
        ('cellSize', POINTER(Vec3DClass(c_double))),
        ('periodicBoundary', POINTER(Vec3DClass(c_int))),
        ('cellCount', POINTER(Vec3DClass(c_int))),
        ('specieNameVec', PyVecClass(c_char_p))
    ]

class PySimData_float(Structure):
    _fields_ = [
        ('stateVec', PyVecClass(State_float)),
        ('cellIdVec', PyVecClass(Type.cellId_t)),
        ('cellIdAVec', PyVecClass(Type.cellId_t)),
        ('cellIdBVec', PyVecClass(Type.cellId_t)),
        ('specieVec', PyVecClass(Specie)),
        ('cellVec', PyVecClass(Cell)),
        ('nodeFlagVec', PyVecClass(Type.nodeFlag_t)),
        ('headIdVec', PyVecClass(Type.stateId_t))
    ]

class PySimData_double(Structure):
    _fields_ = [
        ('stateVec', PyVecClass(State_double)),
        ('cellIdVec', PyVecClass(Type.cellId_t)),
        ('cellIdAVec', PyVecClass(Type.cellId_t)),
        ('cellIdBVec', PyVecClass(Type.cellId_t)),
        ('specieVec', PyVecClass(Specie)),
        ('cellVec', PyVecClass(Cell)),
        ('nodeFlagVec', PyVecClass(Type.nodeFlag_t)),
        ('headIdVec', PyVecClass(Type.stateId_t))
    ]

def PySimDataClass():
    if Type.state_t == c_float:
        return PySimData_float
    elif Type.state_t == c_double:
        return PySimData_double
    else:
        return None

if __name__ == '__main__':
    pass