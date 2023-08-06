from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'mpx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'mpx',
        'return_type': 'double',
    },
    'mpy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'mpy',
        'return_type': 'double',
    },
    'met': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'met',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'sumet': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'sumet',
        'return_type': 'double',
    },
    'name': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'name',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'nameHash': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'nameHash',
        'return_type': 'int',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::MissingET_v1',
        'method_name': 'isAvailable',
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
        s_update = s_update.MetaData({
            'metadata_type': 'inject_code',
            'name': 'xAODMissingET/versions/MissingET_v1.h',
            'body_includes': ["xAODMissingET/versions/MissingET_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class MissingET_v1:
    "A class"

    def mpx(self) -> float:
        "A method"
        ...

    def mpy(self) -> float:
        "A method"
        ...

    def met(self) -> float:
        "A method"
        ...

    def phi(self) -> float:
        "A method"
        ...

    def sumet(self) -> float:
        "A method"
        ...

    def name(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def nameHash(self) -> int:
        "A method"
        ...

    def index(self) -> int:
        "A method"
        ...

    def usingPrivateStore(self) -> bool:
        "A method"
        ...

    def usingStandaloneStore(self) -> bool:
        "A method"
        ...

    def hasStore(self) -> bool:
        "A method"
        ...

    def hasNonConstStore(self) -> bool:
        "A method"
        ...

    def clearDecorations(self) -> bool:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr21.type_support.cpp_generic_1arg_callback('auxdataConst', s, a, param_1))
    @property
    def auxdataConst(self) -> func_adl_servicex_xaodr21.type_support.index_type_forwarder[str]:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr21.type_support.cpp_generic_1arg_callback('isAvailable', s, a, param_1))
    @property
    def isAvailable(self) -> func_adl_servicex_xaodr21.type_support.index_type_forwarder[str]:
        "A method"
        ...
