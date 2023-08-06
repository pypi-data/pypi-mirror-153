from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'm',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'e',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'rawConstituent': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'rawConstituent',
        'return_type': 'const xAOD::IParticle*',
    },
    'isTimelike': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'isTimelike',
        'return_type': 'bool',
    },
    'isSpacelike': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::JetConstituent',
        'method_name': 'isSpacelike',
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
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class JetConstituent:
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

    def rawConstituent(self) -> func_adl_servicex_xaodr21.xAOD.iparticle.IParticle:
        "A method"
        ...

    def isTimelike(self) -> bool:
        "A method"
        ...

    def isSpacelike(self) -> bool:
        "A method"
        ...
