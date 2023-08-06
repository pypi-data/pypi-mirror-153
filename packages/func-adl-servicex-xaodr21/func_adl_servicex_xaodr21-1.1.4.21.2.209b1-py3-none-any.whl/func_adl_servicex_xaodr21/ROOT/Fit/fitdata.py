from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'GetCoordComponent': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitData',
        'method_name': 'GetCoordComponent',
        'return_type': 'const double*',
    },
    'Coords': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitData',
        'method_name': 'Coords',
        'return_type': 'const double*',
    },
    'NPoints': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitData',
        'method_name': 'NPoints',
        'return_type': 'unsigned int',
    },
    'Size': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitData',
        'method_name': 'Size',
        'return_type': 'unsigned int',
    },
    'NDim': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitData',
        'method_name': 'NDim',
        'return_type': 'unsigned int',
    },
    'Range': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitData',
        'method_name': 'Range',
        'return_type': 'const ROOT::Fit::DataRange',
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
class FitData:
    "A class"

    def GetCoordComponent(self, ipoint: int, icoord: int) -> float:
        "A method"
        ...

    def Coords(self, ipoint: int) -> float:
        "A method"
        ...

    def NPoints(self) -> int:
        "A method"
        ...

    def Size(self) -> int:
        "A method"
        ...

    def NDim(self) -> int:
        "A method"
        ...

    def Range(self) -> func_adl_servicex_xaodr21.ROOT.Fit.datarange.DataRange:
        "A method"
        ...
