from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'chi2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'chi2',
        'return_type': 'float',
    },
    'NDF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'NDF',
        'return_type': 'float',
    },
    'pv_compatibility': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'pv_compatibility',
        'return_type': 'float',
    },
    'compToOtherSV': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'compToOtherSV',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'track_chi2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'track_chi2',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'track_NDF': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'track_NDF',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'track_refPx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'track_refPx',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'track_refPy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'track_refPy',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'track_refPz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'track_refPz',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
    },
    'track_links': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'track_links',
        'return_type_element': 'ElementLink<DataVector<xAOD::TrackParticle_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TrackParticle_v1>>>',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::BTagVertex_v1',
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
            'name': 'xAODBTagging/versions/BTagVertex_v1.h',
            'body_includes': ["xAODBTagging/versions/BTagVertex_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class BTagVertex_v1:
    "A class"

    def chi2(self) -> float:
        "A method"
        ...

    def NDF(self) -> float:
        "A method"
        ...

    def pv_compatibility(self) -> float:
        "A method"
        ...

    def compToOtherSV(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def track_chi2(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def track_NDF(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def track_refPx(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def track_refPy(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def track_refPz(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def track_links(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_trackparticle_v1___.vector_ElementLink_DataVector_xAOD_TrackParticle_v1___:
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
