from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'I': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'I',
        'return_type': 'TComplex',
    },
    'One': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'One',
        'return_type': 'TComplex',
    },
    'Sqrt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Sqrt',
        'return_type': 'TComplex',
    },
    'Exp': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Exp',
        'return_type': 'TComplex',
    },
    'Log': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Log',
        'return_type': 'TComplex',
    },
    'Log2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Log2',
        'return_type': 'TComplex',
    },
    'Log10': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Log10',
        'return_type': 'TComplex',
    },
    'Sin': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Sin',
        'return_type': 'TComplex',
    },
    'Cos': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Cos',
        'return_type': 'TComplex',
    },
    'Tan': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Tan',
        'return_type': 'TComplex',
    },
    'ASin': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ASin',
        'return_type': 'TComplex',
    },
    'ACos': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ACos',
        'return_type': 'TComplex',
    },
    'ATan': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ATan',
        'return_type': 'TComplex',
    },
    'SinH': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'SinH',
        'return_type': 'TComplex',
    },
    'CosH': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'CosH',
        'return_type': 'TComplex',
    },
    'TanH': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'TanH',
        'return_type': 'TComplex',
    },
    'ASinH': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ASinH',
        'return_type': 'TComplex',
    },
    'ACosH': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ACosH',
        'return_type': 'TComplex',
    },
    'ATanH': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ATanH',
        'return_type': 'TComplex',
    },
    'Power': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Power',
        'return_type': 'TComplex',
    },
    'Finite': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Finite',
        'return_type': 'int',
    },
    'IsNaN': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'IsNaN',
        'return_type': 'int',
    },
    'Min': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Min',
        'return_type': 'TComplex',
    },
    'Max': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Max',
        'return_type': 'TComplex',
    },
    'Normalize': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Normalize',
        'return_type': 'TComplex',
    },
    'Conjugate': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Conjugate',
        'return_type': 'TComplex',
    },
    'Range': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'Range',
        'return_type': 'TComplex',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TComplex',
        'method_name': 'DeclFileLine',
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
class TComplex:
    "A class"

    def I(self) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def One(self) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Sqrt(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Exp(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Log(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Log2(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Log10(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Sin(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Cos(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Tan(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ASin(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ACos(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ATan(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def SinH(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def CosH(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def TanH(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ASinH(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ACosH(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ATanH(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Power(self, x: TComplex, y: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Finite(self, c: TComplex) -> int:
        "A method"
        ...

    def IsNaN(self, c: TComplex) -> int:
        "A method"
        ...

    def Min(self, a: TComplex, b: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Max(self, a: TComplex, b: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Normalize(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Conjugate(self, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def Range(self, lb: TComplex, ub: TComplex, c: TComplex) -> func_adl_servicex_xaodr21.tcomplex.TComplex:
        "A method"
        ...

    def ImplFileLine(self) -> int:
        "A method"
        ...

    def DeclFileLine(self) -> int:
        "A method"
        ...
