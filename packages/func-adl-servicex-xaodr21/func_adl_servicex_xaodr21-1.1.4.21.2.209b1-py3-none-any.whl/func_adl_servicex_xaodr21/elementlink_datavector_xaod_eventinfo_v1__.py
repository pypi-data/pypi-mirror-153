from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'runNumber': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'runNumber',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'eventNumber': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'eventNumber',
        'return_type': 'unsigned long long',
        'deref_count': 2
    },
    'lumiBlock': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'lumiBlock',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'timeStamp': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'timeStamp',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'timeStampNSOffset': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'timeStampNSOffset',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'bcid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'bcid',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'detectorMask0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'detectorMask0',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'detectorMask1': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'detectorMask1',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'detectorMask2': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'detectorMask2',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'detectorMask3': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'detectorMask3',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'mcChannelNumber': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'mcChannelNumber',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'mcEventNumber': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'mcEventNumber',
        'return_type': 'unsigned long long',
        'deref_count': 2
    },
    'mcEventWeights': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'mcEventWeights',
        'return_type_element': 'float',
        'return_type_collection': 'const vector<float>',
        'deref_count': 2
    },
    'mcEventWeight': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'mcEventWeight',
        'return_type': 'float',
        'deref_count': 2
    },
    'hasMCEventWeights': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'hasMCEventWeights',
        'return_type': 'bool',
        'deref_count': 2
    },
    'eventTypeBitmask': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'eventTypeBitmask',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'statusElement': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'statusElement',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'extendedLevel1ID': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'extendedLevel1ID',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'streamTags': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'streamTags',
        'return_type_element': 'xAOD::EventInfo_v1::StreamTag',
        'return_type_collection': 'const vector<xAOD::EventInfo_v1::StreamTag>',
        'deref_count': 2
    },
    'actualInteractionsPerCrossing': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'actualInteractionsPerCrossing',
        'return_type': 'float',
        'deref_count': 2
    },
    'averageInteractionsPerCrossing': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'averageInteractionsPerCrossing',
        'return_type': 'float',
        'deref_count': 2
    },
    'subEvents': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'subEvents',
        'return_type_element': 'xAOD::EventInfo_v1::SubEvent',
        'return_type_collection': 'const vector<xAOD::EventInfo_v1::SubEvent>',
        'deref_count': 2
    },
    'beamPosX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosX',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamPosY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosY',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamPosZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosZ',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamPosSigmaX': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosSigmaX',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamPosSigmaY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosSigmaY',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamPosSigmaZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosSigmaZ',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamPosSigmaXY': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamPosSigmaXY',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamTiltXZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamTiltXZ',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamTiltYZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamTiltYZ',
        'return_type': 'float',
        'deref_count': 2
    },
    'beamStatus': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'beamStatus',
        'return_type': 'unsigned int',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::EventInfo_v1>>',
        'method_name': 'isAvailable',
        'return_type': 'bool',
        'deref_count': 2
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
class ElementLink_DataVector_xAOD_EventInfo_v1__:
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def runNumber(self) -> int:
        "A method"
        ...

    def eventNumber(self) -> int:
        "A method"
        ...

    def lumiBlock(self) -> int:
        "A method"
        ...

    def timeStamp(self) -> int:
        "A method"
        ...

    def timeStampNSOffset(self) -> int:
        "A method"
        ...

    def bcid(self) -> int:
        "A method"
        ...

    def detectorMask0(self) -> int:
        "A method"
        ...

    def detectorMask1(self) -> int:
        "A method"
        ...

    def detectorMask2(self) -> int:
        "A method"
        ...

    def detectorMask3(self) -> int:
        "A method"
        ...

    def mcChannelNumber(self) -> int:
        "A method"
        ...

    def mcEventNumber(self) -> int:
        "A method"
        ...

    def mcEventWeights(self) -> func_adl_servicex_xaodr21.vector_float_.vector_float_:
        "A method"
        ...

    def mcEventWeight(self, i: int) -> float:
        "A method"
        ...

    def hasMCEventWeights(self) -> bool:
        "A method"
        ...

    def eventTypeBitmask(self) -> int:
        "A method"
        ...

    def statusElement(self) -> int:
        "A method"
        ...

    def extendedLevel1ID(self) -> int:
        "A method"
        ...

    def streamTags(self) -> func_adl_servicex_xaodr21.vector_xaod_eventinfo_v1_streamtag_.vector_xAOD_EventInfo_v1_StreamTag_:
        "A method"
        ...

    def actualInteractionsPerCrossing(self) -> float:
        "A method"
        ...

    def averageInteractionsPerCrossing(self) -> float:
        "A method"
        ...

    def subEvents(self) -> func_adl_servicex_xaodr21.vector_xaod_eventinfo_v1_subevent_.vector_xAOD_EventInfo_v1_SubEvent_:
        "A method"
        ...

    def beamPosX(self) -> float:
        "A method"
        ...

    def beamPosY(self) -> float:
        "A method"
        ...

    def beamPosZ(self) -> float:
        "A method"
        ...

    def beamPosSigmaX(self) -> float:
        "A method"
        ...

    def beamPosSigmaY(self) -> float:
        "A method"
        ...

    def beamPosSigmaZ(self) -> float:
        "A method"
        ...

    def beamPosSigmaXY(self) -> float:
        "A method"
        ...

    def beamTiltXZ(self) -> float:
        "A method"
        ...

    def beamTiltYZ(self) -> float:
        "A method"
        ...

    def beamStatus(self) -> int:
        "A method"
        ...

    def index(self) -> int:
        "A method"
        ...

    def usingPrivateStore(self) -> bool:
        "A method"
        ...

    def usingStandaloneStore(self) -> bool:
        "A method"
        ...

    def hasStore(self) -> bool:
        "A method"
        ...

    def hasNonConstStore(self) -> bool:
        "A method"
        ...

    def clearDecorations(self) -> bool:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr21.type_support.cpp_generic_1arg_callback('auxdataConst', s, a, param_1))
    @property
    def auxdataConst(self) -> func_adl_servicex_xaodr21.type_support.index_type_forwarder[str]:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr21.type_support.cpp_generic_1arg_callback('isAvailable', s, a, param_1))
    @property
    def isAvailable(self) -> func_adl_servicex_xaodr21.type_support.index_type_forwarder[str]:
        "A method"
        ...
