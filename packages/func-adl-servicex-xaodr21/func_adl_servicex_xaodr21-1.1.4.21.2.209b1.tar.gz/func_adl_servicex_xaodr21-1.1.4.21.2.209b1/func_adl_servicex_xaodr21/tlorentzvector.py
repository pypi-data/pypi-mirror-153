from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'Vect': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'Vect',
        'return_type': 'TVector3',
    },
    'EtaPhiVector': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'EtaPhiVector',
        'return_type': 'TVector2',
    },
    'BoostVector': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'BoostVector',
        'return_type': 'TVector3',
    },
    'Transform': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'Transform',
        'return_type': 'TLorentzVector',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TLorentzVector',
        'method_name': 'DistancetoPrimitive',
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
class TLorentzVector:
    "A class"

    def Vect(self) -> func_adl_servicex_xaodr21.tvector3.TVector3:
        "A method"
        ...

    def EtaPhiVector(self) -> func_adl_servicex_xaodr21.tvector2.TVector2:
        "A method"
        ...

    def BoostVector(self) -> func_adl_servicex_xaodr21.tvector3.TVector3:
        "A method"
        ...

    def Transform(self, noname_arg: TRotation) -> func_adl_servicex_xaodr21.tlorentzvector.TLorentzVector:
        "A method"
        ...

    def ImplFileLine(self) -> int:
        "A method"
        ...

    def DeclFileLine(self) -> int:
        "A method"
        ...

    def DistancetoPrimitive(self, px: int, py: int) -> int:
        "A method"
        ...
