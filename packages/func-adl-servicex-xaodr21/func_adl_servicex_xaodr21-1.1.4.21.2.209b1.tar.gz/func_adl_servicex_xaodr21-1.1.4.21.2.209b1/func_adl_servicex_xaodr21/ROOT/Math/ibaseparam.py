from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'Parameters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::IBaseParam',
        'method_name': 'Parameters',
        'return_type': 'const double*',
    },
    'NPar': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::IBaseParam',
        'method_name': 'NPar',
        'return_type': 'unsigned int',
    },
    'ParameterName': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::IBaseParam',
        'method_name': 'ParameterName',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
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
class IBaseParam:
    "A class"

    def Parameters(self) -> float:
        "A method"
        ...

    def NPar(self) -> int:
        "A method"
        ...

    def ParameterName(self, i: int) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...
