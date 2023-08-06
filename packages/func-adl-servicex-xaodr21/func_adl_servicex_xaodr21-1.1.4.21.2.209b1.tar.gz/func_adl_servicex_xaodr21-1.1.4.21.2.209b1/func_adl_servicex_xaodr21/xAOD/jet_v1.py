from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'm',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'e',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
    },
    'px': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'px',
        'return_type': 'float',
    },
    'py': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'py',
        'return_type': 'float',
    },
    'pz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'pz',
        'return_type': 'float',
    },
    'getConstituents': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'getConstituents',
        'return_type_element': 'xAOD::JetConstituent*',
        'return_type_collection': 'xAOD::JetConstituentVector',
    },
    'numConstituents': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'numConstituents',
        'return_type': 'int',
    },
    'rawConstituent': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'rawConstituent',
        'return_type': 'const xAOD::IParticle*',
    },
    'constituentLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'constituentLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::IParticle>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::IParticle>>>',
    },
    'btagging': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'btagging',
        'return_type': 'const xAOD::BTagging_v1*',
    },
    'btaggingLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'btaggingLink',
        'return_type': 'const ElementLink<DataVector<xAOD::BTagging_v1>>',
    },
    'getSizeParameter': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'getSizeParameter',
        'return_type': 'float',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'getAttribute': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'getAttribute',
        'return_type': 'U',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::Jet_v1',
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
            'name': 'xAODJet/versions/Jet_v1.h',
            'body_includes': ["xAODJet/versions/Jet_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class Jet_v1:
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

    def px(self) -> float:
        "A method"
        ...

    def py(self) -> float:
        "A method"
        ...

    def pz(self) -> float:
        "A method"
        ...

    def getConstituents(self) -> func_adl_servicex_xaodr21.xAOD.jetconstituentvector.JetConstituentVector:
        "A method"
        ...

    def numConstituents(self) -> int:
        "A method"
        ...

    def rawConstituent(self, i: int) -> func_adl_servicex_xaodr21.xAOD.iparticle.IParticle:
        "A method"
        ...

    def constituentLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_iparticle___.vector_ElementLink_DataVector_xAOD_IParticle___:
        "A method"
        ...

    def btagging(self) -> func_adl_servicex_xaodr21.xAOD.btagging_v1.BTagging_v1:
        "A method"
        ...

    def btaggingLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_btagging_v1__.ElementLink_DataVector_xAOD_BTagging_v1__:
        "A method"
        ...

    def getSizeParameter(self) -> float:
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

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr21.type_support.cpp_generic_1arg_callback('getAttribute', s, a, param_1))
    @property
    def getAttribute(self) -> func_adl_servicex_xaodr21.type_support.index_type_forwarder[str]:
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
