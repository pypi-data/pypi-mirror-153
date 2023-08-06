from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'isValid': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isValid',
        'return_type': 'bool',
    },
    'pdgId': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'pdgId',
        'return_type': 'int',
        'deref_count': 2
    },
    'absPdgId': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'absPdgId',
        'return_type': 'int',
        'deref_count': 2
    },
    'barcode': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'barcode',
        'return_type': 'int',
        'deref_count': 2
    },
    'status': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'status',
        'return_type': 'int',
        'deref_count': 2
    },
    'hasProdVtx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasProdVtx',
        'return_type': 'bool',
        'deref_count': 2
    },
    'prodVtx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'prodVtx',
        'return_type': 'const xAOD::TruthVertex_v1*',
        'deref_count': 2
    },
    'prodVtxLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'prodVtxLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'deref_count': 2
    },
    'hasDecayVtx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasDecayVtx',
        'return_type': 'bool',
        'deref_count': 2
    },
    'decayVtx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'decayVtx',
        'return_type': 'const xAOD::TruthVertex_v1*',
        'deref_count': 2
    },
    'decayVtxLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'decayVtxLink',
        'return_type': 'const ElementLink<DataVector<xAOD::TruthVertex_v1>>',
        'deref_count': 2
    },
    'nParents': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'nParents',
        'return_type': 'int',
        'deref_count': 2
    },
    'parent': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'parent',
        'return_type': 'const xAOD::TruthParticle_v1*',
        'deref_count': 2
    },
    'nChildren': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'nChildren',
        'return_type': 'int',
        'deref_count': 2
    },
    'child': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'child',
        'return_type': 'const xAOD::TruthParticle_v1*',
        'deref_count': 2
    },
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'pt',
        'return_type': 'double',
        'deref_count': 2
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'eta',
        'return_type': 'double',
        'deref_count': 2
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'phi',
        'return_type': 'double',
        'deref_count': 2
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'm',
        'return_type': 'double',
        'deref_count': 2
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'e',
        'return_type': 'double',
        'deref_count': 2
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'rapidity',
        'return_type': 'double',
        'deref_count': 2
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
        'deref_count': 2
    },
    'abseta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'abseta',
        'return_type': 'double',
        'deref_count': 2
    },
    'absrapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'absrapidity',
        'return_type': 'double',
        'deref_count': 2
    },
    'px': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'px',
        'return_type': 'float',
        'deref_count': 2
    },
    'py': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'py',
        'return_type': 'float',
        'deref_count': 2
    },
    'pz': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'pz',
        'return_type': 'float',
        'deref_count': 2
    },
    'charge': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'charge',
        'return_type': 'double',
        'deref_count': 2
    },
    'threeCharge': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'threeCharge',
        'return_type': 'int',
        'deref_count': 2
    },
    'isCharged': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isCharged',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isNeutral': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isNeutral',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isPhoton': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isPhoton',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isLepton': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isLepton',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isChLepton': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isChLepton',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isElectron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isElectron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isMuon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isMuon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isTau': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isTau',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isNeutrino': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isNeutrino',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isHadron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isHadron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isMeson': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isMeson',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isBaryon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isBaryon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStrange': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasStrange',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasCharm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasCharm',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasBottom': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasBottom',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isLightMeson': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isLightMeson',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isLightBaryon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isLightBaryon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isLightHadron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isLightHadron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isHeavyMeson': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isHeavyMeson',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isHeavyBaryon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isHeavyBaryon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isHeavyHadron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isHeavyHadron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isBottomMeson': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isBottomMeson',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isBottomBaryon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isBottomBaryon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isBottomHadron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isBottomHadron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isCharmMeson': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isCharmMeson',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isCharmBaryon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isCharmBaryon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isCharmHadron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isCharmHadron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isStrangeMeson': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isStrangeMeson',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isStrangeBaryon': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isStrangeBaryon',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isStrangeHadron': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isStrangeHadron',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isQuark': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isQuark',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isParton': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isParton',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isTop': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isTop',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isW': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isW',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isZ': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isZ',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isHiggs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isHiggs',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isResonance': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isResonance',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isGenSpecific': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isGenSpecific',
        'return_type': 'bool',
        'deref_count': 2
    },
    'isBSM': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'isBSM',
        'return_type': 'bool',
        'deref_count': 2
    },
    'polarization': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'polarization',
        'return_type': 'xAOD::TruthParticle_v1::Polarization',
        'deref_count': 2
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'index',
        'return_type': 'int',
        'deref_count': 2
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
        'deref_count': 2
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
        'deref_count': 2
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
        'method_name': 'auxdataConst',
        'return_type': 'U',
        'deref_count': 2
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ElementLink<DataVector<xAOD::TruthParticle_v1>>',
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
class ElementLink_DataVector_xAOD_TruthParticle_v1__:
    "A class"

    def isValid(self) -> bool:
        "A method"
        ...

    def pdgId(self) -> int:
        "A method"
        ...

    def absPdgId(self) -> int:
        "A method"
        ...

    def barcode(self) -> int:
        "A method"
        ...

    def status(self) -> int:
        "A method"
        ...

    def hasProdVtx(self) -> bool:
        "A method"
        ...

    def prodVtx(self) -> func_adl_servicex_xaodr21.xAOD.truthvertex_v1.TruthVertex_v1:
        "A method"
        ...

    def prodVtxLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_truthvertex_v1__.ElementLink_DataVector_xAOD_TruthVertex_v1__:
        "A method"
        ...

    def hasDecayVtx(self) -> bool:
        "A method"
        ...

    def decayVtx(self) -> func_adl_servicex_xaodr21.xAOD.truthvertex_v1.TruthVertex_v1:
        "A method"
        ...

    def decayVtxLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_truthvertex_v1__.ElementLink_DataVector_xAOD_TruthVertex_v1__:
        "A method"
        ...

    def nParents(self) -> int:
        "A method"
        ...

    def parent(self, i: int) -> func_adl_servicex_xaodr21.xAOD.truthparticle_v1.TruthParticle_v1:
        "A method"
        ...

    def nChildren(self) -> int:
        "A method"
        ...

    def child(self, i: int) -> func_adl_servicex_xaodr21.xAOD.truthparticle_v1.TruthParticle_v1:
        "A method"
        ...

    def pt(self) -> float:
        "A method"
        ...

    def eta(self) -> float:
        "A method"
        ...

    def phi(self) -> float:
        "A method"
        ...

    def m(self) -> float:
        "A method"
        ...

    def e(self) -> float:
        "A method"
        ...

    def rapidity(self) -> float:
        "A method"
        ...

    def p4(self) -> func_adl_servicex_xaodr21.tlorentzvector.TLorentzVector:
        "A method"
        ...

    def abseta(self) -> float:
        "A method"
        ...

    def absrapidity(self) -> float:
        "A method"
        ...

    def px(self) -> float:
        "A method"
        ...

    def py(self) -> float:
        "A method"
        ...

    def pz(self) -> float:
        "A method"
        ...

    def charge(self) -> float:
        "A method"
        ...

    def threeCharge(self) -> int:
        "A method"
        ...

    def isCharged(self) -> bool:
        "A method"
        ...

    def isNeutral(self) -> bool:
        "A method"
        ...

    def isPhoton(self) -> bool:
        "A method"
        ...

    def isLepton(self) -> bool:
        "A method"
        ...

    def isChLepton(self) -> bool:
        "A method"
        ...

    def isElectron(self) -> bool:
        "A method"
        ...

    def isMuon(self) -> bool:
        "A method"
        ...

    def isTau(self) -> bool:
        "A method"
        ...

    def isNeutrino(self) -> bool:
        "A method"
        ...

    def isHadron(self) -> bool:
        "A method"
        ...

    def isMeson(self) -> bool:
        "A method"
        ...

    def isBaryon(self) -> bool:
        "A method"
        ...

    def hasStrange(self) -> bool:
        "A method"
        ...

    def hasCharm(self) -> bool:
        "A method"
        ...

    def hasBottom(self) -> bool:
        "A method"
        ...

    def isLightMeson(self) -> bool:
        "A method"
        ...

    def isLightBaryon(self) -> bool:
        "A method"
        ...

    def isLightHadron(self) -> bool:
        "A method"
        ...

    def isHeavyMeson(self) -> bool:
        "A method"
        ...

    def isHeavyBaryon(self) -> bool:
        "A method"
        ...

    def isHeavyHadron(self) -> bool:
        "A method"
        ...

    def isBottomMeson(self) -> bool:
        "A method"
        ...

    def isBottomBaryon(self) -> bool:
        "A method"
        ...

    def isBottomHadron(self) -> bool:
        "A method"
        ...

    def isCharmMeson(self) -> bool:
        "A method"
        ...

    def isCharmBaryon(self) -> bool:
        "A method"
        ...

    def isCharmHadron(self) -> bool:
        "A method"
        ...

    def isStrangeMeson(self) -> bool:
        "A method"
        ...

    def isStrangeBaryon(self) -> bool:
        "A method"
        ...

    def isStrangeHadron(self) -> bool:
        "A method"
        ...

    def isQuark(self) -> bool:
        "A method"
        ...

    def isParton(self) -> bool:
        "A method"
        ...

    def isTop(self) -> bool:
        "A method"
        ...

    def isW(self) -> bool:
        "A method"
        ...

    def isZ(self) -> bool:
        "A method"
        ...

    def isHiggs(self) -> bool:
        "A method"
        ...

    def isResonance(self) -> bool:
        "A method"
        ...

    def isGenSpecific(self) -> bool:
        "A method"
        ...

    def isBSM(self) -> bool:
        "A method"
        ...

    def polarization(self) -> func_adl_servicex_xaodr21.xAOD.TruthParticle_v1.polarization.Polarization:
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
