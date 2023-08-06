from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'pt',
        'return_type': 'double',
        'deref_count': 2
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'eta',
        'return_type': 'double',
        'deref_count': 2
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'phi',
        'return_type': 'double',
        'deref_count': 2
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'm',
        'return_type': 'double',
        'deref_count': 2
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'e',
        'return_type': 'double',
        'deref_count': 2
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'rapidity',
        'return_type': 'double',
        'deref_count': 2
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
        'deref_count': 2
    },
    'charge': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'charge',
        'return_type': 'float',
        'deref_count': 2
    },
    'd0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'd0',
        'return_type': 'float',
        'deref_count': 2
    },
    'z0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'z0',
        'return_type': 'float',
        'deref_count': 2
    },
    'phi0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'phi0',
        'return_type': 'float',
        'deref_count': 2
    },
    'theta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'theta',
        'return_type': 'float',
        'deref_count': 2
    },
    'qOverP': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'qOverP',
        'return_type': 'float',
        'deref_count': 2
    },
    'definingParametersCovMatrixVec': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'definingParametersCovMatrixVec',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
        'deref_count': 2
    },
    'vx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'vx',
        'return_type': 'float',
        'deref_count': 2
    },
    'vy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'vy',
        'return_type': 'float',
        'deref_count': 2
    },
    'vz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'vz',
        'return_type': 'float',
        'deref_count': 2
    },
    'numberOfParameters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'numberOfParameters',
        'return_type': 'int',
        'deref_count': 2
    },
    'parameterX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'parameterX',
        'return_type': 'float',
        'deref_count': 2
    },
    'parameterY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'parameterY',
        'return_type': 'float',
        'deref_count': 2
    },
    'parameterZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'parameterZ',
        'return_type': 'float',
        'deref_count': 2
    },
    'parameterPX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'parameterPX',
        'return_type': 'float',
        'deref_count': 2
    },
    'parameterPY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'parameterPY',
        'return_type': 'float',
        'deref_count': 2
    },
    'parameterPZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'parameterPZ',
        'return_type': 'float',
        'deref_count': 2
    },
    'radiusOfFirstHit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'radiusOfFirstHit',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamlineTiltX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'beamlineTiltX',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamlineTiltY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'beamlineTiltY',
        'return_type': 'float',
        'deref_count': 2
    },
    'hitPattern': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'hitPattern',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'chiSquared': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'chiSquared',
        'return_type': 'float',
        'deref_count': 2
    },
    'numberDoF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'numberDoF',
        'return_type': 'float',
        'deref_count': 2
    },
    'vertexLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'vertexLink',
        'return_type': 'const ElementLink<DataVector<xAOD::Vertex_v1>>',
        'deref_count': 2
    },
    'vertex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'vertex',
        'return_type': 'const xAOD::Vertex_v1*',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
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
class ElementLink_DataVector_xAOD_TrackParticle_v1__:
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def pt(self) -> float:
        "A method"
        ...

    def eta(self) -> float:
        "A method"
        ...

    def phi(self) -> float:
        "A method"
        ...

    def m(self) -> float:
        "A method"
        ...

    def e(self) -> float:
        "A method"
        ...

    def rapidity(self) -> float:
        "A method"
        ...

    def p4(self) -> func_adl_servicex_xaodr21.tlorentzvector.TLorentzVector:
        "A method"
        ...

    def charge(self) -> float:
        "A method"
        ...

    def d0(self) -> float:
        "A method"
        ...

    def z0(self) -> float:
        "A method"
        ...

    def phi0(self) -> float:
        "A method"
        ...

    def theta(self) -> float:
        "A method"
        ...

    def qOverP(self) -> float:
        "A method"
        ...

    def definingParametersCovMatrixVec(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def vx(self) -> float:
        "A method"
        ...

    def vy(self) -> float:
        "A method"
        ...

    def vz(self) -> float:
        "A method"
        ...

    def numberOfParameters(self) -> int:
        "A method"
        ...

    def parameterX(self, index: int) -> float:
        "A method"
        ...

    def parameterY(self, index: int) -> float:
        "A method"
        ...

    def parameterZ(self, index: int) -> float:
        "A method"
        ...

    def parameterPX(self, index: int) -> float:
        "A method"
        ...

    def parameterPY(self, index: int) -> float:
        "A method"
        ...

    def parameterPZ(self, index: int) -> float:
        "A method"
        ...

    def radiusOfFirstHit(self) -> float:
        "A method"
        ...

    def beamlineTiltX(self) -> float:
        "A method"
        ...

    def beamlineTiltY(self) -> float:
        "A method"
        ...

    def hitPattern(self) -> int:
        "A method"
        ...

    def chiSquared(self) -> float:
        "A method"
        ...

    def numberDoF(self) -> float:
        "A method"
        ...

    def vertexLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_vertex_v1__.ElementLink_DataVector_xAOD_Vertex_v1__:
        "A method"
        ...

    def vertex(self) -> func_adl_servicex_xaodr21.xAOD.vertex_v1.Vertex_v1:
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
