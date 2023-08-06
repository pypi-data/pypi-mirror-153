from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'MinimizerType': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'MinimizerType',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'IsValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'IsValid',
        'return_type': 'bool',
    },
    'IsEmpty': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'IsEmpty',
        'return_type': 'bool',
    },
    'MinFcnValue': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'MinFcnValue',
        'return_type': 'double',
    },
    'NCalls': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'NCalls',
        'return_type': 'unsigned int',
    },
    'Edm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Edm',
        'return_type': 'double',
    },
    'NTotalParameters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'NTotalParameters',
        'return_type': 'unsigned int',
    },
    'NPar': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'NPar',
        'return_type': 'unsigned int',
    },
    'NFreeParameters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'NFreeParameters',
        'return_type': 'unsigned int',
    },
    'Status': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Status',
        'return_type': 'int',
    },
    'CovMatrixStatus': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'CovMatrixStatus',
        'return_type': 'int',
    },
    'FittedBinData': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'FittedBinData',
        'return_type': 'const ROOT::Fit::BinData*',
    },
    'Chi2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Chi2',
        'return_type': 'double',
    },
    'Ndf': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Ndf',
        'return_type': 'unsigned int',
    },
    'Prob': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Prob',
        'return_type': 'double',
    },
    'Errors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Errors',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<double>',
    },
    'GetErrors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'GetErrors',
        'return_type': 'const double*',
    },
    'Parameters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Parameters',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<double>',
    },
    'GetParams': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'GetParams',
        'return_type': 'const double*',
    },
    'Value': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Value',
        'return_type': 'double',
    },
    'Parameter': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Parameter',
        'return_type': 'double',
    },
    'Error': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Error',
        'return_type': 'double',
    },
    'ParError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'ParError',
        'return_type': 'double',
    },
    'ParName': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'ParName',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
    },
    'HasMinosError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'HasMinosError',
        'return_type': 'bool',
    },
    'LowerError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'LowerError',
        'return_type': 'double',
    },
    'UpperError': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'UpperError',
        'return_type': 'double',
    },
    'GlobalCC': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'GlobalCC',
        'return_type': 'double',
    },
    'CovMatrix': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'CovMatrix',
        'return_type': 'double',
    },
    'Correlation': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Correlation',
        'return_type': 'double',
    },
    'Scan': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Scan',
        'return_type': 'bool',
    },
    'Contour': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Contour',
        'return_type': 'bool',
    },
    'Index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'Index',
        'return_type': 'int',
    },
    'NormalizedErrors': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'NormalizedErrors',
        'return_type': 'bool',
    },
    'IsParameterBound': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'IsParameterBound',
        'return_type': 'bool',
    },
    'IsParameterFixed': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'IsParameterFixed',
        'return_type': 'bool',
    },
    'ParameterBounds': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'ParameterBounds',
        'return_type': 'bool',
    },
    'GetParameterName': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::FitResult',
        'method_name': 'GetParameterName',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
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
class FitResult:
    "A class"

    def MinimizerType(self) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def IsValid(self) -> bool:
        "A method"
        ...

    def IsEmpty(self) -> bool:
        "A method"
        ...

    def MinFcnValue(self) -> float:
        "A method"
        ...

    def NCalls(self) -> int:
        "A method"
        ...

    def Edm(self) -> float:
        "A method"
        ...

    def NTotalParameters(self) -> int:
        "A method"
        ...

    def NPar(self) -> int:
        "A method"
        ...

    def NFreeParameters(self) -> int:
        "A method"
        ...

    def Status(self) -> int:
        "A method"
        ...

    def CovMatrixStatus(self) -> int:
        "A method"
        ...

    def FittedBinData(self) -> func_adl_servicex_xaodr21.ROOT.Fit.bindata.BinData:
        "A method"
        ...

    def Chi2(self) -> float:
        "A method"
        ...

    def Ndf(self) -> int:
        "A method"
        ...

    def Prob(self) -> float:
        "A method"
        ...

    def Errors(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def GetErrors(self) -> float:
        "A method"
        ...

    def Parameters(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def GetParams(self) -> float:
        "A method"
        ...

    def Value(self, i: int) -> float:
        "A method"
        ...

    def Parameter(self, i: int) -> float:
        "A method"
        ...

    def Error(self, i: int) -> float:
        "A method"
        ...

    def ParError(self, i: int) -> float:
        "A method"
        ...

    def ParName(self, i: int) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def HasMinosError(self, i: int) -> bool:
        "A method"
        ...

    def LowerError(self, i: int) -> float:
        "A method"
        ...

    def UpperError(self, i: int) -> float:
        "A method"
        ...

    def GlobalCC(self, i: int) -> float:
        "A method"
        ...

    def CovMatrix(self, i: int, j: int) -> float:
        "A method"
        ...

    def Correlation(self, i: int, j: int) -> float:
        "A method"
        ...

    def Scan(self, ipar: int, npoints: int, pntsx: float, pntsy: float, xmin: float, xmax: float) -> bool:
        "A method"
        ...

    def Contour(self, ipar: int, jpar: int, npoints: int, pntsx: float, pntsy: float, confLevel: float) -> bool:
        "A method"
        ...

    def Index(self, name: str) -> int:
        "A method"
        ...

    def NormalizedErrors(self) -> bool:
        "A method"
        ...

    def IsParameterBound(self, ipar: int) -> bool:
        "A method"
        ...

    def IsParameterFixed(self, ipar: int) -> bool:
        "A method"
        ...

    def ParameterBounds(self, ipar: int, lower: float, upper: float) -> bool:
        "A method"
        ...

    def GetParameterName(self, ipar: int) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...
