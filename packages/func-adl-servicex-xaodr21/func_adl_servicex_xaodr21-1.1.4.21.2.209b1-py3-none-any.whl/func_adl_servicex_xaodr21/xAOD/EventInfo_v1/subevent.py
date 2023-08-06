from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'typeName': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::EventInfo_v1::SubEvent',
        'method_name': 'typeName',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'link': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::EventInfo_v1::SubEvent',
        'method_name': 'link',
        'return_type': 'const ElementLink<DataVector<xAOD::EventInfo_v1>>',
    },
    'ptr': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::EventInfo_v1::SubEvent',
        'method_name': 'ptr',
        'return_type': 'const xAOD::EventInfo_v1*',
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
class SubEvent:
    "A class"

    def typeName(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def link(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_eventinfo_v1__.ElementLink_DataVector_xAOD_EventInfo_v1__:
        "A method"
        ...

    def ptr(self) -> func_adl_servicex_xaodr21.xAOD.eventinfo_v1.EventInfo_v1:
        "A method"
        ...
