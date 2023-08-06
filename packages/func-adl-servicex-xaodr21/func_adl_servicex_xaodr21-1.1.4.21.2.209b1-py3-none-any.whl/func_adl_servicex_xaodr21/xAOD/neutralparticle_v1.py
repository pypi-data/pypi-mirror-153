from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'm',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'e',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
    },
    'd0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'd0',
        'return_type': 'float',
    },
    'z0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'z0',
        'return_type': 'float',
    },
    'phi0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'phi0',
        'return_type': 'float',
    },
    'theta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'theta',
        'return_type': 'float',
    },
    'oneOverP': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'oneOverP',
        'return_type': 'float',
    },
    'definingParametersCovMatrixVec': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'definingParametersCovMatrixVec',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'vx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'vx',
        'return_type': 'float',
    },
    'vy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'vy',
        'return_type': 'float',
    },
    'vz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'vz',
        'return_type': 'float',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::NeutralParticle_v1',
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
            'name': 'xAODTracking/versions/NeutralParticle_v1.h',
            'body_includes': ["xAODTracking/versions/NeutralParticle_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class NeutralParticle_v1:
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

    def oneOverP(self) -> float:
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
