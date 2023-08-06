from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'Value': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'Value',
        'return_type': 'double',
    },
    'StepSize': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'StepSize',
        'return_type': 'double',
    },
    'LowerLimit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'LowerLimit',
        'return_type': 'double',
    },
    'UpperLimit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'UpperLimit',
        'return_type': 'double',
    },
    'IsFixed': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'IsFixed',
        'return_type': 'bool',
    },
    'HasLowerLimit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'HasLowerLimit',
        'return_type': 'bool',
    },
    'HasUpperLimit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'HasUpperLimit',
        'return_type': 'bool',
    },
    'IsBound': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'IsBound',
        'return_type': 'bool',
    },
    'IsDoubleBound': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'IsDoubleBound',
        'return_type': 'bool',
    },
    'Name': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::ParameterSettings',
        'method_name': 'Name',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
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
class ParameterSettings:
    "A class"

    def Value(self) -> float:
        "A method"
        ...

    def StepSize(self) -> float:
        "A method"
        ...

    def LowerLimit(self) -> float:
        "A method"
        ...

    def UpperLimit(self) -> float:
        "A method"
        ...

    def IsFixed(self) -> bool:
        "A method"
        ...

    def HasLowerLimit(self) -> bool:
        "A method"
        ...

    def HasUpperLimit(self) -> bool:
        "A method"
        ...

    def IsBound(self) -> bool:
        "A method"
        ...

    def IsDoubleBound(self) -> bool:
        "A method"
        ...

    def Name(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...
