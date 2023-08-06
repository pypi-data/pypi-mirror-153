from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'm',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'e',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
    },
    'charge': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'charge',
        'return_type': 'float',
    },
    'passesIDCuts': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'passesIDCuts',
        'return_type': 'bool',
    },
    'passesHighPtCuts': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'passesHighPtCuts',
        'return_type': 'bool',
    },
    'primaryTrackParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'primaryTrackParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TrackParticle_v1>>',
    },
    'primaryTrackParticle': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'primaryTrackParticle',
        'return_type': 'const xAOD::TrackParticle_v1*',
    },
    'inDetTrackParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'inDetTrackParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TrackParticle_v1>>',
    },
    'muonSpectrometerTrackParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'muonSpectrometerTrackParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TrackParticle_v1>>',
    },
    'combinedTrackParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'combinedTrackParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TrackParticle_v1>>',
    },
    'extrapolatedMuonSpectrometerTrackParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'extrapolatedMuonSpectrometerTrackParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TrackParticle_v1>>',
    },
    'msOnlyExtrapolatedMuonSpectrometerTrackParticleLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'msOnlyExtrapolatedMuonSpectrometerTrackParticleLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TrackParticle_v1>>',
    },
    'clusterLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'clusterLink',
        'return_type': 'const ElementLink<DataVector<xAOD::CaloCluster_v1>>',
    },
    'cluster': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'cluster',
        'return_type': 'const xAOD::CaloCluster_v1*',
    },
    'muonSegmentLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'muonSegmentLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::MuonSegment_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::MuonSegment_v1>>>',
    },
    'nMuonSegments': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'nMuonSegments',
        'return_type': 'int',
    },
    'muonSegment': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'muonSegment',
        'return_type': 'const xAOD::MuonSegment_v1*',
    },
    'muonSegmentLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'muonSegmentLink',
        'return_type': 'const ElementLink<DataVector<xAOD::MuonSegment_v1>>',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Muon_v1',
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
            'name': 'xAODMuon/versions/Muon_v1.h',
            'body_includes': ["xAODMuon/versions/Muon_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class Muon_v1:
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

    def passesIDCuts(self) -> bool:
        "A method"
        ...

    def passesHighPtCuts(self) -> bool:
        "A method"
        ...

    def primaryTrackParticleLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__.ElementLink_DataVector_xAOD_TrackParticle_v1__:
        "A method"
        ...

    def primaryTrackParticle(self) -> func_adl_servicex_xaodr21.xAOD.trackparticle_v1.TrackParticle_v1:
        "A method"
        ...

    def inDetTrackParticleLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__.ElementLink_DataVector_xAOD_TrackParticle_v1__:
        "A method"
        ...

    def muonSpectrometerTrackParticleLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__.ElementLink_DataVector_xAOD_TrackParticle_v1__:
        "A method"
        ...

    def combinedTrackParticleLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__.ElementLink_DataVector_xAOD_TrackParticle_v1__:
        "A method"
        ...

    def extrapolatedMuonSpectrometerTrackParticleLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__.ElementLink_DataVector_xAOD_TrackParticle_v1__:
        "A method"
        ...

    def msOnlyExtrapolatedMuonSpectrometerTrackParticleLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__.ElementLink_DataVector_xAOD_TrackParticle_v1__:
        "A method"
        ...

    def clusterLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_calocluster_v1__.ElementLink_DataVector_xAOD_CaloCluster_v1__:
        "A method"
        ...

    def cluster(self) -> func_adl_servicex_xaodr21.xAOD.calocluster_v1.CaloCluster_v1:
        "A method"
        ...

    def muonSegmentLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_muonsegment_v1___.vector_ElementLink_DataVector_xAOD_MuonSegment_v1___:
        "A method"
        ...

    def nMuonSegments(self) -> int:
        "A method"
        ...

    def muonSegment(self, i: int) -> func_adl_servicex_xaodr21.xAOD.muonsegment_v1.MuonSegment_v1:
        "A method"
        ...

    def muonSegmentLink(self, i: int) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_muonsegment_v1__.ElementLink_DataVector_xAOD_MuonSegment_v1__:
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
