from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'EtaPhiVector': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'EtaPhiVector',
        'return_type': 'TVector2',
    },
    'Unit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'Unit',
        'return_type': 'TVector3',
    },
    'Orthogonal': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'Orthogonal',
        'return_type': 'TVector3',
    },
    'Cross': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'Cross',
        'return_type': 'TVector3',
    },
    'Transform': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'Transform',
        'return_type': 'TVector3',
    },
    'XYvector': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'XYvector',
        'return_type': 'TVector2',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector3',
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
class TVector3:
    "A class"

    def EtaPhiVector(self) -> func_adl_servicex_xaodr21.tvector2.TVector2:
        "A method"
        ...

    def Unit(self) -> func_adl_servicex_xaodr21.tvector3.TVector3:
        "A method"
        ...

    def Orthogonal(self) -> func_adl_servicex_xaodr21.tvector3.TVector3:
        "A method"
        ...

    def Cross(self, noname_arg: TVector3) -> func_adl_servicex_xaodr21.tvector3.TVector3:
        "A method"
        ...

    def Transform(self, noname_arg: TRotation) -> func_adl_servicex_xaodr21.tvector3.TVector3:
        "A method"
        ...

    def XYvector(self) -> func_adl_servicex_xaodr21.tvector2.TVector2:
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
