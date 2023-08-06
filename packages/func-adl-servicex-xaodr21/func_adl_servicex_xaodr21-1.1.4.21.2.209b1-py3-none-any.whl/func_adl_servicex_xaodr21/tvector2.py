from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'Unit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
        'method_name': 'Unit',
        'return_type': 'TVector2',
    },
    'Ort': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
        'method_name': 'Ort',
        'return_type': 'TVector2',
    },
    'Proj': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
        'method_name': 'Proj',
        'return_type': 'TVector2',
    },
    'Norm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
        'method_name': 'Norm',
        'return_type': 'TVector2',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TVector2',
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
class TVector2:
    "A class"

    def Unit(self) -> func_adl_servicex_xaodr21.tvector2.TVector2:
        "A method"
        ...

    def Ort(self) -> func_adl_servicex_xaodr21.tvector2.TVector2:
        "A method"
        ...

    def Proj(self, v: TVector2) -> func_adl_servicex_xaodr21.tvector2.TVector2:
        "A method"
        ...

    def Norm(self, v: TVector2) -> func_adl_servicex_xaodr21.tvector2.TVector2:
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
