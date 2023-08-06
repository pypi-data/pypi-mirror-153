from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'SetVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariable',
        'return_type': 'bool',
    },
    'SetLowerLimitedVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetLowerLimitedVariable',
        'return_type': 'bool',
    },
    'SetUpperLimitedVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetUpperLimitedVariable',
        'return_type': 'bool',
    },
    'SetLimitedVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetLimitedVariable',
        'return_type': 'bool',
    },
    'SetFixedVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetFixedVariable',
        'return_type': 'bool',
    },
    'SetVariableValue': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableValue',
        'return_type': 'bool',
    },
    'SetVariableValues': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableValues',
        'return_type': 'bool',
    },
    'SetVariableStepSize': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableStepSize',
        'return_type': 'bool',
    },
    'SetVariableLowerLimit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableLowerLimit',
        'return_type': 'bool',
    },
    'SetVariableUpperLimit': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableUpperLimit',
        'return_type': 'bool',
    },
    'SetVariableLimits': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableLimits',
        'return_type': 'bool',
    },
    'FixVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'FixVariable',
        'return_type': 'bool',
    },
    'ReleaseVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'ReleaseVariable',
        'return_type': 'bool',
    },
    'IsFixedVariable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'IsFixedVariable',
        'return_type': 'bool',
    },
    'GetVariableSettings': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'GetVariableSettings',
        'return_type': 'bool',
    },
    'SetVariableInitialRange': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'SetVariableInitialRange',
        'return_type': 'bool',
    },
    'Minimize': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Minimize',
        'return_type': 'bool',
    },
    'MinValue': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'MinValue',
        'return_type': 'double',
    },
    'X': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'X',
        'return_type': 'const double*',
    },
    'Edm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Edm',
        'return_type': 'double',
    },
    'MinGradient': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'MinGradient',
        'return_type': 'const double*',
    },
    'NCalls': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'NCalls',
        'return_type': 'unsigned int',
    },
    'NIterations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'NIterations',
        'return_type': 'unsigned int',
    },
    'NDim': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'NDim',
        'return_type': 'unsigned int',
    },
    'NFree': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'NFree',
        'return_type': 'unsigned int',
    },
    'ProvidesError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'ProvidesError',
        'return_type': 'bool',
    },
    'Errors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Errors',
        'return_type': 'const double*',
    },
    'CovMatrix': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'CovMatrix',
        'return_type': 'double',
    },
    'GetCovMatrix': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'GetCovMatrix',
        'return_type': 'bool',
    },
    'GetHessianMatrix': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'GetHessianMatrix',
        'return_type': 'bool',
    },
    'CovMatrixStatus': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'CovMatrixStatus',
        'return_type': 'int',
    },
    'Correlation': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Correlation',
        'return_type': 'double',
    },
    'GlobalCC': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'GlobalCC',
        'return_type': 'double',
    },
    'GetMinosError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'GetMinosError',
        'return_type': 'bool',
    },
    'Hesse': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Hesse',
        'return_type': 'bool',
    },
    'Scan': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Scan',
        'return_type': 'bool',
    },
    'Contour': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Contour',
        'return_type': 'bool',
    },
    'VariableName': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'VariableName',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
    },
    'VariableIndex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'VariableIndex',
        'return_type': 'int',
    },
    'PrintLevel': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'PrintLevel',
        'return_type': 'int',
    },
    'MaxFunctionCalls': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'MaxFunctionCalls',
        'return_type': 'unsigned int',
    },
    'MaxIterations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'MaxIterations',
        'return_type': 'unsigned int',
    },
    'Tolerance': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Tolerance',
        'return_type': 'double',
    },
    'Precision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Precision',
        'return_type': 'double',
    },
    'Strategy': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Strategy',
        'return_type': 'int',
    },
    'Status': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Status',
        'return_type': 'int',
    },
    'ErrorDef': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'ErrorDef',
        'return_type': 'double',
    },
    'IsValidError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'IsValidError',
        'return_type': 'bool',
    },
    'Options': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Math::Minimizer',
        'method_name': 'Options',
        'return_type': 'ROOT::Math::MinimizerOptions',
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
class Minimizer:
    "A class"

    def SetVariable(self, ivar: int, name: str, val: float, step: float) -> bool:
        "A method"
        ...

    def SetLowerLimitedVariable(self, ivar: int, name: str, val: float, step: float, lower: float) -> bool:
        "A method"
        ...

    def SetUpperLimitedVariable(self, ivar: int, name: str, val: float, step: float, upper: float) -> bool:
        "A method"
        ...

    def SetLimitedVariable(self, ivar: int, name: str, val: float, step: float, lower: float, upper: float) -> bool:
        "A method"
        ...

    def SetFixedVariable(self, ivar: int, name: str, val: float) -> bool:
        "A method"
        ...

    def SetVariableValue(self, ivar: int, value: float) -> bool:
        "A method"
        ...

    def SetVariableValues(self, x: float) -> bool:
        "A method"
        ...

    def SetVariableStepSize(self, ivar: int, value: float) -> bool:
        "A method"
        ...

    def SetVariableLowerLimit(self, ivar: int, lower: float) -> bool:
        "A method"
        ...

    def SetVariableUpperLimit(self, ivar: int, upper: float) -> bool:
        "A method"
        ...

    def SetVariableLimits(self, ivar: int, lower: float, upper: float) -> bool:
        "A method"
        ...

    def FixVariable(self, ivar: int) -> bool:
        "A method"
        ...

    def ReleaseVariable(self, ivar: int) -> bool:
        "A method"
        ...

    def IsFixedVariable(self, ivar: int) -> bool:
        "A method"
        ...

    def GetVariableSettings(self, ivar: int, pars: ParameterSettings) -> bool:
        "A method"
        ...

    def SetVariableInitialRange(self, noname_arg: int, noname_arg_1: float, noname_arg_2: float) -> bool:
        "A method"
        ...

    def Minimize(self) -> bool:
        "A method"
        ...

    def MinValue(self) -> float:
        "A method"
        ...

    def X(self) -> float:
        "A method"
        ...

    def Edm(self) -> float:
        "A method"
        ...

    def MinGradient(self) -> float:
        "A method"
        ...

    def NCalls(self) -> int:
        "A method"
        ...

    def NIterations(self) -> int:
        "A method"
        ...

    def NDim(self) -> int:
        "A method"
        ...

    def NFree(self) -> int:
        "A method"
        ...

    def ProvidesError(self) -> bool:
        "A method"
        ...

    def Errors(self) -> float:
        "A method"
        ...

    def CovMatrix(self, ivar: int, jvar: int) -> float:
        "A method"
        ...

    def GetCovMatrix(self, covMat: float) -> bool:
        "A method"
        ...

    def GetHessianMatrix(self, hMat: float) -> bool:
        "A method"
        ...

    def CovMatrixStatus(self) -> int:
        "A method"
        ...

    def Correlation(self, i: int, j: int) -> float:
        "A method"
        ...

    def GlobalCC(self, ivar: int) -> float:
        "A method"
        ...

    def GetMinosError(self, ivar: int, errLow: float, errUp: float, option: int) -> bool:
        "A method"
        ...

    def Hesse(self) -> bool:
        "A method"
        ...

    def Scan(self, ivar: int, nstep: int, x: float, y: float, xmin: float, xmax: float) -> bool:
        "A method"
        ...

    def Contour(self, ivar: int, jvar: int, npoints: int, xi: float, xj: float) -> bool:
        "A method"
        ...

    def VariableName(self, ivar: int) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def VariableIndex(self, name: str) -> int:
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

    def Tolerance(self) -> float:
        "A method"
        ...

    def Precision(self) -> float:
        "A method"
        ...

    def Strategy(self) -> int:
        "A method"
        ...

    def Status(self) -> int:
        "A method"
        ...

    def ErrorDef(self) -> float:
        "A method"
        ...

    def IsValidError(self) -> bool:
        "A method"
        ...

    def Options(self) -> func_adl_servicex_xaodr21.ROOT.Math.minimizeroptions.MinimizerOptions:
        "A method"
        ...
