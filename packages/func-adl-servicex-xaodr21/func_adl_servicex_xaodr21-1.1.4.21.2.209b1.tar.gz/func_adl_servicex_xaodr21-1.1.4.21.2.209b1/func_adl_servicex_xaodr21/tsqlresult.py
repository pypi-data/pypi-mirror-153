from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'GetFieldCount': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TSQLResult',
        'method_name': 'GetFieldCount',
        'return_type': 'int',
    },
    'GetRowCount': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TSQLResult',
        'method_name': 'GetRowCount',
        'return_type': 'int',
    },
    'Next': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TSQLResult',
        'method_name': 'Next',
        'return_type': 'TSQLRow*',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TSQLResult',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TSQLResult',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TSQLResult',
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
class TSQLResult:
    "A class"

    def GetFieldCount(self) -> int:
        "A method"
        ...

    def GetRowCount(self) -> int:
        "A method"
        ...

    def Next(self) -> func_adl_servicex_xaodr21.tsqlrow.TSQLRow:
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
