from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'empty': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'empty',
        'return_type': 'bool',
    },
    'size': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'size',
        'return_type': 'int',
    },
    'at': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'at',
        'return_type': 'xAOD::JetConstituent',
    },
    'front': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'front',
        'return_type': 'xAOD::JetConstituent',
    },
    'back': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'back',
        'return_type': 'xAOD::JetConstituent',
    },
    'asSTLVector': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituentVector',
        'method_name': 'asSTLVector',
        'return_type_element': 'xAOD::JetConstituent',
        'return_type_collection': 'vector<xAOD::JetConstituent>',
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
class JetConstituentVector(Iterable[func_adl_servicex_xaodr21.xAOD.jetconstituent.JetConstituent]):
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def empty(self) -> bool:
        "A method"
        ...

    def size(self) -> int:
        "A method"
        ...

    def at(self, i: int) -> func_adl_servicex_xaodr21.xAOD.jetconstituent.JetConstituent:
        "A method"
        ...

    def front(self) -> func_adl_servicex_xaodr21.xAOD.jetconstituent.JetConstituent:
        "A method"
        ...

    def back(self) -> func_adl_servicex_xaodr21.xAOD.jetconstituent.JetConstituent:
        "A method"
        ...

    def asSTLVector(self) -> func_adl_servicex_xaodr21.vector_xaod_jetconstituent_.vector_xAOD_JetConstituent_:
        "A method"
        ...
