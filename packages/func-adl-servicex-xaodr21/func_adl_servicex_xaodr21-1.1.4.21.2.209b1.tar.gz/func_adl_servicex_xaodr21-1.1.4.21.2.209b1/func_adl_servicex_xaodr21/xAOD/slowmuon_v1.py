from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'beta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'beta',
        'return_type': 'float',
    },
    'betaT': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'betaT',
        'return_type': 'float',
    },
    'ann': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'ann',
        'return_type': 'float',
    },
    'nRpcHits': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'nRpcHits',
        'return_type': 'int',
    },
    'nTileCells': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'nTileCells',
        'return_type': 'int',
    },
    'rpcBetaAvg': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'rpcBetaAvg',
        'return_type': 'float',
    },
    'rpcBetaRms': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'rpcBetaRms',
        'return_type': 'float',
    },
    'rpcBetaChi2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'rpcBetaChi2',
        'return_type': 'float',
    },
    'rpcBetaDof': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'rpcBetaDof',
        'return_type': 'int',
    },
    'mdtBetaAvg': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'mdtBetaAvg',
        'return_type': 'float',
    },
    'mdtBetaRms': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'mdtBetaRms',
        'return_type': 'float',
    },
    'mdtBetaChi2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'mdtBetaChi2',
        'return_type': 'float',
    },
    'mdtBetaDof': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'mdtBetaDof',
        'return_type': 'int',
    },
    'caloBetaAvg': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'caloBetaAvg',
        'return_type': 'float',
    },
    'caloBetaRms': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'caloBetaRms',
        'return_type': 'float',
    },
    'caloBetaChi2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'caloBetaChi2',
        'return_type': 'float',
    },
    'caloBetaDof': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'caloBetaDof',
        'return_type': 'int',
    },
    'dEdxPixel': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'dEdxPixel',
        'return_type': 'float',
    },
    'dEdxCalo': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'dEdxCalo',
        'return_type': 'float',
    },
    'dEdxNClusters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'dEdxNClusters',
        'return_type': 'int',
    },
    'muonLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'muonLink',
        'return_type': 'const ElementLink<DataVector<xAOD::Muon_v1>>',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::SlowMuon_v1',
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
            'name': 'xAODMuon/versions/SlowMuon_v1.h',
            'body_includes': ["xAODMuon/versions/SlowMuon_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class SlowMuon_v1:
    "A class"

    def beta(self) -> float:
        "A method"
        ...

    def betaT(self) -> float:
        "A method"
        ...

    def ann(self) -> float:
        "A method"
        ...

    def nRpcHits(self) -> int:
        "A method"
        ...

    def nTileCells(self) -> int:
        "A method"
        ...

    def rpcBetaAvg(self) -> float:
        "A method"
        ...

    def rpcBetaRms(self) -> float:
        "A method"
        ...

    def rpcBetaChi2(self) -> float:
        "A method"
        ...

    def rpcBetaDof(self) -> int:
        "A method"
        ...

    def mdtBetaAvg(self) -> float:
        "A method"
        ...

    def mdtBetaRms(self) -> float:
        "A method"
        ...

    def mdtBetaChi2(self) -> float:
        "A method"
        ...

    def mdtBetaDof(self) -> int:
        "A method"
        ...

    def caloBetaAvg(self) -> float:
        "A method"
        ...

    def caloBetaRms(self) -> float:
        "A method"
        ...

    def caloBetaChi2(self) -> float:
        "A method"
        ...

    def caloBetaDof(self) -> int:
        "A method"
        ...

    def dEdxPixel(self) -> float:
        "A method"
        ...

    def dEdxCalo(self) -> float:
        "A method"
        ...

    def dEdxNClusters(self) -> int:
        "A method"
        ...

    def muonLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_muon_v1__.ElementLink_DataVector_xAOD_Muon_v1__:
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
