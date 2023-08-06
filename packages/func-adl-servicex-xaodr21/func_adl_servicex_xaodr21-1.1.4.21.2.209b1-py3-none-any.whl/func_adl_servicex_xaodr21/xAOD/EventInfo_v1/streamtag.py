from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'name': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::EventInfo_v1::StreamTag',
        'method_name': 'name',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'type': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::EventInfo_v1::StreamTag',
        'method_name': 'type',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'obeysLumiblock': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::EventInfo_v1::StreamTag',
        'method_name': 'obeysLumiblock',
        'return_type': 'bool',
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
class StreamTag:
    "A class"

    def name(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def type(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def obeysLumiblock(self) -> bool:
        "A method"
        ...
