from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'DefaultMinimizerType': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultMinimizerType',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'DefaultMinimizerAlgo': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultMinimizerAlgo',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'DefaultErrorDef': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultErrorDef',
        'return_type': 'double',
    },
    'DefaultTolerance': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultTolerance',
        'return_type': 'double',
    },
    'DefaultPrecision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultPrecision',
        'return_type': 'double',
    },
    'DefaultMaxFunctionCalls': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultMaxFunctionCalls',
        'return_type': 'int',
    },
    'DefaultMaxIterations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultMaxIterations',
        'return_type': 'int',
    },
    'DefaultStrategy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultStrategy',
        'return_type': 'int',
    },
    'DefaultPrintLevel': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultPrintLevel',
        'return_type': 'int',
    },
    'DefaultExtraOptions': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'DefaultExtraOptions',
        'return_type': 'ROOT::Math::IOptions*',
    },
    'PrintLevel': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'PrintLevel',
        'return_type': 'int',
    },
    'MaxFunctionCalls': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'MaxFunctionCalls',
        'return_type': 'unsigned int',
    },
    'MaxIterations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'MaxIterations',
        'return_type': 'unsigned int',
    },
    'Strategy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'Strategy',
        'return_type': 'int',
    },
    'Tolerance': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'Tolerance',
        'return_type': 'double',
    },
    'Precision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'Precision',
        'return_type': 'double',
    },
    'ErrorDef': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'ErrorDef',
        'return_type': 'double',
    },
    'ExtraOptions': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'ExtraOptions',
        'return_type': 'const ROOT::Math::IOptions*',
    },
    'MinimizerType': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'MinimizerType',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'MinimizerAlgorithm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::MinimizerOptions',
        'method_name': 'MinimizerAlgorithm',
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
class MinimizerOptions:
    "A class"

    def DefaultMinimizerType(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def DefaultMinimizerAlgo(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def DefaultErrorDef(self) -> float:
        "A method"
        ...

    def DefaultTolerance(self) -> float:
        "A method"
        ...

    def DefaultPrecision(self) -> float:
        "A method"
        ...

    def DefaultMaxFunctionCalls(self) -> int:
        "A method"
        ...

    def DefaultMaxIterations(self) -> int:
        "A method"
        ...

    def DefaultStrategy(self) -> int:
        "A method"
        ...

    def DefaultPrintLevel(self) -> int:
        "A method"
        ...

    def DefaultExtraOptions(self) -> func_adl_servicex_xaodr21.ROOT.Math.ioptions.IOptions:
        "A method"
        ...

    def PrintLevel(self) -> int:
        "A method"
        ...

    def MaxFunctionCalls(self) -> int:
        "A method"
        ...

    def MaxIterations(self) -> int:
        "A method"
        ...

    def Strategy(self) -> int:
        "A method"
        ...

    def Tolerance(self) -> float:
        "A method"
        ...

    def Precision(self) -> float:
        "A method"
        ...

    def ErrorDef(self) -> float:
        "A method"
        ...

    def ExtraOptions(self) -> func_adl_servicex_xaodr21.ROOT.Math.ioptions.IOptions:
        "A method"
        ...

    def MinimizerType(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def MinimizerAlgorithm(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...
