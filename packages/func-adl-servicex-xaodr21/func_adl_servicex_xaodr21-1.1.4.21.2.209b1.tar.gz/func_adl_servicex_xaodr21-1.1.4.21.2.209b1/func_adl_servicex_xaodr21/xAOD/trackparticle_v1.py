from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'm',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'e',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
    },
    'charge': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'charge',
        'return_type': 'float',
    },
    'd0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'd0',
        'return_type': 'float',
    },
    'z0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'z0',
        'return_type': 'float',
    },
    'phi0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'phi0',
        'return_type': 'float',
    },
    'theta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'theta',
        'return_type': 'float',
    },
    'qOverP': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'qOverP',
        'return_type': 'float',
    },
    'definingParametersCovMatrixVec': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'definingParametersCovMatrixVec',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'vx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'vx',
        'return_type': 'float',
    },
    'vy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'vy',
        'return_type': 'float',
    },
    'vz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'vz',
        'return_type': 'float',
    },
    'numberOfParameters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'numberOfParameters',
        'return_type': 'int',
    },
    'parameterX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'parameterX',
        'return_type': 'float',
    },
    'parameterY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'parameterY',
        'return_type': 'float',
    },
    'parameterZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'parameterZ',
        'return_type': 'float',
    },
    'parameterPX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'parameterPX',
        'return_type': 'float',
    },
    'parameterPY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'parameterPY',
        'return_type': 'float',
    },
    'parameterPZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'parameterPZ',
        'return_type': 'float',
    },
    'radiusOfFirstHit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'radiusOfFirstHit',
        'return_type': 'float',
    },
    'beamlineTiltX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'beamlineTiltX',
        'return_type': 'float',
    },
    'beamlineTiltY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'beamlineTiltY',
        'return_type': 'float',
    },
    'hitPattern': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'hitPattern',
        'return_type': 'unsigned int',
    },
    'chiSquared': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'chiSquared',
        'return_type': 'float',
    },
    'numberDoF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'numberDoF',
        'return_type': 'float',
    },
    'vertexLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'vertexLink',
        'return_type': 'const ElementLink<DataVector<xAOD::Vertex_v1>>',
    },
    'vertex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'vertex',
        'return_type': 'const xAOD::Vertex_v1*',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrackParticle_v1',
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
            'name': 'xAODTracking/versions/TrackParticle_v1.h',
            'body_includes': ["xAODTracking/versions/TrackParticle_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TrackParticle_v1:
    "A class"

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
