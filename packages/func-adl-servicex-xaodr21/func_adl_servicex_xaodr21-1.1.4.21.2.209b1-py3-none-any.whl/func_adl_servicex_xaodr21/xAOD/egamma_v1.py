from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'm',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'e',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
    },
    'nCaloClusters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'nCaloClusters',
        'return_type': 'int',
    },
    'caloCluster': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'caloCluster',
        'return_type': 'const xAOD::CaloCluster_v1*',
    },
    'caloClusterLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'caloClusterLink',
        'return_type': 'const ElementLink<DataVector<xAOD::CaloCluster_v1>>',
    },
    'caloClusterLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'caloClusterLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::CaloCluster_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::CaloCluster_v1>>>',
    },
    'ambiguousObject': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'ambiguousObject',
        'return_type': 'const xAOD::Egamma_v1*',
    },
    'isGoodOQ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'isGoodOQ',
        'return_type': 'bool',
    },
    'OQ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'OQ',
        'return_type': 'unsigned int',
    },
    'likelihoodValue': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'likelihoodValue',
        'return_type': 'bool',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Egamma_v1',
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
            'name': 'xAODEgamma/versions/Egamma_v1.h',
            'body_includes': ["xAODEgamma/versions/Egamma_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class Egamma_v1:
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

    def nCaloClusters(self) -> int:
        "A method"
        ...

    def caloCluster(self, index: int) -> func_adl_servicex_xaodr21.xAOD.calocluster_v1.CaloCluster_v1:
        "A method"
        ...

    def caloClusterLink(self, index: int) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_calocluster_v1__.ElementLink_DataVector_xAOD_CaloCluster_v1__:
        "A method"
        ...

    def caloClusterLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_calocluster_v1___.vector_ElementLink_DataVector_xAOD_CaloCluster_v1___:
        "A method"
        ...

    def ambiguousObject(self) -> func_adl_servicex_xaodr21.xAOD.egamma_v1.Egamma_v1:
        "A method"
        ...

    def isGoodOQ(self, mask: int) -> bool:
        "A method"
        ...

    def OQ(self) -> int:
        "A method"
        ...

    def likelihoodValue(self, value: float, LHValue: str) -> bool:
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
