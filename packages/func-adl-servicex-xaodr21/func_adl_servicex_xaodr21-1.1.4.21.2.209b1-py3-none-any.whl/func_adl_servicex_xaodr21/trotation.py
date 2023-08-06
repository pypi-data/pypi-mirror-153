from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'Transform': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'Transform',
        'return_type': 'TRotation',
    },
    'Inverse': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'Inverse',
        'return_type': 'TRotation',
    },
    'Invert': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'Invert',
        'return_type': 'TRotation',
    },
    'RotateAxes': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'RotateAxes',
        'return_type': 'TRotation',
    },
    'SetToIdentity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'SetToIdentity',
        'return_type': 'TRotation',
    },
    'SetXAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'SetXAxis',
        'return_type': 'TRotation',
    },
    'SetYAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'SetYAxis',
        'return_type': 'TRotation',
    },
    'SetZAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'SetZAxis',
        'return_type': 'TRotation',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TRotation',
        'method_name': 'DistancetoPrimitive',
        'return_type': 'int',
    },
}


T = TypeVar('T')


def _add_method_metadata(s: ObjectStream[T], a: ast.Call) -> Tuple[ObjectStream[T], ast.Call]:
    '''Add metadata for a collection to the func_adl stream if we know about it
    '''
    assert isinstance(a.func, ast.Attribute)
    if a.func.attr in _method_map:
        s_update = s.MetaData(_method_map[a.func.attr])
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TRotation:
    "A class"

    def Transform(self, noname_arg: TRotation) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def Inverse(self) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def Invert(self) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def RotateAxes(self, newX: TVector3, newY: TVector3, newZ: TVector3) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def SetToIdentity(self) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def SetXAxis(self, axis: TVector3) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def SetYAxis(self, axis: TVector3) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def SetZAxis(self, axis: TVector3) -> func_adl_servicex_xaodr21.trotation.TRotation:
        "A method"
        ...

    def ImplFileLine(self) -> int:
        "A method"
        ...

    def DeclFileLine(self) -> int:
        "A method"
        ...

    def DistancetoPrimitive(self, px: int, py: int) -> int:
        "A method"
        ...
