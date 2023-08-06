from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'Kill': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'Kill',
        'return_type': 'int',
    },
    'Exists': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'Exists',
        'return_type': 'int',
    },
    'Lock': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'Lock',
        'return_type': 'int',
    },
    'TryLock': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'TryLock',
        'return_type': 'int',
    },
    'UnLock': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'UnLock',
        'return_type': 'int',
    },
    'Self': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'Self',
        'return_type': 'TThread*',
    },
    'SetCancelOn': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'SetCancelOn',
        'return_type': 'int',
    },
    'SetCancelOff': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'SetCancelOff',
        'return_type': 'int',
    },
    'SetCancelAsynchronous': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'SetCancelAsynchronous',
        'return_type': 'int',
    },
    'SetCancelDeferred': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'SetCancelDeferred',
        'return_type': 'int',
    },
    'CancelPoint': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'CancelPoint',
        'return_type': 'int',
    },
    'CleanUpPop': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'CleanUpPop',
        'return_type': 'int',
    },
    'CleanUp': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'CleanUp',
        'return_type': 'int',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'Sizeof': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
        'method_name': 'Sizeof',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'TThread',
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
class TThread:
    "A class"

    def Kill(self) -> int:
        "A method"
        ...

    def Exists(self) -> int:
        "A method"
        ...

    def Lock(self) -> int:
        "A method"
        ...

    def TryLock(self) -> int:
        "A method"
        ...

    def UnLock(self) -> int:
        "A method"
        ...

    def Self(self) -> func_adl_servicex_xaodr21.tthread.TThread:
        "A method"
        ...

    def SetCancelOn(self) -> int:
        "A method"
        ...

    def SetCancelOff(self) -> int:
        "A method"
        ...

    def SetCancelAsynchronous(self) -> int:
        "A method"
        ...

    def SetCancelDeferred(self) -> int:
        "A method"
        ...

    def CancelPoint(self) -> int:
        "A method"
        ...

    def CleanUpPop(self, exe: int) -> int:
        "A method"
        ...

    def CleanUp(self) -> int:
        "A method"
        ...

    def ImplFileLine(self) -> int:
        "A method"
        ...

    def DeclFileLine(self) -> int:
        "A method"
        ...

    def Sizeof(self) -> int:
        "A method"
        ...

    def DistancetoPrimitive(self, px: int, py: int) -> int:
        "A method"
        ...
