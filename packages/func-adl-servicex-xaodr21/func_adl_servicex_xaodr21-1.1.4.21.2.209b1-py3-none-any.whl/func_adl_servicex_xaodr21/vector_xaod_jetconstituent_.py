from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'size': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'vector<xAOD::JetConstituent>',
        'method_name': 'size',
        'return_type': 'int',
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
class vector_xAOD_JetConstituent_(Iterable[func_adl_servicex_xaodr21.xAOD.jetconstituent.JetConstituent]):
    "A class"

    def size(self) -> int:
        "A method"
        ...
