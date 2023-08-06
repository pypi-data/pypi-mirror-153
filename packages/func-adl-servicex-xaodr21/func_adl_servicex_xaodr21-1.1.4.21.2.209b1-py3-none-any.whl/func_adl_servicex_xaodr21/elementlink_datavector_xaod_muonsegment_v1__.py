from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'x': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'x',
        'return_type': 'float',
        'deref_count': 2
    },
    'y': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'y',
        'return_type': 'float',
        'deref_count': 2
    },
    'z': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'z',
        'return_type': 'float',
        'deref_count': 2
    },
    'px': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'px',
        'return_type': 'float',
        'deref_count': 2
    },
    'py': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'py',
        'return_type': 'float',
        'deref_count': 2
    },
    'pz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'pz',
        'return_type': 'float',
        'deref_count': 2
    },
    't0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 't0',
        'return_type': 'float',
        'deref_count': 2
    },
    't0error': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 't0error',
        'return_type': 'float',
        'deref_count': 2
    },
    'chiSquared': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'chiSquared',
        'return_type': 'float',
        'deref_count': 2
    },
    'numberDoF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'numberDoF',
        'return_type': 'float',
        'deref_count': 2
    },
    'sector': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'sector',
        'return_type': 'int',
        'deref_count': 2
    },
    'etaIndex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'etaIndex',
        'return_type': 'int',
        'deref_count': 2
    },
    'nPrecisionHits': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'nPrecisionHits',
        'return_type': 'int',
        'deref_count': 2
    },
    'nPhiLayers': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'nPhiLayers',
        'return_type': 'int',
        'deref_count': 2
    },
    'nTrigEtaLayers': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'nTrigEtaLayers',
        'return_type': 'int',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'method_name': 'isAvailable',
        'return_type': 'bool',
        'deref_count': 2
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
class ElementLink_DataVector_xAOD_MuonSegment_v1__:
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def x(self) -> float:
        "A method"
        ...

    def y(self) -> float:
        "A method"
        ...

    def z(self) -> float:
        "A method"
        ...

    def px(self) -> float:
        "A method"
        ...

    def py(self) -> float:
        "A method"
        ...

    def pz(self) -> float:
        "A method"
        ...

    def t0(self) -> float:
        "A method"
        ...

    def t0error(self) -> float:
        "A method"
        ...

    def chiSquared(self) -> float:
        "A method"
        ...

    def numberDoF(self) -> float:
        "A method"
        ...

    def sector(self) -> int:
        "A method"
        ...

    def etaIndex(self) -> int:
        "A method"
        ...

    def nPrecisionHits(self) -> int:
        "A method"
        ...

    def nPhiLayers(self) -> int:
        "A method"
        ...

    def nTrigEtaLayers(self) -> int:
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
