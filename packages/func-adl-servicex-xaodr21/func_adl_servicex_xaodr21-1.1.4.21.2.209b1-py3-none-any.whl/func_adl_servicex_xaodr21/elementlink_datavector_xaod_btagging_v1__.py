from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'SV0_significance3D': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV0_significance3D',
        'return_type': 'double',
        'deref_count': 2
    },
    'SV0_TrackParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV0_TrackParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TrackParticle_v1>>>',
        'deref_count': 2
    },
    'SV0_TrackParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV0_TrackParticle',
        'return_type': 'const xAOD::TrackParticle_v1*',
        'deref_count': 2
    },
    'nSV0_TrackParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'nSV0_TrackParticles',
        'return_type': 'int',
        'deref_count': 2
    },
    'SV1_pb': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1_pb',
        'return_type': 'double',
        'deref_count': 2
    },
    'SV1_pc': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1_pc',
        'return_type': 'double',
        'deref_count': 2
    },
    'SV1_pu': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1_pu',
        'return_type': 'double',
        'deref_count': 2
    },
    'SV1_loglikelihoodratio': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1_loglikelihoodratio',
        'return_type': 'double',
        'deref_count': 2
    },
    'SV1_TrackParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1_TrackParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TrackParticle_v1>>>',
        'deref_count': 2
    },
    'SV1_TrackParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1_TrackParticle',
        'return_type': 'const xAOD::TrackParticle_v1*',
        'deref_count': 2
    },
    'nSV1_TrackParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'nSV1_TrackParticles',
        'return_type': 'int',
        'deref_count': 2
    },
    'IP2D_pb': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP2D_pb',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP2D_pc': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP2D_pc',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP2D_pu': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP2D_pu',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP2D_loglikelihoodratio': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP2D_loglikelihoodratio',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP2D_TrackParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP2D_TrackParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TrackParticle_v1>>>',
        'deref_count': 2
    },
    'IP2D_TrackParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP2D_TrackParticle',
        'return_type': 'const xAOD::TrackParticle_v1*',
        'deref_count': 2
    },
    'nIP2D_TrackParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'nIP2D_TrackParticles',
        'return_type': 'int',
        'deref_count': 2
    },
    'IP3D_pb': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP3D_pb',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP3D_pc': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP3D_pc',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP3D_pu': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP3D_pu',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP3D_loglikelihoodratio': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP3D_loglikelihoodratio',
        'return_type': 'double',
        'deref_count': 2
    },
    'IP3D_TrackParticleLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP3D_TrackParticleLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TrackParticle_v1>>>',
        'deref_count': 2
    },
    'IP3D_TrackParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'IP3D_TrackParticle',
        'return_type': 'const xAOD::TrackParticle_v1*',
        'deref_count': 2
    },
    'nIP3D_TrackParticles': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'nIP3D_TrackParticles',
        'return_type': 'int',
        'deref_count': 2
    },
    'SV1plusIP3D_discriminant': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'SV1plusIP3D_discriminant',
        'return_type': 'double',
        'deref_count': 2
    },
    'JetFitter_pb': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'JetFitter_pb',
        'return_type': 'double',
        'deref_count': 2
    },
    'JetFitter_pc': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'JetFitter_pc',
        'return_type': 'double',
        'deref_count': 2
    },
    'JetFitter_pu': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'JetFitter_pu',
        'return_type': 'double',
        'deref_count': 2
    },
    'JetFitter_loglikelihoodratio': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'JetFitter_loglikelihoodratio',
        'return_type': 'double',
        'deref_count': 2
    },
    'MV1_discriminant': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'MV1_discriminant',
        'return_type': 'double',
        'deref_count': 2
    },
    'loglikelihoodratio': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'loglikelihoodratio',
        'return_type': 'bool',
        'deref_count': 2
    },
    'MVx_discriminant': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'MVx_discriminant',
        'return_type': 'bool',
        'deref_count': 2
    },
    'pu': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'pu',
        'return_type': 'bool',
        'deref_count': 2
    },
    'pb': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'pb',
        'return_type': 'bool',
        'deref_count': 2
    },
    'pc': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'pc',
        'return_type': 'bool',
        'deref_count': 2
    },
    'calcLLR': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'calcLLR',
        'return_type': 'double',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::BTagging_v1>>',
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
class ElementLink_DataVector_xAOD_BTagging_v1__:
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def SV0_significance3D(self) -> float:
        "A method"
        ...

    def SV0_TrackParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_trackparticle_v1___.vector_ElementLink_DataVector_xAOD_TrackParticle_v1___:
        "A method"
        ...

    def SV0_TrackParticle(self, i: int) -> func_adl_servicex_xaodr21.xAOD.trackparticle_v1.TrackParticle_v1:
        "A method"
        ...

    def nSV0_TrackParticles(self) -> int:
        "A method"
        ...

    def SV1_pb(self) -> float:
        "A method"
        ...

    def SV1_pc(self) -> float:
        "A method"
        ...

    def SV1_pu(self) -> float:
        "A method"
        ...

    def SV1_loglikelihoodratio(self) -> float:
        "A method"
        ...

    def SV1_TrackParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_trackparticle_v1___.vector_ElementLink_DataVector_xAOD_TrackParticle_v1___:
        "A method"
        ...

    def SV1_TrackParticle(self, i: int) -> func_adl_servicex_xaodr21.xAOD.trackparticle_v1.TrackParticle_v1:
        "A method"
        ...

    def nSV1_TrackParticles(self) -> int:
        "A method"
        ...

    def IP2D_pb(self) -> float:
        "A method"
        ...

    def IP2D_pc(self) -> float:
        "A method"
        ...

    def IP2D_pu(self) -> float:
        "A method"
        ...

    def IP2D_loglikelihoodratio(self) -> float:
        "A method"
        ...

    def IP2D_TrackParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_trackparticle_v1___.vector_ElementLink_DataVector_xAOD_TrackParticle_v1___:
        "A method"
        ...

    def IP2D_TrackParticle(self, i: int) -> func_adl_servicex_xaodr21.xAOD.trackparticle_v1.TrackParticle_v1:
        "A method"
        ...

    def nIP2D_TrackParticles(self) -> int:
        "A method"
        ...

    def IP3D_pb(self) -> float:
        "A method"
        ...

    def IP3D_pc(self) -> float:
        "A method"
        ...

    def IP3D_pu(self) -> float:
        "A method"
        ...

    def IP3D_loglikelihoodratio(self) -> float:
        "A method"
        ...

    def IP3D_TrackParticleLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_trackparticle_v1___.vector_ElementLink_DataVector_xAOD_TrackParticle_v1___:
        "A method"
        ...

    def IP3D_TrackParticle(self, i: int) -> func_adl_servicex_xaodr21.xAOD.trackparticle_v1.TrackParticle_v1:
        "A method"
        ...

    def nIP3D_TrackParticles(self) -> int:
        "A method"
        ...

    def SV1plusIP3D_discriminant(self) -> float:
        "A method"
        ...

    def JetFitter_pb(self) -> float:
        "A method"
        ...

    def JetFitter_pc(self) -> float:
        "A method"
        ...

    def JetFitter_pu(self) -> float:
        "A method"
        ...

    def JetFitter_loglikelihoodratio(self) -> float:
        "A method"
        ...

    def MV1_discriminant(self) -> float:
        "A method"
        ...

    def loglikelihoodratio(self, taggername: str, value: float, signal: str, bckgd: str) -> bool:
        "A method"
        ...

    def MVx_discriminant(self, taggername: str, value: float) -> bool:
        "A method"
        ...

    def pu(self, taggername: str, value: float) -> bool:
        "A method"
        ...

    def pb(self, taggername: str, value: float) -> bool:
        "A method"
        ...

    def pc(self, taggername: str, value: float) -> bool:
        "A method"
        ...

    def calcLLR(self, num: float, den: float) -> float:
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
