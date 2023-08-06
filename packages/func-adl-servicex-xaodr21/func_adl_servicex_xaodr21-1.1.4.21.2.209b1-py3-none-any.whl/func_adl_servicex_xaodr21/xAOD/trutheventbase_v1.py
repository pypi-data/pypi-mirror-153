from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'truthParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'truthParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TruthParticle_v1>>>',
    },
    'nTruthParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'nTruthParticles',
        'return_type': 'int',
    },
    'truthParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'truthParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TruthParticle_v1>>',
    },
    'truthParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'truthParticle',
        'return_type': 'const xAOD::TruthParticle_v1*',
    },
    'truthVertexLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'truthVertexLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TruthVertex_v1>>>',
    },
    'nTruthVertices': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'nTruthVertices',
        'return_type': 'int',
    },
    'truthVertexLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'truthVertexLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TruthVertex_v1>>',
    },
    'truthVertex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'truthVertex',
        'return_type': 'const xAOD::TruthVertex_v1*',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TruthEventBase_v1',
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
            'name': 'xAODTruth/versions/TruthEventBase_v1.h',
            'body_includes': ["xAODTruth/versions/TruthEventBase_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TruthEventBase_v1:
    "A class"

    def truthParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_truthparticle_v1___.vector_ElementLink_DataVector_xAOD_TruthParticle_v1___:
        "A method"
        ...

    def nTruthParticles(self) -> int:
        "A method"
        ...

    def truthParticleLink(self, index: int) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_truthparticle_v1__.ElementLink_DataVector_xAOD_TruthParticle_v1__:
        "A method"
        ...

    def truthParticle(self, index: int) -> func_adl_servicex_xaodr21.xAOD.truthparticle_v1.TruthParticle_v1:
        "A method"
        ...

    def truthVertexLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_truthvertex_v1___.vector_ElementLink_DataVector_xAOD_TruthVertex_v1___:
        "A method"
        ...

    def nTruthVertices(self) -> int:
        "A method"
        ...

    def truthVertexLink(self, index: int) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_truthvertex_v1__.ElementLink_DataVector_xAOD_TruthVertex_v1__:
        "A method"
        ...

    def truthVertex(self, index: int) -> func_adl_servicex_xaodr21.xAOD.truthvertex_v1.TruthVertex_v1:
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
