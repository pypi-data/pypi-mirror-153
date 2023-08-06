from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'mcChannelNumber': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'mcChannelNumber',
        'return_type': 'unsigned int',
    },
    'weightNames': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'weightNames',
        'return_type_element': 'string',
        'return_type_collection': 'const vector<string>',
    },
    'lhefGenerator': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'lhefGenerator',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'generators': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'generators',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'evgenProcess': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'evgenProcess',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'evgenTune': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'evgenTune',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'hardPDF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'hardPDF',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'softPDF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'softPDF',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthMetaData_v1',
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
            'name': 'xAODTruth/versions/TruthMetaData_v1.h',
            'body_includes': ["xAODTruth/versions/TruthMetaData_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TruthMetaData_v1:
    "A class"

    def mcChannelNumber(self) -> int:
        "A method"
        ...

    def weightNames(self) -> func_adl_servicex_xaodr21.vector_str_.vector_str_:
        "A method"
        ...

    def lhefGenerator(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def generators(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def evgenProcess(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def evgenTune(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def hardPDF(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def softPDF(self) -> func_adl_servicex_xaodr21.str.str:
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
