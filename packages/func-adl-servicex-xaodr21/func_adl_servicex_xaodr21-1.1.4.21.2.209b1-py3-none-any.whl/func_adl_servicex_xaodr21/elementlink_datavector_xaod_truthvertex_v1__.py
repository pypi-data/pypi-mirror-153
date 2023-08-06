from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'id': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'id',
        'return_type': 'int',
        'deref_count': 2
    },
    'barcode': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'barcode',
        'return_type': 'int',
        'deref_count': 2
    },
    'incomingParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'incomingParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TruthParticle_v1>>>',
        'deref_count': 2
    },
    'nIncomingParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'nIncomingParticles',
        'return_type': 'int',
        'deref_count': 2
    },
    'incomingParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'incomingParticle',
        'return_type': 'const xAOD::TruthParticle_v1*',
        'deref_count': 2
    },
    'outgoingParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'outgoingParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TruthParticle_v1>>>',
        'deref_count': 2
    },
    'nOutgoingParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'nOutgoingParticles',
        'return_type': 'int',
        'deref_count': 2
    },
    'outgoingParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'outgoingParticle',
        'return_type': 'const xAOD::TruthParticle_v1*',
        'deref_count': 2
    },
    'x': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'x',
        'return_type': 'float',
        'deref_count': 2
    },
    'y': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'y',
        'return_type': 'float',
        'deref_count': 2
    },
    'z': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'z',
        'return_type': 'float',
        'deref_count': 2
    },
    'perp': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'perp',
        'return_type': 'float',
        'deref_count': 2
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'eta',
        'return_type': 'float',
        'deref_count': 2
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'phi',
        'return_type': 'float',
        'deref_count': 2
    },
    't': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 't',
        'return_type': 'float',
        'deref_count': 2
    },
    'v4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'v4',
        'return_type': 'const TLorentzVector',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
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
class ElementLink_DataVector_xAOD_TruthVertex_v1__:
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def id(self) -> int:
        "A method"
        ...

    def barcode(self) -> int:
        "A method"
        ...

    def incomingParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_truthparticle_v1___.vector_ElementLink_DataVector_xAOD_TruthParticle_v1___:
        "A method"
        ...

    def nIncomingParticles(self) -> int:
        "A method"
        ...

    def incomingParticle(self, index: int) -> func_adl_servicex_xaodr21.xAOD.truthparticle_v1.TruthParticle_v1:
        "A method"
        ...

    def outgoingParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_truthparticle_v1___.vector_ElementLink_DataVector_xAOD_TruthParticle_v1___:
        "A method"
        ...

    def nOutgoingParticles(self) -> int:
        "A method"
        ...

    def outgoingParticle(self, index: int) -> func_adl_servicex_xaodr21.xAOD.truthparticle_v1.TruthParticle_v1:
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

    def perp(self) -> float:
        "A method"
        ...

    def eta(self) -> float:
        "A method"
        ...

    def phi(self) -> float:
        "A method"
        ...

    def t(self) -> float:
        "A method"
        ...

    def v4(self) -> func_adl_servicex_xaodr21.tlorentzvector.TLorentzVector:
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
