from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'ParSettings': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'ParSettings',
        'return_type': 'const ROOT::Fit::ParameterSettings',
    },
    'ParamsSettings': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'ParamsSettings',
        'return_type_element': 'ROOT::Fit::ParameterSettings',
        'return_type_collection': 'const vector<ROOT::Fit::ParameterSettings>',
    },
    'NPar': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'NPar',
        'return_type': 'unsigned int',
    },
    'ParamsValues': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'ParamsValues',
        'return_type_element': 'float',
        'return_type_collection': 'vector<double>',
    },
    'CreateMinimizer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'CreateMinimizer',
        'return_type': 'ROOT::Math::Minimizer*',
    },
    'MinimizerOptions': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'MinimizerOptions',
        'return_type': 'ROOT::Math::MinimizerOptions',
    },
    'MinimizerType': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'MinimizerType',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'MinimizerAlgoType': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'MinimizerAlgoType',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'MinimizerName': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'MinimizerName',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
    },
    'NormalizeErrors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'NormalizeErrors',
        'return_type': 'bool',
    },
    'ParabErrors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'ParabErrors',
        'return_type': 'bool',
    },
    'MinosErrors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'MinosErrors',
        'return_type': 'bool',
    },
    'UpdateAfterFit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'UpdateAfterFit',
        'return_type': 'bool',
    },
    'UseWeightCorrection': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitConfig',
        'method_name': 'UseWeightCorrection',
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
class FitConfig:
    "A class"

    def ParSettings(self, i: int) -> func_adl_servicex_xaodr21.ROOT.Fit.parametersettings.ParameterSettings:
        "A method"
        ...

    def ParamsSettings(self) -> func_adl_servicex_xaodr21.vector_root_fit_parametersettings_.vector_ROOT_Fit_ParameterSettings_:
        "A method"
        ...

    def NPar(self) -> int:
        "A method"
        ...

    def ParamsValues(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def CreateMinimizer(self) -> func_adl_servicex_xaodr21.ROOT.Math.minimizer.Minimizer:
        "A method"
        ...

    def MinimizerOptions(self) -> func_adl_servicex_xaodr21.ROOT.Math.minimizeroptions.MinimizerOptions:
        "A method"
        ...

    def MinimizerType(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def MinimizerAlgoType(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def MinimizerName(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def NormalizeErrors(self) -> bool:
        "A method"
        ...

    def ParabErrors(self) -> bool:
        "A method"
        ...

    def MinosErrors(self) -> bool:
        "A method"
        ...

    def UpdateAfterFit(self) -> bool:
        "A method"
        ...

    def UseWeightCorrection(self) -> bool:
        "A method"
        ...
