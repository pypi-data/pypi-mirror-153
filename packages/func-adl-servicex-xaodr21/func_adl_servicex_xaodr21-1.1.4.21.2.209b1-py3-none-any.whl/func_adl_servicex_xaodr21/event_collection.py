from __future__ import annotations
from typing import Any, Dict, Iterable, List, Tuple, TypeVar, Union, Optional
from func_adl import ObjectStream, func_adl_callback
import ast
import copy
import func_adl_servicex_xaodr21

# The map for collection definitions in ATLAS
_collection_map = {
    'SlowMuons': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'SlowMuons',
        'include_files': ['xAODMuon/SlowMuonContainer.h',],
        'container_type': 'DataVector<xAOD::SlowMuon_v1>',
        'element_type': 'xAOD::SlowMuon_v1',
        'contains_collection': True,
        'link_libraries': ['xAODMuon'],
    },
    'MuonSegments': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'MuonSegments',
        'include_files': ['xAODMuon/MuonSegmentContainer.h',],
        'container_type': 'DataVector<xAOD::MuonSegment_v1>',
        'element_type': 'xAOD::MuonSegment_v1',
        'contains_collection': True,
        'link_libraries': ['xAODMuon'],
    },
    'Muons': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'Muons',
        'include_files': ['xAODMuon/MuonContainer.h',],
        'container_type': 'DataVector<xAOD::Muon_v1>',
        'element_type': 'xAOD::Muon_v1',
        'contains_collection': True,
        'link_libraries': ['xAODMuon'],
    },
    'TauJets': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TauJets',
        'include_files': ['xAODTau/TauJetContainer.h',],
        'container_type': 'DataVector<xAOD::TauJet_v3>',
        'element_type': 'xAOD::TauJet_v3',
        'contains_collection': True,
        'link_libraries': ['xAODTau'],
    },
    'TauTracks': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TauTracks',
        'include_files': ['xAODTau/TauTrackContainer.h',],
        'container_type': 'DataVector<xAOD::TauTrack_v1>',
        'element_type': 'xAOD::TauTrack_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTau'],
    },
    'DiTauJets': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'DiTauJets',
        'include_files': ['xAODTau/DiTauJetContainer.h',],
        'container_type': 'DataVector<xAOD::DiTauJet_v1>',
        'element_type': 'xAOD::DiTauJet_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTau'],
    },
    'CaloClusters': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'CaloClusters',
        'include_files': ['xAODCaloEvent/CaloClusterContainer.h',],
        'container_type': 'DataVector<xAOD::CaloCluster_v1>',
        'element_type': 'xAOD::CaloCluster_v1',
        'contains_collection': True,
        'link_libraries': ['xAODCaloEvent'],
    },
    'CaloTowers': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'CaloTowers',
        'include_files': ['xAODCaloEvent/CaloTowerContainer.h',],
        'container_type': 'xAOD::CaloTowerContainer_v1',
        'element_type': 'xAOD::CaloTower_v1',
        'contains_collection': True,
        'link_libraries': ['xAODCaloEvent'],
    },
    'TrackCaloClusters': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TrackCaloClusters',
        'include_files': ['xAODPFlow/TrackCaloClusterContainer.h',],
        'container_type': 'DataVector<xAOD::TrackCaloCluster_v1>',
        'element_type': 'xAOD::TrackCaloCluster_v1',
        'contains_collection': True,
        'link_libraries': ['xAODPFlow'],
    },
    'PFOs': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'PFOs',
        'include_files': ['xAODPFlow/PFOContainer.h',],
        'container_type': 'DataVector<xAOD::PFO_v1>',
        'element_type': 'xAOD::PFO_v1',
        'contains_collection': True,
        'link_libraries': ['xAODPFlow'],
    },
    'TruthMetaDatas': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TruthMetaDatas',
        'include_files': ['xAODTruth/TruthMetaDataContainer.h',],
        'container_type': 'DataVector<xAOD::TruthMetaData_v1>',
        'element_type': 'xAOD::TruthMetaData_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTruth'],
    },
    'TruthParticles': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TruthParticles',
        'include_files': ['xAODTruth/TruthParticleContainer.h',],
        'container_type': 'DataVector<xAOD::TruthParticle_v1>',
        'element_type': 'xAOD::TruthParticle_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTruth'],
    },
    'TruthVertices': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TruthVertices',
        'include_files': ['xAODTruth/TruthVertexContainer.h',],
        'container_type': 'DataVector<xAOD::TruthVertex_v1>',
        'element_type': 'xAOD::TruthVertex_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTruth'],
    },
    'TruthEvents': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TruthEvents',
        'include_files': ['xAODTruth/TruthEventContainer.h',],
        'container_type': 'DataVector<xAOD::TruthEvent_v1>',
        'element_type': 'xAOD::TruthEvent_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTruth'],
    },
    'BTagVertices': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'BTagVertices',
        'include_files': ['xAODBTagging/BTagVertexContainer.h',],
        'container_type': 'DataVector<xAOD::BTagVertex_v1>',
        'element_type': 'xAOD::BTagVertex_v1',
        'contains_collection': True,
        'link_libraries': ['xAODBTagging'],
    },
    'BTaggings': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'BTaggings',
        'include_files': ['xAODBTagging/BTaggingContainer.h',],
        'container_type': 'DataVector<xAOD::BTagging_v1>',
        'element_type': 'xAOD::BTagging_v1',
        'contains_collection': True,
        'link_libraries': ['xAODBTagging'],
    },
    'MissingET': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'MissingET',
        'include_files': ['xAODMissingET/MissingETContainer.h',],
        'container_type': 'xAOD::MissingETContainer_v1',
        'element_type': 'xAOD::MissingET_v1',
        'contains_collection': True,
        'link_libraries': ['xAODMissingET'],
    },
    'Jets': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'Jets',
        'include_files': ['xAODJet/JetContainer.h',],
        'container_type': 'DataVector<xAOD::Jet_v1>',
        'element_type': 'xAOD::Jet_v1',
        'contains_collection': True,
        'link_libraries': ['xAODJet'],
    },
    'IParticles': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'IParticles',
        'include_files': ['xAODBase/IParticleContainer.h',],
        'container_type': 'DataVector<xAOD::IParticle>',
        'element_type': 'xAOD::IParticle',
        'contains_collection': True,
        'link_libraries': ['xAODBase'],
    },
    'Electrons': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'Electrons',
        'include_files': ['xAODEgamma/ElectronContainer.h',],
        'container_type': 'DataVector<xAOD::Electron_v1>',
        'element_type': 'xAOD::Electron_v1',
        'contains_collection': True,
        'link_libraries': ['xAODEgamma'],
    },
    'Photons': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'Photons',
        'include_files': ['xAODEgamma/PhotonContainer.h',],
        'container_type': 'DataVector<xAOD::Photon_v1>',
        'element_type': 'xAOD::Photon_v1',
        'contains_collection': True,
        'link_libraries': ['xAODEgamma'],
    },
    'Egammas': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'Egammas',
        'include_files': ['xAODEgamma/EgammaContainer.h',],
        'container_type': 'DataVector<xAOD::Egamma_v1>',
        'element_type': 'xAOD::Egamma_v1',
        'contains_collection': True,
        'link_libraries': ['xAODEgamma'],
    },
    'EventInfos': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'EventInfos',
        'include_files': ['xAODEventInfo/EventInfoContainer.h',],
        'container_type': 'DataVector<xAOD::EventInfo_v1>',
        'element_type': 'xAOD::EventInfo_v1',
        'contains_collection': True,
        'link_libraries': ['xAODEventInfo'],
    },
    'NeutralParticles': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'NeutralParticles',
        'include_files': ['xAODTracking/NeutralParticleContainer.h',],
        'container_type': 'DataVector<xAOD::NeutralParticle_v1>',
        'element_type': 'xAOD::NeutralParticle_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTracking'],
    },
    'TrackParticles': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'TrackParticles',
        'include_files': ['xAODTracking/TrackParticleContainer.h',],
        'container_type': 'DataVector<xAOD::TrackParticle_v1>',
        'element_type': 'xAOD::TrackParticle_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTracking'],
    },
    'Vertices': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'Vertices',
        'include_files': ['xAODTracking/VertexContainer.h',],
        'container_type': 'DataVector<xAOD::Vertex_v1>',
        'element_type': 'xAOD::Vertex_v1',
        'contains_collection': True,
        'link_libraries': ['xAODTracking'],
    },
    'EventInfo': {
        'metadata_type': 'add_atlas_event_collection_info',
        'name': 'EventInfo',
        'include_files': ['xAODEventInfo/versions/EventInfo_v1.h',],
        'container_type': 'xAOD::EventInfo_v1',
        'contains_collection': False,
        'link_libraries': ['xAODEventInfo'],
    },
}

_param_metadata : Dict[str, Dict[str, Any]] = {
    'sys_error_tool': {
        'metadata_type':"add_job_script",
        'name':"sys_error_tool",
        'script':[
                "# pulled from:https://gitlab.cern.ch/atlas/athena/-/blob/21.2/PhysicsAnalysis/Algorithms/JetAnalysisAlgorithms/python/JetAnalysisAlgorithmsTest.py ",
                "# Set up the systematics loader/handler service:",
                "from AnaAlgorithm.DualUseConfig import createService",
                "from AnaAlgorithm.AlgSequence import AlgSequence",
                "calibrationAlgSeq = AlgSequence()",
                "sysService = createService( 'CP::SystematicsSvc', 'SystematicsSvc', sequence = calibrationAlgSeq )",
                "sysService.systematicsList = ['{calibration}']",
                "# Add sequence to job",
            ],
    },
    'pileup_tool': {
        'metadata_type':"add_job_script",
        'name':"pileup_tool",
        'script':[
                "from AsgAnalysisAlgorithms.PileupAnalysisSequence import makePileupAnalysisSequence",
                "pileupSequence = makePileupAnalysisSequence( 'mc' )",
                "pileupSequence.configure( inputName = {}, outputName = {} )",
                "print( pileupSequence ) # For debugging",
                "calibrationAlgSeq += pileupSequence",
            ],
        'depends_on':[
                "sys_error_tool",
            ],
    },
    'common_corrections': {
        'metadata_type':"add_job_script",
        'name':"common_corrections",
        'script':[
                "jetContainer = '{calib.jet_collection}'",
                "from JetAnalysisAlgorithms.JetAnalysisSequence import makeJetAnalysisSequence",
                "jetSequence = makeJetAnalysisSequence( 'mc', jetContainer)",
                "jetSequence.configure( inputName = jetContainer, outputName = jetContainer + '_Base_%SYS%' )",
                "jetSequence.JvtEfficiencyAlg.truthJetCollection = '{calib.jet_calib_truth_collection}'",
                "jetSequence.ForwardJvtEfficiencyAlg.truthJetCollection = '{calib.jet_calib_truth_collection}'",
                "calibrationAlgSeq += jetSequence",
                "print( jetSequence ) # For debugging",
                "",
                "# Include, and then set up the jet analysis algorithm sequence:",
                "from JetAnalysisAlgorithms.JetJvtAnalysisSequence import makeJetJvtAnalysisSequence",
                "jvtSequence = makeJetJvtAnalysisSequence( 'mc', jetContainer, enableCutflow=True )",
                "jvtSequence.configure( inputName = {'jets'      : jetContainer + '_Base_%SYS%' },",
                "                       outputName = { 'jets'      : jetContainer + 'Calib_%SYS%' },",
                "                       )",
                "calibrationAlgSeq += jvtSequence",
                "print( jvtSequence ) # For debugging",
                "#",
                "muon_container = '{calib.muon_collection}'",
                "from MuonAnalysisAlgorithms.MuonAnalysisSequence import makeMuonAnalysisSequence",
                "muonSequence = makeMuonAnalysisSequence('mc', workingPoint='{calib.muon_working_point}.{calib.muon_isolation}', postfix = '{calib.muon_working_point}_{calib.muon_isolation}')",
                "muonSequence.configure( inputName = muon_container,",
                "                        outputName = muon_container + 'Calib_{calib.muon_working_point}{calib.muon_isolation}_%SYS%' )",
                "calibrationAlgSeq += muonSequence",
                "print( muonSequence ) # For debugging",
                "#",
                "from EgammaAnalysisAlgorithms.ElectronAnalysisSequence import makeElectronAnalysisSequence",
                "electronSequence = makeElectronAnalysisSequence( 'mc', '{working_point}.{isolation}', postfix = '{working_point}_{isolation}')",
                "electronSequence.configure( inputName = '{calib.electron_collection}',",
                "                            outputName = '{calib.electron_collection}_{working_point}_{isolation}_%SYS%' )",
                "calibrationAlgSeq += electronSequence",
                "print( electronSequence ) # For debugging",
                "#",
                "from EgammaAnalysisAlgorithms.PhotonAnalysisSequence import makePhotonAnalysisSequence",
                "photonSequence = makePhotonAnalysisSequence( 'mc', '{calib.photon_working_point}.{calib.photon_isolation}', postfix = '{calib.photon_working_point}_{calib.photon_isolation}')",
                "photonSequence.configure( inputName = '{calib.photon_collection}',",
                "                            outputName = '{calib.photon_collection}_{calib.photon_working_point}_{calib.photon_isolation}_%SYS%' )",
                "calibrationAlgSeq += photonSequence",
                "print( photonSequence ) # For debugging",
                "#",
                "from TauAnalysisAlgorithms.TauAnalysisSequence import makeTauAnalysisSequence",
                "tauSequence = makeTauAnalysisSequence( 'mc', '{calib.tau_working_point}', postfix = '{calib.tau_working_point}', rerunTruthMatching=False)",
                "tauSequence.configure( inputName = '{calib.tau_collection}',",
                "                       outputName = '{calib.tau_collection}_{calib.tau_working_point}_%SYS%' )",
                "calibrationAlgSeq += tauSequence",
                "print( tauSequence ) # For debugging",
            ],
        'depends_on':[
                "pileup_tool",
            ],
    },
    'ditau_corrections': {
        'metadata_type':"add_job_script",
        'name':"ditau_corrections",
        'script':[
                "from TauAnalysisAlgorithms.DiTauAnalysisSequence import makeDiTauAnalysisSequence",
                "diTauSequence = makeDiTauAnalysisSequence( 'mc', '{working_point}', postfix = '{working_point}')",
                "diTauSequence.configure( inputName = '{bank_name}',",
                "                       outputName = '{bank_name}_{working_point}_%SYS%' )",
                "calibrationAlgSeq += diTauSequence",
                "print( diTauSequence ) # For debugging",
            ],
        'depends_on':[
                "pileup_tool",
            ],
    },
    'add_calibration_to_job': {
        'metadata_type':"add_job_script",
        'name':"add_calibration_to_job",
        'script':[
                "calibrationAlgSeq.addSelfToJob( job )",
                "print(job) # for debugging",
            ],
        'depends_on':[
                "*PREVIOUS*",
            ],
    },
}

PType = TypeVar('PType')


def _get_param(call_ast: ast.Call, arg_index: int, arg_name: str, default_value: PType) -> PType:
    'Fetch the argument from the arg list'
    # Look for it as a positional argument
    if len(call_ast.args) > arg_index:
        return ast.literal_eval(call_ast.args[arg_index])

    # Look for it as a keyword argument
    kw_args = [kwa for kwa in call_ast.keywords if kwa.arg == arg_name]
    if len(kw_args) > 0:
        return ast.literal_eval(kw_args[0].value)
    
    # We can't find it - return the default value.
    return default_value


MDReplType = TypeVar('MDReplType', bound=Union[str, List[str]])



def _replace_md_value(v: MDReplType, p_name: str, new_value: str) -> MDReplType:
    'Replace one MD item'
    if isinstance(v, str):
        return v.replace('{' + p_name + '}', str(new_value))
    else:
        return [x.replace('{' + p_name + '}', str(new_value)) for x in v]


def _replace_param_values(source: MDReplType, param_values: Dict[str, Any]) -> MDReplType:
    'Replace parameter types in a string or list of strings'
    result = source
    for k, v in param_values.items():
        result = _replace_md_value(result, k, v)
    return result


def _resolve_md_params(md: Dict[str, Any], param_values: Dict[str, Any]):
    'Do parameter subst in the metadata'
    for k, v in param_values.items():
        result = {}
        for mk_key, mk_value in md.items():
            new_value = _replace_md_value(mk_value, k, v)
            if new_value != mk_value:
                result[mk_key] = new_value
        if len(result) > 0:
            md = dict(md)
            md.update(result)
            md['name'] = f"{md['name']}_{v}"
    return md

T = TypeVar('T')


def match_param_value(value, to_match) -> bool:
    'Match a parameter with special values'
    if isinstance(to_match, str):
        if to_match == "*None*":
            return value is None
        if to_match == "*Any*":
            return True
    
    return value == to_match


class _process_extra_arguments:
    'Static class that will deal with the extra arguments for each collection'
    @staticmethod
    def process_DiTauJets(bank_name: str, s: ObjectStream[T], a: ast.Call) -> Tuple[str, ObjectStream[T], ast.AST]:
        param_values = {}
        i_param = 0
        i_param += 1
        param_values['calibration'] = _get_param(a, i_param, "calibration", 'NOSYS')
        # assert isinstance(param_values['calibration'], str), f'Parameter calibration must be of type str, not {type(param_values["calibration"])}'
        i_param += 1
        param_values['working_point'] = _get_param(a, i_param, "working_point", 'Tight')
        # assert isinstance(param_values['working_point'], str), f'Parameter working_point must be of type str, not {type(param_values["working_point"])}'
        param_values['bank_name'] = bank_name

        md_name_mapping: Dict[str, str] = {}
        md_list: List[Dict[str, Any]] = []
        p_matched = False
        last_md_name = None
        if not p_matched and match_param_value(param_values['calibration'], '*None*'):
            p_matched = True
            bank_name = _replace_param_values('{bank_name}', param_values)
        if not p_matched and match_param_value(param_values['calibration'], '*Any*'):
            p_matched = True
            old_md = _param_metadata['sys_error_tool']
            md = _resolve_md_params(old_md, param_values)
            if 'depends_on' in md:
                if '*PREVIOUS*' in md['depends_on']:
                    md = dict(md)
                    md['depends_on'] = [x for x in md['depends_on'] if x != '*PREVIOUS*']
                    if last_md_name is not None:
                        md['depends_on'].append(last_md_name)
            last_md_name = md['name']
            md_list.append(md)
            md_name_mapping[old_md['name']] = md['name']
            old_md = _param_metadata['pileup_tool']
            md = _resolve_md_params(old_md, param_values)
            if 'depends_on' in md:
                if '*PREVIOUS*' in md['depends_on']:
                    md = dict(md)
                    md['depends_on'] = [x for x in md['depends_on'] if x != '*PREVIOUS*']
                    if last_md_name is not None:
                        md['depends_on'].append(last_md_name)
            last_md_name = md['name']
            md_list.append(md)
            md_name_mapping[old_md['name']] = md['name']
            old_md = _param_metadata['ditau_corrections']
            md = _resolve_md_params(old_md, param_values)
            if 'depends_on' in md:
                if '*PREVIOUS*' in md['depends_on']:
                    md = dict(md)
                    md['depends_on'] = [x for x in md['depends_on'] if x != '*PREVIOUS*']
                    if last_md_name is not None:
                        md['depends_on'].append(last_md_name)
            last_md_name = md['name']
            md_list.append(md)
            md_name_mapping[old_md['name']] = md['name']
            old_md = _param_metadata['add_calibration_to_job']
            md = _resolve_md_params(old_md, param_values)
            if 'depends_on' in md:
                if '*PREVIOUS*' in md['depends_on']:
                    md = dict(md)
                    md['depends_on'] = [x for x in md['depends_on'] if x != '*PREVIOUS*']
                    if last_md_name is not None:
                        md['depends_on'].append(last_md_name)
            last_md_name = md['name']
            md_list.append(md)
            md_name_mapping[old_md['name']] = md['name']
            bank_name = _replace_param_values('{bank_name}_{working_point}_{calibration}', param_values)
        p_matched = False
        last_md_name = None

        for md in md_list:
            if 'depends_on' in md:
                md = dict(md) # Make a copy so we don't mess up downstream queries
                md['depends_on'] = [(md_name_mapping[x] if x in md_name_mapping else x) for x in md['depends_on']]
            s = s.MetaData(md)

        return bank_name, s, a


def _add_collection_metadata(s: ObjectStream[T], a: ast.Call) -> Tuple[ObjectStream[T], ast.Call]:
    '''Add metadata for a collection to the func_adl stream if we know about it
    '''
    # Unpack the call as needed
    assert isinstance(a.func, ast.Attribute)
    collection_name = a.func.attr
    # collection_bank = ast.literal_eval(a.args[0])

    # # If it has extra arguments, we need to process those.
    # arg_processor = getattr(_process_extra_arguments, f'process_{collection_name}', None)
    # if arg_processor is not None:
    #     new_a = copy.deepcopy(a)
    #     new_bank, s, a = arg_processor(collection_bank, s, new_a)
    #     a.args = [ast.Constant(new_bank)]


    # Finally, add the collection defining metadata so the backend
    # knows about this collection and how to access it.
    if collection_name in _collection_map:
        s_update = s.MetaData(_collection_map[collection_name])
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_collection_metadata)
class Event:
    '''The top level event class. All data in the event is accessed from here
    '''



    def SlowMuons(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.slowmuon_v1.SlowMuon_v1]:
        ...

    def MuonSegments(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.muonsegment_v1.MuonSegment_v1]:
        ...

    @func_adl_callback(lambda s, a: func_adl_servicex_xaodr21.calibration_support.fixup_collection_call(s, a, 'muon_collection'))
    def Muons(self, calibrated_collection: Optional[str] = None, uncalibrated_collection: Optional[str] = None) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.muon_v1.Muon_v1]:
        ...

    @func_adl_callback(lambda s, a: func_adl_servicex_xaodr21.calibration_support.fixup_collection_call(s, a, 'tau_collection'))
    def TauJets(self, calibrated_collection: Optional[str] = None, uncalibrated_collection: Optional[str] = None) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.taujet_v3.TauJet_v3]:
        ...

    def TauTracks(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.tautrack_v1.TauTrack_v1]:
        ...

    def DiTauJets(self, calibration: str = 'NOSYS', working_point: str = 'Tight') -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.ditaujet_v1.DiTauJet_v1]:
        ...

    def CaloClusters(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.calocluster_v1.CaloCluster_v1]:
        ...

    def CaloTowers(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.calotower_v1.CaloTower_v1]:
        ...

    def TrackCaloClusters(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.trackcalocluster_v1.TrackCaloCluster_v1]:
        ...

    def PFOs(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1]:
        ...

    def TruthMetaDatas(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.truthmetadata_v1.TruthMetaData_v1]:
        ...

    def TruthParticles(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.truthparticle_v1.TruthParticle_v1]:
        ...

    def TruthVertices(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.truthvertex_v1.TruthVertex_v1]:
        ...

    def TruthEvents(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.truthevent_v1.TruthEvent_v1]:
        ...

    def BTagVertices(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.btagvertex_v1.BTagVertex_v1]:
        ...

    def BTaggings(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.btagging_v1.BTagging_v1]:
        ...

    @func_adl_callback(lambda s, a: func_adl_servicex_xaodr21.calibration_support.fixup_collection_call(s, a, 'met_collection'))
    def MissingET(self, calibrated_collection: Optional[str] = None, uncalibrated_collection: Optional[str] = None) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.missinget_v1.MissingET_v1]:
        ...

    @func_adl_callback(lambda s, a: func_adl_servicex_xaodr21.calibration_support.fixup_collection_call(s, a, 'jet_collection'))
    def Jets(self, calibrated_collection: Optional[str] = None, uncalibrated_collection: Optional[str] = None) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.jet_v1.Jet_v1]:
        ...

    def IParticles(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.iparticle.IParticle]:
        ...

    @func_adl_callback(lambda s, a: func_adl_servicex_xaodr21.calibration_support.fixup_collection_call(s, a, 'electron_collection'))
    def Electrons(self, calibrated_collection: Optional[str] = None, uncalibrated_collection: Optional[str] = None) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.electron_v1.Electron_v1]:
        ...

    @func_adl_callback(lambda s, a: func_adl_servicex_xaodr21.calibration_support.fixup_collection_call(s, a, 'photon_collection'))
    def Photons(self, calibrated_collection: Optional[str] = None, uncalibrated_collection: Optional[str] = None) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.photon_v1.Photon_v1]:
        ...

    def Egammas(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.egamma_v1.Egamma_v1]:
        ...

    def EventInfos(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.eventinfo_v1.EventInfo_v1]:
        ...

    def NeutralParticles(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.neutralparticle_v1.NeutralParticle_v1]:
        ...

    def TrackParticles(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.trackparticle_v1.TrackParticle_v1]:
        ...

    def Vertices(self, name: str) -> func_adl_servicex_xaodr21.FADLStream[func_adl_servicex_xaodr21.xAOD.vertex_v1.Vertex_v1]:
        ...

    def EventInfo(self, name: str) -> func_adl_servicex_xaodr21.xAOD.eventinfo_v1.EventInfo_v1:
        ...
