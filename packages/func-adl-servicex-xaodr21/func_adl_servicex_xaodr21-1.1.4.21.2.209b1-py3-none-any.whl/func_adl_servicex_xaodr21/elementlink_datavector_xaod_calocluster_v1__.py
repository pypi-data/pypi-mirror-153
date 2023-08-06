from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'pt',
        'return_type': 'double',
        'deref_count': 2
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'eta',
        'return_type': 'double',
        'deref_count': 2
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'phi',
        'return_type': 'double',
        'deref_count': 2
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'm',
        'return_type': 'double',
        'deref_count': 2
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'e',
        'return_type': 'double',
        'deref_count': 2
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'rapidity',
        'return_type': 'double',
        'deref_count': 2
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
        'deref_count': 2
    },
    'et': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'et',
        'return_type': 'double',
        'deref_count': 2
    },
    'energyBE': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'energyBE',
        'return_type': 'float',
        'deref_count': 2
    },
    'etaBE': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'etaBE',
        'return_type': 'float',
        'deref_count': 2
    },
    'phiBE': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'phiBE',
        'return_type': 'float',
        'deref_count': 2
    },
    'samplingPattern': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'samplingPattern',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'nSamples': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'nSamples',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'inBarrel': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'inBarrel',
        'return_type': 'bool',
        'deref_count': 2
    },
    'inEndcap': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'inEndcap',
        'return_type': 'bool',
        'deref_count': 2
    },
    'getClusterEtaSize': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'getClusterEtaSize',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'getClusterPhiSize': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'getClusterPhiSize',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'badChannelList': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'badChannelList',
        'return_type_element': 'xAOD::CaloClusterBadChannelData_v1',
        'return_type_collection': 'const vector<xAOD::CaloClusterBadChannelData_v1>',
        'deref_count': 2
    },
    'getSisterCluster': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'getSisterCluster',
        'return_type': 'const xAOD::CaloCluster_v1*',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
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
class ElementLink_DataVector_xAOD_CaloCluster_v1__:
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

    def et(self) -> float:
        "A method"
        ...

    def energyBE(self, layer: int) -> float:
        "A method"
        ...

    def etaBE(self, layer: int) -> float:
        "A method"
        ...

    def phiBE(self, layer: int) -> float:
        "A method"
        ...

    def samplingPattern(self) -> int:
        "A method"
        ...

    def nSamples(self) -> int:
        "A method"
        ...

    def inBarrel(self) -> bool:
        "A method"
        ...

    def inEndcap(self) -> bool:
        "A method"
        ...

    def getClusterEtaSize(self) -> int:
        "A method"
        ...

    def getClusterPhiSize(self) -> int:
        "A method"
        ...

    def badChannelList(self) -> func_adl_servicex_xaodr21.vector_xaod_caloclusterbadchanneldata_v1_.vector_xAOD_CaloClusterBadChannelData_v1_:
        "A method"
        ...

    def getSisterCluster(self) -> func_adl_servicex_xaodr21.xAOD.calocluster_v1.CaloCluster_v1:
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
